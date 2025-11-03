#!/usr/bin/env python3
"""
Enhanced Figma to React Converter - Full Content Extraction
Extracts ALL text, inputs, layouts, and content from Figma designs
Similar to the Penpot converter but using Figma API
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
sys.path.insert(0, str(Path(__file__).parent))
from core.superman_figma_integration import SupermanFigmaIntegration


class EnhancedFigmaConverter:
    """Full-fidelity Figma to React converter with complete content extraction"""

    def __init__(self, figma_token: str):
        self.figma = SupermanFigmaIntegration(figma_token)
        self.processed_ids = set()

    def convert(self, figma_url: str, node_id: str) -> Dict:
        """Convert Figma node to React with full content"""

        print("\n" + "="*80)
        print("🎨 ENHANCED FIGMA TO REACT CONVERTER")
        print("="*80 + "\n")

        # Extract file key
        file_key = self.figma.extract_file_key(figma_url)
        print(f"📁 File: {file_key}")
        print(f"🎯 Node: {node_id}\n")

        # Fetch node data
        print("📥 Fetching Figma data...")
        node_data = self.figma.get_file_nodes(file_key, [node_id])

        if 'error' in node_data:
            print(f"❌ Error: {node_data['error']}")
            return node_data

        # Get the node
        nodes = node_data.get('nodes', {})
        if node_id not in nodes:
            print(f"❌ Node {node_id} not found!")
            return {}

        document = nodes[node_id]['document']
        print(f"✅ Loaded: {document.get('name', 'Unnamed')}\n")

        # Analyze structure
        self._analyze_node(document)

        # Generate React code
        component_code = self._generate_react_component(document)

        # Save
        self._save_files(document.get('name', 'Component'), component_code)

        return {
            'success': True,
            'component_code': component_code,
            'node_name': document.get('name')
        }

    def _analyze_node(self, node: Dict):
        """Analyze node structure"""

        print("🔍 ANALYZING STRUCTURE")
        print("="*80 + "\n")

        # Count elements
        stats = {
            'text': 0,
            'input': 0,
            'button': 0,
            'frame': 0,
            'total': 0
        }

        def count(n):
            stats['total'] += 1
            node_type = n.get('type', '')
            name = n.get('name', '').lower()

            if node_type == 'TEXT':
                stats['text'] += 1
            elif 'input' in name or 'textfield' in name:
                stats['input'] += 1
            elif 'button' in name or 'btn' in name:
                stats['button'] += 1
            elif node_type == 'FRAME':
                stats['frame'] += 1

            for child in n.get('children', []):
                count(child)

        count(node)

        print(f"📊 Structure:")
        print(f"   • Total elements: {stats['total']}")
        print(f"   • Text elements: {stats['text']}")
        print(f"   • Input fields: {stats['input']}")
        print(f"   • Buttons: {stats['button']}")
        print(f"   • Frames: {stats['frame']}\n")

    def _generate_react_component(self, node: Dict) -> str:
        """Generate React component with full content"""

        print("💻 GENERATING REACT CODE")
        print("="*80 + "\n")

        component_name = self._sanitize_name(node.get('name', 'Component'))

        # Generate JSX
        jsx_body = self._generate_jsx(node, indent=3)

        # Build component
        component = f'''import React from 'react';

export interface {component_name}Props {{
  className?: string;
}}

export default function {component_name}({{ className }}: {component_name}Props) {{
  return (
    <div className={{`w-full min-h-screen bg-gray-50 ${{className || ''}}`}}>
      <div style={{{{position: 'relative', width: '{node.get("absoluteBoundingBox", {}).get("width", 1280)}px', margin: '0 auto'}}}}>
{jsx_body}
      </div>
    </div>
  );
}}
'''

        print(f"✅ Generated {component_name}.tsx\n")
        return component

    def _generate_jsx(self, node: Dict, indent: int = 0) -> str:
        """Recursively generate JSX with full content extraction"""

        indent_str = '  ' * indent
        node_type = node.get('type', '')
        name = node.get('name', '').lower()
        children = node.get('children', [])

        # Get position
        bbox = node.get('absoluteBoundingBox', {})
        parent_bbox = node.get('parent', {}).get('absoluteBoundingBox', {})

        x = bbox.get('x', 0) - parent_bbox.get('x', 0)
        y = bbox.get('y', 0) - parent_bbox.get('y', 0)
        width = bbox.get('width', 0)
        height = bbox.get('height', 0)

        # TEXT elements
        if node_type == 'TEXT':
            text = node.get('characters', '')
            if not text:
                return ''

            # Get text style
            style = node.get('style', {})
            font_size = style.get('fontSize', 14)
            font_weight = style.get('fontWeight', 400)

            # Get color
            fills = node.get('fills', [])
            color = '#000000'
            if fills:
                fill = fills[0]
                if fill.get('type') == 'SOLID':
                    color_obj = fill.get('color', {})
                    r = int(color_obj.get('r', 0) * 255)
                    g = int(color_obj.get('g', 0) * 255)
                    b = int(color_obj.get('b', 0) * 255)
                    color = f'#{r:02x}{g:02x}{b:02x}'

            # Escape text
            text = text.replace('<', '&lt;').replace('>', '&gt;')

            return f'''{indent_str}<div style={{{{position: 'absolute', left: '{x}px', top: '{y}px', fontSize: '{font_size}px', fontWeight: '{font_weight}', color: '{color}'}}}}>
{indent_str}  {text}
{indent_str}</div>'''

        # INPUT fields (detect by name)
        if 'input' in name or 'textfield' in name or 'field' in name:
            # Try to find label
            label = ''
            placeholder = ''

            # Look for text children
            for child in children:
                if child.get('type') == 'TEXT':
                    text = child.get('characters', '')
                    if text:
                        if not label:
                            label = text
                        else:
                            placeholder = text

            # Get background
            bg_color = '#ffffff'
            fills = node.get('fills', [])
            if fills and fills[0].get('type') == 'SOLID':
                color_obj = fills[0].get('color', {})
                r = int(color_obj.get('r', 1) * 255)
                g = int(color_obj.get('g', 1) * 255)
                b = int(color_obj.get('b', 1) * 255)
                bg_color = f'#{r:02x}{g:02x}{b:02x}'

            # Get border radius
            radius = node.get('cornerRadius', 4)

            return f'''{indent_str}<div style={{{{position: 'absolute', left: '{x}px', top: '{y}px', width: '{width}px'}}}}>
{indent_str}  {f'<label style={{{{display: "block", marginBottom: "4px", fontSize: "14px"}}}}>{label}</label>' if label else ''}
{indent_str}  <input
{indent_str}    type="text"
{indent_str}    placeholder="{placeholder or label}"
{indent_str}    style={{{{
{indent_str}      width: '100%',
{indent_str}      padding: '8px 12px',
{indent_str}      backgroundColor: '{bg_color}',
{indent_str}      border: '1px solid #d1d5db',
{indent_str}      borderRadius: '{radius}px',
{indent_str}      fontSize: '14px'
{indent_str}    }}}}
{indent_str}  />
{indent_str}</div>'''

        # BUTTON elements
        if 'button' in name or 'btn' in name:
            # Get button text
            button_text = 'Button'
            for child in children:
                if child.get('type') == 'TEXT':
                    button_text = child.get('characters', button_text)
                    break

            # Get background
            bg_color = '#3b82f6'
            fills = node.get('fills', [])
            if fills and fills[0].get('type') == 'SOLID':
                color_obj = fills[0].get('color', {})
                r = int(color_obj.get('r', 0) * 255)
                g = int(color_obj.get('g', 0) * 255)
                b = int(color_obj.get('b', 0) * 255)
                bg_color = f'#{r:02x}{g:02x}{b:02x}'

            radius = node.get('cornerRadius', 4)

            return f'''{indent_str}<button style={{{{position: 'absolute', left: '{x}px', top: '{y}px', width: '{width}px', height: '{height}px', backgroundColor: '{bg_color}', color: 'white', border: 'none', borderRadius: '{radius}px', cursor: 'pointer'}}}}>
{indent_str}  {button_text}
{indent_str}</button>'''

        # CONTAINER elements (FRAME, GROUP, etc.)
        if node_type in ['FRAME', 'GROUP', 'COMPONENT', 'INSTANCE']:
            # Get background
            bg_color = 'transparent'
            fills = node.get('fills', [])
            if fills and fills[0].get('type') == 'SOLID':
                color_obj = fills[0].get('color', {})
                r = int(color_obj.get('r', 1) * 255)
                g = int(color_obj.get('g', 1) * 255)
                b = int(color_obj.get('b', 1) * 255)
                bg_color = f'#{r:02x}{g:02x}{b:02x}'

            radius = node.get('cornerRadius', 0)

            # Render children
            children_jsx = []
            for child in children:
                child['parent'] = {'absoluteBoundingBox': bbox}
                child_jsx = self._generate_jsx(child, indent + 1)
                if child_jsx:
                    children_jsx.append(child_jsx)

            children_str = '\n'.join(children_jsx)

            # Only render if has children or background
            if not children_jsx and bg_color == 'transparent':
                return ''

            return f'''{indent_str}<div style={{{{position: 'absolute', left: '{x}px', top: '{y}px', width: '{width}px', height: '{height}px', backgroundColor: '{bg_color}', borderRadius: '{radius}px'}}}}>
{children_str}
{indent_str}</div>'''

        return ''

    def _sanitize_name(self, name: str) -> str:
        """Convert to valid component name"""
        name = ''.join(c for c in name if c.isalnum() or c.isspace())
        words = name.split()
        return ''.join(word.capitalize() for word in words if word) or 'Component'

    def _save_files(self, name: str, code: str):
        """Save generated files"""

        print("💾 SAVING FILES")
        print("="*80 + "\n")

        component_name = self._sanitize_name(name)

        # Save component
        output_dir = Path('generated_components')
        output_dir.mkdir(exist_ok=True)

        component_path = output_dir / f'{component_name}.tsx'
        with open(component_path, 'w') as f:
            f.write(code)

        print(f"✅ Saved: {component_path}")

        # Copy to preview
        preview_path = Path('preview-app/src/components') / f'{component_name}.tsx'
        preview_path.parent.mkdir(parents=True, exist_ok=True)
        with open(preview_path, 'w') as f:
            f.write(code)

        print(f"✅ Copied to: {preview_path}\n")


def main():
    figma_url = "https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=2-948"
    node_id = "2:948"
    figma_token = "figd_aPXrH3Rqpm8sdez_nHmmXKHvZ9vcK3sOcJwvhE7s"

    converter = EnhancedFigmaConverter(figma_token)
    result = converter.convert(figma_url, node_id)

    if result.get('success'):
        print("🎉 CONVERSION COMPLETE!")
        print(f"🔗 View at: http://localhost:3005")

    return result


if __name__ == "__main__":
    main()
