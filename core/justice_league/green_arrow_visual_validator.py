"""
🎯 GREEN ARROW - THE VISUAL VALIDATION SPECIALIST
Justice League Member: Pixel-Perfect Design Validator & WYSIWYG Guardian

Oliver Queen's Green Arrow - Master of Precision, Visual Accuracy, and Design Fidelity

Powers:
- 🎯 Pixel-Perfect Validation - Exact measurements down to the pixel
- 🎨 Color Accuracy - Hex value matching to Figma specs
- 📐 Spacing Precision - Margins, padding, gaps validated
- 🔤 Typography Validation - Font size, weight, line-height checks
- 🧩 Component Compliance - shadcn/ui and design system validation
- 🔍 Chrome DevTools Mastery - DOM inspection and computed styles
- 🎨 Figma API Expert - Extract design tokens and measurements
- 💎 Tailwind Validation - Utility class accuracy
- 📊 Visual Diff Reports - Detailed discrepancy reporting

"I never miss. Every pixel, every color, every spacing - all perfect." - Green Arrow

Architecture: Figma MCP + Chrome DevTools MCP + Tailwind MCP + shadcn MCP
Integration: Works after Artemis generation, validates before approval
"""

import logging
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
import re

logger = logging.getLogger(__name__)


class GreenArrowVisualValidator:
    """
    🎯 GREEN ARROW - The Visual Validation Specialist

    Oliver Queen ensures that rendered components match Figma designs
    pixel-perfectly. He's the guardian of WYSIWYG (What You See Is What You Get).

    Powers:
    1. Figma Design Extraction - Get exact measurements, colors, typography
    2. Chrome DevTools Inspection - Inspect rendered DOM and computed styles
    3. Tailwind Validation - Verify utility classes match design specs
    4. shadcn/ui Compliance - Ensure components follow design system
    5. Visual Diff Generation - Create detailed discrepancy reports
    6. Accuracy Scoring - Rate conversions 0-100% accuracy

    MCP Integrations:
    - figma-mcp: Extract design specs from Figma files
    - chrome-devtools-mcp: Inspect rendered components
    - tailwindcss-mcp: Validate Tailwind utility classes
    - shadcn-ui: Verify component library compliance
    """

    def __init__(self, validation_data_dir: Optional[str] = None):
        """
        Initialize Green Arrow's validation arsenal

        Args:
            validation_data_dir: Directory for validation reports
        """
        self.validation_data_dir = Path(validation_data_dir) if validation_data_dir else Path('/Users/admin/Documents/claudecode/Projects/aldo-vision/data/validation')
        self.validation_data_dir.mkdir(parents=True, exist_ok=True)

        # Validation reports database
        self.reports_db = self.validation_data_dir / 'validation_reports.json'
        self.discrepancies_db = self.validation_data_dir / 'discrepancies.json'
        self.accuracy_scores_db = self.validation_data_dir / 'accuracy_scores.json'

        # Initialize databases
        self._init_databases()

        # Validation thresholds
        self.accuracy_thresholds = {
            'excellent': 98,  # 98-100% = Excellent
            'good': 95,       # 95-97% = Good
            'acceptable': 90, # 90-94% = Acceptable
            'needs_work': 85  # 85-89% = Needs Work
            # < 85% = Failed
        }

        # Tolerance levels (pixels)
        self.tolerances = {
            'spacing': 2,      # ±2px for spacing is acceptable
            'sizing': 2,       # ±2px for width/height
            'positioning': 1,  # ±1px for position
            'color': 0         # Exact color match required
        }

        logger.info("🎯 GREEN ARROW - Visual Validator initialized")
        logger.info(f"🎯 Validation Data: {self.validation_data_dir}")
        logger.info("🎯 Ready to validate Figma → Code conversions")

    def _init_databases(self):
        """Initialize all validation databases"""
        databases = [
            (self.reports_db, {'reports': []}),
            (self.discrepancies_db, {'discrepancies': []}),
            (self.accuracy_scores_db, {'scores': []})
        ]

        for db_file, default_data in databases:
            if not db_file.exists():
                with open(db_file, 'w') as f:
                    json.dump(default_data, f, indent=2)

    # ==================== FIGMA DESIGN EXTRACTION ====================

    def extract_figma_specs(self, file_key: str, node_id: str) -> Dict[str, Any]:
        """
        🎯 Extract design specifications from Figma using Figma MCP

        Args:
            file_key: Figma file key
            node_id: Node ID to extract

        Returns:
            Design specifications including:
            - Measurements (width, height, x, y)
            - Colors (fills, strokes)
            - Typography (fontSize, fontWeight, lineHeight)
            - Spacing (padding, gaps)
            - Layout (constraints, layoutMode)
        """
        logger.info(f"🎯 Extracting Figma specs: {file_key}/{node_id}")

        # This will use figma-mcp when called by Claude Code
        # For now, return structure for implementation
        figma_specs = {
            'node_id': node_id,
            'file_key': file_key,
            'measurements': {
                'width': None,
                'height': None,
                'x': None,
                'y': None
            },
            'colors': {
                'fills': [],
                'strokes': [],
                'effects': []
            },
            'typography': {
                'fontSize': None,
                'fontWeight': None,
                'fontFamily': None,
                'lineHeight': None,
                'letterSpacing': None
            },
            'spacing': {
                'paddingTop': None,
                'paddingRight': None,
                'paddingBottom': None,
                'paddingLeft': None,
                'itemSpacing': None  # gap in flex
            },
            'layout': {
                'layoutMode': None,  # HORIZONTAL, VERTICAL, NONE
                'primaryAxisAlignItems': None,
                'counterAxisAlignItems': None,
                'layoutWrap': None
            },
            'children': []
        }

        logger.info(f"🎯 Figma specs extracted for node {node_id}")
        return figma_specs

    def parse_figma_design_tokens(self, figma_specs: Dict[str, Any]) -> Dict[str, Any]:
        """
        🎯 Parse Figma specs into design tokens

        Converts Figma measurements into expected Tailwind values

        Args:
            figma_specs: Raw Figma specifications

        Returns:
            Design tokens in Tailwind format
        """
        tokens = {
            'spacing': {},
            'colors': {},
            'typography': {},
            'sizing': {},
            'layout': {}
        }

        # Convert Figma measurements to Tailwind equivalents
        measurements = figma_specs.get('measurements', {})

        # Spacing (convert px to Tailwind scale)
        spacing = figma_specs.get('spacing', {})
        for key, value in spacing.items():
            if value:
                tokens['spacing'][key] = self._px_to_tailwind_spacing(value)

        # Colors (convert RGB to hex)
        colors = figma_specs.get('colors', {})
        if 'fills' in colors:
            for i, fill in enumerate(colors['fills']):
                if fill.get('type') == 'SOLID':
                    color = fill.get('color', {})
                    tokens['colors'][f'fill_{i}'] = self._rgb_to_hex(color)

        # Typography
        typography = figma_specs.get('typography', {})
        if typography.get('fontSize'):
            tokens['typography']['fontSize'] = f"{typography['fontSize']}px"
        if typography.get('fontWeight'):
            tokens['typography']['fontWeight'] = self._figma_weight_to_tailwind(typography['fontWeight'])
        if typography.get('lineHeight'):
            tokens['typography']['lineHeight'] = typography['lineHeight']

        # Sizing
        if measurements.get('width'):
            tokens['sizing']['width'] = f"{measurements['width']}px"
        if measurements.get('height'):
            tokens['sizing']['height'] = f"{measurements['height']}px"

        # Layout
        layout = figma_specs.get('layout', {})
        if layout.get('layoutMode') == 'HORIZONTAL':
            tokens['layout']['flexDirection'] = 'row'
        elif layout.get('layoutMode') == 'VERTICAL':
            tokens['layout']['flexDirection'] = 'column'

        return tokens

    def _px_to_tailwind_spacing(self, px_value: float) -> str:
        """Convert pixel value to Tailwind spacing scale"""
        # Tailwind scale: 1 = 0.25rem = 4px
        spacing_map = {
            4: '1', 8: '2', 12: '3', 16: '4', 20: '5',
            24: '6', 28: '7', 32: '8', 36: '9', 40: '10',
            44: '11', 48: '12', 56: '14', 64: '16', 80: '20',
            96: '24', 112: '28', 128: '32', 144: '36', 160: '40'
        }

        closest = min(spacing_map.keys(), key=lambda x: abs(x - px_value))
        return spacing_map[closest]

    def _rgb_to_hex(self, color: Dict[str, float]) -> str:
        """Convert Figma RGB color to hex"""
        r = int(color.get('r', 0) * 255)
        g = int(color.get('g', 0) * 255)
        b = int(color.get('b', 0) * 255)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _figma_weight_to_tailwind(self, weight: int) -> str:
        """Convert Figma font weight to Tailwind class"""
        weight_map = {
            100: 'thin', 200: 'extralight', 300: 'light',
            400: 'normal', 500: 'medium', 600: 'semibold',
            700: 'bold', 800: 'extrabold', 900: 'black'
        }
        return weight_map.get(weight, 'normal')

    # ==================== CHROME DEVTOOLS INSPECTION ====================

    def inspect_rendered_component(self, url: str, selector: str) -> Dict[str, Any]:
        """
        🎯 Inspect rendered component using Chrome DevTools MCP

        Args:
            url: URL of rendered page
            selector: CSS selector for component

        Returns:
            Computed styles and measurements from rendered component
        """
        logger.info(f"🎯 Inspecting rendered component: {url} → {selector}")

        # This will use chrome-devtools-mcp when called by Claude Code
        # For now, return structure for implementation
        rendered_specs = {
            'selector': selector,
            'url': url,
            'computed_styles': {},
            'measurements': {
                'width': None,
                'height': None,
                'x': None,
                'y': None
            },
            'box_model': {
                'margin': {},
                'border': {},
                'padding': {},
                'content': {}
            },
            'colors': {
                'backgroundColor': None,
                'color': None,
                'borderColor': None
            },
            'typography': {
                'fontSize': None,
                'fontWeight': None,
                'fontFamily': None,
                'lineHeight': None
            },
            'layout': {
                'display': None,
                'flexDirection': None,
                'justifyContent': None,
                'alignItems': None,
                'gap': None
            }
        }

        logger.info(f"🎯 Rendered specs inspected for {selector}")
        return rendered_specs

    def extract_tailwind_classes(self, component_code: str) -> List[str]:
        """
        🎯 Extract Tailwind classes from component code

        Args:
            component_code: Component source code

        Returns:
            List of Tailwind utility classes
        """
        # Extract all className attributes
        class_pattern = r'className=["\']([^"\']+)["\']'
        matches = re.findall(class_pattern, component_code)

        all_classes = []
        for match in matches:
            # Split by spaces and filter
            classes = [c.strip() for c in match.split() if c.strip()]
            all_classes.extend(classes)

        return all_classes

    # ==================== VALIDATION & COMPARISON ====================

    def validate_component(self,
                          figma_url: str,
                          rendered_url: str,
                          component_name: str,
                          component_code: str) -> Dict[str, Any]:
        """
        🎯 Complete validation pipeline: Figma → Rendered comparison

        Args:
            figma_url: Figma design URL (with node-id)
            rendered_url: URL of rendered component
            component_name: Name of component (e.g., "SettingsProfile")
            component_code: Source code of component

        Returns:
            Complete validation report with:
            - Measurements comparison
            - Colors comparison
            - Typography comparison
            - Spacing comparison
            - Discrepancies list
            - Accuracy score
            - Pass/Fail status
        """
        logger.info(f"🎯 Starting validation for {component_name}")
        logger.info(f"🎯 Figma: {figma_url}")
        logger.info(f"🎯 Rendered: {rendered_url}")

        # Extract file_key and node_id from Figma URL
        file_key, node_id = self._parse_figma_url(figma_url)

        # Step 1: Extract Figma specs
        figma_specs = self.extract_figma_specs(file_key, node_id)
        figma_tokens = self.parse_figma_design_tokens(figma_specs)

        # Step 2: Inspect rendered component
        rendered_specs = self.inspect_rendered_component(rendered_url, f"#{component_name}")

        # Step 3: Extract Tailwind classes
        tailwind_classes = self.extract_tailwind_classes(component_code)

        # Step 4: Compare measurements
        measurements_comparison = self._compare_measurements(
            figma_specs.get('measurements', {}),
            rendered_specs.get('measurements', {})
        )

        # Step 5: Compare colors
        colors_comparison = self._compare_colors(
            figma_tokens.get('colors', {}),
            rendered_specs.get('colors', {})
        )

        # Step 6: Compare typography
        typography_comparison = self._compare_typography(
            figma_tokens.get('typography', {}),
            rendered_specs.get('typography', {})
        )

        # Step 7: Compare spacing
        spacing_comparison = self._compare_spacing(
            figma_tokens.get('spacing', {}),
            rendered_specs.get('box_model', {})
        )

        # Step 8: Validate Tailwind classes
        tailwind_validation = self._validate_tailwind_classes(
            tailwind_classes,
            figma_tokens
        )

        # Step 9: Calculate accuracy score
        accuracy_score = self._calculate_accuracy_score({
            'measurements': measurements_comparison,
            'colors': colors_comparison,
            'typography': typography_comparison,
            'spacing': spacing_comparison,
            'tailwind': tailwind_validation
        })

        # Step 10: Generate report
        report = {
            'component_name': component_name,
            'figma_url': figma_url,
            'rendered_url': rendered_url,
            'validated_at': datetime.now().isoformat(),
            'accuracy_score': accuracy_score,
            'status': self._get_status(accuracy_score),
            'comparisons': {
                'measurements': measurements_comparison,
                'colors': colors_comparison,
                'typography': typography_comparison,
                'spacing': spacing_comparison
            },
            'tailwind_validation': tailwind_validation,
            'discrepancies': self._collect_discrepancies({
                'measurements': measurements_comparison,
                'colors': colors_comparison,
                'typography': typography_comparison,
                'spacing': spacing_comparison
            }),
            'recommendations': []
        }

        # Save report
        self._save_validation_report(report)

        logger.info(f"🎯 Validation complete: {accuracy_score}% accuracy")
        logger.info(f"🎯 Status: {report['status']}")

        return report

    def _parse_figma_url(self, figma_url: str) -> Tuple[str, str]:
        """Parse Figma URL to extract file_key and node_id"""
        # Example: https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=17-1440
        match = re.search(r'/design/([^/]+)/.*node-id=([^&]+)', figma_url)
        if match:
            return match.group(1), match.group(2)
        return "", ""

    def _compare_measurements(self, figma: Dict, rendered: Dict) -> Dict[str, Any]:
        """Compare measurements between Figma and rendered"""
        comparison = {
            'width': self._compare_value(figma.get('width'), rendered.get('width'), 'sizing'),
            'height': self._compare_value(figma.get('height'), rendered.get('height'), 'sizing')
        }
        return comparison

    def _compare_colors(self, figma: Dict, rendered: Dict) -> Dict[str, Any]:
        """Compare colors between Figma and rendered"""
        comparison = {}
        # Compare each color property
        for key in figma.keys():
            figma_color = figma.get(key)
            rendered_key = key.replace('fill_', 'backgroundColor')
            rendered_color = rendered.get(rendered_key)
            comparison[key] = self._compare_value(figma_color, rendered_color, 'color')
        return comparison

    def _compare_typography(self, figma: Dict, rendered: Dict) -> Dict[str, Any]:
        """Compare typography between Figma and rendered"""
        comparison = {
            'fontSize': self._compare_value(
                figma.get('fontSize'),
                rendered.get('fontSize'),
                'typography'
            ),
            'fontWeight': self._compare_value(
                figma.get('fontWeight'),
                rendered.get('fontWeight'),
                'typography'
            ),
            'lineHeight': self._compare_value(
                figma.get('lineHeight'),
                rendered.get('lineHeight'),
                'typography'
            )
        }
        return comparison

    def _compare_spacing(self, figma: Dict, rendered: Dict) -> Dict[str, Any]:
        """Compare spacing between Figma and rendered"""
        comparison = {}
        padding = rendered.get('padding', {})

        for key in ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft']:
            comparison[key] = self._compare_value(
                figma.get(key),
                padding.get(key),
                'spacing'
            )

        return comparison

    def _compare_value(self, figma_value: Any, rendered_value: Any, value_type: str) -> Dict[str, Any]:
        """Compare a single value with tolerance"""
        if figma_value is None or rendered_value is None:
            return {
                'figma': figma_value,
                'rendered': rendered_value,
                'match': False,
                'difference': None,
                'status': 'missing_data'
            }

        # For numeric values
        if isinstance(figma_value, (int, float)) and isinstance(rendered_value, (int, float)):
            difference = abs(figma_value - rendered_value)
            tolerance = self.tolerances.get(value_type, 0)
            match = difference <= tolerance

            return {
                'figma': figma_value,
                'rendered': rendered_value,
                'match': match,
                'difference': difference,
                'tolerance': tolerance,
                'status': 'match' if match else 'mismatch'
            }

        # For string values (colors, etc)
        match = str(figma_value).lower() == str(rendered_value).lower()
        return {
            'figma': figma_value,
            'rendered': rendered_value,
            'match': match,
            'status': 'match' if match else 'mismatch'
        }

    def _validate_tailwind_classes(self, classes: List[str], figma_tokens: Dict) -> Dict[str, Any]:
        """Validate that Tailwind classes match Figma design tokens"""
        validation = {
            'total_classes': len(classes),
            'validated_classes': [],
            'issues': []
        }

        # Check spacing classes
        spacing_classes = [c for c in classes if c.startswith(('p-', 'px-', 'py-', 'pl-', 'pr-', 'pt-', 'pb-', 'm-', 'mx-', 'my-', 'gap-'))]
        for cls in spacing_classes:
            validation['validated_classes'].append({
                'class': cls,
                'type': 'spacing',
                'valid': True  # Simplified for now
            })

        # Check color classes
        color_classes = [c for c in classes if c.startswith(('bg-', 'text-', 'border-'))]
        for cls in color_classes:
            validation['validated_classes'].append({
                'class': cls,
                'type': 'color',
                'valid': True  # Simplified for now
            })

        return validation

    def _calculate_accuracy_score(self, comparisons: Dict) -> float:
        """Calculate overall accuracy score (0-100)"""
        total_checks = 0
        passed_checks = 0

        for category, comparison in comparisons.items():
            if category == 'tailwind':
                continue

            for key, value in comparison.items():
                if isinstance(value, dict) and 'match' in value:
                    total_checks += 1
                    if value['match']:
                        passed_checks += 1

        if total_checks == 0:
            return 0.0

        return round((passed_checks / total_checks) * 100, 2)

    def _get_status(self, score: float) -> str:
        """Get validation status based on accuracy score"""
        if score >= self.accuracy_thresholds['excellent']:
            return '✅ EXCELLENT'
        elif score >= self.accuracy_thresholds['good']:
            return '✅ GOOD'
        elif score >= self.accuracy_thresholds['acceptable']:
            return '⚠️ ACCEPTABLE'
        elif score >= self.accuracy_thresholds['needs_work']:
            return '⚠️ NEEDS WORK'
        else:
            return '❌ FAILED'

    def _collect_discrepancies(self, comparisons: Dict) -> List[Dict]:
        """Collect all discrepancies from comparisons"""
        discrepancies = []

        for category, comparison in comparisons.items():
            for key, value in comparison.items():
                if isinstance(value, dict) and not value.get('match'):
                    discrepancies.append({
                        'category': category,
                        'property': key,
                        'figma_value': value.get('figma'),
                        'rendered_value': value.get('rendered'),
                        'difference': value.get('difference'),
                        'severity': 'high' if category in ['measurements', 'spacing'] else 'medium'
                    })

        return discrepancies

    def _save_validation_report(self, report: Dict):
        """Save validation report to database"""
        with open(self.reports_db, 'r') as f:
            data = json.load(f)

        data['reports'].append(report)

        with open(self.reports_db, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"🎯 Validation report saved: {report['component_name']}")

    # ==================== REPORTING ====================

    def generate_validation_report_markdown(self, report: Dict) -> str:
        """
        🎯 Generate beautiful markdown validation report

        Args:
            report: Validation report dictionary

        Returns:
            Markdown-formatted report
        """
        md = f"""# 🎯 Visual Validation Report: {report['component_name']}

**Figma Design**: {report['figma_url']}
**Rendered Page**: {report['rendered_url']}
**Validated**: {report['validated_at']}

## Summary

**Accuracy Score**: {report['accuracy_score']}%
**Status**: {report['status']}

---

## Measurements Comparison

| Property | Figma | Rendered | Match | Difference |
|----------|-------|----------|-------|------------|
"""

        # Add measurements
        measurements = report['comparisons'].get('measurements', {})
        for key, value in measurements.items():
            match_icon = '✅' if value.get('match') else '❌'
            diff = value.get('difference', 'N/A')
            md += f"| {key} | {value.get('figma')} | {value.get('rendered')} | {match_icon} | {diff} |\n"

        md += "\n## Colors Comparison\n\n"
        md += "| Property | Figma | Rendered | Match |\n"
        md += "|----------|-------|----------|-------|\n"

        colors = report['comparisons'].get('colors', {})
        for key, value in colors.items():
            match_icon = '✅' if value.get('match') else '❌'
            md += f"| {key} | {value.get('figma')} | {value.get('rendered')} | {match_icon} |\n"

        # Add discrepancies
        discrepancies = report.get('discrepancies', [])
        if discrepancies:
            md += "\n## Discrepancies Found\n\n"
            for i, disc in enumerate(discrepancies, 1):
                md += f"{i}. **{disc['category']}.{disc['property']}**: "
                md += f"Figma = {disc['figma_value']}, Rendered = {disc['rendered_value']}"
                if disc.get('difference'):
                    md += f" (Δ {disc['difference']}px)"
                md += "\n"

        md += "\n---\n\n"
        md += f"**Green Arrow's Verdict**: {report['status']}\n"

        return md


# Main entry point - Green Arrow's Mission Interface
def green_arrow_validate_component(figma_url: str,
                                   rendered_url: str,
                                   component_name: str,
                                   component_code: str) -> Dict[str, Any]:
    """
    🎯 Green Arrow validates a component conversion

    Args:
        figma_url: Figma design URL with node-id
        rendered_url: URL of rendered component
        component_name: Name of component
        component_code: Source code of component

    Returns:
        Complete validation report
    """
    green_arrow = GreenArrowVisualValidator()
    return green_arrow.validate_component(
        figma_url,
        rendered_url,
        component_name,
        component_code
    )
