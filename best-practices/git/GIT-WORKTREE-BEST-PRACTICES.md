# Git Worktree Best Practices for Claude Code Agents

**Last Updated**: 2025-12-08
**Version**: 1.0.0
**Purpose**: Prevent common git worktree issues in parallel development

---

## Executive Summary

This guide addresses recurring issues with git worktrees in Claude Code parallel development sessions.

**Common Issues Diagnosed**:
1. Commits not saved to feature branches (work done directly on main)
2. Stale worktrees blocking new worktree creation
3. Feature branches not diverging from base
4. Merge conflicts from uncommitted work in worktrees

**Solution**: A structured workflow with verification steps at each stage.

---

## Table of Contents

1. [Diagnosed Issues](#diagnosed-issues)
2. [The Correct Workflow](#the-correct-workflow)
3. [Pre-Flight Checklist](#pre-flight-checklist)
4. [Creating Worktrees Properly](#creating-worktrees-properly)
5. [Working in Worktrees](#working-in-worktrees)
6. [Committing and Merging](#committing-and-merging)
7. [Cleanup Protocol](#cleanup-protocol)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Claude Code Agent Instructions](#claude-code-agent-instructions)

---

## Diagnosed Issues

### Issue 1: Work Not Committed to Feature Branches

**What Happened** (ATCK! December 8, 2025):
- Created 6 worktrees for parallel feature development
- Work was done, but commits ended up directly on main
- Feature branches showed same commit as base (`d3969e8`)
- No actual divergence occurred

**Root Cause**: Agents worked in worktrees but:
- Did not commit within the worktree
- Or committed to detached HEAD
- Or work was merged directly to main bypassing branches

**Prevention**: Always verify commits are on the correct branch BEFORE merging.

### Issue 2: Stale Worktrees

**What Happened**:
```
fatal: '/private/tmp/atck-worktrees/file-attachments' is a missing but already registered worktree
```

**Root Cause**: Previous worktrees were deleted from filesystem but not from git's worktree registry.

**Prevention**: Always use `git worktree prune` before creating new worktrees.

### Issue 3: Branch Already Checked Out

**What Happened**:
```
fatal: 'feat/my-feature' is already checked out at '/path/to/main'
```

**Root Cause**: Trying to create worktree with a branch already checked out elsewhere.

**Prevention**: Use detached HEAD or unique branch names per worktree.

---

## The Correct Workflow

### Phase 1: Setup (CRITICAL)

```bash
# 1. Prune stale worktrees FIRST
git worktree prune

# 2. Verify clean state
git worktree list
# Should only show main worktree

# 3. Ensure main is up to date
git checkout main
git pull origin main
```

### Phase 2: Create Feature Branches BEFORE Worktrees

```bash
# Create all feature branches from main
git branch feat/file-attachments
git branch feat/task-templates
git branch feat/recurring-tasks
# etc.

# Verify branches exist
git branch -a | grep feat/
```

### Phase 3: Create Worktrees with Branches

```bash
# Create worktrees linked to branches
git worktree add /tmp/atck-worktrees/file-attachments feat/file-attachments
git worktree add /tmp/atck-worktrees/task-templates feat/task-templates
git worktree add /tmp/atck-worktrees/recurring-tasks feat/recurring-tasks

# Verify worktrees
git worktree list
```

### Phase 4: Work in Worktrees

```bash
# Navigate to worktree
cd /tmp/atck-worktrees/file-attachments

# Verify correct branch
git branch --show-current  # Should show: feat/file-attachments

# Make changes, stage, commit
git add .
git commit -m "feat: implement file attachments"

# VERIFY commit is on branch
git log --oneline -1  # Should show new commit
```

### Phase 5: Merge Feature Branches

```bash
# Return to main worktree
cd /path/to/main/repo

# Merge each feature branch
git checkout main
git merge feat/file-attachments --no-ff -m "Merge feat/file-attachments"
git merge feat/task-templates --no-ff -m "Merge feat/task-templates"
# etc.
```

### Phase 6: Cleanup

```bash
# Remove worktrees
git worktree remove /tmp/atck-worktrees/file-attachments
git worktree remove /tmp/atck-worktrees/task-templates
# etc.

# Optionally delete merged branches
git branch -d feat/file-attachments
git branch -d feat/task-templates

# Final prune
git worktree prune
```

---

## Pre-Flight Checklist

**BEFORE creating any worktrees, verify:**

```bash
# 1. Clean git state
git status
# Expected: "nothing to commit, working tree clean"

# 2. No stale worktrees
git worktree prune
git worktree list
# Expected: Only main worktree listed

# 3. Main is up to date
git fetch origin
git log --oneline HEAD..origin/main
# Expected: No commits (already up to date)

# 4. Base directory exists and is writable
ls -la /tmp/atck-worktrees/ 2>/dev/null || mkdir -p /tmp/atck-worktrees

# 5. Sufficient disk space (each worktree is full repo copy minus .git objects)
df -h /tmp
```

---

## Creating Worktrees Properly

### Method 1: New Branch (Recommended)

```bash
# Creates branch and worktree in one command
git worktree add -b feat/new-feature /tmp/worktrees/new-feature main
```

### Method 2: Existing Branch

```bash
# Branch must exist and NOT be checked out elsewhere
git branch feat/existing-feature  # Create if needed
git worktree add /tmp/worktrees/existing-feature feat/existing-feature
```

### Method 3: Detached HEAD (For Read-Only Work)

```bash
# Creates worktree at specific commit, no branch
git worktree add --detach /tmp/worktrees/investigation HEAD
```

### Naming Conventions

| Worktree Location | Branch Name | Purpose |
|-------------------|-------------|---------|
| `/tmp/{project}-worktrees/{feature}` | `feat/{feature}` | Feature development |
| `/tmp/{project}-worktrees/fix-{bug}` | `fix/{bug-id}` | Bug fixes |
| `/tmp/{project}-worktrees/test-{name}` | `test/{name}` | Testing |

---

## Working in Worktrees

### Verify Before Working

```bash
# ALWAYS verify you're on the right branch
cd /tmp/atck-worktrees/file-attachments
git branch --show-current
# Must show: feat/file-attachments

# If it shows nothing or wrong branch, FIX IT:
git checkout feat/file-attachments
```

### Commit Frequently

```bash
# Stage all changes
git add .

# Commit with descriptive message
git commit -m "feat: add FileUpload component with drag-and-drop"

# VERIFY commit is on feature branch
git log --oneline -3
# First commit should be your new commit, second should be base
```

### Sync with Main (If Long-Running)

```bash
# Pull latest main into feature branch
git fetch origin main
git merge origin/main --no-edit

# OR rebase (cleaner history)
git rebase origin/main
```

---

## Committing and Merging

### Before Merging: Verification Checklist

```bash
# 1. Check each worktree has commits
for wt in /tmp/atck-worktrees/*/; do
  echo "=== $(basename $wt) ==="
  git -C "$wt" log --oneline -1
  git -C "$wt" log --oneline main..HEAD | wc -l | xargs echo "Commits ahead of main:"
done

# 2. Verify no uncommitted changes
for wt in /tmp/atck-worktrees/*/; do
  echo "=== $(basename $wt) ==="
  git -C "$wt" status --short
done
# Should be empty for all worktrees
```

### Merging Options

**Option A: Merge Commits (Preserves History)**
```bash
git checkout main
git merge feat/file-attachments --no-ff -m "Merge feat/file-attachments: Add file upload with Supabase Storage"
```

**Option B: Squash Merge (Clean Single Commit)**
```bash
git checkout main
git merge --squash feat/file-attachments
git commit -m "feat: implement file attachments with drag-and-drop upload"
```

**Option C: Rebase and Fast-Forward (Linear History)**
```bash
git checkout feat/file-attachments
git rebase main
git checkout main
git merge feat/file-attachments --ff-only
```

### Post-Merge Verification

```bash
# Verify merge succeeded
git log --oneline -5
# Should show merge commit(s)

# Verify features are present
ls src/components/FileUpload.tsx  # Example
```

---

## Cleanup Protocol

### Standard Cleanup

```bash
# 1. Remove worktrees (AFTER merging)
git worktree remove /tmp/atck-worktrees/file-attachments
git worktree remove /tmp/atck-worktrees/task-templates
# etc.

# 2. Delete merged branches
git branch -d feat/file-attachments
git branch -d feat/task-templates

# 3. Prune worktree metadata
git worktree prune

# 4. Verify clean state
git worktree list
git branch -a | grep feat/
```

### Force Cleanup (If Errors)

```bash
# Force remove worktree with uncommitted changes
git worktree remove --force /tmp/atck-worktrees/problematic-worktree

# Force delete branch
git branch -D feat/abandoned-feature

# Clean up orphaned worktree directories
rm -rf /tmp/atck-worktrees/*
git worktree prune
```

### Automated Cleanup Script

```bash
#!/bin/bash
# cleanup-worktrees.sh

WORKTREE_BASE="/tmp/atck-worktrees"

echo "=== Worktree Cleanup ==="

# Check for uncommitted changes
for wt in "$WORKTREE_BASE"/*/; do
  if [ -d "$wt" ]; then
    name=$(basename "$wt")
    changes=$(git -C "$wt" status --porcelain 2>/dev/null | wc -l)
    if [ "$changes" -gt 0 ]; then
      echo "WARNING: $name has $changes uncommitted changes"
    fi
  fi
done

read -p "Proceed with cleanup? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  git worktree prune
  for wt in "$WORKTREE_BASE"/*/; do
    if [ -d "$wt" ]; then
      git worktree remove --force "$wt" 2>/dev/null
      echo "Removed: $(basename $wt)"
    fi
  done
  git worktree prune
  echo "Cleanup complete"
fi
```

---

## Troubleshooting Guide

### Error: "is a missing but already registered worktree"

**Solution**:
```bash
git worktree prune
git worktree add /path/to/worktree branch-name
```

### Error: "branch is already checked out"

**Solutions**:

1. Use a different branch name:
```bash
git worktree add -b feat/file-attachments-v2 /tmp/worktrees/file-attachments
```

2. Use detached HEAD:
```bash
git worktree add --detach /tmp/worktrees/file-attachments HEAD
```

### Error: "fatal: invalid reference"

**Solution**:
```bash
# Verify branch exists
git branch -a | grep your-branch

# If not, create it first
git branch your-branch
git worktree add /tmp/worktrees/your-branch your-branch
```

### Error: "worktree contains modified or untracked files"

**Solutions**:

1. Commit the changes:
```bash
cd /path/to/worktree
git add .
git commit -m "WIP: saving changes before cleanup"
```

2. Force remove:
```bash
git worktree remove --force /path/to/worktree
```

### Commits Not Showing on Branch

**Diagnosis**:
```bash
cd /path/to/worktree
git log --oneline -3
git branch --show-current
git log main..HEAD --oneline
```

**If detached HEAD** (no branch shown):
```bash
# Create branch from current state
git checkout -b feat/recovered-work

# Push or merge as needed
```

---

## Claude Code Agent Instructions

### For Task Agents Running Parallel Features

**MANDATORY: Include these steps in your workflow:**

```markdown
## Git Worktree Workflow (FOLLOW EXACTLY)

### Step 1: Prune Before Creating
git worktree prune

### Step 2: Create Branch and Worktree
git worktree add -b feat/my-feature /tmp/project-worktrees/my-feature main

### Step 3: Navigate and Verify
cd /tmp/project-worktrees/my-feature
git branch --show-current  # MUST show feat/my-feature

### Step 4: Do Work and Commit
# ... make changes ...
git add .
git commit -m "feat: description of changes"

### Step 5: Verify Commit
git log --oneline -1  # MUST show your new commit
git log main..HEAD --oneline  # MUST show commits ahead of main

### Step 6: Report Back
Return these verification outputs in your final report.
```

### For Superman/Coordinator Agents

**MANDATORY: Verification after parallel agent completion:**

```bash
# Run this after all parallel agents complete
echo "=== Verifying Parallel Worktree Results ==="

for wt in /tmp/*-worktrees/*/; do
  name=$(basename "$wt")
  echo ""
  echo "=== $name ==="

  # Check branch
  branch=$(git -C "$wt" branch --show-current 2>/dev/null)
  echo "Branch: $branch"

  # Check commits ahead of main
  commits=$(git -C "$wt" log main..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ')
  echo "Commits ahead: $commits"

  # Latest commit
  latest=$(git -C "$wt" log --oneline -1 2>/dev/null)
  echo "Latest: $latest"

  # Uncommitted changes
  changes=$(git -C "$wt" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  echo "Uncommitted changes: $changes"

  # Verification
  if [ "$commits" -gt 0 ] && [ "$changes" -eq 0 ]; then
    echo "Status: READY TO MERGE"
  else
    echo "Status: NEEDS ATTENTION"
  fi
done
```

---

## Quick Reference Card

### Essential Commands

| Task | Command |
|------|---------|
| Prune stale worktrees | `git worktree prune` |
| List worktrees | `git worktree list` |
| Create worktree + branch | `git worktree add -b feat/name /tmp/wt/name main` |
| Create worktree (existing branch) | `git worktree add /tmp/wt/name feat/name` |
| Verify branch | `git branch --show-current` |
| Commits ahead of main | `git log main..HEAD --oneline` |
| Remove worktree | `git worktree remove /tmp/wt/name` |
| Force remove | `git worktree remove --force /tmp/wt/name` |

### Workflow Checklist

- [ ] `git worktree prune` before starting
- [ ] Create branches before worktrees (or use `-b`)
- [ ] Verify branch with `git branch --show-current`
- [ ] Commit frequently in each worktree
- [ ] Verify commits with `git log main..HEAD`
- [ ] Merge with `--no-ff` to preserve history
- [ ] Remove worktrees after merging
- [ ] Delete merged branches
- [ ] Final `git worktree prune`

---

## Sources

- [Git Worktrees and Claude Code: A Guide for Developers in 2025](https://www.geeky-gadgets.com/how-to-use-git-worktrees-with-claude-code-for-seamless-multitasking/)
- [How Git Worktrees Changed My AI Agent Workflow | Nx Blog](https://nx.dev/blog/git-worktrees-ai-agents)
- [Git Worktrees + Claude Code: Effortless Parallel Development](https://medium.com/@francoisschuers/git-worktrees-claude-code-effortless-parallel-development-2a43e746c28c)
- [Using Git Worktrees for Parallel AI Development | Steve Kinney](https://stevekinney.com/courses/ai-development/git-worktrees)
- [Git worktree reference and best practices | GitHub Gist](https://gist.github.com/induratized/49cdedace4a200fa8ae32db9ba3e9a44)
- Justice League `git_worktree_manager.py` implementation
- Justice League `GIT_TREES_OPTIMIZATION_GUIDE.md`

---

**Version**: 1.0.0
**Author**: Justice League Documentation Team
**Last Updated**: 2025-12-08
