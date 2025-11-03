"""
🧠 Cross-Agent Learning System
Share knowledge and solutions across all Justice League agents

This module enables agents to learn from each other by:
- Sharing successful solutions across agents
- Identifying transferable patterns
- Recommending solutions from other agents
- Building collective intelligence
- Preventing duplicate problem-solving

"When one learns, we all learn. The League's knowledge is shared knowledge." - Oracle
"""

import logging
import json
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import hashlib

logger = logging.getLogger(__name__)


class KnowledgeTransferability(str):
    """How transferable knowledge is between agents"""
    HIGH = "high"              # Applies to all agents
    MEDIUM = "medium"          # Applies to similar agents
    LOW = "low"                # Agent-specific
    UNIVERSAL = "universal"    # Applies universally


class CrossAgentLearning:
    """
    🧠 Cross-Agent Learning System

    Enables knowledge sharing across all Justice League agents:
    - Identifies transferable solutions
    - Recommends solutions from similar agents
    - Builds collective knowledge base
    - Prevents redundant problem-solving
    """

    # Agent similarity matrix (which agents have similar responsibilities)
    AGENT_SIMILARITIES = {
        'batman': ['green_lantern', 'cyborg'],  # Testing & Integration
        'green_lantern': ['batman', 'wonder_woman'],  # Visual & Accessibility
        'wonder_woman': ['green_lantern', 'zatanna'],  # Accessibility & SEO
        'flash': ['aquaman'],  # Performance & Network
        'aquaman': ['flash', 'cyborg'],  # Network & Integration
        'cyborg': ['batman', 'aquaman'],  # Integration & Testing
        'atom': ['plastic_man'],  # Component & Responsive
        'martian_manhunter': [],  # Security (unique)
        'green_arrow': ['batman'],  # QA & Testing
        'plastic_man': ['atom', 'wonder_woman'],  # Responsive & Accessibility
        'zatanna': ['wonder_woman'],  # SEO & Accessibility
    }

    # Universal patterns that apply to all agents
    UNIVERSAL_PATTERNS = [
        'timeout',
        'error_handling',
        'retry_logic',
        'configuration',
        'dependency_update',
        'performance_optimization',
        'logging',
        'monitoring',
    ]

    def __init__(self, oracle_kb_dir: Optional[str] = None):
        """
        Initialize Cross-Agent Learning System

        Args:
            oracle_kb_dir: Path to Oracle's knowledge base directory
        """
        self.kb_dir = Path(oracle_kb_dir) if oracle_kb_dir else Path('/tmp/aldo-vision-justice-league/oracle')
        self.errors_db = self.kb_dir / 'errors_solutions.json'
        self.learning_db = self.kb_dir / 'cross_agent_learning.json'

        # Initialize learning database
        if not self.learning_db.exists():
            self._init_learning_db()

        logger.info("🧠 Cross-Agent Learning System initialized")

    def _init_learning_db(self):
        """Initialize cross-agent learning database"""
        initial_data = {
            'knowledge_transfers': [],
            'successful_transfers': [],
            'failed_transfers': [],
            'transfer_recommendations': [],
            'agent_learning_stats': {},
            'last_updated': datetime.now().isoformat()
        }

        with open(self.learning_db, 'w') as f:
            json.dump(initial_data, f, indent=2)

    def find_transferable_solutions(self,
                                   target_agent: str,
                                   issue_type: str,
                                   context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        🧠 Find solutions from other agents that can be transferred

        Args:
            target_agent: Agent that needs a solution
            issue_type: Type of issue to solve
            context: Optional context about the issue

        Returns:
            List of transferable solutions from other agents
        """
        transferable_solutions = []

        if not self.errors_db.exists():
            return transferable_solutions

        with open(self.errors_db, 'r') as f:
            errors_data = json.load(f)

        # Find solutions from all other agents
        for error_id, error_record in errors_data.items():
            source_agent = error_record.get('agent')

            # Skip if same agent (already handled by fix proposal engine)
            if source_agent == target_agent:
                continue

            # Check if issue type matches
            if error_record.get('error_type', '').lower() != issue_type.lower():
                continue

            # Assess transferability
            transferability = self._assess_transferability(
                source_agent,
                target_agent,
                issue_type,
                error_record
            )

            if transferability['is_transferable']:
                transferable_solutions.append({
                    'solution_id': error_id,
                    'source_agent': source_agent,
                    'target_agent': target_agent,
                    'issue_type': issue_type,
                    'solution': error_record.get('solution'),
                    'success_rate': error_record.get('success_rate', 1.0),
                    'times_used': error_record.get('times_encountered', 1),
                    'transferability': transferability['level'],
                    'confidence': transferability['confidence'],
                    'adaptation_needed': transferability['adaptation_needed'],
                    'adaptation_notes': transferability['adaptation_notes'],
                    'original_context': error_record.get('context', {})
                })

        # Sort by confidence and success rate
        transferable_solutions.sort(
            key=lambda x: (x['confidence'], x['success_rate']),
            reverse=True
        )

        logger.info(f"🧠 Found {len(transferable_solutions)} transferable solutions for {target_agent}")

        return transferable_solutions

    def _assess_transferability(self,
                               source_agent: str,
                               target_agent: str,
                               issue_type: str,
                               error_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess how transferable a solution is from source to target agent

        Returns:
            Transferability assessment
        """
        assessment = {
            'is_transferable': False,
            'level': KnowledgeTransferability.LOW,
            'confidence': 0.0,
            'adaptation_needed': True,
            'adaptation_notes': []
        }

        # Check if it's a universal pattern
        if any(pattern in issue_type.lower() for pattern in self.UNIVERSAL_PATTERNS):
            assessment['is_transferable'] = True
            assessment['level'] = KnowledgeTransferability.UNIVERSAL
            assessment['confidence'] = 0.95
            assessment['adaptation_needed'] = False
            assessment['adaptation_notes'].append("Universal pattern - applies to all agents")
            return assessment

        # Check agent similarity
        similar_agents = self.AGENT_SIMILARITIES.get(target_agent, [])

        if source_agent in similar_agents:
            # High similarity - high transferability
            assessment['is_transferable'] = True
            assessment['level'] = KnowledgeTransferability.HIGH
            assessment['confidence'] = 0.85
            assessment['adaptation_needed'] = True
            assessment['adaptation_notes'].append(
                f"{source_agent} and {target_agent} have similar responsibilities"
            )
        elif source_agent in self.AGENT_SIMILARITIES.get(source_agent, []):
            # Medium similarity
            assessment['is_transferable'] = True
            assessment['level'] = KnowledgeTransferability.MEDIUM
            assessment['confidence'] = 0.65
            assessment['adaptation_needed'] = True
            assessment['adaptation_notes'].append(
                "Agents have some overlap - adaptation recommended"
            )
        else:
            # Different agents - low but possible transferability
            assessment['is_transferable'] = True
            assessment['level'] = KnowledgeTransferability.LOW
            assessment['confidence'] = 0.40
            assessment['adaptation_needed'] = True
            assessment['adaptation_notes'].append(
                "Different agent types - careful adaptation required"
            )

        # Boost confidence if solution has high success rate
        success_rate = error_record.get('success_rate', 0.0)
        if success_rate >= 0.95:
            assessment['confidence'] = min(assessment['confidence'] + 0.1, 1.0)
            assessment['adaptation_notes'].append(
                f"High success rate ({success_rate:.0%}) increases confidence"
            )

        # Boost confidence if solution used multiple times
        times_used = error_record.get('times_encountered', 1)
        if times_used >= 5:
            assessment['confidence'] = min(assessment['confidence'] + 0.05, 1.0)
            assessment['adaptation_notes'].append(
                f"Proven solution (used {times_used} times)"
            )

        return assessment

    def recommend_knowledge_transfer(self,
                                    target_agent: str,
                                    issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        🧠 Recommend knowledge transfer from other agents

        Args:
            target_agent: Agent needing solution
            issue: Issue details

        Returns:
            Knowledge transfer recommendation
        """
        issue_type = issue.get('type', 'unknown')

        # Find transferable solutions
        transferable_solutions = self.find_transferable_solutions(
            target_agent,
            issue_type,
            issue.get('context', {})
        )

        recommendation = {
            'recommendation_id': self._generate_recommendation_id(target_agent, issue_type),
            'created_at': datetime.now().isoformat(),
            'target_agent': target_agent,
            'issue': issue,
            'transferable_solutions': transferable_solutions[:5],  # Top 5
            'recommended_action': None,
            'learning_opportunities': []
        }

        if transferable_solutions:
            # Get best solution
            best_solution = transferable_solutions[0]

            recommendation['recommended_action'] = {
                'action': 'transfer_and_adapt',
                'source_agent': best_solution['source_agent'],
                'solution': best_solution['solution'],
                'confidence': best_solution['confidence'],
                'adaptation_steps': self._generate_adaptation_steps(
                    best_solution,
                    target_agent
                )
            }

            # Identify learning opportunities
            for solution in transferable_solutions:
                if solution['transferability'] in [KnowledgeTransferability.HIGH, KnowledgeTransferability.UNIVERSAL]:
                    recommendation['learning_opportunities'].append({
                        'type': 'pattern_learning',
                        'description': f"Learn {issue_type} pattern from {solution['source_agent']}",
                        'benefit': 'Prevent similar issues in the future'
                    })
        else:
            recommendation['recommended_action'] = {
                'action': 'new_solution_needed',
                'reason': 'No transferable solutions found',
                'benefit': 'New solution can be shared with other agents'
            }

        # Store recommendation
        self._store_recommendation(recommendation)

        logger.info(f"🧠 Generated knowledge transfer recommendation for {target_agent}")

        return recommendation

    def _generate_adaptation_steps(self,
                                  solution: Dict[str, Any],
                                  target_agent: str) -> List[str]:
        """Generate steps to adapt solution for target agent"""
        steps = []

        if solution['adaptation_needed']:
            steps.append(f"Review {solution['source_agent']}'s solution for applicability")
            steps.append(f"Adapt solution for {target_agent}'s specific context")

            if solution['transferability'] == KnowledgeTransferability.LOW:
                steps.append("Carefully test adapted solution - low transferability")
            elif solution['transferability'] == KnowledgeTransferability.MEDIUM:
                steps.append("Test adapted solution in safe environment")

            steps.append(f"Update {target_agent}'s implementation")
            steps.append("Verify solution resolves the issue")
            steps.append("Record success/failure for future transfers")
        else:
            steps.append("Apply solution directly (universal pattern)")
            steps.append("Test in target agent context")
            steps.append("Verify and record results")

        return steps

    def record_transfer_attempt(self,
                               recommendation_id: str,
                               success: bool,
                               details: str,
                               actual_solution: str) -> bool:
        """
        Record the result of a knowledge transfer attempt

        Args:
            recommendation_id: Recommendation that was attempted
            success: Whether transfer succeeded
            details: Details about the transfer
            actual_solution: Final solution that was implemented

        Returns:
            True if recorded successfully
        """
        with open(self.learning_db, 'r') as f:
            data = json.load(f)

        transfer_record = {
            'recommendation_id': recommendation_id,
            'success': success,
            'details': details,
            'actual_solution': actual_solution,
            'recorded_at': datetime.now().isoformat()
        }

        data['knowledge_transfers'].append(transfer_record)

        if success:
            data['successful_transfers'].append(transfer_record)
        else:
            data['failed_transfers'].append(transfer_record)

        data['last_updated'] = datetime.now().isoformat()

        with open(self.learning_db, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"🧠 Recorded transfer attempt: {'success' if success else 'failed'}")

        return True

    def get_learning_stats(self, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get learning statistics

        Args:
            agent_name: Optional agent name to filter by

        Returns:
            Learning statistics
        """
        with open(self.learning_db, 'r') as f:
            data = json.load(f)

        stats = {
            'total_transfers': len(data.get('knowledge_transfers', [])),
            'successful_transfers': len(data.get('successful_transfers', [])),
            'failed_transfers': len(data.get('failed_transfers', [])),
            'success_rate': 0.0,
            'recommendations_generated': len(data.get('transfer_recommendations', [])),
        }

        if stats['total_transfers'] > 0:
            stats['success_rate'] = stats['successful_transfers'] / stats['total_transfers']

        # Agent-specific stats
        if agent_name:
            agent_transfers = [
                t for t in data.get('knowledge_transfers', [])
                if agent_name in str(t)  # Simple check
            ]
            stats['agent_specific'] = {
                'agent': agent_name,
                'transfers': len(agent_transfers),
                'successful': len([t for t in agent_transfers if t.get('success', False)])
            }

        return stats

    def propagate_universal_solution(self,
                                    solution: Dict[str, Any],
                                    source_agent: str) -> Dict[str, Any]:
        """
        🧠 Propagate a universal solution to all agents

        Args:
            solution: Solution to propagate
            source_agent: Agent that discovered the solution

        Returns:
            Propagation report
        """
        all_agents = [
            'batman', 'green_lantern', 'wonder_woman', 'flash', 'aquaman',
            'cyborg', 'atom', 'martian_manhunter', 'green_arrow',
            'plastic_man', 'zatanna'
        ]

        propagation_report = {
            'propagation_id': f"PROP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'source_agent': source_agent,
            'solution': solution,
            'target_agents': [],
            'propagation_results': [],
            'created_at': datetime.now().isoformat()
        }

        for agent in all_agents:
            if agent == source_agent:
                continue  # Skip source agent

            # Create transfer recommendation
            recommendation = {
                'target_agent': agent,
                'source_agent': source_agent,
                'solution': solution,
                'transferability': KnowledgeTransferability.UNIVERSAL,
                'confidence': 0.95,
                'propagation_id': propagation_report['propagation_id']
            }

            propagation_report['target_agents'].append(agent)
            propagation_report['propagation_results'].append({
                'agent': agent,
                'status': 'recommended',
                'recommendation': recommendation
            })

        logger.info(f"🧠 Propagated universal solution to {len(propagation_report['target_agents'])} agents")

        return propagation_report

    def _generate_recommendation_id(self, agent_name: str, issue_type: str) -> str:
        """Generate unique recommendation ID"""
        content = f"{agent_name}{issue_type}{datetime.now().isoformat()}"
        hash_val = hashlib.md5(content.encode()).hexdigest()[:8].upper()
        return f"REC-{hash_val}"

    def _store_recommendation(self, recommendation: Dict[str, Any]):
        """Store recommendation in database"""
        with open(self.learning_db, 'r') as f:
            data = json.load(f)

        data['transfer_recommendations'].append(recommendation)
        data['last_updated'] = datetime.now().isoformat()

        with open(self.learning_db, 'w') as f:
            json.dump(data, f, indent=2)


def share_knowledge_across_league(issue_type: str,
                                 source_agent: str,
                                 solution: str,
                                 is_universal: bool = False) -> Dict[str, Any]:
    """
    🧠 Share knowledge across the entire Justice League

    Args:
        issue_type: Type of issue solved
        source_agent: Agent that solved it
        solution: Solution that worked
        is_universal: Whether solution applies to all agents

    Returns:
        Knowledge sharing report
    """
    learning_system = CrossAgentLearning()

    if is_universal:
        # Propagate to all agents
        solution_data = {
            'type': issue_type,
            'solution': solution,
            'success_rate': 1.0
        }
        report = learning_system.propagate_universal_solution(solution_data, source_agent)
        report['sharing_type'] = 'universal'
    else:
        # Find similar agents and share
        similar_agents = CrossAgentLearning.AGENT_SIMILARITIES.get(source_agent, [])

        report = {
            'sharing_type': 'targeted',
            'source_agent': source_agent,
            'solution': solution,
            'shared_with': similar_agents,
            'created_at': datetime.now().isoformat()
        }

    logger.info(f"🧠 Shared knowledge from {source_agent} to {len(report.get('target_agents', report.get('shared_with', [])))} agents")

    return report
