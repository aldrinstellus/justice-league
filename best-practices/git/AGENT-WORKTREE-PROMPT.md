# Git Worktree Best Practices - Agent Prompt Template

**Purpose**: Copy-paste instructions for Justice League agent prompts
**Target**: All Task and Coordinator agents using git worktrees
**Last Updated**: 2025-12-08

---

## For Task Agents (Copy to Agent Prompts)

```markdown
## MANDATORY: Git Worktree Protocol

When working with git worktrees, you MUST follow this exact workflow:

### Pre-Flight Check
```bash
# ALWAYS prune before creating worktrees
git worktree prune
```

### Creating Your Worktree
```bash
# Create worktree WITH branch in ONE command
git worktree add -b feat/{feature-name} /tmp/{project}-worktrees/{feature-name} main

# Navigate to worktree
cd /tmp/{project}-worktrees/{feature-name}
```

### CRITICAL: Verify Branch Immediately
```bash
# Check you're on the correct branch (NOT main!)
git branch --show-current
# MUST show: feat/{feature-name}

# If blank or wrong, STOP and report error
```

### Working in Worktree
```bash
# Make your changes
# ... code generation, modifications, etc. ...

# Stage and commit
git add .
git commit -m "feat: description of what you did"
```

### CRITICAL: Verify Commits Before Reporting
```bash
# Verify commit is on branch
git log --oneline -1

# Verify commits ahead of main (MUST be > 0)
git log main..HEAD --oneline
```

### Required Report Format
When reporting completion, you MUST include:

```
✅ Worktree created: /tmp/{project}-worktrees/{feature-name}
✅ Branch verified: feat/{feature-name}
✅ Commits ahead of main: {number}
✅ Latest commit: {sha} {message}
✅ Status: READY FOR REVIEW
```

### DO NOT
- ❌ Create worktree without `-b` flag
- ❌ Skip `git worktree prune`
- ❌ Skip branch verification
- ❌ Report success if commits ahead = 0
- ❌ Work on detached HEAD
- ❌ Commit to main branch
```

---

## For Coordinator Agents (Copy to Agent Prompts)

```markdown
## MANDATORY: Parallel Worktree Verification Protocol

After deploying parallel task agents, you MUST verify all worktrees before merging:

### Post-Deployment Verification
```bash
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

### Merging Criteria
ONLY proceed with merging if ALL worktrees show:
- ✅ Branch is feature branch (NOT main, NOT blank)
- ✅ Commits ahead of main > 0
- ✅ Uncommitted changes = 0

### Merge Workflow
```bash
# Return to main worktree
cd {main-repo-path}

# Merge each feature branch
git checkout main
git merge feat/{feature-1} --no-ff -m "Merge feat/{feature-1}: {description}"
git merge feat/{feature-2} --no-ff -m "Merge feat/{feature-2}: {description}"
# etc.

# Clean up worktrees
git worktree remove /tmp/{project}-worktrees/{feature-1}
git worktree remove /tmp/{project}-worktrees/{feature-2}

# Clean up branches (optional)
git branch -d feat/{feature-1}
git branch -d feat/{feature-2}

# Final prune
git worktree prune
```

### Required Coordinator Report
Your post-merge report MUST include:

```
✅ Verified {N} worktrees before merge
✅ All worktrees had commits ahead of main
✅ Merged {N} feature branches
✅ Cleaned up {N} worktrees
✅ Final verification: {status}
```
```

---

## For Python Agents (GitWorktreeManager Integration)

```python
# RECOMMENDED: Use GitWorktreeManager for automatic best practices

from core.utils.git_worktree_manager import GitWorktreeManager

# Initialize manager
manager = GitWorktreeManager()

# Create worktree with automatic best practices enforcement
worktree_info = manager.create_worktree(
    task_name="my-feature",
    branch="feat/my-feature",  # Optional - auto-generates if None
    auto_prune=True,  # Automatically prunes before creation
    create_branch=True  # Creates branch if doesn't exist
)

# Verify branch immediately
verification = worktree_info['verification']
if not verification['branch_correct']:
    raise Exception(f"Branch verification FAILED: {verification}")

print(f"✅ Worktree created on branch: {worktree_info['branch']}")
print(f"✅ Path: {worktree_info['path']}")

# ... do work in worktree ...

# Before reporting success, verify commits exist
verification = manager.verify_commits(base_branch='main')
if not verification['all_verified']:
    raise Exception(f"Worktree verification FAILED: {verification['failed_worktrees']}")

print(f"✅ All {verification['total_worktrees']} worktrees verified")
print(f"✅ Ready to merge: {verification['ready_to_merge']} worktrees")
```

---

## Common Agent Errors and Fixes

### Error 1: "No commits on feature branch"

**Agent sees**:
```bash
git log main..HEAD --oneline
# Shows nothing
```

**What happened**: Agent worked on main or detached HEAD instead of feature branch

**Agent should**:
```bash
# Check current branch
git branch --show-current
# If blank or "main", STOP and report error immediately

# Do NOT continue working
# Do NOT report success
```

**Report**:
```
❌ CRITICAL ERROR: Branch verification failed
   Current branch: {blank or main}
   Expected branch: feat/{feature-name}

   Work may have been committed to wrong branch.
   Awaiting coordinator intervention.
```

### Error 2: "Worktree already registered"

**Agent sees**:
```
fatal: '/tmp/worktrees/feature' is a missing but already registered worktree
```

**What happened**: Forgot to run `git worktree prune`

**Agent should**:
```bash
# Run prune
git worktree prune

# Retry worktree creation
git worktree add -b feat/{feature-name} /tmp/worktrees/{feature-name} main
```

### Error 3: "Detached HEAD"

**Agent sees**:
```bash
git branch --show-current
# Shows nothing (blank)
```

**What happened**: Worktree created without branch

**Agent should**:
```bash
# Create branch from current state
git checkout -b feat/{feature-name}

# Verify now on branch
git branch --show-current
# Should show feat/{feature-name}
```

---

## Training Verification for Agents

Each agent implementing worktree workflows should verify:

- [ ] Agent prompt includes pre-flight `git worktree prune`
- [ ] Agent creates worktree WITH `-b` flag
- [ ] Agent verifies branch immediately after creation
- [ ] Agent verifies commits before reporting success
- [ ] Agent reports failure if verification fails
- [ ] Agent includes verification output in reports
- [ ] Coordinator verifies ALL worktrees before merging

---

## Quick Reference: Mandatory Commands

**Every Task Agent MUST run**:
```bash
# 1. Before creating
git worktree prune

# 2. Create with branch
git worktree add -b feat/{name} /tmp/worktrees/{name} main

# 3. Verify immediately
git branch --show-current  # Must show feat/{name}

# 4. Before reporting
git log main..HEAD --oneline  # Must show commits
```

**Every Coordinator MUST run**:
```bash
# After all agents complete
for wt in /tmp/*-worktrees/*/; do
  commits=$(git -C "$wt" log main..HEAD --oneline | wc -l)
  if [ "$commits" -eq 0 ]; then
    echo "❌ ERROR: No commits on $(basename $wt)"
  fi
done

# Only merge if ALL worktrees have commits > 0
```

---

## Resources

- **Full Best Practices**: `/Users/admin/Documents/claudecode/justice-league-github/best-practices/git/GIT-WORKTREE-BEST-PRACTICES.md`
- **Team Training**: `/Users/admin/Documents/claudecode/justice-league-github/best-practices/git/TEAM-TRAINING-SUMMARY.md`
- **GitWorktreeManager**: `/Users/admin/Documents/claudecode/justice-league-github/core/utils/git_worktree_manager.py`

---

**Version**: 1.0.0
**Created**: 2025-12-08
**For**: All Justice League Agents
**Status**: MANDATORY - Include in all agent prompts
