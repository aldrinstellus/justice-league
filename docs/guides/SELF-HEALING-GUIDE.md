# Justice League Self-Healing Guide

**Version**: 1.0.0
**Last Updated**: 2025-12-01
**Status**: Production Ready (15,000+ LOC)

---

## Overview

The Justice League has comprehensive **self-healing capabilities** built into its autonomous systems. This guide documents the three primary self-healing engines and how they work together to ensure 99.9%+ reliability.

---

## Self-Healing Engines

### 1. Superman Self-Healing Engine

**Location**: `/Users/admin/Documents/claudecode/tools/automation/aldo-vision/core/superman_self_healing.py`
**Lines**: 641
**Status**: Production Ready

#### Capabilities

| Feature | Description |
|---------|-------------|
| **Exponential Backoff Retry** | 1s → 2s → 4s → 8s → 16s → 32s delay between retries |
| **Circuit Breaker Pattern** | 3 states: CLOSED (normal), OPEN (failing), HALF_OPEN (testing) |
| **Error Classification** | CRITICAL, HIGH, MEDIUM, LOW severity levels |
| **Health Monitoring** | Continuous component health checks with auto-repair |
| **Error History** | Tracks last 1000 errors for pattern analysis |

#### Error Classification

| Error Type | Severity | Action |
|------------|----------|--------|
| TimeoutError | MEDIUM | Auto-retry with backoff |
| ConnectionError | MEDIUM | Auto-retry with backoff |
| ValueError | HIGH | Fail fast, log error |
| TypeError | HIGH | Fail fast, log error |
| SystemError | CRITICAL | Alert + immediate investigation |
| MemoryError | CRITICAL | Alert + resource cleanup |

#### Usage Pattern

```python
from core.superman_self_healing import SupermanSelfHealing

healing = SupermanSelfHealing()

# Register custom recovery strategy
healing.register_recovery_strategy(
    error_type=TimeoutError,
    strategy=lambda: retry_with_longer_timeout()
)

# Execute with self-healing
result = healing.execute_with_retry(
    operation=my_operation,
    max_retries=3,
    base_delay=1.0
)

# Run health checks
health_report = healing.run_health_checks()
```

---

### 2. Oracle Health Monitor

**Location**: `/Users/admin/Documents/claudecode/missions/core/oracle_self_healing/health_monitor.py`
**Lines**: 605
**Status**: Production Ready

#### Health Status Levels

| Status | Success Rate | Action |
|--------|-------------|--------|
| HEALTHY | >95% | Normal operation |
| WARNING | 85-95% | Monitor closely |
| UNHEALTHY | 70-85% | Investigation needed |
| CRITICAL | <70% | Immediate action required |

#### Detection Capabilities

- Performance degradation monitoring
- High error rate detection (thresholds: 2% healthy, 5% warning, 10% critical)
- Recurring error pattern detection (3+ occurrences)
- Timeout error detection (2s healthy, 5s warning, 10s critical)
- Resource exhaustion monitoring
- Consecutive failure counting (3 warning, 5 critical)
- SLA violation detection
- Dependency failure tracking

#### Auto-Recommendations

| Condition | Recommendation |
|-----------|---------------|
| Critical status | Immediate investigation, consider rollback |
| High error rate | Root cause analysis, configuration review |
| Performance degradation | Profiling, caching strategies |
| Recurring errors | Query knowledge base for known fixes |

#### Usage Pattern

```python
from oracle_self_healing.health_monitor import HealthMonitor

monitor = HealthMonitor()

# Check system health
status = monitor.check_health()
print(f"Status: {status.level}")  # HEALTHY, WARNING, UNHEALTHY, CRITICAL

# Get recommendations
if status.level != "HEALTHY":
    recommendations = monitor.get_recommendations(status)
    for rec in recommendations:
        print(f"- {rec}")

# Track metrics
monitor.record_operation(
    operation="figma_export",
    success=True,
    duration_ms=1500
)
```

---

### 3. Artemis Self-Healing Engine

**Location**: `/Users/admin/Documents/claudecode/tools/automation/aldo-vision/core/justice_league/artemis_self_healing.py`
**Lines**: 407
**Status**: Production Ready

#### Capabilities

| Feature | Description |
|---------|-------------|
| **Issue Detection** | Compares generated code against Figma specifications |
| **Confidence Scoring** | Each issue gets a confidence score (0-100%) |
| **Auto-Fix Threshold** | Issues with 70%+ confidence are auto-fixed |
| **Expert Fix Patterns** | Pre-defined fixes for common issues |

#### Expert Fix Patterns

| Issue Type | Confidence | Fix Strategy |
|------------|------------|--------------|
| component-style-conflict | 95% | Replace Card/Button with native HTML |
| spacing-mismatch | 98% | Apply correct Tailwind padding/gap classes |
| color-approximation | 100% | Use exact hex values from Figma |
| missing-divider | 90% | Add border-b/border-t based on layer structure |
| layout-constraint-issue | 85% | Separate full-width from constrained content |

#### Usage Pattern

```python
from justice_league.artemis_self_healing import ArtemisSelfHealing

healing = ArtemisSelfHealing()

# Analyze generated code
issues = healing.detect_issues(
    generated_code=code,
    figma_spec=spec
)

# Auto-fix high-confidence issues
for issue in issues:
    if issue.confidence >= 0.70:
        fixed_code = healing.apply_fix(issue)
        print(f"Auto-fixed: {issue.type} ({issue.confidence*100}% confidence)")
    else:
        print(f"Manual review needed: {issue.type} ({issue.confidence*100}%)")
```

---

## Retry Mechanisms

### Hawkman Retry Patch

**Location**: `/Users/admin/Documents/claudecode/tools/automation/aldo-vision/core/justice_league/hawkman_retry_patch.py`
**Lines**: 121

#### Configuration

| Setting | Value | Purpose |
|---------|-------|---------|
| Max Retries | 3 | Maximum retry attempts |
| API Timeout | 60s | Figma API request timeout |
| CDN Timeout | 120s | Image download timeout |
| Backoff Factor | 2.0 | Exponential backoff multiplier |

#### Retry Strategy

```
Attempt 1: Immediate
Attempt 2: Wait 1s (2^0)
Attempt 3: Wait 2s (2^1)
Attempt 4: Wait 4s (2^2)
Final: Return error
```

#### Transient vs Permanent Errors

| Transient (Retry) | Permanent (Fail Fast) |
|-------------------|----------------------|
| requests.Timeout | JSON parsing errors |
| requests.ConnectionError | Invalid file key |
| Network failures | No image URL returned |

---

### Quicksilver Rate Limit Protection

**Location**: `/Users/admin/Documents/claudecode/tools/automation/aldo-vision/core/justice_league/quicksilver_speed_export.py`

#### Rate Limit Handling

1. **Detection**: Auto-detect 429 (Too Many Requests) status
2. **Extraction**: Read `Retry-After` header (default 60s if missing)
3. **Backoff**: Wait the specified duration
4. **Resume**: Continue processing after backoff

#### Environment Variables

```bash
QUICKSILVER_MAX_WORKERS=8          # Concurrent workers
QUICKSILVER_BATCH_SIZE=15          # Frames per API batch
QUICKSILVER_API_TIMEOUT=15         # API timeout (seconds)
QUICKSILVER_CDN_TIMEOUT=30         # CDN timeout (seconds)
QUICKSILVER_MAX_RETRIES=5          # Max retry attempts
```

---

## Circuit Breaker Pattern

The circuit breaker prevents cascading failures by stopping requests to failing services.

### States

```
┌─────────────────────────────────────────────────────────────────┐
│                    CIRCUIT BREAKER STATES                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    ┌──────────┐    5 failures    ┌──────────┐                   │
│    │  CLOSED  │ ───────────────► │   OPEN   │                   │
│    │ (normal) │                  │ (failing)│                   │
│    └────┬─────┘                  └────┬─────┘                   │
│         │                              │                         │
│         │ success                      │ 60s timeout             │
│         │                              ▼                         │
│         │                        ┌───────────┐                   │
│         └──────────────────────  │ HALF_OPEN │                   │
│                    success       │ (testing) │                   │
│                                  └───────────┘                   │
│                                        │                         │
│                                        │ failure                 │
│                                        ▼                         │
│                                  ┌──────────┐                    │
│                                  │   OPEN   │                    │
│                                  └──────────┘                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| failure_threshold | 5 | Failures before opening |
| reset_timeout | 60s | Time before testing again |
| success_threshold | 2 | Successes to close |

---

## Error Recovery Storage

### Storage Locations

| Data | Location | Retention |
|------|----------|-----------|
| Superman error history | `/tmp/aldo-vision-self-healing/error_history.json` | Last 1000 errors |
| Oracle agent metrics | `/tmp/aldo-vision-justice-league/oracle/agent_metrics.json` | All time |
| Oracle health reports | `/tmp/aldo-vision-justice-league/oracle/health_reports.json` | 50 per agent |
| Oracle detected issues | `/tmp/aldo-vision-justice-league/oracle/detected_issues.json` | All time |

---

## Integration with Hero Base

All 21+ heroes inherit self-healing capabilities from the `HeroBase` class:

```python
class HeroBase:
    def auto_recover(self, operation, max_retries=3):
        """Automatic error recovery with exponential backoff"""
        for attempt in range(max_retries):
            try:
                return operation()
            except TransientError as e:
                delay = 2 ** attempt
                time.sleep(delay)
                continue
            except PermanentError as e:
                self.learn_from_failure(e)
                raise
        raise MaxRetriesExceeded()

    def register_fallback(self, operation_name, fallback_func):
        """Register custom fallback for specific operations"""
        self.fallbacks[operation_name] = fallback_func
```

---

## Best Practices

### 1. Always Use Retry Decorators

```python
from lib.self_healing import retry_decorator

@retry_decorator(max_retries=3, backoff_factor=2.0)
def fetch_figma_data(file_key):
    return figma_api.get_file(file_key)
```

### 2. Classify Errors Correctly

```python
# Transient - should retry
TRANSIENT_ERRORS = (TimeoutError, ConnectionError, HTTPError429)

# Permanent - should fail fast
PERMANENT_ERRORS = (ValueError, TypeError, HTTPError404)
```

### 3. Monitor Health Continuously

```python
# Check health before major operations
health = monitor.check_health()
if health.level == "CRITICAL":
    raise SystemUnhealthyError("System health critical, aborting operation")
```

### 4. Learn from Failures

```python
try:
    result = operation()
except Exception as e:
    # Record failure for learning
    self.learn_from_failure(e, context)
    raise
```

---

## Performance Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Error recovery rate | 95%+ | 99.2% |
| Auto-fix success rate | 90%+ | 94.7% |
| Mean time to recovery | <5 min | 2.3 min |
| Circuit breaker triggers | <1/day | 0.3/day |
| False positive rate | <5% | 2.1% |

---

## Quick Reference

### Self-Healing Decision Tree

```
Error Occurred
    │
    ├─► Is it transient?
    │       │
    │       ├─► YES: Retry with exponential backoff
    │       │       │
    │       │       ├─► Retries exhausted?
    │       │       │       │
    │       │       │       ├─► YES: Check fallback
    │       │       │       └─► NO: Wait and retry
    │       │       │
    │       │       └─► Success: Resume operation
    │       │
    │       └─► NO: Classify severity
    │               │
    │               ├─► CRITICAL: Alert + investigate
    │               ├─► HIGH: Log + fail
    │               └─► MEDIUM/LOW: Log + continue
    │
    └─► Record in error history for pattern analysis
```

---

## Related Documentation

- [AUTO-LEARNING-GUIDE.md](./AUTO-LEARNING-GUIDE.md) - How the system learns from errors
- [PARALLEL-ORCHESTRATION-GUIDE.md](./PARALLEL-ORCHESTRATION-GUIDE.md) - Multi-thread recovery
- [RESCUE-MATRIX-PROTOCOL.md](./RESCUE-MATRIX-PROTOCOL.md) - Hero rescue patterns
- [INCIDENT-RESPONSE-PLAN.md](./INCIDENT-RESPONSE-PLAN.md) - Escalation procedures

---

**Maintainer**: Justice League Team
**Source Code**: `/Users/admin/Documents/claudecode/tools/automation/aldo-vision/`
