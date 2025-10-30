#!/usr/bin/env python3
"""
🌊 AQUAMAN NETWORK - Test Suite
=================================

Tests for network traffic analysis and resource optimization.

Author: Justice League
Created: October 23, 2025
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.justice_league.aquaman_network import AquamanNetwork


def test_aquaman_initialization():
    """Test 1: Aquaman Network initialization."""
    print("\n" + "=" * 70)
    print("Test 1: Aquaman Network Initialization")
    print("=" * 70)

    aquaman = AquamanNetwork()

    assert aquaman is not None, "Aquaman should initialize"
    assert hasattr(aquaman, 'analyze_network_traffic'), "Should have analyze_network_traffic method"
    assert hasattr(aquaman, '_analyze_request_types'), "Should have _analyze_request_types method"
    assert hasattr(aquaman, '_analyze_timing_waterfall'), "Should have _analyze_timing_waterfall method"
    assert hasattr(aquaman, '_detect_blocking_resources'), "Should have _detect_blocking_resources method"
    assert hasattr(aquaman, '_calculate_network_score'), "Should have _calculate_network_score method"

    print("✅ PASSED: Aquaman initialized successfully")
    return True


def test_analyze_request_types():
    """Test 2: Analyze network request types."""
    print("\n" + "=" * 70)
    print("Test 2: Analyze Network Request Types")
    print("=" * 70)

    aquaman = AquamanNetwork()

    # Mock network requests
    mock_requests = [
        {'url': 'https://example.com/index.html', 'resourceType': 'document', 'size': 5000},
        {'url': 'https://example.com/style.css', 'resourceType': 'stylesheet', 'size': 10000},
        {'url': 'https://example.com/script.js', 'resourceType': 'script', 'size': 50000},
        {'url': 'https://example.com/image.jpg', 'resourceType': 'image', 'size': 100000},
        {'url': 'https://example.com/image2.png', 'resourceType': 'image', 'size': 80000},
        {'url': 'https://example.com/font.woff2', 'resourceType': 'font', 'size': 30000},
        {'url': 'https://api.example.com/data', 'resourceType': 'xhr', 'size': 2000},
    ]

    analysis = aquaman._analyze_request_types(mock_requests)

    # Actual return structure: type_counts, type_sizes, total_size, aquaman_observation
    assert 'type_counts' in analysis, "Should have type_counts"
    assert 'type_sizes' in analysis, "Should have type_sizes"
    assert 'total_size' in analysis, "Should have total_size"
    assert 'aquaman_observation' in analysis, "Should have aquaman_observation"

    # Verify counts
    assert analysis['type_counts']['image'] == 2, f"Should have 2 images, got {analysis['type_counts'].get('image', 0)}"
    assert analysis['type_counts']['script'] == 1, f"Should have 1 script, got {analysis['type_counts'].get('script', 0)}"
    assert analysis['type_counts']['stylesheet'] == 1, "Should have 1 stylesheet"
    assert analysis['type_counts']['document'] == 1, "Should have 1 document"

    # Verify total size
    expected_total = 5000 + 10000 + 50000 + 100000 + 80000 + 30000 + 2000
    assert analysis['total_size'] == expected_total, f"Total size should be {expected_total}, got {analysis['total_size']}"

    # Verify observation message
    assert 'resource types' in analysis['aquaman_observation'].lower(), "Should have observation about resource types"

    print(f"✅ PASSED: Request type analysis works")
    print(f"   Total Size: {analysis['total_size']} bytes")
    print(f"   Resource Types: {len(analysis['type_counts'])}")
    print(f"   Observation: {analysis['aquaman_observation']}")
    return True


def test_analyze_timing_waterfall():
    """Test 3: Analyze timing waterfall."""
    print("\n" + "=" * 70)
    print("Test 3: Analyze Timing Waterfall")
    print("=" * 70)

    aquaman = AquamanNetwork()

    # Mock requests with timing data
    mock_requests = [
        {
            'url': 'https://example.com/1.js',
            'startTime': 0,
            'endTime': 100,
            'timing': {
                'requestStart': 0,
                'responseStart': 50,
                'responseEnd': 100
            }
        },
        {
            'url': 'https://example.com/2.css',
            'startTime': 50,
            'endTime': 200,
            'timing': {
                'requestStart': 50,
                'responseStart': 150,
                'responseEnd': 200
            }
        },
        {
            'url': 'https://example.com/3.jpg',
            'startTime': 100,
            'endTime': 500,
            'timing': {
                'requestStart': 100,
                'responseStart': 300,
                'responseEnd': 500
            }
        }
    ]

    waterfall = aquaman._analyze_timing_waterfall(mock_requests)

    # Actual return structure: total_time_ms, average_time_ms, slowest_5_requests, aquaman_verdict
    assert 'total_time_ms' in waterfall, "Should have total_time_ms"
    assert 'average_time_ms' in waterfall, "Should have average_time_ms"
    assert 'slowest_5_requests' in waterfall, "Should have slowest_5_requests"
    assert 'aquaman_verdict' in waterfall, "Should have aquaman_verdict"

    # Timing is calculated from timing phases (dns, connect, ssl, send, wait, receive)
    # Our mock requests have these calculated from responseEnd - requestStart
    assert waterfall['total_time_ms'] >= 0, f"Total time should be >= 0, got {waterfall['total_time_ms']}"
    assert len(waterfall['slowest_5_requests']) <= 5, "Should have at most 5 slowest requests"

    print(f"✅ PASSED: Timing waterfall analysis works")
    print(f"   Total Time: {waterfall['total_time_ms']}ms")
    print(f"   Average Time: {waterfall['average_time_ms']}ms")
    print(f"   Verdict: {waterfall['aquaman_verdict']}")
    return True


def test_detect_blocking_resources():
    """Test 4: Detect blocking resources."""
    print("\n" + "=" * 70)
    print("Test 4: Detect Blocking Resources")
    print("=" * 70)

    aquaman = AquamanNetwork()

    # Mock requests with blocking indicators
    mock_requests = [
        {
            'url': 'https://example.com/critical.css',
            'resourceType': 'stylesheet',
            'isBlocking': True,
            'size': 50000
        },
        {
            'url': 'https://example.com/blocking.js',
            'resourceType': 'script',
            'isBlocking': True,
            'size': 100000
        },
        {
            'url': 'https://example.com/async.js',
            'resourceType': 'script',
            'isBlocking': False,
            'size': 30000
        },
        {
            'url': 'https://example.com/image.jpg',
            'resourceType': 'image',
            'isBlocking': False,
            'size': 200000
        }
    ]

    blocking_analysis = aquaman._detect_blocking_resources(mock_requests)

    # Actual return structure: blocking_count, blocking_resources, severity, aquaman_command
    assert 'blocking_count' in blocking_analysis, "Should have blocking_count"
    assert 'blocking_resources' in blocking_analysis, "Should have blocking_resources"
    assert 'severity' in blocking_analysis, "Should have severity"
    assert 'aquaman_command' in blocking_analysis, "Should have aquaman_command"

    assert blocking_analysis['blocking_count'] == 2, f"Should have 2 blocking, got {blocking_analysis['blocking_count']}"
    assert len(blocking_analysis['blocking_resources']) == 2, f"Should list 2 blocking resources, got {len(blocking_analysis['blocking_resources'])}"

    # Verify severity is set
    assert blocking_analysis['severity'] in ['low', 'medium', 'high', 'critical'], f"Severity should be valid level, got {blocking_analysis['severity']}"

    print(f"✅ PASSED: Blocking resource detection works")
    print(f"   Blocking: {blocking_analysis['blocking_count']}")
    print(f"   Severity: {blocking_analysis['severity']}")
    print(f"   Command: {blocking_analysis['aquaman_command']}")
    return True


def test_identify_critical_path():
    """Test 5: Identify critical path."""
    print("\n" + "=" * 70)
    print("Test 5: Identify Critical Path")
    print("=" * 70)

    aquaman = AquamanNetwork()

    # Mock requests for critical path analysis
    mock_requests = [
        {'url': 'https://example.com/index.html', 'resourceType': 'document', 'priority': 'VeryHigh', 'startTime': 0, 'endTime': 100},
        {'url': 'https://example.com/critical.css', 'resourceType': 'stylesheet', 'priority': 'VeryHigh', 'startTime': 10, 'endTime': 150},
        {'url': 'https://example.com/main.js', 'resourceType': 'script', 'priority': 'High', 'startTime': 20, 'endTime': 200},
        {'url': 'https://example.com/image.jpg', 'resourceType': 'image', 'priority': 'Low', 'startTime': 100, 'endTime': 500},
    ]

    critical_path = aquaman._identify_critical_path(mock_requests)

    # Actual return structure: critical_resource_count, critical_resources, optimization_opportunity, aquaman_strategy
    assert 'critical_resource_count' in critical_path, "Should have critical_resource_count"
    assert 'critical_resources' in critical_path, "Should have critical_resources"
    assert 'optimization_opportunity' in critical_path, "Should have optimization_opportunity"
    assert 'aquaman_strategy' in critical_path, "Should have aquaman_strategy"

    # High priority resources should be in critical path (document, stylesheet, font)
    critical_urls = [r['url'] for r in critical_path['critical_resources']]
    assert 'https://example.com/index.html' in critical_urls, "Document should be critical"
    assert 'https://example.com/critical.css' in critical_urls, "CSS should be critical"

    print(f"✅ PASSED: Critical path identification works")
    print(f"   Critical Resources: {critical_path['critical_resource_count']}")
    print(f"   Strategy: {critical_path['aquaman_strategy']}")
    return True


def test_analyze_cache_efficiency():
    """Test 6: Analyze cache efficiency."""
    print("\n" + "=" * 70)
    print("Test 6: Analyze Cache Efficiency")
    print("=" * 70)

    aquaman = AquamanNetwork()

    # Mock requests with cache data
    mock_requests = [
        {'url': 'https://example.com/1.js', 'fromCache': True, 'size': 50000},
        {'url': 'https://example.com/2.css', 'fromCache': True, 'size': 30000},
        {'url': 'https://example.com/3.jpg', 'fromCache': False, 'size': 100000},
        {'url': 'https://example.com/4.png', 'fromCache': False, 'size': 80000},
    ]

    cache_analysis = aquaman._analyze_cache_efficiency(mock_requests)

    # Actual return structure: total_requests, cached_requests, not_cached_requests, cache_hit_rate_percent, cacheable_but_not_cached, aquaman_verdict
    assert 'total_requests' in cache_analysis, "Should have total_requests"
    assert 'cached_requests' in cache_analysis, "Should have cached_requests"
    assert 'not_cached_requests' in cache_analysis, "Should have not_cached_requests"
    assert 'cache_hit_rate_percent' in cache_analysis, "Should have cache_hit_rate_percent"
    assert 'cacheable_but_not_cached' in cache_analysis, "Should have cacheable_but_not_cached"
    assert 'aquaman_verdict' in cache_analysis, "Should have aquaman_verdict"

    assert cache_analysis['total_requests'] == 4, f"Should have 4 total, got {cache_analysis['total_requests']}"
    assert cache_analysis['cached_requests'] == 2, f"Should have 2 cached, got {cache_analysis['cached_requests']}"
    assert cache_analysis['not_cached_requests'] == 2, f"Should have 2 not cached, got {cache_analysis['not_cached_requests']}"
    assert cache_analysis['cache_hit_rate_percent'] == 50.0, f"Cache hit rate should be 50%, got {cache_analysis['cache_hit_rate_percent']}"

    print(f"✅ PASSED: Cache efficiency analysis works")
    print(f"   Cache Hit Rate: {cache_analysis['cache_hit_rate_percent']}%")
    print(f"   Verdict: {cache_analysis['aquaman_verdict']}")
    return True


def test_track_third_party_resources():
    """Test 7: Track third-party resources."""
    print("\n" + "=" * 70)
    print("Test 7: Track Third-Party Resources")
    print("=" * 70)

    aquaman = AquamanNetwork()

    # Mock requests with various domains
    mock_requests = [
        {'url': 'https://example.com/script.js', 'size': 50000},
        {'url': 'https://example.com/style.css', 'size': 30000},
        {'url': 'https://cdn.thirdparty.com/analytics.js', 'size': 100000},
        {'url': 'https://ads.network.com/banner.jpg', 'size': 200000},
        {'url': 'https://cdn.thirdparty.com/tracker.js', 'size': 50000},
    ]

    third_party = aquaman._track_third_party_resources(mock_requests)

    # Actual return structure: third_party_domain_count, third_party_request_count, third_party_domains, top_third_parties, aquaman_warning
    assert 'third_party_domain_count' in third_party, "Should have third_party_domain_count"
    assert 'third_party_request_count' in third_party, "Should have third_party_request_count"
    assert 'third_party_domains' in third_party, "Should have third_party_domains"
    assert 'top_third_parties' in third_party, "Should have top_third_parties"
    assert 'aquaman_warning' in third_party, "Should have aquaman_warning"

    # First request is example.com (first party), others are third party
    assert third_party['third_party_domain_count'] == 2, f"Should have 2 third-party domains, got {third_party['third_party_domain_count']}"
    assert third_party['third_party_request_count'] == 3, f"Should have 3 third-party requests, got {third_party['third_party_request_count']}"

    # Should group by domain (count of requests per domain)
    assert 'cdn.thirdparty.com' in third_party['third_party_domains'], "Should track cdn.thirdparty.com"
    assert third_party['third_party_domains']['cdn.thirdparty.com'] == 2, f"Should have 2 requests from cdn.thirdparty.com, got {third_party['third_party_domains']['cdn.thirdparty.com']}"

    print(f"✅ PASSED: Third-party resource tracking works")
    print(f"   Third-party Domains: {third_party['third_party_domain_count']}")
    print(f"   Third-party Requests: {third_party['third_party_request_count']}")
    print(f"   Warning: {third_party['aquaman_warning']}")
    return True


def test_calculate_network_score():
    """Test 8: Calculate Aquaman network score."""
    print("\n" + "=" * 70)
    print("Test 8: Calculate Aquaman Network Score")
    print("=" * 70)

    aquaman = AquamanNetwork()

    # High quality network performance
    # Actual structure expected by _calculate_network_score:
    # - cache_analysis.cache_hit_rate_percent
    # - blocking_resources.blocking_count
    # - third_party_analysis.third_party_domain_count
    # - total_requests
    high_quality_results = {
        'cache_analysis': {
            'cache_hit_rate_percent': 80.0  # Excellent cache
        },
        'blocking_resources': {
            'blocking_count': 2  # Low blocking
        },
        'third_party_analysis': {
            'third_party_domain_count': 3  # Few third-party
        },
        'total_requests': 20  # Good - not too many
    }

    score_high = aquaman._calculate_network_score(high_quality_results)

    assert score_high['score'] >= 70, f"High quality should score >= 70, got {score_high['score']}"
    assert 'grade' in score_high, "Should have grade"
    assert 'verdict' in score_high, "Should have verdict"

    # Low quality network performance
    low_quality_results = {
        'cache_analysis': {
            'cache_hit_rate_percent': 10.0  # Poor cache
        },
        'blocking_resources': {
            'blocking_count': 20  # High blocking
        },
        'third_party_analysis': {
            'third_party_domain_count': 50  # Too many third-party
        },
        'total_requests': 150  # Too many!
    }

    score_low = aquaman._calculate_network_score(low_quality_results)
    assert score_low['score'] < 50, f"Low quality should score < 50, got {score_low['score']}"

    print(f"✅ PASSED: Network score calculation works")
    print(f"   High Quality: {score_high['score']}/100 ({score_high['grade']})")
    print(f"   Low Quality:  {score_low['score']}/100 ({score_low['grade']})")
    return True


def test_generate_aquaman_recommendations():
    """Test 9: Generate Aquaman recommendations."""
    print("\n" + "=" * 70)
    print("Test 9: Generate Aquaman Recommendations")
    print("=" * 70)

    aquaman = AquamanNetwork()

    # Mock results with issues
    # Actual structure: cache_analysis, blocking_resources, third_party_analysis, total_requests
    mock_results = {
        'cache_analysis': {
            'cache_hit_rate_percent': 20.0  # Poor caching - will trigger high priority rec
        },
        'blocking_resources': {
            'blocking_count': 15  # Many blocking - will trigger high priority rec
        },
        'third_party_analysis': {
            'third_party_domain_count': 40  # Too many third-party - will trigger medium priority rec
        },
        'total_requests': 120  # Too many - will trigger recommendation
    }

    recommendations = aquaman._generate_aquaman_recommendations(mock_results)

    assert len(recommendations) > 0, "Should generate recommendations"

    # Check for specific recommendation types
    priorities = [r['priority'] for r in recommendations]
    assert 'high' in priorities, "Should have high priority recommendations"

    # Check for specific areas
    areas = [r['area'] for r in recommendations]
    assert 'Caching' in areas, "Should have caching recommendations (cache hit rate < 70%)"
    assert 'Render Blocking' in areas, "Should have blocking resource recommendations (> 3 blocking)"

    print(f"✅ PASSED: Aquaman recommendations generated")
    print(f"   Total Recommendations: {len(recommendations)}")
    for rec in recommendations:
        print(f"   - [{rec['priority']}] {rec['area']}: {rec['issue']}")
    return True


def test_full_network_analysis():
    """Test 10: Full Aquaman network analysis."""
    print("\n" + "=" * 70)
    print("Test 10: Full Aquaman Network Analysis")
    print("=" * 70)

    aquaman = AquamanNetwork()

    # Mock MCP tools
    def mock_list_requests(resourceTypes=None, pageIdx=None, pageSize=None):
        return {
            'requests': [
                {
                    'url': 'https://example.com/index.html',
                    'resourceType': 'document',
                    'size': 10000,
                    'fromCache': False,
                    'isBlocking': True,
                    'priority': 'VeryHigh',
                    'startTime': 0,
                    'endTime': 100,
                    'timing': {'requestStart': 0, 'responseStart': 50, 'responseEnd': 100}
                },
                {
                    'url': 'https://example.com/style.css',
                    'resourceType': 'stylesheet',
                    'size': 20000,
                    'fromCache': True,
                    'isBlocking': True,
                    'priority': 'High',
                    'startTime': 10,
                    'endTime': 120,
                    'timing': {'requestStart': 10, 'responseStart': 80, 'responseEnd': 120}
                },
                {
                    'url': 'https://cdn.example.com/analytics.js',
                    'resourceType': 'script',
                    'size': 50000,
                    'fromCache': False,
                    'isBlocking': False,
                    'priority': 'Low',
                    'startTime': 50,
                    'endTime': 300,
                    'timing': {'requestStart': 50, 'responseStart': 200, 'responseEnd': 300}
                }
            ],
            'total': 3
        }

    mcp_tools = {
        'list_network_requests': mock_list_requests
    }

    # Run full analysis
    result = aquaman.analyze_network_traffic(mcp_tools)

    # Validate results
    assert 'error' not in result, f"Should not have errors, got {result.get('error')}"
    assert result['hero'] == '🌊 Aquaman - King of Network Seas', "Should identify as Aquaman"

    # Check top-level structure (NOT network_analysis, these are direct keys)
    assert 'total_requests' in result, "Should have total_requests"
    assert 'all_requests' in result, "Should have all_requests"
    assert 'request_types' in result, "Should have request_types"
    assert 'timing_analysis' in result, "Should have timing_analysis"
    assert 'blocking_resources' in result, "Should have blocking_resources"
    assert 'critical_path' in result, "Should have critical_path"
    assert 'cache_analysis' in result, "Should have cache_analysis"
    assert 'third_party_analysis' in result, "Should have third_party_analysis"
    assert 'aquaman_score' in result, "Should have aquaman_score"
    assert 'aquaman_recommendations' in result, "Should have aquaman_recommendations"

    # Validate data types and structure
    assert result['total_requests'] == 3, f"Should have 3 requests, got {result['total_requests']}"
    assert 0 <= result['aquaman_score']['score'] <= 100, "Score should be 0-100"

    print(f"\n✅ PASSED: Full network analysis successful")
    print(f"   Network Score: {result['aquaman_score']['score']}/100")
    print(f"   Grade: {result['aquaman_score']['grade']}")
    print(f"   Total Requests: {result['total_requests']}")
    print(f"   Cache Hit Rate: {result['cache_analysis']['cache_hit_rate_percent']}%")
    return True


def run_all_tests():
    """Run complete test suite."""
    print("\n🌊 Aquaman Network - Test Suite")
    print("=" * 70)
    print("Testing Network Traffic Analysis and Optimization")
    print("=" * 70)

    tests = [
        ("Initialization", test_aquaman_initialization),
        ("Analyze Request Types", test_analyze_request_types),
        ("Analyze Timing Waterfall", test_analyze_timing_waterfall),
        ("Detect Blocking Resources", test_detect_blocking_resources),
        ("Identify Critical Path", test_identify_critical_path),
        ("Analyze Cache Efficiency", test_analyze_cache_efficiency),
        ("Track Third-Party Resources", test_track_third_party_resources),
        ("Calculate Network Score", test_calculate_network_score),
        ("Generate Aquaman Recommendations", test_generate_aquaman_recommendations),
        ("Full Network Analysis", test_full_network_analysis),
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
        print("\n🎉 ALL TESTS PASSED! Aquaman commands the network seas!")
        print("🌊 King of Atlantis approves - All network traffic optimized!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review.")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
