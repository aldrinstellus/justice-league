#!/usr/bin/env python3
"""
Test PDF compilation on existing Figma export directory
"""

import sys
from pathlib import Path

# Add parent for imports
sys.path.append(str(Path(__file__).parent))

from core.justice_league import PDFCompiler

def main():
    # Existing export directory
    export_dir = Path("/Users/admin/Documents/claudecode/Projects/aldo-vision/figma-export-ui-master")

    if not export_dir.exists():
        print(f"❌ Export directory not found: {export_dir}")
        sys.exit(1)

    print("=" * 80)
    print("     💨 PDF COMPILATION TEST")
    print("=" * 80)
    print()
    print(f"📁 Export Directory: {export_dir}")
    print()
    print("Starting PDF compilation...")
    print()

    # Create PDF compiler
    compiler = PDFCompiler()

    # Output PDF in the same directory
    pdf_path = export_dir / f"{export_dir.name}.pdf"

    # Compile PDF
    result = compiler.compile_pdf(
        export_dir=export_dir,
        output_path=pdf_path,
        figma_file_name="UI Master",
        export_metadata={
            'scale': 2.0,
            'export_date': '2025-10-31'
        }
    )

    # Show results
    print()
    print("=" * 80)

    if result.get('success'):
        print("✅ PDF COMPILATION COMPLETE")
        print("=" * 80)
        print(f"PDF File: {result['pdf_path']}")
        print(f"Total Frames: {result['total_frames']}")
        print(f"Total Pages: {result['total_pages']}")
        print(f"File Size: {result['file_size_mb']:.1f} MB")
        print("=" * 80)
    else:
        print("❌ PDF COMPILATION FAILED")
        print("=" * 80)
        if 'error' in result:
            print(f"Error: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
