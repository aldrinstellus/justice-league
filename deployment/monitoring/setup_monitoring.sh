#!/bin/bash

################################################################################
# Oracle Monitoring Setup Script
# Week 11-12: Production Deployment Infrastructure
#
# Sets up comprehensive monitoring with:
# - Prometheus for metrics collection
# - Grafana for visualization
# - Alert rules for critical issues
# - Custom Oracle dashboards
################################################################################

set -e

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ENVIRONMENT="${1:-production}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Oracle Monitoring Setup${NC}"
echo -e "${GREEN}Environment: ${ENVIRONMENT}${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo ""

################################################################################
# Create Prometheus Configuration
################################################################################
echo -e "${YELLOW}Creating Prometheus configuration...${NC}"

cat > "${SCRIPT_DIR}/prometheus.yml" << 'EOF'
# Prometheus Configuration for Oracle Monitoring
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'oracle-production'
    environment: 'production'

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

# Load alerting rules
rule_files:
  - 'alerts/*.yml'

# Scrape configurations
scrape_configs:
  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Oracle Blue Instance
  - job_name: 'oracle-blue'
    static_configs:
      - targets: ['oracle-blue:8000']
    metrics_path: '/metrics'

  # Oracle Green Instance
  - job_name: 'oracle-green'
    static_configs:
      - targets: ['oracle-green:8000']
    metrics_path: '/metrics'

  # Node Exporter (system metrics)
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  # Docker metrics
  - job_name: 'docker'
    static_configs:
      - targets: ['docker-host:9323']

  # Nginx metrics
  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx:9113']
EOF

echo -e "${GREEN}✓ Prometheus configuration created${NC}"

################################################################################
# Create Alert Rules
################################################################################
echo -e "${YELLOW}Creating alert rules...${NC}"

mkdir -p "${SCRIPT_DIR}/alerts"

cat > "${SCRIPT_DIR}/alerts/oracle_alerts.yml" << 'EOF'
groups:
  - name: oracle_alerts
    interval: 30s
    rules:
      # Oracle Instance Down
      - alert: OracleInstanceDown
        expr: up{job=~"oracle-.*"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Oracle instance {{ $labels.instance }} is down"
          description: "Oracle instance {{ $labels.instance }} has been down for more than 1 minute."

      # High Error Rate
      - alert: HighErrorRate
        expr: rate(oracle_errors_total[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate on {{ $labels.instance }}"
          description: "Error rate is {{ $value }} errors/second on {{ $labels.instance }}"

      # Database Connection Issues
      - alert: DatabaseConnectionFailed
        expr: oracle_database_connection_status == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Database connection failed on {{ $labels.instance }}"
          description: "Cannot connect to database on {{ $labels.instance }}"

      # Agent Health Critical
      - alert: AgentHealthCritical
        expr: oracle_agent_health_percentage < 60
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Agent health below 60% on {{ $labels.instance }}"
          description: "Only {{ $value }}% of agents are healthy on {{ $labels.instance }}"

      # High Memory Usage
      - alert: HighMemoryUsage
        expr: (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100 < 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Available memory is {{ $value }}% on {{ $labels.instance }}"

      # Low Disk Space
      - alert: LowDiskSpace
        expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 < 10
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Only {{ $value }}% disk space available on {{ $labels.instance }}"

      # High Response Time
      - alert: HighResponseTime
        expr: oracle_operation_duration_seconds{quantile="0.95"} > 2
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High response time on {{ $labels.instance }}"
          description: "95th percentile response time is {{ $value }}s on {{ $labels.instance }}"

      # Version Control Failures
      - alert: VersionControlFailures
        expr: rate(oracle_version_control_failures_total[5m]) > 0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Version control failures on {{ $labels.instance }}"
          description: "Version control is failing at {{ $value }} operations/second on {{ $labels.instance }}"
EOF

echo -e "${GREEN}✓ Alert rules created${NC}"

################################################################################
# Create Grafana Datasource Configuration
################################################################################
echo -e "${YELLOW}Creating Grafana datasource configuration...${NC}"

mkdir -p "${SCRIPT_DIR}/grafana/datasources"

cat > "${SCRIPT_DIR}/grafana/datasources/prometheus.yml" << 'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: false
EOF

echo -e "${GREEN}✓ Grafana datasource configured${NC}"

################################################################################
# Create Grafana Dashboard Configuration
################################################################################
echo -e "${YELLOW}Creating Grafana dashboard configuration...${NC}"

mkdir -p "${SCRIPT_DIR}/grafana/dashboards"

cat > "${SCRIPT_DIR}/grafana/dashboards/oracle_dashboard.json" << 'EOF'
{
  "dashboard": {
    "title": "Oracle System Overview",
    "tags": ["oracle", "production"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Oracle Instance Status",
        "type": "stat",
        "targets": [
          {
            "expr": "up{job=~\"oracle-.*\"}",
            "legendFormat": "{{ instance }}"
          }
        ]
      },
      {
        "id": 2,
        "title": "Agent Health Percentage",
        "type": "gauge",
        "targets": [
          {
            "expr": "oracle_agent_health_percentage",
            "legendFormat": "Health %"
          }
        ]
      },
      {
        "id": 3,
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(oracle_errors_total[5m])",
            "legendFormat": "{{ instance }}"
          }
        ]
      },
      {
        "id": 4,
        "title": "Operation Duration (p95)",
        "type": "graph",
        "targets": [
          {
            "expr": "oracle_operation_duration_seconds{quantile=\"0.95\"}",
            "legendFormat": "{{ operation }}"
          }
        ]
      },
      {
        "id": 5,
        "title": "Version Control Operations",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(oracle_version_control_operations_total[5m])",
            "legendFormat": "{{ operation_type }}"
          }
        ]
      }
    ]
  }
}
EOF

cat > "${SCRIPT_DIR}/grafana/dashboards/dashboard-config.yml" << 'EOF'
apiVersion: 1

providers:
  - name: 'Oracle Dashboards'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 30
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards
EOF

echo -e "${GREEN}✓ Grafana dashboards configured${NC}"

################################################################################
# Create Monitoring Health Check
################################################################################
echo -e "${YELLOW}Creating monitoring health check...${NC}"

cat > "${SCRIPT_DIR}/check_monitoring.sh" << 'EOF'
#!/bin/bash

# Check if Prometheus is up
if ! curl -s http://localhost:9090/-/healthy > /dev/null; then
    echo "❌ Prometheus is not healthy"
    exit 1
fi
echo "✓ Prometheus is healthy"

# Check if Grafana is up
if ! curl -s http://localhost:3000/api/health > /dev/null; then
    echo "❌ Grafana is not healthy"
    exit 1
fi
echo "✓ Grafana is healthy"

# Check if alerts are configured
alert_count=$(curl -s http://localhost:9090/api/v1/rules | grep -o '"groups"' | wc -l)
if [ "$alert_count" -lt 1 ]; then
    echo "❌ No alert rules configured"
    exit 1
fi
echo "✓ Alert rules configured"

echo "✅ All monitoring systems healthy"
EOF

chmod +x "${SCRIPT_DIR}/check_monitoring.sh"

echo -e "${GREEN}✓ Monitoring health check created${NC}"

################################################################################
# Summary
################################################################################
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Monitoring Setup Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo ""
echo "Configuration files created:"
echo "  - ${SCRIPT_DIR}/prometheus.yml"
echo "  - ${SCRIPT_DIR}/alerts/oracle_alerts.yml"
echo "  - ${SCRIPT_DIR}/grafana/datasources/prometheus.yml"
echo "  - ${SCRIPT_DIR}/grafana/dashboards/oracle_dashboard.json"
echo ""
echo "Access URLs (after docker-compose up):"
echo "  - Prometheus: http://localhost:9090"
echo "  - Grafana:    http://localhost:3000 (admin/admin)"
echo ""
echo "To verify monitoring:"
echo "  ${SCRIPT_DIR}/check_monitoring.sh"
echo ""
