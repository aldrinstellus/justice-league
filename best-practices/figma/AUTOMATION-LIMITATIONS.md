# Figma Automation Limitations

**Purpose**: Document what CAN and CANNOT be automated with Figma
**Last Updated**: 2025-11-25

---

## Executive Summary

| Task | Automatable | Method | Notes |
|------|-------------|--------|-------|
| List files in project | ✅ Yes | REST API | Full automation |
| Get file structure | ✅ Yes | REST API | Full automation |
| Export PNGs/PDFs | ✅ Yes | REST API | Full automation |
| Get node properties | ✅ Yes | REST API | Full automation |
| Get design tokens | ✅ Yes | REST API | Full automation |
| **Extract CSS (99%)** | ❌ No | N/A | Client-side only |
| **"Copy as code"** | ❌ No | N/A | UI feature only |
| Create/edit designs | ⚠️ Partial | Plugin API | Requires desktop |
| Comments/collaboration | ✅ Yes | REST API | Full automation |

---

## What CAN Be Automated

### 1. File Discovery & Structure

```python
# List all files in a project
import requests

def list_project_files(project_id, token):
    headers = {'X-Figma-Token': token}
    url = f'https://api.figma.com/v1/projects/{project_id}/files'
    response = requests.get(url, headers=headers)
    return response.json()['files']

# Get file structure
def get_file_structure(file_key, token):
    headers = {'X-Figma-Token': token}
    url = f'https://api.figma.com/v1/files/{file_key}'
    response = requests.get(url, headers=headers)
    return response.json()
```

**Automation Level**: 100%
**Rate Limit**: 1.2s between calls

---

### 2. PNG/PDF/SVG Export

```python
# Export frames as images
def export_frames(file_key, node_ids, format='png', scale=2, token=None):
    headers = {'X-Figma-Token': token}
    ids = ','.join(node_ids)
    url = f'https://api.figma.com/v1/images/{file_key}?ids={ids}&format={format}&scale={scale}'
    response = requests.get(url, headers=headers)
    return response.json()['images']  # Returns URLs to download
```

**Automation Level**: 100%
**Formats**: PNG, JPG, SVG, PDF
**Scale**: 0.01 to 4x

---

### 3. Node Property Extraction

```python
# Get detailed node properties
def get_node_properties(file_key, node_id, token):
    headers = {'X-Figma-Token': token}
    url = f'https://api.figma.com/v1/files/{file_key}/nodes?ids={node_id}'
    response = requests.get(url, headers=headers)
    return response.json()['nodes'][node_id]
```

**Returns**:
- Dimensions (width, height, x, y)
- Fills (colors, gradients)
- Strokes (borders)
- Effects (shadows, blur)
- Corner radius
- Auto-layout properties
- Typography (for text nodes)

**Automation Level**: 100%
**Accuracy for CSS reconstruction**: 90-95%

---

### 4. Design Tokens/Variables

```python
# Get published styles
def get_file_styles(file_key, token):
    headers = {'X-Figma-Token': token}
    url = f'https://api.figma.com/v1/files/{file_key}/styles'
    response = requests.get(url, headers=headers)
    return response.json()['meta']['styles']

# Get variables (Figma Variables API)
def get_variables(file_key, token):
    headers = {'X-Figma-Token': token}
    url = f'https://api.figma.com/v1/files/{file_key}/variables/local'
    response = requests.get(url, headers=headers)
    return response.json()
```

**Automation Level**: 100%

---

### 5. Comments & Version History

```python
# Get comments
def get_comments(file_key, token):
    headers = {'X-Figma-Token': token}
    url = f'https://api.figma.com/v1/files/{file_key}/comments'
    response = requests.get(url, headers=headers)
    return response.json()['comments']

# Post comment
def post_comment(file_key, message, token):
    headers = {'X-Figma-Token': token}
    url = f'https://api.figma.com/v1/files/{file_key}/comments'
    data = {'message': message}
    response = requests.post(url, headers=headers, json=data)
    return response.json()
```

**Automation Level**: 100%

---

## What CANNOT Be Automated

### 1. "Copy as code" → CSS (all layers)

**The Problem**:
```
┌─────────────────────────────────────────────────────────────┐
│  "Copy as code" is a CLIENT-SIDE UI feature                 │
│                                                             │
│  - Lives in Figma Desktop/Web app                          │
│  - No API endpoint exists                                   │
│  - No programmatic access                                   │
│  - Uses Figma's internal rendering engine                   │
│  - Computes CSS from internal state (not just properties)   │
└─────────────────────────────────────────────────────────────┘
```

**Why It Matters**:
- Only method for 99%+ accurate CSS
- Critical for pixel-perfect conversions
- No workaround exists

**Workaround Attempts**:
| Approach | Feasibility | Result |
|----------|-------------|--------|
| Browser automation (Puppeteer) | Possible | Complex, fragile |
| Figma Plugin | Unknown | Needs investigation |
| API reconstruction | Works | 90-95% accuracy only |
| Third-party service | Paid | 80-90% accuracy |

---

### 2. Real-time Design Editing

**The Problem**:
- REST API is read-only for design content
- Cannot create/modify frames, shapes, text via API
- Must use Plugin API (requires Figma Desktop)

**Plugin API Limitations**:
- Runs inside Figma Desktop only
- No remote triggering
- User must have file open
- Manual execution required

---

### 3. Font Rendering Information

**The Problem**:
- API provides font family name
- Cannot access actual rendered glyphs
- Font fallback behavior is client-side
- Web font availability not in API

---

### 4. Interactive Prototype Behavior

**The Problem**:
- Prototype connections in API
- Actual interaction behavior is client-side
- Animations not exportable
- Hover states are design-time only

---

## The Automation Gap

### Visual Representation

```
┌─────────────────────────────────────────────────────────────┐
│                    FIGMA CAPABILITIES                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           REST API (Fully Automated)                │   │
│  │                                                     │   │
│  │  • File listing                                     │   │
│  │  • Structure traversal                              │   │
│  │  • Node properties                                  │   │
│  │  • Image export (PNG/PDF/SVG)                       │   │
│  │  • Design tokens                                    │   │
│  │  • Comments                                         │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         CLIENT-SIDE ONLY (Not Automated)            │   │
│  │                                                     │   │
│  │  • "Copy as code" (99% CSS)        ← THE GAP       │   │
│  │  • Dev Mode inspect                                 │   │
│  │  • Real-time editing                                │   │
│  │  • Prototype playback                               │   │
│  │  • Font rendering                                   │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           PLUGIN API (Semi-Automated)               │   │
│  │                                                     │   │
│  │  • Design editing                                   │   │
│  │  • Custom exports                                   │   │
│  │  • getCSSAsync() ← NEEDS INVESTIGATION              │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Rate Limits (REST API)

| Endpoint | Rate Limit | Best Practice |
|----------|-----------|---------------|
| File structure | ~30 req/min | 1.2s delay |
| Node details | ~30 req/min | 1.2s delay |
| Image export | ~30 req/min | 1.2s delay |
| Batch requests | Max 50 nodes | Chunk requests |

**Throughput Calculation**:
```
24,820 frames ÷ 0.5 fps = 49,640 seconds = 13.8 hours
```

This is a HARD LIMIT - cannot be bypassed without multiple accounts.

---

## Possible Future Solutions

### 1. Figma Plugin with `getCSSAsync()`

**Hypothesis**: Plugin API may have CSS export capability

**To Investigate**:
```javascript
// Does this work in Figma Plugin API?
const node = figma.currentPage.selection[0];
const css = await node.getCSSAsync();
console.log(css);
```

**If it works**:
- Create plugin that exports all frames' CSS to a file
- Run manually once, get all CSS
- Use for subsequent automation

---

### 2. Browser Automation (Puppeteer/Playwright)

**Approach**:
```javascript
// Theoretical Puppeteer script
const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.goto('https://www.figma.com/file/xxxxx');
await page.waitForSelector('[data-node-id="123:456"]');
await page.click('[data-node-id="123:456"]');
await page.keyboard.press('Control+Alt+C'); // Copy as code shortcut
const css = await page.evaluate(() => navigator.clipboard.readText());
```

**Challenges**:
- Figma authentication
- Dynamic element selectors
- Clipboard access restrictions
- Fragile to UI changes

---

### 3. Figma Feature Request

**Request**: Add `/v1/files/{key}/nodes/{id}/css` endpoint

**Benefit**: Would enable 99% CSS at scale

**Status**: Not available as of 2025-11-25

---

## Summary

### Can Automate (Do This)
- File discovery and listing
- Structure traversal
- Node property extraction
- PNG/PDF/SVG export
- Design token extraction
- Comments and collaboration

### Cannot Automate (Accept Limitation)
- 99% accurate CSS extraction
- "Copy as code" feature
- Real-time design editing via API
- Interactive prototype behavior

### Workaround for Scale
1. Use API for 90-95% accuracy (acceptable for most use cases)
2. Manual QA for critical 5-10% of components
3. Hybrid pipeline: automation + human review

---

**Conclusion**: Full automation of Figma-to-code at 99% accuracy is NOT currently possible due to the client-side nature of CSS export. Choose your tradeoff: accuracy (manual) vs scale (API).
