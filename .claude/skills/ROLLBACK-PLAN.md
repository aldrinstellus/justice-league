# Skills Installation Rollback Plan

## If Issues Arise

If the Skills system causes problems, follow this rollback procedure:

### Step 1: Remove Skill Files

```bash
# Remove frontend-design skill
rm -rf ~/.claude/skills/frontend-design

# Optional: Remove entire skills directory
rm -rf ~/.claude/skills
```

### Step 2: Revert Agent Changes

```bash
# Revert frontend-developer agent to original
git checkout ~/.claude/agents/frontend-developer.md

# Or manually edit the file to remove lines 10-14:
# **Integration with Skills:**
# - Leverages frontend-design skill...
# (4 lines total)
```

### Step 3: Revert CLAUDE.md Changes

```bash
# Revert global CLAUDE.md
git checkout ~/.claude/CLAUDE.md

# Or manually remove lines 219-264:
# (The entire "🎨 Skills System Integration" section)
```

### Step 4: Restart Claude Code

```bash
# Close and reopen Claude Code application
# (Required for changes to take effect)
```

## Success Criteria

✅ Skill auto-activates on "build UI" requests
✅ Agent provides responsive + accessible implementation
✅ No conflicts between skill and agent
✅ Justice League `/superman` coordinates both
✅ Documentation updated and clear
✅ Team can use without training

## Verification Tests

### Test 1: Skill Auto-Activation
```
Input: "Build a landing page for an AI security startup"
Expected: Bold aesthetic design (distinctive fonts, colors)
```

### Test 2: Agent + Skill Combination
```
Input: "Make it responsive and add WCAG 2.1 AA accessibility"
Expected: Responsive implementation with accessibility features
```

### Test 3: Justice League Coordination
```
Input: "/superman build a dashboard with backend API"
Expected: Aesthetic + responsive + API + MCP verification
```

### Test 4: No Conflicts
```
Input: "Fix this broken form validation"
Expected: Engineering fix without aesthetic changes
```

## Troubleshooting

### Skill Not Activating

**Symptoms**: Frontend responses still generic (Inter font, purple gradients)

**Fix**:
1. Verify skill file exists: `cat ~/.claude/skills/frontend-design/SKILL.md`
2. Check YAML frontmatter is valid
3. Restart Claude Code
4. Try explicit prompt: "Use frontend-design skill to build..."

### Skill Conflicts with Agent

**Symptoms**: Aesthetic changes break responsive design

**Fix**:
1. This shouldn't happen (complementary focus areas)
2. If it does, report as bug
3. Temporary workaround: Remove skill, use agent only

### Skill Too Opinionated

**Symptoms**: User wants generic design, skill forces bold aesthetics

**Fix**:
1. Add to prompt: "Use minimal aesthetic, keep it simple"
2. Or: "Ignore skill guidance for this request"
3. Skill respects explicit user direction

## File Locations

- **Skill**: `~/.claude/skills/frontend-design/SKILL.md`
- **Agent**: `~/.claude/agents/frontend-developer.md`
- **Global Config**: `~/.claude/CLAUDE.md`
- **README**: `~/.claude/skills/README.md`
- **This File**: `~/.claude/skills/ROLLBACK-PLAN.md`

## Backup Before Installation

Before installing skills, backup files:

```bash
# Backup agent
cp ~/.claude/agents/frontend-developer.md \
   ~/.claude/agents/frontend-developer.md.backup

# Backup CLAUDE.md
cp ~/.claude/CLAUDE.md \
   ~/.claude/CLAUDE.md.backup

# Verify backups
ls -lh ~/.claude/agents/*.backup
ls -lh ~/.claude/CLAUDE.md.backup
```

## Restore from Backup

```bash
# Restore agent
mv ~/.claude/agents/frontend-developer.md.backup \
   ~/.claude/agents/frontend-developer.md

# Restore CLAUDE.md
mv ~/.claude/CLAUDE.md.backup \
   ~/.claude/CLAUDE.md

# Remove skills
rm -rf ~/.claude/skills

# Restart Claude Code
```

## What NOT to Do

❌ Don't manually edit SKILL.md (fork to custom name instead)
❌ Don't delete agents directory (only remove frontend-developer backup)
❌ Don't forget to restart Claude Code after changes
❌ Don't remove MCP tools (unrelated to Skills)
❌ Don't remove Justice League system (complementary to Skills)

## Support

If rollback doesn't resolve issues:

1. Check Claude Code logs: `~/.claude/debug/`
2. Report issue with:
   - Skill name and version
   - Expected vs actual behavior
   - Steps to reproduce
   - Claude Code version

## Timeline

- **Rollback time**: ~5 minutes
- **Verification**: 10 minutes
- **Total recovery**: ~15 minutes

## Risk Assessment

**Installation Risk**: LOW
- Skills don't modify core Claude Code
- Easy to remove (just delete directory)
- Agents continue working without skills

**Rollback Risk**: MINIMAL
- Backup files protect against data loss
- Git can revert changes
- No system-level changes made
