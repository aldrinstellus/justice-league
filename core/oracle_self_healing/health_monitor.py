"""
🏥 Oracle Health Monitor
Real-time agent health monitoring and issue detection

This module continuously monitors all Justice League agents and detects:
- Performance degradation
- Recurring errors
- Critical failures
- Resource issues
- SLA violations

"I watch over them all. When they stumble, I'm there to catch them." - Oracle
"""

import logging
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum
import statistics

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Agent health status levels"""
    HEALTHY = "healthy"
    WARNING = "warning"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class IssueType(Enum):
    """Types of issues that can be detected"""
    PERFORMANCE_DEGRADATION = "performance_degradation"
    HIGH_ERROR_RATE = "high_error_rate"
    RECURRING_ERROR = "recurring_error"
    TIMEOUT_ERRORS = "timeout_errors"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    SLA_VIOLATION = "sla_violation"
    DEPENDENCY_FAILURE = "dependency_failure"
    CONFIGURATION_ERROR = "configuration_error"


class AgentHealthMonitor:
    """
    🏥 Real-time Agent Health Monitor

    Continuously monitors all agents and detects issues before they become critical.
    Integrates with Oracle's knowledge base for context-aware monitoring.
    """

    # Health thresholds
    THRESHOLDS = {
        'success_rate_healthy': 0.95,      # 95%+ is healthy
        'success_rate_warning': 0.85,      # 85-95% is warning
        'success_rate_unhealthy': 0.70,    # 70-85% is unhealthy
        # < 70% is critical

        'response_time_healthy': 2000,     # < 2s is healthy
        'response_time_warning': 5000,     # 2-5s is warning
        'response_time_critical': 10000,   # > 10s is critical

        'error_rate_healthy': 0.02,        # < 2% is healthy
        'error_rate_warning': 0.05,        # 2-5% is warning
        'error_rate_critical': 0.10,       # > 10% is critical

        'memory_usage_warning': 0.80,      # > 80% is warning
        'memory_usage_critical': 0.95,     # > 95% is critical

        'consecutive_failures_warning': 3,  # 3 consecutive failures
        'consecutive_failures_critical': 5, # 5 consecutive failures
    }

    def __init__(self, oracle_metrics_path: Optional[str] = None):
        """
        Initialize Agent Health Monitor

        Args:
            oracle_metrics_path: Path to Oracle's metrics database
        """
        self.metrics_path = Path(oracle_metrics_path) if oracle_metrics_path else Path('/tmp/aldo-vision-justice-league/oracle/agent_metrics.json')
        self.health_reports_path = self.metrics_path.parent / 'health_reports.json'
        self.issues_db_path = self.metrics_path.parent / 'detected_issues.json'

        # Initialize databases
        if not self.health_reports_path.exists():
            self._init_health_reports()
        if not self.issues_db_path.exists():
            self._init_issues_db()

        logger.info("🏥 Agent Health Monitor initialized")

    def _init_health_reports(self):
        """Initialize health reports database"""
        initial_data = {
            'last_updated': datetime.now().isoformat(),
            'agents': {},
            'system_health': {
                'overall_status': HealthStatus.UNKNOWN.value,
                'last_check': datetime.now().isoformat()
            }
        }
        with open(self.health_reports_path, 'w') as f:
            json.dump(initial_data, f, indent=2)

    def _init_issues_db(self):
        """Initialize detected issues database"""
        initial_data = {
            'issues': [],
            'last_updated': datetime.now().isoformat(),
            'resolved_issues': []
        }
        with open(self.issues_db_path, 'w') as f:
            json.dump(initial_data, f, indent=2)

    def check_agent_health(self, agent_name: str, recent_metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        🏥 Check health of a specific agent

        Args:
            agent_name: Name of the agent to check
            recent_metrics: List of recent performance metrics

        Returns:
            Health report with status, issues, and recommendations
        """
        health_report = {
            'agent': agent_name,
            'timestamp': datetime.now().isoformat(),
            'status': HealthStatus.HEALTHY.value,
            'issues_detected': [],
            'warnings': [],
            'metrics_summary': {},
            'recommendations': [],
            'trend': 'stable'
        }

        if not recent_metrics or len(recent_metrics) == 0:
            health_report['status'] = HealthStatus.UNKNOWN.value
            health_report['warnings'].append("No metrics available for analysis")
            return health_report

        # Calculate metrics summary
        success_count = sum(1 for m in recent_metrics if m.get('success', False))
        total_count = len(recent_metrics)
        success_rate = success_count / total_count if total_count > 0 else 0

        execution_times = [m.get('execution_time', 0) for m in recent_metrics if 'execution_time' in m]
        avg_execution_time = statistics.mean(execution_times) if execution_times else 0

        error_count = total_count - success_count
        error_rate = error_count / total_count if total_count > 0 else 0

        health_report['metrics_summary'] = {
            'success_rate': round(success_rate, 3),
            'avg_execution_time': round(avg_execution_time, 2),
            'error_rate': round(error_rate, 3),
            'total_runs': total_count,
            'success_count': success_count,
            'error_count': error_count
        }

        # Check for performance degradation
        if success_rate < self.THRESHOLDS['success_rate_unhealthy']:
            health_report['status'] = HealthStatus.CRITICAL.value
            health_report['issues_detected'].append({
                'type': IssueType.HIGH_ERROR_RATE.value,
                'severity': 'critical',
                'message': f"Critical: Success rate at {success_rate:.1%} (< {self.THRESHOLDS['success_rate_unhealthy']:.1%})",
                'detected_at': datetime.now().isoformat()
            })
        elif success_rate < self.THRESHOLDS['success_rate_warning']:
            if health_report['status'] != HealthStatus.CRITICAL.value:
                health_report['status'] = HealthStatus.UNHEALTHY.value
            health_report['issues_detected'].append({
                'type': IssueType.PERFORMANCE_DEGRADATION.value,
                'severity': 'high',
                'message': f"Success rate degraded to {success_rate:.1%} (< {self.THRESHOLDS['success_rate_warning']:.1%})",
                'detected_at': datetime.now().isoformat()
            })
        elif success_rate < self.THRESHOLDS['success_rate_healthy']:
            if health_report['status'] == HealthStatus.HEALTHY.value:
                health_report['status'] = HealthStatus.WARNING.value
            health_report['warnings'].append(f"Success rate at {success_rate:.1%} - below optimal threshold")

        # Check response time
        if avg_execution_time > self.THRESHOLDS['response_time_critical']:
            if health_report['status'] not in [HealthStatus.CRITICAL.value, HealthStatus.UNHEALTHY.value]:
                health_report['status'] = HealthStatus.UNHEALTHY.value
            health_report['issues_detected'].append({
                'type': IssueType.PERFORMANCE_DEGRADATION.value,
                'severity': 'high',
                'message': f"Critical response time: {avg_execution_time:.0f}ms (> {self.THRESHOLDS['response_time_critical']}ms)",
                'detected_at': datetime.now().isoformat()
            })
        elif avg_execution_time > self.THRESHOLDS['response_time_warning']:
            if health_report['status'] == HealthStatus.HEALTHY.value:
                health_report['status'] = HealthStatus.WARNING.value
            health_report['warnings'].append(f"Response time elevated: {avg_execution_time:.0f}ms")

        # Check for consecutive failures
        consecutive_failures = self._count_consecutive_failures(recent_metrics)
        if consecutive_failures >= self.THRESHOLDS['consecutive_failures_critical']:
            health_report['status'] = HealthStatus.CRITICAL.value
            health_report['issues_detected'].append({
                'type': IssueType.HIGH_ERROR_RATE.value,
                'severity': 'critical',
                'message': f"Critical: {consecutive_failures} consecutive failures detected",
                'detected_at': datetime.now().isoformat()
            })
        elif consecutive_failures >= self.THRESHOLDS['consecutive_failures_warning']:
            if health_report['status'] not in [HealthStatus.CRITICAL.value]:
                health_report['status'] = HealthStatus.UNHEALTHY.value
            health_report['issues_detected'].append({
                'type': IssueType.HIGH_ERROR_RATE.value,
                'severity': 'high',
                'message': f"{consecutive_failures} consecutive failures detected",
                'detected_at': datetime.now().isoformat()
            })

        # Detect recurring error patterns
        recurring_errors = self._detect_recurring_errors(recent_metrics)
        if recurring_errors:
            for error_pattern in recurring_errors:
                health_report['issues_detected'].append({
                    'type': IssueType.RECURRING_ERROR.value,
                    'severity': 'medium',
                    'message': f"Recurring error: '{error_pattern['error']}' ({error_pattern['count']} times)",
                    'detected_at': datetime.now().isoformat(),
                    'pattern': error_pattern
                })

        # Analyze trend
        health_report['trend'] = self._analyze_trend(recent_metrics)

        # Generate recommendations
        health_report['recommendations'] = self._generate_recommendations(health_report)

        # Store health report
        self._store_health_report(agent_name, health_report)

        # If issues detected, store them
        if health_report['issues_detected']:
            self._store_detected_issues(agent_name, health_report['issues_detected'])

        logger.info(f"🏥 Health check for {agent_name}: {health_report['status']} ({len(health_report['issues_detected'])} issues)")

        return health_report

    def _count_consecutive_failures(self, metrics: List[Dict[str, Any]]) -> int:
        """Count consecutive failures at the end of metrics list"""
        consecutive = 0
        for metric in reversed(metrics):
            if not metric.get('success', False):
                consecutive += 1
            else:
                break
        return consecutive

    def _detect_recurring_errors(self, metrics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect recurring error patterns"""
        error_counts: Dict[str, int] = {}

        for metric in metrics:
            if not metric.get('success', False):
                error_msg = metric.get('error', 'Unknown error')
                # Normalize error message (first 50 chars)
                error_key = error_msg[:50]
                error_counts[error_key] = error_counts.get(error_key, 0) + 1

        # Return errors that occurred 3+ times
        recurring = []
        for error, count in error_counts.items():
            if count >= 3:
                recurring.append({
                    'error': error,
                    'count': count,
                    'frequency': count / len(metrics) if metrics else 0
                })

        return recurring

    def _analyze_trend(self, metrics: List[Dict[str, Any]]) -> str:
        """Analyze performance trend"""
        if len(metrics) < 5:
            return 'insufficient_data'

        # Split into two halves
        mid = len(metrics) // 2
        first_half = metrics[:mid]
        second_half = metrics[mid:]

        first_success_rate = sum(1 for m in first_half if m.get('success', False)) / len(first_half)
        second_success_rate = sum(1 for m in second_half if m.get('success', False)) / len(second_half)

        diff = second_success_rate - first_success_rate

        if diff > 0.1:
            return 'improving'
        elif diff < -0.1:
            return 'declining'
        else:
            return 'stable'

    def _generate_recommendations(self, health_report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations based on health report"""
        recommendations = []

        status = health_report['status']
        issues = health_report['issues_detected']
        metrics = health_report['metrics_summary']

        # Critical status recommendations
        if status == HealthStatus.CRITICAL.value:
            recommendations.append({
                'priority': 'critical',
                'action': 'immediate_investigation',
                'description': f"Agent {health_report['agent']} requires immediate attention",
                'suggested_steps': [
                    'Review recent error logs',
                    'Check agent configuration',
                    'Verify dependencies are available',
                    'Consider rolling back to previous version'
                ]
            })

        # High error rate
        if metrics.get('error_rate', 0) > self.THRESHOLDS['error_rate_critical']:
            recommendations.append({
                'priority': 'high',
                'action': 'reduce_error_rate',
                'description': f"Error rate at {metrics['error_rate']:.1%} - investigate root cause",
                'suggested_steps': [
                    'Analyze error patterns in Oracle knowledge base',
                    'Check for recent configuration changes',
                    'Review agent dependencies'
                ]
            })

        # Performance degradation
        avg_time = metrics.get('avg_execution_time', 0)
        if avg_time > self.THRESHOLDS['response_time_warning']:
            recommendations.append({
                'priority': 'medium',
                'action': 'optimize_performance',
                'description': f"Average execution time at {avg_time:.0f}ms - consider optimization",
                'suggested_steps': [
                    'Profile agent execution',
                    'Check for resource constraints',
                    'Review code for inefficiencies',
                    'Consider caching strategies'
                ]
            })

        # Recurring errors
        recurring_issues = [i for i in issues if i.get('type') == IssueType.RECURRING_ERROR.value]
        if recurring_issues:
            recommendations.append({
                'priority': 'medium',
                'action': 'fix_recurring_errors',
                'description': f"{len(recurring_issues)} recurring error patterns detected",
                'suggested_steps': [
                    'Query Oracle knowledge base for similar issues',
                    'Implement error-specific fixes',
                    'Add error handling for common cases'
                ]
            })

        # Declining trend
        if health_report.get('trend') == 'declining':
            recommendations.append({
                'priority': 'high',
                'action': 'investigate_decline',
                'description': "Performance trend is declining",
                'suggested_steps': [
                    'Compare with historical performance data',
                    'Check for environmental changes',
                    'Review recent code changes',
                    'Consider predictive maintenance'
                ]
            })

        return recommendations

    def _store_health_report(self, agent_name: str, health_report: Dict[str, Any]):
        """Store health report in database"""
        with open(self.health_reports_path, 'r') as f:
            data = json.load(f)

        if agent_name not in data['agents']:
            data['agents'][agent_name] = {
                'current_health': health_report,
                'history': []
            }
        else:
            # Move current to history
            if 'current_health' in data['agents'][agent_name]:
                data['agents'][agent_name]['history'].insert(0, data['agents'][agent_name]['current_health'])
                # Keep only last 50 reports
                data['agents'][agent_name]['history'] = data['agents'][agent_name]['history'][:50]

            data['agents'][agent_name]['current_health'] = health_report

        data['last_updated'] = datetime.now().isoformat()

        with open(self.health_reports_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _store_detected_issues(self, agent_name: str, issues: List[Dict[str, Any]]):
        """Store detected issues in issues database"""
        with open(self.issues_db_path, 'r') as f:
            data = json.load(f)

        for issue in issues:
            issue_record = {
                'id': f"ISSUE-{datetime.now().strftime('%Y%m%d%H%M%S')}-{len(data['issues'])}",
                'agent': agent_name,
                'issue_type': issue['type'],
                'severity': issue['severity'],
                'message': issue['message'],
                'detected_at': issue['detected_at'],
                'status': 'open',
                'resolution': None,
                'resolved_at': None
            }

            if 'pattern' in issue:
                issue_record['pattern'] = issue['pattern']

            data['issues'].append(issue_record)

        data['last_updated'] = datetime.now().isoformat()

        with open(self.issues_db_path, 'w') as f:
            json.dump(data, f, indent=2)

    def get_system_health(self) -> Dict[str, Any]:
        """
        🏥 Get overall system health across all agents

        Returns:
            System-wide health report
        """
        with open(self.health_reports_path, 'r') as f:
            data = json.load(f)

        agents = data.get('agents', {})

        system_health = {
            'overall_status': HealthStatus.HEALTHY.value,
            'timestamp': datetime.now().isoformat(),
            'total_agents': len(agents),
            'healthy_agents': 0,
            'warning_agents': 0,
            'unhealthy_agents': 0,
            'critical_agents': 0,
            'unknown_agents': 0,
            'agents_by_status': {},
            'system_recommendations': []
        }

        # Count agents by status
        for agent_name, agent_data in agents.items():
            current_health = agent_data.get('current_health', {})
            status = current_health.get('status', HealthStatus.UNKNOWN.value)

            if status not in system_health['agents_by_status']:
                system_health['agents_by_status'][status] = []
            system_health['agents_by_status'][status].append(agent_name)

            if status == HealthStatus.HEALTHY.value:
                system_health['healthy_agents'] += 1
            elif status == HealthStatus.WARNING.value:
                system_health['warning_agents'] += 1
            elif status == HealthStatus.UNHEALTHY.value:
                system_health['unhealthy_agents'] += 1
            elif status == HealthStatus.CRITICAL.value:
                system_health['critical_agents'] += 1
            else:
                system_health['unknown_agents'] += 1

        # Determine overall system health
        if system_health['critical_agents'] > 0:
            system_health['overall_status'] = HealthStatus.CRITICAL.value
            system_health['system_recommendations'].append({
                'priority': 'critical',
                'message': f"{system_health['critical_agents']} agent(s) in critical state - immediate action required"
            })
        elif system_health['unhealthy_agents'] > 0:
            system_health['overall_status'] = HealthStatus.UNHEALTHY.value
            system_health['system_recommendations'].append({
                'priority': 'high',
                'message': f"{system_health['unhealthy_agents']} agent(s) unhealthy - investigation recommended"
            })
        elif system_health['warning_agents'] > 0:
            system_health['overall_status'] = HealthStatus.WARNING.value
            system_health['system_recommendations'].append({
                'priority': 'medium',
                'message': f"{system_health['warning_agents']} agent(s) with warnings - monitor closely"
            })

        logger.info(f"🏥 System health: {system_health['overall_status']} ({system_health['healthy_agents']}/{system_health['total_agents']} healthy)")

        return system_health

    def get_open_issues(self, agent_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all open issues, optionally filtered by agent

        Args:
            agent_name: Optional agent name filter

        Returns:
            List of open issues
        """
        with open(self.issues_db_path, 'r') as f:
            data = json.load(f)

        issues = data.get('issues', [])

        # Filter open issues
        open_issues = [i for i in issues if i.get('status') == 'open']

        # Filter by agent if specified
        if agent_name:
            open_issues = [i for i in open_issues if i.get('agent') == agent_name]

        return open_issues

    def resolve_issue(self, issue_id: str, resolution: str) -> bool:
        """
        Mark an issue as resolved

        Args:
            issue_id: Issue ID to resolve
            resolution: Resolution description

        Returns:
            True if issue was resolved, False if not found
        """
        with open(self.issues_db_path, 'r') as f:
            data = json.load(f)

        for issue in data['issues']:
            if issue['id'] == issue_id:
                issue['status'] = 'resolved'
                issue['resolution'] = resolution
                issue['resolved_at'] = datetime.now().isoformat()

                # Move to resolved issues
                data['resolved_issues'].append(issue)

                data['last_updated'] = datetime.now().isoformat()

                with open(self.issues_db_path, 'w') as f:
                    json.dump(data, f, indent=2)

                logger.info(f"🏥 Resolved issue {issue_id}: {resolution}")
                return True

        return False


def monitor_all_agents(metrics_db_path: str) -> Dict[str, Any]:
    """
    🏥 Monitor all agents and generate comprehensive health report

    Args:
        metrics_db_path: Path to Oracle's metrics database

    Returns:
        Complete health monitoring report
    """
    monitor = AgentHealthMonitor(metrics_db_path)

    # Load metrics from Oracle
    with open(metrics_db_path, 'r') as f:
        metrics_data = json.load(f)

    agent_health_reports = {}

    # Check health of each agent
    for agent_name, agent_metrics in metrics_data.items():
        if isinstance(agent_metrics, dict) and 'history' in agent_metrics:
            recent_metrics = agent_metrics['history'][-20:]  # Last 20 runs
            health_report = monitor.check_agent_health(agent_name, recent_metrics)
            agent_health_reports[agent_name] = health_report

    # Get system health
    system_health = monitor.get_system_health()

    # Get open issues
    open_issues = monitor.get_open_issues()

    return {
        'timestamp': datetime.now().isoformat(),
        'system_health': system_health,
        'agent_health': agent_health_reports,
        'open_issues': open_issues,
        'monitoring_status': 'active'
    }
