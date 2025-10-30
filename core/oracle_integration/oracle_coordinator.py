"""
🔮 Oracle Coordinator
Oracle's side of coordination with Superman

This coordinator provides:
- Proactive monitoring and alerts
- Automated recommendations
- System-wide health oversight
- Predictive maintenance
- Emergency response coordination

"I don't just respond to Superman. I anticipate his needs." - Oracle
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class OracleCoordinator:
    """
    🔮 Oracle Coordinator

    Oracle's coordinating intelligence:
    - Monitors all agents proactively
    - Generates automated recommendations
    - Predicts failures before they happen
    - Coordinates emergency responses
    - Maintains system-wide awareness
    """

    def __init__(self, oracle_kb_dir: Optional[str] = None):
        """
        Initialize Oracle Coordinator

        Args:
            oracle_kb_dir: Path to Oracle's knowledge base
        """
        self.kb_dir = Path(oracle_kb_dir) if oracle_kb_dir else Path('/tmp/aldo-vision-justice-league/oracle')
        self.kb_dir.mkdir(parents=True, exist_ok=True)

        self.coordination_db = self.kb_dir / 'coordination.json'
        self.alerts_db = self.kb_dir / 'alerts.json'

        self._init_databases()

        logger.info("🔮 Oracle Coordinator initialized")

    def _init_databases(self):
        """Initialize coordination databases"""
        if not self.coordination_db.exists():
            coordination_data = {
                'active_tasks': [],
                'pending_alerts': [],
                'recommendations': [],
                'system_status': {
                    'last_scan': datetime.now().isoformat(),
                    'next_scan': (datetime.now() + timedelta(minutes=5)).isoformat()
                }
            }

            with open(self.coordination_db, 'w') as f:
                json.dump(coordination_data, f, indent=2)

        if not self.alerts_db.exists():
            alerts_data = {
                'alerts': [],
                'alert_history': []
            }

            with open(self.alerts_db, 'w') as f:
                json.dump(alerts_data, f, indent=2)

    def perform_system_scan(self) -> Dict[str, Any]:
        """
        🔮 Perform comprehensive system scan

        Scans all agents and generates insights

        Returns:
            System scan results with recommendations
        """
        from core.oracle_self_healing.health_monitor import AgentHealthMonitor

        monitor = AgentHealthMonitor(str(self.kb_dir))

        # All Justice League heroes
        agents = [
            'batman', 'superman', 'wonder_woman', 'flash', 'green_lantern',
            'aquaman', 'cyborg', 'martian_manhunter', 'hawkgirl',
            'green_arrow', 'black_canary'
        ]

        scan_results = {
            'timestamp': datetime.now().isoformat(),
            'agents_scanned': len(agents),
            'health_issues': [],
            'predictions': [],
            'recommendations': [],
            'alerts': []
        }

        for agent in agents:
            # Check health
            health = monitor.check_agent_health(agent, [])

            # Check if agent is unhealthy based on status
            if health.get('status') != 'healthy':
                scan_results['health_issues'].append({
                    'agent': agent,
                    'issues': health.get('issues_detected', [])
                })

                # Create alert for unhealthy agents
                if health.get('status') == 'critical':
                    self._create_alert(
                        f"Critical health issue for {agent}",
                        'critical',
                        {
                            'agent': agent,
                            'status': health.get('status'),
                            'action': 'Immediate investigation required'
                        }
                    )

        # Generate recommendations
        scan_results['recommendations'] = self._generate_recommendations(scan_results)

        # Update coordination database
        with open(self.coordination_db, 'r') as f:
            data = json.load(f)

        data['system_status']['last_scan'] = datetime.now().isoformat()
        data['system_status']['next_scan'] = (datetime.now() + timedelta(minutes=5)).isoformat()
        data['recommendations'] = scan_results['recommendations']

        with open(self.coordination_db, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"🔮 System scan complete: {len(scan_results['health_issues'])} issues, {len(scan_results['predictions'])} predictions")

        return scan_results

    def _generate_recommendations(self, scan_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate automated recommendations based on scan"""
        recommendations = []

        # Health issue recommendations
        for issue in scan_results['health_issues']:
            recommendations.append({
                'priority': 'high',
                'type': 'health',
                'agent': issue['agent'],
                'recommendation': f"Investigate and fix health issues in {issue['agent']}",
                'details': issue['issues']
            })

        # Predictive maintenance recommendations
        for prediction in scan_results['predictions']:
            if prediction['probability'] > 0.6:
                recommendations.append({
                    'priority': 'medium',
                    'type': 'predictive',
                    'agent': prediction['agent'],
                    'recommendation': f"Schedule preventive maintenance for {prediction['agent']}",
                    'details': {
                        'probability': prediction['probability'],
                        'time_to_failure': prediction['time_to_failure']
                    }
                })

        return recommendations

    def _create_alert(self, message: str, severity: str, context: Dict[str, Any]):
        """Create new alert"""
        with open(self.alerts_db, 'r') as f:
            data = json.load(f)

        alert = {
            'id': f"alert_{len(data['alerts']) + 1}",
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'severity': severity,
            'context': context,
            'acknowledged': False
        }

        data['alerts'].append(alert)

        with open(self.alerts_db, 'w') as f:
            json.dump(data, f, indent=2)

        logger.warning(f"🚨 Alert created: {message}")

    def get_pending_alerts(self) -> List[Dict[str, Any]]:
        """
        🔮 Get pending alerts for Superman

        Returns:
            List of unacknowledged alerts
        """
        with open(self.alerts_db, 'r') as f:
            data = json.load(f)

        pending = [a for a in data['alerts'] if not a['acknowledged']]

        logger.info(f"🔮 {len(pending)} pending alerts")

        return pending

    def acknowledge_alert(self, alert_id: str) -> bool:
        """
        🔮 Acknowledge an alert

        Args:
            alert_id: Alert ID to acknowledge

        Returns:
            Success status
        """
        with open(self.alerts_db, 'r') as f:
            data = json.load(f)

        for alert in data['alerts']:
            if alert['id'] == alert_id:
                alert['acknowledged'] = True
                alert['acknowledged_at'] = datetime.now().isoformat()

                # Move to history
                data['alert_history'].append(alert)

                with open(self.alerts_db, 'w') as f:
                    json.dump(data, f, indent=2)

                return True

        return False

    def coordinate_version_update(self,
                                  agent_name: str,
                                  new_version: str) -> Dict[str, Any]:
        """
        🔮 Coordinate version update across dependencies

        Args:
            agent_name: Agent to update
            new_version: New version

        Returns:
            Update coordination plan
        """
        from core.oracle_version_control.dependency_tracker import DependencyTracker
        from core.oracle_version_control.breaking_change_detector import BreakingChangeDetector

        tracker = DependencyTracker(str(self.kb_dir))

        # Analyze impact
        impact = tracker.analyze_update_impact(agent_name, new_version)

        # Create update plan
        update_plan = {
            'agent': agent_name,
            'new_version': new_version,
            'update_order': impact['update_order'],
            'total_affected': impact['total_affected'],
            'breaking_risk': impact['breaking_risk'],
            'phases': []
        }

        # Phase the update
        if impact['total_affected'] == 0:
            # Simple update, no dependents
            update_plan['phases'].append({
                'phase': 1,
                'agents': [agent_name],
                'risk': 'low'
            })
        else:
            # Complex update with dependents
            # Phase 1: Update the target agent
            update_plan['phases'].append({
                'phase': 1,
                'agents': [agent_name],
                'risk': impact['breaking_risk'],
                'note': 'Update primary agent'
            })

            # Phase 2: Update direct dependents
            if impact['direct_dependents']:
                update_plan['phases'].append({
                    'phase': 2,
                    'agents': impact['direct_dependents'],
                    'risk': 'medium',
                    'note': 'Update direct dependents'
                })

            # Phase 3: Update indirect dependents
            if impact['indirect_dependents']:
                update_plan['phases'].append({
                    'phase': 3,
                    'agents': impact['indirect_dependents'],
                    'risk': 'low',
                    'note': 'Update indirect dependents'
                })

        logger.info(f"🔮 Update plan for {agent_name}: {len(update_plan['phases'])} phases, {impact['total_affected']} affected")

        return update_plan

    def monitor_active_tasks(self) -> Dict[str, Any]:
        """
        🔮 Monitor all active tasks

        Returns:
            Active task status
        """
        with open(self.coordination_db, 'r') as f:
            data = json.load(f)

        active_tasks = data.get('active_tasks', [])

        monitoring = {
            'timestamp': datetime.now().isoformat(),
            'total_active': len(active_tasks),
            'tasks_by_status': {},
            'overdue_tasks': []
        }

        for task in active_tasks:
            status = task.get('status', 'unknown')
            monitoring['tasks_by_status'][status] = monitoring['tasks_by_status'].get(status, 0) + 1

            # Check if overdue
            if 'deadline' in task:
                deadline = datetime.fromisoformat(task['deadline'])
                if deadline < datetime.now() and task['status'] != 'completed':
                    monitoring['overdue_tasks'].append(task)

        return monitoring

    def generate_system_report(self) -> Dict[str, Any]:
        """
        🔮 Generate comprehensive system report

        Returns:
            Complete system status report
        """
        from core.oracle_self_healing.health_monitor import AgentHealthMonitor
        from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl
        from core.oracle_version_control.dependency_tracker import DependencyTracker

        monitor = AgentHealthMonitor(str(self.kb_dir))
        vc = EnhancedVersionControl(str(self.kb_dir), git_enabled=False)
        tracker = DependencyTracker(str(self.kb_dir))

        # All agents
        agents = [
            'batman', 'superman', 'wonder_woman', 'flash', 'green_lantern',
            'aquaman', 'cyborg', 'martian_manhunter', 'hawkgirl',
            'green_arrow', 'black_canary'
        ]

        # Health summary
        healthy_count = 0
        for agent in agents:
            health = monitor.check_agent_health(agent, [])
            if health.get('status') == 'healthy':
                healthy_count += 1

        # Version summary
        versions = {}
        for agent in agents:
            version = vc.get_current_version(agent)
            versions[agent] = version if version else '0.0.0'

        # Dependency summary
        dep_report = tracker.generate_dependency_report()

        # Alerts
        pending_alerts = self.get_pending_alerts()

        report = {
            'generated_at': datetime.now().isoformat(),
            'system_health': {
                'total_agents': len(agents),
                'healthy_agents': healthy_count,
                'health_percentage': (healthy_count / len(agents)) * 100
            },
            'versions': versions,
            'dependencies': {
                'total': dep_report['total_dependencies'],
                'circular': dep_report['has_circular']
            },
            'alerts': {
                'pending': len(pending_alerts),
                'critical': len([a for a in pending_alerts if a['severity'] == 'critical'])
            },
            'oracle_status': 'operational'
        }

        logger.info(f"🔮 System report: {healthy_count}/{len(agents)} healthy, {len(pending_alerts)} alerts")

        return report

    def auto_heal_system(self) -> Dict[str, Any]:
        """
        🔮 Automatically heal system issues

        Returns:
            Auto-healing results
        """
        from core.oracle_self_healing.health_monitor import AgentHealthMonitor
        from core.oracle_self_healing.fix_proposal_engine import FixProposalEngine

        monitor = AgentHealthMonitor(str(self.kb_dir))
        engine = FixProposalEngine(str(self.kb_dir))

        agents = [
            'batman', 'superman', 'wonder_woman', 'flash', 'green_lantern',
            'aquaman', 'cyborg', 'martian_manhunter', 'hawkgirl',
            'green_arrow', 'black_canary'
        ]

        healing_results = {
            'timestamp': datetime.now().isoformat(),
            'agents_checked': len(agents),
            'issues_found': 0,
            'fixes_applied': 0,
            'healing_actions': []
        }

        for agent in agents:
            health = monitor.check_agent_health(agent, [])

            if health.get('status') != 'healthy':
                issues = health.get('issues_detected', [])
                healing_results['issues_found'] += len(issues)

                # Generate and apply fixes
                for issue in issues:
                    proposal = engine.generate_fix_proposal(issue, agent)
                    if proposal and proposal.get('risk_assessment', {}).get('level') == 'low':
                        result = engine.apply_fix(proposal['proposal_id'])
                        if result.get('success'):
                            healing_results['fixes_applied'] += 1
                            healing_results['healing_actions'].append({
                                'agent': agent,
                                'fix': proposal.get('fix_description', 'Unknown fix'),
                                'success': True
                            })

        logger.info(f"🔮 Auto-heal: {healing_results['fixes_applied']} fixes applied for {healing_results['issues_found']} issues")

        return healing_results


def get_oracle_coordinator(oracle_kb_dir: Optional[str] = None) -> OracleCoordinator:
    """
    🔮 Get Oracle coordinator instance

    Args:
        oracle_kb_dir: Path to Oracle KB

    Returns:
        Oracle coordinator instance
    """
    return OracleCoordinator(oracle_kb_dir)
