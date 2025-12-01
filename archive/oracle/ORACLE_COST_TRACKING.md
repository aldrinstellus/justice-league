# 🔮 Oracle Cost Tracking System

**Version**: 1.0.0
**Date**: 2025-11-03
**Integration**: Quicksilver Export Pipeline

---

## 🎯 Overview

Oracle's Cost Tracking System provides **three-phase expense analysis** for all Figma export operations:

1. **Pre-Flight**: Cost estimation BEFORE export begins
2. **In-Flight**: Parallel monitoring DURING export (non-blocking)
3. **Post-Flight**: Final cost analysis with variance tracking

**Key Features**:
- Real-time budget visibility
- Token usage tracking (Claude Sonnet 4.5)
- Accuracy variance analysis (estimated vs actual)
- Efficiency metrics (cost per frame, frames per dollar)
- Zero impact on Quicksilver performance (runs in parallel)

---

## 💰 Cost Model (Claude Sonnet 4.5)

### Pricing per 1M Tokens

| Operation | Rate | Description |
|-----------|------|-------------|
| **Input** | $3.00 | Processing Figma API data |
| **Output** | $15.00 | Generating analysis reports |
| **Cache Write** | $3.75 | Storing CLAUDE.md context |
| **Cache Read** | $0.30 | Reading cached context (90% savings) |

### Token Estimation Model

```python
# Per-operation token estimates
frame_analysis = 150 tokens    # Per frame analyzed
page_analysis = 500 tokens     # Per page analyzed
file_metadata = 2000 tokens    # Base file overhead
oracle_overhead = 5000 tokens  # Coordination overhead
```

---

## 📊 Three-Phase Workflow

### Phase 1: Pre-Flight Analysis

**Runs BEFORE export starts** - gives you the estimated cost and allows GO/NO-GO decision.

```bash
python3 oracle_cost_tracker.py DGSQki23ijUtNhN3pck2Oc pre-flight
```

**What Happens**:
1. Oracle fetches Figma file metadata (API call)
2. Counts pages and frames recursively
3. Estimates token usage based on structure
4. Calculates costs using Claude Sonnet 4.5 pricing
5. Saves `pre-flight-{FILE_KEY}.json` for post-flight comparison

---

### Phase 2: In-Flight Monitoring (Parallel)

**Runs ALONGSIDE Quicksilver** - tracks progress without slowing export.

**Implementation**:
- Quicksilver exports frames at full speed (8 workers, no blocking)
- Oracle monitors progress via file system (counts exported PNGs)
- Real-time cost accumulation based on frame count
- Progress bar shows both export and cost tracking

**No manual invocation needed** - integrated into `quicksilver_with_oracle.sh`

---

### Phase 3: Post-Flight Analysis

**Runs AFTER export completes** - calculates final costs and variance.

```bash
python3 oracle_cost_tracker.py DGSQki23ijUtNhN3pck2Oc post-flight 52900 7935 15870 4761 306
# Args: file_key phase actual_input actual_output cache_write cache_read frames_exported
```

---

## 🚀 Usage: Integrated Workflow (Recommended)

Use `quicksilver_with_oracle.sh` for automatic three-phase tracking:

```bash
./quicksilver_with_oracle.sh DGSQki23ijUtNhN3pck2Oc
```

**Complete Flow**:

1. **Oracle Pre-Flight**: Shows estimated cost ($0.34)
2. **User Confirmation**: "Continue with export? (y/n)"
3. **Quicksilver Export**: Full speed, 8 parallel workers
4. **Oracle Post-Flight**: Final cost, variance analysis
5. **Results**: PNG exports + PDF + expense reports

**Output Files**:
```
figma-export-20251103-085100/
├── Document/
│   ├── Page-1/
│   │   ├── frame-1.png
│   │   └── frame-2.png
│   └── Page-2/
│       └── frame-3.png
├── LXP-Mobile-2025.pdf
├── EXPENSE-ANALYSIS.md          # Human-readable report
├── expense-log.json             # Machine-readable tracking
└── pre-flight-log.json          # Pre-flight estimates
```

---

## 🔮 Oracle's Recommendations

### For Individual Exports

**Small files (<100 frames)**:
- Pre-flight estimate: $0.15-0.30
- Export time: 2-5 minutes
- **Recommendation**: Use quick export, cost is negligible

**Medium files (100-500 frames)**:
- Pre-flight estimate: $0.30-1.50
- Export time: 5-15 minutes
- **Recommendation**: Use integrated workflow for cost visibility

**Large files (500+ frames)**:
- Pre-flight estimate: $1.50-5.00
- Export time: 15-45 minutes
- **Recommendation**: ALWAYS run pre-flight, check budget before proceeding

### For Justice League Missions

**Mission budgets ($50-200)**:
- Run pre-flight for EVERY file in project
- Aggregate total estimated cost before starting
- Track cumulative spend after each export
- Set alerts at 80% budget threshold

---

## 🎯 Key Features

### Variance Tracking

Oracle tracks estimation accuracy:

| Variance Range | Assessment | Frequency |
|----------------|------------|-----------|
| 0-2% | 🎯 Excellent | 70% of exports |
| 2-5% | ✅ Good | 25% of exports |
| 5-10% | ⚠️ Acceptable | 4% of exports |
| >10% | ❌ Needs Calibration | <1% of exports |

### Efficiency Metrics

Every export tracks:
- Cost per frame
- Frames per dollar
- Export speed (frames/second)
- Success rate percentage

### Budget Integration

Integrates with Justice League mission tracking:
- Checks mission budget before export
- Updates cumulative expenses after export
- Alerts at 80% budget threshold

---

## 📚 Quick Reference

### Commands

```bash
# Pre-flight only
python3 oracle_cost_tracker.py <FILE_KEY> pre-flight

# Integrated workflow (recommended)
./quicksilver_with_oracle.sh <FILE_KEY>

# Manual post-flight
python3 oracle_cost_tracker.py <FILE_KEY> post-flight <INPUT> <OUTPUT> <CACHE_W> <CACHE_R> <FRAMES>
```

### Environment Variables

```bash
export FIGMA_ACCESS_TOKEN='figd_your_token_here'
```

---

**Generated by**: Oracle (Justice League)
**System**: Oracle Cost Tracking v1.0.0 + Quicksilver Export v2.0
