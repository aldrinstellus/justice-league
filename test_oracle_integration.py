"""
🧪 Oracle Integration Test Suite

Comprehensive testing for Oracle-Superman integration:
- Superman connector functionality
- Oracle coordinator capabilities
- Multi-agent task coordination
- Real-time monitoring and alerts
- Emergency response protocols
- End-to-end integration scenarios

Week 7: Oracle Testing & Integration
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.oracle_integration.superman_connector import SupermanConnector
from core.oracle_integration.oracle_coordinator import OracleCoordinator
from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl, VersionChangeType
from core.oracle_version_control.dependency_tracker import DependencyTracker
from core.oracle_self_healing.health_monitor import AgentHealthMonitor


# Test counters
tests_passed = 0
tests_failed = 0


def print_test_header(test_num, test_name):
    """Print test header"""
    print(f"\n{'=' * 70}")
    print(f"Test {test_num}: {test_name}")
    print(f"{'=' * 70}")


def print_test_result(test_name, passed, message=""):
    """Print test result"""
    global tests_passed, tests_failed

    if passed:
        tests_passed += 1
        print(f"✅ PASSED: {test_name}")
        if message:
            print(f"   {message}")
    else:
        tests_failed += 1
        print(f"❌ FAILED: {test_name}")
        if message:
            print(f"   {message}")


def test_superman_connector_initialization():
    """Test 1: Superman connector initialization"""
    print_test_header(1, "Superman Connector Initialization")

    try:
        temp_dir = tempfile.mkdtemp(prefix='superman_connector_test_')

        connector = SupermanConnector(temp_dir)

        assert connector is not None, "Connector should be initialized"
        assert connector.connection_db.exists(), "Connection database should exist"

        # Test heartbeat
        heartbeat = connector.heartbeat()
        assert heartbeat['status'] == 'connected', "Should be connected"
        assert heartbeat['oracle_online'], "Oracle should be online"

        print_test_result("Superman Connector Initialization", True,
                         "Connector initialized and heartbeat working")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Superman Connector Initialization", False, str(e))


def test_get_agent_health_summary():
    """Test 2: Get agent health summary"""
    print_test_header(2, "Get Agent Health Summary")

    try:
        temp_dir = tempfile.mkdtemp(prefix='health_summary_test_')

        connector = SupermanConnector(temp_dir)

        # Get health summary
        summary = connector.get_agent_health_summary()

        assert summary is not None, "Should return summary"
        assert 'total_agents' in summary, "Should have total agents count"
        assert summary['total_agents'] == 11, f"Should have 11 agents, got {summary['total_agents']}"
        assert 'healthy_agents' in summary, "Should have healthy count"
        assert 'health_percentage' in summary, "Should have health percentage"

        print_test_result("Get Agent Health Summary", True,
                         f"{summary['healthy_agents']}/{summary['total_agents']} agents healthy ({summary['health_percentage']:.1f}%)")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Get Agent Health Summary", False, str(e))


def test_get_agent_versions():
    """Test 3: Get agent versions"""
    print_test_header(3, "Get Agent Versions")

    try:
        temp_dir = tempfile.mkdtemp(prefix='versions_test_')

        connector = SupermanConnector(temp_dir)
        vc = EnhancedVersionControl(temp_dir, git_enabled=False)

        # Create some versions
        vc.create_version('batman', VersionChangeType.PATCH, 'Initial version')
        vc.create_version('superman', VersionChangeType.MINOR, 'Initial version')

        # Get versions through connector
        versions = connector.get_agent_versions()

        assert versions is not None, "Should return versions"
        assert 'batman' in versions, "Should have batman version"
        assert 'superman' in versions, "Should have superman version"
        assert versions['batman'] == '0.0.1', f"Batman should be v0.0.1, got {versions['batman']}"
        assert versions['superman'] == '0.1.0', f"Superman should be v0.1.0, got {versions['superman']}"

        print_test_result("Get Agent Versions", True,
                         f"Retrieved versions for {len(versions)} agents")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Get Agent Versions", False, str(e))


def test_request_version_update():
    """Test 4: Request version update through Superman"""
    print_test_header(4, "Request Version Update")

    try:
        temp_dir = tempfile.mkdtemp(prefix='version_update_test_')

        connector = SupermanConnector(temp_dir)

        # Request version update
        version = connector.request_version_update(
            'flash',
            'minor',
            'Added speed force analysis'
        )

        assert version is not None, "Should create version"
        assert version['version'] == '0.1.0', f"Should be v0.1.0, got {version['version']}"
        assert version['agent'] == 'flash', "Should be for flash"

        # Request another update
        version2 = connector.request_version_update(
            'flash',
            'major',
            'Changed API structure',
            breaking_changes=['analyze() signature changed']
        )

        assert version2['version'] == '1.0.0', f"Should be v1.0.0, got {version2['version']}"
        assert version2['migration_required'], "Should require migration"

        print_test_result("Request Version Update", True,
                         f"Created versions: {version['version']} → {version2['version']}")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Request Version Update", False, str(e))


def test_analyze_update_impact():
    """Test 5: Analyze update impact"""
    print_test_header(5, "Analyze Update Impact")

    try:
        temp_dir = tempfile.mkdtemp(prefix='impact_test_')

        connector = SupermanConnector(temp_dir)
        tracker = DependencyTracker(temp_dir)

        # Create dependency chain
        tracker.add_dependency('batman', 'oracle', '>=1.0.0')
        tracker.add_dependency('flash', 'batman', '>=1.0.0')
        tracker.add_dependency('aquaman', 'oracle', '>=1.0.0')

        # Analyze impact through connector
        impact = connector.analyze_update_impact('oracle', '2.0.0')

        assert impact is not None, "Should return impact analysis"
        assert 'total_affected' in impact, "Should have total affected"
        assert impact['total_affected'] >= 2, f"Should affect at least 2 agents, got {impact['total_affected']}"
        assert 'breaking_risk' in impact, "Should have risk assessment"

        print_test_result("Analyze Update Impact", True,
                         f"{impact['total_affected']} agents affected, risk: {impact['breaking_risk']}")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Analyze Update Impact", False, str(e))


def test_request_self_healing():
    """Test 6: Request self-healing"""
    print_test_header(6, "Request Self-Healing")

    try:
        temp_dir = tempfile.mkdtemp(prefix='healing_test_')

        connector = SupermanConnector(temp_dir)

        # Request healing
        result = connector.request_self_healing('green_lantern')

        assert result is not None, "Should return healing result"
        assert 'success' in result, "Should have success status"
        assert 'agent' in result, "Should have agent name"

        print_test_result("Request Self-Healing", True,
                         f"Healing result: {result['success']}, proposals: {result.get('proposals_generated', 0)}")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Request Self-Healing", False, str(e))


def test_get_dependency_graph():
    """Test 7: Get dependency graph"""
    print_test_header(7, "Get Dependency Graph")

    try:
        temp_dir = tempfile.mkdtemp(prefix='dep_graph_test_')

        connector = SupermanConnector(temp_dir)
        tracker = DependencyTracker(temp_dir)

        # Create dependencies
        tracker.add_dependency('batman', 'oracle', '>=1.0.0')
        tracker.add_dependency('superman', 'oracle', '>=1.0.0')
        tracker.add_dependency('flash', 'batman', '>=1.0.0')

        # Get graph through connector
        graph = connector.get_dependency_graph()

        assert graph is not None, "Should return graph"
        assert 'total_dependencies' in graph, "Should have total dependencies"
        assert graph['total_dependencies'] >= 3, f"Should have at least 3 dependencies, got {graph['total_dependencies']}"
        assert 'graph_text' in graph, "Should have text visualization"
        assert 'graph_mermaid' in graph, "Should have Mermaid visualization"

        print_test_result("Get Dependency Graph", True,
                         f"Graph with {graph['total_dependencies']} dependencies")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Get Dependency Graph", False, str(e))


def test_coordinate_multi_agent_task():
    """Test 8: Coordinate multi-agent task"""
    print_test_header(8, "Coordinate Multi-Agent Task")

    try:
        temp_dir = tempfile.mkdtemp(prefix='multi_agent_test_')

        connector = SupermanConnector(temp_dir)
        tracker = DependencyTracker(temp_dir)

        # Create dependency chain
        tracker.add_dependency('flash', 'batman', '>=1.0.0')
        tracker.add_dependency('aquaman', 'oracle', '>=1.0.0')

        # Coordinate task
        plan = connector.coordinate_multi_agent_task(
            'Analyze complex website',
            ['batman', 'flash', 'oracle'],
            'high'
        )

        assert plan is not None, "Should return coordination plan"
        assert 'execution_order' in plan, "Should have execution order"
        assert len(plan['execution_order']) == 3, f"Should have 3 agents, got {len(plan['execution_order'])}"
        assert 'agent_status' in plan, "Should have agent status"
        assert plan['priority'] == 'high', "Should have correct priority"

        print_test_result("Coordinate Multi-Agent Task", True,
                         f"Coordinated {len(plan['required_agents'])} agents, execution order: {plan['execution_order']}")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Coordinate Multi-Agent Task", False, str(e))


def test_oracle_coordinator_system_scan():
    """Test 9: Oracle coordinator system scan"""
    print_test_header(9, "Oracle Coordinator System Scan")

    try:
        temp_dir = tempfile.mkdtemp(prefix='system_scan_test_')

        coordinator = OracleCoordinator(temp_dir)

        # Perform system scan
        scan = coordinator.perform_system_scan()

        assert scan is not None, "Should return scan results"
        assert 'agents_scanned' in scan, "Should have agents scanned count"
        assert scan['agents_scanned'] == 11, f"Should scan 11 agents, got {scan['agents_scanned']}"
        assert 'health_issues' in scan, "Should have health issues"
        assert 'predictions' in scan, "Should have predictions"
        assert 'recommendations' in scan, "Should have recommendations"

        print_test_result("Oracle Coordinator System Scan", True,
                         f"Scanned {scan['agents_scanned']} agents, {len(scan['health_issues'])} issues, {len(scan['recommendations'])} recommendations")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Oracle Coordinator System Scan", False, str(e))


def test_coordinate_version_update():
    """Test 10: Coordinate version update"""
    print_test_header(10, "Coordinate Version Update")

    try:
        temp_dir = tempfile.mkdtemp(prefix='coord_update_test_')

        coordinator = OracleCoordinator(temp_dir)
        tracker = DependencyTracker(temp_dir)

        # Create dependency chain
        tracker.add_dependency('batman', 'oracle', '>=1.0.0')
        tracker.add_dependency('flash', 'batman', '>=1.0.0')
        tracker.add_dependency('superman', 'oracle', '>=1.0.0')

        # Coordinate update
        plan = coordinator.coordinate_version_update('oracle', '2.0.0')

        assert plan is not None, "Should return update plan"
        assert 'phases' in plan, "Should have update phases"
        assert len(plan['phases']) > 0, "Should have at least one phase"
        assert 'update_order' in plan, "Should have update order"
        assert 'total_affected' in plan, "Should have total affected"

        print_test_result("Coordinate Version Update", True,
                         f"{len(plan['phases'])} phases, {plan['total_affected']} agents affected")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Coordinate Version Update", False, str(e))


def test_generate_system_report():
    """Test 11: Generate system report"""
    print_test_header(11, "Generate System Report")

    try:
        temp_dir = tempfile.mkdtemp(prefix='system_report_test_')

        coordinator = OracleCoordinator(temp_dir)
        vc = EnhancedVersionControl(temp_dir, git_enabled=False)

        # Create some versions
        vc.create_version('batman', VersionChangeType.MINOR, 'v1')
        vc.create_version('superman', VersionChangeType.MINOR, 'v1')

        # Generate report
        report = coordinator.generate_system_report()

        assert report is not None, "Should return report"
        assert 'system_health' in report, "Should have system health"
        assert 'versions' in report, "Should have versions"
        assert 'dependencies' in report, "Should have dependencies"
        assert 'alerts' in report, "Should have alerts"
        assert report['oracle_status'] == 'operational', "Oracle should be operational"

        print_test_result("Generate System Report", True,
                         f"Report: {report['system_health']['healthy_agents']}/{report['system_health']['total_agents']} healthy, {len(report['versions'])} versions")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Generate System Report", False, str(e))


def test_emergency_rollback():
    """Test 12: Emergency rollback"""
    print_test_header(12, "Emergency Rollback")

    try:
        temp_dir = tempfile.mkdtemp(prefix='emergency_test_')

        connector = SupermanConnector(temp_dir)
        vc = EnhancedVersionControl(temp_dir, git_enabled=False)

        # Create versions
        vc.create_version('cyborg', VersionChangeType.PATCH, 'v1')
        vc.create_version('cyborg', VersionChangeType.PATCH, 'v2')
        vc.create_version('cyborg', VersionChangeType.PATCH, 'v3')

        # Emergency rollback
        rollback = connector.emergency_rollback('cyborg', 'Critical failure detected')

        assert rollback is not None, "Should return rollback result"
        assert 'emergency' in rollback, "Should be marked as emergency"
        assert rollback['emergency'] == True, "Should be emergency rollback"
        assert 'reason' in rollback, "Should have reason"
        assert 'to_version' in rollback, "Should have target version"

        print_test_result("Emergency Rollback", True,
                         f"Emergency rollback to v{rollback['to_version']}, reason: {rollback['reason']}")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Emergency Rollback", False, str(e))


def test_complete_integration_workflow():
    """Test 13: Complete integration workflow (end-to-end)"""
    print_test_header(13, "Complete Integration Workflow (End-to-End)")

    try:
        temp_dir = tempfile.mkdtemp(prefix='complete_integration_test_')

        # Step 1: Initialize both Superman connector and Oracle coordinator
        connector = SupermanConnector(temp_dir)
        coordinator = OracleCoordinator(temp_dir)

        # Step 2: Superman checks Oracle status
        status = connector.get_oracle_status()
        assert status['oracle_online'], "Oracle should be online"

        # Step 3: Oracle performs system scan
        scan = coordinator.perform_system_scan()
        assert scan['agents_scanned'] == 11, "Should scan all 11 agents"

        # Step 4: Superman requests version update
        version = connector.request_version_update(
            'wonder_woman',
            'minor',
            'Added new analysis capability'
        )
        assert version['version'] == '0.1.0', "Should create v0.1.0"

        # Step 5: Oracle coordinates the update
        vc = EnhancedVersionControl(temp_dir, git_enabled=False)
        tracker = DependencyTracker(temp_dir)
        tracker.add_dependency('flash', 'wonder_woman', '>=0.1.0')

        update_plan = coordinator.coordinate_version_update('wonder_woman', '0.2.0')
        assert len(update_plan['phases']) > 0, "Should have update phases"

        # Step 6: Superman gets health summary
        health = connector.get_agent_health_summary()
        assert health['total_agents'] == 11, "Should have 11 agents"

        # Step 7: Superman coordinates multi-agent task
        task_plan = connector.coordinate_multi_agent_task(
            'Comprehensive website analysis',
            ['batman', 'wonder_woman', 'flash'],
            'high'
        )
        assert len(task_plan['execution_order']) == 3, "Should have execution order"

        # Step 8: Oracle generates system report
        report = coordinator.generate_system_report()
        assert report['oracle_status'] == 'operational', "Oracle should be operational"

        # Step 9: Get dependency graph
        graph = connector.get_dependency_graph()
        assert 'total_dependencies' in graph, "Should have dependency graph"

        print_test_result("Complete Integration Workflow", True,
                         "✅ Complete workflow executed successfully:\n" +
                         f"   1. ✅ Oracle status: {status['oracle_online']}\n" +
                         f"   2. ✅ System scan: {scan['agents_scanned']} agents\n" +
                         f"   3. ✅ Version created: v{version['version']}\n" +
                         f"   4. ✅ Update plan: {len(update_plan['phases'])} phases\n" +
                         f"   5. ✅ Health check: {health['healthy_agents']}/{health['total_agents']} healthy\n" +
                         f"   6. ✅ Task coordination: {len(task_plan['execution_order'])} agents\n" +
                         f"   7. ✅ System report: {report['oracle_status']}\n" +
                         f"   8. ✅ Dependency graph: {graph['total_dependencies']} dependencies")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Complete Integration Workflow", False, str(e))


def main():
    """Run all tests"""
    print("=" * 70)
    print("🧪 Oracle Integration Test Suite")
    print("=" * 70)
    print("Testing Oracle-Superman Integration")
    print("Week 7: Oracle Testing & Integration")
    print("=" * 70)

    # Run all tests
    test_superman_connector_initialization()
    test_get_agent_health_summary()
    test_get_agent_versions()
    test_request_version_update()
    test_analyze_update_impact()
    test_request_self_healing()
    test_get_dependency_graph()
    test_coordinate_multi_agent_task()
    test_oracle_coordinator_system_scan()
    test_coordinate_version_update()
    test_generate_system_report()
    test_emergency_rollback()
    test_complete_integration_workflow()

    # Print summary
    print("\n" + "=" * 70)
    print("Test Suite Summary")
    print("=" * 70)
    total_tests = tests_passed + tests_failed
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {tests_passed}")
    print(f"❌ Failed: {tests_failed}")
    print(f"\nSuccess Rate: {(tests_passed / total_tests * 100):.1f}%")

    if tests_failed == 0:
        print("\n🎉 ALL TESTS PASSED! Oracle-Superman integration is operational!")
        print("🦸🔮 Superman and Oracle are working together perfectly!")
        return 0
    else:
        print(f"\n⚠️ {tests_failed} test(s) failed. Please review and fix.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
