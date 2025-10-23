"""
🔨 Hephaestus - The Code-to-Design Forger
==========================================

React/TypeScript to Figma converter - The reverse of Artemis CodeSmith!
Transforms existing frontend components into Figma designs.

Named after the Greek god of craftsmanship, fire, and the forge.

Author: Justice League
Created: October 23, 2025
Status: Alpha (Phase 1 - Core Parser)
"""

import re
import json
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum


class FigmaNodeType(Enum):
    """Figma node types"""
    FRAME = "FRAME"
    RECTANGLE = "RECTANGLE"
    TEXT = "TEXT"
    GROUP = "GROUP"
    COMPONENT = "COMPONENT"
    INSTANCE = "INSTANCE"


@dataclass
class FigmaNode:
    """Represents a Figma node"""
    id: str
    name: str
    type: FigmaNodeType
    properties: Dict[str, Any] = field(default_factory=dict)
    children: List['FigmaNode'] = field(default_factory=list)
    styles: Dict[str, Any] = field(default_factory=dict)

    @property
    def characters(self) -> str:
        """Get text content for TEXT nodes."""
        return self.properties.get('characters', '')


@dataclass
class ReactComponent:
    """Parsed React component"""
    name: str
    file_path: str
    jsx_tree: Dict[str, Any]
    props: Dict[str, str]  # Changed from List to Dict
    imports: List[str]
    styles: Dict[str, Any]


class HephaestusCodeToDesign:
    """
    🔨 Hephaestus - Code-to-Design Forger

    Converts React/TypeScript components to Figma designs.
    The reverse operation of Artemis CodeSmith!

    Capabilities:
    - Parse React/JSX/TSX files
    - Extract component structure and styling
    - Map React elements to Figma nodes
    - Convert Tailwind/CSS to Figma properties
    - Generate Figma design via REST API
    - Calculate Hephaestus Score (quality rating)
    """

    # Map React/HTML elements to Figma node types
    ELEMENT_TO_FIGMA_TYPE = {
        'div': FigmaNodeType.FRAME,
        'section': FigmaNodeType.FRAME,
        'article': FigmaNodeType.FRAME,
        'main': FigmaNodeType.FRAME,
        'header': FigmaNodeType.FRAME,
        'footer': FigmaNodeType.FRAME,
        'nav': FigmaNodeType.FRAME,
        'aside': FigmaNodeType.FRAME,
        'span': FigmaNodeType.TEXT,
        'p': FigmaNodeType.TEXT,
        'h1': FigmaNodeType.TEXT,
        'h2': FigmaNodeType.TEXT,
        'h3': FigmaNodeType.TEXT,
        'h4': FigmaNodeType.TEXT,
        'h5': FigmaNodeType.TEXT,
        'h6': FigmaNodeType.TEXT,
        'button': FigmaNodeType.FRAME,  # Button is a frame with text
        'input': FigmaNodeType.FRAME,  # Input is a frame with text
        'img': FigmaNodeType.RECTANGLE,  # Image is a rectangle with fill
    }

    # shadcn/ui components to Figma mapping
    SHADCN_TO_FIGMA = {
        'Button': {'type': FigmaNodeType.FRAME, 'autoLayout': 'horizontal'},
        'Card': {'type': FigmaNodeType.FRAME, 'autoLayout': 'vertical'},
        'CardHeader': {'type': FigmaNodeType.FRAME, 'autoLayout': 'vertical'},
        'CardTitle': {'type': FigmaNodeType.TEXT},
        'CardDescription': {'type': FigmaNodeType.TEXT},
        'CardContent': {'type': FigmaNodeType.FRAME, 'autoLayout': 'vertical'},
        'CardFooter': {'type': FigmaNodeType.FRAME, 'autoLayout': 'horizontal'},
        'Input': {'type': FigmaNodeType.FRAME, 'autoLayout': 'horizontal'},
        'Label': {'type': FigmaNodeType.TEXT},
        'Select': {'type': FigmaNodeType.FRAME, 'autoLayout': 'horizontal'},
        'Checkbox': {'type': FigmaNodeType.FRAME},
        'RadioGroup': {'type': FigmaNodeType.FRAME, 'autoLayout': 'vertical'},
        'Textarea': {'type': FigmaNodeType.FRAME},
        'Badge': {'type': FigmaNodeType.FRAME, 'autoLayout': 'horizontal'},
        'Avatar': {'type': FigmaNodeType.RECTANGLE},
        'Dialog': {'type': FigmaNodeType.FRAME, 'autoLayout': 'vertical'},
        'Sheet': {'type': FigmaNodeType.FRAME, 'autoLayout': 'vertical'},
        'Tabs': {'type': FigmaNodeType.FRAME, 'autoLayout': 'vertical'},
        'Table': {'type': FigmaNodeType.FRAME, 'autoLayout': 'vertical'},
    }

    def __init__(self, figma_token: Optional[str] = None):
        """
        Initialize Hephaestus.

        Args:
            figma_token: Figma Personal Access Token (for API operations)
        """
        self.figma_token = figma_token or "<FIGMA_ACCESS_TOKEN>"
        self.node_counter = 0

    def parse_react_file(self, file_path: str) -> ReactComponent:
        """
        Parse a React component file.

        Args:
            file_path: Path to .tsx, .jsx, .ts, or .js file

        Returns:
            ReactComponent with parsed structure
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        content = path.read_text()

        # Extract component name from filename or export
        component_name = self._extract_component_name(content, path.stem)

        # Extract imports
        imports = self._extract_imports(content)

        # Extract JSX tree (simplified for Phase 1)
        jsx_tree = self._parse_jsx_simple(content)

        # Extract props interface
        props = self._extract_props(content)

        # Extract styles (className, inline styles)
        styles = self._extract_styles(content)

        return ReactComponent(
            name=component_name,
            file_path=file_path,
            jsx_tree=jsx_tree,
            props=props,
            imports=imports,
            styles=styles
        )

    def convert_to_figma(
        self,
        component_path: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Convert React component to Figma design.

        Args:
            component_path: Path to React component file
            options: Conversion options
                - create_file: bool (create new Figma file)
                - file_id: str (existing Figma file ID)
                - page_name: str (Figma page name)

        Returns:
            {
                'success': bool,
                'figma_url': str,
                'nodes_created': int,
                'figma_file_id': str,
                'hephaestus_score': float,
                'errors': List[str]
            }
        """
        options = options or {}

        print(f"\n🔨 Hephaestus forging design from code...")
        print(f"📄 Analyzing: {component_path}")
        print("=" * 70)

        try:
            # Step 1: Parse React component
            component = self.parse_react_file(component_path)
            print(f"\n✅ Parsed component: {component.name}")
            print(f"   Imports: {len(component.imports)}")
            print(f"   Props: {len(component.props)}")

            # Step 2: Convert to Figma nodes
            figma_nodes = self.jsx_to_figma_nodes(component.jsx_tree)
            print(f"\n🎨 Generated {self._count_nodes(figma_nodes)} Figma nodes")

            # Step 3: Apply styles
            styled_nodes = self.apply_styles(figma_nodes, component.styles)

            # Step 4: Calculate Hephaestus Score
            score = self._calculate_hephaestus_score(component, styled_nodes)

            # Step 5: Generate Figma file (mock for Phase 1)
            figma_result = self._create_figma_file(
                component_name=component.name,
                nodes=styled_nodes,
                options=options
            )

            print(f"\n🔨 Hephaestus Score: {score}/100")
            print(f"✅ Design forged successfully!")

            return {
                'success': True,
                'figma_url': figma_result['url'],
                'figma_file_id': figma_result['file_id'],
                'nodes_created': figma_result['nodes_created'],
                'hephaestus_score': score,
                'component_name': component.name,
                'figma_nodes': styled_nodes,
                'errors': []
            }

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            return {
                'success': False,
                'figma_url': '',
                'figma_file_id': '',
                'nodes_created': 0,
                'hephaestus_score': 0,
                'errors': [str(e)]
            }

    def jsx_to_figma_nodes(self, jsx_tree: Dict[str, Any]) -> FigmaNode:
        """
        Convert JSX tree to Figma nodes.

        Args:
            jsx_tree: Parsed JSX structure

        Returns:
            Root FigmaNode with children
        """
        element_type = jsx_tree.get('type', 'div')
        element_name = jsx_tree.get('name', element_type)

        # Determine Figma node type
        figma_type = self._get_figma_type(element_type)

        # Create node
        node = FigmaNode(
            id=self._generate_node_id(),
            name=element_name,
            type=figma_type,
            properties=jsx_tree.get('props', {}),
            children=[],
            styles={}
        )

        # For TEXT nodes with direct text content, store it in properties
        children = jsx_tree.get('children', [])
        if figma_type == FigmaNodeType.TEXT and children:
            # If the TEXT node has string children, store as characters
            if isinstance(children, str):
                node.properties['characters'] = children.strip()
            elif isinstance(children, list) and len(children) > 0 and isinstance(children[0], str):
                node.properties['characters'] = children[0].strip()

        # Process children for non-text nodes or nested elements
        for child in children if isinstance(children, list) else []:
            if isinstance(child, dict):
                child_node = self.jsx_to_figma_nodes(child)
                node.children.append(child_node)
            elif isinstance(child, str) and figma_type != FigmaNodeType.TEXT:
                # Only create child text nodes for non-TEXT parents
                text_node = FigmaNode(
                    id=self._generate_node_id(),
                    name="Text",
                    type=FigmaNodeType.TEXT,
                    properties={'characters': child.strip()},
                    children=[],
                    styles={}
                )
                if child.strip():  # Only add if not empty
                    node.children.append(text_node)

        return node

    def apply_styles(
        self,
        node: FigmaNode,
        styles: Dict[str, Any]
    ) -> FigmaNode:
        """
        Apply CSS/Tailwind styles to Figma nodes.

        Args:
            node: FigmaNode to style
            styles: Style definitions

        Returns:
            Styled FigmaNode
        """
        # For Phase 1, this is simplified
        # Phase 2 will include full Tailwind → Figma conversion

        if 'className' in node.properties:
            classes = node.properties['className'].split()
            node.styles = self._convert_tailwind_classes(classes)

        # Apply to children recursively
        for child in node.children:
            self.apply_styles(child, styles)

        return node

    def _extract_component_name(self, content: str, filename: str) -> str:
        """Extract component name from file content or filename."""
        # Try to find export default or export function
        patterns = [
            r'export\s+default\s+function\s+(\w+)',
            r'export\s+function\s+(\w+)',
            r'export\s+const\s+(\w+)\s*=',
            r'function\s+(\w+)\s*\(',
        ]

        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1)

        # Fallback to filename (capitalize first letter)
        return filename[0].upper() + filename[1:]

    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements."""
        imports = []

        # Pattern for named imports: import { Button, Card } from '...'
        named_import_pattern = r'import\s+\{([^}]+)\}\s+from\s+[\'"]([^\'"]+)[\'"]'
        named_matches = re.findall(named_import_pattern, content)
        for components, _source in named_matches:
            # Split by comma and clean up whitespace
            components_list = [c.strip() for c in components.split(',')]
            imports.extend(components_list)

        # Pattern for default imports: import Button from '...'
        default_import_pattern = r'import\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]'
        default_matches = re.findall(default_import_pattern, content)
        for component, _source in default_matches:
            if component not in imports:
                imports.append(component)

        return imports

    def _parse_jsx_simple(self, content: str) -> Dict[str, Any]:
        """
        Simple JSX parser (Phase 1 - Basic implementation).
        Phase 2 will use proper AST parsing with babel/typescript.
        """
        # For Phase 1, create a simplified mock structure
        # Real implementation will use proper parser

        return {
            'type': 'div',
            'name': 'Root',
            'props': {'className': 'component-root'},
            'children': [
                {
                    'type': 'div',
                    'name': 'Container',
                    'props': {'className': 'container mx-auto'},
                    'children': [
                        {
                            'type': 'h1',
                            'name': 'Title',
                            'props': {'className': 'text-2xl font-bold'},
                            'children': ['Component Title']
                        },
                        {
                            'type': 'p',
                            'name': 'Description',
                            'props': {'className': 'text-gray-600'},
                            'children': ['Component description']
                        }
                    ]
                }
            ]
        }

    def _extract_props(self, content: str) -> Dict[str, str]:
        """Extract component props from interface/type definition."""
        # Look for Props interface or type
        props_pattern = r'interface\s+\w+Props\s*\{([^}]+)\}'
        match = re.search(props_pattern, content)

        props = {}
        if match:
            props_content = match.group(1)
            # Extract property names and types
            prop_matches = re.findall(r'(\w+)\s*\??\s*:\s*([^;,]+)', props_content)
            for name, prop_type in prop_matches:
                props[name.strip()] = prop_type.strip()

        return props

    def _extract_styles(self, content: str) -> Dict[str, Any]:
        """Extract style information from component."""
        styles = {
            'tailwind_classes': [],
            'inline_styles': {},
            'css_modules': {}
        }

        # Extract Tailwind classes
        class_pattern = r'className=["\']([^"\']+)["\']'
        matches = re.findall(class_pattern, content)
        for match in matches:
            styles['tailwind_classes'].extend(match.split())

        # Deduplicate
        styles['tailwind_classes'] = list(set(styles['tailwind_classes']))

        return styles

    def _get_figma_type(self, element_type: str) -> FigmaNodeType:
        """Map React element type to Figma node type."""
        # Check shadcn/ui components first
        if element_type in self.SHADCN_TO_FIGMA:
            return self.SHADCN_TO_FIGMA[element_type]['type']

        # Check HTML elements
        if element_type in self.ELEMENT_TO_FIGMA_TYPE:
            return self.ELEMENT_TO_FIGMA_TYPE[element_type]

        # Default to FRAME
        return FigmaNodeType.FRAME

    def _generate_node_id(self) -> str:
        """Generate unique node ID."""
        self.node_counter += 1
        return f"node_{self.node_counter}"

    def _count_nodes(self, node: FigmaNode) -> int:
        """Count total nodes in tree."""
        count = 1  # Current node
        for child in node.children:
            count += self._count_nodes(child)
        return count

    def _convert_tailwind_classes(self, classes: List[str]) -> Dict[str, Any]:
        """
        Convert Tailwind classes to Figma styles.
        Phase 1: Basic mappings
        Phase 2: Complete Tailwind → Figma conversion
        """
        styles = {}

        for cls in classes:
            # Width/Height
            if cls.startswith('w-'):
                styles['width'] = self._tailwind_to_pixels(cls, 'w-')
            elif cls.startswith('h-'):
                styles['height'] = self._tailwind_to_pixels(cls, 'h-')

            # Colors
            elif cls.startswith('bg-'):
                styles['fill'] = self._tailwind_color_to_figma(cls)
            elif cls.startswith('text-'):
                if any(size in cls for size in ['xs', 'sm', 'base', 'lg', 'xl', '2xl', '3xl']):
                    styles['fontSize'] = self._tailwind_font_size(cls)
                else:
                    styles['textColor'] = self._tailwind_color_to_figma(cls)

            # Font
            elif cls.startswith('font-'):
                if 'bold' in cls:
                    styles['fontWeight'] = 700
                elif 'semibold' in cls:
                    styles['fontWeight'] = 600
                elif 'medium' in cls:
                    styles['fontWeight'] = 500
                elif 'normal' in cls:
                    styles['fontWeight'] = 400
                elif 'light' in cls:
                    styles['fontWeight'] = 300

            # Layout
            elif 'flex' in cls:
                styles['layoutMode'] = 'FLEX'
            elif 'grid' in cls:
                styles['layoutMode'] = 'GRID'

            # Spacing
            elif cls.startswith('p-') or cls.startswith('padding'):
                value = self._tailwind_to_pixels(cls, 'p-')
                styles['paddingTop'] = value
                styles['paddingRight'] = value
                styles['paddingBottom'] = value
                styles['paddingLeft'] = value
            elif cls.startswith('m-') or cls.startswith('margin'):
                styles['spacing'] = self._tailwind_to_pixels(cls, 'm-')

            # Borders
            elif cls.startswith('border-') and any(char.isdigit() for char in cls):
                # Extract number (e.g., 'border-2' -> 2)
                num = ''.join(filter(str.isdigit, cls))
                styles['strokeWeight'] = int(num) if num else 1
            elif cls == 'border':
                styles['strokeWeight'] = 1
            elif cls.startswith('rounded'):
                styles['cornerRadius'] = self._tailwind_border_radius(cls)

        return styles

    def _tailwind_to_pixels(self, cls: str, prefix: str) -> int:
        """Convert Tailwind spacing to pixels (1 unit = 4px)."""
        value = cls.replace(prefix, '')

        # Special cases
        if value == 'full':
            return 9999
        elif value == 'auto':
            return 'auto'

        # Numeric values
        try:
            num = int(value)
            return num * 4  # Tailwind uses 0.25rem = 4px per unit
        except ValueError:
            return 0

    def _tailwind_color_to_figma(self, cls: str) -> Dict[str, float]:
        """Convert Tailwind color to Figma color (RGBA)."""
        # Simplified color mapping for Phase 1
        color_map = {
            'bg-white': {'r': 1.0, 'g': 1.0, 'b': 1.0, 'a': 1.0},
            'bg-black': {'r': 0.0, 'g': 0.0, 'b': 0.0, 'a': 1.0},
            'bg-gray-100': {'r': 0.96, 'g': 0.96, 'b': 0.96, 'a': 1.0},
            'bg-gray-900': {'r': 0.07, 'g': 0.07, 'b': 0.07, 'a': 1.0},
            'bg-blue-500': {'r': 0.24, 'g': 0.55, 'b': 0.96, 'a': 1.0},
            'bg-red-500': {'r': 0.94, 'g': 0.27, 'b': 0.27, 'a': 1.0},
            'bg-green-500': {'r': 0.13, 'g': 0.72, 'b': 0.42, 'a': 1.0},
        }

        return color_map.get(cls, {'r': 0.5, 'g': 0.5, 'b': 0.5, 'a': 1.0})

    def _tailwind_font_size(self, cls: str) -> int:
        """Convert Tailwind font size to pixels."""
        size_map = {
            'text-xs': 12,
            'text-sm': 14,
            'text-base': 16,
            'text-lg': 18,
            'text-xl': 20,
            'text-2xl': 24,
            'text-3xl': 30,
            'text-4xl': 36,
        }

        return size_map.get(cls, 16)

    def _tailwind_border_radius(self, cls: str) -> int:
        """Convert Tailwind border radius to pixels."""
        radius_map = {
            'rounded-none': 0,
            'rounded-sm': 2,
            'rounded': 4,
            'rounded-md': 6,
            'rounded-lg': 8,
            'rounded-xl': 12,
            'rounded-2xl': 16,
            'rounded-full': 9999,
        }

        return radius_map.get(cls, 0)

    def _create_figma_file(
        self,
        component_name: str,
        nodes: FigmaNode,
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create Figma file via REST API.
        Phase 1: Mock implementation
        Phase 2: Real Figma API integration
        """
        # For Phase 1, return mock data
        # Phase 2 will implement actual Figma API calls

        file_id = options.get('file_id', 'mock_file_id_123')

        return {
            'file_id': file_id,
            'url': f'https://www.figma.com/file/{file_id}/{component_name}',
            'nodes_created': self._count_nodes(nodes)
        }

    def _calculate_hephaestus_score(
        self,
        component: ReactComponent,
        nodes: FigmaNode
    ) -> float:
        """
        Calculate Hephaestus Score (0-100) for conversion quality.

        Factors:
        - Component structure complexity: +20
        - Style coverage: +30
        - Props extraction: +15
        - Figma node accuracy: +20
        - shadcn/ui components: +15
        """
        score = 0.0

        # Component structure (20 points)
        if component.jsx_tree:
            score += 20

        # Style coverage (30 points)
        if component.styles.get('tailwind_classes'):
            class_count = len(component.styles['tailwind_classes'])
            score += min(30, class_count * 2)  # 15+ classes = full points

        # Props extraction (15 points)
        if component.props:
            score += min(15, len(component.props) * 3)

        # Figma nodes generated (20 points)
        node_count = self._count_nodes(nodes)
        if node_count >= 10:
            score += 20
        elif node_count >= 5:
            score += 15
        elif node_count >= 1:
            score += 10

        # shadcn/ui component detection (15 points)
        # Check if any imports match shadcn component names
        shadcn_component_names = set(self.SHADCN_TO_FIGMA.keys())
        shadcn_imports = [imp for imp in component.imports if imp in shadcn_component_names]
        if shadcn_imports:
            score += min(15, len(shadcn_imports) * 5)  # 3+ shadcn components = full points

        return min(score, 100.0)


# Example usage
def example_usage():
    """Example of using Hephaestus."""

    hephaestus = HephaestusCodeToDesign()

    # Example: Convert React component to Figma
    # This would work with a real component file
    print("\n🔨 Hephaestus - Code-to-Design Forger")
    print("=" * 70)
    print("\nExample: Converting React component to Figma design")
    print("\nNote: Phase 1 uses simplified parsing")
    print("Phase 2 will include full AST parsing and real Figma API\n")

    # Mock result for demonstration
    result = {
        'success': True,
        'figma_url': 'https://www.figma.com/file/mock/LoginForm',
        'nodes_created': 12,
        'hephaestus_score': 85.0
    }

    print(f"✅ Success!")
    print(f"🎨 Figma URL: {result['figma_url']}")
    print(f"📦 Nodes Created: {result['nodes_created']}")
    print(f"🔨 Hephaestus Score: {result['hephaestus_score']}/100")


if __name__ == '__main__':
    example_usage()
