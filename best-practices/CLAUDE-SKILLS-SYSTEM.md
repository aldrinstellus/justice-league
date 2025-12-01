# Claude Skills System: Complete Guide

**Understanding Skills vs Agents vs Commands - Best Practices for Domain Expertise**

---

## The Problem We Faced

### Initial Confusion
User asked: **"What skills are available? List all installed skills with their descriptions."**

**Issue**: Unclear what "skills" meant in Claude Code context:
- Are they agent definitions?
- Are they slash commands?
- Are they MCP tools?
- Something else entirely?

### Root Cause
Three similar-sounding features with overlapping purposes:
1. **Skills** (domain expertise documents)
2. **Agents** (specialized execution contexts via Task tool)
3. **Commands** (user-triggered workflows via slash commands)

**Result**: Confusion about when to use which feature and how they interact.

---

## The Solution

### What Are Skills?

**Definition**: Auto-activated domain expertise documents (markdown files) that Claude loads when relevant keywords are detected.

**Location**: `~/.claude/skills/skill-name/SKILL.md`

**Purpose**: Provide just-in-time context without permanent conversation overhead.

**Key Characteristic**: **Portable expertise** that can be shared across users and projects.

---

## Skills vs Agents vs Commands

### Clear Distinctions

| Feature | Activation | Purpose | Context | Example |
|---------|-----------|---------|---------|---------|
| **Skills** | Auto-detected by Claude | Portable domain expertise | Shares main conversation | `frontend-design` auto-loads on "build UI" |
| **Agents** | Explicit Task tool invocation | Specialized execution contexts | Independent context window | `frontend-developer` via Task tool |
| **Commands** | User types `/command` | User-triggered workflows | Main conversation | `/superman` coordination |

### When to Use What

#### Use Skills When:
- ✅ You need **repeatable expertise** across conversations
- ✅ You want **auto-activation** on keyword detection
- ✅ You need **portable knowledge** (share with team)
- ✅ You want **just-in-time context** (no permanent overhead)
- ✅ Example: Design principles, coding standards, best practices

#### Use Agents When:
- ✅ You need **complex multi-step workflows**
- ✅ You want **independent execution context**
- ✅ You need **specialized capabilities** (Task tool)
- ✅ You want **parallel execution** (multiple agents)
- ✅ Example: Backend development, frontend testing, security audits

#### Use Commands When:
- ✅ You need **user-triggered shortcuts**
- ✅ You want **quick access to workflows**
- ✅ You need **context restoration** (/init)
- ✅ You want **savepoint creation** (/savepoint)
- ✅ Example: Session management, coordination, status checks

---

## Installed Skills (Current State)

### Official Anthropic Skills

#### 1. frontend-design ✅

**Type**: Official Anthropic skill (user-installed)

**Purpose**: Creates distinctive, production-grade frontend interfaces with high design quality.

**Auto-Activation Keywords**:
- "build" + UI-related terms
- "create" + component/page/interface
- "design" + web/app/component

**Key Features**:
- Avoids "AI slop" (Inter/Roboto fonts, purple gradients, predictable layouts)
- Teaches distinctive typography, bold color schemes, high-impact animations
- Emphasizes spatial composition (asymmetry, overlap, diagonal flow)
- Provides aesthetic frameworks (brutally minimal, maximalist chaos, retro-futuristic)

**Installation Location**: `~/.claude/skills/frontend-design/SKILL.md`

**Documentation**: `~/.claude/skills/README.md`

---

## How Skills Work with Justice League

### Integration Pattern

**User Request**: `/superman build dashboard`

**Activation Flow**:
1. `frontend-design` skill **auto-activates** (keyword: "build dashboard")
2. Superman coordinates agents via Task tool
3. Task(`frontend-developer`) provides responsive implementation
4. Task(`backend-developer`) handles API integration
5. MCP Chrome DevTools for visual verification

**Result**: Bold aesthetics (skill) + production engineering (agents) + automated testing (MCP)

### Skills + Agents = Complementary Focus

| Layer | Provider | Focus | Benefit |
|-------|----------|-------|---------|
| **Aesthetic Direction** | Skills | Creative guidance | Distinctive design |
| **Engineering Robustness** | Agents | Implementation | Production quality |
| **Verification** | MCP Tools | Testing | Automated validation |

**Key Insight**: No conflicts - each layer enhances the others.

---

## Installing Skills

### Installation Methods

#### Method 1: Official Anthropic Skills
```bash
# Skills are installed via Claude Code interface
# Location: ~/.claude/skills/skill-name/SKILL.md
# Documentation: ~/.claude/skills/README.md
```

#### Method 2: Custom Skills (Future)
```bash
# Create custom skill directory
mkdir -p ~/.claude/skills/my-skill

# Create SKILL.md with expertise content
cat > ~/.claude/skills/my-skill/SKILL.md << 'EOF'
# My Custom Skill

[Domain expertise content here]
EOF
```

### Verification
```bash
# List installed skills
ls -la ~/.claude/skills/

# Check skill content
cat ~/.claude/skills/frontend-design/SKILL.md
```

---

## Best Practices for Skills

### 1. When to Create a Custom Skill

**Good Candidates**:
- ✅ Company coding standards (reusable across projects)
- ✅ Domain-specific expertise (medical, legal, finance)
- ✅ Design system guidelines (consistent UI/UX)
- ✅ Security best practices (OWASP, compliance)
- ✅ Architecture patterns (microservices, event-driven)

**Bad Candidates**:
- ❌ Project-specific code (use project CLAUDE.md)
- ❌ Temporary workarounds (document in codebase)
- ❌ Historical context (use session-learnings/)
- ❌ Troubleshooting guides (use troubleshooting/)

### 2. Skill Structure Guidelines

**Effective Skill Format**:
```markdown
# Skill Name

## Purpose
[What this skill provides]

## Auto-Activation Keywords
[Keywords that trigger this skill]

## Core Principles
[Key concepts and guidelines]

## Examples
[Practical examples and patterns]

## Anti-Patterns
[What to avoid]
```

**Size Recommendation**: 5-15k characters (detailed but focused)

### 3. Skill vs Global CLAUDE.md

| Content Type | Location | Reason |
|--------------|----------|--------|
| Auto-activation keywords | CLAUDE.md | Must be immediately available |
| Detailed expertise | Skill file | Loaded on-demand |
| Trigger conditions | CLAUDE.md | Core behavior |
| Examples and patterns | Skill file | Reference content |

**Rule**: CLAUDE.md declares skills exist, skill files contain expertise.

---

## Skills System Architecture

### How Auto-Activation Works

#### Step 1: Keyword Detection
```
User: "Let's build a dashboard interface"
         ↓
Claude detects: "build" + "dashboard" + "interface"
         ↓
Matches: frontend-design skill keywords
```

#### Step 2: Skill Loading
```
Claude loads: ~/.claude/skills/frontend-design/SKILL.md
         ↓
Expertise available in conversation context
         ↓
Responses informed by skill content
```

#### Step 3: Integration
```
Skill provides: Aesthetic guidance
Agents provide: Implementation
MCP provides: Verification
         ↓
Complete solution
```

### Context Management

**Before Skills** (permanent overhead):
```
Global CLAUDE.md = 64k chars
Every conversation loads all 64k
Context window: Reduced
```

**With Skills** (on-demand loading):
```
Global CLAUDE.md = 8.8k chars
Skills loaded only when needed
Context window: Maximized
```

---

## Skills vs Other Systems

### Skills vs Knowledge Base

| Feature | Skills | Knowledge Base |
|---------|--------|----------------|
| **Activation** | Auto (keywords) | Manual (search) |
| **Purpose** | Expertise | Information |
| **Integration** | Automatic | User-requested |
| **Portability** | High (share files) | Low (platform-specific) |
| **Maintenance** | Simple (edit markdown) | Complex (database) |

### Skills vs Fine-Tuning

| Feature | Skills | Fine-Tuning |
|---------|--------|-------------|
| **Update Speed** | Instant (edit file) | Slow (retrain model) |
| **Cost** | Free | Expensive |
| **Portability** | Perfect (markdown) | Locked (model-specific) |
| **Version Control** | Git-friendly | Difficult |
| **Iteration** | Fast | Slow |

**Recommendation**: Use skills for domain expertise, not fine-tuning.

---

## Common Issues and Solutions

### Issue 1: Skill Not Auto-Activating

**Symptoms**: Skill exists but doesn't load on expected keywords

**Diagnosis**:
```bash
# Check skill exists
ls ~/.claude/skills/skill-name/SKILL.md

# Verify SKILL.md format
cat ~/.claude/skills/skill-name/SKILL.md | head -20
```

**Solutions**:
- ✅ Verify skill filename is exactly `SKILL.md` (case-sensitive)
- ✅ Check keywords are documented in skill file
- ✅ Try more explicit keywords in user request
- ✅ Restart Claude Code to refresh skills registry

---

### Issue 2: Skill Conflicts with Global CLAUDE.md

**Symptoms**: Contradictory guidance between skill and global instructions

**Root Cause**: Overlapping content in both locations

**Solution**:
```markdown
# In Global CLAUDE.md
## Frontend Development
**Design Expertise**: Auto-activates via frontend-design skill
**Implementation**: Use Task(frontend-developer) agent

# In Skill (frontend-design/SKILL.md)
[Detailed design principles and examples]
```

**Rule**: Global declares, skill delivers.

---

### Issue 3: Too Many Skills Loaded

**Symptoms**: Context window shrinking, slower responses

**Diagnosis**:
```bash
# Count skills
ls ~/.claude/skills/ | wc -l

# Check sizes
du -sh ~/.claude/skills/*/
```

**Solutions**:
- ✅ Keep skills focused (5-15k chars each)
- ✅ Remove unused skills
- ✅ Merge overlapping skills
- ✅ Use more specific activation keywords

**Recommendation**: Maximum 5-10 skills per system.

---

## Skills Roadmap (Future Enhancements)

### Potential Features

#### 1. Skill Composition
```markdown
# In composite-skill/SKILL.md
Imports: frontend-design, backend-patterns, security-best-practices

[Combined expertise from multiple skills]
```

#### 2. Conditional Activation
```markdown
# In skill/SKILL.md
Activation:
  keywords: ["build", "create"]
  file_types: [".tsx", ".jsx"]
  project_type: "react"
```

#### 3. Skill Metrics
```bash
# Track skill effectiveness
claude skills stats

Skill: frontend-design
Activations: 47 times
Average quality: 9.2/10
Last updated: 2025-11-20
```

#### 4. Skill Marketplace
```bash
# Browse community skills
claude skills search "api design"

# Install from marketplace
claude skills install @anthropic/api-patterns
```

---

## Quick Reference

### Skill Management Commands

```bash
# List installed skills
ls ~/.claude/skills/

# Create new skill
mkdir -p ~/.claude/skills/my-skill
touch ~/.claude/skills/my-skill/SKILL.md

# Edit skill
code ~/.claude/skills/my-skill/SKILL.md

# Remove skill
rm -rf ~/.claude/skills/my-skill

# Check skill documentation
cat ~/.claude/skills/README.md
```

### Verification Checklist

When creating/installing a skill:
- [ ] Skill file is named exactly `SKILL.md`
- [ ] Located in `~/.claude/skills/skill-name/`
- [ ] Contains clear purpose statement
- [ ] Lists activation keywords
- [ ] Size is reasonable (5-15k chars)
- [ ] No overlap with global CLAUDE.md
- [ ] No conflicts with other skills
- [ ] Tested with sample keywords

---

## Decision Tree

```
Need to add expertise to Claude Code?
↓
Is it domain expertise (reusable)?
├─ YES → Is it project-specific?
│   ├─ YES → Add to project CLAUDE.md
│   └─ NO → Is it user-specific?
│       ├─ YES → Add to global CLAUDE.md
│       └─ NO → Create SKILL
└─ NO → Is it a workflow?
    ├─ Multi-step complex → Create AGENT
    └─ User-triggered → Create COMMAND
```

---

## Example: Creating a Custom Skill

### Scenario
Company has specific API design standards that should apply across all projects.

### Implementation

#### Step 1: Create Skill Structure
```bash
mkdir -p ~/.claude/skills/company-api-patterns
```

#### Step 2: Write SKILL.md
```markdown
# Company API Design Patterns

## Purpose
Enforce company-wide API design standards for consistency and quality.

## Auto-Activation Keywords
- "api design"
- "create endpoint"
- "rest api"
- "graphql schema"

## Core Principles

### RESTful Conventions
- Use plural nouns for resources (/users, /orders)
- Use HTTP verbs correctly (GET, POST, PUT, DELETE)
- Return appropriate status codes (200, 201, 400, 404, 500)

### Response Format
All API responses must follow:
```json
{
  "success": boolean,
  "data": object | array,
  "error": null | { "code": string, "message": string }
}
```

### Authentication
- All endpoints require Bearer token
- Token in Authorization header
- JWT format with 1-hour expiration

### Rate Limiting
- 100 requests per minute per API key
- Return 429 status when exceeded
- Include X-RateLimit headers

## Examples

[Detailed examples of good/bad API designs]

## Anti-Patterns

- ❌ Using verbs in URLs (/getUser, /createOrder)
- ❌ Returning different response structures
- ❌ Exposing internal error details
- ❌ Missing pagination on list endpoints
```

#### Step 3: Test Activation
```
User: "I need to create an endpoint for user management"
         ↓
Skill auto-activates
         ↓
Claude applies company API standards
```

---

## Key Takeaways

### The Golden Rules

1. **Skills = Portable Expertise** - Share knowledge via markdown files
2. **Auto-Activation = Efficiency** - No manual loading required
3. **On-Demand = Performance** - Context loaded only when needed
4. **Complementary, Not Conflicting** - Skills + Agents + Commands work together
5. **Focused Scope** - Keep skills to 5-15k chars, single domain

### Remember

- ✅ Skills for repeatable expertise (design, standards, patterns)
- ✅ Agents for complex workflows (implementation, testing)
- ✅ Commands for user shortcuts (savepoint, init)
- ✅ MCP for automation (browser testing, verification)
- ✅ Global CLAUDE.md for core behavior only

---

## Resources

### Official Documentation
- **Skills README**: `~/.claude/skills/README.md`
- **Installed Skills**: `ls ~/.claude/skills/`
- **Claude Code Docs**: [claude.com/code](https://claude.com/code)

### Example Skills
- **frontend-design**: Official Anthropic skill for UI/UX
- **[Add more as they become available]**

### Community
- **GitHub Discussions**: Share custom skills
- **Best Practices**: This document
- **Issue Tracking**: Report skill-related issues

---

**Document Version**: 1.0
**Date**: 2025-11-24
**Author**: Based on real-world Claude Code skills system usage
**Status**: Production-tested ✅

---

**Share this document** with your team to understand and effectively use the Claude Code skills system.
