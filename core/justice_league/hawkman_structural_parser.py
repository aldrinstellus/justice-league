"""
🦅 HAWKMAN - THE STRUCTURAL PARSING SPECIALIST
Justice League Member: Layer-by-Layer Figma Parser & Archaeological Precision Master

Carter Hall's Hawkman - Master of Structural Analysis, Layer Traversal, and Adaptive Code Generation

Powers:
- 🦅 Layer-by-Layer Parsing - Traverse Figma hierarchies with archaeological precision
- 🔍 Adaptive Depth Analysis - Determine optimal parsing granularity automatically
- 🎨 Format Intelligence - Choose HTML/CSS or React based on complexity
- 📐 Structural Mapping - Convert Figma layers to semantic HTML structure
- ✅ Visual Verification - Integrate with Green Arrow for accuracy validation
- 🔄 Iterative Refinement - Auto-improve until 95%+ accuracy achieved
- 🧠 Pattern Recognition - Learn and reuse structural patterns
- 📊 Hierarchy Analysis - Maintain parent-child relationships precisely

"Every layer, every frame, every element - parsed with archaeological precision." - Hawkman

Architecture: Figma MCP + Chrome DevTools MCP + Green Arrow Integration + Oracle Learning
Integration: Works independently or coordinated by Superman
"""

import logging
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
import re
from enum import Enum

from .hero_base import HeroBase, HeroPriority
# Assuming we have access to Green Arrow
from .green_arrow_visual_validator import GreenArrowVisualValidator

logger = logging.getLogger(__name__)


class OutputFormat(Enum):
    """Available output formats"""
    HTML_CSS = "html_css"           # Pure HTML with CSS
    HTML_TAILWIND = "html_tailwind" # HTML with Tailwind classes
    REACT_TAILWIND = "react_tailwind" # React components with Tailwind
    AUTO = "auto"                   # Let agent decide


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
    VECTOR = "VECTOR"
    IMAGE = "IMAGE"


class HawkmanStructuralParser(HeroBase):
    """
    🦅 HAWKMAN - The Structural Parser Specialist

    Carter Hall parses Figma files layer by layer with archaeological precision,
    converting each structural element to appropriate code while maintaining
    design fidelity through visual verification.

    Powers:
    1. Figma Layer Traversal - Parse hierarchical layer structure
    2. Adaptive Format Selection - Choose output format based on complexity
    3. Structural Code Generation - Convert layers to semantic HTML/React
    4. Visual Verification Loop - Compare rendered output with Figma export
    5. Auto-Refinement - Iteratively improve until 95%+ accuracy
    6. Pattern Learning - Identify and reuse common structures

    MCP Integrations:
    - Figma MCP: Layer parsing and image export
    - Chrome DevTools MCP: Render and inspect generated code
    - Green Arrow: Visual validation and accuracy scoring
    - Oracle: Pattern storage and reuse
    """

    def __init__(self, parsing_data_dir: Optional[str] = None):
        """
        Initialize Hawkman's structural parsing capabilities

        Args:
            parsing_data_dir: Directory for parsing data and reports
        """
        super().__init__(
            hero_name="Hawkman",
            hero_emoji="🦅",
            baseline_dir=parsing_data_dir
        )

        self.parsing_data_dir = Path(parsing_data_dir) if parsing_data_dir else Path('/Users/admin/Documents/claudecode/Projects/aldo-vision/data/hawkman')
        self.parsing_data_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Green Arrow for visual validation
        self.green_arrow = GreenArrowVisualValidator()

        # Parsing history database
        self.parsing_history_db = self.parsing_data_dir / 'parsing_history.json'
        self.layer_mappings_db = self.parsing_data_dir / 'layer_mappings.json'
        self.patterns_db = self.parsing_data_dir / 'structural_patterns.json'

        # Initialize databases
        self._init_databases()

        # Format selection intelligence
        self.complexity_thresholds = {
            'simple': 10,      # < 10 layers = HTML/CSS
            'moderate': 30,    # 10-30 layers = HTML + Tailwind
            'complex': 100     # > 30 layers = React + Tailwind
        }

        # Adaptive depth configuration
        self.depth_config = {
            'max_children_per_level': 15,  # If more, go deeper
            'max_nesting_depth': 8,        # Stop at this depth
            'component_indicators': [       # Patterns suggesting component boundary
                'button', 'card', 'modal', 'dialog', 'form', 'menu', 'nav'
            ]
        }

        # Accuracy targets
        self.accuracy_targets = {
            'minimum': 90,     # 90% minimum acceptable
            'target': 95,      # 95% target accuracy
            'excellent': 98    # 98%+ = excellent
        }

        logger.info("🦅 HAWKMAN - Structural Parser initialized")
        logger.info(f"🦅 Parsing Data: {self.parsing_data_dir}")
        logger.info("🦅 Ready to parse Figma layers with precision")

    def _init_databases(self):
        """Initialize all parsing databases"""
        databases = [
            (self.parsing_history_db, {'parsings': []}),
            (self.layer_mappings_db, {'mappings': []}),
            (self.patterns_db, {'patterns': []})
        ]

        for db_path, default_data in databases:
            if not db_path.exists():
                with open(db_path, 'w') as f:
                    json.dump(default_data, f, indent=2)

    def parse_figma(
        self,
        figma_url: str,
        output_format: OutputFormat = OutputFormat.AUTO,
        parsing_depth: ParsingDepth = ParsingDepth.ADAPTIVE,
        verify: bool = True,
        max_iterations: int = 3
    ) -> Dict[str, Any]:
        """
        Parse Figma file layer by layer and generate code

        Args:
            figma_url: Figma file URL
            output_format: Desired output format (auto-detect if AUTO)
            parsing_depth: How deep to parse (adaptive if ADAPTIVE)
            verify: Enable visual verification with Green Arrow
            max_iterations: Maximum refinement iterations

        Returns:
            Dict containing generated code, layer structure, accuracy scores
        """
        logger.info(f"🦅 HAWKMAN: Starting layer-by-layer parsing")
        logger.info(f"🦅 Figma URL: {figma_url}")
        logger.info(f"🦅 Output Format: {output_format.value}")
        logger.info(f"🦅 Parsing Depth: {parsing_depth.value}")

        # Extract Figma file key and node ID
        file_key, node_id = self._extract_figma_identifiers(figma_url)

        # Step 1: Fetch Figma file structure via API/MCP
        figma_structure = self._fetch_figma_structure(file_key, node_id)

        # Step 2: Analyze complexity and determine output format
        if output_format == OutputFormat.AUTO:
            output_format = self._determine_output_format(figma_structure)
            logger.info(f"🦅 Auto-selected format: {output_format.value}")

        # Step 3: Determine parsing depth
        if parsing_depth == ParsingDepth.ADAPTIVE:
            parsing_depth = self._determine_parsing_depth(figma_structure)
            logger.info(f"🦅 Adaptive depth: {parsing_depth.value}")

        # Step 4: Parse layer hierarchy
        layer_hierarchy = self._parse_layer_hierarchy(
            figma_structure,
            depth=parsing_depth
        )

        # Step 5: Generate code from layers
        generated_code = self._generate_code_from_layers(
            layer_hierarchy,
            output_format=output_format
        )

        # Step 6: Visual verification (if enabled)
        accuracy_score = 0
        verification_results = {}

        if verify:
            logger.info("🦅 Starting visual verification with Green Arrow...")

            for iteration in range(max_iterations):
                # Export Figma as image
                figma_image_path = self._export_figma_image(file_key, node_id)

                # Render generated code
                rendered_image_path = self._render_generated_code(
                    generated_code,
                    output_format
                )

                # Compare with Green Arrow
                verification_results = self.green_arrow.validate_conversion(
                    figma_image=figma_image_path,
                    rendered_image=rendered_image_path,
                    code=generated_code
                )

                accuracy_score = verification_results.get('accuracy_score', 0)
                logger.info(f"🦅 Iteration {iteration + 1}: {accuracy_score}% accuracy")

                # If accuracy met, break
                if accuracy_score >= self.accuracy_targets['target']:
                    logger.info(f"🦅 Target accuracy achieved: {accuracy_score}%")
                    break

                # Otherwise, refine code
                if iteration < max_iterations - 1:
                    logger.info("🦅 Refining code based on discrepancies...")
                    generated_code = self._refine_code(
                        generated_code,
                        verification_results.get('discrepancies', []),
                        output_format
                    )

        # Step 7: Save parsing history
        parsing_record = {
            'timestamp': datetime.now().isoformat(),
            'figma_url': figma_url,
            'file_key': file_key,
            'node_id': node_id,
            'output_format': output_format.value,
            'parsing_depth': parsing_depth.value,
            'layer_count': self._count_layers(layer_hierarchy),
            'accuracy_score': accuracy_score,
            'iterations_used': iteration + 1 if verify else 0,
            'verification_enabled': verify
        }

        self._save_parsing_record(parsing_record)

        return {
            'generated_code': generated_code,
            'layer_hierarchy': layer_hierarchy,
            'output_format': output_format.value,
            'accuracy_score': accuracy_score,
            'verification_results': verification_results,
            'parsing_record': parsing_record
        }

    def _extract_figma_identifiers(self, figma_url: str) -> Tuple[str, str]:
        """
        Extract file key and node ID from Figma URL

        Example URL: https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=2-948
        Returns: ('6Pmf9gCcUccyqbCO9nN6Ts', '2-948')
        """
        # Extract file key
        file_key_match = re.search(r'/design/([a-zA-Z0-9]+)', figma_url)
        file_key = file_key_match.group(1) if file_key_match else None

        # Extract node ID
        node_id_match = re.search(r'node-id=([^&]+)', figma_url)
        node_id = node_id_match.group(1) if node_id_match else None

        if not file_key:
            raise ValueError(f"Could not extract file key from URL: {figma_url}")

        logger.info(f"🦅 Extracted - File Key: {file_key}, Node ID: {node_id}")
        return file_key, node_id

    def _fetch_figma_structure(self, file_key: str, node_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch Figma file structure via API or MCP

        Args:
            file_key: Figma file key
            node_id: Specific node ID (optional)

        Returns:
            Figma file structure as dict
        """
        logger.info(f"🦅 Fetching Figma structure for {file_key}")

        # TODO: Implement actual Figma API/MCP call
        # For now, return mock structure for development
        mock_structure = {
            'name': 'POC Test Component',
            'type': 'FRAME',
            'children': [
                {
                    'name': 'Header',
                    'type': 'FRAME',
                    'children': [
                        {'name': 'Logo', 'type': 'COMPONENT'},
                        {'name': 'Navigation', 'type': 'FRAME'},
                        {'name': 'Actions', 'type': 'FRAME'}
                    ]
                },
                {
                    'name': 'Main Content',
                    'type': 'FRAME',
                    'children': [
                        {'name': 'Sidebar', 'type': 'FRAME'},
                        {'name': 'Content Area', 'type': 'FRAME'}
                    ]
                }
            ]
        }

        logger.info(f"🦅 Fetched Figma structure with {len(mock_structure.get('children', []))} top-level children")
        return mock_structure

    def _determine_output_format(self, figma_structure: Dict[str, Any]) -> OutputFormat:
        """
        Analyze complexity and determine best output format

        Args:
            figma_structure: Figma file structure

        Returns:
            Recommended OutputFormat
        """
        layer_count = self._count_layers(figma_structure)
        has_interactivity = self._detect_interactivity(figma_structure)
        has_components = self._detect_components(figma_structure)

        logger.info(f"🦅 Complexity Analysis: {layer_count} layers, Interactivity: {has_interactivity}, Components: {has_components}")

        # Decision logic
        if layer_count <= self.complexity_thresholds['simple']:
            return OutputFormat.HTML_CSS
        elif layer_count <= self.complexity_thresholds['moderate'] and not has_interactivity:
            return OutputFormat.HTML_TAILWIND
        else:
            return OutputFormat.REACT_TAILWIND

    def _determine_parsing_depth(self, figma_structure: Dict[str, Any]) -> ParsingDepth:
        """
        Determine optimal parsing depth based on structure complexity

        Args:
            figma_structure: Figma file structure

        Returns:
            Recommended ParsingDepth
        """
        max_depth = self._calculate_max_depth(figma_structure)
        avg_children = self._calculate_avg_children(figma_structure)

        logger.info(f"🦅 Depth Analysis: Max depth: {max_depth}, Avg children: {avg_children}")

        if max_depth <= 3 and avg_children <= 5:
            return ParsingDepth.FRAME
        elif max_depth <= 6:
            return ParsingDepth.COMPONENT
        else:
            return ParsingDepth.ELEMENT

    def _parse_layer_hierarchy(
        self,
        figma_structure: Dict[str, Any],
        depth: ParsingDepth,
        current_depth: int = 0
    ) -> Dict[str, Any]:
        """
        Parse Figma layer hierarchy to specified depth

        Args:
            figma_structure: Figma structure to parse
            depth: Parsing depth level
            current_depth: Current recursion depth

        Returns:
            Parsed layer hierarchy with metadata
        """
        layer = {
            'name': figma_structure.get('name', 'Unnamed'),
            'type': figma_structure.get('type', 'UNKNOWN'),
            'depth': current_depth,
            'children': []
        }

        # Check if we should parse children
        should_parse_children = self._should_parse_children(
            figma_structure,
            depth,
            current_depth
        )

        if should_parse_children and 'children' in figma_structure:
            for child in figma_structure['children']:
                parsed_child = self._parse_layer_hierarchy(
                    child,
                    depth,
                    current_depth + 1
                )
                layer['children'].append(parsed_child)

        return layer

    def _should_parse_children(
        self,
        layer: Dict[str, Any],
        target_depth: ParsingDepth,
        current_depth: int
    ) -> bool:
        """Determine if children should be parsed based on depth strategy"""
        if current_depth >= self.depth_config['max_nesting_depth']:
            return False

        if target_depth == ParsingDepth.FRAME:
            return current_depth < 1
        elif target_depth == ParsingDepth.COMPONENT:
            # Parse until component boundaries
            return current_depth < 3 or not self._is_component_boundary(layer)
        else:  # ELEMENT
            return True

    def _is_component_boundary(self, layer: Dict[str, Any]) -> bool:
        """Check if layer represents a component boundary"""
        layer_name = layer.get('name', '').lower()
        layer_type = layer.get('type', '')

        if layer_type in ['COMPONENT', 'INSTANCE']:
            return True

        for indicator in self.depth_config['component_indicators']:
            if indicator in layer_name:
                return True

        return False

    def _generate_code_from_layers(
        self,
        layer_hierarchy: Dict[str, Any],
        output_format: OutputFormat
    ) -> str:
        """
        Generate code from parsed layer hierarchy

        Args:
            layer_hierarchy: Parsed layer structure
            output_format: Output format to generate

        Returns:
            Generated code as string
        """
        logger.info(f"🦅 Generating {output_format.value} code from layers...")

        if output_format == OutputFormat.HTML_CSS:
            return self._generate_html_css(layer_hierarchy)
        elif output_format == OutputFormat.HTML_TAILWIND:
            return self._generate_html_tailwind(layer_hierarchy)
        elif output_format == OutputFormat.REACT_TAILWIND:
            return self._generate_react_tailwind(layer_hierarchy)

        return "// Error: Unknown format"

    def _generate_html_css(self, layer: Dict[str, Any], indent: int = 0) -> str:
        """Generate pure HTML/CSS from layer structure"""
        indent_str = "  " * indent
        layer_name = layer['name'].replace(' ', '-').lower()
        layer_type = layer['type']

        # Generate HTML
        html = f"{indent_str}<div class=\"{layer_name}\">\n"

        # Add children
        for child in layer.get('children', []):
            html += self._generate_html_css(child, indent + 1)

        html += f"{indent_str}</div>\n"

        return html

    def _generate_html_tailwind(self, layer: Dict[str, Any], indent: int = 0) -> str:
        """Generate HTML with Tailwind classes"""
        indent_str = "  " * indent
        layer_name = layer['name'].replace(' ', '-').lower()

        # Map layer types to Tailwind classes
        tailwind_classes = self._map_layer_to_tailwind(layer)

        html = f"{indent_str}<div class=\"{tailwind_classes}\">\n"

        for child in layer.get('children', []):
            html += self._generate_html_tailwind(child, indent + 1)

        html += f"{indent_str}</div>\n"

        return html

    def _generate_react_tailwind(self, layer: Dict[str, Any]) -> str:
        """Generate React component with Tailwind"""
        component_name = layer['name'].replace(' ', '')

        react_code = f"""
import React from 'react';

export default function {component_name}() {{
  return (
    {self._generate_react_jsx(layer, 2)}
  );
}}
"""
        return react_code.strip()

    def _generate_react_jsx(self, layer: Dict[str, Any], indent: int = 0) -> str:
        """Generate React JSX from layer"""
        indent_str = "  " * indent
        tailwind_classes = self._map_layer_to_tailwind(layer)

        jsx = f"{indent_str}<div className=\"{tailwind_classes}\">\n"

        for child in layer.get('children', []):
            jsx += self._generate_react_jsx(child, indent + 1)

        jsx += f"{indent_str}</div>\n"

        return jsx

    def _map_layer_to_tailwind(self, layer: Dict[str, Any]) -> str:
        """Map layer properties to Tailwind classes"""
        # TODO: Implement intelligent mapping based on layer properties
        # For now, return basic classes
        base_classes = "relative"

        if layer['type'] == 'FRAME':
            base_classes += " flex flex-col"

        return base_classes

    def _export_figma_image(self, file_key: str, node_id: str) -> str:
        """Export Figma node as image"""
        # TODO: Implement actual Figma image export
        return "/tmp/figma_export.png"

    def _render_generated_code(self, code: str, output_format: OutputFormat) -> str:
        """Render generated code and capture screenshot"""
        # TODO: Implement code rendering and screenshot capture
        return "/tmp/rendered_code.png"

    def _refine_code(
        self,
        code: str,
        discrepancies: List[Dict[str, Any]],
        output_format: OutputFormat
    ) -> str:
        """Refine code based on identified discrepancies"""
        # TODO: Implement intelligent code refinement
        return code

    def _count_layers(self, structure: Dict[str, Any]) -> int:
        """Count total layers in structure"""
        count = 1
        for child in structure.get('children', []):
            count += self._count_layers(child)
        return count

    def _detect_interactivity(self, structure: Dict[str, Any]) -> bool:
        """Detect if structure contains interactive elements"""
        # TODO: Implement interactivity detection
        return False

    def _detect_components(self, structure: Dict[str, Any]) -> bool:
        """Detect if structure contains reusable components"""
        layer_type = structure.get('type', '')
        if layer_type in ['COMPONENT', 'INSTANCE']:
            return True

        for child in structure.get('children', []):
            if self._detect_components(child):
                return True

        return False

    def _calculate_max_depth(self, structure: Dict[str, Any], current_depth: int = 0) -> int:
        """Calculate maximum depth of layer hierarchy"""
        if not structure.get('children'):
            return current_depth

        max_child_depth = current_depth
        for child in structure['children']:
            child_depth = self._calculate_max_depth(child, current_depth + 1)
            max_child_depth = max(max_child_depth, child_depth)

        return max_child_depth

    def _calculate_avg_children(self, structure: Dict[str, Any]) -> float:
        """Calculate average number of children per layer"""
        total_children = 0
        total_layers = 0

        def count_recursive(layer):
            nonlocal total_children, total_layers
            total_layers += 1
            children = layer.get('children', [])
            total_children += len(children)
            for child in children:
                count_recursive(child)

        count_recursive(structure)
        return total_children / total_layers if total_layers > 0 else 0

    def _save_parsing_record(self, record: Dict[str, Any]):
        """Save parsing record to history"""
        with open(self.parsing_history_db, 'r') as f:
            data = json.load(f)

        data['parsings'].append(record)

        with open(self.parsing_history_db, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"🦅 Parsing record saved: {record['timestamp']}")


# Convenience function for quick usage
def parse_figma_to_code(
    figma_url: str,
    output_format: str = "auto",
    verify: bool = True
) -> Dict[str, Any]:
    """
    Convenience function to parse Figma file to code

    Args:
        figma_url: Figma file URL
        output_format: 'auto', 'html_css', 'html_tailwind', or 'react_tailwind'
        verify: Enable visual verification

    Returns:
        Parsing results with generated code and accuracy scores
    """
    hawkman = HawkmanStructuralParser()

    format_map = {
        'auto': OutputFormat.AUTO,
        'html_css': OutputFormat.HTML_CSS,
        'html_tailwind': OutputFormat.HTML_TAILWIND,
        'react_tailwind': OutputFormat.REACT_TAILWIND
    }

    return hawkman.parse_figma(
        figma_url=figma_url,
        output_format=format_map.get(output_format, OutputFormat.AUTO),
        parsing_depth=ParsingDepth.ADAPTIVE,
        verify=verify
    )
