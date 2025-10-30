# 🔮 Oracle API Reference

**Complete API documentation for Oracle Meta-Agent**

Version: 1.0.0
Last Updated: January 2025

---

## Table of Contents

1. [Superman Connector API](#superman-connector-api)
2. [Oracle Coordinator API](#oracle-coordinator-api)
3. [Health Monitor API](#health-monitor-api)
4. [Version Control API](#version-control-api)
5. [Dependency Tracker API](#dependency-tracker-api)
6. [Self-Healing API](#self-healing-api)
7. [Learning System API](#learning-system-api)
8. [Data Types](#data-types)

---

## Superman Connector API

### `SupermanConnector`

Interface for Superman to access Oracle capabilities.

#### Constructor

```python
SupermanConnector(oracle_kb_dir: Optional[str] = None)
```

**Parameters:**
- `oracle_kb_dir` (str, optional): Path to Oracle's knowledge base. Defaults to `/tmp/aldo-vision-justice-league/oracle`

**Example:**
```python
from core.oracle_integration.superman_connector import SupermanConnector

connector = SupermanConnector('/path/to/kb')
```

---

#### `heartbeat()`

Send heartbeat to Oracle to verify connection.

**Returns:** `Dict[str, Any]`
```python
{
    'status': 'connected',
    'oracle_online': True,
    'last_heartbeat': '2025-01-23T10:00:00'
}
```

**Example:**
```python
status = connector.heartbeat()
if status['oracle_online']:
    print("Oracle is online")
```

---

#### `get_agent_health_summary()`

Get health summary for all Justice League agents.

**Returns:** `Dict[str, Any]`
```python
{
    'timestamp': str,           # ISO format timestamp
    'total_agents': int,        # Total number of agents (11)
    'healthy_agents': int,      # Number of healthy agents
    'unhealthy_agents': int,    # Number of unhealthy agents
    'warning_agents': int,      # Number with warnings
    'health_percentage': float, # Overall health percentage (0-100)
    'agents': {
        'agent_name': {
            'status': str,      # 'healthy', 'warning', 'unhealthy', 'critical'
            'warnings': List[str],
            'issues_detected': List[Dict],
            ...
        }
    }
}
```

**Example:**
```python
health = connector.get_agent_health_summary()
print(f"System Health: {health['health_percentage']:.1f}%")

for agent, status in health['agents'].items():
    if status['status'] != 'healthy':
        print(f"{agent}: {status['status']}")
```

---

#### `get_agent_versions()`

Get current versions of all agents.

**Returns:** `Dict[str, str]`
```python
{
    'batman': '1.2.3',
    'flash': '0.5.0',
    'wonder_woman': '2.1.0',
    ...
}
```

**Example:**
```python
versions = connector.get_agent_versions()
for agent, version in versions.items():
    print(f"{agent}: v{version}")
```

---

#### `request_version_update()`

Request Oracle to create new version for agent.

**Parameters:**
- `agent_name` (str): Agent to update
- `change_type` (str): 'major', 'minor', or 'patch'
- `changes` (str): Description of changes
- `breaking_changes` (List[str], optional): List of breaking changes

**Returns:** `Dict[str, Any]`
```python
{
    'agent': str,
    'version': str,              # New version number
    'change_type': str,
    'changes': str,
    'breaking_changes': List[str],
    'migration_required': bool,
    'created_at': str,
    ...
}
```

**Example:**
```python
version = connector.request_version_update(
    'batman',
    'minor',
    'Added stealth mode analysis',
    breaking_changes=[]
)
print(f"Created v{version['version']}")
```

---

#### `analyze_update_impact()`

Analyze impact of updating an agent.

**Parameters:**
- `agent_name` (str): Agent to update
- `new_version` (str): Target version

**Returns:** `Dict[str, Any]`
```python
{
    'agent': str,
    'new_version': str,
    'direct_dependents': List[str],      # Agents directly depending on this
    'indirect_dependents': List[str],    # Indirect dependents
    'total_affected': int,
    'breaking_risk': str,                # 'low', 'medium', 'high'
    'update_order': List[str],           # Order to update agents
    'warnings': List[str]
}
```

**Example:**
```python
impact = connector.analyze_update_impact('oracle', '2.0.0')
print(f"Affects {impact['total_affected']} agents")
print(f"Risk: {impact['breaking_risk']}")
```

---

#### `request_self_healing()`

Request Oracle to heal a failing agent.

**Parameters:**
- `agent_name` (str): Agent that needs healing

**Returns:** `Dict[str, Any]`
```python
{
    'success': bool,
    'agent': str,
    'proposals_generated': int,
    'fixes_applied': int,
    'applied_fixes': List[Dict],
    'remaining_issues': List[Dict]
}
```

**Example:**
```python
result = connector.request_self_healing('flash')
print(f"Applied {result['fixes_applied']} fixes")
```

---

#### `get_dependency_graph()`

Get dependency graph for all agents.

**Returns:** `Dict[str, Any]`
```python
{
    'total_agents': int,
    'total_dependencies': int,
    'circular_dependencies': List[List[str]],
    'has_circular': bool,
    'dependency_type_counts': Dict[str, int],
    'agents_with_most_dependencies': List[Tuple[str, int]],
    'most_depended_upon_agents': List[Tuple[str, int]],
    'graph_text': str,           # Text visualization
    'graph_mermaid': str,        # Mermaid diagram
    'recommendations': List[Dict]
}
```

**Example:**
```python
graph = connector.get_dependency_graph()
print(graph['graph_text'])
```

---

#### `coordinate_multi_agent_task()`

Coordinate multi-agent task with Oracle oversight.

**Parameters:**
- `task_description` (str): Description of task
- `required_agents` (List[str]): List of agents needed
- `priority` (str, optional): 'low', 'normal', 'high', 'critical'. Defaults to 'normal'

**Returns:** `Dict[str, Any]`
```python
{
    'task': str,
    'priority': str,
    'required_agents': List[str],
    'all_agents_healthy': bool,
    'agent_status': Dict[str, Dict],
    'execution_order': List[str],
    'estimated_duration': int,   # Seconds
    'warnings': List[str]
}
```

**Example:**
```python
plan = connector.coordinate_multi_agent_task(
    'Analyze complex website',
    ['batman', 'flash', 'oracle'],
    'high'
)
print(f"Order: {plan['execution_order']}")
```

---

#### `get_oracle_status()`

Get Oracle's overall system status.

**Returns:** `Dict[str, Any]`
```python
{
    'timestamp': str,
    'oracle_online': bool,
    'modules': {
        'knowledge_base': {
            'available': bool,
            'path': str
        },
        'self_healing': {...},
        'learning': {...},
        'version_control': {...}
    },
    'superman_connected': bool,
    'active_capabilities': int
}
```

**Example:**
```python
status = connector.get_oracle_status()
print(f"Oracle online: {status['oracle_online']}")
print(f"Active: {status['active_capabilities']}/4 modules")
```

---

#### `emergency_rollback()`

Emergency rollback for failing agent.

**Parameters:**
- `agent_name` (str): Agent to rollback
- `reason` (str): Reason for emergency rollback

**Returns:** `Dict[str, Any]`
```python
{
    'success': bool,
    'from_version': str,
    'to_version': str,
    'emergency': bool,          # Always True
    'reason': str,
    'safety_level': str,        # 'safe', 'caution', 'dangerous'
    'warnings': List[str],
    'log': Dict
}
```

**Example:**
```python
rollback = connector.emergency_rollback(
    'batman',
    'Critical production failure'
)
print(f"Rolled back: v{rollback['from_version']} → v{rollback['to_version']}")
```

---

## Oracle Coordinator API

### `OracleCoordinator`

Oracle's proactive coordination and monitoring system.

#### Constructor

```python
OracleCoordinator(oracle_kb_dir: Optional[str] = None)
```

**Parameters:**
- `oracle_kb_dir` (str, optional): Path to Oracle's knowledge base

**Example:**
```python
from core.oracle_integration.oracle_coordinator import OracleCoordinator

coordinator = OracleCoordinator('/path/to/kb')
```

---

#### `perform_system_scan()`

Perform comprehensive system scan of all agents.

**Returns:** `Dict[str, Any]`
```python
{
    'timestamp': str,
    'agents_scanned': int,
    'health_issues': List[Dict],
    'predictions': List[Dict],
    'recommendations': List[Dict],
    'alerts': List[Dict]
}
```

**Example:**
```python
scan = coordinator.perform_system_scan()
print(f"Scanned {scan['agents_scanned']} agents")
print(f"Found {len(scan['health_issues'])} issues")
```

---

#### `get_pending_alerts()`

Get pending unacknowledged alerts.

**Returns:** `List[Dict[str, Any]]`
```python
[
    {
        'id': str,
        'timestamp': str,
        'message': str,
        'severity': str,        # 'info', 'warning', 'critical'
        'context': Dict,
        'acknowledged': bool
    },
    ...
]
```

**Example:**
```python
alerts = coordinator.get_pending_alerts()
for alert in alerts:
    if alert['severity'] == 'critical':
        print(f"🚨 {alert['message']}")
```

---

#### `acknowledge_alert()`

Acknowledge an alert.

**Parameters:**
- `alert_id` (str): Alert ID to acknowledge

**Returns:** `bool` - Success status

**Example:**
```python
success = coordinator.acknowledge_alert('alert_1')
```

---

#### `coordinate_version_update()`

Coordinate version update across dependencies.

**Parameters:**
- `agent_name` (str): Agent to update
- `new_version` (str): New version number

**Returns:** `Dict[str, Any]`
```python
{
    'agent': str,
    'new_version': str,
    'update_order': List[str],
    'total_affected': int,
    'breaking_risk': str,
    'phases': List[Dict]        # Update phases
}
```

**Example:**
```python
plan = coordinator.coordinate_version_update('oracle', '2.0.0')
for phase in plan['phases']:
    print(f"Phase {phase['phase']}: {phase['agents']}")
```

---

#### `generate_system_report()`

Generate comprehensive system status report.

**Returns:** `Dict[str, Any]`
```python
{
    'generated_at': str,
    'system_health': {
        'total_agents': int,
        'healthy_agents': int,
        'health_percentage': float
    },
    'versions': Dict[str, str],
    'dependencies': {
        'total': int,
        'circular': bool
    },
    'alerts': {
        'pending': int,
        'critical': int
    },
    'oracle_status': str
}
```

**Example:**
```python
report = coordinator.generate_system_report()
print(f"Health: {report['system_health']['health_percentage']:.1f}%")
```

---

#### `auto_heal_system()`

Automatically heal system issues.

**Returns:** `Dict[str, Any]`
```python
{
    'timestamp': str,
    'agents_checked': int,
    'issues_found': int,
    'fixes_applied': int,
    'healing_actions': List[Dict]
}
```

**Example:**
```python
results = coordinator.auto_heal_system()
print(f"Fixed {results['fixes_applied']}/{results['issues_found']} issues")
```

---

## Health Monitor API

### `AgentHealthMonitor`

Real-time health monitoring for agents.

#### Constructor

```python
AgentHealthMonitor(oracle_metrics_path: Optional[str] = None)
```

---

#### `check_agent_health()`

Check health of a specific agent.

**Parameters:**
- `agent_name` (str): Name of agent to check
- `recent_metrics` (List[Dict[str, Any]]): Recent performance metrics

**Returns:** `Dict[str, Any]`
```python
{
    'agent': str,
    'timestamp': str,
    'status': str,              # HealthStatus enum value
    'issues_detected': List[Dict],
    'warnings': List[str],
    'metrics_summary': Dict,
    'recommendations': List[str],
    'trend': str               # 'improving', 'stable', 'degrading'
}
```

**Example:**
```python
from core.oracle_self_healing.health_monitor import AgentHealthMonitor

monitor = AgentHealthMonitor()
health = monitor.check_agent_health('batman', [
    {'success_rate': 0.95, 'response_time': 1500, ...},
    ...
])
```

---

#### `get_system_health()`

Get overall system health status.

**Returns:** `Dict[str, Any]`
```python
{
    'timestamp': str,
    'overall_status': str,
    'healthy_agents': int,
    'unhealthy_agents': int,
    'agents_status': Dict[str, str],
    'system_metrics': Dict
}
```

---

## Version Control API

### `EnhancedVersionControl`

Semantic versioning with git integration.

#### Constructor

```python
EnhancedVersionControl(oracle_kb_dir: str, git_enabled: bool = False)
```

**Parameters:**
- `oracle_kb_dir` (str): Path to Oracle KB
- `git_enabled` (bool): Enable git integration

---

#### `create_version()`

Create new version for an agent.

**Parameters:**
- `agent_name` (str): Agent name
- `change_type` (VersionChangeType): MAJOR, MINOR, or PATCH
- `changes` (str): Description of changes
- `breaking_changes` (List[str], optional): Breaking changes
- `dependencies` (Dict[str, str], optional): Version dependencies

**Returns:** `Dict[str, Any]`
```python
{
    'agent': str,
    'version': str,
    'change_type': str,
    'changes': str,
    'breaking_changes': List[str],
    'migration_required': bool,
    'migration_script': str,
    'created_at': str,
    'code_hash': str,
    'git_commit': str,
    'git_tag': str
}
```

**Example:**
```python
from core.oracle_version_control.enhanced_version_control import (
    EnhancedVersionControl, VersionChangeType
)

vc = EnhancedVersionControl('/tmp/oracle', git_enabled=True)
version = vc.create_version(
    'batman',
    VersionChangeType.MINOR,
    'Added new feature'
)
```

---

#### `rollback_version()`

Rollback agent to previous version.

**Parameters:**
- `agent_name` (str): Agent to rollback
- `target_version` (str): Target version to rollback to
- `force` (bool, optional): Force dangerous rollback. Defaults to False

**Returns:** `Dict[str, Any]`
```python
{
    'success': bool,
    'from_version': str,
    'to_version': str,
    'safety_level': str,
    'warnings': List[str],
    'breaking_changes': List[str],
    'migration_applied': bool,
    'method': str              # 'git_checkout' or 'backup_restore'
}
```

**Example:**
```python
rollback = vc.rollback_version('batman', '1.2.0')
if rollback['safety_level'] == 'dangerous':
    print("⚠️ Dangerous rollback!")
```

---

#### `get_version_history()`

Get version history for an agent.

**Parameters:**
- `agent_name` (str): Agent name
- `limit` (int, optional): Maximum versions to return

**Returns:** `List[Dict[str, Any]]` - List of version records

**Example:**
```python
history = vc.get_version_history('batman', limit=10)
for version in history:
    print(f"v{version['version']}: {version['changes']}")
```

---

#### `get_current_version()`

Get current version of an agent.

**Parameters:**
- `agent_name` (str): Agent name

**Returns:** `str` - Version number (e.g., "1.2.3")

**Example:**
```python
current = vc.get_current_version('batman')
print(f"Current version: v{current}")
```

---

## Dependency Tracker API

### `DependencyTracker`

Track and manage dependencies between agents.

#### Constructor

```python
DependencyTracker(oracle_kb_dir: Optional[str] = None)
```

---

#### `add_dependency()`

Add dependency relationship.

**Parameters:**
- `agent_name` (str): Agent that has the dependency
- `depends_on` (str): Agent that is depended upon
- `version_constraint` (str): Version requirement (e.g., ">=1.0.0")
- `dependency_type` (DependencyType, optional): Type of dependency

**Returns:** `bool` - Success status

**Example:**
```python
from core.oracle_version_control.dependency_tracker import (
    DependencyTracker, DependencyType
)

tracker = DependencyTracker()
tracker.add_dependency(
    'batman',
    'oracle',
    '>=1.0.0',
    DependencyType.REQUIRES
)
```

---

#### `get_dependencies()`

Get all dependencies for an agent.

**Parameters:**
- `agent_name` (str): Agent to check

**Returns:** `List[Dict[str, Any]]`
```python
[
    {
        'agent': str,
        'version_constraint': str,
        'dependency_type': str,
        'added_at': str
    },
    ...
]
```

---

#### `get_dependents()`

Get all agents that depend on this agent.

**Parameters:**
- `agent_name` (str): Agent to check

**Returns:** `List[str]` - List of dependent agent names

---

#### `detect_circular_dependencies()`

Detect circular dependency chains.

**Returns:** `List[List[str]]` - List of circular chains

**Example:**
```python
circular = tracker.detect_circular_dependencies()
if circular:
    for cycle in circular:
        print(f"Circular: {' → '.join(cycle)}")
```

---

#### `analyze_update_impact()`

Analyze impact of updating an agent.

**Parameters:**
- `agent_name` (str): Agent to update
- `new_version` (str): New version

**Returns:** `Dict[str, Any]`
```python
{
    'agent': str,
    'new_version': str,
    'direct_dependents': List[str],
    'indirect_dependents': List[str],
    'total_affected': int,
    'breaking_risk': str,
    'update_order': List[str],
    'warnings': List[str]
}
```

---

## Self-Healing API

### `FixProposalEngine`

Generate and apply fixes for detected issues.

#### Constructor

```python
FixProposalEngine(oracle_kb_dir: Optional[str] = None)
```

---

#### `generate_fix_proposal()`

Generate fix proposal for a detected issue.

**Parameters:**
- `issue` (Dict[str, Any]): Issue details from health monitor
- `agent_name` (str): Name of affected agent
- `context` (Dict[str, Any], optional): Additional context

**Returns:** `Dict[str, Any]`
```python
{
    'proposal_id': str,
    'agent': str,
    'issue_type': str,
    'fix_description': str,
    'risk_assessment': {
        'level': str,           # 'low', 'medium', 'high', 'critical'
        'confidence': float,
        'potential_impact': str
    },
    'rollback_plan': str,
    'estimated_downtime': int,
    'requires_approval': bool,
    'created_at': str
}
```

---

#### `apply_fix()`

Apply an approved fix.

**Parameters:**
- `proposal_id` (str): Proposal ID to apply

**Returns:** `Dict[str, Any]`
```python
{
    'success': bool,
    'proposal_id': str,
    'applied_at': str,
    'result': str,
    'error': str              # If failed
}
```

---

## Learning System API

### `CrossAgentLearning`

Cross-agent pattern recognition and knowledge sharing.

#### Constructor

```python
CrossAgentLearning(oracle_kb_dir: Optional[str] = None)
```

---

#### `learn_pattern()`

Learn a new pattern from agent behavior.

**Parameters:**
- `pattern_category` (str): Category of pattern
- `pattern_data` (Dict[str, Any]): Pattern details

**Example:**
```python
from core.oracle_learning.cross_agent_learning import CrossAgentLearning

learning = CrossAgentLearning()
learning.learn_pattern(
    'selector_optimization',
    {
        'agent': 'batman',
        'pattern': 'Use data-testid for stability',
        'confidence': 0.95,
        'success_rate_improvement': 0.15
    }
)
```

---

#### `get_learned_patterns()`

Get patterns learned by an agent.

**Parameters:**
- `agent_name` (str): Agent name

**Returns:** `List[Dict[str, Any]]` - List of learned patterns

---

#### `get_recommendations()`

Get learning-based recommendations for an agent.

**Parameters:**
- `agent_name` (str): Agent name

**Returns:** `List[str]` - List of recommendations

---

## Data Types

### Enums

#### `VersionChangeType`
```python
class VersionChangeType(str):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
```

#### `DependencyType`
```python
class DependencyType(str):
    REQUIRES = "requires"
    RECOMMENDS = "recommends"
    CONFLICTS = "conflicts"
    ENHANCES = "enhances"
```

#### `HealthStatus`
```python
class HealthStatus(str):
    HEALTHY = "healthy"
    WARNING = "warning"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"
    UNKNOWN = "unknown"
```

#### `RollbackSafety`
```python
class RollbackSafety(str):
    SAFE = "safe"
    CAUTION = "caution"
    DANGEROUS = "dangerous"
```

### Type Aliases

```python
from typing import Dict, List, Any, Optional

MetricsData = List[Dict[str, Any]]
VersionNumber = str
AgentName = str
Timestamp = str  # ISO 8601 format
```

---

## Error Handling

All API methods may raise exceptions. Always use try-except blocks:

```python
try:
    health = connector.get_agent_health_summary()
except Exception as e:
    logger.error(f"Failed to get health: {e}")
    # Handle error
```

Common exceptions:
- `FileNotFoundError`: Database file not found
- `json.JSONDecodeError`: Corrupted database
- `KeyError`: Missing required data
- `ValueError`: Invalid parameter value

---

**Oracle says**: "The API is the interface to wisdom. Use it with precision." 🔮
