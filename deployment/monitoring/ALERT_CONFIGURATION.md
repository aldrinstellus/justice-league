# 🚨 Oracle Alert Configuration Guide

**Version**: 1.0.0
**Purpose**: Configure Prometheus alerts and notification channels for Oracle monitoring
**Time Required**: 30-45 minutes

---

## Overview

This guide covers configuring alerts for Oracle production monitoring. Alerts notify operators of issues before they become critical, enabling proactive problem resolution.

---

## Alert Architecture

```
┌─────────────┐     ┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Prometheus │────▶│ Alert Rules │────▶│ Alertmanager │────▶│ Destinations │
│  (Metrics)  │     │  (Evaluate) │     │  (Route/     │     │ Email/Slack/ │
│             │     │             │     │   Group)     │     │ PagerDuty    │
└─────────────┘     └─────────────┘     └──────────────┘     └──────────────┘
```

---

## Prerequisites

- Prometheus running (`docker-compose up prometheus`)
- Alertmanager running (`docker-compose up alertmanager`)
- Email/Slack/PagerDuty credentials available

---

## Step 1: Configure Alert Rules

### Location
`deployment/monitoring/alert_rules.yml`

### Core Alert Rules (Already Configured)

#### 1. Agent Health Alert
```yaml
- alert: AgentUnhealthy
  expr: oracle_agent_health < 70
  for: 5m
  labels:
    severity: warning
    component: agent
  annotations:
    summary: "Agent {{ $labels.agent }} is unhealthy"
    description: "Agent {{ $labels.agent }} health is {{ $value }}% (threshold: 70%)"
    runbook: "See TROUBLESHOOTING_GUIDE.md - Agent Not Responding"
```

**Triggers when**: Any agent health below 70% for 5+ minutes
**Action**: Check agent logs, review recent changes

---

#### 2. Agent Critical Alert
```yaml
- alert: AgentCritical
  expr: oracle_agent_health < 50
  for: 2m
  labels:
    severity: critical
    component: agent
  annotations:
    summary: "Agent {{ $labels.agent }} is CRITICAL"
    description: "Agent {{ $labels.agent }} health is {{ $value }}% (threshold: 50%)"
    runbook: "IMMEDIATE ACTION REQUIRED - Follow Agent Critical Runbook"
```

**Triggers when**: Any agent health below 50% for 2+ minutes
**Action**: Immediate investigation, potential rollback

---

#### 3. System Health Alert
```yaml
- alert: SystemHealthLow
  expr: avg(oracle_agent_health) < 90
  for: 10m
  labels:
    severity: warning
    component: system
  annotations:
    summary: "Overall system health is low"
    description: "System health is {{ $value }}% (threshold: 90%)"
    runbook: "See TROUBLESHOOTING_GUIDE.md - Multiple Agents Unhealthy"
```

**Triggers when**: Average system health below 90% for 10+ minutes
**Action**: Check for systemic issues (database, disk, memory)

---

#### 4. High Error Rate Alert
```yaml
- alert: HighErrorRate
  expr: rate(oracle_errors_total[5m]) > 10
  for: 5m
  labels:
    severity: critical
    component: system
  annotations:
    summary: "High error rate detected"
    description: "Error rate is {{ $value }} errors/sec (threshold: 10/sec)"
    runbook: "Check recent changes, consider rollback"
```

**Triggers when**: More than 10 errors/second for 5+ minutes
**Action**: Check error logs, recent deployments, consider rollback

---

#### 5. Slow Response Time Alert
```yaml
- alert: SlowResponseTime
  expr: histogram_quantile(0.95, rate(oracle_operation_duration_seconds_bucket[5m])) > 1
  for: 10m
  labels:
    severity: warning
    component: performance
  annotations:
    summary: "Slow response times detected"
    description: "P95 response time is {{ $value }}s (threshold: 1s)"
    runbook: "Check database performance, system resources"
```

**Triggers when**: P95 response time exceeds 1 second for 10+ minutes
**Action**: Check database size, query performance, system resources

---

#### 6. Database Size Alert
```yaml
- alert: DatabaseSizeHigh
  expr: oracle_database_size_bytes > 1000000000
  for: 5m
  labels:
    severity: warning
    component: database
  annotations:
    summary: "Database size is growing large"
    description: "Database is {{ $value | humanize1024 }}B (threshold: 1GB)"
    runbook: "Review data retention policy, archive old data"
```

**Triggers when**: Database exceeds 1GB for 5+ minutes
**Action**: Review retention policy, archive historical data

---

#### 7. Disk Space Alert
```yaml
- alert: DiskSpaceLow
  expr: node_filesystem_avail_bytes{mountpoint="/"} < 1000000000
  for: 5m
  labels:
    severity: critical
    component: infrastructure
  annotations:
    summary: "Disk space critically low"
    description: "Only {{ $value | humanize1024 }}B free (threshold: 1GB)"
    runbook: "Free disk space immediately - cleanup logs, archives"
```

**Triggers when**: Less than 1GB free disk space for 5+ minutes
**Action**: Clean up logs, rotate backups, free space immediately

---

#### 8. Memory High Alert
```yaml
- alert: MemoryHigh
  expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes > 0.9
  for: 10m
  labels:
    severity: warning
    component: infrastructure
  annotations:
    summary: "Memory usage is high"
    description: "Memory usage is {{ $value | humanizePercentage }} (threshold: 90%)"
    runbook: "Check for memory leaks, restart services if needed"
```

**Triggers when**: Memory usage exceeds 90% for 10+ minutes
**Action**: Check for memory leaks, consider service restart

---

#### 9. Service Down Alert
```yaml
- alert: OracleServiceDown
  expr: up{job="oracle"} == 0
  for: 1m
  labels:
    severity: critical
    component: system
  annotations:
    summary: "Oracle service is down"
    description: "Oracle has been down for 1+ minutes"
    runbook: "IMMEDIATE ACTION - Check service status, restart if needed"
```

**Triggers when**: Oracle service unreachable for 1+ minute
**Action**: Immediate investigation and restart

---

#### 10. Backup Failed Alert
```yaml
- alert: BackupFailed
  expr: oracle_backup_last_success_timestamp < time() - 172800
  for: 5m
  labels:
    severity: warning
    component: backup
  annotations:
    summary: "Backup has not succeeded recently"
    description: "Last successful backup was {{ $value | humanizeDuration }} ago (threshold: 48h)"
    runbook: "Check backup logs, verify backup system operational"
```

**Triggers when**: No successful backup in 48+ hours
**Action**: Check backup logs, verify backup system

---

### Custom Alert Rules

Add custom rules to `deployment/monitoring/alert_rules.yml`:

```yaml
groups:
  - name: oracle_custom_alerts
    rules:
      # Add your custom alerts here
      - alert: YourCustomAlert
        expr: your_metric > threshold
        for: duration
        labels:
          severity: warning|critical
          component: system|agent|infrastructure
        annotations:
          summary: "Brief description"
          description: "Detailed description with {{ $value }}"
          runbook: "Link to runbook or procedure"
```

---

## Step 2: Configure Alertmanager

### Location
`deployment/monitoring/alertmanager.yml`

### Basic Configuration

```yaml
global:
  # Global settings
  resolve_timeout: 5m

# Alert routing
route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'default'

  # Route critical alerts differently
  routes:
    - match:
        severity: critical
      receiver: 'critical-alerts'
      continue: true

    - match:
        severity: warning
      receiver: 'warning-alerts'

# Inhibition rules (suppress alerts)
inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'agent']

# Notification receivers
receivers:
  - name: 'default'
    # Configure default receiver

  - name: 'critical-alerts'
    # Configure critical alert destinations

  - name: 'warning-alerts'
    # Configure warning alert destinations
```

---

## Step 3: Configure Notification Channels

### Option 1: Email Notifications

#### Configure Email Receiver

Edit `deployment/monitoring/alertmanager.yml`:

```yaml
receivers:
  - name: 'email-alerts'
    email_configs:
      - to: 'oracle-ops@example.com'
        from: 'oracle-alerts@example.com'
        smarthost: 'smtp.example.com:587'
        auth_username: 'oracle-alerts@example.com'
        auth_password: 'your-email-password'
        headers:
          Subject: '🚨 [{{ .Status | toUpper }}] Oracle Alert: {{ .GroupLabels.alertname }}'
        html: |
          <!DOCTYPE html>
          <html>
          <body>
            <h2>Oracle Alert</h2>
            <p><strong>Status:</strong> {{ .Status }}</p>
            <p><strong>Severity:</strong> {{ .GroupLabels.severity }}</p>
            {{ range .Alerts }}
            <hr>
            <p><strong>Alert:</strong> {{ .Labels.alertname }}</p>
            <p><strong>Description:</strong> {{ .Annotations.description }}</p>
            <p><strong>Runbook:</strong> {{ .Annotations.runbook }}</p>
            {{ end }}
          </body>
          </html>
```

#### Email Configuration Options

**Gmail**:
```yaml
smarthost: 'smtp.gmail.com:587'
auth_username: 'your-email@gmail.com'
auth_password: 'your-app-password'  # Use app password, not regular password
```

**SendGrid**:
```yaml
smarthost: 'smtp.sendgrid.net:587'
auth_username: 'apikey'
auth_password: 'your-sendgrid-api-key'
```

**AWS SES**:
```yaml
smarthost: 'email-smtp.us-east-1.amazonaws.com:587'
auth_username: 'your-ses-smtp-username'
auth_password: 'your-ses-smtp-password'
```

---

### Option 2: Slack Notifications

#### Step 1: Create Slack Webhook

1. Go to https://api.slack.com/apps
2. Create new app → From scratch
3. Name: "Oracle Alerts"
4. Choose your workspace
5. Add features → Incoming Webhooks
6. Activate Incoming Webhooks
7. Add New Webhook to Workspace
8. Choose channel (e.g., #oracle-alerts)
9. Copy webhook URL

#### Step 2: Configure Slack Receiver

Edit `deployment/monitoring/alertmanager.yml`:

```yaml
receivers:
  - name: 'slack-alerts'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
        channel: '#oracle-alerts'
        username: 'Oracle Alertmanager'
        icon_emoji: ':robot_face:'
        title: '🚨 {{ .Status | toUpper }} - {{ .GroupLabels.alertname }}'
        text: |
          *Severity:* {{ .GroupLabels.severity }}
          *Component:* {{ .GroupLabels.component }}
          {{ range .Alerts }}
          *Description:* {{ .Annotations.description }}
          *Runbook:* {{ .Annotations.runbook }}
          {{ end }}
```

#### Slack Color Coding

```yaml
slack_configs:
  - api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
    channel: '#oracle-alerts'
    color: '{{ if eq .Status "firing" }}{{ if eq .GroupLabels.severity "critical" }}danger{{ else }}warning{{ end }}{{ else }}good{{ end }}'
```

---

### Option 3: PagerDuty Notifications

#### Step 1: Create PagerDuty Service

1. Login to PagerDuty
2. Services → New Service
3. Name: "Oracle Production"
4. Escalation Policy: Choose or create
5. Integration: Events API v2
6. Create service
7. Copy Integration Key

#### Step 2: Configure PagerDuty Receiver

Edit `deployment/monitoring/alertmanager.yml`:

```yaml
receivers:
  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: 'your-pagerduty-integration-key'
        severity: '{{ .GroupLabels.severity }}'
        description: '{{ .GroupLabels.alertname }}: {{ .Annotations.summary }}'
        details:
          firing: '{{ .Alerts.Firing | len }}'
          resolved: '{{ .Alerts.Resolved | len }}'
          description: '{{ .Annotations.description }}'
          runbook: '{{ .Annotations.runbook }}'
```

---

### Option 4: Microsoft Teams Notifications

#### Step 1: Create Teams Webhook

1. Open Microsoft Teams
2. Go to desired channel
3. Click "..." → Connectors
4. Search "Incoming Webhook"
5. Configure → Name: "Oracle Alerts"
6. Copy webhook URL

#### Step 2: Configure Teams via Webhook (Custom)

```yaml
receivers:
  - name: 'teams-alerts'
    webhook_configs:
      - url: 'https://outlook.office.com/webhook/YOUR-WEBHOOK-URL'
        send_resolved: true
        http_config:
          bearer_token: 'optional-bearer-token'
```

---

## Step 4: Alert Routing Strategy

### Recommended Routing Configuration

```yaml
route:
  group_by: ['alertname', 'agent']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'default'

  routes:
    # Critical alerts → PagerDuty + Slack
    - match:
        severity: critical
      receiver: 'critical-pagerduty'
      continue: true
      repeat_interval: 5m

    - match:
        severity: critical
      receiver: 'critical-slack'
      continue: false

    # Warning alerts → Slack only
    - match:
        severity: warning
      receiver: 'warning-slack'
      repeat_interval: 1h

    # Business hours only (9 AM - 6 PM weekdays)
    - match:
        severity: info
      receiver: 'business-hours-email'
      active_time_intervals:
        - business_hours

# Time intervals
time_intervals:
  - name: business_hours
    time_intervals:
      - times:
          - start_time: '09:00'
            end_time: '18:00'
        weekdays: ['monday:friday']
```

---

## Step 5: Alert Grouping and Throttling

### Grouping Strategy

```yaml
route:
  # Group alerts by alert name and agent
  group_by: ['alertname', 'agent']

  # Wait 10s before sending first alert (collect multiple)
  group_wait: 10s

  # Send updates every 10s if new alerts arrive
  group_interval: 10s

  # Don't repeat alerts more than once per 12 hours
  repeat_interval: 12h
```

### Inhibition Rules

Suppress lower-severity alerts when higher-severity alerts are firing:

```yaml
inhibit_rules:
  # If agent is critical, suppress warning for same agent
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['agent']

  # If system is down, suppress all other alerts
  - source_match:
      alertname: 'OracleServiceDown'
    target_match_re:
      alertname: '.*'
```

---

## Step 6: Testing Alerts

### Test Alert Rules

```bash
# Validate alert rules syntax
docker-compose -f deployment/docker-compose.yml exec prometheus \
  promtool check rules /etc/prometheus/alert_rules.yml

# Should output: SUCCESS
```

### Test Alertmanager Config

```bash
# Validate alertmanager config
docker-compose -f deployment/docker-compose.yml exec alertmanager \
  amtool check-config /etc/alertmanager/alertmanager.yml

# Should output: Checking '/etc/alertmanager/alertmanager.yml'  SUCCESS
```

### Send Test Alert

```bash
# Send test alert to Alertmanager
curl -XPOST http://localhost:9093/api/v1/alerts -d '[
  {
    "labels": {
      "alertname": "TestAlert",
      "severity": "warning",
      "component": "test"
    },
    "annotations": {
      "summary": "This is a test alert",
      "description": "Testing Oracle alert configuration"
    },
    "startsAt": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'",
    "endsAt": "'"$(date -u -d '+5 minutes' +%Y-%m-%dT%H:%M:%SZ)"'"
  }
]'
```

### Verify Alert Reception

1. **Slack**: Check #oracle-alerts channel for test message
2. **Email**: Check oracle-ops@example.com inbox
3. **PagerDuty**: Check incidents list
4. **Alertmanager UI**: Visit http://localhost:9093

---

## Step 7: Alert Silencing

### Silence Alerts During Maintenance

```bash
# Silence all alerts for 1 hour
amtool silence add alertname=~ '.*' \
  --comment="Scheduled maintenance" \
  --duration=1h \
  --author="operator@example.com"

# Silence specific alert
amtool silence add alertname="AgentUnhealthy" agent="Batman" \
  --comment="Known issue, investigating" \
  --duration=2h \
  --author="operator@example.com"

# List active silences
amtool silence query

# Delete silence
amtool silence expire <silence-id>
```

### Silence via Alertmanager UI

1. Visit http://localhost:9093
2. Click "Silences" tab
3. Click "New Silence"
4. Fill in matchers (e.g., `alertname="AgentUnhealthy"`)
5. Set duration and comment
6. Click "Create"

---

## Step 8: Alert Dashboard

### Grafana Alert Dashboard

1. Login to Grafana: http://localhost:3000
2. Import dashboard ID: 11098 (Alertmanager Dashboard)
3. View active alerts, silences, and alert history

### Key Metrics to Monitor

- **Active Alerts**: Number of currently firing alerts
- **Alert Rate**: Alerts firing per hour
- **Notification Success Rate**: % of successful notifications
- **Silenced Alerts**: Number of silenced alerts

---

## Alert Escalation Matrix

| Severity | Initial Response | Escalation (15 min) | Escalation (30 min) | Escalation (60 min) |
|----------|------------------|---------------------|---------------------|---------------------|
| **Critical** | On-Call Engineer | Backup On-Call | Engineering Manager | CTO |
| **Warning** | On-Call Engineer | - | Backup On-Call | Engineering Manager |
| **Info** | Team Slack | - | - | - |

---

## Best Practices

### 1. Alert Fatigue Prevention
- ✅ Set appropriate thresholds (not too sensitive)
- ✅ Use `for: duration` to avoid flapping alerts
- ✅ Group related alerts
- ✅ Inhibit lower-severity alerts when higher-severity fires

### 2. Actionable Alerts
- ✅ Every alert should have a runbook link
- ✅ Include metric values in descriptions
- ✅ Clear summary of what's wrong
- ✅ Next steps or investigation hints

### 3. Testing
- ✅ Test each notification channel monthly
- ✅ Validate alert rules after changes
- ✅ Run fire drills for critical alerts

### 4. Documentation
- ✅ Document all alert escalation paths
- ✅ Keep runbooks up-to-date
- ✅ Document silencing procedures

### 5. Review
- ✅ Review alert effectiveness quarterly
- ✅ Tune thresholds based on actual incidents
- ✅ Remove or adjust noisy alerts

---

## Troubleshooting

### Issue 1: Alerts Not Firing

**Check**:
```bash
# Verify Prometheus is evaluating rules
curl http://localhost:9090/api/v1/rules | jq .

# Check alert state
curl http://localhost:9090/api/v1/alerts | jq .
```

**Solution**: Verify metrics exist and threshold is correct

---

### Issue 2: Notifications Not Received

**Check**:
```bash
# Check Alertmanager logs
docker-compose -f deployment/docker-compose.yml logs alertmanager

# Verify receiver configuration
amtool config routes
```

**Solution**: Check receiver credentials, network connectivity

---

### Issue 3: Too Many Alerts

**Solution**:
- Increase alert duration threshold
- Adjust metric thresholds
- Enable inhibition rules
- Group related alerts

---

### Issue 4: Alerts Flapping

**Solution**:
```yaml
# Increase "for" duration
- alert: ExampleAlert
  expr: metric > threshold
  for: 10m  # Increase from 5m to 10m
```

---

## Monitoring Checklist

### Pre-Production Checklist

- [ ] Alert rules created and validated
- [ ] Alertmanager configured with notification channels
- [ ] Test alerts sent and received successfully
- [ ] Alert routing configured appropriately
- [ ] Inhibition rules configured
- [ ] Silencing procedures documented
- [ ] Escalation matrix defined and communicated
- [ ] Grafana dashboards imported
- [ ] Alert documentation complete
- [ ] Team trained on alert response

---

## Production Verification

```bash
# Run verification script
./deployment/monitoring/verify_alerts.sh
```

Or manually:

```bash
echo "=== Alert Configuration Verification ==="
echo ""

# 1. Check Prometheus
echo "[1/5] Checking Prometheus..."
if curl -s http://localhost:9090/-/healthy | grep -q "Prometheus"; then
    echo "✅ Prometheus is running"
else
    echo "❌ Prometheus is not running"
fi

# 2. Check Alertmanager
echo "[2/5] Checking Alertmanager..."
if curl -s http://localhost:9093/-/healthy | grep -q "OK"; then
    echo "✅ Alertmanager is running"
else
    echo "❌ Alertmanager is not running"
fi

# 3. Validate alert rules
echo "[3/5] Validating alert rules..."
docker-compose -f deployment/docker-compose.yml exec -T prometheus \
  promtool check rules /etc/prometheus/alert_rules.yml

# 4. Check configured receivers
echo "[4/5] Checking receivers..."
RECEIVERS=$(docker-compose -f deployment/docker-compose.yml exec -T alertmanager \
  amtool config show | grep "receiver:" | wc -l)
echo "✅ $RECEIVERS receivers configured"

# 5. Send test alert
echo "[5/5] Sending test alert..."
curl -XPOST http://localhost:9093/api/v1/alerts -d '[
  {
    "labels": {"alertname": "TestAlert", "severity": "info"},
    "annotations": {"summary": "Test alert from verification script"},
    "startsAt": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"
  }
]'
echo "✅ Test alert sent"

echo ""
echo "=== Verification Complete ==="
echo "Check your notification channels for test alert"
```

---

## Reference

### Alert Severity Levels

| Severity | Response Time | Notification | Example |
|----------|---------------|--------------|---------|
| **Critical** | Immediate | PagerDuty + Slack | Service down, agent critical |
| **Warning** | 15 minutes | Slack | Agent unhealthy, slow performance |
| **Info** | Business hours | Email | Backup completed, deployment success |

### Common Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Agent Health | < 70% | < 50% |
| System Health | < 90% | < 75% |
| Error Rate | > 5/sec | > 10/sec |
| Response Time (p95) | > 500ms | > 1000ms |
| Disk Space | < 5GB | < 1GB |
| Memory Usage | > 80% | > 90% |

---

**Oracle says**: "Alerts are the early warning system. Configure them wisely." 🚨
