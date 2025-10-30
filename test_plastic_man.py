#!/usr/bin/env python3
"""
🎨 PLASTIC MAN - Responsive Design Test Suite
===============================================

Tests for responsive design and multi-device testing capabilities.

Author: Justice League
Created: October 23, 2025
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.justice_league.plastic_man_responsive import PlasticManResponsive


def test_plastic_man_initialization():
    """Test 1: Plastic Man responsive testing initialization."""
    print("\n" + "=" * 70)
    print("Test 1: Plastic Man Responsive Testing Initialization")
    print("=" * 70)

    pm = PlasticManResponsive()

    assert pm is not None, "Plastic Man should initialize"
    assert hasattr(pm, 'test_all_breakpoints'), "Should have test_all_breakpoints method"
    assert hasattr(pm, '_elastic_stretch_test'), "Should have _elastic_stretch_test method"
    assert hasattr(pm, '_shapeshift_device_test'), "Should have _shapeshift_device_test method"
    assert hasattr(pm, '_malleable_viewport_test'), "Should have _malleable_viewport_test method"
    assert hasattr(pm, '_flexible_orientation_test'), "Should have _flexible_orientation_test method"
    assert hasattr(pm, '_extensible_touch_target_test'), "Should have _extensible_touch_target_test method"

    # Check breakpoints
    assert hasattr(pm, 'BREAKPOINTS'), "Should have BREAKPOINTS"
    assert 'mobile' in pm.BREAKPOINTS, "Should have mobile breakpoint"
    assert 'tablet_portrait' in pm.BREAKPOINTS, "Should have tablet breakpoint"
    assert 'desktop' in pm.BREAKPOINTS, "Should have desktop breakpoint"

    # Check minimum touch target size
    assert pm.MIN_TOUCH_TARGET_SIZE == 44, "Should have 44px min touch target (WCAG AAA)"

    print("✅ PASSED: Plastic Man initialized successfully")
    print(f"   Breakpoints Available: {len(pm.BREAKPOINTS)}")
    print(f"   Min Touch Target Size: {pm.MIN_TOUCH_TARGET_SIZE}px")
    return True


def test_breakpoints_configuration():
    """Test 2: Breakpoint configuration and definitions."""
    print("\n" + "=" * 70)
    print("Test 2: Breakpoint Configuration")
    print("=" * 70)

    pm = PlasticManResponsive()

    # Validate all breakpoints have required fields
    for bp_name, bp_data in pm.BREAKPOINTS.items():
        assert 'width' in bp_data, f"{bp_name} should have width"
        assert 'height' in bp_data, f"{bp_name} should have height"
        assert 'label' in bp_data, f"{bp_name} should have label"
        assert bp_data['width'] > 0, f"{bp_name} width should be positive"
        assert bp_data['height'] > 0, f"{bp_name} height should be positive"

    # Check specific breakpoints
    assert pm.BREAKPOINTS['mobile']['width'] == 375, "Mobile width should be 375px"
    assert pm.BREAKPOINTS['desktop']['width'] == 1920, "Desktop width should be 1920px"
    assert pm.BREAKPOINTS['desktop_4k']['width'] == 3840, "4K width should be 3840px"

    # Mobile-first approach: smallest should be smartwatch or mobile_small
    widths = [bp['width'] for bp in pm.BREAKPOINTS.values()]
    assert min(widths) <= 375, "Should support small mobile devices"

    print("✅ PASSED: All breakpoints configured correctly")
    print(f"   Total Breakpoints: {len(pm.BREAKPOINTS)}")
    print(f"   Smallest Width: {min(widths)}px")
    print(f"   Largest Width: {max(widths)}px")
    return True


def test_elastic_stretch_test():
    """Test 3: Elastic stretch test (breakpoint testing)."""
    print("\n" + "=" * 70)
    print("Test 3: Elastic Stretch Test - Breakpoint Testing")
    print("=" * 70)

    pm = PlasticManResponsive()

    # Mock MCP tools (minimal implementation)
    mock_mcp_tools = {
        'resize_page': lambda width, height: True,
        'take_snapshot': lambda: {'snapshot': 'data'},
        'evaluate_script': lambda function: False  # No horizontal scroll
    }

    result = pm._elastic_stretch_test('mobile', mock_mcp_tools)

    # Validate structure
    assert 'breakpoint' in result, "Should have breakpoint"
    assert result['breakpoint'] == 'mobile', "Should test mobile breakpoint"
    assert 'dimensions' in result, "Should have dimensions"
    assert 'label' in result, "Should have label"
    assert 'issues' in result, "Should have issues list"
    assert 'passed' in result, "Should have passed boolean"

    # Validate data types
    assert isinstance(result['issues'], list), "Issues should be a list"
    assert isinstance(result['passed'], bool), "Passed should be boolean"

    print("✅ PASSED: Elastic stretch test works")
    print(f"   Breakpoint: {result['breakpoint']}")
    print(f"   Dimensions: {result['dimensions']}")
    print(f"   Passed: {result['passed']}")
    return True


def test_shapeshift_device_test():
    """Test 4: Shape-shifting device test (device features)."""
    print("\n" + "=" * 70)
    print("Test 4: Shape-shifting Device Test")
    print("=" * 70)

    pm = PlasticManResponsive()

    # Mock MCP tools
    mock_mcp_tools = {
        'evaluate_script': lambda function: True  # Simulate touch-enabled device
    }

    result = pm._shapeshift_device_test(mock_mcp_tools)

    # Validate structure
    assert 'devices_tested' in result, "Should have devices_tested"
    assert 'touch_enabled' in result, "Should have touch_enabled"
    assert 'hover_supported' in result, "Should have hover_supported"
    assert 'pointer_fine' in result, "Should have pointer_fine"
    assert 'issues' in result, "Should have issues"

    # Validate data types
    assert isinstance(result['devices_tested'], list), "devices_tested should be list"
    assert isinstance(result['touch_enabled'], bool), "touch_enabled should be boolean"
    assert isinstance(result['issues'], list), "issues should be list"

    print("✅ PASSED: Shape-shifting device test works")
    print(f"   Touch Enabled: {result['touch_enabled']}")
    print(f"   Hover Supported: {result['hover_supported']}")
    print(f"   Pointer Fine: {result['pointer_fine']}")
    return True


def test_malleable_viewport_test():
    """Test 5: Malleable viewport test (viewport meta tag validation)."""
    print("\n" + "=" * 70)
    print("Test 5: Malleable Viewport Test")
    print("=" * 70)

    pm = PlasticManResponsive()

    # Test with good viewport
    good_viewport_tools = {
        'evaluate_script': lambda function: 'width=device-width, initial-scale=1'
    }

    result_good = pm._malleable_viewport_test(good_viewport_tools)

    assert 'viewport_meta_present' in result_good, "Should have viewport_meta_present"
    assert 'viewport_content' in result_good, "Should have viewport_content"
    assert 'issues' in result_good, "Should have issues"
    assert 'recommendations' in result_good, "Should have recommendations"

    assert result_good['viewport_meta_present'] is True, "Good viewport should be detected"
    assert len(result_good['issues']) == 0, "Good viewport should have no issues"

    # Test with bad viewport (user-scalable=no)
    bad_viewport_tools = {
        'evaluate_script': lambda function: 'width=device-width, user-scalable=no'
    }

    result_bad = pm._malleable_viewport_test(bad_viewport_tools)

    assert len(result_bad['issues']) > 0, "Bad viewport should have issues"
    assert any('zoom' in str(issue).lower() for issue in result_bad['issues']), "Should detect zoom restriction"

    print("✅ PASSED: Viewport testing works")
    print(f"   Good Viewport Issues: {len(result_good['issues'])}")
    print(f"   Bad Viewport Issues: {len(result_bad['issues'])}")
    return True


def test_flexible_orientation_test():
    """Test 6: Flexible orientation test (portrait/landscape)."""
    print("\n" + "=" * 70)
    print("Test 6: Flexible Orientation Test")
    print("=" * 70)

    pm = PlasticManResponsive()

    # Mock MCP tools
    mock_mcp_tools = {
        'resize_page': lambda width, height: True
    }

    result = pm._flexible_orientation_test(mock_mcp_tools)

    # Validate structure
    assert 'orientations_tested' in result, "Should have orientations_tested"
    assert 'issues' in result, "Should have issues"
    assert 'supports_both_orientations' in result, "Should have supports_both_orientations"

    # Validate data types
    assert isinstance(result['orientations_tested'], list), "orientations_tested should be list"
    assert isinstance(result['supports_both_orientations'], bool), "supports_both_orientations should be boolean"

    # Should test both orientations
    assert len(result['orientations_tested']) == 2, "Should test 2 orientations"
    assert 'portrait' in result['orientations_tested'], "Should test portrait"
    assert 'landscape' in result['orientations_tested'], "Should test landscape"

    print("✅ PASSED: Orientation testing works")
    print(f"   Orientations Tested: {result['orientations_tested']}")
    print(f"   Supports Both: {result['supports_both_orientations']}")
    return True


def test_extensible_touch_target_test():
    """Test 7: Extensible touch target test (touch target sizes)."""
    print("\n" + "=" * 70)
    print("Test 7: Extensible Touch Target Test")
    print("=" * 70)

    pm = PlasticManResponsive()

    # Mock with good touch targets
    good_targets_tools = {
        'evaluate_script': lambda function: {
            'total': 10,
            'smallCount': 0,
            'examples': []
        }
    }

    result_good = pm._extensible_touch_target_test(good_targets_tools)

    assert 'interactive_elements_checked' in result_good, "Should have interactive_elements_checked"
    assert 'too_small_targets' in result_good, "Should have too_small_targets"
    assert 'issues' in result_good, "Should have issues"
    assert 'passed' in result_good, "Should have passed"

    assert result_good['interactive_elements_checked'] == 10, "Should check 10 elements"
    assert result_good['too_small_targets'] == 0, "Should have 0 small targets"
    assert result_good['passed'] is True, "Should pass with good targets"
    assert len(result_good['issues']) == 0, "Should have no issues"

    # Mock with small touch targets
    bad_targets_tools = {
        'evaluate_script': lambda function: {
            'total': 10,
            'smallCount': 3,
            'examples': [
                {'tag': 'BUTTON', 'width': 30, 'height': 30, 'text': 'Close'}
            ]
        }
    }

    result_bad = pm._extensible_touch_target_test(bad_targets_tools)

    assert result_bad['too_small_targets'] == 3, "Should detect 3 small targets"
    assert result_bad['passed'] is False, "Should fail with small targets"
    assert len(result_bad['issues']) > 0, "Should have issues"

    print("✅ PASSED: Touch target testing works")
    print(f"   Good Targets: {result_good['interactive_elements_checked']} checked, {result_good['too_small_targets']} small")
    print(f"   Bad Targets: {result_bad['interactive_elements_checked']} checked, {result_bad['too_small_targets']} small")
    return True


def test_calculate_plastic_man_score():
    """Test 8: Calculate Plastic Man responsive design score."""
    print("\n" + "=" * 70)
    print("Test 8: Calculate Plastic Man Score")
    print("=" * 70)

    pm = PlasticManResponsive()

    # Perfect responsive design
    perfect_results = {
        'breakpoint_results': {
            'mobile': {'passed': True},
            'tablet_portrait': {'passed': True},
            'desktop': {'passed': True}
        },
        'viewport_issues': [],
        'touch_target_issues': [],
        'device_specific': {'issues': []},
        'breakpoints_tested': ['mobile', 'tablet_portrait', 'desktop']
    }

    score_perfect = pm._calculate_plastic_man_score(perfect_results)

    assert 'score' in score_perfect, "Should have score"
    assert 'grade' in score_perfect, "Should have grade"
    assert 'verdict' in score_perfect, "Should have verdict"
    assert 'breakpoints_tested' in score_perfect, "Should have breakpoints_tested"
    assert 'total_issues' in score_perfect, "Should have total_issues"

    assert score_perfect['score'] == 100, f"Perfect design should score 100, got {score_perfect['score']}"
    assert score_perfect['grade'] == "S+ (Perfect Elasticity)", "Perfect design should be S+ grade"
    assert score_perfect['total_issues'] == 0, "Perfect design should have 0 issues"

    # Poor responsive design
    poor_results = {
        'breakpoint_results': {
            'mobile': {'passed': False},
            'tablet_portrait': {'passed': False}
        },
        'viewport_issues': [{'issue': 'missing viewport'}, {'issue': 'no zoom'}],
        'touch_target_issues': [{'issue': 'small targets'}],
        'device_specific': {'issues': [{'issue': 'hover-only'}]},
        'breakpoints_tested': ['mobile', 'tablet_portrait']
    }

    score_poor = pm._calculate_plastic_man_score(poor_results)

    assert score_poor['score'] < 70, f"Poor design should score < 70, got {score_poor['score']}"
    assert score_poor['total_issues'] > 0, "Poor design should have issues"

    print("✅ PASSED: Scoring works correctly")
    print(f"   Perfect: {score_perfect['score']}/100 ({score_perfect['grade']})")
    print(f"   Poor: {score_poor['score']:.1f}/100 ({score_poor['grade']})")
    return True


def test_generate_elastic_recommendations():
    """Test 9: Generate elastic recommendations."""
    print("\n" + "=" * 70)
    print("Test 9: Generate Elastic Recommendations")
    print("=" * 70)

    pm = PlasticManResponsive()

    # Results with issues
    results_with_issues = {
        'viewport_issues': [
            {'issue': 'Missing viewport', 'severity': 'critical'}
        ],
        'touch_target_analysis': {
            'too_small_targets': 5
        },
        'breakpoint_results': {
            'mobile': {'passed': False},
            'desktop': {'passed': True}
        },
        'device_specific': {
            'issues': [
                {'issue': 'Hover-only UI', 'severity': 'high', 'recommendation': 'Make tappable'}
            ]
        }
    }

    recommendations = pm._generate_elastic_recommendations(results_with_issues)

    assert isinstance(recommendations, list), "Should return list of recommendations"
    assert len(recommendations) > 0, "Should have recommendations for issues"

    # Check recommendation structure
    for rec in recommendations:
        assert 'priority' in rec, "Should have priority"
        assert 'area' in rec, "Should have area"
        assert 'issue' in rec, "Should have issue"
        assert 'recommendation' in rec, "Should have recommendation"
        assert 'plastic_man_says' in rec, "Should have plastic_man_says"

    # Results without issues
    perfect_results = {
        'viewport_issues': [],
        'touch_target_analysis': {'too_small_targets': 0},
        'breakpoint_results': {
            'mobile': {'passed': True},
            'desktop': {'passed': True}
        },
        'device_specific': {'issues': []}
    }

    recommendations_perfect = pm._generate_elastic_recommendations(perfect_results)

    assert len(recommendations_perfect) == 1, "Perfect results should have 1 recommendation"
    assert recommendations_perfect[0]['priority'] == 'low', "Perfect results should be low priority"

    print("✅ PASSED: Recommendation generation works")
    print(f"   With Issues: {len(recommendations)} recommendations")
    print(f"   Perfect: {len(recommendations_perfect)} recommendation")
    return True


def test_full_breakpoint_testing():
    """Test 10: Full breakpoint testing integration."""
    print("\n" + "=" * 70)
    print("Test 10: Full Breakpoint Testing Integration")
    print("=" * 70)

    pm = PlasticManResponsive()

    # Mock MCP tools
    mock_mcp_tools = {
        'resize_page': lambda width, height: True,
        'take_snapshot': lambda: {'snapshot': 'data'},
        'evaluate_script': lambda function: 'width=device-width, initial-scale=1' if 'viewport' in function else False
    }

    # Test subset of breakpoints
    test_scenarios = ['mobile', 'tablet_portrait', 'desktop']
    result = pm.test_all_breakpoints(mock_mcp_tools, test_scenarios)

    # Validate top-level structure
    assert 'hero' in result, "Should identify hero"
    assert result['hero'] == '🎨 Plastic Man - Responsive Design Specialist', "Should be Plastic Man"
    assert 'timestamp' in result, "Should have timestamp"
    assert 'breakpoints_tested' in result, "Should have breakpoints_tested"
    assert 'breakpoint_results' in result, "Should have breakpoint_results"
    assert 'responsive_issues' in result, "Should have responsive_issues"
    assert 'touch_target_issues' in result, "Should have touch_target_issues"
    assert 'viewport_issues' in result, "Should have viewport_issues"

    # Check all requested breakpoints were tested
    assert len(result['breakpoints_tested']) == 3, "Should test 3 breakpoints"
    assert 'mobile' in result['breakpoints_tested'], "Should test mobile"
    assert 'tablet_portrait' in result['breakpoints_tested'], "Should test tablet"
    assert 'desktop' in result['breakpoints_tested'], "Should test desktop"

    # Check device-specific tests
    assert 'device_specific' in result, "Should have device_specific"

    # Check viewport analysis
    assert 'viewport_analysis' in result, "Should have viewport_analysis"

    # Check orientation testing
    assert 'orientation_testing' in result, "Should have orientation_testing"

    # Check touch target analysis
    assert 'touch_target_analysis' in result, "Should have touch_target_analysis"

    # Check score
    assert 'plastic_man_score' in result, "Should have plastic_man_score"
    score = result['plastic_man_score']
    assert 'score' in score, "Should have score value"
    assert 'grade' in score, "Should have grade"
    assert 'verdict' in score, "Should have verdict"
    assert 0 <= score['score'] <= 100, f"Score should be 0-100, got {score['score']}"

    # Check recommendations
    assert 'recommendations' in result, "Should have recommendations"
    assert isinstance(result['recommendations'], list), "Recommendations should be list"

    print("\n✅ PASSED: Full breakpoint testing successful")
    print(f"   Breakpoints Tested: {len(result['breakpoints_tested'])}")
    print(f"   Responsive Score: {score['score']:.1f}/100")
    print(f"   Grade: {score['grade']}")
    print(f"   Recommendations: {len(result['recommendations'])}")
    return True


def run_all_tests():
    """Run complete test suite."""
    print("\n🎨 Plastic Man - Responsive Design Test Suite")
    print("=" * 70)
    print("Testing Responsive Design and Multi-Device Capabilities")
    print("=" * 70)

    tests = [
        ("Initialization", test_plastic_man_initialization),
        ("Breakpoints Configuration", test_breakpoints_configuration),
        ("Elastic Stretch Test", test_elastic_stretch_test),
        ("Shape-shifting Device Test", test_shapeshift_device_test),
        ("Malleable Viewport Test", test_malleable_viewport_test),
        ("Flexible Orientation Test", test_flexible_orientation_test),
        ("Extensible Touch Target Test", test_extensible_touch_target_test),
        ("Calculate Plastic Man Score", test_calculate_plastic_man_score),
        ("Generate Elastic Recommendations", test_generate_elastic_recommendations),
        ("Full Breakpoint Testing", test_full_breakpoint_testing),
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
        print("\n🎉 ALL TESTS PASSED! Plastic Man stretches perfectly!")
        print("🎨 Your responsive testing is flawless!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review.")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
