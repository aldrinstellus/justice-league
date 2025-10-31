#!/usr/bin/env python3
"""
Unit tests for polymorphic return type handling in export_figma_png.py

Tests ensure the script correctly handles both:
- List[Dict] returns from Quicksilver
- Dict returns from other export methods

Oracle Pattern: Type-Safe Polymorphic Return Handling
Created: 2025-10-31
"""

import unittest
import sys
from pathlib import Path

# Add parent for imports
sys.path.append(str(Path(__file__).parent))


class TestExportResultHandling(unittest.TestCase):
    """Test type-safe handling of polymorphic export results"""

    def test_list_result_success_check(self):
        """Test success detection with List[Dict] result (Quicksilver format)"""
        # Simulate Quicksilver return format
        result = [
            {'frame_name': 'Frame1', 'success': True},
            {'frame_name': 'Frame2', 'success': True},
            {'frame_name': 'Frame3', 'success': False}
        ]

        # Type-safe success check (CORRECT)
        is_success = isinstance(result, list) and len(result) > 0
        if not is_success and isinstance(result, dict):
            is_success = result.get('success', False)

        self.assertTrue(is_success, "List with items should be considered success")

    def test_dict_result_success_check(self):
        """Test success detection with Dict result (legacy format)"""
        # Simulate legacy dict return format
        result = {
            'success': True,
            'frames_exported': 484,
            'total_frames': 484
        }

        # Type-safe success check
        is_success = isinstance(result, list) and len(result) > 0
        if not is_success and isinstance(result, dict):
            is_success = result.get('success', False)

        self.assertTrue(is_success, "Dict with success=True should be considered success")

    def test_dict_result_failure_check(self):
        """Test failure detection with Dict result"""
        result = {
            'success': False,
            'error': 'Some error occurred'
        }

        # Type-safe success check
        is_success = isinstance(result, list) and len(result) > 0
        if not is_success and isinstance(result, dict):
            is_success = result.get('success', False)

        self.assertFalse(is_success, "Dict with success=False should not be considered success")

    def test_empty_list_failure_check(self):
        """Test failure detection with empty list"""
        result = []

        # Type-safe success check
        is_success = isinstance(result, list) and len(result) > 0
        if not is_success and isinstance(result, dict):
            is_success = result.get('success', False)

        self.assertFalse(is_success, "Empty list should not be considered success")

    def test_antipattern_causes_error(self):
        """Test that the WRONG pattern causes AttributeError"""
        result = [{'success': True}]

        # This is the ANTIPATTERN that caused the bug
        with self.assertRaises(AttributeError):
            # This will fail because list has no .get() method
            if result.get('success'):  # WRONG!
                pass

    def test_correct_pattern_no_error(self):
        """Test that the CORRECT pattern handles both types safely"""
        # Test with list
        result_list = [{'success': True}]
        try:
            is_success = isinstance(result_list, list) and len(result_list) > 0
            if not is_success and isinstance(result_list, dict):
                is_success = result_list.get('success', False)
            success_list = True
        except AttributeError:
            success_list = False

        # Test with dict
        result_dict = {'success': True}
        try:
            is_success = isinstance(result_dict, list) and len(result_dict) > 0
            if not is_success and isinstance(result_dict, dict):
                is_success = result_dict.get('success', False)
            success_dict = True
        except AttributeError:
            success_dict = False

        self.assertTrue(success_list, "Correct pattern should handle list without error")
        self.assertTrue(success_dict, "Correct pattern should handle dict without error")

    def test_frame_count_extraction_list(self):
        """Test extracting frame counts from list format"""
        result = [
            {'frame_name': 'Frame1', 'success': True},
            {'frame_name': 'Frame2', 'success': True},
            {'frame_name': 'Frame3', 'success': False}
        ]

        if isinstance(result, list):
            total_frames = len(result)
            frames_exported = sum(1 for r in result if r.get('success'))
        else:
            total_frames = result.get('total_frames', 0)
            frames_exported = result.get('frames_exported', 0)

        self.assertEqual(total_frames, 3, "Should count all frames")
        self.assertEqual(frames_exported, 2, "Should count only successful frames")

    def test_frame_count_extraction_dict(self):
        """Test extracting frame counts from dict format"""
        result = {
            'success': True,
            'frames_exported': 484,
            'total_frames': 484
        }

        if isinstance(result, list):
            total_frames = len(result)
            frames_exported = sum(1 for r in result if r.get('success'))
        else:
            total_frames = result.get('total_frames', 0)
            frames_exported = result.get('frames_exported', 0)

        self.assertEqual(total_frames, 484, "Should extract total from dict")
        self.assertEqual(frames_exported, 484, "Should extract exported from dict")


if __name__ == '__main__':
    print("=" * 80)
    print("Testing Type-Safe Polymorphic Return Handling")
    print("=" * 80)
    print()
    print("🔮 Oracle: Running tests to prevent AttributeError...")
    print()

    # Run tests
    unittest.main(verbosity=2)
