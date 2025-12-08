# Justice League - Git Worktree Training Summary

**Date**: 2025-12-08
**Trainer**: Superman (Mission Coordinator)
**Status**: MANDATORY Training - All Heroes
**Reference**: `/Users/admin/Documents/claudecode/justice-league-github/best-practices/git/GIT-WORKTREE-BEST-PRACTICES.md`

---

## Executive Summary

This training addresses recurring issues with git worktrees in parallel Claude Code development sessions. All Justice League heroes MUST follow these practices to prevent work from ending up on the wrong branch.

**Critical Issues Diagnosed**:
1. Work committed directly to `main` instead of feature branches
2. Stale worktrees blocking new worktree creation
3. Feature branches not diverging from base
4. Merge conflicts from uncommitted work

**Impact**: These issues caused failed deployments and lost work in the ATCK! project (December 8, 2025).

---

## Quick Reference Card (POST ON YOUR WALL!)

```
═══════════════════════════════════════════════════════════
   JUSTICE LEAGUE GIT WORKTREE QUICK REFERENCE
═══════════════════════════════════════════════════════════

BEFORE Creating Worktrees:
  git worktree prune

CREATE Worktree + Branch (ONE command):
  git worktree add -b feat/feature-name /tmp/worktrees/feature-name main

VERIFY You're on the Right Branch:
  git branch --show-current
  # MUST show: feat/feature-name (NOT main!)

COMMIT Your Work:
  git add .
  git commit -m "feat: description"

VERIFY Commits Are On Branch:
  git log main..HEAD --oneline
  # MUST show commits ahead of main!

BEFORE Merging - VERIFY ALL WORKTREES:
  for wt in /tmp/*-worktrees/*/; do
    commits=$(git -C "$wt" log main..HEAD --oneline | wc -l)
    if [ "$commits" -eq 0 ]; then
      echo "ERROR: No commits on $(basename $wt)"
    fi
  done

═══════════════════════════════════════════════════════════
```

---

## The CRITICAL "DO NOT" List

| DO NOT | WHY | CONSEQUENCE |
|--------|-----|-------------|
| ❌ Create worktree without `-b` flag | Creates detached HEAD or wrong branch | Work ends up on main |
| ❌ Skip `git worktree prune` before creating | Old entries block new worktrees | "already registered" errors |
| ❌ Forget to verify branch after creation | Might be on wrong branch | Commits go to main |
| ❌ Commit without checking branch first | Could be on detached HEAD | Lost work or wrong branch |
| ❌ Merge without verifying commits exist | Feature branch = base branch | Nothing to merge |
| ❌ Use same branch in multiple worktrees | Git blocks this | Errors or wrong state |
| ❌ Delete worktree folders manually | Leaves orphaned git entries | Registry corruption |

---

## Mandatory Verification Commands

### Step 1: Before Creating ANY Worktree
```bash
# Clean up stale worktrees (ALWAYS RUN THIS FIRST!)
git worktree prune

# Verify only main worktree exists
git worktree list
# Should show only one entry
```

### Step 2: After Creating Worktree
```bash
# Navigate to worktree
cd /tmp/project-worktrees/my-feature

# VERIFY branch is correct (CRITICAL!)
git branch --show-current
# MUST show: feat/my-feature (NOT blank, NOT main!)

# If blank or wrong, FIX IT:
git checkout -b feat/my-feature
```

### Step 3: After Committing Work
```bash
# Verify commit is on branch
git log --oneline -1
# Should show your new commit

# Verify commits ahead of main
git log main..HEAD --oneline
# MUST show at least one commit!
```

### Step 4: Before Reporting Success (Coordinators Only)
```bash
# Verify ALL worktrees have commits
for wt in /tmp/*-worktrees/*/; do
  echo "=== $(basename $wt) ==="
  git -C "$wt" branch --show-current
  git -C "$wt" log main..HEAD --oneline | wc -l | xargs echo "Commits ahead:"
done

# ALL worktrees must show commits ahead > 0
```

---

## Role-Specific Instructions

### Task Agents (Artemis, Hephaestus, Hawkman, etc.)

**Your Workflow**:
```markdown
## MANDATORY: Git Worktree Workflow (FOLLOW EXACTLY)

### Step 1: Prune Before Creating
git worktree prune

### Step 2: Create Branch and Worktree (ONE command)
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
Return verification outputs in your final report:
- Branch name
- Commit SHA
- Commits ahead of main
```

**Include in EVERY worktree task report**:
```
✅ Branch verified: feat/my-feature
✅ Commits ahead of main: 3
✅ Latest commit: abc1234 feat: implemented component
```

### Coordinator Agents (Superman, Oracle)

**Your Workflow**:
```bash
# AFTER all parallel agents complete, run this verification:
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
    echo "Status: ✅ READY TO MERGE"
  else
    echo "Status: ❌ NEEDS ATTENTION"
  fi
done
```

**ONLY merge if ALL worktrees show**:
- ✅ Commits ahead > 0
- ✅ Uncommitted changes = 0
- ✅ Branch is feature branch (NOT main)

---

## Common Failure Scenarios and Fixes

### Scenario 1: "No commits on feature branch"

**Diagnosis**:
```bash
cd /tmp/worktrees/my-feature
git log main..HEAD --oneline
# Shows nothing
```

**Cause**: Work was done on main or detached HEAD

**Fix**:
```bash
# Check what branch you're actually on
git branch --show-current

# If blank (detached HEAD), create branch from current state
git checkout -b feat/recovered-work

# If on main, create branch and cherry-pick commits
git checkout -b feat/my-feature
git cherry-pick <commit-sha>
```

### Scenario 2: "Worktree already registered"

**Diagnosis**:
```bash
git worktree add /tmp/worktrees/feature feat/feature
# fatal: '/tmp/worktrees/feature' is a missing but already registered worktree
```

**Cause**: Worktree deleted from filesystem but not from git registry

**Fix**:
```bash
# Prune stale entries
git worktree prune

# Now create worktree
git worktree add -b feat/feature /tmp/worktrees/feature main
```

### Scenario 3: "Branch is already checked out"

**Diagnosis**:
```bash
git worktree add /tmp/worktrees/feature feat/feature
# fatal: 'feat/feature' is already checked out at '/path/to/main'
```

**Cause**: Trying to check out same branch in multiple places

**Fix**:
```bash
# Option 1: Use different branch name
git worktree add -b feat/feature-v2 /tmp/worktrees/feature main

# Option 2: Checkout different branch in main first
cd /path/to/main
git checkout main
cd -
git worktree add /tmp/worktrees/feature feat/feature
```

---

## Training Verification Checklist

After completing this training, you MUST be able to:

- [ ] Explain why `git worktree prune` is run before creating worktrees
- [ ] Create a worktree with a feature branch in ONE command
- [ ] Verify you're on the correct branch after worktree creation
- [ ] Verify commits are on the feature branch (not main)
- [ ] Diagnose "no commits on branch" issue
- [ ] Fix stale worktree errors
- [ ] Verify ALL worktrees before merging (coordinators only)
- [ ] Clean up worktrees after merging

---

## GitWorktreeManager Integration

The Python `GitWorktreeManager` class has been updated to enforce these best practices:

**New Features**:
```python
from core.utils.git_worktree_manager import GitWorktreeManager

manager = GitWorktreeManager()

# Creates worktree with automatic best practices
worktree_info = manager.create_worktree(
    task_name="file-attachments",
    branch="feat/file-attachments",  # Optional - auto-generates if None
    auto_prune=True,  # Prunes before creation (recommended)
    create_branch=True  # Creates branch if doesn't exist (recommended)
)

# Returns verification data
print(worktree_info['verification'])
# {
#   'current_branch': 'feat/file-attachments',
#   'expected_branch': 'feat/file-attachments',
#   'branch_correct': True,
#   'is_detached': False,
#   'commits_ahead_of_main': 0,
#   'status': 'VERIFIED'
# }

# Verify ALL worktrees before merging
verification = manager.verify_commits(base_branch='main')
if verification['all_verified']:
    print("✅ All worktrees ready to merge")
else:
    print(f"❌ {verification['failed']} worktrees failed verification")
    print(verification['failed_worktrees'])
```

**Best Practice Workflow**:
```python
# 1. Create worktree with auto-prune and branch creation
worktree = manager.create_worktree(
    task_name="my-feature",
    auto_prune=True,
    create_branch=True
)

# 2. Verify immediately
if worktree['verification']['branch_correct']:
    print(f"✅ On correct branch: {worktree['branch']}")
else:
    print(f"❌ Branch verification FAILED!")

# 3. Do work in worktree...

# 4. Before merging, verify ALL worktrees
verification = manager.verify_commits()
if not verification['all_verified']:
    print("⚠️ Some worktrees have issues:")
    for wt in verification['worktrees']:
        if wt['status'] != 'READY_TO_MERGE':
            print(f"  - {wt['task_name']}: {wt['status']}")
```

---

## Training Test Cases

Practice these scenarios to verify understanding:

### Test 1: Basic Worktree Creation
```bash
# Create worktree for new feature
git worktree prune
git worktree add -b feat/user-auth /tmp/worktrees/user-auth main
cd /tmp/worktrees/user-auth

# Verify (should show feat/user-auth)
git branch --show-current

# Make change and commit
echo "test" > test.txt
git add test.txt
git commit -m "test: verify worktree"

# Verify commit is on branch
git log main..HEAD --oneline
# Should show 1 commit
```

### Test 2: Parallel Worktrees
```bash
# Create 3 parallel worktrees
git worktree prune
git worktree add -b feat/feature-1 /tmp/worktrees/feature-1 main
git worktree add -b feat/feature-2 /tmp/worktrees/feature-2 main
git worktree add -b feat/feature-3 /tmp/worktrees/feature-3 main

# Verify all
git worktree list
# Should show 4 entries (main + 3 features)

# Verify each branch
for wt in /tmp/worktrees/feature-*; do
  echo "$(basename $wt): $(git -C $wt branch --show-current)"
done
```

### Test 3: Verification Before Merge
```bash
# Check if worktrees have commits
for wt in /tmp/worktrees/feature-*; do
  commits=$(git -C "$wt" log main..HEAD --oneline | wc -l)
  echo "$(basename $wt): $commits commits"
done

# All should show > 0 commits
```

---

## Emergency Recovery Procedures

### Recovery 1: Work Went to Main Instead of Feature Branch

**Symptoms**: Feature branch shows same commit as main

**Recovery**:
```bash
# Find commits that should be on feature branch
git log --oneline -10

# Create feature branch from current state
git checkout -b feat/recovered-feature

# Cherry-pick commits from main
git cherry-pick <commit-sha>

# Reset main to before commits
git checkout main
git reset --hard origin/main
```

### Recovery 2: Detached HEAD with Uncommitted Work

**Symptoms**: `git branch --show-current` shows nothing

**Recovery**:
```bash
# Create branch from detached HEAD state
git checkout -b feat/recovered-work

# Commit work
git add .
git commit -m "recover: work from detached HEAD"

# Continue normally
```

### Recovery 3: Stale Worktrees Blocking Creation

**Symptoms**: "already registered worktree" error

**Recovery**:
```bash
# Prune stale entries
git worktree prune

# Remove orphaned directories if needed
rm -rf /tmp/*-worktrees/*

# Prune again
git worktree prune

# Now create fresh worktrees
```

---

## Training Status by Hero

| Hero | Training Status | Verified By | Date |
|------|----------------|-------------|------|
| Superman | ✅ TRAINED | Self | 2025-12-08 |
| Oracle | 🔄 PENDING | - | - |
| Artemis | 🔄 PENDING | - | - |
| Hephaestus | 🔄 PENDING | - | - |
| Hawkman | 🔄 PENDING | - | - |
| Quicksilver | 🔄 PENDING | - | - |
| Batman | 🔄 PENDING | - | - |
| Flash | 🔄 PENDING | - | - |
| Green Arrow | 🔄 PENDING | - | - |
| Green Lantern | 🔄 PENDING | - | - |
| Wonder Woman | 🔄 PENDING | - | - |
| Aquaman | 🔄 PENDING | - | - |
| Cyborg | 🔄 PENDING | - | - |
| The Atom | 🔄 PENDING | - | - |
| Plastic Man | 🔄 PENDING | - | - |
| Zatanna | 🔄 PENDING | - | - |
| Litty | 🔄 PENDING | - | - |
| Martian Manhunter | 🔄 PENDING | - | - |
| Vision Analyst | 🔄 PENDING | - | - |
| The Architect | 🔄 PENDING | - | - |
| Product Manager | 🔄 PENDING | - | - |
| Aldrin | 🔄 PENDING | - | - |

---

## Next Steps

1. **All Heroes**: Review this training summary and complete verification checklist
2. **Task Agents**: Update workflows to include mandatory verification steps
3. **Coordinators**: Implement pre-merge verification checks
4. **Superman**: Update agent prompts/instructions with worktree best practices
5. **Oracle**: Add worktree verification to budget/cost tracking reports

---

## Resources

- **Full Best Practices Guide**: `/Users/admin/Documents/claudecode/justice-league-github/best-practices/git/GIT-WORKTREE-BEST-PRACTICES.md`
- **GitWorktreeManager Source**: `/Users/admin/Documents/claudecode/justice-league-github/core/utils/git_worktree_manager.py`
- **Training Summary**: `/Users/admin/Documents/claudecode/justice-league-github/best-practices/git/TEAM-TRAINING-SUMMARY.md` (this file)

---

**Training Version**: 1.0.0
**Created**: 2025-12-08
**Author**: Superman (Mission Coordinator)
**Mandatory Review**: ALL Justice League Heroes
**Status**: ACTIVE - Immediate Implementation Required
