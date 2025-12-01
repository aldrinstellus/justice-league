# CLAUDE.md Optimization: Best Practices

**Problem, Solution, and Guidelines for Keeping Global Instructions Lean**

---

## The Problem

### What Happened
Global `~/.claude/CLAUDE.md` grew to **41,300 characters**, exceeding the **40,000 character recommended limit**.

### Performance Impact
- ⚠️ Claude Code displayed warning: "Large /Users/admin/.claude/CLAUDE.md will impact performance (41.3k chars > 40.0k)"
- Slower conversation starts (more context to load upfront)
- Increased token usage on every conversation
- Reduced available context window for actual work

### Root Cause
Over time, essential behavior, detailed examples, troubleshooting guides, and historical learnings accumulated in a single file without organization strategy.

---

## The Solution

### Optimization Strategy: Reference Architecture

**Core Principle**: Keep only **essential behavior** in global CLAUDE.md, move **reference content** to separate files loaded on-demand.

### What We Did

#### 1. Analyzed Content (5 Categories)
- **Essential**: Must stay (core protocols, trigger keywords)
- **Reference**: Can move (detailed examples, workflows)
- **Redundant**: Can remove (duplicates other files)
- **Historical**: Archive (session learnings)
- **Troubleshooting**: Separate (specific guides)

#### 2. Created Reference File Structure
```
~/.claude/
├── CLAUDE.md (8.8k) ✅ Essential only
├── oracle-reference.md (10k) - Detailed examples
├── oracle-skills-reference.md (13k) - Troubleshooting
├── mcp-workflows.md (13k) - Automation workflows
├── commands/
│   └── init-guide.md (10k) - Protocol details
├── troubleshooting/
│   └── nextjs-cache-errors.md (10k) - Specific fixes
└── session-learnings/
    └── 2025-11-07.md (7.6k) - Historical context
```

#### 3. Condensed Global CLAUDE.md
- Kept: Trigger keywords, core behavior, quick references
- Replaced: Long examples with "See file.md"
- Removed: Redundant content duplicating other files

### Results
- **86% reduction**: 41,300 chars → 8,797 chars
- **78% under limit**: 31,203 char buffer remaining
- **No functionality lost**: All content preserved in references
- **Better organization**: Purpose-specific files

---

## Best Practices

### 1. Keep Global CLAUDE.md Under 30k Characters

**Target**: 20-30k chars (50-75% of limit)
**Buffer**: Leave room for growth

**What Belongs in Global CLAUDE.md**:
- ✅ Core behavior protocols (essential, short)
- ✅ Trigger keywords (must be immediate)
- ✅ Activation rules (core functionality)
- ✅ Quick command references (1-2 lines each)
- ✅ File location references (pointers to details)

**What Does NOT Belong**:
- ❌ Detailed examples (move to reference files)
- ❌ Long troubleshooting guides (create separate guides)
- ❌ Historical session learnings (archive separately)
- ❌ Complete workflows (link to workflow docs)
- ❌ Redundant content (remove duplicates)

---

### 2. Use Reference Architecture Pattern

**Pattern**: Essential → Reference → On-Demand

#### Global CLAUDE.md (Always Loaded)
```markdown
## Oracle Auto-Activation Protocol

**Trigger Keywords**: "oracle", "hey oracle", etc.

**Core Functions**:
- Budget health checks
- Cost estimation
- Optimization recommendations

**Detailed Reference**: See ~/.claude/oracle-reference.md
```

#### Reference File (Loaded When Needed)
```markdown
# Oracle Reference Guide

## Detailed Example Activations
[Full examples with code blocks, use cases, etc.]

## Cost Optimization Strategies
[Complete strategies, pricing tables, etc.]
```

---

### 3. Organize by Purpose

**File Organization**:
```
~/.claude/
├── CLAUDE.md (core behavior)
├── {feature}-reference.md (detailed docs)
├── commands/ (slash command details)
├── troubleshooting/ (specific issue guides)
└── session-learnings/ (historical archive)
```

**Naming Convention**:
- `{feature}-reference.md` - Detailed documentation
- `{topic}-guide.md` - How-to guides
- `{issue}-errors.md` - Troubleshooting guides
- `YYYY-MM-DD.md` - Session learnings (date-based)

---

### 4. Write Concise Summaries with Pointers

**Before** (bloats global file):
```markdown
## Oracle's New Skills

### Vercel Deployment Management
Oracle can configure and manage Vercel deployments:
- ✅ Add environment variables via Vercel CLI: `echo 'value' | vercel env add VAR_NAME production`
- ✅ List environment variables: `vercel env ls`
[...20 more lines of detailed commands and examples...]
```

**After** (lean with pointer):
```markdown
## Oracle's Skills

Oracle has troubleshooting skills for:
- Vercel deployment management
- TypeScript error debugging
- Next.js cache issues
- Justice League patterns

**Detailed Reference**: See ~/.claude/oracle-skills-reference.md
```

**Savings**: 500+ chars → 100 chars (80% reduction per section)

---

### 5. Archive Historical Content

**Problem**: Session learnings accumulate over time

**Solution**: Create dated archives
```
session-learnings/
├── 2025-11-07.md
├── 2025-11-15.md
└── 2025-12-01.md
```

**In Global CLAUDE.md**:
```markdown
**Historical Context**: See ~/.claude/session-learnings/ for past session learnings
```

---

### 6. Eliminate Redundancy

**Before**:
```markdown
## Oracle Token Limit Management
[500 lines of protocol details]

[Later in file...]
## Complete Protocol
See AUTO-SAVEPOINT-PROTOCOL.md
```

**After**:
```markdown
## Oracle Token Limit Management
**System**: Automated savepoint at 95% token usage (190K/200K)
**Complete Protocol**: See ~/.claude/AUTO-SAVEPOINT-PROTOCOL.md
```

**Rule**: If content exists in another file, reference it—don't duplicate it.

---

### 7. Regular Maintenance Checklist

**Monthly Review**:
- [ ] Check CLAUDE.md character count: `wc -c ~/.claude/CLAUDE.md`
- [ ] Target: Under 30,000 chars
- [ ] Identify sections that grew beyond 300 chars
- [ ] Extract detailed content to reference files
- [ ] Update pointers in CLAUDE.md
- [ ] Archive old session learnings

**Quarterly Cleanup**:
- [ ] Review all reference files for outdated content
- [ ] Consolidate similar troubleshooting guides
- [ ] Remove obsolete workflows
- [ ] Update best practices based on learnings

---

## Quick Decision Tree

```
Adding new content to CLAUDE.md?
↓
Is it a core behavior/trigger?
├─ YES → Add to CLAUDE.md (keep concise)
└─ NO → Is it detailed/reference?
    ├─ YES → Create reference file, add pointer
    └─ NO → Is it historical/troubleshooting?
        ├─ Historical → Archive in session-learnings/
        └─ Troubleshooting → Create guide in troubleshooting/
```

---

## Example Transformation

### Before (Bloated Section - 500 chars)
```markdown
### Lesson 1: Environment Variables Block Deployment
**Context**: 17 failed Vercel deployments all showed 0ms build time
**Root Cause**: Missing environment variables caused immediate failure
**Key Learning**:
- 0ms build time = environment variable issue, not code issue
- Always set BETTER_AUTH_SECRET, BETTER_AUTH_URL, DATABASE_URL
- Placeholder database URLs work for build

**Commands Used**:
```bash
echo 'value' | vercel env add VAR_NAME production
vercel env ls
vercel --prod
```
```

### After (Lean Reference - 50 chars)
```markdown
**Session Learnings**: See ~/.claude/session-learnings/2025-11-07.md
```

**Extracted Content**: Moved full lesson to `session-learnings/2025-11-07.md`

**Result**: 90% size reduction, no information lost

---

## Implementation Checklist

When your CLAUDE.md exceeds 30k chars:

### Phase 1: Analysis (15 min)
- [ ] Count characters: `wc -c ~/.claude/CLAUDE.md`
- [ ] Identify largest sections (>300 chars each)
- [ ] Categorize: Essential, Reference, Historical, Redundant
- [ ] Plan extraction: Which sections move where?

### Phase 2: Extraction (30 min)
- [ ] Create reference files for detailed content
- [ ] Create troubleshooting guides for specific issues
- [ ] Archive historical learnings by date
- [ ] Remove redundant content (duplicates other files)

### Phase 3: Condensation (20 min)
- [ ] Rewrite large sections as concise summaries
- [ ] Add clear pointers to reference files
- [ ] Keep only trigger keywords and core behavior
- [ ] Verify all file paths are correct

### Phase 4: Verification (10 min)
- [ ] Check final character count (target: <30k)
- [ ] Test that references are accessible
- [ ] Verify no functionality lost
- [ ] Document changes in OPTIMIZATION-COMPLETE.md

**Total Time**: ~75 minutes for comprehensive optimization

---

## Maintenance Commands

```bash
# Check current size
wc -c ~/.claude/CLAUDE.md

# Target: < 30,000 chars
# Warning threshold: > 35,000 chars
# Critical threshold: > 40,000 chars

# List all reference files with sizes
ls -lh ~/.claude/*.md ~/.claude/**/*.md

# Find largest sections in CLAUDE.md
grep -n "^## " ~/.claude/CLAUDE.md

# Archive old learnings
mv ~/.claude/temp-learnings.md ~/.claude/session-learnings/$(date +%Y-%m-%d).md
```

---

## Key Takeaways

### The Golden Rules
1. **Essential only in global file** - Everything else goes to references
2. **30k character target** - Leave buffer for growth
3. **Concise summaries with pointers** - Don't duplicate, reference
4. **Purpose-based organization** - Group related content
5. **Regular maintenance** - Review monthly, cleanup quarterly

### Remember
- ✅ Small global file = Fast performance
- ✅ Reference files = Organized knowledge
- ✅ On-demand loading = Efficient context usage
- ✅ Clear pointers = Easy navigation
- ✅ Regular cleanup = Sustainable system

---

## Before/After Comparison

| Aspect | Before | After |
|--------|--------|-------|
| **Size** | 41,300 chars | 8,797 chars |
| **Load Time** | Slow | Fast |
| **Organization** | Single file chaos | Structured references |
| **Maintenance** | Hard to update | Easy to update |
| **Scalability** | Bloats over time | Scales with references |
| **Performance** | ⚠️ Warning | ✅ Optimized |

---

**Document Version**: 1.0
**Date**: 2025-11-24
**Author**: Optimized from real-world Claude Code usage
**Status**: Production-tested ✅

---

**Share this document** with your team to maintain lean, performant global CLAUDE.md files across all projects.
