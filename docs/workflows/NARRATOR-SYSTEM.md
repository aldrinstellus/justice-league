# Narrator System Documentation

**Version**: 1.0.0
**Last Updated**: 2025-12-01
**Status**: Production Ready

---

## Overview

The Narrator System provides real-time progress reporting and mission storytelling for Justice League operations. It creates human-readable logs that track agent activities, decisions, and outcomes.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    NARRATOR SYSTEM                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Event     │───▶│  Narrator   │───▶│   Output    │     │
│  │  Collector  │    │   Engine    │    │  Formatter  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│        │                  │                  │              │
│        ▼                  ▼                  ▼              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Agent     │    │  Template   │    │    Log      │     │
│  │  Monitors   │    │   Library   │    │   Writers   │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Components

### 1. Event Collector

Captures events from all Justice League agents:

| Event Type | Source | Priority |
|------------|--------|----------|
| `mission.start` | Superman | High |
| `task.begin` | Any Hero | Medium |
| `task.complete` | Any Hero | Medium |
| `error.detected` | Batman | High |
| `recovery.started` | Self-Healing | High |
| `optimization.found` | Oracle | Low |

### 2. Narrator Engine

Transforms raw events into narrative text:

```python
def narrate_event(event):
    """Convert event to human-readable narrative."""
    templates = {
        'mission.start': "🦸 Superman activated mission: {mission_name}",
        'task.begin': "⚡ {hero} began: {task_description}",
        'task.complete': "✅ {hero} completed: {task_description} ({duration})",
        'error.detected': "🚨 Batman detected: {error_type}",
        'recovery.started': "🔧 Self-healing initiated: {recovery_action}",
        'optimization.found': "💡 Oracle suggests: {optimization}"
    }
    return templates[event.type].format(**event.data)
```

### 3. Output Formatter

Formats narratives for different outputs:

| Format | Use Case | Example |
|--------|----------|---------|
| Console | Real-time monitoring | Colored terminal output |
| Markdown | Mission logs | `mission-log.md` files |
| JSON | API responses | Structured data |
| HTML | Dashboards | Rich web display |

---

## Event Categories

### Mission Events

```markdown
🦸 **Mission Start**: Superman activated JL-003-auzmor-learn
📋 **Scope**: 100+ Figma files, 14 weeks, $125 budget
👥 **Heroes Assigned**: Quicksilver, Artemis, Vision Analyst
```

### Progress Events

```markdown
⚡ **Quicksilver** processing file 47/100 (47%)
   └── Current: dashboard-v2.fig
   └── Speed: 6.2x baseline
   └── ETA: 12 minutes remaining
```

### Error Events

```markdown
🚨 **Error Detected**: Rate limit exceeded
   └── Source: Figma API
   └── Severity: P2 (Degraded)
   └── Auto-recovery: Enabled
   └── Action: Exponential backoff initiated
```

### Recovery Events

```markdown
🔧 **Self-Healing**: Recovery successful
   └── Error: Rate limit exceeded
   └── Strategy: Exponential backoff
   └── Duration: 45 seconds
   └── Result: Operation resumed
```

---

## Configuration

### narrator-config.json

```json
{
  "version": "1.0.0",
  "output": {
    "console": true,
    "file": true,
    "api": false
  },
  "verbosity": "normal",
  "include_timestamps": true,
  "emoji_enabled": true,
  "formats": {
    "default": "markdown",
    "error": "detailed",
    "summary": "compact"
  },
  "filters": {
    "min_priority": "low",
    "exclude_types": []
  }
}
```

### Verbosity Levels

| Level | Description | Use Case |
|-------|-------------|----------|
| `quiet` | Errors only | Production |
| `normal` | Key events | Default |
| `verbose` | All events | Debugging |
| `debug` | Full traces | Development |

---

## Integration

### With Mission Logs

Narrator automatically updates mission-log.md:

```markdown
## Mission Log: JL-003

### 2025-12-01 10:30:00
🦸 Mission activated by Superman
- Budget: $125.00
- Timeline: 14 weeks
- Heroes: 5 assigned

### 2025-12-01 10:31:00
⚡ Quicksilver began Figma export
- Files queued: 100
- Export format: PNG @ 2x

### 2025-12-01 11:15:00
✅ Quicksilver completed Phase 1
- Files processed: 100
- Success rate: 98%
- Duration: 45 minutes
```

### With Expense Tracking

```markdown
💰 **Cost Update**:
   └── Activity: Figma export batch
   └── Tokens: 125,000 input / 45,000 output
   └── Cost: $0.52
   └── Running total: $12.45 / $125.00
```

---

## Templates

### Mission Start Template

```markdown
# 🦸 Mission Activated

**Mission ID**: {mission_id}
**Name**: {mission_name}
**Started**: {timestamp}

## Objective
{objective}

## Resources
- **Budget**: ${budget}
- **Timeline**: {timeline}
- **Heroes**: {hero_count} assigned

## Initial Status
- [ ] Planning complete
- [ ] Resources allocated
- [ ] Tracking initialized
```

### Task Completion Template

```markdown
## ✅ Task Complete: {task_name}

**Hero**: {hero}
**Duration**: {duration}
**Status**: {status}

### Results
{results}

### Metrics
- Files processed: {file_count}
- Success rate: {success_rate}%
- Cost: ${cost}
```

---

## API Reference

### NarratorService

```typescript
interface NarratorService {
  // Start narrating a mission
  startMission(missionId: string): void;

  // Log an event
  logEvent(event: NarratorEvent): void;

  // Get mission narrative
  getNarrative(missionId: string): string;

  // Subscribe to live updates
  subscribe(callback: (event: NarratorEvent) => void): void;
}

interface NarratorEvent {
  type: EventType;
  hero: string;
  timestamp: Date;
  data: Record<string, any>;
  priority: 'low' | 'medium' | 'high';
}
```

---

## Best Practices

### 1. Event Naming

```
✅ Good: "export.batch.complete"
❌ Bad: "done"
```

### 2. Data Inclusion

Always include:
- Timestamp
- Hero/agent source
- Relevant metrics
- Context for errors

### 3. Verbosity Balance

- Console: Key milestones only
- File logs: Detailed for audit
- API: Minimal for performance

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Missing events | Filter too strict | Adjust min_priority |
| Log too verbose | Debug mode on | Set verbosity to "normal" |
| Timestamps wrong | Timezone issue | Use UTC internally |
| Emoji not showing | Terminal encoding | Set UTF-8 encoding |

---

## See Also

- [Hero Autonomy](./HERO-AUTONOMY.md) - How heroes operate independently
- [Mission Coordination](./MISSION-COORDINATION.md) - Multi-hero orchestration
- [Error Handling](../protocols/ERROR-HANDLING-PROCEDURES.md) - Error event handling

---

**Maintainer**: Justice League Team
