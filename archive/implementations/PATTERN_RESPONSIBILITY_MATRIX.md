# 🎯 Pattern Responsibility Matrix - Justice League

**Created**: October 23, 2025
**Purpose**: Define who is responsible for ensuring reusable patterns are identified and applied across multiple screens from the same Figma project

---

## 🚨 Problem Identified

**User Observation**: "These are screens from the same project hence it will have similar reusable patterns like menu bars etc, so you need to keep an eye. Who is going to take responsibility to ensure these are taken into consideration so the output would be better?"

**Current Issue**:
- Settings and SettingsProfile both have the same header, navigation, sidebar
- Both components generate these elements independently
- No shared component extraction
- Potential for inconsistencies
- Duplication of code

---

## 👥 Responsibility Matrix

### 1. 🔮 Oracle - Project-Level Pattern Guardian

**PRIMARY RESPONSIBILITY**: Cross-component pattern detection and enforcement

**Oracle's Duties**:
- ✅ Track all conversions from the same Figma project
- ✅ Identify common elements across multiple screens (navigation, headers, sidebars)
- ✅ Maintain project-level pattern library
- ✅ Alert Artemis when shared components should be extracted
- ✅ Enforce consistency across conversions from same project
- ✅ Store project metadata (file_key, design system, brand colors)

**Knowledge Files Oracle Manages**:
```
oracle/
├── project_patterns.json          ← NEW! Project-level patterns
├── shared_components.json         ← NEW! Reusable components
├── figma_project_metadata.json    ← NEW! Project info
└── cross_component_insights.json  ← NEW! Shared element tracking
```

**Oracle's Pattern Detection Algorithm**:
1. When conversion starts, check: "Is this from a known Figma project?"
2. If yes: Load existing patterns from that project
3. Compare new screen with previous conversions from same project
4. Identify shared elements (navigation, headers, sidebars)
5. Recommend extracting shared components
6. Update project-level pattern library

---

### 2. 🎨 Artemis - Component Pattern Expert

**SECONDARY RESPONSIBILITY**: Apply project-level patterns during conversion

**Artemis's Duties**:
- ✅ Query Oracle for project-level patterns before generation
- ✅ Identify which elements are shared vs. unique
- ✅ Generate shared components separately (Layout, Navigation, Header)
- ✅ Compose screens using shared components
- ✅ Extract new reusable patterns and report to Oracle
- ✅ Ensure consistency with previous screens from same project

**Artemis's Enhanced Workflow**:
```python
def generate_component_code_expert():
    # 1. Extract Figma file_key from URL
    file_key = extract_file_key(figma_url)

    # 2. Query Oracle: "Do we have patterns from this project?"
    project_patterns = oracle.get_project_patterns(file_key)

    # 3. If patterns exist, identify shared elements
    if project_patterns:
        shared_components = identify_shared_elements(
            current_screen,
            project_patterns['common_elements']
        )

    # 4. Generate code:
    #    - Reuse shared components
    #    - Generate unique elements
    #    - Compose final component

    # 5. Update Oracle with new insights
    oracle.update_project_patterns(file_key, new_patterns)
```

---

### 3. 🦸 Superman - Mission Coordinator

**SUPPORTING RESPONSIBILITY**: Orchestrate cross-component consistency

**Superman's Duties**:
- ✅ Before deploying Artemis, check with Oracle for project context
- ✅ Coordinate multi-screen conversions from same project
- ✅ Ensure all conversions from same project use shared components
- ✅ Report cross-component inconsistencies

---

## 📊 Project-Level Pattern Library Structure

### Example: poc-test Project (6Pmf9gCcUccyqbCO9nN6Ts)

```json
{
  "figma_file_key": "6Pmf9gCcUccyqbCO9nN6Ts",
  "project_name": "poc test",
  "conversions_count": 2,
  "shared_components": {
    "AppHeader": {
      "description": "Top navigation with logo, menu, upgrade button, avatar",
      "used_in": ["Settings", "SettingsProfile"],
      "props": ["currentPage"],
      "file": "components/layout/AppHeader.tsx",
      "elements": [
        "Logo (Z in black square)",
        "Navigation (Dashboard, Orders, Products, Customers, Settings)",
        "Upgrade button (black with lightning)",
        "User avatar (gradient)"
      ]
    },
    "SettingsSidebar": {
      "description": "Settings navigation sidebar",
      "used_in": ["Settings", "SettingsProfile"],
      "props": ["activePage"],
      "file": "components/layout/SettingsSidebar.tsx",
      "elements": [
        "Profile", "Account", "Members",
        "Billing", "Invoices", "API"
      ]
    },
    "AppLayout": {
      "description": "Main layout wrapper with header",
      "used_in": ["Settings", "SettingsProfile"],
      "props": ["children"],
      "file": "components/layout/AppLayout.tsx"
    }
  },
  "design_system": {
    "colors": {
      "primary_black": "#000000",
      "primary_white": "#FFFFFF",
      "background": "#fafafa",
      "surface": "#ffffff",
      "border": "#e5e7eb",
      "text_primary": "#18181b",
      "text_secondary": "#71717a"
    },
    "spacing": {
      "standard": "24px",
      "tailwind": "6"
    },
    "typography": {
      "heading_xl": "text-3xl font-bold",
      "heading_lg": "text-xl font-semibold",
      "body": "text-sm"
    }
  },
  "common_patterns": [
    "full-width-divider",
    "sidebar-layout",
    "24px-spacing",
    "black-cta-buttons",
    "form-field-styling"
  ]
}
```

---

## 🔄 Enhanced Conversion Workflow

### Step-by-Step Process

**1. User Requests Conversion**
```
User: "Convert this Figma frame: https://figma.com/design/6Pmf.../node-id=17-1440"
```

**2. Superman Coordinator Starts**
```python
superman = SupermanCoordinator()

# Extract Figma file_key
file_key = "6Pmf9gCcUccyqbCO9nN6Ts"

# Ask Oracle: "Do we know this project?"
project_context = oracle.get_project_context(file_key)
```

**3. Oracle Responds**
```json
{
  "project_known": true,
  "conversions_count": 1,
  "shared_components": ["AppHeader", "SettingsSidebar"],
  "design_system": { ... },
  "recommendation": "Reuse AppHeader and SettingsSidebar components"
}
```

**4. Superman Deploys Artemis with Context**
```python
result = artemis.generate_component_code_expert(
    figma_url=url,
    component_name="SettingsProfile",
    project_context=project_context  # ← NEW!
)
```

**5. Artemis Generates Code**
```typescript
// Instead of duplicating header:
import AppHeader from '@/components/layout/AppHeader';
import SettingsSidebar from '@/components/layout/SettingsSidebar';
import AppLayout from '@/components/layout/AppLayout';

export default function SettingsProfile() {
  return (
    <AppLayout>
      <AppHeader currentPage="Settings" />
      <div className="flex gap-6">
        <SettingsSidebar activePage="Profile" />
        <main className="flex-1">
          {/* Unique content here */}
        </main>
      </div>
    </AppLayout>
  );
}
```

**6. Oracle Updates Project Library**
```python
oracle.record_conversion(
    file_key="6Pmf9gCcUccyqbCO9nN6Ts",
    component_name="SettingsProfile",
    shared_components_used=["AppHeader", "SettingsSidebar", "AppLayout"],
    new_patterns_discovered=[]
)
```

---

## ✅ Benefits of This System

### Code Quality
- ✅ **DRY Principle**: Don't Repeat Yourself - shared components extracted once
- ✅ **Consistency**: All screens use same navigation, header, sidebar
- ✅ **Maintainability**: Update header once, all screens benefit
- ✅ **Type Safety**: Shared component props are consistent

### Development Speed
- ✅ **Faster Conversions**: Reuse existing components instead of regenerating
- ✅ **Fewer Iterations**: Less debugging when components are proven
- ✅ **Automatic Consistency**: Oracle ensures patterns are followed

### Knowledge Growth
- ✅ **Project-Level Learning**: Each conversion improves project understanding
- ✅ **Design System Extraction**: Automatically builds design system
- ✅ **Cross-Component Insights**: Learn from multiple screens

---

## 🎯 Implementation Checklist

### Phase 1: Oracle Enhancement
- [ ] Create `oracle/project_patterns.json`
- [ ] Create `oracle/shared_components.json`
- [ ] Add `get_project_context(file_key)` method to Oracle
- [ ] Add `update_project_patterns(file_key, patterns)` method
- [ ] Add project-level pattern detection algorithm

### Phase 2: Artemis Enhancement
- [ ] Update `generate_component_code_expert()` to accept `project_context`
- [ ] Add `identify_shared_elements()` method
- [ ] Add shared component extraction logic
- [ ] Update generation to compose with shared components

### Phase 3: Superman Enhancement
- [ ] Extract `file_key` from Figma URL
- [ ] Query Oracle for project context before deploying Artemis
- [ ] Pass project context to Artemis

### Phase 4: Shared Component Library
- [ ] Create `components/layout/AppHeader.tsx`
- [ ] Create `components/layout/SettingsSidebar.tsx`
- [ ] Create `components/layout/AppLayout.tsx`
- [ ] Refactor Settings.tsx to use shared components
- [ ] Refactor SettingsProfile.tsx to use shared components

---

## 📝 Responsibility Summary

| Aspect | Oracle | Artemis | Superman |
|--------|--------|---------|----------|
| **Detect project patterns** | ✅ Primary | ❌ | ❌ |
| **Track cross-component reuse** | ✅ Primary | ❌ | ❌ |
| **Store project metadata** | ✅ Primary | ❌ | ❌ |
| **Apply patterns in generation** | ❌ | ✅ Primary | ❌ |
| **Extract shared components** | ❌ | ✅ Primary | ❌ |
| **Report new patterns** | ❌ | ✅ Primary | ❌ |
| **Orchestrate consistency** | ❌ | ❌ | ✅ Primary |
| **Coordinate multi-screen** | ❌ | ❌ | ✅ Primary |

---

## 🌟 Future Vision

With this system in place:

**Conversion #1** (Settings):
- Generates full header, sidebar, content
- Takes 8 iterations to get right

**Conversion #2** (SettingsProfile):
- Oracle: "I know this project! Reuse header and sidebar from Settings"
- Artemis: Composes with shared components
- Takes 1 iteration (only unique content needs work)

**Conversion #3** (any other screen):
- Oracle: "Use AppHeader, SettingsSidebar, AppLayout"
- Artemis: Generates only unique screen content
- Takes <1 iteration (proven components)

**Result**:
- ⚡ **3x faster** conversions
- ✅ **100% consistent** UI across all screens
- 🎯 **Maintainable** codebase with shared components

---

**"One pattern, infinite screens. That's the Oracle way."** 🔮✨

Oracle + Artemis + Superman = Complete Project-Level Pattern Management
