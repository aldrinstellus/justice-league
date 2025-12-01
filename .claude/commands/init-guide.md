# Dynamic `/init` Command Protocol

Complete reference for Oracle's dynamic `/init` command that auto-detects current project and restores session context.

## Overview

**CRITICAL FIX**: `/init` command is now DYNAMIC and auto-detects current project based on working directory.

---

## How It Works

### 1. Auto-Detection
Oracle checks `pwd` to determine active project using pattern matching.

### 2. Pattern Matching Logic

| Path Pattern | Project Detected | Action |
|--------------|------------------|--------|
| `/v15-presentation$` | V15-Presentation | Load V15 savepoint |
| `/tweakcn-clone-IT3$` | atc.ds Design System | Load atc.ds savepoint |
| `/v14-production$` | V14 Production | Load V14 savepoint |
| `/justice-league-missions` | Justice League | Load JL savepoint |
| No match | Unknown | Ask user for selection |

### 3. Latest Savepoint Lookup

Oracle automatically finds the most recent savepoint for the detected project:

```bash
# V15-Presentation
ls -t /Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v15-presentation/PROJECT-SAVEPOINT*.md | head -1

# atc.ds Design System
ls -t /Users/admin/Documents/claudecode/workspaces/auzmor/apps/tweakcn-clone-IT3/*SAVEPOINT*.md | head -1

# V14-Production
ls -t /Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v14-production/PROJECT-SAVEPOINT*.md | head -1

# Justice League
ls -t /Users/admin/Documents/claudecode/justice-league-missions/PROJECT-SAVEPOINT*.md | head -1
```

### 4. Context Restoration

Oracle provides comprehensive context restoration:
- ✅ Project name and status
- ✅ Budget status (spent, remaining)
- ✅ Latest achievements/fixes
- ✅ Quick resume commands (cd, npm run dev)
- ✅ Dev server URL and port
- ✅ Next steps or pending tasks
- ✅ Recent file modifications
- ✅ Git status and branch
- ✅ Environment variables status (if applicable)
- ✅ Links to dashboards (Vercel, GitHub, etc.)

---

## Known Projects

### 1. V15-Presentation (Enterprise AI Support)

**Path**: `/Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v15-presentation`

**Details**:
- Framework: Next.js 15
- Port: 3016
- Latest Savepoint: `PROJECT-SAVEPOINT-2025-11-09-PERSONA-FIXES.md`
- Status: Active development

**Resume Commands**:
```bash
cd /Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v15-presentation
PORT=3016 npm run dev
```

**URL**: http://localhost:3016

---

### 2. atc.ds Design System (IT3)

**Path**: `/Users/admin/Documents/claudecode/workspaces/auzmor/apps/tweakcn-clone-IT3`

**Details**:
- Framework: Design system implementation
- Port: 3003
- Latest Savepoint: `SAVEPOINT-2025-11-06-FOUC-FIX.md`
- Status: Production-ready

**Resume Commands**:
```bash
cd /Users/admin/Documents/claudecode/workspaces/auzmor/apps/tweakcn-clone-IT3
PORT=3003 pnpm dev
```

**URL**: http://localhost:3003

---

### 3. V14-Production (Enterprise AI Support)

**Path**: `/Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v14-production`

**Details**:
- Framework: Next.js 14
- Status: Stable production baseline
- **IMPORTANT**: Never push to this project (stable baseline)

**Resume Commands**:
```bash
cd /Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v14-production
npm run dev
```

---

### 4. Justice League Missions

**Path**: `/Users/admin/Documents/claudecode/justice-league-missions`

**Details**:
- Type: Documentation and mission tracking system
- No dev server required
- Active missions tracked in `/missions/` folder

**Resume Commands**:
```bash
cd /Users/admin/Documents/claudecode/justice-league-missions
cat MISSIONS.md  # View all missions
```

---

## Why This Was Needed

### Problem
`/init` was hardcoded to atc.ds project, causing wrong context when user was in v15-presentation or other projects.

### Solution
Dynamic detection based on current working directory (`pwd` pattern matching).

### Result
`/init` now works correctly regardless of which project user is in.

### Lesson Learned
Always make slash commands context-aware in multi-project monorepos.

---

## Oracle's `/init` Workflow

### Step 1: Detect Project
```bash
pwd  # Get current working directory
# Example: /Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v15-presentation
```

### Step 2: Pattern Match
```bash
# Check if path contains known patterns
if [[ "$pwd" =~ "v15-presentation" ]]; then
  project="V15-Presentation"
elif [[ "$pwd" =~ "tweakcn-clone-IT3" ]]; then
  project="atc.ds Design System"
elif [[ "$pwd" =~ "v14-production" ]]; then
  project="V14-Production"
elif [[ "$pwd" =~ "justice-league-missions" ]]; then
  project="Justice League"
else
  project="Unknown"
fi
```

### Step 3: Find Latest Savepoint
```bash
# Use appropriate path for detected project
latest_savepoint=$(ls -t /path/to/project/PROJECT-SAVEPOINT*.md | head -1)
```

### Step 4: Read and Parse Savepoint
```bash
# Read savepoint content
cat "$latest_savepoint"

# Extract key information:
# - Git status and branch
# - Build status and error counts
# - Environment variables
# - Recent changes
# - Pending tasks
# - Quick commands
```

### Step 5: Present Context to User
```
🔮 **Oracle activated.** Restoring from savepoint...

✅ **Project**: V15-Presentation
✅ **Savepoint**: PROJECT-SAVEPOINT-2025-11-09-PERSONA-FIXES.md
✅ **Status**: Active development

**Environment**:
• Local: http://localhost:3016
• Git: feature/persona-fixes
• Build: ✅ Successful (0 errors)

**Quick Resume**:
cd /Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v15-presentation
PORT=3016 npm run dev

**Next Steps**:
• Continue persona switching implementation
• Test MCP integration
• Verify console errors = 0

Ready to continue!
```

---

## Savepoint Requirements

For `/init` to work properly, savepoints must contain:

### Required Sections
1. **Project Information**
   - Name
   - Framework/Stack
   - Dev server port
   - Status (active, stable, archived)

2. **Environment Status**
   - Local dev server URL
   - Git branch and status
   - Build status (success/failure, error count)
   - Environment variables (if applicable)

3. **Recent Changes**
   - Files modified
   - Commits made
   - Features added/fixed
   - Issues resolved

4. **Quick Resume Commands**
   - `cd` to project directory
   - Start dev server command
   - Any project-specific setup commands

5. **Next Steps**
   - Pending tasks
   - Priority items
   - Blockers (if any)
   - Recommendations

### Optional Sections
- Budget status (for Justice League missions)
- Deployment status (for Vercel projects)
- Performance metrics
- Test results
- Dashboard links

---

## User Experience Flow

### Scenario 1: Resume Work After Break
```
User: /init

Oracle: 🔮 Oracle activated. Restoring from savepoint...
        ✅ Project: V15-Presentation
        ✅ Savepoint: PROJECT-SAVEPOINT-2025-11-09-PERSONA-FIXES.md

        Environment: http://localhost:3016
        Git: feature/persona-fixes
        Build: ✅ 0 errors

        Quick Resume:
        cd /Users/admin/.../v15-presentation
        PORT=3016 npm run dev

        Next: Continue persona switching implementation

        Ready to continue!
```

### Scenario 2: Wrong Project Directory
```
User: /init
[User is in v14-production but wants to work on v15]

Oracle: 🔮 Oracle activated. Restoring from savepoint...
        ✅ Project: V14-Production (stable baseline)

        ⚠️ Note: You're in v14-production (stable baseline)

        Did you mean to resume work on:
        • V15-Presentation? (cd ../v15-presentation)
        • atc.ds? (cd ../../auzmor/apps/tweakcn-clone-IT3)

        Or continue with V14-Production?
```

### Scenario 3: Unknown Project
```
User: /init
[User is in unknown directory]

Oracle: 🔮 Oracle activated.

        Current directory not recognized as known project.

        Known projects:
        • V15-Presentation: cd /Users/.../v15-presentation
        • atc.ds: cd /Users/.../tweakcn-clone-IT3
        • V14-Production: cd /Users/.../v14-production
        • Justice League: cd /Users/.../justice-league-missions

        Which project would you like to resume?
```

---

## Best Practices

### For Users
1. Always run `/init` at the start of new Claude Code sessions
2. Ensure you're in the correct project directory before running `/init`
3. Create savepoints regularly with `/savepoint` command
4. Use descriptive milestone names in savepoint filenames

### For Oracle
1. Always check `pwd` before pattern matching
2. Always find the LATEST savepoint (most recent timestamp)
3. Always provide quick resume commands with full absolute paths
4. Always include next steps to help user continue work
5. If project unrecognized, list all known projects with paths

---

## Troubleshooting

### Issue: No Savepoint Found
**Symptom**: `/init` says "No savepoint found for this project"

**Solution**:
1. Check if savepoint exists: `ls -la PROJECT-SAVEPOINT*.md`
2. Create savepoint if missing: `/savepoint`
3. Verify savepoint naming follows convention

---

### Issue: Wrong Project Loaded
**Symptom**: `/init` loads wrong project context

**Solution**:
1. Verify current directory: `pwd`
2. Navigate to correct project directory
3. Run `/init` again

---

### Issue: Savepoint Content Incomplete
**Symptom**: `/init` loads savepoint but missing key information

**Solution**:
1. Review savepoint file manually
2. Update savepoint with missing sections
3. Run `/init` again

---

## Advanced Features

### Savepoint Comparison
Oracle can compare current state to savepoint:
- Files added/removed since savepoint
- Git commits since savepoint
- New dependencies installed
- Environment variable changes

### Multi-Project Context
Oracle can track multiple projects simultaneously and help user switch between them with proper context.

### Budget-Aware Resume
For Justice League missions, Oracle includes budget status in context restoration and can advise if sufficient budget remains for continued work.

---

**Last Updated**: 2025-11-24
**Purpose**: Complete reference for Oracle's dynamic `/init` command protocol
