# Next Session: Skills Installation Instructions

**Date Created**: 2025-11-24
**Status**: Ready to Execute
**Estimated Time**: 10-15 minutes

---

## ⚡ Quick Start (Copy & Paste in Claude Code UI)

**IMPORTANT**: These commands must be run in **Claude Code chat interface**, NOT in terminal.

### Step 1: Install Superpowers (CRITICAL - Do This First)

In Claude Code chat, type:
```
/plugin marketplace add obra/superpowers-marketplace
```

Wait for confirmation, then type:
```
/plugin install superpowers@superpowers-marketplace
```

**What you'll get**: 20+ skills including:
- `dispatching-parallel-agents` - Coordinate multiple agents
- `systematic-debugging` - 4-phase debugging
- `test-driven-development` - TDD workflow
- `writing-plans` / `executing-plans` - Task management
- `/brainstorm`, `/write-plan`, `/execute-plan` - New slash commands

---

### Step 2: Install Document Skills (Optional but Recommended)

In Claude Code chat, type:
```
/plugin marketplace add anthropics/skills
```

Wait for confirmation, then type:
```
/plugin install document-skills@anthropic-agent-skills
```

**What you'll get**: 4 document skills:
- `docx` - Create/edit Word documents
- `pdf` - PDF extraction and manipulation
- `pptx` - Create PowerPoint presentations
- `xlsx` - Excel spreadsheet operations

---

### Step 3: Restart Claude Code (REQUIRED)

**Close and reopen Claude Code application completely.**

Skills only load after restart!

---

### Step 4: Verify Installation

In Claude Code chat, ask:
```
What skills are available? List all installed skills with their descriptions.
```

**Expected response**: Should list:
- frontend-design (already installed)
- 20+ Superpowers skills
- 4 Document skills (if installed in Step 2)

---

### Step 5: Test Skill Activation

Try these test queries:

**Test 1: Superpowers Brainstorming**
```
/brainstorm how to coordinate frontend and backend agents for a complex mission
```
Expected: Superpowers guides systematic thinking

**Test 2: TDD Workflow**
```
Build a new API endpoint using test-driven development
```
Expected: `test-driven-development` skill activates, guides RED-GREEN-REFACTOR

**Test 3: Document Generation**
```
Create a PowerPoint presentation outline for Wisconsin DNR RFP
```
Expected: `pptx` skill activates (if installed in Step 2)

**Test 4: Systematic Debugging**
```
Debug this error using systematic approach: [describe error]
```
Expected: `systematic-debugging` skill activates with 4-phase analysis

**Test 5: Frontend Design (Already Installed)**
```
Build a landing page for AI security startup
```
Expected: `frontend-design` skill activates with bold aesthetics

---

## 📋 Verification Checklist

After installation and restart, verify:

- [ ] Claude Code restarted successfully
- [ ] `/brainstorm` slash command works
- [ ] `/write-plan` slash command works
- [ ] `/execute-plan` slash command works
- [ ] Skills list shows 24+ skills (frontend-design + Superpowers + Documents)
- [ ] TDD skill activates when building new features
- [ ] Document skills activate when creating docs (if installed)
- [ ] No error messages or conflicts

---

## 🔧 Troubleshooting

### Problem: "Plugin not found"
**Solution**: Check marketplace name spelling
```
/plugin marketplace add obra/superpowers-marketplace
```
(Note: "marketplace" not "marketplace-plugin")

### Problem: Skills don't activate after installation
**Solution**: Restart Claude Code completely
- Close all windows
- Quit application
- Reopen and test again

### Problem: Slash commands don't work
**Solution**:
1. Verify Superpowers installed: Check skills list
2. Restart Claude Code again
3. Type `/` and see if commands appear in autocomplete

### Problem: "Already installed" message
**Solution**: Skills already installed, just restart Claude Code

### Problem: Skills conflict or overlap
**Solution**: This shouldn't happen, but if it does:
- Skills auto-select based on relevance
- Multiple skills can activate simultaneously
- Check `ROLLBACK-PLAN.md` if issues persist

---

## 📊 What Happens After Installation

### Context Window Impact
- **Before**: 40K tokens (CLAUDE.md only)
- **After**: ~42K tokens (+2,400 for Superpowers metadata)
- **Impact**: +1.2% context usage
- **Remaining**: 158K tokens (79%)

### New Capabilities

#### Oracle (Coordination)
- **Before**: Manual agent coordination
- **After**: `dispatching-parallel-agents` provides systematic coordination
- **Benefit**: Fewer coordination errors

#### Backend Developer
- **Before**: Generic backend guidance
- **After**: `test-driven-development` + `systematic-debugging`
- **Benefit**: Higher code quality, systematic bug fixes

#### Frontend Developer
- **Before**: `frontend-design` only
- **After**: + Superpowers TDD workflow
- **Benefit**: Aesthetic + quality + testing

#### Justice League Missions
- **Before**: Hero banter + parallel Task calls
- **After**: + Superpowers coordination + verification gates
- **Benefit**: More reliable execution, better error recovery

---

## 📝 Next Steps After Installation

### Immediate (Same Session)
1. Test all verification queries above
2. Try `/brainstorm` for a real problem
3. Test Justice League with Superpowers:
   ```
   /superman fix TypeScript errors using systematic debugging
   ```

### This Week
1. Use for 1 week with normal workflow
2. Monitor which skills activate frequently
3. Note any skill activation patterns
4. Measure time savings (compare to previous missions)

### After 1 Week
1. Review usage patterns
2. Decide: Add ClaudeKit (30+ more skills)?
   ```bash
   git clone https://github.com/mrgoonie/claudekit-skills ~/.claude/skills/claudekit
   ```
3. Consider specialized skills:
   - Playwright (browser testing)
   - FFUF (security scanning)
   - D3.js (visualizations)

---

## 🎯 Success Metrics

Track these after installation:

### Efficiency Metrics
- [ ] Time to complete missions (before vs after)
- [ ] Number of debugging cycles (fewer = better)
- [ ] Parallel agent coordination success rate
- [ ] Task planning clarity

### Quality Metrics
- [ ] Bug recurrence rate (lower = better)
- [ ] Test coverage percentage (higher = better)
- [ ] Code review feedback volume (less = better)

### Cost Metrics (Oracle Tracks)
- [ ] Token usage per mission
- [ ] Monthly budget utilization
- [ ] Cost per completed task

**Target**: 20-30% improvement in efficiency + cost within 1 month

---

## 🔮 Oracle Integration

After installation, Oracle will automatically use Superpowers skills:

**Example Oracle Workflow**:
```
User: "Oracle, deploy Justice League to fix authentication"

Oracle activates:
1. systematic-debugging - Analyze auth issue
2. writing-plans - Break into tasks:
   - Backend: Fix API auth middleware
   - Frontend: Update login form
   - Security: Audit auth flow
3. dispatching-parallel-agents - Deploy agents simultaneously
4. verification-before-completion - Validate all fixes
5. MCP Chrome DevTools - Visual verification

Result: Faster, more systematic mission execution
```

---

## 📚 Resources for Next Session

### Documentation
- Research: `~/.claude/skills/AVAILABLE-SKILLS-RESEARCH.md`
- This File: `~/.claude/skills/NEXT-SESSION-INSTALLATION.md`
- Usage Guide: `~/.claude/skills/README.md`
- Rollback: `~/.claude/skills/ROLLBACK-PLAN.md`

### External Links
- Superpowers: https://github.com/obra/superpowers
- Tutorial: https://betazeta.dev/blog/claude-code-superpowers/
- Official Skills: https://github.com/anthropics/skills
- Marketplace: https://skillsmp.com/

### Quick Commands
```bash
# List installed skills
ls -la ~/.claude/skills/

# View skill content
cat ~/.claude/skills/frontend-design/SKILL.md

# Remove skill if needed
rm -rf ~/.claude/skills/[skill-name]
```

---

## ⏱️ Installation Timeline

### Step 1: Install Superpowers (3-5 min)
- Add marketplace: 1 min
- Install plugin: 1 min
- Wait for completion: 1-3 min

### Step 2: Install Documents (2-3 min)
- Add marketplace: 30 sec
- Install plugin: 30 sec
- Wait for completion: 1-2 min

### Step 3: Restart (1 min)
- Close Claude Code
- Reopen application

### Step 4: Verify (2-3 min)
- List skills: 30 sec
- Test queries: 1-2 min

### Step 5: Test (3-5 min)
- Try slash commands: 1 min
- Test skill activation: 2-4 min

**Total Time**: 11-17 minutes

---

## 💡 Pro Tips

1. **Run verification tests immediately** - Don't wait to discover issues later
2. **Try slash commands first** - `/brainstorm`, `/write-plan`, `/execute-plan`
3. **Use systematic-debugging** - Better than ad-hoc debugging
4. **Leverage TDD workflow** - Saves debugging time later
5. **Document patterns** - Note which skills activate when

---

## 🚨 Important Reminders

- ✅ Skills load **on-demand** (not all at once)
- ✅ Multiple skills can activate simultaneously
- ✅ Skills enhance agents (don't replace them)
- ✅ Restart required after installation
- ✅ Context overhead minimal (~2.5%)
- ✅ Reversible (see ROLLBACK-PLAN.md)

---

## Ready to Install?

1. Open this file in next session
2. Copy commands from "Quick Start" section
3. Paste in Claude Code chat (NOT terminal)
4. Follow Step 1 → Step 2 → Step 3 → Step 4 → Step 5
5. Enjoy enhanced Justice League coordination! 🦸‍♂️

---

**Created**: 2025-11-24 11:45 AM
**Status**: Ready to Execute
**Next Action**: Run Step 1 in Claude Code UI
