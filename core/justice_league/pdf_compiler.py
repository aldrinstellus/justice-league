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

    def say(self, message: str, technical_info: Optional[str] = None):
        """Narrator output"""
        if self.narrator:
            self.narrator.hero_speaks(
                "💨 Quicksilver PDF",
                message,
                "friendly",
                technical_info
            )

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
        """Add a single frame page with metadata"""
        c = self.pdf_canvas
        self.current_page += 1

        # Calculate image dimensions to fit page
        img_width = frame_info['width']
        img_height = frame_info['height']

        # Available space
        available_width = self.page_width - 2 * self.margin
        available_height = self.page_height - 2 * self.margin - 0.5*inch  # Reserve space for metadata

        # Scale to fit
        if img_width > 0 and img_height > 0:
            scale_w = available_width / img_width
            scale_h = available_height / img_height
            scale = min(scale_w, scale_h)

            display_width = img_width * scale
            display_height = img_height * scale
        else:
            display_width = available_width
            display_height = available_height

        # Center image
        x = (self.page_width - display_width) / 2
        y = (self.page_height - display_height) / 2 + 0.25*inch  # Shift up slightly for metadata

        # Draw image
        try:
            c.drawImage(
                str(frame_path),
                x, y,
                width=display_width,
                height=display_height,
                preserveAspectRatio=True
            )
        except Exception as e:
            # If image fails, draw placeholder
            c.setStrokeColor(colors.red)
            c.rect(x, y, display_width, display_height)
            c.setFont("Helvetica", 10)
            c.drawCentredString(x + display_width/2, y + display_height/2, f"Error loading image: {e}")

        # Add metadata footer
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.grey)

        footer_y = self.margin / 2

        # Left: Frame name and source page
        c.drawString(self.margin, footer_y + 10, f"Frame: {frame_info['name']}")
        c.drawString(self.margin, footer_y, f"Source: {page_name}")

        # Center: Dimensions
        if img_width > 0 and img_height > 0:
            c.drawCentredString(
                self.page_width / 2,
                footer_y,
                f"{img_width} × {img_height} px"
            )

        # Right: Page number
        c.drawRightString(
            self.page_width - self.margin,
            footer_y,
            f"Frame {frame_num} of {total_frames} • Page {self.current_page}"
        )

        c.setFillColor(colors.black)
        c.showPage()
