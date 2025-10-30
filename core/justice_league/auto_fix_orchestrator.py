"""
🔮 AUTO-FIX ORCHESTRATOR - Oracle's Autonomous Error Recovery System
=====================================================================

Connects Oracle's error detection → fix proposal → auto-implementation pipeline
with Superman's mission coordination for seamless autonomous operation.

Key Features:
- Confidence-based auto-fix (≥80% confidence = auto-implement)
- Self-learning from every fix outcome
- Complete audit trail of all decisions
- Integration with existing self-healing systems

Version: 1.0.0 (v1.9.3)
Created: 2025-10-30
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class AutoFixOrchestrator:
    """
    Orchestrates autonomous error detection and recovery

    Workflow:
    1. Error detected in Superman mission
    2. Oracle classifies error type
    3. Query knowledge base for similar errors (≥80% similarity)
    4. Check confidence score:
       - ≥80%: Auto-implement fix
       - 50-79%: Generate fix, ask user
       - <50%: Log error, defer to user
    5. Apply fix and retry mission
    6. Track outcome and update knowledge base
    """

    # Confidence thresholds
    CONFIDENCE_AUTO_FIX = 0.80      # 80%+ confidence = auto-fix
    CONFIDENCE_SUGGEST = 0.50       # 50-79% = suggest to user

    # Error pattern similarity threshold
    SIMILARITY_THRESHOLD = 0.80     # 80%+ similarity = proven solution

    def __init__(self, oracle=None, narrator=None):
        """
        Initialize Auto-Fix Orchestrator

        Args:
            oracle: Oracle meta agent instance
            narrator: Mission Control Narrator instance
        """
        self.oracle = oracle
        self.narrator = narrator

        # Fix history for learning
        self.fix_history: List[Dict[str, Any]] = []

        # Statistics
        self.stats = {
            'total_errors': 0,
            'auto_fixed': 0,
            'suggested': 0,
            'deferred': 0,
            'success_rate': 0.0
        }

        logger.info("🔮 Auto-Fix Orchestrator initialized")

    def handle_failure(
        self,
        mission: Dict[str, Any],
        result: Dict[str, Any],
        confidence_threshold: float = None
    ) -> Dict[str, Any]:
        """
        Handle mission failure with automatic fix attempt

        Args:
            mission: Original mission configuration
            result: Failed mission result
            confidence_threshold: Override default confidence threshold

        Returns:
            dict with 'fixed', 'solution', 'confidence', 'retry_recommended'
        """
        if confidence_threshold is None:
            confidence_threshold = self.CONFIDENCE_AUTO_FIX

        self.stats['total_errors'] += 1

        if self.narrator:
            self.narrator.hero_speaks(
                "🔮 Oracle",
                "Error detected. Analyzing pattern and searching for solution...",
                "tactical"
            )

        # Extract error details
        error = self._extract_error_details(result)

        # Classify error type
        error_classification = self._classify_error(error)

        if self.narrator:
            self.narrator.hero_speaks(
                "🔮 Oracle",
                f"Classified as: {error_classification['type']}",
                "tactical",
                technical_info=f"Category: {error_classification['category']}"
            )

        # Query Oracle knowledge base for similar errors
        if self.oracle:
            similar_errors = self.oracle.query_error_solutions(
                error,
                min_similarity=self.SIMILARITY_THRESHOLD
            )
        else:
            similar_errors = self._query_local_patterns(error)

        # Decide on action based on confidence
        if similar_errors and len(similar_errors) > 0:
            # Found proven solution
            best_match = similar_errors[0]
            confidence = best_match.get('confidence', best_match.get('similarity', 0.0))

            if self.narrator:
                self.narrator.hero_speaks(
                    "🔮 Oracle",
                    f"Found proven solution with {confidence*100:.0f}% confidence",
                    "tactical"
                )

            if confidence >= confidence_threshold:
                # AUTO-FIX: High confidence
                return self._auto_implement_fix(
                    error, best_match['solution'], confidence, mission
                )
            elif confidence >= self.CONFIDENCE_SUGGEST:
                # SUGGEST: Medium confidence
                return self._suggest_fix(
                    error, best_match['solution'], confidence
                )

        # No proven solution found - generate new fix proposal
        if self.oracle and hasattr(self.oracle, 'fix_proposal_engine'):
            fix_proposal = self.oracle.fix_proposal_engine.generate_fix(error)

            if fix_proposal and fix_proposal.get('confidence', 0) >= confidence_threshold:
                # AUTO-FIX: High confidence new solution
                return self._auto_implement_fix(
                    error, fix_proposal['fix'], fix_proposal['confidence'], mission
                )
            elif fix_proposal and fix_proposal.get('confidence', 0) >= self.CONFIDENCE_SUGGEST:
                # SUGGEST: Medium confidence new solution
                return self._suggest_fix(
                    error, fix_proposal['fix'], fix_proposal['confidence']
                )

        # Low confidence or no fix found - defer to user
        self.stats['deferred'] += 1

        if self.narrator:
            self.narrator.hero_speaks(
                "🔮 Oracle",
                "No high-confidence solution found. Manual intervention required.",
                "tactical"
            )

        return {
            'fixed': False,
            'confidence': 0.0,
            'reason': 'No high-confidence solution available',
            'retry_recommended': False,
            'manual_review_required': True,
            'error': error
        }

    def handle_exception(
        self,
        exception: Exception,
        mission: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle unexpected exceptions during mission execution

        Args:
            exception: The exception that was raised
            mission: Original mission configuration

        Returns:
            dict with fix result
        """
        error = {
            'type': type(exception).__name__,
            'message': str(exception),
            'context': mission.get('mission_type', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return self.handle_failure(
            mission,
            {'success': False, 'error': error},
            confidence_threshold=self.CONFIDENCE_AUTO_FIX
        )

    def _extract_error_details(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract structured error details from mission result"""
        if 'error' in result and isinstance(result['error'], dict):
            return result['error']

        # Extract from errors list
        errors = result.get('errors', [])
        if errors:
            error_msg = errors[0] if isinstance(errors, list) else str(errors)
        else:
            error_msg = result.get('error', 'Unknown error')

        # Parse error message for patterns
        error_details = {
            'message': str(error_msg),
            'timestamp': datetime.now().isoformat(),
            'context': result.get('mission_type', 'unknown')
        }

        # Detect common error patterns
        error_msg_lower = str(error_msg).lower()

        if 'timeout' in error_msg_lower:
            error_details['type'] = 'timeout'
        elif 'connectionpool' in error_msg_lower or 'connection' in error_msg_lower:
            error_details['type'] = 'network'
        elif 'httperror' in error_msg_lower or 'status' in error_msg_lower:
            error_details['type'] = 'http_error'
        elif 'permission' in error_msg_lower or 'forbidden' in error_msg_lower:
            error_details['type'] = 'permission'
        else:
            error_details['type'] = 'unknown'

        return error_details

    def _classify_error(self, error: Dict[str, Any]) -> Dict[str, str]:
        """Classify error into categories for pattern matching"""
        error_type = error.get('type', 'unknown')
        error_msg = str(error.get('message', '')).lower()

        # Classification rules
        if error_type == 'timeout' or 'timeout' in error_msg:
            return {
                'type': 'Network Timeout',
                'category': 'network_reliability',
                'severity': 'medium',
                'auto_fixable': True
            }
        elif error_type == 'network' or 'connection' in error_msg:
            return {
                'type': 'Network Connection',
                'category': 'network_reliability',
                'severity': 'medium',
                'auto_fixable': True
            }
        elif error_type == 'http_error':
            return {
                'type': 'HTTP Error',
                'category': 'api_error',
                'severity': 'high',
                'auto_fixable': False
            }
        elif error_type == 'permission':
            return {
                'type': 'Permission Denied',
                'category': 'authentication',
                'severity': 'high',
                'auto_fixable': False
            }
        else:
            return {
                'type': 'Unknown Error',
                'category': 'general',
                'severity': 'medium',
                'auto_fixable': False
            }

    def _query_local_patterns(self, error: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query local error recovery patterns if Oracle unavailable"""
        error_type = error.get('type', 'unknown')

        # Built-in patterns (from Oracle knowledge base)
        patterns = {
            'timeout': {
                'pattern': 'figma-export-retry-with-exponential-backoff',
                'solution': {
                    'technique': 'Exponential backoff retry',
                    'parameters': {
                        'max_retries': 5,
                        'timeout_api': 60,
                        'timeout_cdn': 120,
                        'backoff_factor': 2.0
                    },
                    'script': 'scripts/export_figma_standalone.py'
                },
                'confidence': 1.0,
                'similarity': 1.0
            },
            'network': {
                'pattern': 'network-resilience-retry',
                'solution': {
                    'technique': 'Retry with backoff',
                    'parameters': {
                        'max_retries': 3,
                        'timeout': 60,
                        'backoff_factor': 2.0
                    }
                },
                'confidence': 0.9,
                'similarity': 0.9
            }
        }

        if error_type in patterns:
            return [patterns[error_type]]

        return []

    def _auto_implement_fix(
        self,
        error: Dict[str, Any],
        solution: Dict[str, Any],
        confidence: float,
        mission: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Automatically implement fix with high confidence"""
        self.stats['auto_fixed'] += 1

        if self.narrator:
            self.narrator.hero_speaks(
                "🔮 Oracle",
                f"Auto-implementing fix (confidence: {confidence*100:.0f}%)",
                "tactical"
            )

        # Record fix attempt
        fix_record = {
            'error': error,
            'solution': solution,
            'confidence': confidence,
            'auto_implemented': True,
            'timestamp': datetime.now().isoformat(),
            'mission': mission
        }
        self.fix_history.append(fix_record)

        # Update statistics
        self._update_stats()

        return {
            'fixed': True,
            'solution': solution,
            'confidence': confidence,
            'retry_recommended': True,
            'auto_implemented': True,
            'fix_record': fix_record
        }

    def _suggest_fix(
        self,
        error: Dict[str, Any],
        solution: Dict[str, Any],
        confidence: float
    ) -> Dict[str, Any]:
        """Suggest fix to user for medium confidence"""
        self.stats['suggested'] += 1

        if self.narrator:
            self.narrator.hero_speaks(
                "🔮 Oracle",
                f"Found potential solution (confidence: {confidence*100:.0f}%). Suggesting to user...",
                "tactical"
            )

        return {
            'fixed': False,
            'solution': solution,
            'confidence': confidence,
            'retry_recommended': False,
            'suggestion': True,
            'message': f"Potential fix found with {confidence*100:.0f}% confidence. Review and apply manually?"
        }

    def track_fix_outcome(
        self,
        fix_record: Dict[str, Any],
        success: bool,
        mission_result: Dict[str, Any] = None
    ):
        """
        Track the outcome of a fix attempt for learning

        Args:
            fix_record: The fix record from auto_implement_fix()
            success: Whether the fix was successful
            mission_result: Optional mission result after fix
        """
        # Update fix record
        fix_record['success'] = success
        fix_record['tracked_at'] = datetime.now().isoformat()

        if mission_result:
            fix_record['mission_result'] = mission_result

        # Update Oracle knowledge base
        if self.oracle and success:
            # Increase confidence for successful fix
            self.oracle.reinforce_solution(
                error=fix_record['error'],
                solution=fix_record['solution'],
                success=True
            )

            if self.narrator:
                self.narrator.hero_speaks(
                    "🔮 Oracle",
                    "Auto-fix successful! Knowledge base updated with reinforced confidence.",
                    "friendly"
                )
        elif self.oracle and not success:
            # Decrease confidence for failed fix
            self.oracle.reinforce_solution(
                error=fix_record['error'],
                solution=fix_record['solution'],
                success=False
            )

            if self.narrator:
                self.narrator.hero_speaks(
                    "🔮 Oracle",
                    "Auto-fix unsuccessful. Adjusting confidence scores...",
                    "tactical"
                )

        # Update statistics
        self._update_stats()

    def _update_stats(self):
        """Update success rate statistics"""
        total_attempts = self.stats['auto_fixed'] + self.stats['suggested']

        if total_attempts > 0:
            # Count successful fixes from history
            successful_fixes = sum(
                1 for fix in self.fix_history
                if fix.get('success', False)
            )
            self.stats['success_rate'] = successful_fixes / total_attempts

    def get_stats(self) -> Dict[str, Any]:
        """Get current auto-fix statistics"""
        return {
            **self.stats,
            'total_fix_attempts': len(self.fix_history),
            'recent_fixes': self.fix_history[-5:] if self.fix_history else []
        }


def create_auto_fix_orchestrator(oracle=None, narrator=None) -> AutoFixOrchestrator:
    """
    Factory function to create auto-fix orchestrator

    Args:
        oracle: Oracle meta agent instance
        narrator: Mission Control Narrator instance

    Returns:
        AutoFixOrchestrator instance
    """
    return AutoFixOrchestrator(oracle=oracle, narrator=narrator)
