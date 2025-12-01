# Justice League Error Handling Procedures

**Version**: 1.0.0
**Last Updated**: 2025-12-01
**Status**: Production Ready

---

## Overview

This document defines error classification, handling strategies, and recovery procedures for the Justice League system.

---

## Error Classification

### Severity Levels

| Level | Name | Recovery | Examples |
|-------|------|----------|----------|
| **CRITICAL** | System-threatening | Immediate | MemoryError, SystemExit |
| **HIGH** | Major functionality broken | <5 min | ValueError, TypeError |
| **MEDIUM** | Partial failure, recoverable | Auto-retry | Timeout, ConnectionError |
| **LOW** | Minor issue, continue | Log only | DeprecationWarning |

### Error Categories

| Category | Description | Default Action |
|----------|-------------|----------------|
| **Transient** | Temporary, likely to resolve | Retry with backoff |
| **Permanent** | Will not resolve on retry | Fail fast, log |
| **Configuration** | Setup/config issue | Alert, require fix |
| **Resource** | Memory, disk, CPU | Scale/cleanup |
| **External** | Third-party API | Fallback or wait |

---

## Error Classification Matrix

```python
ERROR_CLASSIFICATION = {
    # Transient - Retry
    "TimeoutError": {"severity": "MEDIUM", "category": "transient", "max_retries": 3},
    "ConnectionError": {"severity": "MEDIUM", "category": "transient", "max_retries": 3},
    "requests.Timeout": {"severity": "MEDIUM", "category": "transient", "max_retries": 5},
    "HTTPError429": {"severity": "MEDIUM", "category": "external", "max_retries": 1, "wait": "Retry-After"},

    # Permanent - Fail Fast
    "ValueError": {"severity": "HIGH", "category": "permanent", "max_retries": 0},
    "TypeError": {"severity": "HIGH", "category": "permanent", "max_retries": 0},
    "KeyError": {"severity": "HIGH", "category": "permanent", "max_retries": 0},
    "JSONDecodeError": {"severity": "HIGH", "category": "permanent", "max_retries": 0},

    # Critical - Alert
    "MemoryError": {"severity": "CRITICAL", "category": "resource", "action": "alert_and_cleanup"},
    "SystemError": {"severity": "CRITICAL", "category": "permanent", "action": "alert_and_stop"},
    "OSError": {"severity": "HIGH", "category": "resource", "action": "check_disk_space"},

    # Configuration - Require Fix
    "KeyError(FIGMA_TOKEN)": {"severity": "HIGH", "category": "configuration", "action": "halt"},
    "ModuleNotFoundError": {"severity": "HIGH", "category": "configuration", "action": "halt"}
}
```

---

## Handling Procedures

### Transient Error Handling

```python
def handle_transient_error(error: Exception, context: Dict) -> Any:
    """Handle transient errors with exponential backoff retry"""

    config = ERROR_CLASSIFICATION.get(type(error).__name__, DEFAULT_CONFIG)
    max_retries = config.get("max_retries", 3)
    base_delay = config.get("base_delay", 1.0)

    for attempt in range(max_retries + 1):
        try:
            return context["operation"]()
        except type(error) as e:
            if attempt == max_retries:
                raise MaxRetriesExceeded(f"Failed after {max_retries} retries: {e}")

            delay = base_delay * (2 ** attempt)  # Exponential backoff
            logger.warning(f"Retry {attempt + 1}/{max_retries} after {delay}s: {e}")
            time.sleep(delay)
```

### Permanent Error Handling

```python
def handle_permanent_error(error: Exception, context: Dict) -> None:
    """Handle permanent errors - fail fast, log, learn"""

    # Log detailed error
    logger.error(f"Permanent error: {type(error).__name__}: {error}")

    # Record for learning
    oracle.store_error_solution(
        agent_name=context.get("hero", "Unknown"),
        error_type=type(error).__name__,
        error_details={
            "message": str(error),
            "traceback": traceback.format_exc(),
            "context": context
        },
        solution="pending_analysis",
        context=context
    )

    # Check if known solution exists
    solutions = oracle.query_error_solutions({
        "type": type(error).__name__,
        "message": str(error)
    })

    if solutions and solutions[0]["confidence"] > 0.9:
        logger.info(f"Known solution found: {solutions[0]['solution']}")
        raise PermanentErrorWithSolution(error, solutions[0])

    raise error
```

### Critical Error Handling

```python
def handle_critical_error(error: Exception, context: Dict) -> None:
    """Handle critical errors - immediate response required"""

    # 1. Stop all operations
    superman.pause_all_missions()

    # 2. Alert Aldrin
    notification = {
        "severity": "CRITICAL",
        "error": str(error),
        "timestamp": datetime.now().isoformat(),
        "affected_heroes": context.get("heroes", []),
        "action_required": True
    }
    aldrin.notify(notification)

    # 3. Trigger emergency procedures
    if isinstance(error, MemoryError):
        emergency_cleanup()
    elif isinstance(error, SystemError):
        save_state_and_halt()

    # 4. Log for post-mortem
    oracle.log_critical_incident(error, context)
```

---

## Error Recovery Strategies

### Strategy 1: Retry with Backoff

```
Attempt 1: Immediate
Attempt 2: Wait 1s
Attempt 3: Wait 2s
Attempt 4: Wait 4s
Failed: Escalate or fail
```

### Strategy 2: Fallback to Alternative

```python
def execute_with_fallback(primary_operation, fallback_operation):
    try:
        return primary_operation()
    except TransientError:
        logger.warning("Primary failed, trying fallback")
        return fallback_operation()
```

### Strategy 3: Graceful Degradation

```python
def graceful_degradation(full_operation, minimal_operation):
    try:
        return full_operation()  # Full functionality
    except ResourceError:
        logger.warning("Resources limited, using minimal mode")
        return minimal_operation()  # Reduced functionality
```

### Strategy 4: Circuit Breaker

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failures = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def execute(self, operation):
        if self.state == "OPEN":
            raise CircuitOpenError("Circuit is open, try later")

        try:
            result = operation()
            self.record_success()
            return result
        except Exception as e:
            self.record_failure()
            raise
```

---

## Hero-Specific Error Handling

### Artemis (Code Generation)

| Error | Cause | Solution |
|-------|-------|----------|
| Low accuracy | Complex layout | Switch to Image-to-HTML |
| Missing component | shadcn not installed | Install missing component |
| Invalid JSX | Syntax error | Run through linter |

### Quicksilver (Parallel Export)

| Error | Cause | Solution |
|-------|-------|----------|
| Rate limit (429) | Too many requests | Wait, reduce batch size |
| Timeout | Large file | Increase timeout, retry |
| Connection reset | Network issue | Retry with backoff |

### Oracle (Knowledge Management)

| Error | Cause | Solution |
|-------|-------|----------|
| JSON corruption | Write interrupted | Restore from backup |
| Query timeout | Large dataset | Add indexes, paginate |
| Memory error | Too much history | Prune old entries |

---

## Error Logging Standards

### Log Format

```
[TIMESTAMP] [LEVEL] [HERO] [ERROR_TYPE]: Message
Context: {...}
Stack: ...
```

### Example

```
[2025-12-01T10:30:00Z] [ERROR] [Quicksilver] [TimeoutError]: Figma API request timed out after 60s
Context: {"file_key": "RSMfJWl...", "frame_id": "17:1440", "attempt": 3}
Stack: File "quicksilver_speed_export.py", line 245, in export_frame...
```

### Required Fields

- Timestamp (ISO 8601)
- Severity level
- Hero name
- Error type
- Error message
- Context (operation, parameters)
- Stack trace (for HIGH and CRITICAL)

---

## Error Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Error rate | <2% | >5% |
| Critical errors | 0/day | Any |
| Mean time to recovery | <5 min | >15 min |
| Unhandled exceptions | 0 | Any |
| Retry success rate | >80% | <60% |

---

## Related Documentation

- [SELF-HEALING-GUIDE.md](../guides/SELF-HEALING-GUIDE.md) - Automatic recovery
- [INCIDENT-RESPONSE-PLAN.md](./INCIDENT-RESPONSE-PLAN.md) - Escalation
- [ROLLBACK-PROCEDURES.md](./ROLLBACK-PROCEDURES.md) - Version rollback

---

**Maintainer**: Justice League Team
