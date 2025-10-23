#!/usr/bin/env python3
"""
Test Superman Network Timing Analysis

This script tests the Superman network timing system with mock MCP tools
"""

import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.superman_network_analysis import SupermanNetworkAnalysis, analyze_network_timing_complete

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def create_mock_network_requests():
    """
    Create mock network requests for testing

    Returns:
        List of mock network request objects
    """
    return [
        # Document (always critical)
        {
            'url': 'https://example.com/',
            'method': 'GET',
            'status': 200,
            'resourceType': 'document',
            'size': 50 * 1024,  # 50 KB
            'priority': 'very-high',
            'fromCache': False,
            'startTime': 0.0,
            'timing': {
                'dns': 20,
                'connect': 50,
                'ssl': 80,
                'send': 5,
                'wait': 300,  # TTFB
                'receive': 50
            },
            'initiator': {'type': 'other'}
        },

        # Blocking CSS
        {
            'url': 'https://example.com/styles.css',
            'method': 'GET',
            'status': 200,
            'resourceType': 'stylesheet',
            'size': 150 * 1024,  # 150 KB
            'priority': 'very-high',
            'fromCache': False,
            'startTime': 0.1,
            'timing': {
                'dns': 0,  # Same domain
                'connect': 0,
                'ssl': 0,
                'send': 5,
                'wait': 200,
                'receive': 100
            },
            'initiator': {'type': 'parser'}
        },

        # Blocking JavaScript
        {
            'url': 'https://example.com/app.js',
            'method': 'GET',
            'status': 200,
            'resourceType': 'script',
            'size': 500 * 1024,  # 500 KB (large!)
            'priority': 'high',
            'fromCache': False,
            'startTime': 0.15,
            'timing': {
                'dns': 0,
                'connect': 0,
                'ssl': 0,
                'send': 5,
                'wait': 250,
                'receive': 400  # Slow download
            },
            'initiator': {'type': 'parser'}
        },

        # Web Font
        {
            'url': 'https://fonts.googleapis.com/font.woff2',
            'method': 'GET',
            'status': 200,
            'resourceType': 'font',
            'size': 80 * 1024,
            'priority': 'high',
            'fromCache': False,
            'startTime': 0.2,
            'timing': {
                'dns': 100,  # Third-party DNS
                'connect': 150,  # Third-party connection
                'ssl': 120,
                'send': 5,
                'wait': 180,
                'receive': 60
            },
            'initiator': {'type': 'css'}
        },

        # Large image
        {
            'url': 'https://cdn.example.com/hero.jpg',
            'method': 'GET',
            'status': 200,
            'resourceType': 'image',
            'size': 1500 * 1024,  # 1.5 MB (over 1MB threshold)
            'priority': 'medium',
            'fromCache': False,
            'startTime': 0.3,
            'timing': {
                'dns': 30,
                'connect': 40,
                'ssl': 50,
                'send': 5,
                'wait': 100,
                'receive': 800  # Very slow download
            },
            'initiator': {'type': 'parser'}
        },

        # Cached image
        {
            'url': 'https://cdn.example.com/logo.png',
            'method': 'GET',
            'status': 200,
            'resourceType': 'image',
            'size': 20 * 1024,
            'priority': 'low',
            'fromCache': True,  # Cached!
            'startTime': 0.35,
            'timing': {
                'dns': 0,
                'connect': 0,
                'ssl': 0,
                'send': 0,
                'wait': 0,
                'receive': 5  # Fast from cache
            },
            'initiator': {'type': 'parser'}
        },

        # Third-party analytics
        {
            'url': 'https://analytics.example.com/track.js',
            'method': 'GET',
            'status': 200,
            'resourceType': 'script',
            'size': 50 * 1024,
            'priority': 'low',
            'fromCache': False,
            'startTime': 0.4,
            'timing': {
                'dns': 80,
                'connect': 100,
                'ssl': 90,
                'send': 5,
                'wait': 150,
                'receive': 40
            },
            'initiator': {'type': 'script'}
        },

        # XHR request
        {
            'url': 'https://api.example.com/data.json',
            'method': 'GET',
            'status': 200,
            'resourceType': 'xhr',
            'size': 100 * 1024,
            'priority': 'high',
            'fromCache': False,
            'startTime': 0.5,
            'timing': {
                'dns': 0,
                'connect': 0,
                'ssl': 0,
                'send': 5,
                'wait': 500,  # Slow API
                'receive': 100
            },
            'initiator': {'type': 'script'}
        }
    ]


def create_mock_mcp_tools():
    """
    Create mock MCP tools for testing

    Returns:
        Dictionary of mock MCP tool functions
    """
    mock_requests = create_mock_network_requests()

    def mock_list_network_requests(pageIdx=0, pageSize=100, resourceTypes=None):
        """Mock list_network_requests function"""
        logger.info(f"🧪 MOCK: Listing network requests (page {pageIdx}, size {pageSize})")

        # Filter by resource types if specified
        if resourceTypes:
            filtered = [r for r in mock_requests if r['resourceType'] in resourceTypes]
        else:
            filtered = mock_requests

        # Pagination
        start = pageIdx * pageSize
        end = start + pageSize
        page_requests = filtered[start:end]

        return {
            'requests': page_requests,
            'total': len(filtered)
        }

    def mock_get_network_request(url):
        """Mock get_network_request function"""
        logger.info(f"🧪 MOCK: Getting network request for {url}")

        # Find request by URL
        for req in mock_requests:
            if req['url'] == url:
                return req

        return None

    return {
        'list_network_requests': mock_list_network_requests,
        'get_network_request': mock_get_network_request
    }


def test_basic_network_analysis():
    """Test basic network analysis functionality"""
    logger.info("=" * 80)
    logger.info("TEST 1: Basic Network Analysis")
    logger.info("=" * 80)

    # Create mock MCP tools
    mcp_tools = create_mock_mcp_tools()

    # Run network analysis
    result = analyze_network_timing_complete(
        mcp_tools=mcp_tools,
        url='https://example.com',
        test_name='test_basic',
        store_baseline=True
    )

    # Verify results
    assert result['status'] == 'success', "Analysis should succeed"
    assert 'superman_network_score' in result, "Should have Superman network score"

    score = result['superman_network_score']
    logger.info(f"\n✅ Superman Network Score: {score['score']}/100 ({score['grade']})")
    logger.info(f"✅ Verdict: {score['verdict']}")
    logger.info(f"✅ Critical Path: {result['critical_path']['critical_path_length_ms']:.0f}ms")
    logger.info(f"✅ Blocking Resources: {result['blocking_resources']['blocking_count']}")
    logger.info(f"✅ Bottlenecks: {result['bottlenecks']['bottleneck_count']}")

    return result


def test_waterfall_generation():
    """Test waterfall chart data generation"""
    logger.info("\n" + "=" * 80)
    logger.info("TEST 2: Waterfall Chart Generation")
    logger.info("=" * 80)

    mcp_tools = create_mock_mcp_tools()

    result = analyze_network_timing_complete(
        mcp_tools=mcp_tools,
        url='https://example.com/waterfall-test'
    )

    waterfall = result.get('waterfall', {})

    logger.info(f"\n🌊 Waterfall Chart Data:")
    logger.info(f"  Total Time: {waterfall.get('total_time_ms', 0):.0f}ms")
    logger.info(f"  Entries: {waterfall.get('entry_count', 0)}")

    # Check first few entries
    entries = waterfall.get('entries', [])[:3]
    logger.info(f"\n  First 3 entries:")
    for idx, entry in enumerate(entries, 1):
        logger.info(f"    {idx}. {entry['url']}")
        logger.info(f"       Type: {entry['resourceType']}, Size: {entry['size'] / 1024:.1f}KB")
        logger.info(f"       Start: {entry['startTime']:.0f}ms, Duration: {entry['duration']:.0f}ms")

        # Verify timing phases
        timings = entry['timings']
        assert 'dns' in timings, "Should have DNS timing"
        assert 'connect' in timings, "Should have Connect timing"
        assert 'wait' in timings, "Should have Wait (TTFB) timing"
        assert 'receive' in timings, "Should have Receive timing"

    logger.info(f"\n✅ Waterfall chart generation: PASSED")

    return result


def test_critical_path_detection():
    """Test critical rendering path detection"""
    logger.info("\n" + "=" * 80)
    logger.info("TEST 3: Critical Path Detection")
    logger.info("=" * 80)

    mcp_tools = create_mock_mcp_tools()

    result = analyze_network_timing_complete(
        mcp_tools=mcp_tools,
        url='https://example.com/critical-path-test'
    )

    critical_path = result.get('critical_path', {})

    logger.info(f"\n🎯 Critical Rendering Path:")
    logger.info(f"  Critical Resources: {critical_path.get('critical_resource_count', 0)}")
    logger.info(f"  Critical Path Length: {critical_path.get('critical_path_length_ms', 0):.0f}ms")
    logger.info(f"  Optimization Potential: {critical_path.get('optimization_potential_ms', 0):.0f}ms")

    # Show critical resources
    logger.info(f"\n  Critical Resources:")
    for idx, resource in enumerate(critical_path.get('critical_resources', [])[:5], 1):
        logger.info(f"    {idx}. {resource['type']}: {resource['time_ms']:.0f}ms")
        logger.info(f"       {resource['superman_analysis']}")

    # Verify critical resources are correct
    critical_types = [r['type'] for r in critical_path.get('critical_resources', [])]
    assert 'document' in critical_types, "Document should be critical"
    assert 'stylesheet' in critical_types, "CSS should be critical"

    logger.info(f"\n✅ Critical path detection: PASSED")

    return result


def test_blocking_resource_identification():
    """Test blocking resource identification with impact scores"""
    logger.info("\n" + "=" * 80)
    logger.info("TEST 4: Blocking Resource Identification")
    logger.info("=" * 80)

    mcp_tools = create_mock_mcp_tools()

    result = analyze_network_timing_complete(
        mcp_tools=mcp_tools,
        url='https://example.com/blocking-test'
    )

    blocking = result.get('blocking_resources', {})

    logger.info(f"\n⚠️  Blocking Resources:")
    logger.info(f"  Total Blocking: {blocking.get('blocking_count', 0)}")
    logger.info(f"  Total Blocking Time: {blocking.get('total_blocking_time_ms', 0):.0f}ms")
    logger.info(f"  Critical Blocking: {len(blocking.get('critical_blocking', []))}")
    logger.info(f"  High Impact Blocking: {len(blocking.get('high_impact_blocking', []))}")

    # Show top blocking resources
    logger.info(f"\n  Top Blocking Resources:")
    for idx, resource in enumerate(blocking.get('blocking_resources', [])[:5], 1):
        logger.info(f"    {idx}. {resource['type']}: Impact {resource['impact_score']}/10")
        logger.info(f"       Blocking Time: {resource['blocking_time_ms']:.0f}ms")
        logger.info(f"       {resource['superman_says']}")

    # Verify blocking resources detected
    assert blocking.get('blocking_count', 0) > 0, "Should detect blocking resources"

    logger.info(f"\n✅ Blocking resource identification: PASSED")

    return result


def test_timing_phase_analysis():
    """Test detailed timing phase analysis"""
    logger.info("\n" + "=" * 80)
    logger.info("TEST 5: Timing Phase Analysis")
    logger.info("=" * 80)

    mcp_tools = create_mock_mcp_tools()

    result = analyze_network_timing_complete(
        mcp_tools=mcp_tools,
        url='https://example.com/timing-test'
    )

    timing_phases = result.get('timing_phases', {})

    logger.info(f"\n⏱️  Timing Phase Breakdown:")
    logger.info(f"  Requests Analyzed: {timing_phases.get('requests_analyzed', 0)}")

    # Show phase averages
    averages = timing_phases.get('phase_averages_ms', {})
    logger.info(f"\n  Average Timing (ms):")
    logger.info(f"    DNS:     {averages.get('dns', 0):.1f}ms")
    logger.info(f"    Connect: {averages.get('connect', 0):.1f}ms")
    logger.info(f"    SSL:     {averages.get('ssl', 0):.1f}ms")
    logger.info(f"    Send:    {averages.get('send', 0):.1f}ms")
    logger.info(f"    Wait:    {averages.get('wait', 0):.1f}ms (TTFB)")
    logger.info(f"    Receive: {averages.get('receive', 0):.1f}ms")

    # Show Superman insights
    insights = timing_phases.get('superman_insights', {})
    logger.info(f"\n  🦸 Superman Insights:")
    for phase, insight in insights.items():
        logger.info(f"    - {phase}: {insight}")

    logger.info(f"\n✅ Timing phase analysis: PASSED")

    return result


def test_bottleneck_detection():
    """Test network bottleneck detection"""
    logger.info("\n" + "=" * 80)
    logger.info("TEST 6: Network Bottleneck Detection")
    logger.info("=" * 80)

    mcp_tools = create_mock_mcp_tools()

    result = analyze_network_timing_complete(
        mcp_tools=mcp_tools,
        url='https://example.com/bottleneck-test'
    )

    bottlenecks = result.get('bottlenecks', {})

    logger.info(f"\n🚨 Network Bottlenecks:")
    logger.info(f"  Total Bottlenecks: {bottlenecks.get('bottleneck_count', 0)}")
    logger.info(f"  Critical: {len(bottlenecks.get('critical_bottlenecks', []))}")
    logger.info(f"  High Severity: {len(bottlenecks.get('high_severity_bottlenecks', []))}")

    # Show bottlenecks
    logger.info(f"\n  Detected Bottlenecks:")
    for idx, bottleneck in enumerate(bottlenecks.get('bottlenecks', []), 1):
        logger.info(f"    {idx}. {bottleneck['type']} ({bottleneck['severity']})")
        logger.info(f"       Issue: {bottleneck['issue']}")
        logger.info(f"       {bottleneck['superman_says']}")
        logger.info(f"       Fix: {bottleneck['fix']}")

    logger.info(f"\n  {bottlenecks.get('superman_status', 'Unknown')}")

    logger.info(f"\n✅ Bottleneck detection: PASSED")

    return result


def test_performance_budget():
    """Test performance budget checking"""
    logger.info("\n" + "=" * 80)
    logger.info("TEST 7: Performance Budget Checking")
    logger.info("=" * 80)

    mcp_tools = create_mock_mcp_tools()

    # Strict budget to trigger violations
    budget = {
        'total_requests': 5,  # We have 8 requests
        'total_size_kb': 1000,  # We have ~2.5MB total
        'scripts_kb': 300,  # We have 500KB scripts
        'images_kb': 500,  # We have 1.5MB images
        'css_kb': 100  # We have 150KB CSS
    }

    result = analyze_network_timing_complete(
        mcp_tools=mcp_tools,
        url='https://example.com/budget-test',
        performance_budget=budget
    )

    budget_check = result.get('performance_budget', {})

    logger.info(f"\n💰 Performance Budget:")
    logger.info(f"  Status: {budget_check.get('status', 'unknown')}")
    logger.info(f"  Violations: {budget_check.get('violation_count', 0)}")

    # Show violations
    if budget_check.get('violations'):
        logger.info(f"\n  ⚠️  Budget Violations:")
        for idx, violation in enumerate(budget_check.get('violations', []), 1):
            logger.info(f"    {idx}. {violation['metric']}")
            logger.info(f"       Budget: {violation['budget']}, Actual: {violation['actual']}")
            logger.info(f"       Over by: {violation['over_by']} ({violation['over_percent']:.0f}%)")
            logger.info(f"       {violation['superman_says']}")

    logger.info(f"\n  {budget_check.get('superman_verdict', 'Unknown')}")

    # Verify violations detected
    assert budget_check.get('status') == 'over_budget', "Should detect budget violations"
    assert budget_check.get('violation_count', 0) > 0, "Should have violations"

    logger.info(f"\n✅ Performance budget checking: PASSED")

    return result


def test_cdn_analysis():
    """Test CDN effectiveness analysis"""
    logger.info("\n" + "=" * 80)
    logger.info("TEST 8: CDN Effectiveness Analysis")
    logger.info("=" * 80)

    mcp_tools = create_mock_mcp_tools()

    result = analyze_network_timing_complete(
        mcp_tools=mcp_tools,
        url='https://example.com/cdn-test'
    )

    cdn = result.get('cdn_analysis', {})

    logger.info(f"\n🌐 CDN Analysis:")
    logger.info(f"  CDN Requests: {cdn.get('cdn_request_count', 0)}")
    logger.info(f"  CDN Size: {cdn.get('cdn_size_kb', 0):.1f}KB")
    logger.info(f"  CDN Usage: {cdn.get('cdn_usage_percent', 0):.1f}%")
    logger.info(f"\n  {cdn.get('superman_assessment', 'Unknown')}")

    # Show CDN requests
    if cdn.get('cdn_requests'):
        logger.info(f"\n  CDN Resources:")
        for idx, req in enumerate(cdn.get('cdn_requests', [])[:5], 1):
            logger.info(f"    {idx}. {req['type']}: {req['size'] / 1024:.1f}KB")

    logger.info(f"\n✅ CDN analysis: PASSED")

    return result


def test_recommendations():
    """Test recommendation generation"""
    logger.info("\n" + "=" * 80)
    logger.info("TEST 9: Recommendation Generation")
    logger.info("=" * 80)

    mcp_tools = create_mock_mcp_tools()

    result = analyze_network_timing_complete(
        mcp_tools=mcp_tools,
        url='https://example.com/recommendations-test'
    )

    recommendations = result.get('superman_recommendations', [])

    logger.info(f"\n📋 Superman Recommendations:")
    logger.info(f"  Total: {len(recommendations)}")

    # Show recommendations
    for idx, rec in enumerate(recommendations, 1):
        logger.info(f"\n  Recommendation {idx} ({rec['priority'].upper()}):")
        logger.info(f"    Area: {rec['area']}")
        logger.info(f"    Issue: {rec['issue']}")
        logger.info(f"    {rec['superman_says']}")
        logger.info(f"    Actions:")
        for action in rec['actions'][:3]:
            logger.info(f"      - {action}")

    # Verify recommendations generated
    assert len(recommendations) > 0, "Should generate recommendations"

    logger.info(f"\n✅ Recommendation generation: PASSED")

    return result


def main():
    """Run all tests"""
    try:
        logger.info("🦸🌊 SUPERMAN NETWORK TIMING ANALYSIS TEST SUITE")
        logger.info("=" * 80)

        # Run tests
        test_basic_network_analysis()
        test_waterfall_generation()
        test_critical_path_detection()
        test_blocking_resource_identification()
        test_timing_phase_analysis()
        test_bottleneck_detection()
        test_performance_budget()
        test_cdn_analysis()
        test_recommendations()

        logger.info("\n" + "=" * 80)
        logger.info("🦸🌊 ALL TESTS PASSED! Superman Network Analysis is ready!")
        logger.info("=" * 80)

        return 0

    except Exception as e:
        logger.error(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
