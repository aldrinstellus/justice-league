# /savepoint - Manual Savepoint Creation

🔮 **Oracle Manual Savepoint**

You requested a manual savepoint. Oracle will capture current state for session continuity.

## Step 1: Gather Current Context

**Collect the following information**:

### Token Usage
- Current tokens: {CHECK_TOKEN_COUNTER}
- Max tokens: 200,000
- Percentage: {CALCULATE_PERCENTAGE}%

### Budget Status
```bash
python3 /Users/admin/Documents/claudecode/justice-league-missions/scripts/check-budget.py
```

### Active Missions
```bash
cat /Users/admin/Documents/claudecode/justice-league-missions/MISSIONS.md
```

### Current Working Directory
```bash
pwd
```

### Recent Git Status (if in repo)
```bash
git status 2>/dev/null || echo "Not in git repo"
```

## Step 2: Prompt User for Details

Ask the user:

```
🔮 **Creating Manual Savepoint**

**Optional**: What's the reason for this savepoint?
Examples:
- "End of work session"
- "Before major refactor"
- "Phase 1 complete"
- "Backup before experiment"
- Or just press Enter to skip

Reason: _____
```

## Step 3: Generate Savepoint File

Use the auto-savepoint template:
- **Template**: `/Users/admin/Documents/claudecode/justice-league-missions/_templates/auto-savepoint-template.md`
- **Output Location**: `/Users/admin/Documents/claudecode/justice-league-missions/`
- **Filename Format**:
  - If 95% tokens: `PROJECT-SAVEPOINT-{YYYY-MM-DD}-TOKEN-LIMIT.md`
  - If manual: `PROJECT-SAVEPOINT-{YYYY-MM-DD}-{HH-MM}.md`
  - If reason given: `PROJECT-SAVEPOINT-{YYYY-MM-DD}-{REASON-SLUG}.md`

**Fill in all placeholders**:
- `{DATE}` - Current date (YYYY-MM-DD)
- `{TIME}` - Current time (HH:MM AM/PM)
- `{REASON}` - User-provided reason or "Manual Savepoint"
- `{VERSION}` - System version (e.g., 2.3.0)
- `{CURRENT_TOKENS}` - Actual token count
- `{MAX_TOKENS}` - 200000
- `{PERCENTAGE}` - Calculated percentage
- `{MISSION_*}` - Extract from MISSIONS.md
- `{BUDGET_*}` - Extract from check-budget.py output
- `{TASK_*}` - Ask user for pending tasks or extract from conversation
- All other placeholders from template

## Step 4: Capture Critical Context

### Mission States

For each active mission, capture:
- Mission ID (e.g., JL-003)
- Mission name
- Current phase
- Progress percentage (estimate if needed)
- Budget allocated vs spent
- Current task description

### Pending Tasks

Ask user:
```
**Pending Tasks** (optional):

High priority:
1. _____
2. _____

Medium priority:
1. _____

Low priority:
1. _____

Press Enter when done.
```

### Recent File Modifications

Check recently modified files:
```bash
cd /Users/admin/Documents/claudecode/justice-league-missions
find . -name "*.md" -o -name "*.py" -o -name "*.json" | xargs ls -lt | head -10
```

### Key Decisions This Session

Ask user:
```
**Key Decisions** made this session (optional):

1. _____
2. _____

Press Enter when done.
```

## Step 5: Create Savepoint File

Write the populated template to file:
```bash
cat > /Users/admin/Documents/claudecode/justice-league-missions/PROJECT-SAVEPOINT-{FILENAME}.md << 'EOF'
{POPULATED_TEMPLATE_CONTENT}
EOF
```

## Step 6: Confirm Creation

Display confirmation:
```
✅ **Savepoint Created Successfully**

📁 **File**: PROJECT-SAVEPOINT-{FILENAME}.md
📍 **Location**: /Users/admin/Documents/claudecode/justice-league-missions/

**Contents Captured**:
- ✅ Token usage: {TOKENS} ({PERCENTAGE}%)
- ✅ Budget status: ${REMAINING} remaining
- ✅ Active missions: {COUNT} mission(s)
- ✅ Pending tasks: {COUNT} task(s)
- ✅ File modifications: {COUNT} file(s)
- ✅ Quick resume commands

**To Resume Later**:
1. Start new Claude Code session
2. Type: `/init`
3. Oracle will restore this exact state

**View Savepoint**:
```bash
cat /Users/admin/Documents/claudecode/justice-league-missions/PROJECT-SAVEPOINT-{FILENAME}.md
```

**Savepoint ready!** ✅
```

---

## Oracle Standing Instructions for Manual Savepoints

When `/savepoint` is invoked:

1. **Ask user about urgency**:
   - "Is this urgent (approaching token limit or compaction warning)? (y/n)"
   - If yes: Prioritize speed, gather essential context only
   - If no: Take time for comprehensive context gathering

2. **Gather context** systematically:
   - Token usage
   - Budget status
   - Mission states
   - Pending tasks
   - Recent modifications

3. **Ask user for optional details**:
   - Reason for savepoint
   - Pending tasks
   - Key decisions
   - Known blockers

4. **Use template** consistently:
   - Load from _templates/auto-savepoint-template.md
   - Fill ALL placeholders
   - No {PLACEHOLDER} should remain in output

5. **Save to standard location**:
   - Always in justice-league-missions/ root
   - Use standard naming convention
   - Confirm absolute path in output

6. **Provide clear confirmation**:
   - Show filename
   - Show full path
   - List what was captured
   - Give resume instructions

7. **Make it actionable**:
   - Include command to view savepoint
   - Include `/init` reminder
   - Show quick commands

**IMPORTANT**: Manual savepoints are instant backups. Make them as complete and useful as possible for future resume.

---

## Examples

### Example 1: End of Work Session

```
User: /savepoint
Oracle: 🔮 Creating manual savepoint...

What's the reason? End of work session
Oracle: [gathers context]
Oracle: ✅ Savepoint: PROJECT-SAVEPOINT-2025-11-05-END-OF-WORK.md
       • Budget: $87.66 remaining
       • Mission: JL-003 at 50%
       • Tasks: 5 pending
       Resume with: /init
```

### Example 2: Before Risky Operation

```
User: /savepoint
Oracle: 🔮 Creating manual savepoint...

What's the reason? Before refactoring database schema
Oracle: [gathers context]
Oracle: ✅ Savepoint: PROJECT-SAVEPOINT-2025-11-05-BEFORE-REFACTOR.md
       Backup created before risky operation.
       If things go wrong, run /init to restore.
```

### Example 3: Phase Completion

```
User: /savepoint
Oracle: 🔮 Creating manual savepoint...

What's the reason? JL-003 Phase 2 complete
Oracle: [gathers context]
Oracle: ✅ Savepoint: PROJECT-SAVEPOINT-2025-11-05-PHASE2-COMPLETE.md
       • Phase 2: ✅ Complete
       • Budget used: $35.00
       • Next: Phase 3 planning
       Resume with: /init
```

---

**Command Type**: Manual savepoint creation
**Trigger**: User types `/savepoint`
**Output**: Savepoint file in justice-league-missions/
**Resume**: Use `/init` in new session
