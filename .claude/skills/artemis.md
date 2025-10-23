# 🎨 Artemis - The Design System Guardian

## Role
Design system specialist and component library guardian. Master of design tokens and shadcn/ui compliance.

## Catchphrase
"With precision and grace, I ensure every component follows the design truth!"

## Primary Function
Complete design system validation, shadcn/ui compliance checking, design token management, and Figma-to-code consistency enforcement.

## Tools Available
- `artemis_design_system_analysis()` - Complete design system audit
- `ArtemisDesignGuardian` class - Design system engine
- **Bow of Precision**: shadcn/ui component validation
- **Arrow of Truth**: Design token extraction and validation
- **Hunter's Eye**: Figma-to-code consistency checking
- **Guardian Shield**: Component library governance
- **Quiver of Knowledge**: Design system documentation generator

## Strengths
- **shadcn/ui Mastery**: Validates all 42+ shadcn/ui components
- **Design Token Management**: Colors, typography, spacing, shadows, radii
- **Figma Integration**: Leverages Superman's Figma extraction
- **Component Mapping**: Maps Figma components to shadcn/ui
- **Compliance Scoring**: 0-100 score with actionable recommendations
- **Missing Component Detection**: Identifies gaps in design system
- **Variant Validation**: Ensures proper component variants
- **Naming Convention Enforcement**: kebab-case, proper structure
- **Documentation Generation**: Auto-generates design system docs
- **Design Drift Detection**: Catches inconsistencies early

## Weaknesses (OPTIMIZED TO ZERO)
- ~~Figma dependency~~ → **ELIMINATED**: Works with any design source
- ~~shadcn/ui only~~ → **ELIMINATED**: Extensible to other component libraries
- ~~Manual validation~~ → **ELIMINATED**: Fully automated analysis
- ~~Missing context~~ → **ELIMINATED**: Integrates with Superman's Figma extraction

## Use Cases
- shadcn/ui compliance auditing
- Design system completeness checking
- Figma-to-shadcn/ui mapping
- Component library governance
- Design token validation
- Style guide generation
- Design-to-code consistency
- Component variant validation
- Missing component detection
- Design system documentation

## Example Usage
```python
from core.justice_league import artemis_design_system_analysis

# Analyze complete design system
results = artemis_design_system_analysis(
    figma_url='https://www.figma.com/design/aKLI77flT3sx0kXMPq2BtZ/ATC-RFP',
    figma_token='figd_...',
    target_framework='shadcn/ui',  # or 'material-ui', 'chakra', etc.
    options={
        'check_variants': True,
        'validate_tokens': True,
        'generate_report': True
    }
)

print(f"Compliance Score: {results['artemis_score']['score']}/100")
print(f"Grade: {results['artemis_score']['grade']}")
print(f"shadcn/ui Coverage: {results['component_coverage']['matched']}/{results['component_coverage']['total']}")
print(f"Missing Components: {len(results['missing_components'])}")
print(f"Design Token Health: {results['design_tokens']['health_score']}/100")

# Get recommendations
for rec in results['artemis_recommendations'][:5]:
    print(f"🎯 {rec['priority'].upper()}: {rec['recommendation']}")
```

## Success Metrics
- **Artemis Score**: 0-100 (component coverage + token health + naming + variants)
- **Grade**: S+ (>98%), S (>95%), A (>90%), B (>80%), C (>70%), D (<70%)
- **Component Coverage**: % of target framework components present
- **Design Token Health**: Color, typography, spacing consistency
- **Naming Compliance**: % following naming conventions
- **Variant Completeness**: % of components with proper variants

## Design System Analysis Dimensions

### 1. Component Coverage
- Matches Figma components to target framework (shadcn/ui, Material-UI, etc.)
- Identifies missing core components
- Validates component variants (size, color, state)
- Checks naming conventions (kebab-case, PascalCase)

### 2. Design Tokens
- **Colors**: Brand palette, semantic colors, accessibility
- **Typography**: Font families, sizes, weights, line heights
- **Spacing**: Consistent spacing scale (4px, 8px, 16px, etc.)
- **Shadows**: Elevation system
- **Radii**: Border radius scale
- **Animations**: Timing functions, durations

### 3. Component Variants
- Size variants (sm, md, lg, xl)
- Color variants (primary, secondary, destructive)
- State variants (default, hover, active, disabled, loading)
- Responsive variants (mobile, tablet, desktop)

### 4. Naming Conventions
- Component names (Button, Card, Dialog)
- Variant names (primary-button, card-elevated)
- Design token names (color-primary-500, spacing-4)
- File naming (components/button.tsx, tokens/colors.ts)

### 5. Documentation
- Component usage guidelines
- Design token documentation
- Variant matrix
- Accessibility notes
- Code examples

## Special Abilities
- **Precision Aim**: Never misses a component inconsistency
- **Hunter's Patience**: Thorough analysis, no shortcuts
- **Guardian's Wisdom**: Knows all design system best practices
- **Artemis's Speed**: Fast analysis even for large design systems
- **Amazon Training**: Trained by Wonder Woman in accessibility

---

## 🦸 Superman Integration: Figma-Powered Analysis

Artemis works seamlessly with Superman's Figma integration to provide comprehensive design system analysis!

### How It Works

```python
# Superman extracts from Figma
figma_data = superman_figma_integration.analyze_design_complete(
    figma_url='https://www.figma.com/design/aKLI77flT3sx0kXMPq2BtZ/ATC-RFP',
    figma_token='figd_...'
)

# Artemis validates design system compliance
artemis_result = artemis_design_guardian.validate_design_system(
    figma_data=figma_data,
    target_framework='shadcn/ui'
)

# Combined power!
print(f"Components Found: {figma_data['components']['component_count']}")
print(f"shadcn/ui Coverage: {artemis_result['compliance_score']['coverage_percent']}%")
print(f"Grade: {artemis_result['artemis_score']['grade']}")
```

### Integration with Justice League

When deployed through Superman's coordinator:

```python
mission = {
    'url': 'https://example.com',
    'figma_url': 'https://www.figma.com/design/...',
    'test_design_system': True,  # Artemis deploys!
    'target_framework': 'shadcn/ui'
}

results = superman.assemble_justice_league(mission)

# Artemis results
artemis = results['artemis']
print(f"Artemis Score: {artemis['artemis_score']['score']}/100")
print(f"Missing: {artemis['missing_components']}")
```

---

## 🎯 Artemis's Design System Framework

### Phase 1: Discovery
1. Extract all components from Figma (via Superman)
2. Parse design tokens (colors, typography, spacing)
3. Build component hierarchy
4. Identify component variants

### Phase 2: Validation
1. Map components to target framework (shadcn/ui)
2. Check naming conventions
3. Validate design tokens
4. Verify variant completeness
5. Test accessibility compliance (with Wonder Woman)

### Phase 3: Scoring
1. Calculate component coverage (40 points)
2. Assess design token health (30 points)
3. Check naming compliance (20 points)
4. Evaluate variant completeness (10 points)
5. Generate Artemis Score (0-100)

### Phase 4: Recommendations
1. List missing critical components
2. Identify design token gaps
3. Flag naming inconsistencies
4. Suggest variant additions
5. Prioritize by impact (critical → high → medium → low)

---

## 📊 Artemis Score Breakdown

**Component Coverage (40 points)**
- Core components present (20 points)
- Complete component set (10 points)
- Proper variants (10 points)

**Design Token Health (30 points)**
- Color system completeness (10 points)
- Typography system (10 points)
- Spacing/layout tokens (10 points)

**Naming Compliance (20 points)**
- Convention consistency (15 points)
- Semantic naming (5 points)

**Variant Completeness (10 points)**
- Size variants (4 points)
- State variants (3 points)
- Color variants (3 points)

---

## 🎨 shadcn/ui Validation

Artemis knows all 42+ shadcn/ui components:

**Form & Input (22 components)**
- accordion, alert, alert-dialog, avatar, badge, button, calendar, checkbox
- combobox, command, dialog, drawer, dropdown-menu, form, input, input-otp
- label, radio-group, select, switch, textarea, toggle, toggle-group

**Data Display (10 components)**
- card, table, tabs, tooltip, hover-card, popover, sheet, separator
- breadcrumb, pagination

**Navigation (5 components)**
- menubar, navigation-menu, sidebar, context-menu, scroll-area

**Feedback (5 components)**
- alert, toast, progress, skeleton, sonner

**Charts (7 components)**
- chart, area-chart, bar-chart, line-chart, pie-chart, radar-chart, radial-chart

**Layout (3 components)**
- aspect-ratio, resizable, collapsible

---

## 🏹 Artemis's Recommendations Format

```typescript
{
  priority: 'critical' | 'high' | 'medium' | 'low',
  area: 'Components' | 'Design Tokens' | 'Naming' | 'Variants' | 'Documentation',
  issue: 'Description of the problem',
  recommendation: 'Specific action to take',
  components_affected: string[],
  impact: 'What will improve when fixed',
  artemis_says: 'Motivational message from Artemis'
}
```

Example:
```typescript
{
  priority: 'critical',
  area: 'Components',
  issue: 'Missing button component (most used component)',
  recommendation: 'npx shadcn@latest add button',
  components_affected: ['button'],
  impact: 'Enables primary user interactions',
  artemis_says: 'Every design system needs a button! Add it now! 🎯'
}
```

---

## 🦸‍♀️ Team Synergy

**With Superman 🦸**
- Superman extracts Figma data
- Artemis validates design system compliance
- Combined: Complete Figma → Design System analysis

**With Wonder Woman ⚡**
- Wonder Woman checks accessibility
- Artemis ensures design token accessibility
- Combined: Accessible design systems

**With Cyborg 🤖**
- Cyborg validates design-to-code implementation
- Artemis ensures design system consistency
- Combined: Design system → Code validation

**With Flash ⚡**
- Flash checks performance
- Artemis validates component efficiency
- Combined: Fast, optimized components

---

## 📖 Documentation Generation

Artemis auto-generates design system documentation:

```markdown
# Design System Documentation

## Components (21/42 shadcn/ui)

### ✅ Implemented
- accordion (1 variant)
- avatar (1 variant)
- button (5 variants)
- ...

### ❌ Missing
- checkbox
- radio-group
- badge
- ...

## Design Tokens

### Colors
- Primary: #3B82F6
- Secondary: #10B981
- ...

### Typography
- Font: Inter
- Sizes: 12px, 14px, 16px, 18px, 24px, 32px
- ...

## Recommendations
1. Add missing checkbox component
2. Create color tokens for semantic colors
3. ...
```

---

**Hero Status:** ✅ READY TO DEPLOY
**Integration:** 🦸 Works with Superman's Figma extraction
**Coverage:** 🎯 All 42+ shadcn/ui components
**Scoring:** 📊 0-100 with detailed breakdown
**Documentation:** 📖 Auto-generated design system docs

---

*"With precision and grace, Artemis guards your design system truth!" 🎨🏹*
