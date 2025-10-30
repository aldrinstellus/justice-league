#!/bin/bash
################################################################################
# Oracle Staging Deployment Validation Script
# Validates staging deployment before production launch
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
STAGING_URL="${STAGING_URL:-http://localhost:8000}"

# Counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Functions
test_pass() {
    echo -e "${GREEN}✓ $1${NC}"
    ((PASSED_TESTS++))
    ((TOTAL_TESTS++))
}

test_fail() {
    echo -e "${RED}✗ $1${NC}"
    ((FAILED_TESTS++))
    ((TOTAL_TESTS++))
}

test_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

section_header() {
    echo ""
    echo "================================================================================"
    echo "$1"
    echo "================================================================================"
    echo ""
}

# Validation tests
section_header "Oracle Staging Deployment Validation"
echo "Date: $(date)"
echo "Staging URL: $STAGING_URL"
echo ""

# Test 1: Deployment exists
section_header "[1/10] Deployment Status"

cd "$PROJECT_ROOT"

if docker-compose -f deployment/docker-compose.yml ps | grep -q "oracle-blue.*Up"; then
    test_pass "Oracle service is running"
else
    test_fail "Oracle service is not running"
fi

if docker-compose -f deployment/docker-compose.yml ps | grep -q "nginx.*Up"; then
    test_pass "Nginx service is running"
else
    test_fail "Nginx service is not running"
fi

# Test 2: Health checks
section_header "[2/10] Health Checks"

echo "Running comprehensive health check..."
if python3 deployment/health_check.py; then
    test_pass "All health checks passed"
else
    test_fail "Health checks failed"
fi

# Test 3: Agent health
section_header "[3/10] Agent Health"

HEALTH_JSON=$(python3 -c "
from core.oracle_integration.superman_connector import get_superman_interface
import json
try:
    connector = get_superman_interface()
    summary = connector.get_agent_health_summary()
    print(json.dumps(summary))
except Exception as e:
    print(json.dumps({'error': str(e)}))
" 2>&1)

if echo "$HEALTH_JSON" | jq . > /dev/null 2>&1; then
    OVERALL_HEALTH=$(echo "$HEALTH_JSON" | jq -r '.overall_health // 0')
    HEALTHY_COUNT=$(echo "$HEALTH_JSON" | jq -r '.healthy_count // 0')
    TOTAL_AGENTS=$(echo "$HEALTH_JSON" | jq -r '.total_agents // 11')

    test_info "System Health: ${OVERALL_HEALTH}%"
    test_info "Healthy Agents: ${HEALTHY_COUNT}/${TOTAL_AGENTS}"

    if (( $(echo "$OVERALL_HEALTH >= 90" | bc -l) )); then
        test_pass "System health above 90%"
    else
        test_fail "System health below 90%: ${OVERALL_HEALTH}%"
    fi

    if [[ $HEALTHY_COUNT -eq $TOTAL_AGENTS ]]; then
        test_pass "All $TOTAL_AGENTS agents healthy"
    else
        test_fail "Only $HEALTHY_COUNT/$TOTAL_AGENTS agents healthy"
    fi
else
    test_fail "Could not get agent health"
fi

# Test 4: HTTP endpoints
section_header "[4/10] HTTP Endpoints"

# Test health endpoint
if curl -s -f "$STAGING_URL/health" > /dev/null 2>&1; then
    test_pass "Health endpoint responding"
else
    test_fail "Health endpoint not responding"
fi

# Test with actual health check
HEALTH_RESPONSE=$(curl -s "$STAGING_URL/health" 2>/dev/null || echo "{}")
if echo "$HEALTH_RESPONSE" | jq . > /dev/null 2>&1; then
    STATUS=$(echo "$HEALTH_RESPONSE" | jq -r '.status // "unknown"')
    if [[ "$STATUS" == "healthy" ]]; then
        test_pass "Health endpoint returns healthy status"
    else
        test_fail "Health endpoint returns: $STATUS"
    fi
fi

# Test 5: SSL/HTTPS (if configured)
section_header "[5/10] SSL/HTTPS"

if [[ "$STAGING_URL" == https://* ]]; then
    if curl -s -f "$STAGING_URL/health" > /dev/null 2>&1; then
        test_pass "HTTPS connection successful"
    else
        test_fail "HTTPS connection failed"
    fi

    # Check certificate
    CERT_DAYS=$(echo | openssl s_client -servername "${STAGING_URL#https://}" -connect "${STAGING_URL#https://}:443" 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | sed 's/notAfter=//' | xargs -I {} date -d {} +%s | xargs -I {} echo $(( ({} - $(date +%s)) / 86400 )) || echo "0")

    if [[ $CERT_DAYS -gt 30 ]]; then
        test_pass "SSL certificate valid for $CERT_DAYS days"
    elif [[ $CERT_DAYS -gt 0 ]]; then
        test_fail "SSL certificate expires in $CERT_DAYS days"
    else
        test_fail "SSL certificate expired or invalid"
    fi
else
    test_info "Skipping HTTPS tests (HTTP staging environment)"
fi

# Test 6: Database
section_header "[6/10] Database"

if [[ -f "$PROJECT_ROOT/oracle.db" ]]; then
    test_pass "Database file exists"

    # Check database integrity
    if sqlite3 "$PROJECT_ROOT/oracle.db" "PRAGMA integrity_check;" | grep -q "ok"; then
        test_pass "Database integrity OK"
    else
        test_fail "Database integrity check failed"
    fi

    # Check database size
    DB_SIZE=$(du -m "$PROJECT_ROOT/oracle.db" | cut -f1)
    test_info "Database size: ${DB_SIZE}MB"

    if [[ $DB_SIZE -lt 1000 ]]; then
        test_pass "Database size reasonable (<1GB)"
    else
        test_fail "Database size large (${DB_SIZE}MB)"
    fi
else
    test_fail "Database file not found"
fi

# Test 7: Logs
section_header "[7/10] Logs"

# Check for critical errors in logs
CRITICAL_ERRORS=$(docker-compose -f deployment/docker-compose.yml logs oracle-blue --tail=1000 2>&1 | grep -i "critical" | wc -l)
ERROR_COUNT=$(docker-compose -f deployment/docker-compose.yml logs oracle-blue --tail=1000 2>&1 | grep -i "error" | wc -l)

test_info "Critical errors in logs: $CRITICAL_ERRORS"
test_info "Errors in logs: $ERROR_COUNT"

if [[ $CRITICAL_ERRORS -eq 0 ]]; then
    test_pass "No critical errors in logs"
else
    test_fail "$CRITICAL_ERRORS critical errors found"
fi

if [[ $ERROR_COUNT -lt 10 ]]; then
    test_pass "Error count acceptable (<10)"
else
    test_fail "$ERROR_COUNT errors found (investigate)"
fi

# Test 8: Performance
section_header "[8/10] Performance"

echo "Running performance smoke test..."

# Health check response time
START_TIME=$(date +%s%N)
curl -s "$STAGING_URL/health" > /dev/null 2>&1
END_TIME=$(date +%s%N)
RESPONSE_TIME=$(( (END_TIME - START_TIME) / 1000000 ))  # Convert to milliseconds

test_info "Health endpoint response time: ${RESPONSE_TIME}ms"

if [[ $RESPONSE_TIME -lt 1000 ]]; then
    test_pass "Response time < 1 second"
else
    test_fail "Response time slow: ${RESPONSE_TIME}ms"
fi

# Test 9: Monitoring
section_header "[9/10] Monitoring"

# Check Prometheus
if curl -s "http://localhost:9090/-/healthy" | grep -q "Prometheus"; then
    test_pass "Prometheus is running"
else
    test_fail "Prometheus is not responding"
fi

# Check Alertmanager
if curl -s "http://localhost:9093/-/healthy" | grep -q "OK"; then
    test_pass "Alertmanager is running"
else
    test_fail "Alertmanager is not responding"
fi

# Check Grafana
if curl -s "http://localhost:3000/api/health" | jq -r '.database' 2>/dev/null | grep -q "ok"; then
    test_pass "Grafana is running"
else
    test_fail "Grafana is not responding"
fi

# Test 10: Integration
section_header "[10/10] Integration Tests"

echo "Testing Superman connector..."
SUPERMAN_TEST=$(python3 -c "
from core.oracle_integration.superman_connector import get_superman_interface
try:
    connector = get_superman_interface()
    result = connector.heartbeat()
    print('success' if result.get('status') else 'fail')
except Exception as e:
    print(f'error: {e}')
" 2>&1)

if [[ "$SUPERMAN_TEST" == "success" ]]; then
    test_pass "Superman connector working"
else
    test_fail "Superman connector failed: $SUPERMAN_TEST"
fi

echo "Testing version control..."
VERSION_TEST=$(python3 -c "
from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl
try:
    vc = EnhancedVersionControl()
    versions = vc.get_all_versions()
    print('success' if len(versions) >= 0 else 'fail')
except Exception as e:
    print(f'error: {e}')
" 2>&1)

if [[ "$VERSION_TEST" == "success" ]]; then
    test_pass "Version control working"
else
    test_fail "Version control failed: $VERSION_TEST"
fi

# Summary
section_header "Validation Summary"

echo "Total Tests: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
echo -e "${RED}Failed: $FAILED_TESTS${NC}"
echo ""

PASS_PERCENT=$((PASSED_TESTS * 100 / TOTAL_TESTS))
echo "Pass Rate: $PASS_PERCENT%"
echo ""

# Determine readiness
if [[ $FAILED_TESTS -eq 0 ]]; then
    echo -e "${GREEN}✅ STAGING VALIDATION PASSED${NC}"
    echo "Staging environment is ready for production promotion"
    EXIT_CODE=0
elif [[ $FAILED_TESTS -lt 3 ]]; then
    echo -e "${YELLOW}⚠️ STAGING VALIDATION PARTIAL${NC}"
    echo "Minor issues detected - review before production"
    EXIT_CODE=1
else
    echo -e "${RED}❌ STAGING VALIDATION FAILED${NC}"
    echo "Significant issues detected - do not promote to production"
    EXIT_CODE=2
fi

echo ""
echo "Next Steps:"
if [[ $EXIT_CODE -eq 0 ]]; then
    echo "1. Review validation results"
    echo "2. Proceed with production deployment"
    echo "3. Monitor closely during launch"
elif [[ $EXIT_CODE -eq 1 ]]; then
    echo "1. Review and address failed tests"
    echo "2. Re-run validation"
    echo "3. Proceed with caution"
else
    echo "1. Address all failed tests"
    echo "2. Re-deploy to staging"
    echo "3. Re-run validation"
    echo "4. Do not proceed to production"
fi

echo ""
section_header "Oracle says: \"Staging validation complete. Review carefully.\" 🔍"

exit $EXIT_CODE
