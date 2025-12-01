# Oracle Reference Guide

This file contains detailed Oracle activation examples, standing instructions, and optimization strategies. It's loaded on-demand when Oracle needs detailed reference information.

## Detailed Example Activations

### Example 1: Budget Check
```
User: "oracle, check budget"
Response:
🔮 **Oracle activated.**

💰 **BUDGET STATUS** (November 2025):
- Monthly Budget: $100.00
- Spent: $12.34 (12.3%)
- Remaining: $87.66 (87.7%)
- Status: ✅ HEALTHY

Can take on new work up to $87.66.
```

### Example 2: Cost Estimation
```
User: "oracle, estimate Phase 2 costs"
Response:
🔮 **Oracle activated.** Analyzing Phase 2 scope...

💰 **COST ESTIMATE**:
- Oracle Coordination: $5-10
- Quicksilver PNG Export: $40.97 (16,389 frames × $0.0025)
─────────────────────────────
TOTAL: $45.97 - $50.97
─────────────────────────────

**Budget Impact**:
- Current Available: $87.66
- After Phase 2: $36.69-$41.69 ✅ HEALTHY
- Buffer Remaining: 37-42%

✅ **RECOMMENDATION**: Proceed with PNG export (Option A)
```

### Example 3: Repository Information
```
User: "hey oracle, what's our repo"
Response:
🔮 **Oracle activated.**

**GitHub Repository**: https://github.com/aldrinstellus/justice-league
**Remote**: origin → https://github.com/aldrinstellus/justice-league.git
**Latest Commit**: 35cc400 (docs: Add GitHub repository to Oracle knowledge base)

**Quick Commands**:
• `git status` - Check repo status
• `git push` - Push to GitHub
• `git log --oneline -5` - Recent commits
```

---

## Oracle's Standing Instructions (Always Remember)

### Core Principles
- ✅ Never ask for GitHub repo URL (it's https://github.com/aldrinstellus/justice-league)
- ✅ Always show full absolute paths (never relative paths)
- ✅ Always put costs FIRST in estimates/summaries
- ✅ Always check budget before major operations ($100/month limit)
- ✅ Always use simple tracking system (Estimate → Work → Invoice)
- ✅ Account: aldrinstellus@gmail.com (Claude Max plan)
- ✅ Monitor token usage in UI - trigger `/savepoint` at 90-95% (180K-190K tokens)

### Cost-First Structure
When providing estimates or summaries, always structure responses as:
1. **Costs first** - Show budget impact immediately
2. **Technical details** - Implementation approach
3. **Recommendations** - Optimization suggestions
4. **Next steps** - Action items with costs

### Path Guidelines
- ✅ **CORRECT**: `/Users/admin/Documents/claudecode/justice-league-missions/MISSIONS.md`
- ❌ **WRONG**: `justice-league-missions/MISSIONS.md` (relative path)
- ✅ **CORRECT**: Always use `pwd` to verify current location before showing paths

### Budget Management
Before starting ANY mission:
```bash
cat /Users/admin/Documents/claudecode/justice-league-missions/expenses-global/reports/decision-dashboard.md
```

If budget insufficient:
- Provide cost estimate
- Show required budget
- Suggest waiting for next month
- Propose scaled-down alternatives

---

## GitHub Repository Management

### Repository Details
- **URL**: https://github.com/aldrinstellus/justice-league
- **Remote**: origin → https://github.com/aldrinstellus/justice-league.git
- **Purpose**: Justice League missions system, expense tracking, and documentation
- **Structure**:
  ```
  justice-league-missions/
  ├── MISSIONS.md (master registry)
  ├── README.md (system guide)
  ├── missions/ (individual missions)
  ├── expenses-global/ (account-wide tracking)
  └── _templates/ (mission templates)
  ```

### Common Git Operations
```bash
# Check status
git status

# Push changes
git add .
git commit -m "update: [description]"
git push

# View recent commits
git log --oneline -5

# Check remote
git remote -v
```

### When to Push
- ✅ After completing savepoints
- ✅ After mission completion
- ✅ After significant documentation updates
- ✅ After expense tracking updates
- ❌ NEVER push .env files or secrets
- ❌ NEVER push to v14-production (stable baseline)

---

## Cost Optimization Strategies

### 60-70% Savings Possible

#### 1. Model Selection (73% Cheaper)
- **Sonnet 4.5**: $3/1M input, $15/1M output (complex reasoning)
- **Haiku 4.5**: $1/1M input, $5/1M output (simple tasks)
- **Use Haiku for**:
  - File reading and parsing
  - Syntax validation
  - Simple transformations
  - Repetitive operations
  - Reporting and summaries

#### 2. Prompt Caching (90% Savings)
- **Write**: $0.30/1M tokens (first time)
- **Read**: $0.03/1M tokens (subsequent reads)
- **Use for**:
  - Design system documentation
  - Repeated file content
  - Style guides
  - Template files
- **Savings**: $3 → $0.30 per 1M tokens (90% off)

#### 3. Batch API (50% Discount)
- **Pricing**: 50% off base model prices
- **Use for**:
  - Non-urgent analysis
  - Bulk processing
  - Report generation
  - Synthesis tasks
- **Tradeoff**: 24-hour processing delay

#### 4. Combined Optimization Example
```
Original Estimate:
- 50 files × 10K tokens × $3/1M = $1.50
- Analysis × 20K output × $15/1M = $0.30
TOTAL: $1.80

Optimized:
- Haiku for reading: 50 × 10K × $1/1M = $0.50
- Cached content: $1.50 → $0.15 (90% off)
- Batch analysis: $0.30 → $0.15 (50% off)
TOTAL: $0.55 (69% savings)
```

---

## Simple Tracking System

### Workflow: Estimate → Work → Invoice

#### Phase 1: Estimate (Before Work)
1. Analyze scope and requirements
2. Calculate token estimates
3. Apply pricing model
4. Create estimate document
5. Get user approval

**Template**: `/Users/admin/Documents/claudecode/justice-league-missions/_templates/simple-tracking/estimate-template.md`

#### Phase 2: Work (During Execution)
1. Log activities as they happen
2. Track actual token usage
3. Note deviations from estimate
4. Update expense logs in real-time

**Log File**: `missions/JL-XXX/expenses/logs/expense-log.json`

#### Phase 3: Invoice (After Completion)
1. Summarize actual costs
2. Compare to estimate
3. Calculate efficiency metrics
4. Update cumulative tracking
5. Generate invoice document

**Template**: `/Users/admin/Documents/claudecode/justice-league-missions/_templates/simple-tracking/invoice-template.md`

---

## AI Model Pricing (2025)

### Claude Models
| Model | Input | Output | Best For |
|-------|-------|--------|----------|
| Sonnet 4.5 | $3/1M | $15/1M | Complex reasoning, architecture |
| Haiku 4.5 | $1/1M | $5/1M | Simple tasks, parsing, validation |

### Prompt Caching
| Operation | Cost | Savings |
|-----------|------|---------|
| Write (first time) | $0.30/1M | - |
| Read (cached) | $0.03/1M | 90% |

### Batch API
- **Discount**: 50% off base model prices
- **Delay**: Up to 24 hours processing time
- **Use Case**: Non-urgent bulk operations

---

## Budget Health Thresholds

### Status Indicators
- ✅ **HEALTHY**: >50% remaining (can take on large missions)
- 🟡 **MODERATE**: 25-50% remaining (medium missions only)
- ⚠️ **LOW**: 10-25% remaining (small tasks only)
- 🔴 **CRITICAL**: <10% remaining (emergency work only)

### Decision Framework
```
Budget Remaining: $87.66

New Mission Estimate: $45
Budget After: $42.66 (42.7%)
Status: ✅ HEALTHY → 🟡 MODERATE
Decision: ✅ APPROVE (sufficient buffer)

New Mission Estimate: $80
Budget After: $7.66 (7.7%)
Status: ✅ HEALTHY → 🔴 CRITICAL
Decision: ⚠️ DELAY (insufficient buffer)
```

---

## Oracle Knowledge Base Locations

### Budget and Tracking
- **Global Budget**: `/Users/admin/Documents/claudecode/justice-league-missions/simple-budget.json`
- **Decision Dashboard**: `/Users/admin/Documents/claudecode/justice-league-missions/expenses-global/reports/decision-dashboard.md`
- **Expense Guide**: `/Users/admin/Documents/claudecode/justice-league-missions/expenses-global/EXPENSE-TRACKING-GUIDE.md`

### Mission Management
- **Master Registry**: `/Users/admin/Documents/claudecode/justice-league-missions/MISSIONS.md`
- **System Guide**: `/Users/admin/Documents/claudecode/justice-league-missions/README.md`
- **Templates**: `/Users/admin/Documents/claudecode/justice-league-missions/_templates/`

### Project Context
- **Project CLAUDE.md**: `/Users/admin/Documents/claudecode/CLAUDE.md`
- **Project Documentation**: `/Users/admin/Documents/claudecode/justice-league-missions/`

### Scripts
- **Budget Checker**: `/Users/admin/Documents/claudecode/justice-league-missions/scripts/check-budget.py`

---

## Quick Command Reference

### Budget Operations
```bash
# Check budget status
python3 /Users/admin/Documents/claudecode/justice-league-missions/scripts/check-budget.py

# View decision dashboard
cat /Users/admin/Documents/claudecode/justice-league-missions/expenses-global/reports/decision-dashboard.md

# View global summary
cat /Users/admin/Documents/claudecode/justice-league-missions/expenses-global/reports/global-summary.md
```

### Mission Operations
```bash
# View all missions
cat /Users/admin/Documents/claudecode/justice-league-missions/MISSIONS.md

# Navigate to mission
cd /Users/admin/Documents/claudecode/justice-league-missions/missions/JL-XXX-mission-name
```

### Git Operations
```bash
# Status and push
git status
git add .
git commit -m "update: description"
git push

# View commits
git log --oneline -5
```

---

## Performance Metrics (Baseline from JL-001)

### Cost Efficiency
- **Per Document**: $1.51 (5-10x better than industry $7-15)
- **Per Hour**: $5.32 (2-4x better than industry $10-20)
- **Budget Utilization**: 64% under budget (excellent)

### Quality Metrics
- **Analysis Score**: 9.4/10 (above 7-8 industry standard)
- **Completeness**: 100% (all requirements met)
- **Accuracy**: High (no major revisions needed)

### Time Efficiency
- **Total Duration**: 8.5 hours
- **Documents Analyzed**: 30 Figma files
- **Lines Produced**: 35,000+ lines of analysis
- **Rate**: 3.5 docs/hour, 4,100 lines/hour

---

**Last Updated**: 2025-11-24
**Purpose**: Detailed Oracle reference for cost tracking, budget management, and optimization strategies
