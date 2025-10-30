# 🎯 GREEN ARROW - Visual Validation Specialist

**Oliver Queen** | **Role**: Pixel-Perfect Validator | **Expertise**: WYSIWYG Guardian

---

## Mission

Green Arrow ensures every Figma→Code conversion is **pixel-perfect**. He validates:
- ✅ Spacing (margins, padding, gaps)
- ✅ Colors (hex values, gradients)
- ✅ Typography (font-size, weight, line-height)
- ✅ Measurements (width, height, positioning)
- ✅ Layout (flexbox, grid, alignment)
- ✅ Design Tokens (Tailwind compliance)
- ✅ Component Usage (shadcn/ui compliance)

**"I never miss. Every pixel, every color, every spacing - all perfect."** - Green Arrow

---

## Arsenal: MCP Server Mastery

Green Arrow coordinates **4 MCP servers** to achieve perfect validation:

### 1. 🎨 Figma MCP (`figma-mcp`)

**Purpose**: Extract exact design specifications from Figma

**What Green Arrow Extracts**:
```json
{
  "measurements": {
    "width": 224,
    "height": 88,
    "x": 0,
    "y": 0
  },
  "colors": {
    "fills": [{"type": "SOLID", "color": {"r": 0, "g": 0, "b": 0}}],
    "background": "#fafafa",
    "text": "#18181b"
  },
  "typography": {
    "fontSize": 30,
    "fontWeight": 700,
    "fontFamily": "Inter",
    "lineHeight": 1.5,
    "letterSpacing": 0
  },
  "spacing": {
    "paddingTop": 24,
    "paddingRight": 16,
    "paddingBottom": 24,
    "paddingLeft": 16,
    "itemSpacing": 24
  },
  "layout": {
    "layoutMode": "HORIZONTAL",
    "primaryAxisAlignItems": "CENTER",
    "counterAxisAlignItems": "CENTER"
  }
}
```

**How He Uses It**:
1. Parse Figma URL to extract `file_key` and `node_id`
2. Call Figma API to get node data
3. Extract bounding boxes, fills, strokes, typography
4. Convert to design tokens (Tailwind-compatible)

---

### 2. 🔍 Chrome DevTools MCP (`chrome-devtools-mcp`)

**Purpose**: Inspect rendered components in real browsers

**What Green Arrow Inspects**:
```json
{
  "computed_styles": {
    "width": "224px",
    "height": "88px",
    "backgroundColor": "rgb(250, 250, 250)",
    "color": "rgb(24, 24, 27)",
    "fontSize": "30px",
    "fontWeight": "700",
    "lineHeight": "45px",
    "padding": "24px 16px",
    "gap": "24px",
    "display": "flex",
    "flexDirection": "row",
    "alignItems": "center"
  },
  "box_model": {
    "margin": {"top": 0, "right": 0, "bottom": 0, "left": 0},
    "border": {"top": 0, "right": 0, "bottom": 1, "left": 0},
    "padding": {"top": 24, "right": 16, "bottom": 24, "left": 16},
    "content": {"width": 224, "height": 40}
  }
}
```

**How He Uses It**:
1. Navigate to rendered page (e.g., `localhost:3005/settings-profile`)
2. Take snapshot of DOM structure
3. Select target element by CSS selector
4. Extract computed styles using `window.getComputedStyle()`
5. Capture box model (margin, border, padding, content)
6. Screenshot for visual diff

---

### 3. 💎 Tailwind CSS MCP (`tailwindcss-mcp`)

**Purpose**: Validate Tailwind utility classes match design specs

**What Green Arrow Validates**:

**Spacing Classes**:
- `p-6` = 24px padding ✅
- `gap-6` = 24px gap ✅
- `space-y-1` = 4px vertical spacing ✅

**Color Classes**:
- `bg-[#fafafa]` matches Figma background ✅
- `text-zinc-900` = #18181b ✅
- `border-zinc-200` = #e5e7eb ✅

**Typography Classes**:
- `text-3xl` = 30px font-size ✅
- `font-bold` = 700 weight ✅
- `leading-normal` = 1.5 line-height ✅

**Layout Classes**:
- `flex` + `items-center` = centered alignment ✅
- `w-[224px]` = exact 224px width ✅
- `max-w-[1400px]` = constrained content ✅

**How He Uses It**:
1. Extract all `className` attributes from component code
2. Parse Tailwind utility classes
3. Convert classes to CSS values (e.g., `p-6` → `padding: 24px`)
4. Compare with Figma specs
5. Flag mismatches (e.g., `p-4` when Figma says 24px)

---

### 4. 🧩 shadcn/ui MCP (`shadcn-ui`)

**Purpose**: Verify component library compliance

**What Green Arrow Checks**:

**Component Usage**:
```typescript
// ✅ CORRECT: Using shadcn Input component
import { Input } from './ui/input';
<Input id="username" type="text" defaultValue="nicol43" />

// ❌ WRONG: Using native input without shadcn
<input type="text" />  // Missing shadcn styling
```

**Props Validation**:
```typescript
// ✅ CORRECT: shadcn Button with proper variant
import { Button } from './ui/button';
<Button variant="default" size="lg">Submit</Button>

// ⚠️ WARNING: Custom styling might override shadcn
<Button className="custom-styles">Submit</Button>
```

**Design System Compliance**:
- ✅ Using `cn()` utility for className merging
- ✅ Following shadcn color tokens (zinc, slate)
- ✅ Using shadcn spacing scale
- ✅ Accessible props (aria-*, role)

**How He Uses It**:
1. Check if shadcn components are imported
2. Validate component props match shadcn API
3. Verify `cn()` utility is used for className merging
4. Check design token compliance (colors, spacing)
5. Ensure accessibility attributes are present

---

## Validation Pipeline

### Step-by-Step Process

**Input**:
- Figma URL: `https://figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=17-1440`
- Rendered URL: `http://localhost:3005/settings-profile`
- Component Name: `SettingsProfile`
- Component Code: `SettingsProfile.tsx`

**Step 1: Extract Figma Specs** (Figma MCP)
```python
figma_specs = green_arrow.extract_figma_specs(
    file_key="6Pmf9gCcUccyqbCO9nN6Ts",
    node_id="17-1440"
)
# → Gets exact measurements, colors, typography from Figma
```

**Step 2: Inspect Rendered Component** (Chrome DevTools MCP)
```python
rendered_specs = green_arrow.inspect_rendered_component(
    url="http://localhost:3005/settings-profile",
    selector="#SettingsProfile"
)
# → Gets computed styles from actual rendered page
```

**Step 3: Extract Tailwind Classes** (Code Parsing)
```python
tailwind_classes = green_arrow.extract_tailwind_classes(component_code)
# → ['bg-[#fafafa]', 'p-6', 'gap-6', 'text-3xl', 'font-bold', ...]
```

**Step 4: Validate Tailwind** (Tailwind MCP)
```python
tailwind_validation = green_arrow.validate_tailwind_classes(
    tailwind_classes,
    figma_specs
)
# → Checks if 'p-6' matches Figma's 24px padding
```

**Step 5: Validate shadcn/ui** (shadcn MCP)
```python
shadcn_validation = green_arrow.validate_shadcn_usage(component_code)
# → Checks Input, Label, Button component usage
```

**Step 6: Compare & Calculate Score**
```python
accuracy_score = green_arrow.calculate_accuracy_score({
    'measurements': measurements_comparison,
    'colors': colors_comparison,
    'typography': typography_comparison,
    'spacing': spacing_comparison,
    'tailwind': tailwind_validation,
    'shadcn': shadcn_validation
})
# → Score: 97.5% (Excellent)
```

**Step 7: Generate Report**
```python
report = green_arrow.generate_validation_report(
    component_name="SettingsProfile",
    accuracy_score=97.5,
    discrepancies=[...],
    recommendations=[...]
)
```

---

## Validation Report Example

```markdown
# 🎯 Visual Validation Report: SettingsProfile

**Figma Design**: https://figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=17-1440
**Rendered Page**: http://localhost:3005/settings-profile
**Validated**: 2025-10-23T22:45:00Z

## Summary

**Accuracy Score**: 97.5%
**Status**: ✅ EXCELLENT

---

## Measurements Comparison

| Property | Figma | Rendered | Match | Difference |
|----------|-------|----------|-------|------------|
| Width | 224px | 224px | ✅ | 0px |
| Height | 88px | 88px | ✅ | 0px |
| Sidebar Width | 224px | 224px | ✅ | 0px |
| Content Max Width | 1400px | 1400px | ✅ | 0px |

## Colors Comparison

| Property | Figma | Rendered | Match |
|----------|-------|----------|-------|
| Background | #fafafa | #fafafa | ✅ |
| Primary | #000000 | #000000 | ✅ |
| Text | #18181b | #18181b | ✅ |
| Border | #e5e7eb | #e5e7eb | ✅ |

## Typography Comparison

| Property | Figma | Rendered | Match |
|----------|-------|----------|-------|
| H1 Font Size | 30px | 30px | ✅ |
| H1 Font Weight | 700 | 700 | ✅ |
| Body Font Size | 14px | 14px | ✅ |
| Line Height | 1.5 | 1.5 | ✅ |

## Spacing Comparison

| Property | Figma | Rendered | Match | Difference |
|----------|-------|----------|-------|------------|
| Main Padding | 24px | 24px | ✅ | 0px |
| Gap | 24px | 24px | ✅ | 0px |
| Form Section Padding | 24px | 24px | ✅ | 0px |

## Tailwind Validation

✅ **Total Classes Validated**: 47
✅ **Spacing Classes**: p-6, gap-6, space-y-6 (all correct)
✅ **Color Classes**: bg-[#fafafa], text-zinc-900 (all correct)
✅ **Layout Classes**: flex, items-center, max-w-[1400px] (all correct)

## shadcn/ui Validation

✅ **Input Component**: Used correctly with Label
✅ **cn() Utility**: Properly implemented
✅ **Accessibility**: All form inputs have labels

## Discrepancies Found

1. **spacing.cardPadding**: Figma = 24px, Rendered = 20px (Δ 4px)
   - **Severity**: Low
   - **Fix**: Change `p-5` to `p-6` in card component

---

**Green Arrow's Verdict**: ✅ EXCELLENT (97.5% accuracy)

Minor spacing adjustment needed in card component. Otherwise, pixel-perfect match achieved.
```

---

## Accuracy Scoring System

Green Arrow uses a sophisticated scoring system:

### Score Ranges

| Score | Status | Meaning |
|-------|--------|---------|
| 98-100% | ✅ EXCELLENT | Pixel-perfect or near-perfect |
| 95-97% | ✅ GOOD | Minor discrepancies, acceptable |
| 90-94% | ⚠️ ACCEPTABLE | Some issues, review recommended |
| 85-89% | ⚠️ NEEDS WORK | Multiple issues, refactoring needed |
| <85% | ❌ FAILED | Major discrepancies, regenerate |

### Tolerance Levels

Green Arrow understands that some variance is acceptable:

- **Spacing**: ±2px tolerance (browser rounding)
- **Sizing**: ±2px tolerance
- **Positioning**: ±1px tolerance
- **Colors**: 0px tolerance (must be exact)
- **Typography**: 0px tolerance (must be exact)

### Weighted Categories

Not all checks are equal:

1. **Critical (40% weight)**:
   - Layout structure
   - Component hierarchy
   - Design system compliance

2. **High Priority (30% weight)**:
   - Colors
   - Typography
   - Major spacing

3. **Medium Priority (20% weight)**:
   - Minor spacing
   - Border radius
   - Shadows

4. **Low Priority (10% weight)**:
   - Hover states
   - Transitions
   - Non-critical styling

---

## Integration with Justice League

### Where Green Arrow Fits

```
Conversion Workflow:
1. Superman coordinates mission
2. Artemis generates component code
3. → GREEN ARROW validates output ← (NEW!)
4. If EXCELLENT/GOOD → Approve
5. If NEEDS WORK/FAILED → Send back to Artemis
6. Oracle records validation results
```

### Automated Validation

Green Arrow runs automatically after every conversion:

```python
# In superman_coordinator.py
result = artemis.generate_component_code_expert(...)

# NEW: Automatic validation
validation = green_arrow.validate_component(
    figma_url=figma_url,
    rendered_url="http://localhost:3005/" + component_name.lower(),
    component_name=component_name,
    component_code=result['code']
)

if validation['accuracy_score'] < 90:
    # Send back to Artemis for fixes
    result = artemis.fix_discrepancies(validation['discrepancies'])
```

---

## Manual Validation

You can also call Green Arrow manually:

```python
from core.justice_league.green_arrow_visual_validator import green_arrow_validate_component

report = green_arrow_validate_component(
    figma_url="https://figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=17-1440",
    rendered_url="http://localhost:3005/settings-profile",
    component_name="SettingsProfile",
    component_code=open("preview-app/src/components/SettingsProfile.tsx").read()
)

print(f"Accuracy: {report['accuracy_score']}%")
print(f"Status: {report['status']}")
print(f"Discrepancies: {len(report['discrepancies'])}")
```

---

## Best Practices

### For Artemis (Code Generation)

When Artemis generates code, she should follow these rules to pass Green Arrow's inspection:

1. **Use Exact Figma Values**:
   ```typescript
   // ✅ GOOD: Exact Figma spacing
   className="gap-6"  // 24px = Figma itemSpacing

   // ❌ BAD: Approximate spacing
   className="gap-5"  // 20px ≠ 24px
   ```

2. **Use Design Tokens**:
   ```typescript
   // ✅ GOOD: Tailwind design token
   className="bg-[#fafafa]"

   // ❌ BAD: Inline style
   style={{backgroundColor: '#f5f5f5'}}  // Wrong hex
   ```

3. **Use shadcn Components**:
   ```typescript
   // ✅ GOOD: shadcn Input
   <Input id="username" />

   // ❌ BAD: Native input
   <input id="username" />
   ```

4. **Match Layout Structure**:
   - If Figma uses horizontal auto-layout → `flex flex-row`
   - If Figma uses vertical auto-layout → `flex flex-col`
   - If Figma centers items → `items-center justify-center`

### For Future Conversions

Every new conversion should:
1. Run Green Arrow validation automatically
2. Aim for 95%+ accuracy score
3. Fix all HIGH severity discrepancies
4. Document any acceptable LOW severity variances

---

## Validation Database

Green Arrow maintains validation history:

**Location**: `data/validation/`

**Files**:
- `validation_reports.json` - All validation reports
- `discrepancies.json` - Historical discrepancies
- `accuracy_scores.json` - Score trends over time

**Usage**:
```python
# Get all validations for a component
reports = green_arrow.get_validation_history("SettingsProfile")

# Get average accuracy score
avg_score = green_arrow.get_average_accuracy("poc test")

# Find common discrepancies
common_issues = green_arrow.find_common_discrepancies()
```

---

## Future Enhancements

Green Arrow will get even better:

1. **Visual Regression Testing**: Screenshot comparison
2. **Responsive Validation**: Check mobile, tablet, desktop breakpoints
3. **Animation Validation**: Verify transitions match Figma
4. **Accessibility Audit**: WCAG 2.1 compliance
5. **Performance Metrics**: Load time, render time
6. **Cross-Browser Testing**: Chrome, Firefox, Safari

---

## Summary

Green Arrow is the **Quality Assurance Guardian** of the Justice League. He ensures:

✅ **What You See (Figma) = What You Get (Rendered)**

His expertise in **4 MCP servers** makes him the most precise validator:
- 🎨 Figma MCP → Extract design specs
- 🔍 Chrome DevTools MCP → Inspect rendered output
- 💎 Tailwind MCP → Validate utility classes
- 🧩 shadcn MCP → Check component compliance

With Green Arrow on the team, every Figma→Code conversion is **pixel-perfect**! 🎯

---

**"Precision is not optional. It's mandatory."** - Green Arrow 🎯
