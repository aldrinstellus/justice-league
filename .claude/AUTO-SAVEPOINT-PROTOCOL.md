# 🔮 AUTO-SAVEPOINT PROTOCOL
## Automated Token Monitoring & Session Recovery

**Created**: 2025-11-09
**Updated**: 2025-11-09 (Bulletproof v2)
**Status**: ACTIVE
**Purpose**: Automatically trigger savepoints at 95% token usage to prevent context loss

---

## 🎯 CRITICAL REQUIREMENT

**Problem**: Claude Code has 200K token limit. At 190K tokens (95%), context may be lost due to compaction.

**Solution**: Automatically create comprehensive savepoint at **EXACTLY 95% (190K tokens)** with context-aware project detection and routing.

---

## 📊 TOKEN THRESHOLDS

**UPDATED 2025-11-09**: Simplified to single 95% threshold per user request.

| Token Count | Percentage | Status | Action |
|-------------|------------|--------|--------|
| 0-180K | 0-90% | ✅ SAFE | Normal operation |
| 180K-190K | 90-95% | 🟡 CAUTION | Monitor (NO auto-savepoint yet) |
| **190K** | **95%** | ⚠️ **TRIGGER** | **AUTO-SAVEPOINT NOW** ← ONLY TRIGGER POINT |
| 190K-200K | 95-100% | 🔴 CRITICAL | User must start new session with `/init` |

**Key Change**: NO longer triggers at 90%. ONLY triggers at EXACTLY 95% (190K tokens).

---

## 🤖 ORACLE AUTO-SAVEPOINT DETECTION

### **How Oracle Detects Token Usage**

**Limitation**: Oracle (Claude) CANNOT directly access real-time token counter.

**Available Signal**: System warnings that appear AFTER tool execution:
```
<system_warning>Token usage: 190000/200000; 10000 remaining</system_warning>
```

**Detection Method**: Oracle must parse these warnings from tool outputs.

### **Auto-Savepoint Trigger Logic**

```typescript
// Pseudo-code for Oracle's detection logic
// UPDATED 2025-11-09: Single 95% threshold only

function checkTokenUsage(systemWarning: string): SavepointAction {
  const match = systemWarning.match(/Token usage: (\d+)\/200000/);
  if (!match) return 'NO_ACTION';

  const tokensUsed = parseInt(match[1]);
  const percentage = (tokensUsed / 200000) * 100;

  // ONLY trigger at 95% or above
  if (percentage >= 95) {
    return 'AUTO_SAVEPOINT'; // 190K+ tokens
  }

  return 'NO_ACTION';
}
```

---

## 🗺️ PROJECT DETECTION & ROUTING

### **PWD-Based Project Detection**

**Strategy**: Use current working directory to detect project context automatically.

**Detection Logic**:
```bash
#!/bin/bash
# Oracle runs this logic internally

CWD=$(pwd)

# Pattern matching (check most specific first)
if [[ "$CWD" =~ /v15-presentation$ ]]; then
    PROJECT_TYPE="v15-presentation"
    SAVEPOINT_DIR="/Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v15-presentation"
    GIT_PUSH="YES"

elif [[ "$CWD" =~ /tweakcn-clone-IT3$ ]]; then
    PROJECT_TYPE="atc-ds"
    SAVEPOINT_DIR="/Users/admin/Documents/claudecode/workspaces/auzmor/apps/tweakcn-clone-IT3"
    GIT_PUSH="YES"

elif [[ "$CWD" =~ /justice-league-missions ]]; then
    PROJECT_TYPE="justice-league"
    SAVEPOINT_DIR="/Users/admin/Documents/claudecode/justice-league-missions"
    GIT_PUSH="YES"

elif [[ "$CWD" =~ /v14-production$ ]]; then
    PROJECT_TYPE="v14-production"
    SAVEPOINT_DIR="/Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v14-production"
    GIT_PUSH="NO"  # Stable baseline - don't touch

else
    PROJECT_TYPE="unknown"
    SAVEPOINT_DIR="/Users/admin/Documents/claudecode/justice-league-missions"  # Global fallback
    GIT_PUSH="NO"  # Safety - don't push unknown projects
fi
```

### **Routing Table**

Single source of truth for ALL auto-savepoint decisions:

| Project Type | Detection Pattern | Savepoint Location | Git Push | Vercel Deploy |
|-------------|-------------------|-------------------|----------|---------------|
| **v15-presentation** | `/v15-presentation$` | `/Users/.../v15-presentation/` | ✅ YES | ❌ MANUAL ONLY |
| **atc.ds (IT3)** | `/tweakcn-clone-IT3$` | `/Users/.../tweakcn-clone-IT3/` | ✅ YES | ❌ MANUAL ONLY |
| **justice-league** | `/justice-league-missions` | `/Users/.../justice-league-missions/` | ✅ YES | ❌ NO (docs only) |
| **v14-production** | `/v14-production$` | `/Users/.../v14-production/` | ❌ NO | ❌ NO (stable baseline) |
| **unknown** | Other | `/Users/.../justice-league-missions/` | ❌ NO | ❌ NO (safety fallback) |

**Critical Rules**:
- **v14-production**: NEVER push (stable production baseline, don't touch)
- **Justice League**: Push docs but NO Vercel (not a web app)
- **v15 & atc.ds**: Push to Git, but Vercel deployment is MANUAL ONLY (user triggers explicitly)
- **Unknown projects**: Save to global fallback, NO Git operations (safety)

**Vercel Deployment Policy** (UPDATED 2025-11-09):
- **NEVER automatic** - User must explicitly request "deploy to vercel"
- Auto-savepoint ONLY does: savepoint creation + Git push (if appropriate)
- Vercel is project-dependent and requires manual trigger

---

## 🔄 AUTO-SAVEPOINT WORKFLOW

### **Complete End-to-End Flow**

```
1. Oracle Detects System Warning
   ↓
   "Token usage: 190000/200000; 10000 remaining"

2. Calculate Percentage
   ↓
   190000 / 200000 = 95% ✅ TRIGGER

3. Detect Project (pwd)
   ↓
   /Users/.../v15-presentation → Project: "v15-presentation"

4. Lookup Routing Table
   ↓
   v15-presentation → Git: YES, Vercel: MANUAL ONLY

5. Gather Context
   ↓
   - Budget: check-budget.py
   - Git status: git status
   - Recent files: find . -mtime -1
   - Session progress: memory

6. Create Savepoint File
   ↓
   Location: /Users/.../v15-presentation/PROJECT-SAVEPOINT-2025-11-09-AUTO-190K.md
   Content: Budget, progress, files, recovery instructions
   Retry: 3x with exponential backoff (2s, 4s, 8s)
   Fallback: /tmp/ if all retries fail

7. Git Operations (if GIT_PUSH=YES)
   ↓
   git add PROJECT-SAVEPOINT-*.md
   git commit -m "📁 Auto-savepoint: 95% token limit"
   git push origin main
   (failures logged but don't block)

8. Oracle Confirms
   ↓
   "✅ Savepoint created + pushed to GitHub"
   "⚠️ Start new session with /init"

9. NO Vercel Deployment
   ↓
   Vercel deployment skipped (user will trigger manually if needed)
```

---

## 📋 AUTO-SAVEPOINT TEMPLATE

When Oracle triggers auto-savepoint at 95%, it creates:

```markdown
# 🔮 AUTO-SAVEPOINT - [DATE]
## Session Recovery Point (Auto-Generated at 95% tokens)

**Created**: [DateTime]
**Trigger**: Token usage reached 190K/200K (95%)
**Project**: [v15-presentation | atc-ds | justice-league | etc.]
**Location**: [Current directory]
**Status**: 🤖 AUTO-GENERATED

---

## 💰 BUDGET STATUS
[Current budget state from check-budget.py]

---

## 🎯 ACTIVE WORK
[What was being worked on this session]

---

## 📊 SESSION PROGRESS
[What was completed this session]

---

## 📁 FILES MODIFIED
[List of files changed - from git status]

---

## 🚀 QUICK RESUME
```bash
# To restore context:
/init

# Oracle will load this savepoint automatically
```

---

## 🎯 NEXT STEPS
[What needs to be done next]

---

**Recovery Instructions**:
1. Start new Claude Code window
2. Type: `/init`
3. Oracle restores full context from this savepoint
4. Continue work seamlessly
```

---

## 🔄 `/INIT` RECOVERY FLOW

### **User Action**: Type `/init` in new Claude Code session

### **Oracle Response**:
```
🔮 **Oracle activated.** Initializing session recovery...

[Oracle checks current directory]
[Oracle detects project type]
[Oracle finds latest savepoint]
[Oracle reads savepoint content]

✅ **Context Restored**: PROJECT-SAVEPOINT-2025-11-09-AUTO-190K.md

**Session Summary**:
- Project: v15-presentation
- Budget: $X remaining
- Session Progress: [Summary]
- Files Modified: [N] files
- Next Steps: [List]

**Quick Commands**:
- Dev server: npm run dev
- Build: npm run build
- GitHub: git status

Ready to continue! What would you like to work on?
```

---

## ⚠️ ERROR HANDLING

### **Fail-Safe Architecture**

**Critical Operations** (MUST succeed):
- Savepoint file creation
  - Retry 3x with exponential backoff (2s, 4s, 8s)
  - Fallback to `/tmp/` if all retries fail
  - NEVER let this fail completely

**Non-Critical Operations** (logged but don't block):
- Git add/commit/push
  - Log failures with recovery instructions
  - Savepoint still exists locally
- Budget script execution
  - Continue without budget if script fails
- File modification tracking
  - Continue without file list if find fails

### **Error Scenarios & Recovery**

#### **Scenario 1: Savepoint Write Fails (Disk Full)**
```
❌ Attempt 1: FAILED (No space left on device)
⏱️  Waiting 2 seconds...
❌ Attempt 2: FAILED (No space left on device)
⏱️  Waiting 4 seconds...
❌ Attempt 3: FAILED (No space left on device)

⚠️ **Fallback Activated**: Saving to /tmp/

✅ Emergency Savepoint: /tmp/PROJECT-SAVEPOINT-2025-11-09-AUTO-190K.md

**Recovery**:
1. Free up disk space
2. Copy to correct location:
   cp /tmp/PROJECT-SAVEPOINT-2025-11-09-AUTO-190K.md /Users/.../v15-presentation/
3. Resume with /init
```

#### **Scenario 2: Git Push Fails (Network Down)**
```
✅ Savepoint Created: PROJECT-SAVEPOINT-2025-11-09-AUTO-190K.md
✅ Git Add: Staged
✅ Git Commit: Committed locally
❌ Git Push: FAILED (network unreachable)

⚠️ **Git Push Failed**: Network unreachable

**What Succeeded**:
- Savepoint created locally ✅
- Committed to Git ✅

**What Failed**:
- Push to GitHub ❌

**Recovery**:
When network is restored:
  cd /Users/.../v15-presentation
  git push origin main

**Impact**:
- Resume with /init works (savepoint exists locally)
- GitHub will sync when you push later
```

---

## 📊 SAVEPOINT NAMING CONVENTION

**Pattern**: `PROJECT-SAVEPOINT-{DATE}-AUTO-{TOKENS}K.md`

**Examples**:
```
PROJECT-SAVEPOINT-2025-11-09-AUTO-190K.md  (auto-generated at 190K)
PROJECT-SAVEPOINT-2025-11-09-MANUAL.md     (user-triggered via /savepoint)
```

**Location Routing**:
- v15-presentation → `/Users/.../v15-presentation/PROJECT-SAVEPOINT-*.md`
- atc.ds → `/Users/.../tweakcn-clone-IT3/PROJECT-SAVEPOINT-*.md`
- justice-league → `/Users/.../justice-league-missions/PROJECT-SAVEPOINT-*.md`
- v14-production → `/Users/.../v14-production/PROJECT-SAVEPOINT-*.md`
- unknown → `/Users/.../justice-league-missions/PROJECT-SAVEPOINT-*.md` (global fallback)

---

## ✅ SUCCESS CRITERIA

**Auto-Savepoint System is Bulletproof When**:

1. ✅ Triggers EXACTLY at 95% (190K tokens) - NOT at 90%
2. ✅ Automatically detects project type from pwd
3. ✅ Routes savepoint to correct project directory
4. ✅ NEVER saves to wrong project (zero contamination)
5. ✅ Pushes to Git for appropriate projects only
6. ✅ NEVER auto-deploys to Vercel (manual only)
7. ✅ Savepoint creation always succeeds (retry + fallback)
8. ✅ Git failures don't block savepoint
9. ✅ Clear error messages with recovery instructions
10. ✅ /init recovery works for all projects (<30 seconds)

---

## 🔗 RELATED DOCUMENTATION

- **Oracle Protocol**: `/Users/admin/.claude/CLAUDE.md` (Oracle Auto-Activation section)
- **Project Detection Script**: `/Users/admin/.claude/scripts/detect_project.sh`
- **Budget Tracking**: `/Users/admin/Documents/claudecode/justice-league-missions/simple-budget.json`

---

**Protocol Status**: ✅ ACTIVE (Bulletproof v2)
**Last Updated**: 2025-11-09
**Maintained By**: Oracle (Auto-Savepoint System)

---
