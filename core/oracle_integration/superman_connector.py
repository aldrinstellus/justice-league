"""
🦸 Superman Connector
Interface for Superman to interact with Oracle

This connector provides Superman with:
- Agent health monitoring
- Version management
- Self-healing coordination
- Learning insights
- Dependency management

"Superman leads, Oracle supports. Together we protect the League." - Oracle
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class SupermanConnector:
    """
    🦸 Superman Connector

    Provides Superman with access to all Oracle capabilities:
    - Health monitoring for all agents
    - Version control and updates
    - Self-healing coordination
    - Learning insights and recommendations
    - Dependency analysis
    """

    def __init__(self, oracle_kb_dir: Optional[str] = None):
        """
        Initialize Superman Connector

        Args:
            oracle_kb_dir: Path to Oracle's knowledge base
        """
        self.kb_dir = Path(oracle_kb_dir) if oracle_kb_dir else Path('/tmp/aldo-vision-justice-league/oracle')
        self.kb_dir.mkdir(parents=True, exist_ok=True)

        # Connection status
        self.connection_db = self.kb_dir / 'superman_connection.json'
        self._init_connection()

        logger.info("🦸 Superman Connector initialized")

    def _init_connection(self):
        """Initialize connection database"""
        if not self.connection_db.exists():
            connection_data = {
                'connected': True,
                'connected_at': datetime.now().isoformat(),
                'last_heartbeat': datetime.now().isoformat(),
                'connection_history': [],
                'active_requests': []
            }

            with open(self.connection_db, 'w') as f:
                json.dump(connection_data, f, indent=2)

    def heartbeat(self) -> Dict[str, Any]:
        """
        🦸 Send heartbeat to Oracle

        Returns:
            Connection status and Oracle health
        """
        try:
            # Try to read existing data with error handling for concurrent access
            try:
                with open(self.connection_db, 'r') as f:
                    data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                # File corrupted or missing - reinitialize
                self._init_connection()
                with open(self.connection_db, 'r') as f:
                    data = json.load(f)

            data['last_heartbeat'] = datetime.now().isoformat()
            data['connected'] = True

            # Write atomically to prevent corruption during concurrent access
            import os
            temp_file = self.connection_db.with_suffix('.tmp')
            try:
                with open(temp_file, 'w') as f:
                    json.dump(data, f, indent=2)
                # Use os.replace for better cross-platform atomic operation
                os.replace(str(temp_file), str(self.connection_db))
            except OSError:
                # Fallback to direct write if atomic operation fails
                with open(self.connection_db, 'w') as f:
                    json.dump(data, f, indent=2)
                # Clean up temp file if it exists
                if temp_file.exists():
                    temp_file.unlink()

            return {
                'status': 'connected',
                'oracle_online': True,
                'last_heartbeat': data['last_heartbeat']
            }
        except Exception as e:
            logger.error(f"Heartbeat error: {e}")
            # Return degraded status on error
            return {
                'status': 'degraded',
                'oracle_online': False,
                'error': str(e),
                'last_heartbeat': datetime.now().isoformat()
            }

    def get_agent_health_summary(self) -> Dict[str, Any]:
        """
        🦸 Get health summary for all agents

        Returns:
            Complete health status for Justice League
        """
        from core.oracle_self_healing.health_monitor import AgentHealthMonitor

        monitor = AgentHealthMonitor(str(self.kb_dir))

        # All Justice League heroes
        agents = [
            'batman', 'superman', 'wonder_woman', 'flash', 'green_lantern',
            'aquaman', 'cyborg', 'martian_manhunter', 'hawkgirl',
            'green_arrow', 'black_canary'
        ]

        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_agents': len(agents),
            'healthy_agents': 0,
            'unhealthy_agents': 0,
            'warning_agents': 0,
            'agents': {}
        }

        for agent in agents:
            health = monitor.check_agent_health(agent, [])
            summary['agents'][agent] = health

            if health.get('status') == 'healthy':
                summary['healthy_agents'] += 1
            else:
                summary['unhealthy_agents'] += 1

            if health.get('warnings'):
                summary['warning_agents'] += 1

        summary['health_percentage'] = (summary['healthy_agents'] / summary['total_agents']) * 100

        logger.info(f"🦸 Health summary: {summary['healthy_agents']}/{summary['total_agents']} agents healthy")

        return summary

    def get_agent_versions(self) -> Dict[str, str]:
        """
        🦸 Get current versions of all agents

        Returns:
            Dict mapping agent names to versions
        """
        from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl

        vc = EnhancedVersionControl(str(self.kb_dir), git_enabled=False)

        agents = [
            'batman', 'superman', 'wonder_woman', 'flash', 'green_lantern',
            'aquaman', 'cyborg', 'martian_manhunter', 'hawkgirl',
            'green_arrow', 'black_canary'
        ]

        versions = {}
        for agent in agents:
            version = vc.get_current_version(agent)
            versions[agent] = version if version else '0.0.0'

        logger.info(f"🦸 Retrieved versions for {len(versions)} agents")

        return versions

    def request_version_update(self,
                              agent_name: str,
                              change_type: str,
                              changes: str,
                              breaking_changes: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        🦸 Request Oracle to create new version for agent

        Args:
            agent_name: Agent to update
            change_type: 'major', 'minor', or 'patch'
            changes: Description of changes
            breaking_changes: List of breaking changes (if any)

        Returns:
            Version update result
        """
        from core.oracle_version_control.enhanced_version_control import (
            EnhancedVersionControl, VersionChangeType
        )

        vc = EnhancedVersionControl(str(self.kb_dir), git_enabled=False)

        # Map string to VersionChangeType
        change_type_map = {
            'major': VersionChangeType.MAJOR,
            'minor': VersionChangeType.MINOR,
            'patch': VersionChangeType.PATCH
        }

        version = vc.create_version(
            agent_name,
            change_type_map[change_type],
            changes,
            breaking_changes
        )

        logger.info(f"🦸 Created version {version['version']} for {agent_name}")

        return version

    def analyze_update_impact(self, agent_name: str, new_version: str) -> Dict[str, Any]:
        """
        🦸 Analyze impact of updating an agent

        Args:
            agent_name: Agent to update
            new_version: Target version

        Returns:
            Impact analysis with affected agents
        """
        from core.oracle_version_control.dependency_tracker import DependencyTracker

        tracker = DependencyTracker(str(self.kb_dir))
        impact = tracker.analyze_update_impact(agent_name, new_version)

        logger.info(f"🦸 Update impact: {impact['total_affected']} agents affected")

        return impact

    def request_self_healing(self, agent_name: str) -> Dict[str, Any]:
        """
        🦸 Request Oracle to heal a failing agent

        Args:
            agent_name: Agent that needs healing

        Returns:
            Healing result
        """
        from core.oracle_self_healing.fix_proposal_engine import FixProposalEngine
        from core.oracle_self_healing.health_monitor import AgentHealthMonitor

        monitor = AgentHealthMonitor(str(self.kb_dir))
        engine = FixProposalEngine(str(self.kb_dir))

        # Check health first
        health = monitor.check_agent_health(agent_name, [])

        if health.get('status') == 'healthy':
            return {
                'success': True,
                'message': f'{agent_name} is already healthy',
                'health': health
            }

        # Generate fix proposals
        issues = health.get('issues_detected', [])
        proposals = []
        for issue in issues:
            proposal = engine.generate_fix_proposal(issue, agent_name)
            if proposal:
                proposals.append(proposal)

        # Auto-apply low-risk fixes
        applied_fixes = []
        for proposal in proposals:
            if proposal.get('risk_assessment', {}).get('level') == 'low':
                result = engine.apply_fix(proposal['proposal_id'])
                if result.get('success'):
                    applied_fixes.append(proposal)

        return {
            'success': len(applied_fixes) > 0,
            'agent': agent_name,
            'proposals_generated': len(proposals),
            'fixes_applied': len(applied_fixes),
            'applied_fixes': applied_fixes,
            'remaining_issues': [p for p in proposals if p not in applied_fixes]
        }

    def get_learning_insights(self, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """
        🦸 Get learning insights from Oracle

        Args:
            agent_name: Specific agent (optional, defaults to all)

        Returns:
            Learning insights and recommendations
        """
        from core.oracle_learning.cross_agent_learning import CrossAgentLearning

        learning = CrossAgentLearning(str(self.kb_dir))

        if agent_name:
            patterns = learning.get_learned_patterns(agent_name)
            recommendations = learning.get_recommendations(agent_name)

            return {
                'agent': agent_name,
                'patterns_learned': len(patterns),
                'patterns': patterns,
                'recommendations': recommendations
            }
        else:
            # All agents
            all_patterns = learning.get_all_patterns()

            return {
                'all_agents': True,
                'total_patterns': len(all_patterns),
                'patterns_by_category': self._categorize_patterns(all_patterns),
                'top_insights': self._get_top_insights(all_patterns)
            }

    def _categorize_patterns(self, patterns: List[Dict[str, Any]]) -> Dict[str, int]:
        """Categorize patterns by type"""
        categories = {}
        for pattern in patterns:
            category = pattern.get('category', 'unknown')
            categories[category] = categories.get(category, 0) + 1
        return categories

    def _get_top_insights(self, patterns: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
        """Get top insights by confidence"""
        sorted_patterns = sorted(
            patterns,
            key=lambda p: p.get('confidence', 0),
            reverse=True
        )
        return sorted_patterns[:limit]

    def get_dependency_graph(self) -> Dict[str, Any]:
        """
        🦸 Get dependency graph for all agents

        Returns:
            Complete dependency graph
        """
        from core.oracle_version_control.dependency_tracker import DependencyTracker

        tracker = DependencyTracker(str(self.kb_dir))

        # Generate comprehensive report
        report = tracker.generate_dependency_report()

        # Add visualization
        report['graph_text'] = tracker.visualize_dependency_graph('text')
        report['graph_mermaid'] = tracker.visualize_dependency_graph('mermaid')

        logger.info(f"🦸 Dependency graph: {report['total_dependencies']} dependencies")

        return report

    def coordinate_multi_agent_task(self,
                                   task_description: str,
                                   required_agents: List[str],
                                   priority: str = 'normal') -> Dict[str, Any]:
        """
        🦸 Coordinate multi-agent task with Oracle oversight

        Args:
            task_description: Description of task
            required_agents: List of agents needed
            priority: Task priority (low/normal/high/critical)

        Returns:
            Task coordination plan
        """
        from core.oracle_self_healing.health_monitor import AgentHealthMonitor
        from core.oracle_version_control.dependency_tracker import DependencyTracker

        monitor = AgentHealthMonitor(str(self.kb_dir))
        tracker = DependencyTracker(str(self.kb_dir))

        # Check health of required agents
        agent_status = {}
        all_healthy = True

        for agent in required_agents:
            health = monitor.check_agent_health(agent, [])
            is_healthy = health.get('status') == 'healthy'
            agent_status[agent] = {
                'healthy': is_healthy,
                'version': health.get('version', 'unknown'),
                'issues': health.get('issues_detected', [])
            }
            if not is_healthy:
                all_healthy = False

        # Determine execution order based on dependencies
        execution_order = []
        for agent in required_agents:
            deps = tracker.get_dependencies(agent)
            execution_order.append({
                'agent': agent,
                'dependencies': [d['agent'] for d in deps],
                'position': len([d for d in deps if d['agent'] in required_agents])
            })

        # Sort by dependency depth
        execution_order.sort(key=lambda x: x['position'])

        coordination_plan = {
            'task': task_description,
            'priority': priority,
            'required_agents': required_agents,
            'all_agents_healthy': all_healthy,
            'agent_status': agent_status,
            'execution_order': [e['agent'] for e in execution_order],
            'estimated_duration': len(required_agents) * 5,  # 5 seconds per agent
            'warnings': []
        }

        # Add warnings
        if not all_healthy:
            unhealthy = [a for a, s in agent_status.items() if not s['healthy']]
            coordination_plan['warnings'].append(
                f"Some agents are unhealthy: {', '.join(unhealthy)}"
            )

        logger.info(f"🦸 Coordinated task with {len(required_agents)} agents")

        return coordination_plan

    def get_oracle_status(self) -> Dict[str, Any]:
        """
        🦸 Get Oracle's overall status

        Returns:
            Oracle system status
        """
        status = {
            'timestamp': datetime.now().isoformat(),
            'oracle_online': True,
            'modules': {
                'knowledge_base': self._check_module('knowledge_base'),
                'self_healing': self._check_module('self_healing'),
                'learning': self._check_module('learning'),
                'version_control': self._check_module('version_control')
            },
            'superman_connected': True
        }

        # Count active capabilities
        status['active_capabilities'] = sum(
            1 for module in status['modules'].values() if module['available']
        )

        return status

    def _check_module(self, module_name: str) -> Dict[str, Any]:
        """Check if a module is available"""
        module_paths = {
            'knowledge_base': self.kb_dir / 'knowledge_base.db',
            'self_healing': self.kb_dir / 'agent_health.json',
            'learning': self.kb_dir / 'learned_patterns.json',
            'version_control': self.kb_dir / 'agent_versions.json'
        }

        path = module_paths.get(module_name)
        available = path.exists() if path else False

        return {
            'available': available,
            'path': str(path) if path else None
        }

    def emergency_rollback(self, agent_name: str, reason: str) -> Dict[str, Any]:
        """
        🦸 Emergency rollback for failing agent

        Args:
            agent_name: Agent to rollback
            reason: Reason for emergency rollback

        Returns:
            Rollback result
        """
        from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl
        from core.oracle_self_healing.health_monitor import AgentHealthMonitor

        vc = EnhancedVersionControl(str(self.kb_dir), git_enabled=False)
        monitor = AgentHealthMonitor(str(self.kb_dir))

        # Get last known good version
        # For emergency rollback, we'll use a simple fallback
        # In a real system, this would be stored in the health monitor
        last_good = '0.0.1'  # Default to first version

        # Attempt rollback
        rollback = vc.rollback_version(agent_name, last_good, force=True)

        # Log emergency action
        emergency_log = {
            'timestamp': datetime.now().isoformat(),
            'agent': agent_name,
            'reason': reason,
            'rollback_to': last_good,
            'success': rollback.get('success', False)
        }

        logger.warning(f"🚨 Emergency rollback: {agent_name} → v{last_good} (reason: {reason})")

        return {
            **rollback,
            'emergency': True,
            'reason': reason,
            'log': emergency_log
        }


def get_superman_interface(oracle_kb_dir: Optional[str] = None) -> SupermanConnector:
    """
    🦸 Get Superman's interface to Oracle

    Args:
        oracle_kb_dir: Path to Oracle KB

    Returns:
        Superman connector instance
    """
    return SupermanConnector(oracle_kb_dir)
