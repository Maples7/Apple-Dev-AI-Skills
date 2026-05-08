#!/usr/bin/env python3
"""Reference template: rebuild the screenshot path arrays in
`store.config.json` from filesystem state.

Why this exists
---------------
Once raw captures (or final composed exports) settle on a stable
filesystem layout, regenerating the metadata config from the disk is
much safer than hand-editing arrays. The numeric prefix in each filename
encodes display order, so a deterministic walk produces a deterministic
config.

Assumed filesystem layout:

    <root>/<locale>/<deviceFolder>/<NN>-<screenId>-<W>x<H>.png

Example (matches `store.config.json` references in many EAS-managed
Apple metadata projects):

    store/apple/screenshot/en-US/APP_IPHONE_67/01-home-1290x2796.png
    store/apple/screenshot/en-US/APP_IPHONE_67/02-report-1290x2796.png

This script walks every `<locale>/<deviceFolder>/` cell, sorts the PNGs
by numeric prefix, and replaces the relative-path array under
`apple.info[<locale>].screenshots[<deviceFolder>]` in the config file.

It does NOT introduce new locales, new device folders, or new screens.
That is by design: the config keeps its existing structure, only the
ordered file lists change.

Requirements:
    none beyond the standard library.

Usage:
    python3 scripts/sync-store-config-screenshots.py
    python3 scripts/sync-store-config-screenshots.py --config store.config.json --root store/apple/screenshot
    python3 scripts/sync-store-config-screenshots.py --check       # exit 1 if drift detected
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PATH_PATTERN = re.compile(
    r"^(?P<index>\d{2})-(?P<slug>[^-]+(?:-[^-]+)*?)-(?P<size>\d+x\d+)\.png$"
)


def collect_paths(cell_dir: Path) -> list[str]:
    """Return relative-from-root file names sorted by their numeric prefix."""
    files = []
    for entry in cell_dir.iterdir():
        if not entry.is_file():
            continue
        match = PATH_PATTERN.match(entry.name)
        if not match:
            continue
        files.append((int(match.group("index")), entry.name))
    files.sort(key=lambda x: x[0])
    return [name for _, name in files]


def rebuild(config_path: Path, root: Path, *, check_only: bool) -> int:
    data = json.loads(config_path.read_text(encoding="utf-8"))
    apple_info = data.get("apple", {}).get("info") or {}
    if not apple_info:
        raise SystemExit("Config has no apple.info block; nothing to do.")

    drift_detected = False
    rewritten_cells = 0

    for locale, payload in apple_info.items():
        screenshots = payload.get("screenshots") or {}
        if not screenshots:
            continue
        for device_folder, current_paths in list(screenshots.items()):
            cell_dir = root / locale / device_folder
            if not cell_dir.is_dir():
                continue
            file_names = collect_paths(cell_dir)
            new_paths = [
                str(Path(root.name) / locale / device_folder / name)
                for name in file_names
            ]
            # Walk relative from the config-root convention used in the
            # existing array, so the rewrite produces matching strings.
            existing_root_prefix = _detect_root_prefix(current_paths) or root
            new_paths = [
                f"{existing_root_prefix}/{locale}/{device_folder}/{name}"
                for name in file_names
            ]
            if list(current_paths) == new_paths:
                continue
            drift_detected = True
            if not check_only:
                screenshots[device_folder] = new_paths
                rewritten_cells += 1

    if check_only:
        if drift_detected:
            print("Drift detected. Run without --check to rewrite the config.", file=sys.stderr)
            return 1
        print("No drift between filesystem and config.")
        return 0

    if rewritten_cells == 0:
        print("No drift between filesystem and config; nothing rewritten.")
        return 0

    config_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Rewrote {rewritten_cells} (locale x device) cells in {config_path}.")
    return 0


def _detect_root_prefix(paths: list[str]) -> str | None:
    """Return the leading directory portion of an existing array, e.g.
    `store/apple/screenshot`, so the rewrite preserves it.
    """
    if not paths:
        return None
    head = paths[0]
    parts = head.split("/")
    # Expected shape: <root>/.../<locale>/<deviceFolder>/<file>.png
    # Drop the last three components (locale, deviceFolder, file).
    if len(parts) < 4:
        return None
    return "/".join(parts[:-3])


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync store config screenshot arrays from filesystem state.")
    parser.add_argument("--config", type=Path, default=Path("store.config.json"))
    parser.add_argument("--root", type=Path, default=Path("store/apple/screenshot"))
    parser.add_argument("--check", action="store_true",
                        help="Exit 1 if filesystem state differs from config; do not rewrite.")
    args = parser.parse_args()

    if not args.config.is_file():
        parser.error(f"Config file not found: {args.config}")
    if not args.root.is_dir():
        parser.error(f"Screenshot root not found: {args.root}")

    return rebuild(args.config, args.root, check_only=args.check)


if __name__ == "__main__":
    sys.exit(main())
