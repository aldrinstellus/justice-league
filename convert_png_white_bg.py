#!/usr/bin/env python3
"""
Convert transparent PNGs to white background PNGs
Fixes black borders in PDF viewers caused by PNG alpha channels
"""

import sys
from pathlib import Path
from PIL import Image

def convert_transparent_to_white(png_path, output_path):
    """Convert transparent PNG to white background PNG"""
    with Image.open(png_path) as img:
        if img.mode in ('RGBA', 'LA', 'PA'):
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            # Paste image on white using alpha as mask
            background.paste(img, mask=img.split()[3])
            background.save(output_path, 'PNG')
            return True
        else:
            # No transparency, just copy
            img.save(output_path, 'PNG')
            return False

def main():
    input_dir = Path("/Users/admin/Documents/claudecode/Projects/aldo-vision/figma-export-20251031-081543")
    output_dir = input_dir.parent / f"{input_dir.name}-white-bg"

    print("=" * 80)
    print("     🎨 PNG TRANSPARENCY → WHITE BACKGROUND CONVERSION")
    print("=" * 80)
    print()
    print(f"Input:  {input_dir}")
    print(f"Output: {output_dir}")
    print()

    # Find all PNGs
    png_files = list(input_dir.rglob("*.png"))
    print(f"Found {len(png_files)} PNG files")
    print()
    print("Converting...")

    converted = 0
    for i, png_path in enumerate(png_files, 1):
        # Preserve directory structure
        rel_path = png_path.relative_to(input_dir)
        out_path = output_dir / rel_path
        out_path.parent.mkdir(parents=True, exist_ok=True)

        was_converted = convert_transparent_to_white(png_path, out_path)
        if was_converted:
            converted += 1

        if i % 50 == 0:
            print(f"  Progress: {i}/{len(png_files)}")

    print()
    print("=" * 80)
    print("✅ CONVERSION COMPLETE")
    print("=" * 80)
    print(f"Total PNGs: {len(png_files)}")
    print(f"Converted (RGBA→RGB): {converted}")
    print(f"Already RGB: {len(png_files) - converted}")
    print()
    print(f"Output directory: {output_dir}")
    print("=" * 80)

if __name__ == "__main__":
    main()
