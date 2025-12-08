# Justice League Full Transfer Plan
## Date: 2025-12-08
## Status: Ready for Execution

---

## Executive Summary

This plan consolidates ALL custom Claude Code assets from `~/.claude/` into the `justice-league-github` repository, making it the single source of truth for the Justice League AI system.

### Current State
- **~/.claude/**: Active development, latest updates (Dec 4-8, 2025)
- **justice-league-github/**: Last sync Dec 1, 2025 (7 days behind)

### Gap Analysis
| Category | ~/.claude | justice-league | Gap |
|----------|-----------|----------------|-----|
| Hero Skills | 23 files | 22 files | Missing: bug-bot |
| Commands | 8 files | 10 files | Missing: bug-bot.md |
| Scripts | 6 files | 17 files | Need to merge (no overlap) |
| Agents | 11 files | 11 files | Sync (identical) |
| Roster | v3.1.0 (23 heroes) | v3.0.0 (22 heroes) | Update needed |

---

## Phase 1: New Assets (Missing from justice-league)

### 1.1 Bug-Bot Skill (NEW - Dec 8, 2025)
| Source | Destination |
|--------|-------------|
| `~/.claude/skills/bug-bot/SKILL.md` | `.claude/skills/bug-bot/SKILL.md` |
| `~/.claude/commands/bug-bot.md` | `.claude/commands/bug-bot.md` |

### 1.2 Updated Roster
| Source | Destination |
|--------|-------------|
| `~/.claude/justice-league-roster.md` | `justice-league-roster.md` |
| | `.claude/justice-league-roster.md` |

---

## Phase 2: Updated Skills (Newer in ~/.claude)

These hero skills have been updated since Dec 1:

| Hero | ~/.claude Date | Action |
|------|----------------|--------|
| aldrin.md | Dec 4 12:04 | Overwrite |
| artemis.md | Dec 4 12:04 | Overwrite |
| batman.md | Dec 3 18:25 | Overwrite |
| flash.md | Dec 3 18:25 | Overwrite |
| hephaestus.md | Dec 4 12:04 | Overwrite |
| oracle.md | Dec 4 12:04 | Overwrite |
| quicksilver.md | Dec 4 12:04 | Overwrite |
| the-architect.md | Dec 4 12:04 | Overwrite |

---

## Phase 3: Scripts to Add

Scripts in ~/.claude/scripts NOT in justice-league/scripts:

| Script | Purpose |
|--------|---------|
| `auto-learn.sh` | Automated learning extraction |
| `cleanup-temp-folders.sh` | Temp folder cleanup utility |
| `convert-to-gamma.py` | Markdown to Gamma.app converter |
| `detect_project.sh` | Project detection for /init |
| `extract-learnings.py` | Session learning extractor |
| `update-hero-skills.py` | Hero skill updater |

---

## Phase 4: Configuration Files

### 4.1 CLAUDE.md Updates Needed
The justice-league `.claude/CLAUDE.md` needs these additions from `~/.claude/CLAUDE.md`:

1. Bug-Bot Protocol section
2. Updated roster (23 heroes)
3. Cost Tracking Protocol (DEFACTO)
4. Next.js Dev Indicators Protocol
5. Global API Keys Protocol
6. Gamma Presentation Converter section
7. Auto-Savepoint Protocol updates

### 4.2 Other Config Files to Sync
| File | Action |
|------|--------|
| `AUTO-SAVEPOINT-PROTOCOL.md` | Compare and update |
| `mcp-workflows.md` | Compare and update |
| `oracle-reference.md` | Compare and update |

---

## Phase 5: Session Learnings & Savepoints

| Source | Destination |
|--------|-------------|
| `~/.claude/session-learnings/2025-12-03.md` | `.claude/session-learnings/` |
| `~/.claude/savepoints/customer-support-portal/` | `.claude/savepoints/` |
| `~/.claude/savepoints/SAVEPOINT-2025-12-01-21-HEROES.md` | `.claude/savepoints/` |
| `~/.claude/savepoints/SAVEPOINT-2025-12-01-FULL-MOBILIZATION.md` | `.claude/savepoints/` |

---

## Execution Commands

### Step 1: Create bug-bot skill folder
```bash
mkdir -p /Users/admin/Documents/claudecode/justice-league-github/.claude/skills/bug-bot
```

### Step 2: Copy new assets
```bash
# Bug-Bot skill
cp /Users/admin/.claude/skills/bug-bot/SKILL.md \
   /Users/admin/Documents/claudecode/justice-league-github/.claude/skills/bug-bot/

# Bug-Bot command
cp /Users/admin/.claude/commands/bug-bot.md \
   /Users/admin/Documents/claudecode/justice-league-github/.claude/commands/

# Updated roster
cp /Users/admin/.claude/justice-league-roster.md \
   /Users/admin/Documents/claudecode/justice-league-github/
cp /Users/admin/.claude/justice-league-roster.md \
   /Users/admin/Documents/claudecode/justice-league-github/.claude/
```

### Step 3: Update hero skills
```bash
for skill in aldrin artemis batman flash hephaestus oracle quicksilver the-architect; do
  cp /Users/admin/.claude/skills/$skill.md \
     /Users/admin/Documents/claudecode/justice-league-github/.claude/skills/
done
```

### Step 4: Add new scripts
```bash
cp /Users/admin/.claude/scripts/auto-learn.sh \
   /Users/admin/Documents/claudecode/justice-league-github/scripts/
cp /Users/admin/.claude/scripts/cleanup-temp-folders.sh \
   /Users/admin/Documents/claudecode/justice-league-github/scripts/
cp /Users/admin/.claude/scripts/convert-to-gamma.py \
   /Users/admin/Documents/claudecode/justice-league-github/scripts/
cp /Users/admin/.claude/scripts/detect_project.sh \
   /Users/admin/Documents/claudecode/justice-league-github/scripts/
cp /Users/admin/.claude/scripts/extract-learnings.py \
   /Users/admin/Documents/claudecode/justice-league-github/scripts/
cp /Users/admin/.claude/scripts/update-hero-skills.py \
   /Users/admin/Documents/claudecode/justice-league-github/scripts/
```

### Step 5: Sync session learnings
```bash
cp /Users/admin/.claude/session-learnings/2025-12-03.md \
   /Users/admin/Documents/claudecode/justice-league-github/.claude/session-learnings/
```

### Step 6: Sync savepoints
```bash
mkdir -p /Users/admin/Documents/claudecode/justice-league-github/.claude/savepoints/customer-support-portal
cp /Users/admin/.claude/savepoints/customer-support-portal/*.md \
   /Users/admin/Documents/claudecode/justice-league-github/.claude/savepoints/customer-support-portal/
cp /Users/admin/.claude/savepoints/SAVEPOINT-2025-12-01-*.md \
   /Users/admin/Documents/claudecode/justice-league-github/.claude/savepoints/
```

---

## Verification Checklist

After transfer, verify:

- [ ] Bug-Bot skill exists: `.claude/skills/bug-bot/SKILL.md`
- [ ] Bug-Bot command exists: `.claude/commands/bug-bot.md`
- [ ] Roster shows 23 heroes (including Bug-Bot)
- [ ] All 8 updated hero skills have Dec 3-4 dates
- [ ] 6 new scripts added to `scripts/`
- [ ] Session learnings synced
- [ ] Savepoints synced
- [ ] Git commit created
- [ ] Pushed to GitHub

---

## Post-Transfer: CLAUDE.md Update

The justice-league `.claude/CLAUDE.md` needs manual update to add:
1. Bug-Bot Protocol section (lines 145-190 from ~/.claude/CLAUDE.md)
2. Cost Tracking Protocol (DEFACTO) section
3. Next.js Dev Indicators Protocol
4. Updated hero count (22 → 23)

---

## Files Summary

| Category | Count | Action |
|----------|-------|--------|
| New skill folder | 1 | bug-bot |
| New command | 1 | bug-bot.md |
| Updated skills | 8 | Overwrite |
| New scripts | 6 | Add |
| Roster | 1 | Overwrite |
| Session learnings | 1 | Add |
| Savepoints | 3+ | Add |
| **Total files** | **~21** | |

---

## Estimated Time
- File transfers: 5 minutes
- CLAUDE.md updates: 10 minutes
- Verification: 5 minutes
- Git commit & push: 2 minutes
- **Total: ~22 minutes**

---

**Prepared by**: Superman 🦸
**Date**: 2025-12-08
**Status**: Ready for execution
