"""
🔧 Oracle Fix Proposal Engine
Automatically generates fix proposals for detected issues

This module analyzes detected issues and proposes fixes by:
- Querying Oracle's knowledge base for similar problems
- Analyzing error patterns
- Generating code fixes
- Creating test cases for fixes
- Providing implementation steps

"I don't just find the problem. I show you how to fix it." - Oracle
"""

import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import hashlib
import re

logger = logging.getLogger(__name__)


class FixCategory(str):
    """Categories of fixes"""
    TIMEOUT_FIX = "timeout_fix"
    ERROR_HANDLING = "error_handling"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    DEPENDENCY_UPDATE = "dependency_update"
    CONFIGURATION_CHANGE = "configuration_change"
    CODE_REFACTORING = "code_refactoring"
    RESOURCE_MANAGEMENT = "resource_management"
    SECURITY_PATCH = "security_patch"


class FixProposalEngine:
    """
    🔧 Automated Fix Proposal Engine

    Generates fix proposals for detected issues using:
    - Knowledge base of past solutions
    - Pattern matching
    - Best practices library
    - Code analysis
    """

    # Common error patterns and their fixes
    ERROR_PATTERNS = {
        'timeout': {
            'category': FixCategory.TIMEOUT_FIX,
            'common_causes': [
                'Network latency',
                'Slow external service',
                'Insufficient timeout value',
                'Resource contention'
            ],
            'fix_templates': [
                {
                    'name': 'Increase timeout duration',
                    'description': 'Increase timeout from {current} to {proposed}',
                    'risk_level': 'low',
                    'implementation_steps': [
                        'Identify timeout configuration',
                        'Increase timeout value by 50-100%',
                        'Test with realistic scenarios',
                        'Monitor for improvements'
                    ]
                },
                {
                    'name': 'Add retry logic',
                    'description': 'Implement exponential backoff retry',
                    'risk_level': 'low',
                    'implementation_steps': [
                        'Add retry decorator/wrapper',
                        'Implement exponential backoff',
                        'Set maximum retry attempts',
                        'Log retry attempts'
                    ]
                },
                {
                    'name': 'Optimize slow operation',
                    'description': 'Profile and optimize the slow operation',
                    'risk_level': 'medium',
                    'implementation_steps': [
                        'Profile the operation',
                        'Identify bottlenecks',
                        'Apply optimizations',
                        'Verify performance improvement'
                    ]
                }
            ]
        },
        'high_error_rate': {
            'category': FixCategory.ERROR_HANDLING,
            'common_causes': [
                'Insufficient error handling',
                'Unhandled edge cases',
                'Invalid input validation',
                'External dependency failures'
            ],
            'fix_templates': [
                {
                    'name': 'Add comprehensive error handling',
                    'description': 'Implement try-catch blocks and graceful degradation',
                    'risk_level': 'low',
                    'implementation_steps': [
                        'Wrap operations in try-catch',
                        'Add specific exception handlers',
                        'Implement fallback mechanisms',
                        'Add error logging'
                    ]
                },
                {
                    'name': 'Add input validation',
                    'description': 'Validate inputs before processing',
                    'risk_level': 'low',
                    'implementation_steps': [
                        'Define input schema',
                        'Add validation checks',
                        'Return clear error messages',
                        'Test with invalid inputs'
                    ]
                }
            ]
        },
        'performance_degradation': {
            'category': FixCategory.PERFORMANCE_OPTIMIZATION,
            'common_causes': [
                'Inefficient algorithms',
                'Memory leaks',
                'Unnecessary computations',
                'Blocking operations'
            ],
            'fix_templates': [
                {
                    'name': 'Add caching layer',
                    'description': 'Cache frequently accessed data',
                    'risk_level': 'low',
                    'implementation_steps': [
                        'Identify cacheable operations',
                        'Implement cache with TTL',
                        'Add cache invalidation logic',
                        'Monitor cache hit rate'
                    ]
                },
                {
                    'name': 'Optimize algorithm',
                    'description': 'Replace with more efficient algorithm',
                    'risk_level': 'medium',
                    'implementation_steps': [
                        'Profile current implementation',
                        'Research optimal algorithm',
                        'Implement optimization',
                        'Benchmark improvements'
                    ]
                },
                {
                    'name': 'Use async operations',
                    'description': 'Convert blocking operations to async',
                    'risk_level': 'medium',
                    'implementation_steps': [
                        'Identify blocking operations',
                        'Convert to async/await',
                        'Add proper error handling',
                        'Test concurrent scenarios'
                    ]
                }
            ]
        },
        'recurring_error': {
            'category': FixCategory.ERROR_HANDLING,
            'common_causes': [
                'Unhandled edge case',
                'Configuration issue',
                'Data quality problem',
                'Race condition'
            ],
            'fix_templates': [
                {
                    'name': 'Add specific error handler',
                    'description': 'Handle this specific error case',
                    'risk_level': 'low',
                    'implementation_steps': [
                        'Analyze error pattern',
                        'Implement specific handler',
                        'Add comprehensive logging',
                        'Test error scenario'
                    ]
                },
                {
                    'name': 'Fix root cause',
                    'description': 'Address underlying issue causing error',
                    'risk_level': 'medium',
                    'implementation_steps': [
                        'Investigate root cause',
                        'Design proper fix',
                        'Implement with tests',
                        'Verify error no longer occurs'
                    ]
                }
            ]
        },
        'dependency_failure': {
            'category': FixCategory.DEPENDENCY_UPDATE,
            'common_causes': [
                'Outdated dependency',
                'Broken API contract',
                'Service unavailable',
                'Network issues'
            ],
            'fix_templates': [
                {
                    'name': 'Update dependency',
                    'description': 'Update to latest stable version',
                    'risk_level': 'medium',
                    'implementation_steps': [
                        'Check for updates',
                        'Review changelog',
                        'Update dependency',
                        'Run full test suite'
                    ]
                },
                {
                    'name': 'Add fallback mechanism',
                    'description': 'Implement graceful degradation',
                    'risk_level': 'low',
                    'implementation_steps': [
                        'Design fallback behavior',
                        'Implement fallback logic',
                        'Add circuit breaker',
                        'Test failure scenarios'
                    ]
                }
            ]
        },
        'configuration_error': {
            'category': FixCategory.CONFIGURATION_CHANGE,
            'common_causes': [
                'Missing configuration',
                'Invalid configuration value',
                'Environment mismatch',
                'Secrets not set'
            ],
            'fix_templates': [
                {
                    'name': 'Update configuration',
                    'description': 'Fix configuration values',
                    'risk_level': 'low',
                    'implementation_steps': [
                        'Identify configuration issue',
                        'Update configuration file',
                        'Validate new configuration',
                        'Restart affected services'
                    ]
                },
                {
                    'name': 'Add configuration validation',
                    'description': 'Validate configuration on startup',
                    'risk_level': 'low',
                    'implementation_steps': [
                        'Define configuration schema',
                        'Add validation on startup',
                        'Fail fast with clear errors',
                        'Document required config'
                    ]
                }
            ]
        }
    }

    def __init__(self, oracle_knowledge_base_dir: Optional[str] = None):
        """
        Initialize Fix Proposal Engine

        Args:
            oracle_knowledge_base_dir: Path to Oracle's knowledge base
        """
        self.kb_dir = Path(oracle_knowledge_base_dir) if oracle_knowledge_base_dir else Path('/tmp/aldo-vision-justice-league/oracle')
        self.errors_db = self.kb_dir / 'errors_solutions.json'
        self.best_practices_db = self.kb_dir / 'best_practices.json'
        self.proposals_db = self.kb_dir / 'fix_proposals.json'

        # Initialize proposals database
        if not self.proposals_db.exists():
            self._init_proposals_db()

        logger.info("🔧 Fix Proposal Engine initialized")

    def _init_proposals_db(self):
        """Initialize fix proposals database"""
        initial_data = {
            'proposals': [],
            'approved_proposals': [],
            'rejected_proposals': [],
            'implemented_proposals': [],
            'last_updated': datetime.now().isoformat()
        }
        with open(self.proposals_db, 'w') as f:
            json.dump(initial_data, f, indent=2)

    def generate_fix_proposal(self,
                             issue: Dict[str, Any],
                             agent_name: str,
                             context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        🔧 Generate fix proposal for a detected issue

        Args:
            issue: Issue details from health monitor
            agent_name: Name of affected agent
            context: Optional additional context

        Returns:
            Fix proposal with implementation details
        """
        proposal = {
            'proposal_id': self._generate_proposal_id(issue, agent_name),
            'created_at': datetime.now().isoformat(),
            'agent': agent_name,
            'issue': issue,
            'status': 'pending_review',
            'fix_options': [],
            'recommended_fix': None,
            'estimated_effort': 'unknown',
            'risk_assessment': {},
            'implementation_plan': [],
            'test_plan': [],
            'rollback_plan': [],
            'similar_past_issues': []
        }

        # Determine issue type
        issue_type = issue.get('type', 'unknown')

        # Search knowledge base for similar issues
        similar_issues = self._search_similar_issues(issue, agent_name)
        proposal['similar_past_issues'] = similar_issues

        # Generate fix options based on issue type
        if issue_type in self.ERROR_PATTERNS:
            pattern = self.ERROR_PATTERNS[issue_type]
            for template in pattern['fix_templates']:
                fix_option = {
                    'name': template['name'],
                    'description': template['description'],
                    'category': pattern['category'],
                    'risk_level': template['risk_level'],
                    'implementation_steps': template['implementation_steps'],
                    'estimated_time': self._estimate_implementation_time(template),
                    'success_probability': 0.7  # Default
                }

                # Adjust success probability based on similar issues
                if similar_issues:
                    # If we've seen this before, higher success probability
                    fix_option['success_probability'] = 0.9

                proposal['fix_options'].append(fix_option)

        # If we have past solutions, add them as fix options
        if similar_issues:
            for similar in similar_issues[:3]:  # Top 3 similar
                if 'solution' in similar:
                    proposal['fix_options'].append({
                        'name': 'Apply proven solution',
                        'description': f"Use solution from {similar.get('id', 'previous fix')}",
                        'category': 'proven_solution',
                        'risk_level': 'low',
                        'solution': similar['solution'],
                        'implementation_steps': [
                            'Review previous solution',
                            'Adapt for current context',
                            'Implement fix',
                            'Test thoroughly'
                        ],
                        'estimated_time': '30-60 minutes',
                        'success_probability': 0.95,  # High probability - worked before
                        'previous_success_rate': similar.get('success_rate', 1.0)
                    })

        # Select recommended fix
        if proposal['fix_options']:
            # Recommend the fix with highest success probability
            proposal['recommended_fix'] = max(
                proposal['fix_options'],
                key=lambda x: x.get('success_probability', 0)
            )

        # Generate implementation plan
        if proposal['recommended_fix']:
            proposal['implementation_plan'] = self._generate_implementation_plan(
                proposal['recommended_fix'],
                agent_name,
                issue
            )

            # Generate test plan
            proposal['test_plan'] = self._generate_test_plan(
                proposal['recommended_fix'],
                agent_name,
                issue
            )

            # Generate rollback plan
            proposal['rollback_plan'] = self._generate_rollback_plan(agent_name)

            # Estimate effort
            proposal['estimated_effort'] = proposal['recommended_fix'].get('estimated_time', 'medium')

        # Risk assessment
        proposal['risk_assessment'] = self._assess_risk(proposal)

        # Store proposal
        self._store_proposal(proposal)

        logger.info(f"🔧 Generated fix proposal {proposal['proposal_id']} for {agent_name}")
        logger.info(f"🔧 {len(proposal['fix_options'])} fix options proposed")

        return proposal

    def _generate_proposal_id(self, issue: Dict[str, Any], agent_name: str) -> str:
        """Generate unique proposal ID"""
        content = f"{agent_name}{issue.get('type', '')}{datetime.now().isoformat()}"
        hash_val = hashlib.md5(content.encode()).hexdigest()[:8].upper()
        return f"FIX-{hash_val}"

    def _search_similar_issues(self, issue: Dict[str, Any], agent_name: str) -> List[Dict[str, Any]]:
        """Search knowledge base for similar issues"""
        if not self.errors_db.exists():
            return []

        with open(self.errors_db, 'r') as f:
            errors_data = json.load(f)

        similar = []
        issue_type = issue.get('type', '')
        issue_message = issue.get('message', '').lower()

        for error_id, error_record in errors_data.items():
            # Check same agent
            if error_record.get('agent') == agent_name:
                # Check same error type
                if error_record.get('error_type', '').lower() == issue_type.lower():
                    similar.append({
                        'id': error_id,
                        'solution': error_record.get('solution', ''),
                        'success_rate': error_record.get('success_rate', 1.0),
                        'times_encountered': error_record.get('times_encountered', 1),
                        'similarity_score': 0.9
                    })
                # Check similar message
                elif issue_message in error_record.get('error_details', {}).get('message', '').lower():
                    similar.append({
                        'id': error_id,
                        'solution': error_record.get('solution', ''),
                        'success_rate': error_record.get('success_rate', 1.0),
                        'times_encountered': error_record.get('times_encountered', 1),
                        'similarity_score': 0.7
                    })

        # Sort by similarity score and success rate
        similar.sort(key=lambda x: (x['similarity_score'], x['success_rate']), reverse=True)

        return similar[:5]  # Return top 5

    def _estimate_implementation_time(self, template: Dict[str, Any]) -> str:
        """Estimate implementation time based on complexity"""
        steps = len(template.get('implementation_steps', []))
        risk = template.get('risk_level', 'medium')

        if risk == 'low' and steps <= 3:
            return '15-30 minutes'
        elif risk == 'low' and steps <= 5:
            return '30-60 minutes'
        elif risk == 'medium' and steps <= 4:
            return '1-2 hours'
        elif risk == 'medium':
            return '2-4 hours'
        else:
            return '4-8 hours'

    def _generate_implementation_plan(self,
                                     fix: Dict[str, Any],
                                     agent_name: str,
                                     issue: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate detailed implementation plan"""
        plan = []

        # Step 1: Backup current version
        plan.append({
            'step': 1,
            'action': 'Create agent backup',
            'description': f'Create version snapshot of {agent_name}',
            'commands': [
                f'oracle.create_agent_version("{agent_name}", "pre-fix-backup")'
            ],
            'verification': 'Verify backup created successfully'
        })

        # Step 2: Implement fix steps
        for idx, step in enumerate(fix.get('implementation_steps', []), start=2):
            plan.append({
                'step': idx,
                'action': step,
                'description': step,
                'commands': [],  # To be filled in by developer
                'verification': 'Verify step completed'
            })

        # Final step: Verify fix
        plan.append({
            'step': len(plan) + 1,
            'action': 'Verify fix',
            'description': 'Run tests to verify fix resolves the issue',
            'commands': [
                f'python3 test_{agent_name}.py'
            ],
            'verification': 'All tests pass'
        })

        return plan

    def _generate_test_plan(self,
                           fix: Dict[str, Any],
                           agent_name: str,
                           issue: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate test plan for the fix"""
        tests = []

        # Test 1: Verify issue is resolved
        tests.append({
            'test_name': 'Verify issue resolution',
            'description': f"Ensure {issue.get('type', 'issue')} no longer occurs",
            'test_type': 'regression',
            'expected_result': 'Issue no longer occurs under same conditions'
        })

        # Test 2: Verify no side effects
        tests.append({
            'test_name': 'Check for side effects',
            'description': 'Ensure fix doesn\'t break existing functionality',
            'test_type': 'integration',
            'expected_result': 'All existing tests pass'
        })

        # Test 3: Performance test
        if 'performance' in issue.get('type', '').lower():
            tests.append({
                'test_name': 'Performance validation',
                'description': 'Verify performance improvement',
                'test_type': 'performance',
                'expected_result': 'Execution time within acceptable range'
            })

        # Test 4: Edge cases
        tests.append({
            'test_name': 'Edge case testing',
            'description': 'Test with boundary conditions',
            'test_type': 'edge_case',
            'expected_result': 'Handles edge cases gracefully'
        })

        return tests

    def _generate_rollback_plan(self, agent_name: str) -> List[Dict[str, str]]:
        """Generate rollback plan in case fix fails"""
        return [
            {
                'step': '1',
                'action': 'Stop using new version',
                'command': f'# Stop any processes using {agent_name}'
            },
            {
                'step': '2',
                'action': 'Rollback to previous version',
                'command': f'oracle.rollback_agent("{agent_name}", "pre-fix-backup")'
            },
            {
                'step': '3',
                'action': 'Verify rollback',
                'command': f'python3 test_{agent_name}.py'
            },
            {
                'step': '4',
                'action': 'Document failure',
                'command': 'oracle.store_error_solution(...)'
            }
        ]

    def _assess_risk(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risk of implementing the fix"""
        recommended_fix = proposal.get('recommended_fix')

        if not recommended_fix:
            return {'overall_risk': 'unknown', 'factors': []}

        risk_factors = []
        risk_score = 0.0

        # Factor 1: Fix complexity
        steps = len(recommended_fix.get('implementation_steps', []))
        if steps > 5:
            risk_score += 0.3
            risk_factors.append('Complex implementation (>5 steps)')
        elif steps > 3:
            risk_score += 0.1
            risk_factors.append('Moderate complexity (3-5 steps)')

        # Factor 2: Stated risk level
        risk_level = recommended_fix.get('risk_level', 'medium')
        if risk_level == 'high':
            risk_score += 0.4
            risk_factors.append('High inherent risk')
        elif risk_level == 'medium':
            risk_score += 0.2
            risk_factors.append('Medium inherent risk')

        # Factor 3: Past success rate
        success_prob = recommended_fix.get('success_probability', 0.5)
        if success_prob < 0.7:
            risk_score += 0.3
            risk_factors.append(f'Low success probability ({success_prob:.0%})')

        # Factor 4: Similar issues
        if not proposal.get('similar_past_issues'):
            risk_score += 0.1
            risk_factors.append('No historical data for this issue type')

        # Determine overall risk
        if risk_score < 0.3:
            overall_risk = 'low'
        elif risk_score < 0.6:
            overall_risk = 'medium'
        else:
            overall_risk = 'high'

        return {
            'overall_risk': overall_risk,
            'risk_score': round(risk_score, 2),
            'risk_factors': risk_factors,
            'recommendation': 'approve' if overall_risk in ['low', 'medium'] else 'review_required'
        }

    def _store_proposal(self, proposal: Dict[str, Any]):
        """Store fix proposal in database"""
        with open(self.proposals_db, 'r') as f:
            data = json.load(f)

        data['proposals'].append(proposal)
        data['last_updated'] = datetime.now().isoformat()

        with open(self.proposals_db, 'w') as f:
            json.dump(data, f, indent=2)

    def approve_proposal(self, proposal_id: str, approved_by: str) -> bool:
        """
        Approve a fix proposal

        Args:
            proposal_id: Proposal ID to approve
            approved_by: Name of approver

        Returns:
            True if approved successfully
        """
        with open(self.proposals_db, 'r') as f:
            data = json.load(f)

        for proposal in data['proposals']:
            if proposal['proposal_id'] == proposal_id:
                proposal['status'] = 'approved'
                proposal['approved_by'] = approved_by
                proposal['approved_at'] = datetime.now().isoformat()

                data['approved_proposals'].append(proposal)
                data['last_updated'] = datetime.now().isoformat()

                with open(self.proposals_db, 'w') as f:
                    json.dump(data, f, indent=2)

                logger.info(f"🔧 Approved fix proposal {proposal_id} by {approved_by}")
                return True

        return False

    def reject_proposal(self, proposal_id: str, rejected_by: str, reason: str) -> bool:
        """
        Reject a fix proposal

        Args:
            proposal_id: Proposal ID to reject
            rejected_by: Name of rejector
            reason: Reason for rejection

        Returns:
            True if rejected successfully
        """
        with open(self.proposals_db, 'r') as f:
            data = json.load(f)

        for proposal in data['proposals']:
            if proposal['proposal_id'] == proposal_id:
                proposal['status'] = 'rejected'
                proposal['rejected_by'] = rejected_by
                proposal['rejected_at'] = datetime.now().isoformat()
                proposal['rejection_reason'] = reason

                data['rejected_proposals'].append(proposal)
                data['last_updated'] = datetime.now().isoformat()

                with open(self.proposals_db, 'w') as f:
                    json.dump(data, f, indent=2)

                logger.info(f"🔧 Rejected fix proposal {proposal_id}: {reason}")
                return True

        return False

    def get_pending_proposals(self) -> List[Dict[str, Any]]:
        """Get all pending fix proposals"""
        with open(self.proposals_db, 'r') as f:
            data = json.load(f)

        return [p for p in data['proposals'] if p.get('status') == 'pending_review']

    def get_approved_proposals(self) -> List[Dict[str, Any]]:
        """Get all approved fix proposals ready for implementation"""
        with open(self.proposals_db, 'r') as f:
            data = json.load(f)

        return [p for p in data.get('approved_proposals', []) if p.get('status') == 'approved']
