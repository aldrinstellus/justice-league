#!/usr/bin/env python3
"""
🎨 ARTEMIS CODESMITH - FIGMA TO CODE CONVERTER
==============================================

Converts specific Figma frames/components to production-ready React/TypeScript code.

Author: Artemis CodeSmith + Justice League
Date: October 23, 2025
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from core.superman_figma_integration import SupermanFigmaIntegration


class ArtemisCodeGenerator:
    """Generate production-ready code from Figma designs."""

    def __init__(self, figma_token: str):
        self.figma_token = figma_token
        self.superman = SupermanFigmaIntegration(figma_token)

    def convert_to_code(self, figma_url: str, node_id: str) -> Dict[str, Any]:
        """Convert Figma node to React/TypeScript code."""

        print("\n" + "="*80)
        print("🎨 ARTEMIS CODESMITH - FIGMA TO CODE CONVERSION")
        print("="*80 + "\n")

        file_key = self.superman.extract_file_key(figma_url)
        print(f"🔑 File Key: {file_key}")
        print(f"🎯 Node ID: {node_id}\n")

        # Get node data
        print("📥 Fetching Figma node data...")
        node_data = self.superman.get_file_nodes(file_key, [node_id])

        if 'error' in node_data:
            print(f"❌ ERROR: {node_data['error']}")
            return node_data

        print("✅ Node data loaded!\n")

        # Analyze the node
        analysis = self._analyze_node(node_data, node_id)

        # Generate code
        code_result = self._generate_code(analysis)

        # Save files
        self._save_generated_files(code_result)

        return code_result

    def _analyze_node(self, node_data: Dict, node_id: str) -> Dict[str, Any]:
        """Analyze Figma node structure."""

        print("\n" + "="*80)
        print("🔍 ANALYZING FIGMA NODE")
        print("="*80 + "\n")

        nodes = node_data.get('nodes', {})
        if not nodes or node_id not in nodes:
            print(f"❌ Node {node_id} not found!")
            return {}

        node = nodes[node_id]['document']
        name = node.get('name', 'Unnamed')
        node_type = node.get('type', 'UNKNOWN')

        print(f"📝 Component Name: {name}")
        print(f"📦 Node Type: {node_type}")

        # Get dimensions
        bbox = node.get('absoluteBoundingBox', {})
        width = bbox.get('width', 0)
        height = bbox.get('height', 0)

        print(f"📏 Dimensions: {width:.0f}×{height:.0f}px")

        # Analyze children
        children = node.get('children', [])
        print(f"🧩 Child Elements: {len(children)}")

        # Detect component types
        detected_components = self._detect_components(node)
        print(f"\n🎯 Detected shadcn/ui Components:")
        for comp_type, count in detected_components.items():
            print(f"  • {comp_type}: {count}")

        # Analyze layout
        layout = self._analyze_layout(node)
        print(f"\n📐 Layout:")
        print(f"  • Type: {layout['type']}")
        print(f"  • Direction: {layout['direction']}")
        print(f"  • Spacing: {layout['spacing']}px")

        # Analyze text content
        text_nodes = self._extract_text_content(node)
        if text_nodes:
            print(f"\n📝 Text Content: {len(text_nodes)} text elements")

        return {
            'name': name,
            'type': node_type,
            'width': width,
            'height': height,
            'children_count': len(children),
            'components': detected_components,
            'layout': layout,
            'text_nodes': text_nodes,
            'raw_node': node
        }

    def _detect_components(self, node: Dict) -> Dict[str, int]:
        """Detect shadcn/ui components in the design."""

        components = {
            'Button': 0,
            'Card': 0,
            'Input': 0,
            'Label': 0,
            'Badge': 0,
            'Avatar': 0,
            'Separator': 0,
            'Tabs': 0,
            'Dialog': 0,
            'Select': 0,
            'Checkbox': 0,
            'Radio': 0,
            'Switch': 0,
            'Table': 0,
        }

        def traverse(n):
            name = n.get('name', '').lower()
            node_type = n.get('type', '')

            # Detect by name
            if 'button' in name or 'btn' in name:
                components['Button'] += 1
            elif 'card' in name:
                components['Card'] += 1
            elif 'input' in name or 'textfield' in name:
                components['Input'] += 1
            elif 'label' in name:
                components['Label'] += 1
            elif 'badge' in name or 'tag' in name:
                components['Badge'] += 1
            elif 'avatar' in name or 'profile' in name:
                components['Avatar'] += 1
            elif 'separator' in name or 'divider' in name:
                components['Separator'] += 1
            elif 'tab' in name:
                components['Tabs'] += 1
            elif 'modal' in name or 'dialog' in name:
                components['Dialog'] += 1
            elif 'select' in name or 'dropdown' in name:
                components['Select'] += 1
            elif 'checkbox' in name or 'check' in name:
                components['Checkbox'] += 1
            elif 'radio' in name:
                components['Radio'] += 1
            elif 'switch' in name or 'toggle' in name:
                components['Switch'] += 1
            elif 'table' in name or 'grid' in name:
                components['Table'] += 1

            # Traverse children
            for child in n.get('children', []):
                traverse(child)

        traverse(node)

        # Return only detected components
        return {k: v for k, v in components.items() if v > 0}

    def _analyze_layout(self, node: Dict) -> Dict[str, Any]:
        """Analyze layout properties."""

        layout_mode = node.get('layoutMode', 'NONE')
        primary_axis = node.get('primaryAxisAlignItems', 'MIN')
        counter_axis = node.get('counterAxisAlignItems', 'MIN')
        item_spacing = node.get('itemSpacing', 0)

        layout_type = 'Stack'
        direction = 'vertical'

        if layout_mode == 'HORIZONTAL':
            layout_type = 'Flex'
            direction = 'horizontal'
        elif layout_mode == 'VERTICAL':
            layout_type = 'Flex'
            direction = 'vertical'
        else:
            layout_type = 'Absolute'
            direction = 'none'

        return {
            'type': layout_type,
            'direction': direction,
            'spacing': item_spacing,
            'align_primary': primary_axis,
            'align_counter': counter_axis
        }

    def _extract_text_content(self, node: Dict) -> List[Dict[str, Any]]:
        """Extract all text content from node."""

        text_nodes = []

        def traverse(n):
            if n.get('type') == 'TEXT':
                text_nodes.append({
                    'content': n.get('characters', ''),
                    'style': n.get('style', {}),
                    'name': n.get('name', 'Text')
                })

            for child in n.get('children', []):
                traverse(child)

        traverse(node)
        return text_nodes

    def _generate_code(self, analysis: Dict) -> Dict[str, Any]:
        """Generate React/TypeScript code."""

        print("\n" + "="*80)
        print("💻 GENERATING CODE")
        print("="*80 + "\n")

        component_name = self._sanitize_component_name(analysis['name'])
        print(f"🎯 Component Name: {component_name}")

        # Generate component code
        component_code = self._generate_component_code(analysis, component_name)

        # Generate test code
        test_code = self._generate_test_code(component_name)

        # Generate Storybook story
        story_code = self._generate_story_code(component_name)

        # Generate installation commands
        install_commands = self._generate_install_commands(analysis['components'])

        print(f"\n✅ Code generation complete!")
        print(f"   • Component: {component_name}.tsx")
        print(f"   • Tests: {component_name}.test.tsx")
        print(f"   • Stories: {component_name}.stories.tsx")

        return {
            'component_name': component_name,
            'files': {
                f'{component_name}.tsx': component_code,
                f'{component_name}.test.tsx': test_code,
                f'{component_name}.stories.tsx': story_code
            },
            'install_commands': install_commands,
            'artemis_score': self._calculate_artemis_score(analysis)
        }

    def _sanitize_component_name(self, name: str) -> str:
        """Convert name to valid React component name."""

        # Remove special characters
        name = ''.join(c for c in name if c.isalnum() or c.isspace())

        # Convert to PascalCase
        words = name.split()
        pascal_case = ''.join(word.capitalize() for word in words if word)

        # Ensure it starts with uppercase
        if pascal_case and not pascal_case[0].isupper():
            pascal_case = pascal_case[0].upper() + pascal_case[1:]

        return pascal_case or 'Component'

    def _generate_component_code(self, analysis: Dict, component_name: str) -> str:
        """Generate React component code."""

        components = analysis.get('components', {})
        raw_node = analysis.get('raw_node', {})
        layout = analysis.get('layout', {})

        # Determine imports
        imports = ['import React from "react";']
        shadcn_imports = []

        if 'Button' in components:
            shadcn_imports.append('Button')
        if 'Card' in components:
            shadcn_imports.append('Card')
        if 'Input' in components:
            shadcn_imports.append('Input')
        if 'Badge' in components:
            shadcn_imports.append('Badge')
        if 'Avatar' in components:
            shadcn_imports.append('Avatar')
        if 'Checkbox' in components:
            shadcn_imports.append('Checkbox')

        if shadcn_imports:
            imports.append(f'import {{ {", ".join(shadcn_imports)} }} from "@/components/ui";')

        # Generate component structure
        layout_classes = []
        if layout['direction'] == 'horizontal':
            layout_classes.append('flex flex-row')
        elif layout['direction'] == 'vertical':
            layout_classes.append('flex flex-col')

        if layout['spacing'] > 0:
            gap_class = f'gap-{min(layout["spacing"] // 4, 16)}'
            layout_classes.append(gap_class)

        container_class = ' '.join(layout_classes) if layout_classes else 'flex flex-col gap-4'

        # Generate JSX by traversing the entire node tree
        jsx_content = self._generate_jsx_from_node(raw_node, indent=2)

        imports_str = '\n'.join(imports)
        code = f'''{imports_str}

export interface {component_name}Props {{
  className?: string;
}}

export function {component_name}({{ className }}: {component_name}Props) {{
  return (
    <div className="`{container_class} ${{className}}`">
{jsx_content}
    </div>
  );
}}
'''

        return code

    def _generate_jsx_from_node(self, node: Dict, indent: int = 0, depth: int = 0) -> str:
        """Recursively generate JSX from Figma node structure."""

        if depth > 5:  # Prevent infinite recursion
            return ''

        indent_str = ' ' * indent
        name = node.get('name', '').lower()
        node_type = node.get('type', '')
        children = node.get('children', [])

        jsx_parts = []

        # Handle different node types
        if node_type == 'TEXT':
            content = node.get('characters', '')
            if len(content) > 100:
                content = content[:100] + '...'
            # Escape special characters
            content = content.replace('<', '&lt;').replace('>', '&gt;')
            jsx_parts.append(f'{indent_str}<p className="text-sm">{content}</p>')

        elif 'card' in name or node_type == 'FRAME':
            # Detect if this should be a Card
            is_card = 'card' in name or (node_type == 'FRAME' and len(children) > 2)

            if is_card:
                jsx_parts.append(f'{indent_str}<Card className="p-4 space-y-2">')
                for child in children:
                    child_jsx = self._generate_jsx_from_node(child, indent + 2, depth + 1)
                    if child_jsx:
                        jsx_parts.append(child_jsx)
                jsx_parts.append(f'{indent_str}</Card>')
            else:
                # Regular frame - use div
                jsx_parts.append(f'{indent_str}<div className="space-y-2">')
                for child in children:
                    child_jsx = self._generate_jsx_from_node(child, indent + 2, depth + 1)
                    if child_jsx:
                        jsx_parts.append(child_jsx)
                jsx_parts.append(f'{indent_str}</div>')

        elif 'button' in name or 'btn' in name:
            text = self._extract_first_text(node) or 'Button'
            jsx_parts.append(f'{indent_str}<Button>{text}</Button>')

        elif 'input' in name or 'textfield' in name:
            jsx_parts.append(f'{indent_str}<Input placeholder="Enter text..." />')

        elif 'badge' in name or 'tag' in name:
            text = self._extract_first_text(node) or 'Badge'
            jsx_parts.append(f'{indent_str}<Badge>{text}</Badge>')

        elif 'avatar' in name or 'profile' in name:
            jsx_parts.append(f'{indent_str}<Avatar />')

        elif 'checkbox' in name or 'check' in name:
            jsx_parts.append(f'{indent_str}<Checkbox />')

        elif children:
            # Has children but no specific component type - render as container
            for child in children[:10]:  # Limit to first 10 children to avoid huge components
                child_jsx = self._generate_jsx_from_node(child, indent, depth + 1)
                if child_jsx:
                    jsx_parts.append(child_jsx)

        return '\n'.join(jsx_parts)

    def _extract_first_text(self, node: Dict) -> str:
        """Extract first text content from node or its children."""

        if node.get('type') == 'TEXT':
            return node.get('characters', '')[:50]

        for child in node.get('children', []):
            text = self._extract_first_text(child)
            if text:
                return text

        return ''

    def _generate_test_code(self, component_name: str) -> str:
        """Generate Jest test code."""

        code = f'''import {{ render, screen }} from '@testing-library/react';
import {{ {component_name} }} from './{component_name}';

describe('{component_name}', () => {{
  it('renders without crashing', () => {{
    render(<{component_name} />);
  }});

  it('applies custom className', () => {{
    const {{ container }} = render(<{component_name} className="custom-class" />);
    expect(container.firstChild).toHaveClass('custom-class');
  }});

  // Add more tests based on component functionality
}});
'''

        return code

    def _generate_story_code(self, component_name: str) -> str:
        """Generate Storybook story."""

        code = f'''import type {{ Meta, StoryObj }} from '@storybook/react';
import {{ {component_name} }} from './{component_name}';

const meta: Meta<typeof {component_name}> = {{
  title: 'Components/{component_name}',
  component: {component_name},
  tags: ['autodocs'],
  argTypes: {{
    className: {{
      control: 'text',
      description: 'Additional CSS classes',
    }},
  }},
}};

export default meta;
type Story = StoryObj<typeof {component_name}>;

export const Default: Story = {{
  args: {{}},
}};

export const WithCustomClass: Story = {{
  args: {{
    className: 'bg-gray-100 p-8',
  }},
}};
'''

        return code

    def _generate_install_commands(self, components: Dict[str, int]) -> List[str]:
        """Generate shadcn/ui installation commands."""

        commands = []

        component_map = {
            'Button': 'button',
            'Card': 'card',
            'Input': 'input',
            'Label': 'label',
            'Badge': 'badge',
            'Avatar': 'avatar',
            'Separator': 'separator',
            'Tabs': 'tabs',
            'Dialog': 'dialog',
            'Select': 'select',
            'Checkbox': 'checkbox',
            'Radio': 'radio-group',
            'Switch': 'switch',
            'Table': 'table',
        }

        for comp_type in components.keys():
            if comp_type in component_map:
                shadcn_name = component_map[comp_type]
                commands.append(f'npx shadcn@latest add {shadcn_name}')

        return commands

    def _calculate_artemis_score(self, analysis: Dict) -> float:
        """Calculate Artemis code quality score."""

        score = 100.0

        # Deduct if no components detected
        if not analysis.get('components'):
            score -= 20

        # Deduct if no text content
        if not analysis.get('text_nodes'):
            score -= 10

        # Deduct if layout is absolute (harder to make responsive)
        if analysis.get('layout', {}).get('type') == 'Absolute':
            score -= 15

        return max(score, 0)

    def _save_generated_files(self, result: Dict):
        """Save generated files to disk."""

        print("\n" + "="*80)
        print("💾 SAVING GENERATED FILES")
        print("="*80 + "\n")

        output_dir = Path('generated_components')
        output_dir.mkdir(exist_ok=True)

        for filename, content in result['files'].items():
            file_path = output_dir / filename
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"✅ Saved: {file_path}")

        # Save metadata
        metadata_path = output_dir / 'generation_metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump({
                'component_name': result['component_name'],
                'install_commands': result['install_commands'],
                'artemis_score': result['artemis_score'],
                'generated_at': datetime.now().isoformat()
            }, f, indent=2)
        print(f"✅ Saved: {metadata_path}")

        print(f"\n📦 Installation Commands:")
        for cmd in result['install_commands']:
            print(f"   {cmd}")

        print(f"\n🏆 Artemis Score: {result['artemis_score']}/100")


def main():
    # Settings page from Figma
    figma_url = "https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=2-948&t=2TlHng7DSkyXuuCy-4"
    # Convert node-id format from URL (2-948) to API format (2:948)
    node_id = "2:948"
    figma_token = "figd_aPXrH3Rqpm8sdez_nHmmXKHvZ9vcK3sOcJwvhE7s"

    generator = ArtemisCodeGenerator(figma_token)
    result = generator.convert_to_code(figma_url, node_id)

    return result


if __name__ == "__main__":
    result = main()
