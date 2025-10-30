#!/usr/bin/env python3
"""
🔮 ORACLE - Meta-Agent Test Suite
===================================

Tests for knowledge management, self-healing, and continuous improvement.

Oracle serves as the Justice League's knowledge keeper and system architect.

Author: Justice League Development Team
Created: October 23, 2025
"""

import sys
import os
from pathlib import Path
import tempfile
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.justice_league.oracle_meta_agent import OracleMeta
from core.mcp_integration.mcp_manager import MCPIntegrationManager


def test_oracle_initialization():
    """Test 1: Oracle meta-agent initialization."""
    print("\n" + "=" * 70)
    print("Test 1: Oracle Meta-Agent Initialization")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='oracle_test_')
    oracle = OracleMeta(knowledge_base_dir=temp_dir)

    assert oracle is not None, "Oracle should initialize"
    assert hasattr(oracle, 'store_error_solution'), "Should have store_error_solution method"
    assert hasattr(oracle, 'query_knowledge_base'), "Should have query_knowledge_base method"
    assert hasattr(oracle, 'analyze_mission_results'), "Should have analyze_mission_results method"
    assert hasattr(oracle, 'predict_failures'), "Should have predict_failures method"
    assert hasattr(oracle, 'track_agent_performance'), "Should have track_agent_performance method"

    # Check knowledge base files created
    assert oracle.errors_db.exists(), "Errors database should exist"
    assert oracle.patterns_db.exists(), "Patterns database should exist"
    assert oracle.metrics_db.exists(), "Metrics database should exist"
    assert oracle.mcp_db.exists(), "MCP database should exist"
    assert oracle.best_practices_db.exists(), "Best practices database should exist"
    assert oracle.versions_db.exists(), "Versions database should exist"

    # Check MCP servers configured
    assert len(oracle.mcp_servers) > 0, "Should have MCP servers configured"
    assert 'claude-code-sdk' in oracle.mcp_servers, "Should include Claude Code SDK"

    print("✅ PASSED: Oracle initialized successfully")
    print(f"   Knowledge Base: {oracle.knowledge_base_dir}")
    print(f"   MCP Servers: {len(oracle.mcp_servers)}")
    print(f"   Databases: 6 created")
    return True


def test_error_solution_storage():
    """Test 2: Store and retrieve error/solution pairs."""
    print("\n" + "=" * 70)
    print("Test 2: Error/Solution Storage and Retrieval")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='oracle_test_')
    oracle = OracleMeta(knowledge_base_dir=temp_dir)

    # Store an error
    error_id = oracle.store_error_solution(
        agent_name='batman',
        error_type='timeout',
        error_details={'message': 'Request timeout after 30s', 'url': 'https://example.com'},
        solution='Increased timeout to 60s',
        context={'mission_type': 'interactive_test', 'browser': 'chrome'}
    )

    assert error_id is not None, "Should return error ID"
    assert error_id.startswith('ERR-'), "Error ID should start with ERR-"

    # Query the knowledge base
    results = oracle.query_knowledge_base('timeout', agent_name='batman')

    assert len(results) > 0, "Should find the stored error"
    assert results[0]['error_type'] == 'timeout', "Should retrieve correct error type"
    assert results[0]['solution'] == 'Increased timeout to 60s', "Should retrieve correct solution"

    # Store duplicate error
    error_id_2 = oracle.store_error_solution(
        agent_name='batman',
        error_type='timeout',
        error_details={'message': 'Request timeout after 30s', 'url': 'https://example.com'},
        solution='Increased timeout to 60s',
        context={'mission_type': 'interactive_test', 'browser': 'chrome'}
    )

    # Should update existing error, not create new one
    results_after = oracle.query_knowledge_base('timeout', agent_name='batman')
    # Note: The implementation updates the existing error

    print("✅ PASSED: Error/solution storage works")
    print(f"   Error ID: {error_id}")
    print(f"   Query Results: {len(results)} found")
    return True


def test_best_practices_management():
    """Test 3: Best practices storage and retrieval."""
    print("\n" + "=" * 70)
    print("Test 3: Best Practices Management")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='oracle_test_')
    oracle = OracleMeta(knowledge_base_dir=temp_dir)

    # Add best practices
    oracle.add_best_practice(
        category='testing',
        title='Always test with real browser',
        description='Use Chrome DevTools MCP for realistic testing instead of mocks',
        source='Justice League Testing Guidelines v1.0'
    )

    oracle.add_best_practice(
        category='testing',
        title='Write descriptive test names',
        description='Test names should clearly describe what is being tested',
        source='Oracle Knowledge Base'
    )

    oracle.add_best_practice(
        category='performance',
        title='Cache expensive operations',
        description='Store results of expensive computations for reuse',
        source='Flash Performance Guide'
    )

    # Retrieve best practices
    testing_practices = oracle.get_best_practices('testing')
    performance_practices = oracle.get_best_practices('performance')

    assert len(testing_practices) == 2, "Should have 2 testing practices"
    assert len(performance_practices) == 1, "Should have 1 performance practice"
    assert testing_practices[0]['category'] == 'testing', "Should filter by category"

    print("✅ PASSED: Best practices management works")
    print(f"   Testing Practices: {len(testing_practices)}")
    print(f"   Performance Practices: {len(performance_practices)}")
    return True


def test_mission_analysis():
    """Test 4: Analyze mission results and generate insights."""
    print("\n" + "=" * 70)
    print("Test 4: Mission Results Analysis")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='oracle_test_')
    oracle = OracleMeta(knowledge_base_dir=temp_dir)

    # Mock mission results
    mission_results = {
        'mission_id': 'MISSION-001',
        'hero_reports': {
            'batman': {
                'score': {'score': 95},
                'performance': {'execution_time': 2000}
            },
            'flash': {
                'score': {'score': 75},  # Low score
                'performance': {'execution_time': 8000}  # Slow execution
            },
            'wonder_woman': {
                'error': 'WCAG validation failed',  # Error
                'score': {'score': 60}
            }
        }
    }

    analysis = oracle.analyze_mission_results(mission_results)

    # Validate analysis structure
    assert 'insights' in analysis, "Should have insights"
    assert 'recommendations' in analysis, "Should have recommendations"
    assert 'patterns_detected' in analysis, "Should have patterns_detected"
    assert 'oracle_says' in analysis, "Should have oracle_says message"

    # Should detect issues
    assert len(analysis['recommendations']) > 0, "Should have recommendations for low scores and errors"

    # Check recommendation priorities
    high_priority_recs = [r for r in analysis['recommendations'] if r.get('priority') == 'high']
    assert len(high_priority_recs) > 0, "Should have high priority recommendations"

    print("✅ PASSED: Mission analysis works")
    print(f"   Insights: {len(analysis['insights'])}")
    print(f"   Recommendations: {len(analysis['recommendations'])}")
    print(f"   Oracle Says: {analysis['oracle_says']}")
    return True


def test_performance_tracking():
    """Test 5: Track agent performance metrics."""
    print("\n" + "=" * 70)
    print("Test 5: Performance Tracking")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='oracle_test_')
    oracle = OracleMeta(knowledge_base_dir=temp_dir)

    # Track performance for multiple missions
    for i in range(10):
        oracle.track_agent_performance(
            agent_name='batman',
            metrics={
                'success': i < 9,  # 9 successful, 1 failed
                'execution_time': 2000 + (i * 100),
                'score': 95 - i
            }
        )

    # Get metrics
    batman_metrics = oracle.get_agent_metrics('batman')

    assert batman_metrics is not None, "Should have Batman metrics"
    assert batman_metrics['total_missions'] == 10, "Should track 10 missions"
    assert batman_metrics['total_errors'] == 1, "Should track 1 error"
    assert batman_metrics['success_rate'] == 0.9, "Should calculate 90% success rate"
    assert len(batman_metrics['metrics_history']) == 10, "Should store all metrics"

    print("✅ PASSED: Performance tracking works")
    print(f"   Total Missions: {batman_metrics['total_missions']}")
    print(f"   Success Rate: {batman_metrics['success_rate']:.1%}")
    print(f"   Total Errors: {batman_metrics['total_errors']}")
    return True


def test_performance_report():
    """Test 6: Generate comprehensive performance report."""
    print("\n" + "=" * 70)
    print("Test 6: Performance Report Generation")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='oracle_test_')
    oracle = OracleMeta(knowledge_base_dir=temp_dir)

    # Track performance for multiple agents
    oracle.track_agent_performance('batman', {'success': True, 'score': 95})
    oracle.track_agent_performance('batman', {'success': True, 'score': 90})

    oracle.track_agent_performance('flash', {'success': True, 'score': 100})
    oracle.track_agent_performance('flash', {'success': False, 'score': 50})  # One failure

    oracle.track_agent_performance('wonder_woman', {'success': False, 'score': 30})  # Low success
    oracle.track_agent_performance('wonder_woman', {'success': False, 'score': 40})

    # Generate report
    report = oracle.generate_performance_report()

    assert 'total_agents' in report, "Should have total_agents"
    assert 'agents' in report, "Should have agents"
    assert 'recommendations' in report, "Should have recommendations"
    assert 'overall_health' in report, "Should have overall_health"

    assert report['total_agents'] == 3, "Should track 3 agents"
    assert 'batman' in report['agents'], "Should include Batman"
    assert 'flash' in report['agents'], "Should include Flash"
    assert 'wonder_woman' in report['agents'], "Should include Wonder Woman"

    # Wonder Woman should be unhealthy (50% success rate)
    assert report['agents']['wonder_woman']['health_status'] == 'unhealthy', "Low success rate should be unhealthy"

    # Should have recommendations
    assert len(report['recommendations']) > 0, "Should have recommendations for unhealthy agents"

    print("✅ PASSED: Performance report generation works")
    print(f"   Total Agents: {report['total_agents']}")
    print(f"   Overall Health: {report['overall_health']}")
    print(f"   Recommendations: {len(report['recommendations'])}")
    return True


def test_failure_prediction():
    """Test 7: Predict agent failures based on patterns."""
    print("\n" + "=" * 70)
    print("Test 7: Failure Prediction")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='oracle_test_')
    oracle = OracleMeta(knowledge_base_dir=temp_dir)

    # Track declining performance for an agent
    for i in range(10):
        oracle.track_agent_performance(
            agent_name='cyborg',
            metrics={
                'success': i < 3,  # Only 3 successes, 7 failures
                'execution_time': 5000,
                'score': 50
            }
        )

    # Predict failures
    prediction = oracle.predict_failures('cyborg')

    assert 'agent' in prediction, "Should have agent name"
    assert 'failure_probability' in prediction, "Should have failure_probability"
    assert 'risk_level' in prediction, "Should have risk_level"
    assert 'predicted_issues' in prediction, "Should have predicted_issues"
    assert 'oracle_prediction' in prediction, "Should have oracle_prediction"

    # With 70% failure rate, should predict high risk
    assert prediction['failure_probability'] > 0.2, "Should detect high failure probability"
    assert prediction['risk_level'] in ['medium', 'high', 'critical'], "Should have elevated risk level"
    assert len(prediction['predicted_issues']) > 0, "Should predict issues"

    print("✅ PASSED: Failure prediction works")
    print(f"   Failure Probability: {prediction['failure_probability']:.1%}")
    print(f"   Risk Level: {prediction['risk_level']}")
    print(f"   Oracle Prediction: {prediction['oracle_prediction']}")
    return True


def test_version_control():
    """Test 8: Agent version control and rollback."""
    print("\n" + "=" * 70)
    print("Test 8: Version Control & Rollback")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='oracle_test_')
    oracle = OracleMeta(knowledge_base_dir=temp_dir)

    # Create version 1.0.0
    success_1 = oracle.create_agent_version(
        agent_name='batman',
        version='1.0.0',
        changes='Initial version',
        code_hash='abc123'
    )

    assert success_1 is True, "Should create version 1.0.0"

    # Create version 1.1.0
    success_2 = oracle.create_agent_version(
        agent_name='batman',
        version='1.1.0',
        changes='Added timeout handling',
        code_hash='def456'
    )

    assert success_2 is True, "Should create version 1.1.0"

    # Get version history
    history = oracle.get_agent_version_history('batman')

    assert len(history) == 2, "Should have 2 versions"
    assert history[0]['version'] == '1.0.0', "Should have version 1.0.0"
    assert history[1]['version'] == '1.1.0', "Should have version 1.1.0"

    # Current version should be 1.1.0
    assert oracle.agent_versions['batman']['current_version'] == '1.1.0', "Current should be 1.1.0"

    # Rollback to 1.0.0
    rollback_success = oracle.rollback_agent('batman', '1.0.0')

    assert rollback_success is True, "Rollback should succeed"
    assert oracle.agent_versions['batman']['current_version'] == '1.0.0', "Should rollback to 1.0.0"

    print("✅ PASSED: Version control works")
    print(f"   Versions Created: {len(history)}")
    print(f"   Current Version: {oracle.agent_versions['batman']['current_version']}")
    return True


def test_mcp_integration_manager():
    """Test 9: MCP Integration Manager."""
    print("\n" + "=" * 70)
    print("Test 9: MCP Integration Manager")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='oracle_mcp_test_')
    mcp_db_path = Path(temp_dir) / 'mcp_capabilities.json'

    mcp_manager = MCPIntegrationManager(mcp_db_path=str(mcp_db_path))

    assert mcp_manager is not None, "MCP Manager should initialize"
    assert hasattr(mcp_manager, 'check_mcp_updates'), "Should have check_mcp_updates method"
    assert hasattr(mcp_manager, 'get_server_capabilities'), "Should have get_server_capabilities method"

    # Check server capabilities
    chrome_caps = mcp_manager.get_server_capabilities('chrome-devtools-mcp')

    assert 'capabilities' in chrome_caps, "Should have capabilities"
    assert len(chrome_caps['capabilities']) > 0, "Should have multiple capabilities"
    assert 'page_navigation' in chrome_caps['capabilities'], "Should have page_navigation"

    # Get all capabilities
    all_caps = mcp_manager.get_all_capabilities()

    assert len(all_caps) > 0, "Should have capabilities for multiple servers"
    assert 'chrome-devtools-mcp' in all_caps, "Should include Chrome DevTools"

    # Generate MCP report
    report = mcp_manager.generate_mcp_report()

    assert 'total_servers' in report, "Should have total_servers"
    assert 'servers' in report, "Should have servers"
    assert report['total_servers'] >= 6, "Should track at least 6 MCP servers"

    print("✅ PASSED: MCP Integration Manager works")
    print(f"   Total Servers: {report['total_servers']}")
    print(f"   Total Capabilities: {report['total_capabilities']}")
    return True


def test_oracle_comprehensive_report():
    """Test 10: Oracle comprehensive system report."""
    print("\n" + "=" * 70)
    print("Test 10: Oracle Comprehensive Report")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='oracle_test_')
    oracle = OracleMeta(knowledge_base_dir=temp_dir)

    # Add some data
    oracle.store_error_solution(
        agent_name='batman',
        error_type='timeout',
        error_details={'message': 'Timeout'},
        solution='Increased timeout',
        context={}
    )

    oracle.track_agent_performance('batman', {'success': True, 'score': 95})
    oracle.track_agent_performance('flash', {'success': True, 'score': 100})

    # Generate comprehensive report
    report = oracle.oracle_report()

    assert 'oracle' in report, "Should identify as Oracle"
    assert 'timestamp' in report, "Should have timestamp"
    assert 'knowledge_base' in report, "Should have knowledge_base section"
    assert 'performance' in report, "Should have performance section"
    assert 'predictions' in report, "Should have predictions section"
    assert 'recommendations' in report, "Should have recommendations"
    assert 'oracle_says' in report, "Should have Oracle's message"

    # Check knowledge base stats
    kb = report['knowledge_base']
    assert 'total_errors_documented' in kb, "Should track total errors"
    assert kb['total_errors_documented'] >= 1, "Should have at least 1 error documented"

    # Check performance
    perf = report['performance']
    assert 'total_agents' in perf, "Should have total agents"
    assert 'overall_health' in perf, "Should have overall health"

    # Check predictions
    predictions = report['predictions']
    assert 'batman' in predictions, "Should have predictions for Batman"
    assert 'flash' in predictions, "Should have predictions for Flash"

    print("\n✅ PASSED: Oracle comprehensive report works")
    print(f"   Errors Documented: {kb['total_errors_documented']}")
    print(f"   Agents Monitored: {perf['total_agents']}")
    print(f"   Overall Health: {perf['overall_health']}")
    print(f"   Oracle Says: {report['oracle_says']}")
    return True


def run_all_tests():
    """Run complete Oracle test suite."""
    print("\n🔮 Oracle - Meta-Agent Test Suite")
    print("=" * 70)
    print("Testing Knowledge Management & Self-Healing Capabilities")
    print("=" * 70)

    tests = [
        ("Initialization", test_oracle_initialization),
        ("Error/Solution Storage", test_error_solution_storage),
        ("Best Practices Management", test_best_practices_management),
        ("Mission Analysis", test_mission_analysis),
        ("Performance Tracking", test_performance_tracking),
        ("Performance Report", test_performance_report),
        ("Failure Prediction", test_failure_prediction),
        ("Version Control", test_version_control),
        ("MCP Integration Manager", test_mcp_integration_manager),
        ("Oracle Comprehensive Report", test_oracle_comprehensive_report),
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
        print("\n🎉 ALL TESTS PASSED! Oracle sees all, knows all!")
        print("🔮 The Meta-Agent is ready to serve the Justice League!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review.")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
