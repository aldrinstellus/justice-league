# 🎓 Oracle Operator Training Manual

**Week 13-14: Documentation & Training**
**Target Audience**: Superman and Oracle System Operators
**Training Duration**: 4-6 hours
**Skill Level**: Intermediate to Advanced

---

## Table of Contents

1. [Introduction](#introduction)
2. [Oracle Overview](#oracle-overview)
3. [System Architecture](#system-architecture)
4. [Daily Operations](#daily-operations)
5. [Health Monitoring](#health-monitoring)
6. [Version Management](#version-management)
7. [Incident Response](#incident-response)
8. [Common Operations](#common-operations)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)
11. [Training Exercises](#training-exercises)
12. [Certification Quiz](#certification-quiz)

---

## Introduction

### Welcome to Oracle Operations

Welcome to the Oracle Operations training program. This manual will teach you how to operate, monitor, and maintain the Oracle meta-agent system that manages all 11 Justice League agents.

### What You'll Learn

By the end of this training, you will be able to:
- ✅ Monitor Oracle and all Justice League agents
- ✅ Perform routine health checks and maintenance
- ✅ Manage agent versions and updates
- ✅ Respond to incidents and alerts
- ✅ Troubleshoot common issues
- ✅ Execute emergency procedures
- ✅ Understand when to escalate issues

### Prerequisites

**Required Knowledge**:
- Basic command line usage (bash)
- Understanding of Python basics
- Familiarity with databases (SQLite)
- Basic Docker concepts
- Git fundamentals

**Optional Knowledge** (helpful):
- Prometheus and Grafana
- Load balancing concepts
- Blue-green deployment
- System monitoring

### Training Environment

You'll be working with:
- **Oracle Database**: SQLite database with agent data
- **Justice League Agents**: 11 production agents
- **Superman Connector**: Primary interface for operations
- **Monitoring Stack**: Prometheus + Grafana
- **Deployment Tools**: Docker, Docker Compose

---

## Oracle Overview

### What is Oracle?

Oracle is a meta-agent system that:
- **Monitors** the health of all 11 Justice League agents
- **Heals** agents automatically when issues are detected
- **Learns** from past incidents to prevent future problems
- **Manages** agent versions and dependencies
- **Coordinates** multi-agent tasks efficiently

### The Justice League (11 Agents)

| Agent | Specialty | Key Responsibilities |
|-------|-----------|---------------------|
| **Batman** | Structure Analysis | HTML structure, semantic analysis |
| **Superman** | Coordination | Multi-agent orchestration, leadership |
| **Wonder Woman** | Accessibility | WCAG compliance, a11y testing |
| **Flash** | Performance | Speed analysis, optimization |
| **Green Lantern** | Security | Vulnerability scanning, security analysis |
| **Aquaman** | Data Flow | API analysis, data structures |
| **Cyborg** | Integration | API testing, system integration |
| **Martian Manhunter** | Intelligence | Pattern recognition, analytics |
| **Hawkgirl** | Mobility | Responsive design, mobile testing |
| **Green Arrow** | Precision | Detail-oriented analysis, accuracy |
| **Black Canary** | Communication | User messaging, notifications |

### Oracle Capabilities

Oracle provides 5 core capabilities:

1. **Health Monitoring**
   - Real-time agent health tracking
   - Performance metrics collection
   - Automatic issue detection
   - Custom health checks

2. **Self-Healing**
   - Automatic problem detection
   - Fix proposal generation
   - Low-risk automatic fixes
   - Manual approval for high-risk fixes

3. **Learning System**
   - Cross-agent pattern recognition
   - Knowledge base building
   - Standards enforcement
   - Predictive maintenance

4. **Version Control**
   - Semantic versioning (MAJOR.MINOR.PATCH)
   - Dependency tracking
   - Breaking change detection
   - Automated rollback

5. **Multi-Agent Coordination**
   - Dependency-aware task ordering
   - Parallel execution where possible
   - Backup agent selection
   - Result aggregation

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Superman                             │
│              (Primary Operator Interface)                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                Superman Connector                        │
│          (API for Superman to access Oracle)            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Oracle Coordinator                          │
│    (Proactive monitoring and coordination)              │
└──┬──────────┬──────────┬──────────┬──────────┬─────────┘
   │          │          │          │          │
   ▼          ▼          ▼          ▼          ▼
┌──────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Health│ │Version │ │  Self  │ │Learning│ │ Depend │
│ Mon  │ │Control │ │ Healing│ │ System │ │  Track │
└──────┘ └────────┘ └────────┘ └────────┘ └────────┘
   │          │          │          │          │
   └──────────┴──────────┴──────────┴──────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 Oracle Database                          │
│         (SQLite - Agent data, versions, metrics)        │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              11 Justice League Agents                    │
│  Batman | Superman | Wonder Woman | Flash | ... (11)    │
└─────────────────────────────────────────────────────────┘
```

### Deployment Architecture (Blue-Green)

```
┌──────────────────────────────────────────┐
│         Nginx Load Balancer              │
│      (SSL/TLS Termination)              │
└────┬─────────────────────────────┬───────┘
     │                             │
     ▼                             ▼
┌────────────┐               ┌────────────┐
│ Oracle     │               │ Oracle     │
│  BLUE      │               │  GREEN     │
│ (Active)   │               │ (Standby)  │
└────────────┘               └────────────┘
     │                             │
     └──────────┬──────────────────┘
                ▼
┌─────────────────────────────────────────┐
│      Monitoring Stack                   │
│  Prometheus | Grafana | AlertManager    │
└─────────────────────────────────────────┘
```

### Data Flow

**Typical Operation**:
1. Superman requests agent health via `SupermanConnector`
2. Superman Connector calls `AgentHealthMonitor`
3. Health Monitor queries Oracle Database
4. Results aggregated and returned to Superman
5. Superman acts on the information

**Health Check Flow**:
1. Oracle Coordinator performs system scan (scheduled)
2. Each agent's health is checked
3. Issues detected and categorized
4. Low-risk issues auto-healed
5. High-risk issues create alerts
6. Superman notified of critical issues

---

## Daily Operations

### Morning Checklist (15 minutes)

**Every weekday morning, perform these checks**:

#### 1. System Health Check
```bash
# Check overall Oracle status
python3 deployment/health_check.py

# Expected: All checks passing (✓)
# If degraded (⚠), investigate warnings
# If unhealthy (✗), escalate immediately
```

#### 2. Agent Health Summary
```python
from core.oracle_integration.superman_connector import get_superman_interface

connector = get_superman_interface()
health = connector.get_agent_health_summary()

print(f"System Health: {health['health_percentage']:.1f}%")
print(f"Healthy: {health['healthy_count']}")
print(f"Warning: {health['warning_count']}")
print(f"Unhealthy: {health['unhealthy_count']}")
print(f"Critical: {health['critical_count']}")

# Expected: Health percentage > 90%
# Action: If < 90%, investigate unhealthy agents
```

#### 3. Check Pending Alerts
```python
from core.oracle_integration.oracle_coordinator import OracleCoordinator

coordinator = OracleCoordinator()
alerts = coordinator.get_pending_alerts()

if alerts:
    for alert in alerts['alerts']:
        print(f"⚠ {alert['severity']}: {alert['message']}")
        # Action: Review and acknowledge each alert
        # coordinator.acknowledge_alert(alert['alert_id'])
else:
    print("✓ No pending alerts")
```

#### 4. Review Overnight Activity
```bash
# Check logs from last 24 hours
tail -n 100 logs/oracle.log

# Look for:
# - ERROR level messages
# - Self-healing attempts
# - Failed operations
# - Unusual patterns
```

#### 5. Verify Backups
```bash
# Check latest backup
ls -lht deployment/backups/production/ | head -5

# Expected: Backup from last 12 hours
# Action: If no recent backup, investigate backup system
```

**Morning Checklist Summary**:
```
□ System health check (deployment/health_check.py)
□ Agent health summary (>90% healthy)
□ Pending alerts review
□ Log review (errors and warnings)
□ Backup verification (< 12 hours old)
```

### Weekly Maintenance (1 hour)

**Every Monday morning**:

#### 1. Full System Scan
```python
coordinator = OracleCoordinator()
scan = coordinator.perform_system_scan()

print(f"Scanned {scan['scan_results']['agents_scanned']} agents")
print(f"Issues: {scan['scan_results']['issues_found']}")
print(f"Recommendations: {len(scan['recommendations'])}")

# Review each recommendation
for rec in scan['recommendations']:
    print(f"- {rec}")
```

#### 2. Version Audit
```python
connector = get_superman_interface()
versions = connector.get_agent_versions()

print("\nAgent Versions:")
for agent, info in versions['versions'].items():
    print(f"{agent}: v{info['version']} (deployed {info['deployed_at']})")

# Check for outdated versions (> 90 days)
# Plan updates for agents on old versions
```

#### 3. Performance Review
```python
# Check performance metrics for each agent
health = connector.get_agent_health_summary()

for agent_name, agent_health in health['agents'].items():
    metrics = agent_health['metrics']
    print(f"\n{agent_name}:")
    print(f"  Success Rate: {metrics['success_rate']:.1f}%")
    print(f"  Avg Response: {metrics['avg_response_time']:.0f}ms")
    print(f"  P95 Response: {metrics['p95_response_time']:.0f}ms")

    # Flag if p95 > target
    if metrics['p95_response_time'] > 2000:  # 2 second target
        print(f"  ⚠ Performance degraded")
```

#### 4. Disk Space Cleanup
```bash
# Clean up old logs (keep last 30 days)
find logs/ -name "*.log" -mtime +30 -delete

# Clean up old backups (keep last 30)
cd deployment/backups/production
ls -t oracle_backup_*.db | tail -n +31 | xargs rm -f
```

#### 5. Dependency Audit
```python
# Check for circular dependencies
connector = get_superman_interface()
graph = connector.get_dependency_graph()

if graph['has_circular_dependencies']:
    print("⚠ CIRCULAR DEPENDENCIES DETECTED")
    print(f"Chains: {graph['circular_chains']}")
    # Action: Create ticket to refactor dependencies
else:
    print("✓ No circular dependencies")
```

**Weekly Maintenance Summary**:
```
□ Full system scan
□ Version audit (check for outdated versions)
□ Performance review (all agents)
□ Disk space cleanup (logs and backups)
□ Dependency audit (circular check)
```

### Monthly Tasks (2 hours)

**First Monday of every month**:

#### 1. Security Audit
```bash
# Run security scanner on dependencies
pip freeze | safety check

# Review audit logs
grep "SECURITY" logs/audit.log | tail -100

# Check for failed authentication attempts
grep "AUTH_FAILED" logs/audit.log
```

#### 2. Capacity Planning
```python
# Review growth trends
# - Database size
# - Agent count
# - Request volume
# - Error rates

import os
db_size = os.path.getsize('oracle.db') / (1024**2)  # MB
print(f"Database size: {db_size:.1f} MB")

# If > 500MB, consider optimization or migration to PostgreSQL
```

#### 3. Disaster Recovery Test
```bash
# Test backup restore (on staging)
cd deployment
./deploy.sh staging --rollback --force

# Verify staging works after restore
python3 deployment/health_check.py
```

#### 4. Documentation Review
```bash
# Update runbooks with any new procedures
# Review and update troubleshooting guides
# Document any new patterns or issues discovered
```

**Monthly Tasks Summary**:
```
□ Security audit (dependencies and logs)
□ Capacity planning (database size, trends)
□ Disaster recovery test (backup restore)
□ Documentation review and updates
```

---

## Health Monitoring

### Understanding Health Status

Oracle assigns one of 4 health statuses to each agent:

| Status | Color | Percentage | Description | Action |
|--------|-------|------------|-------------|--------|
| **Healthy** | Green | 90-100% | Normal operation | Monitor |
| **Warning** | Yellow | 70-89% | Minor issues | Investigate |
| **Unhealthy** | Orange | 40-69% | Significant problems | Urgent fix |
| **Critical** | Red | 0-39% | Severe failure | Emergency response |

### Health Metrics Explained

**Success Rate**:
- Percentage of successful operations
- Target: >95%
- Warning: <90%
- Critical: <80%

**Response Time**:
- Time to complete operations
- Measured: Average, P95, P99
- Targets vary by agent (see table below)

**Error Rate**:
- Rate of errors per minute
- Target: <0.1 errors/minute
- Warning: >0.5 errors/minute
- Critical: >1.0 errors/minute

### Performance Targets by Agent

| Agent | Target P95 | Maximum P99 | Criticality |
|-------|------------|-------------|-------------|
| Flash | 1s | 3s | High |
| Batman | 2s | 5s | High |
| Wonder Woman | 3s | 7s | Medium |
| Cyborg | 3s | 7s | Medium |
| Others | 3s | 7s | Medium |

### How to Check Agent Health

**Method 1: Via Python**
```python
from core.oracle_integration.superman_connector import get_superman_interface

connector = get_superman_interface()
health = connector.get_agent_health_summary()

# View specific agent
batman_health = health['agents']['batman']
print(f"Status: {batman_health['status']}")
print(f"Success Rate: {batman_health['metrics']['success_rate']:.1f}%")
print(f"Avg Response: {batman_health['metrics']['avg_response_time']:.0f}ms")

# Check for issues
if batman_health['metrics']['issues_detected']:
    for issue in batman_health['metrics']['issues_detected']:
        print(f"Issue: {issue}")
```

**Method 2: Via Grafana Dashboard**
```bash
# Open Grafana
open http://localhost:3000

# Navigate to: Dashboards > Oracle System Overview
# View:
# - Agent Health Percentage (gauge)
# - Error Rate (graph)
# - Operation Duration (graph)
```

**Method 3: Via Health Check Script**
```bash
python3 deployment/health_check.py

# Output shows:
# ✓ Agent Health System: Health monitoring system operational
```

### Interpreting Health Issues

**Common Issues and Meanings**:

**Issue**: "High error rate detected"
- **Meaning**: Agent is failing > 10% of operations
- **Action**: Check logs for error patterns
- **Priority**: High

**Issue**: "Response time degraded"
- **Meaning**: Agent taking too long to respond
- **Action**: Check system resources, optimize code
- **Priority**: Medium

**Issue**: "Last operation failed"
- **Meaning**: Most recent operation failed
- **Action**: Check logs for specific error
- **Priority**: Medium if isolated, High if pattern

**Issue**: "Agent not responding"
- **Meaning**: Agent failed to respond to health check
- **Action**: Restart agent, check logs
- **Priority**: Critical

### Responding to Health Alerts

**Alert Level: WARNING (Yellow)**
```python
# 1. Investigate the issue
connector = get_superman_interface()
health = connector.get_agent_health_summary()
agent_health = health['agents']['agent_name']

# 2. Request self-healing
healing = connector.request_self_healing('agent_name')

# 3. Monitor for 15 minutes
# 4. If not resolved, escalate
```

**Alert Level: UNHEALTHY (Orange)**
```python
# 1. Immediate investigation required
# 2. Check logs
# 3. Request self-healing
# 4. If not resolved in 5 minutes, manual intervention
# 5. Consider rollback if recent deploy
```

**Alert Level: CRITICAL (Red)**
```python
# 1. IMMEDIATE ACTION REQUIRED
# 2. Page on-call engineer
# 3. Check if agent is down
# 4. Attempt restart
# 5. If recent deploy, rollback immediately
# 6. Create incident ticket
```

---

## Version Management

### Understanding Semantic Versioning

Oracle uses semantic versioning (SemVer):

**Format**: MAJOR.MINOR.PATCH

**Examples**:
- `1.0.0` → `1.0.1` = Patch (bug fix)
- `1.0.1` → `1.1.0` = Minor (new feature)
- `1.1.0` → `2.0.0` = Major (breaking change)

**Version Changes**:

| Change Type | When to Use | Example |
|-------------|-------------|---------|
| **PATCH** | Bug fixes, minor changes | 1.0.0 → 1.0.1 |
| **MINOR** | New features, backward compatible | 1.0.1 → 1.1.0 |
| **MAJOR** | Breaking changes | 1.1.0 → 2.0.0 |

### How to Update an Agent Version

**Patch Update (Bug Fix)**:
```python
connector = get_superman_interface()

# Create patch version
result = connector.request_version_update(
    agent_name='batman',
    change_type='patch',
    changes='Fixed minor bug in HTML parsing',
    breaking_changes=None
)

print(f"Updated to: v{result['new_version']}")  # 1.0.0 → 1.0.1
```

**Minor Update (New Feature)**:
```python
result = connector.request_version_update(
    agent_name='batman',
    change_type='minor',
    changes='Added support for HTML5 semantic elements',
    breaking_changes=None
)

print(f"Updated to: v{result['new_version']}")  # 1.0.1 → 1.1.0
```

**Major Update (Breaking Change)**:
```python
result = connector.request_version_update(
    agent_name='batman',
    change_type='major',
    changes='Completely redesigned HTML analysis engine',
    breaking_changes=[
        'Changed API response format',
        'Removed deprecated analyze_old() method',
        'Updated required Python version to 3.11+'
    ]
)

print(f"Updated to: v{result['new_version']}")  # 1.1.0 → 2.0.0

# WARNING: Breaking changes require coordination with dependent agents!
```

### Analyzing Update Impact

**Before updating, check impact**:
```python
# See which agents will be affected
impact = connector.analyze_update_impact(
    agent_name='batman',
    new_version='2.0.0'
)

print(f"Directly affected: {impact['directly_affected']}")
print(f"Indirectly affected: {impact['indirectly_affected']}")
print(f"Total affected: {impact['total_affected']}")
print(f"Update order: {impact['update_order']}")

# Review before proceeding!
```

### Coordinated Updates (Dependencies)

**Example: Updating Oracle affects multiple agents**:
```python
# Scenario: Oracle 1.0.0 → 2.0.0
# Batman depends on Oracle
# Flash depends on Batman

impact = connector.analyze_update_impact('oracle', '2.0.0')

# Oracle sees:
# - Directly affected: ['batman', 'wonder_woman']
# - Indirectly affected: ['flash']
# - Update order: ['oracle', 'batman', 'wonder_woman', 'flash']

# Generate update plan
coordinator = OracleCoordinator()
plan = coordinator.coordinate_version_update('oracle', '2.0.0')

print(f"Phases: {plan['total_phases']}")
for phase in plan['update_plan']:
    print(f"Phase {phase['phase']}: {phase['agents']}")

# Execute updates in order
```

### Rolling Back Versions

**When to Rollback**:
- New version causing errors
- Performance degradation
- Breaking changes affecting production
- Failed deployment

**How to Rollback**:
```bash
# Option 1: Via deployment script
./deployment/deploy.sh production --rollback

# Option 2: Via Python (specific agent)
from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl

version_control = EnhancedVersionControl()
result = version_control.rollback_version(
    agent_name='batman',
    target_version='1.0.0'
)

print(f"Rolled back: {result['from_version']} → {result['to_version']}")
print(f"Safety level: {result['safety_level']}")
```

### Version Control Best Practices

**DO**:
- ✅ Always analyze impact before updating
- ✅ Test in staging before production
- ✅ Document all breaking changes
- ✅ Update dependent agents in correct order
- ✅ Keep backup before major version updates
- ✅ Communicate breaking changes to team

**DON'T**:
- ❌ Skip impact analysis
- ❌ Update production without testing
- ❌ Deploy breaking changes without notice
- ❌ Update dependencies out of order
- ❌ Forget to backup database
- ❌ Rush major version updates

---

## Incident Response

### Incident Severity Levels

| Severity | Response Time | Description | Example |
|----------|--------------|-------------|---------|
| **P0** | Immediate | Complete system outage | All agents down |
| **P1** | 15 minutes | Critical functionality broken | Superman can't coordinate |
| **P2** | 1 hour | Significant degradation | 50% of agents unhealthy |
| **P3** | 4 hours | Minor impact | Single agent warning |
| **P4** | 24 hours | Cosmetic or very low impact | Log formatting issue |

### P0 - Critical Incident Response

**Symptoms**:
- Oracle completely down
- All agents failing
- Database corrupted
- Deployment rollback failed

**Immediate Actions (First 5 Minutes)**:
```bash
# 1. Acknowledge incident
echo "P0 INCIDENT - $(date)" >> incidents/current.txt

# 2. Check if Oracle is running
docker-compose ps

# 3. Check health
python3 deployment/health_check.py

# 4. Check recent deployments
git log --oneline -5

# 5. Page on-call engineer
echo "Page sent to on-call" >> incidents/current.txt
```

**Mitigation Steps**:
```bash
# If recent deployment caused it:
./deployment/deploy.sh production --rollback --force

# If database corruption:
# 1. Stop Oracle
docker-compose stop oracle-blue oracle-green

# 2. Restore latest backup
cp deployment/backups/production/oracle_backup_latest.db oracle.db

# 3. Restart Oracle
docker-compose up -d oracle-blue

# 4. Verify health
python3 deployment/health_check.py
```

**Communication Template (P0)**:
```
SUBJECT: [P0] Oracle System Outage

STATUS: Investigating / Identified / Mitigating / Resolved

IMPACT:
- All Justice League agents down
- No website analysis possible
- Estimated affected users: [number]

TIMELINE:
- 14:30 UTC: Incident detected
- 14:32 UTC: On-call paged
- 14:35 UTC: Root cause identified (recent deployment)
- 14:40 UTC: Rollback initiated
- 14:45 UTC: System restored

ROOT CAUSE:
[Detailed explanation]

NEXT STEPS:
1. [Action item]
2. [Action item]
3. Post-incident review scheduled for [date/time]
```

### P1 - High Priority Incident

**Symptoms**:
- Critical agent down (Batman, Superman, Flash)
- Database connection issues
- Self-healing system failing

**Response Procedure**:
```python
# 1. Identify the issue
connector = get_superman_interface()
health = connector.get_agent_health_summary()

# Find critical agents
critical_agents = [
    agent for agent, status in health['agents'].items()
    if status['status'] == 'critical'
]

print(f"Critical agents: {critical_agents}")

# 2. Attempt self-healing
for agent in critical_agents:
    healing = connector.request_self_healing(agent)
    print(f"{agent}: {healing['fixes_applied']} fixes applied")

# 3. If not resolved, escalate
# 4. Create incident ticket
# 5. Update status page
```

### P2 - Medium Priority Incident

**Symptoms**:
- Multiple agents in warning state
- Performance degradation
- Elevated error rates

**Response Procedure**:
```python
# 1. Document the issue
# 2. Investigate root cause
coordinator = OracleCoordinator()
scan = coordinator.perform_system_scan()

# 3. Review recommendations
for rec in scan['recommendations']:
    print(f"Recommendation: {rec}")

# 4. Implement fixes within 1 hour
# 5. Monitor for improvement
```

### Incident Escalation Path

```
Operator (You)
      ↓
   Superman
      ↓
Senior Engineer
      ↓
  Engineering Manager
      ↓
      CTO
```

**When to Escalate**:
- P0: Immediate escalation to Superman
- P1: Escalate if not resolved in 15 minutes
- P2: Escalate if not resolved in 1 hour
- P3: Escalate if not resolved in 4 hours

---

## Common Operations

### Operation 1: Adding a New Agent

**Procedure**:
```python
# 1. Register agent with Oracle
from core.oracle_integration.superman_connector import get_superman_interface

connector = get_superman_interface()

# Agent self-registers on first health check
# Or manually register:
# (Normally done automatically by agent code)

# 2. Verify registration
health = connector.get_agent_health_summary()
assert 'new_agent_name' in health['agents']

# 3. Set initial version
from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl

version_control = EnhancedVersionControl()
version_control.create_version(
    agent_name='new_agent_name',
    change_type='initial',
    changes='Initial version',
    breaking_changes=None
)

# 4. Add dependencies (if any)
# (Done via DependencyTracker)

# 5. Monitor first 24 hours
```

### Operation 2: Removing/Decommissioning an Agent

**Procedure**:
```python
# 1. Check dependencies
connector = get_superman_interface()
graph = connector.get_dependency_graph()

# Ensure no other agents depend on this one
# If they do, update them first

# 2. Mark as deprecated
version_control = EnhancedVersionControl()
version_control.create_version(
    agent_name='old_agent',
    change_type='major',
    changes='Agent deprecated - DO NOT USE',
    breaking_changes=['Agent will be removed']
)

# 3. Remove from active roster
# (Update AGENTS environment variable in config)

# 4. Archive data (don't delete from database)
# Keep for historical analysis

# 5. Update documentation
```

### Operation 3: Coordinating Multi-Agent Task

**Procedure**:
```python
connector = get_superman_interface()

# Coordinate task with multiple agents
task_result = connector.coordinate_multi_agent_task(
    task_description="Analyze e-commerce website for enterprise client",
    required_agents=['batman', 'flash', 'wonder_woman', 'cyborg'],
    priority='high'
)

print(f"Task ID: {task_result['task_id']}")
print(f"Execution order: {task_result['execution_order']}")
print(f"Estimated time: {task_result['estimated_time']}s")

# Monitor task progress
# (Agents execute in dependency order)
```

### Operation 4: Emergency System Restart

**When**: After configuration changes, or troubleshooting

**Procedure**:
```bash
# 1. Announce maintenance window
echo "Maintenance window: $(date)" | mail -s "Oracle Maintenance" team@example.com

# 2. Stop all services
docker-compose down

# 3. Verify all stopped
docker-compose ps
# (Should show no running containers)

# 4. Start services
docker-compose up -d

# 5. Wait for services to be ready
sleep 30

# 6. Verify health
python3 deployment/health_check.py

# 7. Check agents
from core.oracle_integration.superman_connector import get_superman_interface
connector = get_superman_interface()
health = connector.get_agent_health_summary()
print(f"Health: {health['health_percentage']:.1f}%")

# Expected: >90% within 5 minutes

# 8. Announce completion
echo "Maintenance complete: $(date)" | mail -s "Oracle Back Online" team@example.com
```

---

## Troubleshooting

### Issue: "Agent showing as unhealthy but should be working"

**Symptoms**:
- Agent status: unhealthy or critical
- No obvious errors in logs
- Agent seems to function normally

**Diagnosis**:
```python
# 1. Check specific agent health
connector = get_superman_interface()
health = connector.get_agent_health_summary()
agent_health = health['agents']['agent_name']

# 2. Check metrics
print(f"Success Rate: {agent_health['metrics']['success_rate']}")
print(f"Error Count: {agent_health['metrics']['error_count']}")
print(f"Last Error: {agent_health['metrics']['last_error']}")

# 3. Check if false positive
# Sometimes health check too strict
```

**Solutions**:
```python
# Solution 1: Request self-healing
healing = connector.request_self_healing('agent_name')

# Solution 2: Reset health metrics
# (If metrics are stale or incorrect)
from core.oracle_self_healing.health_monitor import AgentHealthMonitor
monitor = AgentHealthMonitor()
# Reset metrics for agent (clear error count)

# Solution 3: Manual health check
# Run agent's analyze function manually to verify it works
```

---

### Issue: "High memory usage warning"

**Symptoms**:
- Health check shows memory warning
- System slowing down
- Disk space low

**Diagnosis**:
```bash
# 1. Check actual memory usage
free -h

# 2. Check which containers using most memory
docker stats

# 3. Check disk space
df -h

# 4. Check database size
du -sh oracle.db
```

**Solutions**:
```bash
# Solution 1: Clean up logs
find logs/ -name "*.log" -mtime +7 -delete

# Solution 2: Clean up old backups
cd deployment/backups/production
ls -t oracle_backup_*.db | tail -n +15 | xargs rm

# Solution 3: Optimize database
sqlite3 oracle.db "VACUUM;"

# Solution 4: Restart containers (if memory leak suspected)
docker-compose restart oracle-blue oracle-green
```

---

### Issue: "Version control failed - 'safety_level' error"

**Symptoms**:
- Version update or rollback fails
- Error mentions 'safety_level'

**Diagnosis**:
```python
# Check if backup exists for rollback
import os
backup_path = f"backups/{agent_name}_backup.py"
if not os.path.exists(backup_path):
    print("Backup missing!")
```

**Solutions**:
```python
# Solution 1: Create backup first
version_control = EnhancedVersionControl()
# Backup created automatically on next version update

# Solution 2: Use force flag for rollback
result = version_control.rollback_version(
    agent_name='agent_name',
    target_version='1.0.0',
    force=True  # Skip safety checks
)

# CAUTION: Only use force in emergencies!
```

---

### Issue: "Circular dependency detected"

**Symptoms**:
- Dependency graph shows circular dependencies
- Update coordination fails

**Diagnosis**:
```python
connector = get_superman_interface()
graph = connector.get_dependency_graph()

if graph['has_circular_dependencies']:
    print("Circular chains:")
    for chain in graph['circular_chains']:
        print(f"  {' → '.join(chain)}")
```

**Solutions**:
```python
# Solution: Break the circle by removing one dependency

from core.oracle_version_control.dependency_tracker import DependencyTracker

tracker = DependencyTracker()

# Example: If A → B → C → A
# Remove dependency: C → A
tracker.remove_dependency('C', 'A')

# Verify circle broken
graph = connector.get_dependency_graph()
assert not graph['has_circular_dependencies']
```

---

## Best Practices

### Monitoring Best Practices

1. **Check health daily** - Run morning checklist every weekday
2. **Monitor Grafana** - Keep dashboard open during work hours
3. **Set up alerts** - Configure email/Slack for critical issues
4. **Review trends weekly** - Look for degradation patterns
5. **Document incidents** - Keep runbook updated with solutions

### Version Management Best Practices

1. **Test before deploy** - Always test in staging first
2. **Analyze impact** - Check dependencies before major updates
3. **Communicate breaking changes** - Notify team 24 hours ahead
4. **Keep backups** - Verify backup before version update
5. **Document changes** - Update CHANGELOG.md

### Operational Best Practices

1. **Automate routine tasks** - Use scripts for repetitive operations
2. **Document everything** - Update runbooks with new procedures
3. **Practice DR** - Test disaster recovery monthly
4. **Monitor resource usage** - Track trends for capacity planning
5. **Stay informed** - Review Oracle release notes

### Security Best Practices

1. **Audit logs regularly** - Review security events weekly
2. **Update dependencies** - Run security scan monthly
3. **Rotate credentials** - Change passwords quarterly
4. **Limit access** - Principle of least privilege
5. **Encrypt backups** - Production backups should be encrypted

---

## Training Exercises

### Exercise 1: Morning Health Check

**Objective**: Perform a complete morning health check

**Steps**:
1. Run system health check
2. Get agent health summary
3. Check pending alerts
4. Review logs from last 24 hours
5. Verify backup exists

**Success Criteria**:
- All checks complete without errors
- You can interpret health percentages
- You identify any issues

### Exercise 2: Self-Healing Request

**Objective**: Request and monitor self-healing

**Steps**:
1. Find an agent in warning state
2. Request self-healing for that agent
3. Monitor healing progress
4. Verify agent returns to healthy state

**Success Criteria**:
- Self-healing request successful
- Agent status improves
- You understand what fixes were applied

### Exercise 3: Version Update

**Objective**: Update an agent to new patch version

**Steps**:
1. Check current version of Flash
2. Analyze update impact
3. Create patch version (simulated fix)
4. Verify new version deployed
5. Monitor agent for 5 minutes post-update

**Success Criteria**:
- Version successfully updated
- No errors during update
- Agent remains healthy after update

### Exercise 4: Rollback Procedure

**Objective**: Practice rolling back to previous version

**Steps**:
1. Choose an agent with version history
2. Roll back to previous version
3. Verify rollback successful
4. Check agent still functions

**Success Criteria**:
- Rollback completes without errors
- Agent returns to previous version
- No dependency issues

### Exercise 5: Incident Response Simulation

**Objective**: Respond to simulated P1 incident

**Scenario**: "Batman agent shows as critical with 20% success rate"

**Steps**:
1. Acknowledge incident
2. Check Batman health and metrics
3. Review logs for errors
4. Request self-healing
5. If not resolved, consider rollback
6. Document incident

**Success Criteria**:
- Follow incident response procedure
- Document timeline
- Resolve issue or escalate appropriately

---

## Certification Quiz

### Section 1: Oracle Basics (Multiple Choice)

**Q1: What are the 5 core Oracle capabilities?**
- A) Monitoring, Healing, Learning, Testing, Deploying
- B) Health Monitoring, Self-Healing, Learning, Version Control, Coordination
- C) Analysis, Optimization, Security, Performance, Testing
- D) Batman, Superman, Flash, Oracle, Database

**Q2: Which agents are considered HIGH criticality?**
- A) All 11 agents
- B) Only Superman
- C) Batman, Flash, Superman
- D) Batman and Flash

**Q3: What is the health percentage threshold for "unhealthy" status?**
- A) < 90%
- B) < 70%
- C) 40-69%
- D) < 40%

### Section 2: Version Control (True/False)

**Q4: A PATCH version update (e.g., 1.0.0 → 1.0.1) is used for breaking changes.**
- True / False

**Q5: Before updating an agent, you should always analyze the update impact.**
- True / False

**Q6: Circular dependencies are acceptable in production.**
- True / False

### Section 3: Incident Response (Short Answer)

**Q7: What is the response time for a P0 incident?**
- Answer: __________

**Q8: Name 3 symptoms of a P1 incident.**
- 1. __________
- 2. __________
- 3. __________

**Q9: In what order should you escalate incidents?**
- Answer: __________

### Section 4: Practical Operations (Scenario)

**Q10: You arrive Monday morning and run the health check. It shows:**
```
Health Check Results:
✓  Database: OK
✓  Imports: OK
✓  Superman Connector: OK
✓  Oracle Coordinator: OK
⚠  Agent Health System: Health monitoring degraded
✓  Version Control: OK
✗  Disk Space: Only 5% available
✓  Memory: OK
```

**What are your next 3 actions?**
- 1. __________
- 2. __________
- 3. __________

---

## Answer Key

### Quiz Answers

**Q1**: B - Health Monitoring, Self-Healing, Learning, Version Control, Coordination

**Q2**: D - Batman and Flash (both have 2s and 1s p95 targets)

**Q3**: C - 40-69% is unhealthy range

**Q4**: False - PATCH is for bug fixes, MAJOR is for breaking changes

**Q5**: True - Always analyze impact before updating

**Q6**: False - Circular dependencies should be avoided/removed

**Q7**: Immediate

**Q8**: Any 3 of:
- Critical agent down (Batman, Superman, Flash)
- Database connection issues
- Self-healing system failing
- High error rates
- Multiple agents critical

**Q9**: Operator → Superman → Senior Engineer → Engineering Manager → CTO

**Q10**: Possible answers (vary):
1. Immediate: Clean up disk space (delete old logs/backups)
2. Investigate agent health degradation (check logs)
3. Run disk cleanup script, verify health improves
4. Document incident if disk space caused health degradation
5. Check why backups accumulated (backup rotation issue?)

**Passing Score**: 8/10 correct

---

## Congratulations!

You've completed the Oracle Operator Training Manual. You should now be able to:

✅ Monitor Oracle and Justice League agents
✅ Perform daily, weekly, and monthly operations
✅ Manage agent versions and updates
✅ Respond to incidents at all severity levels
✅ Troubleshoot common issues
✅ Follow operational best practices

### Next Steps

1. **Shadow Superman** - Observe operations for 1 week
2. **Practice in Staging** - Perform all exercises in staging environment
3. **Take Quiz** - Complete certification quiz
4. **On-Call Readiness** - Review incident response procedures
5. **Join Team Meetings** - Attend weekly operational reviews

### Resources

- **Oracle User Guide**: `docs/ORACLE_USER_GUIDE.md`
- **API Reference**: `docs/ORACLE_API_REFERENCE.md`
- **Best Practices**: `docs/ORACLE_BEST_PRACTICES.md`
- **Runbooks**: `docs/OPERATIONAL_RUNBOOKS.md` (Week 13-14)
- **Troubleshooting Guide**: `docs/TROUBLESHOOTING_GUIDE.md` (Week 13-14)

---

**Oracle says**: "Knowledge is power. Operators are the guardians of the system." 🎓
