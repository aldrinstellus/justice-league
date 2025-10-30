#!/usr/bin/env python3
"""
🦇 Batman Testing - Test Suite
================================

Tests for Batman's interactive element testing capabilities.

Author: Justice League
Created: October 23, 2025
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.justice_league.batman_testing import BatmanTesting


def test_batman_initialization():
    """Test 1: Batman initialization."""
    print("\n" + "=" * 70)
    print("Test 1: Batman Initialization")
    print("=" * 70)

    batman = BatmanTesting()

    assert batman is not None, "Batman should initialize"
    assert hasattr(batman, 'test_all_interactive_elements'), "Should have test_all_interactive_elements method"
    assert hasattr(batman, '_test_buttons'), "Should have _test_buttons method"
    assert hasattr(batman, '_test_links'), "Should have _test_links method"
    assert hasattr(batman, '_test_inputs'), "Should have _test_inputs method"
    assert hasattr(batman, '_calculate_batman_score'), "Should have _calculate_batman_score method"
    assert batman.test_results == [], "Should initialize with empty test_results"
    assert batman.accessibility_issues == [], "Should initialize with empty accessibility_issues"

    print("✅ PASSED: Batman initialized successfully")
    return True


def test_extract_interactive_elements():
    """Test 2: Extract interactive elements from page snapshot."""
    print("\n" + "=" * 70)
    print("Test 2: Extract Interactive Elements")
    print("=" * 70)

    batman = BatmanTesting()

    # Mock page snapshot as a text string (Chrome DevTools format)
    mock_snapshot = """
uid=btn_submit button "Submit"
uid=btn_cancel button "Cancel"
uid=link_home link "Home"
uid=link_about link "About"
uid=input_email textbox value=""
uid=input_password textbox value=""
uid=div_container generic "Container"
"""

    elements = batman._extract_interactive_elements(mock_snapshot)

    assert len(elements) > 0, "Should extract interactive elements"

    # Check buttons
    buttons = [e for e in elements if e['type'] == 'button']
    assert len(buttons) >= 2, f"Should find at least 2 buttons, found {len(buttons)}"

    # Check links
    links = [e for e in elements if e['type'] == 'link']
    assert len(links) >= 2, f"Should find at least 2 links, found {len(links)}"

    # Check inputs
    inputs = [e for e in elements if e['type'] in ['textbox', 'combobox']]
    assert len(inputs) >= 2, f"Should find at least 2 inputs, found {len(inputs)}"

    print(f"✅ PASSED: Extracted {len(elements)} interactive elements")
    print(f"   Buttons: {len(buttons)}, Links: {len(links)}, Inputs: {len(inputs)}")

    return True


def test_button_testing():
    """Test 3: Button click testing."""
    print("\n" + "=" * 70)
    print("Test 3: Button Click Testing")
    print("=" * 70)

    batman = BatmanTesting()

    # Mock buttons
    mock_buttons = [
        {'uid': 'btn_submit', 'type': 'button', 'name': 'Submit', 'text': 'Submit'},
        {'uid': 'btn_cancel', 'type': 'button', 'name': 'Cancel', 'text': 'Cancel'}
    ]

    # Mock MCP tools
    click_results = []
    def mock_click(uid, **kwargs):
        click_results.append(uid)
        return {'success': True, 'uid': uid}

    mock_mcp_tools = {
        'click': mock_click,
        'take_snapshot': lambda: {'elements': []},
        'list_console': lambda: []
    }

    results = batman._test_buttons(mock_buttons, mock_mcp_tools)

    assert 'test_type' in results, "Should have test_type"
    assert results['test_type'] == 'Button Testing', "test_type should be 'Button Testing'"
    assert 'elements_tested' in results, "Should have elements_tested count"
    assert results['elements_tested'] == 2, f"Should test 2 buttons, tested {results['elements_tested']}"

    print(f"✅ PASSED: Tested {results['elements_tested']} buttons")
    print(f"   Test Type: {results['test_type']}")

    return True


def test_link_testing():
    """Test 4: Link navigation testing."""
    print("\n" + "=" * 70)
    print("Test 4: Link Navigation Testing")
    print("=" * 70)

    batman = BatmanTesting()

    # Mock links
    mock_links = [
        {'uid': 'link_home', 'type': 'link', 'name': 'Home', 'href': '/'},
        {'uid': 'link_about', 'type': 'link', 'name': 'About', 'href': '/about'},
        {'uid': 'link_contact', 'type': 'link', 'name': 'Contact', 'href': '/contact'}
    ]

    # Mock MCP tools
    click_results = []
    def mock_click(uid, **kwargs):
        click_results.append(uid)
        return {'success': True, 'uid': uid}

    mock_mcp_tools = {
        'click': mock_click,
        'take_snapshot': lambda: {'elements': []},
        'list_console': lambda: []
    }

    results = batman._test_links(mock_links, mock_mcp_tools)

    assert 'test_type' in results, "Should have test_type"
    assert results['test_type'] == 'Link Testing', "test_type should be 'Link Testing'"
    assert 'elements_tested' in results, "Should have elements_tested count"
    assert results['elements_tested'] == 3, f"Should test 3 links, tested {results['elements_tested']}"

    print(f"✅ PASSED: Tested {results['elements_tested']} links")
    print(f"   Test Type: {results['test_type']}")

    return True


def test_input_testing():
    """Test 5: Form input testing."""
    print("\n" + "=" * 70)
    print("Test 5: Form Input Testing")
    print("=" * 70)

    batman = BatmanTesting()

    # Mock inputs
    mock_inputs = [
        {'uid': 'input_email', 'type': 'textbox', 'name': 'Email'},
        {'uid': 'input_password', 'type': 'textbox', 'name': 'Password'},
        {'uid': 'input_name', 'type': 'textbox', 'name': 'Name'}
    ]

    # Mock MCP tools
    fill_results = []
    def mock_fill(uid, value, **kwargs):
        fill_results.append({'uid': uid, 'value': value})
        return {'success': True, 'uid': uid, 'value': value}

    mock_mcp_tools = {
        'fill': mock_fill,
        'take_snapshot': lambda: {'elements': []},
        'list_console': lambda: []
    }

    results = batman._test_inputs(mock_inputs, mock_mcp_tools)

    assert 'test_type' in results, "Should have test_type"
    assert results['test_type'] == 'Form Input Testing', "test_type should be 'Form Input Testing'"
    assert 'elements_tested' in results, "Should have elements_tested count"
    assert results['elements_tested'] == 3, f"Should test 3 inputs, tested {results['elements_tested']}"

    print(f"✅ PASSED: Tested {results['elements_tested']} form inputs")
    print(f"   Test Type: {results['test_type']}")

    return True


def test_batman_score_calculation():
    """Test 6: Batman score calculation."""
    print("\n" + "=" * 70)
    print("Test 6: Batman Score Calculation")
    print("=" * 70)

    batman = BatmanTesting()

    # Test high quality results (Batman score uses success_rate and accessibility_regressions)
    high_quality_results = {
        'success_rate': 90.0,  # 90% success rate
        'accessibility_regressions': 0
    }

    score_high = batman._calculate_batman_score(high_quality_results)

    assert 'score' in score_high, "Should have score"
    assert 'grade' in score_high, "Should have grade"
    assert score_high['score'] >= 70, f"High quality should score >= 70, got {score_high['score']}"

    # Test low quality results
    low_quality_results = {
        'success_rate': 30.0,  # 30% success rate
        'accessibility_regressions': 5  # 5 regressions = -25 points
    }

    score_low = batman._calculate_batman_score(low_quality_results)

    assert score_low['score'] < 30, f"Low quality should score < 30, got {score_low['score']}"

    print(f"✅ PASSED: Batman Score calculation works")
    print(f"   High Quality Score: {score_high['score']}/100 (Grade: {score_high['grade']})")
    print(f"   Low Quality Score:  {score_low['score']}/100 (Grade: {score_low['grade']})")

    return True


def test_generate_recommendations():
    """Test 7: Generate Batman recommendations."""
    print("\n" + "=" * 70)
    print("Test 7: Generate Recommendations")
    print("=" * 70)

    batman = BatmanTesting()

    # Mock results with issues
    mock_results = {
        'elements_tested': 15,
        'tests_passed': 10,
        'tests_failed': 5,
        'accessibility_regressions': 3,
        'test_details': [
            {
                'category': 'buttons',
                'tests_failed': 2,
                'failures': [
                    {'element': 'btn_1', 'error': 'Not clickable'},
                    {'element': 'btn_2', 'error': 'Missing ARIA label'}
                ]
            }
        ]
    }

    recommendations = batman._generate_batman_recommendations(mock_results)

    assert isinstance(recommendations, list), "Should return list of recommendations"
    assert len(recommendations) > 0, "Should generate at least one recommendation"

    # Check recommendation structure
    for rec in recommendations:
        assert 'priority' in rec, "Recommendation should have priority"
        assert 'area' in rec, "Recommendation should have area"
        assert 'issue' in rec, "Recommendation should have issue description"
        assert 'recommendation' in rec, "Recommendation should have recommendation"
        assert 'batman_says' in rec, "Recommendation should have batman_says"

    print(f"✅ PASSED: Generated {len(recommendations)} recommendations")
    for i, rec in enumerate(recommendations[:3], 1):  # Show first 3
        print(f"   {i}. [{rec['priority']}] {rec['issue']}")

    return True


def test_keyboard_navigation():
    """Test 8: Keyboard navigation testing."""
    print("\n" + "=" * 70)
    print("Test 8: Keyboard Navigation Testing")
    print("=" * 70)

    batman = BatmanTesting()

    # Mock elements for keyboard navigation
    mock_elements = [
        {'uid': 'btn_1', 'type': 'button', 'tabindex': '0'},
        {'uid': 'link_1', 'type': 'link', 'tabindex': '0'},
        {'uid': 'input_1', 'type': 'textbox', 'tabindex': '0'}
    ]

    # Mock MCP tools with keyboard support
    keyboard_events = []
    def mock_keyboard(key, **kwargs):
        keyboard_events.append(key)
        return {'success': True, 'key': key}

    mock_mcp_tools = {
        'keyboard': mock_keyboard,
        'take_snapshot': lambda: {'focused_element': mock_elements[0]['uid']},
        'list_console': lambda: []
    }

    results = batman._test_keyboard_navigation(mock_elements, mock_mcp_tools)

    assert 'test_type' in results, "Should have test_type"
    assert results['test_type'] == 'Keyboard Navigation', "test_type should be 'Keyboard Navigation'"
    assert 'focusable_elements' in results, "Should have focusable_elements count"
    assert results['focusable_elements'] == 3, f"Should find 3 focusable elements, found {results['focusable_elements']}"

    print(f"✅ PASSED: Keyboard navigation testing completed")
    print(f"   Focusable elements: {results['focusable_elements']}")

    return True


def test_focus_management():
    """Test 9: Focus management testing."""
    print("\n" + "=" * 70)
    print("Test 9: Focus Management Testing")
    print("=" * 70)

    batman = BatmanTesting()

    # Mock elements for focus testing
    mock_elements = [
        {'uid': 'modal_btn', 'type': 'button', 'text': 'Open Modal'},
        {'uid': 'modal_close', 'type': 'button', 'text': 'Close'},
        {'uid': 'modal_input', 'type': 'textbox', 'name': 'Search'}
    ]

    # Mock MCP tools
    focus_events = []
    def mock_click(uid, **kwargs):
        focus_events.append(f"click:{uid}")
        return {'success': True}

    mock_mcp_tools = {
        'click': mock_click,
        'take_snapshot': lambda: {'focused_element': 'modal_input'},
        'list_console': lambda: []
    }

    results = batman._test_focus_management(mock_elements, mock_mcp_tools)

    assert 'test_type' in results, "Should have test_type"
    assert results['test_type'] == 'Focus Management', "test_type should be 'Focus Management'"
    assert 'elements_tested' in results, "Should have elements_tested count"
    assert results['elements_tested'] == 3, f"Should test 3 elements, tested {results['elements_tested']}"
    assert 'focus_visible' in results, "Should have focus_visible count"

    print(f"✅ PASSED: Focus management testing completed")
    print(f"   Elements tested: {results['elements_tested']}")
    print(f"   Focus visible: {results['focus_visible']}")

    return True


def test_full_integration():
    """Test 10: Full integration test with all interactive elements."""
    print("\n" + "=" * 70)
    print("Test 10: Full Integration Test")
    print("=" * 70)

    batman = BatmanTesting()

    # Comprehensive mock page snapshot (as text string - Chrome DevTools format)
    mock_page_snapshot = """
uid=btn_submit button "Submit"
uid=btn_cancel button "Cancel"
uid=link_home link "Home"
uid=link_about link "About"
uid=input_email textbox value=""
uid=input_password textbox value=""
"""

    # Mock MCP tools with tracking
    test_events = []

    def mock_click(uid, **kwargs):
        test_events.append(f"click:{uid}")
        return {'success': True, 'uid': uid}

    def mock_fill(uid, value, **kwargs):
        test_events.append(f"fill:{uid}={value}")
        return {'success': True, 'uid': uid, 'value': value}

    def mock_snapshot():
        return {'elements': []}

    def mock_console():
        return []

    mock_mcp_tools = {
        'click': mock_click,
        'fill': mock_fill,
        'hover': lambda uid, **kwargs: {'success': True},
        'take_snapshot': mock_snapshot,
        'list_console': mock_console
    }

    # Run full test
    results = batman.test_all_interactive_elements(mock_page_snapshot, mock_mcp_tools)

    assert results['interactive_testing'], "Should have interactive_testing flag"
    assert 'elements_tested' in results, "Should have elements_tested count"
    assert results['elements_tested'] >= 6, f"Should test at least 6 elements, tested {results['elements_tested']}"
    assert 'tests_passed' in results, "Should have tests_passed count"
    assert 'tests_failed' in results, "Should have tests_failed count"
    assert 'test_details' in results, "Should have test_details"
    assert len(results['test_details']) > 0, "Should have at least one test detail"

    print(f"\n✅ PASSED: Full integration test successful")
    print(f"   Elements Tested: {results['elements_tested']}")
    print(f"   Tests Passed: {results['tests_passed']}")
    print(f"   Tests Failed: {results['tests_failed']}")
    print(f"   Test Events: {len(test_events)}")

    return True


def run_all_tests():
    """Run complete test suite."""
    print("\n🦇 Batman Testing - Test Suite")
    print("=" * 70)
    print("Testing Interactive Element Testing Capabilities")
    print("=" * 70)

    tests = [
        ("Initialization", test_batman_initialization),
        ("Extract Interactive Elements", test_extract_interactive_elements),
        ("Button Testing", test_button_testing),
        ("Link Testing", test_link_testing),
        ("Input Testing", test_input_testing),
        ("Batman Score Calculation", test_batman_score_calculation),
        ("Generate Recommendations", test_generate_recommendations),
        ("Keyboard Navigation", test_keyboard_navigation),
        ("Focus Management", test_focus_management),
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
        print("\n🎉 ALL TESTS PASSED! Batman is ready to fight bugs!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Debug required.")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
