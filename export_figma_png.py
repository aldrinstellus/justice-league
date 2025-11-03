#!/usr/bin/env python3
"""
💨 QUICKSILVER PNG EXPORT - Simple CLI
========================================

Export all frames from a Figma file as PNG images.

Usage:
    python3 export_figma_png.py <FILE_KEY_OR_URL>
    python3 export_figma_png.py <FILE_KEY_OR_URL> --output my-export/
    python3 export_figma_png.py <FILE_KEY_OR_URL> --workers 8 --scale 2.0

Examples:
    python3 export_figma_png.py fubdMARNgA2lVhmzpPg77y
    python3 export_figma_png.py "https://www.figma.com/design/ABC123..."
    python3 export_figma_png.py ABC123 --output exports/my-design/

Production-tested settings (default):
- 8 concurrent workers (parallel processing)
- 60s API timeout (handles slow Figma responses)
- 120s CDN timeout (handles large image downloads)
- 2.0x scale (high-quality exports)

Created: 2025-10-31 (Quicksilver v1.0.1)
"""

import argparse
import os
import re
import sys
from pathlib import Path
from datetime import datetime

# Add parent for imports
sys.path.append(str(Path(__file__).parent))

from core.justice_league import export_frames_quicksilver, QuicksilverSpeedExport


def extract_file_key(file_key_or_url: str) -> str:
    """Extract Figma file key from URL or return as-is"""
    # Check if it's a URL
    if 'figma.com' in file_key_or_url:
        match = re.search(r'figma\.com/(?:file|design)/([A-Za-z0-9]+)', file_key_or_url)
        if match:
            return match.group(1)
        else:
            print("❌ Could not extract file key from URL")
            sys.exit(1)
    return file_key_or_url


def main():
    parser = argparse.ArgumentParser(
        description="Export Figma frames as PNG with Quicksilver parallel export",
        epilog="Requires FIGMA_ACCESS_TOKEN environment variable"
    )

    parser.add_argument(
        'file_key',
        help='Figma file key or full URL'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output directory (default: figma-export-TIMESTAMP)',
        default=None
    )
    parser.add_argument(
        '--workers', '-w',
        type=int,
        default=8,
        help='Concurrent workers (default: 8)'
    )
    parser.add_argument(
        '--scale', '-s',
        type=float,
        default=2.0,
        help='Export scale 1.0-4.0 (default: 2.0)'
    )
    parser.add_argument(
        '--token', '-t',
        help='Figma access token (or use FIGMA_ACCESS_TOKEN env var)',
        default=None
    )

    args = parser.parse_args()

    # Extract file key
    file_key = extract_file_key(args.file_key)

    # Get Figma token
    figma_token = args.token or os.getenv('FIGMA_ACCESS_TOKEN')
    if not figma_token:
        print("❌ Error: Figma access token not found!")
        print("   Set FIGMA_ACCESS_TOKEN environment variable or use --token")
        sys.exit(1)

    # Determine output directory
    if args.output:
        output_dir = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_dir = f"figma-export-{timestamp}"

    # Validate scale
    if not (1.0 <= args.scale <= 4.0):
        print("❌ Error: Scale must be between 1.0 and 4.0")
        sys.exit(1)

    # Print banner
    print()
    print("=" * 80)
    print("     💨 QUICKSILVER PNG EXPORT")
    print("=" * 80)
    print()
    print(f"📁 File Key: {file_key}")
    print(f"📂 Output: {output_dir}")
    print(f"⚡ Workers: {args.workers}")
    print(f"📏 Scale: {args.scale}x")
    print()
    print("Starting export...")
    print()

    # Run Quicksilver export
    result = export_frames_quicksilver(
        file_key=file_key,
        output_dir=output_dir,
        figma_token=figma_token,
        max_workers=args.workers,
        scale=args.scale
    )

    # Show results
    print()
    print("=" * 80)

    # Check if result is a list or dict with success
    is_success = isinstance(result, list) and len(result) > 0
    if not is_success and isinstance(result, dict):
        is_success = result.get('success', False)

    if is_success:
        print("✅ EXPORT COMPLETE")
        print("=" * 80)

        # Handle different result formats
        if isinstance(result, list):
            total_frames = len(result)
            frames_exported = sum(1 for r in result if r.get('success'))
            success_rate = (frames_exported / total_frames * 100) if total_frames > 0 else 0

            print(f"Frames Exported: {frames_exported}/{total_frames}")
            print(f"Success Rate: {success_rate:.1f}%")
        else:
            frames_exported = result.get('frames_exported', 0)
            total_frames = result.get('total_frames', 0)
            success_rate = result.get('success_rate', 0)

            print(f"Frames Exported: {frames_exported}/{total_frames}")
            print(f"Success Rate: {success_rate:.1f}%")

        # Get absolute path
        abs_output = str(Path(output_dir).resolve())
        print(f"Output: {abs_output}")

        # Generate PDF compilation
        print()
        print("📄 Generating PDF compilation...")
        print()

        try:
            quicksilver = QuicksilverSpeedExport(figma_token=figma_token)

            # Get Figma file name for PDF metadata
            figma_file_name = f"Figma Export {file_key[:8]}"

            # Prepare export metadata
            export_metadata = {
                'scale': args.scale,
                'workers': args.workers,
                'total_frames': total_frames,
                'frames_exported': frames_exported
            }

            # Compile PDF
            pdf_result = quicksilver.compile_pdf_from_export(
                export_dir=Path(abs_output),
                figma_file_name=figma_file_name,
                export_metadata=export_metadata
            )

            if pdf_result.get('success'):
                pdf_path = pdf_result['pdf_path']
                pdf_size_mb = pdf_result.get('file_size_mb', 0)
                total_pdf_pages = pdf_result.get('total_pages', 0)

                print("✅ PDF COMPILATION COMPLETE")
                print("=" * 80)
                print(f"PDF File: {pdf_path}")
                print(f"PDF Size: {pdf_size_mb:.1f} MB")
                print(f"PDF Pages: {total_pdf_pages}")
                print("=" * 80)
            else:
                print("⚠️  PDF compilation failed (PNG export still successful)")
                if 'error' in pdf_result:
                    print(f"   Error: {pdf_result['error']}")

        except Exception as e:
            print("⚠️  PDF compilation failed (PNG export still successful)")
            print(f"   Error: {str(e)}")

        print()
        print("=" * 80)
        print()
    else:
        print("❌ EXPORT FAILED")
        print("=" * 80)
        if isinstance(result, dict) and 'error' in result:
            print(f"Error: {result['error']}")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
