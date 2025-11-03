#!/usr/bin/env python3
"""
🎨 Figma to HTML/CSS/JS Converter
Justice League Powered Conversion System

Converts Figma designs to pixel-perfect HTML/CSS/JS using:
- Oracle for pattern recognition
- Artemis for intelligent code generation
- Green Arrow for visual validation

Target: 95-99% pixel-perfect accuracy
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class FigmaToHTMLConverter:
    """Convert Figma design to pure HTML/CSS/JS with Tailwind"""

    def __init__(self, figma_data_path: str, output_dir: str):
        self.figma_data_path = Path(figma_data_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load Figma data
        with open(self.figma_data_path, 'r') as f:
            self.figma_data = json.load(f)

        # Design tokens (extracted from Figma)
        self.colors = {}
        self.typography = {}
        self.spacing = {}
        self.components = []

        # Assets to download
        self.assets_needed = []

    def analyze_design(self) -> Dict[str, Any]:
        """Analyze Figma design and extract all specifications"""
        print("🔍 Analyzing Figma design...")

        # Get the main node
        nodes = self.figma_data.get('nodes', {})
        if not nodes:
            raise ValueError("No nodes found in Figma data")

        # Get first (and only) node - our target component
        node_id = list(nodes.keys())[0]
        node_data = nodes[node_id]
        document = node_data.get('document', {})

        analysis = {
            'node_id': node_id,
            'name': document.get('name', 'Untitled'),
            'type': document.get('type', 'UNKNOWN'),
            'dimensions': self._extract_dimensions(document),
            'colors': self._extract_colors(document),
            'typography': self._extract_typography(document),
            'components': self._extract_components(document),
            'layout': self._extract_layout(document),
            'assets': self._extract_assets(document)
        }

        print(f"✅ Analysis complete:")
        print(f"   Component: {analysis['name']}")
        print(f"   Type: {analysis['type']}")
        print(f"   Size: {analysis['dimensions']['width']}x{analysis['dimensions']['height']}px")
        print(f"   Colors: {len(analysis['colors'])} unique colors")
        print(f"   Components: {len(analysis['components'])} child components")
        print(f"   Assets: {len(analysis['assets'])} images/icons")

        return analysis

    def _extract_dimensions(self, node: Dict) -> Dict[str, float]:
        """Extract component dimensions"""
        bbox = node.get('absoluteBoundingBox', {})
        return {
            'width': bbox.get('width', 0),
            'height': bbox.get('height', 0),
            'x': bbox.get('x', 0),
            'y': bbox.get('y', 0)
        }

    def _extract_colors(self, node: Dict, colors: Optional[set] = None) -> List[str]:
        """Recursively extract all colors from design"""
        if colors is None:
            colors = set()

        # Extract fills
        fills = node.get('fills', [])
        for fill in fills:
            if fill.get('type') == 'SOLID':
                color_obj = fill.get('color', {})
                hex_color = self._rgb_to_hex(color_obj)
                colors.add(hex_color)

        # Extract strokes
        strokes = node.get('strokes', [])
        for stroke in strokes:
            if stroke.get('type') == 'SOLID':
                color_obj = stroke.get('color', {})
                hex_color = self._rgb_to_hex(color_obj)
                colors.add(hex_color)

        # Recurse through children
        children = node.get('children', [])
        for child in children:
            self._extract_colors(child, colors)

        return sorted(list(colors))

    def _rgb_to_hex(self, color: Dict) -> str:
        """Convert Figma RGB to hex"""
        r = int(color.get('r', 0) * 255)
        g = int(color.get('g', 0) * 255)
        b = int(color.get('b', 0) * 255)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _extract_typography(self, node: Dict, fonts: Optional[Dict] = None) -> Dict[str, Any]:
        """Extract typography specs"""
        if fonts is None:
            fonts = {}

        if node.get('type') == 'TEXT':
            style = node.get('style', {})
            font_key = f"{style.get('fontFamily', 'Unknown')}-{style.get('fontWeight', 400)}-{style.get('fontSize', 12)}"

            if font_key not in fonts:
                fonts[font_key] = {
                    'fontFamily': style.get('fontFamily', 'sans-serif'),
                    'fontWeight': style.get('fontWeight', 400),
                    'fontSize': style.get('fontSize', 12),
                    'lineHeight': style.get('lineHeightPx', style.get('fontSize', 12) * 1.5),
                    'letterSpacing': style.get('letterSpacing', 0),
                    'textAlign': style.get('textAlignHorizontal', 'LEFT'),
                    'color': self._rgb_to_hex(node.get('fills', [{}])[0].get('color', {})) if node.get('fills') else '#000000'
                }

        # Recurse
        for child in node.get('children', []):
            self._extract_typography(child, fonts)

        return fonts

    def _extract_components(self, node: Dict, components: Optional[List] = None, level: int = 0) -> List[Dict]:
        """Extract all UI components with hierarchy"""
        if components is None:
            components = []

        component = {
            'id': node.get('id'),
            'name': node.get('name'),
            'type': node.get('type'),
            'level': level,
            'dimensions': self._extract_dimensions(node),
            'styles': self._extract_styles(node),
            'content': node.get('characters', '') if node.get('type') == 'TEXT' else '',
            'children': []
        }

        components.append(component)

        # Recurse through children
        for child in node.get('children', []):
            self._extract_components(child, components, level + 1)

        return components

    def _extract_styles(self, node: Dict) -> Dict[str, Any]:
        """Extract styling information from node"""
        styles = {
            'backgroundColor': None,
            'borderRadius': node.get('cornerRadius', 0),
            'padding': self._extract_padding(node),
            'opacity': node.get('opacity', 1.0),
            'layoutMode': node.get('layoutMode', None),
            'itemSpacing': node.get('itemSpacing', 0)
        }

        # Background color
        fills = node.get('fills', [])
        for fill in fills:
            if fill.get('type') == 'SOLID' and fill.get('visible', True):
                styles['backgroundColor'] = self._rgb_to_hex(fill.get('color', {}))
                break

        return styles

    def _extract_padding(self, node: Dict) -> Dict[str, float]:
        """Extract padding values"""
        return {
            'top': node.get('paddingTop', 0),
            'right': node.get('paddingRight', 0),
            'bottom': node.get('paddingBottom', 0),
            'left': node.get('paddingLeft', 0)
        }

    def _extract_layout(self, node: Dict) -> Dict[str, Any]:
        """Analyze layout structure"""
        layout_mode = node.get('layoutMode', None)

        return {
            'mode': layout_mode,  # HORIZONTAL, VERTICAL, or None
            'primaryAxisAlignment': node.get('primaryAxisAlignItems', 'MIN'),
            'counterAxisAlignment': node.get('counterAxisAlignItems', 'MIN'),
            'itemSpacing': node.get('itemSpacing', 0),
            'padding': self._extract_padding(node)
        }

    def _extract_assets(self, node: Dict, assets: Optional[List] = None) -> List[Dict]:
        """Find all images and assets that need to be downloaded"""
        if assets is None:
            assets = []

        # Check for images
        fills = node.get('fills', [])
        for fill in fills:
            if fill.get('type') == 'IMAGE':
                assets.append({
                    'nodeId': node.get('id'),
                    'nodeName': node.get('name'),
                    'imageRef': fill.get('imageRef'),
                    'type': 'IMAGE'
                })

        # Recurse
        for child in node.get('children', []):
            self._extract_assets(child, assets)

        return assets

    def generate_html(self, analysis: Dict[str, Any]) -> str:
        """Generate HTML structure from analysis"""
        print("\n🎨 Generating HTML...")

        # Get root node for recursive generation
        nodes = self.figma_data.get('nodes', {})
        node_id = list(nodes.keys())[0]
        document = nodes[node_id].get('document', {})

        html_body = self._generate_html_recursive(document, level=0)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{analysis['name']}</title>

    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Custom Tailwind Configuration -->
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {self._generate_color_config(analysis['colors'])},
                    fontFamily: {{
                        'manrope': ['Manrope', 'sans-serif']
                    }}
                }}
            }}
        }}
    </script>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">

    <!-- Custom Styles -->
    <link rel="stylesheet" href="styles.css">
</head>
<body class="bg-gray-50 font-manrope antialiased">

{html_body}

    <!-- JavaScript -->
    <script src="script.js"></script>
</body>
</html>"""

        print("✅ HTML generated successfully")
        return html

    def _generate_html_recursive(self, node: Dict, level: int = 0) -> str:
        """Recursively generate HTML from Figma nodes"""
        node_type = node.get('type')
        node_name = node.get('name', '')
        indent = "    " * (level + 1)

        # Handle different node types
        if node_type == 'TEXT':
            return self._generate_text_html(node, indent)
        elif node_type in ['FRAME', 'GROUP']:
            return self._generate_container_html(node, indent, level)
        elif node_type == 'RECTANGLE':
            return self._generate_rectangle_html(node, indent)
        elif node_type == 'ELLIPSE':
            return self._generate_ellipse_html(node, indent)
        elif node_type == 'LINE':
            return self._generate_line_html(node, indent)
        elif node_type == 'INSTANCE':
            return self._generate_instance_html(node, indent, level)
        else:
            # Generic container
            children_html = ""
            for child in node.get('children', []):
                children_html += self._generate_html_recursive(child, level + 1)

            return f'{indent}<div class="figma-{node_type.lower()}">\n{children_html}{indent}</div>\n'

    def _generate_text_html(self, node: Dict, indent: str) -> str:
        """Generate HTML for text nodes"""
        text = node.get('characters', '')
        style = node.get('style', {})

        # Determine text element type
        font_size = style.get('fontSize', 12)
        font_weight = style.get('fontWeight', 400)

        if font_size >= 20 and font_weight >= 700:
            tag = 'h2'
        elif font_size >= 16 and font_weight >= 700:
            tag = 'h3'
        elif font_size >= 14 and font_weight >= 600:
            tag = 'h4'
        else:
            tag = 'p'

        classes = self._generate_text_classes(style)

        return f'{indent}<{tag} class="{classes}">{text}</{tag}>\n'

    def _generate_text_classes(self, style: Dict) -> str:
        """Generate Tailwind classes for text"""
        classes = []

        # Font size
        font_size = style.get('fontSize', 12)
        if font_size <= 12:
            classes.append('text-xs')
        elif font_size <= 14:
            classes.append('text-sm')
        elif font_size <= 16:
            classes.append('text-base')
        elif font_size <= 20:
            classes.append('text-lg')
        elif font_size <= 24:
            classes.append('text-xl')
        else:
            classes.append('text-2xl')

        # Font weight
        font_weight = style.get('fontWeight', 400)
        if font_weight >= 700:
            classes.append('font-bold')
        elif font_weight >= 600:
            classes.append('font-semibold')
        elif font_weight >= 500:
            classes.append('font-medium')
        else:
            classes.append('font-normal')

        # Text align
        text_align = style.get('textAlignHorizontal', 'LEFT')
        if text_align == 'CENTER':
            classes.append('text-center')
        elif text_align == 'RIGHT':
            classes.append('text-right')

        return ' '.join(classes)

    def _generate_container_html(self, node: Dict, indent: str, level: int) -> str:
        """Generate HTML for container nodes (FRAME/GROUP)"""
        classes = self._generate_container_classes(node)
        node_name = node.get('name', '').lower().replace(' ', '-')

        children_html = ""
        for child in node.get('children', []):
            children_html += self._generate_html_recursive(child, level + 1)

        # Use semantic HTML when possible
        if 'header' in node_name or 'nav' in node_name:
            tag = 'header'
        elif 'footer' in node_name:
            tag = 'footer'
        elif 'sidebar' in node_name or 'aside' in node_name:
            tag = 'aside'
        else:
            tag = 'div'

        return f'{indent}<{tag} class="{classes}" data-name="{node.get("name", "")}">\n{children_html}{indent}</{tag}>\n'

    def _generate_container_classes(self, node: Dict) -> str:
        """Generate Tailwind classes for containers"""
        classes = []

        # Layout mode
        layout_mode = node.get('layoutMode')
        if layout_mode == 'HORIZONTAL':
            classes.append('flex flex-row')
        elif layout_mode == 'VERTICAL':
            classes.append('flex flex-col')

        # Alignment
        if layout_mode:
            primary_align = node.get('primaryAxisAlignItems', 'MIN')
            counter_align = node.get('counterAxisAlignItems', 'MIN')

            # Justify content (main axis)
            if primary_align == 'CENTER':
                classes.append('justify-center')
            elif primary_align == 'MAX':
                classes.append('justify-end')
            elif primary_align == 'SPACE_BETWEEN':
                classes.append('justify-between')

            # Align items (cross axis)
            if counter_align == 'CENTER':
                classes.append('items-center')
            elif counter_align == 'MAX':
                classes.append('items-end')

        # Gap/spacing
        item_spacing = node.get('itemSpacing', 0)
        if item_spacing > 0:
            gap_class = self._px_to_tailwind_spacing(item_spacing)
            classes.append(f'gap-{gap_class}')

        # Padding
        padding = self._extract_padding(node)
        if any(padding.values()):
            if all(v == padding['top'] for v in padding.values()):
                # Uniform padding
                classes.append(f'p-{self._px_to_tailwind_spacing(padding["top"])}')
            else:
                # Individual padding
                if padding['top'] > 0:
                    classes.append(f'pt-{self._px_to_tailwind_spacing(padding["top"])}')
                if padding['right'] > 0:
                    classes.append(f'pr-{self._px_to_tailwind_spacing(padding["right"])}')
                if padding['bottom'] > 0:
                    classes.append(f'pb-{self._px_to_tailwind_spacing(padding["bottom"])}')
                if padding['left'] > 0:
                    classes.append(f'pl-{self._px_to_tailwind_spacing(padding["left"])}')

        # Background
        fills = node.get('fills', [])
        for fill in fills:
            if fill.get('type') == 'SOLID' and fill.get('visible', True):
                hex_color = self._rgb_to_hex(fill.get('color', {}))
                if hex_color == '#ffffff':
                    classes.append('bg-white')
                elif hex_color == '#000000':
                    classes.append('bg-black')
                else:
                    # Use custom color
                    classes.append(f'bg-[{hex_color}]')

        # Border radius
        corner_radius = node.get('cornerRadius', 0)
        if corner_radius > 0:
            if corner_radius <= 4:
                classes.append('rounded')
            elif corner_radius <= 6:
                classes.append('rounded-md')
            elif corner_radius <= 8:
                classes.append('rounded-lg')
            else:
                classes.append('rounded-xl')

        # Width constraint
        sizing_horizontal = node.get('layoutSizingHorizontal', '')
        if sizing_horizontal == 'FIXED':
            bbox = node.get('absoluteBoundingBox', {})
            width = bbox.get('width', 0)
            if width > 0:
                classes.append(f'w-[{width}px]')

        return ' '.join(classes) if classes else 'block'

    def _generate_rectangle_html(self, node: Dict, indent: str) -> str:
        """Generate HTML for rectangle nodes"""
        classes = []

        # Check if it's an image
        fills = node.get('fills', [])
        for fill in fills:
            if fill.get('type') == 'IMAGE':
                image_ref = fill.get('imageRef')
                return f'{indent}<img src="assets/images/{image_ref}.png" alt="{node.get("name", "")}" class="object-cover rounded">\n'

        # Otherwise, it's a decorative rectangle
        classes = self._generate_container_classes(node)
        bbox = node.get('absoluteBoundingBox', {})

        return f'{indent}<div class="{classes}" style="width: {bbox.get("width", 0)}px; height: {bbox.get("height", 0)}px;"></div>\n'

    def _generate_ellipse_html(self, node: Dict, indent: str) -> str:
        """Generate HTML for ellipse/circle nodes"""
        bbox = node.get('absoluteBoundingBox', {})
        width = bbox.get('width', 0)
        height = bbox.get('height', 0)

        fills = node.get('fills', [])
        bg_color = '#cccccc'
        for fill in fills:
            if fill.get('type') == 'SOLID':
                bg_color = self._rgb_to_hex(fill.get('color', {}))
                break

        return f'{indent}<div class="rounded-full bg-[{bg_color}]" style="width: {width}px; height: {height}px;"></div>\n'

    def _generate_line_html(self, node: Dict, indent: str) -> str:
        """Generate HTML for line/divider nodes"""
        strokes = node.get('strokes', [])
        color = '#e5e5e5'
        for stroke in strokes:
            if stroke.get('type') == 'SOLID':
                color = self._rgb_to_hex(stroke.get('color', {}))
                break

        return f'{indent}<hr class="border-t border-[{color}]">\n'

    def _generate_instance_html(self, node: Dict, indent: str, level: int) -> str:
        """Generate HTML for component instances"""
        # Treat as container and recurse
        return self._generate_container_html(node, indent, level)

    def _px_to_tailwind_spacing(self, px: float) -> str:
        """Convert px value to Tailwind spacing class"""
        spacing_map = {
            0: '0', 4: '1', 6: '1.5', 8: '2', 10: '2.5', 12: '3',
            14: '3.5', 16: '4', 18: '4.5', 20: '5', 24: '6',
            32: '8', 40: '10', 48: '12', 56: '14', 64: '16'
        }

        # Find closest match
        closest = min(spacing_map.keys(), key=lambda x: abs(x - px))
        return spacing_map[closest]

    def _generate_color_config(self, colors: List[str]) -> str:
        """Generate Tailwind color configuration"""
        # Map common colors
        color_names = {}
        for i, color in enumerate(colors):
            if color == '#ffffff':
                continue  # Skip white, it's default
            elif color == '#000000':
                continue  # Skip black, it's default
            elif color.startswith('#ff'):
                color_names[f'accent-{i}'] = color
            else:
                color_names[f'custom-{i}'] = color

        return json.dumps(color_names, indent=24)

    def generate_css(self, analysis: Dict[str, Any]) -> str:
        """Generate additional custom CSS"""
        print("\n🎨 Generating CSS...")

        css = """/* Custom Styles for Figma Component */

/* Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Body */
body {
    font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* Custom utilities */
.shadow-card {
    box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
}

/* Hover states */
.hover-lift:hover {
    transform: translateY(-2px);
    transition: transform 0.2s ease;
}

/* Animation */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-fade-in {
    animation: fadeIn 0.3s ease-out;
}
"""

        print("✅ CSS generated")
        return css

    def generate_js(self, analysis: Dict[str, Any]) -> str:
        """Generate JavaScript for interactivity"""
        print("\n🎨 Generating JavaScript...")

        js = """// Dashboard 10 - Interactive Features

document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard 10 loaded');

    // Add hover effects
    const cards = document.querySelectorAll('[data-name*="Frame"]');
    cards.forEach(card => {
        card.classList.add('hover-lift');
    });

    // Handle "View all" clicks
    const viewAllLinks = document.querySelectorAll('[data-name*="View all"]');
    viewAllLinks.forEach(link => {
        link.style.cursor = 'pointer';
        link.addEventListener('click', function(e) {
            console.log('View all clicked:', this.textContent);
            // Add your navigation logic here
        });
    });

    // Add fade-in animation
    const animatedElements = document.querySelectorAll('[data-name*="Frame"]');
    animatedElements.forEach((el, index) => {
        el.style.opacity = '0';
        setTimeout(() => {
            el.classList.add('animate-fade-in');
            el.style.opacity = '1';
        }, index * 50);
    });

    // Notification dot pulse
    const notificationDots = document.querySelectorAll('[data-name*="Ellipse 1949"]');
    notificationDots.forEach(dot => {
        dot.style.animation = 'pulse 2s infinite';
    });
});

// Add CSS for pulse animation
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
`;
document.head.appendChild(style);
"""

        print("✅ JavaScript generated")
        return js

    def save_files(self, html: str, css: str, js: str):
        """Save generated files to output directory"""
        print("\n💾 Saving files...")

        # Save HTML
        html_file = self.output_dir / 'index.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"   ✅ Saved: {html_file}")

        # Save CSS
        css_file = self.output_dir / 'styles.css'
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css)
        print(f"   ✅ Saved: {css_file}")

        # Save JS
        js_file = self.output_dir / 'script.js'
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(js)
        print(f"   ✅ Saved: {js_file}")

        print("\n✅ All files saved successfully!")

    def convert(self):
        """Main conversion process"""
        print("=" * 80)
        print("🎨 FIGMA TO HTML/CSS/JS CONVERTER")
        print("=" * 80)
        print(f"Input: {self.figma_data_path}")
        print(f"Output: {self.output_dir}")
        print()

        # Step 1: Analyze design
        analysis = self.analyze_design()

        # Step 2: Generate HTML
        html = self.generate_html(analysis)

        # Step 3: Generate CSS
        css = self.generate_css(analysis)

        # Step 4: Generate JavaScript
        js = self.generate_js(analysis)

        # Step 5: Save files
        self.save_files(html, css, js)

        # Step 6: Summary
        print("\n" + "=" * 80)
        print("✅ CONVERSION COMPLETE!")
        print("=" * 80)
        print(f"\n📁 Generated files:")
        print(f"   - index.html ({len(html)} bytes)")
        print(f"   - styles.css ({len(css)} bytes)")
        print(f"   - script.js ({len(js)} bytes)")
        print(f"\n🚀 Next steps:")
        print(f"   1. Open {self.output_dir}/index.html in browser")
        print(f"   2. Download assets from Figma (images)")
        print(f"   3. Run visual validation with Green Arrow")
        print(f"   4. Iterate and refine for pixel-perfection")
        print("=" * 80)

        return {
            'success': True,
            'output_dir': str(self.output_dir),
            'files': ['index.html', 'styles.css', 'script.js'],
            'analysis': analysis
        }


def main():
    # Configuration
    figma_data_path = "figma_dashboard10_raw.json"
    output_dir = "html"

    # Convert
    converter = FigmaToHTMLConverter(figma_data_path, output_dir)
    result = converter.convert()

    return result


if __name__ == "__main__":
    import sys
    try:
        result = main()
        sys.exit(0 if result['success'] else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
