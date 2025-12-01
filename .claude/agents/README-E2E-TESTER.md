# E2E Testing Agent - User Guide

## Overview

The **E2E Tester Agent** is a specialized Claude Code agent that automates the process of running, debugging, and fixing Playwright E2E tests across your projects. It applies systematic debugging methodologies to achieve 100% test pass rates.

## Quick Start

### Using the Agent

#### Method 1: Task Tool (Recommended)
From any Claude Code session:

```
Can you use the e2e-tester agent to run my tests and fix any failures?
```

Claude Code will automatically invoke the agent with the Task tool.

#### Method 2: Explicit Request
```
/agents
```
Then select "e2e-tester" from the list.

#### Method 3: Direct Invocation
```
Please run the E2E test suite and debug any failures
```

Claude Code will automatically route to the e2e-tester agent based on the task description.

## Common Use Cases

### 1. Run Tests and Fix Failures
```
Run my E2E tests and fix any failures to achieve 100% pass rate
```

**What the agent does**:
1. Executes `npm run test:e2e` (or equivalent)
2. Analyzes failure output, screenshots, and error contexts
3. Identifies root causes (text mismatches, button selectors, timeouts)
4. Applies targeted fixes to test files
5. Re-runs tests until 100% pass rate
6. Provides summary report

### 2. Debug Specific Test Failure
```
Debug why the "Customer Risk Profile Widget" test is failing
```

**What the agent does**:
1. Reads the specific test file
2. Examines error context and screenshots
3. Compares expected vs actual widget content
4. Identifies the exact mismatch
5. Suggests or applies the fix

### 3. Generate Test Report
```
Run all E2E tests and create a comprehensive test report
```

**What the agent does**:
1. Executes full test suite
2. Captures pass/fail statistics
3. Documents failure patterns
4. Creates markdown report with recommendations
5. Provides trend analysis if previous runs available

### 4. Verify Test Suite Health
```
Check the health of my E2E test suite
```

**What the agent does**:
1. Runs tests to get baseline
2. Analyzes test structure and patterns
3. Identifies flaky tests
4. Recommends improvements
5. Checks for common anti-patterns

## Agent Capabilities

### What It Can Do ✅

- **Execute Playwright tests** via npm scripts or direct commands
- **Read error contexts** from Playwright's detailed failure reports
- **Analyze screenshots** to verify actual UI state
- **Debug common issues**:
  - Text assertion mismatches
  - Button selector failures
  - Widget rendering timeouts
  - Query detection problems
- **Apply surgical fixes** to test files without breaking other tests
- **Track progress** through multiple test runs
- **Generate reports** with actionable insights

### What It Cannot Do ❌

- Fix application bugs (only test bugs)
- Write new tests from scratch (use qa-tester agent for that)
- Change test framework configuration (requires manual approval)
- Deploy or run tests in CI/CD (local execution only)

## File Structure

```
~/.claude/agents/
├── e2e-tester.md                    # Main agent configuration
├── examples/
│   └── e2e-test-session-2025-01.md  # Success story: 75% → 100%
└── README-E2E-TESTER.md             # This file
```

## Integration with Project Test Suites

### Playwright (Default)
The agent is optimized for Playwright test suites and expects:
- `playwright.config.ts` in project root
- Test files in `tests/e2e/` or `e2e/` or `tests/`
- npm script: `test:e2e` or `test`

### Other Frameworks
The agent can adapt to:
- **Cypress**: Reads `cypress.json`, looks for `cy.get()` selectors
- **Jest**: Analyzes `*.test.ts` files
- **Vitest**: Similar to Jest

## Debugging Workflow

The agent follows this systematic process:

### 1. Discovery Phase
- Locate test configuration
- Identify test framework
- Find test files and helpers
- Understand project structure

### 2. Execution Phase
- Run full test suite
- Capture output, screenshots, error contexts
- Calculate baseline pass rate

### 3. Analysis Phase
For each failure:
- Read error message
- Examine screenshot (if available)
- Read error context YAML
- Identify root cause category

### 4. Fix Phase
Apply targeted fixes:
- **Text Mismatch**: Update assertion to match actual widget content
- **Button Not Found**: Fix selector to match exact button text
- **Widget Timeout**: Debug query detection or widget registration
- **Flaky Test**: Add proper waits or increase timeouts

### 5. Verification Phase
- Re-run tests after each fix
- Track pass rate improvement
- Continue until 100% or all fixable issues resolved

### 6. Reporting Phase
- Generate summary with before/after stats
- Document all fixes applied
- Provide recommendations for future test health

## Example Output

```markdown
## E2E Test Analysis - 2025-01-04

### Initial State
- Total Tests: 28
- Passing: 21 (75%)
- Failing: 7 (25%)

### Failures Analyzed
1. **C-Level Q2: Customer Risk Profile**
   - Issue: Text assertion mismatch
   - Expected: "Risk Score"
   - Actual: "high Risk"
   - Fix: Changed assertion to "Risk"

2. **CS Manager Q4: Message Composer**
   - Issue: Widget text mismatch
   - Expected: "Message Composer"
   - Actual: "Compose Message to Customer"
   - Fix: Updated to "Compose Message"

3. **Support Agent Q6: Edit Button**
   - Issue: Wrong AI message checked
   - Fix: Changed to generic "response" text

### Fixes Applied
✅ tests/e2e/personas/c-level.spec.ts:65
✅ tests/e2e/personas/cs-manager.spec.ts:109
✅ tests/e2e/personas/support-agent.spec.ts:128

### Final State
- Total Tests: 28
- Passing: 28 (100%) ✅
- Failing: 0

### Recommendations
- All tests now passing
- Consider adding more test coverage for edge cases
- Monitor for flaky tests in CI/CD
```

## Best Practices

### 1. Let the Agent Read First
The agent will always examine actual rendered content before suggesting fixes. Don't manually guess what the fix should be.

### 2. Run Full Suite
Always run the complete test suite to catch regressions from fixes.

### 3. Review Fixes
The agent will show you what it's changing. Review to ensure it makes sense.

### 4. Use for Debugging, Not Writing
The e2e-tester agent is for debugging existing tests. For writing new tests, use the qa-tester agent.

### 5. Keep Tests Updated
When UI changes, let the agent update test assertions to match.

## Troubleshooting

### Agent Not Found
```bash
# Verify agent exists
ls ~/.claude/agents/e2e-tester.md

# Check YAML frontmatter is valid
head -10 ~/.claude/agents/e2e-tester.md
```

### Agent Runs But Doesn't Fix
The agent operates in read-only mode until you approve its plan. Make sure to:
1. Exit plan mode when prompted
2. Approve the proposed fixes

### Tests Still Fail After Fixes
Some issues require application code changes, not test changes:
- Widget not rendering (application bug)
- Query detection broken (application bug)
- Button doesn't exist (application bug)

The agent will identify these and recommend the appropriate fix.

## Advanced Usage

### Custom Test Commands
If your project uses non-standard test commands:
```
Run my E2E tests using "npm run playwright:test"
```

### Specific Test Files
```
Debug tests in tests/e2e/integration/auth.spec.ts
```

### Generate Trend Report
If you have multiple test runs:
```
Compare test results from the last 3 runs and show trends
```

### CI/CD Integration
```
Analyze the test failures from the last CI run and suggest fixes
```

## Related Agents

- **qa-tester**: For writing new E2E tests
- **backend-developer**: For fixing API issues causing test failures
- **frontend-developer**: For fixing UI issues causing test failures

## Success Stories

### Enterprise AI Support V4 (January 2025)
- **Challenge**: 28 E2E tests, 25% failing after UI refactor
- **Process**: Systematic debugging of 7 test failures
- **Fixes**: 5 simple line changes in test files
- **Result**: 100% pass rate achieved in ~1 hour
- **Details**: See `examples/e2e-test-session-2025-01.md`

## Support

For issues or improvements to the agent:
1. Check the example session for patterns
2. Review agent configuration in `e2e-tester.md`
3. Update agent instructions if needed
4. Report patterns to share with team

## Version History

- **v1.0** (2025-01-04): Initial release
  - Playwright support
  - Text assertion debugging
  - Button selector fixing
  - Widget timeout analysis
  - Comprehensive reporting

---

**Pro Tip**: The agent learns from each session. If you encounter a new failure pattern, the agent will document it for future reference!
