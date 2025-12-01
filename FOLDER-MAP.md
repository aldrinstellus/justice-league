# Claudecode Folder Map

**Version**: 1.0.0
**Last Updated**: 2025-12-01
**Maintained By**: Justice League System

---

## Quick Navigation

| Folder | Purpose | Size |
|--------|---------|------|
| `/apps/` | Production applications | ~3 GB |
| `/workspaces/` | Active development projects | ~32 GB |
| `/archive/` | Historical content | ~45 GB |
| `/justice-league-missions/` | Mission tracking system | ~10 MB |
| `/docs/` | Documentation | ~50 MB |
| `/tools/` | Utilities and automation | ~100 MB |
| `/clients/` | Client-specific materials | ~200 MB |
| `/design/` | Design system assets | ~500 MB |
| `/infrastructure/` | Deployment configs | ~20 MB |

---

## Root Structure

```
/Users/admin/Documents/claudecode/
├── .claude/                    # Claude Code configuration
├── .gitignore                  # Git ignore rules
├── .vscode/                    # VS Code settings
├── CLAUDE.md                   # Project instructions for Claude
├── FOLDER-MAP.md               # This file - folder navigation guide
├── README.md                   # Repository overview
│
├── apps/                       # Production applications
├── archive/                    # Historical/archived content
├── clients/                    # Client-specific materials
├── design/                     # Design system and assets
├── docs/                       # Documentation
├── infrastructure/             # Deployment and infrastructure
├── justice-league-missions/    # Mission tracking system
├── tools/                      # Utilities and automation
└── workspaces/                 # Active development projects
```

---

## /apps/ - Production Applications

```
apps/
├── atc-platform/       # ATC Platform (pnpm monorepo)
├── atc-task-manager/   # ATC Task Manager (Next.js 14)
└── atc-tasky/          # ATC Tasky application
```

**Naming Convention**: `kebab-case`
**Status**: Production-ready applications
**Template**: Each app should have `CLAUDE.md` at root

---

## /workspaces/ - Active Development

```
workspaces/
├── atck/                       # Primary active project
├── atc-tasky-g -> atck         # Symlink alias
├── auzmor/                     # Auzmor Learn project
├── bright-energy/              # Bright Energy project
├── enterprise-ai-support/      # Enterprise AI Support (v14+)
├── figma3react/                # Figma to React converter
├── figma4react/                # Figma React toolkit
├── framer/                     # Framer experiments
├── kombai/                     # Kombai integration
├── personal/                   # Personal projects
└── random-tests/               # Experimental code
```

**Naming Convention**: `kebab-case`
**Status**: Active development
**Required Files**: Each workspace MUST have `CLAUDE.md`

---

## /archive/ - Historical Content

```
archive/
├── misc/                # Miscellaneous archived items
├── missions-legacy/     # OLD mission system (36 GB) - DEPRECATED
├── monorepo-config/     # Old monorepo configurations
├── projects/            # Archived project files
├── savepoints/          # All session savepoints (organized by project)
│   ├── atck/
│   ├── atc-task-manager/
│   ├── best-practices/
│   └── docs/
├── scrap/               # Temporary/scrap files
├── screenshots/         # Archived screenshots
└── security/            # Security audit archives
```

**Purpose**: Keep historical content out of active folders
**Key Insight**: `missions-legacy/` is the OLD system (36 GB). Use `/justice-league-missions/` for all new work.

---

## /justice-league-missions/ - Active Mission System

```
justice-league-missions/
├── MISSIONS.md                 # Master registry - START HERE
├── README.md                   # System documentation
├── _templates/                 # Mission templates
├── expenses-global/            # Budget tracking
│   ├── reports/
│   │   └── decision-dashboard.md  # Budget status
│   └── EXPENSE-TRACKING-GUIDE.md
└── missions/                   # Active and completed missions
    └── JL-XXX-mission-name/
        ├── mission-brief.md
        ├── mission-log.md
        ├── metrics.json
        ├── expenses/
        └── deliverables/
```

**Important**: This is the CANONICAL mission system. Do NOT use `/archive/missions-legacy/`.

---

## /docs/ - Documentation

```
docs/
├── architecture/       # System architecture and ADRs
├── best-practices/     # Best practice guides
├── clients/            # Client-specific docs
│   ├── atc/
│   └── wisconsin-dnr/
├── reorganization/     # Reorganization history
└── *.md                # Various documentation files
```

**Naming Convention**: `kebab-case` for folders, `UPPER-CASE.md` for docs

---

## /clients/ - Client Materials

```
clients/
├── atc/                # ATC client materials
│   ├── platform -> /apps/atc-platform
│   └── task-manager -> /apps/atc-task-manager
└── wisconsin-dnr/      # Wisconsin DNR RFP
    ├── rfp/            # RFP documentation
    └── wireframes/     # Design wireframes
```

**Purpose**: Client-facing materials, symlinks to actual apps

---

## /design/ - Design System

```
design/
├── source/             # Source design files
│   ├── penpot/         # Penpot files
│   └── figma/          # Figma exports
├── assets/             # Design assets
│   ├── exports/        # PNG exports (2x scale)
│   ├── icons/          # SVG/PNG icons
│   └── images/         # Project images
└── conversions/        # Code conversions
    ├── shadcn/         # shadcn components
    └── tools/          # Conversion tools
```

---

## /tools/ - Utilities

```
tools/
├── automation/         # Automation scripts
│   └── aldo-vision/    # Justice League vision system
└── [other utilities]
```

---

## /infrastructure/ - Deployment

```
infrastructure/
└── launch-plan/        # Deployment procedures
    ├── terraform/      # AWS infrastructure
    └── kubernetes/     # K8s configs
```

---

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Folders | kebab-case | `enterprise-ai-support` |
| Documentation | UPPER-KEBAB-CASE.md | `FOLDER-MAP.md` |
| Savepoints | SAVEPOINT-YYYY-MM-DD-*.md | `SAVEPOINT-2025-12-01-FIX.md` |
| Missions | JL-XXX-description | `JL-003-auzmor-learn` |

---

## Key Rules

1. **New savepoints**: Go to `/archive/savepoints/{project}/`
2. **New missions**: Go to `/justice-league-missions/missions/`
3. **New workspaces**: Must have `CLAUDE.md` at root
4. **All folders**: Use `kebab-case` naming
5. **Never use**: `/archive/missions-legacy/` (deprecated)

---

## Before Creating New Projects

### Quick Decision Guide

```
Is it a production app?     → /apps/{client}-{product}/
Is it development work?     → /workspaces/{project-name}/
Is it client materials?     → /clients/{client-name}/
Is it a JL mission?         → /justice-league-missions/missions/JL-XXX/
Is it temporary/scratch?    → /archive/scrap/
```

### New Workspace Setup (Copy-Paste)

```bash
# 1. Create workspace with kebab-case name
mkdir -p workspaces/my-new-project

# 2. Copy CLAUDE.md template
cp _templates/WORKSPACE-CLAUDE.md workspaces/my-new-project/CLAUDE.md

# 3. Edit the CLAUDE.md with project details
# (update name, tech stack, commands)

# 4. Create savepoint directory if needed
mkdir -p archive/savepoints/my-new-project
```

### Pre-Commit Verification

Run before every commit to ensure organization:

```bash
# Should return NOTHING (no misplaced savepoints)
find . -name "*SAVEPOINT*" -not -path "./archive/*" -not -path "./.git/*"

# Should show all checkmarks (all workspaces have CLAUDE.md)
for ws in workspaces/*/; do [ -f "$ws/CLAUDE.md" ] && echo "✓ $ws" || echo "✗ MISSING: $ws"; done

# Should return NOTHING (no uppercase folder names)
find . -maxdepth 2 -type d -name "*[A-Z]*" -not -path "./.git/*"
```

---

## Storage Summary

| Category | Size | % of Total |
|----------|------|------------|
| Archive (legacy) | ~45 GB | 56% |
| Workspaces | ~32 GB | 40% |
| Apps | ~3 GB | 4% |
| Everything else | <1 GB | <1% |

**Total**: ~80 GB

---

## External Staging Folders (Temporary)

These folders exist outside the main claudecode directory for specific purposes:

### `/private/tmp/justice-league-update/`
**Purpose**: GitHub staging area for Justice League repository

```
/private/tmp/justice-league-update/
└── jl-push/                    # Git clone of github.com/aldrinstellus/justice-league
    ├── .claude/                # Skills mirror (synced from ~/.claude/)
    ├── core/                   # JL implementation code (2.2 MB)
    ├── docs/                   # Documentation (500 KB)
    ├── examples/               # Demo scripts and examples
    ├── missions/               # Mission archives
    ├── archive/                # Historical docs
    └── best-practices/         # Case studies
```

**Workflow**:
1. Make changes in production (`~/.claude/`)
2. Sync to staging (`jl-push/`)
3. Commit and push to GitHub

### `/private/tmp/jl-sync/`
**Purpose**: Temporary sync workspace (can be cleaned)

**Status**: Contains 300+ files from previous operations. Safe to archive or delete.

### Temp Folder Rules

| Folder | Persistence | Clean Policy |
|--------|-------------|--------------|
| `justice-league-update/jl-push/` | **Keep** | GitHub staging |
| `jl-sync/` | Temporary | Archive or delete |
| `jl-narrator-demo/` | Moved | → `jl-push/examples/` |

**Best Practice**: Always move useful temp content to proper locations before session ends.

---

**Maintainer**: Justice League Team
