#!/usr/bin/env python3
"""Reference template: manifest-driven simulator screenshot capture.

This script is a STARTING POINT. Copy it into a project's own scripts
directory and adapt the navigation registry, device list, screenshot
mode launch flag, and slide schema to the project's app.

What it provides:
- preflight checks for xcrun and idb
- device matrix with per-device UDIDs
- locale loop with launch-argument-driven locale switching
- appearance + status bar + permission stabilization before each capture
- accessibility-first navigation via `idb ui describe-all`
- proof mode (one locale x one device x a subset of screens) and batch
  mode (full matrix), driven by `capture-manifest.yaml`
- per-device parallel workers in batch mode

What it deliberately does NOT do:
- it does not know your app's screens
- it does not know your app's accessibility identifiers
- it does not know your app's screenshot-mode launch flag

Wire those in via the SCREENS registry below and the launch-args list in
`launch_app`.

Requirements:
- Xcode + Xcode command-line tools (`xcrun simctl`)
- idb_companion + fb-idb (`brew install idb-companion && pip install fb-idb`)
- Pillow + PyYAML (`python3 -m pip install Pillow PyYAML`)
- the app already installed on the target simulator(s)

Usage:
    python3 scripts/capture-screenshots.py --proof
    python3 scripts/capture-screenshots.py --proof --locale ja --device iphone
    python3 scripts/capture-screenshots.py --batch
    python3 scripts/capture-screenshots.py --batch --locale ja
    python3 scripts/capture-screenshots.py --batch --screen home
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError as exc:
    raise SystemExit(
        "PyYAML is required. Install it with: python3 -m pip install PyYAML"
    ) from exc


# ---------- Project-specific configuration (edit this block) ----------

# The bundle identifier of the app under capture.
BUNDLE_ID = "com.example.YourApp"

# Project-owned screenshot-mode launch arguments. Keep this list minimal
# and stable; passing more flags than necessary makes simulator state
# harder to reason about.
SCREENSHOT_MODE_LAUNCH_ARGS = [
    "-UseScreenshotSampleData",
    "-ScreenshotSeed", "default",
]

# Devices the capture matrix targets. Replace UDIDs with the simulators
# the project uses, or list them with `xcrun simctl list devices booted`.
DEVICES: dict[str, "Device"] = {}


@dataclass
class Device:
    key: str            # "iphone" | "ipad"
    folder: str         # output subdirectory name
    udid: str           # simulator UDID
    width: int
    height: int


def configure_devices() -> None:
    DEVICES["iphone"] = Device(
        key="iphone",
        folder="iphone",
        udid="REPLACE_WITH_IPHONE_UDID",
        width=402,
        height=874,
    )
    DEVICES["ipad"] = Device(
        key="ipad",
        folder="ipad",
        udid="REPLACE_WITH_IPAD_UDID",
        width=834,
        height=1194,
    )


# Map ISO-style locale codes to AppleLocale values when they differ.
# Extend or override per project.
APPLE_LOCALE_OVERRIDES = {
    "en-US": "en_US",
    "zh-Hans": "zh_Hans_CN",
    "zh-Hant": "zh_Hant_TW",
    "pt-BR": "pt_BR",
}


# Navigation hooks. One entry per screen id used in the manifest.
# Each hook receives (udid, screen_meta) and is expected to leave the
# requested screen on-screen and stable. Add hooks here as the project
# adds screens to its capture manifest.
NAVIGATION_REGISTRY: dict[str, "Callable[[str, dict], None]"] = {}


def register_screen(screen_id: str):
    def decorator(fn):
        NAVIGATION_REGISTRY[screen_id] = fn
        return fn
    return decorator


@register_screen("home")
def navigate_home(udid: str, meta: dict) -> None:
    # The app boots on home in screenshot mode; nothing to do.
    wait_for_app(udid)


# Add more @register_screen("...") hooks here as the project expands the
# capture manifest. Keep each hook small and read its required AXUniqueId
# values from `meta` rather than hardcoding them in the function body.


# ---------- Generic helpers (edit only when the contract changes) ----------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "app-store-assets" / "raw"
DEFAULT_MANIFEST = PROJECT_ROOT / "capture-manifest.yaml"


def run(cmd: list[str], *, check: bool = True, capture: bool = True, timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, capture_output=capture, text=True, timeout=timeout)


def preflight() -> None:
    if shutil.which("xcrun") is None:
        raise SystemExit(
            "xcrun is missing. Install Xcode or the Xcode command-line tools "
            "(e.g. `xcode-select --install`)."
        )
    if shutil.which("idb") is None:
        raise SystemExit(
            "idb is missing. Install with `brew install idb-companion && "
            "python3 -m pip install fb-idb`."
        )


def boot_device(device: Device) -> None:
    run(["xcrun", "simctl", "boot", device.udid], check=False)
    run(["xcrun", "simctl", "bootstatus", device.udid, "-b"], check=False, timeout=120)
    run(["idb", "connect", device.udid], check=False)


def stabilize(udid: str, *, appearance: str = "light") -> None:
    run(["xcrun", "simctl", "ui", udid, "appearance", appearance], check=False)
    run([
        "xcrun", "simctl", "status_bar", udid, "override",
        "--dataNetwork", "wifi",
        "--wifiMode", "active",
        "--wifiBars", "3",
        "--cellularMode", "notSupported",
        "--batteryState", "charged",
        "--batteryLevel", "100",
    ], check=False)
    # Pre-grant permissions the app would otherwise prompt for mid-capture.
    for service in ("location",):
        run(["xcrun", "simctl", "privacy", udid, "grant", service, BUNDLE_ID], check=False)


def launch_app(udid: str, locale: str) -> None:
    run(["xcrun", "simctl", "terminate", udid, BUNDLE_ID], check=False)
    apple_locale = APPLE_LOCALE_OVERRIDES.get(locale, locale.replace("-", "_"))
    args = [
        "xcrun", "simctl", "launch", "--terminate-running-process",
        udid, BUNDLE_ID,
        *SCREENSHOT_MODE_LAUNCH_ARGS,
        "-AppleLanguages", f"({locale})",
        "-AppleLocale", apple_locale,
    ]
    run(args)
    time.sleep(2)


def describe_ui(udid: str) -> list[dict]:
    result = run(["idb", "ui", "describe-all", "--udid", udid, "--json"], timeout=60)
    return json.loads(result.stdout)


def find_node(tree: list[dict], *, uid: str | None = None, label: str | None = None) -> dict | None:
    for node in tree:
        if uid is not None and node.get("AXUniqueId") == uid:
            return node
        if label is not None and node.get("AXLabel") == label:
            return node
    return None


def wait_for_uid(udid: str, uid: str, timeout: float = 8.0) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        tree = describe_ui(udid)
        node = find_node(tree, uid=uid)
        if node is not None:
            return node
        time.sleep(0.3)
    raise RuntimeError(f"Timed out waiting for AXUniqueId={uid!r}")


def wait_for_app(udid: str, timeout: float = 8.0) -> None:
    wait_for_uid(udid, "app.root", timeout=timeout)


def tap_uid(udid: str, uid: str) -> None:
    node = wait_for_uid(udid, uid)
    frame = node["frame"]
    cx = int(frame["x"] + frame["width"] / 2)
    cy = int(frame["y"] + frame["height"] / 2)
    run(["idb", "ui", "tap", "--udid", udid, str(cx), str(cy)])


def navigate(udid: str, screen_id: str, meta: dict) -> None:
    hook = NAVIGATION_REGISTRY.get(screen_id)
    if hook is None:
        # Fallback: interpret a small declarative `steps` list from the
        # manifest. Each step is one of:
        #   { tap_uid: <id> }
        #   { wait_for_uid: <id> }
        steps = meta.get("navigation", {}).get("steps") or []
        for step in steps:
            if "tap_uid" in step:
                tap_uid(udid, step["tap_uid"])
            elif "wait_for_uid" in step:
                wait_for_uid(udid, step["wait_for_uid"])
            else:
                raise RuntimeError(f"Unsupported navigation step: {step!r}")
        return
    hook(udid, meta)


def capture(udid: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    run(["xcrun", "simctl", "io", udid, "screenshot", str(output)])


# ---------- Driver ----------

def load_manifest(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def build_runs(manifest: dict, *, mode: str, locale_override: str | None,
               device_override: str | None, screen_override: str | None) -> list[tuple[str, str, dict]]:
    block = manifest[mode]
    locales = [locale_override] if locale_override else block["locales" if mode == "batch" else "locale"]
    if isinstance(locales, str):
        locales = [locales]
    devices = [device_override] if device_override else block["devices"]
    screen_ids = [screen_override] if screen_override else (
        block.get("screens") or [s["id"] for s in manifest["screens"]]
    )
    screens_by_id = {s["id"]: s for s in manifest["screens"]}
    runs: list[tuple[str, str, dict]] = []
    for device in devices:
        for locale in locales:
            for screen_id in screen_ids:
                meta = screens_by_id[screen_id]
                runs.append((device, locale, meta))
    return runs


def run_one(device_key: str, locale: str, meta: dict, output_root: Path) -> str:
    device = DEVICES[device_key]
    boot_device(device)
    for appearance in meta.get("appearances", ["light"]):
        stabilize(device.udid, appearance=appearance)
        launch_app(device.udid, locale)
        navigate(device.udid, meta["id"], meta)
        out_path = output_root / device.folder / locale / meta["filename"]
        capture(device.udid, out_path)
    return f"{device_key}/{locale}/{meta['filename']}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Manifest-driven simulator screenshot capture.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--proof", action="store_true")
    mode.add_argument("--batch", action="store_true")
    parser.add_argument("--locale")
    parser.add_argument("--device", choices=list(DEVICES.keys()) or None)
    parser.add_argument("--screen")
    parser.add_argument("--workers", type=int, default=2,
                        help="Parallel device workers in batch mode.")
    args = parser.parse_args()

    configure_devices()
    preflight()

    manifest = load_manifest(args.manifest)
    runs = build_runs(
        manifest,
        mode="proof" if args.proof else "batch",
        locale_override=args.locale,
        device_override=args.device,
        screen_override=args.screen,
    )
    if not runs:
        print("No runs to execute. Check manifest filters.", file=sys.stderr)
        return 1

    if args.proof or args.workers <= 1:
        for device_key, locale, meta in runs:
            print(run_one(device_key, locale, meta, args.output_root))
        return 0

    # Parallelize per device key to keep simulators isolated.
    by_device: dict[str, list[tuple[str, str, dict]]] = {}
    for r in runs:
        by_device.setdefault(r[0], []).append(r)

    failures: list[str] = []
    with ProcessPoolExecutor(max_workers=min(args.workers, len(by_device))) as pool:
        futures = {
            pool.submit(_run_device_serial, device_key, runs_for_device, args.output_root): device_key
            for device_key, runs_for_device in by_device.items()
        }
        for fut in as_completed(futures):
            device_key = futures[fut]
            try:
                fut.result()
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{device_key}: {exc}")
    if failures:
        for f in failures:
            print(f"FAIL {f}", file=sys.stderr)
        return 2
    return 0


def _run_device_serial(device_key: str, runs: list[tuple[str, str, dict]], output_root: Path) -> None:
    for d, locale, meta in runs:
        run_one(d, locale, meta, output_root)


if __name__ == "__main__":
    sys.exit(main())
