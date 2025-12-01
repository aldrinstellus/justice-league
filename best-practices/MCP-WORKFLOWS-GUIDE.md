# MCP Workflows Guide

**Last Updated**: 2025-11-24
**Purpose**: Comprehensive guide for using Chrome DevTools MCP with Claude Code agents

---

## Table of Contents

1. [What is Chrome DevTools MCP](#what-is-chrome-devtools-mcp)
2. [Why MCP Matters](#why-mcp-matters)
3. [Agent-Specific Workflows](#agent-specific-workflows)
4. [Common Patterns](#common-patterns)
5. [Troubleshooting](#troubleshooting)
6. [Real-World Examples](#real-world-examples)

---

## What is Chrome DevTools MCP

**MCP (Model Context Protocol)** is Claude Code's integration with Chrome DevTools that enables **automated browser testing and visual verification** directly from agents.

### Key Capabilities

| Feature | Description | Use Case |
|---------|-------------|----------|
| **Visual Verification** | Take screenshots, capture page snapshots | Verify UI changes, document bugs |
| **Console Debugging** | List console errors automatically | Catch JavaScript issues |
| **Network Inspection** | Monitor API calls, check status codes | Debug failed requests |
| **Performance Testing** | Run performance traces, analyze Core Web Vitals | Optimize load times |
| **Interactive Testing** | Click, fill forms, navigate pages | Automate user flows |

### MCP vs Manual Testing

| Task | Manual | With MCP | Time Saved |
|------|--------|----------|------------|
| Check UI across 3 viewports | 5 min | 30 sec | 90% |
| Verify deployment | 3 min | 45 sec | 75% |
| Test user flow | 10 min | 2 min | 80% |
| Check console errors | 2 min | 15 sec | 87% |

**Total time savings per task: 40-80%**

---

## Why MCP Matters

### Before MCP (Manual Workflow)

```
Agent: "I've fixed the responsive layout bug"
User: [Opens browser manually]
User: [Resizes to mobile]
User: [Takes screenshot]
User: [Checks console]
User: [Resizes to tablet]
User: [Takes screenshot]
User: [Resizes to desktop]
User: [Takes screenshot]
User: "Looks good!"
⏱️ Total: 5 minutes
```

### After MCP (Automated Workflow)

```typescript
Agent: "I've fixed the responsive layout bug"
// Agent automatically verifies
await mcp__chrome-devtools__resize_page({ width: 375, height: 667 })
await mcp__chrome-devtools__take_screenshot({ filePath: "mobile.png" })
await mcp__chrome-devtools__resize_page({ width: 768, height: 1024 })
await mcp__chrome-devtools__take_screenshot({ filePath: "tablet.png" })
await mcp__chrome-devtools__resize_page({ width: 1920, height: 1080 })
await mcp__chrome-devtools__take_screenshot({ filePath: "desktop.png" })
await mcp__chrome-devtools__list_console_messages({ types: ["error"] })

Agent: "Verified: mobile.png, tablet.png, desktop.png - 0 console errors"
⏱️ Total: 30 seconds
```

### Benefits

1. **Faster Feedback Loops**: Agents verify their own work immediately
2. **Visual Proof**: Screenshots document bugs and fixes
3. **Reduced Back-and-Forth**: No "can you check" messages
4. **Automated Error Detection**: Console errors caught automatically
5. **Better Documentation**: Screenshots serve as evidence

---

## Agent-Specific Workflows

### Frontend Developer MCP Workflows

**Primary Use Cases**: Responsive design, accessibility, performance optimization

#### Workflow 1: Responsive Design Verification (REQUIRED)

**When to use**: After ANY UI change (component, layout, styling)

```typescript
// Step 1: Navigate to page
await mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3000/dashboard",
  type: "url"
})

// Step 2: Test Mobile (375px)
await mcp__chrome-devtools__resize_page({ width: 375, height: 667 })
await mcp__chrome-devtools__take_screenshot({ filePath: "frontend-mobile-375px.png" })

// Step 3: Test Tablet (768px)
await mcp__chrome-devtools__resize_page({ width: 768, height: 1024 })
await mcp__chrome-devtools__take_screenshot({ filePath: "frontend-tablet-768px.png" })

// Step 4: Test Desktop (1920px)
await mcp__chrome-devtools__resize_page({ width: 1920, height: 1080 })
await mcp__chrome-devtools__take_screenshot({ filePath: "frontend-desktop-1920px.png" })

// Step 5: Check console errors
await mcp__chrome-devtools__list_console_messages({ types: ["error", "warn"] })
```

**Report Template**:
```markdown
✅ **Responsive Design Verified**
- Mobile (375px): ✅ Layout adapts correctly (frontend-mobile-375px.png)
- Tablet (768px): ✅ No horizontal scroll (frontend-tablet-768px.png)
- Desktop (1920px): ✅ Max-width container works (frontend-desktop-1920px.png)
- Console: 0 errors, 2 warnings (font loading - non-blocking)
```

**Time Savings**: 4.5 min → 30 sec (90% faster)

---

#### Workflow 2: Accessibility Verification

**When to use**: After adding interactive elements (buttons, forms, modals)

```typescript
// Navigate to page
await mcp__chrome-devtools__navigate_page({ url: "http://localhost:3000/signup", type: "url" })

// Take snapshot to get element UIDs
await mcp__chrome-devtools__take_snapshot({ verbose: false })

// Test keyboard navigation
await mcp__chrome-devtools__press_key({ key: "Tab" })
await mcp__chrome-devtools__press_key({ key: "Tab" })
await mcp__chrome-devtools__take_screenshot({ filePath: "a11y-focus-visible.png" })

// Check ARIA attributes in snapshot
// Look for: role="button", aria-label, aria-describedby

// Test screen reader announcements in console
await mcp__chrome-devtools__list_console_messages({ types: ["log", "info"] })
```

**Report Template**:
```markdown
✅ **Accessibility Verified (WCAG 2.1 AA)**
- Keyboard navigation: ✅ All interactive elements focusable
- Focus indicators: ✅ 2px solid outline visible (a11y-focus-visible.png)
- ARIA labels: ✅ All buttons have aria-label
- Color contrast: ✅ 4.5:1 minimum (checked in snapshot)
```

---

#### Workflow 3: Performance Optimization

**When to use**: After adding heavy components (charts, images, animations)

```typescript
// Start performance trace
await mcp__chrome-devtools__performance_start_trace({
  reload: true,
  autoStop: true
})

// Navigate to page (triggers trace)
await mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3000/analytics",
  type: "url"
})

// Wait for trace to complete (auto-stops)
// Check for performance insights
// Tool provides Core Web Vitals automatically

// Take screenshot after load
await mcp__chrome-devtools__take_screenshot({ filePath: "perf-loaded.png" })
```

**Report Template**:
```markdown
✅ **Performance Verified**
- LCP: 1.8s (target: <2.5s) ✅
- FID: 45ms (target: <100ms) ✅
- CLS: 0.05 (target: <0.1) ✅
- Time to Interactive: 2.1s
- Screenshot: perf-loaded.png
```

---

### Backend Developer MCP Workflows

**Primary Use Cases**: API testing, authentication flows, database verification

#### Workflow 1: API Endpoint Verification (REQUIRED)

**When to use**: After creating/modifying ANY API endpoint

```typescript
// Step 1: Navigate to page that calls API
await mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3000/dashboard",
  type: "url"
})

// Step 2: Monitor network requests
await mcp__chrome-devtools__list_network_requests({
  resourceTypes: ["fetch", "xhr"]
})
// Check: Status 200, correct response body, no errors

// Step 3: Check console for API errors
await mcp__chrome-devtools__list_console_messages({ types: ["error"] })
```

**Report Template**:
```markdown
✅ **API Endpoints Verified**
- GET /api/users: 200 OK (152ms)
- POST /api/tasks: 201 Created (89ms)
- GET /api/analytics: 200 OK (243ms)
- Console: 0 errors
```

**Time Savings**: 3 min → 45 sec (75% faster)

---

#### Workflow 2: Authentication Flow Testing

**When to use**: After implementing login, signup, password reset

```typescript
// Step 1: Navigate to login
await mcp__chrome-devtools__navigate_page({ url: "http://localhost:3000/login", type: "url" })

// Step 2: Fill login form
await mcp__chrome-devtools__fill_form({
  elements: [
    { uid: "email-input", value: "test@example.com" },
    { uid: "password-input", value: "testpass123" }
  ]
})

// Step 3: Submit and monitor auth API
await mcp__chrome-devtools__click({ uid: "submit-button" })

// Step 4: Check network for auth request
await mcp__chrome-devtools__list_network_requests({ resourceTypes: ["fetch", "xhr"] })
// Look for: POST /api/auth/login

// Step 5: Verify redirect
await mcp__chrome-devtools__wait_for({ text: "Dashboard" })
await mcp__chrome-devtools__take_screenshot({ filePath: "backend-auth-success.png" })
```

**Report Template**:
```markdown
✅ **Authentication Flow Verified**
- Login form: ✅ Submits correctly
- API: POST /api/auth/login → 200 OK
- Session: ✅ Cookie set (httpOnly, secure, sameSite)
- Redirect: ✅ /dashboard loaded (backend-auth-success.png)
```

---

#### Workflow 3: Error Handling Verification

**When to use**: After implementing error handling for API failures

```typescript
// Test 1: Invalid credentials
await mcp__chrome-devtools__fill_form({
  elements: [
    { uid: "email-input", value: "wrong@example.com" },
    { uid: "password-input", value: "wrongpass" }
  ]
})
await mcp__chrome-devtools__click({ uid: "submit-button" })

// Check for error message in UI
await mcp__chrome-devtools__take_snapshot()
// Look for: "Invalid credentials" text

// Check network response
await mcp__chrome-devtools__list_network_requests({ resourceTypes: ["fetch"] })
// Expected: POST /api/auth/login → 401 Unauthorized

// Test 2: Server error (500)
// (Temporarily break server or mock failure)
// Verify error message shown to user

await mcp__chrome-devtools__take_screenshot({ filePath: "backend-error-handling.png" })
```

**Report Template**:
```markdown
✅ **Error Handling Verified**
- Invalid credentials: ✅ 401 → "Invalid credentials" shown
- Server error: ✅ 500 → "Something went wrong" shown
- Network failure: ✅ Timeout → "Connection error" shown
- Screenshot: backend-error-handling.png
```

---

### Security Specialist MCP Workflows

**Primary Use Cases**: OWASP testing, XSS/CSRF/SQL injection, RBAC verification

#### Workflow 1: XSS Prevention Testing (REQUIRED)

**When to use**: After implementing user input fields (comments, forms, profiles)

```typescript
// Step 1: Navigate to page with input
await mcp__chrome-devtools__navigate_page({ url: "http://localhost:3000/profile", type: "url" })

// Step 2: Attempt XSS attack
await mcp__chrome-devtools__fill({
  uid: "bio-input",
  value: "<script>alert('XSS')</script><img src=x onerror=alert('XSS')>"
})

// Step 3: Submit form
await mcp__chrome-devtools__click({ uid: "save-button" })

// Step 4: Check if script executed
await mcp__chrome-devtools__evaluate_script({
  function: `() => {
    const alerts = document.querySelectorAll('script');
    return { scriptTagsFound: alerts.length > 0 };
  }`
})
// Expected: { scriptTagsFound: false }

// Step 5: Check console for XSS attempts
await mcp__chrome-devtools__list_console_messages({ types: ["error", "warn"] })

// Step 6: Take screenshot
await mcp__chrome-devtools__take_screenshot({ filePath: "security-xss-test.png" })
```

**Report Template**:
```markdown
✅ **XSS Prevention Verified**
- Input sanitized: ✅ <script> tags removed
- No alert dialogs: ✅ Script did not execute
- Console: No XSS warnings
- Screenshot: security-xss-test.png shows sanitized output
```

**Time Savings**: 5 min → 1 min (80% faster)

---

#### Workflow 2: CSRF Protection Testing

**When to use**: After implementing state-changing endpoints (POST/PUT/DELETE)

```typescript
// Step 1: Attempt request without CSRF token
await mcp__chrome-devtools__navigate_page({ url: "http://localhost:3000/dashboard", type: "url" })

// Step 2: Try CSRF attack via JavaScript
await mcp__chrome-devtools__evaluate_script({
  function: `() => {
    return fetch('/api/users/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId: 123 })
      // No CSRF token included
    }).then(r => ({ status: r.status, statusText: r.statusText }));
  }`
})
// Expected: { status: 403, statusText: "Forbidden" }

// Step 3: Verify rejection in network panel
await mcp__chrome-devtools__list_network_requests({ resourceTypes: ["fetch"] })
// Look for: POST /api/users/delete → 403

await mcp__chrome-devtools__take_screenshot({ filePath: "security-csrf-blocked.png" })
```

**Report Template**:
```markdown
✅ **CSRF Protection Verified**
- Request without token: ✅ 403 Forbidden
- CSRF token validation: ✅ Active
- Same-origin policy: ✅ Enforced
```

---

#### Workflow 3: SQL Injection Testing

**When to use**: After implementing search, filters, or dynamic queries

```typescript
// Step 1: Navigate to search page
await mcp__chrome-devtools__navigate_page({ url: "http://localhost:3000/search", type: "url" })

// Step 2: Attempt SQL injection
await mcp__chrome-devtools__fill({
  uid: "search-input",
  value: "'; DROP TABLE users; --"
})

// Step 3: Submit search
await mcp__chrome-devtools__click({ uid: "search-button" })

// Step 4: Check network response
await mcp__chrome-devtools__list_network_requests({ resourceTypes: ["fetch"] })
// Expected: GET /api/search?q=%27%3B%20DROP%20TABLE%20users%3B%20-- → 200
// Should return empty results, NOT execute SQL

// Step 5: Check console for SQL errors
await mcp__chrome-devtools__list_console_messages({ types: ["error"] })
// Expected: <no console messages found>

await mcp__chrome-devtools__take_screenshot({ filePath: "security-sql-safe.png" })
```

**Report Template**:
```markdown
✅ **SQL Injection Prevention Verified**
- SQL injection attempt: ✅ Blocked (parameterized queries)
- No database errors: ✅ Console clean
- Empty results returned: ✅ Safe behavior
```

---

### DevOps Engineer MCP Workflows

**Primary Use Cases**: Deployment verification, blue-green testing, performance checks

#### Workflow 1: Deployment Verification (REQUIRED)

**When to use**: After EVERY deployment to staging/production

```typescript
// Step 1: Navigate to deployed URL
await mcp__chrome-devtools__navigate_page({
  url: "https://your-app.vercel.app",
  type: "url"
})

// Step 2: Take screenshot
await mcp__chrome-devtools__take_screenshot({ filePath: "devops-deployment-live.png" })

// Step 3: Check console errors
await mcp__chrome-devtools__list_console_messages({ types: ["error"] })
// Expected: <no console messages found>

// Step 4: Verify API endpoints
await mcp__chrome-devtools__list_network_requests({ resourceTypes: ["fetch", "xhr"] })
// Check all API calls return 200 OK

// Step 5: Performance check
await mcp__chrome-devtools__performance_start_trace({
  reload: true,
  autoStop: true
})
// Check LCP, FID, CLS metrics
```

**Report Template**:
```markdown
✅ **Deployment Verified**
- URL: https://app.vercel.app → 200 OK
- Screenshot: devops-deployment-live.png
- Console: 0 errors
- API endpoints: All responding correctly
- Performance: LCP 1.8s, FID 45ms, CLS 0.05
- SSL: Valid certificate
- Uptime: Monitoring enabled
```

**Time Savings**: 5 min → 1.5 min (70% faster)

---

#### Workflow 2: Blue-Green Deployment Testing

**When to use**: Before cutting over to new version

```typescript
// Test Blue (current production)
await mcp__chrome-devtools__new_page({ url: "https://blue.app.com" })
await mcp__chrome-devtools__take_screenshot({ filePath: "devops-blue-env.png" })
await mcp__chrome-devtools__list_console_messages({ types: ["error"] })

// Test Green (new version)
await mcp__chrome-devtools__new_page({ url: "https://green.app.com" })
await mcp__chrome-devtools__take_screenshot({ filePath: "devops-green-env.png" })
await mcp__chrome-devtools__list_console_messages({ types: ["error"] })

// Compare: Both should work, green has new features
```

**Report Template**:
```markdown
✅ **Blue-Green Deployment Ready**
- Blue (current): ✅ Stable (0 errors)
- Green (new): ✅ Stable (0 errors)
- New features: ✅ Working in green
- Rollback plan: ✅ Blue remains available
- Decision: **Ready for cutover**
```

---

### QA Tester MCP Workflows

**Primary Use Cases**: Automated test execution, cross-browser testing, error state testing

#### Workflow 1: User Flow Testing (REQUIRED)

**When to use**: After implementing ANY user-facing feature

```typescript
// Step 1: Navigate to app
await mcp__chrome-devtools__navigate_page({ url: "http://localhost:3000", type: "url" })

// Step 2: Fill registration form
await mcp__chrome-devtools__fill_form({
  elements: [
    { uid: "username", value: "testuser" },
    { uid: "email", value: "test@example.com" },
    { uid: "password", value: "SecurePass123!" }
  ]
})

// Step 3: Submit form
await mcp__chrome-devtools__click({ uid: "submit-btn" })

// Step 4: Wait for success message
await mcp__chrome-devtools__wait_for({ text: "Registration successful" })

// Step 5: Take screenshot
await mcp__chrome-devtools__take_screenshot({ filePath: "qa-registration-success.png" })

// Step 6: Verify redirect
await mcp__chrome-devtools__wait_for({ text: "Dashboard" })
await mcp__chrome-devtools__take_screenshot({ filePath: "qa-dashboard-loaded.png" })
```

**Report Template**:
```markdown
✅ **User Flow Tested: Registration → Dashboard**
- Form submission: ✅ Successful
- Success message: ✅ Displayed
- Redirect: ✅ Dashboard loaded
- Screenshots: qa-registration-success.png, qa-dashboard-loaded.png
```

**Time Savings**: 10 min → 2 min (80% faster)

---

#### Workflow 2: Cross-Browser Testing

**When to use**: Before production release

```typescript
// Test Mobile viewport
await mcp__chrome-devtools__resize_page({ width: 375, height: 667 })
await mcp__chrome-devtools__take_screenshot({ filePath: "qa-mobile.png" })
await mcp__chrome-devtools__list_console_messages({ types: ["error"] })

// Test Tablet viewport
await mcp__chrome-devtools__resize_page({ width: 768, height: 1024 })
await mcp__chrome-devtools__take_screenshot({ filePath: "qa-tablet.png" })

// Test Desktop viewport
await mcp__chrome-devtools__resize_page({ width: 1920, height: 1080 })
await mcp__chrome-devtools__take_screenshot({ filePath: "qa-desktop.png" })
```

**Report Template**:
```markdown
✅ **Cross-Browser Testing Complete**
- Mobile (375px): ✅ Layout responsive (qa-mobile.png)
- Tablet (768px): ✅ No overflow (qa-tablet.png)
- Desktop (1920px): ✅ Centered layout (qa-desktop.png)
- Console errors: 0 across all viewports
```

---

#### Workflow 3: Error State Testing

**When to use**: After implementing form validation or error handling

```typescript
// Test invalid input
await mcp__chrome-devtools__navigate_page({ url: "http://localhost:3000/signup", type: "url" })
await mcp__chrome-devtools__fill({ uid: "email", value: "invalid-email" })
await mcp__chrome-devtools__click({ uid: "submit-btn" })

// Verify error message
await mcp__chrome-devtools__take_snapshot()
// Check: Error message "Please enter a valid email" appears

await mcp__chrome-devtools__take_screenshot({ filePath: "qa-validation-error.png" })

// Test empty required fields
await mcp__chrome-devtools__fill({ uid: "email", value: "" })
await mcp__chrome-devtools__click({ uid: "submit-btn" })
await mcp__chrome-devtools__take_screenshot({ filePath: "qa-required-error.png" })
```

**Report Template**:
```markdown
✅ **Error State Testing Complete**
- Invalid email: ✅ Validation message shown
- Empty fields: ✅ "Required field" shown
- Error styling: ✅ Red border on invalid inputs
- Screenshots: qa-validation-error.png, qa-required-error.png
```

---

### Data Analysis Specialist MCP Workflows

**Primary Use Cases**: Dashboard visualization verification

#### Workflow 1: Dashboard Verification

**When to use**: After implementing charts or analytics dashboards

```typescript
// Navigate to analytics dashboard
await mcp__chrome-devtools__navigate_page({ url: "http://localhost:3000/analytics", type: "url" })

// Take screenshot of visualizations
await mcp__chrome-devtools__take_screenshot({ filePath: "data-dashboard-rendered.png" })

// Check console for chart rendering errors
await mcp__chrome-devtools__list_console_messages({ types: ["error"] })
// Expected: No errors (Recharts, Chart.js, D3 loaded correctly)

// Verify data loaded
await mcp__chrome-devtools__list_network_requests({ resourceTypes: ["fetch"] })
// Check: GET /api/analytics → 200 OK
```

**Report Template**:
```markdown
✅ **Analytics Dashboard Verified**
- Charts: All visualizations rendered ✅
- Data: API endpoints returning correct format ✅
- Performance: Dashboard loads in <2s ✅
- Screenshot: data-dashboard-rendered.png
```

---

## Common Patterns

### Pattern 1: Before/After Screenshot Documentation

**Use case**: Documenting bug fixes or feature implementations

```typescript
// BEFORE: Capture broken state
await mcp__chrome-devtools__navigate_page({ url: "http://localhost:3000", type: "url" })
await mcp__chrome-devtools__take_screenshot({ filePath: "bug-before-fix.png" })

// [Agent applies fix]

// AFTER: Capture fixed state
await mcp__chrome-devtools__navigate_page({ type: "reload", ignoreCache: true })
await mcp__chrome-devtools__take_screenshot({ filePath: "bug-after-fix.png" })

// Report
"Bug fixed: bug-before-fix.png shows overlapping text, bug-after-fix.png shows correct layout"
```

---

### Pattern 2: Multi-Page Testing

**Use case**: Testing navigation flows across multiple pages

```typescript
// Open multiple pages
await mcp__chrome-devtools__list_pages()
// [0] http://localhost:3000/

await mcp__chrome-devtools__new_page({ url: "http://localhost:3000/profile" })
// [0] http://localhost:3000/
// [1] http://localhost:3000/profile

await mcp__chrome-devtools__new_page({ url: "http://localhost:3000/settings" })
// [0] http://localhost:3000/
// [1] http://localhost:3000/profile
// [2] http://localhost:3000/settings

// Switch between pages
await mcp__chrome-devtools__select_page({ pageIdx: 1 })
await mcp__chrome-devtools__take_screenshot({ filePath: "profile-page.png" })

await mcp__chrome-devtools__select_page({ pageIdx: 2 })
await mcp__chrome-devtools__take_screenshot({ filePath: "settings-page.png" })

// Close unnecessary pages
await mcp__chrome-devtools__close_page({ pageIdx: 0 })
```

---

### Pattern 3: Network Failure Simulation

**Use case**: Testing offline behavior or API failure handling

```typescript
// Enable network throttling
await mcp__chrome-devtools__emulate({
  networkConditions: "Offline"
})

// Try to load page
await mcp__chrome-devtools__navigate_page({ url: "http://localhost:3000", type: "url" })

// Check error message
await mcp__chrome-devtools__take_screenshot({ filePath: "offline-error.png" })

// Disable throttling
await mcp__chrome-devtools__emulate({
  networkConditions: "No emulation"
})
```

---

### Pattern 4: Console Error Filtering

**Use case**: Focusing on critical errors, ignoring warnings

```typescript
// Get only errors (no warnings)
await mcp__chrome-devtools__list_console_messages({ types: ["error"] })

// Get errors + warnings
await mcp__chrome-devtools__list_console_messages({ types: ["error", "warn"] })

// Get all console output
await mcp__chrome-devtools__list_console_messages({ types: ["log", "debug", "info", "error", "warn"] })
```

---

### Pattern 5: Network Request Filtering

**Use case**: Debugging specific types of requests

```typescript
// Get only API calls
await mcp__chrome-devtools__list_network_requests({
  resourceTypes: ["fetch", "xhr"]
})

// Get only failed requests
const requests = await mcp__chrome-devtools__list_network_requests()
// Filter for status codes 4xx, 5xx in response

// Get only images
await mcp__chrome-devtools__list_network_requests({
  resourceTypes: ["image"]
})
```

---

### Pattern 6: Performance Regression Testing

**Use case**: Ensuring performance doesn't degrade

```typescript
// Baseline trace (before changes)
await mcp__chrome-devtools__performance_start_trace({ reload: true, autoStop: true })
// Record: LCP 1.8s, FID 45ms, CLS 0.05

// [Make changes]

// New trace (after changes)
await mcp__chrome-devtools__performance_start_trace({ reload: true, autoStop: true })
// Compare: LCP 2.3s (regressed!), FID 50ms, CLS 0.05

// Report: "Performance regression: LCP increased by 0.5s"
```

---

## Troubleshooting

### Issue 1: Screenshots Not Saving

**Symptoms**: Screenshot command succeeds but file not found

**Cause**: Incorrect file path or permissions

**Solution**:
```typescript
// ❌ Wrong: Relative path without context
await mcp__chrome-devtools__take_screenshot({ filePath: "screenshot.png" })

// ✅ Correct: Absolute path
await mcp__chrome-devtools__take_screenshot({
  filePath: "/Users/admin/Documents/claudecode/screenshots/screenshot.png"
})

// ✅ Also correct: Project-relative path
await mcp__chrome-devtools__take_screenshot({
  filePath: "./screenshots/screenshot.png"
})
```

---

### Issue 2: Element UID Not Found

**Symptoms**: `click()` or `fill()` fails with "element not found"

**Cause**: UID from snapshot is stale or incorrect

**Solution**:
```typescript
// Step 1: ALWAYS take fresh snapshot before interacting
await mcp__chrome-devtools__take_snapshot()

// Step 2: Read snapshot output to get correct UID
// Look for: button [uid="submit-button-123"]

// Step 3: Use correct UID
await mcp__chrome-devtools__click({ uid: "submit-button-123" })
```

---

### Issue 3: Console Messages Empty

**Symptoms**: `list_console_messages()` returns empty even though errors visible

**Cause**: Console cleared or messages filtered

**Solution**:
```typescript
// Include preserved messages (last 3 navigations)
await mcp__chrome-devtools__list_console_messages({
  types: ["error", "warn"],
  includePreservedMessages: true
})
```

---

### Issue 4: Network Requests Missing

**Symptoms**: API call made but not showing in network panel

**Cause**: Request completed before tool called, or wrong resource type

**Solution**:
```typescript
// Call BEFORE navigation to capture all requests
await mcp__chrome-devtools__list_network_requests({
  resourceTypes: ["fetch", "xhr", "document"],
  includePreservedRequests: true
})
```

---

### Issue 5: Performance Trace Fails

**Symptoms**: `performance_start_trace()` doesn't complete

**Cause**: `autoStop: false` requires manual stop

**Solution**:
```typescript
// ✅ Correct: Auto-stop enabled
await mcp__chrome-devtools__performance_start_trace({
  reload: true,
  autoStop: true  // ← Required for automatic completion
})

// ❌ Wrong: Auto-stop disabled (requires manual stop)
await mcp__chrome-devtools__performance_start_trace({
  reload: true,
  autoStop: false
})
await mcp__chrome-devtools__performance_stop_trace()  // Must call manually
```

---

### Issue 6: Page Not Loading

**Symptoms**: `navigate_page()` times out

**Cause**: Dev server not running or wrong port

**Solution**:
```bash
# Check if dev server running
lsof -ti:3000

# Start dev server if needed
npm run dev

# Verify correct port in URL
await mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3000",  # ← Correct port
  type: "url"
})
```

---

## Real-World Examples

### Example 1: Full Frontend Feature Implementation

**Scenario**: User requests "Add dark mode toggle to settings page"

**Agent Workflow with MCP**:

```typescript
// 1. Implement dark mode toggle component
// [Agent writes code]

// 2. Navigate to settings page
await mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3000/settings",
  type: "url"
})

// 3. Take "light mode" screenshot
await mcp__chrome-devtools__take_screenshot({ filePath: "darkmode-light.png" })

// 4. Click dark mode toggle
await mcp__chrome-devtools__take_snapshot()  // Get toggle UID
await mcp__chrome-devtools__click({ uid: "darkmode-toggle" })

// 5. Take "dark mode" screenshot
await mcp__chrome-devtools__take_screenshot({ filePath: "darkmode-dark.png" })

// 6. Test responsive (mobile, tablet, desktop)
await mcp__chrome-devtools__resize_page({ width: 375, height: 667 })
await mcp__chrome-devtools__take_screenshot({ filePath: "darkmode-mobile.png" })

// 7. Check console errors
await mcp__chrome-devtools__list_console_messages({ types: ["error"] })

// 8. Report
Agent: "✅ Dark mode implemented:
- Light mode: darkmode-light.png
- Dark mode: darkmode-dark.png
- Mobile responsive: darkmode-mobile.png
- Console: 0 errors
- LocalStorage persists preference ✅"
```

**User Benefit**: Feature verified in 1 minute vs 5 minutes manually

---

### Example 2: Backend API Debugging

**Scenario**: User reports "Login API returning 500 error"

**Agent Workflow with MCP**:

```typescript
// 1. Navigate to login page
await mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3000/login",
  type: "url"
})

// 2. Fill login form
await mcp__chrome-devtools__fill_form({
  elements: [
    { uid: "email", value: "test@example.com" },
    { uid: "password", value: "testpass123" }
  ]
})

// 3. Submit and monitor network
await mcp__chrome-devtools__click({ uid: "submit" })
await mcp__chrome-devtools__list_network_requests({ resourceTypes: ["fetch"] })

// Output shows: POST /api/auth/login → 500 Internal Server Error

// 4. Get request details
await mcp__chrome-devtools__get_network_request({ reqid: 123 })
// Response: { error: "Database connection failed" }

// 5. Check server console
await mcp__chrome-devtools__list_console_messages({ types: ["error"] })
// Error: "ECONNREFUSED 127.0.0.1:5432"

// 6. Take screenshot of error state
await mcp__chrome-devtools__take_screenshot({ filePath: "login-500-error.png" })

// 7. Diagnose
Agent: "❌ Database connection issue found:
- API: POST /api/auth/login → 500
- Root cause: PostgreSQL not running
- Fix: Start database with `docker-compose up -d`
- Screenshot: login-500-error.png"
```

**User Benefit**: Issue diagnosed in 2 minutes vs 10 minutes manually

---

### Example 3: Security Vulnerability Detection

**Scenario**: QA tester discovers XSS vulnerability

**Agent Workflow with MCP**:

```typescript
// 1. Navigate to vulnerable page
await mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3000/comments",
  type: "url"
})

// 2. Attempt XSS attack
await mcp__chrome-devtools__fill({
  uid: "comment-input",
  value: "<img src=x onerror=alert('XSS')>"
})

await mcp__chrome-devtools__click({ uid: "post-comment" })

// 3. Check if script executed
const result = await mcp__chrome-devtools__evaluate_script({
  function: `() => {
    return document.body.innerHTML.includes('<img src=x onerror=');
  }`
})
// Result: true (VULNERABILITY FOUND!)

// 4. Take screenshot of vulnerability
await mcp__chrome-devtools__take_screenshot({ filePath: "xss-vulnerability.png" })

// 5. Report
Agent: "🚨 **XSS VULNERABILITY DETECTED**
- Location: /comments
- Attack vector: <img> tag with onerror
- Impact: HIGH (malicious script can execute)
- Screenshot: xss-vulnerability.png
- Fix required: Sanitize user input with DOMPurify"

// 6. Apply fix
// [Agent implements DOMPurify]

// 7. Re-test
await mcp__chrome-devtools__navigate_page({ type: "reload", ignoreCache: true })
await mcp__chrome-devtools__fill({ uid: "comment-input", value: "<img src=x onerror=alert('XSS')>" })
await mcp__chrome-devtools__click({ uid: "post-comment" })

const fixed = await mcp__chrome-devtools__evaluate_script({
  function: `() => {
    return document.body.innerHTML.includes('<img src=x onerror=');
  }`
})
// Result: false (FIXED!)

await mcp__chrome-devtools__take_screenshot({ filePath: "xss-fixed.png" })

Agent: "✅ **XSS VULNERABILITY FIXED**
- Input sanitized: <img> tag removed
- Screenshot: xss-fixed.png"
```

**User Benefit**: Vulnerability found, fixed, and verified in 5 minutes vs 30 minutes manually

---

### Example 4: Performance Optimization

**Scenario**: User reports "Dashboard loads too slowly"

**Agent Workflow with MCP**:

```typescript
// 1. Baseline performance trace
await mcp__chrome-devtools__performance_start_trace({
  reload: true,
  autoStop: true
})

await mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3000/dashboard",
  type: "url"
})

// Performance results:
// LCP: 4.2s (target: <2.5s) ❌
// FID: 180ms (target: <100ms) ❌
// CLS: 0.15 (target: <0.1) ❌

// 2. Analyze insights
// Insight: "Large images blocking LCP"
// Insight: "Excessive JavaScript blocking main thread"

// 3. Apply optimizations
// - Lazy load images below fold
// - Code split heavy components
// - Use next/image for optimization

// 4. Re-test after optimizations
await mcp__chrome-devtools__performance_start_trace({
  reload: true,
  autoStop: true
})

// New results:
// LCP: 1.8s (improved 57%) ✅
// FID: 45ms (improved 75%) ✅
// CLS: 0.05 (improved 67%) ✅

// 5. Take screenshot
await mcp__chrome-devtools__take_screenshot({ filePath: "dashboard-optimized.png" })

// 6. Report
Agent: "✅ **Dashboard Performance Optimized**
- LCP: 4.2s → 1.8s (57% improvement)
- FID: 180ms → 45ms (75% improvement)
- CLS: 0.15 → 0.05 (67% improvement)
- All Core Web Vitals now passing ✅
- Screenshot: dashboard-optimized.png"
```

**User Benefit**: Performance issue diagnosed and fixed in 15 minutes vs 1 hour manually

---

## Summary: When to Use MCP

| Agent Type | MCP Usage | Frequency | Priority |
|-----------|-----------|-----------|----------|
| **Frontend Developer** | Responsive, accessibility, performance | ALWAYS | CRITICAL |
| **Backend Developer** | API testing, auth flows, error handling | ALWAYS | CRITICAL |
| **Security Specialist** | OWASP testing, XSS/CSRF/SQL injection | ALWAYS | CRITICAL |
| **DevOps Engineer** | Deployment verification, blue-green | ALWAYS | CRITICAL |
| **QA Tester** | User flows, cross-browser, error states | ALWAYS | CRITICAL |
| **Data Analysis** | Dashboard visualization | RECOMMENDED | MEDIUM |

---

**Key Takeaways**:

1. **MCP saves 40-80% time per task** through automated verification
2. **Screenshots provide visual proof** that reduces back-and-forth
3. **Console/network inspection catches issues early** before users report them
4. **Agents verify their own work** creating faster feedback loops
5. **Use MCP on EVERY user-facing change** for maximum efficiency

---

**Next Steps**:

- Read [AGENT-DEVELOPMENT-GUIDE.md](./AGENT-DEVELOPMENT-GUIDE.md) to create custom agents with MCP
- Read [SKILL-CREATION-GUIDE.md](./SKILL-CREATION-GUIDE.md) to add domain expertise
- Practice MCP workflows on your current project

---

**Last Updated**: 2025-11-24
**Version**: 1.0
**Feedback**: Report issues at https://github.com/anthropics/claude-code/issues
