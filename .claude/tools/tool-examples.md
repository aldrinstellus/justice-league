# Tool Use Examples Library

> **Reference**: Anthropic Advanced Tool Use Patterns
> **Purpose**: Minimal → Partial → Full parameter examples for improved accuracy (72% → 90%)
> **Registry**: See `tool-registry.json` for complete tool catalog

---

## Usage Guide

Each tool example follows a progression:
1. **Minimal** - Required params only (fastest, basic use)
2. **Partial** - Common use case (recommended default)
3. **Full** - All parameters (advanced use)

---

## MCP Chrome DevTools

### Screenshot {#screenshot}

**Agents**: frontend-developer, qa-tester, e2e-tester, devops-engineer

```typescript
// MINIMAL - Viewport only, returns base64 (caution: large context)
await mcp__chrome-devtools__take_screenshot({})

// PARTIAL - Save to file (RECOMMENDED)
await mcp__chrome-devtools__take_screenshot({
  filePath: "feature-verification.png"
})

// FULL - All options
await mcp__chrome-devtools__take_screenshot({
  filePath: "/absolute/path/to/verification-desktop.png",
  format: "png",       // "png" | "jpeg" | "webp"
  quality: 95,         // 0-100, ignored for PNG
  fullPage: true       // Capture entire scrollable page
})

// ELEMENT-SPECIFIC - Capture specific component
await mcp__chrome-devtools__take_screenshot({
  uid: "nav-header",   // From take_snapshot output
  filePath: "header-component.png"
})
```

**Common Errors**:
- Using `uid` with `fullPage: true` - incompatible
- Missing `filePath` creates large base64 in context
- Relative paths may fail - use absolute paths

---

### Snapshot (A11y Tree) {#snapshot}

**Agents**: frontend-developer (accessibility), e2e-tester (element UIDs)

```typescript
// MINIMAL - Basic accessibility tree
await mcp__chrome-devtools__take_snapshot({})

// FULL - Verbose with all attributes
await mcp__chrome-devtools__take_snapshot({
  verbose: true,       // Include all a11y properties
  filePath: "page-snapshot.txt"  // Save to file
})
```

**Use Cases**:
- Find element UIDs for click/fill operations
- Verify ARIA labels present
- Check keyboard navigation order

---

### Navigation {#navigation}

**Agents**: ALL

```typescript
// URL Navigation (most common)
await mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3000",
  type: "url"
})

// Reload (fresh page)
await mcp__chrome-devtools__navigate_page({
  type: "reload",
  ignoreCache: true    // Bypass cache
})

// History navigation
await mcp__chrome-devtools__navigate_page({
  type: "back"         // or "forward"
})

// With timeout for slow pages
await mcp__chrome-devtools__navigate_page({
  url: "https://slow-site.com",
  type: "url",
  timeout: 30000       // 30 seconds
})
```

---

### Click {#click}

**Agents**: e2e-tester, qa-tester

**Prerequisite**: Run `take_snapshot` first to get element UIDs

```typescript
// MINIMAL - Single click
await mcp__chrome-devtools__click({
  uid: "submit-button"
})

// Double click
await mcp__chrome-devtools__click({
  uid: "item-row",
  dblClick: true
})
```

**Common Pattern**:
```typescript
// 1. Get element UIDs
await mcp__chrome-devtools__take_snapshot({})
// 2. Find target in snapshot output: button "Submit" [uid: "e7"]
// 3. Click
await mcp__chrome-devtools__click({ uid: "e7" })
```

---

### Fill (Single Field) {#fill}

**Agents**: e2e-tester, qa-tester

```typescript
// Single input
await mcp__chrome-devtools__fill({
  uid: "email-input",
  value: "test@example.com"
})

// Select dropdown
await mcp__chrome-devtools__fill({
  uid: "country-select",
  value: "United States"  // Option text, not value
})
```

---

### Fill Form (Multiple Fields) {#form-filling}

**Agents**: e2e-tester, qa-tester, security-specialist

**PREFERRED for multi-field forms** - More efficient than multiple fill calls

```typescript
// FULL - Batch form filling
await mcp__chrome-devtools__fill_form({
  elements: [
    { uid: "email", value: "test@example.com" },
    { uid: "password", value: "SecurePass123!" },
    { uid: "confirm-password", value: "SecurePass123!" },
    { uid: "terms", value: "true" },  // Checkbox
    { uid: "country", value: "United States" }  // Select
  ]
})
```

**Schema**:
```typescript
interface FillFormParams {
  elements: Array<{
    uid: string;    // Element UID from snapshot
    value: string;  // Text, select option, or checkbox value
  }>;
}
```

---

### Keyboard {#keyboard}

**Agents**: e2e-tester

```typescript
// Simple key
await mcp__chrome-devtools__press_key({
  key: "Enter"
})

// Modifier combinations
await mcp__chrome-devtools__press_key({
  key: "Control+A"     // Select all
})

await mcp__chrome-devtools__press_key({
  key: "Control+Shift+R"  // Hard refresh
})

// Special keys
await mcp__chrome-devtools__press_key({
  key: "Escape"
})

await mcp__chrome-devtools__press_key({
  key: "Tab"
})
```

**Modifiers**: Control, Shift, Alt, Meta

---

### Console Messages {#console}

**Agents**: ALL (debugging)

```typescript
// MINIMAL - All messages
await mcp__chrome-devtools__list_console_messages({})

// PARTIAL - Errors only (COMMON)
await mcp__chrome-devtools__list_console_messages({
  types: ["error"]
})

// PARTIAL - Errors and warnings
await mcp__chrome-devtools__list_console_messages({
  types: ["error", "warn"]
})

// FULL - Comprehensive debugging
await mcp__chrome-devtools__list_console_messages({
  types: ["error", "warn", "info", "log"],
  pageSize: 50,
  includePreservedMessages: true  // Include from previous navigations
})
```

**Type Values**: `log`, `debug`, `info`, `error`, `warn`, `dir`, `table`, `trace`

---

### Network Requests {#network}

**Agents**: backend-developer, qa-tester, security-specialist

```typescript
// MINIMAL - All requests
await mcp__chrome-devtools__list_network_requests({})

// PARTIAL - API calls only (COMMON)
await mcp__chrome-devtools__list_network_requests({
  resourceTypes: ["fetch", "xhr"]
})

// FULL - Comprehensive analysis
await mcp__chrome-devtools__list_network_requests({
  resourceTypes: ["fetch", "xhr", "document", "script"],
  pageSize: 50,
  includePreservedRequests: true
})

// Get detailed request
await mcp__chrome-devtools__get_network_request({
  reqid: 123  // From list_network_requests output
})
```

**Resource Types**: `document`, `stylesheet`, `image`, `font`, `script`, `xhr`, `fetch`, `websocket`, `manifest`

---

### Performance Trace {#performance}

**Agents**: frontend-developer (Core Web Vitals)

```typescript
// Start trace with auto-stop
await mcp__chrome-devtools__performance_start_trace({
  reload: true,    // Reload page during trace
  autoStop: true   // Stop automatically
})

// Manual stop (if autoStop: false)
await mcp__chrome-devtools__performance_stop_trace({})

// Analyze specific insight
await mcp__chrome-devtools__performance_analyze_insight({
  insightSetId: "Navigation-1",
  insightName: "LCPBreakdown"  // Largest Contentful Paint
})
```

**Insight Names**:
- `DocumentLatency` - Time to first byte
- `LCPBreakdown` - Largest Contentful Paint analysis
- `RenderBlocking` - Resources blocking render
- `NetworkDependencyTree` - Request waterfall

---

### Responsive Testing {#responsive}

**Agents**: frontend-developer

```typescript
// Mobile
await mcp__chrome-devtools__resize_page({
  width: 375,
  height: 667
})

// Tablet
await mcp__chrome-devtools__resize_page({
  width: 768,
  height: 1024
})

// Desktop
await mcp__chrome-devtools__resize_page({
  width: 1920,
  height: 1080
})
```

**Common Breakpoints**:
| Device | Width | Height |
|--------|-------|--------|
| iPhone SE | 375 | 667 |
| iPhone 14 | 390 | 844 |
| iPad | 768 | 1024 |
| iPad Pro | 1024 | 1366 |
| Desktop | 1920 | 1080 |

---

### Wait For Text {#wait}

**Agents**: e2e-tester

```typescript
// MINIMAL - Wait for text to appear
await mcp__chrome-devtools__wait_for({
  text: "Success"
})

// With timeout
await mcp__chrome-devtools__wait_for({
  text: "Loading complete",
  timeout: 10000  // 10 seconds
})
```

---

### Handle Dialog {#dialog}

**Agents**: e2e-tester

```typescript
// Accept dialog (confirm, alert)
await mcp__chrome-devtools__handle_dialog({
  action: "accept"
})

// Dismiss dialog
await mcp__chrome-devtools__handle_dialog({
  action: "dismiss"
})

// Prompt with text
await mcp__chrome-devtools__handle_dialog({
  action: "accept",
  promptText: "User input here"
})
```

---

### Evaluate Script {#evaluate}

**Agents**: security-specialist, advanced debugging

```typescript
// Get page title
await mcp__chrome-devtools__evaluate_script({
  function: "() => document.title"
})

// Get element text
await mcp__chrome-devtools__evaluate_script({
  function: "(el) => el.innerText",
  args: [{ uid: "header-title" }]
})

// Check localStorage
await mcp__chrome-devtools__evaluate_script({
  function: "() => JSON.stringify(localStorage)"
})

// Async operation
await mcp__chrome-devtools__evaluate_script({
  function: "async () => { const res = await fetch('/api/status'); return res.json(); }"
})
```

**Security Note**: Use for testing only, be cautious with user-provided scripts.

---

### Emulation {#emulate}

**Agents**: frontend-developer, qa-tester

```typescript
// Slow network
await mcp__chrome-devtools__emulate({
  networkConditions: "Slow 3G"
})

// CPU throttling
await mcp__chrome-devtools__emulate({
  cpuThrottlingRate: 4  // 4x slowdown
})

// Combined (performance testing)
await mcp__chrome-devtools__emulate({
  networkConditions: "Fast 4G",
  cpuThrottlingRate: 2
})

// Reset
await mcp__chrome-devtools__emulate({
  networkConditions: "No emulation",
  cpuThrottlingRate: 1
})
```

**Network Conditions**: `No emulation`, `Offline`, `Slow 3G`, `Fast 3G`, `Slow 4G`, `Fast 4G`

---

## File Operations

### Read {#read}

```typescript
// Full file
Read({
  file_path: "/absolute/path/to/file.ts"
})

// Partial (large files)
Read({
  file_path: "/absolute/path/to/large-file.ts",
  offset: 100,  // Start at line 100
  limit: 50     // Read 50 lines
})
```

---

### Grep {#grep}

```typescript
// Find files containing pattern
Grep({
  pattern: "useState|useEffect",
  glob: "*.tsx",
  output_mode: "files_with_matches"
})

// Show matching lines
Grep({
  pattern: "TODO|FIXME",
  output_mode: "content",
  "-n": true,  // Line numbers
  "-i": true   // Case insensitive
})

// With context
Grep({
  pattern: "function handleSubmit",
  output_mode: "content",
  "-A": 10,  // 10 lines after
  "-B": 2    // 2 lines before
})
```

---

### Glob {#glob}

```typescript
// Find TypeScript files
Glob({
  pattern: "**/*.tsx"
})

// Find in specific directory
Glob({
  pattern: "*.md",
  path: "/Users/admin/Documents/claudecode"
})

// Multiple extensions
Glob({
  pattern: "**/*.{ts,tsx,js,jsx}"
})
```

---

## Git Operations (via Bash)

### Status & Diff

```bash
# Current status
git status

# Staged changes
git diff --staged

# Full diff with stats
git diff --stat

# Parallel (efficient)
git status && git diff --stat
```

### Commit

```bash
# With HEREDOC for multiline message
git commit -m "$(cat <<'EOF'
feat: add user authentication

- Implement OAuth 2.0 flow
- Add session management
- Include CSRF protection

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Figma API

### Fetch File

```typescript
// Basic file fetch
const response = await fetch(
  `https://api.figma.com/v1/files/${FILE_KEY}`,
  { headers: { "X-Figma-Token": FIGMA_TOKEN } }
)

// Specific nodes
const response = await fetch(
  `https://api.figma.com/v1/files/${FILE_KEY}/nodes?ids=${NODE_IDS.join(',')}`,
  { headers: { "X-Figma-Token": FIGMA_TOKEN } }
)

// Export images
const response = await fetch(
  `https://api.figma.com/v1/images/${FILE_KEY}?ids=${NODE_ID}&format=png&scale=2`,
  { headers: { "X-Figma-Token": FIGMA_TOKEN } }
)
```

---

## BrightData Web Scraping

### Scrape Page

```typescript
// Scrape as markdown
await mcp__brightdata__scrape_as_markdown({
  url: "https://example.com/page"
})
```

### Search

```typescript
// Google search
await mcp__brightdata__search_engine({
  query: "Claude Code advanced patterns",
  engine: "google"
})

// Bing search
await mcp__brightdata__search_engine({
  query: "site:anthropic.com tool use",
  engine: "bing"
})
```

---

## Common Workflows

### Visual Verification (Recommended)

```typescript
// 1. Navigate
await mcp__chrome-devtools__navigate_page({ url: "http://localhost:3000", type: "url" })

// 2. Screenshot
await mcp__chrome-devtools__take_screenshot({ filePath: "feature-complete.png" })

// 3. Check errors
await mcp__chrome-devtools__list_console_messages({ types: ["error"] })
```

### Form Testing

```typescript
// 1. Navigate to form
await mcp__chrome-devtools__navigate_page({ url: "http://localhost:3000/register", type: "url" })

// 2. Fill all fields
await mcp__chrome-devtools__fill_form({
  elements: [
    { uid: "name", value: "Test User" },
    { uid: "email", value: "test@example.com" },
    { uid: "password", value: "SecurePass123!" }
  ]
})

// 3. Submit
await mcp__chrome-devtools__click({ uid: "submit-btn" })

// 4. Wait for response
await mcp__chrome-devtools__wait_for({ text: "Success" })

// 5. Verify
await mcp__chrome-devtools__take_screenshot({ filePath: "registration-success.png" })
```

### Responsive Testing

```typescript
const breakpoints = [
  { name: "mobile", width: 375, height: 667 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "desktop", width: 1920, height: 1080 }
]

await mcp__chrome-devtools__navigate_page({ url: "http://localhost:3000", type: "url" })

for (const bp of breakpoints) {
  await mcp__chrome-devtools__resize_page({ width: bp.width, height: bp.height })
  await mcp__chrome-devtools__take_screenshot({ filePath: `responsive-${bp.name}.png` })
}
```

---

## Error Recovery

### If Tool Call Fails

1. Check parameters against examples above
2. Verify element UIDs exist (run take_snapshot first)
3. Check page has loaded (use wait_for if needed)
4. Try with timeout for slow operations

### Common Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Element not found | UID changed | Re-run take_snapshot |
| Timeout | Page slow | Increase timeout parameter |
| Network error | Page didn't load | Add navigate_page first |
| Permission denied | File path issue | Use absolute path |

---

**Last Updated**: 2025-11-25
**Reference**: [Anthropic Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)
