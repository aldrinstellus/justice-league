# Justice League Rollback Procedures

**Version**: 1.0.0
**Last Updated**: 2025-12-01
**Status**: Production Ready

---

## Overview

This document outlines the rollback procedures for the Justice League system. Rollbacks can be triggered automatically by the self-healing system or manually by Aldrin command.

---

## Rollback Types

| Type | Scope | Trigger | Recovery Time |
|------|-------|---------|---------------|
| **Hero Rollback** | Single hero | Hero failure rate >20% | <1 minute |
| **Module Rollback** | Subsystem | Module errors >10% | <5 minutes |
| **Full Rollback** | Entire system | P0 incident | <15 minutes |
| **Checkpoint Restore** | Data state | Data corruption | <10 minutes |

---

## Version Control System

### Hero Versioning

Oracle maintains version history for all heroes:

```json
{
  "agent_versions": {
    "Artemis": {
      "current": "2.1.0",
      "previous": ["2.0.3", "2.0.2", "2.0.1"],
      "stable": "2.0.3",
      "last_rollback": null
    },
    "Quicksilver": {
      "current": "1.0.3",
      "previous": ["1.0.2", "1.0.1", "1.0.0"],
      "stable": "1.0.2",
      "last_rollback": "2025-11-28T14:30:00Z"
    }
  }
}
```

### Checkpoints

Automatic checkpoints created:
- Before each mission start
- After successful mission completion
- Before hero upgrades
- Every 5 minutes during active operations

---

## Rollback Procedures

### 1. Hero Rollback

**When**: Single hero experiencing issues

```python
from core.justice_league import OracleMeta

oracle = OracleMeta()

# Roll back Artemis to previous stable version
oracle.rollback_agent(
    agent_name="Artemis",
    target_version="2.0.3",  # Or "stable" for last known good
    reason="Code generation accuracy dropped to 60%"
)
```

**Steps**:
1. Pause hero's active tasks
2. Save current state for analysis
3. Restore previous version
4. Run validation tests
5. Resume operations if tests pass

### 2. Module Rollback

**When**: Entire subsystem failing (e.g., parallel processing)

```bash
# Roll back parallel processing module
python3 scripts/rollback_module.py --module parallel_orchestration --version 1.9.6

# Verify rollback
python3 scripts/verify_module.py --module parallel_orchestration
```

**Affected Modules**:
- `parallel_orchestration`: Quicksilver, thread pools
- `visual_validation`: Green Arrow, Green Lantern
- `code_generation`: Artemis, Hephaestus
- `knowledge_management`: Oracle, learning systems

### 3. Full System Rollback

**When**: P0 incident affecting multiple components

```bash
# Emergency full rollback to last stable version
python3 scripts/emergency_rollback.py --target v1.9.6

# This will:
# 1. Pause all active missions
# 2. Save current state
# 3. Restore v1.9.6 codebase
# 4. Restore v1.9.6 knowledge base
# 5. Run full test suite
# 6. Resume operations if tests pass
```

### 4. Checkpoint Restore

**When**: Data corruption or state inconsistency

```python
oracle = OracleMeta()

# Restore to specific checkpoint
oracle.restore_checkpoint(
    checkpoint_id="CP-2025-12-01-093000",
    components=["knowledge_base", "agent_metrics", "mission_history"]
)

# Verify data integrity
validation = oracle.validate_data_integrity()
if validation["status"] == "OK":
    print("Checkpoint restore successful")
```

---

## Automatic Rollback Triggers

### Configuration

```python
ROLLBACK_CONFIG = {
    "hero_failure_threshold": 0.20,      # 20% failure rate
    "consecutive_failures": 5,           # 5 in a row
    "error_rate_threshold": 0.10,        # 10% errors
    "auto_rollback_enabled": True,       # Enable automatic rollbacks
    "require_approval_for_full": True    # Full rollback needs Aldrin approval
}
```

### Trigger Conditions

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Hero failure rate | >20% | Hero rollback |
| Consecutive failures | 5 | Hero rollback |
| Module error rate | >10% | Module rollback |
| P0 incident | Any | Full rollback (with approval) |
| Data corruption detected | Any | Checkpoint restore |

---

## Rollback Validation

### Post-Rollback Checks

```python
def validate_rollback(rollback_type: str, target: str) -> Dict:
    """Validate rollback was successful"""

    checks = {
        "version_correct": check_version(target),
        "tests_passing": run_validation_tests(target),
        "health_ok": check_health_status(),
        "no_regressions": check_for_regressions(),
        "data_integrity": validate_data()
    }

    return {
        "success": all(checks.values()),
        "checks": checks,
        "timestamp": datetime.now().isoformat()
    }
```

### Test Suite After Rollback

```bash
# Run critical path tests
python3 run_all_justice_league_tests.py --suite critical

# Check hero health
python3 scripts/check_hero_health.py --all

# Verify Oracle knowledge base
python3 scripts/verify_oracle.py
```

---

## Recovery from Failed Rollback

### If Rollback Fails

1. **Isolate**: Disable affected components
2. **Analyze**: Review rollback logs for cause
3. **Manual Restore**: Use backup files directly
4. **Escalate**: Notify Aldrin for command decision

### Manual Restore Procedure

```bash
# 1. Stop all services
pkill -f "justice_league"

# 2. Restore from backup
cp -r /backups/justice-league-v1.9.6/* /path/to/justice-league/

# 3. Restore knowledge base
cp /backups/oracle_kb_v1.9.6.json /tmp/aldo-vision-justice-league/oracle/

# 4. Restart services
python3 main.py --mode production
```

---

## Rollback History

Oracle maintains complete rollback history:

```json
{
  "rollback_history": [
    {
      "id": "RB-001",
      "timestamp": "2025-11-28T14:30:00Z",
      "type": "hero",
      "target": "Quicksilver",
      "from_version": "1.0.2",
      "to_version": "1.0.1",
      "reason": "Rate limiting issues in v1.0.2",
      "success": true,
      "validated": true
    }
  ]
}
```

---

## Best Practices

### 1. Always Create Checkpoint Before Changes

```python
oracle.create_checkpoint(
    description="Before Artemis 2.1.0 upgrade",
    components=["all"]
)
```

### 2. Test Rollback Capability Regularly

```bash
# Weekly rollback drill
python3 scripts/rollback_drill.py --dry-run
```

### 3. Keep Previous Versions Available

- Maintain last 5 versions for each hero
- Keep last 20 checkpoints
- Archive older versions monthly

### 4. Document Every Rollback

```python
oracle.log_rollback(
    type="hero",
    target="Artemis",
    reason="Accuracy regression in 2.1.0",
    impact="3 missions delayed",
    lessons_learned=["Need more testing for accuracy metrics"]
)
```

---

## Related Documentation

- [INCIDENT-RESPONSE-PLAN.md](./INCIDENT-RESPONSE-PLAN.md) - When to trigger rollback
- [SELF-HEALING-GUIDE.md](../guides/SELF-HEALING-GUIDE.md) - Automatic recovery before rollback
- [ERROR-HANDLING-PROCEDURES.md](./ERROR-HANDLING-PROCEDURES.md) - Error classification

---

**Maintainer**: Justice League Team
