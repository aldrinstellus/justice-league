#!/usr/bin/env python3
"""
🔨 Hephaestus Code-to-Design Test Suite
========================================

Tests for React/TypeScript to Figma conversion capability.

Author: Justice League
Created: October 23, 2025
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.justice_league.hephaestus_code_to_design import HephaestusCodeToDesign


def test_hephaestus_initialization():
    """Test 1: Hephaestus Code-to-Design initialization."""
    print("\n" + "=" * 70)
    print("Test 1: Hephaestus Code-to-Design Initialization")
    print("=" * 70)

    hephaestus = HephaestusCodeToDesign()

    assert hephaestus is not None, "Hephaestus should initialize"
    assert hasattr(hephaestus, 'convert_to_figma'), "Should have convert_to_figma method"
    assert hasattr(hephaestus, 'parse_react_file'), "Should have parse_react_file method"
    assert hasattr(hephaestus, 'jsx_to_figma_nodes'), "Should have jsx_to_figma_nodes method"

    print("✅ PASSED: Hephaestus Code-to-Design initialized successfully")
    return True


def test_react_file_parsing():
    """Test 2: React component file parsing."""
    print("\n" + "=" * 70)
    print("Test 2: React Component File Parsing")
    print("=" * 70)

    hephaestus = HephaestusCodeToDesign()

    # Create test React component
    test_component = '''
import React from 'react';
import { Button } from '@/components/ui/button';

interface TestComponentProps {
  title: string;
  onClick?: () => void;
}

export function TestComponent({ title, onClick }: TestComponentProps) {
  return (
    <div className="flex flex-col gap-4 p-4">
      <h1 className="text-2xl font-bold">{title}</h1>
      <Button onClick={onClick}>Click Me</Button>
    </div>
  );
}
'''

    # Write test file
    test_file = Path('/tmp/test_component.tsx')
    test_file.write_text(test_component)

    # Parse component
    component = hephaestus.parse_react_file(str(test_file))

    assert component is not None, "Should parse component"
    assert component.name == 'TestComponent', f"Expected 'TestComponent', got '{component.name}'"
    assert len(component.imports) > 0, "Should extract imports"
    assert 'Button' in str(component.imports), "Should find Button import"
    assert component.jsx_tree is not None, "Should extract JSX tree"
    assert 'title' in component.props, "Should extract 'title' prop"
    assert 'onClick' in component.props, "Should extract 'onClick' prop"

    # Cleanup
    test_file.unlink()

    print(f"✅ PASSED: Parsed React component '{component.name}' with {len(component.imports)} imports")
    print(f"   Props found: {', '.join(component.props.keys())}")

    return True


def test_jsx_to_figma_conversion():
    """Test 3: JSX to Figma node conversion."""
    print("\n" + "=" * 70)
    print("Test 3: JSX to Figma Node Conversion")
    print("=" * 70)

    hephaestus = HephaestusCodeToDesign()

    # Test simple JSX tree
    jsx_tree = {
        'type': 'div',
        'props': {
            'className': 'flex flex-col gap-4'
        },
        'children': [
            {
                'type': 'h1',
                'props': {
                    'className': 'text-2xl font-bold'
                },
                'children': 'Hello World'
            },
            {
                'type': 'Button',
                'props': {
                    'variant': 'default'
                },
                'children': 'Click Me'
            }
        ]
    }

    figma_node = hephaestus.jsx_to_figma_nodes(jsx_tree)

    assert figma_node is not None, "Should create Figma node"
    assert figma_node.type.value == 'FRAME', f"div should map to FRAME, got {figma_node.type.value}"
    assert figma_node.name == 'div', "Should preserve element name"
    assert len(figma_node.children) == 2, f"Should have 2 children, got {len(figma_node.children)}"

    # Check first child (h1)
    h1_node = figma_node.children[0]
    assert h1_node.type.value == 'TEXT', f"h1 should map to TEXT, got {h1_node.type.value}"
    assert h1_node.characters == 'Hello World', "Should preserve text content"

    # Check second child (Button)
    button_node = figma_node.children[1]
    assert button_node.type.value == 'FRAME', f"Button should map to FRAME, got {button_node.type.value}"

    print(f"✅ PASSED: Converted JSX tree to {len(figma_node.children)} Figma nodes")
    print(f"   Node types: {figma_node.type} → {[child.type for child in figma_node.children]}")

    return True


def test_tailwind_style_conversion():
    """Test 4: Tailwind CSS to Figma style conversion."""
    print("\n" + "=" * 70)
    print("Test 4: Tailwind CSS to Figma Style Conversion")
    print("=" * 70)

    hephaestus = HephaestusCodeToDesign()

    # Test various Tailwind classes
    test_classes = [
        'w-64',           # width
        'h-32',           # height
        'bg-blue-500',    # background color
        'text-2xl',       # font size
        'font-bold',      # font weight
        'p-4',            # padding
        'm-2',            # margin
        'flex',           # display flex
        'rounded-lg',     # border radius
        'border-2'        # border width
    ]

    styles = hephaestus._convert_tailwind_classes(test_classes)

    assert 'width' in styles, "Should convert w-64 to width"
    assert 'height' in styles, "Should convert h-32 to height"
    assert 'fill' in styles or 'backgroundColor' in styles, "Should convert bg-blue-500"
    assert 'fontSize' in styles, "Should convert text-2xl to fontSize"
    assert 'fontWeight' in styles, "Should convert font-bold to fontWeight"
    assert 'paddingTop' in styles or 'padding' in styles, "Should convert p-4 to padding"
    assert 'layoutMode' in styles, "Should convert flex to layoutMode"
    assert 'cornerRadius' in styles, "Should convert rounded-lg to cornerRadius"
    assert 'strokeWeight' in styles, "Should convert border-2 to strokeWeight"

    print(f"✅ PASSED: Converted {len(test_classes)} Tailwind classes to {len(styles)} Figma styles")
    print(f"   Styles: {', '.join(styles.keys())}")

    return True


def test_hephaestus_score_calculation():
    """Test 5: Hephaestus Score calculation."""
    print("\n" + "=" * 70)
    print("Test 5: Hephaestus Score Calculation")
    print("=" * 70)

    hephaestus = HephaestusCodeToDesign()

    # Import the dataclasses we need
    from core.justice_league.hephaestus_code_to_design import ReactComponent, FigmaNode, FigmaNodeType

    # Test high quality component
    high_quality_component = ReactComponent(
        name='HighQualityComponent',
        file_path='/tmp/test.tsx',
        imports=['Button', 'Card', 'Input'],
        props={'title': 'string', 'onClick': 'function', 'disabled': 'boolean', 'className': 'string', 'children': 'ReactNode'},
        styles={
            'tailwind_classes': ['w-64', 'h-32', 'bg-blue-500', 'text-2xl', 'font-bold',
                                'p-4', 'm-2', 'flex', 'rounded-lg', 'border-2',
                                'text-white', 'hover:bg-blue-600', 'gap-4', 'items-center', 'justify-center'],
            'inline_styles': {},
            'css_modules': {}
        },
        jsx_tree={'type': 'div', 'children': [{'type': 'h1', 'children': ['Title']}]}
    )

    high_quality_nodes = FigmaNode(
        id='node_1',
        name='HighQualityComponent',
        type=FigmaNodeType.FRAME,
        properties={},
        children=[
            FigmaNode(id='node_2', name='Text1', type=FigmaNodeType.TEXT, properties={}, children=[], styles={}),
            FigmaNode(id='node_3', name='Frame1', type=FigmaNodeType.FRAME, properties={}, children=[], styles={}),
            FigmaNode(id='node_4', name='Text2', type=FigmaNodeType.TEXT, properties={}, children=[], styles={}),
            FigmaNode(id='node_5', name='Button', type=FigmaNodeType.FRAME, properties={}, children=[], styles={}),
            FigmaNode(id='node_6', name='Card', type=FigmaNodeType.FRAME, properties={}, children=[], styles={}),
            FigmaNode(id='node_7', name='Input', type=FigmaNodeType.FRAME, properties={}, children=[], styles={}),
        ],
        styles={}
    )

    score_high = hephaestus._calculate_hephaestus_score(high_quality_component, high_quality_nodes)
    assert score_high >= 70, f"High quality should score >= 70, got {score_high}"

    # Test low quality component
    low_quality_component = ReactComponent(
        name='LowQualityComponent',
        file_path='/tmp/low.tsx',
        imports=[],
        props={},
        styles={},
        jsx_tree={'type': 'div', 'children': []}
    )

    low_quality_nodes = FigmaNode(
        id='node_1',
        name='LowQualityComponent',
        type=FigmaNodeType.FRAME,
        properties={},
        children=[],
        styles={}
    )

    score_low = hephaestus._calculate_hephaestus_score(low_quality_component, low_quality_nodes)
    assert score_low < 50, f"Low quality should score < 50, got {score_low}"

    print(f"✅ PASSED: Hephaestus Score calculation works")
    print(f"   High Quality Score: {score_high}/100")
    print(f"   Low Quality Score:  {score_low}/100")

    return True


def test_shadcn_component_detection():
    """Test 6: shadcn/ui component detection and mapping."""
    print("\n" + "=" * 70)
    print("Test 6: shadcn/ui Component Detection")
    print("=" * 70)

    hephaestus = HephaestusCodeToDesign()

    # Test shadcn/ui components
    shadcn_components = ['Button', 'Card', 'Input', 'Label', 'Select', 'Dialog']

    for component in shadcn_components:
        jsx_node = {
            'type': component,
            'props': {},
            'children': []
        }

        figma_node = hephaestus.jsx_to_figma_nodes(jsx_node)

        assert figma_node is not None, f"Should convert {component}"
        assert figma_node.type.value in ['FRAME', 'TEXT', 'COMPONENT'], \
            f"{component} should map to valid Figma type, got {figma_node.type.value}"

    print(f"✅ PASSED: Successfully detected and converted {len(shadcn_components)} shadcn/ui components")
    print(f"   Components: {', '.join(shadcn_components)}")

    return True


def test_full_integration():
    """Test 7: Full integration test."""
    print("\n" + "=" * 70)
    print("Test 7: Full Integration Test")
    print("=" * 70)

    hephaestus = HephaestusCodeToDesign()

    # Create comprehensive test component
    test_component = '''
import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

interface LoginFormProps {
  onSubmit?: (data: any) => void;
  className?: string;
}

export function LoginForm({ onSubmit, className }: LoginFormProps) {
  return (
    <Card className="w-96 mx-auto p-6">
      <CardHeader>
        <CardTitle className="text-2xl font-bold">Login</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <input
          type="email"
          placeholder="Email"
          className="border rounded p-2"
        />
        <input
          type="password"
          placeholder="Password"
          className="border rounded p-2"
        />
        <Button className="w-full bg-blue-500">
          Sign In
        </Button>
      </CardContent>
    </Card>
  );
}
'''

    # Write test file
    test_file = Path('/tmp/login_form.tsx')
    test_file.write_text(test_component)

    # Full conversion
    result = hephaestus.convert_to_figma(
        component_path=str(test_file),
        options={
            'figma_file_id': 'test-file-123',
            'create_frame': True,
            'organize_layers': True
        }
    )

    assert result['success'], f"Conversion should succeed, got errors: {result.get('errors')}"
    assert 'figma_url' in result, "Result should contain figma_url"
    assert 'nodes_created' in result, "Result should contain nodes_created"
    assert 'hephaestus_score' in result, "Result should contain hephaestus_score"
    assert result['hephaestus_score'] > 0, f"Hephaestus score should be > 0, got {result['hephaestus_score']}"
    assert result['nodes_created'] >= 3, f"Should create at least 3 nodes, got {result['nodes_created']}"

    # Cleanup
    test_file.unlink()

    print(f"\n✅ PASSED: Full integration test successful")
    print(f"   Hephaestus Score: {result['hephaestus_score']}/100")
    print(f"   Nodes Created: {result['nodes_created']}")
    print(f"   Component: {result['component_name']}")

    return True


def run_all_tests():
    """Run complete test suite."""
    print("\n🔨 Hephaestus Code-to-Design Test Suite")
    print("=" * 70)
    print("Testing React/TypeScript to Figma Conversion Capability")
    print("=" * 70)

    tests = [
        ("Initialization", test_hephaestus_initialization),
        ("React File Parsing", test_react_file_parsing),
        ("JSX to Figma Conversion", test_jsx_to_figma_conversion),
        ("Tailwind Style Conversion", test_tailwind_style_conversion),
        ("Hephaestus Score Calculation", test_hephaestus_score_calculation),
        ("shadcn/ui Component Detection", test_shadcn_component_detection),
        ("Full Integration", test_full_integration),
    ]

    passed = 0
    failed = 0
    errors = []

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except AssertionError as e:
            failed += 1
            errors.append(f"{test_name}: {str(e)}")
            print(f"\n❌ FAILED: {test_name}")
            print(f"   Error: {str(e)}")
        except Exception as e:
            failed += 1
            errors.append(f"{test_name}: {str(e)}")
            print(f"\n❌ ERROR: {test_name}")
            print(f"   Error: {str(e)}")

    # Summary
    print("\n" + "=" * 70)
    print("Test Suite Summary")
    print("=" * 70)
    print(f"Total Tests: {len(tests)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")

    if errors:
        print(f"\n❌ Errors:")
        for error in errors:
            print(f"   - {error}")

    success_rate = (passed / len(tests)) * 100
    print(f"\nSuccess Rate: {success_rate:.1f}%")

    if success_rate == 100:
        print("\n🎉 ALL TESTS PASSED! Hephaestus Code-to-Design is ready!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review.")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
