#!/usr/bin/env python3
"""
Penpot to React Converter
Converts Penpot design data to pixel-perfect React/TypeScript components
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

class PenpotToReactConverter:
    def __init__(self, page_data: Dict[str, Any]):
        self.page_data = page_data
        self.objects = page_data.get('objects', {})
        self.component_name = "Dashboard"

    def hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def get_fill_style(self, fills: List[Dict]) -> Dict[str, str]:
        """Extract CSS styles from Penpot fills"""
        styles = {}

        if not fills:
            return styles

        # Get the last fill (top layer)
        fill = fills[-1]

        if 'fillColor' in fill:
            color = fill['fillColor']
            opacity = fill.get('fillOpacity', 1)

            if opacity < 1:
                # Convert to RGBA
                r, g, b = self.hex_to_rgb(color)
                styles['backgroundColor'] = f'rgba({r}, {g}, {b}, {opacity})'
            else:
                styles['backgroundColor'] = color

        if 'fillImage' in fill:
            # Handle image fills
            styles['backgroundImage'] = 'url(...)' # Placeholder
            styles['backgroundSize'] = 'cover'

        return styles

    def get_stroke_style(self, strokes: List[Dict]) -> Dict[str, str]:
        """Extract border styles from Penpot strokes"""
        styles = {}

        if not strokes:
            return styles

        stroke = strokes[0]

        if 'strokeColor' in stroke:
            color = stroke['strokeColor']
            width = stroke.get('strokeWidth', 1)
            opacity = stroke.get('strokeOpacity', 1)

            styles['borderWidth'] = f'{width}px'
            styles['borderStyle'] = 'solid'

            if opacity < 1:
                r, g, b = self.hex_to_rgb(color)
                styles['borderColor'] = f'rgba({r}, {g}, {b}, {opacity})'
            else:
                styles['borderColor'] = color

        return styles

    def get_border_radius(self, obj: Dict) -> Optional[str]:
        """Get border radius from object"""
        # Check for individual corner radii
        if 'r1' in obj and 'r2' in obj and 'r3' in obj and 'r4' in obj:
            r1, r2, r3, r4 = obj['r1'], obj['r2'], obj['r3'], obj['r4']
            if r1 == r2 == r3 == r4:
                return f'{r1}px' if r1 else None
            else:
                return f'{r1}px {r2}px {r3}px {r4}px'
        elif 'rx' in obj or 'ry' in obj:
            return f"{obj.get('rx', 0)}px"
        return None

    def get_layout_classes(self, obj: Dict) -> List[str]:
        """Convert Penpot layout properties to Tailwind classes"""
        classes = []

        layout = obj.get('layout')
        if layout == 'flex':
            classes.append('flex')

            # Flex direction
            flex_dir = obj.get('layoutFlexDir', 'row')
            if flex_dir == 'column':
                classes.append('flex-col')
            elif flex_dir == 'row':
                classes.append('flex-row')

            # Justify content
            justify = obj.get('layoutJustifyContent', '')
            justify_map = {
                'start': 'justify-start',
                'end': 'justify-end',
                'center': 'justify-center',
                'space-between': 'justify-between',
                'space-around': 'justify-around',
                'space-evenly': 'justify-evenly'
            }
            if justify in justify_map:
                classes.append(justify_map[justify])

            # Align items
            align = obj.get('layoutAlignItems', '')
            align_map = {
                'start': 'items-start',
                'end': 'items-end',
                'center': 'items-center',
                'stretch': 'items-stretch'
            }
            if align in align_map:
                classes.append(align_map[align])

            # Gap
            gap = obj.get('layoutGap', {})
            if isinstance(gap, dict):
                row_gap = gap.get('rowGap', 0)
                col_gap = gap.get('columnGap', 0)
                if row_gap and row_gap == col_gap:
                    classes.append(f'gap-[{row_gap}px]')
                elif row_gap or col_gap:
                    if row_gap:
                        classes.append(f'gap-y-[{row_gap}px]')
                    if col_gap:
                        classes.append(f'gap-x-[{col_gap}px]')
            elif gap:
                classes.append(f'gap-[{gap}px]')

        return classes

    def get_position_styles(self, obj: Dict) -> Dict[str, str]:
        """Get positioning styles"""
        styles = {}

        x = obj.get('x', 0)
        y = obj.get('y', 0)
        width = obj.get('width')
        height = obj.get('height')

        if width is not None:
            styles['width'] = f'{width}px'
        if height is not None:
            styles['height'] = f'{height}px'

        return styles

    def get_text_styles(self, obj: Dict) -> Dict[str, str]:
        """Extract text styling"""
        styles = {}

        if 'fontSize' in obj:
            styles['fontSize'] = f"{obj['fontSize']}px"
        if 'fontFamily' in obj:
            styles['fontFamily'] = obj['fontFamily']
        if 'fontWeight' in obj:
            styles['fontWeight'] = str(obj['fontWeight'])
        if 'lineHeight' in obj:
            styles['lineHeight'] = str(obj['lineHeight'])
        if 'letterSpacing' in obj:
            styles['letterSpacing'] = f"{obj['letterSpacing']}px"
        if 'textAlign' in obj:
            styles['textAlign'] = obj['textAlign']

        return styles

    def extract_text_content(self, obj: Dict) -> str:
        """Extract text content from Penpot text object"""
        content = obj.get('content', {})

        if not content:
            return ""

        children = content.get('children', [])
        text_parts = []

        for child in children:
            if isinstance(child, dict):
                text = child.get('text', '')
                text_parts.append(text)
            elif isinstance(child, str):
                text_parts.append(child)

        return ''.join(text_parts)

    def generate_jsx_element(self, obj: Dict, indent: int = 2) -> str:
        """Generate JSX for a single object"""
        indent_str = ' ' * indent
        obj_type = obj.get('type', 'frame')
        obj_name = obj.get('name', 'Element')

        # Get children
        children_ids = obj.get('shapes', [])
        children_jsx = []

        for child_id in children_ids:
            if child_id in self.objects:
                child_obj = self.objects[child_id]
                children_jsx.append(self.generate_jsx_element(child_obj, indent + 2))

        # Build element based on type
        if obj_type == 'text':
            text_content = self.extract_text_content(obj)

            # Get styles
            all_styles = {}
            all_styles.update(self.get_position_styles(obj))
            all_styles.update(self.get_fill_style(obj.get('fills', [])))
            all_styles.update(self.get_text_styles(obj))

            if obj.get('opacity', 1) < 1:
                all_styles['opacity'] = str(obj['opacity'])

            # Build style string
            style_str = '{' + ', '.join([f"{k}: '{v}'" for k, v in all_styles.items()]) + '}'

            return f'{indent_str}<div style={{{style_str}}}>{text_content}</div>'

        elif obj_type in ['frame', 'group']:
            # Get layout classes
            classes = self.get_layout_classes(obj)

            # Get styles
            all_styles = {}
            all_styles.update(self.get_position_styles(obj))
            all_styles.update(self.get_fill_style(obj.get('fills', [])))
            all_styles.update(self.get_stroke_style(obj.get('strokes', [])))

            border_radius = self.get_border_radius(obj)
            if border_radius:
                all_styles['borderRadius'] = border_radius

            if obj.get('opacity', 1) < 1:
                all_styles['opacity'] = str(obj['opacity'])

            # Padding
            padding = obj.get('layoutPadding', {})
            if padding:
                if isinstance(padding, dict):
                    p1 = padding.get('p1', 0)
                    p2 = padding.get('p2', 0)
                    p3 = padding.get('p3', 0)
                    p4 = padding.get('p4', 0)
                    all_styles['padding'] = f'{p1}px {p2}px {p3}px {p4}px'

            # Build className
            class_str = ' '.join(classes) if classes else ''

            # Build style string
            style_str = '{' + ', '.join([f"{k}: '{v}'" for k, v in all_styles.items()]) + '}' if all_styles else ''

            # Build element
            if children_jsx:
                children_str = '\n'.join(children_jsx)
                if style_str:
                    return f'{indent_str}<div className="{class_str}" style={{{style_str}}}>\n{children_str}\n{indent_str}</div>'
                else:
                    return f'{indent_str}<div className="{class_str}">\n{children_str}\n{indent_str}</div>'
            else:
                if style_str:
                    return f'{indent_str}<div className="{class_str}" style={{{style_str}}} />'
                else:
                    return f'{indent_str}<div className="{class_str}" />'

        elif obj_type == 'rect':
            # Rectangle - render as div
            all_styles = {}
            all_styles.update(self.get_position_styles(obj))
            all_styles.update(self.get_fill_style(obj.get('fills', [])))
            all_styles.update(self.get_stroke_style(obj.get('strokes', [])))

            border_radius = self.get_border_radius(obj)
            if border_radius:
                all_styles['borderRadius'] = border_radius

            if obj.get('opacity', 1) < 1:
                all_styles['opacity'] = str(obj['opacity'])

            style_str = '{' + ', '.join([f"{k}: '{v}'" for k, v in all_styles.items()]) + '}'

            if children_jsx:
                children_str = '\n'.join(children_jsx)
                return f'{indent_str}<div style={{{style_str}}}>\n{children_str}\n{indent_str}</div>'
            else:
                return f'{indent_str}<div style={{{style_str}}} />'

        elif obj_type in ['path', 'circle']:
            # SVG elements - render as placeholder for now
            all_styles = {}
            all_styles.update(self.get_position_styles(obj))

            if obj.get('opacity', 1) < 1:
                all_styles['opacity'] = str(obj['opacity'])

            style_str = '{' + ', '.join([f"{k}: '{v}'" for k, v in all_styles.items()]) + '}'

            return f'{indent_str}<div style={{{style_str}}} className="svg-placeholder" />'

        # Default
        return f'{indent_str}<div><!-- {obj_type}: {obj_name} --></div>'

    def generate_component(self) -> str:
        """Generate complete React component"""

        # Find root frame or main content
        root_frames = []
        for obj_id, obj in self.objects.items():
            if obj.get('type') == 'frame':
                parent_id = obj.get('parentId')
                if not parent_id or parent_id == '00000000-0000-0000-0000-000000000000':
                    if obj.get('name') != 'Root Frame':
                        root_frames.append((obj_id, obj))

        # Generate JSX for root frames
        jsx_elements = []
        for frame_id, frame_obj in root_frames[:10]:  # Limit to first 10 root frames
            jsx_elements.append(self.generate_jsx_element(frame_obj, indent=6))

        jsx_body = '\n'.join(jsx_elements)

        # Build component
        component = f'''import React from 'react';

export interface {self.component_name}Props {{
  className?: string;
}}

export function {self.component_name}({{ className }}: {self.component_name}Props) {{
  return (
    <div className={{`w-full h-full ${{className || ''}}`}}>
{jsx_body}
    </div>
  );
}}

export default {self.component_name};
'''

        return component


def main():
    print("🎨 PENPOT TO REACT CONVERTER")
    print("=" * 80)

    # Load Penpot page data
    print("\n📥 Loading Penpot page data...")
    with open('penpot_page_data.json', 'r') as f:
        page_data = json.load(f)

    print(f"✅ Loaded {len(page_data.get('objects', {}))} objects")

    # Create converter
    print("\n🔄 Converting to React...")
    converter = PenpotToReactConverter(page_data)

    # Generate component
    component_code = converter.generate_component()

    # Save component
    output_path = Path("generated_components/PenpotDashboard.tsx")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(component_code)

    print(f"✅ Generated React component!")
    print(f"📂 Saved to: {output_path}")
    print(f"📊 Component size: {len(component_code)} characters")

    # Show preview
    print("\n" + "=" * 80)
    print("📄 COMPONENT PREVIEW (first 50 lines)")
    print("=" * 80)
    lines = component_code.split('\n')
    print('\n'.join(lines[:50]))
    if len(lines) > 50:
        print(f"\n... and {len(lines) - 50} more lines")

    print("\n✅ CONVERSION COMPLETE!")
    print("\n🚀 Next steps:")
    print("   1. Set up Next.js preview environment")
    print("   2. Render the component")
    print("   3. Take screenshot for comparison")


if __name__ == "__main__":
    main()
