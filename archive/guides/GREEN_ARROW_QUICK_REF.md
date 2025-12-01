# 🎯 Green Arrow - Quick Reference Card

**Oliver Queen** | **Visual Validation Specialist** | **Pixel-Perfect Guardian**

---

## Core Mission

Ensure **WYSIWYG** (What You See Is What You Get) - Figma design = Rendered output

---

## MCP Arsenal

| MCP Server | Purpose | Key Actions |
|------------|---------|-------------|
| 🎨 **Figma MCP** | Extract design specs | Get measurements, colors, typography, spacing, layout |
| 🔍 **Chrome DevTools** | Inspect rendered output | Get computed styles, box model, DOM structure |
| 💎 **Tailwind MCP** | Validate utility classes | Check `p-6` = 24px, `bg-[#fafafa]` matches Figma |
| 🧩 **shadcn MCP** | Check component usage | Verify Input, Label, Button compliance |

---

## What He Validates

✅ **Spacing** - Margins, padding, gaps (±2px tolerance)
✅ **Colors** - Hex values, RGB (exact match required)
✅ **Typography** - Font size, weight, line-height (exact match)
✅ **Measurements** - Width, height, positioning (±2px tolerance)
✅ **Layout** - Flexbox, grid, alignment (structure match)
✅ **Tailwind Classes** - Utility class accuracy
✅ **shadcn/ui** - Component library compliance

---

## Accuracy Scoring

| Score | Status | Action |
|-------|--------|--------|
| 98-100% | ✅ **EXCELLENT** | Approve immediately |
| 95-97% | ✅ **GOOD** | Approve with minor notes |
| 90-94% | ⚠️ **ACCEPTABLE** | Review recommendations |
| 85-89% | ⚠️ **NEEDS WORK** | Fix high-priority issues |
| <85% | ❌ **FAILED** | Regenerate component |

---

## Validation Pipeline

```
1. Extract Figma specs     → figma-mcp
2. Inspect rendered page   → chrome-devtools-mcp
3. Parse Tailwind classes  → code analysis
4. Validate Tailwind       → tailwindcss-mcp
5. Check shadcn usage      → shadcn-ui
6. Compare & calculate     → accuracy score
7. Generate report         → markdown report
```

---

## Usage

### Automatic (with Superman)
```python
# Green Arrow validates automatically after Artemis
result = artemis.generate_component_code_expert(...)
validation = green_arrow.validate_component(...)  # Auto-runs

if validation['accuracy_score'] < 90:
    artemis.fix_discrepancies(validation['discrepancies'])
```

### Manual
```python
from core.justice_league.green_arrow_visual_validator import green_arrow_validate_component

report = green_arrow_validate_component(
    figma_url="https://figma.com/design/.../node-id=17-1440",
    rendered_url="http://localhost:3005/settings-profile",
    component_name="SettingsProfile",
    component_code=code
)

print(f"Score: {report['accuracy_score']}%")
print(f"Status: {report['status']}")
```

---

## Validation Report Format

```markdown
# 🎯 Visual Validation Report: ComponentName
**Accuracy**: 97.5%
**Status**: ✅ EXCELLENT

## Measurements
| Property | Figma | Rendered | Match | Δ |
|----------|-------|----------|-------|---|
| Width | 224px | 224px | ✅ | 0px |

## Colors
| Property | Figma | Rendered | Match |
|----------|-------|----------|-------|
| Background | #fafafa | #fafafa | ✅ |

## Discrepancies
1. spacing.padding: Figma = 24px, Rendered = 20px (Δ 4px)

**Verdict**: ✅ EXCELLENT - Minor fix needed
```

---

## Common Discrepancies

| Issue | Figma | Rendered | Fix |
|-------|-------|----------|-----|
| Padding off | 24px | 20px | Change `p-5` → `p-6` |
| Wrong color | #fafafa | #f5f5f5 | Change `bg-zinc-50` → `bg-[#fafafa]` |
| Font size | 30px | 28px | Change `text-2xl` → `text-3xl` |
| Gap missing | 24px | 0px | Add `gap-6` |

---

## Best Practices for Artemis

To pass Green Arrow's inspection:

1. **Use exact Figma values**: `gap-6` (24px) not `gap-5` (20px)
2. **Match color hex codes**: `bg-[#fafafa]` not `bg-zinc-50`
3. **Use shadcn components**: `<Input />` not `<input />`
4. **Follow layout structure**: Figma horizontal → `flex flex-row`
5. **Include accessibility**: All inputs have labels

---

## Integration Points

**Before Green Arrow** (Old):
```
Artemis → Generate → Deploy → Hope it's correct
```

**After Green Arrow** (New):
```
Artemis → Generate → Green Arrow Validate →
  If ✅ → Deploy
  If ❌ → Fix → Re-validate
```

---

## Databases

**Location**: `data/validation/`

- `validation_reports.json` - All validation reports
- `discrepancies.json` - Historical issues
- `accuracy_scores.json` - Score trends

---

## Quick Commands

```python
# Get validation history
green_arrow.get_validation_history("SettingsProfile")

# Get average accuracy for project
green_arrow.get_average_accuracy("poc test")

# Find common issues
green_arrow.find_common_discrepancies()
```

---

## Tolerances

| Type | Tolerance | Reason |
|------|-----------|--------|
| Spacing | ±2px | Browser rounding |
| Sizing | ±2px | Sub-pixel rendering |
| Position | ±1px | Layout engine variance |
| Color | 0px | Must be exact |
| Typography | 0px | Must be exact |

---

## Workflow Position

```
Justice League Conversion Pipeline:

1. Superman coordinates
2. Artemis generates code
3. 🎯 GREEN ARROW VALIDATES ← YOU ARE HERE
4. Oracle records results
5. Deploy to preview
```

---

## Contact Points

**Works With**:
- **Artemis** - Validates her code generation
- **Oracle** - Records validation results
- **Superman** - Reports to coordinator

**Reports**:
- Component accuracy scores
- Design token compliance
- Common discrepancies
- Improvement recommendations

---

## Success Metrics

**Target**: 95%+ accuracy on all conversions

**Current**:
- SettingsProfile: 97.5% ✅
- Settings: (pending validation)

**Goal**: 100% of conversions pass validation before deployment

---

**"I never miss. Every pixel, every color, every spacing - all perfect."** 🎯

---

*See GREEN_ARROW_GUIDE.md for complete documentation*
