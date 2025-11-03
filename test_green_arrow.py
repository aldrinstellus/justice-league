#!/usr/bin/env python3
"""
🏹 GREEN ARROW - QA Testing Test Suite
=======================================

Tests for comprehensive quality assurance and testing capabilities.

Author: Justice League
Created: October 23, 2025
"""

import sys
import os
from pathlib import Path
import tempfile

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.justice_league.green_arrow_testing import GreenArrowTesting


def test_green_arrow_initialization():
    """Test 1: Green Arrow testing arsenal initialization."""
    print("\n" + "=" * 70)
    print("Test 1: Green Arrow Testing Arsenal Initialization")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='ga_testing_')
    ga = GreenArrowTesting(test_results_dir=temp_dir)

    assert ga is not None, "Green Arrow should initialize"
    assert hasattr(ga, 'test_justice_league'), "Should have test_justice_league method"
    assert hasattr(ga, '_fire_standard_arrow'), "Should have _fire_standard_arrow method"
    assert hasattr(ga, '_fire_net_arrow'), "Should have _fire_net_arrow method"
    assert hasattr(ga, '_fire_fire_arrow'), "Should have _fire_fire_arrow method"
    assert hasattr(ga, '_fire_explosive_arrow'), "Should have _fire_explosive_arrow method"

    # Check quiver (arrow types)
    assert hasattr(ga, 'quiver'), "Should have quiver"
    assert 'standard' in ga.quiver, "Should have standard arrows"
    assert 'explosive' in ga.quiver, "Should have explosive arrows"
    assert 'fire' in ga.quiver, "Should have fire arrows"
    assert 'net' in ga.quiver, "Should have net arrows"

    assert ga.test_results_dir == Path(temp_dir), "Should set test results directory"
    assert ga.test_results_dir.exists(), "Test results directory should exist"

    print("✅ PASSED: Green Arrow initialized successfully")
    print(f"   Test Results Directory: {ga.test_results_dir}")
    print(f"   Arrow Types in Quiver: {len(ga.quiver)}")
    return True


def test_fire_standard_arrow():
    """Test 2: Fire standard arrow (basic tests)."""
    print("\n" + "=" * 70)
    print("Test 2: Fire Standard Arrow - Basic Tests")
    print("=" * 70)

    ga = GreenArrowTesting()

    result = ga._fire_standard_arrow()

    # Actual structure: total, passed, failed, details, success_rate
    assert 'total' in result, "Should have total"
    assert 'passed' in result, "Should have passed"
    assert 'failed' in result, "Should have failed"
    assert 'details' in result, "Should have details"
    assert 'success_rate' in result, "Should have success_rate"

    print("✅ PASSED: Standard arrow fired successfully")
    print(f"   Total Tests: {result['total']}")
    print(f"   Passed: {result['passed']}")
    print(f"   Success Rate: {result['success_rate']:.1f}%")
    return True


def test_fire_net_arrow():
    """Test 3: Fire net arrow (integration tests)."""
    print("\n" + "=" * 70)
    print("Test 3: Fire Net Arrow - Integration Tests")
    print("=" * 70)

    ga = GreenArrowTesting()

    result = ga._fire_net_arrow()

    # Actual structure: total, passed, failed, details, success_rate
    assert 'total' in result, "Should have total"
    assert 'passed' in result, "Should have passed"
    assert 'failed' in result, "Should have failed"
    assert 'details' in result, "Should have details"
    assert 'success_rate' in result, "Should have success_rate"

    print("✅ PASSED: Net arrow fired successfully")
    print(f"   Total Tests: {result['total']}")
    print(f"   Passed: {result['passed']}")
    print(f"   Success Rate: {result['success_rate']:.1f}%")
    return True


def test_fire_fire_arrow():
    """Test 4: Fire fire arrow (performance tests)."""
    print("\n" + "=" * 70)
    print("Test 4: Fire Fire Arrow - Performance Tests")
    print("=" * 70)

    ga = GreenArrowTesting()

    result = ga._fire_fire_arrow()

    # Actual structure: total, passed, failed, details, success_rate, benchmarks (optional)
    assert 'total' in result, "Should have total"
    assert 'passed' in result, "Should have passed"
    assert 'failed' in result, "Should have failed"
    assert 'details' in result, "Should have details"
    assert 'success_rate' in result, "Should have success_rate"

    print("✅ PASSED: Fire arrow fired successfully")
    print(f"   Total Tests: {result['total']}")
    print(f"   Passed: {result['passed']}")
    print(f"   Success Rate: {result['success_rate']:.1f}%")
    return True


def test_fire_explosive_arrow():
    """Test 5: Fire explosive arrow (stress tests)."""
    print("\n" + "=" * 70)
    print("Test 5: Fire Explosive Arrow - Stress Tests")
    print("=" * 70)

    ga = GreenArrowTesting()

    result = ga._fire_explosive_arrow()

    # Actual structure: total, passed, failed, details
    assert 'total' in result, "Should have total"
    assert 'passed' in result, "Should have passed"
    assert 'failed' in result, "Should have failed"
    assert 'details' in result, "Should have details"

    print("✅ PASSED: Explosive arrow fired successfully")
    print(f"   Total Tests: {result['total']}")
    print(f"   Passed: {result['passed']}")
    return True


def test_fire_smoke_arrow():
    """Test 6: Fire smoke arrow (edge case tests)."""
    print("\n" + "=" * 70)
    print("Test 6: Fire Smoke Arrow - Edge Case Tests")
    print("=" * 70)

    ga = GreenArrowTesting()

    result = ga._fire_smoke_arrow()

    # Actual structure: total, passed, failed, details
    assert 'total' in result, "Should have total"
    assert 'passed' in result, "Should have passed"
    assert 'failed' in result, "Should have failed"
    assert 'details' in result, "Should have details"

    print("✅ PASSED: Smoke arrow fired successfully")
    print(f"   Total Tests: {result['total']}")
    print(f"   Passed: {result['passed']}")
    return True


def test_fire_freeze_arrow():
    """Test 7: Fire freeze arrow (snapshot tests)."""
    print("\n" + "=" * 70)
    print("Test 7: Fire Freeze Arrow - Snapshot Tests")
    print("=" * 70)

    ga = GreenArrowTesting()

    result = ga._fire_freeze_arrow()

    # Actual structure: total, passed, failed, details
    assert 'total' in result, "Should have total"
    assert 'passed' in result, "Should have passed"
    assert 'failed' in result, "Should have failed"
    assert 'details' in result, "Should have details"

    print("✅ PASSED: Freeze arrow fired successfully")
    print(f"   Total Tests: {result['total']}")
    print(f"   Passed: {result['passed']}")
    return True


def test_fire_tracker_arrow():
    """Test 8: Fire tracker arrow (coverage analysis)."""
    print("\n" + "=" * 70)
    print("Test 8: Fire Tracker Arrow - Coverage Analysis")
    print("=" * 70)

    ga = GreenArrowTesting()

    result = ga._fire_tracker_arrow()

    # Actual structure: total, passed, failed, details
    assert 'total' in result, "Should have total"
    assert 'passed' in result, "Should have passed"
    assert 'failed' in result, "Should have failed"
    assert 'details' in result, "Should have details"

    print("✅ PASSED: Tracker arrow fired successfully")
    print(f"   Total Tests: {result['total']}")
    print(f"   Passed: {result['passed']}")
    return True


def test_calculate_test_score():
    """Test 9: Calculate overall test score."""
    print("\n" + "=" * 70)
    print("Test 9: Calculate Test Score")
    print("=" * 70)

    ga = GreenArrowTesting()

    # High quality test results (actual structure uses 'total' and 'passed')
    high_quality_results = {
        'test_results': {
            'basic': {
                'total': 100,
                'passed': 98,
                'failed': 2
            },
            'integration': {
                'total': 10,
                'passed': 10,
                'failed': 0
            },
            'performance': {
                'total': 5,
                'passed': 5,
                'failed': 0
            }
        }
    }

    score_high = ga._calculate_test_score(high_quality_results)

    assert 'score' in score_high, "Should have score"
    assert 'status' in score_high, "Should have status"
    assert 'verdict' in score_high, "Should have verdict"
    assert 'grade' in score_high, "Should have grade"
    assert 'total_tests' in score_high, "Should have total_tests"
    assert 'passed_tests' in score_high, "Should have passed_tests"
    assert 'failed_tests' in score_high, "Should have failed_tests"
    assert score_high['score'] >= 95, f"High quality should score >= 95, got {score_high['score']}"

    # Low quality test results
    low_quality_results = {
        'test_results': {
            'basic': {
                'total': 100,
                'passed': 50,
                'failed': 50
            },
            'integration': {
                'total': 10,
                'passed': 3,
                'failed': 7
            }
        }
    }

    score_low = ga._calculate_test_score(low_quality_results)
    assert score_low['score'] < 60, f"Low quality should score < 60, got {score_low['score']}"

    print("✅ PASSED: Test score calculation works")
    print(f"   High Quality: {score_high['score']:.1f}/100 ({score_high['status']})")
    print(f"   Low Quality: {score_low['score']:.1f}/100 ({score_low['status']})")
    return True


def test_full_justice_league_testing():
    """Test 10: Full Justice League testing suite."""
    print("\n" + "=" * 70)
    print("Test 10: Full Justice League Testing")
    print("=" * 70)

    ga = GreenArrowTesting()

    # Run comprehensive test suite
    test_scenarios = ['basic', 'integration', 'performance']
    result = ga.test_justice_league(test_scenarios)

    # Validate top-level structure
    assert 'hero' in result, "Should identify hero"
    assert result['hero'] == '🏹 Green Arrow - Precision Tester', "Should be Green Arrow"
    assert 'timestamp' in result, "Should have timestamp"
    assert 'test_scenarios' in result, "Should have test_scenarios"
    assert result['test_scenarios'] == test_scenarios, "Test scenarios should match"

    # Check test results
    assert 'test_results' in result, "Should have test_results"
    test_results = result['test_results']

    assert 'basic' in test_results, "Should have basic test results"
    assert 'integration' in test_results, "Should have integration test results"
    assert 'performance' in test_results, "Should have performance test results"

    # Check test score
    assert 'test_score' in result, "Should have test_score"
    score = result['test_score']
    assert 'score' in score, "Should have score value"
    assert 'status' in score, "Should have status"
    assert 'verdict' in score, "Should have verdict"
    assert 'grade' in score, "Should have grade"
    assert 'total_tests' in score, "Should have total_tests"
    assert 'passed_tests' in score, "Should have passed_tests"
    assert 'failed_tests' in score, "Should have failed_tests"
    assert 0 <= score['score'] <= 100, f"Score should be 0-100, got {score['score']}"

    # Check test report
    assert 'test_report' in result, "Should have test_report"
    report = result['test_report']
    assert 'generated_at' in report, "Should have generated_at"
    assert 'test_scenarios_run' in report, "Should have test_scenarios_run"
    assert 'overall_score' in report, "Should have overall_score"
    assert 'overall_status' in report, "Should have overall_status"
    assert 'summary' in report, "Should have summary"
    assert 'green_arrow_says' in report, "Should have green_arrow_says"

    # Check overall status (uses test_score['status'] not 'passed'/'failed')
    assert 'overall_status' in result, "Should have overall_status"

    print("\n✅ PASSED: Full Justice League testing successful")
    print(f"   Test Score: {score['score']:.1f}/100")
    print(f"   Status: {score['status']}")
    print(f"   Overall: {result['overall_status']}")
    print(f"   Total Tests: {score['total_tests']}")
    return True


def run_all_tests():
    """Run complete test suite."""
    print("\n🏹 Green Arrow - QA Testing Test Suite")
    print("=" * 70)
    print("Testing Quality Assurance and Testing Capabilities")
    print("=" * 70)

    tests = [
        ("Initialization", test_green_arrow_initialization),
        ("Fire Standard Arrow", test_fire_standard_arrow),
        ("Fire Net Arrow", test_fire_net_arrow),
        ("Fire Fire Arrow", test_fire_fire_arrow),
        ("Fire Explosive Arrow", test_fire_explosive_arrow),
        ("Fire Smoke Arrow", test_fire_smoke_arrow),
        ("Fire Freeze Arrow", test_fire_freeze_arrow),
        ("Fire Tracker Arrow", test_fire_tracker_arrow),
        ("Calculate Test Score", test_calculate_test_score),
        ("Full Justice League Testing", test_full_justice_league_testing),
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
        print("\n🎉 ALL TESTS PASSED! Green Arrow never misses!")
        print("🏹 You have NOT failed this test suite!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review.")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
