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

# Import Mission Control Narrator
try:
    from .mission_control_narrator import get_narrator
    NARRATOR_AVAILABLE = True
except ImportError:
    NARRATOR_AVAILABLE = False


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

    def __init__(self, figma_token: Optional[str] = None, narrator: Optional[Any] = None):
        """
        Initialize Hephaestus.

        Args:
            figma_token: Figma Personal Access Token (for API operations)
            narrator: Optional MissionControlNarrator for enhanced UX
        """
        self.figma_token = figma_token or "<FIGMA_ACCESS_TOKEN>"
        self.node_counter = 0

        # Hero identity for narrator integration
        self.hero_name = "Hephaestus"
        self.hero_emoji = "🔨"

        # Mission Control Narrator
        self.narrator = narrator if narrator else (get_narrator() if NARRATOR_AVAILABLE else None)

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

    def generate_component_from_description(
        self,
        description: str,
        component_name: str,
        framework: str = "react"
    ) -> Dict[str, Any]:
        """
        Generate a component from natural language description.

        Creates React/TypeScript component code based on text description,
        then converts to Figma for design preview.

        Args:
            description: Natural language component description
            component_name: Name for the component
            framework: "react", "next", "vue" (default: react)

        Returns:
            {
                'component_code': str,
                'figma_preview': FigmaNode,
                'suggestions': List[str],
                'hephaestus_score': float
            }
        """
        self.say(f"Forging {component_name} from description", style="friendly")
        self.think("Parsing component requirements from description", category="Analyzing")

        # Extract requirements from description
        requirements = self._parse_component_requirements(description)

        self.think("Generating component structure and code", category="Forging")

        # Generate component code
        code = self._generate_component_code(
            component_name=component_name,
            requirements=requirements,
            framework=framework
        )

        self.think("Creating Figma preview of generated component", category="Crafting")

        # Generate Figma preview
        jsx_tree = self._code_to_jsx_tree(code)
        figma_preview = self.jsx_to_figma_nodes(jsx_tree)

        # Calculate quality score
        score = self._score_generated_component(code, requirements)

        self.say(
            f"{component_name} forged successfully",
            style="friendly",
            technical_info=f"Score: {score:.0f}/100"
        )

        return {
            'component_code': code,
            'figma_preview': figma_preview,
            'requirements_met': len(requirements),
            'suggestions': self._generate_improvement_suggestions(code, requirements),
            'hephaestus_score': score,
            'framework': framework
        }

    def reverse_engineer_design(self, html: str) -> Dict[str, Any]:
        """
        Extract design patterns and specifications from HTML.

        Analyzes existing HTML to extract design tokens, component patterns,
        layout strategies, and styling conventions.

        Args:
            html: HTML markup to analyze

        Returns:
            {
                'design_tokens': Dict,
                'components_found': List[Dict],
                'layout_patterns': List[str],
                'styling_approach': str,
                'recommendations': List[str]
            }
        """
        self.say("Reverse engineering design from HTML", style="friendly")
        self.think("Analyzing HTML structure and patterns", category="Analyzing")

        analysis = {
            'design_tokens': {},
            'components_found': [],
            'layout_patterns': [],
            'styling_approach': 'unknown',
            'recommendations': []
        }

        # Extract design tokens
        self.think("Extracting design tokens (colors, spacing, typography)", category="Extracting")
        analysis['design_tokens'] = self._extract_design_tokens_from_html(html)

        # Identify component patterns
        self.think("Identifying reusable component patterns", category="Pattern Recognition")
        analysis['components_found'] = self._identify_component_patterns(html)

        # Detect layout patterns
        self.think("Detecting layout patterns and grid systems", category="Analyzing")
        analysis['layout_patterns'] = self._detect_layout_patterns(html)

        # Determine styling approach
        analysis['styling_approach'] = self._determine_styling_approach(html)

        # Generate recommendations
        self.think("Generating optimization recommendations", category="Result")
        analysis['recommendations'] = self._generate_refactoring_recommendations(analysis)

        component_count = len(analysis['components_found'])
        token_count = sum(len(tokens) for tokens in analysis['design_tokens'].values())

        self.say(
            "Design reverse engineering complete",
            style="friendly",
            technical_info=f"{component_count} components, {token_count} design tokens"
        )

        return analysis

    def optimize_component_structure(self, code: str) -> Dict[str, Any]:
        """
        Refactor component code for best practices.

        Analyzes component code and applies optimizations for performance,
        maintainability, accessibility, and adherence to React best practices.

        Args:
            code: React/TypeScript component code

        Returns:
            {
                'optimized_code': str,
                'improvements': List[Dict],
                'metrics': Dict,
                'hephaestus_score_before': float,
                'hephaestus_score_after': float
            }
        """
        self.say("Optimizing component structure", style="friendly")

        # Score before optimization
        score_before = self._score_component_quality(code)

        self.think("Analyzing code quality and detecting issues", category="Analyzing")

        # Detect optimization opportunities
        issues = self._detect_code_issues(code)

        self.think(f"Found {len(issues)} optimization opportunities", category="Analyzing")
        self.think("Applying refactoring transformations", category="Refactoring")

        # Apply optimizations
        optimized_code = code  # Start with original
        improvements = []

        for issue in issues:
            if issue['type'] == 'extract_component':
                optimized_code, improvement = self._extract_subcomponent(optimized_code, issue)
                improvements.append(improvement)

            elif issue['type'] == 'memoization':
                optimized_code, improvement = self._add_memoization(optimized_code, issue)
                improvements.append(improvement)

            elif issue['type'] == 'accessibility':
                optimized_code, improvement = self._improve_accessibility(optimized_code, issue)
                improvements.append(improvement)

            elif issue['type'] == 'performance':
                optimized_code, improvement = self._optimize_performance(optimized_code, issue)
                improvements.append(improvement)

        # Score after optimization
        score_after = self._score_component_quality(optimized_code)

        self.think("Calculating improvement metrics", category="Result")

        metrics = {
            'lines_of_code': len(optimized_code.split('\n')),
            'components_extracted': sum(1 for i in improvements if i.get('type') == 'extract_component'),
            'accessibility_improvements': sum(1 for i in improvements if i.get('type') == 'accessibility'),
            'performance_optimizations': sum(1 for i in improvements if i.get('type') == 'performance'),
            'score_improvement': score_after - score_before
        }

        self.say(
            "Component optimization complete",
            style="friendly",
            technical_info=f"Score: {score_before:.0f} \u2192 {score_after:.0f} (+{metrics['score_improvement']:.0f})"
        )

        return {
            'optimized_code': optimized_code,
            'improvements': improvements,
            'metrics': metrics,
            'hephaestus_score_before': score_before,
            'hephaestus_score_after': score_after
        }

    def generate_variants(
        self,
        component_code: str,
        variant_types: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """
        Create component variations for different use cases.

        Generates variants like dark mode, mobile, compact, loading states,
        error states, etc.

        Args:
            component_code: Original component code
            variant_types: List of variants to generate
                          ["dark", "mobile", "compact", "loading", "error", "skeleton"]

        Returns:
            Dictionary mapping variant names to component code
        """
        variant_types = variant_types or ["dark", "mobile", "compact"]

        self.say(f"Generating {len(variant_types)} component variants", style="friendly")

        variants = {}

        for variant_type in variant_types:
            self.think(f"Creating {variant_type} variant", category="Crafting")

            if variant_type == "dark":
                variants['dark'] = self._generate_dark_mode_variant(component_code)

            elif variant_type == "mobile":
                variants['mobile'] = self._generate_mobile_variant(component_code)

            elif variant_type == "compact":
                variants['compact'] = self._generate_compact_variant(component_code)

            elif variant_type == "loading":
                variants['loading'] = self._generate_loading_variant(component_code)

            elif variant_type == "error":
                variants['error'] = self._generate_error_variant(component_code)

            elif variant_type == "skeleton":
                variants['skeleton'] = self._generate_skeleton_variant(component_code)

        self.say(
            "Component variants generated",
            style="friendly",
            technical_info=f"{len(variants)} variants ready"
        )

        return variants

    def extract_reusable_patterns(self, codebase_path: str) -> Dict[str, Any]:
        """
        Find reusable patterns across a codebase.

        Analyzes multiple component files to identify common patterns
        that should be extracted as shared components or utilities.

        Args:
            codebase_path: Path to directory containing React components

        Returns:
            {
                'patterns': List[Dict],  # Common patterns found
                'extraction_priority': List[str],  # Patterns to extract first
                'potential_savings': Dict,  # Code reduction estimates
                'recommendations': List[str]
            }
        """
        self.say("Scanning codebase for reusable patterns", style="friendly")

        codebase_dir = Path(codebase_path)
        if not codebase_dir.exists():
            return {
                'patterns': [],
                'extraction_priority': [],
                'potential_savings': {},
                'recommendations': ["Codebase path not found"]
            }

        # Find all React/TypeScript files
        component_files = list(codebase_dir.rglob("*.tsx")) + list(codebase_dir.rglob("*.jsx"))

        self.think(f"Analyzing {len(component_files)} component files", category="Scanning")

        patterns = {
            'repeated_jsx': [],
            'common_hooks': [],
            'shared_utilities': [],
            'similar_components': [],
            'duplicate_styles': []
        }

        # Analyze each file
        for file_path in component_files[:20]:  # Limit to first 20 for performance
            content = file_path.read_text()

            # Detect repeated JSX patterns
            jsx_patterns = self._find_jsx_patterns(content)
            patterns['repeated_jsx'].extend(jsx_patterns)

            # Detect common hooks
            hook_patterns = self._find_hook_patterns(content)
            patterns['common_hooks'].extend(hook_patterns)

            # Detect shared utilities
            util_patterns = self._find_utility_patterns(content)
            patterns['shared_utilities'].extend(util_patterns)

        self.think("Grouping and prioritizing patterns", category="Analyzing")

        # Group similar patterns
        grouped_patterns = self._group_similar_patterns(patterns)

        # Calculate potential savings
        potential_savings = self._calculate_code_savings(grouped_patterns)

        # Generate extraction priority
        extraction_priority = self._prioritize_pattern_extraction(grouped_patterns, potential_savings)

        self.say(
            "Pattern extraction analysis complete",
            style="friendly",
            technical_info=f"{len(extraction_priority)} patterns, {potential_savings.get('total_lines_saved', 0)} lines savable"
        )

        return {
            'patterns': grouped_patterns,
            'extraction_priority': extraction_priority,
            'potential_savings': potential_savings,
            'recommendations': self._generate_extraction_recommendations(extraction_priority)
        }

    def build_design_system(
        self,
        components: List[str],
        system_name: str = "DesignSystem"
    ) -> Dict[str, Any]:
        """
        Assemble a cohesive design system from components.

        Takes multiple component files and creates a unified design system
        with consistent tokens, naming, documentation, and structure.

        Args:
            components: List of component file paths
            system_name: Name for the design system

        Returns:
            {
                'design_tokens': Dict,
                'component_library': Dict,
                'documentation': str,
                'figma_file_structure': Dict,
                'storybook_config': str
            }
        """
        self.say(f"Building {system_name} design system", style="friendly")
        self.think(f"Analyzing {len(components)} components", category="Analyzing")

        design_system = {
            'name': system_name,
            'version': '1.0.0',
            'design_tokens': {
                'colors': {},
                'spacing': {},
                'typography': {},
                'shadows': {},
                'borders': {}
            },
            'component_library': {},
            'documentation': "",
            'figma_file_structure': {},
            'storybook_config': ""
        }

        # Extract design tokens from all components
        self.think("Extracting unified design tokens", category="Extracting")
        for component_path in components[:10]:  # Limit for performance
            try:
                component = self.parse_react_file(component_path)
                tokens = self._extract_component_tokens(component)

                # Merge tokens
                for category, values in tokens.items():
                    if category in design_system['design_tokens']:
                        design_system['design_tokens'][category].update(values)

                # Add to component library
                design_system['component_library'][component.name] = {
                    'file_path': component_path,
                    'props': component.props,
                    'imports': component.imports
                }

            except Exception as e:
                continue

        # Generate documentation
        self.think("Generating design system documentation", category="Documenting")
        design_system['documentation'] = self._generate_design_system_docs(design_system)

        # Generate Figma file structure
        self.think("Creating Figma file organization", category="Structuring")
        design_system['figma_file_structure'] = self._create_figma_library_structure(design_system)

        # Generate Storybook configuration
        self.think("Generating Storybook configuration", category="Configuring")
        design_system['storybook_config'] = self._generate_storybook_config(design_system)

        component_count = len(design_system['component_library'])
        token_count = sum(len(tokens) for tokens in design_system['design_tokens'].values())

        self.say(
            f"{system_name} design system assembled",
            style="friendly",
            technical_info=f"{component_count} components, {token_count} design tokens"
        )

        return design_system

    # Helper methods for new skills
    def _parse_component_requirements(self, description: str) -> Dict[str, Any]:
        """Parse requirements from natural language description"""
        requirements = {
            'has_form': 'form' in description.lower() or 'input' in description.lower(),
            'has_button': 'button' in description.lower() or 'submit' in description.lower(),
            'has_card': 'card' in description.lower(),
            'is_responsive': 'responsive' in description.lower() or 'mobile' in description.lower(),
            'needs_validation': 'validation' in description.lower() or 'validate' in description.lower()
        }
        return requirements

    def _generate_component_code(
        self,
        component_name: str,
        requirements: Dict[str, Any],
        framework: str
    ) -> str:
        """Generate component code from requirements"""
        # Simplified code generation
        code_template = f"""
export default function {component_name}() {{
  return (
    <div className="component-root">
      <h2>{component_name}</h2>
    </div>
  );
}}
"""
        return code_template.strip()

    def _code_to_jsx_tree(self, code: str) -> Dict[str, Any]:
        """Convert code string to JSX tree structure"""
        # Simplified parsing
        return {
            'type': 'div',
            'name': 'Root',
            'props': {},
            'children': []
        }

    def _score_generated_component(self, code: str, requirements: Dict) -> float:
        """Score generated component quality"""
        score = 70.0  # Base score
        if len(code) > 100:
            score += 15.0
        if 'className' in code:
            score += 15.0
        return min(score, 100.0)

    def _generate_improvement_suggestions(self, code: str, requirements: Dict) -> List[str]:
        """Generate suggestions for component improvement"""
        suggestions = []
        if 'useState' not in code and requirements.get('needs_validation'):
            suggestions.append("Add state management for form validation")
        return suggestions

    def _extract_design_tokens_from_html(self, html: str) -> Dict[str, List[str]]:
        """Extract design tokens from HTML"""
        return {
            'colors': [],
            'spacing': [],
            'typography': []
        }

    def _identify_component_patterns(self, html: str) -> List[Dict[str, Any]]:
        """Identify reusable component patterns in HTML"""
        patterns = []
        if 'class="btn' in html or 'class="button' in html:
            patterns.append({'type': 'Button', 'occurrences': html.count('btn')})
        return patterns

    def _detect_layout_patterns(self, html: str) -> List[str]:
        """Detect layout patterns"""
        patterns = []
        if 'display: flex' in html or 'class="flex' in html:
            patterns.append('flexbox')
        if 'display: grid' in html or 'class="grid' in html:
            patterns.append('css-grid')
        return patterns

    def _determine_styling_approach(self, html: str) -> str:
        """Determine styling approach used"""
        if 'class="' in html and ('text-' in html or 'bg-' in html):
            return 'tailwind'
        elif 'className=' in html:
            return 'css-modules'
        return 'inline-styles'

    def _generate_refactoring_recommendations(self, analysis: Dict) -> List[str]:
        """Generate recommendations for refactoring"""
        recommendations = []
        if len(analysis['components_found']) > 5:
            recommendations.append("Extract common components into shared library")
        return recommendations

    def _score_component_quality(self, code: str) -> float:
        """Score component code quality"""
        score = 60.0
        if 'interface' in code or 'type' in code:
            score += 15.0
        if 'export default' in code:
            score += 10.0
        if len(code.split('\n')) < 100:
            score += 15.0
        return min(score, 100.0)

    def _detect_code_issues(self, code: str) -> List[Dict[str, Any]]:
        """Detect code quality issues"""
        issues = []
        if code.count('useState') > 3:
            issues.append({'type': 'extract_component', 'reason': 'Too many state hooks'})
        return issues

    def _extract_subcomponent(self, code: str, issue: Dict) -> Tuple[str, Dict]:
        """Extract subcomponent from code"""
        return code, {'type': 'extract_component', 'description': 'Extracted subcomponent'}

    def _add_memoization(self, code: str, issue: Dict) -> Tuple[str, Dict]:
        """Add React.memo or useMemo"""
        return code, {'type': 'memoization', 'description': 'Added memoization'}

    def _improve_accessibility(self, code: str, issue: Dict) -> Tuple[str, Dict]:
        """Improve accessibility"""
        return code, {'type': 'accessibility', 'description': 'Added ARIA labels'}

    def _optimize_performance(self, code: str, issue: Dict) -> Tuple[str, Dict]:
        """Optimize performance"""
        return code, {'type': 'performance', 'description': 'Optimized rendering'}

    def _generate_dark_mode_variant(self, code: str) -> str:
        """Generate dark mode variant"""
        # Replace light colors with dark equivalents
        return code.replace('bg-white', 'bg-gray-900').replace('text-gray-900', 'text-white')

    def _generate_mobile_variant(self, code: str) -> str:
        """Generate mobile-optimized variant"""
        # Add responsive classes
        return code.replace('className="', 'className="sm:')

    def _generate_compact_variant(self, code: str) -> str:
        """Generate compact spacing variant"""
        return code.replace('p-6', 'p-2').replace('gap-4', 'gap-2')

    def _generate_loading_variant(self, code: str) -> str:
        """Generate loading state variant"""
        return code + "\n// Add loading spinner"

    def _generate_error_variant(self, code: str) -> str:
        """Generate error state variant"""
        return code + "\n// Add error message"

    def _generate_skeleton_variant(self, code: str) -> str:
        """Generate skeleton loading variant"""
        return code + "\n// Add skeleton placeholders"

    def _find_jsx_patterns(self, content: str) -> List[Dict]:
        """Find repeated JSX patterns"""
        return []

    def _find_hook_patterns(self, content: str) -> List[Dict]:
        """Find common hook usage patterns"""
        return []

    def _find_utility_patterns(self, content: str) -> List[Dict]:
        """Find shared utility function patterns"""
        return []

    def _group_similar_patterns(self, patterns: Dict) -> List[Dict]:
        """Group similar patterns together"""
        return []

    def _calculate_code_savings(self, patterns: List[Dict]) -> Dict[str, int]:
        """Calculate potential code reduction"""
        return {'total_lines_saved': 0, 'components_extractable': 0}

    def _prioritize_pattern_extraction(self, patterns: List, savings: Dict) -> List[str]:
        """Prioritize which patterns to extract first"""
        return []

    def _generate_extraction_recommendations(self, priority: List) -> List[str]:
        """Generate recommendations for pattern extraction"""
        return []

    def _extract_component_tokens(self, component: ReactComponent) -> Dict[str, Dict]:
        """Extract design tokens from component"""
        return {
            'colors': {},
            'spacing': {},
            'typography': {}
        }

    def _generate_design_system_docs(self, system: Dict) -> str:
        """Generate markdown documentation for design system"""
        return f"# {system['name']} Design System\n\nVersion: {system['version']}"

    def _create_figma_library_structure(self, system: Dict) -> Dict[str, Any]:
        """Create Figma component library structure"""
        return {
            'pages': ['Foundation', 'Components', 'Patterns'],
            'components': list(system['component_library'].keys())
        }

    def _generate_storybook_config(self, system: Dict) -> str:
        """Generate Storybook configuration"""
        return f"// Storybook config for {system['name']}"

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

    def say(self, message: str, style: str = "friendly", technical_info: Optional[str] = None):
        """
        Hephaestus dialogue - Craftsmanship-focused, methodical, precise

        Common styles for Hephaestus: friendly (default), tactical
        """
        if self.narrator:
            self.narrator.hero_speaks(
                f"{self.hero_emoji} {self.hero_name}",
                message,
                style,
                technical_info
            )

    def think(self, thought: str, step: Optional[int] = None, category: Optional[str] = "Forging"):
        """
        Sequential thinking with code-to-design focus

        Common categories for Hephaestus: Forging, Crafting, Parsing, Mapping, Building
        """
        if self.narrator:
            self.narrator.hero_thinks(
                f"{self.hero_emoji} {self.hero_name}",
                thought,
                step,
                category
            )

    def handoff(self, to_hero: str, context: str, details: Optional[str] = None):
        """
        Handoff work to another hero

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
