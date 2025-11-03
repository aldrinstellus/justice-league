#!/usr/bin/env python3
"""
⚡ THE FLASH PERFORMANCE - Test Suite
======================================

Tests for performance profiling with Core Web Vitals analysis.

Author: Justice League
Created: October 23, 2025
"""

import sys
import os
from pathlib import Path
import tempfile
import shutil

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.justice_league.flash_performance import FlashPerformance


def test_flash_initialization():
    """Test 1: Flash Performance initialization."""
    print("\n" + "=" * 70)
    print("Test 1: Flash Performance Initialization")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='flash_test_')

    try:
        flash = FlashPerformance(baseline_dir=temp_dir)

        assert flash is not None, "Flash should initialize"
        assert hasattr(flash, 'profile_performance'), "Should have profile_performance method"
        assert hasattr(flash, '_extract_core_web_vitals'), "Should have _extract_core_web_vitals method"
        assert hasattr(flash, '_calculate_speed_score'), "Should have _calculate_speed_score method"
        assert hasattr(flash, '_check_performance_regression'), "Should have _check_performance_regression method"
        assert flash.baseline_dir == Path(temp_dir), f"Baseline dir should be {temp_dir}"
        assert flash.baseline_dir.exists(), "Baseline directory should exist"

        print(f"✅ PASSED: Flash initialized with baseline dir: {temp_dir}")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_extract_core_web_vitals():
    """Test 2: Extract Core Web Vitals from trace data."""
    print("\n" + "=" * 70)
    print("Test 2: Extract Core Web Vitals")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='flash_test_')

    try:
        flash = FlashPerformance(baseline_dir=temp_dir)

        # Mock trace data with good performance
        mock_trace_good = {
            'lcp': 2000,   # 2s - GOOD (< 2.5s)
            'fid': 50,     # 50ms - GOOD (< 100ms)
            'cls': 0.05,   # 0.05 - GOOD (< 0.1)
            'fcp': 1500,   # 1.5s - GOOD (< 1.8s)
            'tti': 3000,   # 3s - GOOD (< 3.8s)
            'tbt': 150     # 150ms - GOOD (< 200ms)
        }

        vitals = flash._extract_core_web_vitals(mock_trace_good)

        # Check all metrics extracted
        assert 'LCP' in vitals, "Should extract LCP"
        assert 'FID' in vitals, "Should extract FID"
        assert 'CLS' in vitals, "Should extract CLS"
        assert 'FCP' in vitals, "Should extract FCP"
        assert 'TTI' in vitals, "Should extract TTI"
        assert 'TBT' in vitals, "Should extract TBT"

        # Check LCP status
        assert vitals['LCP']['value'] == 2000, f"LCP should be 2000, got {vitals['LCP']['value']}"
        assert vitals['LCP']['status'] == 'good', f"LCP status should be 'good', got {vitals['LCP']['status']}"

        # Check CLS status (special case - lower is better)
        assert vitals['CLS']['value'] == 0.05, f"CLS should be 0.05, got {vitals['CLS']['value']}"
        assert vitals['CLS']['status'] == 'good', f"CLS status should be 'good', got {vitals['CLS']['status']}"

        # Test poor performance
        mock_trace_poor = {
            'lcp': 5000,   # 5s - POOR (> 4s)
            'fid': 400,    # 400ms - POOR (> 300ms)
            'cls': 0.3,    # 0.3 - POOR (> 0.25)
            'fcp': 4000,   # 4s - POOR (> 3s)
            'tti': 8000,   # 8s - POOR (> 7.3s)
            'tbt': 700     # 700ms - POOR (> 600ms)
        }

        vitals_poor = flash._extract_core_web_vitals(mock_trace_poor)
        assert vitals_poor['LCP']['status'] == 'poor', "LCP should be poor"
        assert vitals_poor['CLS']['status'] == 'poor', "CLS should be poor"

        print(f"✅ PASSED: Core Web Vitals extraction works correctly")
        print(f"   Good Performance: All 6 metrics = 'good'")
        print(f"   Poor Performance: All 6 metrics = 'poor'")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_calculate_speed_score():
    """Test 3: Calculate Flash Speed Score."""
    print("\n" + "=" * 70)
    print("Test 3: Calculate Flash Speed Score")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='flash_test_')

    try:
        flash = FlashPerformance(baseline_dir=temp_dir)

        # High quality performance (all good)
        high_quality_results = {
            'core_web_vitals': {
                'LCP': {'status': 'good'},
                'FID': {'status': 'good'},
                'CLS': {'status': 'good'},
                'FCP': {'status': 'good'},
                'TTI': {'status': 'good'},
                'TBT': {'status': 'good'}
            },
            'performance_insights': []
        }

        score_high = flash._calculate_speed_score(high_quality_results)

        assert score_high['score'] >= 90, f"High quality should score >= 90, got {score_high['score']}"
        assert 'S+' in score_high['grade'] or 'A' in score_high['grade'], f"Should get S+ or A grade, got {score_high['grade']}"
        assert score_high['core_vitals_passed'] == 6, f"Should pass all 6 vitals, got {score_high['core_vitals_passed']}"
        assert score_high['core_vitals_total'] == 6, "Should have 6 total vitals"
        assert 'LIGHTNING FAST' in score_high['verdict'] or 'Very Fast' in score_high['verdict'], "Should have fast verdict"

        # Low quality performance (all poor)
        low_quality_results = {
            'core_web_vitals': {
                'LCP': {'status': 'poor'},
                'FID': {'status': 'poor'},
                'CLS': {'status': 'poor'},
                'FCP': {'status': 'poor'},
                'TTI': {'status': 'poor'},
                'TBT': {'status': 'poor'}
            },
            'performance_insights': [
                {'severity': 'critical', 'name': 'Issue 1'},
                {'severity': 'critical', 'name': 'Issue 2'},
                {'severity': 'warning', 'name': 'Issue 3'}
            ]
        }

        score_low = flash._calculate_speed_score(low_quality_results)
        assert score_low['score'] < 50, f"Low quality should score < 50, got {score_low['score']}"
        assert score_low['core_vitals_passed'] == 0, "Should pass 0 vitals"

        print(f"✅ PASSED: Flash Speed Score calculation works")
        print(f"   High Performance: {score_high['score']}/100 ({score_high['grade']})")
        print(f"   Low Performance:  {score_low['score']}/100 ({score_low['grade']})")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_store_performance_baseline():
    """Test 4: Store performance baseline."""
    print("\n" + "=" * 70)
    print("Test 4: Store Performance Baseline")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='flash_test_')

    try:
        flash = FlashPerformance(baseline_dir=temp_dir)

        # Mock performance results
        mock_results = {
            'timestamp': '2025-10-23T12:00:00',
            'url': 'https://example.com',
            'core_web_vitals': {
                'LCP': {'value': 2000, 'status': 'good'}
            },
            'flash_speed_score': {
                'score': 95.0,
                'grade': 'S+',
                'verdict': '⚡ LIGHTNING FAST'
            }
        }

        # Store baseline
        flash._store_performance_baseline('homepage-test', mock_results)

        # Verify baseline file exists
        baseline_path = flash.baseline_dir / 'homepage-test_baseline.json'
        assert baseline_path.exists(), f"Baseline file should exist at {baseline_path}"

        # Load and verify baseline content
        import json
        with open(baseline_path, 'r') as f:
            baseline = json.load(f)

        assert baseline['test_name'] == 'homepage-test', "Test name should match"
        assert baseline['timestamp'] == '2025-10-23T12:00:00', "Timestamp should match"
        assert baseline['url'] == 'https://example.com', "URL should match"
        assert 'core_web_vitals' in baseline, "Should store core web vitals"
        assert 'flash_speed_score' in baseline, "Should store speed score"

        print(f"✅ PASSED: Performance baseline stored successfully")
        print(f"   Baseline file: {baseline_path}")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_check_performance_regression():
    """Test 5: Check for performance regressions."""
    print("\n" + "=" * 70)
    print("Test 5: Check for Performance Regressions")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='flash_test_')

    try:
        flash = FlashPerformance(baseline_dir=temp_dir)

        # Test 1: No baseline exists
        result_no_baseline = flash._check_performance_regression('no-baseline-test', {
            'flash_speed_score': {'score': 85.0}
        })

        assert result_no_baseline['status'] == 'no_baseline', "Should report no baseline"

        # Test 2: Create baseline and test no regression
        baseline_results = {
            'timestamp': '2025-10-23T12:00:00',
            'core_web_vitals': {},
            'flash_speed_score': {'score': 90.0}
        }
        flash._store_performance_baseline('regression-test', baseline_results)

        current_results_good = {
            'flash_speed_score': {'score': 92.0}  # Better than baseline
        }

        result_no_regression = flash._check_performance_regression('regression-test', current_results_good)
        assert result_no_regression['status'] == 'no_regression', "Should report no regression"
        assert result_no_regression['is_regression'] == False, "is_regression should be False"
        assert result_no_regression['score_difference'] == 2.0, "Score should improve by 2"

        # Test 3: Regression detected
        current_results_bad = {
            'flash_speed_score': {'score': 80.0}  # 10 points worse (> 5 point threshold)
        }

        result_regression = flash._check_performance_regression('regression-test', current_results_bad)
        assert result_regression['status'] == 'regression_detected', "Should detect regression"
        assert result_regression['is_regression'] == True, "is_regression should be True"
        assert result_regression['score_difference'] == -10.0, "Score should drop by 10"
        assert 'REGRESSION' in result_regression['flash_verdict'], "Verdict should mention regression"

        print(f"✅ PASSED: Performance regression detection works")
        print(f"   No Baseline: {result_no_baseline['status']}")
        print(f"   No Regression: Score improved by {result_no_regression['score_difference']}")
        print(f"   Regression Detected: Score dropped by {abs(result_regression['score_difference'])}")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_generate_flash_recommendations():
    """Test 6: Generate Flash recommendations."""
    print("\n" + "=" * 70)
    print("Test 6: Generate Flash Recommendations")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='flash_test_')

    try:
        flash = FlashPerformance(baseline_dir=temp_dir)

        # Mock results with poor performance metrics
        mock_results = {
            'core_web_vitals': {
                'LCP': {'status': 'poor', 'value': 5000},
                'FID': {'status': 'good', 'value': 50},
                'CLS': {'status': 'needs_improvement', 'value': 0.15},
                'FCP': {'status': 'good', 'value': 1500},
                'TTI': {'status': 'good', 'value': 3000},
                'TBT': {'status': 'poor', 'value': 800}
            }
        }

        recommendations = flash._generate_flash_recommendations(mock_results)

        assert len(recommendations) > 0, "Should generate recommendations"

        # Check for LCP recommendation (poor)
        lcp_recs = [r for r in recommendations if 'LCP' in r.get('metric', '')]
        assert len(lcp_recs) > 0, "Should have LCP recommendation"
        assert lcp_recs[0]['priority'] == 'high', "LCP should be high priority"
        assert 'flash_says' in lcp_recs[0], "Should have Flash's message"
        assert 'actions' in lcp_recs[0], "Should have action items"

        # Check for CLS recommendation (needs improvement)
        cls_recs = [r for r in recommendations if 'CLS' in r.get('metric', '')]
        assert len(cls_recs) > 0, "Should have CLS recommendation"

        # Check for TBT recommendation (poor)
        tbt_recs = [r for r in recommendations if 'TBT' in r.get('metric', '')]
        assert len(tbt_recs) > 0, "Should have TBT recommendation"

        # No FID recommendation (good performance)
        fid_recs = [r for r in recommendations if 'FID' in r.get('metric', '')]
        assert len(fid_recs) == 0, "Should NOT have FID recommendation (good status)"

        print(f"✅ PASSED: Flash recommendations generated successfully")
        print(f"   Total Recommendations: {len(recommendations)}")
        print(f"   Metrics needing help: LCP, CLS, TBT")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_profile_performance_no_mcp():
    """Test 7: Profile performance without MCP tools."""
    print("\n" + "=" * 70)
    print("Test 7: Profile Performance (No MCP Tools)")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='flash_test_')

    try:
        flash = FlashPerformance(baseline_dir=temp_dir)

        # Test without MCP tools
        result = flash.profile_performance(
            mcp_tools={},
            test_name='no-mcp-test',
            url='https://example.com'
        )

        assert result['status'] == 'mcp_tools_missing', "Should report missing MCP tools"
        assert 'required_tools' in result, "Should list required tools"
        assert result['hero'] == '⚡ The Flash - Speed Analyzer', "Should identify as Flash"
        assert result['test_name'] == 'no-mcp-test', "Test name should match"

        print(f"✅ PASSED: Handles missing MCP tools gracefully")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_profile_performance_with_mocks():
    """Test 8: Profile performance with mock MCP tools."""
    print("\n" + "=" * 70)
    print("Test 8: Profile Performance (Mock MCP Tools)")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='flash_test_')

    try:
        flash = FlashPerformance(baseline_dir=temp_dir)

        # Mock MCP tools
        def mock_start_trace(reload=True, autoStop=True):
            return {'status': 'started', 'reload': reload, 'autoStop': autoStop}

        def mock_stop_trace():
            return {
                'lcp': 2200,
                'fid': 80,
                'cls': 0.08,
                'fcp': 1600,
                'tti': 3500,
                'tbt': 180,
                'insights': [
                    {'name': 'DocumentLatency', 'severity': 'warning'},
                    {'name': 'LCPBreakdown', 'severity': 'info'}
                ]
            }

        def mock_analyze_insight(insightName):
            return {'insight': insightName, 'details': 'Mock details'}

        mcp_tools = {
            'start_trace': mock_start_trace,
            'stop_trace': mock_stop_trace,
            'analyze_insight': mock_analyze_insight
        }

        # Run profiling
        result = flash.profile_performance(
            mcp_tools=mcp_tools,
            test_name='mock-test',
            url='https://example.com',
            reload_page=True
        )

        # Validate results
        assert 'error' not in result, f"Should not have errors, got {result.get('error')}"
        assert result['test_name'] == 'mock-test', "Test name should match"
        assert result['url'] == 'https://example.com', "URL should match"

        # Check trace started
        assert 'trace_started' in result, "Should have trace_started"

        # Check Core Web Vitals extracted
        assert 'core_web_vitals' in result, "Should have core_web_vitals"
        assert 'LCP' in result['core_web_vitals'], "Should extract LCP"
        assert result['core_web_vitals']['LCP']['value'] == 2200, "LCP should be 2200"

        # Check performance insights
        assert 'performance_insights' in result, "Should have performance_insights"
        assert len(result['performance_insights']) == 2, "Should have 2 insights"

        # Check Flash Speed Score
        assert 'flash_speed_score' in result, "Should have flash_speed_score"
        assert 'score' in result['flash_speed_score'], "Should have score"
        assert 0 <= result['flash_speed_score']['score'] <= 100, "Score should be 0-100"

        # Check regression check
        assert 'regression_check' in result, "Should have regression_check"

        # Check recommendations
        assert 'flash_recommendations' in result, "Should have flash_recommendations"

        print(f"\n✅ PASSED: Full performance profiling works with mock tools")
        print(f"   Flash Speed Score: {result['flash_speed_score']['score']}/100")
        print(f"   Grade: {result['flash_speed_score']['grade']}")
        print(f"   Insights: {len(result['performance_insights'])}")
        print(f"   Recommendations: {len(result['flash_recommendations'])}")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_core_web_vitals_thresholds():
    """Test 9: Core Web Vitals thresholds validation."""
    print("\n" + "=" * 70)
    print("Test 9: Core Web Vitals Thresholds")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='flash_test_')

    try:
        flash = FlashPerformance(baseline_dir=temp_dir)

        # Test LCP thresholds
        lcp_test = {
            'lcp': 2500,  # Exactly at threshold
            'fid': 0,
            'cls': 0,
            'fcp': 0,
            'tti': 0,
            'tbt': 0
        }

        vitals_lcp = flash._extract_core_web_vitals(lcp_test)
        assert vitals_lcp['LCP']['threshold_good'] == 2500, "LCP good threshold should be 2500ms"
        assert vitals_lcp['LCP']['threshold_needs_improvement'] == 4000, "LCP needs improvement threshold should be 4000ms"

        # Test CLS thresholds (different - lower is better)
        cls_test = {
            'lcp': 0,
            'fid': 0,
            'cls': 0.1,  # Exactly at threshold
            'fcp': 0,
            'tti': 0,
            'tbt': 0
        }

        vitals_cls = flash._extract_core_web_vitals(cls_test)
        assert vitals_cls['CLS']['threshold_good'] == 0.1, "CLS good threshold should be 0.1"
        assert vitals_cls['CLS']['threshold_needs_improvement'] == 0.25, "CLS needs improvement threshold should be 0.25"

        # Test boundary conditions
        boundary_tests = [
            ({'lcp': 2500}, 'LCP', 'good'),         # Exactly at good threshold
            ({'lcp': 2501}, 'LCP', 'needs_improvement'),  # Just over
            ({'lcp': 4000}, 'LCP', 'needs_improvement'),  # At needs improvement
            ({'lcp': 4001}, 'LCP', 'poor'),         # Over needs improvement
        ]

        for trace_data, metric, expected_status in boundary_tests:
            full_trace = {'lcp': 0, 'fid': 0, 'cls': 0, 'fcp': 0, 'tti': 0, 'tbt': 0}
            full_trace.update(trace_data)
            vitals = flash._extract_core_web_vitals(full_trace)
            assert vitals[metric]['status'] == expected_status, \
                f"{metric} with value {trace_data[metric.lower()]} should be '{expected_status}', got '{vitals[metric]['status']}'"

        print(f"✅ PASSED: Core Web Vitals thresholds validated")
        print(f"   LCP: ≤2500ms (good), ≤4000ms (needs improvement), >4000ms (poor)")
        print(f"   CLS: ≤0.1 (good), ≤0.25 (needs improvement), >0.25 (poor)")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_full_integration():
    """Test 10: Full Flash integration test."""
    print("\n" + "=" * 70)
    print("Test 10: Full Flash Integration Test")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='flash_test_')

    try:
        flash = FlashPerformance(baseline_dir=temp_dir)

        # Mock excellent performance
        def mock_start_trace(reload=True, autoStop=True):
            return {'status': 'started'}

        def mock_stop_trace():
            return {
                'lcp': 1800,   # Excellent
                'fid': 40,     # Excellent
                'cls': 0.05,   # Excellent
                'fcp': 1200,   # Excellent
                'tti': 2800,   # Excellent
                'tbt': 120,    # Excellent
                'insights': []  # No issues!
            }

        mcp_tools = {
            'start_trace': mock_start_trace,
            'stop_trace': mock_stop_trace
        }

        # Run full integration
        result = flash.profile_performance(
            mcp_tools=mcp_tools,
            test_name='integration-test',
            url='https://example.com/optimized',
            reload_page=True
        )

        # Validate complete workflow
        assert 'error' not in result, "Should not have errors"
        assert result['hero'] == '⚡ The Flash - Speed Analyzer', "Should identify as Flash"

        # All Core Web Vitals should be good
        for metric in ['LCP', 'FID', 'CLS', 'FCP', 'TTI', 'TBT']:
            assert result['core_web_vitals'][metric]['status'] == 'good', \
                f"{metric} should be 'good', got '{result['core_web_vitals'][metric]['status']}'"

        # Speed score should be excellent
        assert result['flash_speed_score']['score'] >= 90, \
            f"Excellent performance should score >= 90, got {result['flash_speed_score']['score']}"

        # Should have S+ or A grade
        assert result['flash_speed_score']['grade'] in ['S+', 'A'], \
            f"Should get S+ or A grade, got {result['flash_speed_score']['grade']}"

        # Regression check - baseline was just stored, so it compares to itself (0 difference)
        # Status will be 'no_regression' since score_diff = 0 (not < -5)
        assert result['regression_check']['status'] == 'no_regression', \
            "First run compares to just-stored baseline (should be no regression)"
        assert result['regression_check']['score_difference'] == 0, \
            "First run should have 0 score difference (comparing to itself)"

        # Recommendations should be minimal/empty for excellent performance
        assert len(result['flash_recommendations']) == 0, \
            f"Excellent performance should have 0 recommendations, got {len(result['flash_recommendations'])}"

        # Baseline should be stored
        baseline_path = flash.baseline_dir / 'integration-test_baseline.json'
        assert baseline_path.exists(), "Baseline should be stored"

        print(f"\n✅ PASSED: Full Flash integration successful")
        print(f"   Speed Score: {result['flash_speed_score']['score']}/100")
        print(f"   Grade: {result['flash_speed_score']['grade']}")
        print(f"   Verdict: {result['flash_speed_score']['verdict']}")
        print(f"   All 6 Core Web Vitals: GOOD ✓")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def run_all_tests():
    """Run complete test suite."""
    print("\n⚡ The Flash Performance - Test Suite")
    print("=" * 70)
    print("Testing Performance Profiling with Core Web Vitals")
    print("=" * 70)

    tests = [
        ("Initialization", test_flash_initialization),
        ("Extract Core Web Vitals", test_extract_core_web_vitals),
        ("Calculate Speed Score", test_calculate_speed_score),
        ("Store Performance Baseline", test_store_performance_baseline),
        ("Check Performance Regression", test_check_performance_regression),
        ("Generate Flash Recommendations", test_generate_flash_recommendations),
        ("Profile Performance (No MCP)", test_profile_performance_no_mcp),
        ("Profile Performance (Mock MCP)", test_profile_performance_with_mocks),
        ("Core Web Vitals Thresholds", test_core_web_vitals_thresholds),
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
        print("\n🎉 ALL TESTS PASSED! Flash runs at lightning speed!")
        print("⚡ I'm the fastest performance analyzer alive!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review.")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
