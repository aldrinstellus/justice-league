# Justice League Expense Tracking Guide

**Last Updated**: 2025-11-03
**Account**: aldrinstellus@gmail.com (Claude Max)

---

## 🎯 Quick Start

### Before Starting ANY New Mission

**Step 1**: Check the Decision Dashboard
```bash
cat expenses-global/reports/decision-dashboard.md
```

**Look for**:
- Available budget (currently $29.77 for November)
- Monthly status (85.1% allocated)
- Can we afford this mission? (YES/NO table)

**Step 2**: If Mission Approved → Create Expense Folder
```bash
mkdir -p missions/JL-XXX/expenses/{config,logs,reports}
```

**Step 3**: Copy Templates
```bash
cp _templates/expenses/pricing-config.json missions/JL-XXX/expenses/config/
cp _templates/expenses/budget-limits.json missions/JL-XXX/expenses/config/
# Edit budget-limits.json with mission-specific budgets
```

**Step 4**: Initialize Tracking
```bash
# Initialize expense-log.json with zero values
# Start logging activities as mission progresses
```

---

## 📊 How Expense Tracking Works

### 5 Levels of Granularity

1. **Per-Activity**: Every single action logged (research, analysis, file processing)
2. **Per-Task**: Group of related activities (e.g., "Competitive Analysis")
3. **Per-File**: Cost to analyze each Figma file
4. **Per-Phase**: Cost per mission phase (Discovery, Analysis, etc.)
5. **Per-Agent**: Cost per Justice League agent (Wonder Woman, Aldrin, Oracle)

### Automatic Tracking

When an agent performs an activity:
1. Log entry created in `expenses/logs/expense-log.json`
2. Tokens counted (input + output + cached)
3. Cost calculated using `pricing-config.json`
4. All breakdowns updated (by agent, phase, file, task)
5. Budget alerts checked (50%, 75%, 90%, 100%)

---

## 💰 Understanding Costs

### Token Pricing (2025)

**Claude Sonnet 4.5** (Primary):
- Input: $3 per 1M tokens ($0.000003 per token)
- Output: $15 per 1M tokens ($0.000015 per token)

**Claude Haiku 4.5** (Cost-Effective):
- Input: $1 per 1M tokens ($0.000001 per token)
- Output: $5 per 1M tokens ($0.000005 per token)
- **73% cheaper than Sonnet!**

### Example Calculation

**Activity**: Analyze Figma file "color-palette.fig"
```
Input Tokens: 45,000
Output Tokens: 22,000
Model: Claude Sonnet 4.5

Input Cost: 45,000 × $0.000003 = $0.135
Output Cost: 22,000 × $0.000015 = $0.330
Total Cost: $0.465
```

**With Prompt Caching** (90% savings on cached content):
```
Cached Tokens: 12,000
Cache Cost: 12,000 × $0.0000003 = $0.0036
Cache Read Savings: ~$0.356
Net Cost: $0.109 (77% cheaper!)
```

---

## 🚀 Cost Optimization Strategies

### Strategy 1: Model Selection (73% Savings)

**Use Claude Haiku for**:
- File cataloging and inventory
- Simple coordination tasks
- Synthesis and summaries
- Routine documentation

**Use Claude Sonnet for**:
- Complex analysis
- Architecture design
- Deep research
- Critical reasoning

**Example**:
```
Oracle (Coordinator): Uses Haiku
- 5 activities, 300K tokens
- Sonnet cost: $5.25
- Haiku cost: $1.75
- Savings: $3.50 (67%)
```

### Strategy 2: Prompt Caching (90% Savings)

**Enable for**:
- Repeated file analysis (100 Figma files)
- Design system documentation reuse
- Template-based generation

**Example**:
```
Analyzing 100 Figma files with shared design system:
- Without caching: $125
- With caching: $50
- Savings: $75 (60%)
```

### Strategy 3: Batch API (50% Savings)

**Use for**:
- Non-urgent synthesis
- Reporting and documentation
- Bulk processing tasks

**Example**:
```
Generate 50 component docs:
- Real-time: $25
- Batch API: $12.50
- Savings: $12.50 (50%)
```

### Combined Optimization

**Mission Budget**: $125
**With all optimizations**: $50 (60% reduction)
- Model selection: -20%
- Prompt caching: -36%
- Batch API: -4%

---

## 📈 Reports & Monitoring

### Global Reports (`/expenses-global/reports/`)

**decision-dashboard.md** - Before starting missions
- Check: Can we afford this mission?
- Shows: Available budget, monthly status, GO/NO-GO scenarios

**global-summary.md** - Performance overview
- Shows: All-time totals, mission leaderboard, trends
- Updated: Monthly + after each mission completion

### Per-Mission Reports (`/missions/JL-XXX/expenses/reports/`)

**expense-summary.md** - Mission overview
- Budget status
- Phase breakdown
- Agent breakdown
- Cost optimization plan

**expense-detailed.md** - Full breakdown (generated at completion)
- Every activity line-item
- Cost calculations
- Optimization opportunities

---

## 🎯 Budget Alert System

### Thresholds

| Threshold | Action |
|-----------|--------|
| 50% | ✅ Normal - continue |
| 75% | ⚠️ Warning - monitor closely |
| 85% | ⚠️ Caution - new missions <$30 only |
| 90% | 🚨 Alert - mission completion only |
| 100% | 🛑 Hard stop - auto-stop enabled |

### How Alerts Work

1. After each activity, check budget %
2. If threshold crossed → Alert triggered
3. Email sent to aldrinstellus@gmail.com
4. Dashboard updated with warning status
5. At 100% → Auto-stop all new activities

---

## 📊 Key Files Reference

### Global Files

| File | Purpose | When to Check |
|------|---------|---------------|
| `account-config.json` | Claude Max plan details | Setup only |
| `cumulative-expenses.json` | Cross-mission totals | Real-time |
| `mission-forecasts.json` | Future mission planning | Before new missions |
| `decision-dashboard.md` | GO/NO-GO decisions | Before EVERY mission |
| `global-summary.md` | Performance overview | Monthly |

### Per-Mission Files

| File | Purpose | When to Update |
|------|---------|----------------|
| `config/pricing-config.json` | Model pricing | Copy from template |
| `config/budget-limits.json` | Mission budget | Before mission start |
| `logs/expense-log.json` | All activities | After EVERY activity |
| `reports/expense-summary.md` | Quick overview | Weekly + completion |

---

## 💡 Best Practices

### DO ✅
- **Check decision dashboard before starting missions**
- **Log every activity immediately**
- **Enable cost optimizations from start**
- **Review expense summary weekly**
- **Update global cumulative after each activity**

### DON'T ❌
- **Don't skip budget checks**
- **Don't forget to log activities**
- **Don't ignore alert thresholds**
- **Don't start missions without available budget**
- **Don't use Sonnet when Haiku works**

---

## 🔍 FAQ

### Q: How do I know if I can start a new mission?
**A**: Check `/expenses-global/reports/decision-dashboard.md` → Look at "Available Budget" and "Can We Start a New Mission?" section.

### Q: What if my mission exceeds budget?
**A**: Alerts trigger at 75%, 90%, 100%. Auto-stop at 100%. Consider: (1) Wait for next month, (2) Enable optimizations, (3) Reduce scope.

### Q: How accurate are the estimates?
**A**: JL-001 came in 64% under budget ($125 estimate, $45 actual). Future estimates can be tighter. Use historical data for better accuracy.

### Q: Can I track multiple missions simultaneously?
**A**: Yes! Each mission has its own `/expenses/` folder. Global tracking shows cumulative across all missions.

### Q: When does the monthly budget reset?
**A**: First of each month (e.g., December 1 = fresh $200 budget).

---

## 🎯 Example: Starting JL-004

**Scenario**: Want to start JL-004 (Component Migration, $80 estimated)

**Step 1**: Check Decision Dashboard
```bash
cat expenses-global/reports/decision-dashboard.md
```

**Result**: November available = $29.77. Mission needs $80. ❌ **NO-GO**

**Options**:
1. ⏳ Wait until December (full $200 budget)
2. ✂️ Reduce scope to Phase 1 only ($25)
3. 🎯 Optimize heavily (target $25 with Haiku + caching)

**Decision**: Wait until December ✅

**Step 2 (December 1)**: Re-check dashboard
```bash
cat expenses-global/reports/decision-dashboard.md
```

**Result**: December available = $200. Mission needs $80. ✅ **GO**

**Step 3**: Create mission structure
```bash
mkdir -p missions/JL-004-component-migration/expenses/{config,logs,reports}
cp _templates/expenses/*.json missions/JL-004-component-migration/expenses/config/
```

**Step 4**: Update budget-limits.json for JL-004
```bash
nano missions/JL-004-component-migration/expenses/config/budget-limits.json
# Set totalBudget: 80.00
# Allocate by phase and agent
```

**Step 5**: Update global cumulative
```bash
# Add JL-004 to expenses-global/cumulative-expenses.json
# Update "thisMonth" and "missions" arrays
```

**Step 6**: Start mission, log activities

---

## 📞 Support

**Questions?**
- See examples in JL-001 and JL-003 folders
- Check decision-dashboard.md for current status
- Review global-summary.md for performance trends

**Issues?**
- Budget alerts not triggering → Check alert thresholds in budget-limits.json
- Cost calculations wrong → Verify pricing-config.json is up to date
- Can't start mission → Check decision-dashboard.md for available budget

---

**System Version**: 1.0.0
**Last Updated**: 2025-11-03
**Maintained By**: Oracle (Justice League Coordinator)
