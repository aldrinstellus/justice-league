# Figma Export Decision Tree

**Purpose**: Quick decision guide for choosing the right export approach
**Based on**: JL-004 learnings (182 files, 24,820 frames, 99% savings)
**Updated**: 2025-11-05

---

## Quick Decision Flowchart

```
START: Need to export Figma files
│
├─ Q1: How many Figma Pro accounts do you have?
│   │
│   ├─ 1 account
│   │   └─→ [Continue to Q2: Budget]
│   │
│   └─ 2+ accounts
│       └─→ [Skip to PARALLEL PATH]
│
├─ Q2: What's your budget?
│   │
│   ├─ <$10
│   │   └─→ [DIRECT API: $1]
│   │
│   ├─ $10-$100
│   │   └─→ [Continue to Q3: Timeline]
│   │
│   └─ >$100
│       └─→ [Continue to Q4: Urgency]
│
├─ Q3: What's your timeline?
│   │
│   ├─ >24 hours
│   │   └─→ [DIRECT API: $1, 13-14h]
│   │
│   ├─ 12-24 hours
│   │   └─→ [Continue to Q4: Urgency]
│   │
│   └─ <12 hours
│       └─→ [PAID SERVICE: $95-136, 3-4h]
│
├─ Q4: How urgent is this?
│   │
│   ├─ Can wait overnight
│   │   └─→ [DIRECT API: $1, 13-14h]
│   │
│   ├─ Need within business day
│   │   └─→ [Continue to Q5: Frame count]
│   │
│   └─ Emergency (same day)
│       └─→ [PAID SERVICE: $95-136, 3-4h]
│
├─ Q5: How many frames to export?
│   │
│   ├─ <5,000 frames
│   │   └─→ [Either approach works]
│   │       ├─ Budget priority → [DIRECT API: $1]
│   │       └─ Time priority → [PAID SERVICE: ~$27]
│   │
│   ├─ 5,000-15,000 frames
│   │   └─→ [DIRECT API recommended: $1 vs $40-80]
│   │
│   └─ >15,000 frames
│       └─→ [DIRECT API strongly recommended: $1 vs $95+]
│
└─ Q6: Is this recurring?
    │
    ├─ One-time export
    │   └─→ [Consider paid service (no setup)]
    │
    ├─ 2-5 times/year
    │   └─→ [DIRECT API: Setup worth it]
    │
    └─ Weekly/monthly
        └─→ [DIRECT API + PARALLEL: Maximum efficiency]

PARALLEL PATH (for 2+ accounts):
│
├─ Q7: What hardware do you have?
│   │
│   ├─ <8 cores, <16GB RAM
│   │   └─→ [Sequential with best account]
│   │
│   ├─ 8-10 cores, 16-32GB RAM
│   │   └─→ [PARALLEL BASIC: 6x speedup, FREE]
│   │
│   └─ 10+ cores, 32GB+ RAM
│       └─→ [PARALLEL OPTIMIZED: 18x speedup, $5]
│
END: Decision made!
```

---

## Common Scenarios

### Scenario 1: Research Project (Budget Tight)

**Context**:
- Non-profit or academic
- Budget: <$50/month
- Timeline: Flexible (can wait days)
- Files: 100+ files, 15,000+ frames
- Recurring: Monthly audits

**Decision Path**:
```
Q1: 1 account → Q2: <$10 → DIRECT API
```

**Recommendation**: ✅ **Direct API ($1)**
- Cost: $1.00 Oracle
- Time: 13-15 hours (overnight)
- Success: 98-99%
- ROI: 99% savings vs paid

---

### Scenario 2: Client Deliverable (Deadline Tomorrow)

**Context**:
- Agency work for client
- Budget: $500 (billable)
- Timeline: 24 hours (hard deadline)
- Files: 50 files, 8,000 frames
- Recurring: No (one-time)

**Decision Path**:
```
Q1: 1 account → Q2: >$100 → Q3: <24h → Q4: Need within business day → PAID SERVICE
```

**Recommendation**: ✅ **Paid Service ($44)**
- Cost: $44 (billed to client)
- Time: 3-4 hours
- Success: 99%+
- Justification: Client deadline + budget allows

---

### Scenario 3: Design System Audit (Monthly)

**Context**:
- Internal design team
- Budget: $200/month allocated
- Timeline: Week to complete
- Files: 80 files, 12,000 frames
- Recurring: Monthly (12 times/year)

**Decision Path**:
```
Q1: 1 account → Q6: Weekly/monthly → DIRECT API + consider PARALLEL
```

**Recommendation**: ✅ **Direct API ($1) → then PARALLEL**
- **First Month**: Direct API ($1, 13-15h)
  - Validate process
  - Test success rate
  - Baseline metrics
- **Second Month**: Set up Parallel (if 2+ accounts)
  - Setup: $50 one-time
  - Per export: $0, 2-3 hours
  - ROI: 12 months × $75 saved = $900/year

---

### Scenario 4: Startup MVP (Fast Iteration)

**Context**:
- Startup product team
- Budget: $1,000/month (burn rate)
- Timeline: Need fast iterations
- Files: 30 files, 5,000 frames
- Recurring: Weekly sprints

**Decision Path**:
```
Q1: 1 account → Q5: <5,000 frames → Q6: Weekly → Consider either
```

**Recommendation**: ⚖️ **Hybrid Approach**
- **Weekly exports**: Direct API ($1, 7-8h overnight)
- **Emergency exports**: Paid Service ($27, 2-3h same day)
- **Annual Cost**: 52 × $1 + 10 × $27 = $322/year
  - vs all paid: 62 × $27 = $1,674/year
  - **Savings**: $1,352/year (81%)

---

### Scenario 5: Enterprise Design System (Massive Scale)

**Context**:
- Fortune 500 company
- Budget: Unlimited (approved)
- Timeline: Quarterly audits
- Files: 200+ files, 30,000+ frames
- Recurring: Quarterly (4 times/year)

**Decision Path**:
```
Q1: 6 accounts (enterprise team) → PARALLEL PATH → Q7: 10+ cores → PARALLEL OPTIMIZED
```

**Recommendation**: ✅ **Parallel Optimized ($5)**
- Setup: $150 one-time (engineer time)
- Per export: $5 cloud, 45 minutes
- Annual: 4 × $5 = $20
- vs Sequential: 4 × 13h = 52 hours saved/year
- vs Paid: 4 × $165 = $660 saved/year
- **ROI**: 33x ($660 saved, $20 spent)

---

## Decision Matrix

### Budget × Timeline Matrix

| Budget | <12h | 12-24h | >24h |
|--------|------|--------|------|
| **<$10** | ❌ Not possible | ⚠️ Direct API (stretch) | ✅ Direct API ($1) |
| **$10-$50** | ❌ Not possible | ⚠️ Paid if small (<5K frames) | ✅ Direct API ($1) |
| **$50-$100** | ⚠️ Paid if urgent | ⚖️ Either approach | ✅ Direct API ($1) |
| **>$100** | ✅ Paid Service | ✅ Paid Service | ⚖️ Either (time vs cost) |

### Frame Count × Budget Matrix

| Frames | <$10 | $10-$50 | $50-$100 | >$100 |
|--------|------|---------|----------|-------|
| **<5,000** | ✅ Direct ($1) | ✅ Direct ($1) | ⚖️ Either | ✅ Paid (~$27) |
| **5K-15K** | ✅ Direct ($1) | ✅ Direct ($1) | ✅ Direct ($1) | ⚖️ Either |
| **>15K** | ✅ Direct ($1) | ✅ Direct ($1) | ✅ Direct ($1) | ✅ Direct ($1) |

**Key Insight**: Direct API ($1) is optimal for most large exports, regardless of budget.

### Accounts × Hardware Matrix

| Accounts | <8 cores | 8-10 cores | 10+ cores |
|----------|----------|------------|-----------|
| **1** | Sequential (14h) | Sequential (14h) | Sequential (14h) |
| **2-3** | Sequential | Parallel 2-3x (7-9h) | Parallel 2-3x (7-9h) |
| **4-6** | Sequential | Parallel 6x (2.3h) | Parallel 6x + opt (2.3h-45m) |
| **6+** | Sequential | Parallel 6x (2.3h) | Parallel 18x (45m) |

**Key Insight**: Hardware + accounts = multiplicative speedup.

---

## Decision Criteria

### Primary Criteria (Must Consider)

1. **Budget Available**
   - <$10: Direct API only
   - $10-$100: Consider both
   - >$100: Either (evaluate others)

2. **Timeline Required**
   - <12h: Paid service (if budget allows)
   - 12-24h: Either (evaluate frame count)
   - >24h: Direct API (cost efficient)

3. **Frame Count**
   - <5,000: Either approach viable
   - 5,000-15,000: Direct API preferred
   - >15,000: Direct API strongly preferred

4. **Figma Accounts**
   - 1: Sequential only
   - 2-6: Parallel viable (6x speedup)
   - 6+: Parallel optimized (18x speedup)

### Secondary Criteria (Nice to Consider)

5. **Technical Expertise**
   - Low: Paid service (managed)
   - Medium: Direct API with tutorials
   - High: Direct API + parallel

6. **Recurring Exports**
   - One-time: Consider paid (no setup)
   - 2-5 times/year: Direct API (setup worth it)
   - Weekly/monthly: Parallel (maximum ROI)

7. **Hardware Available**
   - <8 cores: Sequential
   - 8-10 cores: Parallel basic (6x)
   - 10+ cores: Parallel optimized (18x)

8. **Network Speed**
   - <10 Mbps: +2-3 hours (any approach)
   - 10-50 Mbps: Standard timelines
   - >50 Mbps: -20-30% time (all approaches)

---

## Special Cases

### Case 1: Emergency Export (ASAP)

**Context**: Need results in <6 hours, budget flexible

**Decision**:
```
IF budget >$100:
  → Paid Service ($95-136, 3-4h)
ELSE IF 2+ accounts AND hardware OK:
  → Parallel Basic (FREE, 2.3h)
ELSE:
  → Not possible (minimum 2.3h)
```

---

### Case 2: Very Large Export (50,000+ frames)

**Context**: Massive design system, 300+ files

**Decision**:
```
IF 6+ accounts AND 10+ core hardware:
  → Parallel Optimized ($5, ~90min)
ELSE IF 6+ accounts AND 8+ core hardware:
  → Parallel Basic (FREE, ~4-5h)
ELSE:
  → Direct API Sequential ($1, 28+ hours)
  → Consider multi-day approach
```

---

### Case 3: First-Time Export (Learning)

**Context**: Never exported before, testing feasibility

**Decision**:
```
Start with: Direct API Sequential ($1)
Reason: Establish baseline, validate process
Then evaluate:
  - Success rate achieved?
  - Time acceptable?
  - Need faster? → Consider parallel
  - Need managed? → Consider paid
```

---

### Case 4: Mixed Project (Some Urgent, Some Not)

**Context**: 100 files, 20 need same-day, 80 can wait

**Decision**:
```
Urgent files (20):
  → Paid Service ($20-40, 1-2h)

Non-urgent files (80):
  → Direct API ($1, overnight)

Total cost: $21-41 (vs $110+ all paid)
Total time: 1-2h urgent + overnight bulk
Savings: 60-70%
```

---

## Quick Reference Table

| Scenario | Budget | Timeline | Frames | Accounts | Recommendation |
|----------|--------|----------|--------|----------|----------------|
| **Research** | <$10 | Flexible | 15K+ | 1 | ✅ Direct API ($1) |
| **Client Work** | >$100 | <24h | 8K | 1 | ✅ Paid Service ($44) |
| **Monthly Audit** | $200 | Week | 12K | 1→6 | ✅ Direct → Parallel |
| **Startup MVP** | $1K | Weekly | 5K | 1 | ⚖️ Hybrid (Direct + occasional Paid) |
| **Enterprise** | Unlimited | Quarterly | 30K+ | 6+ | ✅ Parallel Optimized ($5) |
| **Emergency** | Flexible | <6h | Any | Any | ✅ Paid (if 1 account) or Parallel (if 6+) |
| **First-Time** | Any | Any | Any | Any | ✅ Direct Sequential (baseline) |

---

## Cost-Benefit Quick Calculator

### Input Your Scenario

```python
# Your project parameters
frame_count = 15000        # Total frames to export
budget_available = 100     # Dollars available
timeline_hours = 24        # Hours available
figma_accounts = 1         # Number of Figma Pro accounts
recurring_per_year = 4     # How many exports per year

# Calculate costs
direct_api_cost = 1.00
paid_service_cost = frame_count * 0.0055

# Calculate times
sequential_time = frame_count / 0.50 / 3600  # hours
parallel_time = sequential_time / figma_accounts if figma_accounts > 1 else sequential_time
paid_service_time = 3.5  # hours average

# Decision logic
if budget_available < 10:
    print("✅ Direct API ($1) - Budget constraints")
elif timeline_hours < 12:
    if budget_available >= paid_service_cost:
        print("✅ Paid Service - Timeline critical")
    elif figma_accounts >= 6:
        print("✅ Parallel (FREE) - 6x speedup")
    else:
        print("❌ Not possible - Need 12+ hours minimum")
elif frame_count > 15000:
    print("✅ Direct API ($1) - Large export, cost efficient")
elif recurring_per_year > 2:
    print("✅ Direct API ($1) - Recurring, ROI high")
else:
    print("⚖️ Either - Evaluate budget vs time")
```

### Example Outputs

**Scenario A**:
```
Input: 15,000 frames, $50 budget, 48h timeline, 1 account, 4/year
Output: ✅ Direct API ($1) - Large export, cost efficient
Reasoning: Large frame count + recurring + flexible timeline
```

**Scenario B**:
```
Input: 5,000 frames, $200 budget, 8h timeline, 1 account, 1 time
Output: ✅ Paid Service ($27.50) - Timeline critical
Reasoning: Tight deadline + budget allows + one-time
```

**Scenario C**:
```
Input: 25,000 frames, $100 budget, 24h timeline, 6 accounts, 12/year
Output: ✅ Parallel Basic (FREE) - 6x speedup
Reasoning: Multiple accounts + large export + recurring
```

---

## Final Decision Checklist

### Before You Decide

- [ ] **Calculate frame count** (run Phase 1 analysis)
- [ ] **Filter empty files** (only count frame_count > 0)
- [ ] **Apply 50% buffer** (multiply by 1.5 for estimates)
- [ ] **Check budget** (how much is available?)
- [ ] **Confirm timeline** (when do you need results?)
- [ ] **Count Figma accounts** (how many Pro accounts with access?)
- [ ] **Verify hardware** (cores, RAM, disk space)

### After Phase 1 Analysis

- [ ] **Exportable files**: ___ (frame_count > 0)
- [ ] **Total frames**: ___ (raw count)
- [ ] **Buffered frames**: ___ × 1.5 = ___
- [ ] **Budget available**: $___
- [ ] **Timeline required**: ___ hours
- [ ] **Figma accounts**: ___
- [ ] **Hardware**: ___ cores, ___ GB RAM

### Decision

**I choose**: [ ] Direct API ($1) [ ] Paid Service ($___) [ ] Parallel (FREE/$5)

**Reasoning**:
- Budget: ___
- Timeline: ___
- Frame count: ___
- Accounts: ___
- Recurring: ___

---

**Version**: 1.0.0
**Based On**: JL-004 learnings + parallel strategy
**Last Updated**: 2025-11-05
**Author**: Oracle (Justice League Coordinator)

---

**Oracle's Rule #4**: "Know your constraints (budget, time, accounts, hardware). The right choice becomes obvious."
