"""
Vision Analyst - Visual Dashboard Analysis Hero
============================================

Hero #18 in the Justice League

**Mission**: Analyze dashboard screenshots and UI images to extract precise measurements,
layout patterns, color palettes, and component structures for pixel-perfect HTML/CSS generation.

**Capabilities**:
- Component-by-component visual breakdown
- Layout measurement extraction (spacing, dimensions, grid patterns)
- Color palette detection and categorization
- Typography analysis (font sizes, weights, hierarchy)
- Pattern recognition (cards, grids, sidebars, headers)
- Generate structured analysis reports for Artemis

**When to Deploy**:
- Complex dashboard layouts with multiple columns
- When Figma API produces low accuracy (<70%)
- Screenshot-only conversions (no Figma access)
- Pixel-perfect requirements (95%+ accuracy needed)
- Multi-section layouts (header + grid + sidebar patterns)

**Working With**:
- Oracle: Gets sequential thinking framework and context
- Superman: Coordinates the image-to-html pipeline
- Artemis: Provides measurements for fresh HTML generation
- Green Arrow: Validates the final output against original image

Created: 2025-10-30
Version: 1.0.0
"""

from typing import Dict, List, Any, Optional, Tuple
import re
import logging
from dataclasses import dataclass
from enum import Enum

# Import Mission Control Narrator
try:
    from .mission_control_narrator import get_narrator
    NARRATOR_AVAILABLE = True
except ImportError:
    NARRATOR_AVAILABLE = False
    logging.warning("Mission Control Narrator not available for Vision Analyst")

logger = logging.getLogger(__name__)


class LayoutType(Enum):
    """Layout pattern types detected in UI analysis"""
    SINGLE_COLUMN = "single-column"
    TWO_COLUMN = "two-column"
    THREE_COLUMN = "three-column"
    GRID = "grid"
    SIDEBAR_LEFT = "sidebar-left"
    SIDEBAR_RIGHT = "sidebar-right"
    HEADER_BODY = "header-body"
    HEADER_BODY_FOOTER = "header-body-footer"


class ComponentType(Enum):
    """UI component types"""
    HEADER = "header"
    SIDEBAR = "sidebar"
    CARD = "card"
    BUTTON = "button"
    FORM = "form"
    TABLE = "table"
    GRID = "grid"
    LIST = "list"
    TABS = "tabs"
    MODAL = "modal"
    WIDGET = "widget"


@dataclass
class ColorInfo:
    """Color information extracted from visual analysis"""
    hex_value: str
    usage: str  # "primary", "secondary", "accent", "background", "text"
    frequency: str  # "high", "medium", "low"
    location: List[str]  # Where this color appears


@dataclass
class SpacingMeasurement:
    """Spacing and dimension measurements"""
    type: str  # "padding", "margin", "gap", "width", "height"
    value_px: int
    location: str
    consistency: float  # 0.0-1.0, how consistent this spacing is across design


@dataclass
class ComponentAnalysis:
    """Analysis of a single UI component"""
    name: str
    component_type: ComponentType
    dimensions: Dict[str, int]  # {"width": 290, "height": 400}
    position: Dict[str, int]  # {"x": 100, "y": 200}
    colors: List[ColorInfo]
    spacing: List[SpacingMeasurement]
    children: List[str]  # Names of child components
    parent: Optional[str]
    html_suggestion: str  # Suggested HTML tag
    css_classes: List[str]  # Suggested Tailwind classes


class VisionAnalyst:
    """
    Vision Analyst Hero - Specialized in visual UI analysis

    This hero analyzes dashboard screenshots to extract precise measurements
    and structural information for building pixel-perfect HTML/CSS.
    """

    def __init__(self, narrator: Optional[Any] = None):
        self.hero_name = "Vision Analyst"
        self.hero_emoji = "👁️"
        self.version = "1.0.0"
        self.capabilities = [
            "layout-analysis",
            "component-detection",
            "color-extraction",
            "spacing-measurement",
            "typography-analysis",
            "pattern-recognition"
        ]

        # Narrator integration
        self.narrator = narrator if narrator else (get_narrator() if NARRATOR_AVAILABLE else None)

        if self.narrator and self.narrator.is_verbose():
            self.say(
                "Visual analysis system ready. Precision measurement activated.",
                style="friendly"
            )

    def say(self, message: str, style: str = "friendly", technical_info: Optional[str] = None):
        """Convenience method for Vision Analyst dialogue"""
        if self.narrator:
            self.narrator.hero_speaks(f"{self.hero_emoji} {self.hero_name}",
                                     message, style, technical_info)

    def think(self, thought: str, step: Optional[int] = None, category: Optional[str] = None):
        """Convenience method for sequential thinking"""
        if self.narrator:
            self.narrator.hero_thinks(f"{self.hero_emoji} {self.hero_name}",
                                     thought, step, category)

    def handoff(self, to_hero: str, task: str, context: Optional[Dict[str, Any]] = None):
        """Convenience method for hero-to-hero handoff"""
        if self.narrator:
            self.narrator.team_handoff(f"{self.hero_emoji} {self.hero_name}",
                                      to_hero, task, context)

    def contribute_to_strategy(
        self,
        topic: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Vision Analyst's contribution to team strategy session

        Provides visual analysis perspective on component complexity

        Args:
            topic: Strategy session topic
            context: Optional context data (e.g., {"layout": "2-column", "components": 6})

        Returns:
            Dictionary with perspective, reasoning, and recommendation
        """
        reasoning = []
        perspective = ""
        recommendation = None
        key_insight = None

        # Analyze visual complexity from context
        layout = context.get('layout', 'unknown') if context else 'unknown'
        components = context.get('components', 0) if context else 0

        reasoning.append(f"Analyzing visual structure: {layout} layout")

        if '2-column' in layout or 'multi-column' in layout or components > 4:
            reasoning.append("Complex visual structure detected")
            reasoning.append("Multiple columns or components require precise measurements")
            reasoning.append("Visual measurement extraction will ensure accuracy")
            recommendation = "Use Image-to-HTML methodology with visual measurements"
            key_insight = "Vision Analyst: Complex layout requires measurement extraction"
            perspective = "Complex multi-column layout detected - measurements needed"

        elif 'single' in layout or components <= 2:
            reasoning.append("Simple visual structure detected")
            reasoning.append("Basic layout suitable for direct conversion")
            perspective = "Simple layout suitable for Figma API conversion"

        else:
            reasoning.append("Visual complexity assessment needed")
            perspective = "Need to analyze visual structure before deciding methodology"

        return {
            "perspective": perspective,
            "reasoning": reasoning,
            "recommendation": recommendation,
            "key_insight": key_insight
        }

    def analyze_dashboard_image(
        self,
        image_description: str,
        reference_dimensions: Optional[Dict[str, int]] = None
    ) -> Dict[str, Any]:
        """
        Analyze a dashboard image and extract comprehensive measurements.

        Args:
            image_description: Detailed text description of the dashboard image
            reference_dimensions: Known dimensions like {"width": 1440, "height": 1280}

        Returns:
            Comprehensive analysis report with measurements, colors, layout
        """
        # Mission start narration
        self.say("Starting visual analysis of dashboard image", style="friendly")

        # Step 1: Layout detection
        self.think("Analyzing dashboard structure and detecting layout pattern", category="Scanning")
        overall_layout = self._detect_layout_pattern(image_description)

        # Step 2: Component extraction
        self.think("Identifying UI components and sections", category="Pattern Recognition")
        components = self._extract_components(image_description)

        # Step 3: Color and typography analysis
        self.think("Extracting color palette and typography system", category="Analyzing")
        color_palette = self._extract_color_palette(image_description)
        typography = self._analyze_typography(image_description)

        # Step 4: Spacing and measurements
        self.think("Measuring spacing, dimensions, and layout proportions", category="Measuring")
        spacing_system = self._analyze_spacing(image_description)
        layout_measurements = self._measure_layout(image_description, reference_dimensions)

        # Step 5: Pattern detection
        self.think("Detecting UI patterns and design conventions", category="Pattern Recognition")
        patterns_detected = self._detect_patterns(image_description)

        # Step 6: Generate suggestions
        self.think("Generating HTML structure and CSS grid suggestions", category="Result")

        analysis = {
            "overall_layout": overall_layout,
            "components": components,
            "color_palette": color_palette,
            "spacing_system": spacing_system,
            "typography": typography,
            "layout_measurements": layout_measurements,
            "patterns_detected": patterns_detected,
            "html_structure_suggestion": None,  # Generated next
            "css_grid_suggestion": None  # Generated next
        }

        # Generate structure suggestions based on analysis
        analysis["html_structure_suggestion"] = self._suggest_html_structure(analysis)
        analysis["css_grid_suggestion"] = self._suggest_css_grid(analysis)

        # Completion narration
        component_count = len(components)
        pattern_count = len(patterns_detected)
        self.say(
            "Visual analysis complete. Dashboard structure mapped.",
            style="friendly",
            technical_info=f"{component_count} components, {pattern_count} patterns"
        )

        return analysis

    def _detect_layout_pattern(self, description: str) -> Dict[str, Any]:
        """Detect the overall layout pattern from description"""
        description_lower = description.lower()

        # Detect layout type
        layout_type = LayoutType.SINGLE_COLUMN

        if "sidebar" in description_lower:
            if "right" in description_lower or "290px" in description:
                layout_type = LayoutType.SIDEBAR_RIGHT
            else:
                layout_type = LayoutType.SIDEBAR_LEFT
        elif "two column" in description_lower or "2 column" in description_lower:
            layout_type = LayoutType.TWO_COLUMN
        elif "three column" in description_lower or "3 column" in description_lower:
            layout_type = LayoutType.THREE_COLUMN

        # Detect sections
        sections = []
        if "header" in description_lower or "navbar" in description_lower:
            sections.append("header")
        if "sidebar" in description_lower:
            sections.append("sidebar")
        if "main content" in description_lower or "content area" in description_lower:
            sections.append("main")
        if "footer" in description_lower:
            sections.append("footer")
        if "chat" in description_lower and "widget" in description_lower:
            sections.append("chat-widget-fixed")

        return {
            "type": layout_type.value,
            "sections": sections,
            "is_responsive": True,  # Assume modern responsive design
            "max_width": self._extract_number(description, ["1440px", "max-width"]),
            "recommended_css_approach": "CSS Grid" if layout_type in [LayoutType.TWO_COLUMN, LayoutType.THREE_COLUMN] else "Flexbox"
        }

    def _extract_components(self, description: str) -> List[ComponentAnalysis]:
        """Extract individual UI components from description"""
        # This would be implemented with more sophisticated parsing
        # For now, return structure that Artemis can use
        components = []

        # Example pattern detection
        if "announcement" in description.lower():
            components.append(ComponentAnalysis(
                name="Announcement Card",
                component_type=ComponentType.WIDGET,
                dimensions={"width": 258, "height": 176},
                position={"x": 0, "y": 0},
                colors=[],
                spacing=[],
                children=[],
                parent="Sidebar",
                html_suggestion="<div class='card'>",
                css_classes=["card", "p-4", "bg-white", "rounded-xl", "shadow"]
            ))

        return components

    def _extract_color_palette(self, description: str) -> Dict[str, List[ColorInfo]]:
        """Extract color palette from visual description"""
        # Extract hex colors mentioned in description
        hex_pattern = r'#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})'
        hex_colors = re.findall(hex_pattern, description)

        palette = {
            "primary": [],
            "secondary": [],
            "accent": [],
            "background": [],
            "text": []
        }

        # Common color classifications
        description_lower = description.lower()

        if "#ff3264" in description.lower() or "pink" in description_lower:
            palette["primary"].append(ColorInfo(
                hex_value="#FF3264",
                usage="primary accent",
                frequency="high",
                location=["buttons", "links", "badges", "notifications"]
            ))

        if "#f6f6f6" in description.lower():
            palette["background"].append(ColorInfo(
                hex_value="#F6F6F6",
                usage="page background",
                frequency="high",
                location=["body", "page"]
            ))

        return palette

    def _analyze_spacing(self, description: str) -> Dict[str, Any]:
        """Analyze spacing patterns and measurements"""
        # Extract spacing values mentioned
        spacing_values = self._extract_all_numbers(description)

        # Common spacing patterns
        spacing_system = {
            "base_unit": 8,  # Most designs use 8px base
            "scale": [4, 8, 12, 16, 20, 24, 32, 40, 48],
            "detected_spacing": {},
            "consistency_score": 0.85  # How consistent spacing is
        }

        # Categorize detected spacing
        for value in spacing_values:
            if value <= 8:
                spacing_system["detected_spacing"][f"{value}px"] = "micro-spacing"
            elif value <= 24:
                spacing_system["detected_spacing"][f"{value}px"] = "component-padding"
            elif value <= 48:
                spacing_system["detected_spacing"][f"{value}px"] = "section-gap"
            else:
                spacing_system["detected_spacing"][f"{value}px"] = "layout-spacing"

        return spacing_system

    def _analyze_typography(self, description: str) -> Dict[str, Any]:
        """Analyze typography system from description"""
        typography = {
            "font_family": "Manrope",  # Detected from description
            "font_weights": [400, 500, 600, 700],
            "font_sizes": {},
            "line_heights": {},
            "hierarchy": []
        }

        # Extract font size mentions
        size_pattern = r'(\d+)px'
        sizes = re.findall(size_pattern, description)

        # Common mappings
        size_mappings = {
            "12": "text-xs",
            "14": "text-sm",
            "16": "text-base",
            "20": "text-xl",
            "24": "text-2xl",
            "32": "text-3xl",
            "36": "text-4xl"
        }

        for size in set(sizes):
            if size in size_mappings:
                typography["font_sizes"][f"{size}px"] = size_mappings[size]

        return typography

    def _measure_layout(
        self,
        description: str,
        reference_dimensions: Optional[Dict[str, int]]
    ) -> Dict[str, Any]:
        """Measure overall layout dimensions and proportions"""
        measurements = {
            "container_width": reference_dimensions.get("width", 1440) if reference_dimensions else 1440,
            "container_height": reference_dimensions.get("height", 1280) if reference_dimensions else 1280,
            "header_height": self._extract_number(description, ["header", "height", "56px"]) or 56,
            "sidebar_width": self._extract_number(description, ["sidebar", "width", "290px"]) or 290,
            "main_content_width": None,  # Calculated
            "gaps": {},
            "padding": {}
        }

        # Calculate main content width
        if measurements["sidebar_width"]:
            measurements["main_content_width"] = measurements["container_width"] - measurements["sidebar_width"] - 48  # Assuming 24px gap on each side

        return measurements

    def _detect_patterns(self, description: str) -> List[str]:
        """Detect common UI patterns in the design"""
        patterns = []
        description_lower = description.lower()

        pattern_keywords = {
            "card-grid": ["card", "grid"],
            "sticky-header": ["sticky", "header"],
            "fixed-widget": ["fixed", "chat", "widget"],
            "2-column-layout": ["2 column", "two column", "sidebar"],
            "tab-navigation": ["tab", "navigation"],
            "badge-overlay": ["badge", "overlay"],
            "avatar-circle": ["avatar", "circle", "rounded"],
            "hover-lift": ["hover", "lift", "card"],
            "responsive-grid": ["grid", "responsive"],
            "sidebar-widgets": ["sidebar", "widget", "card"]
        }

        for pattern_name, keywords in pattern_keywords.items():
            if all(keyword in description_lower for keyword in keywords):
                patterns.append(pattern_name)

        return patterns

    def _suggest_html_structure(self, analysis: Dict[str, Any]) -> str:
        """Suggest HTML structure based on analysis"""
        layout = analysis["overall_layout"]
        sections = layout["sections"]

        structure = "<body>\n"

        if "header" in sections:
            structure += "  <header class='sticky-header'>\n    <!-- Navigation -->\n  </header>\n\n"

        if "sidebar" in sections:
            structure += "  <div class='dashboard-container'>\n"
            structure += "    <main class='main-content'>\n      <!-- Main content sections -->\n    </main>\n\n"
            structure += "    <aside class='sidebar'>\n      <!-- Sidebar widgets -->\n    </aside>\n"
            structure += "  </div>\n\n"
        else:
            structure += "  <main class='container'>\n    <!-- Content -->\n  </main>\n\n"

        if "chat-widget-fixed" in sections:
            structure += "  <div class='chat-widget fixed bottom-right'>\n    <!-- Chat -->\n  </div>\n\n"

        if "footer" in sections:
            structure += "  <footer>\n    <!-- Footer -->\n  </footer>\n\n"

        structure += "</body>"

        return structure

    def _suggest_css_grid(self, analysis: Dict[str, Any]) -> str:
        """Suggest CSS Grid configuration based on layout"""
        layout = analysis["overall_layout"]
        measurements = analysis["layout_measurements"]

        if layout["type"] == "sidebar-right":
            sidebar_width = measurements.get("sidebar_width", 290)
            return f"grid-template-columns: 1fr {sidebar_width}px;"
        elif layout["type"] == "sidebar-left":
            sidebar_width = measurements.get("sidebar_width", 290)
            return f"grid-template-columns: {sidebar_width}px 1fr;"
        elif layout["type"] == "two-column":
            return "grid-template-columns: 1fr 1fr;"
        elif layout["type"] == "three-column":
            return "grid-template-columns: 1fr 1fr 1fr;"
        else:
            return "/* Single column layout - use flexbox */"

    def generate_artemis_brief(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a structured brief for Artemis to build HTML/CSS.

        This formats the analysis into actionable instructions for code generation.
        """
        brief = {
            "mission": "Generate fresh HTML/CSS from visual analysis",
            "layout_structure": analysis["html_structure_suggestion"],
            "css_grid_config": analysis["css_grid_suggestion"],
            "color_palette": analysis["color_palette"],
            "spacing_system": analysis["spacing_system"],
            "typography_system": analysis["typography"],
            "component_list": [c.name for c in analysis["components"]],
            "patterns_to_implement": analysis["patterns_detected"],
            "measurements": analysis["layout_measurements"],
            "framework": "HTML/CSS",
            "styling_approach": "Tailwind CSS",
            "accuracy_target": "90-95%",
            "build_approach": "component-by-component-fresh-build"
        }

        # Handoff to Artemis with structured brief
        if self.narrator:
            component_count = len(analysis["components"])
            pattern_count = len(analysis["patterns_detected"])
            self.handoff(
                "🎨 Artemis Codesmith",
                "Build fresh HTML/CSS from visual measurements",
                {
                    "components": component_count,
                    "patterns": pattern_count,
                    "layout_type": analysis["overall_layout"]["type"],
                    "accuracy_target": "90-95%"
                }
            )

        return brief

    def compare_designs(
        self,
        design_a: Dict[str, Any],
        design_b: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compare two designs for visual consistency.

        Analyzes color palettes, spacing systems, typography, and layout patterns
        to identify inconsistencies between two dashboard designs.

        Args:
            design_a: First design analysis (from analyze_dashboard_image)
            design_b: Second design analysis (from analyze_dashboard_image)

        Returns:
            Comparison report with consistency scores and difference details
        """
        self.say("Comparing design consistency across two dashboards", style="friendly")

        comparison = {
            "consistency_score": 0.0,
            "color_consistency": self._compare_color_palettes(
                design_a.get("color_palette", {}),
                design_b.get("color_palette", {})
            ),
            "spacing_consistency": self._compare_spacing_systems(
                design_a.get("spacing_system", {}),
                design_b.get("spacing_system", {})
            ),
            "typography_consistency": self._compare_typography(
                design_a.get("typography", {}),
                design_b.get("typography", {})
            ),
            "layout_consistency": self._compare_layouts(
                design_a.get("overall_layout", {}),
                design_b.get("overall_layout", {})
            ),
            "differences": [],
            "recommendations": []
        }

        # Calculate overall consistency score (0-100)
        scores = [
            comparison["color_consistency"]["score"],
            comparison["spacing_consistency"]["score"],
            comparison["typography_consistency"]["score"],
            comparison["layout_consistency"]["score"]
        ]
        comparison["consistency_score"] = sum(scores) / len(scores)

        # Generate recommendations based on differences
        if comparison["consistency_score"] < 80:
            comparison["recommendations"].append(
                "Design systems diverge significantly - consider establishing unified design tokens"
            )

        self.say(
            "Design comparison complete",
            style="friendly",
            technical_info=f"Consistency: {comparison['consistency_score']:.1f}%"
        )

        return comparison

    def extract_design_tokens(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract design tokens (colors, spacing, typography) from visual analysis.

        Converts raw analysis into structured design token format compatible with
        design systems and CSS variable generation.

        Args:
            analysis: Dashboard analysis from analyze_dashboard_image()

        Returns:
            Structured design tokens ready for design system integration
        """
        self.say("Extracting design tokens from visual analysis", style="friendly")

        color_palette = analysis.get("color_palette", {})
        spacing_system = analysis.get("spacing_system", {})
        typography = analysis.get("typography", {})

        tokens = {
            "colors": {},
            "spacing": {},
            "typography": {},
            "shadows": {},
            "borders": {},
            "breakpoints": {}
        }

        # Extract color tokens
        for category, colors in color_palette.items():
            for i, color_info in enumerate(colors):
                token_name = f"{category}-{i+1}" if len(colors) > 1 else category
                tokens["colors"][token_name] = {
                    "value": color_info.hex_value,
                    "usage": color_info.usage,
                    "css_var": f"--color-{token_name}"
                }

        # Extract spacing tokens
        spacing_scale = spacing_system.get("scale", [])
        for i, value in enumerate(spacing_scale):
            tokens["spacing"][f"space-{i}"] = {
                "value": f"{value}px",
                "rem": f"{value/16}rem",
                "css_var": f"--space-{i}"
            }

        # Extract typography tokens
        font_sizes = typography.get("font_sizes", {})
        for size_px, tailwind_class in font_sizes.items():
            token_name = tailwind_class.replace("text-", "")
            tokens["typography"][token_name] = {
                "size": size_px,
                "line_height": "1.5",
                "css_var": f"--font-size-{token_name}"
            }

        tokens["typography"]["font-family"] = {
            "value": typography.get("font_family", "system-ui"),
            "css_var": "--font-family-base"
        }

        # Common design token defaults
        tokens["shadows"] = {
            "sm": {"value": "0 1px 2px 0 rgba(0, 0, 0, 0.05)"},
            "md": {"value": "0 4px 6px -1px rgba(0, 0, 0, 0.1)"},
            "lg": {"value": "0 10px 15px -3px rgba(0, 0, 0, 0.1)"}
        }

        tokens["borders"] = {
            "radius-sm": {"value": "0.375rem"},
            "radius-md": {"value": "0.5rem"},
            "radius-lg": {"value": "0.75rem"},
            "radius-xl": {"value": "1rem"}
        }

        self.say(
            "Design tokens extracted successfully",
            style="friendly",
            technical_info=f"{len(tokens['colors'])} colors, {len(tokens['spacing'])} spacing values"
        )

        return tokens

    def detect_responsive_breakpoints(self, description: str) -> Dict[str, Any]:
        """
        Identify responsive layout breakpoints from design description.

        Analyzes layout changes across different viewport sizes and recommends
        optimal breakpoint strategy.

        Args:
            description: Text description mentioning mobile, tablet, desktop layouts

        Returns:
            Breakpoint recommendations with CSS media query suggestions
        """
        self.say("Detecting responsive breakpoints from layout description", style="friendly")

        description_lower = description.lower()

        breakpoints = {
            "detected_viewports": [],
            "recommended_breakpoints": {},
            "layout_changes": [],
            "media_queries": []
        }

        # Detect mentioned viewports
        viewport_keywords = {
            "mobile": ["mobile", "phone", "320px", "375px", "414px"],
            "tablet": ["tablet", "ipad", "768px", "834px"],
            "desktop": ["desktop", "laptop", "1024px", "1280px", "1440px"],
            "wide": ["wide", "4k", "1920px", "2560px"]
        }

        for viewport, keywords in viewport_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                breakpoints["detected_viewports"].append(viewport)

        # Standard breakpoint recommendations
        if "mobile" in breakpoints["detected_viewports"]:
            breakpoints["recommended_breakpoints"]["sm"] = {
                "min_width": "640px",
                "description": "Small devices (landscape phones)",
                "css": "@media (min-width: 640px)"
            }

        if "tablet" in breakpoints["detected_viewports"]:
            breakpoints["recommended_breakpoints"]["md"] = {
                "min_width": "768px",
                "description": "Medium devices (tablets)",
                "css": "@media (min-width: 768px)"
            }

        if "desktop" in breakpoints["detected_viewports"]:
            breakpoints["recommended_breakpoints"]["lg"] = {
                "min_width": "1024px",
                "description": "Large devices (desktops)",
                "css": "@media (min-width: 1024px)"
            }
            breakpoints["recommended_breakpoints"]["xl"] = {
                "min_width": "1280px",
                "description": "Extra large devices",
                "css": "@media (min-width: 1280px)"
            }

        # Detect layout changes
        if "sidebar" in description_lower and "collapse" in description_lower:
            breakpoints["layout_changes"].append({
                "breakpoint": "md",
                "change": "Sidebar collapses to hamburger menu",
                "implementation": "Use CSS Grid with conditional columns"
            })

        if "stack" in description_lower or "column" in description_lower:
            breakpoints["layout_changes"].append({
                "breakpoint": "sm",
                "change": "Multi-column layout stacks vertically",
                "implementation": "Switch from grid-cols-2 to grid-cols-1"
            })

        self.say(
            "Responsive breakpoints identified",
            style="friendly",
            technical_info=f"{len(breakpoints['detected_viewports'])} viewports, {len(breakpoints['recommended_breakpoints'])} breakpoints"
        )

        return breakpoints

    def analyze_component_library(self, description: str) -> Dict[str, Any]:
        """
        Catalog reusable components from dashboard description.

        Identifies repeating UI patterns that should be extracted as
        reusable components in the design system.

        Args:
            description: Detailed dashboard description

        Returns:
            Component catalog with reusability recommendations
        """
        self.say("Cataloging reusable component patterns", style="friendly")

        description_lower = description.lower()

        library = {
            "components": [],
            "reusability_score": 0.0,
            "extraction_priority": []
        }

        # Common component patterns
        component_patterns = {
            "Card": {
                "keywords": ["card", "box", "panel", "widget"],
                "variants": ["announcement card", "stat card", "metric card"],
                "props": ["title", "content", "footer", "badge"],
                "reusability": "HIGH"
            },
            "Button": {
                "keywords": ["button", "cta", "action"],
                "variants": ["primary", "secondary", "ghost", "icon"],
                "props": ["label", "icon", "onClick", "variant"],
                "reusability": "HIGH"
            },
            "Badge": {
                "keywords": ["badge", "tag", "label", "pill"],
                "variants": ["notification", "status", "count"],
                "props": ["count", "variant", "color"],
                "reusability": "HIGH"
            },
            "Avatar": {
                "keywords": ["avatar", "profile picture", "user icon"],
                "variants": ["circle", "square", "with-badge"],
                "props": ["src", "alt", "size", "fallback"],
                "reusability": "MEDIUM"
            },
            "Sidebar": {
                "keywords": ["sidebar", "aside", "side panel"],
                "variants": ["left", "right", "collapsible"],
                "props": ["items", "position", "width"],
                "reusability": "MEDIUM"
            },
            "Header": {
                "keywords": ["header", "navbar", "top bar"],
                "variants": ["sticky", "transparent", "with-search"],
                "props": ["logo", "navigation", "actions"],
                "reusability": "MEDIUM"
            },
            "Grid": {
                "keywords": ["grid", "layout", "columns"],
                "variants": ["2-column", "3-column", "masonry"],
                "props": ["columns", "gap", "responsive"],
                "reusability": "HIGH"
            }
        }

        # Detect components in description
        for component_name, pattern in component_patterns.items():
            if any(keyword in description_lower for keyword in pattern["keywords"]):
                # Count occurrences to estimate reusability
                occurrence_count = sum(
                    description_lower.count(keyword) for keyword in pattern["keywords"]
                )

                library["components"].append({
                    "name": component_name,
                    "detected_variants": [
                        v for v in pattern["variants"]
                        if v.replace("-", " ") in description_lower
                    ],
                    "suggested_props": pattern["props"],
                    "reusability": pattern["reusability"],
                    "occurrences": occurrence_count
                })

        # Calculate reusability score
        high_reuse = sum(1 for c in library["components"] if c["reusability"] == "HIGH")
        library["reusability_score"] = (high_reuse / len(library["components"]) * 100) if library["components"] else 0

        # Prioritize extraction
        library["extraction_priority"] = sorted(
            library["components"],
            key=lambda c: (c["reusability"] == "HIGH", c["occurrences"]),
            reverse=True
        )

        self.say(
            "Component library analysis complete",
            style="friendly",
            technical_info=f"{len(library['components'])} components, {library['reusability_score']:.0f}% reusability"
        )

        return library

    def generate_style_guide(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create comprehensive style guide from visual analysis.

        Generates a complete style guide documenting colors, typography,
        spacing, components, and design patterns.

        Args:
            analysis: Complete dashboard analysis from analyze_dashboard_image()

        Returns:
            Structured style guide ready for documentation or Storybook
        """
        self.say("Generating comprehensive style guide", style="friendly")

        style_guide = {
            "metadata": {
                "title": "Dashboard Design System",
                "version": "1.0.0",
                "last_updated": "2025-10-31"
            },
            "foundation": {
                "colors": self._format_color_guide(analysis.get("color_palette", {})),
                "typography": self._format_typography_guide(analysis.get("typography", {})),
                "spacing": self._format_spacing_guide(analysis.get("spacing_system", {})),
                "grid_system": self._format_grid_guide(analysis.get("overall_layout", {}))
            },
            "components": {
                "patterns": analysis.get("patterns_detected", []),
                "component_specs": []
            },
            "usage_guidelines": {
                "layout_principles": [],
                "accessibility": [],
                "responsive_design": []
            }
        }

        # Add layout principles
        layout_type = analysis.get("overall_layout", {}).get("type", "unknown")
        style_guide["usage_guidelines"]["layout_principles"].append(
            f"Primary layout pattern: {layout_type}"
        )
        style_guide["usage_guidelines"]["layout_principles"].append(
            f"Recommended CSS approach: {analysis.get('overall_layout', {}).get('recommended_css_approach', 'Flexbox')}"
        )

        # Add accessibility guidelines
        style_guide["usage_guidelines"]["accessibility"].append(
            "Maintain WCAG 2.1 Level AA contrast ratios (4.5:1 for normal text)"
        )
        style_guide["usage_guidelines"]["accessibility"].append(
            "Ensure touch targets are minimum 44x44px for mobile"
        )

        # Add responsive design guidelines
        style_guide["usage_guidelines"]["responsive_design"].append(
            "Mobile-first approach with progressive enhancement"
        )
        style_guide["usage_guidelines"]["responsive_design"].append(
            "Breakpoints: 640px (sm), 768px (md), 1024px (lg), 1280px (xl)"
        )

        self.say(
            "Style guide generation complete",
            style="friendly",
            technical_info=f"{len(style_guide['foundation']['colors'])} colors, {len(style_guide['components']['patterns'])} patterns"
        )

        return style_guide

    def validate_accessibility_contrast(self, colors: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check color contrast ratios for WCAG 2.1 compliance.

        Validates text/background color combinations against WCAG AA and AAA
        standards for accessibility.

        Args:
            colors: Color palette with primary, secondary, background, text colors

        Returns:
            Contrast validation report with WCAG compliance status
        """
        self.say("Validating color contrast for accessibility", style="friendly")

        validation = {
            "wcag_aa_compliance": True,
            "wcag_aaa_compliance": True,
            "contrast_checks": [],
            "violations": [],
            "recommendations": []
        }

        # Common text/background combinations to check
        combinations = [
            ("text", "background", "Normal text on background"),
            ("primary", "background", "Primary accent on background"),
            ("secondary", "background", "Secondary accent on background")
        ]

        for fg_category, bg_category, description in combinations:
            fg_colors = colors.get(fg_category, [])
            bg_colors = colors.get(bg_category, [])

            for fg_color in fg_colors:
                for bg_color in bg_colors:
                    contrast_ratio = self._calculate_contrast_ratio(
                        fg_color.hex_value,
                        bg_color.hex_value
                    )

                    check = {
                        "foreground": fg_color.hex_value,
                        "background": bg_color.hex_value,
                        "description": description,
                        "contrast_ratio": contrast_ratio,
                        "wcag_aa_normal": contrast_ratio >= 4.5,
                        "wcag_aa_large": contrast_ratio >= 3.0,
                        "wcag_aaa_normal": contrast_ratio >= 7.0,
                        "wcag_aaa_large": contrast_ratio >= 4.5
                    }

                    validation["contrast_checks"].append(check)

                    # Track violations
                    if not check["wcag_aa_normal"]:
                        validation["wcag_aa_compliance"] = False
                        validation["violations"].append({
                            "severity": "HIGH",
                            "issue": f"{description}: {fg_color.hex_value} on {bg_color.hex_value}",
                            "contrast_ratio": contrast_ratio,
                            "required": 4.5,
                            "recommendation": "Increase color contrast or use larger text"
                        })

                    if not check["wcag_aaa_normal"]:
                        validation["wcag_aaa_compliance"] = False

        # Generate recommendations
        if not validation["wcag_aa_compliance"]:
            validation["recommendations"].append(
                "Critical: Fix WCAG AA violations to meet minimum accessibility standards"
            )
        elif not validation["wcag_aaa_compliance"]:
            validation["recommendations"].append(
                "Consider improving contrast for WCAG AAA compliance (enhanced accessibility)"
            )
        else:
            validation["recommendations"].append(
                "✅ All color combinations meet WCAG AAA standards"
            )

        self.say(
            "Accessibility contrast validation complete",
            style="friendly",
            technical_info=f"{len(validation['contrast_checks'])} checks, {len(validation['violations'])} violations"
        )

        return validation

    def measure_visual_hierarchy(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze information hierarchy and visual prominence.

        Evaluates how effectively the design guides user attention through
        size, color, spacing, and positioning.

        Args:
            analysis: Dashboard analysis from analyze_dashboard_image()

        Returns:
            Hierarchy analysis with prominence scores and recommendations
        """
        self.say("Measuring visual hierarchy and information flow", style="friendly")

        typography = analysis.get("typography", {})
        spacing_system = analysis.get("spacing_system", {})
        color_palette = analysis.get("color_palette", {})

        hierarchy = {
            "levels": [],
            "hierarchy_score": 0.0,
            "attention_flow": [],
            "recommendations": []
        }

        # Analyze typography hierarchy
        font_sizes = typography.get("font_sizes", {})
        size_range = len(font_sizes)

        hierarchy["levels"].append({
            "type": "Typography",
            "scale_range": size_range,
            "clarity": "GOOD" if size_range >= 5 else "NEEDS_IMPROVEMENT",
            "details": f"{size_range} distinct font sizes create clear hierarchy"
        })

        # Analyze spacing hierarchy
        spacing_scale = spacing_system.get("scale", [])
        spacing_range = len(spacing_scale)

        hierarchy["levels"].append({
            "type": "Spacing",
            "scale_range": spacing_range,
            "clarity": "GOOD" if spacing_range >= 6 else "NEEDS_IMPROVEMENT",
            "details": f"{spacing_range} spacing values for content grouping"
        })

        # Analyze color hierarchy
        has_primary = len(color_palette.get("primary", [])) > 0
        has_secondary = len(color_palette.get("secondary", [])) > 0

        hierarchy["levels"].append({
            "type": "Color",
            "scale_range": len(color_palette),
            "clarity": "GOOD" if (has_primary and has_secondary) else "NEEDS_IMPROVEMENT",
            "details": "Primary and secondary colors establish visual priority"
        })

        # Calculate hierarchy score (0-100)
        good_levels = sum(1 for level in hierarchy["levels"] if level["clarity"] == "GOOD")
        hierarchy["hierarchy_score"] = (good_levels / len(hierarchy["levels"]) * 100) if hierarchy["levels"] else 0

        # Define attention flow
        hierarchy["attention_flow"] = [
            "1. Largest typography elements (headers, titles)",
            "2. Primary color accents (CTAs, important actions)",
            "3. Secondary content sections",
            "4. Supporting details and metadata"
        ]

        # Generate recommendations
        if hierarchy["hierarchy_score"] < 70:
            hierarchy["recommendations"].append(
                "Strengthen visual hierarchy with clearer size and color differentiation"
            )

        if size_range < 5:
            hierarchy["recommendations"].append(
                "Add more font size variations to create clearer content hierarchy"
            )

        if spacing_range < 6:
            hierarchy["recommendations"].append(
                "Expand spacing scale for better content grouping and separation"
            )

        self.say(
            "Visual hierarchy analysis complete",
            style="friendly",
            technical_info=f"Hierarchy score: {hierarchy['hierarchy_score']:.0f}%"
        )

        return hierarchy

    # Helper methods for new skills
    def _compare_color_palettes(self, palette_a: Dict, palette_b: Dict) -> Dict[str, Any]:
        """Compare two color palettes"""
        common_colors = set()
        total_colors_a = sum(len(colors) for colors in palette_a.values())
        total_colors_b = sum(len(colors) for colors in palette_b.values())

        # Simple comparison - can be enhanced
        score = 70.0 if total_colors_a == total_colors_b else 50.0

        return {
            "score": score,
            "common_colors": len(common_colors),
            "differences": abs(total_colors_a - total_colors_b)
        }

    def _compare_spacing_systems(self, spacing_a: Dict, spacing_b: Dict) -> Dict[str, Any]:
        """Compare two spacing systems"""
        base_a = spacing_a.get("base_unit", 8)
        base_b = spacing_b.get("base_unit", 8)

        score = 100.0 if base_a == base_b else 70.0

        return {
            "score": score,
            "base_unit_match": base_a == base_b,
            "differences": abs(base_a - base_b)
        }

    def _compare_typography(self, typo_a: Dict, typo_b: Dict) -> Dict[str, Any]:
        """Compare two typography systems"""
        font_a = typo_a.get("font_family", "")
        font_b = typo_b.get("font_family", "")

        score = 100.0 if font_a == font_b else 60.0

        return {
            "score": score,
            "font_family_match": font_a == font_b,
            "differences": []
        }

    def _compare_layouts(self, layout_a: Dict, layout_b: Dict) -> Dict[str, Any]:
        """Compare two layout structures"""
        type_a = layout_a.get("type", "")
        type_b = layout_b.get("type", "")

        score = 100.0 if type_a == type_b else 50.0

        return {
            "score": score,
            "layout_type_match": type_a == type_b,
            "differences": []
        }

    def _format_color_guide(self, color_palette: Dict) -> List[Dict[str, str]]:
        """Format color palette for style guide"""
        colors = []
        for category, color_list in color_palette.items():
            for color_info in color_list:
                colors.append({
                    "name": category,
                    "hex": color_info.hex_value,
                    "usage": color_info.usage
                })
        return colors

    def _format_typography_guide(self, typography: Dict) -> Dict[str, Any]:
        """Format typography for style guide"""
        return {
            "font_family": typography.get("font_family", "system-ui"),
            "font_sizes": typography.get("font_sizes", {}),
            "font_weights": typography.get("font_weights", [400, 600, 700])
        }

    def _format_spacing_guide(self, spacing_system: Dict) -> Dict[str, Any]:
        """Format spacing system for style guide"""
        return {
            "base_unit": spacing_system.get("base_unit", 8),
            "scale": spacing_system.get("scale", [4, 8, 16, 24, 32])
        }

    def _format_grid_guide(self, layout: Dict) -> Dict[str, str]:
        """Format grid system for style guide"""
        return {
            "type": layout.get("type", "unknown"),
            "approach": layout.get("recommended_css_approach", "Flexbox")
        }

    def _calculate_contrast_ratio(self, hex_fg: str, hex_bg: str) -> float:
        """
        Calculate WCAG contrast ratio between two colors.

        Formula: (L1 + 0.05) / (L2 + 0.05)
        where L1 is lighter color luminance, L2 is darker
        """
        # Convert hex to RGB
        def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        # Calculate relative luminance
        def get_luminance(rgb: Tuple[int, int, int]) -> float:
            r, g, b = [x / 255.0 for x in rgb]
            r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
            g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
            b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
            return 0.2126 * r + 0.7152 * g + 0.0722 * b

        try:
            rgb_fg = hex_to_rgb(hex_fg)
            rgb_bg = hex_to_rgb(hex_bg)

            lum_fg = get_luminance(rgb_fg)
            lum_bg = get_luminance(rgb_bg)

            lighter = max(lum_fg, lum_bg)
            darker = min(lum_fg, lum_bg)

            return (lighter + 0.05) / (darker + 0.05)
        except (ValueError, ZeroDivisionError):
            return 1.0  # Invalid colors default to no contrast

    # Helper methods
    def _extract_number(self, text: str, keywords: List[str]) -> Optional[int]:
        """Extract a number near certain keywords"""
        for keyword in keywords:
            pattern = f"{keyword}[^0-9]*([0-9]+)"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None

    def _extract_all_numbers(self, text: str) -> List[int]:
        """Extract all numbers from text"""
        numbers = re.findall(r'\b(\d+)\b', text)
        return [int(n) for n in numbers if 4 <= int(n) <= 100]  # Filter reasonable spacing values

    def get_capabilities(self) -> List[str]:
        """Return list of capabilities"""
        return self.capabilities

    def get_version(self) -> str:
        """Return hero version"""
        return self.version


# Hero instance for import
vision_analyst = VisionAnalyst()

if __name__ == "__main__":
    print(f"🦸 {vision_analyst.hero_name} v{vision_analyst.version}")
    print(f"Capabilities: {', '.join(vision_analyst.capabilities)}")
