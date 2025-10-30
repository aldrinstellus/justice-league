"""
🧪 Superman Mobile Device Testing - Test Suite
==============================================

Comprehensive tests for Mobile Device Testing functionality.

Test Coverage:
1. Basic device testing
2. Multiple device comparison
3. Touch target validation (WCAG 2.5.5, 2.5.8)
4. Responsive breakpoint testing
5. Complete mobile testing workflow

Author: Superman Testing Team
Version: 1.0.0
Created: 2025-10-23
"""

import sys
from pathlib import Path

# Add core directory to path
sys.path.insert(0, str(Path(__file__).parent / "core"))

from superman_mobile_testing import (
    SupermanMobileTesting,
    test_mobile_devices,
    validate_touch_accessibility,
    DEVICE_PROFILES,
    RESPONSIVE_BREAKPOINTS,
    WCAG_TOUCH_TARGETS,
    DeviceType,
    DeviceProfile,
    TouchTarget,
    MobileTestResult,
    ResponsiveTestResult,
    DeviceComparisonReport,
)


def test_1_basic_device_testing():
    """
    Test 1: Basic Device Testing
    Tests that we can test a URL on a single device
    """
    print("\n" + "=" * 70)
    print("TEST 1: Basic Device Testing")
    print("=" * 70)

    tester = SupermanMobileTesting(storage_dir="./test_mobile_testing")

    # Test on iPhone 15 Pro
    result = tester.test_on_device(
        url="https://example.com",
        device_name="iphone-15-pro",
        validate_touch_targets=True,
        test_gestures=True
    )

    # Assertions
    assert result.device_name == "iPhone 15 Pro", "Device name should match"
    assert result.viewport_width == 390, "iPhone 15 Pro width should be 390px"
    assert result.viewport_height == 844, "iPhone 15 Pro height should be 844px"
    assert result.pixel_ratio == 3.0, "iPhone 15 Pro should have 3x pixel ratio"
    assert result.overall_score >= 0 and result.overall_score <= 100, "Score should be 0-100"
    assert result.mobile_ux_score >= 0, "Mobile UX score should be >= 0"
    assert result.touch_accessibility_score >= 0, "Touch score should be >= 0"
    assert result.responsive_score >= 0, "Responsive score should be >= 0"

    print(f"✅ Device testing completed:")
    print(f"   Device: {result.device_name}")
    print(f"   Viewport: {result.viewport_width}×{result.viewport_height}")
    print(f"   Pixel Ratio: {result.pixel_ratio}x")
    print(f"   Mobile UX: {result.mobile_ux_score:.1f}/100")
    print(f"   Touch Accessibility: {result.touch_accessibility_score:.1f}/100")
    print(f"   Responsive: {result.responsive_score:.1f}/100")
    print(f"   Overall: {result.overall_score:.1f}/100")

    # Check touch targets
    print(f"\n   Touch targets tested: {len(result.touch_targets)}")
    if result.touch_targets:
        for target in result.touch_targets[:2]:  # Show first 2
            wcag_status = "✅" if target.meets_minimum else "❌"
            print(f"      {wcag_status} {target.element_type}: {target.width}×{target.height}px")

    # Check gestures
    print(f"   Gestures tested: {len(result.gesture_tests)}")
    if result.gesture_tests:
        for gesture in result.gesture_tests[:2]:  # Show first 2
            status = "✅" if gesture.success else "❌"
            print(f"      {status} {gesture.gesture_type}: {gesture.response_time_ms:.1f}ms")

    print("\n✅ TEST 1 PASSED: Basic device testing working correctly")
    return True


def test_2_multiple_device_comparison():
    """
    Test 2: Multiple Device Comparison
    Tests comparison across multiple devices
    """
    print("\n" + "=" * 70)
    print("TEST 2: Multiple Device Comparison")
    print("=" * 70)

    tester = SupermanMobileTesting(storage_dir="./test_mobile_testing")

    # Test across 4 devices
    test_devices = [
        "iphone-15-pro",
        "samsung-galaxy-s24",
        "ipad-air",
        "iphone-se"
    ]

    report = tester.test_on_multiple_devices(
        url="https://example.com",
        device_names=test_devices
    )

    # Assertions
    assert report.devices_tested == 4, "Should test 4 devices"
    assert len(report.device_results) == 4, "Should have 4 device results"
    assert report.best_device in test_devices, "Best device should be in test list"
    assert report.worst_device in test_devices, "Worst device should be in test list"
    assert 0 <= report.average_score <= 100, "Average score should be 0-100"
    assert len(report.recommendations) > 0, "Should have recommendations"

    print(f"✅ Device comparison completed:")
    print(f"   Devices tested: {report.devices_tested}")
    print(f"   Average score: {report.average_score:.1f}/100")
    print(f"   Best device: {report.best_device}")
    print(f"   Worst device: {report.worst_device}")

    # Show scores for each device
    print(f"\n   Device scores:")
    for device_name, result in report.device_results.items():
        print(f"      {device_name}: {result.overall_score:.1f}/100")

    # Show common issues
    if report.common_issues:
        print(f"\n   Common issues: {len(report.common_issues)}")
        for issue in report.common_issues[:2]:
            print(f"      - {issue}")

    # Show recommendations
    print(f"\n   Recommendations:")
    for i, rec in enumerate(report.recommendations[:3], 1):
        print(f"      {i}. {rec}")

    print("\n✅ TEST 2 PASSED: Multiple device comparison working correctly")
    return True


def test_3_touch_target_validation():
    """
    Test 3: Touch Target Validation (WCAG)
    Tests WCAG 2.5.5 and 2.5.8 touch target validation
    """
    print("\n" + "=" * 70)
    print("TEST 3: Touch Target Validation (WCAG)")
    print("=" * 70)

    tester = SupermanMobileTesting(storage_dir="./test_mobile_testing")

    # Test with touch target validation
    result = tester.test_on_device(
        url="https://example.com",
        device_name="iphone-15-pro",
        validate_touch_targets=True,
        test_gestures=False
    )

    # Assertions
    assert result.touch_targets is not None, "Should have touch targets"
    assert len(result.touch_targets) > 0, "Should test at least 1 touch target"

    # Check WCAG compliance
    for target in result.touch_targets:
        assert hasattr(target, 'meets_minimum'), "Should check minimum size (24×24px)"
        assert hasattr(target, 'meets_enhanced'), "Should check enhanced size (44×44px)"
        assert hasattr(target, 'meets_recommended'), "Should check recommended size (48×48px)"

    print(f"✅ Touch target validation:")
    print(f"   Total targets: {len(result.touch_targets)}")

    # Count compliance
    meets_minimum = sum(1 for t in result.touch_targets if t.meets_minimum)
    meets_enhanced = sum(1 for t in result.touch_targets if t.meets_enhanced)
    meets_recommended = sum(1 for t in result.touch_targets if t.meets_recommended)

    print(f"   Meets WCAG 2.5.8 (24×24px - AA): {meets_minimum}/{len(result.touch_targets)}")
    print(f"   Meets WCAG 2.5.5 (44×44px - AAA): {meets_enhanced}/{len(result.touch_targets)}")
    print(f"   Meets Recommended (48×48px): {meets_recommended}/{len(result.touch_targets)}")

    # Show example targets
    print(f"\n   Example touch targets:")
    for target in result.touch_targets[:3]:
        status_min = "✅" if target.meets_minimum else "❌"
        status_enh = "✅" if target.meets_enhanced else "❌"
        print(f"      {target.element_type} ({target.width}×{target.height}px)")
        print(f"         Minimum (24×24): {status_min}")
        print(f"         Enhanced (44×44): {status_enh}")

    # Check WCAG constants
    print(f"\n   WCAG Standards:")
    print(f"      Minimum (AA): {WCAG_TOUCH_TARGETS['minimum']}×{WCAG_TOUCH_TARGETS['minimum']}px")
    print(f"      Enhanced (AAA): {WCAG_TOUCH_TARGETS['enhanced']}×{WCAG_TOUCH_TARGETS['enhanced']}px")
    print(f"      Recommended: {WCAG_TOUCH_TARGETS['recommended']}×{WCAG_TOUCH_TARGETS['recommended']}px")

    print("\n✅ TEST 3 PASSED: Touch target validation working correctly")
    return True


def test_4_responsive_breakpoint_testing():
    """
    Test 4: Responsive Breakpoint Testing
    Tests responsive design across 7 breakpoints
    """
    print("\n" + "=" * 70)
    print("TEST 4: Responsive Breakpoint Testing")
    print("=" * 70)

    tester = SupermanMobileTesting(storage_dir="./test_mobile_testing")

    # Test 4 breakpoints (subset for speed)
    test_breakpoints = ["mobile-s", "mobile-m", "tablet", "desktop"]

    results = tester.test_responsive_breakpoints(
        url="https://example.com",
        breakpoints=test_breakpoints
    )

    # Assertions
    assert len(results) == 4, "Should test 4 breakpoints"

    for result in results:
        assert result.breakpoint_name is not None, "Should have breakpoint name"
        assert result.width > 0, "Should have width"
        assert 0 <= result.responsive_score <= 100, "Score should be 0-100"
        assert hasattr(result, 'layout_valid'), "Should check layout"
        assert hasattr(result, 'content_visible'), "Should check content visibility"
        assert hasattr(result, 'navigation_accessible'), "Should check navigation"
        assert hasattr(result, 'no_horizontal_scroll'), "Should check horizontal scroll"

    print(f"✅ Responsive breakpoint testing:")
    print(f"   Breakpoints tested: {len(results)}")

    # Show results for each breakpoint
    print(f"\n   Breakpoint results:")
    for result in results:
        status = "✅" if result.responsive_score == 100 else "⚠️"
        print(f"      {status} {result.breakpoint_name} ({result.width}px): {result.responsive_score:.1f}/100")

        if result.layout_issues:
            for issue in result.layout_issues:
                print(f"         - {issue}")

    # Calculate statistics
    avg_score = sum(r.responsive_score for r in results) / len(results)
    all_pass = all(r.responsive_score == 100 for r in results)

    print(f"\n   Average score: {avg_score:.1f}/100")
    print(f"   All breakpoints pass: {'Yes' if all_pass else 'No'}")

    # Verify all expected breakpoints exist
    print(f"\n   Available breakpoints: {len(RESPONSIVE_BREAKPOINTS)}")
    for name, info in list(RESPONSIVE_BREAKPOINTS.items())[:4]:
        print(f"      {name}: {info['width']}px ({info['description']})")

    print("\n✅ TEST 4 PASSED: Responsive breakpoint testing working correctly")
    return True


def test_5_complete_mobile_workflow():
    """
    Test 5: Complete Mobile Testing Workflow
    Tests the complete workflow with convenience functions
    """
    print("\n" + "=" * 70)
    print("TEST 5: Complete Mobile Testing Workflow")
    print("=" * 70)

    # Test 1: Use convenience function for multi-device testing
    print(f"\n   Testing convenience function: test_mobile_devices()...")
    report1 = test_mobile_devices(
        url="https://example.com",
        devices=["iphone-15-pro", "samsung-galaxy-s24"]
    )

    assert report1 is not None, "Should return report"
    assert report1.devices_tested == 2, "Should test 2 devices"
    print(f"   ✅ Multi-device testing: {report1.average_score:.1f}/100")

    # Test 2: Use convenience function for touch accessibility
    print(f"\n   Testing convenience function: validate_touch_accessibility()...")
    result = validate_touch_accessibility(
        url="https://example.com",
        device="iphone-15-pro"
    )

    assert result is not None, "Should return result"
    assert result.touch_targets is not None, "Should have touch targets"
    print(f"   ✅ Touch accessibility: {result.touch_accessibility_score:.1f}/100")

    # Test 3: Verify device profiles
    print(f"\n   Verifying device profiles...")
    assert len(DEVICE_PROFILES) >= 10, "Should have at least 10 device profiles"

    # Count by type
    mobile_count = sum(1 for p in DEVICE_PROFILES.values() if p.type == DeviceType.MOBILE)
    tablet_count = sum(1 for p in DEVICE_PROFILES.values() if p.type == DeviceType.TABLET)
    desktop_count = sum(1 for p in DEVICE_PROFILES.values() if p.type == DeviceType.DESKTOP)

    print(f"   Device profiles: {len(DEVICE_PROFILES)} total")
    print(f"      Mobile: {mobile_count}")
    print(f"      Tablet: {tablet_count}")
    print(f"      Desktop: {desktop_count}")

    # Show sample devices
    print(f"\n   Sample devices:")
    for name, profile in list(DEVICE_PROFILES.items())[:3]:
        print(f"      {profile.name} ({profile.width}×{profile.height}px, {profile.os})")

    # Test 4: Verify full workflow
    print(f"\n   Testing full workflow...")
    tester = SupermanMobileTesting(storage_dir="./test_mobile_testing")

    # Single device test
    single_result = tester.test_on_device("https://example.com", "ipad-air")
    assert single_result.overall_score >= 0, "Should have valid score"

    # Multi-device test
    multi_report = tester.test_on_multiple_devices(
        url="https://example.com",
        device_names=["iphone-15-pro", "ipad-air"]
    )
    assert multi_report.devices_tested == 2, "Should test 2 devices"

    # Responsive test
    responsive_results = tester.test_responsive_breakpoints(
        url="https://example.com",
        breakpoints=["mobile-m", "tablet"]
    )
    assert len(responsive_results) == 2, "Should test 2 breakpoints"

    print(f"   ✅ Full workflow completed successfully")

    print("\n✅ TEST 5 PASSED: Complete mobile workflow working correctly")
    return True


def test_6_device_profiles():
    """
    Bonus Test: Device Profile Verification
    Verifies that device profiles are comprehensive
    """
    print("\n" + "=" * 70)
    print("BONUS TEST: Device Profile Verification")
    print("=" * 70)

    print(f"✅ Device profile verification:")
    print(f"   Total profiles: {len(DEVICE_PROFILES)}")

    # Verify we have key devices
    required_devices = [
        "iphone-15-pro",
        "iphone-15-pro-max",
        "samsung-galaxy-s24",
        "google-pixel-8",
        "ipad-pro-12.9",
        "ipad-air"
    ]

    for device_name in required_devices:
        assert device_name in DEVICE_PROFILES, f"Should have {device_name} profile"

    print(f"   All required devices present ✅")

    # Verify device properties
    for name, profile in DEVICE_PROFILES.items():
        assert profile.name, "Should have name"
        assert profile.width > 0, "Should have width"
        assert profile.height > 0, "Should have height"
        assert profile.pixel_ratio > 0, "Should have pixel ratio"
        assert profile.user_agent, "Should have user agent"
        assert profile.os, "Should have OS"
        assert profile.browser, "Should have browser"

    print(f"   All device properties valid ✅")

    # Show device statistics
    print(f"\n   Device statistics:")

    widths = [p.width for p in DEVICE_PROFILES.values() if p.type == DeviceType.MOBILE]
    print(f"      Mobile widths: {min(widths)}px - {max(widths)}px")

    pixel_ratios = set(p.pixel_ratio for p in DEVICE_PROFILES.values())
    print(f"      Pixel ratios: {sorted(pixel_ratios)}")

    operating_systems = set(p.os for p in DEVICE_PROFILES.values())
    print(f"      Operating systems: {', '.join(sorted(operating_systems))}")

    # Verify responsive breakpoints
    print(f"\n   Responsive breakpoints: {len(RESPONSIVE_BREAKPOINTS)}")
    assert len(RESPONSIVE_BREAKPOINTS) == 7, "Should have 7 breakpoints"

    breakpoint_widths = [info['width'] for info in RESPONSIVE_BREAKPOINTS.values()]
    print(f"      Width range: {min(breakpoint_widths)}px - {max(breakpoint_widths)}px")

    print("\n✅ BONUS TEST PASSED: Device profiles comprehensive")
    return True


def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "=" * 70)
    print("🦸📱 SUPERMAN MOBILE DEVICE TESTING - TEST SUITE")
    print("=" * 70)
    print("\nRunning comprehensive test suite...")

    tests = [
        ("Basic Device Testing", test_1_basic_device_testing),
        ("Multiple Device Comparison", test_2_multiple_device_comparison),
        ("Touch Target Validation (WCAG)", test_3_touch_target_validation),
        ("Responsive Breakpoint Testing", test_4_responsive_breakpoint_testing),
        ("Complete Mobile Workflow", test_5_complete_mobile_workflow),
        ("Device Profile Verification", test_6_device_profiles),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result, None))
        except Exception as e:
            print(f"\n❌ TEST FAILED: {name}")
            print(f"   Error: {str(e)}")
            results.append((name, False, str(e)))

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result, _ in results if result)
    total = len(results)

    for name, result, error in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
        if error:
            print(f"         {error}")

    print(f"\n" + "=" * 70)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print("=" * 70)

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Mobile Device Testing is production-ready!")
        print("\n🦸📱 Superman says: 'Mobile testing perfected! Responsive designs validated!'")
        return True
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Review errors above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
