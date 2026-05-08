#!/usr/bin/env python3
"""Reconcile App Store Connect screenshot order with a local store.config.json.

Generic helper. It does not assume any particular project. It reads desired
order from ``store.config.json`` (the same file consumed by EAS CLI) and
reconciles it directly against the App Store Connect API using a private-key
JWT.

Use this when ``eas metadata:push`` reports success but the App Store Connect
dashboard still shows screenshots in a different order than the local config —
e.g. when EAS CLI skipped the screenshot phase because every (filename +
filesize) already matched and the reorder step was therefore not invoked,
leaving stale order from earlier transient failures.

Modes
-----
``--check``  Read-only. Print drift report and exit non-zero if drift exists.
``--fix``    PATCH the App Store Connect screenshot sets so live order matches
             the local config.

Authentication
--------------
Resolves ASC API credentials in this order:

1. ``--asc-api-key-id`` / ``--asc-api-issuer-id`` / ``--asc-api-key-path`` flags
2. ``ASC_API_KEY_ID`` / ``ASC_API_ISSUER_ID`` / ``ASC_API_KEY_PATH`` env vars
3. ``submit.<eas-profile>.ios`` block in ``./eas.json`` (env-backed values like
   ``"$ASC_API_KEY_PATH"`` are expanded)

The ``--app-id`` flag falls back to ``submit.<eas-profile>.ios.ascAppId`` in
``eas.json``.

Dependencies
------------
``cryptography`` (for ES256 JWT signing). Standard library only otherwise.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

try:
    from cryptography.hazmat.primitives.asymmetric.ec import ECDSA
    from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
    from cryptography.hazmat.primitives.hashes import SHA256
    from cryptography.hazmat.primitives.serialization import load_pem_private_key
except ImportError:
    sys.stderr.write(
        "ERROR: This script requires the 'cryptography' package for ES256 JWT "
        "signing.\nInstall with: pip3 install cryptography\n"
    )
    sys.exit(2)


ASC_BASE = "https://api.appstoreconnect.apple.com"

# App Store states where metadata (including screenshot order) is editable.
# Apps in READY_FOR_SALE / REMOVED_FROM_SALE / PROCESSING_FOR_DISTRIBUTION etc.
# do not allow PATCH on screenshot relationships.
EDITABLE_STATES = [
    "PREPARE_FOR_SUBMISSION",
    "WAITING_FOR_REVIEW",
    "IN_REVIEW",
    "DEVELOPER_REJECTED",
    "REJECTED",
    "METADATA_REJECTED",
    "READY_FOR_REVIEW",
    "PENDING_DEVELOPER_RELEASE",
]


# ---------- JWT ----------------------------------------------------------------


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def make_token(key_id: str, issuer_id: str, key_path: Path, ttl_seconds: int = 1200) -> str:
    """Sign an ES256 JWT for App Store Connect API."""
    pem = key_path.read_bytes()
    priv = load_pem_private_key(pem, password=None)
    header = {"alg": "ES256", "kid": key_id, "typ": "JWT"}
    now = int(time.time())
    payload = {
        "iss": issuer_id,
        "iat": now,
        "exp": now + ttl_seconds,
        "aud": "appstoreconnect-v1",
    }
    signing_input = (
        _b64url(json.dumps(header, separators=(",", ":")).encode())
        + "."
        + _b64url(json.dumps(payload, separators=(",", ":")).encode())
    ).encode("ascii")
    der_sig = priv.sign(signing_input, ECDSA(SHA256()))
    r, s = decode_dss_signature(der_sig)
    raw_sig = r.to_bytes(32, "big") + s.to_bytes(32, "big")
    return signing_input.decode() + "." + _b64url(raw_sig)


# ---------- HTTP --------------------------------------------------------------


class ASCClient:
    def __init__(self, token: str, verbose: bool = False, sleep_between: float = 0.0):
        self.token = token
        self.verbose = verbose
        self.sleep_between = sleep_between

    def _req(self, method: str, url: str, body: Any | None = None) -> dict | None:
        if not url.startswith("http"):
            url = ASC_BASE + url
        data = None
        headers = {"Authorization": f"Bearer {self.token}"}
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        if self.verbose:
            sys.stderr.write(f"  {method} {url}\n")
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read()
                if self.sleep_between:
                    time.sleep(self.sleep_between)
                if not raw:
                    return None
                return json.loads(raw)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            sys.stderr.write(f"  HTTP {e.code} {method} {url}\n  body: {err_body}\n")
            raise

    def get(self, path: str) -> dict:
        return self._req("GET", path) or {}

    def get_paginated(self, path: str) -> list[dict]:
        results: list[dict] = []
        url = path
        while True:
            payload = self._req("GET", url)
            if not payload:
                break
            results.extend(payload.get("data", []))
            url = payload.get("links", {}).get("next")
            if not url:
                break
        return results

    def patch(self, path: str, body: dict) -> None:
        self._req("PATCH", path, body=body)


# ---------- Config + creds ----------------------------------------------------


def load_eas_json(repo_root: Path) -> dict | None:
    p = repo_root / "eas.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        return None


def _expand_env(value: Any) -> Any:
    if isinstance(value, str) and value.startswith("$"):
        return os.environ.get(value[1:])
    return value


def resolve_credentials(args: argparse.Namespace) -> tuple[str, str, Path, str]:
    """Return ``(key_id, issuer_id, key_path, app_id)``."""
    key_id = args.asc_api_key_id or os.environ.get("ASC_API_KEY_ID")
    issuer_id = args.asc_api_issuer_id or os.environ.get("ASC_API_ISSUER_ID")
    key_path = args.asc_api_key_path or os.environ.get("ASC_API_KEY_PATH")
    app_id = args.app_id

    if not (key_id and issuer_id and key_path and app_id):
        eas = load_eas_json(args.repo_root)
        if eas:
            ios = (
                eas.get("submit", {})
                .get(args.eas_profile, {})
                .get("ios", {})
            )
            key_id = key_id or _expand_env(ios.get("ascApiKeyId"))
            issuer_id = issuer_id or _expand_env(ios.get("ascApiKeyIssuerId"))
            key_path = key_path or _expand_env(ios.get("ascApiKeyPath"))
            app_id = app_id or _expand_env(ios.get("ascAppId"))

    missing: list[str] = []
    if not key_id:
        missing.append("ASC_API_KEY_ID / --asc-api-key-id")
    if not issuer_id:
        missing.append("ASC_API_ISSUER_ID / --asc-api-issuer-id")
    if not key_path:
        missing.append("ASC_API_KEY_PATH / --asc-api-key-path")
    if not app_id:
        missing.append("--app-id (or eas.json submit.<profile>.ios.ascAppId)")
    if missing:
        sys.stderr.write("ERROR: missing credentials: " + ", ".join(missing) + "\n")
        sys.exit(2)

    p = Path(str(key_path)).expanduser()
    if not p.exists():
        sys.stderr.write(f"ERROR: ASC API key file not found: {p}\n")
        sys.exit(2)
    return str(key_id), str(issuer_id), p, str(app_id)


def desired_order_from_config(config_path: Path) -> dict[str, dict[str, list[str]]]:
    """Return ``{locale: {displayType: [basename, ...]}}`` from the apple info section."""
    config = json.loads(config_path.read_text())
    out: dict[str, dict[str, list[str]]] = {}
    info = config.get("apple", {}).get("info", {}) or {}
    for locale, locale_info in info.items():
        ss_map = locale_info.get("screenshots") or {}
        if not ss_map:
            continue
        out.setdefault(locale, {})
        for display_type, paths in ss_map.items():
            out[locale][display_type] = [os.path.basename(p) for p in paths]
    return out


# ---------- Discovery ---------------------------------------------------------


def _version_key(v: dict) -> tuple[int, ...]:
    """Sort key for App Store versions; later versions sort larger."""
    raw = (v.get("attributes") or {}).get("versionString") or ""
    parts: list[int] = []
    for token in raw.split("."):
        try:
            parts.append(int(token))
        except ValueError:
            parts.append(0)
    return tuple(parts) or (0,)


def find_editable_version(client: ASCClient, app_id: str, platform: str) -> dict:
    states_filter = ",".join(EDITABLE_STATES)
    qs = (
        f"filter[platform]={platform}"
        f"&filter[appStoreState]={urllib.parse.quote(states_filter, safe=',')}"
        f"&limit=20"
    )
    versions = client.get_paginated(f"/v1/apps/{app_id}/appStoreVersions?{qs}")
    if not versions:
        sys.stderr.write(
            f"ERROR: No editable App Store version found for app {app_id} on {platform}.\n"
            f"Editable states checked: {states_filter}\n"
        )
        sys.exit(3)
    versions.sort(key=_version_key, reverse=True)
    if len(versions) > 1:
        sys.stderr.write(f"NOTE: {len(versions)} editable versions found. Using the latest:\n")
        for v in versions[:5]:
            sys.stderr.write(
                f"  {v['attributes'].get('versionString')} "
                f"({v['attributes'].get('appStoreState')})  id={v['id']}\n"
            )
    return versions[0]


# ---------- Main --------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Read-only drift report.")
    mode.add_argument("--fix", action="store_true", help="PATCH ASC to match local order.")
    ap.add_argument(
        "--config",
        default="store.config.json",
        type=Path,
        help="Path to store.config.json (default: ./store.config.json).",
    )
    ap.add_argument(
        "--repo-root",
        default=Path("."),
        type=Path,
        help="Repo root used to locate eas.json (default: cwd).",
    )
    ap.add_argument(
        "--eas-profile",
        default="production",
        help="EAS submit profile name to read fallback creds from (default: production).",
    )
    ap.add_argument("--app-id", help="App Store Connect numeric app ID.")
    ap.add_argument(
        "--platform",
        default="IOS",
        choices=["IOS", "MAC_OS", "TV_OS", "VISION_OS"],
    )
    ap.add_argument("--asc-api-key-id")
    ap.add_argument("--asc-api-issuer-id")
    ap.add_argument("--asc-api-key-path")
    ap.add_argument(
        "--locale",
        action="append",
        help="Filter to a specific locale (repeatable).",
    )
    ap.add_argument(
        "--display-type",
        action="append",
        help="Filter to a specific screenshotDisplayType (repeatable).",
    )
    ap.add_argument(
        "--sleep",
        type=float,
        default=0.0,
        help="Seconds to sleep between API calls to avoid rate limits.",
    )
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    config_path: Path = args.config
    if not config_path.exists():
        sys.stderr.write(f"ERROR: config not found: {config_path}\n")
        return 2

    desired = desired_order_from_config(config_path)
    if args.locale:
        keep = set(args.locale)
        desired = {k: v for k, v in desired.items() if k in keep}
    if args.display_type:
        keep_dt = set(args.display_type)
        desired = {
            k: {dt: v for dt, v in inner.items() if dt in keep_dt}
            for k, inner in desired.items()
        }

    key_id, issuer_id, key_path, app_id = resolve_credentials(args)
    token = make_token(key_id, issuer_id, key_path)
    client = ASCClient(token, verbose=args.verbose, sleep_between=args.sleep)

    sys.stderr.write(f"App {app_id} ({args.platform}). Looking up editable version...\n")
    version = find_editable_version(client, app_id, args.platform)
    version_id = version["id"]
    version_attrs = version["attributes"]
    sys.stderr.write(
        f"Using App Store version {version_attrs.get('versionString')} "
        f"({version_attrs.get('appStoreState')}) id={version_id}\n"
    )

    sys.stderr.write("Loading localizations...\n")
    localizations = client.get_paginated(
        f"/v1/appStoreVersions/{version_id}/appStoreVersionLocalizations?limit=200"
    )
    by_locale: dict[str, str] = {
        loc["attributes"]["locale"]: loc["id"] for loc in localizations
    }
    sys.stderr.write(f"  found {len(by_locale)} localizations on ASC\n")

    drift_count = 0
    fixed_count = 0
    set_mismatch = 0
    skipped_missing = 0

    for locale, by_display in sorted(desired.items()):
        loc_id = by_locale.get(locale)
        if not loc_id:
            sys.stderr.write(f"WARN: locale {locale} not present on ASC; skipping\n")
            skipped_missing += 1
            continue

        sets = client.get_paginated(
            f"/v1/appStoreVersionLocalizations/{loc_id}/appScreenshotSets?limit=50"
        )
        sets_by_dt = {s["attributes"]["screenshotDisplayType"]: s for s in sets}

        for dt, desired_basenames in by_display.items():
            ss_set = sets_by_dt.get(dt)
            if not ss_set:
                sys.stderr.write(f"WARN: {locale}/{dt}: no ASC screenshotSet; skipping\n")
                skipped_missing += 1
                continue
            set_id = ss_set["id"]

            current = client.get_paginated(
                f"/v1/appScreenshotSets/{set_id}/appScreenshots"
                f"?limit=200&fields[appScreenshots]=fileName"
            )
            current_ids = [s["id"] for s in current]
            current_names = [s["attributes"]["fileName"] for s in current]
            name_to_id: dict[str, str] = dict(zip(current_names, current_ids))

            if sorted(current_names) != sorted(desired_basenames):
                sys.stderr.write(
                    f"DRIFT (set mismatch) {locale}/{dt}:\n"
                    f"  ASC:    {current_names}\n"
                    f"  config: {desired_basenames}\n"
                )
                set_mismatch += 1
                continue

            ordered_ids = [name_to_id[n] for n in desired_basenames]
            if ordered_ids == current_ids:
                if args.verbose:
                    sys.stderr.write(f"  ok   {locale}/{dt}\n")
                continue

            first = next(
                (i for i, (a, b) in enumerate(zip(current_ids, ordered_ids)) if a != b),
                None,
            )
            drift_count += 1
            sys.stderr.write(
                f"DRIFT {locale}/{dt}: first mismatch at index {first}\n"
                f"  ASC:    {current_names}\n"
                f"  config: {desired_basenames}\n"
            )

            if args.fix:
                body = {
                    "data": [{"type": "appScreenshots", "id": sid} for sid in ordered_ids]
                }
                client.patch(
                    f"/v1/appScreenshotSets/{set_id}/relationships/appScreenshots",
                    body,
                )
                fixed_count += 1
                sys.stderr.write(f"  -> reordered {locale}/{dt}\n")

    sys.stderr.write(
        f"\nsummary: drift={drift_count} fixed={fixed_count} "
        f"set_mismatch={set_mismatch} skipped_missing={skipped_missing}\n"
    )
    if (drift_count + set_mismatch) and not args.fix:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
