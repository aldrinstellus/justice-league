# 📘 Oracle Operational Runbooks

**Week 13-14: Documentation & Training**
**Target Audience**: On-Call Operators, Superman, Production Support
**Purpose**: Quick reference procedures for common operations

---

## Table of Contents

1. [Daily Operations](#daily-operations)
2. [Deployment Procedures](#deployment-procedures)
3. [Emergency Procedures](#emergency-procedures)
4. [Health & Monitoring](#health-monitoring)
5. [Version Management](#version-management)
6. [Troubleshooting](#troubleshooting)
7. [Maintenance Tasks](#maintenance-tasks)

---

## Daily Operations

### Runbook: Morning System Check

**Duration**: 10-15 minutes
**Frequency**: Daily (weekdays)
**Prerequisites**: Access to Oracle server, Python environment

**Procedure**:

```bash
# Step 1: Navigate to Oracle directory
cd /Users/admin/Documents/claudecode/Projects/aldo-vision

# Step 2: Run system health check
python3 deployment/health_check.py

# Expected output:
# ✅ Status: HEALTHY
# OR
# ⚠️  Status: DEGRADED (investigate warnings)
# OR
# ❌ Status: UNHEALTHY (escalate immediately)

# Step 3: Check agent health summary
python3 -c "
from core.oracle_integration.superman_connector import get_superman_interface
connector = get_superman_interface()
health = connector.get_agent_health_summary()
print(f'System Health: {health[\"health_percentage\"]:.1f}%')
print(f'Healthy: {health[\"healthy_count\"]}/{health[\"total_agents\"]}')
print(f'Warnings: {health[\"warning_count\"]}')
print(f'Unhealthy: {health[\"unhealthy_count\"]}')
print(f'Critical: {health[\"critical_count\"]}')
"

# Expected: Health percentage > 90%

# Step 4: Check for alerts
python3 -c "
from core.oracle_integration.oracle_coordinator import OracleCoordinator
coordinator = OracleCoordinator()
alerts = coordinator.get_pending_alerts()
print(f'Pending Alerts: {len(alerts.get(\"alerts\", []))}')
if alerts.get('alerts'):
    for alert in alerts['alerts']:
        print(f'  - {alert[\"severity\"]}: {alert[\"message\"]}')
"

# Step 5: Verify latest backup
ls -lht deployment/backups/production/ | head -3

# Expected: Backup from last 12 hours

# Step 6: Check logs for errors
tail -n 50 logs/oracle.log | grep -i error

# Step 7: Open Grafana dashboard (optional)
open http://localhost:3000
```

**Success Criteria**:
- ✅ Health check passes or shows only warnings
- ✅ Agent health > 90%
- ✅ No critical alerts
- ✅ Recent backup exists (< 12 hours)
- ✅ No critical errors in logs

**If Issues Found**:
- Health < 90%: See [Runbook: Investigate Unhealthy Agents](#runbook-investigate-unhealthy-agents)
- Critical alerts: See [Runbook: Handle Critical Alert](#runbook-handle-critical-alert)
- No recent backup: See [Runbook: Manual Backup](#runbook-manual-backup)

---

### Runbook: Weekly System Scan

**Duration**: 30 minutes
**Frequency**: Weekly (Monday mornings)
**Prerequisites**: Completed morning system check

**Procedure**:

```bash
# Step 1: Full system scan
python3 -c "
from core.oracle_integration.oracle_coordinator import OracleCoordinator
coordinator = OracleCoordinator()
scan = coordinator.perform_system_scan()
print(f'Agents Scanned: {scan[\"scan_results\"][\"agents_scanned\"]}')
print(f'Issues Found: {scan[\"scan_results\"][\"issues_found\"]}')
print(f'Recommendations: {len(scan[\"recommendations\"])}')
print('\nRecommendations:')
for i, rec in enumerate(scan['recommendations'], 1):
    print(f'  {i}. {rec}')
"

# Step 2: Version audit
python3 -c "
from core.oracle_integration.superman_connector import get_superman_interface
connector = get_superman_interface()
versions = connector.get_agent_versions()
print('Agent Versions:')
for agent, info in sorted(versions['versions'].items()):
    print(f'  {agent}: v{info[\"version\"]}')
"

# Step 3: Performance review
python3 -c "
from core.oracle_integration.superman_connector import get_superman_interface
import sys
connector = get_superman_interface()
health = connector.get_agent_health_summary()
slow_agents = []
for agent, info in health['agents'].items():
    metrics = info['metrics']
    p95 = metrics.get('p95_response_time', 0)
    if agent in ['flash'] and p95 > 1000:  # Flash should be < 1s
        slow_agents.append(f'{agent} (p95: {p95:.0f}ms)')
    elif agent in ['batman'] and p95 > 2000:  # Batman should be < 2s
        slow_agents.append(f'{agent} (p95: {p95:.0f}ms)')
    elif p95 > 3000:  # Others should be < 3s
        slow_agents.append(f'{agent} (p95: {p95:.0f}ms)')

if slow_agents:
    print('⚠ Slow Agents:')
    for agent in slow_agents:
        print(f'  - {agent}')
else:
    print('✓ All agents meeting performance targets')
"

# Step 4: Disk cleanup
echo "Cleaning old logs (> 30 days)..."
find logs/ -name "*.log" -mtime +30 -exec rm -f {} \;

echo "Cleaning old backups (keeping last 30)..."
cd deployment/backups/production
ls -t oracle_backup_*.db | tail -n +31 | xargs rm -f
cd -

# Step 5: Check for circular dependencies
python3 -c "
from core.oracle_integration.superman_connector import get_superman_interface
connector = get_superman_interface()
graph = connector.get_dependency_graph()
if graph['has_circular_dependencies']:
    print('⚠ CIRCULAR DEPENDENCIES DETECTED!')
    print('Circular chains:')
    for chain in graph['circular_chains']:
        print(f'  {\" → \".join(chain)}')
else:
    print('✓ No circular dependencies')
"
```

**Success Criteria**:
- ✅ System scan completes
- ✅ All agents on supported versions
- ✅ No performance issues
- ✅ Disk space freed up
- ✅ No circular dependencies

**Follow-up Actions**:
- Document any recommendations for future action
- Create tickets for performance issues
- Plan agent updates if versions outdated

---

## Deployment Procedures

### Runbook: Deploy to Staging

**Duration**: 30 minutes
**Frequency**: As needed (typically after each feature)
**Prerequisites**: Code merged to `develop` branch, all tests passing

**Procedure**:

```bash
# Step 1: Verify prerequisites
cd /Users/admin/Documents/claudecode/Projects/aldo-vision

# Check current git branch
git branch
# Should be on develop branch

# Check for uncommitted changes
git status
# Should show "working tree clean"

# Step 2: Pull latest changes
git pull origin develop

# Step 3: Review changes being deployed
git log --oneline -10

# Step 4: Run pre-deployment checks
python3 deployment/health_check.py
# Verify system is healthy before deploying

# Step 5: Execute deployment
./deployment/deploy.sh staging

# Deployment script will:
# - Check prerequisites
# - Backup database
# - Run test suite
# - Build Docker images
# - Deploy to staging (blue-green)
# - Run health checks
# - Switch traffic
# - Setup monitoring

# Step 6: Monitor deployment
# Watch for any errors during deployment
# Process should take 10-15 minutes

# Step 7: Post-deployment verification
sleep 30  # Wait for services to stabilize

python3 deployment/health_check.py
# Expected: ✅ Status: HEALTHY

# Step 8: Smoke tests
python3 -c "
from core.oracle_integration.superman_connector import get_superman_interface
connector = get_superman_interface()

# Test heartbeat
heartbeat = connector.heartbeat()
assert heartbeat['status'] == 'ok', 'Heartbeat failed'

# Test agent health
health = connector.get_agent_health_summary()
assert health['health_percentage'] > 80, 'Health too low'

print('✓ All smoke tests passed')
"

# Step 9: Monitor for 15 minutes
echo "Monitoring staging for 15 minutes..."
# Watch Grafana dashboard: http://localhost:3000
# Look for:
# - Error rate spikes
# - Response time increases
# - Health percentage drops

# Step 10: Document deployment
echo "Deployment to staging completed: $(date)" >> deployment/logs/deployments.log
```

**Success Criteria**:
- ✅ Deployment completes without errors
- ✅ Health check passes
- ✅ Smoke tests pass
- ✅ No alerts in first 15 minutes
- ✅ Grafana shows stable metrics

**If Deployment Fails**:
- Deployment automatically rolls back
- Check logs: `deployment/logs/deployment_*.log`
- Review errors and fix before retrying
- See [Runbook: Investigate Deployment Failure](#runbook-investigate-deployment-failure)

---

### Runbook: Deploy to Production

**Duration**: 45 minutes
**Frequency**: As needed (typically weekly)
**Prerequisites**: Tested in staging, change approval obtained, maintenance window scheduled

**Procedure**:

```bash
# Step 1: Pre-deployment checklist
cat << 'EOF'
Production Deployment Checklist:
□ Code tested in staging
□ All tests passing (110/110 + 10/10 deployment)
□ Change approval obtained
□ Stakeholders notified
□ Rollback plan documented
□ Backup verified recent
□ Maintenance window scheduled (if needed)
EOF

read -p "All items checked? (yes/no): " response
[[ "$response" != "yes" ]] && echo "Complete checklist first" && exit 1

# Step 2: Announce deployment
echo "PRODUCTION DEPLOYMENT STARTING: $(date)" | mail -s "Oracle Production Deployment" team@example.com

# Step 3: Pre-deployment backup
cd /Users/admin/Documents/claudecode/Projects/aldo-vision
python3 -c "
import shutil
from datetime import datetime
backup_name = f'deployment/backups/production/pre_deploy_{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}.db'
shutil.copy('oracle.db', backup_name)
print(f'Backup created: {backup_name}')
"

# Step 4: Verify production health before deploy
python3 deployment/health_check.py
# Must be HEALTHY before proceeding

# Step 5: Execute production deployment
./deployment/deploy.sh production

# NOTE: Deployment script will prompt for confirmation
# Review summary carefully before confirming

# Deployment process:
# - Backup database
# - Run full test suite (all 7 test files)
# - Build Docker images
# - Deploy to inactive environment (blue or green)
# - Health check new environment (5 min timeout)
# - Switch traffic via Nginx
# - Monitor new environment
# - Stop old environment

# Step 6: Post-deployment health check (immediate)
sleep 60  # Wait 1 minute for stabilization

python3 deployment/health_check.py
# Expected: ✅ Status: HEALTHY

# Step 7: Comprehensive verification
python3 -c "
from core.oracle_integration.superman_connector import get_superman_interface
connector = get_superman_interface()

print('Running post-deployment verification...')

# 1. Heartbeat
heartbeat = connector.heartbeat()
assert heartbeat['status'] == 'ok', 'Heartbeat failed'
print('✓ Heartbeat OK')

# 2. Agent health
health = connector.get_agent_health_summary()
assert health['health_percentage'] > 90, f'Health only {health[\"health_percentage\"]:.1f}%'
print(f'✓ Agent Health: {health[\"health_percentage\"]:.1f}%')

# 3. Versions
versions = connector.get_agent_versions()
print(f'✓ {len(versions[\"versions\"])} agent versions tracked')

# 4. Oracle status
from core.oracle_integration.oracle_coordinator import OracleCoordinator
coordinator = OracleCoordinator()
status = coordinator.get_oracle_status()
assert status['operational'], 'Oracle not operational'
print(f'✓ Oracle operational ({len(status[\"active_capabilities\"])} capabilities)')

print('\n✅ All verification checks passed')
"

# Step 8: Monitor for 15 minutes (critical period)
echo "======================================"
echo "CRITICAL MONITORING PERIOD: 15 minutes"
echo "======================================"
echo "Start time: $(date)"
echo ""
echo "Monitoring:"
echo "  - Grafana: http://localhost:3000"
echo "  - Prometheus: http://localhost:9090"
echo ""
echo "Watch for:"
echo "  - Error rate spikes"
echo "  - Response time increases"
echo "  - Health percentage drops"
echo "  - Agent failures"
echo ""

# Set up monitoring loop
for i in {1..15}; do
    echo "Minute $i/15 - $(date)"

    # Quick health check
    python3 -c "
from core.oracle_integration.superman_connector import get_superman_interface
connector = get_superman_interface()
health = connector.get_agent_health_summary()
print(f'  Health: {health[\"health_percentage\"]:.1f}% ({health[\"healthy_count\"]}/{health[\"total_agents\"]} healthy)')
if health['health_percentage'] < 90:
    print('  ⚠ WARNING: Health below 90%!')
if health['critical_count'] > 0:
    print(f'  ⚠ ALERT: {health[\"critical_count\"]} agent(s) critical!')
    " 2>/dev/null || echo "  ⚠ Health check failed"

    sleep 60
done

echo ""
echo "======================================"
echo "15-minute monitoring complete: $(date)"
echo "======================================"

# Step 9: Extended monitoring (next 45 minutes)
echo "Continuing extended monitoring for 45 minutes..."
echo "Check Grafana dashboard regularly"
echo "Alert if any issues arise"

# Step 10: Deployment completion
echo "Production deployment completed: $(date)" | mail -s "Oracle Production Deployment Complete" team@example.com

echo "
Deployment Summary:
- Started: [check deployment log]
- Completed: $(date)
- Health: [check current health]
- Issues: [none or list issues]

Next steps:
- Continue monitoring for 24 hours
- Review metrics tomorrow
- Update deployment log
"
```

**Success Criteria**:
- ✅ Deployment completes without errors
- ✅ Health check passes immediately
- ✅ All verification checks pass
- ✅ No alerts in first 15 minutes
- ✅ Metrics stable in Grafana
- ✅ No increase in error rates
- ✅ Response times within targets

**If Issues Arise**:
- **High error rate**: See [Runbook: Emergency Rollback](#runbook-emergency-rollback)
- **Health < 90%**: Investigate immediately, consider rollback
- **Any critical alerts**: Execute emergency rollback
- **Response time degraded**: Monitor for 5 more minutes, rollback if no improvement

---

## Emergency Procedures

### Runbook: Emergency Rollback

**Duration**: 5-10 minutes
**When**: Production deployment causing issues, high error rate, system instability
**Prerequisites**: Issue confirmed, decision made to rollback

⚠️ **CRITICAL PROCEDURE - READ CAREFULLY** ⚠️

**Procedure**:

```bash
# Step 1: Announce rollback
echo "EMERGENCY ROLLBACK INITIATED: $(date)" | mail -s "URGENT: Oracle Rollback" team@example.com

# Step 2: Execute rollback
cd /Users/admin/Documents/claudecode/Projects/aldo-vision

# Rollback to previous version (Blue-green switch)
./deployment/deploy.sh production --rollback --force

# This will:
# - Start previous environment (currently stopped)
# - Health check previous environment
# - Switch traffic back to previous environment
# - Stop failed environment

# Process should take < 5 minutes

# Step 3: Verify rollback successful
sleep 30

python3 deployment/health_check.py
# Expected: ✅ Status: HEALTHY

# Step 4: Verify agent health
python3 -c "
from core.oracle_integration.superman_connector import get_superman_interface
connector = get_superman_interface()
health = connector.get_agent_health_summary()
print(f'Post-rollback Health: {health[\"health_percentage\"]:.1f}%')
print(f'Healthy agents: {health[\"healthy_count\"]}/{health[\"total_agents\"]}')

if health['health_percentage'] > 90:
    print('✅ ROLLBACK SUCCESSFUL')
else:
    print('⚠ WARNING: Health still degraded')
    print('ESCALATE IMMEDIATELY')
"

# Step 5: Monitor for 10 minutes
echo "Monitoring rolled-back system for 10 minutes..."

for i in {1..10}; do
    echo "Minute $i/10"
    python3 -c "
from core.oracle_integration.superman_connector import get_superman_interface
connector = get_superman_interface()
health = connector.get_agent_health_summary()
print(f'  Health: {health[\"health_percentage\"]:.1f}%')
" 2>/dev/null
    sleep 60
done

# Step 6: Announce rollback complete
echo "ROLLBACK COMPLETE: $(date)" | mail -s "Oracle Rollback Complete" team@example.com

# Step 7: Create incident report
cat > incident_reports/rollback_$(date +%Y%m%d_%H%M%S).txt << EOF
Incident: Emergency Production Rollback
Date: $(date)
Operator: $(whoami)

Timeline:
- Deployment started: [time]
- Issue detected: [time]
- Rollback initiated: [time]
- Rollback completed: [time]

Issue Description:
[Describe what went wrong]

Resolution:
- Rolled back to previous version
- System stable after rollback
- Health: [current health percentage]

Root Cause:
[To be determined - post-incident review]

Action Items:
1. Post-incident review meeting
2. Fix underlying issue
3. Additional testing before retry
4. Update deployment procedures if needed
EOF

echo "Incident report created. Schedule post-incident review."
```

**Success Criteria**:
- ✅ Rollback completes in < 5 minutes
- ✅ Health returns to > 90%
- ✅ No critical alerts
- ✅ Metrics stable in Grafana
- ✅ Error rate returns to baseline

**If Rollback Fails**:
This is a CRITICAL situation. Escalate immediately.

1. Check if both blue and green environments are down
2. Try manual restart: `docker-compose up -d oracle-blue`
3. If still failing, restore from backup:
```bash
docker-compose down
cp deployment/backups/production/oracle_backup_latest.db oracle.db
docker-compose up -d
```
4. Page senior engineer
5. Activate incident response team

---

### Runbook: System Complete Outage

**Duration**: 15-30 minutes
**When**: Oracle completely down, all agents failing
**Prerequisites**: Confirmed outage, incident declared

⚠️ **P0 INCIDENT - IMMEDIATE ESCALATION REQUIRED** ⚠️

**Procedure**:

```bash
# Step 1: Declare P0 incident
echo "P0 INCIDENT DECLARED: $(date) - Oracle complete outage" >> incidents/current_p0.txt
echo "P0: Oracle Complete Outage" | mail -s "P0 INCIDENT" oncall@example.com team@example.com

# Step 2: Quick diagnostic
cd /Users/admin/Documents/claudecode/Projects/aldo-vision

# Check if containers running
docker-compose ps

# Check recent logs
tail -n 100 logs/oracle.log

# Check disk space
df -h

# Check if database file exists and accessible
ls -lh oracle.db

# Step 3: Attempt restart
echo "Attempting Oracle restart..."
docker-compose restart oracle-blue oracle-green

sleep 30

# Check if services came up
docker-compose ps

# Step 4: Health check
python3 deployment/health_check.py

# If health check passes:
if [ $? -eq 0 ]; then
    echo "✅ System recovered after restart"
    echo "Continue monitoring for 30 minutes"
    # Skip to Step 8
fi

# Step 5: If restart failed, try full redeploy
echo "Restart failed. Attempting full recovery..."

# Stop all services
docker-compose down

# Backup current state
cp oracle.db oracle_failed_$(date +%Y%m%d_%H%M%S).db

# Restore latest backup
cp deployment/backups/production/oracle_backup_latest.db oracle.db

# Restart services
docker-compose up -d

sleep 60

# Step 6: Verify recovery
python3 deployment/health_check.py

if [ $? -eq 0 ]; then
    echo "✅ System recovered from backup"
else
    echo "❌ RECOVERY FAILED - ESCALATE TO SENIOR ENGINEER"
    # This is worst-case scenario
    # Manual intervention required
fi

# Step 7: Document recovery
cat >> incidents/current_p0.txt << EOF

Recovery Timeline:
- Outage detected: [time]
- P0 declared: [time]
- Restart attempted: [time]
- Backup restored: [time]
- System recovered: [time]
- Total downtime: [duration]

Recovery Actions:
1. [action taken]
2. [action taken]
3. [result]

Current Status:
- Oracle: [up/down]
- Health: [percentage]
- All agents: [status]
EOF

# Step 8: Extended monitoring (1 hour)
echo "CRITICAL: Monitor system for next hour"
echo "Watch for:"
echo "  - Health drops"
echo "  - Error spikes"
echo "  - Agent failures"

# Step 9: Post-incident
echo "
POST-INCIDENT ACTIONS REQUIRED:
1. Complete incident report
2. Root cause analysis
3. Post-mortem meeting (within 24 hours)
4. Implement preventative measures
5. Update runbooks if needed
"
```

**Success Criteria**:
- ✅ System back online
- ✅ Health > 90%
- ✅ All critical agents operational
- ✅ Downtime documented
- ✅ Post-incident review scheduled

**Escalation**:
If system cannot be recovered:
1. Page senior engineer immediately
2. Contact engineering manager
3. Activate full incident response team
4. Consider manual migration to backup server

---

## Health & Monitoring

### Runbook: Investigate Unhealthy Agents

**Duration**: 15-30 minutes
**When**: Agent health < 90%, multiple agents in warning/unhealthy state
**Prerequisites**: Morning health check identified issues

**Procedure**:

```python
# Step 1: Identify unhealthy agents
from core.oracle_integration.superman_connector import get_superman_interface

connector = get_superman_interface()
health = connector.get_agent_health_summary()

unhealthy_agents = []
for agent, status in health['agents'].items():
    if status['status'] in ['unhealthy', 'critical', 'warning']:
        unhealthy_agents.append({
            'name': agent,
            'status': status['status'],
            'success_rate': status['metrics']['success_rate'],
            'error_count': status['metrics']['error_count'],
            'last_error': status['metrics'].get('last_error', 'None')
        })

print(f"Found {len(unhealthy_agents)} unhealthy agents:")
for agent in unhealthy_agents:
    print(f"\n{agent['name']}:")
    print(f"  Status: {agent['status']}")
    print(f"  Success Rate: {agent['success_rate']:.1f}%")
    print(f"  Error Count: {agent['error_count']}")
    print(f"  Last Error: {agent['last_error']}")

# Step 2: Check logs for each unhealthy agent
import subprocess
for agent in unhealthy_agents:
    print(f"\nRecent errors for {agent['name']}:")
    subprocess.run(f"grep -i {agent['name']} logs/oracle.log | grep -i error | tail -10", shell=True)

# Step 3: Attempt self-healing for each agent
print("\nAttempting self-healing...")
for agent in unhealthy_agents:
    print(f"\nHealing {agent['name']}...")
    healing_result = connector.request_self_healing(agent['name'])

    if healing_result.get('success'):
        print(f"  ✓ Applied {healing_result['fixes_applied']} fixes")
        print(f"  Risk level: {healing_result['risk_level']}")
    else:
        print(f"  ✗ Healing failed: {healing_result.get('error', 'Unknown error')}")

# Step 4: Wait and re-check health (5 minutes)
import time
print("\nWaiting 5 minutes for healing to take effect...")
time.sleep(300)

# Re-check health
health_after = connector.get_agent_health_summary()
print(f"\nHealth after healing: {health_after['health_percentage']:.1f}%")

improved = []
still_unhealthy = []

for agent in unhealthy_agents:
    agent_name = agent['name']
    new_status = health_after['agents'][agent_name]['status']

    if new_status == 'healthy':
        improved.append(agent_name)
    else:
        still_unhealthy.append((agent_name, new_status))

print(f"\nImproved: {len(improved)} agents")
for agent in improved:
    print(f"  ✓ {agent}")

if still_unhealthy:
    print(f"\nStill unhealthy: {len(still_unhealthy)} agents")
    for agent, status in still_unhealthy:
        print(f"  ✗ {agent} - {status}")

    print("\nManual intervention required for remaining agents.")
    print("Actions:")
    print("  1. Review agent-specific logs")
    print("  2. Check recent code changes")
    print("  3. Consider rolling back agent version")
    print("  4. Check external dependencies")
else:
    print("\n✅ All agents healthy after self-healing")
```

**Success Criteria**:
- ✅ All agents return to healthy status
- ✅ System health > 90%
- ✅ No errors in logs after healing
- ✅ Self-healing fixes documented

**Next Steps if Still Unhealthy**:
1. Review agent code for bugs
2. Check if recent version update caused issue
3. Consider rollback of specific agent
4. Check external API availability (if agent depends on external service)
5. Escalate if unable to resolve

---

### Runbook: Handle Critical Alert

**Duration**: 5-15 minutes
**When**: Critical alert received (email/Slack/Prometheus)
**Prerequisites**: Alert notification received

**Procedure**:

```bash
# Step 1: Acknowledge alert
python3 -c "
from core.oracle_integration.oracle_coordinator import OracleCoordinator
coordinator = OracleCoordinator()

# Get pending alerts
alerts = coordinator.get_pending_alerts()

print('Critical Alerts:')
for alert in alerts.get('alerts', []):
    if alert['severity'] == 'critical':
        print(f\"  ID: {alert['alert_id']}\")
        print(f\"  Message: {alert['message']}\")
        print(f\"  Agent: {alert.get('agent_name', 'system')}\")
        print()

        # Acknowledge alert (marks as seen)
        coordinator.acknowledge_alert(alert['alert_id'])
        print(f\"  ✓ Alert {alert['alert_id']} acknowledged\")
"

# Step 2: Investigate based on alert type

# Alert Type: "OracleInstanceDown"
if [[ $ALERT_TYPE == "OracleInstanceDown" ]]; then
    echo "Oracle instance down - checking..."
    docker-compose ps

    # If container stopped, restart
    docker-compose up -d oracle-blue oracle-green
    sleep 30
    python3 deployment/health_check.py
fi

# Alert Type: "DatabaseConnectionFailed"
if [[ $ALERT_TYPE == "DatabaseConnectionFailed" ]]; then
    echo "Database connection failed - checking..."

    # Check if database file exists
    ls -lh oracle.db

    # Check file permissions
    ls -l oracle.db

    # Try to open database
    sqlite3 oracle.db "SELECT COUNT(*) FROM agents;" && echo "Database accessible" || echo "Database corrupted"

    # If corrupted, restore backup
    # cp deployment/backups/production/oracle_backup_latest.db oracle.db
fi

# Alert Type: "LowDiskSpace"
if [[ $ALERT_TYPE == "LowDiskSpace" ]]; then
    echo "Low disk space - cleaning up..."

    # Show disk usage
    df -h

    # Clean old logs
    find logs/ -name "*.log" -mtime +7 -delete

    # Clean old backups
    cd deployment/backups/production
    ls -t oracle_backup_*.db | tail -n +15 | xargs rm -f
    cd -

    # Check disk after cleanup
    df -h
fi

# Alert Type: "AgentHealthCritical"
if [[ $ALERT_TYPE == "AgentHealthCritical" ]]; then
    echo "Agent health critical - investigating..."

    python3 -c "
from core.oracle_integration.superman_connector import get_superman_interface
connector = get_superman_interface()
health = connector.get_agent_health_summary()

critical_agents = [
    agent for agent, status in health['agents'].items()
    if status['status'] == 'critical'
]

print(f'Critical agents: {critical_agents}')

for agent in critical_agents:
    print(f'\nAttempting heal: {agent}')
    healing = connector.request_self_healing(agent)
    print(f'  Fixes applied: {healing.get(\"fixes_applied\", 0)}')
    "
fi

# Step 3: Verify alert resolved
sleep 60

python3 -c "
from core.oracle_integration.oracle_coordinator import OracleCoordinator
coordinator = OracleCoordinator()
alerts = coordinator.get_pending_alerts()

critical_alerts = [a for a in alerts.get('alerts', []) if a['severity'] == 'critical']

if not critical_alerts:
    print('✅ All critical alerts resolved')
else:
    print(f'⚠ Still {len(critical_alerts)} critical alerts:')
    for alert in critical_alerts:
        print(f'  - {alert[\"message\"]}')
    print('\nESCALATE IF NOT RESOLVED IN 10 MINUTES')
"

# Step 4: Document resolution
cat >> logs/alert_resolutions.log << EOF
$(date): Critical alert resolved
Alert: $ALERT_TYPE
Actions taken: [describe actions]
Resolution time: [time]
Status: Resolved/Escalated
EOF
```

**Success Criteria**:
- ✅ Alert acknowledged
- ✅ Root cause identified
- ✅ Issue resolved
- ✅ No new critical alerts
- ✅ System stable

**Escalation**:
If alert cannot be resolved within 15 minutes:
1. Escalate to Superman
2. Create incident ticket
3. Consider emergency rollback if recent deployment
4. Activate incident response team if P0/P1

---

## Version Management

### Runbook: Update Agent Version

**Duration**: 20 minutes
**When**: Bug fix deployed, new feature ready, security patch
**Prerequisites**: Code changes tested, version number determined

**Procedure**:

```python
# Step 1: Determine version change type
# PATCH: 1.0.0 → 1.0.1 (bug fixes)
# MINOR: 1.0.1 → 1.1.0 (new features, backward compatible)
# MAJOR: 1.1.0 → 2.0.0 (breaking changes)

agent_name = "batman"  # Change to your agent
change_type = "patch"  # patch/minor/major
changes_description = "Fixed HTML parsing bug for nested elements"
breaking_changes_list = None  # Only for MAJOR updates

# Step 2: Check current version
from core.oracle_integration.superman_connector import get_superman_interface

connector = get_superman_interface()
versions = connector.get_agent_versions()
current_version = versions['versions'][agent_name]['version']
print(f"Current version: {current_version}")

# Step 3: Analyze update impact (IMPORTANT for MINOR/MAJOR)
if change_type in ['minor', 'major']:
    # Calculate new version first
    parts = [int(x) for x in current_version.split('.')]
    if change_type == 'major':
        new_version = f"{parts[0] + 1}.0.0"
    else:  # minor
        new_version = f"{parts[0]}.{parts[1] + 1}.0"

    print(f"\nAnalyzing impact of {current_version} → {new_version}...")
    impact = connector.analyze_update_impact(agent_name, new_version)

    print(f"Directly affected: {impact['directly_affected']}")
    print(f"Indirectly affected: {impact['indirectly_affected']}")
    print(f"Total affected: {impact['total_affected']} agents")
    print(f"Update order: {impact['update_order']}")

    # Review before proceeding
    response = input("\nProceed with update? (yes/no): ")
    if response.lower() != 'yes':
        print("Update cancelled")
        exit()

# Step 4: Create new version
print(f"\nCreating new {change_type} version...")

result = connector.request_version_update(
    agent_name=agent_name,
    change_type=change_type,
    changes=changes_description,
    breaking_changes=breaking_changes_list
)

if result.get('success'):
    new_version = result['new_version']
    print(f"✓ Updated: {current_version} → {new_version}")
    print(f"  Backup created: {result.get('backup_path', 'N/A')}")
    print(f"  Git commit: {result.get('git_commit', 'N/A')}")
else:
    print(f"✗ Update failed: {result.get('error', 'Unknown error')}")
    exit(1)

# Step 5: Verify agent still healthy
import time
print("\nWaiting 2 minutes for stability...")
time.sleep(120)

health = connector.get_agent_health_summary()
agent_health = health['agents'][agent_name]

print(f"\nPost-update health:")
print(f"  Status: {agent_health['status']}")
print(f"  Success rate: {agent_health['metrics']['success_rate']:.1f}%")

if agent_health['status'] != 'healthy':
    print("\n⚠ WARNING: Agent not healthy after update")
    print("Consider rollback:")
    print(f"  python3 -c \"from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl; vc = EnhancedVersionControl(); vc.rollback_version('{agent_name}', '{current_version}')\"")
else:
    print("\n✓ Version update successful")

# Step 6: If MAJOR update, update dependent agents
if change_type == 'major' and impact['directly_affected']:
    print("\n⚠ MAJOR update - dependent agents need updating:")
    for dep_agent in impact['directly_affected']:
        print(f"  - {dep_agent}")
    print("\nUpdate dependent agents manually or coordinate via OracleCoordinator")

# Step 7: Document update
with open('logs/version_updates.log', 'a') as f:
    from datetime import datetime
    f.write(f"\n{datetime.now()}: {agent_name} {current_version} → {new_version}")
    f.write(f"\n  Type: {change_type}")
    f.write(f"\n  Changes: {changes_description}")
    if breaking_changes_list:
        f.write(f"\n  Breaking changes: {breaking_changes_list}")
    f.write("\n")

print("\nVersion update complete!")
```

**Success Criteria**:
- ✅ New version created
- ✅ Agent remains healthy
- ✅ Backup created
- ✅ Git commit made (if enabled)
- ✅ No dependent agents broken (MAJOR updates)

**Rollback if Needed**:
```python
from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl

vc = EnhancedVersionControl()
vc.rollback_version(agent_name='batman', target_version='1.0.0')
```

---

### Runbook: Manual Backup

**Duration**: 2 minutes
**When**: Before risky changes, before major updates, backup schedule failed
**Prerequisites**: Oracle database accessible

**Procedure**:

```bash
# Step 1: Create backup directory if needed
mkdir -p deployment/backups/production

# Step 2: Create backup with timestamp
backup_name="deployment/backups/production/manual_backup_$(date +%Y%m%d_%H%M%S).db"
cp oracle.db "$backup_name"

# Step 3: Verify backup created
if [ -f "$backup_name" ]; then
    size=$(du -h "$backup_name" | cut -f1)
    echo "✓ Backup created: $backup_name ($size)"
else
    echo "✗ Backup failed!"
    exit 1
fi

# Step 4: Verify backup integrity
sqlite3 "$backup_name" "PRAGMA integrity_check;" | grep "ok" && echo "✓ Backup integrity verified" || echo "⚠ Backup may be corrupted"

# Step 5: Compress backup (optional, for long-term storage)
gzip "$backup_name"
echo "✓ Backup compressed: ${backup_name}.gz"

# Step 6: Document backup
echo "$(date): Manual backup created - $backup_name" >> logs/backups.log
```

**Success Criteria**:
- ✅ Backup file created
- ✅ Backup same size as original database (approximately)
- ✅ Integrity check passes
- ✅ Backup documented

---

## Troubleshooting

### Runbook: Investigate Deployment Failure

**Duration**: 30 minutes
**When**: Deployment to staging/production fails
**Prerequisites**: Deployment error occurred

**Procedure**:

```bash
# Step 1: Find latest deployment log
latest_log=$(ls -t deployment/logs/deployment_*.log | head -1)
echo "Reviewing: $latest_log"

# Step 2: Check for common errors
echo "\n=== Checking for common errors ==="

# Test failures
if grep -q "FAILED" "$latest_log"; then
    echo "✗ Test failures detected:"
    grep "FAILED" "$latest_log"
fi

# Docker build errors
if grep -q "ERROR.*docker" "$latest_log"; then
    echo "✗ Docker build errors:"
    grep -i "error.*docker" "$latest_log" | tail -10
fi

# Health check failures
if grep -q "Health check.*failed" "$latest_log"; then
    echo "✗ Health check failed"
    grep -i "health" "$latest_log" | tail -10
fi

# Step 3: Check Docker status
echo "\n=== Docker status ==="
docker-compose ps

# Step 4: Check recent container logs
echo "\n=== Recent container logs ==="
docker-compose logs --tail=50 oracle-blue oracle-green 2>/dev/null || echo "Containers not running"

# Step 5: Try to reproduce error
echo "\n=== Attempting to reproduce ==="

# Run health check manually
python3 deployment/health_check.py

# Run a test file that might have failed
# python3 test_oracle_integration.py

# Step 6: Check system resources
echo "\n=== System resources ==="
df -h | grep -E "Filesystem|/dev/"
free -h || vm_stat  # Linux or macOS
docker system df

# Step 7: Recommendations
echo "\n=== Recommendations ==="
echo "Common fixes:"
echo "  1. If tests failed: Fix failing tests, rerun"
echo "  2. If Docker build failed: Check Dockerfile syntax, rebuild"
echo "  3. If health check failed: Check database, restart services"
echo "  4. If disk space low: Clean up logs and old images"
echo "  5. If containers won't start: Check docker-compose.yml, check logs"
```

**Next Steps**:
- Fix identified issues
- Test fix in local environment
- Retry deployment

---

## Maintenance Tasks

### Runbook: Monthly Security Audit

**Duration**: 1 hour
**Frequency**: Monthly (first Monday)
**Prerequisites**: Access to security scanning tools

**Procedure**:

```bash
# Step 1: Dependency vulnerability scan
echo "=== Dependency Vulnerability Scan ==="
pip freeze | safety check --json > security_scan_$(date +%Y%m%d).json

# Step 2: Code security scan
echo "\n=== Code Security Scan ==="
bandit -r core/ -ll -f json -o bandit_scan_$(date +%Y%m%d).json

# Step 3: Review audit logs
echo "\n=== Audit Log Review ==="

# Check for failed auth attempts
grep "AUTH_FAILED" logs/audit.log | wc -l
echo "Failed auth attempts found: $?"

# Check for security-related events
grep -i "SECURITY" logs/audit.log | tail -20

# Step 4: Review access controls
echo "\n=== Access Control Review ==="
# List who has access
# Review role assignments
# Check for unused accounts

# Step 5: Check SSL/TLS certificates
echo "\n=== Certificate Check ==="
# Check Nginx certificates
if [ -f deployment/nginx/ssl/oracle.crt ]; then
    openssl x509 -in deployment/nginx/ssl/oracle.crt -noout -dates
else
    echo "⚠ No SSL certificate found"
fi

# Step 6: Generate security report
cat > security_reports/monthly_$(date +%Y%m).md << EOF
# Security Audit Report
Date: $(date)

## Vulnerability Scan
- Dependencies scanned: $(pip list | wc -l)
- Vulnerabilities found: [check safety output]

## Code Security
- Files scanned: $(find core/ -name "*.py" | wc -l)
- Issues found: [check bandit output]

## Audit Log Review
- Failed auth attempts: [count]
- Security events: [count]
- Unusual activity: [describe]

## Access Control
- Active users: [count]
- Roles reviewed: Yes/No
- Access changes: [list]

## Certificates
- SSL expiration: [date]
- Renewal needed: [yes/no]

## Recommendations
1. [recommendation]
2. [recommendation]

## Action Items
- [ ] Fix critical vulnerabilities
- [ ] Review access for inactive users
- [ ] Renew certificates if expiring < 30 days
- [ ] Update security documentation
EOF

echo "\n✓ Security audit complete"
echo "Report: security_reports/monthly_$(date +%Y%m).md"
```

**Follow-up Actions**:
- Fix any critical/high vulnerabilities
- Update dependencies with security patches
- Review and revoke unnecessary access
- Schedule certificate renewal if needed

---

## Quick Reference Card

### Emergency Contacts
- **On-Call Engineer**: [phone/pager]
- **Superman**: [contact]
- **Engineering Manager**: [contact]
- **Incident Hotline**: [number]

### Critical Commands

**Health Check**:
```bash
python3 deployment/health_check.py
```

**Agent Health**:
```python
from core.oracle_integration.superman_connector import get_superman_interface
connector = get_superman_interface()
health = connector.get_agent_health_summary()
print(f"Health: {health['health_percentage']:.1f}%")
```

**Emergency Rollback**:
```bash
./deployment/deploy.sh production --rollback --force
```

**System Restart**:
```bash
docker-compose restart oracle-blue oracle-green
```

**View Logs**:
```bash
tail -f logs/oracle.log
docker-compose logs -f oracle-blue
```

### Performance Targets
- Flash: < 1s (p95)
- Batman: < 2s (p95)
- Others: < 3s (p95)
- System Health: > 90%

### Escalation Thresholds
- P0: Immediate (complete outage)
- P1: 15 minutes (critical agent down)
- P2: 1 hour (degraded performance)
- P3: 4 hours (minor issues)

---

**Oracle says**: "Preparation prevents poor performance. Follow the runbook." 📘
