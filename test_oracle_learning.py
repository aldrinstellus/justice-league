"""
🧪 Oracle Learning & Knowledge Sharing Test Suite

Comprehensive testing for Oracle's learning capabilities:
- Cross-Agent Learning
- Pattern Recognition
- Standards Enforcement

Week 5: Learning & Knowledge Sharing
"""

import sys
import tempfile
import shutil
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.oracle_learning.cross_agent_learning import CrossAgentLearning, KnowledgeTransferability
from core.oracle_learning.pattern_recognition import PatternRecognition, PatternType
from core.oracle_learning.standards_enforcement import StandardsEnforcement, ComplianceLevel, StandardCategory


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


def test_cross_agent_learning_initialization():
    """Test 1: Cross-agent learning initialization"""
    print_test_header(1, "Cross-Agent Learning Initialization")

    try:
        temp_dir = tempfile.mkdtemp(prefix='cross_learning_test_')

        # Create required files
        errors_db = Path(temp_dir) / 'errors_solutions.json'
        errors_db.write_text(json.dumps({}))

        learning = CrossAgentLearning(str(temp_dir))

        assert learning is not None, "Learning system should be initialized"
        assert learning.learning_db.exists(), "Learning database should exist"
        assert len(learning.AGENT_SIMILARITIES) > 0, "Should have agent similarity matrix"
        assert len(learning.UNIVERSAL_PATTERNS) > 0, "Should have universal patterns"

        print_test_result("Cross-Agent Learning Initialization", True,
                         f"Initialized with {len(learning.AGENT_SIMILARITIES)} agent relationships")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Cross-Agent Learning Initialization", False, str(e))


def test_find_transferable_solutions():
    """Test 2: Find transferable solutions from other agents"""
    print_test_header(2, "Find Transferable Solutions")

    try:
        temp_dir = tempfile.mkdtemp(prefix='transferable_test_')

        # Create errors database with solutions from different agents
        errors_db_data = {
            'ERR-001': {
                'agent': 'batman',
                'error_type': 'timeout',
                'solution': 'Increased timeout from 5s to 30s',
                'success_rate': 1.0,
                'times_encountered': 5
            },
            'ERR-002': {
                'agent': 'green_lantern',
                'error_type': 'timeout',
                'solution': 'Added retry logic with exponential backoff',
                'success_rate': 0.95,
                'times_encountered': 3
            },
            'ERR-003': {
                'agent': 'flash',
                'error_type': 'performance',
                'solution': 'Added caching layer',
                'success_rate': 1.0,
                'times_encountered': 2
            }
        }

        errors_db = Path(temp_dir) / 'errors_solutions.json'
        errors_db.write_text(json.dumps(errors_db_data))

        learning = CrossAgentLearning(str(temp_dir))

        # Find timeout solutions for aquaman
        transferable = learning.find_transferable_solutions('aquaman', 'timeout', {})

        assert len(transferable) > 0, "Should find transferable solutions"

        # Check transferability assessment
        assert all('transferability' in sol for sol in transferable), "All should have transferability level"
        assert all('confidence' in sol for sol in transferable), "All should have confidence score"

        # Check sorting (highest confidence first)
        for i in range(len(transferable) - 1):
            assert transferable[i]['confidence'] >= transferable[i + 1]['confidence'], "Should be sorted by confidence"

        print_test_result("Find Transferable Solutions", True,
                         f"Found {len(transferable)} transferable solutions with confidence scores")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Find Transferable Solutions", False, str(e))


def test_knowledge_transfer_recommendation():
    """Test 3: Generate knowledge transfer recommendations"""
    print_test_header(3, "Knowledge Transfer Recommendations")

    try:
        temp_dir = tempfile.mkdtemp(prefix='recommendation_test_')

        # Create errors database
        errors_db_data = {
            'ERR-001': {
                'agent': 'batman',
                'error_type': 'timeout',
                'solution': 'Increased timeout to 30s',
                'success_rate': 1.0,
                'times_encountered': 5
            }
        }

        errors_db = Path(temp_dir) / 'errors_solutions.json'
        errors_db.write_text(json.dumps(errors_db_data))

        learning = CrossAgentLearning(str(temp_dir))

        issue = {
            'type': 'timeout',
            'severity': 'high',
            'message': 'Request timed out'
        }

        recommendation = learning.recommend_knowledge_transfer('cyborg', issue)

        assert recommendation is not None, "Should generate recommendation"
        assert 'recommendation_id' in recommendation, "Should have recommendation ID"
        assert recommendation['target_agent'] == 'cyborg', "Should target correct agent"
        assert 'recommended_action' in recommendation, "Should have recommended action"

        if recommendation['transferable_solutions']:
            assert 'adaptation_steps' in recommendation['recommended_action'], "Should have adaptation steps"

        print_test_result("Knowledge Transfer Recommendations", True,
                         f"Generated recommendation with {len(recommendation.get('transferable_solutions', []))} solutions")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Knowledge Transfer Recommendations", False, str(e))


def test_pattern_recognition_initialization():
    """Test 4: Pattern recognition initialization"""
    print_test_header(4, "Pattern Recognition Initialization")

    try:
        temp_dir = tempfile.mkdtemp(prefix='pattern_test_')

        # Create required files
        (Path(temp_dir) / 'errors_solutions.json').write_text(json.dumps({}))
        (Path(temp_dir) / 'agent_metrics.json').write_text(json.dumps({}))

        pattern_engine = PatternRecognition(str(temp_dir))

        assert pattern_engine is not None, "Pattern engine should be initialized"
        assert pattern_engine.patterns_db.exists(), "Patterns database should exist"
        assert pattern_engine.MIN_PATTERN_OCCURRENCES > 0, "Should have minimum occurrences threshold"

        print_test_result("Pattern Recognition Initialization", True,
                         f"Initialized with min {pattern_engine.MIN_PATTERN_OCCURRENCES} occurrences for pattern detection")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Pattern Recognition Initialization", False, str(e))


def test_error_cluster_detection():
    """Test 5: Detect error clusters"""
    print_test_header(5, "Error Cluster Detection")

    try:
        temp_dir = tempfile.mkdtemp(prefix='cluster_test_')

        # Create errors database with clustered errors
        errors_db_data = {
            'ERR-001': {'agent': 'batman', 'error_type': 'timeout', 'times_encountered': 3, 'success_rate': 0.8},
            'ERR-002': {'agent': 'cyborg', 'error_type': 'timeout', 'times_encountered': 2, 'success_rate': 0.9},
            'ERR-003': {'agent': 'aquaman', 'error_type': 'timeout', 'times_encountered': 4, 'success_rate': 0.7},
            'ERR-004': {'agent': 'flash', 'error_type': 'network', 'times_encountered': 1, 'success_rate': 1.0},
        }

        (Path(temp_dir) / 'errors_solutions.json').write_text(json.dumps(errors_db_data))
        (Path(temp_dir) / 'agent_metrics.json').write_text(json.dumps({}))

        pattern_engine = PatternRecognition(str(temp_dir))
        analysis = pattern_engine.analyze_all_patterns()

        # Should detect timeout cluster
        clusters = [p for p in analysis['patterns_detected'] if p['pattern_type'] == PatternType.ERROR_CLUSTER]

        assert len(clusters) > 0, "Should detect error clusters"

        timeout_cluster = next((c for c in clusters if c['error_type'] == 'timeout'), None)
        assert timeout_cluster is not None, "Should detect timeout cluster"
        assert timeout_cluster['cluster_size'] >= 3, "Timeout cluster should have 3+ errors"
        assert len(timeout_cluster['affected_agents']) >= 3, "Should affect multiple agents"

        print_test_result("Error Cluster Detection", True,
                         f"Detected {len(clusters)} clusters, timeout cluster affects {len(timeout_cluster['affected_agents'])} agents")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Error Cluster Detection", False, str(e))


def test_temporal_pattern_detection():
    """Test 6: Detect temporal patterns"""
    print_test_header(6, "Temporal Pattern Detection")

    try:
        temp_dir = tempfile.mkdtemp(prefix='temporal_test_')

        # Create metrics with degradation pattern
        metrics_data = {
            'batman': {
                'history': [
                    {'success': True, 'timestamp': '2025-01-01T10:00:00'},
                    {'success': True, 'timestamp': '2025-01-01T10:01:00'},
                    {'success': True, 'timestamp': '2025-01-01T10:02:00'},
                    {'success': True, 'timestamp': '2025-01-01T10:03:00'},
                    {'success': True, 'timestamp': '2025-01-01T10:04:00'},
                    # Degradation starts
                    {'success': False, 'timestamp': '2025-01-01T10:05:00'},
                    {'success': False, 'timestamp': '2025-01-01T10:06:00'},
                    {'success': False, 'timestamp': '2025-01-01T10:07:00'},
                    {'success': False, 'timestamp': '2025-01-01T10:08:00'},
                    {'success': False, 'timestamp': '2025-01-01T10:09:00'},
                ]
            }
        }

        (Path(temp_dir) / 'errors_solutions.json').write_text(json.dumps({}))
        (Path(temp_dir) / 'agent_metrics.json').write_text(json.dumps(metrics_data))

        pattern_engine = PatternRecognition(str(temp_dir))
        analysis = pattern_engine.analyze_all_patterns()

        # Should detect degradation
        temporal = [p for p in analysis['patterns_detected'] if p['pattern_type'] == PatternType.TEMPORAL]

        assert len(temporal) > 0, "Should detect temporal patterns"

        degradation = next((t for t in temporal if t.get('trend') == 'degradation'), None)
        assert degradation is not None, "Should detect degradation pattern"
        assert degradation['severity'] == 'high', "Degradation should be high severity"

        print_test_result("Temporal Pattern Detection", True,
                         f"Detected degradation from {degradation['older_success_rate']:.0%} to {degradation['recent_success_rate']:.0%}")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Temporal Pattern Detection", False, str(e))


def test_standards_enforcement_initialization():
    """Test 7: Standards enforcement initialization"""
    print_test_header(7, "Standards Enforcement Initialization")

    try:
        temp_dir = tempfile.mkdtemp(prefix='standards_test_')

        enforcement = StandardsEnforcement(str(temp_dir))

        assert enforcement is not None, "Enforcement engine should be initialized"
        assert enforcement.compliance_db.exists(), "Compliance database should exist"
        assert len(enforcement.STANDARDS) > 0, "Should have standards defined"

        # Check all categories
        assert StandardCategory.TESTING in enforcement.STANDARDS, "Should have testing standards"
        assert StandardCategory.PERFORMANCE in enforcement.STANDARDS, "Should have performance standards"
        assert StandardCategory.SECURITY in enforcement.STANDARDS, "Should have security standards"

        total_rules = sum(len(s['rules']) for s in enforcement.STANDARDS.values())

        print_test_result("Standards Enforcement Initialization", True,
                         f"Initialized with {len(enforcement.STANDARDS)} categories, {total_rules} total rules")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Standards Enforcement Initialization", False, str(e))


def test_agent_compliance_audit():
    """Test 8: Audit agent compliance"""
    print_test_header(8, "Agent Compliance Audit")

    try:
        temp_dir = tempfile.mkdtemp(prefix='compliance_test_')

        enforcement = StandardsEnforcement(str(temp_dir))

        # Mock agent metrics (good performance)
        agent_metrics = {
            'success_rate': 0.98,
            'avg_execution_time': 2000,  # 2 seconds
        }

        audit = enforcement.audit_agent_compliance('batman', agent_metrics)

        assert audit is not None, "Should generate audit report"
        assert 'compliance_level' in audit, "Should have compliance level"
        assert 'compliance_score' in audit, "Should have compliance score"
        assert 'violations' in audit, "Should have violations list"
        assert 'category_compliance' in audit, "Should have category compliance"

        # Check all categories audited
        assert len(audit['category_compliance']) > 0, "Should audit all categories"

        print_test_result("Agent Compliance Audit", True,
                         f"Compliance: {audit['compliance_level']} ({audit['compliance_score']:.1%}), " +
                         f"{len(audit['violations'])} violations")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Agent Compliance Audit", False, str(e))


def test_violation_detection():
    """Test 9: Detect compliance violations"""
    print_test_header(9, "Compliance Violation Detection")

    try:
        temp_dir = tempfile.mkdtemp(prefix='violation_test_')

        enforcement = StandardsEnforcement(str(temp_dir))

        # Mock agent with poor performance (violations)
        agent_metrics = {
            'success_rate': 0.70,  # Below 95% threshold
            'avg_execution_time': 8000,  # Above 5s threshold
        }

        audit = enforcement.audit_agent_compliance('flash', agent_metrics)

        # Should detect violations
        perf_violations = [v for v in audit['violations'] if v['category'] == StandardCategory.PERFORMANCE]

        assert len(perf_violations) > 0, "Should detect performance violations"

        # Should have high/critical severity
        severe_violations = [v for v in audit['violations'] if v['severity'] in ['high', 'critical']]
        assert len(severe_violations) > 0, "Should have severe violations"

        # Should generate recommendations
        assert len(audit['recommendations']) > 0, "Should generate recommendations"

        print_test_result("Compliance Violation Detection", True,
                         f"Detected {len(audit['violations'])} violations, {len(severe_violations)} severe")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Compliance Violation Detection", False, str(e))


def test_complete_learning_workflow():
    """Test 10: Complete learning and knowledge sharing workflow"""
    print_test_header(10, "Complete Learning Workflow (End-to-End)")

    try:
        temp_dir = tempfile.mkdtemp(prefix='learning_workflow_test_')

        # Step 1: Create initial knowledge base
        errors_db_data = {
            'ERR-001': {
                'agent': 'batman',
                'error_type': 'timeout',
                'solution': 'Increased timeout from 5s to 30s',
                'success_rate': 1.0,
                'times_encountered': 5
            },
            'ERR-002': {
                'agent': 'batman',
                'error_type': 'timeout',
                'solution': 'Added retry logic',
                'success_rate': 0.95,
                'times_encountered': 3
            },
            'ERR-003': {
                'agent': 'green_lantern',
                'error_type': 'timeout',
                'solution': 'Optimized query',
                'success_rate': 1.0,
                'times_encountered': 2
            }
        }

        (Path(temp_dir) / 'errors_solutions.json').write_text(json.dumps(errors_db_data))

        # Step 2: Cross-agent learning finds transferable solution
        learning = CrossAgentLearning(str(temp_dir))

        issue = {'type': 'timeout', 'severity': 'high'}
        recommendation = learning.recommend_knowledge_transfer('cyborg', issue)

        assert len(recommendation['transferable_solutions']) > 0, "Should find transferable solutions"

        # Step 3: Pattern recognition detects timeout cluster
        metrics_data = {
            'batman': {'history': [{'success': True}] * 10},
            'green_lantern': {'history': [{'success': True}] * 10}
        }
        (Path(temp_dir) / 'agent_metrics.json').write_text(json.dumps(metrics_data))

        pattern_engine = PatternRecognition(str(temp_dir))
        pattern_analysis = pattern_engine.analyze_all_patterns()

        timeout_cluster = next(
            (p for p in pattern_analysis['patterns_detected']
             if p.get('error_type') == 'timeout'),
            None
        )
        assert timeout_cluster is not None, "Should detect timeout cluster pattern"

        # Step 4: Standards enforcement audits compliance
        enforcement = StandardsEnforcement(str(temp_dir))

        good_metrics = {'success_rate': 0.98, 'avg_execution_time': 2000}
        audit = enforcement.audit_agent_compliance('batman', good_metrics)

        assert audit['compliance_level'] in [ComplianceLevel.FULLY_COMPLIANT, ComplianceLevel.MOSTLY_COMPLIANT], \
            "Good agent should be compliant"

        # Step 5: Record transfer attempt
        transfer_success = learning.record_transfer_attempt(
            recommendation['recommendation_id'],
            True,
            'Successfully applied solution',
            'Increased timeout to 30s'
        )
        assert transfer_success, "Should record transfer"

        # Get learning stats
        stats = learning.get_learning_stats()
        assert stats['total_transfers'] > 0, "Should have transfer records"

        print_test_result("Complete Learning Workflow", True,
                         "✅ Complete learning workflow executed successfully:\n" +
                         f"   1. ✅ Found {len(recommendation['transferable_solutions'])} transferable solutions\n" +
                         f"   2. ✅ Detected {len(pattern_analysis['patterns_detected'])} patterns\n" +
                         f"   3. ✅ Compliance audit: {audit['compliance_level']}\n" +
                         f"   4. ✅ Recorded knowledge transfer\n" +
                         f"   5. ✅ Learning stats: {stats['total_transfers']} transfers")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Complete Learning Workflow", False, str(e))


def main():
    """Run all tests"""
    print("=" * 70)
    print("🧪 Oracle Learning & Knowledge Sharing Test Suite")
    print("=" * 70)
    print("Testing Oracle's Learning Capabilities")
    print("Week 5: Learning & Knowledge Sharing")
    print("=" * 70)

    # Run all tests
    test_cross_agent_learning_initialization()
    test_find_transferable_solutions()
    test_knowledge_transfer_recommendation()
    test_pattern_recognition_initialization()
    test_error_cluster_detection()
    test_temporal_pattern_detection()
    test_standards_enforcement_initialization()
    test_agent_compliance_audit()
    test_violation_detection()
    test_complete_learning_workflow()

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
        print("\n🎉 ALL TESTS PASSED! Oracle's learning system is operational!")
        print("🧠 Cross-agent learning, pattern recognition, and standards enforcement verified!")
        return 0
    else:
        print(f"\n⚠️ {tests_failed} test(s) failed. Please review and fix.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
