"""
🧪 Oracle Self-Healing Test Suite

Comprehensive testing for Oracle's self-healing capabilities:
- Health Monitor
- Fix Proposal Engine
- Fix Testing Pipeline
- Approval Workflow

Week 4: Oracle Self-Healing Enhancement
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.oracle_self_healing.health_monitor import AgentHealthMonitor, HealthStatus, IssueType
from core.oracle_self_healing.fix_proposal_engine import FixProposalEngine, FixCategory
from core.oracle_self_healing.fix_testing_pipeline import FixTestingPipeline, TestResult
from core.oracle_self_healing.approval_workflow import ApprovalWorkflow, ApprovalStatus


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


def test_health_monitor_initialization():
    """Test 1: Health monitor initialization"""
    print_test_header(1, "Health Monitor Initialization")

    try:
        temp_dir = tempfile.mkdtemp(prefix='health_monitor_test_')
        metrics_path = Path(temp_dir) / 'agent_metrics.json'

        # Create mock metrics file
        import json
        with open(metrics_path, 'w') as f:
            json.dump({}, f)

        monitor = AgentHealthMonitor(str(metrics_path))

        assert monitor is not None, "Monitor should be initialized"
        assert monitor.health_reports_path.exists(), "Health reports database should exist"
        assert monitor.issues_db_path.exists(), "Issues database should exist"
        assert len(monitor.THRESHOLDS) > 0, "Thresholds should be defined"

        print_test_result("Health Monitor Initialization", True,
                         f"Monitor initialized with {len(monitor.THRESHOLDS)} thresholds")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Health Monitor Initialization", False, str(e))


def test_health_check_healthy_agent():
    """Test 2: Health check for healthy agent"""
    print_test_header(2, "Health Check - Healthy Agent")

    try:
        temp_dir = tempfile.mkdtemp(prefix='health_check_test_')
        metrics_path = Path(temp_dir) / 'agent_metrics.json'

        import json
        with open(metrics_path, 'w') as f:
            json.dump({}, f)

        monitor = AgentHealthMonitor(str(metrics_path))

        # Create healthy metrics (95%+ success rate)
        healthy_metrics = [
            {'success': True, 'execution_time': 1500, 'timestamp': '2025-01-01T10:00:00'}
            for _ in range(19)
        ]
        healthy_metrics.append(
            {'success': False, 'execution_time': 2000, 'timestamp': '2025-01-01T10:20:00'}
        )

        health_report = monitor.check_agent_health('batman', healthy_metrics)

        assert health_report['status'] == HealthStatus.HEALTHY.value, f"Should be healthy, got {health_report['status']}"
        assert health_report['metrics_summary']['success_rate'] == 0.95, "Success rate should be 95%"
        assert len(health_report['issues_detected']) == 0, "Should have no issues"

        print_test_result("Health Check - Healthy Agent", True,
                         f"Status: {health_report['status']}, Success rate: {health_report['metrics_summary']['success_rate']:.1%}")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Health Check - Healthy Agent", False, str(e))


def test_health_check_unhealthy_agent():
    """Test 3: Health check for unhealthy agent"""
    print_test_header(3, "Health Check - Unhealthy Agent")

    try:
        temp_dir = tempfile.mkdtemp(prefix='health_check_test_')
        metrics_path = Path(temp_dir) / 'agent_metrics.json'

        import json
        with open(metrics_path, 'w') as f:
            json.dump({}, f)

        monitor = AgentHealthMonitor(str(metrics_path))

        # Create unhealthy metrics (50% success rate)
        unhealthy_metrics = []
        for i in range(20):
            unhealthy_metrics.append({
                'success': i % 2 == 0,  # 50% success rate
                'execution_time': 8000,  # Slow
                'timestamp': f'2025-01-01T10:{i:02d}:00'
            })

        health_report = monitor.check_agent_health('flash', unhealthy_metrics)

        assert health_report['status'] in [HealthStatus.CRITICAL.value, HealthStatus.UNHEALTHY.value], \
            f"Should be critical/unhealthy, got {health_report['status']}"
        assert health_report['metrics_summary']['success_rate'] == 0.5, "Success rate should be 50%"
        assert len(health_report['issues_detected']) > 0, "Should have detected issues"

        print_test_result("Health Check - Unhealthy Agent", True,
                         f"Status: {health_report['status']}, Issues detected: {len(health_report['issues_detected'])}")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Health Check - Unhealthy Agent", False, str(e))


def test_issue_detection():
    """Test 4: Issue detection (consecutive failures)"""
    print_test_header(4, "Issue Detection - Consecutive Failures")

    try:
        temp_dir = tempfile.mkdtemp(prefix='issue_detection_test_')
        metrics_path = Path(temp_dir) / 'agent_metrics.json'

        import json
        with open(metrics_path, 'w') as f:
            json.dump({}, f)

        monitor = AgentHealthMonitor(str(metrics_path))

        # Create metrics with 5 consecutive failures at the end
        metrics = [
            {'success': True, 'execution_time': 1000, 'timestamp': f'2025-01-01T10:{i:02d}:00'}
            for i in range(15)
        ]
        metrics.extend([
            {'success': False, 'execution_time': 2000, 'error': 'Timeout', 'timestamp': f'2025-01-01T10:{i:02d}:00'}
            for i in range(15, 20)
        ])

        health_report = monitor.check_agent_health('aquaman', metrics)

        # Find consecutive failure issue
        has_consecutive_failure_issue = any(
            issue.get('type') == IssueType.HIGH_ERROR_RATE.value and 'consecutive' in issue.get('message', '').lower()
            for issue in health_report['issues_detected']
        )

        assert has_consecutive_failure_issue, "Should detect consecutive failures"
        assert health_report['status'] == HealthStatus.CRITICAL.value, "Should be critical"

        print_test_result("Issue Detection - Consecutive Failures", True,
                         f"Detected {len(health_report['issues_detected'])} issues")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Issue Detection - Consecutive Failures", False, str(e))


def test_fix_proposal_generation():
    """Test 5: Fix proposal generation"""
    print_test_header(5, "Fix Proposal Generation")

    try:
        temp_dir = tempfile.mkdtemp(prefix='fix_proposal_test_')
        kb_dir = Path(temp_dir)

        # Initialize knowledge base files
        import json
        (kb_dir / 'errors_solutions.json').write_text(json.dumps({}))
        (kb_dir / 'best_practices.json').write_text(json.dumps({}))

        engine = FixProposalEngine(str(kb_dir))

        # Create a test issue
        issue = {
            'type': 'timeout',
            'severity': 'high',
            'message': 'Request timed out after 5 seconds',
            'detected_at': '2025-01-01T10:00:00'
        }

        proposal = engine.generate_fix_proposal(issue, 'batman', {})

        assert proposal is not None, "Proposal should be generated"
        assert 'proposal_id' in proposal, "Should have proposal ID"
        assert len(proposal['fix_options']) > 0, f"Should have fix options, got {len(proposal['fix_options'])}"
        assert proposal['recommended_fix'] is not None, "Should have recommended fix"
        assert len(proposal['implementation_plan']) > 0, "Should have implementation plan"
        assert len(proposal['test_plan']) > 0, "Should have test plan"

        print_test_result("Fix Proposal Generation", True,
                         f"Generated {len(proposal['fix_options'])} fix options for timeout issue")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Fix Proposal Generation", False, str(e))


def test_fix_proposal_with_knowledge_base():
    """Test 6: Fix proposal using knowledge base"""
    print_test_header(6, "Fix Proposal with Knowledge Base")

    try:
        temp_dir = tempfile.mkdtemp(prefix='fix_kb_test_')
        kb_dir = Path(temp_dir)

        # Create knowledge base with past solution
        import json
        errors_db = {
            'ERR-001': {
                'agent': 'batman',
                'error_type': 'timeout',
                'error_details': {'message': 'Timeout after 5s'},
                'solution': 'Increased timeout to 30s and added retry logic',
                'success_rate': 1.0,
                'times_encountered': 5
            }
        }
        (kb_dir / 'errors_solutions.json').write_text(json.dumps(errors_db))
        (kb_dir / 'best_practices.json').write_text(json.dumps({}))

        engine = FixProposalEngine(str(kb_dir))

        issue = {
            'type': 'timeout',
            'severity': 'medium',
            'message': 'Request timed out',
            'detected_at': '2025-01-01T10:00:00'
        }

        proposal = engine.generate_fix_proposal(issue, 'batman', {})

        assert len(proposal['similar_past_issues']) > 0, "Should find similar past issues"
        # Check if any fix option is a proven solution
        has_proven_solution = any(
            opt.get('category') == 'proven_solution' for opt in proposal['fix_options']
        )
        assert has_proven_solution, "Should have proven solution from knowledge base"

        print_test_result("Fix Proposal with Knowledge Base", True,
                         f"Found {len(proposal['similar_past_issues'])} similar issues, recommended proven solution")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Fix Proposal with Knowledge Base", False, str(e))


def test_fix_testing_pipeline():
    """Test 7: Fix testing pipeline"""
    print_test_header(7, "Fix Testing Pipeline")

    try:
        temp_dir = tempfile.mkdtemp(prefix='fix_testing_test_')

        pipeline = FixTestingPipeline(str(temp_dir))

        # Create a mock proposal
        proposal = {
            'proposal_id': 'FIX-TEST001',
            'agent': 'batman',
            'issue': {'type': 'timeout'},
            'recommended_fix': {
                'name': 'Increase timeout',
                'implementation_steps': ['Step 1', 'Step 2']
            }
        }

        # Run tests (skip full suite for speed)
        test_report = pipeline.test_fix_proposal(proposal, run_all_tests=False)

        assert test_report is not None, "Test report should be generated"
        assert 'proposal_id' in test_report, "Should have proposal ID"
        assert test_report['total_tests'] > 0, "Should have run tests"
        assert 'test_stages' in test_report, "Should have test stages"
        assert len(test_report['test_stages']) > 0, "Should have at least one stage"

        print_test_result("Fix Testing Pipeline", True,
                         f"Ran {test_report['total_tests']} tests across {len(test_report['test_stages'])} stages")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Fix Testing Pipeline", False, str(e))


def test_approval_workflow_initialization():
    """Test 8: Approval workflow initialization"""
    print_test_header(8, "Approval Workflow Initialization")

    try:
        temp_dir = tempfile.mkdtemp(prefix='approval_test_')
        workflow_db = Path(temp_dir) / 'workflow.json'

        workflow = ApprovalWorkflow(str(workflow_db))

        assert workflow is not None, "Workflow should be initialized"
        assert workflow.workflow_db_path.exists(), "Workflow database should exist"

        # Check database structure
        import json
        with open(workflow.workflow_db_path, 'r') as f:
            data = json.load(f)

        assert 'workflows' in data, "Should have workflows"
        assert 'review_queue' in data, "Should have review queue"
        assert 'statistics' in data, "Should have statistics"

        print_test_result("Approval Workflow Initialization", True,
                         "Workflow initialized with proper database structure")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Approval Workflow Initialization", False, str(e))


def test_workflow_submission_and_approval():
    """Test 9: Workflow submission and approval"""
    print_test_header(9, "Workflow Submission and Approval")

    try:
        temp_dir = tempfile.mkdtemp(prefix='workflow_test_')
        workflow_db = Path(temp_dir) / 'workflow.json'

        workflow = ApprovalWorkflow(str(workflow_db))

        # Create mock proposal
        proposal = {
            'proposal_id': 'FIX-001',
            'agent': 'batman',
            'issue': {'type': 'timeout', 'severity': 'high'},
            'recommended_fix': {'name': 'Increase timeout'},
            'risk_assessment': {'overall_risk': 'low'},
            'estimated_effort': '30 minutes'
        }

        # Submit for review
        workflow_record = workflow.submit_for_review(proposal, 'Oracle', 'high')

        assert workflow_record is not None, "Workflow should be created"
        assert workflow_record['status'] == ApprovalStatus.PENDING_REVIEW, "Should be pending review"
        assert 'workflow_id' in workflow_record, "Should have workflow ID"

        # Assign reviewer
        success = workflow.assign_reviewer(workflow_record['workflow_id'], 'John Doe', 'developer')
        assert success, "Should assign reviewer"

        # Approve
        approved_workflow = workflow.approve_fix(
            workflow_record['workflow_id'],
            'John Doe',
            'Looks good to me'
        )

        assert approved_workflow['status'] == ApprovalStatus.APPROVED, "Should be approved"
        assert approved_workflow['approval_decision']['approved'] is True, "Should have approval decision"

        # Check review queue
        review_queue = workflow.get_review_queue()
        assert workflow_record['workflow_id'] not in [w['workflow_id'] for w in review_queue], \
            "Should be removed from review queue"

        # Check approved queue
        approved_queue = workflow.get_approved_queue()
        assert workflow_record['workflow_id'] in [w['workflow_id'] for w in approved_queue], \
            "Should be in approved queue"

        print_test_result("Workflow Submission and Approval", True,
                         f"Workflow {workflow_record['workflow_id']} approved successfully")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Workflow Submission and Approval", False, str(e))


def test_complete_self_healing_workflow():
    """Test 10: Complete self-healing workflow (end-to-end)"""
    print_test_header(10, "Complete Self-Healing Workflow (End-to-End)")

    try:
        temp_dir = tempfile.mkdtemp(prefix='complete_workflow_test_')

        # Step 1: Health monitoring detects issue
        metrics_path = Path(temp_dir) / 'agent_metrics.json'
        import json
        with open(metrics_path, 'w') as f:
            json.dump({}, f)

        monitor = AgentHealthMonitor(str(metrics_path))

        unhealthy_metrics = [
            {'success': False, 'execution_time': 8000, 'error': 'Timeout', 'timestamp': f'2025-01-01T10:{i:02d}:00'}
            for i in range(10)
        ]

        health_report = monitor.check_agent_health('batman', unhealthy_metrics)
        assert len(health_report['issues_detected']) > 0, "Should detect issues"

        # Step 2: Fix proposal engine generates fix
        kb_dir = Path(temp_dir)
        (kb_dir / 'errors_solutions.json').write_text(json.dumps({}))
        (kb_dir / 'best_practices.json').write_text(json.dumps({}))

        engine = FixProposalEngine(str(kb_dir))
        issue = health_report['issues_detected'][0]

        proposal = engine.generate_fix_proposal(issue, 'batman', {})
        assert proposal is not None, "Should generate fix proposal"
        assert len(proposal['fix_options']) > 0, "Should have fix options"

        # Step 3: Workflow approval
        workflow = ApprovalWorkflow(str(Path(temp_dir) / 'workflow.json'))

        workflow_record = workflow.submit_for_review(proposal, 'Oracle', 'high')
        assert workflow_record['status'] == ApprovalStatus.PENDING_REVIEW, "Should be pending review"

        workflow.assign_reviewer(workflow_record['workflow_id'], 'Tech Lead', 'tech_lead')
        approved = workflow.approve_fix(workflow_record['workflow_id'], 'Tech Lead', 'Approved')
        assert approved['status'] == ApprovalStatus.APPROVED, "Should be approved"

        # Step 4: Testing (simulated)
        pipeline = FixTestingPipeline(str(Path(temp_dir) / 'test_results'))
        test_report = pipeline.test_fix_proposal(proposal, run_all_tests=False)
        assert test_report is not None, "Should generate test report"

        # Step 5: Record implementation
        success = workflow.record_implementation(
            workflow_record['workflow_id'],
            'Developer',
            True,
            'Fix implemented successfully',
            test_report
        )
        assert success, "Should record implementation"

        # Step 6: Verify fix
        success = workflow.verify_fix(
            workflow_record['workflow_id'],
            'QA Lead',
            True,
            'Fix verified - issue resolved'
        )
        assert success, "Should verify fix"

        # Get final workflow state
        final_workflow = workflow.get_workflow_by_id(workflow_record['workflow_id'])
        assert final_workflow['status'] == ApprovalStatus.VERIFIED, "Should be verified"

        print_test_result("Complete Self-Healing Workflow", True,
                         "✅ Complete self-healing workflow executed successfully:\n" +
                         "   1. ✅ Health monitor detected issue\n" +
                         "   2. ✅ Fix proposal generated\n" +
                         "   3. ✅ Workflow approved\n" +
                         "   4. ✅ Tests executed\n" +
                         "   5. ✅ Implementation recorded\n" +
                         "   6. ✅ Fix verified")

        shutil.rmtree(temp_dir)

    except Exception as e:
        print_test_result("Complete Self-Healing Workflow", False, str(e))


def main():
    """Run all tests"""
    print("=" * 70)
    print("🧪 Oracle Self-Healing Test Suite")
    print("=" * 70)
    print("Testing Oracle's Self-Healing Capabilities")
    print("Week 4: Self-Healing Enhancement")
    print("=" * 70)

    # Run all tests
    test_health_monitor_initialization()
    test_health_check_healthy_agent()
    test_health_check_unhealthy_agent()
    test_issue_detection()
    test_fix_proposal_generation()
    test_fix_proposal_with_knowledge_base()
    test_fix_testing_pipeline()
    test_approval_workflow_initialization()
    test_workflow_submission_and_approval()
    test_complete_self_healing_workflow()

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
        print("\n🎉 ALL TESTS PASSED! Oracle's self-healing system is operational!")
        print("🏥 Health monitoring, fix proposals, testing, and approval workflow verified!")
        return 0
    else:
        print(f"\n⚠️ {tests_failed} test(s) failed. Please review and fix.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
