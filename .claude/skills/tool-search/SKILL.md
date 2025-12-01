---
name: tool-search
description: Dynamic tool discovery for on-demand tool loading. Use this skill when you need to find the right MCP tool, check tool parameters, or discover available tools for a specific task. Reduces context overhead by loading tool documentation only when needed.
---

# Tool Search Skill

This skill enables dynamic discovery of MCP tools and their parameters, reducing context overhead by 85% through on-demand loading rather than including all tool definitions in the system prompt.

## When to Use This Skill

Use this skill when:
- You need to find the right tool for a specific task
- You're unsure about tool parameters or syntax
- You want to discover available tools for a category
- You need to check agent-specific tool mappings
- You want orchestration pattern recommendations

## Tool Registry

**Location**: `/Users/admin/.claude/tools/tool-registry.json`

The registry contains:
- **40+ tools** across 10 categories
- Tool parameters and examples
- Agent-to-tool mappings
- Defer loading recommendations
- Orchestration patterns

## Categories

| Category | Tools | Primary Agents |
|----------|-------|----------------|
| visual-verification | screenshot, snapshot | frontend, qa-tester |
| browser-navigation | navigate_page, new_page, close_page | ALL |
| form-interaction | click, fill, fill_form, press_key | e2e-tester, qa-tester |
| console-debugging | list_console_messages, get_console_message | ALL |
| network-analysis | list_network_requests, get_network_request | backend, security |
| performance-analysis | performance_start_trace, analyze_insight | frontend, devops |
| page-manipulation | resize_page, emulate, hover, drag | frontend, qa-tester |
| script-evaluation | evaluate_script | security, backend |
| dialog-handling | handle_dialog, wait_for | e2e-tester |
| file-operations | upload_file | qa-tester |

## Quick Tool Lookup

### By Task Type

**"I need to test a form"**
```
Tools: fill_form, click, wait_for
Pattern: verifyAPI(formData, submitBtn, expectedText, endpoint)
```

**"I need to verify UI after a fix"**
```
Tools: navigate_page, take_screenshot, list_console_messages
Pattern: verifyUI(url, screenshotPath)
```

**"I need to test authentication"**
```
Tools: fill_form, click, evaluate_script, list_network_requests
Pattern: verifyAuthFlow(loginUrl, credentials, submitBtn, expectedRedirect)
```

**"I need to test responsive design"**
```
Tools: resize_page, take_screenshot (x3)
Pattern: verifyResponsive(url, breakpoints)
```

**"I need to check performance"**
```
Tools: performance_start_trace, performance_analyze_insight
Pattern: auditPerformance(url)
```

**"I need to debug an error"**
```
Tools: list_console_messages, list_network_requests, take_screenshot
```

## Agent Tool Mappings

### frontend-developer
**Always Loaded**: navigate_page, take_screenshot, list_console_messages, resize_page
**Defer Loaded**: take_snapshot, performance_start_trace, performance_analyze_insight, list_network_requests

### backend-developer
**Always Loaded**: navigate_page, list_console_messages, list_network_requests
**Defer Loaded**: take_screenshot, get_network_request, fill_form, click, evaluate_script

### e2e-tester
**Always Loaded**: navigate_page, click, fill, fill_form, wait_for
**Defer Loaded**: take_screenshot, list_console_messages, press_key, hover, take_snapshot

### qa-tester
**Always Loaded**: navigate_page, take_screenshot, click, fill_form, wait_for
**Defer Loaded**: take_snapshot, list_console_messages, list_network_requests, resize_page, press_key, hover

### security-specialist
**Always Loaded**: navigate_page, fill_form, click, list_network_requests, evaluate_script
**Defer Loaded**: take_screenshot, take_snapshot, list_console_messages, get_network_request, press_key

### devops-engineer
**Always Loaded**: navigate_page, take_screenshot, list_console_messages, list_network_requests
**Defer Loaded**: performance_start_trace, performance_analyze_insight, new_page, get_network_request

## Parameter Examples

### Screenshot
```typescript
// Basic (save to file - RECOMMENDED)
mcp__chrome-devtools__take_screenshot({ filePath: "verification.png" })

// Element-specific
mcp__chrome-devtools__take_screenshot({ uid: "nav-header", filePath: "header.png" })

// Full page
mcp__chrome-devtools__take_screenshot({ fullPage: true, filePath: "full-page.png" })
```

### Form Filling
```typescript
// Single field
mcp__chrome-devtools__fill({ uid: "email", value: "test@example.com" })

// Multiple fields (PREFERRED)
mcp__chrome-devtools__fill_form({
  elements: [
    { uid: "email", value: "test@example.com" },
    { uid: "password", value: "SecurePass123!" }
  ]
})
```

### Console Messages
```typescript
// Errors only
mcp__chrome-devtools__list_console_messages({ types: ["error"] })

// Errors and warnings
mcp__chrome-devtools__list_console_messages({ types: ["error", "warn"] })
```

### Network Requests
```typescript
// API calls only
mcp__chrome-devtools__list_network_requests({ resourceTypes: ["fetch", "xhr"] })

// With pagination
mcp__chrome-devtools__list_network_requests({ resourceTypes: ["fetch"], pageSize: 20 })
```

### Viewport Resize
```typescript
// Mobile
mcp__chrome-devtools__resize_page({ width: 375, height: 667 })

// Tablet
mcp__chrome-devtools__resize_page({ width: 768, height: 1024 })

// Desktop
mcp__chrome-devtools__resize_page({ width: 1920, height: 1080 })
```

## Orchestration Patterns

For multi-tool workflows, use orchestration patterns to reduce token usage by 40-88%.

**Reference**: `/Users/admin/.claude/tools/orchestration-patterns.md`

| Pattern | Use Case | Savings |
|---------|----------|---------|
| verifyUI | After UI fixes | 82% |
| verifyAPI | After API changes | 75% |
| verifyResponsive | Responsive testing | 83% |
| verifyAuthFlow | Auth implementation | 79% |
| auditPerformance | Performance optimization | 81% |
| runE2EWorkflow | E2E testing | 83% |
| verifyMission | Multi-hero missions | 88% |

## Full Documentation

- **Tool Registry**: `/Users/admin/.claude/tools/tool-registry.json`
- **Tool Examples**: `/Users/admin/.claude/tools/tool-examples.md`
- **Orchestration**: `/Users/admin/.claude/tools/orchestration-patterns.md`

## Token Savings

**Before Tool Search Skill**:
- All tool definitions in system prompt: ~3000 tokens
- Each task loads full tool documentation

**With Tool Search Skill**:
- On-demand tool lookup: ~350 tokens
- Load only what you need

**Result**: 85% token reduction for tool discovery
