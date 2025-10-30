"""
🔗 Dependency Tracker
Track and manage dependencies between Justice League agents

This module provides:
- Inter-agent dependency mapping
- Dependency graph visualization
- Circular dependency detection
- Dependency impact analysis
- Update propagation planning

"Everything is connected. I track every dependency." - Oracle
"""

import logging
import json
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime
from pathlib import Path
from collections import defaultdict, deque

logger = logging.getLogger(__name__)


class DependencyType(str):
    """Types of dependencies"""
    REQUIRES = "requires"              # Hard dependency (must have)
    RECOMMENDS = "recommends"          # Soft dependency (should have)
    CONFLICTS = "conflicts"            # Incompatible versions
    ENHANCES = "enhances"              # Optional enhancement


class DependencyTracker:
    """
    🔗 Dependency Tracker

    Manages dependencies between Justice League agents:
    - Tracks inter-agent dependencies
    - Detects circular dependencies
    - Analyzes update impact
    - Plans update order
    """

    def __init__(self, oracle_kb_dir: Optional[str] = None):
        """
        Initialize Dependency Tracker

        Args:
            oracle_kb_dir: Path to Oracle's knowledge base
        """
        self.kb_dir = Path(oracle_kb_dir) if oracle_kb_dir else Path('/tmp/aldo-vision-justice-league/oracle')
        self.dependencies_db = self.kb_dir / 'agent_dependencies.json'

        # Initialize database
        if not self.dependencies_db.exists():
            self._init_dependencies_db()

        logger.info("🔗 Dependency Tracker initialized")

    def _init_dependencies_db(self):
        """Initialize dependencies database"""
        initial_data = {
            'dependencies': {},
            'dependency_graph': {},
            'update_history': [],
            'last_updated': datetime.now().isoformat()
        }

        with open(self.dependencies_db, 'w') as f:
            json.dump(initial_data, f, indent=2)

    def add_dependency(self,
                      agent_name: str,
                      depends_on: str,
                      version_constraint: str,
                      dependency_type: str = DependencyType.REQUIRES) -> bool:
        """
        🔗 Add dependency relationship

        Args:
            agent_name: Agent that has the dependency
            depends_on: Agent that is depended upon
            version_constraint: Version requirement (e.g., ">=1.0.0")
            dependency_type: Type of dependency

        Returns:
            True if added successfully
        """
        with open(self.dependencies_db, 'r') as f:
            data = json.load(f)

        if agent_name not in data['dependencies']:
            data['dependencies'][agent_name] = []

        # Check if dependency already exists
        existing = next(
            (d for d in data['dependencies'][agent_name] if d['agent'] == depends_on),
            None
        )

        if existing:
            # Update existing
            existing['version_constraint'] = version_constraint
            existing['dependency_type'] = dependency_type
            existing['updated_at'] = datetime.now().isoformat()
        else:
            # Add new
            data['dependencies'][agent_name].append({
                'agent': depends_on,
                'version_constraint': version_constraint,
                'dependency_type': dependency_type,
                'added_at': datetime.now().isoformat()
            })

        # Update dependency graph
        self._update_dependency_graph(data)

        data['last_updated'] = datetime.now().isoformat()

        with open(self.dependencies_db, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"🔗 Added dependency: {agent_name} → {depends_on} ({version_constraint})")

        return True

    def _update_dependency_graph(self, data: Dict[str, Any]):
        """Update the dependency graph structure"""
        graph = {}

        for agent, deps in data['dependencies'].items():
            graph[agent] = [d['agent'] for d in deps if d['dependency_type'] == DependencyType.REQUIRES]

        data['dependency_graph'] = graph

    def get_dependencies(self, agent_name: str) -> List[Dict[str, Any]]:
        """Get all dependencies for an agent"""
        with open(self.dependencies_db, 'r') as f:
            data = json.load(f)

        return data.get('dependencies', {}).get(agent_name, [])

    def get_dependents(self, agent_name: str) -> List[str]:
        """
        Get all agents that depend on this agent

        Args:
            agent_name: Agent to check

        Returns:
            List of agents that depend on this agent
        """
        with open(self.dependencies_db, 'r') as f:
            data = json.load(f)

        dependents = []

        for agent, deps in data.get('dependencies', {}).items():
            if any(d['agent'] == agent_name for d in deps):
                dependents.append(agent)

        return dependents

    def detect_circular_dependencies(self) -> List[List[str]]:
        """
        🔗 Detect circular dependency chains

        Returns:
            List of circular dependency chains
        """
        with open(self.dependencies_db, 'r') as f:
            data = json.load(f)

        graph = data.get('dependency_graph', {})
        cycles = []

        def dfs(node: str, path: List[str], visited: Set[str]):
            """Depth-first search for cycles"""
            if node in path:
                # Found cycle
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                if cycle not in cycles:
                    cycles.append(cycle)
                return

            if node in visited:
                return

            visited.add(node)
            path.append(node)

            for neighbor in graph.get(node, []):
                dfs(neighbor, path.copy(), visited)

        # Check each node
        for node in graph:
            dfs(node, [], set())

        logger.info(f"🔗 Detected {len(cycles)} circular dependency chains")

        return cycles

    def analyze_update_impact(self, agent_name: str, new_version: str) -> Dict[str, Any]:
        """
        🔗 Analyze impact of updating an agent

        Args:
            agent_name: Agent to update
            new_version: New version

        Returns:
            Impact analysis
        """
        impact = {
            'agent': agent_name,
            'new_version': new_version,
            'direct_dependents': [],
            'indirect_dependents': [],
            'total_affected': 0,
            'breaking_risk': 'low',
            'update_order': [],
            'warnings': []
        }

        # Get direct dependents
        direct = self.get_dependents(agent_name)
        impact['direct_dependents'] = direct

        # Get indirect dependents (dependents of dependents)
        indirect = set()
        for dep in direct:
            indirect.update(self._get_all_dependents(dep))
        indirect -= set(direct)  # Remove direct dependents
        impact['indirect_dependents'] = list(indirect)

        impact['total_affected'] = len(direct) + len(indirect)

        # Analyze breaking risk
        if impact['total_affected'] > 5:
            impact['breaking_risk'] = 'high'
            impact['warnings'].append(f"Update affects {impact['total_affected']} agents")
        elif impact['total_affected'] > 2:
            impact['breaking_risk'] = 'medium'

        # Calculate update order
        impact['update_order'] = self._calculate_update_order(agent_name)

        logger.info(f"🔗 Update impact for {agent_name}: {impact['total_affected']} agents affected")

        return impact

    def _get_all_dependents(self, agent_name: str) -> Set[str]:
        """Recursively get all dependents"""
        all_dependents = set()

        def collect_dependents(agent: str):
            dependents = self.get_dependents(agent)
            for dep in dependents:
                if dep not in all_dependents:
                    all_dependents.add(dep)
                    collect_dependents(dep)

        collect_dependents(agent_name)
        return all_dependents

    def _calculate_update_order(self, agent_name: str) -> List[str]:
        """
        Calculate order in which agents should be updated

        Returns agents in topological order (dependencies first)
        """
        with open(self.dependencies_db, 'r') as f:
            data = json.load(f)

        graph = data.get('dependency_graph', {})

        # Build reverse graph (dependents)
        reverse_graph = defaultdict(list)
        all_agents = set([agent_name])

        for agent, deps in graph.items():
            all_agents.add(agent)
            for dep in deps:
                reverse_graph[dep].append(agent)
                all_agents.add(dep)

        # Topological sort using Kahn's algorithm
        in_degree = {agent: 0 for agent in all_agents}
        for agent in all_agents:
            for dependent in reverse_graph.get(agent, []):
                in_degree[dependent] += 1

        queue = deque([agent for agent, degree in in_degree.items() if degree == 0])
        order = []

        while queue:
            agent = queue.popleft()
            order.append(agent)

            for dependent in reverse_graph.get(agent, []):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        return order

    def generate_dependency_report(self) -> Dict[str, Any]:
        """
        🔗 Generate comprehensive dependency report

        Returns:
            Complete dependency analysis
        """
        with open(self.dependencies_db, 'r') as f:
            data = json.load(f)

        # Detect circular dependencies
        circular = self.detect_circular_dependencies()

        # Count dependency types
        dependency_counts = defaultdict(int)
        for agent, deps in data.get('dependencies', {}).items():
            for dep in deps:
                dependency_counts[dep['dependency_type']] += 1

        # Find agents with most dependencies
        most_dependencies = sorted(
            [(agent, len(deps)) for agent, deps in data.get('dependencies', {}).items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]

        # Find most depended-upon agents
        dependent_counts = defaultdict(int)
        for agent, deps in data.get('dependencies', {}).items():
            for dep in deps:
                dependent_counts[dep['agent']] += 1

        most_depended = sorted(
            [(agent, count) for agent, count in dependent_counts.items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]

        report = {
            'generated_at': datetime.now().isoformat(),
            'total_agents': len(data.get('dependency_graph', {})),
            'total_dependencies': sum(len(deps) for deps in data.get('dependencies', {}).values()),
            'circular_dependencies': circular,
            'has_circular': len(circular) > 0,
            'dependency_type_counts': dict(dependency_counts),
            'agents_with_most_dependencies': most_dependencies,
            'most_depended_upon_agents': most_depended,
            'recommendations': []
        }

        # Generate recommendations
        if circular:
            report['recommendations'].append({
                'priority': 'high',
                'issue': f"{len(circular)} circular dependency chains detected",
                'action': 'Refactor to remove circular dependencies'
            })

        if any(count > 10 for _, count in most_dependencies):
            report['recommendations'].append({
                'priority': 'medium',
                'issue': 'Some agents have too many dependencies',
                'action': 'Consider reducing coupling'
            })

        logger.info(f"🔗 Dependency report: {report['total_dependencies']} dependencies, {len(circular)} circular")

        return report

    def visualize_dependency_graph(self, output_format: str = 'text') -> str:
        """
        Generate visualization of dependency graph

        Args:
            output_format: 'text' or 'mermaid' (for Mermaid.js diagrams)

        Returns:
            Graph visualization
        """
        with open(self.dependencies_db, 'r') as f:
            data = json.load(f)

        graph = data.get('dependency_graph', {})

        if output_format == 'mermaid':
            # Generate Mermaid.js diagram
            lines = ['graph TD']
            for agent, deps in graph.items():
                for dep in deps:
                    lines.append(f'    {agent}-->{dep}')
            return '\n'.join(lines)

        else:  # text format
            lines = ['Dependency Graph:', '']
            for agent, deps in sorted(graph.items()):
                if deps:
                    lines.append(f'{agent}:')
                    for dep in deps:
                        lines.append(f'  → {dep}')
                else:
                    lines.append(f'{agent}: (no dependencies)')
            return '\n'.join(lines)


def analyze_agent_dependencies(agent_name: str) -> Dict[str, Any]:
    """
    🔗 Analyze dependencies for a specific agent

    Args:
        agent_name: Agent to analyze

    Returns:
        Complete dependency analysis
    """
    tracker = DependencyTracker()

    analysis = {
        'agent': agent_name,
        'direct_dependencies': tracker.get_dependencies(agent_name),
        'dependents': tracker.get_dependents(agent_name),
        'update_impact': None,
        'circular_check': []
    }

    # Check for circular dependencies involving this agent
    all_circular = tracker.detect_circular_dependencies()
    analysis['circular_check'] = [c for c in all_circular if agent_name in c]

    # Analyze update impact
    if analysis['direct_dependencies']:
        analysis['update_impact'] = tracker.analyze_update_impact(agent_name, '2.0.0')

    logger.info(f"🔗 Analyzed {agent_name}: {len(analysis['direct_dependencies'])} dependencies, {len(analysis['dependents'])} dependents")

    return analysis
