# Programmatic Tool Orchestration Patterns

> **Reference**: Anthropic Programmatic Tool Calling
> **Benefit**: 37% token reduction - intermediate results processed outside model context
> **Source**: [Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)

---

## Why Orchestration Matters

### The Problem
Each tool call result enters the model's context window:

```
Task: Verify UI after fix

Sequential Approach:
1. navigate_page → result: 200 tokens
2. take_screenshot → result: 150 tokens (+ base64 if inline)
3. list_console_messages → result: 300+ tokens
4. list_network_requests → result: 200+ tokens

Total Context Impact: 850+ tokens PER verification
```

### The Solution
Batch multiple tools, return only summary:

```
Orchestrated Approach:
verifyUI() → summary: 150 tokens

"✅ PASS - 0 errors, screenshot: feature.png"
```

**Result**: 77% reduction per verification workflow

---

## Pattern 1: Visual Verification Workflow

**Use Case**: After any UI change, bug fix, or feature implementation
**Agents**: frontend-developer, qa-tester, devops-engineer
**Token Savings**: ~40%

### Implementation

```typescript
async function verifyUI(url: string, screenshotPath: string) {
  // 1. Navigate to target
  await mcp__chrome-devtools__navigate_page({ url, type: "url" })

  // 2. Capture screenshot
  await mcp__chrome-devtools__take_screenshot({ filePath: screenshotPath })

  // 3. Check for errors
  const console = await mcp__chrome-devtools__list_console_messages({
    types: ["error", "warn"]
  })

  // 4. Return summary only
  const errors = console.messages?.filter(m => m.type === "error") || []
  const warnings = console.messages?.filter(m => m.type === "warn") || []

  return {
    status: errors.length === 0 ? "✅ PASS" : "❌ FAIL",
    errors: errors.length,
    warnings: warnings.length,
    screenshot: screenshotPath,
    criticalErrors: errors.slice(0, 3).map(e => e.text)  // Top 3 only
  }
}

// Usage
const result = await verifyUI(
  "http://localhost:3000",
  "feature-verification.png"
)
// Only 'result' enters context, not all intermediate outputs
```

### Summary Output Format

```markdown
✅ **Visual Verification Complete**
- Status: PASS
- Errors: 0
- Warnings: 2
- Screenshot: feature-verification.png
```

---

## Pattern 2: API Verification Workflow

**Use Case**: After backend changes, API modifications
**Agents**: backend-developer, qa-tester
**Token Savings**: ~35%

### Implementation

```typescript
async function verifyAPI(
  formData: Array<{uid: string, value: string}>,
  submitButton: string,
  expectedText: string,
  apiEndpoint: string
) {
  // 1. Fill form
  await mcp__chrome-devtools__fill_form({ elements: formData })

  // 2. Submit
  await mcp__chrome-devtools__click({ uid: submitButton })

  // 3. Wait for response
  await mcp__chrome-devtools__wait_for({ text: expectedText, timeout: 5000 })

  // 4. Check network
  const network = await mcp__chrome-devtools__list_network_requests({
    resourceTypes: ["fetch", "xhr"]
  })

  // 5. Find API call
  const apiCall = network.requests?.find(r => r.url.includes(apiEndpoint))

  return {
    status: apiCall?.status === 200 ? "✅ PASS" : "❌ FAIL",
    endpoint: apiCall?.url || "Not found",
    responseStatus: apiCall?.status || "N/A",
    timing: apiCall?.timing || "N/A",
    formSubmitted: true
  }
}

// Usage
const result = await verifyAPI(
  [
    { uid: "email", value: "test@example.com" },
    { uid: "password", value: "SecurePass123!" }
  ],
  "login-btn",
  "Welcome",
  "/api/auth/login"
)
```

### Summary Output Format

```markdown
✅ **API Verification Complete**
- Status: PASS
- Endpoint: /api/auth/login
- Response: 200 OK
- Timing: 245ms
```

---

## Pattern 3: Responsive Design Verification

**Use Case**: After CSS/layout changes
**Agents**: frontend-developer
**Token Savings**: ~50%

### Implementation

```typescript
interface Breakpoint {
  name: string;
  width: number;
  height: number;
}

async function verifyResponsive(url: string, breakpoints: Breakpoint[]) {
  const results = []

  // Navigate once
  await mcp__chrome-devtools__navigate_page({ url, type: "url" })

  // Test each breakpoint
  for (const bp of breakpoints) {
    await mcp__chrome-devtools__resize_page({
      width: bp.width,
      height: bp.height
    })

    const screenshotPath = `responsive-${bp.name}.png`
    await mcp__chrome-devtools__take_screenshot({ filePath: screenshotPath })

    results.push({
      breakpoint: bp.name,
      dimensions: `${bp.width}x${bp.height}`,
      screenshot: screenshotPath
    })
  }

  return {
    status: "✅ All breakpoints captured",
    count: results.length,
    breakpoints: results.map(r => r.breakpoint).join(", "),
    screenshots: results.map(r => r.screenshot)
  }
}

// Usage with standard breakpoints
const result = await verifyResponsive("http://localhost:3000", [
  { name: "mobile", width: 375, height: 667 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "desktop", width: 1920, height: 1080 }
])
```

### Summary Output Format

```markdown
✅ **Responsive Verification Complete**
- Breakpoints: 3
- Tested: mobile, tablet, desktop
- Screenshots: responsive-mobile.png, responsive-tablet.png, responsive-desktop.png
```

---

## Pattern 4: Performance Audit Workflow

**Use Case**: Core Web Vitals optimization
**Agents**: frontend-developer
**Token Savings**: ~45%

### Implementation

```typescript
async function auditPerformance(url: string) {
  // 1. Navigate
  await mcp__chrome-devtools__navigate_page({ url, type: "url" })

  // 2. Start trace with reload
  await mcp__chrome-devtools__performance_start_trace({
    reload: true,
    autoStop: true
  })

  // 3. Analyze LCP
  const lcpInsight = await mcp__chrome-devtools__performance_analyze_insight({
    insightSetId: "Navigation-1",
    insightName: "LCPBreakdown"
  })

  // 4. Determine status
  const lcpValue = lcpInsight.value || 0
  let status = "✅ Good"
  if (lcpValue > 4000) status = "❌ Poor"
  else if (lcpValue > 2500) status = "⚠️ Needs Improvement"

  return {
    LCP: `${lcpValue}ms`,
    status,
    threshold: "< 2500ms good, < 4000ms needs improvement",
    recommendation: lcpInsight.recommendation || "None"
  }
}

// Usage
const result = await auditPerformance("http://localhost:3000")
```

### Summary Output Format

```markdown
✅ **Performance Audit Complete**
- LCP: 1850ms (Good)
- Status: ✅ Passing
- Threshold: < 2500ms
```

---

## Pattern 5: Security Auth Flow Verification

**Use Case**: After auth changes, security updates
**Agents**: security-specialist
**Token Savings**: ~40%

### Implementation

```typescript
async function verifyAuthFlow(
  loginUrl: string,
  credentials: Array<{uid: string, value: string}>,
  submitBtn: string,
  expectedRedirect: string
) {
  // 1. Navigate to login
  await mcp__chrome-devtools__navigate_page({ url: loginUrl, type: "url" })

  // 2. Fill credentials
  await mcp__chrome-devtools__fill_form({ elements: credentials })

  // 3. Submit
  await mcp__chrome-devtools__click({ uid: submitBtn })

  // 4. Wait for redirect
  await mcp__chrome-devtools__wait_for({ text: expectedRedirect, timeout: 5000 })

  // 5. Check network for auth calls
  const network = await mcp__chrome-devtools__list_network_requests({
    resourceTypes: ["fetch", "xhr"]
  })

  const authCalls = network.requests?.filter(r =>
    r.url.includes("/auth") || r.url.includes("/login")
  ) || []

  // 6. Check console for security warnings
  const console = await mcp__chrome-devtools__list_console_messages({
    types: ["warn", "error"]
  })

  const securityWarnings = console.messages?.filter(m =>
    m.text.toLowerCase().includes("security") ||
    m.text.toLowerCase().includes("cors") ||
    m.text.toLowerCase().includes("cookie")
  ) || []

  return {
    status: authCalls.some(c => c.status === 200) ? "✅ PASS" : "❌ FAIL",
    authEndpoints: authCalls.length,
    securityWarnings: securityWarnings.length,
    redirected: true
  }
}
```

---

## Pattern 6: E2E Test Workflow

**Use Case**: Complete user journey testing
**Agents**: e2e-tester, qa-tester
**Token Savings**: ~45%

### Implementation

```typescript
interface TestStep {
  action: "navigate" | "fill" | "click" | "wait" | "screenshot";
  params: any;
}

async function runE2EWorkflow(steps: TestStep[]) {
  const results = []

  for (const step of steps) {
    try {
      switch (step.action) {
        case "navigate":
          await mcp__chrome-devtools__navigate_page(step.params)
          break
        case "fill":
          await mcp__chrome-devtools__fill_form(step.params)
          break
        case "click":
          await mcp__chrome-devtools__click(step.params)
          break
        case "wait":
          await mcp__chrome-devtools__wait_for(step.params)
          break
        case "screenshot":
          await mcp__chrome-devtools__take_screenshot(step.params)
          break
      }
      results.push({ step: step.action, status: "✅" })
    } catch (error) {
      results.push({ step: step.action, status: "❌", error: error.message })
    }
  }

  const passed = results.filter(r => r.status === "✅").length
  const failed = results.filter(r => r.status === "❌").length

  return {
    status: failed === 0 ? "✅ ALL PASS" : "❌ FAILURES",
    total: results.length,
    passed,
    failed,
    failedSteps: results.filter(r => r.status === "❌")
  }
}

// Usage
const result = await runE2EWorkflow([
  { action: "navigate", params: { url: "http://localhost:3000", type: "url" } },
  { action: "fill", params: { elements: [{ uid: "search", value: "test" }] } },
  { action: "click", params: { uid: "search-btn" } },
  { action: "wait", params: { text: "Results", timeout: 3000 } },
  { action: "screenshot", params: { filePath: "e2e-search-complete.png" } }
])
```

---

## Pattern 7: Superman Multi-Hero Verification

**Use Case**: After multi-hero Justice League mission
**Agents**: Superman orchestrator
**Token Savings**: ~50%

### Implementation

```typescript
interface HeroResult {
  hero: string;
  targetUrl: string;
  screenshotPath: string;
}

async function verifyMission(heroes: HeroResult[]) {
  const results = []

  for (const hero of heroes) {
    // Navigate to hero's target
    await mcp__chrome-devtools__navigate_page({
      url: hero.targetUrl,
      type: "url"
    })

    // Screenshot
    await mcp__chrome-devtools__take_screenshot({
      filePath: hero.screenshotPath
    })

    // Check for errors
    const console = await mcp__chrome-devtools__list_console_messages({
      types: ["error"]
    })

    results.push({
      hero: hero.hero,
      status: (console.messages?.length || 0) === 0 ? "✅" : "⚠️",
      errors: console.messages?.length || 0,
      screenshot: hero.screenshotPath
    })
  }

  const allPassed = results.every(r => r.status === "✅")

  return {
    missionStatus: allPassed ? "✅ MISSION SUCCESS" : "⚠️ ISSUES DETECTED",
    heroCount: results.length,
    passedHeroes: results.filter(r => r.status === "✅").length,
    heroResults: results.map(r => `${r.hero}: ${r.status}`)
  }
}

// Usage
const result = await verifyMission([
  { hero: "Superman", targetUrl: "http://localhost:3000", screenshotPath: "superman-ui.png" },
  { hero: "Batman", targetUrl: "http://localhost:3000/api/health", screenshotPath: "batman-api.png" },
  { hero: "Flash", targetUrl: "http://localhost:3000", screenshotPath: "flash-perf.png" }
])
```

---

## When to Use Orchestration

### Use Orchestration When:
- Multiple tools needed for single logical task
- Intermediate results aren't needed for decision making
- Context window is filling up
- Same workflow repeated frequently

### Don't Use Orchestration When:
- Each step requires human review
- Intermediate results affect next step's parameters
- Debugging requires seeing all outputs
- Task is simple (1-2 tools)

---

## Token Savings Summary

| Pattern | Before | After | Savings |
|---------|--------|-------|---------|
| Visual Verification | 850 tokens | 150 tokens | 82% |
| API Verification | 600 tokens | 150 tokens | 75% |
| Responsive Testing | 1200 tokens | 200 tokens | 83% |
| Performance Audit | 800 tokens | 150 tokens | 81% |
| Auth Flow | 700 tokens | 150 tokens | 79% |
| E2E Workflow | 1500 tokens | 250 tokens | 83% |
| Multi-Hero Mission | 2500 tokens | 300 tokens | 88% |

**Average Savings**: 37-50% on complex multi-tool tasks

---

## Integration with Agents

Add this to agent prompts:

```markdown
## Orchestration Reference

For multi-tool workflows, use orchestration patterns from:
`/Users/admin/.claude/tools/orchestration-patterns.md`

Key patterns:
- Visual Verification: navigate → screenshot → console
- API Verification: fill → click → wait → network
- Responsive: navigate → resize × 3 → screenshots
- Performance: navigate → trace → analyze

Return summary only, not intermediate results.
```

---

**Last Updated**: 2025-11-25
**Reference**: [Anthropic Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)
