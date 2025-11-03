# Justice League Missions System - CLAUDE.md

This file provides guidance to Claude Code when working within the Justice League Missions tracking system.

---

## System Overview

**Location**: `/Users/admin/Documents/claudecode/justice-league-missions/`
**GitHub Repository**: `https://github.com/aldrinstellus/justice-league`
**Remote**: `origin` → `https://github.com/aldrinstellus/justice-league.git`

**Purpose**: Centralized tracking system for multi-agent design analysis missions with comprehensive expense tracking.

**Designed to Handle**:
- 100s of Figma files per project
- 1000s of pages and components per file
- Complete mission lifecycle tracking (brief → execution → deliverables → metrics)
- Per-activity cost tracking and budget management

**Account**: aldrinstellus@gmail.com (Claude Max plan)
**Monthly Budget**: $100.00 (Claude Max $20/month subscription)

**Latest Savepoint**: `PROJECT-SAVEPOINT-2025-11-03-SIMPLE-TRACKING.md` (Simple Cost Tracking System Complete)

---

## 🔗 Git Workflow & Repository

**Primary Repository**: https://github.com/aldrinstellus/justice-league

**Standard Git Commands**:
```bash
# Always use this remote for push/pull
git remote -v  # Verify: origin → https://github.com/aldrinstellus/justice-league.git

# Commit changes
git add .
git commit -m "message"

# Push to GitHub
git push origin main
# OR
git push  # (if tracking branch is set)
```

**Oracle Standing Instructions**:
1. **ALWAYS** remember this GitHub repository exists
2. **NEVER** ask user for repository URL again
3. **AUTOMATICALLY** use this repo for all Justice League git operations
4. **DOCUMENT** all major changes with proper commit messages

---

## ⚠️ CRITICAL: Before Starting ANY Work

### Quick Budget Check (Simple System)
```bash
cd /Users/admin/Documents/claudecode/justice-league-missions
python3 scripts/check-budget.py
```

**Output shows**:
- Monthly budget: $100.00
- Current spent: $XX.XX
- Remaining: $XX.XX
- Status: ✅ HEALTHY / ⚠️ CAUTION / 🚨 CRITICAL

### Alternative: Decision Dashboard (Complex System)
```bash
cat /Users/admin/Documents/claudecode/justice-league-missions/expenses-global/reports/decision-dashboard.md
```

**If budget is insufficient**:
- ⏳ Wait for next month (budget resets on 1st)
- ✂️ Reduce mission scope to fit available budget
- 🎯 Apply cost optimizations (Haiku + caching + batch API)

---

## File Structure

```
justice-league-missions/
├── MISSIONS.md                                      # Master registry (START HERE)
├── README.md                                        # System documentation
├── SIMPLE-COST-TRACKING-GUIDE.md                   # User guide for simple system ⭐
├── simple-budget.json                               # Simple budget tracker ⭐
├── PROJECT-SAVEPOINT-2025-11-03-SIMPLE-TRACKING.md # Latest savepoint ⭐
├── _templates/                                      # Templates for new missions
│   ├── simple-tracking/                            # ⭐ Simple system templates
│   │   ├── ESTIMATE-TEMPLATE.md
│   │   ├── INVOICE-TEMPLATE.md
│   │   └── MONTHLY-SUMMARY-TEMPLATE.md
│   ├── mission-brief.md
│   ├── metrics.json
│   ├── mission-log.md
│   └── expenses/
│       ├── pricing-config.json
│       ├── budget-limits.json
│       └── expense-log-template.json
├── expenses-global/                     # Global expense tracking
│   ├── account-config.json              # Claude Max plan config
│   ├── cumulative-expenses.json         # Cross-mission totals
│   ├── mission-forecasts.json           # Future mission planning
│   ├── EXPENSE-TRACKING-GUIDE.md        # Complete usage guide
│   └── reports/
│       ├── decision-dashboard.md        # GO/NO-GO decisions ⭐
│       └── global-summary.md            # All-time performance
├── scripts/                             # ⭐ Simple tracking scripts
│   ├── check-budget.py                  # Quick budget status
│   └── README.md                        # Scripts documentation
└── missions/                            # All mission folders
    ├── JL-001-tweakcn-research/         # Completed mission
    ├── JL-002-example/                  # Example template
    └── JL-003-auzmor-learn-web-mobile/  # Active mission (Phase 1 complete)
        ├── JL-003-PHASE1-INVOICE.md     # ⭐ Simple invoice (Phase 1)
        ├── JL-003-PHASE2-ESTIMATE.md    # ⭐ Simple estimate (Phase 2)
        ├── SUMMARY-FOR-ALDO.md          # Phase 1 summary (cost-first)
        ├── mission-brief.md
        ├── mission-log.md
        ├── metrics.json
        ├── detailed-analysis.json       # Complete file analysis (52KB)
        ├── phase1-files-list.json       # File inventory (92KB)
        ├── expenses/                    # Complex tracking (optional)
        │   ├── config/
        │   │   ├── pricing-config.json
        │   │   └── budget-limits.json
        │   ├── logs/
        │   │   └── expense-log.json
        │   └── reports/
        │       └── expense-summary.md
        └── figma-files/                 # Figma analysis
            └── {file-name}/
                ├── pages/
                └── analysis.md
```

---

## Current Budget Status (November 2025)

**Monthly Limit**: $100.00
**Spent (completed)**: $12.34 (JL-003 Phase 1)
**Available**: $87.66 (87.7%)

**Status**: ✅ HEALTHY - Can take on more work

**Quick Check**:
```bash
python3 /Users/admin/Documents/claudecode/justice-league-missions/scripts/check-budget.py
```

---

## 💡 Simple Cost Tracking System (RECOMMENDED)

### Overview

**System Type**: Option A - Simple invoice-style tracking

**How It Works**:
1. **ESTIMATE** before work → Clean cost projection with options
2. **WORK** happens → Oracle tracks internally (hidden from user)
3. **INVOICE** after work → Actual costs vs estimate, budget updated

**No complex logs, no per-activity tracking, just clean estimates and invoices.**

### Quick Commands

**Check Budget**:
```bash
cd /Users/admin/Documents/claudecode/justice-league-missions
python3 scripts/check-budget.py
```

**View User Guide**:
```bash
cat /Users/admin/Documents/claudecode/justice-league-missions/SIMPLE-COST-TRACKING-GUIDE.md
```

**View Budget Tracker**:
```bash
cat /Users/admin/Documents/claudecode/justice-league-missions/simple-budget.json
```

### Generating Estimates & Invoices

**For Figma Export Tasks**:
1. Analyze Figma project/file with Python scripts
2. Calculate costs: Oracle (Claude API) + Agent (Quicksilver/external)
3. Create estimate file using template: `_templates/simple-tracking/ESTIMATE-TEMPLATE.md`
4. After work complete, create invoice using: `_templates/simple-tracking/INVOICE-TEMPLATE.md`
5. Update `simple-budget.json` with actual costs

**Cost Structure**:
- **Oracle Coordination** (Claude API): $2-10 per task
- **Agent Execution** (External services): Varies by service
- **Total** = Oracle + Agent costs

### File Naming Convention

**Estimates**: `{MISSION-ID}-{PHASE-ID}-ESTIMATE.md`
- Example: `JL-003-PHASE2-ESTIMATE.md`

**Invoices**: `{MISSION-ID}-{PHASE-ID}-INVOICE.md`
- Example: `JL-003-PHASE1-INVOICE.md`

**Location**: Store in mission folder:
```
/Users/admin/Documents/claudecode/justice-league-missions/missions/{mission-folder}/
```

### Simple vs Complex Tracking

**Use Simple System When**:
- User wants clean cost estimates only
- Don't need per-activity tracking
- Invoice-style reporting preferred
- Minimal overhead required

**Use Complex System When**:
- Need detailed token tracking
- Per-activity cost analysis required
- Research project with auditing needs
- Real-time monitoring essential

**Current Default**: Simple system (Option A)

---

## Creating a New Mission

### Step 1: Check Budget
```bash
cat expenses-global/reports/decision-dashboard.md
```

### Step 2: Determine Mission Number
```bash
# Check latest mission ID in registry
cat MISSIONS.md
# Increment by 1 (e.g., if latest is JL-003, next is JL-004)
```

### Step 3: Create Mission Folder
```bash
cd missions
mkdir JL-XXX-mission-name
cd JL-XXX-mission-name
```

### Step 4: Copy Templates
```bash
cp ../../_templates/mission-brief.md .
cp ../../_templates/metrics.json .
cp ../../_templates/mission-log.md .
```

### Step 5: Set Up Expense Tracking
```bash
mkdir -p expenses/{config,logs,reports}
cp ../../_templates/expenses/pricing-config.json expenses/config/
cp ../../_templates/expenses/budget-limits.json expenses/config/
# Edit budget-limits.json with mission-specific budgets
```

### Step 6: Create Folder Structure
**For Figma missions**:
```bash
mkdir -p figma-files
```

**For other missions**:
```bash
mkdir -p deliverables
```

### Step 7: Fill Out Mission Brief
Edit `mission-brief.md` with:
- Mission ID and name
- Objective
- Agents deployed
- Figma files (if applicable)
- Budget allocation
- Deliverables
- Success criteria

### Step 8: Update Master Registry
Add mission entry to `MISSIONS.md` in "Active Missions" section

### Step 9: Update Global Cumulative
Update `expenses-global/cumulative-expenses.json` with new mission

---

## Expense Tracking

### 5 Levels of Granularity

1. **Per-Activity**: Every single action logged (tokens + cost)
2. **Per-Task**: Group of related activities
3. **Per-File**: Cost per Figma file analyzed
4. **Per-Phase**: Cost per mission phase
5. **Per-Agent**: Cost per Justice League agent

### AI Model Pricing (2025)

**Claude Sonnet 4.5** (Complex tasks):
- Input: $3 per 1M tokens
- Output: $15 per 1M tokens

**Claude Haiku 4.5** (Simple tasks - 73% cheaper):
- Input: $1 per 1M tokens
- Output: $5 per 1M tokens

**Prompt Caching** (90% savings):
- Write: $0.30 per 1M tokens
- Read: $0.03 per 1M tokens

**Batch API** (50% discount):
- Use for non-urgent synthesis and reporting

### Cost Optimization Strategies

**Strategy 1: Model Selection** (73% savings)
- Use **Haiku** for: Cataloging, coordination, synthesis, routine docs
- Use **Sonnet** for: Complex analysis, architecture, deep research

**Strategy 2: Prompt Caching** (90% savings)
- Enable for: Repeated file analysis, design system docs reuse, templates

**Strategy 3: Batch API** (50% savings)
- Use for: Non-urgent synthesis, reporting, documentation, bulk processing

**Combined Optimization**: 60-70% cost reduction
- Example: $125 mission → $50 with full optimization

### Budget Alert Thresholds

| Threshold | Action |
|-----------|--------|
| 50% | ✅ Normal - continue |
| 75% | ⚠️ Warning - monitor closely |
| 85% | ⚠️ Caution - new missions <$30 only |
| 90% | 🚨 Alert - mission completion only |
| 100% | 🛑 Hard stop - auto-stop enabled |

---

## Key Files Reference

### Must-Read Before Starting
1. `MISSIONS.md` - Master registry of all missions
2. `expenses-global/reports/decision-dashboard.md` - Budget GO/NO-GO
3. `README.md` - Complete system documentation
4. `expenses-global/EXPENSE-TRACKING-GUIDE.md` - Detailed expense guide

### Templates
- `_templates/mission-brief.md` - Mission structure template
- `_templates/metrics.json` - Metrics tracking template
- `_templates/mission-log.md` - Progress log template
- `_templates/expenses/*.json` - Expense tracking templates

### Global Tracking
- `expenses-global/account-config.json` - Claude Max plan details
- `expenses-global/cumulative-expenses.json` - All-time totals
- `expenses-global/mission-forecasts.json` - Future mission estimates
- `expenses-global/reports/global-summary.md` - Performance overview

### Per-Mission Files
- `mission-brief.md` - Objective, scope, budget
- `mission-log.md` - Chronological progress
- `metrics.json` - Performance metrics
- `expenses/config/budget-limits.json` - Mission budget
- `expenses/logs/expense-log.json` - Activity tracking
- `expenses/reports/expense-summary.md` - Budget status

---

## Active Missions

### JL-001: TweakCN Research
**Status**: ✅ Completed
**Cost**: $45.23 (64% under budget)
**Output**: 35,000+ lines of documentation
**Performance**: $1.51/doc, $5.32/hour, 9.4/10 quality

### JL-003: Auzmor Learn Web&Mobile
**Status**: ⏳ Active (Phase 1 ✅ COMPLETE)
**Budget**: $125.00 ($0 spent Phase 1, $90.14 estimated Phase 2)
**Phase 1 Results**: 182 files analyzed, 16,389 frames, 1,243 pages, 20,447 components
**Duration**: 14 weeks (Nov 2025 - Feb 2026)
**Summary**: `missions/JL-003-auzmor-learn-web-mobile/SUMMARY-FOR-ALDO.md`

---

## Common Workflows

### Check Budget Before New Mission
```bash
cat expenses-global/reports/decision-dashboard.md
```

### View All Missions
```bash
cat MISSIONS.md
```

### Check Global Performance
```bash
cat expenses-global/reports/global-summary.md
```

### View Active Mission Status
```bash
# Quick summary with cost-first structure
cat missions/JL-003-auzmor-learn-web-mobile/SUMMARY-FOR-ALDO.md

# Detailed expense tracking
cat missions/JL-003-auzmor-learn-web-mobile/expenses/reports/expense-summary.md

# Complete analysis data (JSON)
cat missions/JL-003-auzmor-learn-web-mobile/detailed-analysis.json
```

### Start New Phase
1. Update `mission-log.md` with phase start
2. Log first activity in `expenses/logs/expense-log.json`
3. Monitor budget in `expenses/reports/expense-summary.md`

### Complete Mission
1. Update `metrics.json` with final metrics
2. Generate final expense report
3. Move mission from "Active" to "Completed" in `MISSIONS.md`
4. Update global cumulative expenses
5. Add final summary to `mission-log.md`

---

## Best Practices

### DO ✅
- **Always check budget before starting work** (run `check-budget.py`)
- **Always show FULL PATH URLs** for all files (user standing instruction)
- **Generate estimates before work** using estimate templates
- **Generate invoices after work** with actual costs
- **Update simple-budget.json** after completing tasks
- **Use cost-first structure** in all summaries (cost at top, details below)
- **Use Haiku for simple tasks** (73% cheaper than Sonnet)
- **Enable prompt caching for repeated content** (90% savings)
- **Update mission-log.md with progress**

### DON'T ❌
- **Don't skip budget checks** before starting missions
- **Don't use relative paths** - ALWAYS use full absolute paths
- **Don't bury cost information** - always put it first in summaries
- **Don't ignore alert thresholds** (75%, 90%, 100%)
- **Don't start missions without available budget**
- **Don't use Sonnet when Haiku will work**
- **Don't skip mission ID numbers** (always sequential)
- **Don't forget to update MISSIONS.md**
- **Don't use sampling for Figma analysis** - always use Analysis Mode
- **Don't forget user preferences** (simple tracking, full paths, cost-first)

---

## Performance Metrics (JL-001 Baseline)

**Efficiency**:
- $1.51/document (5-10x better than industry average of $8-15)
- $5.32/hour (2-4x better than industry average of $8+)
- 64% under budget (excellent efficiency)

**Quality**:
- 9.4/10 quality score (above 7-8 industry average)
- 35,000+ lines of comprehensive documentation
- Complete technical architecture and PRD

**Speed**:
- Full competitive analysis in 1 week
- Multi-agent coordination with minimal overhead

---

## Troubleshooting

### Budget Exceeded
**Problem**: Monthly budget at 100%
**Solution**:
1. Wait for next month (budget resets on 1st)
2. Review cost optimization opportunities
3. Apply Haiku + caching + batch API for current work

### Mission Over Budget
**Problem**: Mission exceeding allocated budget
**Solution**:
1. Check `expenses/reports/expense-summary.md`
2. Enable cost optimizations
3. Reduce scope if necessary
4. Consider multi-month approach

### Can't Find Mission Files
**Problem**: Looking for specific mission or file
**Solution**:
1. Check `MISSIONS.md` for mission registry
2. Use `find missions -name "*keyword*"`
3. Check mission-brief.md for file locations

---

## Quick Reference Commands

```bash
# Change to project directory
cd /Users/admin/Documents/claudecode/justice-league-missions

# Budget check (ALWAYS do first) - Simple System
python3 scripts/check-budget.py

# Budget check (Alternative) - Complex System
cat expenses-global/reports/decision-dashboard.md

# View all missions
cat MISSIONS.md

# View simple tracking guide
cat SIMPLE-COST-TRACKING-GUIDE.md

# View budget tracker
cat simple-budget.json

# View latest estimate (JL-003 Phase 2)
cat missions/JL-003-auzmor-learn-web-mobile/JL-003-PHASE2-ESTIMATE.md

# View latest invoice (JL-003 Phase 1)
cat missions/JL-003-auzmor-learn-web-mobile/JL-003-PHASE1-INVOICE.md

# Read complete guides
cat README.md
cat SIMPLE-COST-TRACKING-GUIDE.md
cat expenses-global/EXPENSE-TRACKING-GUIDE.md
```

---

## 🔮 Oracle Knowledge Base (Learned Skills)

### Figma Analysis Mode

**When user says "analysis mode" for Figma projects, Oracle will**:
1. **Individual File Analysis** - No sampling, analyze every file individually
2. **Exact Structure Counts** - Precise pages, frames, sections, components per file
3. **Per-File Cost Calculation** - Calculate export costs individually for each file
4. **Export Folder Planning** - Generate safe folder names for all exports
5. **Live Progress Tracking** - Show real-time progress bar during analysis

**Implementation**: Use Python scripts with live progress:
```python
# analyze_with_progress.py pattern
for idx, file_info in enumerate(files, 1):
    print(f"\r{progress_bar(idx-1, total)}", end='', flush=True)
    print(f"\n📊 [{idx}/{total}] {file_name}")
    result = analyze_file(file_key, file_name)
    print(f"   ✅ Pages: {pages}, Frames: {frames}, Cost: ${cost}")
    time.sleep(1.2)  # Rate limiting
```

**Trigger**: User explicitly requests "analysis mode" or "individual file analysis"

### Cost-First Summary Structure

**All Figma project summaries must follow this structure**:

1. **💰 TOTAL COST SUMMARY** (Top-Level - Always First)
   - Quick answer: What will it cost?
   - Budget status vs allocated
   - What you get (files, frames, pages, components)
   - Cost efficiency (per file, per page, per frame)
   - Bottom line statement

2. **🎯 Executive Summary** (Second)
   - Objective and method
   - Results overview

3. **📊 Detailed Analytics** (Following sections)
   - File distribution
   - Top expensive files
   - Recommendations
   - Next steps

**Pattern**: Cost and budget first, then details. Never bury cost information.

### Quicksilver Export Pricing

**Standard Figma Export Costs** (2025):
- **PNG Export**: $0.0025 per frame
- **PDF Export**: $0.0030 per frame
- **Combined PNG + PDF**: $0.0055 per frame

**Usage**: Multiply frame count × pricing for accurate cost estimates.

### Python Scripts for Figma Analysis

**Common Commands**:
```bash
# File-by-file analysis with live progress
python3 analyze_with_progress.py

# Detailed analysis with comprehensive reporting
python3 detailed_file_analysis.py

# Initial inventory
python3 figma_project_inventory.py
```

**Requirements**:
```python
import os, json, requests, time
from datetime import datetime

FIGMA_TOKEN = os.getenv('FIGMA_ACCESS_TOKEN')
FIGMA_API_BASE = 'https://api.figma.com/v1'
```

**Rate Limiting**: Always use `time.sleep(1.2)` between API calls to respect Figma limits.

### Full Path URLs Requirement ⚠️

**CRITICAL USER PREFERENCE**: Always show FULL ABSOLUTE PATHS for all file references.

**Correct Format**:
```
/Users/admin/Documents/claudecode/justice-league-missions/missions/JL-003-auzmor-learn-web-mobile/JL-003-PHASE1-INVOICE.md
```

**NEVER Use**:
```
missions/JL-003-auzmor-learn-web-mobile/JL-003-PHASE1-INVOICE.md  ❌ WRONG
./missions/JL-003-auzmor-learn-web-mobile/JL-003-PHASE1-INVOICE.md  ❌ WRONG
JL-003-PHASE1-INVOICE.md  ❌ WRONG
```

**User will remind you if forgotten** - this is a standing instruction for ALL work.

---

## Python Scripts Reference

### Budget Management

**check-budget.py** - Quick budget status
```bash
cd /Users/admin/Documents/claudecode/justice-league-missions
python3 scripts/check-budget.py
```
Shows: Budget, spent, remaining, status, completed tasks

### Figma Analysis Scripts

**Location**: `/Users/admin/Documents/claudecode/justice-league-missions/missions/JL-003-auzmor-learn-web-mobile/scripts/`

**Phase 1 - Discovery**:
- `analyze_with_progress.py` - Live progress file-by-file analysis
- `detailed_file_analysis.py` - Comprehensive analysis with reporting
- `figma_project_inventory.py` - Initial file inventory

**Phase 2 - Export**:
- `export_with_sections.py` - Quicksilver export with sections support

**Environment Setup**:
```bash
export FIGMA_ACCESS_TOKEN='your_token_here'
export QUICKSILVER_API_TIMEOUT=60
export QUICKSILVER_CDN_TIMEOUT=120
```

---

## Related Documentation

- **Main repository CLAUDE.md**: `/Users/admin/Documents/claudecode/CLAUDE.md`
- **Simple tracking guide**: `/Users/admin/Documents/claudecode/justice-league-missions/SIMPLE-COST-TRACKING-GUIDE.md`
- **Complex tracking guide**: `/Users/admin/Documents/claudecode/justice-league-missions/expenses-global/EXPENSE-TRACKING-GUIDE.md`
- **Latest savepoint**: `/Users/admin/Documents/claudecode/justice-league-missions/PROJECT-SAVEPOINT-2025-11-03-SIMPLE-TRACKING.md`
- **Agent definitions**: `/Users/admin/Documents/claudecode/workspaces/auzmor/apps/unified-ds/docs/JUSTICE-LEAGUE-AGENTS.md`
- **Auzmor Unified DS**: `/Users/admin/Documents/claudecode/workspaces/auzmor/apps/unified-ds/`

---

**System Version**: 2.0.0 (Simple Cost Tracking)
**Last Updated**: 2025-11-03
**Maintained By**: Oracle (Justice League Coordinator)
**Account**: aldrinstellus@gmail.com (Claude Max $100/month)
