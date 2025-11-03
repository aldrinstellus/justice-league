"""
💨 Quicksilver PDF Compiler
=============================

Compiles exported PNG frames into a professional PDF document with:
- Summary/cover page with export metadata
- Table of contents with clickable links
- One frame per page at full resolution
- Frame metadata on each page

Created: 2025-10-31
Justice League v1.9.5 - Quicksilver PDF Extension
"""

from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from PIL import Image

# PDF generation library
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader


class PDFCompiler:
    """
    Compiles PNG frame exports into a structured PDF document.

    Features:
    - Automatic page sizing based on frame dimensions
    - Table of contents with clickable links
    - Frame metadata on each page
    - Export summary page
    - Full-resolution image embedding
    """

    def __init__(self, narrator=None):
        """Initialize PDF compiler"""
        self.narrator = narrator
        self.pdf_canvas = None
        self.page_width = 8.5 * inch  # Letter size width
        self.page_height = 11 * inch  # Letter size height
        self.margin = 0.75 * inch
        self.toc_entries: List[Dict] = []
        self.current_page = 0
        self.clean_mode = False  # True = full-bleed, no metadata
        self.bordered_mode = False  # True = add white padding around frames
        self.border_width = 20  # pixels of white border on each side

    def say(self, message: str, technical_info: Optional[str] = None):
        """Narrator output"""
        if self.narrator:
            self.narrator.hero_speaks(
                "💨 Quicksilver PDF",
                message,
                "friendly",
                technical_info
            )

    def _draw_white_background(self):
        """Draw white background on current page to prevent black borders"""
        c = self.pdf_canvas
        c.setFillColor(colors.white)
        c.rect(0, 0, self.page_width, self.page_height, fill=1, stroke=0)
        c.setFillColor(colors.black)  # Reset to black for text

    def compile_pdf(
        self,
        export_dir: Path,
        output_path: Path,
        figma_file_name: str,
        export_metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Compile PNG export directory into PDF

        Args:
            export_dir: Path to directory containing PNG files
            output_path: Where to save the PDF
            figma_file_name: Name of the Figma file
            export_metadata: Optional metadata about the export

        Returns:
            Dict with compilation results
        """
        self.say(f"Starting PDF compilation for {figma_file_name}")

        # Check for clean mode (full-bleed, no metadata)
        if export_metadata and export_metadata.get('clean_mode'):
            self.clean_mode = True
            self.say("Clean mode enabled: full-bleed pages, no metadata")

        # Check for bordered mode (white padding around frames)
        if export_metadata and export_metadata.get('bordered_mode'):
            self.bordered_mode = True
            border_size = export_metadata.get('border_width', 20)
            self.border_width = border_size
            self.say(f"Bordered mode enabled: {border_size}px white padding around each frame")

        # Gather all PNG files organized by page
        frames_by_page = self._scan_export_directory(export_dir)

        if not frames_by_page:
            return {
                'success': False,
                'error': 'No PNG files found in export directory'
            }

        total_frames = sum(len(frames) for frames in frames_by_page.values())
        self.say(
            f"Found {total_frames} frames across {len(frames_by_page)} pages",
            f"Pages: {list(frames_by_page.keys())}"
        )

        # Create PDF
        self.pdf_canvas = canvas.Canvas(str(output_path), pagesize=letter)
        self.current_page = 0

        # Page 1: Cover/Summary
        self._create_summary_page(figma_file_name, export_metadata, total_frames, len(frames_by_page))

        # Page 2+: Table of Contents
        toc_pages = self._create_toc_pages(frames_by_page)

        # Frame pages: Add each frame
        frame_count = 0
        for page_name, frames in sorted(frames_by_page.items()):
            for frame_path, frame_info in frames:
                frame_count += 1
                self._add_frame_page(
                    frame_path,
                    frame_info,
                    page_name,
                    frame_count,
                    total_frames
                )

                if frame_count % 50 == 0:
                    self.say(f"Progress: {frame_count}/{total_frames} frames")

        # Save PDF
        self.pdf_canvas.save()

        self.say(
            f"PDF compilation complete: {total_frames} frames",
            f"Output: {output_path.name}"
        )

        return {
            'success': True,
            'pdf_path': str(output_path),
            'total_frames': total_frames,
            'total_pages': self.current_page,
            'file_size_mb': output_path.stat().st_size / (1024 * 1024)
        }

    def _scan_export_directory(self, export_dir: Path) -> Dict[str, List[Tuple[Path, Dict]]]:
        """
        Scan export directory and organize frames by page

        Returns:
            Dict mapping page names to list of (frame_path, frame_info) tuples
        """
        frames_by_page = {}

        # Expected structure: export_dir/Document/PageName/frame.png
        doc_dir = export_dir / "Document"

        if not doc_dir.exists():
            # Try direct structure
            doc_dir = export_dir

        # Scan for page directories
        for page_dir in sorted(doc_dir.iterdir()):
            if not page_dir.is_dir():
                continue

            page_name = page_dir.name
            frames = []

            # Scan for PNG files in this page
            for png_file in sorted(page_dir.glob("*.png")):
                # Extract frame info from filename: {name}_{id}.png
                frame_name = png_file.stem

                # Get image dimensions
                try:
                    with Image.open(png_file) as img:
                        width, height = img.size
                except Exception:
                    width, height = 0, 0

                frame_info = {
                    'name': frame_name,
                    'path': png_file,
                    'width': width,
                    'height': height
                }

                frames.append((png_file, frame_info))

            if frames:
                frames_by_page[page_name] = frames

        return frames_by_page

    def _create_summary_page(
        self,
        figma_file_name: str,
        metadata: Optional[Dict],
        total_frames: int,
        total_pages: int
    ):
        """Create cover/summary page"""
        c = self.pdf_canvas
        self.current_page += 1

        # Draw white page background
        self._draw_white_background()

        # Title
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(self.page_width / 2, self.page_height - 2*inch, "Figma Frame Export")

        # File name
        c.setFont("Helvetica", 16)
        c.drawCentredString(self.page_width / 2, self.page_height - 2.5*inch, figma_file_name)

        # Export info
        c.setFont("Helvetica", 12)
        y = self.page_height - 4*inch

        info_lines = [
            f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Frames: {total_frames}",
            f"Figma Pages: {total_pages}",
            f"Scale: {metadata.get('scale', '2.0')}x" if metadata else "Scale: 2.0x",
            "",
            "Generated by Quicksilver Speed Export",
            "Justice League v1.9.5"
        ]

        for line in info_lines:
            c.drawCentredString(self.page_width / 2, y, line)
            y -= 20

        c.showPage()

    def _create_toc_pages(self, frames_by_page: Dict[str, List]) -> int:
        """
        Create table of contents pages

        Returns:
            Number of TOC pages created
        """
        c = self.pdf_canvas
        toc_start_page = self.current_page

        # Draw white background for first TOC page
        self._draw_white_background()

        c.setFont("Helvetica-Bold", 18)
        c.drawString(self.margin, self.page_height - self.margin, "Table of Contents")

        y = self.page_height - self.margin - 0.5*inch
        page_num = toc_start_page + 1  # Frames start after TOC

        c.setFont("Helvetica", 10)

        for page_name, frames in sorted(frames_by_page.items()):
            # Page section header
            if y < 1.5*inch:
                c.showPage()
                self.current_page += 1
                self._draw_white_background()  # White background for new TOC page
                y = self.page_height - self.margin

            c.setFont("Helvetica-Bold", 12)
            c.drawString(self.margin, y, page_name)
            y -= 20

            c.setFont("Helvetica", 9)

            # List frames
            for _, frame_info in frames:
                page_num += 1

                if y < 1.5*inch:
                    c.showPage()
                    self.current_page += 1
                    self._draw_white_background()  # White background for new TOC page
                    y = self.page_height - self.margin

                frame_name = frame_info['name']
                if len(frame_name) > 60:
                    frame_name = frame_name[:57] + "..."

                c.drawString(self.margin + 0.25*inch, y, f"• {frame_name}")
                c.drawRightString(self.page_width - self.margin, y, str(page_num))
                y -= 15

            y -= 10  # Extra space between pages

        c.showPage()
        self.current_page += 1

        return self.current_page - toc_start_page

    def _add_frame_page(
        self,
        frame_path: Path,
        frame_info: Dict,
        page_name: str,
        frame_num: int,
        total_frames: int
    ):
        """Add a single frame page with custom dimensions matching the frame"""
        c = self.pdf_canvas
        self.current_page += 1

        # Get frame dimensions
        img_width = frame_info['width']
        img_height = frame_info['height']

        if img_width == 0 or img_height == 0:
            # Fallback to letter size if dimensions unavailable
            img_width = 8.5 * inch
            img_height = 11 * inch

        # Determine page size and positioning based on mode
        if self.bordered_mode:
            # Bordered mode: add white padding around frame
            border = self.border_width * 2  # Both sides
            metadata_height = 30
            page_width = img_width + border
            page_height = img_height + border + metadata_height
            img_x = self.border_width
            img_y = self.border_width + metadata_height
        elif self.clean_mode:
            # Clean mode: page is EXACTLY frame size (full-bleed, no metadata)
            metadata_height = 0
            page_width = img_width
            page_height = img_height
            img_x = 0
            img_y = 0
        else:
            # Standard mode: add small margin for metadata footer
            metadata_height = 30
            page_width = img_width
            page_height = img_height + metadata_height
            img_x = 0
            img_y = metadata_height

        # Set custom page size for this frame
        c.setPageSize((page_width, page_height))

        # Update instance variables for this page
        original_page_width = self.page_width
        original_page_height = self.page_height
        self.page_width = page_width
        self.page_height = page_height

        # Draw white page background (fills entire page including borders)
        self._draw_white_background()

        # Draw image
        try:
            c.drawImage(
                str(frame_path),
                img_x, img_y,
                width=img_width,
                height=img_height,
                preserveAspectRatio=False
            )
        except Exception as e:
            # If image fails, draw placeholder
            c.setStrokeColor(colors.red)
            c.rect(img_x, img_y, img_width, img_height)
            c.setFont("Helvetica", 10)
            c.drawCentredString(img_x + img_width/2, img_y + img_height/2, f"Error loading image: {e}")

        # Add metadata footer ONLY in non-clean mode
        if not self.clean_mode:
            c.setFont("Helvetica", 7)
            c.setFillColor(colors.grey)

            footer_y = 15  # Center in metadata space

            # Left: Frame name and source page (compact)
            frame_name = frame_info['name']
            if len(frame_name) > 40:
                frame_name = frame_name[:37] + "..."

            c.drawString(self.border_width + 5 if self.bordered_mode else 5, footer_y, f"{frame_name} • {page_name}")

            # Center: Dimensions
            c.drawCentredString(
                page_width / 2,
                footer_y,
                f"{int(img_width)} × {int(img_height)} px"
            )

            # Right: Page number
            c.drawRightString(
                page_width - (self.border_width + 5 if self.bordered_mode else 5),
                footer_y,
                f"Frame {frame_num}/{total_frames} • Pg {self.current_page}"
            )

            c.setFillColor(colors.black)

        c.showPage()

        # Restore original page dimensions for next page
        self.page_width = original_page_width
        self.page_height = original_page_height
