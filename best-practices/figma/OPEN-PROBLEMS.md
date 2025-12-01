# Open Problems - Figma Automation

**Purpose**: Track unsolved problems for future iteration
**Status**: Active research needed
**Last Updated**: 2025-11-25

---

## Problem #1: 99% CSS at Scale

### The Gap
| What We Want | What Exists |
|--------------|-------------|
| 99% accurate CSS | Manual copy only |
| Fully automated | No API for CSS export |
| 100+ files | 1 file at a time |

### Current Workarounds (Not Satisfactory)
1. **Manual CSS paste** - Doesn't scale
2. **API reconstruction** - Only 90-95% accurate
3. **Hybrid** - Manual QA required

### Investigation Paths

#### Path A: Figma Plugin API
**Question**: Does `getCSSAsync()` exist in Plugin API?

**To Test**:
```javascript
// Create test plugin
figma.showUI(__html__);

const node = figma.currentPage.selection[0];
if (node) {
  // Does this method exist?
  if (typeof node.getCSSAsync === 'function') {
    const css = await node.getCSSAsync();
    figma.ui.postMessage({ type: 'css', data: css });
  } else {
    figma.ui.postMessage({ type: 'error', data: 'getCSSAsync not available' });
  }
}
```

**Status**: NOT TESTED

---

#### Path B: Browser Automation
**Question**: Can Puppeteer/Playwright control Figma web app?

**Challenges**:
- [ ] Figma authentication (OAuth or session)
- [ ] Element selector stability
- [ ] Clipboard access in headless mode
- [ ] Rate limiting / detection

**To Test**:
```javascript
const puppeteer = require('puppeteer');

async function extractCSS(fileKey, nodeId) {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();

  // Login to Figma (need to solve auth)
  await page.goto('https://www.figma.com/login');
  // ... authentication steps

  // Navigate to file
  await page.goto(`https://www.figma.com/file/${fileKey}`);

  // Select node and copy CSS
  // ... interaction steps

  // Get clipboard content
  const css = await page.evaluate(() => navigator.clipboard.readText());

  return css;
}
```

**Status**: NOT TESTED

---

#### Path C: Improved API Reconstruction
**Question**: Can we improve API → CSS accuracy to 98%+?

**Missing Properties to Map**:
| CSS Property | API Field | Mapping Complexity |
|--------------|-----------|-------------------|
| Complex gradients | fills[].gradientStops | High |
| Multiple shadows | effects[] | Medium |
| Backdrop blur | effects[].type='BACKGROUND_BLUR' | Medium |
| Text decoration | textDecoration | Low |
| Letter spacing | letterSpacing | Low |
| Text transform | textCase | Low |

**To Build**:
```python
def improved_css_reconstruction(node):
    css = {}

    # Handle complex gradients
    for fill in node.get('fills', []):
        if fill['type'] == 'GRADIENT_LINEAR':
            stops = fill['gradientStops']
            angle = calculate_gradient_angle(fill['gradientHandlePositions'])
            css['background'] = f"linear-gradient({angle}deg, {format_stops(stops)})"

    # Handle multiple shadows
    shadows = []
    for effect in node.get('effects', []):
        if effect['type'] == 'DROP_SHADOW' and effect.get('visible', True):
            shadows.append(format_shadow(effect))
    if shadows:
        css['box-shadow'] = ', '.join(shadows)

    # ... more mappings

    return css
```

**Status**: PARTIALLY IMPLEMENTED (90-95%)

---

#### Path D: Figma Feature Request
**Question**: Will Figma add a CSS export API endpoint?

**Proposed Endpoint**:
```
GET /v1/files/{file_key}/nodes/{node_id}/css
```

**Response**:
```json
{
  "css": ".node { display: flex; ... }",
  "cssAllLayers": "/* Parent */\n.parent { ... }\n/* Child */\n.child { ... }"
}
```

**Status**: NOT REQUESTED (should we submit?)

---

## Problem #2: Batch CSS Export

### The Gap
Even if we solve #1, how do we export 100+ frames efficiently?

### Considerations
- Rate limits (1.2s per request)
- Memory for large exports
- Error handling for partial failures
- Resume capability for interrupted jobs

### Proposed Solution Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    BATCH EXPORT PIPELINE                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. DISCOVERY PHASE                                         │
│     └─ List all frames via API (fast)                      │
│                                                             │
│  2. CSS EXTRACTION PHASE                                    │
│     ├─ If Plugin: Run plugin, export to JSON file          │
│     ├─ If Browser: Puppeteer loop with delays              │
│     └─ If API: Reconstruct CSS (90-95%)                    │
│                                                             │
│  3. CONVERSION PHASE                                        │
│     └─ CSS → React/Tailwind (Claude)                       │
│                                                             │
│  4. VERIFICATION PHASE                                      │
│     └─ Chrome MCP screenshots for visual diff              │
│                                                             │
│  5. QA PHASE (if needed)                                   │
│     └─ Human review of failed conversions                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Status**: CONCEPTUAL - not implemented

---

## Problem #3: Visual Diff Automation

### The Gap
How do we automatically verify conversion accuracy?

### Current Method
- Chrome MCP screenshot
- Manual visual comparison

### Desired Method
- Automated pixel diff between Figma export and React render
- Threshold-based pass/fail (e.g., >98% match = pass)
- Highlight differences for QA

### Tools to Investigate
- **pixelmatch** - Node.js pixel comparison
- **looks-same** - Yandex image comparison
- **reg-suit** - Visual regression testing
- **Percy** - Visual testing service

**Status**: NOT IMPLEMENTED

---

## Problem #4: Component Detection

### The Gap
How do we detect reusable components vs one-off elements?

### Why It Matters
- Components should map to React components
- One-offs can be inline styles
- Design system compliance

### Signals for Component Detection
- [ ] Figma Component instances
- [ ] Repeated similar structures
- [ ] Named with pattern (e.g., "Button/Primary")
- [ ] Published to library

**Status**: PARTIALLY SOLVED (Figma components API exists)

---

## Problem #5: Responsive Breakpoints

### The Gap
Figma designs are fixed-width. How do we generate responsive code?

### Current Approach
- Single breakpoint per design
- Manual responsive adjustments

### Desired Approach
- Auto-detect fluid vs fixed elements
- Generate responsive Tailwind classes
- Support multiple Figma frames for breakpoints

### Investigation Needed
- Figma auto-layout constraints → CSS responsive behavior
- Min/max width constraints
- Fluid typography patterns

**Status**: NOT SOLVED

---

## Priority Ranking

| Problem | Impact | Effort | Priority |
|---------|--------|--------|----------|
| #1 99% CSS at Scale | High | High | **P0** |
| #2 Batch Export | High | Medium | **P1** |
| #3 Visual Diff | Medium | Medium | P2 |
| #4 Component Detection | Medium | Low | P2 |
| #5 Responsive | Medium | High | P3 |

---

## Next Actions

### Immediate (This Week)
- [ ] Test Figma Plugin API for `getCSSAsync()`
- [ ] Research Figma community for existing solutions

### Short-term (This Month)
- [ ] Build improved API reconstruction (target 95%+)
- [ ] Prototype browser automation approach
- [ ] Evaluate visual diff tools

### Long-term (Future)
- [ ] Submit Figma feature request for CSS API
- [ ] Build production batch export pipeline
- [ ] Implement responsive generation

---

## Resources

### Figma Documentation
- [REST API Reference](https://www.figma.com/developers/api)
- [Plugin API Reference](https://www.figma.com/plugin-docs/)
- [Variables API](https://www.figma.com/developers/api#variables)

### Community
- [Figma Community Plugins](https://www.figma.com/community/plugins)
- [Figma Developer Forum](https://forum.figma.com/c/developers/)

### Related Projects
- [figma-mcp-server](https://www.npmjs.com/package/figma-mcp-server)
- [figma-js](https://github.com/jemgold/figma-js)

---

## Contribution Notes

When solving any of these problems:
1. Document the approach in this folder
2. Update this file with status changes
3. Add code examples to relevant docs
4. Test with real Figma files before claiming solved

---

**This document is a living record of unsolved problems. Update as progress is made.**
