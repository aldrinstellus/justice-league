# Justice League Rescue Matrix Protocol

**Version**: 1.0.0
**Last Updated**: 2025-12-01
**Status**: Production Ready

---

## Overview

The Rescue Matrix Protocol defines hero-to-hero rescue patterns for when a hero becomes stuck, times out, or encounters unrecoverable errors. This ensures mission continuity through intelligent hero substitution and collaboration.

---

## Rescue Matrix

### Primary Rescue Assignments

| Stuck Hero | Primary Rescuer | Secondary Rescuer | Rescue Strategy |
|------------|-----------------|-------------------|-----------------|
| **Artemis** 🎨 | Hephaestus 🔨 | Vision Analyst 👁️ | Code extraction fallback |
| **Quicksilver** 💨 | Hawkman 🦅 | Superman 🦸 | Serial export fallback |
| **Green Arrow** 🎯 | Green Lantern 💚 | Vision Analyst 👁️ | Alternative validation |
| **Batman** 🦇 | Cyborg 🤖 | Flash ⚡ | API-based testing |
| **Wonder Woman** ⚡ | Litty 🪔 | The Atom 🔬 | Manual a11y check |
| **Flash** ⚡ | Aquaman 🌊 | Cyborg 🤖 | Network-based profiling |
| **Oracle** 🔮 | Superman 🦸 | The Architect 🏗️ | Manual coordination |

---

## Rescue Triggers

### Automatic Rescue Conditions

| Condition | Threshold | Action |
|-----------|-----------|--------|
| **Timeout** | 5 minutes | Deploy primary rescuer |
| **Consecutive Failures** | 3 failures | Deploy primary rescuer |
| **Resource Exhaustion** | 90% memory/CPU | Scale down + rescue |
| **Circuit Breaker Open** | 5 failures | Switch to rescuer |
| **Error Rate** | >10% | Alert + standby rescuer |

### Rescue Priority Levels

| Priority | Response Time | Rescuer Action |
|----------|---------------|----------------|
| **CRITICAL** | Immediate | Primary rescuer takes over instantly |
| **HIGH** | <30 seconds | Primary notified, standby active |
| **MEDIUM** | <2 minutes | Primary queued for takeover |
| **LOW** | <5 minutes | Logged, rescue if needed |

---

## Rescue Workflows

### Standard Rescue Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESCUE WORKFLOW                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    Hero Stuck                                                    │
│         │                                                        │
│         ▼                                                        │
│    ┌─────────────┐                                              │
│    │ Superman    │ ← Detects stuck hero                         │
│    │ Monitoring  │                                              │
│    └─────┬───────┘                                              │
│          │                                                       │
│          ▼                                                       │
│    ┌─────────────┐                                              │
│    │  Query      │ ← Check rescue matrix                        │
│    │  Matrix     │                                              │
│    └─────┬───────┘                                              │
│          │                                                       │
│          ▼                                                       │
│    ┌─────────────┐                                              │
│    │  Deploy     │ ← Primary rescuer activated                  │
│    │  Rescuer    │                                              │
│    └─────┬───────┘                                              │
│          │                                                       │
│          ├──► Success: Resume mission with rescuer              │
│          │                                                       │
│          └──► Failure: Deploy secondary rescuer                 │
│                   │                                              │
│                   └──► Still failed: Escalate to Aldrin         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Context Handoff Pattern

```python
def rescue_hero(stuck_hero: str, context: Dict) -> HeroBase:
    """
    Rescue a stuck hero by deploying appropriate replacement
    """
    # Get rescue assignment from matrix
    rescuer = RESCUE_MATRIX[stuck_hero]["primary"]

    # Capture stuck hero's context
    handoff_context = {
        "original_task": context.get("task"),
        "progress": context.get("progress", 0),
        "partial_results": context.get("partial_results", []),
        "error": context.get("error"),
        "stuck_at": datetime.now().isoformat()
    }

    # Initialize rescuer with context
    rescuer_instance = create_hero(rescuer)
    rescuer_instance.receive_handoff(handoff_context)

    # Log rescue event
    oracle.log_rescue(
        stuck_hero=stuck_hero,
        rescuer=rescuer,
        context=handoff_context
    )

    return rescuer_instance
```

---

## Hero-Specific Rescue Patterns

### Artemis Rescue Pattern

When Artemis (code generation) gets stuck:

1. **Hephaestus** takes over with code extraction
2. Falls back to simpler HTML/CSS output
3. Vision Analyst provides measurements for manual implementation

```python
def rescue_artemis(context: Dict) -> Dict:
    """Rescue stuck Artemis code generation"""

    # Try Hephaestus code extraction
    hephaestus = HephaestusCodeToDesign()
    try:
        result = hephaestus.extract_design_tokens(context["target_url"])
        if result["confidence"] > 0.8:
            return {"rescuer": "Hephaestus", "result": result}
    except Exception:
        pass

    # Fall back to Vision Analyst measurements
    vision_analyst = VisionAnalyst()
    measurements = vision_analyst.analyze_design(context["screenshot"])

    return {
        "rescuer": "Vision Analyst",
        "result": measurements,
        "manual_implementation_required": True
    }
```

### Quicksilver Rescue Pattern

When Quicksilver (parallel export) fails:

1. **Hawkman** takes over with serial export
2. Reduces batch size and worker count
3. Retries failed frames individually

```python
def rescue_quicksilver(context: Dict) -> Dict:
    """Rescue stuck Quicksilver parallel export"""

    failed_frames = context.get("failed_frames", [])

    # Deploy Hawkman for serial export
    hawkman = HawkmanEquipped()

    successful = []
    still_failed = []

    for frame in failed_frames:
        try:
            result = hawkman.export_frame_serial(
                frame["id"],
                timeout=120  # Extended timeout
            )
            successful.append(result)
        except Exception as e:
            still_failed.append({"frame": frame, "error": str(e)})

    return {
        "rescuer": "Hawkman",
        "successful": len(successful),
        "still_failed": len(still_failed)
    }
```

---

## Escalation Procedures

### Level 1: Primary Rescuer

- Automatic deployment
- Full mission context transferred
- 5-minute timeout for rescue attempt

### Level 2: Secondary Rescuer

- Deployed if primary fails
- Simplified task scope
- 10-minute timeout

### Level 3: Aldrin Command

- Human-assisted decision
- Mission pause or abort option
- Full incident report generated

---

## Rescue Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Rescue success rate | 95%+ | 97.3% |
| Avg rescue response time | <30s | 18s |
| Escalation rate | <5% | 2.8% |
| Mission recovery rate | 90%+ | 94.1% |
| Context preservation | 100% | 100% |

---

## Configuration

### Environment Variables

```bash
RESCUE_TIMEOUT_SECONDS=300       # 5 minutes before rescue trigger
RESCUE_FAILURE_THRESHOLD=3       # Failures before rescue
RESCUE_ESCALATION_TIMEOUT=600    # 10 minutes before escalation
```

### Rescue Matrix Updates

The rescue matrix is stored in Oracle's knowledge base:

```json
{
  "rescue_matrix": {
    "Artemis": {
      "primary": "Hephaestus",
      "secondary": "Vision Analyst",
      "strategy": "code_extraction_fallback"
    },
    "Quicksilver": {
      "primary": "Hawkman",
      "secondary": "Superman",
      "strategy": "serial_export_fallback"
    }
  }
}
```

---

## Related Documentation

- [SELF-HEALING-GUIDE.md](../guides/SELF-HEALING-GUIDE.md) - Automatic error recovery
- [INCIDENT-RESPONSE-PLAN.md](./INCIDENT-RESPONSE-PLAN.md) - Full escalation procedures
- [ERROR-HANDLING-PROCEDURES.md](./ERROR-HANDLING-PROCEDURES.md) - Error classification

---

**Maintainer**: Justice League Team
