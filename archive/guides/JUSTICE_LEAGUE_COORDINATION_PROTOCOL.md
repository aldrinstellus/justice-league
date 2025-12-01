# 🦸 JUSTICE LEAGUE COORDINATION PROTOCOL

**Version**: 2.0
**Date**: October 23, 2025
**Status**: ✅ ACTIVE

---

## Overview

This document defines the official coordination protocol for all Justice League members in the Figma-to-Code conversion pipeline. All agents must follow this protocol to ensure seamless collaboration and pixel-perfect output.

---

## Justice League Roster (15 Active Heroes)

### Core Conversion Team

| Hero | Role | Primary Responsibility | MCP Servers |
|------|------|----------------------|-------------|
| 🦸 **Superman** | Coordinator | Orchestrate all missions, manage workflow | None (delegates) |
| 🔮 **Oracle** | Pattern Tracker | Track project patterns, provide context | None (data only) |
| 🎨 **Artemis** | Code Generator | Generate pixel-perfect React/Next.js code | Figma MCP, shadcn MCP |
| 🎯 **Green Arrow** | Visual Validator | Validate WYSIWYG accuracy (spacing, colors, typography) | Figma MCP, Chrome DevTools MCP, Tailwind MCP, shadcn MCP |

### Quality Assurance Team

| Hero | Role | Primary Responsibility | MCP Servers |
|------|------|----------------------|-------------|
| 🦇 **Batman** | Interactive Testing | Test all interactive elements (clicks, forms) | Chrome DevTools MCP |
| 💚 **Green Lantern** | Visual Regression | Compare screenshots for visual changes | None (baseline comparison) |
| ⚡ **Wonder Woman** | Accessibility | WCAG 2.2 compliance, screen reader support | Chrome DevTools MCP |
| ⚡ **Flash** | Performance | Page load speed, Core Web Vitals | Chrome DevTools MCP (Performance Profiler) |

### Integration & Security Team

| Hero | Role | Primary Responsibility | MCP Servers |
|------|------|----------------------|-------------|
| 🌊 **Aquaman** | Network Analysis | API calls, network timing, resource loading | Chrome DevTools MCP (Network) |
| 🤖 **Cyborg** | Integrations | Third-party API integration checks | None |
| 🧠 **Martian Manhunter** | Security | XSS, CSRF, security vulnerabilities | None |

### UI/UX Excellence Team

| Hero | Role | Primary Responsibility | MCP Servers |
|------|------|----------------------|-------------|
| 🔬 **The Atom** | Component Analysis | Component library validation | None |
| 🤸 **Plastic Man** | Responsive Design | Mobile, tablet, desktop breakpoints | Chrome DevTools MCP (Device Emulation) |
| 🎩 **Zatanna** | SEO & Metadata | Meta tags, Open Graph, schema markup | Chrome DevTools MCP |
| 🪔 **Litty** | Ethics & Empathy | Dark patterns, user ethics validation | None |

---

## Figma-to-Code Conversion Workflow

### Complete Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    1. MISSION INITIATION                         │
│  🦸 Superman receives Figma URL + component name + requirements │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  2. ORACLE KNOWLEDGE QUERY                       │
│  🔮 Oracle checks if project is known                           │
│     - Extract file_key from Figma URL                          │
│     - Query project patterns database                           │
│     - Return: shared_components, design_system, patterns        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   3. ARTEMIS CODE GENERATION                     │
│  🎨 Artemis generates component code                            │
│     - Use Figma MCP to extract design specs                    │
│     - Apply project_context from Oracle (if available)         │
│     - Generate React/Next.js + TypeScript code                 │
│     - Use shadcn/ui components                                  │
│     - Apply Tailwind CSS utility classes                       │
│     - Expert Mode: Self-healing with max 3 iterations          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                4. GREEN ARROW VISUAL VALIDATION                  │
│  🎯 Green Arrow validates pixel-perfect accuracy                │
│     Step 1: Extract Figma specs (Figma MCP)                    │
│     Step 2: Inspect rendered component (Chrome DevTools MCP)   │
│     Step 3: Extract Tailwind classes from code                 │
│     Step 4: Validate Tailwind (Tailwind MCP)                   │
│     Step 5: Validate shadcn usage (shadcn MCP)                 │
│     Step 6: Compare & calculate accuracy score (0-100%)        │
│     Step 7: Generate validation report                          │
│                                                                  │
│  Accuracy Thresholds:                                           │
│   • 98-100% → ✅ EXCELLENT (proceed)                           │
│   • 95-97%  → ✅ GOOD (proceed)                                │
│   • 90-94%  → ⚠️  ACCEPTABLE (proceed with notes)              │
│   • <90%    → ❌ NEEDS WORK (return to Artemis)                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  5. ORACLE PATTERN UPDATE                        │
│  🔮 Oracle records new patterns from conversion                 │
│     - Update project_patterns.json with:                       │
│       * component_name, node_id, timestamp                     │
│       * shared_elements detected                                │
│       * design tokens (colors, spacing, typography)            │
│       * common patterns (layouts, components)                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              6. OPTIONAL: FULL JUSTICE LEAGUE ASSEMBLY           │
│  🦸 Superman deploys additional heroes (if requested)           │
│     - 🦇 Batman: Interactive testing                            │
│     - 💚 Green Lantern: Visual regression                       │
│     - ⚡ Wonder Woman: Accessibility                            │
│     - ⚡ Flash: Performance                                     │
│     - 🌊 Aquaman: Network analysis                              │
│     - 🧠 Martian Manhunter: Security scan                       │
│     - 🤸 Plastic Man: Responsive design                         │
│     - 🎩 Zatanna: SEO validation                                │
│     - 🪔 Litty: Ethics check                                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      7. MISSION COMPLETE                         │
│  🦸 Superman generates final report                             │
│     - Component code files                                      │
│     - Artemis accuracy score                                    │
│     - Green Arrow validation report                             │
│     - Optional: Full Justice League scores                      │
│     - Installation commands                                     │
│     - Deployment recommendations                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Coordination Rules

### Rule 1: Oracle-First Protocol

**Before any code generation:**

1. Superman MUST query Oracle for project context
2. Extract `file_key` from Figma URL using regex: `figma\.com/(?:design|file)/([a-zA-Z0-9]+)`
3. Call `oracle.get_project_context(file_key)`
4. Pass `project_context` to Artemis

**Why**: Ensures pattern reuse and DRY principles across multi-screen projects.

### Rule 2: Artemis Generation Standards

**Artemis MUST:**

1. Accept `project_context` parameter in both methods:
   - `generate_component_code()`
   - `generate_component_code_expert()`

2. Use Oracle context when available:
   ```python
   if project_context and project_context.get('project_known'):
       shared_components = project_context.get('shared_components', [])
       # Reuse shared components in generation
   ```

3. Use Expert Mode by default:
   - `max_iterations=3`
   - `target_accuracy=98.0%`
   - Self-healing enabled

4. Follow design system rules:
   - Use shadcn/ui components exclusively
   - Apply Tailwind CSS utility classes
   - Match exact Figma spacing, colors, typography
   - Extract and reuse design tokens

### Rule 3: Green Arrow Validation Protocol

**Green Arrow MUST validate every conversion:**

1. Run validation immediately after Artemis generation
2. Use all 4 MCP servers in sequence:
   - Figma MCP → Extract design specs
   - Chrome DevTools MCP → Inspect rendered output
   - Tailwind MCP → Validate utility classes
   - shadcn MCP → Check component compliance

3. Calculate accuracy score with tolerance levels:
   - Spacing: ±2px tolerance
   - Sizing: ±2px tolerance
   - Position: ±1px tolerance
   - Colors: 0px tolerance (exact match)
   - Typography: 0px tolerance (exact match)

4. Generate comprehensive validation report:
   - Measurements comparison table
   - Colors comparison table
   - Typography comparison table
   - Spacing comparison table
   - Tailwind validation results
   - shadcn usage validation
   - List of discrepancies with severity
   - Recommendations for fixes

5. **Decision Matrix**:
   - Score ≥90% → APPROVE and proceed
   - Score <90% → RETURN to Artemis with discrepancy list

### Rule 4: Oracle Update Protocol

**After successful conversion:**

1. Superman MUST update Oracle with new patterns
2. Extract `node_id` from Figma URL using regex: `node-id=([^&]+)`
3. Call `oracle.update_project_patterns()` with:
   - `file_key`: Figma project ID
   - `component_name`: Generated component name
   - `node_id`: Figma node ID
   - `new_shared_elements`: Detected reusable components
   - `new_patterns`: Layout/design patterns found

**Why**: Enables continuous learning for future conversions.

### Rule 5: Superman Coordination Standards

**Superman MUST:**

1. Import correct agent modules:
   ```python
   from .green_arrow_visual_validator import GreenArrowVisualValidator  # ✅ CORRECT
   from .oracle_meta_agent import OracleMeta  # ✅ REQUIRED
   ```

2. Initialize all agents in `__init__`:
   ```python
   self.oracle = OracleMeta() if ORACLE_AVAILABLE else None
   self.green_arrow = GreenArrowVisualValidator(validation_dir) if GREEN_ARROW_VISUAL_AVAILABLE else None
   self.artemis = ArtemisCodeSmith(expert_mode=True) if ARTEMIS_AVAILABLE else None
   ```

3. Follow deployment sequence in `_deploy_artemis()`:
   - STEP 1: Query Oracle for project context
   - STEP 2: Deploy Artemis with context
   - STEP 3: Deploy Green Arrow for validation
   - STEP 4: Update Oracle with new patterns

4. Pass complete mission parameters:
   ```python
   mission = {
       'figma_url': 'https://...',
       'component_name': 'ComponentName',
       'framework': 'next',
       'language': 'typescript',
       'expert_mode': True,
       'rendered_url': 'http://localhost:3005/component-name',  # REQUIRED for Green Arrow
       'options': {},
       'max_iterations': 3,
       'target_accuracy': 98.0
   }
   ```

---

## MCP Server Access Matrix

| Hero | Figma MCP | Chrome DevTools MCP | Tailwind MCP | shadcn MCP |
|------|-----------|-------------------|--------------|------------|
| 🎨 Artemis | ✅ Primary | ❌ | ❌ | ✅ Secondary |
| 🎯 Green Arrow | ✅ Primary | ✅ Primary | ✅ Primary | ✅ Primary |
| 🦇 Batman | ❌ | ✅ Primary | ❌ | ❌ |
| 💚 Green Lantern | ❌ | ❌ | ❌ | ❌ |
| ⚡ Wonder Woman | ❌ | ✅ Secondary | ❌ | ❌ |
| ⚡ Flash | ❌ | ✅ Primary (Perf) | ❌ | ❌ |
| 🌊 Aquaman | ❌ | ✅ Primary (Network) | ❌ | ❌ |
| 🤸 Plastic Man | ❌ | ✅ Secondary | ❌ | ❌ |
| 🎩 Zatanna | ❌ | ✅ Secondary | ❌ | ❌ |

**Legend**:
- ✅ Primary: Core functionality depends on this MCP
- ✅ Secondary: Enhanced functionality uses this MCP
- ❌: No access needed

---

## Communication Protocols

### Superman → Oracle

```python
# Query for project context
project_context = oracle.get_project_context(file_key)

# Response format
{
    'project_known': bool,
    'conversions_count': int,
    'shared_components': ['AppHeader', 'SettingsSidebar', ...],
    'design_system': {
        'colors': {...},
        'spacing': {...},
        'typography': {...}
    },
    'common_patterns': ['full-width-divider', 'sidebar-layout', ...],
    'recommendation': str
}
```

### Superman → Artemis

```python
# Pass project context to Artemis
result = artemis.generate_component_code_expert(
    figma_url=figma_url,
    component_name=component_name,
    framework='next',
    language='typescript',
    options={},
    max_iterations=3,
    target_accuracy=98.0,
    project_context=project_context  # Oracle context
)

# Response format
{
    'success': bool,
    'files': {...},
    'code': str,
    'accuracy_score': float,
    'expert_rating': str,
    'iterations': int,
    'shared_elements': {...},
    'patterns_detected': [...]
}
```

### Artemis → Green Arrow (via Superman)

```python
# Deploy Green Arrow for validation
green_arrow_result = green_arrow.validate_component(
    figma_url=figma_url,
    rendered_url='http://localhost:3005/component-name',
    component_name=component_name,
    component_code=artemis_result['code']
)

# Response format
{
    'accuracy_score': float,  # 0-100
    'status': str,  # 'EXCELLENT', 'GOOD', 'ACCEPTABLE', 'NEEDS WORK', 'FAILED'
    'discrepancies': [
        {
            'category': 'spacing',
            'property': 'padding',
            'figma_value': '24px',
            'rendered_value': '20px',
            'difference': '4px',
            'severity': 'LOW'
        }
    ],
    'tailwind_validation': {...},
    'shadcn_validation': {...},
    'recommendations': [...]
}
```

### Superman → Oracle (Update)

```python
# Update Oracle after conversion
oracle.update_project_patterns(
    file_key=file_key,
    component_name=component_name,
    node_id=node_id,
    new_shared_elements=artemis_result.get('shared_elements'),
    new_patterns=artemis_result.get('patterns_detected')
)

# Oracle stores this in:
# - data/oracle_project_patterns.json
# - data/oracle_shared_components.json
```

---

## Error Handling & Fallbacks

### Oracle Not Available

```python
if not ORACLE_AVAILABLE:
    logger.warning("🔮 Oracle not available - proceeding without project context")
    project_context = None
    # Continue with standard generation
```

**Impact**: No pattern reuse, may duplicate shared components.

### Green Arrow Not Available

```python
if not GREEN_ARROW_VISUAL_AVAILABLE:
    logger.warning("🎯 Green Arrow not available - skipping visual validation")
    # Deploy component without validation
```

**Impact**: No WYSIWYG guarantee, potential pixel mismatches.

### Artemis Expert Mode Fails

```python
try:
    result = artemis.generate_component_code_expert(...)
except Exception as e:
    logger.error(f"❌ Expert mode failed: {e}")
    # Fallback to standard generation
    result = artemis.generate_component_code(...)
```

**Impact**: Reduced accuracy, no self-healing.

### Green Arrow Validation Fails

```python
if green_arrow_result['accuracy_score'] < 90:
    logger.warning("⚠️ Accuracy below 90% - consider refinement")
    # Options:
    # 1. Return to Artemis for fixes (if iterations < max_iterations)
    # 2. Deploy with warnings
    # 3. Manual review required
```

**Impact**: Component may not match Figma design exactly.

---

## Best Practices

### For Superman (Coordinator)

1. ✅ Always query Oracle before deploying Artemis
2. ✅ Always deploy Green Arrow after Artemis (if rendered_url provided)
3. ✅ Always update Oracle after successful conversion
4. ✅ Pass complete mission parameters to all agents
5. ✅ Log all coordination steps for audit trail
6. ⚠️ Handle agent unavailability gracefully
7. ⚠️ Never skip Green Arrow validation unless unavoidable

### For Artemis (Code Generator)

1. ✅ Always accept and use `project_context` parameter
2. ✅ Check for shared components in project_context
3. ✅ Reuse shared components when detected
4. ✅ Extract and return `shared_elements` and `patterns_detected`
5. ✅ Use Expert Mode for production conversions
6. ✅ Apply exact Figma values (spacing, colors, typography)
7. ⚠️ Never use inline styles - always Tailwind classes
8. ⚠️ Never use native HTML - always shadcn components

### For Green Arrow (Visual Validator)

1. ✅ Always validate all 4 aspects: measurements, colors, typography, spacing
2. ✅ Use all 4 MCP servers in validation pipeline
3. ✅ Apply proper tolerance levels (±2px spacing, 0px colors)
4. ✅ Generate detailed discrepancy reports
5. ✅ Provide actionable recommendations for fixes
6. ⚠️ Never approve components with <90% accuracy without warnings
7. ⚠️ Never skip Tailwind or shadcn validation steps

### For Oracle (Pattern Tracker)

1. ✅ Always track conversions by Figma file_key
2. ✅ Always detect and record shared elements
3. ✅ Always extract design system tokens
4. ✅ Always provide recommendations for reuse
5. ✅ Maintain immutable audit trail (never delete records)
6. ⚠️ Never return project_context without validating file_key exists

---

## Testing & Validation

### Integration Tests Required

1. **Oracle → Artemis Integration**:
   ```python
   # Test that project_context is passed correctly
   assert 'shared_components' in artemis_result
   assert artemis_result['project_context_used'] == True
   ```

2. **Artemis → Green Arrow Integration**:
   ```python
   # Test that Green Arrow receives correct inputs
   assert green_arrow_result['accuracy_score'] >= 0
   assert green_arrow_result['accuracy_score'] <= 100
   assert 'status' in green_arrow_result
   ```

3. **Green Arrow → Oracle Integration** (via Superman):
   ```python
   # Test that Oracle is updated after validation
   updated_context = oracle.get_project_context(file_key)
   assert updated_context['conversions_count'] > 0
   ```

### End-to-End Test

```python
# Complete workflow test
mission = {
    'figma_url': 'https://figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=17-1440',
    'component_name': 'TestComponent',
    'rendered_url': 'http://localhost:3005/test-component',
    'framework': 'next',
    'expert_mode': True
}

superman = SupermanCoordinator()
result = superman._deploy_artemis(mission)

# Assertions
assert result['success'] == True
assert 'green_arrow_validation' in result
assert result['green_arrow_validation']['accuracy_score'] >= 90
```

---

## Versioning & Updates

### Current Version: 2.0 (October 23, 2025)

**Major Changes from 1.0**:
1. ✅ Added Oracle integration throughout workflow
2. ✅ Replaced Green Arrow Testing with Green Arrow Visual Validator
3. ✅ Enhanced Artemis with `project_context` parameter
4. ✅ Added Green Arrow 4-MCP validation pipeline
5. ✅ Defined complete coordination protocols

**Breaking Changes**:
- `green_arrow_testing.py` deprecated → use `green_arrow_visual_validator.py`
- Artemis methods now require `project_context` parameter (optional)
- Superman `_deploy_artemis` now requires `rendered_url` in mission

### Future Enhancements (v3.0 Roadmap)

1. **Automated Refactoring**: If Green Arrow score <90%, auto-trigger Artemis refinement
2. **Cross-Browser Validation**: Green Arrow validates in Chrome, Firefox, Safari
3. **Visual Regression Automation**: Auto-run Green Lantern after Green Arrow
4. **Performance Integration**: Green Arrow + Flash combined scoring
5. **AI Learning**: Oracle uses ML to predict patterns from historical data

---

## Quick Reference

### Critical Imports

```python
# In superman_coordinator.py
from .green_arrow_visual_validator import GreenArrowVisualValidator  # ✅
from .oracle_meta_agent import OracleMeta  # ✅
from .artemis_codesmith import ArtemisCodeSmith  # ✅
```

### Critical Method Signatures

```python
# Artemis
def generate_component_code_expert(
    figma_url: str,
    component_name: str,
    project_context: Optional[Dict[str, Any]] = None  # ✅ REQUIRED
) -> Dict[str, Any]

# Green Arrow
def validate_component(
    figma_url: str,
    rendered_url: str,
    component_name: str,
    component_code: str
) -> Dict[str, Any]

# Oracle
def get_project_context(file_key: str) -> Dict[str, Any]
def update_project_patterns(file_key: str, component_name: str, node_id: str, ...) -> bool
```

### Critical Workflow Steps

1. **Query Oracle** → `oracle.get_project_context(file_key)`
2. **Deploy Artemis** → `artemis.generate_component_code_expert(..., project_context=context)`
3. **Deploy Green Arrow** → `green_arrow.validate_component(...)`
4. **Update Oracle** → `oracle.update_project_patterns(...)`

---

## Troubleshooting

### Issue: Oracle not tracking conversions

**Symptoms**: `project_known` always returns False

**Solution**:
```python
# Check Oracle database files exist
ls -la data/oracle_project_patterns.json
ls -la data/oracle_shared_components.json

# Verify update_project_patterns is called after conversion
grep "update_project_patterns" core/justice_league/superman_coordinator.py
```

### Issue: Green Arrow always fails validation

**Symptoms**: Accuracy score always <90%

**Solution**:
```python
# Check rendered_url is accessible
curl http://localhost:3005/component-name

# Verify all 4 MCP servers are available
# Check Green Arrow initialization logs
```

### Issue: Artemis ignores project_context

**Symptoms**: Shared components not reused

**Solution**:
```python
# Verify Artemis receives context
assert project_context is not None
assert project_context.get('project_known') == True

# Check Artemis method signature includes project_context
grep "def generate_component_code_expert" core/justice_league/artemis_codesmith.py
```

---

## Appendix

### A. Figma URL Patterns

```regex
# File key extraction
figma\.com/(?:design|file)/([a-zA-Z0-9]+)

# Node ID extraction
node-id=([^&]+)

# Examples
https://figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=17-1440
  file_key: 6Pmf9gCcUccyqbCO9nN6Ts
  node_id: 17-1440
```

### B. Accuracy Score Calculation

```python
# Green Arrow scoring formula
total_checks = (
    measurements_checks +
    colors_checks +
    typography_checks +
    spacing_checks +
    tailwind_checks +
    shadcn_checks
)

passed_checks = sum(check.passed for check in all_checks)

accuracy_score = (passed_checks / total_checks) * 100

# Grade assignment
if accuracy_score >= 98: grade = "EXCELLENT"
elif accuracy_score >= 95: grade = "GOOD"
elif accuracy_score >= 90: grade = "ACCEPTABLE"
elif accuracy_score >= 85: grade = "NEEDS WORK"
else: grade = "FAILED"
```

### C. Oracle Database Schema

**data/oracle_project_patterns.json**:
```json
{
  "projects": {
    "6Pmf9gCcUccyqbCO9nN6Ts": {
      "project_name": "poc test",
      "conversions": [
        {
          "component_name": "Settings",
          "node_id": "17-1439",
          "timestamp": "2025-10-23T20:00:00Z",
          "shared_elements": ["AppHeader", "SettingsSidebar"]
        }
      ],
      "design_system": {...},
      "common_patterns": [...]
    }
  }
}
```

**data/oracle_shared_components.json**:
```json
{
  "components": {
    "AppHeader": {
      "status": "extracted",
      "file_path": "preview-app/src/components/layout/AppHeader.tsx",
      "first_seen": "2025-10-23T20:00:00Z",
      "usage_count": 2,
      "projects": ["6Pmf9gCcUccyqbCO9nN6Ts"]
    }
  }
}
```

---

**"Together, we are the Justice League! No design flaw escapes us!"** 🦸✨

---

*Last Updated: October 23, 2025*
*Coordinator: Superman*
*Protocol Approved By: Oracle, Artemis, Green Arrow*
