# Claude Code Skills

Skills provide auto-activated domain expertise across all conversations.

## Installed Skills

### frontend-design (Official Anthropic)
- **Purpose**: Create distinctive, production-grade frontend interfaces
- **Auto-activates**: When building web components, pages, or applications
- **Provides**: Bold aesthetic direction, typography guidance, color philosophy, animation patterns
- **Avoids**: Generic AI patterns (Inter fonts, purple gradients, predictable layouts)
- **Source**: https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design

## How Skills Work

1. **Auto-Activation**: Skills load automatically when Claude detects relevant requests (no manual invocation)
2. **Progressive Disclosure**: Claude uses metadata first, loads full instructions only when needed
3. **Agent Enhancement**: Agents invoked via Task tool automatically benefit from relevant skills
4. **Team Benefit**: All team members benefit from skills without learning new commands

## Installation

To add new skills:

```bash
# 1. Create directory
mkdir -p ~/.claude/skills/skill-name

# 2. Add SKILL.md file with YAML frontmatter
# (See official Anthropic skills repo for examples)

# 3. Restart Claude Code
```

## Skills vs Agents vs Commands

- **Skills**: Auto-activated expertise (frontend-design, web-artifacts-builder)
- **Agents**: Task-delegated specialists (frontend-developer, backend-developer)
- **Commands**: User-triggered workflows (/superman, /init, /savepoint)
- **MCP**: Browser automation tools (Chrome DevTools)

All four systems work together seamlessly.

## Integration with Justice League

When using `/superman` for frontend missions:

1. **Skills auto-activate** - `frontend-design` provides aesthetic guidance
2. **Agents execute** - `frontend-developer` implements responsive, accessible code
3. **MCP verifies** - Chrome DevTools takes screenshots and checks console
4. **Result** - Bold aesthetics + production engineering + automated testing

Example:
```
User: "/superman build a dashboard"

What happens:
├── frontend-design skill auto-activates (aesthetics)
├── Task(frontend-developer) for implementation
├── Task(backend-developer) for API integration
└── MCP Chrome DevTools for verification
```

## Skill Structure

Each skill directory contains:
```
skill-name/
└── SKILL.md               # YAML frontmatter + instructions
```

**SKILL.md Format**:
```markdown
---
name: skill-name
description: What it does and when Claude should use it
license: Optional
allowed-tools: Optional
---

# Skill Instructions
Detailed guidance, procedures, and domain knowledge...
```

## Troubleshooting

**Skill not activating?**
- Restart Claude Code after installation
- Check SKILL.md has correct YAML frontmatter
- Verify skill directory in `~/.claude/skills/`

**Conflicts with agents?**
- Skills and agents are complementary, not competing
- Skills provide expertise, agents provide execution contexts
- Both can be active simultaneously

**How to check if skill is loaded?**
- Skills load automatically when relevant (no explicit indicator)
- Look for responses that follow skill guidelines
- Example: Frontend responses avoiding Inter font = skill active

## Additional Resources

- **Official Skills**: https://github.com/anthropics/skills
- **Community Skills**: https://github.com/ComposioHQ/awesome-claude-skills
- **Skills Blog Post**: https://www.claude.com/blog/improving-frontend-design-through-skills
- **Documentation**: https://code.claude.com/docs/en/skills

## Installed Skills Details

### frontend-design

**When it activates**:
- User mentions: "build", "create", "design", "implement" + UI/component/page/app
- Example triggers: "build a dashboard", "create a landing page", "design a form"

**What it provides**:
- Bold aesthetic direction before coding
- Typography: Distinctive fonts (avoid Inter/Roboto/Arial)
- Color: Dominant colors with sharp accents, CSS variables
- Motion: High-impact animations, scroll-triggered effects
- Spatial: Asymmetry, overlap, diagonal flow
- Background: Gradient meshes, noise textures, layered transparencies

**What it avoids**:
- Generic AI aesthetics
- Purple gradients on white
- Inter/Roboto/Arial fonts
- Predictable layouts
- Cookie-cutter designs

**Integration with frontend-developer agent**:
- Skill provides aesthetic guidance
- Agent provides responsive design, accessibility, testing
- Combined result: Bold + production-ready
