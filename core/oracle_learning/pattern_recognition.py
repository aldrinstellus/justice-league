"""
🔍 Pattern Recognition Engine
Automatically detect patterns in errors, solutions, and agent behavior

This module identifies patterns through:
- Error clustering and categorization
- Solution effectiveness analysis
- Temporal pattern detection
- Correlation analysis
- Predictive pattern matching

"Patterns emerge from chaos. I see them all." - Oracle
"""

import logging
import json
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter
import re

logger = logging.getLogger(__name__)


class PatternType(str):
    """Types of patterns that can be detected"""
    ERROR_CLUSTER = "error_cluster"              # Similar errors grouped
    TEMPORAL = "temporal"                        # Time-based patterns
    AGENT_SPECIFIC = "agent_specific"            # Patterns for specific agents
    SOLUTION_EFFECTIVENESS = "solution_effectiveness"  # Which solutions work best
    RECURRING = "recurring"                      # Recurring issues
    CORRELATION = "correlation"                  # Correlated issues
    PREDICTIVE = "predictive"                    # Predictive patterns


class PatternRecognition:
    """
    🔍 Pattern Recognition Engine

    Automatically detects patterns in:
    - Error types and frequencies
    - Solution effectiveness
    - Temporal trends
    - Agent behaviors
    - Issue correlations
    """

    # Minimum occurrences to consider it a pattern
    MIN_PATTERN_OCCURRENCES = 3

    # Time window for temporal patterns (in days)
    TEMPORAL_WINDOW_DAYS = 7

    def __init__(self, oracle_kb_dir: Optional[str] = None):
        """
        Initialize Pattern Recognition Engine

        Args:
            oracle_kb_dir: Path to Oracle's knowledge base
        """
        self.kb_dir = Path(oracle_kb_dir) if oracle_kb_dir else Path('/tmp/aldo-vision-justice-league/oracle')
        self.errors_db = self.kb_dir / 'errors_solutions.json'
        self.patterns_db = self.kb_dir / 'patterns.json'
        self.metrics_db = self.kb_dir / 'agent_metrics.json'

        # Initialize patterns database if needed
        if not self.patterns_db.exists():
            self._init_patterns_db()

        logger.info("🔍 Pattern Recognition Engine initialized")

    def _init_patterns_db(self):
        """Initialize patterns database"""
        initial_data = {
            'detected_patterns': [],
            'pattern_alerts': [],
            'pattern_history': [],
            'last_analysis': None,
            'statistics': {
                'total_patterns_detected': 0,
                'active_patterns': 0,
                'resolved_patterns': 0
            }
        }

        with open(self.patterns_db, 'w') as f:
            json.dump(initial_data, f, indent=2)

    def analyze_all_patterns(self) -> Dict[str, Any]:
        """
        🔍 Analyze all data and detect patterns

        Returns:
            Complete pattern analysis report
        """
        analysis_report = {
            'analyzed_at': datetime.now().isoformat(),
            'patterns_detected': [],
            'pattern_summary': defaultdict(int),
            'recommendations': []
        }

        # 1. Analyze error clustering
        error_clusters = self._detect_error_clusters()
        analysis_report['patterns_detected'].extend(error_clusters)
        analysis_report['pattern_summary'][PatternType.ERROR_CLUSTER] = len(error_clusters)

        # 2. Analyze temporal patterns
        temporal_patterns = self._detect_temporal_patterns()
        analysis_report['patterns_detected'].extend(temporal_patterns)
        analysis_report['pattern_summary'][PatternType.TEMPORAL] = len(temporal_patterns)

        # 3. Analyze solution effectiveness
        solution_patterns = self._analyze_solution_effectiveness()
        analysis_report['patterns_detected'].extend(solution_patterns)
        analysis_report['pattern_summary'][PatternType.SOLUTION_EFFECTIVENESS] = len(solution_patterns)

        # 4. Detect recurring issues
        recurring_patterns = self._detect_recurring_issues()
        analysis_report['patterns_detected'].extend(recurring_patterns)
        analysis_report['pattern_summary'][PatternType.RECURRING] = len(recurring_patterns)

        # 5. Detect correlations
        correlations = self._detect_correlations()
        analysis_report['patterns_detected'].extend(correlations)
        analysis_report['pattern_summary'][PatternType.CORRELATION] = len(correlations)

        # 6. Agent-specific patterns
        agent_patterns = self._detect_agent_specific_patterns()
        analysis_report['patterns_detected'].extend(agent_patterns)
        analysis_report['pattern_summary'][PatternType.AGENT_SPECIFIC] = len(agent_patterns)

        # Generate recommendations
        analysis_report['recommendations'] = self._generate_pattern_recommendations(
            analysis_report['patterns_detected']
        )

        # Store patterns
        self._store_patterns(analysis_report['patterns_detected'])

        # Update statistics
        with open(self.patterns_db, 'r') as f:
            data = json.load(f)
        data['last_analysis'] = datetime.now().isoformat()
        data['statistics']['total_patterns_detected'] = len(analysis_report['patterns_detected'])
        data['statistics']['active_patterns'] = len([p for p in analysis_report['patterns_detected'] if p.get('active', True)])
        with open(self.patterns_db, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"🔍 Pattern analysis complete: {len(analysis_report['patterns_detected'])} patterns detected")

        return analysis_report

    def _detect_error_clusters(self) -> List[Dict[str, Any]]:
        """Detect clusters of similar errors"""
        if not self.errors_db.exists():
            return []

        with open(self.errors_db, 'r') as f:
            errors_data = json.load(f)

        # Group errors by type
        error_types = defaultdict(list)
        for error_id, error_record in errors_data.items():
            error_type = error_record.get('error_type', 'unknown')
            error_types[error_type].append(error_record)

        clusters = []

        for error_type, errors in error_types.items():
            if len(errors) >= self.MIN_PATTERN_OCCURRENCES:
                # This is a cluster
                affected_agents = list(set(e.get('agent') for e in errors))
                total_occurrences = sum(e.get('times_encountered', 1) for e in errors)
                avg_success_rate = sum(e.get('success_rate', 0) for e in errors) / len(errors)

                cluster = {
                    'pattern_id': f"CLUSTER-{error_type.upper()[:10]}-{len(errors)}",
                    'pattern_type': PatternType.ERROR_CLUSTER,
                    'error_type': error_type,
                    'cluster_size': len(errors),
                    'affected_agents': affected_agents,
                    'total_occurrences': total_occurrences,
                    'avg_success_rate': round(avg_success_rate, 3),
                    'detected_at': datetime.now().isoformat(),
                    'active': True,
                    'severity': 'high' if len(affected_agents) > 3 else 'medium',
                    'description': f"Cluster of {len(errors)} {error_type} errors across {len(affected_agents)} agents"
                }

                clusters.append(cluster)

        return clusters

    def _detect_temporal_patterns(self) -> List[Dict[str, Any]]:
        """Detect time-based patterns"""
        if not self.metrics_db.exists():
            return []

        with open(self.metrics_db, 'r') as f:
            metrics_data = json.load(f)

        temporal_patterns = []

        # Analyze each agent's temporal trends
        for agent_name, agent_data in metrics_data.items():
            if not isinstance(agent_data, dict) or 'history' not in agent_data:
                continue

            history = agent_data['history']
            if len(history) < self.MIN_PATTERN_OCCURRENCES:
                continue

            # Check for time-of-day patterns (if timestamps available)
            # Check for day-of-week patterns
            # Check for degradation trends

            # Simple trend detection: compare recent vs. older performance
            if len(history) >= 10:
                recent = history[-5:]  # Last 5 runs
                older = history[-10:-5]  # Previous 5 runs

                recent_success = sum(1 for m in recent if m.get('success', False)) / len(recent)
                older_success = sum(1 for m in older if m.get('success', False)) / len(older)

                # Significant degradation
                if older_success - recent_success > 0.3:  # 30% drop
                    pattern = {
                        'pattern_id': f"TEMPORAL-{agent_name.upper()}-DEGRADATION",
                        'pattern_type': PatternType.TEMPORAL,
                        'agent': agent_name,
                        'trend': 'degradation',
                        'older_success_rate': round(older_success, 3),
                        'recent_success_rate': round(recent_success, 3),
                        'detected_at': datetime.now().isoformat(),
                        'active': True,
                        'severity': 'high',
                        'description': f"{agent_name} showing performance degradation: {older_success:.1%} → {recent_success:.1%}"
                    }
                    temporal_patterns.append(pattern)

                # Significant improvement
                elif recent_success - older_success > 0.3:  # 30% improvement
                    pattern = {
                        'pattern_id': f"TEMPORAL-{agent_name.upper()}-IMPROVEMENT",
                        'pattern_type': PatternType.TEMPORAL,
                        'agent': agent_name,
                        'trend': 'improvement',
                        'older_success_rate': round(older_success, 3),
                        'recent_success_rate': round(recent_success, 3),
                        'detected_at': datetime.now().isoformat(),
                        'active': True,
                        'severity': 'low',
                        'description': f"{agent_name} showing improvement: {older_success:.1%} → {recent_success:.1%}"
                    }
                    temporal_patterns.append(pattern)

        return temporal_patterns

    def _analyze_solution_effectiveness(self) -> List[Dict[str, Any]]:
        """Analyze which solutions are most effective"""
        if not self.errors_db.exists():
            return []

        with open(self.errors_db, 'r') as f:
            errors_data = json.load(f)

        # Group solutions by type/category
        solution_groups = defaultdict(list)

        for error_id, error_record in errors_data.items():
            solution = error_record.get('solution', '')
            error_type = error_record.get('error_type', 'unknown')

            # Extract solution category (first few words)
            solution_category = ' '.join(solution.split()[:3]) if solution else 'unknown'

            solution_groups[error_type].append({
                'solution': solution,
                'category': solution_category,
                'success_rate': error_record.get('success_rate', 0.0),
                'times_used': error_record.get('times_encountered', 1)
            })

        effectiveness_patterns = []

        for error_type, solutions in solution_groups.items():
            if len(solutions) >= self.MIN_PATTERN_OCCURRENCES:
                # Find most effective solutions
                best_solutions = sorted(solutions, key=lambda x: x['success_rate'], reverse=True)[:3]

                if best_solutions and best_solutions[0]['success_rate'] >= 0.9:
                    pattern = {
                        'pattern_id': f"EFFECTIVE-{error_type.upper()[:10]}",
                        'pattern_type': PatternType.SOLUTION_EFFECTIVENESS,
                        'error_type': error_type,
                        'best_solutions': best_solutions,
                        'detected_at': datetime.now().isoformat(),
                        'active': True,
                        'severity': 'low',
                        'description': f"Highly effective solutions identified for {error_type} (success rate: {best_solutions[0]['success_rate']:.1%})"
                    }
                    effectiveness_patterns.append(pattern)

        return effectiveness_patterns

    def _detect_recurring_issues(self) -> List[Dict[str, Any]]:
        """Detect issues that keep recurring"""
        if not self.errors_db.exists():
            return []

        with open(self.errors_db, 'r') as f:
            errors_data = json.load(f)

        recurring_patterns = []

        for error_id, error_record in errors_data.items():
            times_encountered = error_record.get('times_encountered', 1)

            # If encountered 5+ times, it's recurring
            if times_encountered >= 5:
                agent = error_record.get('agent')
                error_type = error_record.get('error_type')

                pattern = {
                    'pattern_id': f"RECURRING-{agent.upper()}-{error_type.upper()[:10]}",
                    'pattern_type': PatternType.RECURRING,
                    'agent': agent,
                    'error_type': error_type,
                    'occurrences': times_encountered,
                    'success_rate': error_record.get('success_rate', 0.0),
                    'detected_at': datetime.now().isoformat(),
                    'active': True,
                    'severity': 'high' if error_record.get('success_rate', 0) < 0.8 else 'medium',
                    'description': f"Recurring {error_type} in {agent} ({times_encountered} times, {error_record.get('success_rate', 0):.1%} success)"
                }
                recurring_patterns.append(pattern)

        return recurring_patterns

    def _detect_correlations(self) -> List[Dict[str, Any]]:
        """Detect correlated issues across agents"""
        if not self.errors_db.exists():
            return []

        with open(self.errors_db, 'r') as f:
            errors_data = json.load(f)

        # Group errors by type and check if they affect multiple agents
        error_by_type = defaultdict(list)

        for error_id, error_record in errors_data.items():
            error_type = error_record.get('error_type')
            agent = error_record.get('agent')
            error_by_type[error_type].append(agent)

        correlations = []

        for error_type, agents in error_by_type.items():
            unique_agents = list(set(agents))

            # If same error type affects 3+ agents, there's a correlation
            if len(unique_agents) >= 3:
                pattern = {
                    'pattern_id': f"CORR-{error_type.upper()[:10]}-{len(unique_agents)}AGENTS",
                    'pattern_type': PatternType.CORRELATION,
                    'error_type': error_type,
                    'correlated_agents': unique_agents,
                    'correlation_strength': len(unique_agents) / 11.0,  # 11 total agents
                    'detected_at': datetime.now().isoformat(),
                    'active': True,
                    'severity': 'high' if len(unique_agents) > 5 else 'medium',
                    'description': f"{error_type} affects {len(unique_agents)} agents - likely systemic issue"
                }
                correlations.append(pattern)

        return correlations

    def _detect_agent_specific_patterns(self) -> List[Dict[str, Any]]:
        """Detect patterns specific to individual agents"""
        if not self.errors_db.exists():
            return []

        with open(self.errors_db, 'r') as f:
            errors_data = json.load(f)

        # Count errors by agent
        agent_errors = defaultdict(list)

        for error_id, error_record in errors_data.items():
            agent = error_record.get('agent')
            agent_errors[agent].append(error_record)

        agent_patterns = []

        for agent, errors in agent_errors.items():
            if len(errors) >= self.MIN_PATTERN_OCCURRENCES:
                # Check if agent has a dominant error type
                error_types = Counter(e.get('error_type') for e in errors)
                most_common = error_types.most_common(1)[0]

                if most_common[1] >= 3:  # Same error type 3+ times
                    pattern = {
                        'pattern_id': f"AGENT-{agent.upper()}-{most_common[0].upper()[:10]}",
                        'pattern_type': PatternType.AGENT_SPECIFIC,
                        'agent': agent,
                        'dominant_error_type': most_common[0],
                        'occurrences': most_common[1],
                        'detected_at': datetime.now().isoformat(),
                        'active': True,
                        'severity': 'medium',
                        'description': f"{agent} has recurring {most_common[0]} pattern ({most_common[1]} occurrences)"
                    }
                    agent_patterns.append(pattern)

        return agent_patterns

    def _generate_pattern_recommendations(self, patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations from detected patterns"""
        recommendations = []

        # Group patterns by type
        by_type = defaultdict(list)
        for pattern in patterns:
            by_type[pattern['pattern_type']].append(pattern)

        # Recommendations for error clusters
        if by_type[PatternType.ERROR_CLUSTER]:
            for cluster in by_type[PatternType.ERROR_CLUSTER]:
                if cluster['severity'] == 'high':
                    recommendations.append({
                        'priority': 'high',
                        'pattern_id': cluster['pattern_id'],
                        'recommendation': f"Address {cluster['error_type']} cluster affecting {len(cluster['affected_agents'])} agents",
                        'action': 'Create universal fix and propagate to all affected agents',
                        'benefit': 'Resolve multiple related issues simultaneously'
                    })

        # Recommendations for temporal degradation
        if by_type[PatternType.TEMPORAL]:
            for temporal in by_type[PatternType.TEMPORAL]:
                if temporal.get('trend') == 'degradation':
                    recommendations.append({
                        'priority': 'high',
                        'pattern_id': temporal['pattern_id'],
                        'recommendation': f"Investigate performance degradation in {temporal['agent']}",
                        'action': 'Review recent changes, check for resource issues',
                        'benefit': 'Prevent further degradation'
                    })

        # Recommendations for recurring issues
        if by_type[PatternType.RECURRING]:
            for recurring in by_type[PatternType.RECURRING]:
                if recurring['occurrences'] >= 10:
                    recommendations.append({
                        'priority': 'critical',
                        'pattern_id': recurring['pattern_id'],
                        'recommendation': f"Fix root cause of recurring {recurring['error_type']} in {recurring['agent']}",
                        'action': 'Current solution is not preventing recurrence - redesign fix',
                        'benefit': 'Eliminate recurring issue permanently'
                    })

        # Recommendations for correlations
        if by_type[PatternType.CORRELATION]:
            for corr in by_type[PatternType.CORRELATION]:
                recommendations.append({
                    'priority': 'high',
                    'pattern_id': corr['pattern_id'],
                    'recommendation': f"Systemic {corr['error_type']} issue detected",
                    'action': 'Fix at system level rather than per-agent',
                    'benefit': 'Resolve issue for all affected agents'
                })

        # Sort by priority
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        recommendations.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 3))

        return recommendations

    def _store_patterns(self, patterns: List[Dict[str, Any]]):
        """Store detected patterns in database"""
        with open(self.patterns_db, 'r') as f:
            data = json.load(f)

        # Add new patterns
        for pattern in patterns:
            # Check if pattern already exists
            existing = next(
                (p for p in data['detected_patterns'] if p.get('pattern_id') == pattern.get('pattern_id')),
                None
            )

            if existing:
                # Update existing pattern
                existing.update(pattern)
            else:
                # Add new pattern
                data['detected_patterns'].append(pattern)

        # Move old patterns to history
        current_time = datetime.now()
        old_patterns = []

        for pattern in data['detected_patterns']:
            detected_at = datetime.fromisoformat(pattern.get('detected_at', datetime.now().isoformat()))
            age_days = (current_time - detected_at).days

            if age_days > 30:  # Older than 30 days
                old_patterns.append(pattern)
                data['pattern_history'].append(pattern)

        # Remove old patterns from active list
        data['detected_patterns'] = [p for p in data['detected_patterns'] if p not in old_patterns]

        data['last_updated'] = datetime.now().isoformat()

        with open(self.patterns_db, 'w') as f:
            json.dump(data, f, indent=2)

    def get_active_patterns(self, pattern_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get currently active patterns

        Args:
            pattern_type: Optional filter by pattern type

        Returns:
            List of active patterns
        """
        with open(self.patterns_db, 'r') as f:
            data = json.load(f)

        patterns = [p for p in data.get('detected_patterns', []) if p.get('active', True)]

        if pattern_type:
            patterns = [p for p in patterns if p.get('pattern_type') == pattern_type]

        return patterns


def run_pattern_analysis() -> Dict[str, Any]:
    """
    🔍 Run complete pattern analysis

    Returns:
        Pattern analysis report
    """
    engine = PatternRecognition()
    report = engine.analyze_all_patterns()

    logger.info(f"🔍 Pattern analysis: {len(report['patterns_detected'])} patterns, {len(report['recommendations'])} recommendations")

    return report
