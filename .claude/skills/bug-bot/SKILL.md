---
name: bug-bot
description: Automatic bug detection and code analysis. Scans for logic errors, type issues, null risks, and framework anti-patterns. Auto-activates after code edits or invoke manually.
triggers:
  - find bugs
  - bug check
  - scan for bugs
  - debug this
  - code review
  - any issues
  - bug-bot
  - check for errors
  - what's wrong
---

# Bug-Bot: Automatic Code Bug Detection

**Role**: Proactive bug hunter that catches issues before they reach production
**Philosophy**: Like Cursor's BugBot - analyze code changes, detect bugs, suggest fixes

## Auto-Activation

Bug-Bot activates automatically when:
1. **After code edits**: Scan changed files for introduced bugs
2. **Manual trigger**: User invokes with trigger keywords
3. **Pre-commit check**: Optional integration with git hooks

## Scope Configuration

| Mode | Command | What's Scanned |
|------|---------|----------------|
| **Default** | `/bug-bot` or trigger keywords | Changed files only (fast) |
| **Full scan** | `/bug-bot --full` | Entire codebase (thorough) |
| **Targeted** | `/bug-bot src/lib/` | Specific directory |

## Bug Categories

### Priority 1: Critical Bugs

#### Logic Errors
- Off-by-one errors (`i < array.length - 1` vs `i < array.length`)
- Wrong boolean conditions (`&&` vs `||`)
- Unreachable code paths
- Infinite loops potential
- Missing break statements in switch

#### Type Safety Issues
- Implicit `any` types
- Missing null/undefined checks
- Type coercion bugs (`==` vs `===`)
- Incorrect generic constraints
- Union type narrowing failures

#### Runtime Risks
- Property access on potentially undefined objects
- Array index out of bounds
- Division by zero potential
- Async/await without try-catch
- Race conditions in state updates
- Memory leaks (event listeners, subscriptions)

### Priority 2: Framework-Specific (React/Next.js)

#### React Anti-Patterns
- Hooks called conditionally
- Hooks called in loops
- Missing dependency arrays
- Stale closures in useEffect
- Direct state mutation
- Missing keys in lists

#### Next.js Issues
- Server/client component mismatches
- `use client` directive missing
- Hydration mismatches
- Invalid `getServerSideProps` patterns
- Route segment config errors
- Metadata export issues

### Priority 3: Code Quality

#### Code Smells
- Dead code (unreachable, unused)
- Duplicate code blocks
- Overly complex functions (cyclomatic complexity)
- Magic numbers without constants
- Long parameter lists

#### Security Quick-Check
*(Defer complex issues to Martian Manhunter)*
- Obvious XSS vulnerabilities
- SQL injection patterns
- Hardcoded secrets
- Unsafe `dangerouslySetInnerHTML`

## Analysis Methodology

### Step 1: Identify Changed Files
```bash
# For default mode, scan git diff
git diff --name-only HEAD~1
git diff --staged --name-only
```

### Step 2: Parse and Analyze
For each file:
1. **Read full file content**
2. **Identify code patterns** using regex and AST-like analysis
3. **Check against bug signatures** for each category
4. **Track variable flow** for null/undefined propagation
5. **Validate framework rules** (React hooks, Next.js patterns)

### Step 3: Generate Report
Output structured findings with:
- Severity level
- File path and line number
- Issue description
- Suggested fix
- Code snippet showing the problem

## Output Format

```markdown
## Bug-Bot Analysis Report

### Summary
| Severity | Count |
|----------|-------|
| Critical | X |
| Warning | X |
| Info | X |

---

### Critical Issues

#### 1. [LOGIC] Off-by-one error
**File**: `src/lib/utils.ts:42`
**Issue**: Loop iterates one element short
```typescript
// Current (buggy)
for (let i = 0; i < array.length - 1; i++) { ... }

// Should be
for (let i = 0; i < array.length; i++) { ... }
```
**Fix**: Remove `- 1` from loop condition

---

#### 2. [NULL] Unsafe property access
**File**: `src/hooks/useData.ts:18`
**Issue**: `data.items` accessed without null check
```typescript
// Current (buggy)
return data.items.map(item => item.name);

// Should be
return data?.items?.map(item => item.name) ?? [];
```
**Fix**: Add optional chaining and nullish coalescing

---

### Warnings

#### 1. [REACT] Missing useEffect dependency
**File**: `src/components/Dashboard.tsx:56`
**Issue**: `userId` used in effect but not in dependency array
```typescript
// Current
useEffect(() => {
  fetchData(userId);
}, []); // userId missing

// Should be
useEffect(() => {
  fetchData(userId);
}, [userId]);
```

---

### Code Quality

#### 1. [SMELL] Magic number
**File**: `src/lib/constants.ts:12`
**Issue**: Unexplained number `86400000`
**Suggestion**: Extract to named constant `MS_PER_DAY`

---

### Files Scanned
- `src/lib/utils.ts` (42 lines)
- `src/hooks/useData.ts` (89 lines)
- `src/components/Dashboard.tsx` (156 lines)

**Total**: 3 files, 287 lines analyzed
```

## Integration with Justice League

### Handoff Protocols

| If Bug-Bot Finds... | Handoff To | Reason |
|---------------------|------------|--------|
| Complex security issues | Martian Manhunter | Deep security analysis |
| UI/interaction bugs | Batman | Interactive testing needed |
| Performance bottlenecks | Flash | Performance profiling |
| Accessibility issues | Wonder Woman | A11y specialist |

### Combined Workflows

**Pre-commit check**:
1. Bug-Bot scans staged files
2. If critical bugs found, block commit
3. Show fixes inline

**After major refactor**:
1. Bug-Bot full scan
2. Batman runs interactive tests
3. Flash checks performance impact

## Common Patterns to Detect

### TypeScript/JavaScript

```typescript
// Pattern: Unsafe array access
array[index]  // Bug if index not validated
// Fix: array[index] ?? defaultValue OR array.at(index)

// Pattern: Promise without await in async
async function foo() {
  somePromise();  // Bug: forgot await
}
// Fix: await somePromise();

// Pattern: Object spread overwriting
const merged = { ...defaults, ...config, important: true };
// Potential bug if config has 'important' key
```

### React Specific

```tsx
// Pattern: State update based on previous state
setCount(count + 1);  // Bug in rapid updates
// Fix: setCount(prev => prev + 1);

// Pattern: Effect cleanup missing
useEffect(() => {
  const subscription = subscribe();
  // Bug: no cleanup
}, []);
// Fix: return () => subscription.unsubscribe();

// Pattern: Conditional hook call
if (condition) {
  useState();  // Bug: violates Rules of Hooks
}
```

### Next.js Specific

```tsx
// Pattern: Server component using client hooks
// In app/page.tsx (server by default)
'use client'  // Missing directive!
export default function Page() {
  const [state, setState] = useState();  // Bug without 'use client'
}

// Pattern: Async client component
'use client'
export default async function Page() {  // Bug: async client component
  const data = await fetch();
}
```

## Activation Examples

**User says**: "find bugs in the auth module"
**Bug-Bot**: Scans `src/lib/auth/` directory

**User says**: "check for errors"
**Bug-Bot**: Scans recently changed files

**User says**: "bug-bot --full"
**Bug-Bot**: Full codebase scan

**After code edit**: Auto-scans edited file for introduced bugs

## Configuration

### Severity Thresholds

| Level | Action |
|-------|--------|
| Critical | Report immediately, suggest blocking |
| Warning | Report in summary, suggest review |
| Info | Collect for code quality report |

### Ignored Patterns

Add to `.bugbotignore` (similar to `.gitignore`):
```
# Ignore test files for certain checks
**/*.test.ts
**/*.spec.ts

# Ignore generated files
src/generated/
```

---

**Version**: 1.0.0
**Author**: Justice League AI System
**Last Updated**: 2025-12-08
