#!/bin/bash
################################################################################
# Oracle Production Monitoring Script
# Continuous monitoring with alerts and reporting
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$PROJECT_ROOT/logs/monitoring"
ALERT_THRESHOLD_HEALTH=90
ALERT_THRESHOLD_ERROR_RATE=10
CHECK_INTERVAL=60  # seconds

# Create log directory
mkdir -p "$LOG_DIR"

# Functions
log_info() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_DIR/monitor.log"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✓ $1${NC}" | tee -a "$LOG_DIR/monitor.log"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] ⚠ $1${NC}" | tee -a "$LOG_DIR/monitor.log"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ✗ $1${NC}" | tee -a "$LOG_DIR/monitor.log"
}

send_alert() {
    local severity=$1
    local message=$2

    log_warning "ALERT [$severity]: $message"

    # Send to Slack if configured
    if [[ -n "${SLACK_WEBHOOK_URL}" ]]; then
        curl -X POST "${SLACK_WEBHOOK_URL}" \
            -H 'Content-Type: application/json' \
            -d "{\"text\":\"🚨 Oracle Alert [$severity]: $message\"}" \
            2>/dev/null || true
    fi

    # Log to alert file
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$severity] $message" >> "$LOG_DIR/alerts.log"
}

check_system_health() {
    log_info "Checking system health..."

    cd "$PROJECT_ROOT"

    # Run health check
    if python3 deployment/health_check.py > /tmp/oracle_health_output.txt 2>&1; then
        local exit_code=$?
        log_success "System health check passed"
        return 0
    else
        local exit_code=$?
        log_error "System health check failed (exit code: $exit_code)"
        cat /tmp/oracle_health_output.txt
        return 1
    fi
}

check_agent_health() {
    log_info "Checking agent health..."

    cd "$PROJECT_ROOT"

    # Get agent health summary
    local health_output=$(python3 -c "
from core.oracle_integration.superman_connector import get_superman_interface
import json
try:
    connector = get_superman_interface()
    summary = connector.get_agent_health_summary()
    print(json.dumps(summary))
except Exception as e:
    print(json.dumps({'error': str(e)}))
" 2>&1)

    if echo "$health_output" | jq . > /dev/null 2>&1; then
        local overall_health=$(echo "$health_output" | jq -r '.overall_health // 0')
        local healthy_count=$(echo "$health_output" | jq -r '.healthy_count // 0')
        local total_agents=$(echo "$health_output" | jq -r '.total_agents // 0')

        log_info "System Health: ${overall_health}% | Healthy: ${healthy_count}/${total_agents}"

        # Check threshold
        if (( $(echo "$overall_health < $ALERT_THRESHOLD_HEALTH" | bc -l) )); then
            send_alert "WARNING" "System health is ${overall_health}% (threshold: ${ALERT_THRESHOLD_HEALTH}%)"

            # List unhealthy agents
            echo "$health_output" | jq -r '.agents | to_entries[] | select(.value.status != "healthy") | "\(.key): \(.value.status) (\(.value.health)%)"' | while read agent_status; do
                log_warning "  $agent_status"
            done
        else
            log_success "All agents healthy (${overall_health}%)"
        fi

        # Save to metrics
        echo "{\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"health\": $overall_health, \"healthy_count\": $healthy_count}" >> "$LOG_DIR/health_metrics.jsonl"

        return 0
    else
        log_error "Failed to get agent health"
        echo "$health_output"
        return 1
    fi
}

check_error_rate() {
    log_info "Checking error rate..."

    # Query Prometheus for error rate (last 5 minutes)
    local error_rate=$(curl -s "http://localhost:9090/api/v1/query?query=rate(oracle_errors_total[5m])" 2>/dev/null | jq -r '.data.result[0].value[1] // "0"')

    if [[ "$error_rate" != "0" ]]; then
        log_info "Error rate: ${error_rate}/sec"

        # Check threshold
        if (( $(echo "$error_rate > $ALERT_THRESHOLD_ERROR_RATE" | bc -l) )); then
            send_alert "CRITICAL" "Error rate is ${error_rate}/sec (threshold: ${ALERT_THRESHOLD_ERROR_RATE}/sec)"
        fi
    else
        log_success "Error rate: 0/sec"
    fi
}

check_active_alerts() {
    log_info "Checking active alerts..."

    # Query Alertmanager
    local alerts=$(curl -s "http://localhost:9093/api/v1/alerts" 2>/dev/null | jq '[.data[] | select(.status.state=="active")] | length')

    if [[ "$alerts" == "0" ]]; then
        log_success "No active alerts"
    else
        log_warning "$alerts active alert(s)"

        # List active alerts
        curl -s "http://localhost:9093/api/v1/alerts" 2>/dev/null | jq -r '.data[] | select(.status.state=="active") | "\(.labels.alertname) [\(.labels.severity)]: \(.annotations.summary)"' | while read alert; do
            log_warning "  $alert"
        done
    fi
}

check_disk_space() {
    log_info "Checking disk space..."

    local disk_free=$(df -BG "$PROJECT_ROOT" | tail -1 | awk '{print $4}' | sed 's/G//')

    if [[ $disk_free -lt 1 ]]; then
        send_alert "CRITICAL" "Disk space critically low: ${disk_free}GB free"
    elif [[ $disk_free -lt 5 ]]; then
        log_warning "Disk space low: ${disk_free}GB free"
    else
        log_success "Disk space: ${disk_free}GB free"
    fi
}

check_memory() {
    log_info "Checking memory..."

    if command -v free &> /dev/null; then
        local mem_used_percent=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')

        if [[ $mem_used_percent -gt 90 ]]; then
            send_alert "WARNING" "Memory usage high: ${mem_used_percent}%"
        elif [[ $mem_used_percent -gt 80 ]]; then
            log_warning "Memory usage: ${mem_used_percent}%"
        else
            log_success "Memory usage: ${mem_used_percent}%"
        fi
    else
        log_info "Memory check skipped (free command not available)"
    fi
}

check_service_status() {
    log_info "Checking service status..."

    cd "$PROJECT_ROOT"

    # Check Docker services
    if docker-compose -f deployment/docker-compose.yml ps | grep -q "oracle-blue.*Up"; then
        log_success "Oracle service running"
    else
        send_alert "CRITICAL" "Oracle service is down"
    fi

    if docker-compose -f deployment/docker-compose.yml ps | grep -q "nginx.*Up"; then
        log_success "Nginx service running"
    else
        send_alert "CRITICAL" "Nginx service is down"
    fi
}

generate_report() {
    local report_file="$LOG_DIR/monitoring_report_$(date +%Y%m%d_%H%M%S).txt"

    cat > "$report_file" << EOF
================================================================================
Oracle Monitoring Report
================================================================================
Date: $(date)
Report Period: Last ${CHECK_INTERVAL} seconds

System Health:
$(tail -10 "$LOG_DIR/health_metrics.jsonl" 2>/dev/null | jq -r '"  \(.timestamp): \(.health)%"' || echo "  No data")

Recent Alerts:
$(tail -10 "$LOG_DIR/alerts.log" 2>/dev/null || echo "  No alerts")

Service Status:
$(docker-compose -f "$PROJECT_ROOT/deployment/docker-compose.yml" ps 2>/dev/null || echo "  Could not get status")

Recent Errors (last 100 lines):
$(docker-compose -f "$PROJECT_ROOT/deployment/docker-compose.yml" logs oracle-blue --tail=100 2>/dev/null | grep -i error | tail -10 || echo "  No errors")

================================================================================
EOF

    log_info "Report generated: $report_file"
}

run_monitoring_cycle() {
    log_info "================================"
    log_info "Starting monitoring cycle"
    log_info "================================"

    check_system_health
    check_agent_health
    check_error_rate
    check_active_alerts
    check_disk_space
    check_memory
    check_service_status

    log_info "Monitoring cycle complete"
    log_info "================================"
    echo ""
}

# Main monitoring loop
main() {
    echo "================================================================================"
    echo "Oracle Production Monitoring"
    echo "================================================================================"
    echo "Started: $(date)"
    echo "Check Interval: ${CHECK_INTERVAL}s"
    echo "Health Alert Threshold: ${ALERT_THRESHOLD_HEALTH}%"
    echo "Error Rate Alert Threshold: ${ALERT_THRESHOLD_ERROR_RATE}/sec"
    echo ""
    echo "Logs: $LOG_DIR/monitor.log"
    echo "Alerts: $LOG_DIR/alerts.log"
    echo "Metrics: $LOG_DIR/health_metrics.jsonl"
    echo ""
    echo "Press Ctrl+C to stop"
    echo "================================================================================"
    echo ""

    # Initial check
    run_monitoring_cycle

    # Continuous monitoring
    while true; do
        sleep "$CHECK_INTERVAL"
        run_monitoring_cycle

        # Generate hourly report
        if [[ $(date +%M) == "00" ]]; then
            generate_report
        fi
    done
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --interval)
            CHECK_INTERVAL="$2"
            shift 2
            ;;
        --once)
            run_monitoring_cycle
            exit 0
            ;;
        --report)
            generate_report
            exit 0
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --interval SECONDS  Check interval (default: 60)"
            echo "  --once              Run one monitoring cycle and exit"
            echo "  --report            Generate report and exit"
            echo "  --help              Show this help message"
            echo ""
            echo "Environment variables:"
            echo "  SLACK_WEBHOOK_URL   Slack webhook for alerts"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run main loop
main
