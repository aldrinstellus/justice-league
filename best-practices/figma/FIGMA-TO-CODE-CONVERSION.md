# Figma-to-Code Conversion

**Problem Domain**: Converting Figma designs to production React/Tailwind code
**Status**: Partially solved - needs iteration
**Priority**: High

---

## The Problem Statement

### What We Want
Convert Figma designs to React components with:
- 99%+ visual accuracy (pixel-perfect)
- Full automation (no manual steps)
- Scalability (100+ files/frames)
- Production-ready code (Tailwind, TypeScript, accessibility)

### What We Have Today

| Capability | Accuracy | Automation | Scale |
|------------|----------|------------|-------|
| Manual CSS paste | 99%+ | None | 1 at a time |
| Figma REST API | 90-95% | Full | Unlimited |
| Figma MCP Server | 90-95% | Full | Unlimited |
| Third-party tools (Anima, Locofy) | 80-90% | Full | Limited |

### The Gap

**No solution exists that provides all three**: 99% accuracy + full automation + scale

---

## Current Solutions

### Solution A: Manual CSS Paste (Single Use)

**Best for**: Demo, critical components, one-off conversions

**Workflow**:
```
1. Open Figma Desktop/Web
2. Select frame
3. Right-click → Copy/Paste as → Copy as code → CSS (all layers)
4. Paste to Claude
5. Claude converts to React/Tailwind
6. Verify with Chrome MCP screenshot
```

**Pros**:
- 99%+ accuracy (Figma's own CSS export)
- All layers included with exact values
- Auto-layout → flexbox conversion built-in
- Works with any Figma design

**Cons**:
- Manual per-frame (doesn't scale)
- Requires Figma Desktop/Web open
- No programmatic access to "Copy as code"

**Code Flow**:
```
Figma Frame
    │
    ▼ (Manual: Copy as code → CSS all layers)
CSS Text
    │
    ▼ (Claude: Parse & Convert)
React Component
    │
    ▼ (MCP: Screenshot verification)
Visual Proof
```

---

### Solution B: Figma REST API (Automated)

**Best for**: Bulk exports, automated pipelines, 100+ files

**Workflow**:
```python
# 1. Get file structure
GET https://api.figma.com/v1/files/{file_key}

# 2. Get node details
GET https://api.figma.com/v1/files/{file_key}/nodes?ids={node_ids}

# 3. Reconstruct CSS from properties
node = response['nodes'][node_id]
css = reconstruct_css(node)  # 90-95% accuracy

# 4. Convert to React
react_code = convert_to_react(css)
```

**What API Provides**:
```json
{
  "id": "123:456",
  "name": "ProfileCard",
  "type": "FRAME",
  "absoluteBoundingBox": { "x": 0, "y": 0, "width": 320, "height": 200 },
  "fills": [{ "type": "SOLID", "color": { "r": 1, "g": 1, "b": 1 } }],
  "strokes": [],
  "cornerRadius": 12,
  "paddingLeft": 24,
  "paddingRight": 24,
  "paddingTop": 24,
  "paddingBottom": 24,
  "itemSpacing": 16,
  "layoutMode": "VERTICAL",
  "children": [...]
}
```

**What We Reconstruct**:
```css
.profile-card {
  width: 320px;
  height: 200px;
  background: #FFFFFF;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
```

**Pros**:
- Fully automated
- Scales to 100+ files
- Rate-limited but reliable (1.2s between calls)
- FREE (no per-frame cost)

**Cons**:
- 90-95% accuracy (not pixel-perfect)
- Missing some CSS properties
- Effects (shadows, blurs) need manual mapping
- Complex gradients may not convert correctly

---

### Solution C: Figma MCP Server (Automated)

**Best for**: Claude Code integration, interactive queries

**Available Tools**:
- `get_file_info` - File metadata and structure
- `get_node_info` - Detailed node properties
- `get_styles` - Design system styles
- `get_components` - Reusable components
- `get_variables` - Design tokens/variables

**Same limitations as REST API** - no "Copy as code" equivalent

---

### Solution D: Hybrid (Production Pipeline)

**Best for**: Production use with quality requirements

**Workflow**:
```
1. Automated: Figma API extracts all frames (90-95%)
2. Automated: Claude converts to React components
3. Automated: Chrome MCP takes screenshots
4. Manual: QA review of 5-10% critical components
5. Manual: Fix any accuracy issues
```

**Accuracy**: 95-99% (API + human QA)
**Automation**: 90% (only final QA is manual)

---

## Accuracy Comparison by Property

| CSS Property | Manual CSS | API Reconstruction |
|--------------|------------|-------------------|
| Width/Height | 100% | 100% |
| Padding/Margin | 100% | 100% |
| Border Radius | 100% | 100% |
| Background Color | 100% | 100% |
| Flexbox Layout | 100% | 95% |
| Gap/Spacing | 100% | 100% |
| Font Family | 100% | 95% |
| Font Size/Weight | 100% | 100% |
| Line Height | 100% | 95% |
| Box Shadow | 100% | 85% |
| Gradients | 100% | 80% |
| Filters/Effects | 100% | 70% |
| Transforms | 100% | 80% |
| Animations | N/A | N/A |

---

## Tools & Resources

### MCP Configuration
```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "figma-mcp-server"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "figd_xxxxx"
      }
    }
  }
}
```

### API Rate Limits
- 1.2 second delay between calls (mandatory)
- Max 8-10 concurrent requests
- ~0.5 frames/second throughput

### Verification Tools
- Chrome DevTools MCP for screenshots
- Tailwind CSS MCP for class generation
- shadcn/ui MCP for component scaffolding

---

## Decision Matrix

| Scenario | Recommended Solution |
|----------|---------------------|
| Single component demo | Manual CSS paste (99%) |
| Bulk design system export | API automation (90-95%) |
| Production app components | Hybrid: API + QA (95-99%) |
| Time-critical, quality-critical | Manual (99%) |
| Cost-critical, high-volume | API (90-95%) |

---

## Next Steps (Iteration Needed)

1. **Investigate Figma Plugin API** - Can we create a plugin that programmatically triggers "Copy as code"?
2. **Improve API reconstruction** - Better CSS property mapping for shadows, gradients, effects
3. **Visual diff automation** - Automated comparison between Figma design and generated output
4. **Component library pre-mapping** - Map common patterns to known components

---

**Status**: This solution is NOT satisfactory for 99% + automation + scale. Iteration required.
