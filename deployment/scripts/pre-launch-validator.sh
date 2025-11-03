#!/bin/bash
################################################################################
# Oracle Pre-Launch Validation Script
# Comprehensive validation of all pre-launch requirements
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

# Counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

# Functions
check_pass() {
    echo -e "${GREEN}✓ $1${NC}"
    ((PASSED_CHECKS++))
    ((TOTAL_CHECKS++))
}

check_fail() {
    echo -e "${RED}✗ $1${NC}"
    ((FAILED_CHECKS++))
    ((TOTAL_CHECKS++))
}

check_warn() {
    echo -e "${YELLOW}⚠ $1${NC}"
    ((WARNING_CHECKS++))
    ((TOTAL_CHECKS++))
}

check_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

section_header() {
    echo ""
    echo "================================================================================"
    echo "$1"
    echo "================================================================================"
    echo ""
}

# Main validation
section_header "Oracle Pre-Launch Validation"
echo "Date: $(date)"
echo "Project: $PROJECT_ROOT"
echo ""

# Category 1: Code & Testing
section_header "[1/8] Code & Testing"

echo "[1.1] Checking test files exist..."
TEST_FILES=(
    "test_justice_league.py"
    "test_oracle_version_control.py"
    "test_oracle_integration.py"
    "test_real_world_scenarios.py"
    "test_deployment.py"
)

for test_file in "${TEST_FILES[@]}"; do
    if [[ -f "$PROJECT_ROOT/$test_file" ]]; then
        check_pass "Found $test_file"
    else
        check_fail "Missing $test_file"
    fi
done

echo ""
echo "[1.2] Running test suites..."
cd "$PROJECT_ROOT"

# Run tests if Python is available
if command -v python3 &> /dev/null; then
    for test_file in "${TEST_FILES[@]}"; do
        if [[ -f "$test_file" ]]; then
            echo "Running $test_file..."
            if python3 "$test_file" > /tmp/oracle_test_output.txt 2>&1; then
                PASS_COUNT=$(grep -o "passed" /tmp/oracle_test_output.txt | wc -l || echo "0")
                check_pass "$test_file: Tests passed ($PASS_COUNT)"
            else
                check_fail "$test_file: Tests failed"
                cat /tmp/oracle_test_output.txt | tail -20
            fi
        fi
    done
else
    check_warn "Python3 not found - skipping test execution"
fi

echo ""
echo "[1.3] Checking security audit..."
if [[ -f "$PROJECT_ROOT/security/security_audit.py" ]]; then
    check_pass "Security audit script exists"
    if python3 "$PROJECT_ROOT/security/security_audit.py" > /tmp/oracle_security.txt 2>&1; then
        CRITICAL=$(grep -i "critical.*0" /tmp/oracle_security.txt | wc -l || echo "0")
        if [[ $CRITICAL -gt 0 ]]; then
            check_pass "Security audit: 0 critical findings"
        else
            check_warn "Security audit: Review required"
        fi
    else
        check_warn "Security audit execution failed"
    fi
else
    check_fail "Security audit script missing"
fi

echo ""
echo "[1.4] Checking performance benchmarks..."
if [[ -f "$PROJECT_ROOT/performance/benchmark_suite.py" ]]; then
    check_pass "Benchmark suite exists"
    if python3 "$PROJECT_ROOT/performance/benchmark_suite.py" > /tmp/oracle_benchmark.txt 2>&1; then
        BENCH_PASS=$(grep -o "8/8 passed" /tmp/oracle_benchmark.txt | wc -l || echo "0")
        if [[ $BENCH_PASS -gt 0 ]]; then
            check_pass "Performance benchmarks: 8/8 passed"
        else
            check_warn "Performance benchmarks: Review required"
        fi
    else
        check_warn "Benchmark execution failed"
    fi
else
    check_fail "Benchmark suite missing"
fi

# Category 2: Infrastructure
section_header "[2/8] Infrastructure"

echo "[2.1] Checking deployment files..."
DEPLOY_FILES=(
    "deployment/deploy.sh"
    "deployment/Dockerfile"
    "deployment/docker-compose.yml"
    "deployment/health_check.py"
    "deployment/nginx/nginx.conf"
)

for file in "${DEPLOY_FILES[@]}"; do
    if [[ -f "$PROJECT_ROOT/$file" ]]; then
        check_pass "Found $file"
    else
        check_fail "Missing $file"
    fi
done

echo ""
echo "[2.2] Checking deployment script permissions..."
if [[ -x "$PROJECT_ROOT/deployment/deploy.sh" ]]; then
    check_pass "deploy.sh is executable"
else
    check_fail "deploy.sh is not executable (run: chmod +x deployment/deploy.sh)"
fi

echo ""
echo "[2.3] Checking Docker..."
if command -v docker &> /dev/null; then
    check_pass "Docker installed: $(docker --version | cut -d' ' -f3)"
    if docker ps &> /dev/null; then
        check_pass "Docker daemon running"
    else
        check_fail "Docker daemon not running"
    fi
else
    check_fail "Docker not installed"
fi

echo ""
echo "[2.4] Checking Docker Compose..."
if command -v docker-compose &> /dev/null; then
    check_pass "Docker Compose installed: $(docker-compose --version | cut -d' ' -f3)"
else
    check_fail "Docker Compose not installed"
fi

echo ""
echo "[2.5] Checking SSL certificates..."
if [[ -f "$PROJECT_ROOT/deployment/nginx/ssl/oracle.crt" ]] && [[ -f "$PROJECT_ROOT/deployment/nginx/ssl/oracle.key" ]]; then
    check_pass "SSL certificate files exist"

    # Check certificate expiration
    if command -v openssl &> /dev/null; then
        DAYS_LEFT=$(openssl x509 -in "$PROJECT_ROOT/deployment/nginx/ssl/oracle.crt" -noout -enddate 2>/dev/null | sed 's/notAfter=//' | xargs -I {} date -d {} +%s 2>/dev/null | xargs -I {} echo $(( ({} - $(date +%s)) / 86400 )) 2>/dev/null || echo "0")
        if [[ $DAYS_LEFT -gt 30 ]]; then
            check_pass "SSL certificate valid for $DAYS_LEFT more days"
        elif [[ $DAYS_LEFT -gt 0 ]]; then
            check_warn "SSL certificate expires in $DAYS_LEFT days - renewal needed soon"
        else
            check_fail "SSL certificate expired or invalid"
        fi
    fi

    # Check permissions
    CERT_PERMS=$(stat -c %a "$PROJECT_ROOT/deployment/nginx/ssl/oracle.crt" 2>/dev/null || stat -f %A "$PROJECT_ROOT/deployment/nginx/ssl/oracle.crt" 2>/dev/null || echo "unknown")
    KEY_PERMS=$(stat -c %a "$PROJECT_ROOT/deployment/nginx/ssl/oracle.key" 2>/dev/null || stat -f %A "$PROJECT_ROOT/deployment/nginx/ssl/oracle.key" 2>/dev/null || echo "unknown")

    if [[ "$CERT_PERMS" == "644" ]]; then
        check_pass "Certificate permissions correct (644)"
    else
        check_warn "Certificate permissions: $CERT_PERMS (should be 644)"
    fi

    if [[ "$KEY_PERMS" == "600" ]]; then
        check_pass "Private key permissions correct (600)"
    else
        check_warn "Private key permissions: $KEY_PERMS (should be 600)"
    fi
else
    check_fail "SSL certificates not installed (see: deployment/SSL_CERTIFICATE_SETUP.md)"
fi

# Category 3: Documentation
section_header "[3/8] Documentation"

echo "[3.1] Checking core documentation..."
DOCS=(
    "docs/ORACLE_USER_GUIDE.md"
    "docs/ORACLE_API_REFERENCE.md"
    "docs/ORACLE_BEST_PRACTICES.md"
    "docs/ORACLE_INTEGRATION_GUIDE.md"
    "docs/OPERATOR_TRAINING_MANUAL.md"
    "docs/OPERATIONAL_RUNBOOKS.md"
    "docs/TROUBLESHOOTING_GUIDE.md"
)

for doc in "${DOCS[@]}"; do
    if [[ -f "$PROJECT_ROOT/$doc" ]]; then
        check_pass "Found $doc"
    else
        check_fail "Missing $doc"
    fi
done

echo ""
echo "[3.2] Checking launch documentation..."
LAUNCH_DOCS=(
    "PRODUCTION_LAUNCH_CHECKLIST.md"
    "LAUNCH_DAY_EXECUTION_GUIDE.md"
    "PRE_LAUNCH_MATERIALS_COMPLETE.md"
    "ORACLE_PRODUCTION_READY.md"
)

for doc in "${LAUNCH_DOCS[@]}"; do
    if [[ -f "$PROJECT_ROOT/$doc" ]]; then
        check_pass "Found $doc"
    else
        check_fail "Missing $doc"
    fi
done

# Category 4: Monitoring
section_header "[4/8] Monitoring"

echo "[4.1] Checking monitoring configuration..."
MON_FILES=(
    "deployment/monitoring/prometheus.yml"
    "deployment/monitoring/alert_rules.yml"
    "deployment/monitoring/setup_monitoring.sh"
)

for file in "${MON_FILES[@]}"; do
    if [[ -f "$PROJECT_ROOT/$file" ]]; then
        check_pass "Found $file"
    else
        check_fail "Missing $file"
    fi
done

echo ""
echo "[4.2] Checking Alertmanager configuration..."
if [[ -f "$PROJECT_ROOT/deployment/monitoring/alertmanager.yml" ]]; then
    check_pass "Alertmanager configuration exists"
elif [[ -f "$PROJECT_ROOT/deployment/monitoring/alertmanager.example.yml" ]]; then
    check_warn "Only example alertmanager.yml found - configure for production"
else
    check_fail "No alertmanager.yml found"
fi

# Category 5: Database
section_header "[5/8] Database"

echo "[5.1] Checking database files..."
if [[ -f "$PROJECT_ROOT/oracle.db" ]]; then
    check_pass "Database file exists"
    DB_SIZE=$(du -h "$PROJECT_ROOT/oracle.db" | cut -f1)
    check_info "Database size: $DB_SIZE"
else
    check_warn "No database file (will be created on first run)"
fi

echo ""
echo "[5.2] Checking backup directory..."
BACKUP_DIR="$PROJECT_ROOT/backups"
if [[ -d "$BACKUP_DIR" ]]; then
    check_pass "Backup directory exists"
    BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/*.db 2>/dev/null | wc -l || echo "0")
    check_info "Backup files: $BACKUP_COUNT"
else
    check_warn "Backup directory will be created on first backup"
fi

# Category 6: System Resources
section_header "[6/8] System Resources"

echo "[6.1] Checking disk space..."
DISK_FREE=$(df -BG "$PROJECT_ROOT" | tail -1 | awk '{print $4}' | sed 's/G//')
if [[ $DISK_FREE -gt 5 ]]; then
    check_pass "Disk space: ${DISK_FREE}GB free (>5GB required)"
elif [[ $DISK_FREE -gt 1 ]]; then
    check_warn "Disk space: ${DISK_FREE}GB free (5GB+ recommended)"
else
    check_fail "Disk space: ${DISK_FREE}GB free (<1GB critical)"
fi

echo ""
echo "[6.2] Checking memory..."
if command -v free &> /dev/null; then
    MEM_FREE=$(free -g | grep Mem | awk '{print $7}')
    if [[ $MEM_FREE -gt 2 ]]; then
        check_pass "Memory: ${MEM_FREE}GB available (>2GB required)"
    elif [[ $MEM_FREE -gt 1 ]]; then
        check_warn "Memory: ${MEM_FREE}GB available (2GB+ recommended)"
    else
        check_fail "Memory: ${MEM_FREE}GB available (<1GB critical)"
    fi
else
    check_info "Cannot check memory (free command not available)"
fi

# Category 7: Operational Readiness
section_header "[7/8] Operational Readiness"

echo "[7.1] Checking operator certification program..."
if [[ -f "$PROJECT_ROOT/docs/OPERATOR_CERTIFICATION_PROGRAM.md" ]]; then
    check_pass "Certification program available"
else
    check_fail "Operator certification program missing"
fi

echo ""
echo "[7.2] Checking SSL setup guide..."
if [[ -f "$PROJECT_ROOT/deployment/SSL_CERTIFICATE_SETUP.md" ]]; then
    check_pass "SSL setup guide available"
else
    check_fail "SSL setup guide missing"
fi

echo ""
echo "[7.3] Checking alert configuration guide..."
if [[ -f "$PROJECT_ROOT/deployment/monitoring/ALERT_CONFIGURATION.md" ]]; then
    check_pass "Alert configuration guide available"
else
    check_fail "Alert configuration guide missing"
fi

echo ""
echo "[7.4] Checking launch execution guide..."
if [[ -f "$PROJECT_ROOT/LAUNCH_DAY_EXECUTION_GUIDE.md" ]]; then
    check_pass "Launch execution guide available"
else
    check_fail "Launch execution guide missing"
fi

# Category 8: Final Checks
section_header "[8/8] Final Readiness Checks"

echo "[8.1] Summary of critical requirements..."

CRITICAL_REQS=(
    "All tests passing"
    "Security audit passed"
    "Performance benchmarks passed"
    "Deployment files present"
    "SSL certificates installed"
    "Documentation complete"
    "Monitoring configured"
)

for req in "${CRITICAL_REQS[@]}"; do
    check_info "$req"
done

echo ""
echo "[8.2] Checking environment configuration..."
if [[ -f "$PROJECT_ROOT/deployment/config/production.env" ]]; then
    check_pass "Production environment configuration exists"
else
    check_warn "Production environment configuration missing"
fi

echo ""
echo "[8.3] Checking CI/CD configuration..."
if [[ -f "$PROJECT_ROOT/.github/workflows/ci-cd.yml" ]]; then
    check_pass "CI/CD pipeline configured"
else
    check_warn "CI/CD pipeline not configured"
fi

# Final Summary
section_header "Validation Summary"

echo "Total Checks: $TOTAL_CHECKS"
echo -e "${GREEN}Passed: $PASSED_CHECKS${NC}"
echo -e "${YELLOW}Warnings: $WARNING_CHECKS${NC}"
echo -e "${RED}Failed: $FAILED_CHECKS${NC}"
echo ""

# Calculate percentage
PASS_PERCENT=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))

echo "Validation Score: $PASS_PERCENT%"
echo ""

# Determine readiness level
if [[ $FAILED_CHECKS -eq 0 ]] && [[ $WARNING_CHECKS -eq 0 ]]; then
    echo -e "${GREEN}✅ PRODUCTION READY - All checks passed${NC}"
    EXIT_CODE=0
elif [[ $FAILED_CHECKS -eq 0 ]]; then
    echo -e "${YELLOW}⚠️ MOSTLY READY - Address warnings before launch${NC}"
    EXIT_CODE=1
elif [[ $FAILED_CHECKS -lt 5 ]]; then
    echo -e "${YELLOW}⚠️ PREPARATION NEEDED - Address failures before launch${NC}"
    EXIT_CODE=2
else
    echo -e "${RED}❌ NOT READY - Significant preparation required${NC}"
    EXIT_CODE=3
fi

echo ""
echo "Next Steps:"
if [[ $FAILED_CHECKS -gt 0 ]]; then
    echo "1. Address all failed checks above"
fi
if [[ $WARNING_CHECKS -gt 0 ]]; then
    echo "2. Review and address warnings"
fi
if [[ ! -f "$PROJECT_ROOT/deployment/nginx/ssl/oracle.crt" ]]; then
    echo "3. Generate SSL certificates: ./deployment/scripts/setup-ssl.sh"
fi
echo "4. Certify operators: See docs/OPERATOR_CERTIFICATION_PROGRAM.md"
echo "5. Configure monitoring alerts: See deployment/monitoring/ALERT_CONFIGURATION.md"
echo "6. Review launch guide: LAUNCH_DAY_EXECUTION_GUIDE.md"
echo ""

section_header "Oracle says: \"Validation complete. Review results carefully.\" 🔍"

exit $EXIT_CODE
