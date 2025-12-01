# Skill Creation Guide

**Last Updated**: 2025-11-24
**Purpose**: How-to guide for creating custom Claude Code skills

---

## Table of Contents

1. [Understanding Skills](#understanding-skills)
2. [When to Create a Skill](#when-to-create-a-skill)
3. [Skill Structure](#skill-structure)
4. [Auto-Activation Keywords](#auto-activation-keywords)
5. [Writing Skill Content](#writing-skill-content)
6. [Testing Skill Activation](#testing-skill-activation)
7. [Examples](#examples)

---

## Understanding Skills

### What Are Skills?

**Skills** are portable, auto-activated domain expertise documents that Claude loads **just-in-time** when relevant to user requests. They provide deep knowledge without permanent conversation overhead.

### Skills vs Agents vs Commands

| Feature | Skills | Agents | Commands |
|---------|--------|--------|----------|
| **Activation** | Auto-detected by Claude | Explicit Task tool invocation | User types `/command` |
| **Purpose** | Portable domain expertise | Specialized execution contexts | User-triggered workflows |
| **Context** | Shares main conversation | Independent context window | Main conversation |
| **Token Cost** | Loaded on-demand (~1k tokens) | Full context (~2k tokens) | Inline execution (~500 tokens) |
| **Use Case** | Quick requests, repeated procedures | Complex workflows, multi-step tasks | Shortcuts, automation |
| **Example** | `frontend-design` auto-loads on "build UI" | `frontend-developer` via Task tool | `/superman` coordination |

### Key Benefits

✅ **On-Demand Loading**: Skills only use tokens when needed
✅ **Reusable Expertise**: Same skill works across projects
✅ **Auto-Activation**: Claude detects when to load skills
✅ **Composable**: Multiple skills can activate together
✅ **Portable**: Share skills across team

### How Skills Work with Agents

**Example Flow**: User: "Build a responsive dashboard with accessibility"

1. **Skill Auto-Activation**: `frontend-design`, `accessibility-wcag`, `performance-core-web-vitals` skills load
2. **Agent Invocation**: User explicitly calls `frontend-developer` agent (or via `/superman`)
3. **Synergy**: Agent uses skill knowledge + agent-specific MCP workflows
4. **Result**: Bold aesthetics (skill) + production engineering (agent) + automated testing (MCP)

**Key Insight**: Skills provide **what to do** (aesthetic direction, WCAG rules), agents provide **how to do it** (implementation, testing, verification).

---

## When to Create a Skill

### Decision Tree

```
Do you have specialized knowledge that's frequently needed?
│
├─ YES → Is this knowledge procedural or conceptual?
│         │
│         ├─ PROCEDURAL (step-by-step workflows) → Use agent or command
│         │
│         └─ CONCEPTUAL (domain expertise, patterns, best practices) → CREATE SKILL ✅
│
└─ NO → Don't create skill (use one-off responses)
```

### Good Reasons to Create a Skill

✅ **Domain Expertise** (patterns, frameworks, best practices)
- Example: `react-patterns` - React hooks, context, performance patterns
- Example: `aws-architecture` - AWS service patterns, cost optimization

✅ **Standards & Compliance** (rules, checklists, guidelines)
- Example: `accessibility-wcag` - WCAG 2.1 Level AA compliance
- Example: `gdpr-compliance` - GDPR requirements for data handling

✅ **Reference Material** (APIs, configurations, schemas)
- Example: `tailwind-utilities` - Tailwind CSS class reference
- Example: `postgresql-optimization` - Query optimization patterns

✅ **Industry Best Practices** (proven solutions, anti-patterns)
- Example: `security-audit` - OWASP Top 10, security headers
- Example: `performance-core-web-vitals` - Core Web Vitals optimization

### Bad Reasons to Create a Skill

❌ **Project-Specific Knowledge** → Document in project CLAUDE.md instead
- Example: "Our company's API endpoints" → Not a skill

❌ **Procedural Workflows** → Use agent or command instead
- Example: "Deploy to production" → `/deploy` command, not skill

❌ **One-Time Information** → Just provide in conversation
- Example: "How to install npm" → No skill needed

❌ **Too Broad** → Break into focused skills
- Example: "Everything about web development" → Too generic

---

## Skill Structure

### File Location

```bash
~/.claude/skills/skill-name/SKILL.md
```

**IMPORTANT**: Skill must be in a directory with `SKILL.md` filename (uppercase).

```
~/.claude/skills/
├── frontend-design/
│   └── SKILL.md                    ✅ Correct
├── backend-testing/
│   └── SKILL.md                    ✅ Correct
├── security-audit/
│   └── skill.md                    ❌ Wrong (lowercase)
└── my-skill.md                     ❌ Wrong (not in directory)
```

---

### Skill Document Structure

```markdown
# Skill Title

Brief 1-2 sentence description of what this skill provides.

---

## Core Concepts

### Concept 1
[Detailed explanation]

### Concept 2
[Detailed explanation]

---

## Patterns & Best Practices

### Pattern 1: [Name]
**When to use**: [Scenario]
**Implementation**:
```[language]
[Code example]
```
**Benefits**: [Why this pattern works]

### Pattern 2: [Name]
...

---

## Common Pitfalls

❌ **Anti-Pattern 1**: [Bad practice]
✅ **Solution**: [Good practice]

---

## Quick Reference

[Cheatsheet, table, or checklist for fast lookup]

---

## Real-World Examples

### Example 1: [Scenario]
[Complete implementation with code]

### Example 2: [Scenario]
[Complete implementation with code]
```

---

### Optimal Skill Size

| Size | Lines | Use Case |
|------|-------|----------|
| **Small** | 100-300 | Quick reference (API docs, cheatsheets) |
| **Medium** | 300-600 | Standard skill (patterns, best practices) |
| **Large** | 600-1000 | Comprehensive guide (frameworks, standards) |
| **Too Large** | 1000+ | Split into multiple skills |

**Token Estimate**: ~1 token per 4 characters
- 300 lines ≈ 5,000 chars ≈ 1,250 tokens
- 600 lines ≈ 10,000 chars ≈ 2,500 tokens
- 1000 lines ≈ 17,000 chars ≈ 4,250 tokens

**Recommendation**: Keep skills 300-600 lines for optimal balance.

---

## Auto-Activation Keywords

### How Auto-Activation Works

Claude Code automatically loads skills when user messages contain **trigger keywords**. Skills don't have explicit keyword declarations—Claude infers relevance from:

1. **Skill filename**: `backend-testing` → "backend test", "API test"
2. **Skill title**: "Accessibility WCAG" → "accessibility", "wcag", "a11y"
3. **Content**: Mentions of "OWASP" in security-audit skill → "owasp", "security audit"

### Keyword Best Practices

✅ **Use descriptive skill names**:
- `backend-testing` (good) → Triggers on "backend test", "API test"
- `testing` (bad) → Too generic, triggers on everything

✅ **Include keywords in title**:
- "Performance & Core Web Vitals" → Triggers on "performance", "core web vitals"
- "Speed Optimization" → Triggers on "speed", "optimization"

✅ **Mention key terms early**:
```markdown
# Accessibility WCAG

This skill covers WCAG 2.1 Level AA compliance, including ARIA patterns,
keyboard navigation, and screen reader support.
```
→ Triggers on: "accessibility", "wcag", "aria", "screen reader"

### Common Keyword Patterns

| Domain | Effective Keywords | Examples |
|--------|-------------------|----------|
| **Frontend** | "ui", "component", "responsive", "css" | `frontend-design` |
| **Backend** | "api", "backend", "server", "endpoint" | `backend-testing` |
| **Security** | "security", "auth", "owasp", "vulnerability" | `security-audit` |
| **Performance** | "performance", "optimization", "speed", "lcp" | `performance-core-web-vitals` |
| **Accessibility** | "accessibility", "a11y", "wcag", "aria" | `accessibility-wcag` |
| **Data** | "analytics", "metrics", "kpi", "data" | `data-analysis-metrics` |

---

## Writing Skill Content

### Principle 1: Start with Core Concepts

❌ **Bad** (jumps straight to examples):
```markdown
# React Patterns

Here's how to use useState:
```javascript
const [count, setCount] = useState(0);
```
```

✅ **Good** (establishes foundation first):
```markdown
# React Patterns

## Core Concepts

### State Management
React provides multiple state management approaches depending on complexity:
- **Local State**: Component-specific state (useState, useReducer)
- **Lifted State**: Shared state in parent component
- **Global State**: Application-wide state (Context, Redux)

### When to Use useState
Use useState for:
- Component-specific UI state (open/closed, selected item)
- Form inputs and validation
- Simple counters or toggles

**Implementation**:
```javascript
const [count, setCount] = useState(0);

// Update: Pass new value
setCount(count + 1);

// Update: Use function for prev state
setCount(prev => prev + 1);
```
```

**Why This Matters**: Foundation first → users understand WHY before HOW.

---

### Principle 2: Show Patterns, Not Just Syntax

❌ **Bad** (syntax reference only):
```markdown
## Array Methods

### map()
```javascript
array.map(item => item * 2)
```

### filter()
```javascript
array.filter(item => item > 5)
```
```

✅ **Good** (patterns with context):
```markdown
## Data Transformation Patterns

### Pattern 1: Transform Array of Objects
**Scenario**: Extract specific fields from API response

```javascript
// API returns: [{ id: 1, name: "Alice", email: "..." }, ...]
// Need: ["Alice", "Bob", "Charlie"]

const names = users.map(user => user.name);
```

**When to use**: Reshaping API data for display, CSV export, or processing

### Pattern 2: Filter + Transform (Chain)
**Scenario**: Get active users and format for dropdown

```javascript
const activeUserOptions = users
  .filter(user => user.status === 'active')
  .map(user => ({
    value: user.id,
    label: `${user.name} (${user.email})`
  }));
```

**When to use**: Building UI options, data pipelines, reporting
```

**Why This Matters**: Patterns show **when** and **why**, not just **how**.

---

### Principle 3: Include Anti-Patterns

❌ **Bad** (only positive examples):
```markdown
## Performance Optimization

Use React.memo to prevent unnecessary re-renders:
```javascript
const MyComponent = React.memo(({ data }) => {
  return <div>{data.name}</div>;
});
```
```

✅ **Good** (show what NOT to do):
```markdown
## Performance Optimization

### Using React.memo

❌ **Anti-Pattern**: Memoizing everything
```javascript
// DON'T: Memoizing cheap components adds overhead
const SimpleText = React.memo(({ text }) => <span>{text}</span>);
```
**Why bad**: React.memo has cost (shallow comparison), only worth it for expensive renders.

✅ **Good Pattern**: Memoize expensive components
```javascript
// DO: Memoize components with heavy rendering or expensive calculations
const DataTable = React.memo(({ rows }) => {
  const sortedRows = useMemo(() => rows.sort(...), [rows]);
  return <table>...</table>;
});
```
**When to use**: Component renders >50ms, re-renders frequently, or has complex children.

### Benchmarking
```javascript
// Measure render time
const start = performance.now();
// ... render ...
const duration = performance.now() - start;
console.log(`Render took ${duration}ms`);
```
**Rule of thumb**: If render <16ms (60 FPS), don't memoize.
```

**Why This Matters**: Learning what NOT to do is as important as what to do.

---

### Principle 4: Provide Quick Reference

❌ **Bad** (no quick lookup):
```markdown
[Long explanations only, no cheatsheet]
```

✅ **Good** (include reference table):
```markdown
## Quick Reference

### HTTP Status Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST (resource created) |
| 204 | No Content | Successful DELETE (no response body) |
| 400 | Bad Request | Validation failed |
| 401 | Unauthorized | Missing/invalid auth token |
| 403 | Forbidden | Authenticated but no permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource (email taken) |
| 422 | Unprocessable Entity | Valid syntax, semantic errors |
| 500 | Internal Server Error | Server-side exception |
| 503 | Service Unavailable | Server overloaded/down |

### Common Headers

| Header | Purpose | Example |
|--------|---------|---------|
| `Authorization` | Auth credentials | `Bearer <token>` |
| `Content-Type` | Request body format | `application/json` |
| `Accept` | Desired response format | `application/json` |
| `Cache-Control` | Caching behavior | `no-cache` |
```

**Why This Matters**: Cheatsheets enable fast lookup without re-reading entire skill.

---

### Principle 5: Use Real-World Examples

❌ **Bad** (toy examples):
```markdown
## useState Example

```javascript
const [count, setCount] = useState(0);
```
```

✅ **Good** (production-like examples):
```markdown
## Real-World Example: Form Validation

```typescript
interface FormState {
  email: string;
  password: string;
  errors: Record<string, string>;
}

function LoginForm() {
  const [form, setForm] = useState<FormState>({
    email: '',
    password: '',
    errors: {}
  });

  const validateEmail = (email: string): string | null => {
    if (!email) return 'Email is required';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return 'Invalid email format';
    }
    return null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const errors: Record<string, string> = {};
    const emailError = validateEmail(form.email);
    if (emailError) errors.email = emailError;

    if (form.password.length < 8) {
      errors.password = 'Password must be 8+ characters';
    }

    if (Object.keys(errors).length > 0) {
      setForm(prev => ({ ...prev, errors }));
      return;
    }

    // Submit to API
    await api.login({ email: form.email, password: form.password });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={form.email}
        onChange={e => setForm(prev => ({
          ...prev,
          email: e.target.value,
          errors: { ...prev.errors, email: '' }
        }))}
        aria-invalid={!!form.errors.email}
        aria-describedby="email-error"
      />
      {form.errors.email && (
        <span id="email-error" role="alert">{form.errors.email}</span>
      )}
      {/* ... password field ... */}
      <button type="submit">Login</button>
    </form>
  );
}
```

**Key Features Demonstrated**:
- TypeScript interfaces for type safety
- Validation with clear error messages
- Accessible error handling (ARIA attributes)
- API integration pattern
- Error clearing on input change
```

**Why This Matters**: Real examples show patterns in context, not isolation.

---

## Testing Skill Activation

### Manual Test Procedure

**Step 1: Create Test Message**

In Claude Code conversation, send message with trigger keywords:

```
User: "I need to implement accessibility features following WCAG guidelines"
```

**Step 2: Check if Skill Loaded**

Claude should demonstrate knowledge from skill:
- Mentions WCAG 2.1 Level AA requirements
- Provides ARIA patterns
- Shows color contrast ratios (4.5:1, 3:1)
- References keyboard navigation

**If skill NOT loaded**: Claude provides generic accessibility advice without WCAG specifics.

---

**Step 3: Verify Skill Content Used**

```
User: "What's the minimum color contrast ratio for normal text?"

Expected (skill loaded): "4.5:1 for normal text, 3:1 for large text (WCAG 2.1 Level AA)"
Generic (skill not loaded): "You should ensure good color contrast for readability"
```

---

### Testing Multiple Skills Together

**Test Scenario**: "Build a responsive dashboard with accessibility and performance optimization"

**Expected Skills Loaded**:
- `frontend-design` (aesthetics)
- `accessibility-wcag` (WCAG compliance)
- `performance-core-web-vitals` (LCP, FID, CLS)

**Verification**:
- Response mentions bold design patterns (frontend-design)
- Response includes ARIA patterns and color contrast (accessibility-wcag)
- Response optimizes images and lazy loading (performance-core-web-vitals)

---

### Debugging Skill Activation

**Issue 1: Skill Not Loading**

**Symptoms**: Claude doesn't demonstrate skill knowledge

**Possible Causes**:
1. Skill filename not `SKILL.md` (must be uppercase)
2. Skill not in `~/.claude/skills/skill-name/` directory
3. Trigger keywords too specific or not in user message
4. Skill file empty or malformed

**Debug Steps**:
```bash
# Check file location
ls -la ~/.claude/skills/

# Expected:
# frontend-design/SKILL.md
# backend-testing/SKILL.md
# security-audit/SKILL.md

# Check file contents
cat ~/.claude/skills/your-skill/SKILL.md

# Verify non-empty, valid markdown
```

---

**Issue 2: Wrong Skill Loading**

**Symptoms**: Claude loads unrelated skill

**Possible Causes**:
- Trigger keywords too generic
- Skill name ambiguous

**Solution**: Rename skill or adjust keywords

Example:
```
Bad: skills/testing/SKILL.md (too generic)
Good: skills/backend-testing/SKILL.md (specific domain)
```

---

**Issue 3: Multiple Skills Conflict**

**Symptoms**: Claude mixes advice from multiple skills incorrectly

**Possible Causes**:
- Skills overlap in domain
- Skills provide contradictory advice

**Solution**: Consolidate overlapping skills or clarify scope

Example:
```
Bad:
- skills/react-patterns/
- skills/frontend-patterns/ (overlap with React)

Good:
- skills/react-patterns/ (React-specific)
- skills/vue-patterns/ (Vue-specific)
- skills/frontend-design/ (Generic aesthetics)
```

---

## Examples

### Example 1: Backend Testing Skill

**File**: `~/.claude/skills/backend-testing/SKILL.md`

```markdown
# Backend Testing Skill

Comprehensive testing strategies for backend APIs, including TDD, integration testing, security testing, and performance testing.

---

## Testing Pyramid

```
     /\
    /  \ E2E Tests (10%)
   /____\
  /      \ Integration Tests (30%)
 /________\
/__________\ Unit Tests (60%)
```

**Unit Tests (60%)**: Fast, isolated tests for individual functions/classes
**Integration Tests (30%)**: Test multiple components together (API + database)
**E2E Tests (10%)**: Full user workflows across entire system

---

## TDD Workflow (Red-Green-Refactor)

### 1. RED: Write Failing Test First

```typescript
// tests/api/users.test.ts
describe('POST /api/users', () => {
  it('should create new user with valid data', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'test@example.com',
        password: 'SecurePass123!',
        name: 'Test User'
      });

    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('id');
    expect(response.body.email).toBe('test@example.com');
  });
});

// Run: npm test → FAILS (endpoint doesn't exist yet)
```

### 2. GREEN: Implement Minimum Code to Pass

```typescript
// src/routes/users.ts
app.post('/api/users', async (req, res) => {
  const { email, password, name } = req.body;
  const user = await db.users.create({ email, password, name });
  res.status(201).json({ id: user.id, email: user.email });
});

// Run: npm test → PASSES
```

### 3. REFACTOR: Improve Code Quality

```typescript
// src/routes/users.ts (refactored)
app.post('/api/users', validateRequest(userSchema), async (req, res) => {
  const { email, password, name } = req.body;

  // Hash password
  const hashedPassword = await bcrypt.hash(password, 10);

  // Create user
  const user = await db.users.create({
    email,
    password: hashedPassword,
    name
  });

  // Don't return password
  res.status(201).json({
    id: user.id,
    email: user.email,
    name: user.name
  });
});

// Run: npm test → STILL PASSES (refactored safely)
```

---

## API Testing Checklist

### For Every Endpoint, Test:

✅ **Success Cases**:
- Valid request → 200 OK (GET, PUT, PATCH, DELETE)
- Valid request → 201 Created (POST)
- No content → 204 No Content (DELETE)

✅ **Client Errors** (4xx):
- Missing required fields → 400 Bad Request
- Invalid format → 400 Bad Request
- Missing auth token → 401 Unauthorized
- Valid token, no permission → 403 Forbidden
- Resource not found → 404 Not Found
- Duplicate resource → 409 Conflict
- Validation failed → 422 Unprocessable Entity

✅ **Server Errors** (5xx):
- Database connection failed → 500 Internal Server Error
- Mock server exception → 500
- Service unavailable → 503

✅ **Edge Cases**:
- Empty strings
- Very long strings (>255 chars)
- Special characters (<, >, &, ", ')
- SQL injection attempts
- XSS attempts
- Boundary values (0, -1, MAX_INT)

---

## Integration Testing Pattern

```typescript
// tests/integration/auth-flow.test.ts
describe('Complete Authentication Flow', () => {
  let server: Server;
  let db: Database;

  beforeAll(async () => {
    // Start test server
    server = await startServer();

    // Connect to test database
    db = await connectTestDB();
  });

  afterAll(async () => {
    // Cleanup
    await db.close();
    await server.close();
  });

  beforeEach(async () => {
    // Reset database for each test
    await db.users.deleteAll();
  });

  it('should signup, login, and access protected route', async () => {
    // 1. Signup
    const signupRes = await request(server)
      .post('/api/auth/signup')
      .send({
        email: 'test@example.com',
        password: 'SecurePass123!'
      });

    expect(signupRes.status).toBe(201);
    const userId = signupRes.body.userId;

    // 2. Login
    const loginRes = await request(server)
      .post('/api/auth/login')
      .send({
        email: 'test@example.com',
        password: 'SecurePass123!'
      });

    expect(loginRes.status).toBe(200);
    const token = loginRes.body.token;

    // 3. Access protected route
    const profileRes = await request(server)
      .get('/api/users/me')
      .set('Authorization', `Bearer ${token}`);

    expect(profileRes.status).toBe(200);
    expect(profileRes.body.id).toBe(userId);
  });
});
```

---

## Security Testing

### SQL Injection Test

```typescript
it('should prevent SQL injection in search', async () => {
  // Attempt SQL injection
  const response = await request(app)
    .get('/api/users/search')
    .query({ q: "'; DROP TABLE users; --" });

  // Should return empty results, NOT execute SQL
  expect(response.status).toBe(200);
  expect(response.body).toEqual([]);

  // Verify users table still exists
  const users = await db.users.findAll();
  expect(users).toBeDefined(); // Table not dropped
});
```

### XSS Prevention Test

```typescript
it('should sanitize XSS in user bio', async () => {
  const response = await request(app)
    .post('/api/users')
    .send({
      email: 'test@example.com',
      bio: '<script>alert("XSS")</script>'
    });

  expect(response.status).toBe(201);
  expect(response.body.bio).not.toContain('<script>');
  expect(response.body.bio).toBe('alert("XSS")'); // Script tags stripped
});
```

---

## Performance Testing

### Load Testing with K6

```javascript
// k6-load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 50 },  // Ramp up to 50 users
    { duration: '1m', target: 50 },   // Stay at 50 users
    { duration: '30s', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests <500ms
    http_req_failed: ['rate<0.01'],   // <1% failure rate
  },
};

export default function () {
  const res = http.get('http://localhost:3000/api/users');

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}

// Run: k6 run k6-load-test.js
```

---

## Quick Reference

### HTTP Status Codes

| Code | Use Case |
|------|----------|
| 200 | Successful GET, PUT, PATCH |
| 201 | Resource created (POST) |
| 204 | Successful DELETE (no body) |
| 400 | Invalid request format/validation |
| 401 | Missing/invalid auth |
| 403 | Authenticated but no permission |
| 404 | Resource not found |
| 409 | Duplicate resource |
| 422 | Semantic validation failed |
| 500 | Server error |

### Test Coverage Goals

- Unit tests: 80%+ coverage
- Integration tests: Critical paths covered
- E2E tests: Main user flows covered

---

**Last Updated**: 2025-11-24
```

**Trigger Keywords**: "backend test", "api test", "integration test", "tdd", "unit test"

---

### Example 2: Accessibility WCAG Skill

**File**: `~/.claude/skills/accessibility-wcag/SKILL.md`

```markdown
# Accessibility WCAG Skill

WCAG 2.1 Level AA compliance guidelines, including ARIA patterns, keyboard navigation, color contrast, and screen reader support.

---

## WCAG 2.1 Principles (POUR)

### 1. Perceivable
Information must be presentable to users in ways they can perceive.

**Text Alternatives**:
```html
<!-- Images -->
<img src="logo.png" alt="Company Logo">

<!-- Decorative images -->
<img src="pattern.png" alt="" role="presentation">

<!-- Complex images -->
<img src="chart.png" alt="Sales chart" aria-describedby="chart-desc">
<div id="chart-desc">Q4 sales increased 23% from $4.2M to $5.2M</div>
```

**Semantic HTML**:
```html
<!-- Use semantic elements -->
<nav>...</nav>
<main>...</main>
<header>...</header>
<footer>...</footer>
<article>...</article>
<section>...</section>

<!-- NOT generic divs -->
<div class="nav">...</div> ❌
```

---

### 2. Operable
UI components must be operable.

**Keyboard Navigation**:
```html
<!-- All interactive elements must be keyboard accessible -->
<button onclick="handleClick()">Click Me</button> ✅
<div onclick="handleClick()">Click Me</div> ❌

<!-- Custom interactive elements need tabindex -->
<div role="button" tabindex="0" onclick="handleClick()">
  Click Me
</div> ✅
```

**Focus Indicators**:
```css
/* Always show focus indicator */
button:focus {
  outline: 2px solid blue;
  outline-offset: 2px;
}

/* NEVER remove outline without replacement */
button:focus {
  outline: none; ❌
}
```

---

### 3. Understandable
Information must be understandable.

**Form Labels**:
```html
<!-- Always associate labels -->
<label for="email">Email</label>
<input type="email" id="email" name="email"> ✅

<!-- Placeholder is NOT a label -->
<input type="email" placeholder="Email"> ❌

<!-- Error messages -->
<input
  type="email"
  id="email"
  aria-invalid="true"
  aria-describedby="email-error"
>
<span id="email-error" role="alert">
  Please enter a valid email address
</span>
```

---

### 4. Robust
Content must be robust enough for assistive technologies.

**Valid HTML**:
```html
<!-- Valid ARIA -->
<button aria-label="Close dialog">×</button> ✅

<!-- Invalid ARIA -->
<button aria-label="">×</button> ❌
<div aria-label="Click">...</div> ❌ (aria-label on non-interactive)
```

---

## Color Contrast Requirements

### WCAG 2.1 Level AA

| Content Type | Contrast Ratio | Example |
|--------------|----------------|---------|
| Normal text (<18.66px) | 4.5:1 minimum | #767676 on #FFFFFF |
| Large text (≥18.66px or bold ≥14px) | 3:1 minimum | #949494 on #FFFFFF |
| UI components (buttons, inputs) | 3:1 minimum | Border #949494 on #FFFFFF |
| Graphics (icons, charts) | 3:1 minimum | Icon #949494 on #FFFFFF |

**Tools**:
- Chrome DevTools: Inspect → Accessibility panel
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- Figma: Plugins → Stark

---

## ARIA Patterns

### Button

```html
<button type="button" aria-label="Close dialog">
  ×
</button>

<!-- Icon-only button -->
<button aria-label="Search">
  <svg aria-hidden="true">...</svg>
</button>
```

---

### Modal Dialog

```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-desc"
>
  <h2 id="dialog-title">Confirm Delete</h2>
  <p id="dialog-desc">Are you sure you want to delete this item?</p>

  <button>Cancel</button>
  <button>Delete</button>
</div>

<!-- Focus trap: Prevent focus leaving dialog -->
<script>
const dialog = document.querySelector('[role="dialog"]');
const focusableElements = dialog.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
const firstElement = focusableElements[0];
const lastElement = focusableElements[focusableElements.length - 1];

dialog.addEventListener('keydown', (e) => {
  if (e.key === 'Tab') {
    if (e.shiftKey && document.activeElement === firstElement) {
      e.preventDefault();
      lastElement.focus();
    } else if (!e.shiftKey && document.activeElement === lastElement) {
      e.preventDefault();
      firstElement.focus();
    }
  }
});
</script>
```

---

### Accordion

```html
<div class="accordion">
  <button
    aria-expanded="false"
    aria-controls="section1"
    id="button1"
  >
    Section 1
  </button>
  <div id="section1" role="region" aria-labelledby="button1" hidden>
    Content for section 1
  </div>
</div>

<script>
button.addEventListener('click', () => {
  const expanded = button.getAttribute('aria-expanded') === 'true';
  button.setAttribute('aria-expanded', !expanded);
  panel.hidden = expanded;
});
</script>
```

---

## Quick Reference

### Common ARIA Attributes

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `aria-label` | Accessible name | `<button aria-label="Close">×</button>` |
| `aria-labelledby` | References label element | `<input aria-labelledby="label-id">` |
| `aria-describedby` | Additional description | `<input aria-describedby="help-text">` |
| `aria-expanded` | Expandable state | `<button aria-expanded="false">` |
| `aria-hidden` | Hide from screen readers | `<svg aria-hidden="true">` |
| `aria-live` | Live region updates | `<div aria-live="polite">` |
| `aria-invalid` | Validation state | `<input aria-invalid="true">` |

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Tab | Move focus forward |
| Shift + Tab | Move focus backward |
| Enter / Space | Activate button/link |
| Esc | Close modal/dialog |
| Arrow keys | Navigate within components |

---

**Last Updated**: 2025-11-24
```

**Trigger Keywords**: "accessibility", "wcag", "a11y", "aria", "screen reader"

---

## Best Practices Summary

### DO:
✅ Create skills for **conceptual expertise** (patterns, standards, best practices)
✅ Keep skills **focused** (300-600 lines ideal)
✅ Include **anti-patterns** (what NOT to do)
✅ Provide **quick reference** (cheatsheets, tables)
✅ Show **real-world examples** (production-like code)
✅ Use **descriptive filenames** for auto-activation
✅ Structure with **clear sections** (concepts, patterns, reference, examples)

### DON'T:
❌ Create skills for **procedural workflows** (use agents/commands)
❌ Make skills **too broad** (split into focused skills)
❌ Write **toy examples** (show production patterns)
❌ Forget **SKILL.md filename** (must be uppercase)
❌ Use **lowercase skill.md** (won't load)
❌ Create **project-specific skills** (use project CLAUDE.md)

---

## Quick Reference Card

```markdown
# Skill Template

Brief description

---

## Core Concepts

### Concept 1
[Explanation]

---

## Patterns & Best Practices

### Pattern 1: [Name]
**When to use**: [Scenario]
**Implementation**:
```[language]
[Code]
```

❌ **Anti-Pattern**: [Bad practice]
✅ **Good Pattern**: [Good practice]

---

## Quick Reference

[Cheatsheet table]

---

## Real-World Examples

### Example 1: [Scenario]
[Production code]
```

**File Location**: `~/.claude/skills/skill-name/SKILL.md`

---

## Next Steps

1. **Identify Domain**: Choose focused expertise area
2. **Plan Structure**: Core concepts → Patterns → Reference → Examples
3. **Write Content**: Follow template, include anti-patterns
4. **Test Activation**: Use trigger keywords in conversation
5. **Iterate**: Refine based on usage

---

**Related Guides**:
- [AGENT-DEVELOPMENT-GUIDE.md](./AGENT-DEVELOPMENT-GUIDE.md) - Creating agents that use skills
- [MCP-WORKFLOWS-GUIDE.md](./MCP-WORKFLOWS-GUIDE.md) - Adding MCP verification to agents

---

**Last Updated**: 2025-11-24
**Version**: 1.0
**Feedback**: Report issues at https://github.com/anthropics/claude-code/issues
