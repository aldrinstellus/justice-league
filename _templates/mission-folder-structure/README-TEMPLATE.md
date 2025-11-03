# JL-XXX: [Mission Name] - Mission Folder

**Mission Status**: [Phase N] [Status]  
**Current Phase**: [Current Phase Description]  
**Budget**: $[X.XX] allocated

---

## 📁 Folder Structure

```
JL-XXX-mission-name/
├── README.md                      # This file - mission overview
├── SUMMARY-FOR-ALDO.md           # ⭐ Cost summary & results (create at end)
├── mission-brief.md               # Objectives & scope
├── mission-log.md                 # Progress tracking
├── metrics.json                   # Performance metrics
│
├── inputs/                        # Source materials & references
├── scripts/                       # Analysis & processing scripts
│   ├── phase1/
│   ├── phase2/
│   └── phase3/
│
├── outputs/                       # All outputs by phase with iterations
│   ├── phase1/
│   │   ├── iteration-01/
│   │   ├── iteration-02/
│   │   └── FINAL -> iteration-XX  # Symlink to approved iteration
│   ├── phase2/
│   └── phase3/
│
├── exports/                       # Deliverables (if applicable)
│   ├── png/
│   ├── pdf/
│   └── archive/
│
└── expenses/                      # Budget tracking
    ├── config/
    ├── logs/
    └── reports/
```

---

## 🚀 Quick Start

[Add mission-specific quick start commands]

---

## 📊 Phase Results

### Phase 1: [Phase Name]
- [Key metric 1]
- [Key metric 2]
- Status: [✅ Complete / ⏳ In Progress / ⏸️ Paused]

---

## 💡 Working with Iterations

### Creating a New Iteration
```bash
cd outputs/phaseN
mkdir iteration-XX
# ... do work in iteration-XX/
```

### Promoting to FINAL
```bash
cd outputs/phaseN
rm FINAL
ln -s iteration-XX FINAL
```

---

**Mission**: JL-XXX [Mission Name]  
**Last Updated**: [Date]  
**Maintained By**: Oracle (Justice League Mission Control)
