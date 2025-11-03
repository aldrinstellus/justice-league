"""
🦅 HAWKMAN TESTS - Structural Parser Test Suite
===============================================

Tests for Hawkman's layer-by-layer Figma parsing capabilities

Author: Hawkman + Claude Code
Created: October 24, 2025
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.justice_league.hawkman_structural_parser import (
    HawkmanStructuralParser,
    OutputFormat,
    ParsingDepth,
    FigmaLayerType,
    parse_figma_to_code
)


class TestHawkmanStructuralParser(unittest.TestCase):
    """Test suite for Hawkman Structural Parser"""

    def setUp(self):
        """Set up test fixtures"""
        self.hawkman = HawkmanStructuralParser()
        self.test_figma_url = "https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=2-948"

    def test_initialization(self):
        """Test Hawkman initializes correctly"""
        self.assertIsNotNone(self.hawkman)
        self.assertEqual(self.hawkman.hero_name, "Hawkman")
        self.assertEqual(self.hawkman.hero_emoji, "🦅")
        self.assertIsNotNone(self.hawkman.green_arrow)
        self.assertTrue(self.hawkman.parsing_data_dir.exists())

    def test_extract_figma_identifiers(self):
        """Test extraction of file key and node ID from Figma URL"""
        file_key, node_id = self.hawkman._extract_figma_identifiers(self.test_figma_url)

        self.assertEqual(file_key, "6Pmf9gCcUccyqbCO9nN6Ts")
        self.assertEqual(node_id, "2-948")

    def test_extract_figma_identifiers_without_node(self):
        """Test extraction when no node ID present"""
        url_without_node = "https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test"
        file_key, node_id = self.hawkman._extract_figma_identifiers(url_without_node)

        self.assertEqual(file_key, "6Pmf9gCcUccyqbCO9nN6Ts")
        self.assertIsNone(node_id)

    def test_extract_figma_identifiers_invalid_url(self):
        """Test extraction fails with invalid URL"""
        invalid_url = "https://example.com/not-figma"

        with self.assertRaises(ValueError):
            self.hawkman._extract_figma_identifiers(invalid_url)

    def test_count_layers_simple(self):
        """Test layer counting with simple structure"""
        structure = {
            'name': 'Root',
            'type': 'FRAME',
            'children': [
                {'name': 'Child1', 'type': 'FRAME'},
                {'name': 'Child2', 'type': 'FRAME'}
            ]
        }

        count = self.hawkman._count_layers(structure)
        self.assertEqual(count, 3)  # Root + 2 children

    def test_count_layers_nested(self):
        """Test layer counting with nested structure"""
        structure = {
            'name': 'Root',
            'type': 'FRAME',
            'children': [
                {
                    'name': 'Child1',
                    'type': 'FRAME',
                    'children': [
                        {'name': 'Grandchild1', 'type': 'TEXT'},
                        {'name': 'Grandchild2', 'type': 'TEXT'}
                    ]
                },
                {'name': 'Child2', 'type': 'FRAME'}
            ]
        }

        count = self.hawkman._count_layers(structure)
        self.assertEqual(count, 5)  # Root + 2 children + 2 grandchildren

    def test_calculate_max_depth(self):
        """Test maximum depth calculation"""
        structure = {
            'name': 'Root',
            'children': [
                {
                    'name': 'L1',
                    'children': [
                        {
                            'name': 'L2',
                            'children': [
                                {'name': 'L3'}
                            ]
                        }
                    ]
                }
            ]
        }

        max_depth = self.hawkman._calculate_max_depth(structure)
        self.assertEqual(max_depth, 3)

    def test_calculate_avg_children(self):
        """Test average children calculation"""
        structure = {
            'name': 'Root',
            'children': [
                {
                    'name': 'Child1',
                    'children': [
                        {'name': 'G1'},
                        {'name': 'G2'}
                    ]
                },
                {'name': 'Child2'}
            ]
        }

        avg_children = self.hawkman._calculate_avg_children(structure)
        # Root has 2 children, Child1 has 2 children, Child2 has 0, G1 has 0, G2 has 0
        # Total children: 2 + 2 + 0 + 0 + 0 = 4
        # Total layers: 5
        # Average: 4/5 = 0.8
        self.assertAlmostEqual(avg_children, 0.8)

    def test_detect_components_true(self):
        """Test component detection when components exist"""
        structure = {
            'name': 'Root',
            'type': 'FRAME',
            'children': [
                {
                    'name': 'Button',
                    'type': 'COMPONENT'  # This is a component
                }
            ]
        }

        has_components = self.hawkman._detect_components(structure)
        self.assertTrue(has_components)

    def test_detect_components_false(self):
        """Test component detection when no components exist"""
        structure = {
            'name': 'Root',
            'type': 'FRAME',
            'children': [
                {'name': 'Text', 'type': 'TEXT'},
                {'name': 'Rectangle', 'type': 'RECTANGLE'}
            ]
        }

        has_components = self.hawkman._detect_components(structure)
        self.assertFalse(has_components)

    def test_is_component_boundary(self):
        """Test component boundary detection"""
        # Test with COMPONENT type
        component_layer = {'name': 'Button', 'type': 'COMPONENT'}
        self.assertTrue(self.hawkman._is_component_boundary(component_layer))

        # Test with component indicator in name
        button_layer = {'name': 'Primary Button', 'type': 'FRAME'}
        self.assertTrue(self.hawkman._is_component_boundary(button_layer))

        # Test with regular frame
        regular_layer = {'name': 'Container', 'type': 'FRAME'}
        self.assertFalse(self.hawkman._is_component_boundary(regular_layer))

    def test_determine_output_format_simple(self):
        """Test format selection for simple structure"""
        simple_structure = {
            'name': 'Simple',
            'type': 'FRAME',
            'children': [
                {'name': 'Text', 'type': 'TEXT'},
                {'name': 'Rectangle', 'type': 'RECTANGLE'}
            ]
        }

        format = self.hawkman._determine_output_format(simple_structure)
        self.assertEqual(format, OutputFormat.HTML_CSS)

    def test_determine_output_format_moderate(self):
        """Test format selection for moderate complexity"""
        moderate_structure = {
            'name': 'Moderate',
            'type': 'FRAME',
            'children': [
                {'name': f'Child{i}', 'type': 'FRAME'} for i in range(15)
            ]
        }

        format = self.hawkman._determine_output_format(moderate_structure)
        self.assertEqual(format, OutputFormat.HTML_TAILWIND)

    def test_determine_parsing_depth(self):
        """Test adaptive depth determination"""
        shallow_structure = {
            'name': 'Shallow',
            'type': 'FRAME',
            'children': [
                {'name': 'Child1', 'type': 'FRAME'},
                {'name': 'Child2', 'type': 'FRAME'}
            ]
        }

        depth = self.hawkman._determine_parsing_depth(shallow_structure)
        self.assertEqual(depth, ParsingDepth.FRAME)

    def test_parse_layer_hierarchy_frame_depth(self):
        """Test layer parsing at FRAME depth"""
        structure = {
            'name': 'Root',
            'type': 'FRAME',
            'children': [
                {
                    'name': 'Child',
                    'type': 'FRAME',
                    'children': [
                        {'name': 'Grandchild', 'type': 'TEXT'}
                    ]
                }
            ]
        }

        hierarchy = self.hawkman._parse_layer_hierarchy(
            structure,
            depth=ParsingDepth.FRAME
        )

        # At FRAME depth, should only parse top level
        self.assertEqual(len(hierarchy['children']), 1)
        self.assertEqual(len(hierarchy['children'][0]['children']), 0)  # Should not parse grandchildren

    def test_generate_html_css(self):
        """Test HTML/CSS code generation"""
        layer = {
            'name': 'Container',
            'type': 'FRAME',
            'children': [
                {'name': 'Header', 'type': 'FRAME', 'children': []},
                {'name': 'Content', 'type': 'FRAME', 'children': []}
            ]
        }

        html = self.hawkman._generate_html_css(layer)

        self.assertIn('<div class="container">', html)
        self.assertIn('<div class="header">', html)
        self.assertIn('<div class="content">', html)
        self.assertIn('</div>', html)

    def test_generate_html_tailwind(self):
        """Test HTML + Tailwind code generation"""
        layer = {
            'name': 'Container',
            'type': 'FRAME',
            'children': [
                {'name': 'Header', 'type': 'FRAME', 'children': []}
            ]
        }

        html = self.hawkman._generate_html_tailwind(layer)

        self.assertIn('<div class=', html)
        self.assertIn('</div>', html)
        # Tailwind classes should be present
        self.assertIn('relative', html)

    def test_generate_react_tailwind(self):
        """Test React + Tailwind code generation"""
        layer = {
            'name': 'MyComponent',
            'type': 'FRAME',
            'children': []
        }

        react_code = self.hawkman._generate_react_tailwind(layer)

        self.assertIn('import React from', react_code)
        self.assertIn('export default function MyComponent', react_code)
        self.assertIn('className=', react_code)
        self.assertIn('return (', react_code)

    def test_map_layer_to_tailwind(self):
        """Test Tailwind class mapping"""
        frame_layer = {'name': 'Container', 'type': 'FRAME'}
        classes = self.hawkman._map_layer_to_tailwind(frame_layer)

        self.assertIn('relative', classes)
        self.assertIn('flex', classes)

    def test_convenience_function(self):
        """Test convenience function for parsing"""
        # This will use mock data since actual Figma API isn't connected
        result = parse_figma_to_code(
            figma_url=self.test_figma_url,
            output_format="auto",
            verify=False  # Skip verification for unit test
        )

        self.assertIn('generated_code', result)
        self.assertIn('layer_hierarchy', result)
        self.assertIn('output_format', result)
        self.assertIsInstance(result['generated_code'], str)


class TestHawkmanDatabases(unittest.TestCase):
    """Test database initialization and operations"""

    def setUp(self):
        """Set up test fixtures"""
        self.hawkman = HawkmanStructuralParser()

    def test_databases_created(self):
        """Test that all databases are created"""
        self.assertTrue(self.hawkman.parsing_history_db.exists())
        self.assertTrue(self.hawkman.layer_mappings_db.exists())
        self.assertTrue(self.hawkman.patterns_db.exists())

    def test_save_parsing_record(self):
        """Test saving parsing record"""
        record = {
            'timestamp': '2025-10-24T00:00:00',
            'figma_url': 'https://figma.com/test',
            'file_key': 'test123',
            'node_id': '1-2',
            'output_format': 'html_css',
            'accuracy_score': 95
        }

        self.hawkman._save_parsing_record(record)

        # Verify record was saved
        import json
        with open(self.hawkman.parsing_history_db, 'r') as f:
            data = json.load(f)

        self.assertGreater(len(data['parsings']), 0)
        self.assertEqual(data['parsings'][-1]['figma_url'], 'https://figma.com/test')


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    run_tests()
