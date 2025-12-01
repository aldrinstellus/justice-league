# ⚡ Oracle Operator Quick Start Guide

**Version**: 1.0.0
**Time to Complete**: 30-60 minutes
**Purpose**: Get operators productive with Oracle quickly

---

## Welcome! 👋

Welcome to Oracle! This quick start guide will get you up and running as an Oracle operator in under an hour. For comprehensive training, see the full Operator Training Manual after completing this guide.

---

## What is Oracle?

Oracle is a meta-agent system that **monitors and maintains 11 AI agents** called the Justice League:

1. Superman (Coordinator)
2. Batman (Security)
3. Wonder Woman (Communication)
4. Flash (Speed)
5. Aquaman (Research)
6. Green Lantern (Creativity)
7. Martian Manhunter (Integration)
8. Hawkgirl (Precision)
9. Green Arrow (Targeting)
10. Black Canary (Communication)
11. Cyborg (Monitoring)

Your job: **Keep all 11 agents healthy and operational.**

---

## Quick Start Checklist

### ☑️ Before You Begin

- [ ] Access to production server (SSH)
- [ ] Access to monitoring dashboards
- [ ] Access to #oracle-alerts Slack channel
- [ ] This quick start guide
- [ ] 30-60 minutes of focused time

---

## Part 1: The Essentials (15 minutes)

### 1. Access the System

```bash
# SSH to production server
ssh production-server

# Navigate to Oracle directory
cd /opt/oracle

# Verify you're in the right place
ls -la
# You should see: deployment/, core/, docs/, etc.
```

---

### 2. Your Daily Commands

**Learn these 5 commands first**:

```bash
# 1. Check overall health
python3 deployment/health_check.py
# Returns: 0 (healthy), 1 (unhealthy), 2 (degraded)

# 2. Check all agent health
python3 -c "
from core.oracle_integration.superman_connector import get_superman_interface
summary = get_superman_interface().get_agent_health_summary()
print(f'System Health: {summary[\"overall_health\"]:.1f}%')
print(f'Healthy Agents: {summary[\"healthy_count\"]}/{summary[\"total_agents\"]}')
"

# 3. View service logs
docker-compose -f deployment/docker-compose.yml logs -f oracle-blue --tail=50

# 4. Check service status
docker-compose -f deployment/docker-compose.yml ps

# 5. Restart a service (if needed)
docker-compose -f deployment/docker-compose.yml restart oracle-blue
```

---

### 3. Understanding Health Status

Oracle uses **4 health levels**:

| Status | Health % | What It Means | What You Do |
|--------|----------|---------------|-------------|
| **Healthy** | 90-100% | Everything great | Normal monitoring |
| **Warning** | 70-89% | Needs attention | Investigate cause |
| **Unhealthy** | 50-69% | Problem exists | Take action |
| **Critical** | 0-49% | Serious issue | Escalate immediately |

**Target**: System health > 90%

---

### 4. Monitoring Dashboards

Open these in your browser:

```bash
# Grafana (Main dashboard)
http://localhost:3000
Username: admin
Password: admin

# Prometheus (Metrics)
http://localhost:9090

# Alertmanager (Alerts)
http://localhost:9093
```

**Bookmark these URLs!**

---

## Part 2: Morning Routine (10 minutes)

### Your Morning Health Check

Every morning, run through this 5-minute checklist:

```bash
#!/bin/bash
echo "=== Oracle Morning Health Check ==="
echo "Date: $(date)"
echo ""

# 1. Overall health
echo "[1/5] Checking overall system health..."
python3 deployment/health_check.py
echo ""

# 2. Agent health
echo "[2/5] Checking all agents..."
python3 -c "
from core.oracle_integration.superman_connector import get_superman_interface
summary = get_superman_interface().get_agent_health_summary()
print(f'System Health: {summary[\"overall_health\"]:.1f}%')
for agent, health in summary['agents'].items():
    emoji = '✅' if health['status'] == 'healthy' else '⚠️'
    print(f'{emoji} {agent}: {health[\"status\"]}')
"
echo ""

# 3. Check for alerts
echo "[3/5] Checking for active alerts..."
curl -s http://localhost:9093/api/v1/alerts | jq '[.data[] | select(.status.state=="active")] | length'
echo " active alerts"
echo ""

# 4. Check disk space
echo "[4/5] Checking disk space..."
df -h / | grep -v Filesystem
echo ""

# 5. Check recent errors
echo "[5/5] Checking recent errors..."
docker-compose -f deployment/docker-compose.yml logs oracle-blue --since 24h 2>&1 | grep -i error | tail -5
echo ""

echo "=== Morning check complete ==="
```

**Save this as `morning-check.sh` and run it every morning!**

---

## Part 3: Common Tasks (15 minutes)

### Task 1: Investigating a Warning

**Scenario**: Batman agent shows "Warning" status

```bash
# Step 1: Check Batman's health
python3 -c "
from core.oracle_self_healing.health_monitor import AgentHealthMonitor
monitor = AgentHealthMonitor()
health = monitor.check_agent_health('Batman', [])
print(f'Status: {health[\"status\"]}')
print(f'Health: {health[\"health\"]}%')
print(f'Issues: {health.get(\"issues\", \"None\")}')
"

# Step 2: Check Batman's recent metrics
python3 -c "
from core.oracle_foundation.knowledge_base import OracleKnowledgeBase
kb = OracleKnowledgeBase()
metrics = kb.get_agent_metrics('Batman', hours=1)
print(f'Recent metrics (last hour): {len(metrics)}')
for m in metrics[-5:]:
    print(f'  {m}')
"

# Step 3: Check logs for Batman
docker-compose -f deployment/docker-compose.yml logs oracle-blue 2>&1 | grep -i batman | tail -20

# Step 4: If issue persists, create a ticket
# Document: agent name, health %, symptoms, when noticed
```

---

### Task 2: Applying a Fix

**Scenario**: Oracle suggests a fix for an issue

```bash
# Step 1: View proposed fixes
python3 -c "
from core.oracle_self_healing.fix_engine import FixEngine
engine = FixEngine()
fixes = engine.get_active_fixes()
print(f'Active proposed fixes: {len(fixes)}')
for fix in fixes:
    print(f'  Agent: {fix[\"agent_name\"]}')
    print(f'  Risk: {fix[\"risk_level\"]}')
    print(f'  Description: {fix[\"description\"]}')
    print()
"

# Step 2: Review fix details
# - LOW risk: Can apply immediately
# - MEDIUM risk: Needs approval
# - HIGH risk: Needs senior approval

# Step 3: Apply LOW risk fix
python3 -c "
from core.oracle_self_healing.fix_engine import FixEngine
engine = FixEngine()
result = engine.apply_fix('<fix-id>')
print(f'Result: {result}')
"

# Step 4: Verify fix worked
python3 -c "
from core.oracle_self_healing.health_monitor import AgentHealthMonitor
monitor = AgentHealthMonitor()
health = monitor.check_agent_health('<agent-name>', [])
print(f'New health: {health[\"health\"]}%')
"
```

**Rule**: Only apply LOW risk fixes without approval!

---

### Task 3: Checking Versions

**Scenario**: Check agent versions before update

```bash
# Step 1: List all agent versions
python3 -c "
from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl
vc = EnhancedVersionControl()
versions = vc.get_all_versions()
for agent, version in versions.items():
    print(f'{agent}: v{version}')
"

# Step 2: Check if update is safe
python3 -c "
from core.oracle_version_control.dependency_tracker import DependencyTracker
tracker = DependencyTracker()
impact = tracker.analyze_update_impact('AgentName', 'new-version')
print(f'Dependent agents: {impact[\"direct_dependents\"]}')
print(f'Update order: {impact[\"update_order\"]}')
"

# Step 3: Create new version (if approved)
python3 -c "
from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl
vc = EnhancedVersionControl()
result = vc.create_version('AgentName', 'MINOR', 'Description of changes')
print(f'New version: {result[\"new_version\"]}')
"
```

---

## Part 4: Emergency Procedures (10 minutes)

### Emergency Scenario 1: System Health < 75%

```bash
# IMMEDIATE ACTIONS:

# 1. Check which agents are unhealthy
python3 -c "
from core.oracle_integration.superman_connector import get_superman_interface
summary = get_superman_interface().get_agent_health_summary()
for agent, health in summary['agents'].items():
    if health['status'] != 'healthy':
        print(f'⚠️ {agent}: {health[\"status\"]} ({health[\"health\"]}%)')
"

# 2. Check recent errors
docker-compose -f deployment/docker-compose.yml logs oracle-blue --since 30m 2>&1 | grep -i error

# 3. Notify on-call engineer
# Use escalation path: Slack #oracle-critical, then phone

# 4. Document in incident ticket:
#    - Current system health %
#    - Which agents unhealthy
#    - Recent errors
#    - Actions taken
```

---

### Emergency Scenario 2: Critical Alert Fires

```bash
# IMMEDIATE ACTIONS:

# 1. Acknowledge alert in Alertmanager
# Visit: http://localhost:9093

# 2. Assess severity
# Critical = requires immediate action
# Warning = requires investigation

# 3. Follow runbook
# Each alert has a runbook link - follow it!

# 4. If no runbook or unclear, escalate immediately
```

---

### Emergency Scenario 3: Need to Rollback

```bash
# ONLY IF AUTHORIZED!

# Step 1: Verify issue warrants rollback
# - Error rate > 10%
# - System health < 50%
# - Multiple agents down

# Step 2: Execute rollback
./deployment/deploy.sh production --rollback --force

# Step 3: Verify rollback worked
python3 deployment/health_check.py

# Step 4: Monitor for 15 minutes
./monitor.sh

# Step 5: Create incident report
```

**⚠️ Only rollback if authorized or following runbook!**

---

## Part 5: Key Concepts (10 minutes)

### Concept 1: Self-Healing

Oracle can automatically detect and fix issues:

- **LOW risk fixes**: Applied automatically
- **MEDIUM risk fixes**: Require operator approval
- **HIGH risk fixes**: Require senior approval

**You decide**: Review proposed fixes, approve if safe

---

### Concept 2: Learning System

Oracle learns from patterns across agents:

- Detects recurring issues
- Identifies successful solutions
- Shares knowledge between agents
- Suggests improvements

**You benefit**: Better recommendations over time

---

### Concept 3: Version Control

All agent changes are versioned:

- **MAJOR**: Breaking changes (v1.0.0 → v2.0.0)
- **MINOR**: New features (v1.0.0 → v1.1.0)
- **PATCH**: Bug fixes (v1.0.0 → v1.0.1)

**You control**: Safe updates with easy rollback

---

### Concept 4: Superman Integration

Superman coordinates the Justice League, Oracle maintains them:

- Superman assigns tasks
- Oracle ensures agents are healthy
- They work together

**You monitor**: Both Superman and Oracle systems

---

## Part 6: Getting Help (5 minutes)

### When Something Goes Wrong

**Step 1**: Check the troubleshooting guide
```bash
cat docs/TROUBLESHOOTING_GUIDE.md | grep -A 20 "your-issue"
```

**Step 2**: Check operational runbooks
```bash
cat docs/OPERATIONAL_RUNBOOKS.md | grep -A 20 "your-scenario"
```

**Step 3**: Escalate
- Level 1: Senior operator
- Level 2: On-call engineer
- Level 3: Engineering manager

**Emergency**: Call on-call engineer directly

---

### Key Resources

| Document | Purpose | When to Use |
|----------|---------|-------------|
| `OPERATOR_QUICK_START.md` | Getting started | First day |
| `OPERATOR_TRAINING_MANUAL.md` | Full training | First week |
| `OPERATIONAL_RUNBOOKS.md` | Step-by-step procedures | Daily operations |
| `TROUBLESHOOTING_GUIDE.md` | Problem solving | When issues arise |
| `ORACLE_USER_GUIDE.md` | Complete reference | As needed |

---

## Quick Reference Card

Print this and keep it handy:

```
┌─────────────────────────────────────────────────────────────┐
│ ORACLE OPERATOR QUICK REFERENCE                             │
├─────────────────────────────────────────────────────────────┤
│ HEALTH CHECK:                                               │
│   python3 deployment/health_check.py                        │
│                                                             │
│ SYSTEM STATUS:                                              │
│   docker-compose -f deployment/docker-compose.yml ps        │
│                                                             │
│ VIEW LOGS:                                                  │
│   docker-compose -f deployment/docker-compose.yml logs -f   │
│                                                             │
│ RESTART SERVICE:                                            │
│   docker-compose -f deployment/docker-compose.yml restart   │
│                                                             │
│ DASHBOARDS:                                                 │
│   Grafana: http://localhost:3000                            │
│   Prometheus: http://localhost:9090                         │
│   Alerts: http://localhost:9093                             │
│                                                             │
│ HEALTH THRESHOLDS:                                          │
│   Healthy: 90-100% ✅                                       │
│   Warning: 70-89% ⚠️                                        │
│   Unhealthy: 50-69% ⚠️                                      │
│   Critical: 0-49% 🚨                                        │
│                                                             │
│ ESCALATION:                                                 │
│   <75% health → Notify on-call                              │
│   <50% health → Call on-call immediately                    │
│   Error rate >10% → Consider rollback                       │
│                                                             │
│ EMERGENCY CONTACTS:                                         │
│   On-Call: [Phone] [Email]                                  │
│   Backup: [Phone] [Email]                                   │
│   Manager: [Phone] [Email]                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Next Steps

### After This Quick Start

1. **Complete full training** (4-6 hours)
   - Read: `docs/OPERATOR_TRAINING_MANUAL.md`
   - Complete all 5 hands-on exercises

2. **Take certification exam** (1-2 hours)
   - See: `docs/OPERATOR_CERTIFICATION_PROGRAM.md`
   - Pass with 80% to become certified

3. **Shadow experienced operator** (1-2 days)
   - Observe daily operations
   - Handle issues together
   - Build confidence

4. **Independent operations** (Week 2+)
   - Morning health checks
   - Incident response
   - Documentation updates

---

## Common Questions

**Q: What if I break something?**
A: Oracle has comprehensive backups and rollback capability. Follow procedures carefully and ask for help when unsure.

**Q: How do I know if I should escalate?**
A: When in doubt, escalate! Better to ask than to let an issue grow.

**Q: Can I experiment in production?**
A: No. Use staging environment for experiments. Production is for operations only.

**Q: What if alerts fire after hours?**
A: Follow the runbook. If unclear, call on-call engineer immediately.

**Q: How often should I check things?**
A: Morning check daily, monitor dashboards hourly, respond to alerts immediately.

---

## Success Checklist

You're ready to operate Oracle when you can:

- [ ] Run a morning health check
- [ ] Identify unhealthy agents
- [ ] View logs and dashboards
- [ ] Understand health status levels
- [ ] Know when to escalate
- [ ] Apply LOW risk fixes
- [ ] Check agent versions
- [ ] Access all documentation
- [ ] Contact on-call engineer

**If you checked all boxes: You're ready! 🎉**

---

## Final Tips

1. **Take notes**: Document what you learn
2. **Ask questions**: No question is stupid
3. **Be cautious**: When in doubt, escalate
4. **Monitor regularly**: Don't wait for alerts
5. **Keep learning**: Review documentation regularly

---

**Oracle says**: "Every operator starts here. Take your time, ask questions, and remember - you're protecting the Justice League." 🦸‍♂️

**Welcome to the team!** 👋

---

**Need Help?**
- Slack: #oracle-help
- Email: oracle-ops@example.com
- Emergency: [On-call phone number]
