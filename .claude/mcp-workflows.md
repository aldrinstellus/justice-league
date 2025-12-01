# Chrome DevTools MCP Workflows

This file contains detailed Chrome DevTools MCP integration workflows for automated browser testing and verification. Loaded on-demand when Oracle needs to perform visual testing or debugging.

## Overview

Oracle can use Chrome DevTools MCP for automated browser testing and verification without manual browser interaction.

### When to Use Chrome DevTools MCP
1. **User reports UI issue** → Take screenshot first to see the issue
2. **After fixing bugs** → Take before/after screenshots
3. **Deployment verification** → Navigate to URL, take screenshot, check console
4. **TypeScript errors fixed** → Check console for runtime errors
5. **Performance concerns** → Run performance trace
6. **Manual testing needed** → Automate with interactive commands

---

## Visual Verification Workflows

### Screenshot Operations
- ✅ Take screenshots before/after fixes: `mcp__chrome-devtools__take_screenshot`
- ✅ Capture broken UI states for diagnosis
- ✅ Verify deployment visually with screenshots
- ✅ Take text snapshots of page structure: `mcp__chrome-devtools__take_snapshot`
- ✅ Compare before/after states automatically

### Screenshot Options
```javascript
// Basic screenshot
mcp__chrome-devtools__take_screenshot({ filePath: "screenshot.png" })

// Full page screenshot
mcp__chrome-devtools__take_screenshot({
  filePath: "full-page.png",
  fullPage: true
})

// Element screenshot
mcp__chrome-devtools__take_screenshot({
  filePath: "element.png",
  uid: "element-123"
})

// JPEG with compression
mcp__chrome-devtools__take_screenshot({
  filePath: "screenshot.jpg",
  format: "jpeg",
  quality: 80
})
```

---

## Console Debugging Workflows

### Console Error Detection
- ✅ List console errors automatically: `mcp__chrome-devtools__list_console_messages`
- ✅ Filter by error type (error, warn, log, info)
- ✅ Diagnose JavaScript issues without manual browser inspection
- ✅ Get console message details: `mcp__chrome-devtools__get_console_message`

### Console Operations
```javascript
// List all errors
mcp__chrome-devtools__list_console_messages({ types: ["error"] })

// List errors and warnings
mcp__chrome-devtools__list_console_messages({
  types: ["error", "warn"]
})

// Paginated results
mcp__chrome-devtools__list_console_messages({
  types: ["error"],
  pageSize: 20,
  pageIdx: 0
})

// Get specific message details
mcp__chrome-devtools__get_console_message({ msgid: 123 })
```

---

## Network Inspection Workflows

### Network Request Analysis
- ✅ List network requests: `mcp__chrome-devtools__list_network_requests`
- ✅ Check failed requests and status codes
- ✅ Debug API issues automatically
- ✅ Filter by resource type (fetch, xhr, document, etc.)
- ✅ Get detailed request info: `mcp__chrome-devtools__get_network_request`

### Network Operations
```javascript
// List all requests
mcp__chrome-devtools__list_network_requests()

// List failed requests
mcp__chrome-devtools__list_network_requests({
  resourceTypes: ["fetch", "xhr"]
})

// Paginated results
mcp__chrome-devtools__list_network_requests({
  pageSize: 20,
  pageIdx: 0
})

// Get specific request details
mcp__chrome-devtools__get_network_request({ reqid: 456 })

// Get currently selected request
mcp__chrome-devtools__get_network_request()
```

---

## Performance Testing Workflows

### Performance Trace Operations
- ✅ Start performance traces: `mcp__chrome-devtools__performance_start_trace`
- ✅ Stop and analyze traces: `mcp__chrome-devtools__performance_stop_trace`
- ✅ Analyze specific insights: `mcp__chrome-devtools__performance_analyze_insight`
- ✅ Identify Core Web Vitals issues
- ✅ Detect performance bottlenecks automatically

### Performance Operations
```javascript
// Start trace with reload
mcp__chrome-devtools__performance_start_trace({
  reload: true,
  autoStop: true
})

// Start trace without reload
mcp__chrome-devtools__performance_start_trace({
  reload: false,
  autoStop: false
})

// Stop trace
mcp__chrome-devtools__performance_stop_trace()

// Analyze specific insight
mcp__chrome-devtools__performance_analyze_insight({
  insightSetId: "insight-123",
  insightName: "LCPBreakdown"
})
```

---

## Interactive Testing Workflows

### Page Navigation
```javascript
// Navigate to URL
mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3003",
  type: "url"
})

// Navigate back
mcp__chrome-devtools__navigate_page({ type: "back" })

// Navigate forward
mcp__chrome-devtools__navigate_page({ type: "forward" })

// Reload page
mcp__chrome-devtools__navigate_page({
  type: "reload",
  ignoreCache: true
})
```

### Element Interactions
```javascript
// Click element
mcp__chrome-devtools__click({ uid: "button-123" })

// Double click
mcp__chrome-devtools__click({
  uid: "button-123",
  dblClick: true
})

// Hover element
mcp__chrome-devtools__hover({ uid: "element-456" })

// Fill input
mcp__chrome-devtools__fill({
  uid: "input-789",
  value: "test@example.com"
})

// Fill multiple fields
mcp__chrome-devtools__fill_form({
  elements: [
    { uid: "email-input", value: "test@example.com" },
    { uid: "password-input", value: "password123" }
  ]
})

// Press key
mcp__chrome-devtools__press_key({ key: "Enter" })

// Press key combination
mcp__chrome-devtools__press_key({ key: "Control+A" })

// Drag and drop
mcp__chrome-devtools__drag({
  from_uid: "element-1",
  to_uid: "element-2"
})

// Upload file
mcp__chrome-devtools__upload_file({
  uid: "file-input",
  filePath: "/path/to/file.pdf"
})

// Wait for text
mcp__chrome-devtools__wait_for({
  text: "Success",
  timeout: 5000
})
```

---

## Multi-Page Management

### Page Operations
```javascript
// List all pages
mcp__chrome-devtools__list_pages()

// Create new page
mcp__chrome-devtools__new_page({
  url: "https://example.com"
})

// Select active page
mcp__chrome-devtools__select_page({ pageIdx: 0 })

// Close page
mcp__chrome-devtools__close_page({ pageIdx: 1 })

// Resize viewport
mcp__chrome-devtools__resize_page({
  width: 1920,
  height: 1080
})
```

---

## Advanced Features

### Device Emulation
```javascript
// Emulate network conditions
mcp__chrome-devtools__emulate({
  networkConditions: "Slow 3G"
})

// CPU throttling
mcp__chrome-devtools__emulate({
  cpuThrottlingRate: 4
})

// Combined emulation
mcp__chrome-devtools__emulate({
  networkConditions: "Fast 4G",
  cpuThrottlingRate: 2
})

// Disable emulation
mcp__chrome-devtools__emulate({
  networkConditions: "No emulation",
  cpuThrottlingRate: 1
})
```

### JavaScript Execution
```javascript
// Execute simple function
mcp__chrome-devtools__evaluate_script({
  function: "() => { return document.title }"
})

// Execute with arguments
mcp__chrome-devtools__evaluate_script({
  function: "(el) => { return el.innerText }",
  args: [{ uid: "element-123" }]
})

// Execute async function
mcp__chrome-devtools__evaluate_script({
  function: "async () => { return await fetch('/api/data').then(r => r.json()) }"
})
```

### Dialog Handling
```javascript
// Accept dialog
mcp__chrome-devtools__handle_dialog({ action: "accept" })

// Dismiss dialog
mcp__chrome-devtools__handle_dialog({ action: "dismiss" })

// Accept with prompt text
mcp__chrome-devtools__handle_dialog({
  action: "accept",
  promptText: "User input"
})
```

---

## Common MCP Workflows

### Workflow 1: UI Issue Diagnosis
```javascript
// Navigate to page
await mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3003",
  type: "url"
})

// Take screenshot
await mcp__chrome-devtools__take_screenshot({
  filePath: "ui-broken.png"
})

// Check console errors
await mcp__chrome-devtools__list_console_messages({
  types: ["error", "warn"]
})

// Take text snapshot
await mcp__chrome-devtools__take_snapshot({
  verbose: false
})
```

**Use Case**: User reports "UI is broken"
**Time Saved**: 2-3 minutes vs manual browser inspection

---

### Workflow 2: Vercel Deployment Verification
```javascript
// Navigate to deployment
await mcp__chrome-devtools__new_page({
  url: "https://app.vercel.app"
})

// Take screenshot
await mcp__chrome-devtools__take_screenshot({
  filePath: "vercel-deployed.png"
})

// Check for errors
await mcp__chrome-devtools__list_console_messages({
  types: ["error"]
})

// Check network failures
await mcp__chrome-devtools__list_network_requests({
  resourceTypes: ["fetch", "xhr"]
})
```

**Use Case**: Verify deployment succeeded
**Time Saved**: 1-2 minutes vs manual verification

---

### Workflow 3: Theme Editor Testing
```javascript
// Navigate to theme editor
await mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3003/editor/theme",
  type: "url"
})

// Take snapshot to get element UIDs
await mcp__chrome-devtools__take_snapshot()

// Click color picker (using UID from snapshot)
await mcp__chrome-devtools__click({
  uid: "color-picker-123"
})

// Fill color value
await mcp__chrome-devtools__fill({
  uid: "color-input-456",
  value: "#ff3366"
})

// Take screenshot of result
await mcp__chrome-devtools__take_screenshot({
  filePath: "theme-updated.png"
})
```

**Use Case**: Interactive feature testing
**Time Saved**: 2-3 minutes vs manual testing

---

### Workflow 4: Performance Testing
```javascript
// Start performance trace with reload
await mcp__chrome-devtools__performance_start_trace({
  reload: true,
  autoStop: true
})

// Navigate to page (triggers trace)
await mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3003",
  type: "url"
})

// Wait for trace to complete
// Tool provides insight sets automatically

// Analyze specific insights
await mcp__chrome-devtools__performance_analyze_insight({
  insightSetId: "insight-set-1",
  insightName: "LCPBreakdown"
})
```

**Use Case**: Performance optimization
**Time Saved**: 5-10 minutes vs manual Lighthouse testing

---

### Workflow 5: Form Testing
```javascript
// Navigate to form
await mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3003/signup",
  type: "url"
})

// Fill multiple fields at once
await mcp__chrome-devtools__fill_form({
  elements: [
    { uid: "email-input", value: "test@example.com" },
    { uid: "password-input", value: "securepass123" },
    { uid: "name-input", value: "Test User" }
  ]
})

// Click submit button
await mcp__chrome-devtools__click({
  uid: "submit-button"
})

// Wait for success message
await mcp__chrome-devtools__wait_for({
  text: "Account created successfully"
})

// Take screenshot of result
await mcp__chrome-devtools__take_screenshot({
  filePath: "form-submitted.png"
})
```

**Use Case**: End-to-end form testing
**Time Saved**: 2-3 minutes vs manual form testing

---

### Workflow 6: Before/After Fix Documentation
```javascript
// BEFORE FIX
// Navigate to broken page
await mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3003",
  type: "url"
})

// Take "before" screenshot
await mcp__chrome-devtools__take_screenshot({
  filePath: "before-fix.png"
})

// List console errors
const beforeErrors = await mcp__chrome-devtools__list_console_messages({
  types: ["error"]
})

// ... Apply fix (cache cleanup, code changes, etc.) ...

// AFTER FIX
// Hard refresh page
await mcp__chrome-devtools__navigate_page({
  type: "reload",
  ignoreCache: true
})

// Take "after" screenshot
await mcp__chrome-devtools__take_screenshot({
  filePath: "after-fix.png"
})

// List console errors
const afterErrors = await mcp__chrome-devtools__list_console_messages({
  types: ["error"]
})

// Report: "Before: 5 errors → After: 0 errors ✅"
```

**Use Case**: Document bug fixes with visual proof
**Time Saved**: 3-5 minutes vs manual documentation

---

## MCP-First Workflow Pattern

### Old Pattern (Manual)
```
User: "UI is broken"
Oracle: Diagnoses → Fixes → User manually checks
```

### New Pattern (MCP-First)
```
User: "UI is broken"
Oracle: Takes screenshot → Shows user → Diagnoses → Fixes → Takes screenshot → Shows before/after
```

---

## Time Savings with MCP

| Activity | Manual Time | MCP Time | Savings |
|----------|-------------|----------|---------|
| UI verification | 3-5 min | 30 sec | 2-4 min |
| Deployment checking | 2-3 min | 30 sec | 1-2 min |
| Console error diagnosis | 2-3 min | 30 sec | 1-2 min |
| Performance testing | 10-15 min | 2-3 min | 7-12 min |
| Form testing | 3-5 min | 1 min | 2-4 min |
| **Total per session** | - | - | **10-20 min** |

---

## Playwright MCP Research Note

**Current Status**: Playwright MCP not currently available in tool set.

**Chrome DevTools MCP vs Playwright**:
- **Chrome DevTools** = Live browser automation (current, available)
- **Playwright** = Headless browser automation (not available yet)

**If Playwright MCP becomes available in future**:
- Use for headless E2E testing
- Use for CI/CD integration
- Use for parallel test execution
- Chrome DevTools MCP still preferred for visual debugging

**Current Recommendation**: Use Chrome DevTools MCP for all browser automation needs.

---

## Oracle's MCP-First Protocol

1. When user reports "UI is broken" → Take screenshot FIRST
2. When deployment succeeds → Verify with screenshot + console check
3. When fixing bugs → Document with before/after screenshots
4. When testing features → Use interactive MCP commands
5. When optimizing → Use performance trace

---

## Benefits of MCP-First Approach

- ✅ Faster diagnosis (visual evidence immediate)
- ✅ Better communication (show, don't tell)
- ✅ Reduced back-and-forth (screenshot proves it works)
- ✅ Automated verification (no manual browser checking)
- ✅ Documentation (screenshots serve as proof)
- ✅ Time savings (10-20 minutes per session)

---

**Last Updated**: 2025-11-24
**Purpose**: Detailed Chrome DevTools MCP workflows for automated browser testing and verification
