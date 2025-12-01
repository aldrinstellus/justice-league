# E2E Testing Agent - Quick Reference

## Invoke the Agent

```
Run my E2E tests and fix any failures
```

## Common Commands

| What You Want | Say This |
|---------------|----------|
| Run tests and fix failures | "Run E2E tests and achieve 100% pass rate" |
| Debug specific test | "Debug why the [test name] test is failing" |
| Generate report | "Run tests and create a test report" |
| Check test health | "Analyze my E2E test suite health" |
| Fix flaky tests | "Find and fix flaky tests" |

## What Gets Fixed Automatically

✅ Text assertion mismatches
✅ Button selector errors
✅ Widget timeout issues (test-side)
✅ Incorrect expectations vs reality
✅ Multi-message interaction issues

## What Requires Manual Review

⚠️ Application bugs causing test failures
⚠️ Test framework configuration changes
⚠️ New test creation (use qa-tester agent)
⚠️ CI/CD pipeline issues

## Files Created

```
~/.claude/agents/
├── e2e-tester.md              # Agent config
├── examples/
│   └── e2e-test-session-2025-01.md  # Success story
├── README-E2E-TESTER.md       # Full documentation
└── QUICK-REFERENCE.md         # This file
```

## Agent Workflow

1. **Run** → Execute test suite
2. **Analyze** → Read errors, screenshots, contexts
3. **Debug** → Identify root causes
4. **Fix** → Apply targeted changes
5. **Verify** → Re-run until 100%
6. **Report** → Summary of all changes

## Success Metrics

📊 **Enterprise AI Support V4**
- Before: 21/28 (75%)
- After: 28/28 (100%)
- Time: ~1 hour
- Changes: 5 line edits

## Pro Tips

💡 Let the agent read actual content before fixing
💡 Run full suite to catch regressions
💡 Review fixes before applying
💡 Use for debugging, not writing new tests
💡 Keep test assertions matched to reality

## Next Steps

1. Try it: `"Run my E2E tests"`
2. Review: Check the fixes it proposes
3. Learn: Read the success story example
4. Customize: Edit agent config as needed

---

**Need help?** Read `README-E2E-TESTER.md` for full documentation
