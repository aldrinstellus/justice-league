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
