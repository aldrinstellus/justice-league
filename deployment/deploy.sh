#!/bin/bash

################################################################################
# Oracle Production Deployment Script
# Week 11-12: Production Deployment Infrastructure
#
# This script handles the complete deployment of Oracle and all Justice League
# agents to production environment with zero-downtime blue-green deployment.
#
# Usage:
#   ./deploy.sh [environment] [options]
#
# Environments:
#   staging     - Deploy to staging environment
#   production  - Deploy to production environment
#
# Options:
#   --skip-tests      Skip test execution
#   --skip-backup     Skip database backup
#   --force           Force deployment without confirmation
#   --rollback        Rollback to previous version
#
################################################################################

set -e  # Exit on error
set -o pipefail  # Exit on pipe failure

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DEPLOYMENT_LOG="$SCRIPT_DIR/logs/deployment_$(date +%Y%m%d_%H%M%S).log"
HEALTH_CHECK_TIMEOUT=300  # 5 minutes
HEALTH_CHECK_INTERVAL=10  # 10 seconds

# Deployment settings
ENVIRONMENT="${1:-staging}"
SKIP_TESTS=false
SKIP_BACKUP=false
FORCE_DEPLOY=false
ROLLBACK=false

# Parse command line options
shift || true
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --skip-backup)
            SKIP_BACKUP=true
            shift
            ;;
        --force)
            FORCE_DEPLOY=true
            shift
            ;;
        --rollback)
            ROLLBACK=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

################################################################################
# Helper Functions
################################################################################

log() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    echo -e "${timestamp} [${level}] ${message}" | tee -a "$DEPLOYMENT_LOG"
}

log_info() {
    log "INFO" "${BLUE}$@${NC}"
}

log_success() {
    log "SUCCESS" "${GREEN}✓ $@${NC}"
}

log_warning() {
    log "WARNING" "${YELLOW}⚠ $@${NC}"
}

log_error() {
    log "ERROR" "${RED}✗ $@${NC}"
}

check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check required commands
    local required_commands=("python3" "git" "docker" "docker-compose")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            log_error "Required command not found: $cmd"
            exit 1
        fi
    done

    # Check Python version
    local python_version=$(python3 --version | awk '{print $2}')
    log_info "Python version: $python_version"

    # Check Docker daemon
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        exit 1
    fi

    log_success "All prerequisites met"
}

load_environment() {
    log_info "Loading environment: $ENVIRONMENT"

    local env_file="$SCRIPT_DIR/config/${ENVIRONMENT}.env"
    if [[ -f "$env_file" ]]; then
        source "$env_file"
        log_success "Environment loaded from $env_file"
    else
        log_error "Environment file not found: $env_file"
        exit 1
    fi
}

backup_database() {
    if [[ "$SKIP_BACKUP" == "true" ]]; then
        log_warning "Skipping database backup (--skip-backup flag)"
        return 0
    fi

    log_info "Creating database backup..."

    local backup_dir="$SCRIPT_DIR/backups/${ENVIRONMENT}"
    mkdir -p "$backup_dir"

    local backup_file="$backup_dir/oracle_backup_$(date +%Y%m%d_%H%M%S).db"

    # Copy SQLite database
    if [[ -f "$PROJECT_ROOT/oracle.db" ]]; then
        cp "$PROJECT_ROOT/oracle.db" "$backup_file"
        log_success "Database backed up to: $backup_file"
    else
        log_warning "Database file not found, skipping backup"
    fi

    # Keep only last 10 backups
    ls -t "$backup_dir"/oracle_backup_*.db | tail -n +11 | xargs -r rm
    log_info "Cleaned up old backups (keeping last 10)"
}

run_tests() {
    if [[ "$SKIP_TESTS" == "true" ]]; then
        log_warning "Skipping tests (--skip-tests flag)"
        return 0
    fi

    log_info "Running test suite..."

    cd "$PROJECT_ROOT"

    # Run all test files
    local test_files=(
        "test_justice_league.py"
        "test_oracle_foundation.py"
        "test_oracle_self_healing.py"
        "test_oracle_learning.py"
        "test_oracle_version_control.py"
        "test_oracle_integration.py"
        "test_real_world_scenarios.py"
    )

    local total_tests=0
    local passed_tests=0

    for test_file in "${test_files[@]}"; do
        if [[ -f "$test_file" ]]; then
            log_info "Running: $test_file"
            if python3 "$test_file" >> "$DEPLOYMENT_LOG" 2>&1; then
                ((passed_tests++))
            fi
            ((total_tests++))
        fi
    done

    if [[ $passed_tests -eq $total_tests ]]; then
        log_success "All test suites passed ($passed_tests/$total_tests)"
    else
        log_error "Some test suites failed ($passed_tests/$total_tests passed)"
        exit 1
    fi
}

build_docker_images() {
    log_info "Building Docker images..."

    cd "$SCRIPT_DIR"

    # Build with build timestamp
    local build_time=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local git_commit=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

    docker-compose build \
        --build-arg BUILD_TIME="$build_time" \
        --build-arg GIT_COMMIT="$git_commit" \
        --build-arg ENVIRONMENT="$ENVIRONMENT"

    log_success "Docker images built successfully"
}

deploy_blue_green() {
    log_info "Starting blue-green deployment..."

    cd "$SCRIPT_DIR"

    # Determine current and new environments
    local current_env=$(docker-compose ps -q oracle-green &>/dev/null && echo "green" || echo "blue")
    local new_env=$([ "$current_env" == "blue" ] && echo "green" || echo "blue")

    log_info "Current environment: $current_env"
    log_info "Deploying to: $new_env"

    # Start new environment
    log_info "Starting $new_env environment..."
    docker-compose up -d oracle-$new_env

    # Wait for health check
    if wait_for_health_check "oracle-$new_env"; then
        log_success "$new_env environment is healthy"
    else
        log_error "$new_env environment failed health check"
        log_info "Rolling back..."
        docker-compose stop oracle-$new_env
        exit 1
    fi

    # Switch traffic to new environment
    log_info "Switching traffic to $new_env..."
    docker-compose up -d nginx

    # Wait for traffic switch
    sleep 5

    # Verify new environment is serving traffic
    if verify_traffic "$new_env"; then
        log_success "Traffic successfully switched to $new_env"
    else
        log_error "Traffic switch verification failed"
        exit 1
    fi

    # Stop old environment
    log_info "Stopping old environment: $current_env"
    docker-compose stop oracle-$current_env

    log_success "Blue-green deployment completed successfully"
}

wait_for_health_check() {
    local service=$1
    local elapsed=0

    log_info "Waiting for $service to become healthy..."

    while [[ $elapsed -lt $HEALTH_CHECK_TIMEOUT ]]; do
        if docker-compose exec -T "$service" python3 /app/deployment/health_check.py &>/dev/null; then
            return 0
        fi

        sleep $HEALTH_CHECK_INTERVAL
        ((elapsed += HEALTH_CHECK_INTERVAL))

        log_info "Health check attempt $(($elapsed / $HEALTH_CHECK_INTERVAL))... (${elapsed}s elapsed)"
    done

    log_error "Health check timeout after ${HEALTH_CHECK_TIMEOUT}s"
    return 1
}

verify_traffic() {
    local env=$1

    log_info "Verifying traffic routing to $env..."

    # Make test request through load balancer
    local response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health || echo "000")

    if [[ "$response" == "200" ]]; then
        return 0
    else
        log_error "Health endpoint returned: $response"
        return 1
    fi
}

perform_rollback() {
    log_warning "Performing rollback to previous version..."

    cd "$SCRIPT_DIR"

    # Determine environments
    local current_env=$(docker-compose ps -q oracle-green &>/dev/null && echo "green" || echo "blue")
    local previous_env=$([ "$current_env" == "blue" ] && echo "green" || echo "blue")

    log_info "Current: $current_env, Rolling back to: $previous_env"

    # Start previous environment
    docker-compose up -d oracle-$previous_env

    # Wait for health check
    if wait_for_health_check "oracle-$previous_env"; then
        log_success "Previous environment is healthy"
    else
        log_error "Rollback failed - previous environment unhealthy"
        exit 1
    fi

    # Switch traffic back
    docker-compose up -d nginx
    sleep 5

    # Stop current environment
    docker-compose stop oracle-$current_env

    log_success "Rollback completed successfully"
}

setup_monitoring() {
    log_info "Setting up monitoring and alerting..."

    cd "$SCRIPT_DIR/monitoring"

    # Run monitoring setup script
    if [[ -f "setup_monitoring.sh" ]]; then
        bash setup_monitoring.sh "$ENVIRONMENT"
        log_success "Monitoring configured"
    else
        log_warning "Monitoring setup script not found"
    fi
}

generate_deployment_report() {
    log_info "Generating deployment report..."

    local report_file="$SCRIPT_DIR/reports/deployment_$(date +%Y%m%d_%H%M%S).txt"
    mkdir -p "$(dirname "$report_file")"

    cat > "$report_file" << EOF
================================================================================
Oracle Deployment Report
================================================================================

Deployment Time: $(date)
Environment: $ENVIRONMENT
Git Commit: $(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
Deployed By: $(whoami)

Configuration:
- Skip Tests: $SKIP_TESTS
- Skip Backup: $SKIP_BACKUP
- Force Deploy: $FORCE_DEPLOY
- Rollback: $ROLLBACK

Services Status:
$(docker-compose ps)

Recent Logs:
$(tail -n 50 "$DEPLOYMENT_LOG")

================================================================================
EOF

    log_success "Deployment report: $report_file"

    # Print summary
    cat "$report_file"
}

confirm_deployment() {
    if [[ "$FORCE_DEPLOY" == "true" ]]; then
        return 0
    fi

    echo ""
    echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}                  DEPLOYMENT CONFIRMATION${NC}"
    echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
    echo -e "Environment:     ${BLUE}$ENVIRONMENT${NC}"
    echo -e "Skip Tests:      ${BLUE}$SKIP_TESTS${NC}"
    echo -e "Skip Backup:     ${BLUE}$SKIP_BACKUP${NC}"
    echo -e "Git Commit:      ${BLUE}$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')${NC}"
    echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
    echo ""

    read -p "Do you want to proceed? (yes/no): " -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy]es$ ]]; then
        log_warning "Deployment cancelled by user"
        exit 0
    fi
}

################################################################################
# Main Deployment Flow
################################################################################

main() {
    # Create log directory
    mkdir -p "$(dirname "$DEPLOYMENT_LOG")"

    log_info "════════════════════════════════════════════════════════════════"
    log_info "Oracle Production Deployment - Week 11-12"
    log_info "Environment: $ENVIRONMENT"
    log_info "════════════════════════════════════════════════════════════════"

    # Handle rollback
    if [[ "$ROLLBACK" == "true" ]]; then
        confirm_deployment
        perform_rollback
        generate_deployment_report
        log_success "Rollback completed successfully!"
        exit 0
    fi

    # Pre-deployment checks
    check_prerequisites
    load_environment
    confirm_deployment

    # Backup
    backup_database

    # Testing
    run_tests

    # Build
    build_docker_images

    # Deploy
    deploy_blue_green

    # Post-deployment
    setup_monitoring
    generate_deployment_report

    log_success "════════════════════════════════════════════════════════════════"
    log_success "Deployment completed successfully!"
    log_success "Environment: $ENVIRONMENT"
    log_success "Log file: $DEPLOYMENT_LOG"
    log_success "════════════════════════════════════════════════════════════════"
}

# Run main function
main
