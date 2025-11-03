# 🔧 Oracle Troubleshooting Guide

**Week 13-14: Documentation & Training**
**Purpose**: Quick problem resolution for common Oracle issues
**Format**: Problem → Symptoms → Diagnosis → Solution

---

## Table of Contents

1. [Health & Monitoring Issues](#health--monitoring-issues)
2. [Deployment Issues](#deployment-issues)
3. [Version Control Issues](#version-control-issues)
4. [Database Issues](#database-issues)
5. [Performance Issues](#performance-issues)
6. [Integration Issues](#integration-issues)

---

## Health & Monitoring Issues

### Issue 1: Agent Shows Unhealthy But Seems Fine

**Symptoms**:
- Agent status: unhealthy or critical
- Agent functions normally when tested manually
- No obvious errors in logs
- Success rate looks reasonable

**Diagnosis**:
```python
from core.oracle_integration.superman_connector import get_superman_interface

connector = get_superman_interface()
health = connector.get_agent_health_summary()
agent_health = health['agents']['batman']  # Replace with your agent

print(f"Status: {agent_health['status']}")
print(f"Success Rate: {agent_health['metrics']['success_rate']:.1f}%")
print(f"Error Count: {agent_health['metrics']['error_count']}")
print(f"Last Error: {agent_health['metrics'].get('last_error', 'None')}")
print(f"Response Time (avg): {agent_health['metrics']['avg_response_time']:.0f}ms")
```

**Common Causes**:
1. **Stale metrics** - Metrics from old errors still affecting health score
2. **Strict thresholds** - Agent near threshold but functional
3. **Temporary glitches** - Brief errors counted heavily
4. **Incorrect health calc** - Bug in health calculation logic

**Solution 1: Request Self-Healing** (Clears error counts):
```python
healing = connector.request_self_healing('batman')
print(f"Fixes applied: {healing.get('fixes_applied', 0)}")

# Wait 5 minutes and re-check
import time
time.sleep(300)

health_after = connector.get_agent_health_summary()
print(f"Health now: {health_after['agents']['batman']['status']}")
```

**Solution 2: Manual Metric Reset** (If self-healing doesn't help):
```python
from core.oracle_self_healing.health_monitor import AgentHealthMonitor

monitor = AgentHealthMonitor()
# The health metrics will naturally improve as new successful operations occur
# Just ensure agent is working properly
```

**Prevention**:
- Monitor error rates regularly
- Set reasonable health thresholds
- Investigate errors promptly (don't let them accumulate)

---

### Issue 2: "Health Check Timeout" Error

**Symptoms**:
- `deployment/health_check.py` times out
- Takes >30 seconds to complete
- Some checks never finish
- Docker containers unresponsive

**Diagnosis**:
```bash
# Check if containers are running
docker-compose ps

# Check container resource usage
docker stats --no-stream

# Check system resources
free -h  # Linux
vm_stat  # macOS

# Check if database is locked
lsof oracle.db  # See if anyone has lock
```

**Common Causes**:
1. **Database locked** - Long-running query or transaction
2. **Out of memory** - System swapping heavily
3. **CPU pegged** - 100% CPU usage
4. **Network issues** - Can't reach containers
5. **Deadlock** - Process waiting on itself

**Solution 1: Restart Containers**:
```bash
docker-compose restart oracle-blue oracle-green
sleep 30
python3 deployment/health_check.py
```

**Solution 2: Kill Database Locks**:
```bash
# Find processes using database
lsof oracle.db

# Kill specific process if needed
# kill -9 [PID]

# Or restart everything
docker-compose down
sleep 5
docker-compose up -d
```

**Solution 3: Free Up Resources**:
```bash
# Clean up disk space
find logs/ -name "*.log" -mtime +7 -delete

# Clean Docker images
docker system prune -f

# Check resources after cleanup
df -h
free -h
```

**Prevention**:
- Monitor system resources
- Set up alerts for high CPU/memory
- Implement database connection pooling
- Use timeouts on all database operations

---

### Issue 3: Grafana Dashboards Show No Data

**Symptoms**:
- Grafana dashboards empty or showing "No data"
- Prometheus is running
- Oracle is healthy
- Metrics endpoint returns data when checked manually

**Diagnosis**:
```bash
# Check if Prometheus is scraping
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health}'

# Check if metrics endpoint is accessible
curl http://localhost:8000/metrics  # Or container IP

# Check Grafana datasource
curl http://localhost:3000/api/datasources
```

**Common Causes**:
1. **Prometheus not scraping** - Wrong target configuration
2. **Network isolation** - Containers can't reach each other
3. **Metrics not exposed** - Oracle not exposing /metrics endpoint
4. **Datasource misconfigured** - Grafana can't reach Prometheus

**Solution 1: Fix Prometheus Scraping**:
```yaml
# Check deployment/monitoring/prometheus.yml
scrape_configs:
  - job_name: 'oracle-blue'
    static_configs:
      - targets: ['oracle-blue:8000']  # Must match container name

  - job_name: 'oracle-green'
    static_configs:
      - targets: ['oracle-green:8000']
```

**Solution 2: Verify Network Connectivity**:
```bash
# Test from Prometheus container to Oracle
docker-compose exec prometheus wget -O- http://oracle-blue:8000/metrics

# Should return metrics in Prometheus format
```

**Solution 3: Reconfigure Grafana Datasource**:
```bash
# Grafana UI: Configuration > Data Sources > Prometheus
# URL should be: http://prometheus:9090
# Access: Server (default)
# Click "Save & Test"
```

**Prevention**:
- Test monitoring setup after deployment
- Monitor Prometheus scrape success rate
- Set up alerts for scraping failures
- Document network topology

---

## Deployment Issues

### Issue 4: Deployment Fails with "Test Suite Failed"

**Symptoms**:
- `./deployment/deploy.sh` stops during test phase
- Error message: "Some test suites failed"
- Specific test file(s) failing
- Deployment rolls back automatically

**Diagnosis**:
```bash
# Check which tests failed
cat deployment/logs/deployment_*.log | grep -A 5 "FAILED"

# Run tests manually to see detailed errors
python3 test_oracle_integration.py
# Or whichever test failed

# Check recent code changes
git log --oneline -10
git diff HEAD~1
```

**Common Causes**:
1. **Recent code changes broke tests** - Bug introduced
2. **Database state issue** - Tests expect clean state
3. **Missing dependencies** - Package not installed
4. **Environment differences** - Works locally, fails in CI
5. **Flaky tests** - Intermittent failures

**Solution 1: Fix Failing Tests**:
```bash
# Run specific failing test
python3 test_oracle_integration.py

# Read error messages carefully
# Fix the underlying issue
# Re-run to verify

# Then retry deployment
./deployment/deploy.sh staging
```

**Solution 2: Reset Database (if state issue)**:
```bash
# Backup current database
cp oracle.db oracle_backup_$(date +%Y%m%d).db

# Start fresh or restore clean state
# rm oracle.db  # Caution: only in staging!
# Then re-run deployment
```

**Solution 3: Skip Tests (EMERGENCY ONLY)**:
```bash
# Only use in emergency, never in production
./deployment/deploy.sh staging --skip-tests

# BUT YOU MUST:
# 1. Create ticket to fix tests
# 2. Manually verify functionality
# 3. Fix tests before next deployment
```

**Prevention**:
- Run tests locally before pushing code
- Set up pre-commit hooks to run tests
- Keep test database in clean state
- Fix flaky tests immediately

---

### Issue 5: Blue-Green Deployment Health Check Fails

**Symptoms**:
- Deployment starts new environment (blue or green)
- New environment fails health check
- Error: "Health check timeout after 300s"
- Deployment automatically rolls back

**Diagnosis**:
```bash
# Check logs from failed environment
docker-compose logs oracle-green  # Or oracle-blue

# Run health check manually
docker-compose exec oracle-green python3 /app/deployment/health_check.py

# Check if services started
docker-compose ps

# Check if database accessible
docker-compose exec oracle-green ls -lh /app/data/oracle.db
```

**Common Causes**:
1. **Database not mounted** - Volume mount issue
2. **Import errors** - Missing Python packages
3. **Port conflict** - Port already in use
4. **Configuration error** - Environment variables wrong
5. **Resource limits** - Not enough memory/CPU

**Solution 1: Check Logs for Errors**:
```bash
# Look for Python errors
docker-compose logs oracle-green 2>&1 | grep -i error

# Look for import errors
docker-compose logs oracle-green 2>&1 | grep -i "importerror\|modulenotfounderror"

# Fix identified issues and redeploy
```

**Solution 2: Verify Volume Mounts**:
```bash
# Check docker-compose.yml volumes section
cat deployment/docker-compose.yml | grep -A 5 "volumes:"

# Verify volumes exist
docker volume ls | grep oracle

# Recreate volumes if needed
docker-compose down -v
docker-compose up -d
```

**Solution 3: Check Resource Limits**:
```bash
# Check if container OOMed (Out of Memory)
docker inspect oracle-green | grep -i oom

# Increase memory limit in docker-compose.yml if needed
# Under oracle-green service:
# deploy:
#   resources:
#     limits:
#       memory: 2G  # Increase this
```

**Prevention**:
- Test Docker builds locally
- Monitor container resource usage
- Set appropriate resource limits
- Validate configuration before deployment

---

## Version Control Issues

### Issue 6: "Circular Dependency Detected" Error

**Symptoms**:
- Version update fails with circular dependency error
- Dependency graph shows cycle
- Update coordination fails
- Error message lists dependency chain

**Diagnosis**:
```python
from core.oracle_integration.superman_connector import get_superman_interface

connector = get_superman_interface()
graph = connector.get_dependency_graph()

if graph['has_circular_dependencies']:
    print("Circular dependency chains:")
    for chain in graph['circular_chains']:
        print(f"  {' → '.join(chain)}")

# Identify which dependencies to break
```

**Common Causes**:
1. **Mutual dependencies** - A depends on B, B depends on A
2. **Transitive cycle** - A → B → C → A
3. **Incorrect dependency** - Dependency shouldn't exist
4. **Legacy dependency** - Old, unnecessary dependency

**Solution 1: Remove Unnecessary Dependency**:
```python
from core.oracle_version_control.dependency_tracker import DependencyTracker

tracker = DependencyTracker()

# Example: Break A → B → C → A cycle by removing C → A
tracker.remove_dependency('agent_c', 'agent_a')

# Verify circle broken
graph_after = connector.get_dependency_graph()
assert not graph_after['has_circular_dependencies'], "Still has cycles"
print("✓ Circular dependency resolved")
```

**Solution 2: Refactor Dependency Structure**:
```python
# If dependency is legitimate, refactor to remove cycle
# Example: Extract shared functionality to new agent

# Before: A ← → B (mutual dependency)
# After:  A → Common ← B (both depend on shared component)

# This requires code changes and new agent creation
```

**Prevention**:
- Review dependencies before adding
- Use dependency diagram tools
- Enforce acyclic architecture
- Regular dependency audits

---

### Issue 7: Version Rollback Fails with "No Backup Found"

**Symptoms**:
- Rollback command fails
- Error: "Backup file not found"
- `rollback_version()` returns error
- No backup in backups directory

**Diagnosis**:
```bash
# Check if backups exist
ls -lh backups/

# Check git history (if git integration enabled)
git log --oneline

# Check version history in database
python3 -c "
from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl
vc = EnhancedVersionControl()
history = vc.get_version_history('batman')
print('Version history:', history)
"
```

**Common Causes**:
1. **Backups not created** - Backup feature disabled
2. **Backups deleted** - Manual cleanup removed backups
3. **Wrong backup location** - Looking in wrong directory
4. **Git not initialized** - Git integration not working

**Solution 1: Use Force Rollback** (If you know previous version):
```python
from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl

vc = EnhancedVersionControl()

# Force rollback without backup (RISKY!)
result = vc.rollback_version(
    agent_name='batman',
    target_version='1.0.0',
    force=True  # Skip backup check
)

# ⚠️ This may fail if code has breaking changes
```

**Solution 2: Restore from Git**:
```bash
# If git integration enabled
git log --oneline --all | grep batman

# Checkout previous version
git checkout <commit-hash> -- core/justice_league/batman.py

# Then update version in Oracle
python3 -c "
from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl
vc = EnhancedVersionControl()
# Create version with restored code
"
```

**Solution 3: Manual Code Restoration**:
```bash
# If you have code backup elsewhere
# Copy previous version of agent code
# Update version in database manually
```

**Prevention**:
- Enable backup creation on version updates
- Enable git integration
- Verify backups are being created
- Don't manually delete recent backups
- Test rollback capability monthly

---

## Database Issues

### Issue 8: "Database Is Locked" Error

**Symptoms**:
- Operations fail with "database is locked"
- SQLite error code 5
- Health check fails on database check
- Can't write to database

**Diagnosis**:
```bash
# Check if database file exists
ls -lh oracle.db

# Check who has database open
lsof oracle.db

# Check for lingering connections
ps aux | grep oracle

# Check if database is in WAL mode
sqlite3 oracle.db "PRAGMA journal_mode;"
```

**Common Causes**:
1. **Multiple writers** - Two processes writing simultaneously
2. **Long transaction** - Transaction not committed
3. **Crashed process** - Lock file left behind
4. **Network filesystem** - SQLite on NFS (not supported)

**Solution 1: Close All Connections**:
```bash
# Kill processes using database
lsof oracle.db | awk '{print $2}' | tail -n +2 | xargs kill

# Remove lock files
rm oracle.db-shm oracle.db-wal 2>/dev/null || true

# Restart Oracle
docker-compose restart oracle-blue oracle-green
```

**Solution 2: Enable WAL Mode** (Better concurrency):
```bash
# Set journal mode to WAL
sqlite3 oracle.db "PRAGMA journal_mode=WAL;"
sqlite3 oracle.db "PRAGMA journal_mode;"
# Should return: wal

# WAL mode allows multiple readers with one writer
```

**Solution 3: Increase Timeout**:
```python
# In code, increase database timeout
import sqlite3
conn = sqlite3.connect('oracle.db', timeout=30.0)  # 30 second timeout
```

**Prevention**:
- Use WAL mode for better concurrency
- Close database connections promptly
- Use context managers (with statements)
- Avoid long-running transactions
- Consider migrating to PostgreSQL for production

---

### Issue 9: Database Corrupted

**Symptoms**:
- "database disk image is malformed" error
- Integrity check fails
- Can't open database
- Health check fails

**Diagnosis**:
```bash
# Check database integrity
sqlite3 oracle.db "PRAGMA integrity_check;"

# Should return: ok
# If returns errors, database is corrupted

# Check database file
file oracle.db

# Check file size (should be > 0)
ls -lh oracle.db
```

**Common Causes**:
1. **Disk full during write** - Partial write left corruption
2. **Power failure** - Database not synced to disk
3. **Hardware failure** - Disk error
4. **Process killed mid-write** - Force killed during transaction

**Solution 1: Restore from Backup**:
```bash
# Stop Oracle
docker-compose stop oracle-blue oracle-green

# Backup corrupted database (for analysis)
mv oracle.db oracle_corrupted_$(date +%Y%m%d).db

# Restore latest backup
cp deployment/backups/production/oracle_backup_latest.db oracle.db

# Verify restored database
sqlite3 oracle.db "PRAGMA integrity_check;"

# Restart Oracle
docker-compose up -d oracle-blue
sleep 30
python3 deployment/health_check.py
```

**Solution 2: Attempt Repair** (If no recent backup):
```bash
# Dump what you can from corrupted database
sqlite3 oracle.db ".recover" > recovered.sql

# Create new database from dump
rm oracle.db
sqlite3 oracle.db < recovered.sql

# Check integrity
sqlite3 oracle.db "PRAGMA integrity_check;"

# If ok, restart Oracle
```

**Solution 3: Start Fresh** (LAST RESORT):
```bash
# Backup corrupted database
mv oracle.db oracle_corrupted_$(date +%Y%m%d).db

# Oracle will create new database on startup
docker-compose restart oracle-blue

# All agent history lost - will rebuild
```

**Prevention**:
- Regular automated backups
- Use WAL mode
- Don't kill processes forcefully
- Monitor disk space
- Consider RAID for disk redundancy
- Migrate to PostgreSQL for production

---

## Performance Issues

### Issue 10: Slow Response Times (Agent P95 > Target)

**Symptoms**:
- Agent response times higher than target
- P95/P99 metrics elevated
- Grafana shows response time spike
- Users report slowness

**Diagnosis**:
```python
from core.oracle_integration.superman_connector import get_superman_interface

connector = get_superman_interface()
health = connector.get_agent_health_summary()

# Check all agents
for agent, info in health['agents'].items():
    metrics = info['metrics']
    p95 = metrics.get('p95_response_time', 0)

    # Check against targets
    if agent == 'flash' and p95 > 1000:  # Flash: 1s target
        print(f"⚠ {agent}: {p95:.0f}ms (target: 1000ms)")
    elif agent == 'batman' and p95 > 2000:  # Batman: 2s target
        print(f"⚠ {agent}: {p95:.0f}ms (target: 2000ms)")
    elif p95 > 3000:  # Others: 3s target
        print(f"⚠ {agent}: {p95:.0f}ms (target: 3000ms)")
```

**Common Causes**:
1. **Database queries slow** - Needs optimization/indexing
2. **External API slow** - Dependent service degraded
3. **CPU/memory constrained** - Not enough resources
4. **Code inefficiency** - Algorithm problem
5. **Network latency** - Container network issues

**Solution 1: Optimize Database Queries**:
```bash
# Analyze slow queries
sqlite3 oracle.db ".timer on"
sqlite3 oracle.db "EXPLAIN QUERY PLAN SELECT * FROM health_metrics WHERE agent_name='batman';"

# Add indexes if needed
sqlite3 oracle.db "CREATE INDEX IF NOT EXISTS idx_health_agent ON health_metrics(agent_name);"

# Vacuum database
sqlite3 oracle.db "VACUUM;"
```

**Solution 2: Increase Resources**:
```yaml
# In docker-compose.yml, increase limits
services:
  oracle-blue:
    deploy:
      resources:
        limits:
          cpus: '2.0'      # Increase from 1.0
          memory: 4G       # Increase from 2G
```

**Solution 3: Profile Code**:
```python
# Add timing to agent code
import time

start = time.time()
# ... agent operation ...
elapsed = (time.time() - start) * 1000
print(f"Operation took: {elapsed:.0f}ms")

# Identify slow operations and optimize
```

**Prevention**:
- Regular performance testing
- Monitor response time trends
- Optimize database regularly
- Set up performance alerts
- Code review for performance

---

## Integration Issues

### Issue 11: Superman Connector Returns "Connection Refused"

**Symptoms**:
- `get_superman_interface()` fails
- "Connection refused" error
- Can't access Oracle from Superman
- Heartbeat fails

**Diagnosis**:
```python
# Try to create connector
try:
    from core.oracle_integration.superman_connector import get_superman_interface
    connector = get_superman_interface()
    heartbeat = connector.heartbeat()
    print(f"Status: {heartbeat.get('status')}")
except Exception as e:
    print(f"Error: {e}")

# Check if Oracle is running
import subprocess
subprocess.run(["docker-compose", "ps"])
```

**Common Causes**:
1. **Oracle not running** - Containers stopped
2. **Wrong host/port** - Configuration issue
3. **Firewall blocking** - Network security
4. **Container network issue** - Docker network down

**Solution 1: Start Oracle**:
```bash
# Check if Oracle running
docker-compose ps

# If not running, start it
docker-compose up -d oracle-blue

# Wait for startup
sleep 30

# Test connection
python3 -c "
from core.oracle_integration.superman_connector import get_superman_interface
connector = get_superman_interface()
print(connector.heartbeat())
"
```

**Solution 2: Check Configuration**:
```bash
# Verify environment variables
cat deployment/config/production.env | grep -i host

# Verify docker-compose network
docker network ls | grep oracle
```

**Solution 3: Restart Networking**:
```bash
# Restart Docker networking
docker-compose down
docker network prune -f
docker-compose up -d
```

**Prevention**:
- Monitor Oracle uptime
- Set up connection health checks
- Document connection configuration
- Use service discovery in production

---

## Quick Diagnostic Commands

### Check Overall System Health
```bash
python3 deployment/health_check.py && echo "✅ Healthy" || echo "❌ Unhealthy"
```

### Get Agent Health Percentage
```python
from core.oracle_integration.superman_connector import get_superman_interface
connector = get_superman_interface()
health = connector.get_agent_health_summary()
print(f"{health['health_percentage']:.1f}%")
```

### Check for Critical Alerts
```python
from core.oracle_integration.oracle_coordinator import OracleCoordinator
coordinator = OracleCoordinator()
alerts = coordinator.get_pending_alerts()
critical = [a for a in alerts.get('alerts', []) if a['severity'] == 'critical']
print(f"{len(critical)} critical alerts")
```

### Check Database Integrity
```bash
sqlite3 oracle.db "PRAGMA integrity_check;" | grep -q "ok" && echo "✅ DB OK" || echo "❌ DB Corrupted"
```

### Check Docker Containers
```bash
docker-compose ps --format="table {{.Service}}\t{{.Status}}\t{{.Ports}}"
```

### Check Disk Space
```bash
df -h / | awk 'NR==2 {print "Free: " $4 " (" $5 " used)"}'
```

### Check Recent Errors
```bash
tail -100 logs/oracle.log | grep -i error | tail -10
```

---

## Escalation Decision Tree

```
Issue Occurred
      │
      ├─ Can you identify the cause? ────No───┐
      │                                        │
      Yes                                      │
      │                                        ▼
      ├─ Is there a solution in this guide? ──────────> Try solution
      │          │                             │
      │         No                             ▼
      │          │                      Solution worked?
      │          │                             │
      │          │                        No───┤───Yes──> Document and close
      │          │                             │
      │          └─────────────────────────────┘
      ▼
Escalate to Superman
```

**Escalate immediately if**:
- P0 incident (complete outage)
- Database corrupted and no backup
- Security breach suspected
- Unable to resolve within SLA time
- Multiple systems affected

---

**Oracle says**: "Most problems have been solved before. Check the guide first." 🔧
