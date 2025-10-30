# 🚀 Figma MCP + Claude Code + Playwright - Quick Reference

**For Oracle and Justice League Heroes**

---

## When to Use This Workflow

✅ **USE** when:
- Building 3+ components with 2+ breakpoints
- Need pixel-perfect Figma implementation
- Working on responsive component libraries
- Want to catch invisible CSS bugs before deployment

❌ **DON'T USE** when:
- Single landing page (<5 components)
- Quick prototype (no multi-breakpoint requirements)
- No Figma MCP access
- Simple static site

---

## The 7-Step Process

### 1️⃣ Query All Breakpoints FIRST
```typescript
// Don't build desktop first!
// Query ALL breakpoints before any coding:
figmaMCP.getCode('desktop-1920px')
figmaMCP.getCode('laptop-1440px')
figmaMCP.getCode('tablet-1024px')
figmaMCP.getCode('mobile-393px')
```

### 2️⃣ Build Comparison Table
```markdown
| Property   | Desktop | Laptop | Tablet | Mobile  |
|------------|---------|--------|--------|---------|
| Padding X  | 331px   | 346px  | 234px  | 20px    |
| Layout     | row     | row    | row    | col ⚠️  |
```

### 3️⃣ Implement with Exact Values
```jsx
// ✅ GOOD: Exact Figma values
<div className="py-[89px] px-[331px] laptop:px-[346px] tablet:px-[233.78px]">

// ❌ BAD: Approximations
<div className="py-20 px-80 laptop:px-80 tablet:px-56">
```

### 4️⃣ Visual Snapshots
```typescript
// Capture at each breakpoint
[1920, 1440, 1024, 393].forEach(width => {
  page.setViewportSize({ width, height: 1080 });
  page.screenshot({ path: `${width}px.png` });
});
```

### 5️⃣ Computed Style Verification
```typescript
// This catches invisible bugs!
const flexGrow = await page.evaluate(
  el => window.getComputedStyle(el).flexGrow
);
expect(flexGrow).toBe('1'); // ← Screenshots can't show this!
```

### 6️⃣ Console Error Check
```typescript
// Monitor for React errors, missing deps, etc.
page.on('console', msg => {
  if (msg.type() === 'error') {
    errors.push(msg.text());
  }
});
```

### 7️⃣ Fix & Re-validate
- Fix bugs found
- Re-run Playwright validation
- Confirm all breakpoints pass

---

## Three Common Bugs This Catches

### Bug #1: Mobile Component Mismatch
**Problem**: Designer used different component on mobile (not responsive variant)

**Detection**:
```typescript
// Desktop/Laptop/Tablet all return node "1:67560"
// Mobile returns node "816:12905" ← DIFFERENT!
```

**Fix**: Conditional rendering
```jsx
<VideoSection className="hidden tablet:block" />
<PhotoSection className="block tablet:hidden" />
```

---

### Bug #2: Invisible Flex-Grow
**Problem**: Looks correct visually but has `flex-grow: 0` leaving unwanted space

**Detection**:
```typescript
const flexGrow = await page.evaluate(
  el => window.getComputedStyle(el).flexGrow
);
// Returns '0' when you expected '1' ← Visual inspection missed this!
```

**Fix**:
```jsx
<div className="laptop:flex-1">
```

---

### Bug #3: Responsive Visibility Misunderstanding
**Problem**: `tablet:inline-flex` doesn't hide on mobile (it's additive!)

**Detection**:
```typescript
await page.setViewportSize({ width: 393 }); // Mobile
const count = await page.locator('nav a:visible').count();
// Returns 6 when you expected 0 ← Bug!
```

**Fix**:
```jsx
// ✅ GOOD: Start hidden, then show
<a className="hidden tablet:inline-flex">

// ❌ BAD: Missing base state
<a className="tablet:inline-flex">
```

---

## Cheat Sheet: Do's and Don'ts

| ✅ DO | ❌ DON'T |
|------|---------|
| Query all breakpoints before coding | Build desktop first, "make it responsive" later |
| Use arbitrary values `px-[331px]` | Approximate to `px-80` |
| Validate computed CSS properties | Trust visual inspection alone |
| Think mobile-first (base state) | Assume responsive prefixes replace |
| Build comparison tables | Guess which values change |
| Automate validation with Playwright | Manual screenshot comparison at scale |

---

## Tools Needed

```json
{
  "figma-mcp": "Design token extraction",
  "claude-code": "Responsive interpretation",
  "playwright-mcp": "Programmatic validation",
  "tailwind-css": "Arbitrary values support"
}
```

---

## Metrics & ROI

```
Setup: ~2 hours
Savings: ~20 min/component
Break-even: After 6 components

Example: 21 components × 4 breakpoints = 84 variations
- Traditional: 45 min/component = 16 hours
- This workflow: 25 min/component = 9 hours
- Savings: 7 hours + 12+ bugs caught
```

---

## Validation Checklist

- [ ] All 4 breakpoints queried
- [ ] Comparison table created
- [ ] Tailwind arbitrary values used (exact specs)
- [ ] Visual snapshots at all breakpoints
- [ ] Computed CSS properties validated
- [ ] Console errors monitored
- [ ] Mobile-first base state defined
- [ ] Responsive visibility verified
- [ ] Component mappings documented
- [ ] All validations passed

---

## Quick Playwright Examples

### Check flex-grow
```typescript
const flexGrow = await page.locator('.card').evaluate(
  el => window.getComputedStyle(el).flexGrow
);
expect(flexGrow).toBe('1');
```

### Check actual width
```typescript
const width = await page.locator('.container').evaluate(
  el => el.offsetWidth
);
expect(width).toBe(1142);
```

### Check responsive visibility
```typescript
await page.setViewportSize({ width: 393, height: 844 });
const visibleCount = await page.locator('nav a:visible').count();
expect(visibleCount).toBe(0); // Mobile: no links
```

### Check gap value
```typescript
const gap = await page.locator('.flex-container').evaluate(
  el => window.getComputedStyle(el).gap
);
expect(gap).toBe('28px');
```

---

## For More Details

📖 **Full Article**: `./figma-mcp-claude-playwright-workflow.md`
🔍 **Metadata**: `./WORKFLOW_INDEX.json`
📚 **Best Practices**: `../GLOBAL_BEST_PRACTICES.md#design-to-code-workflows-artemis`

---

**Oracle's Note**: This workflow is indexed and ready for Justice League missions involving responsive component libraries. Reference when Artemis or any hero needs to implement design-to-code workflows at scale.

🔮 *"I see everything. I know everything. I improve everything."* - Oracle
