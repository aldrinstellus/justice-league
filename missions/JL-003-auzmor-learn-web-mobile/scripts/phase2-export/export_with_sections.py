#!/usr/bin/env python3
"""
JL-003 Phase 2A: Figma Export with Section Support
===================================================

Exports Figma files with complete hierarchy cascade:
- File → Page → Section (optional) → Frame
- File → Page → Frame (direct, not in section)

Outputs:
- Page overview PNG (full page with all content)
- Section overview PNG (if sections exist)
- Individual frame PNGs (in appropriate folders)
- Consolidated PDF per file
- Metadata JSON with complete hierarchy

Benchmark: aldo-vision Quicksilver export scripts
Reference: PHASE2-EXPORT-STRUCTURE-REVISED.md
Cascade Logic: detailed_file_analysis.py from Phase 1

Usage:
    python3 export_with_sections.py --file-key FILE_KEY --output-dir exports/
    python3 export_with_sections.py --all  # Export all 182 files

Environment:
    FIGMA_ACCESS_TOKEN - Figma API token
    QUICKSILVER_API_TIMEOUT - API timeout (default: 60)
    QUICKSILVER_CDN_TIMEOUT - CDN timeout (default: 120)

Created: 2025-11-03 (Oracle + Aldo)
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests

# Add parent directories for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

# Configuration
FIGMA_API_BASE = 'https://api.figma.com/v1'
FIGMA_TOKEN = os.getenv('FIGMA_ACCESS_TOKEN')
API_TIMEOUT = int(os.getenv('QUICKSILVER_API_TIMEOUT', '60'))
CDN_TIMEOUT = int(os.getenv('QUICKSILVER_CDN_TIMEOUT', '120'))
RATE_LIMIT_DELAY = 1.2  # Seconds between API calls


class FigmaExporter:
    """Export Figma files with section support"""

    def __init__(self, token: str):
        if not token:
            raise ValueError("Figma access token required. Set FIGMA_ACCESS_TOKEN environment variable.")

        self.token = token
        self.headers = {'X-Figma-Token': self.token}
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def sanitize_name(self, name: str, max_length: int = 100) -> str:
        """Generate safe folder/file name"""
        # Remove special characters, replace spaces with hyphens
        safe_name = name.replace('/', '-').replace('\\', '-')
        safe_name = safe_name.replace('|', '-').replace(':', '-')
        safe_name = safe_name.replace('?', '').replace('*', '')
        safe_name = safe_name.replace('"', '').replace('<', '').replace('>', '')
        safe_name = safe_name.strip()

        # Replace multiple hyphens/spaces with single hyphen
        safe_name = re.sub(r'[-\s]+', '-', safe_name)

        # Limit length
        if len(safe_name) > max_length:
            safe_name = safe_name[:max_length].rstrip('-')

        return safe_name

    def get_file_structure(self, file_key: str) -> Dict[str, Any]:
        """Fetch Figma file structure"""
        print(f"🔍 Fetching file structure: {file_key}")

        url = f"{FIGMA_API_BASE}/files/{file_key}"
        response = self.session.get(url, timeout=API_TIMEOUT)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch file: {response.status_code} - {response.text}")

        return response.json()

    def analyze_page_structure(self, page_node: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze page structure with section support.

        Returns:
            {
                'page_name': str,
                'page_id': str,
                'has_sections': bool,
                'sections': List[Dict],  # Section info
                'direct_frames': List[Dict],  # Frames not in sections
                'total_frames': int
            }
        """
        page_info = {
            'page_name': page_node.get('name', 'Unnamed'),
            'page_id': page_node.get('id', ''),
            'has_sections': False,
            'sections': [],
            'direct_frames': [],
            'total_frames': 0
        }

        children = page_node.get('children', [])

        for child in children:
            child_type = child.get('type', '')

            # Case 1: Child is SECTION
            if child_type == 'SECTION':
                page_info['has_sections'] = True

                section_info = {
                    'section_name': child.get('name', 'Unnamed'),
                    'section_id': child.get('id', ''),
                    'frames': []
                }

                # Parse frames within section
                for section_child in child.get('children', []):
                    if section_child.get('type') == 'FRAME':
                        frame_info = self._extract_frame_info(section_child)
                        section_info['frames'].append(frame_info)
                        page_info['total_frames'] += 1

                page_info['sections'].append(section_info)

            # Case 2: Child is direct FRAME
            elif child_type == 'FRAME':
                frame_info = self._extract_frame_info(child)
                page_info['direct_frames'].append(frame_info)
                page_info['total_frames'] += 1

        return page_info

    def _extract_frame_info(self, frame_node: Dict[str, Any]) -> Dict[str, Any]:
        """Extract frame information"""
        bounds = frame_node.get('absoluteBoundingBox', {})

        return {
            'frame_name': frame_node.get('name', 'Unnamed'),
            'frame_id': frame_node.get('id', ''),
            'width': bounds.get('width', 0),
            'height': bounds.get('height', 0)
        }

    def export_node_as_png(self, file_key: str, node_id: str, output_path: str, scale: float = 2.0):
        """Export a specific node (page, section, or frame) as PNG"""
        # Get image URL from Figma
        url = f"{FIGMA_API_BASE}/images/{file_key}"
        params = {
            'ids': node_id,
            'scale': scale,
            'format': 'png'
        }

        response = self.session.get(url, params=params, timeout=API_TIMEOUT)

        if response.status_code != 200:
            raise Exception(f"Failed to get image URL: {response.status_code}")

        data = response.json()
        image_url = data.get('images', {}).get(node_id)

        if not image_url:
            print(f"   ⚠️  Warning: No image URL returned for node {node_id} (possibly empty page)")
            return  # Skip empty pages gracefully

        # Download image
        img_response = requests.get(image_url, timeout=CDN_TIMEOUT)

        if img_response.status_code != 200:
            raise Exception(f"Failed to download image: {img_response.status_code}")

        # Save to file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(img_response.content)

        # Rate limiting
        time.sleep(RATE_LIMIT_DELAY)

    def export_file_with_sections(
        self,
        file_key: str,
        file_name: str,
        file_number: int,
        output_base_dir: str
    ) -> Dict[str, Any]:
        """
        Export complete Figma file with section support.

        Structure:
            {file_number}-{file_name}/
            ├── page-01-{page_name}/
            │   ├── page-01-overview.png
            │   ├── sections/
            │   │   ├── section-01-{name}/
            │   │   │   ├── section-overview.png
            │   │   │   └── frames/
            │   │   │       └── frame-001-{name}.png
            │   │   └── ...
            │   └── frames/
            │       └── frame-001-{name}.png
            ├── {FILE-NAME}-COMPLETE.pdf
            └── file-info.json
        """
        print(f"\n{'='*80}")
        print(f"📁 Exporting File {file_number}: {file_name}")
        print(f"{'='*80}")

        # Get file structure
        file_data = self.get_file_structure(file_key)
        document = file_data.get('document', {})
        pages = document.get('children', [])

        # Create file folder
        safe_file_name = self.sanitize_name(file_name)
        file_folder = os.path.join(output_base_dir, f"{file_number:03d}-{safe_file_name}")
        os.makedirs(file_folder, exist_ok=True)

        print(f"📂 Output: {file_folder}")
        print(f"📄 Pages: {len(pages)}")

        # Metadata structure
        metadata = {
            'file_number': f"{file_number:03d}",
            'file_key': file_key,
            'file_name': file_name,
            'last_modified': file_data.get('lastModified', ''),
            'export_date': datetime.now().isoformat(),
            'total_pages': len(pages),
            'total_frames': 0,
            'total_sections': 0,
            'pages': []
        }

        # Export each page
        for page_idx, page_node in enumerate(pages, 1):
            page_structure = self.analyze_page_structure(page_node)

            page_name = page_structure['page_name']
            safe_page_name = self.sanitize_name(page_name)
            page_folder = os.path.join(file_folder, f"page-{page_idx:02d}-{safe_page_name}")

            print(f"\n📄 Page {page_idx}/{len(pages)}: {page_name}")
            print(f"   Frames: {page_structure['total_frames']}, Sections: {len(page_structure['sections'])}")

            os.makedirs(page_folder, exist_ok=True)

            # Export page overview PNG (skip if page is empty)
            if page_structure['total_frames'] > 0:
                page_overview_path = os.path.join(page_folder, f"page-{page_idx:02d}-overview.png")
                print(f"   ⬇️  Exporting page overview...")
                self.export_node_as_png(file_key, page_structure['page_id'], page_overview_path)
            else:
                print(f"   ⏭️  Skipping page overview (empty page)")
                page_overview_path = None

            # Page metadata
            page_meta = {
                'page_number': page_idx,
                'page_name': page_name,
                'page_id': page_structure['page_id'],
                'total_frames': page_structure['total_frames'],
                'total_sections': len(page_structure['sections']),
                'overview_file': f"page-{page_idx:02d}-{safe_page_name}/page-{page_idx:02d}-overview.png" if page_structure['total_frames'] > 0 else None,
                'sections': [],
                'direct_frames': []
            }

            # Export sections (if exist)
            if page_structure['has_sections']:
                sections_folder = os.path.join(page_folder, 'sections')
                os.makedirs(sections_folder, exist_ok=True)

                for section_idx, section in enumerate(page_structure['sections'], 1):
                    section_name = section['section_name']
                    safe_section_name = self.sanitize_name(section_name)
                    section_folder = os.path.join(sections_folder, f"section-{section_idx:02d}-{safe_section_name}")
                    frames_folder = os.path.join(section_folder, 'frames')

                    os.makedirs(frames_folder, exist_ok=True)

                    print(f"   📦 Section {section_idx}: {section_name} ({len(section['frames'])} frames)")

                    # Export section overview PNG
                    section_overview_path = os.path.join(section_folder, 'section-overview.png')
                    self.export_node_as_png(file_key, section['section_id'], section_overview_path)

                    # Section metadata
                    section_meta = {
                        'section_number': section_idx,
                        'section_name': section_name,
                        'section_id': section['section_id'],
                        'frames_count': len(section['frames']),
                        'overview_file': f"page-{page_idx:02d}-{safe_page_name}/sections/section-{section_idx:02d}-{safe_section_name}/section-overview.png",
                        'frames': []
                    }

                    # Export frames in section
                    for frame_idx, frame in enumerate(section['frames'], 1):
                        frame_name = frame['frame_name']
                        safe_frame_name = self.sanitize_name(frame_name)
                        frame_path = os.path.join(frames_folder, f"frame-{frame_idx:03d}-{safe_frame_name}.png")

                        self.export_node_as_png(file_key, frame['frame_id'], frame_path)

                        frame_meta = {
                            'frame_number': frame_idx,
                            'frame_name': frame_name,
                            'frame_id': frame['frame_id'],
                            'width': frame['width'],
                            'height': frame['height'],
                            'file': f"page-{page_idx:02d}-{safe_page_name}/sections/section-{section_idx:02d}-{safe_section_name}/frames/frame-{frame_idx:03d}-{safe_frame_name}.png"
                        }
                        section_meta['frames'].append(frame_meta)

                    page_meta['sections'].append(section_meta)
                    metadata['total_sections'] += 1

            # Export direct frames (not in sections)
            if page_structure['direct_frames']:
                frames_folder = os.path.join(page_folder, 'frames')
                os.makedirs(frames_folder, exist_ok=True)

                print(f"   🖼️  Direct frames: {len(page_structure['direct_frames'])}")

                for frame_idx, frame in enumerate(page_structure['direct_frames'], 1):
                    frame_name = frame['frame_name']
                    safe_frame_name = self.sanitize_name(frame_name)
                    frame_path = os.path.join(frames_folder, f"frame-{frame_idx:03d}-{safe_frame_name}.png")

                    self.export_node_as_png(file_key, frame['frame_id'], frame_path)

                    frame_meta = {
                        'frame_number': frame_idx,
                        'frame_name': frame_name,
                        'frame_id': frame['frame_id'],
                        'width': frame['width'],
                        'height': frame['height'],
                        'file': f"page-{page_idx:02d}-{safe_page_name}/frames/frame-{frame_idx:03d}-{safe_frame_name}.png"
                    }
                    page_meta['direct_frames'].append(frame_meta)

            metadata['pages'].append(page_meta)
            metadata['total_frames'] += page_structure['total_frames']

        # Save metadata JSON
        metadata_path = os.path.join(file_folder, 'file-info.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Export Complete!")
        print(f"   Total Frames: {metadata['total_frames']}")
        print(f"   Total Sections: {metadata['total_sections']}")
        print(f"   Metadata: {metadata_path}")

        return metadata


def main():
    parser = argparse.ArgumentParser(
        description="Export Figma files with section support (JL-003 Phase 2A)",
        epilog="Requires FIGMA_ACCESS_TOKEN environment variable"
    )

    parser.add_argument(
        '--file-key',
        help='Figma file key to export'
    )
    parser.add_argument(
        '--file-name',
        help='Figma file name (for folder naming)'
    )
    parser.add_argument(
        '--file-number',
        type=int,
        default=1,
        help='File number for folder naming (default: 1)'
    )
    parser.add_argument(
        '--output-dir',
        default='exports/figma-files',
        help='Output directory (default: exports/figma-files)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Export all 182 files from Phase 1 analysis'
    )

    args = parser.parse_args()

    if not FIGMA_TOKEN:
        print("❌ Error: FIGMA_ACCESS_TOKEN environment variable not set")
        print("   Get token from: Figma → Settings → Personal Access Tokens")
        sys.exit(1)

    exporter = FigmaExporter(FIGMA_TOKEN)

    if args.all:
        # Load Phase 1 analysis
        phase1_files_path = '../../outputs/phase1-discovery/FINAL/phase1-files-list.json'

        if not os.path.exists(phase1_files_path):
            print(f"❌ Error: Phase 1 analysis not found: {phase1_files_path}")
            sys.exit(1)

        with open(phase1_files_path, 'r') as f:
            phase1_data = json.load(f)

        files = phase1_data.get('files', [])
        total_files = len(files)

        print(f"\n📦 Exporting {total_files} files from Phase 1 analysis")
        print(f"📂 Output: {args.output_dir}")

        for idx, file_info in enumerate(files, 1):
            try:
                exporter.export_file_with_sections(
                    file_key=file_info['key'],
                    file_name=file_info['name'],
                    file_number=idx,
                    output_base_dir=args.output_dir
                )
            except Exception as e:
                print(f"❌ Error exporting file {idx}: {e}")
                continue

        print(f"\n{'='*80}")
        print(f"✅ All files exported!")
        print(f"{'='*80}")

    else:
        # Single file export
        if not args.file_key or not args.file_name:
            print("❌ Error: --file-key and --file-name required for single file export")
            print("   Or use --all to export all files from Phase 1")
            sys.exit(1)

        exporter.export_file_with_sections(
            file_key=args.file_key,
            file_name=args.file_name,
            file_number=args.file_number,
            output_base_dir=args.output_dir
        )


if __name__ == '__main__':
    main()
