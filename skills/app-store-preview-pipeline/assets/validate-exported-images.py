#!/usr/bin/env python3
"""Validate exported App Store screenshot files for dimensions and opacity.

Copy this script into a project's own scripts directory and adapt the
allowed sizes to the current App Store Connect export plan.

Requirements:
    python3 -m pip install Pillow

Example:
    python3 scripts/validate_exported_images.py \
        --root app-store-export \
        --allowed-size 1320x2868 \
        --allowed-size 1284x2778 \
        --require-opaque
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ModuleNotFoundError as exc:  # pragma: no cover - template runtime guard
    raise SystemExit(
        "Pillow is required. Install it with: python3 -m pip install Pillow"
    ) from exc


SUPPORTED_SUFFIXES = {".png", ".jpg", ".jpeg"}


def parse_size(raw: str) -> tuple[int, int]:
    try:
        width_str, height_str = raw.lower().split("x", 1)
        return int(width_str), int(height_str)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid size '{raw}'. Use WIDTHxHEIGHT, for example 1320x2868."
        ) from exc


def find_images(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )


def has_transparent_alpha(image: Image.Image) -> bool:
    if image.mode in {"RGBA", "LA"}:
        alpha = image.getchannel("A")
        minimum, _ = alpha.getextrema()
        return minimum < 255

    if image.mode == "P" and "transparency" in image.info:
        rgba = image.convert("RGBA")
        alpha = rgba.getchannel("A")
        minimum, _ = alpha.getextrema()
        return minimum < 255

    return False


def validate_image(
    path: Path,
    *,
    allowed_sizes: set[tuple[int, int]],
    require_opaque: bool,
) -> list[str]:
    issues: list[str] = []

    with Image.open(path) as image:
        size = image.size
        if allowed_sizes and size not in allowed_sizes:
            issues.append(
                f"unexpected size {size[0]}x{size[1]} (allowed: "
                + ", ".join(f"{w}x{h}" for w, h in sorted(allowed_sizes))
                + ")"
            )

        if require_opaque and has_transparent_alpha(image):
            issues.append("contains transparent alpha")

    return issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate exported App Store screenshots for size and opacity."
    )
    parser.add_argument(
        "--root",
        required=True,
        type=Path,
        help="Root directory containing exported screenshots.",
    )
    parser.add_argument(
        "--allowed-size",
        action="append",
        default=[],
        type=parse_size,
        help="Allowed screenshot size in WIDTHxHEIGHT form. Repeat as needed.",
    )
    parser.add_argument(
        "--require-opaque",
        action="store_true",
        help="Fail when an image contains transparent alpha.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    root: Path = args.root
    if not root.exists() or not root.is_dir():
        parser.error(f"Root directory does not exist or is not a directory: {root}")

    images = find_images(root)
    if not images:
        parser.error(f"No .png, .jpg, or .jpeg files found under: {root}")

    allowed_sizes = set(args.allowed_size)
    failures: list[tuple[Path, list[str]]] = []

    for image_path in images:
        issues = validate_image(
            image_path,
            allowed_sizes=allowed_sizes,
            require_opaque=args.require_opaque,
        )
        if issues:
            failures.append((image_path, issues))

    if failures:
        print("Validation failed:\n")
        for image_path, issues in failures:
            print(image_path)
            for issue in issues:
                print(f"  - {issue}")
        return 1

    print(
        f"Validated {len(images)} image(s) under {root}. "
        f"Allowed sizes: {', '.join(f'{w}x{h}' for w, h in sorted(allowed_sizes)) or 'any'}; "
        f"require opaque: {'yes' if args.require_opaque else 'no'}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
