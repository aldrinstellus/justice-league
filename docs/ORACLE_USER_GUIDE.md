# 🔮 Oracle User Guide

**Complete guide to using Oracle - The Justice League's Meta-Agent**

Version: 1.0.0
Last Updated: January 2025

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Core Capabilities](#core-capabilities)
4. [Using Oracle with Superman](#using-oracle-with-superman)
5. [Health Monitoring](#health-monitoring)
6. [Version Control](#version-control)
7. [Self-Healing](#self-healing)
8. [Learning System](#learning-system)
9. [Dependency Management](#dependency-management)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)

---

## Introduction

### What is Oracle?

Oracle is the Justice League's meta-agent - an intelligent oversight system that monitors, maintains, and optimizes all 11 Justice League heroes. Think of Oracle as the "guardian of the guardians" - ensuring that Batman, Flash, Wonder Woman, and all other heroes operate at peak performance.

### Key Features

- **🏥 Health Monitoring**: Real-time health checks for all agents
- **🔄 Version Control**: Semantic versioning with git integration
- **🔧 Self-Healing**: Automated issue detection and fixing
- **🧠 Learning System**: Cross-agent pattern recognition and knowledge sharing
- **🔗 Dependency Management**: Dependency tracking and circular detection
- **🦸 Superman Integration**: Seamless coordination with Superman coordinator

### Architecture Overview

```
Oracle Meta-Agent
├── Knowledge Base       (Central data storage)
├── Health Monitor       (Agent health tracking)
├── Version Control      (Semantic versioning)
├── Self-Healing         (Automated fixes)
├── Learning System      (Pattern recognition)
└── Superman Integration (Coordination interface)
```

---

## Getting Started

### Installation

Oracle is already integrated into the Aldo Vision system. No separate installation required.

### Basic Usage

```python
# Import Oracle components
from core.oracle_integration.superman_connector import get_superman_interface
from core.oracle_integration.oracle_coordinator import get_oracle_coordinator

# Get Superman's interface to Oracle
connector = get_superman_interface()

# Check system health
health = connector.get_agent_health_summary()
print(f"System Health: {health['health_percentage']:.1f}%")

# Get all agent versions
versions = connector.get_agent_versions()
for agent, version in versions.items():
    print(f"{agent}: v{version}")
```

### Configuration

Oracle uses a knowledge base directory for all data storage:

```python
# Default location
oracle_kb_dir = '/tmp/aldo-vision-justice-league/oracle'

# Custom location
connector = get_superman_interface('/path/to/custom/kb')
```

---

## Core Capabilities

### 1. Real-Time Health Monitoring

Oracle continuously monitors all 11 Justice League agents:

```python
# Get health summary for all agents
health = connector.get_agent_health_summary()

# Output:
{
    'total_agents': 11,
    'healthy_agents': 9,
    'unhealthy_agents': 2,
    'health_percentage': 81.8,
    'agents': {
        'batman': {'status': 'healthy', 'warnings': [], ...},
        'flash': {'status': 'warning', 'warnings': ['High response time'], ...},
        'aquaman': {'status': 'critical', 'issues': ['Memory leak'], ...}
    }
}
```

### 2. Version Control

Semantic versioning for all agents with rollback capability:

```python
# Create new version
version = connector.request_version_update(
    'batman',
    'minor',  # 'major', 'minor', or 'patch'
    'Added stealth mode analysis'
)
# Creates v0.1.0 → v0.2.0

# Rollback if needed
rollback = connector.emergency_rollback('batman', 'Deployment failed')
# Rolls back to previous stable version
```

### 3. Self-Healing

Automated detection and fixing of issues:

```python
# Request healing for an agent
result = connector.request_self_healing('flash')

# Output:
{
    'success': True,
    'proposals_generated': 5,
    'fixes_applied': 3,
    'applied_fixes': [
        {'fix': 'Restart agent process'},
        {'fix': 'Clear cache'},
        {'fix': 'Reset connection pool'}
    ]
}
```

### 4. Dependency Management

Track and manage dependencies between agents:

```python
# Get dependency graph
graph = connector.get_dependency_graph()

# Analyze update impact
impact = connector.analyze_update_impact('oracle', '2.0.0')
print(f"Affects {impact['total_affected']} agents")
print(f"Update order: {impact['update_order']}")
```

### 5. Learning System

Cross-agent learning and pattern recognition:

```python
# Get learning insights
insights = connector.get_learning_insights('batman')

# Output:
{
    'patterns_learned': 15,
    'recommendations': [
        'Consider caching frequently accessed selectors',
        'Increase timeout for dynamic content',
        ...
    ]
}
```

---

## Using Oracle with Superman

### Superman Connector Interface

Superman uses the SupermanConnector to access Oracle:

```python
from core.oracle_integration.superman_connector import get_superman_interface

connector = get_superman_interface()

# Send heartbeat
heartbeat = connector.heartbeat()
# Returns: {'status': 'connected', 'oracle_online': True}
```

### Common Superman Operations

#### 1. Morning Health Check

```python
# Check overall system health
health = connector.get_agent_health_summary()

if health['health_percentage'] < 80:
    print("⚠️ System health below 80%")

    # Get details on unhealthy agents
    for agent, status in health['agents'].items():
        if status['status'] != 'healthy':
            print(f"  {agent}: {status['status']}")

            # Request healing
            healing = connector.request_self_healing(agent)
            print(f"    Applied {healing['fixes_applied']} fixes")
```

#### 2. Coordinating Multi-Agent Tasks

```python
# Plan a multi-agent mission
plan = connector.coordinate_multi_agent_task(
    'Analyze e-commerce website with dynamic pricing',
    ['batman', 'flash', 'cyborg'],
    'high'
)

print(f"Execution order: {' → '.join(plan['execution_order'])}")
print(f"All agents healthy: {plan['all_agents_healthy']}")

if not plan['all_agents_healthy']:
    print("Warnings:")
    for warning in plan['warnings']:
        print(f"  - {warning}")
```

#### 3. Version Update Coordination

```python
# Before major update, analyze impact
impact = connector.analyze_update_impact('oracle', '2.0.0')

print(f"Total affected: {impact['total_affected']} agents")
print(f"Breaking risk: {impact['breaking_risk']}")
print(f"Update order: {impact['update_order']}")

# If acceptable, proceed with update
if impact['breaking_risk'] != 'high':
    version = connector.request_version_update(
        'oracle',
        'major',
        'Major feature update',
        breaking_changes=['API structure changed']
    )
```

---

## Health Monitoring

### Health Status Levels

Oracle uses four health status levels:

| Status | Description | Action Required |
|--------|-------------|-----------------|
| **healthy** | All metrics normal | None |
| **warning** | Some metrics degraded | Monitor closely |
| **unhealthy** | Multiple issues detected | Investigate soon |
| **critical** | Severe issues | Immediate action |

### Health Check Metrics

Oracle monitors these key metrics:

1. **Success Rate**
   - Healthy: > 95%
   - Warning: 85-95%
   - Unhealthy: 70-85%
   - Critical: < 70%

2. **Response Time**
   - Healthy: < 2 seconds
   - Warning: 2-5 seconds
   - Critical: > 10 seconds

3. **Error Rate**
   - Healthy: < 2%
   - Warning: 2-5%
   - Critical: > 10%

4. **Memory Usage**
   - Warning: > 80%
   - Critical: > 95%

### Custom Health Checks

Add custom health checks for specific agents:

```python
from core.oracle_self_healing.health_monitor import AgentHealthMonitor

monitor = AgentHealthMonitor()

# Check specific agent health
health = monitor.check_agent_health('batman', recent_metrics=[
    {'success_rate': 0.92, 'response_time': 1500, 'error_rate': 0.03},
    {'success_rate': 0.94, 'response_time': 1200, 'error_rate': 0.02},
    ...
])

print(f"Status: {health['status']}")
print(f"Issues: {health['issues_detected']}")
print(f"Recommendations: {health['recommendations']}")
```

---

## Version Control

### Semantic Versioning

Oracle follows SemVer (Semantic Versioning):

- **MAJOR** (x.0.0): Breaking changes
- **MINOR** (0.x.0): New features, backward compatible
- **PATCH** (0.0.x): Bug fixes

### Creating Versions

```python
# Patch version (bug fix)
v1 = connector.request_version_update(
    'batman',
    'patch',
    'Fixed selector timeout issue'
)
# 1.2.3 → 1.2.4

# Minor version (new feature)
v2 = connector.request_version_update(
    'batman',
    'minor',
    'Added support for iframe analysis'
)
# 1.2.4 → 1.3.0

# Major version (breaking change)
v3 = connector.request_version_update(
    'batman',
    'major',
    'Changed return structure for analyze()',
    breaking_changes=['analyze() now returns dict instead of list']
)
# 1.3.0 → 2.0.0
```

### Rollback Strategies

#### 1. Safe Rollback (Same major version)

```python
# Rollback within same major version
rollback = connector.emergency_rollback('batman', 'Minor bug detected')
# 2.3.1 → 2.3.0 (SAFE)
```

#### 2. Caution Rollback (Different minor version)

```python
# Rollback across minor versions
rollback = connector.emergency_rollback('batman', 'Feature causing issues')
# 2.3.0 → 2.2.0 (CAUTION)
```

#### 3. Dangerous Rollback (Different major version)

```python
# Rollback across major versions (use with extreme caution!)
rollback = connector.emergency_rollback('batman', 'Critical production failure')
# 2.0.0 → 1.5.0 (DANGEROUS)
```

### Version History

```python
from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl

vc = EnhancedVersionControl()

# Get version history
history = vc.get_version_history('batman')

for version in history:
    print(f"v{version['version']}: {version['changes']}")
    if version.get('breaking_changes'):
        print(f"  ⚠️ Breaking: {version['breaking_changes']}")
```

---

## Self-Healing

### How Self-Healing Works

1. **Detection**: Health monitor detects issues
2. **Analysis**: Determine root cause
3. **Proposal**: Generate fix proposals
4. **Risk Assessment**: Evaluate risk of each fix
5. **Execution**: Auto-apply low-risk fixes
6. **Verification**: Confirm fix worked

### Risk Levels

| Risk Level | Description | Auto-Apply |
|------------|-------------|------------|
| **low** | Safe, reversible changes | ✅ Yes |
| **medium** | Requires approval | ❌ No |
| **high** | Significant risk | ❌ No |
| **critical** | Dangerous, manual only | ❌ No |

### Manual Healing

For medium/high risk issues:

```python
from core.oracle_self_healing.fix_proposal_engine import FixProposalEngine

engine = FixProposalEngine()

# Get fix proposals
proposal = engine.generate_fix_proposal(
    {'type': 'high_error_rate', 'severity': 'high'},
    'flash'
)

print(f"Fix: {proposal['fix_description']}")
print(f"Risk: {proposal['risk_assessment']['level']}")
print(f"Rollback: {proposal['rollback_plan']}")

# Approve if acceptable
if proposal['risk_assessment']['level'] == 'medium':
    engine.approve_proposal(proposal['proposal_id'], 'superman')
    result = engine.apply_fix(proposal['proposal_id'])
```

---

## Learning System

### Pattern Recognition

Oracle learns from agent behavior:

```python
from core.oracle_learning.cross_agent_learning import CrossAgentLearning

learning = CrossAgentLearning()

# Get learned patterns
patterns = learning.get_learned_patterns('batman')

for pattern in patterns:
    print(f"Pattern: {pattern['pattern_name']}")
    print(f"Confidence: {pattern['confidence']}")
    print(f"Recommendation: {pattern['recommendation']}")
```

### Knowledge Sharing

Patterns learned from one agent benefit others:

```python
# Batman learns a better selector strategy
learning.learn_pattern(
    'selector_optimization',
    {
        'agent': 'batman',
        'pattern': 'Use data-testid attributes for stability',
        'confidence': 0.95,
        'success_rate_improvement': 0.15
    }
)

# Flash automatically benefits from Batman's learning
recommendations = learning.get_recommendations('flash')
# Includes: "Consider using data-testid attributes (learned from batman)"
```

### Standards Enforcement

Oracle enforces coding standards across all agents:

```python
from core.oracle_learning.standards_enforcement import StandardsEnforcer

enforcer = StandardsEnforcer()

# Check agent code against standards
violations = enforcer.check_agent_code('batman')

for violation in violations:
    print(f"❌ {violation['type']}: {violation['description']}")
    print(f"   Fix: {violation['fix_suggestion']}")
```

---

## Dependency Management

### Adding Dependencies

```python
from core.oracle_version_control.dependency_tracker import DependencyTracker, DependencyType

tracker = DependencyTracker()

# Add dependency
tracker.add_dependency(
    'batman',
    'oracle',
    '>=1.0.0',
    DependencyType.REQUIRES
)

# Add optional dependency
tracker.add_dependency(
    'flash',
    'batman',
    '>=2.0.0',
    DependencyType.RECOMMENDS
)
```

### Circular Dependency Detection

```python
# Detect circular dependencies
circular = tracker.detect_circular_dependencies()

if circular:
    print("⚠️ Circular dependencies detected:")
    for cycle in circular:
        print(f"  {' → '.join(cycle)}")
```

### Update Impact Analysis

```python
# Before updating an agent, check impact
impact = tracker.analyze_update_impact('oracle', '2.0.0')

print(f"Direct dependents: {impact['direct_dependents']}")
print(f"Indirect dependents: {impact['indirect_dependents']}")
print(f"Total affected: {impact['total_affected']}")
print(f"Breaking risk: {impact['breaking_risk']}")
print(f"Update order: {impact['update_order']}")
```

---

## Best Practices

### 1. Regular Health Checks

Schedule regular health checks:

```python
import schedule

def daily_health_check():
    connector = get_superman_interface()
    health = connector.get_agent_health_summary()

    if health['health_percentage'] < 90:
        # Send alert
        print(f"⚠️ System health: {health['health_percentage']:.1f}%")

# Run daily at 9 AM
schedule.every().day.at("09:00").do(daily_health_check)
```

### 2. Version Updates

Follow this process for version updates:

1. **Analyze impact** before updating
2. **Test in staging** environment
3. **Update during low-traffic** periods
4. **Monitor closely** after update
5. **Keep rollback plan** ready

```python
# Safe update workflow
impact = connector.analyze_update_impact('batman', '2.0.0')

if impact['breaking_risk'] == 'high':
    print("⚠️ High breaking risk - schedule maintenance window")
elif impact['total_affected'] > 5:
    print("⚠️ Many agents affected - coordinate with team")
else:
    # Proceed with update
    version = connector.request_version_update('batman', 'major', 'Update')
```

### 3. Self-Healing Configuration

Enable auto-healing but review logs:

```python
coordinator = get_oracle_coordinator()

# Run auto-heal daily
results = coordinator.auto_heal_system()

# Review what was fixed
print(f"Issues found: {results['issues_found']}")
print(f"Fixes applied: {results['fixes_applied']}")

for action in results['healing_actions']:
    print(f"  {action['agent']}: {action['fix']}")
```

### 4. Monitoring Alerts

Set up alert monitoring:

```python
# Check for critical alerts
coordinator = get_oracle_coordinator()
alerts = coordinator.get_pending_alerts()

critical_alerts = [a for a in alerts if a['severity'] == 'critical']

if critical_alerts:
    print(f"🚨 {len(critical_alerts)} CRITICAL ALERTS")
    for alert in critical_alerts:
        print(f"  {alert['message']}")
        # Acknowledge after review
        coordinator.acknowledge_alert(alert['id'])
```

---

## Troubleshooting

### Common Issues

#### 1. Agent Showing as Unhealthy

**Problem**: Agent status is 'unhealthy' or 'critical'

**Solution**:
```python
# Get detailed health info
health = connector.get_agent_health_summary()
agent_health = health['agents']['batman']

print(f"Status: {agent_health['status']}")
print(f"Issues: {agent_health.get('issues_detected', [])}")

# Request healing
healing = connector.request_self_healing('batman')

# If auto-heal doesn't work, check logs
```

#### 2. Version Update Failed

**Problem**: Version update failed or caused issues

**Solution**:
```python
# Immediately rollback
rollback = connector.emergency_rollback('batman', 'Update failed')

print(f"Rolled back: {rollback['from_version']} → {rollback['to_version']}")

# Check what went wrong
from core.oracle_version_control.breaking_change_detector import BreakingChangeDetector

detector = BreakingChangeDetector()
# Analyze code changes...
```

#### 3. Circular Dependencies

**Problem**: Circular dependency detected

**Solution**:
```python
tracker = DependencyTracker()
circular = tracker.detect_circular_dependencies()

print("Circular chains detected:")
for cycle in circular:
    print(f"  {' → '.join(cycle)}")

# Refactor to remove circular dependencies
# Remove one dependency from the cycle
```

#### 4. Oracle Not Responding

**Problem**: Oracle connection issues

**Solution**:
```python
# Check Oracle status
status = connector.get_oracle_status()

print(f"Oracle online: {status['oracle_online']}")
print(f"Active capabilities: {status['active_capabilities']}/4")

for module, info in status['modules'].items():
    if not info['available']:
        print(f"❌ {module} not available")
```

### Getting Help

1. **Check Logs**: `/tmp/aldo-vision-justice-league/oracle/logs/`
2. **System Report**: `coordinator.generate_system_report()`
3. **Documentation**: This guide and API reference
4. **GitHub Issues**: Report bugs and request features

---

## Quick Reference

### Most Common Commands

```python
# Get Superman interface
from core.oracle_integration.superman_connector import get_superman_interface
connector = get_superman_interface()

# Health check
health = connector.get_agent_health_summary()

# Get versions
versions = connector.get_agent_versions()

# Update version
version = connector.request_version_update('agent', 'minor', 'description')

# Request healing
healing = connector.request_self_healing('agent')

# Analyze impact
impact = connector.analyze_update_impact('agent', '2.0.0')

# Emergency rollback
rollback = connector.emergency_rollback('agent', 'reason')

# Coordinate task
plan = connector.coordinate_multi_agent_task('task', ['agent1', 'agent2'], 'high')
```

---

**Oracle says**: "Knowledge is power. Use it wisely." 🔮
