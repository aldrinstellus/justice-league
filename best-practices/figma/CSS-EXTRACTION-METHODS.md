# CSS Extraction Methods Comparison

**Purpose**: Compare all available methods for extracting CSS from Figma designs
**Last Updated**: 2025-11-25

---

## Method Overview

| Method | Access Type | Accuracy | Automation | Scale |
|--------|-------------|----------|------------|-------|
| **Copy as code (Desktop)** | Client-side UI | 99%+ | None | Manual |
| **Figma REST API** | HTTP API | 90-95% | Full | Unlimited |
| **Figma MCP Server** | MCP Protocol | 90-95% | Full | Unlimited |
| **Figma Plugin API** | Plugin | Varies | Partial | Per-file |
| **Dev Mode Inspect** | Client-side UI | 99%+ | None | Manual |
| **Third-party (Anima)** | Service | 80-90% | Full | Paid |

---

## Method 1: Figma "Copy as code" (Desktop/Web)

### How to Access
```
1. Open Figma Desktop or figma.com
2. Select a frame
3. Right-click → Copy/Paste as → Copy as code
4. Choose format: CSS, CSS (all layers), iOS, Android
```

### Output Format (CSS all layers)
```css
/* Figma "Copy as code → CSS (all layers)" output */

/* Frame: ProfileCard */
.profile-card {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 24px;
  gap: 16px;
  width: 320px;
  height: 200px;
  background: #FFFFFF;
  border-radius: 12px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

/* Child: Avatar */
.profile-card .avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%);
}

/* Child: Name */
.profile-card .name {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 600;
  font-size: 18px;
  line-height: 24px;
  color: #111827;
}
```

### What's Included
- All nested layers with parent-child relationship
- Exact CSS values (no approximation)
- Auto-layout converted to flexbox
- Gradients fully specified
- Box shadows with exact values
- Font family, size, weight, line-height
- Colors as hex or rgba

### Limitations
- **No API access** - cannot be automated
- **Manual per-frame** - doesn't scale
- **Requires Figma open** - client-side only

### Accuracy: 99%+

---

## Method 2: Figma REST API

### How to Access
```bash
# Get file structure
curl -H "X-Figma-Token: YOUR_TOKEN" \
  https://api.figma.com/v1/files/{file_key}

# Get specific nodes
curl -H "X-Figma-Token: YOUR_TOKEN" \
  https://api.figma.com/v1/files/{file_key}/nodes?ids=123:456
```

### Output Format (JSON)
```json
{
  "document": {
    "id": "0:0",
    "name": "Document",
    "type": "DOCUMENT",
    "children": [{
      "id": "123:456",
      "name": "ProfileCard",
      "type": "FRAME",
      "absoluteBoundingBox": {
        "x": 0, "y": 0, "width": 320, "height": 200
      },
      "fills": [{
        "type": "SOLID",
        "color": { "r": 1, "g": 1, "b": 1, "a": 1 }
      }],
      "strokes": [],
      "cornerRadius": 12,
      "paddingLeft": 24,
      "paddingRight": 24,
      "paddingTop": 24,
      "paddingBottom": 24,
      "itemSpacing": 16,
      "layoutMode": "VERTICAL",
      "primaryAxisAlignItems": "MIN",
      "counterAxisAlignItems": "MIN",
      "effects": [{
        "type": "DROP_SHADOW",
        "color": { "r": 0, "g": 0, "b": 0, "a": 0.1 },
        "offset": { "x": 0, "y": 4 },
        "radius": 6,
        "visible": true
      }]
    }]
  }
}
```

### CSS Reconstruction Required
```python
def reconstruct_css(node):
    css = {}

    # Dimensions
    bbox = node.get('absoluteBoundingBox', {})
    css['width'] = f"{bbox.get('width', 0)}px"
    css['height'] = f"{bbox.get('height', 0)}px"

    # Background
    fills = node.get('fills', [])
    if fills and fills[0]['type'] == 'SOLID':
        color = fills[0]['color']
        css['background'] = rgb_to_hex(color)

    # Border radius
    if 'cornerRadius' in node:
        css['border-radius'] = f"{node['cornerRadius']}px"

    # Padding
    css['padding'] = f"{node.get('paddingTop', 0)}px {node.get('paddingRight', 0)}px"

    # Flexbox from auto-layout
    if node.get('layoutMode') == 'VERTICAL':
        css['display'] = 'flex'
        css['flex-direction'] = 'column'
        css['gap'] = f"{node.get('itemSpacing', 0)}px"

    # Effects (shadows)
    effects = node.get('effects', [])
    for effect in effects:
        if effect['type'] == 'DROP_SHADOW' and effect.get('visible', True):
            shadow = effect
            css['box-shadow'] = f"{shadow['offset']['x']}px {shadow['offset']['y']}px {shadow['radius']}px rgba({int(shadow['color']['r']*255)}, {int(shadow['color']['g']*255)}, {int(shadow['color']['b']*255)}, {shadow['color']['a']})"

    return css
```

### What's Included
- Dimensions and positioning
- Colors (fills, strokes)
- Border radius (simple and per-corner)
- Padding (via auto-layout properties)
- Auto-layout → flexbox mapping
- Effects (shadows, blur)
- Typography (via text nodes)

### What's Missing/Approximate
- Complex gradients (need manual mapping)
- Multi-layer effects
- Some transform properties
- Exact font fallbacks
- Pseudo-elements

### Accuracy: 90-95%

---

## Method 3: Figma MCP Server

### How to Access
```json
// .mcp.json configuration
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

### Available Tools
| Tool | Description |
|------|-------------|
| `get_file_info` | Get file metadata and page structure |
| `get_node_info` | Get detailed properties for specific nodes |
| `get_styles` | Get design system styles |
| `get_components` | Get reusable components |
| `get_variables` | Get design tokens/variables |

### Same Data as REST API
The MCP server wraps the REST API - same data, same limitations.

### Advantage
- Integrated into Claude Code
- Natural language queries
- Easier to use than raw API

### Accuracy: 90-95% (same as REST API)

---

## Method 4: Figma Plugin API

### Possibility
Create a Figma plugin that:
1. Selects frames
2. Extracts CSS (using Figma's internal methods)
3. Exports to file or clipboard

### Plugin API Capabilities
```javascript
// Plugin can access node properties
const node = figma.currentPage.selection[0];
const css = node.getCSSAsync(); // Returns Promise<string>
```

### Status: **Needs Investigation**
- `getCSSAsync()` may exist in newer Figma plugin API
- Could enable automation via plugin + external trigger
- Would require Figma Desktop running

---

## Method 5: Dev Mode Inspect

### How to Access
```
1. Open Figma file
2. Click "Dev Mode" toggle (top right)
3. Select any element
4. View CSS in right panel
```

### What's Shown
- Full CSS properties
- Code snippets (CSS, iOS, Android)
- Spacing and measurements
- Color values

### Limitation
- Client-side only (no API)
- Manual per-element
- Same as "Copy as code" but in-panel

---

## Method 6: Third-Party Tools

### Anima
- Converts Figma to React/Vue/HTML
- 80-90% accuracy
- Paid service
- Automated but quality varies

### Locofy
- AI-powered Figma to code
- Better component detection
- Paid service

### Figma to Code (Community plugins)
- Various quality levels
- Some generate Tailwind
- Manual per-file

---

## Comparison Matrix

| Property | Copy as Code | REST API | MCP | Plugin |
|----------|-------------|----------|-----|--------|
| **Width/Height** | Exact | Exact | Exact | Exact |
| **Padding** | Exact | Exact | Exact | Exact |
| **Margin** | Exact | N/A (computed) | N/A | Exact |
| **Border Radius** | Exact | Exact | Exact | Exact |
| **Background Solid** | Exact | Exact | Exact | Exact |
| **Background Gradient** | Exact | 80% | 80% | Exact |
| **Box Shadow** | Exact | 90% | 90% | Exact |
| **Flexbox** | Exact | 95% | 95% | Exact |
| **Typography** | Exact | 95% | 95% | Exact |
| **Transforms** | Exact | 80% | 80% | Exact |
| **Filters** | Exact | 70% | 70% | Exact |
| **Automation** | None | Full | Full | Partial |
| **Scale** | 1/time | Unlimited | Unlimited | Per-file |

---

## Recommendation by Use Case

### Demo/Presentation (1 frame)
**Use**: Copy as code → CSS (all layers)
**Why**: 99% accuracy, impressive results

### Bulk Export (100+ frames)
**Use**: REST API or MCP
**Why**: Automated, scalable, 90-95% is acceptable

### Production Components
**Use**: Hybrid (API + Manual QA)
**Why**: Scale + quality control

### Design System Migration
**Use**: API for structure + Manual for critical components
**Why**: Need both scale and accuracy

---

## Key Insight

> **The "Copy as code" feature is the ONLY method that produces 99%+ accurate CSS, but it has NO API equivalent.** This is the fundamental gap in Figma's tooling.

### Why This Gap Exists
1. "Copy as code" uses Figma's internal rendering engine
2. It accesses computed styles, not just node properties
3. The REST API only exposes design data, not computed CSS
4. Figma hasn't exposed this as an API endpoint

### Potential Solutions (To Investigate)
1. Figma Plugin with `getCSSAsync()` (if available)
2. Browser automation (Puppeteer/Playwright) to control Figma web
3. Figma feature request for CSS export API
4. Better API reconstruction algorithms

---

**Status**: No perfect automated solution exists. Choose based on accuracy vs scale tradeoff.
