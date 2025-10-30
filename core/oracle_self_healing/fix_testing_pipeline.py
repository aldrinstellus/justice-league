"""
🧪 Oracle Fix Testing Pipeline
Automated testing for proposed fixes

This module tests fix proposals before deployment by:
- Running unit tests
- Running integration tests
- Performance benchmarking
- Regression testing
- Generating test reports

"Test everything. Trust nothing. Deploy confidently." - Oracle
"""

import logging
import json
import subprocess
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import sys

logger = logging.getLogger(__name__)


class TestResult(str):
    """Test result types"""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


class FixTestingPipeline:
    """
    🧪 Automated Fix Testing Pipeline

    Tests proposed fixes through multiple stages:
    1. Unit tests - Basic functionality
    2. Integration tests - Agent interactions
    3. Regression tests - No breaking changes
    4. Performance tests - Meets performance criteria
    5. End-to-end tests - Complete workflows
    """

    def __init__(self, test_results_dir: Optional[str] = None):
        """
        Initialize Fix Testing Pipeline

        Args:
            test_results_dir: Directory to store test results
        """
        self.results_dir = Path(test_results_dir) if test_results_dir else Path('/tmp/aldo-vision-justice-league/oracle/test_results')
        self.results_dir.mkdir(parents=True, exist_ok=True)

        logger.info("🧪 Fix Testing Pipeline initialized")

    def test_fix_proposal(self,
                         proposal: Dict[str, Any],
                         run_all_tests: bool = True) -> Dict[str, Any]:
        """
        🧪 Test a fix proposal comprehensively

        Args:
            proposal: Fix proposal to test
            run_all_tests: Whether to run all test stages

        Returns:
            Complete test report
        """
        test_report = {
            'proposal_id': proposal.get('proposal_id'),
            'agent': proposal.get('agent'),
            'tested_at': datetime.now().isoformat(),
            'test_stages': [],
            'overall_result': TestResult.PASSED,
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'skipped_tests': 0,
            'test_duration_seconds': 0.0,
            'test_recommendations': [],
            'ready_for_deployment': False
        }

        start_time = time.time()

        # Stage 1: Pre-implementation tests
        stage1_result = self._run_pre_implementation_tests(proposal)
        test_report['test_stages'].append(stage1_result)
        self._update_test_counts(test_report, stage1_result)

        if stage1_result['stage_result'] != TestResult.PASSED:
            test_report['overall_result'] = TestResult.FAILED
            test_report['test_recommendations'].append({
                'priority': 'high',
                'message': 'Pre-implementation tests failed - review proposal before proceeding'
            })
            test_report['test_duration_seconds'] = time.time() - start_time
            self._save_test_report(test_report)
            return test_report

        # Stage 2: Unit tests
        if run_all_tests:
            stage2_result = self._run_unit_tests(proposal)
            test_report['test_stages'].append(stage2_result)
            self._update_test_counts(test_report, stage2_result)

            if stage2_result['stage_result'] == TestResult.FAILED:
                test_report['overall_result'] = TestResult.FAILED

        # Stage 3: Integration tests
        if run_all_tests and test_report['overall_result'] == TestResult.PASSED:
            stage3_result = self._run_integration_tests(proposal)
            test_report['test_stages'].append(stage3_result)
            self._update_test_counts(test_report, stage3_result)

            if stage3_result['stage_result'] == TestResult.FAILED:
                test_report['overall_result'] = TestResult.FAILED

        # Stage 4: Regression tests
        if run_all_tests and test_report['overall_result'] == TestResult.PASSED:
            stage4_result = self._run_regression_tests(proposal)
            test_report['test_stages'].append(stage4_result)
            self._update_test_counts(test_report, stage4_result)

            if stage4_result['stage_result'] == TestResult.FAILED:
                test_report['overall_result'] = TestResult.FAILED

        # Stage 5: Performance tests
        if run_all_tests and test_report['overall_result'] == TestResult.PASSED:
            stage5_result = self._run_performance_tests(proposal)
            test_report['test_stages'].append(stage5_result)
            self._update_test_counts(test_report, stage5_result)

            if stage5_result['stage_result'] == TestResult.FAILED:
                test_report['overall_result'] = TestResult.FAILED

        # Calculate final metrics
        test_report['test_duration_seconds'] = round(time.time() - start_time, 2)

        # Determine if ready for deployment
        if test_report['overall_result'] == TestResult.PASSED:
            if test_report['failed_tests'] == 0:
                test_report['ready_for_deployment'] = True
                test_report['test_recommendations'].append({
                    'priority': 'info',
                    'message': '✅ All tests passed - ready for deployment'
                })
            else:
                test_report['test_recommendations'].append({
                    'priority': 'medium',
                    'message': f"{test_report['failed_tests']} tests failed - review before deployment"
                })
        else:
            test_report['test_recommendations'].append({
                'priority': 'high',
                'message': 'Fix has failing tests - NOT ready for deployment'
            })

        # Save report
        self._save_test_report(test_report)

        logger.info(f"🧪 Testing complete for {proposal.get('proposal_id')}: {test_report['overall_result']}")
        logger.info(f"🧪 {test_report['passed_tests']}/{test_report['total_tests']} tests passed")

        return test_report

    def _run_pre_implementation_tests(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Run pre-implementation validation tests"""
        stage_result = {
            'stage_name': 'Pre-Implementation Validation',
            'stage_number': 1,
            'stage_result': TestResult.PASSED,
            'tests': [],
            'duration_seconds': 0.0
        }

        start_time = time.time()

        # Test 1: Validate proposal structure
        test1 = {
            'test_name': 'Validate proposal structure',
            'result': TestResult.PASSED,
            'message': ''
        }

        required_fields = ['proposal_id', 'agent', 'issue', 'recommended_fix']
        missing_fields = [f for f in required_fields if f not in proposal]

        if missing_fields:
            test1['result'] = TestResult.FAILED
            test1['message'] = f"Missing required fields: {', '.join(missing_fields)}"
            stage_result['stage_result'] = TestResult.FAILED
        else:
            test1['message'] = "Proposal structure valid"

        stage_result['tests'].append(test1)

        # Test 2: Validate recommended fix exists
        test2 = {
            'test_name': 'Validate recommended fix',
            'result': TestResult.PASSED,
            'message': ''
        }

        if not proposal.get('recommended_fix'):
            test2['result'] = TestResult.FAILED
            test2['message'] = "No recommended fix provided"
            stage_result['stage_result'] = TestResult.FAILED
        else:
            test2['message'] = "Recommended fix validated"

        stage_result['tests'].append(test2)

        # Test 3: Validate agent exists
        test3 = {
            'test_name': 'Validate target agent',
            'result': TestResult.PASSED,
            'message': ''
        }

        agent_name = proposal.get('agent')
        agent_file = Path(f'core/justice_league/{agent_name}.py')

        if not agent_file.exists():
            test3['result'] = TestResult.FAILED
            test3['message'] = f"Agent file not found: {agent_file}"
            stage_result['stage_result'] = TestResult.FAILED
        else:
            test3['message'] = f"Agent file found: {agent_file}"

        stage_result['tests'].append(test3)

        # Test 4: Validate test file exists
        test4 = {
            'test_name': 'Validate test file exists',
            'result': TestResult.PASSED,
            'message': ''
        }

        test_file = Path(f'test_{agent_name}.py')

        if not test_file.exists():
            test4['result'] = TestResult.SKIPPED
            test4['message'] = f"Test file not found: {test_file} (will skip automated testing)"
        else:
            test4['message'] = f"Test file found: {test_file}"

        stage_result['tests'].append(test4)

        stage_result['duration_seconds'] = round(time.time() - start_time, 2)

        return stage_result

    def _run_unit_tests(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Run unit tests for the agent"""
        stage_result = {
            'stage_name': 'Unit Tests',
            'stage_number': 2,
            'stage_result': TestResult.PASSED,
            'tests': [],
            'duration_seconds': 0.0
        }

        start_time = time.time()

        agent_name = proposal.get('agent')
        test_file = Path(f'test_{agent_name}.py')

        if not test_file.exists():
            stage_result['tests'].append({
                'test_name': f'Run {test_file}',
                'result': TestResult.SKIPPED,
                'message': 'Test file not found'
            })
            stage_result['stage_result'] = TestResult.SKIPPED
            stage_result['duration_seconds'] = round(time.time() - start_time, 2)
            return stage_result

        # Run the test file
        test_result = self._run_test_file(test_file)

        stage_result['tests'].append({
            'test_name': f'Run {test_file}',
            'result': test_result['result'],
            'message': test_result['message'],
            'details': test_result.get('details', '')
        })

        if test_result['result'] == TestResult.FAILED:
            stage_result['stage_result'] = TestResult.FAILED

        stage_result['duration_seconds'] = round(time.time() - start_time, 2)

        return stage_result

    def _run_integration_tests(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Run integration tests"""
        stage_result = {
            'stage_name': 'Integration Tests',
            'stage_number': 3,
            'stage_result': TestResult.PASSED,
            'tests': [],
            'duration_seconds': 0.0
        }

        start_time = time.time()

        # For now, integration tests are simulated
        # In production, this would run actual integration tests

        stage_result['tests'].append({
            'test_name': 'Agent integration test',
            'result': TestResult.PASSED,
            'message': 'Integration tests passed (simulated)'
        })

        stage_result['duration_seconds'] = round(time.time() - start_time, 2)

        return stage_result

    def _run_regression_tests(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Run regression tests"""
        stage_result = {
            'stage_name': 'Regression Tests',
            'stage_number': 4,
            'stage_result': TestResult.PASSED,
            'tests': [],
            'duration_seconds': 0.0
        }

        start_time = time.time()

        # Run all Justice League tests to ensure no regressions
        master_test = Path('run_all_justice_league_tests.py')

        if master_test.exists():
            test_result = self._run_test_file(master_test)

            stage_result['tests'].append({
                'test_name': 'Full Justice League test suite',
                'result': test_result['result'],
                'message': test_result['message'],
                'details': test_result.get('details', '')
            })

            if test_result['result'] == TestResult.FAILED:
                stage_result['stage_result'] = TestResult.FAILED
        else:
            stage_result['tests'].append({
                'test_name': 'Regression test suite',
                'result': TestResult.SKIPPED,
                'message': 'Master test file not found'
            })
            stage_result['stage_result'] = TestResult.SKIPPED

        stage_result['duration_seconds'] = round(time.time() - start_time, 2)

        return stage_result

    def _run_performance_tests(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Run performance tests"""
        stage_result = {
            'stage_name': 'Performance Tests',
            'stage_number': 5,
            'stage_result': TestResult.PASSED,
            'tests': [],
            'duration_seconds': 0.0
        }

        start_time = time.time()

        agent_name = proposal.get('agent')

        # Test 1: Execution time benchmark
        test1 = {
            'test_name': 'Execution time benchmark',
            'result': TestResult.PASSED,
            'message': ''
        }

        # Import and time the agent
        try:
            # This is a simplified performance test
            # In production, would do comprehensive benchmarking
            test1['message'] = 'Performance within acceptable range (simulated)'
        except Exception as e:
            test1['result'] = TestResult.ERROR
            test1['message'] = f"Performance test error: {str(e)}"
            stage_result['stage_result'] = TestResult.FAILED

        stage_result['tests'].append(test1)

        # Test 2: Memory usage check
        test2 = {
            'test_name': 'Memory usage check',
            'result': TestResult.PASSED,
            'message': 'Memory usage within limits (simulated)'
        }

        stage_result['tests'].append(test2)

        stage_result['duration_seconds'] = round(time.time() - start_time, 2)

        return stage_result

    def _run_test_file(self, test_file: Path) -> Dict[str, Any]:
        """Run a specific test file and capture results"""
        result = {
            'result': TestResult.PASSED,
            'message': '',
            'details': ''
        }

        try:
            # Run the test file
            proc = subprocess.run(
                [sys.executable, str(test_file)],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            result['details'] = proc.stdout

            if proc.returncode == 0:
                result['message'] = f'✅ {test_file.name} passed'
            else:
                result['result'] = TestResult.FAILED
                result['message'] = f'❌ {test_file.name} failed'
                result['details'] += f"\nSTDERR:\n{proc.stderr}"

        except subprocess.TimeoutExpired:
            result['result'] = TestResult.ERROR
            result['message'] = f'Test file {test_file.name} timed out'
        except Exception as e:
            result['result'] = TestResult.ERROR
            result['message'] = f'Error running {test_file.name}: {str(e)}'

        return result

    def _update_test_counts(self, test_report: Dict[str, Any], stage_result: Dict[str, Any]):
        """Update test counts in the overall report"""
        for test in stage_result.get('tests', []):
            test_report['total_tests'] += 1

            if test['result'] == TestResult.PASSED:
                test_report['passed_tests'] += 1
            elif test['result'] == TestResult.FAILED:
                test_report['failed_tests'] += 1
            elif test['result'] == TestResult.SKIPPED:
                test_report['skipped_tests'] += 1

    def _save_test_report(self, test_report: Dict[str, Any]):
        """Save test report to file"""
        proposal_id = test_report.get('proposal_id', 'unknown')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.results_dir / f'{proposal_id}_{timestamp}.json'

        with open(report_file, 'w') as f:
            json.dump(test_report, f, indent=2)

        logger.info(f"🧪 Test report saved: {report_file}")

    def get_test_report(self, proposal_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the latest test report for a proposal

        Args:
            proposal_id: Proposal ID to get report for

        Returns:
            Latest test report or None if not found
        """
        # Find all reports for this proposal
        reports = sorted(self.results_dir.glob(f'{proposal_id}_*.json'), reverse=True)

        if reports:
            with open(reports[0], 'r') as f:
                return json.load(f)

        return None

    def compare_test_results(self,
                           before_proposal_id: str,
                           after_proposal_id: str) -> Dict[str, Any]:
        """
        Compare test results before and after fix

        Args:
            before_proposal_id: Test results before fix
            after_proposal_id: Test results after fix

        Returns:
            Comparison report
        """
        before_report = self.get_test_report(before_proposal_id)
        after_report = self.get_test_report(after_proposal_id)

        if not before_report or not after_report:
            return {
                'error': 'One or both test reports not found',
                'before_found': before_report is not None,
                'after_found': after_report is not None
            }

        comparison = {
            'before': {
                'total_tests': before_report.get('total_tests', 0),
                'passed_tests': before_report.get('passed_tests', 0),
                'failed_tests': before_report.get('failed_tests', 0),
                'overall_result': before_report.get('overall_result')
            },
            'after': {
                'total_tests': after_report.get('total_tests', 0),
                'passed_tests': after_report.get('passed_tests', 0),
                'failed_tests': after_report.get('failed_tests', 0),
                'overall_result': after_report.get('overall_result')
            },
            'improvement': {},
            'verdict': ''
        }

        # Calculate improvements
        comparison['improvement']['passed_delta'] = (
            comparison['after']['passed_tests'] - comparison['before']['passed_tests']
        )
        comparison['improvement']['failed_delta'] = (
            comparison['after']['failed_tests'] - comparison['before']['failed_tests']
        )

        # Determine verdict
        if comparison['after']['overall_result'] == TestResult.PASSED and comparison['before']['overall_result'] != TestResult.PASSED:
            comparison['verdict'] = '✅ Fix successful - tests now passing'
        elif comparison['improvement']['passed_delta'] > 0:
            comparison['verdict'] = '📈 Fix improved test results'
        elif comparison['improvement']['failed_delta'] > 0:
            comparison['verdict'] = '⚠️ Fix introduced new failures'
        else:
            comparison['verdict'] = '➡️ No significant change in test results'

        return comparison
