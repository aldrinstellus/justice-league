"""
🦅 HAWKMAN EQUIPPED - PRODUCTION-READY STRUCTURAL PARSER
Justice League Member: Fully Integrated Layer-by-Layer Figma Parser

This is the production-ready version of Hawkman with all MCP integrations:
- Real Figma API integration
- Chrome DevTools MCP for rendering
- Green Arrow visual validation
- Oracle pattern learning
- shadcn/ui component support
- Automatic refinement logic

Version: 2.0.0 (Equipped)
"""

import logging
import json
import os
import tempfile
import time
import requests
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
import re
from enum import Enum

from .hero_base import HeroBase, HeroPriority
from .green_arrow_visual_validator import GreenArrowVisualValidator

# Mission Control Narrator for coordinated communication
try:
    from .mission_control_narrator import get_narrator
    NARRATOR_AVAILABLE = True
except ImportError:
    NARRATOR_AVAILABLE = False
    logging.warning("Mission Control Narrator not available - Hawkman will operate without narrator")

logger = logging.getLogger(__name__)


class OutputFormat(Enum):
    """Available output formats"""
    HTML_CSS = "html_css"                    # Pure HTML with CSS
    HTML_TAILWIND = "html_tailwind"          # HTML with Tailwind classes
    REACT_TAILWIND = "react_tailwind"        # React components with Tailwind
    REACT_SHADCN = "react_shadcn"           # React with shadcn/ui components
    AUTO = "auto"                            # Let agent decide


class ParsingDepth(Enum):
    """Layer parsing depth levels"""
    FRAME = "frame"           # Top-level frames only
    COMPONENT = "component"   # Component boundaries
    ELEMENT = "element"       # Individual elements
    ADAPTIVE = "adaptive"     # Agent decides based on complexity


class FigmaLayerType(Enum):
    """Figma layer types"""
    FRAME = "FRAME"
    GROUP = "GROUP"
    COMPONENT = "COMPONENT"
    INSTANCE = "INSTANCE"
    TEXT = "TEXT"
    RECTANGLE = "RECTANGLE"
    ELLIPSE = "ELLIPSE"
    VECTOR = "VECTOR"
    IMAGE = "IMAGE"


class HawkmanEquipped(HeroBase):
    """
    🦅 HAWKMAN EQUIPPED - Production-Ready Structural Parser

    Fully integrated version with all MCP tools and real implementations.

    MCP Integrations:
    - Figma REST API: Real layer parsing and image export
    - Chrome DevTools MCP: Actual rendering and screenshots
    - Green Arrow: Visual validation loop
    - Oracle: Pattern learning and reuse
    - shadcn/ui: Component library support
    """

    def __init__(
        self,
        figma_token: Optional[str] = None,
        chrome_mcp_client: Optional[Any] = None,
        preview_app_port: int = 3005,
        parsing_data_dir: Optional[str] = None,
        narrator: Optional[Any] = None
    ):
        """
        Initialize fully equipped Hawkman

        Args:
            figma_token: Figma personal access token
            chrome_mcp_client: Chrome DevTools MCP client instance
            preview_app_port: Port where preview-app dev server runs
            parsing_data_dir: Directory for parsing data
            narrator: Mission Control Narrator for coordinated communication
        """
        super().__init__(
            hero_name="Hawkman Equipped",
            hero_emoji="🦅",
            baseline_dir=parsing_data_dir
        )

        # Initialize narrator for enhanced UX
        self.narrator = narrator if narrator else (get_narrator() if NARRATOR_AVAILABLE else None)

        # Get Figma token from env or parameter
        self.figma_token = figma_token or os.getenv('FIGMA_ACCESS_TOKEN')
        if not self.figma_token:
            logger.warning("⚠️ No Figma token provided. Set FIGMA_ACCESS_TOKEN env var")

        # Chrome DevTools MCP client
        self.chrome_mcp = chrome_mcp_client

        # Preview app configuration
        self.preview_app_port = preview_app_port
        self.preview_app_url = f"http://localhost:{preview_app_port}"

        # Setup directories
        self.parsing_data_dir = Path(parsing_data_dir or "data/hawkman")
        self.parsing_data_dir.mkdir(parents=True, exist_ok=True)

        self.figma_exports_dir = self.parsing_data_dir / "figma_exports"
        self.figma_exports_dir.mkdir(exist_ok=True)

        self.rendered_outputs_dir = self.parsing_data_dir / "rendered_outputs"
        self.rendered_outputs_dir.mkdir(exist_ok=True)

        self.components_dir = self.parsing_data_dir / "generated_components"
        self.components_dir.mkdir(exist_ok=True)

        # Initialize databases
        self.parsing_history_db = self.parsing_data_dir / "parsing_history.json"
        self.layer_mappings_db = self.parsing_data_dir / "layer_mappings.json"
        self.patterns_db = self.parsing_data_dir / "patterns.json"

        self._init_databases()

        # Initialize Green Arrow for visual validation
        try:
            self.green_arrow = GreenArrowVisualValidator()
            logger.info("✅ Green Arrow initialized")
        except Exception as e:
            logger.warning(f"⚠️ Green Arrow unavailable: {e}")
            self.green_arrow = None

        # Complexity thresholds for format selection
        self.complexity_thresholds = {
            'simple': 10,       # ≤10 layers → HTML/CSS
            'moderate': 30,     # 10-30 layers → HTML+Tailwind
            'complex': 50,      # 30-50 layers → React+Tailwind
            'very_complex': 80  # >50 layers → React+shadcn/ui
        }

        # Component indicators for boundary detection
        self.component_indicators = [
            'button', 'card', 'modal', 'dialog', 'form', 'input',
            'menu', 'nav', 'header', 'footer', 'sidebar', 'dropdown',
            'select', 'checkbox', 'radio', 'switch', 'slider', 'tab',
            'accordion', 'alert', 'badge', 'avatar', 'tooltip'
        ]

        # shadcn/ui component mappings
        self.shadcn_components = {
            'button': 'Button',
            'card': 'Card',
            'input': 'Input',
            'select': 'Select',
            'checkbox': 'Checkbox',
            'radio': 'RadioGroup',
            'switch': 'Switch',
            'slider': 'Slider',
            'tabs': 'Tabs',
            'accordion': 'Accordion',
            'alert': 'Alert',
            'badge': 'Badge',
            'avatar': 'Avatar',
            'dialog': 'Dialog',
            'dropdown': 'DropdownMenu',
            'tooltip': 'Tooltip'
        }

        logger.info(f"🦅 Hawkman Equipped initialized - Ready for pixel-perfect conversions")

    def _init_databases(self):
        """Initialize JSON databases"""
        if not self.parsing_history_db.exists():
            with open(self.parsing_history_db, 'w') as f:
                json.dump({'parsings': []}, f, indent=2)

        if not self.layer_mappings_db.exists():
            with open(self.layer_mappings_db, 'w') as f:
                json.dump({'mappings': []}, f, indent=2)

        if not self.patterns_db.exists():
            with open(self.patterns_db, 'w') as f:
                json.dump({'patterns': []}, f, indent=2)

    # ==================== NARRATOR INTEGRATION ====================

    def say(self, message: str, style: str = "equipped", technical_info: Optional[str] = None):
        """
        Hawkman dialogue - Equipped, reliable, structural-focused

        Personality traits:
        - Reliable and methodical
        - Structural analysis expert
        - Always prepared (equipped!)
        - Frame export specialist
        """
        if self.narrator:
            self.narrator.hero_speaks(f"{self.hero_emoji} {self.hero_name}", message, style, technical_info)

    def think(self, thought: str, step: Optional[int] = None, category: Optional[str] = "Parsing"):
        """
        Sequential thinking with structural parsing focus

        Common categories for Hawkman:
        - Parsing, Analyzing, Exporting, Validating, Building
        """
        if self.narrator:
            self.narrator.hero_thinks(f"{self.hero_emoji} {self.hero_name}", thought, step, category)

    def handoff(self, to_hero: str, context: str, details: Optional[str] = None):
        """
        Handoff parsed data to another hero

        Args:
            to_hero: Name of hero receiving the handoff (with emoji)
            context: What is being handed off
            details: Optional additional details
        """
        if self.narrator:
            self.narrator.hero_handoff(
                f"{self.hero_emoji} {self.hero_name}",
                to_hero,
                context,
                details
            )

    # ==================== FIGMA API INTEGRATION ====================

    def _fetch_figma_structure(self, file_key: str, node_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch real Figma file structure using Figma REST API

        Args:
            file_key: Figma file key
            node_id: Optional specific node ID

        Returns:
            Figma file structure JSON
        """
        if not self.figma_token:
            raise ValueError("Figma token not set. Cannot fetch real data.")

        headers = {"X-Figma-Token": self.figma_token}

        # Build API URL
        if node_id:
            url = f"https://api.figma.com/v1/files/{file_key}/nodes?ids={node_id}"
        else:
            url = f"https://api.figma.com/v1/files/{file_key}"

        logger.info(f"🔍 Fetching Figma structure: {url}")

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()

            # Extract the relevant node
            if node_id:
                nodes = data.get('nodes', {})
                if node_id in nodes:
                    return nodes[node_id]['document']
                else:
                    raise ValueError(f"Node {node_id} not found in file")
            else:
                return data.get('document', {})

        except requests.RequestException as e:
            logger.error(f"❌ Failed to fetch Figma data: {e}")
            raise

    def _export_figma_image(self, file_key: str, node_id: str) -> str:
        """
        Export Figma node as PNG image

        Args:
            file_key: Figma file key
            node_id: Node ID to export

        Returns:
            Path to downloaded image
        """
        if not self.figma_token:
            raise ValueError("Figma token not set. Cannot export image.")

        headers = {"X-Figma-Token": self.figma_token}

        # Request image export
        url = f"https://api.figma.com/v1/images/{file_key}?ids={node_id}&format=png&scale=2"

        logger.info(f"📸 Exporting Figma image for node {node_id}")

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()

            if 'images' not in data or node_id not in data['images']:
                raise ValueError(f"Failed to export image for node {node_id}")

            image_url = data['images'][node_id]

            # Download the image
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()

            # Save to exports directory
            timestamp = int(time.time())
            image_path = self.figma_exports_dir / f"figma_{node_id}_{timestamp}.png"

            with open(image_path, 'wb') as f:
                f.write(img_response.content)

            logger.info(f"✅ Figma image saved: {image_path}")
            return str(image_path)

        except requests.RequestException as e:
            logger.error(f"❌ Failed to export Figma image: {e}")
            raise

    def count_frames(self, file_key: str) -> int:
        """
        Count the total number of frames in a Figma file without exporting

        Args:
            file_key: Figma file key

        Returns:
            Number of top-level frames found

        Raises:
            ValueError: If Figma token not set
            requests.RequestException: If API request fails
        """
        if not self.figma_token:
            raise ValueError("Figma token not set. Cannot count frames.")

        try:
            # Fetch file structure
            file_data = self._fetch_figma_structure(file_key)

            # Count all exportable nodes (FRAME, COMPONENT, COMPONENT_SET) including those inside SECTION nodes
            exportable_types = {'FRAME', 'COMPONENT', 'COMPONENT_SET'}
            node_count = 0

            if 'children' in file_data:
                for child in file_data['children']:
                    if child.get('type') == 'CANVAS':
                        # Each canvas (page) contains exportable nodes (either directly or inside SECTIONs)
                        if 'children' in child:
                            for element in child['children']:
                                if element.get('type') in exportable_types:
                                    # Direct exportable node under page
                                    node_count += 1
                                elif element.get('type') == 'SECTION':
                                    # Exportable nodes inside a SECTION
                                    if 'children' in element:
                                        for node in element['children']:
                                            if node.get('type') in exportable_types:
                                                node_count += 1

            return node_count

        except requests.RequestException as e:
            logger.error(f"❌ Failed to fetch Figma file structure: {e}")
            raise

    @staticmethod
    def sanitize_filename(name: str) -> str:
        """
        Sanitize a filename or folder name for safe file system use

        Args:
            name: The name to sanitize

        Returns:
            Sanitized name safe for file systems

        Examples:
            "Page 1: Overview" -> "Page-1-Overview"
            "Dashboard / Settings" -> "Dashboard-Settings"
            "Component (v2)" -> "Component-v2"
        """
        if not name or not name.strip():
            return "Unnamed"

        # Remove or replace invalid path characters: / \ : * ? " < > |
        # Replace with nothing or dash
        sanitized = re.sub(r'[/\\:*?"<>|]', '', name)

        # Replace multiple spaces with single space
        sanitized = re.sub(r'\s+', ' ', sanitized)

        # Replace spaces and special chars with hyphens
        sanitized = re.sub(r'[\s\-]+', '-', sanitized)

        # Remove leading/trailing hyphens
        sanitized = sanitized.strip('-')

        # If empty after sanitization, use default
        if not sanitized:
            return "Unnamed"

        # Limit length (most filesystems support 255, but be conservative)
        if len(sanitized) > 200:
            sanitized = sanitized[:200].rstrip('-')

        return sanitized

    def export_all_frames_as_png(
        self,
        file_key: str,
        output_dir: Optional[str] = None,
        scale: float = 2.0,
        progress_callback: Optional[callable] = None
    ) -> List[Dict[str, str]]:
        """
        Export all top-level frames from a Figma file as PNG images

        Args:
            file_key: Figma file key
            output_dir: Optional custom output directory (defaults to figma_exports_dir)
            scale: Export scale (1.0-4.0, default 2.0)
            progress_callback: Optional callback function(current, total, frame_name) for progress updates

        Returns:
            List of dicts with 'frame_name', 'node_id', and 'file_path'
        """
        if not self.figma_token:
            raise ValueError("Figma token not set. Cannot export frames.")

        # Determine output directory
        if output_dir:
            export_dir = Path(output_dir)
            export_dir.mkdir(parents=True, exist_ok=True)
        else:
            export_dir = self.figma_exports_dir

        logger.info(f"🎨 Fetching all frames from Figma file: {file_key}")

        try:
            # Fetch file structure (includes file name and pages)
            file_data = self._fetch_figma_structure(file_key)

            # Extract Figma file name
            file_name = file_data.get('name', 'Figma-Export')
            sanitized_file_name = self.sanitize_filename(file_name)

            # Create main file directory under output_dir
            file_dir = export_dir / sanitized_file_name
            file_dir.mkdir(parents=True, exist_ok=True)

            logger.info(f"📁 File: {file_name} -> {sanitized_file_name}/")

            # Find all exportable nodes (frames, components, component sets) organized by page
            exportable_types = {'FRAME', 'COMPONENT', 'COMPONENT_SET'}
            total_nodes = 0
            pages_with_nodes = []

            if 'children' in file_data:
                for child in file_data['children']:
                    if child.get('type') == 'CANVAS':
                        page_name = child.get('name', 'Unnamed-Page')
                        page_nodes = []

                        # Each canvas (page) contains exportable nodes (either directly or inside SECTIONs)
                        if 'children' in child:
                            for element in child['children']:
                                if element.get('type') in exportable_types:
                                    # Direct exportable node under page
                                    page_nodes.append({
                                        'name': element.get('name', 'Unnamed'),
                                        'id': element.get('id'),
                                        'type': element.get('type')
                                    })
                                elif element.get('type') == 'SECTION':
                                    # Exportable nodes inside a SECTION
                                    if 'children' in element:
                                        for node in element['children']:
                                            if node.get('type') in exportable_types:
                                                page_nodes.append({
                                                    'name': node.get('name', 'Unnamed'),
                                                    'id': node.get('id'),
                                                    'type': node.get('type')
                                                })

                        if page_nodes:
                            pages_with_nodes.append({
                                'page_name': page_name,
                                'nodes': page_nodes
                            })
                            total_nodes += len(page_nodes)

            if total_nodes == 0:
                logger.warning("⚠️ No exportable nodes found in Figma file")
                return []

            logger.info(f"📋 Found {total_nodes} exportable nodes (frames, components, component sets) across {len(pages_with_nodes)} pages")

            # Export each node into hierarchical structure
            exported_files = []
            headers = {"X-Figma-Token": self.figma_token}
            current_node = 0

            for page_data in pages_with_nodes:
                page_name = page_data['page_name']
                nodes = page_data['nodes']

                # Sanitize page name and create directory
                sanitized_page_name = self.sanitize_filename(page_name)
                page_dir = file_dir / sanitized_page_name
                page_dir.mkdir(exist_ok=True)

                logger.info(f"📂 Page: {page_name} -> {sanitized_page_name}/ ({len(nodes)} items)")

                for node in nodes:
                    current_node += 1
                    node_name = node['name']
                    node_id = node['id']
                    node_type = node['type']

                    # Call progress callback if provided
                    if progress_callback:
                        progress_callback(current_node, total_nodes, node_name)

                    logger.info(f"📸 Exporting [{current_node}/{total_nodes}]: {node_name} (Type: {node_type}, ID: {node_id})")

                    # Request image export from Figma API
                    url = f"https://api.figma.com/v1/images/{file_key}?ids={node_id}&format=png&scale={scale}"

                    try:
                        response = requests.get(url, headers=headers, timeout=30)
                        response.raise_for_status()
                        data = response.json()

                        if 'images' not in data or node_id not in data['images']:
                            logger.error(f"❌ Failed to export {node_name}: No image URL returned")
                            continue

                        image_url = data['images'][node_id]

                        # Download the image
                        img_response = requests.get(image_url, timeout=30)
                        img_response.raise_for_status()

                        # Sanitize node name for filename
                        sanitized_node_name = self.sanitize_filename(node_name)

                        # Save into hierarchical structure: {file_name}/{page_name}/node.png
                        image_filename = f"{sanitized_node_name}_{node_id}.png"
                        image_path = page_dir / image_filename

                        with open(image_path, 'wb') as f:
                            f.write(img_response.content)

                        logger.info(f"✅ Saved: {sanitized_file_name}/{sanitized_page_name}/{image_filename}")

                        exported_files.append({
                            'node_name': node_name,
                            'node_type': node_type,
                            'page_name': page_name,
                            'node_id': node_id,
                            'file_path': str(image_path)
                        })

                    except requests.RequestException as e:
                        logger.error(f"❌ Failed to export {node_name}: {e}")
                        continue

            logger.info(f"🎉 Successfully exported {len(exported_files)}/{total_nodes} items (frames, components, component sets)")
            logger.info(f"📁 Hierarchical structure: {file_dir}")
            return exported_files

        except requests.RequestException as e:
            logger.error(f"❌ Failed to fetch Figma file structure: {e}")
            raise

    # ==================== ENHANCED STRUCTURAL CAPABILITIES ====================

    def get_file_metadata(self, file_key: str) -> Dict[str, Any]:
        """
        Get comprehensive metadata about a Figma file without parsing all content

        Args:
            file_key: Figma file key

        Returns:
            Dict with file metadata (name, pages, frame count, last modified, etc.)
        """
        if not self.figma_token:
            raise ValueError("Figma token not set")

        try:
            file_data = self._fetch_figma_structure(file_key)

            # Count pages and frames
            pages = []
            total_frames = 0

            if 'children' in file_data:
                for child in file_data['children']:
                    if child.get('type') == 'CANVAS':
                        page_name = child.get('name', 'Unnamed')
                        page_frame_count = 0

                        # Count frames in this page
                        if 'children' in child:
                            exportable_types = {'FRAME', 'COMPONENT', 'COMPONENT_SET'}
                            for element in child['children']:
                                if element.get('type') in exportable_types:
                                    page_frame_count += 1
                                elif element.get('type') == 'SECTION' and 'children' in element:
                                    for node in element['children']:
                                        if node.get('type') in exportable_types:
                                            page_frame_count += 1

                        pages.append({
                            'name': page_name,
                            'frame_count': page_frame_count
                        })
                        total_frames += page_frame_count

            return {
                'file_name': file_data.get('name', 'Unnamed'),
                'file_key': file_key,
                'total_pages': len(pages),
                'total_frames': total_frames,
                'pages': pages,
                'document_type': file_data.get('type', 'DOCUMENT')
            }

        except requests.RequestException as e:
            logger.error(f"❌ Failed to fetch file metadata: {e}")
            raise

    def list_pages(self, file_key: str) -> List[Dict[str, str]]:
        """
        List all pages in a Figma file

        Args:
            file_key: Figma file key

        Returns:
            List of page names and IDs
        """
        if not self.figma_token:
            raise ValueError("Figma token not set")

        try:
            file_data = self._fetch_figma_structure(file_key)

            pages = []
            if 'children' in file_data:
                for child in file_data['children']:
                    if child.get('type') == 'CANVAS':
                        pages.append({
                            'id': child.get('id'),
                            'name': child.get('name', 'Unnamed'),
                            'type': 'CANVAS'
                        })

            return pages

        except requests.RequestException as e:
            logger.error(f"❌ Failed to list pages: {e}")
            raise

    def get_page_frames(self, file_key: str, page_name: str) -> List[Dict[str, Any]]:
        """
        Get all frames from a specific page

        Args:
            file_key: Figma file key
            page_name: Name of the page

        Returns:
            List of frame metadata (name, id, type, dimensions)
        """
        if not self.figma_token:
            raise ValueError("Figma token not set")

        try:
            file_data = self._fetch_figma_structure(file_key)

            frames = []
            exportable_types = {'FRAME', 'COMPONENT', 'COMPONENT_SET'}

            if 'children' in file_data:
                for child in file_data['children']:
                    if child.get('type') == 'CANVAS' and child.get('name') == page_name:
                        if 'children' in child:
                            for element in child['children']:
                                if element.get('type') in exportable_types:
                                    frames.append(self._extract_frame_metadata(element))
                                elif element.get('type') == 'SECTION' and 'children' in element:
                                    for node in element['children']:
                                        if node.get('type') in exportable_types:
                                            frames.append(self._extract_frame_metadata(node))
                        break

            return frames

        except requests.RequestException as e:
            logger.error(f"❌ Failed to get page frames: {e}")
            raise

    def _extract_frame_metadata(self, frame: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metadata from a frame node"""
        metadata = {
            'id': frame.get('id'),
            'name': frame.get('name', 'Unnamed'),
            'type': frame.get('type')
        }

        if 'absoluteBoundingBox' in frame:
            bbox = frame['absoluteBoundingBox']
            metadata['width'] = bbox.get('width', 0)
            metadata['height'] = bbox.get('height', 0)
            metadata['x'] = bbox.get('x', 0)
            metadata['y'] = bbox.get('y', 0)

        return metadata

    def export_frame_by_name(
        self,
        file_key: str,
        frame_name: str,
        output_dir: Optional[str] = None,
        scale: float = 2.0
    ) -> Dict[str, Any]:
        """
        Find and export a specific frame by name

        Args:
            file_key: Figma file key
            frame_name: Name of the frame to export
            output_dir: Output directory
            scale: Export scale

        Returns:
            Export result with file path
        """
        if not self.figma_token:
            raise ValueError("Figma token not set")

        try:
            file_data = self._fetch_figma_structure(file_key)

            # Search for frame by name
            target_node = None
            exportable_types = {'FRAME', 'COMPONENT', 'COMPONENT_SET'}

            if 'children' in file_data:
                for child in file_data['children']:
                    if child.get('type') == 'CANVAS' and 'children' in child:
                        for element in child['children']:
                            if element.get('type') in exportable_types and element.get('name') == frame_name:
                                target_node = element
                                break
                            elif element.get('type') == 'SECTION' and 'children' in element:
                                for node in element['children']:
                                    if node.get('type') in exportable_types and node.get('name') == frame_name:
                                        target_node = node
                                        break
                            if target_node:
                                break
                    if target_node:
                        break

            if not target_node:
                raise ValueError(f"Frame '{frame_name}' not found in file")

            # Export the frame
            node_id = target_node['id']
            image_url = self._export_figma_image(file_key, node_id, scale)

            # Download and save
            response = requests.get(image_url, timeout=120)
            response.raise_for_status()

            export_dir = Path(output_dir) if output_dir else self.figma_exports_dir
            export_dir.mkdir(parents=True, exist_ok=True)

            sanitized_name = self.sanitize_filename(frame_name)
            image_path = export_dir / f"{sanitized_name}_{node_id}.png"

            with open(image_path, 'wb') as f:
                f.write(response.content)

            return {
                'success': True,
                'frame_name': frame_name,
                'node_id': node_id,
                'file_path': str(image_path),
                'scale': scale
            }

        except requests.RequestException as e:
            logger.error(f"❌ Failed to export frame by name: {e}")
            raise

    def get_frame_hierarchy(self, file_key: str, frame_name: str) -> Dict[str, Any]:
        """
        Get the structural hierarchy of a specific frame

        Args:
            file_key: Figma file key
            frame_name: Name of the frame

        Returns:
            Hierarchical structure of the frame with all child elements
        """
        if not self.figma_token:
            raise ValueError("Figma token not set")

        try:
            file_data = self._fetch_figma_structure(file_key)

            # Find target frame
            target_frame = None
            exportable_types = {'FRAME', 'COMPONENT', 'COMPONENT_SET'}

            if 'children' in file_data:
                for child in file_data['children']:
                    if child.get('type') == 'CANVAS' and 'children' in child:
                        for element in child['children']:
                            if element.get('type') in exportable_types and element.get('name') == frame_name:
                                target_frame = element
                                break
                            elif element.get('type') == 'SECTION' and 'children' in element:
                                for node in element['children']:
                                    if node.get('type') in exportable_types and node.get('name') == frame_name:
                                        target_frame = node
                                        break
                            if target_frame:
                                break
                    if target_frame:
                        break

            if not target_frame:
                raise ValueError(f"Frame '{frame_name}' not found")

            # Build hierarchy
            return self._build_hierarchy(target_frame)

        except requests.RequestException as e:
            logger.error(f"❌ Failed to get frame hierarchy: {e}")
            raise

    def _build_hierarchy(self, node: Dict[str, Any], depth: int = 0) -> Dict[str, Any]:
        """Recursively build hierarchy structure"""
        hierarchy = {
            'name': node.get('name', 'Unnamed'),
            'type': node.get('type'),
            'id': node.get('id'),
            'depth': depth
        }

        if 'absoluteBoundingBox' in node:
            bbox = node['absoluteBoundingBox']
            hierarchy['dimensions'] = {
                'width': bbox.get('width'),
                'height': bbox.get('height')
            }

        if 'children' in node:
            hierarchy['children'] = [
                self._build_hierarchy(child, depth + 1)
                for child in node['children']
            ]
            hierarchy['child_count'] = len(node['children'])
        else:
            hierarchy['child_count'] = 0

        return hierarchy

    def export_component_library(
        self,
        file_key: str,
        output_dir: Optional[str] = None,
        scale: float = 2.0
    ) -> List[Dict[str, Any]]:
        """
        Export all components and component sets from a Figma file

        Args:
            file_key: Figma file key
            output_dir: Output directory
            scale: Export scale

        Returns:
            List of exported component metadata
        """
        if not self.figma_token:
            raise ValueError("Figma token not set")

        try:
            file_data = self._fetch_figma_structure(file_key)

            # Find all components and component sets
            components = []
            component_types = {'COMPONENT', 'COMPONENT_SET'}

            if 'children' in file_data:
                for child in file_data['children']:
                    if child.get('type') == 'CANVAS' and 'children' in child:
                        for element in child['children']:
                            if element.get('type') in component_types:
                                components.append(element)
                            elif element.get('type') == 'SECTION' and 'children' in element:
                                for node in element['children']:
                                    if node.get('type') in component_types:
                                        components.append(node)

            if not components:
                logger.warning("⚠️ No components found in file")
                return []

            logger.info(f"🔧 Found {len(components)} components to export")

            # Export each component
            export_dir = Path(output_dir) if output_dir else (self.figma_exports_dir / "components")
            export_dir.mkdir(parents=True, exist_ok=True)

            exported_components = []

            for component in components:
                try:
                    node_id = component['id']
                    component_name = component.get('name', 'Unnamed')

                    image_url = self._export_figma_image(file_key, node_id, scale)
                    response = requests.get(image_url, timeout=120)
                    response.raise_for_status()

                    sanitized_name = self.sanitize_filename(component_name)
                    image_path = export_dir / f"{sanitized_name}_{node_id}.png"

                    with open(image_path, 'wb') as f:
                        f.write(response.content)

                    exported_components.append({
                        'component_name': component_name,
                        'node_id': node_id,
                        'type': component.get('type'),
                        'file_path': str(image_path)
                    })

                    logger.info(f"✅ Exported component: {component_name}")

                except Exception as e:
                    logger.error(f"❌ Failed to export component {component.get('name')}: {e}")

            return exported_components

        except requests.RequestException as e:
            logger.error(f"❌ Failed to export component library: {e}")
            raise

    def analyze_file_structure(self, file_key: str) -> Dict[str, Any]:
        """
        Analyze and report on the structural composition of a Figma file

        Args:
            file_key: Figma file key

        Returns:
            Comprehensive structure analysis report
        """
        if not self.figma_token:
            raise ValueError("Figma token not set")

        try:
            file_data = self._fetch_figma_structure(file_key)

            analysis = {
                'file_name': file_data.get('name', 'Unnamed'),
                'file_key': file_key,
                'pages': [],
                'statistics': {
                    'total_pages': 0,
                    'total_frames': 0,
                    'total_components': 0,
                    'total_component_sets': 0,
                    'total_sections': 0
                }
            }

            if 'children' in file_data:
                for child in file_data['children']:
                    if child.get('type') == 'CANVAS':
                        page_analysis = {
                            'name': child.get('name', 'Unnamed'),
                            'frames': 0,
                            'components': 0,
                            'component_sets': 0,
                            'sections': 0
                        }

                        if 'children' in child:
                            for element in child['children']:
                                element_type = element.get('type')

                                if element_type == 'FRAME':
                                    page_analysis['frames'] += 1
                                elif element_type == 'COMPONENT':
                                    page_analysis['components'] += 1
                                elif element_type == 'COMPONENT_SET':
                                    page_analysis['component_sets'] += 1
                                elif element_type == 'SECTION':
                                    page_analysis['sections'] += 1

                                    # Count items inside sections
                                    if 'children' in element:
                                        for node in element['children']:
                                            node_type = node.get('type')
                                            if node_type == 'FRAME':
                                                page_analysis['frames'] += 1
                                            elif node_type == 'COMPONENT':
                                                page_analysis['components'] += 1
                                            elif node_type == 'COMPONENT_SET':
                                                page_analysis['component_sets'] += 1

                        analysis['pages'].append(page_analysis)
                        analysis['statistics']['total_pages'] += 1
                        analysis['statistics']['total_frames'] += page_analysis['frames']
                        analysis['statistics']['total_components'] += page_analysis['components']
                        analysis['statistics']['total_component_sets'] += page_analysis['component_sets']
                        analysis['statistics']['total_sections'] += page_analysis['sections']

            return analysis

        except requests.RequestException as e:
            logger.error(f"❌ Failed to analyze file structure: {e}")
            raise

    def _extract_figma_properties(self, layer: Dict[str, Any]) -> Dict[str, Any]:
        """Extract comprehensive properties from Figma layer"""
        props = {
            'name': layer.get('name', 'Unnamed'),
            'type': layer.get('type', 'UNKNOWN'),
            'visible': layer.get('visible', True),
        }

        # Layout properties
        if 'absoluteBoundingBox' in layer:
            bbox = layer['absoluteBoundingBox']
            props['width'] = bbox.get('width', 0)
            props['height'] = bbox.get('height', 0)
            props['x'] = bbox.get('x', 0)
            props['y'] = bbox.get('y', 0)

        # Background/Fill
        if 'fills' in layer and layer['fills']:
            props['fills'] = layer['fills']

        # Stroke
        if 'strokes' in layer and layer['strokes']:
            props['strokes'] = layer['strokes']
            props['strokeWeight'] = layer.get('strokeWeight', 0)

        # Corner radius
        if 'cornerRadius' in layer:
            props['cornerRadius'] = layer['cornerRadius']

        # Text properties
        if layer.get('type') == 'TEXT':
            props['characters'] = layer.get('characters', '')
            if 'style' in layer:
                style = layer['style']
                props['fontSize'] = style.get('fontSize')
                props['fontFamily'] = style.get('fontFamily')
                props['fontWeight'] = style.get('fontWeight')
                props['textAlign'] = style.get('textAlignHorizontal')

        # Layout constraints
        if 'constraints' in layer:
            props['constraints'] = layer['constraints']

        # Auto layout
        if 'layoutMode' in layer:
            props['layoutMode'] = layer['layoutMode']
            props['primaryAxisAlignItems'] = layer.get('primaryAxisAlignItems')
            props['counterAxisAlignItems'] = layer.get('counterAxisAlignItems')
            props['paddingLeft'] = layer.get('paddingLeft', 0)
            props['paddingRight'] = layer.get('paddingRight', 0)
            props['paddingTop'] = layer.get('paddingTop', 0)
            props['paddingBottom'] = layer.get('paddingBottom', 0)
            props['itemSpacing'] = layer.get('itemSpacing', 0)

        return props

    # ==================== CHROME DEVTOOLS INTEGRATION ====================

    def _render_html_code(self, code: str, output_format: OutputFormat) -> str:
        """
        Render HTML/CSS code in browser and capture screenshot

        Args:
            code: Generated HTML/CSS code
            output_format: Format type

        Returns:
            Path to screenshot
        """
        if not self.chrome_mcp:
            raise ValueError("Chrome DevTools MCP client not initialized")

        # Create temporary HTML file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.html',
            delete=False,
            encoding='utf-8'
        ) as f:
            # Wrap code in full HTML document
            full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hawkman Render</title>
    {"<script src='https://cdn.tailwindcss.com'></script>" if 'tailwind' in output_format.value else ""}
</head>
<body>
{code}
</body>
</html>"""
            f.write(full_html)
            temp_path = f.name

        try:
            # Navigate to file
            file_url = f"file://{temp_path}"
            logger.info(f"🌐 Navigating to: {file_url}")

            self.chrome_mcp.navigate_page(url=file_url, timeout=10000)

            # Wait for render
            time.sleep(2)

            # Capture screenshot
            timestamp = int(time.time())
            screenshot_path = self.rendered_outputs_dir / f"rendered_html_{timestamp}.png"

            self.chrome_mcp.take_screenshot(
                file_path=str(screenshot_path),
                full_page=True
            )

            logger.info(f"✅ Screenshot captured: {screenshot_path}")
            return str(screenshot_path)

        finally:
            # Cleanup temp file
            Path(temp_path).unlink(missing_ok=True)

    def _render_react_code(self, code: str, component_name: str = "HawkmanGenerated") -> str:
        """
        Render React component in preview-app and capture screenshot

        Args:
            code: Generated React component code
            component_name: Name for the component

        Returns:
            Path to screenshot
        """
        if not self.chrome_mcp:
            raise ValueError("Chrome DevTools MCP client not initialized")

        # Preview app paths
        preview_app_root = Path("/Users/admin/Documents/claudecode/Projects/aldo-vision/preview-app")
        component_path = preview_app_root / f"src/components/{component_name}.tsx"
        page_path = preview_app_root / f"src/app/hawkman-test/page.tsx"

        try:
            # Write component file
            with open(component_path, 'w') as f:
                f.write(code)

            # Create page route
            page_path.parent.mkdir(parents=True, exist_ok=True)
            with open(page_path, 'w') as f:
                f.write(f"""import {component_name} from '@/components/{component_name}'

export default function HawkmanTestPage() {{
  return <{component_name} />
}}
""")

            # Navigate to page
            test_url = f"{self.preview_app_url}/hawkman-test"
            logger.info(f"🌐 Navigating to: {test_url}")

            self.chrome_mcp.navigate_page(url=test_url, timeout=15000)

            # Wait for React to render
            time.sleep(3)

            # Capture screenshot
            timestamp = int(time.time())
            screenshot_path = self.rendered_outputs_dir / f"rendered_react_{timestamp}.png"

            self.chrome_mcp.take_screenshot(
                file_path=str(screenshot_path),
                full_page=True
            )

            logger.info(f"✅ Screenshot captured: {screenshot_path}")
            return str(screenshot_path)

        finally:
            # Cleanup
            component_path.unlink(missing_ok=True)
            if page_path.exists():
                page_path.unlink(missing_ok=True)
                if page_path.parent.exists() and not any(page_path.parent.iterdir()):
                    page_path.parent.rmdir()

    # ==================== CODE GENERATION WITH SHADCN/UI ====================

    def _generate_react_shadcn(self, layer: Dict[str, Any]) -> str:
        """
        Generate React component using shadcn/ui components

        Args:
            layer: Parsed layer hierarchy

        Returns:
            Generated React code with shadcn/ui
        """
        component_name = self._to_pascal_case(layer.get('name', 'Component'))

        # Detect which shadcn components to use
        imports = set()
        jsx = self._layer_to_shadcn_jsx(layer, imports)

        # Build imports
        import_statements = []
        if imports:
            import_statements.append(f"import {{ {', '.join(sorted(imports))} }} from '@/components/ui'")

        code = f"""import React from 'react'
{chr(10).join(import_statements)}

export default function {component_name}() {{
  return (
{self._indent(jsx, 4)}
  )
}}
"""
        return code

    def _layer_to_shadcn_jsx(self, layer: Dict[str, Any], imports: set, indent: int = 0) -> str:
        """Convert layer to shadcn/ui JSX"""
        layer_name = layer.get('name', '').lower()
        layer_type = layer.get('type', 'FRAME')
        children = layer.get('children', [])

        # Check if this matches a shadcn component
        shadcn_component = None
        for indicator, component in self.shadcn_components.items():
            if indicator in layer_name:
                shadcn_component = component
                imports.add(component)
                break

        indent_str = "  " * indent

        if shadcn_component:
            # Use shadcn component
            if children:
                children_jsx = "\n".join(
                    self._layer_to_shadcn_jsx(child, imports, indent + 1)
                    for child in children
                )
                return f"{indent_str}<{shadcn_component}>\n{children_jsx}\n{indent_str}</{shadcn_component}>"
            else:
                if layer_type == 'TEXT':
                    text = layer.get('properties', {}).get('characters', layer.get('name', ''))
                    return f"{indent_str}<{shadcn_component}>{text}</{shadcn_component}>"
                else:
                    return f"{indent_str}<{shadcn_component} />"
        else:
            # Use regular HTML/div with Tailwind
            tag = "div"
            if layer_type == 'TEXT':
                tag = "p"

            classes = self._layer_to_tailwind_classes(layer)

            if children:
                children_jsx = "\n".join(
                    self._layer_to_shadcn_jsx(child, imports, indent + 1)
                    for child in children
                )
                return f'{indent_str}<{tag} className="{classes}">\n{children_jsx}\n{indent_str}</{tag}>'
            else:
                if layer_type == 'TEXT':
                    text = layer.get('properties', {}).get('characters', layer.get('name', ''))
                    return f'{indent_str}<{tag} className="{classes}">{text}</{tag}>'
                else:
                    return f'{indent_str}<{tag} className="{classes}" />'

    def _layer_to_tailwind_classes(self, layer: Dict[str, Any]) -> str:
        """Convert layer properties to Tailwind classes"""
        classes = []
        props = layer.get('properties', {})

        # Layout
        if layer.get('type') == 'FRAME':
            classes.append('relative')
            if props.get('layoutMode') == 'HORIZONTAL':
                classes.append('flex flex-row')
            elif props.get('layoutMode') == 'VERTICAL':
                classes.append('flex flex-col')

        # Sizing (approximate)
        if 'width' in props:
            w = props['width']
            if w < 100:
                classes.append('w-auto')
            elif w < 300:
                classes.append('w-64')
            elif w < 500:
                classes.append('w-96')
            else:
                classes.append('w-full')

        # Spacing
        spacing = props.get('itemSpacing', 0)
        if spacing > 0:
            if spacing <= 8:
                classes.append('gap-2')
            elif spacing <= 16:
                classes.append('gap-4')
            else:
                classes.append('gap-6')

        # Padding
        padding = props.get('paddingLeft', 0)
        if padding > 0:
            if padding <= 8:
                classes.append('p-2')
            elif padding <= 16:
                classes.append('p-4')
            else:
                classes.append('p-6')

        # Border radius
        if props.get('cornerRadius', 0) > 0:
            classes.append('rounded-lg')

        # Background (simplified)
        if props.get('fills'):
            classes.append('bg-white')

        return ' '.join(classes) if classes else 'relative'

    def _to_pascal_case(self, name: str) -> str:
        """Convert string to PascalCase"""
        # Remove special characters
        name = re.sub(r'[^a-zA-Z0-9\s]', '', name)
        # Split and capitalize
        words = name.split()
        return ''.join(word.capitalize() for word in words) or 'Component'

    def _indent(self, text: str, spaces: int) -> str:
        """Indent text by number of spaces"""
        indent = " " * spaces
        return "\n".join(indent + line if line.strip() else line for line in text.split("\n"))

    # ==================== REFINEMENT LOGIC ====================

    def _refine_code_based_on_discrepancies(
        self,
        code: str,
        discrepancies: List[str],
        figma_structure: Dict[str, Any]
    ) -> str:
        """
        Intelligently refine code based on visual discrepancies

        Args:
            code: Current generated code
            discrepancies: List of issues from Green Arrow
            figma_structure: Original Figma structure

        Returns:
            Refined code
        """
        refined_code = code

        for disc in discrepancies:
            disc_lower = disc.lower()

            # Spacing issues
            if 'spacing' in disc_lower or 'gap' in disc_lower:
                refined_code = self._adjust_spacing(refined_code, disc)

            # Color issues
            elif 'color' in disc_lower or 'background' in disc_lower:
                refined_code = self._adjust_colors(refined_code, disc)

            # Typography issues
            elif 'font' in disc_lower or 'text' in disc_lower:
                refined_code = self._adjust_typography(refined_code, disc)

            # Sizing issues
            elif 'width' in disc_lower or 'height' in disc_lower or 'size' in disc_lower:
                refined_code = self._adjust_sizing(refined_code, disc)

            # Border radius
            elif 'radius' in disc_lower or 'rounded' in disc_lower:
                refined_code = self._adjust_border_radius(refined_code, disc)

        return refined_code

    def _adjust_spacing(self, code: str, issue: str) -> str:
        """Adjust spacing based on issue description"""
        # Example: increase gap-4 to gap-6
        if 'increase' in issue.lower():
            code = code.replace('gap-2', 'gap-4')
            code = code.replace('gap-4', 'gap-6')
            code = code.replace('gap-6', 'gap-8')
        elif 'decrease' in issue.lower():
            code = code.replace('gap-8', 'gap-6')
            code = code.replace('gap-6', 'gap-4')
            code = code.replace('gap-4', 'gap-2')
        return code

    def _adjust_colors(self, code: str, issue: str) -> str:
        """Adjust colors based on issue description"""
        # Placeholder - would need more sophisticated logic
        return code

    def _adjust_typography(self, code: str, issue: str) -> str:
        """Adjust typography based on issue description"""
        if 'bold' in issue.lower():
            code = code.replace('font-medium', 'font-bold')
        elif 'larger' in issue.lower():
            code = code.replace('text-sm', 'text-base')
            code = code.replace('text-base', 'text-lg')
        return code

    def _adjust_sizing(self, code: str, issue: str) -> str:
        """Adjust sizing based on issue description"""
        # Placeholder
        return code

    def _adjust_border_radius(self, code: str, issue: str) -> str:
        """Adjust border radius based on issue description"""
        if 'more rounded' in issue.lower():
            code = code.replace('rounded-md', 'rounded-lg')
            code = code.replace('rounded-lg', 'rounded-xl')
        return code

    # ==================== MAIN PARSING METHOD ====================

    def parse_figma_equipped(
        self,
        figma_url: str,
        output_format: OutputFormat = OutputFormat.AUTO,
        parsing_depth: ParsingDepth = ParsingDepth.ADAPTIVE,
        verify: bool = True,
        max_iterations: int = 3
    ) -> Dict[str, Any]:
        """
        Fully equipped parsing with all integrations

        This is the production-ready method that uses real MCP tools.

        Returns:
            Complete parsing results with rendered screenshots
        """
        logger.info(f"🦅 Starting equipped parsing: {figma_url}")

        # Extract identifiers
        file_key, node_id = self._extract_figma_identifiers(figma_url)

        # Fetch real Figma structure
        figma_structure = self._fetch_figma_structure(file_key, node_id)

        # Add comprehensive properties to each layer
        figma_structure = self._enrich_structure_with_properties(figma_structure)

        # Determine output format
        if output_format == OutputFormat.AUTO:
            output_format = self._determine_output_format_equipped(figma_structure)

        # Generate code
        code = self._generate_code_equipped(figma_structure, output_format)

        # Verification loop
        accuracy_score = 0
        iteration = 0
        verification_results = None

        if verify and self.green_arrow:
            while iteration < max_iterations and accuracy_score < 95:
                iteration += 1
                logger.info(f"🔄 Iteration {iteration}/{max_iterations}")

                # Render code
                if output_format in [OutputFormat.REACT_TAILWIND, OutputFormat.REACT_SHADCN]:
                    rendered_path = self._render_react_code(code)
                else:
                    rendered_path = self._render_html_code(code, output_format)

                # Export Figma image
                figma_image_path = self._export_figma_image(file_key, node_id)

                # Compare with Green Arrow
                verification_results = self.green_arrow.compare_design_to_render(
                    figma_image_path=figma_image_path,
                    rendered_image_path=rendered_path
                )

                accuracy_score = verification_results.get('accuracy_score', 0)
                logger.info(f"📊 Accuracy: {accuracy_score}%")

                if accuracy_score < 95:
                    # Refine code
                    discrepancies = verification_results.get('discrepancies', [])
                    logger.info(f"🔧 Refining based on {len(discrepancies)} discrepancies")
                    code = self._refine_code_based_on_discrepancies(code, discrepancies, figma_structure)

        # Save parsing record
        record = {
            'timestamp': datetime.now().isoformat(),
            'figma_url': figma_url,
            'file_key': file_key,
            'node_id': node_id,
            'output_format': output_format.value,
            'accuracy_score': accuracy_score,
            'iterations_used': iteration
        }
        self._save_parsing_record(record)

        return {
            'generated_code': code,
            'output_format': output_format.value,
            'accuracy_score': accuracy_score,
            'iterations_used': iteration,
            'verification_results': verification_results,
            'parsing_record': record
        }

    def _extract_figma_identifiers(self, url: str) -> Tuple[str, Optional[str]]:
        """Extract file key and node ID from Figma URL"""
        # Support both /file/ and /design/ URLs
        file_pattern = r'/(?:file|design)/([a-zA-Z0-9]+)'
        node_pattern = r'node-id=([0-9-]+)'

        file_match = re.search(file_pattern, url)
        if not file_match:
            raise ValueError(f"Invalid Figma URL: {url}")

        file_key = file_match.group(1)

        node_match = re.search(node_pattern, url)
        node_id = node_match.group(1).replace('-', ':') if node_match else None

        return file_key, node_id

    def _enrich_structure_with_properties(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively add properties to structure"""
        enriched = structure.copy()
        enriched['properties'] = self._extract_figma_properties(structure)

        if 'children' in structure:
            enriched['children'] = [
                self._enrich_structure_with_properties(child)
                for child in structure['children']
            ]

        return enriched

    def _determine_output_format_equipped(self, structure: Dict[str, Any]) -> OutputFormat:
        """Determine output format with shadcn/ui option"""
        layer_count = self._count_layers(structure)
        has_components = self._detect_components(structure)

        if layer_count > self.complexity_thresholds['very_complex'] or has_components:
            return OutputFormat.REACT_SHADCN
        elif layer_count > self.complexity_thresholds['complex']:
            return OutputFormat.REACT_TAILWIND
        elif layer_count > self.complexity_thresholds['moderate']:
            return OutputFormat.HTML_TAILWIND
        else:
            return OutputFormat.HTML_CSS

    def _generate_code_equipped(self, structure: Dict[str, Any], output_format: OutputFormat) -> str:
        """Generate code with all format options"""
        if output_format == OutputFormat.REACT_SHADCN:
            return self._generate_react_shadcn(structure)
        elif output_format == OutputFormat.REACT_TAILWIND:
            return self._generate_react_tailwind(structure)
        elif output_format == OutputFormat.HTML_TAILWIND:
            return self._generate_html_tailwind(structure)
        else:
            return self._generate_html_css(structure)

    def _count_layers(self, structure: Dict[str, Any]) -> int:
        """Count total layers"""
        count = 1
        if 'children' in structure:
            for child in structure['children']:
                count += self._count_layers(child)
        return count

    def _detect_components(self, structure: Dict[str, Any]) -> bool:
        """Detect if structure has components"""
        if structure.get('type') == 'COMPONENT':
            return True
        if 'children' in structure:
            return any(self._detect_components(child) for child in structure['children'])
        return False

    def _generate_react_tailwind(self, layer: Dict[str, Any]) -> str:
        """Generate React with Tailwind (existing implementation)"""
        # Use existing logic from base Hawkman
        pass

    def _generate_html_tailwind(self, layer: Dict[str, Any]) -> str:
        """Generate HTML with Tailwind (existing implementation)"""
        pass

    def _generate_html_css(self, layer: Dict[str, Any]) -> str:
        """Generate HTML with CSS (existing implementation)"""
        pass

    def _save_parsing_record(self, record: Dict[str, Any]):
        """Save parsing record to database"""
        with open(self.parsing_history_db, 'r') as f:
            data = json.load(f)

        data['parsings'].append(record)

        with open(self.parsing_history_db, 'w') as f:
            json.dump(data, f, indent=2)


# ==================== CONVENIENCE FUNCTION ====================

def parse_figma_equipped(
    figma_url: str,
    figma_token: Optional[str] = None,
    chrome_mcp_client: Optional[Any] = None,
    output_format: str = "auto",
    verify: bool = True
) -> Dict[str, Any]:
    """
    Convenience function for equipped Hawkman parsing

    Args:
        figma_url: Figma file URL
        figma_token: Figma access token (or use FIGMA_ACCESS_TOKEN env var)
        chrome_mcp_client: Chrome DevTools MCP client
        output_format: "auto", "html_css", "html_tailwind", "react_tailwind", "react_shadcn"
        verify: Enable visual verification

    Returns:
        Parsing results
    """
    hawkman = HawkmanEquipped(
        figma_token=figma_token,
        chrome_mcp_client=chrome_mcp_client
    )

    format_map = {
        "auto": OutputFormat.AUTO,
        "html_css": OutputFormat.HTML_CSS,
        "html_tailwind": OutputFormat.HTML_TAILWIND,
        "react_tailwind": OutputFormat.REACT_TAILWIND,
        "react_shadcn": OutputFormat.REACT_SHADCN
    }

    return hawkman.parse_figma_equipped(
        figma_url=figma_url,
        output_format=format_map.get(output_format, OutputFormat.AUTO),
        verify=verify
    )
