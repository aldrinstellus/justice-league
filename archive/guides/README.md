# Justice League Missions Tracking System

**Version**: 1.0.0
**Last Updated**: 2025-11-03
**Location**: `/claudecode/justice-league-missions/`

---

## 🎯 Overview

This is the centralized tracking system for all Justice League agent missions. It provides a scalable, Figma-centric structure designed to handle:

- **100s of Figma files** per project
- **100s of pages** per Figma file
- **1000s of frames, sections, and components**
- **Complete mission lifecycle tracking** (brief → execution → deliverables → metrics)

---

## 📁 Directory Structure

```
justice-league-missions/
├── MISSIONS.md                          # Master registry (START HERE)
├── README.md                            # This file
├── _templates/                          # Mission templates
│   ├── mission-brief.md                 # Mission objective template
│   ├── metrics.json                     # Metrics tracking template
│   └── mission-log.md                   # Mission log template
└── missions/                            # All mission folders
    ├── JL-001-tweakcn-research/         # Mission 1
    │   ├── mission-brief.md
    │   ├── mission-log.md
    │   ├── metrics.json
    │   └── deliverables/
    │       ├── research/
    │       ├── prd/
    │       └── architecture/
    └── JL-002-auzmor-learn-figma/       # Mission 2 (Figma-centric)
        ├── mission-brief.md
        ├── mission-log.md
        ├── metrics.json
        └── figma-files/                 # Figma hierarchy
            ├── Q3-2025-LXP-Mobile/
            │   ├── pages/
            │   │   ├── 01-home/
            │   │   ├── 02-courses/
            │   │   └── 03-profile/
            │   └── analysis.md
            ├── Q2-2025-Product-Enhancements/
            │   ├── pages/
            │   └── analysis.md
            └── Q1-2024-LXP-Web/
                ├── pages/
                └── analysis.md
```

---

## 🚀 Quick Start

### Creating a New Mission

**Step 1: Determine Mission Number**
- Check `MISSIONS.md` for the latest mission ID
- Increment by 1 (e.g., if latest is JL-002, next is JL-003)

**Step 2: Create Mission Folder**
```bash
cd /Users/admin/Documents/claudecode/justice-league-missions/missions
mkdir JL-XXX-mission-name
cd JL-XXX-mission-name
```

**Step 3: Copy Templates**
```bash
cp ../_templates/mission-brief.md .
cp ../_templates/metrics.json .
cp ../_templates/mission-log.md .
```

**Step 4: Fill Out Mission Brief**
- Edit `mission-brief.md` with objective, agents, deliverables, Figma files (if applicable)

**Step 5: Create Folder Structure**
- **For Figma missions**: Create `figma-files/` folder
- **For other missions**: Create `deliverables/` folder

**Step 6: Check Budget & Create Expense Tracking**
- **IMPORTANT**: Check `/expenses-global/reports/decision-dashboard.md` BEFORE starting mission
- Confirm available budget for the month
- Create expense tracking folder: `mkdir expenses/{config,logs,reports}`
- Copy expense templates from `_templates/expenses/`

**Step 7: Update Master Registry**
- Add mission entry to `MISSIONS.md` in "Active Missions" section
- Update `/expenses-global/cumulative-expenses.json` with new mission

---

## 💰 Expense Tracking System

### Overview

**Account**: aldrinstellus@gmail.com (Claude Max plan)
**Monthly Budget**: ~$200 (estimated for Claude Max)
**Tracking Levels**: Per-activity, per-task, per-file, per-phase, per-agent, per-mission

### Before Starting ANY Mission

**STEP 1**: Check the Decision Dashboard
```bash
cat expenses-global/reports/decision-dashboard.md
```

**Look for**:
- ✅ Available budget (e.g., $29.77 remaining in November)
- ✅ Monthly status (e.g., 85.1% allocated)
- ✅ Can we afford this mission? (YES/NO decision table)

**If YES** → Proceed to create mission
**If NO** → Wait for next month OR reduce scope OR optimize heavily

### Global Expense Files

| File | Purpose | When to Check |
|------|---------|---------------|
| `/expenses-global/account-config.json` | Claude Max plan details | Setup only |
| `/expenses-global/cumulative-expenses.json` | All-time totals across missions | Real-time |
| `/expenses-global/mission-forecasts.json` | Future mission cost estimates | Before planning |
| `/expenses-global/reports/decision-dashboard.md` | **GO/NO-GO for new missions** | **Before EVERY mission** |
| `/expenses-global/reports/global-summary.md` | Performance overview | Monthly |
| `/expenses-global/EXPENSE-TRACKING-GUIDE.md` | Complete usage guide | Reference |

### Per-Mission Expense Tracking

Each mission has `/expenses/` folder:
```
JL-XXX/expenses/
├── config/
│   ├── pricing-config.json      # AI model pricing (Claude Sonnet/Haiku)
│   └── budget-limits.json        # Mission budget by phase/agent
├── logs/
│   └── expense-log.json          # All activities with token counts & costs
└── reports/
    └── expense-summary.md        # Budget status and optimization plan
```

### Cost Optimization (60-70% Savings Possible)

**Strategy 1: Model Selection** (73% savings)
- Use **Haiku** for simple tasks (cataloging, coordination, synthesis)
- Use **Sonnet** for complex tasks (analysis, architecture, research)
- Example: Oracle uses Haiku → saves 73% vs Sonnet

**Strategy 2: Prompt Caching** (90% savings)
- Enable for repeated file analysis (100 Figma files)
- Cache design system docs, reuse across files
- Example: JL-003 could save $45 (36% of budget)

**Strategy 3: Batch API** (50% savings)
- Use for non-urgent tasks (synthesis, reporting, documentation)
- Example: Generate 50 component docs → save $12.50

**Combined**: $125 mission → $50 with full optimization (60% reduction)

### Quick Reference

**Current Month Status** (November 2025):
- Budget: $200
- Spent: $45.23 (JL-001 completed)
- Committed: $125 (JL-003 active)
- Available: $29.77
- Status: ⚠️ New missions <$30 only OR wait for December

**For Details**: See `/expenses-global/EXPENSE-TRACKING-GUIDE.md`

---

## 📊 Figma-Centric Organization

### When to Use Figma Structure

Use the Figma-centric structure when the mission involves:
- Analyzing Figma design files
- Consolidating design systems from Figma
- Creating component libraries from Figma
- Design-to-code conversions

### Figma Folder Hierarchy

```
figma-files/
├── {figma-file-name}/           # Top-level Figma file (100s)
│   ├── pages/                   # All pages in this file
│   │   ├── 01-page-name/        # Individual page (numbered)
│   │   │   ├── sections/        # Sections within page (if needed)
│   │   │   └── frames/          # Frames within page (if needed)
│   │   └── 02-another-page/
│   └── analysis.md              # Summary of entire file
└── {another-figma-file}/
    └── ...
```

### Naming Conventions

**Figma File Folders**:
- Use kebab-case: `Q3-2025-LXP-Mobile`
- Remove special characters: `(` `)` `,` `-` becomes `-`
- Keep original naming context (quarter, year, product name)

**Page Folders**:
- Prefix with numbers: `01-`, `02-`, `03-`
- Use kebab-case: `01-home-screen`, `02-course-catalog`
- Numbers ensure sorted order

**Analysis Files**:
- One `analysis.md` per Figma file (not per page)
- Summarizes all pages, key components, design patterns

### Example: Auzmor Learn Figma Project

```
figma-files/
├── Q3-2025-LXP-Mobile/
│   ├── pages/
│   │   ├── 01-onboarding/
│   │   ├── 02-home-dashboard/
│   │   ├── 03-course-catalog/
│   │   ├── 04-course-detail/
│   │   ├── 05-learning-path/
│   │   └── 06-profile-settings/
│   └── analysis.md              # Summarizes all 6 pages
├── Q2-2025-Product-Enhancements/
│   ├── pages/
│   │   ├── 01-new-search-feature/
│   │   └── 02-improved-navigation/
│   └── analysis.md
└── Q1-2024-LXP-Web/
    └── analysis.md
```

---

## 📝 Mission Lifecycle

### 1. Planning Phase
- Create mission folder
- Fill out `mission-brief.md` (objective, agents, Figma files, deliverables)
- Update `MISSIONS.md` (add to "Active Missions")

### 2. Execution Phase
- Agents execute research, analysis, design work
- Log progress in `mission-log.md` (chronological updates)
- Create deliverables in appropriate folders

### 3. Completion Phase
- Update `metrics.json` with final metrics (time, tokens, files processed, docs created)
- Move mission from "Active" to "Completed" in `MISSIONS.md`
- Add final summary to `mission-log.md`

---

## 📋 Templates Guide

### mission-brief.md
**Purpose**: Define mission objective, scope, and expected deliverables

**Sections**:
- Mission ID and Name
- Objective (what are we trying to achieve?)
- Agents Deployed (which Justice League members?)
- Figma Files (if applicable - list all files to process)
- Deliverables (what outputs are expected?)
- Success Criteria (how do we know we're done?)

### metrics.json
**Purpose**: Track quantitative mission performance

**Metrics**:
- `mission_id`: Mission identifier
- `start_date`: Start timestamp
- `end_date`: End timestamp (null if active)
- `time_spent_hours`: Total hours spent
- `tokens_used`: Approximate token count
- `figma_files_processed`: Number of Figma files analyzed
- `figma_pages_processed`: Number of Figma pages analyzed
- `documents_created`: Number of markdown/spec files created
- `lines_of_documentation`: Total lines across all docs

### mission-log.md
**Purpose**: Chronological log of mission progress

**Format**:
```markdown
## [Date] - [Update Title]
**Agent**: [Agent Name]
**Activity**: [What was done]
**Outputs**: [Files/folders created]
**Next Steps**: [What's next]
```

---

## 🔍 Navigation & Search Strategies

### Finding Missions

**By Mission ID**:
```bash
cd missions/JL-XXX-*
```

**By Figma File Name**:
```bash
find missions -type d -name "*LXP-Mobile*"
```

**By Agent**:
```bash
grep -r "Wonder Woman" missions/*/mission-brief.md
```

**By Date**:
```bash
grep -r "2025-11-03" missions/*/mission-log.md
```

### Master Registry Search

The `MISSIONS.md` file is your **single source of truth**:
- All missions listed in one place
- Table format for easy scanning
- Quick links to mission folders
- Summary metrics

**Tip**: Open `MISSIONS.md` first, then navigate to specific mission folders.

---

## 📏 Scaling Guidelines

### Handling 100s of Figma Files

**Strategy**: Keep Figma files at top level of `figma-files/` folder
- ✅ Flat structure: `figma-files/File1/`, `figma-files/File2/`
- ❌ Avoid deep nesting: `figma-files/Category/Subcategory/File1/`

**Reason**: Makes searching and navigation easier at scale

### Handling 100s of Pages per File

**Strategy**: Use numbered prefixes and `pages/` subfolder
- ✅ `pages/01-home/`, `pages/02-courses/`, ..., `pages/99-settings/`
- ✅ Groups related pages together
- ✅ Sorted order guaranteed

**Reason**: File systems handle 100s of folders well when numbered

### Handling 1000s of Components

**Strategy**: Summarize in `analysis.md`, don't create folders for every component
- ✅ `analysis.md` lists all components with descriptions
- ✅ Create folders only for components you're actively converting/analyzing
- ❌ Don't create 1000 individual component folders

**Reason**: Balance detail with usability

---

## 🦸 Justice League Agents

### Active Agents

**Wonder Woman** - Product Manager
- Research, competitive analysis
- PRD creation, user stories
- Success metrics, feature prioritization

**Aldrin** - Design Systems Master
- Token architecture, theming
- Component analysis, accessibility
- Real-time systems, performance optimization

**Oracle** - Coordinator
- Multi-agent coordination
- Knowledge synthesis
- Mission planning, documentation

### Future Agents

**Martian Manhunter** - Security Specialist
**Atom** - Component Analysis
**Plastic Man** - Responsive Design
**Zatanna** - SEO & Accessibility
**Litty** - Ethics & Compliance

---

## 📈 Metrics & Reporting

### Per-Mission Metrics

Track in `metrics.json`:
- Time spent (hours)
- Tokens used (approximate)
- Figma files processed
- Pages analyzed
- Documents created
- Lines of documentation

### Aggregate Metrics

View in `MISSIONS.md` → "Metrics Summary" section:
- Total missions
- Total Figma files processed
- Total pages analyzed
- Total documents created
- Average mission duration

---

## 🎓 Best Practices

### Do's ✅

- **Always update `MISSIONS.md`** when starting/completing missions
- **Use templates** for consistency
- **Number pages** for sorted order (01-, 02-, 03-)
- **Create `analysis.md`** per Figma file (not per page)
- **Log progress** in `mission-log.md` during execution
- **Fill metrics** at mission completion

### Don'ts ❌

- **Don't skip mission IDs** (always sequential)
- **Don't create folders for every component** (summarize instead)
- **Don't nest deeply** (keep structure flat when possible)
- **Don't forget to move missions** from "Active" to "Completed" in `MISSIONS.md`
- **Don't duplicate mission IDs** (never reuse)

---

## 🔗 Related Documentation

- **Auzmor Unified DS**: `/workspaces/auzmor/apps/unified-ds/`
- **Agent Definitions**: `/workspaces/auzmor/apps/unified-ds/docs/JUSTICE-LEAGUE-AGENTS.md`
- **Repository Root**: `/CLAUDE.md`

---

## 📞 Support

**Questions about the system?**
- Read this README first
- Check `MISSIONS.md` for examples
- Review `_templates/` for template usage
- Consult existing missions (`JL-001`, `JL-002`) for reference

---

**Created**: 2025-11-03
**Last Updated**: 2025-11-03
**Version**: 1.0.0
**Maintained By**: Oracle (Justice League Coordinator)
