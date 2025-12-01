# Dynamic Project Initialization

**Oracle**: Detect current project and load latest savepoint automatically.

---

## 🔍 Project Detection Logic

**Current Working Directory**: Check `pwd` to determine which project we're in.

**Project Patterns**:
- `/v18-unified-modes` → Load latest V18 savepoint ⭐ ACTIVE
- `/JL-009-v17-takeover/v17-project` → Load latest V17 Justice League savepoint
- `/v16-presentation` → Load latest v16-presentation savepoint (ARCHIVED)
- `/v15-presentation` → Load latest v15-presentation savepoint
- `/tweakcn-clone-IT3` → Load latest atc.ds savepoint
- `/v14-production` → Load latest v14 savepoint
- Other locations → Provide project selection menu

---

## 📍 Known Project Locations

1. **V18 Unified Modes** (Enterprise AI Support) ⭐ ACTIVE
   - Path: `/Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v18-unified-modes`
   - Port: 3019
   - GitHub: https://github.com/aldrinstellus/enterprise-ai-support-v18
   - Vercel: https://v18-unified-modes.vercel.app
   - Latest Savepoint: `PROJECT-SAVEPOINT-2025-11-21-PERSONAS-COMPLETE.md`
   - Status: All personas verified, 3 modes (ATC/Government/Project)

2. **V17 Justice League** (Enterprise AI Support)
   - Path: `/Users/admin/Documents/claudecode/justice-league-missions/missions/JL-009-v17-takeover/v17-project`
   - Mission: `JL-009-v17-takeover`
   - Port: 3018
   - Status: Justice League Managed (based on V16 with all features)

3. **V16-Presentation** (Enterprise AI Support) 📦 ARCHIVED
   - Path: `/Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v16-presentation`
   - Archive: `/Users/admin/Documents/claudecode/justice-league-missions/missions/JL-009-v17-takeover/v16-archive`
   - Port: 3017
   - Status: ARCHIVED (replaced by V17)

4. **V15-Presentation** (Enterprise AI Support)
   - Path: `/Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v15-presentation`
   - Latest Savepoint: `PROJECT-SAVEPOINT-2025-11-09-PERSONA-FIXES.md`
   - Port: 3016
   - Status: 100% Production Ready

5. **atc.ds Design System** (IT3)
   - Path: `/Users/admin/Documents/claudecode/workspaces/auzmor/apps/tweakcn-clone-IT3`
   - Latest Savepoint: `SAVEPOINT-2025-11-06-FOUC-FIX.md`
   - Port: 3003
   - Status: Stable (FOUC fixed)

6. **V14-Production** (Enterprise AI Support)
   - Path: `/Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v14-production`
   - Status: Production baseline

---

## 🚀 Auto-Detection Instructions

Oracle should:

1. **Check current directory**:
   ```bash
   pwd
   ```

2. **Match against known projects**:
   - If path contains `v18-unified-modes` → Load V18 context ⭐
   - If path contains `v17-project` → Load V17 Justice League context
   - If path contains `v16-presentation` → Load V16 archive context
   - If path contains `v15-presentation` → Load V15 context
   - If path contains `tweakcn-clone-IT3` → Load atc.ds context
   - If path contains `v14-production` → Load V14 context
   - If no match → Ask user which project to initialize

3. **Find latest savepoint**:
   ```bash
   # V18 Unified Modes ⭐ ACTIVE
   ls -t /Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v18-unified-modes/PROJECT-SAVEPOINT*.md | head -1

   # V17 Justice League
   ls -t /Users/admin/Documents/claudecode/justice-league-missions/missions/JL-009-v17-takeover/PROJECT-SAVEPOINT*.md | head -1

   # V16-Presentation (ARCHIVED)
   cat /Users/admin/Documents/claudecode/justice-league-missions/missions/JL-009-v17-takeover/v16-archive/ARCHIVE-2025-11-11.txt

   # V15-Presentation
   ls -t /Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v15-presentation/PROJECT-SAVEPOINT*.md | head -1

   # atc.ds
   ls -t /Users/admin/Documents/claudecode/workspaces/auzmor/apps/tweakcn-clone-IT3/*SAVEPOINT*.md | head -1
   ```

4. **Read and summarize savepoint**:
   - Budget status
   - Latest achievements
   - Quick resume commands
   - Next steps

5. **Provide context**:
   - Project location
   - Dev server port
   - Key files
   - Recent commits

---

## 📋 Fallback: Manual Project Selection

If Oracle can't detect project automatically, ask user:

**Which project do you want to initialize?**
1. V17 Justice League (Enterprise AI Support) ⭐ ACTIVE
2. V16-Presentation (Enterprise AI Support) 📦 ARCHIVED
3. V15-Presentation (Enterprise AI Support)
4. atc.ds Design System (IT3)
5. V14-Production
6. Other (specify path)

Then load appropriate savepoint.

---

## ✅ Success Criteria

After `/init` completes, Oracle should provide:
- ✅ Project name and status
- ✅ Budget status (spent, remaining)
- ✅ Latest achievements/fixes
- ✅ Quick resume commands (cd, npm run dev)
- ✅ Dev server URL and port
- ✅ Next steps or pending tasks

---

**Oracle Note**: Always check for the LATEST savepoint (newest timestamp) and provide full context restoration in <30 seconds.
