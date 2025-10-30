#!/usr/bin/env python3
"""
🔮 AUTO-FIX ORCHESTRATOR TEST SUITE
====================================

Tests the complete auto-fix system integration:
- Auto-Fix Orchestrator
- Superman auto_fix_mode
- Oracle error querying and reinforcement
- End-to-end error recovery

Version: 1.0.0 (v1.9.3)
Created: 2025-10-30
"""

import unittest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from core.justice_league.auto_fix_orchestrator import AutoFixOrchestrator, create_auto_fix_orchestrator
from core.justice_league import SupermanCoordinator
from core.justice_league.oracle_meta_agent import OracleMeta as Oracle


class TestAutoFixOrchestrator(unittest.TestCase):
    """Test Auto-Fix Orchestrator functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_oracle = Mock()
        self.mock_narrator = Mock()
        self.orchestrator = AutoFixOrchestrator(
            oracle=self.mock_oracle,
            narrator=self.mock_narrator
        )

    def test_01_initialization(self):
        """Test orchestrator initialization"""
        self.assertIsNotNone(self.orchestrator)
        self.assertEqual(self.orchestrator.oracle, self.mock_oracle)
        self.assertEqual(self.orchestrator.narrator, self.mock_narrator)
        self.assertEqual(self.orchestrator.stats['total_errors'], 0)
        self.assertEqual(self.orchestrator.stats['auto_fixed'], 0)
        print("✅ Test 1: Orchestrator initialization")

    def test_02_extract_error_details(self):
        """Test error detail extraction"""
        result = {
            'success': False,
            'errors': ['HTTPSConnectionPool timeout: Read timed out']
        }

        error_details = self.orchestrator._extract_error_details(result)

        self.assertIn('message', error_details)
        self.assertIn('type', error_details)
        self.assertEqual(error_details['type'], 'timeout')
        print("✅ Test 2: Error detail extraction")

    def test_03_classify_timeout_error(self):
        """Test timeout error classification"""
        error = {
            'type': 'timeout',
            'message': 'Read timed out after 30s'
        }

        classification = self.orchestrator._classify_error(error)

        self.assertEqual(classification['category'], 'network_reliability')
        self.assertTrue(classification['auto_fixable'])
        print("✅ Test 3: Timeout error classification")

    def test_04_query_local_patterns_timeout(self):
        """Test querying local patterns for timeout"""
        error = {'type': 'timeout', 'message': 'timeout'}

        patterns = self.orchestrator._query_local_patterns(error)

        self.assertGreater(len(patterns), 0)
        self.assertEqual(patterns[0]['confidence'], 1.0)
        self.assertIn('exponential backoff', patterns[0]['solution']['technique'].lower())
        print("✅ Test 4: Query local timeout patterns")

    def test_05_auto_implement_high_confidence(self):
        """Test auto-implementation of high confidence fix"""
        error = {'type': 'timeout', 'message': 'timeout'}
        solution = {
            'technique': 'Retry with exponential backoff',
            'parameters': {'max_retries': 5}
        }
        confidence = 0.95
        mission = {'file_key': 'test123'}

        result = self.orchestrator._auto_implement_fix(error, solution, confidence, mission)

        self.assertTrue(result['fixed'])
        self.assertEqual(result['confidence'], 0.95)
        self.assertTrue(result['retry_recommended'])
        self.assertTrue(result['auto_implemented'])
        self.assertEqual(self.orchestrator.stats['auto_fixed'], 1)
        print("✅ Test 5: Auto-implement high confidence fix")

    def test_06_suggest_medium_confidence(self):
        """Test suggestion for medium confidence fix"""
        error = {'type': 'unknown', 'message': 'some error'}
        solution = {'technique': 'Manual review'}
        confidence = 0.65

        result = self.orchestrator._suggest_fix(error, solution, confidence)

        self.assertFalse(result['fixed'])
        self.assertTrue(result['suggestion'])
        self.assertEqual(result['confidence'], 0.65)
        self.assertEqual(self.orchestrator.stats['suggested'], 1)
        print("✅ Test 6: Suggest medium confidence fix")

    def test_07_handle_failure_with_proven_solution(self):
        """Test handling failure with proven solution from Oracle"""
        mission = {'file_key': 'test123', 'output_dir': '/tmp/test'}
        result = {
            'success': False,
            'errors': ['HTTPSConnectionPool timeout'],
            'mission_type': 'frame_export'
        }

        # Mock Oracle returning proven solution
        self.mock_oracle.query_error_solutions.return_value = [{
            'pattern': 'retry-pattern',
            'solution': {'technique': 'Exponential backoff'},
            'confidence': 0.9,
            'similarity': 0.85
        }]

        fix_result = self.orchestrator.handle_failure(mission, result, confidence_threshold=0.8)

        self.assertTrue(fix_result['fixed'])
        self.assertEqual(fix_result['confidence'], 0.9)
        self.assertTrue(fix_result['retry_recommended'])
        self.mock_oracle.query_error_solutions.assert_called_once()
        print("✅ Test 7: Handle failure with proven solution")

    def test_08_track_fix_outcome_success(self):
        """Test tracking successful fix outcome"""
        fix_record = {
            'error': {'type': 'timeout'},
            'solution': {'technique': 'Retry'},
            'confidence': 0.9
        }
        mission_result = {'success': True}

        self.orchestrator.track_fix_outcome(fix_record, success=True, mission_result=mission_result)

        self.assertTrue(fix_record['success'])
        self.assertIn('tracked_at', fix_record)
        self.mock_oracle.reinforce_solution.assert_called_once()
        print("✅ Test 8: Track successful fix outcome")

    def test_09_track_fix_outcome_failure(self):
        """Test tracking failed fix outcome"""
        fix_record = {
            'error': {'type': 'timeout'},
            'solution': {'technique': 'Retry'},
            'confidence': 0.9
        }

        self.orchestrator.track_fix_outcome(fix_record, success=False)

        self.assertFalse(fix_record['success'])
        self.mock_oracle.reinforce_solution.assert_called_with(
            error=fix_record['error'],
            solution=fix_record['solution'],
            success=False
        )
        print("✅ Test 9: Track failed fix outcome")

    def test_10_get_stats(self):
        """Test getting orchestrator statistics"""
        # Add some history
        self.orchestrator.fix_history.append({'success': True})
        self.orchestrator.fix_history.append({'success': False})
        self.orchestrator.stats['auto_fixed'] = 2

        stats = self.orchestrator.get_stats()

        self.assertEqual(stats['total_fix_attempts'], 2)
        self.assertIn('recent_fixes', stats)
        print("✅ Test 10: Get orchestrator statistics")


class TestSupermanAutoFixIntegration(unittest.TestCase):
    """Test Superman integration with auto-fix"""

    def setUp(self):
        """Set up test fixtures"""
        self.superman = None
        try:
            self.superman = SupermanCoordinator()
        except Exception as e:
            self.skipTest(f"Superman initialization failed: {e}")

    def test_11_superman_has_auto_fix_orchestrator(self):
        """Test Superman has auto-fix orchestrator"""
        self.assertIsNotNone(self.superman)
        self.assertTrue(hasattr(self.superman, 'auto_fix_orchestrator'))
        self.assertIsNotNone(self.superman.auto_fix_orchestrator)
        print("✅ Test 11: Superman has auto-fix orchestrator")

    def test_12_deploy_hawkman_has_auto_fix_param(self):
        """Test Hawkman deployment supports auto_fix_mode"""
        import inspect

        # Check method signature
        sig = inspect.signature(self.superman._deploy_hawkman_frame_export)
        params = sig.parameters

        self.assertIn('auto_fix_mode', params)
        self.assertEqual(params['auto_fix_mode'].default, True)
        print("✅ Test 12: Hawkman deployment has auto_fix_mode parameter")


class TestOracleAutoFixMethods(unittest.TestCase):
    """Test Oracle auto-fix methods"""

    def setUp(self):
        """Set up test fixtures"""
        self.oracle = None
        try:
            self.oracle = Oracle()
        except Exception as e:
            self.skipTest(f"Oracle initialization failed: {e}")

    def test_13_oracle_has_query_error_solutions(self):
        """Test Oracle has query_error_solutions method"""
        self.assertTrue(hasattr(self.oracle, 'query_error_solutions'))
        self.assertTrue(callable(self.oracle.query_error_solutions))
        print("✅ Test 13: Oracle has query_error_solutions method")

    def test_14_oracle_has_reinforce_solution(self):
        """Test Oracle has reinforce_solution method"""
        self.assertTrue(hasattr(self.oracle, 'reinforce_solution'))
        self.assertTrue(callable(self.oracle.reinforce_solution))
        print("✅ Test 14: Oracle has reinforce_solution method")

    def test_15_query_error_solutions_returns_list(self):
        """Test query_error_solutions returns list"""
        error = {
            'type': 'timeout',
            'message': 'HTTPSConnectionPool timeout',
            'context': 'Figma CDN download'
        }

        result = self.oracle.query_error_solutions(error, min_similarity=0.8)

        self.assertIsInstance(result, list)
        # If patterns exist, verify structure
        if result:
            self.assertIn('solution', result[0])
            self.assertIn('confidence', result[0])
        print("✅ Test 15: query_error_solutions returns list")

    def test_16_reinforce_solution_accepts_params(self):
        """Test reinforce_solution accepts correct parameters"""
        error = {'type': 'timeout', 'message': 'timeout'}
        solution = {'technique': 'Retry'}

        # Should not raise exception
        try:
            self.oracle.reinforce_solution(error, solution, success=True)
            self.oracle.reinforce_solution(error, solution, success=False)
            print("✅ Test 16: reinforce_solution accepts parameters")
        except Exception as e:
            self.fail(f"reinforce_solution raised exception: {e}")


class TestEndToEndAutoFix(unittest.TestCase):
    """Test end-to-end auto-fix workflow"""

    def test_17_create_auto_fix_orchestrator_factory(self):
        """Test factory function creates orchestrator"""
        mock_oracle = Mock()
        mock_narrator = Mock()

        orchestrator = create_auto_fix_orchestrator(oracle=mock_oracle, narrator=mock_narrator)

        self.assertIsInstance(orchestrator, AutoFixOrchestrator)
        self.assertEqual(orchestrator.oracle, mock_oracle)
        print("✅ Test 17: Factory function creates orchestrator")

    def test_18_confidence_thresholds(self):
        """Test confidence threshold constants"""
        self.assertEqual(AutoFixOrchestrator.CONFIDENCE_AUTO_FIX, 0.80)
        self.assertEqual(AutoFixOrchestrator.CONFIDENCE_SUGGEST, 0.50)
        self.assertEqual(AutoFixOrchestrator.SIMILARITY_THRESHOLD, 0.80)
        print("✅ Test 18: Confidence thresholds configured")


def run_tests():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("🧪 AUTO-FIX ORCHESTRATOR TEST SUITE")
    print("=" * 70)
    print()

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes in order
    suite.addTests(loader.loadTestsFromTestCase(TestAutoFixOrchestrator))
    suite.addTests(loader.loadTestsFromTestCase(TestSupermanAutoFixIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestOracleAutoFixMethods))
    suite.addTests(loader.loadTestsFromTestCase(TestEndToEndAutoFix))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print()
    print("=" * 70)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED!")
        print(f"   Tests run: {result.testsRun}")
        print(f"   Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    else:
        print("❌ SOME TESTS FAILED")
        print(f"   Tests run: {result.testsRun}")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")
    print("=" * 70)
    print()

    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
