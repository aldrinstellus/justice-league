# Mission Folder Structure Guide

**Version**: 2.0  
**Last Updated**: 2025-11-03  
**Purpose**: Standard folder organization for all Justice League missions

---

## 📋 Standard Structure

Every mission folder should follow this structure:

```
JL-XXX-mission-name/
├── README.md                      # Mission overview & quick start
├── SUMMARY-FOR-ALDO.md           # Final summary (cost-first structure)
├── mission-brief.md               # Objectives, scope, deliverables
├── mission-log.md                 # Chronological progress updates
├── metrics.json                   # Performance tracking
│
├── inputs/                        # Source materials
│   ├── requirements.md
│   ├── reference-docs/
│   └── source-files/
│
├── scripts/                       # Processing scripts by phase
│   ├── phase1-[name]/
│   │   └── *.py, *.js, etc.
│   ├── phase2-[name]/
│   └── phase3-[name]/
│
├── outputs/                       # All outputs with iteration tracking
│   ├── phase1-[name]/
│   │   ├── iteration-01/          # First attempt
│   │   ├── iteration-02/          # Revision
│   │   ├── iteration-03/          # Additional revision (if needed)
│   │   └── FINAL -> iteration-XX  # Symlink to approved iteration
│   ├── phase2-[name]/
│   │   └── [same structure]
│   └── phase3-[name]/
│       └── [same structure]
│
├── exports/                       # Mission deliverables (optional)
│   ├── [format-type]/             # e.g., png/, pdf/, html/
│   └── archive/                   # Old/deprecated exports
│
└── expenses/                      # Budget tracking
    ├── config/
    │   ├── pricing-config.json
    │   └── budget-limits.json
    ├── logs/
    │   └── expense-log.json
    └── reports/
        └── expense-summary.md
```

---

## 🎯 Key Principles

### 1. Clean Root Directory
**Keep only mission documents at root level:**
- README.md (quick start guide)
- SUMMARY-FOR-ALDO.md (final summary - created at end)
- mission-brief.md (objectives)
- mission-log.md (progress)
- metrics.json (tracking)

**Everything else goes in subfolders!**

### 2. Phase-Based Organization
- Scripts organized by phase: `scripts/phase1-discovery/`
- Outputs organized by phase: `outputs/phase1-discovery/`
- Phase names should be descriptive: `phase1-discovery`, `phase2-export`, `phase3-documentation`

### 3. Iteration Tracking
- Each phase output has iterations: `iteration-01`, `iteration-02`, etc.
- Always use a `FINAL` symlink pointing to the approved iteration
- Keep at least 2 most recent iterations, archive older ones

### 4. FINAL Symlink
```bash
# Create FINAL symlink
cd outputs/phase1-discovery/
ln -s iteration-02 FINAL

# Update FINAL symlink
rm FINAL
ln -s iteration-03 FINAL

# Access latest approved output
cat outputs/phase1-discovery/FINAL/results.json
```

---

## 📝 Naming Conventions

### Phases
- `phase1-discovery` - Initial research/analysis
- `phase2-export` - Export/generation phase
- `phase3-documentation` - Documentation phase
- Use descriptive names, not just numbers

### Iterations
- `iteration-01` - First attempt
- `iteration-02` - Second attempt (revision)
- `iteration-03` - Third attempt (if needed)
- Always zero-padded for sorting

### Exports
- Organize by type: `png/`, `pdf/`, `html/`
- Use year-based subfolders: `2025/`, `2024/`
- Archive old exports: `archive/`

---

## 🚀 Workflow

### Starting a New Phase

```bash
# 1. Create phase folders
mkdir -p scripts/phase2-export
mkdir -p outputs/phase2-export/iteration-01

# 2. Add scripts
cd scripts/phase2-export/
# ... create/copy scripts here

# 3. Run phase work
python3 scripts/phase2-export/main_script.py

# 4. Save outputs to iteration folder
# ... outputs saved to outputs/phase2-export/iteration-01/

# 5. After approval, create FINAL symlink
cd outputs/phase2-export/
ln -s iteration-01 FINAL
```

### Creating a Revision

```bash
# 1. Create new iteration folder
cd outputs/phase2-export/
mkdir iteration-02

# 2. Make changes, save to iteration-02/

# 3. After approval, update FINAL symlink
rm FINAL
ln -s iteration-02 FINAL
```

### Cleaning Up

```bash
# After multiple iterations, archive old ones
cd outputs/phase2-export/
tar -czf iterations-archive-2025-11-03.tar.gz iteration-01 iteration-02
mv iterations-archive-2025-11-03.tar.gz ../../exports/archive/
rm -rf iteration-01 iteration-02
# Keep FINAL and latest 2 iterations
```

---

## 📂 Folder Purposes

### inputs/
- Source materials provided by Aldo
- Requirements documents
- Reference files
- Design files (small references only)

### scripts/
- Processing/analysis scripts
- Export scripts
- Automation tools
- Organized by phase

### outputs/
- All generated analysis results
- Reports, summaries, data files
- Iteration-tracked for versioning
- FINAL symlink points to approved version

### exports/
- Final deliverables for Aldo
- Figma exports, PDFs, documentation
- Organized by type and year
- Archive for old/deprecated exports

### expenses/
- Budget tracking (standard structure)
- Config, logs, reports
- Per-mission expense tracking

---

## ✅ Best Practices

### DO:
- ✅ Use descriptive phase names (`phase1-discovery` not `phase1`)
- ✅ Create new iteration for each major revision
- ✅ Update FINAL symlink after approval
- ✅ Keep outputs organized by phase
- ✅ Document structure in README.md
- ✅ Archive old iterations after validation

### DON'T:
- ❌ Put scripts at root level
- ❌ Put outputs at root level
- ❌ Skip iteration tracking
- ❌ Forget to update FINAL symlink
- ❌ Delete all old iterations (keep latest 2)
- ❌ Mix different phase outputs in same folder

---

## 📊 Example: JL-003 Structure

See `missions/JL-003-auzmor-learn-web-mobile/` for a complete example of this structure in action.

Key features demonstrated:
- Phase 1 with 2 iterations
- FINAL symlink pointing to iteration-02
- Scripts organized in scripts/phase1-discovery/
- Clean root directory with only mission docs
- Ready for Phase 2 with pre-created folders

---

## 🔧 Quick Setup Script

```bash
#!/bin/bash
# Create new mission with standard structure

MISSION_ID=$1
MISSION_NAME=$2

cd missions/
mkdir -p ${MISSION_ID}-${MISSION_NAME}/{inputs,scripts/{phase1,phase2,phase3},outputs/{phase1,phase2,phase3},exports/{archive},expenses/{config,logs,reports}}

# Copy templates
cp ../_templates/mission-brief.md ${MISSION_ID}-${MISSION_NAME}/
cp ../_templates/mission-log.md ${MISSION_ID}-${MISSION_NAME}/
cp ../_templates/metrics.json ${MISSION_ID}-${MISSION_NAME}/
cp ../_templates/README-TEMPLATE.md ${MISSION_ID}-${MISSION_NAME}/README.md

echo "✅ Mission folder created: ${MISSION_ID}-${MISSION_NAME}"
```

---

**Guide Version**: 2.0  
**Created**: 2025-11-03  
**Maintained By**: Oracle (Justice League Mission Control)  
**Based On**: JL-003 Phase 1 experience
