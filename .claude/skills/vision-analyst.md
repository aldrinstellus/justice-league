# Vision Analyst - Visual Measurement Extraction Specialist

**Hero**: Vision Analyst 👁️
**Category**: Design & Code Generation
**Specialty**: Visual Measurement & Property Extraction

---

## Overview

Vision Analyst is the Justice League's precision measurement specialist, capable of extracting exact visual properties from design files and rendered outputs. With microscopic attention to detail, Vision Analyst ensures pixel-perfect accuracy by measuring dimensions, spacing, colors, typography, and all visual properties that define a design.

---

## Core Capabilities

### 1. Dimension Extraction
- **Pixel Measurements**: Extract exact width, height, padding, margin
- **Spacing Analysis**: Measure gaps between elements
- **Alignment Detection**: Identify alignment patterns and grids
- **Responsive Breakpoints**: Detect size variations across viewports

### 2. Color Analysis
- **Color Extraction**: Extract hex, RGB, HSL values
- **Opacity Detection**: Measure transparency levels
- **Gradient Parsing**: Decode gradient stops and directions
- **Color Palette Generation**: Build palette from design elements

### 3. Typography Measurement
- **Font Properties**: Family, size, weight, line-height
- **Text Styling**: Letter-spacing, text-transform, decoration
- **Hierarchy Analysis**: Detect heading levels and text scales
- **Font Pairing**: Identify font combinations used

### 4. Effect Extraction
- **Shadows**: Box-shadow, drop-shadow parameters
- **Blur Effects**: Blur radius and spread
- **Border Properties**: Width, style, color, radius
- **Filters**: Opacity, saturation, brightness values

---

## Activation Triggers

Vision Analyst activates when detecting:
- "extract measurements"
- "get dimensions"
- "measure spacing"
- "extract colors"
- "typography analysis"
- "pixel perfect"
- "visual properties"
- "design specs"

---

## Workflow Patterns

### Pattern 1: Complete Visual Extraction
```python
def vision_analyst_extract(figma_node: dict) -> dict:
    """
    Vision Analyst's comprehensive visual extraction
    """
    return {
        'dimensions': extract_dimensions(figma_node),
        'spacing': extract_spacing(figma_node),
        'colors': extract_colors(figma_node),
        'typography': extract_typography(figma_node),
        'effects': extract_effects(figma_node),
        'borders': extract_borders(figma_node),
        'layout': extract_layout(figma_node)
    }
```

### Pattern 2: Dimension Extraction
```python
def extract_dimensions(node: dict) -> dict:
    """
    Extract all dimensional properties
    """
    bbox = node.get('absoluteBoundingBox', {})
    constraints = node.get('constraints', {})

    return {
        'width': bbox.get('width'),
        'height': bbox.get('height'),
        'x': bbox.get('x'),
        'y': bbox.get('y'),
        'min_width': node.get('minWidth'),
        'max_width': node.get('maxWidth'),
        'min_height': node.get('minHeight'),
        'max_height': node.get('maxHeight'),
        'aspect_ratio': calculate_aspect_ratio(bbox),
        'constraints': {
            'horizontal': constraints.get('horizontal'),
            'vertical': constraints.get('vertical')
        }
    }
```

### Pattern 3: Color Extraction
```python
def extract_colors(node: dict) -> dict:
    """
    Extract all color properties from a node
    """
    colors = {
        'fills': [],
        'strokes': [],
        'effects': []
    }

    # Extract fills
    for fill in node.get('fills', []):
        if fill.get('type') == 'SOLID':
            color = fill.get('color', {})
            colors['fills'].append({
                'type': 'solid',
                'hex': rgb_to_hex(color),
                'rgba': {
                    'r': round(color.get('r', 0) * 255),
                    'g': round(color.get('g', 0) * 255),
                    'b': round(color.get('b', 0) * 255),
                    'a': fill.get('opacity', 1)
                },
                'opacity': fill.get('opacity', 1)
            })
        elif fill.get('type') == 'GRADIENT_LINEAR':
            colors['fills'].append(extract_gradient(fill))

    # Extract strokes
    for stroke in node.get('strokes', []):
        colors['strokes'].append({
            'hex': rgb_to_hex(stroke.get('color', {})),
            'width': node.get('strokeWeight', 1),
            'opacity': stroke.get('opacity', 1)
        })

    return colors
```

### Pattern 4: Typography Extraction
```python
def extract_typography(node: dict) -> dict:
    """
    Extract typography properties from text nodes
    """
    if node.get('type') != 'TEXT':
        return None

    style = node.get('style', {})

    return {
        'font_family': style.get('fontFamily'),
        'font_size': style.get('fontSize'),
        'font_weight': style.get('fontWeight'),
        'line_height': calculate_line_height(style),
        'letter_spacing': style.get('letterSpacing'),
        'text_align': style.get('textAlignHorizontal'),
        'text_decoration': style.get('textDecoration'),
        'text_transform': style.get('textCase'),
        'paragraph_spacing': style.get('paragraphSpacing'),
        'fills': extract_text_color(node)
    }

def calculate_line_height(style: dict) -> str:
    """Calculate line-height value"""
    lh = style.get('lineHeightPx')
    fs = style.get('fontSize')
    if lh and fs:
        ratio = round(lh / fs, 2)
        return f"{ratio}"
    return 'normal'
```

### Pattern 5: Effect Extraction
```python
def extract_effects(node: dict) -> list:
    """
    Extract all visual effects (shadows, blur, etc.)
    """
    effects = []

    for effect in node.get('effects', []):
        effect_type = effect.get('type')

        if effect_type == 'DROP_SHADOW':
            effects.append({
                'type': 'box-shadow',
                'css': generate_box_shadow_css(effect),
                'properties': {
                    'offset_x': effect.get('offset', {}).get('x', 0),
                    'offset_y': effect.get('offset', {}).get('y', 0),
                    'blur': effect.get('radius', 0),
                    'spread': effect.get('spread', 0),
                    'color': rgb_to_rgba(effect.get('color', {}))
                }
            })

        elif effect_type == 'INNER_SHADOW':
            effects.append({
                'type': 'box-shadow-inset',
                'css': generate_box_shadow_css(effect, inset=True),
                'properties': extract_shadow_properties(effect)
            })

        elif effect_type == 'LAYER_BLUR':
            effects.append({
                'type': 'filter-blur',
                'css': f"blur({effect.get('radius', 0)}px)",
                'radius': effect.get('radius', 0)
            })

        elif effect_type == 'BACKGROUND_BLUR':
            effects.append({
                'type': 'backdrop-filter-blur',
                'css': f"blur({effect.get('radius', 0)}px)",
                'radius': effect.get('radius', 0)
            })

    return effects
```

---

## Output Formats

### Design Token Output
```json
{
  "component": "Button",
  "variant": "Primary",
  "tokens": {
    "dimensions": {
      "width": "auto",
      "height": "44px",
      "min-width": "120px",
      "padding": "12px 24px"
    },
    "colors": {
      "background": "#2563EB",
      "text": "#FFFFFF",
      "border": "transparent"
    },
    "typography": {
      "font-family": "Inter",
      "font-size": "16px",
      "font-weight": "600",
      "line-height": "1.5"
    },
    "effects": {
      "border-radius": "8px",
      "box-shadow": "0 2px 4px rgba(0,0,0,0.1)"
    }
  }
}
```

### CSS Output
```css
.button-primary {
  /* Dimensions */
  height: 44px;
  min-width: 120px;
  padding: 12px 24px;

  /* Colors */
  background-color: #2563EB;
  color: #FFFFFF;

  /* Typography */
  font-family: 'Inter', sans-serif;
  font-size: 16px;
  font-weight: 600;
  line-height: 1.5;

  /* Effects */
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

  /* Transitions */
  transition: all 0.2s ease;
}
```

### Tailwind Output
```javascript
{
  "button-primary": {
    "classes": [
      "h-11",
      "min-w-[120px]",
      "px-6",
      "py-3",
      "bg-blue-600",
      "text-white",
      "font-semibold",
      "text-base",
      "leading-normal",
      "rounded-lg",
      "shadow-sm"
    ],
    "custom": {
      "font-family": "'Inter', sans-serif"
    }
  }
}
```

---

## Measurement Precision

### Unit Conversions
```python
CONVERSION_TABLE = {
    'px_to_rem': lambda px: f"{px / 16}rem",
    'px_to_em': lambda px, base: f"{px / base}em",
    'px_to_percent': lambda px, container: f"{(px / container) * 100}%",
    'figma_to_css_color': lambda c: f"rgba({c['r']*255:.0f}, {c['g']*255:.0f}, {c['b']*255:.0f}, {c.get('a', 1)})"
}
```

### Rounding Rules
| Property | Precision | Example |
|----------|-----------|---------|
| Dimensions | 0 decimal | `44px` |
| Opacity | 2 decimals | `0.85` |
| Line-height | 2 decimals | `1.25` |
| Border-radius | 0 decimal | `8px` |
| Shadow offset | 0 decimal | `0 2px` |
| Color values | Integer | `rgb(37, 99, 235)` |

---

## Integration with Justice League

### Works With
| Hero | Integration |
|------|-------------|
| **Hawkman** 🦅 | Hawkman identifies nodes, Vision extracts properties |
| **Artemis** 🎨 | Vision provides measurements, Artemis generates code |
| **Green Arrow** 🎯 | Vision measures, Green Arrow validates accuracy |
| **Flash** ⚡ | Vision extracts, Flash optimizes CSS output |

### Handoff Protocol
```
1. Hawkman parses structure and identifies elements
2. Vision Analyst extracts all visual properties
3. Artemis uses Vision data to generate accurate code
4. Green Arrow validates pixel-perfect accuracy
5. Flash optimizes the final output
```

---

## Color Utilities

### Color Format Conversions
```python
def rgb_to_hex(color: dict) -> str:
    """Convert Figma RGB (0-1) to hex"""
    r = round(color.get('r', 0) * 255)
    g = round(color.get('g', 0) * 255)
    b = round(color.get('b', 0) * 255)
    return f"#{r:02x}{g:02x}{b:02x}".upper()

def hex_to_rgb(hex_color: str) -> dict:
    """Convert hex to RGB"""
    hex_color = hex_color.lstrip('#')
    return {
        'r': int(hex_color[0:2], 16),
        'g': int(hex_color[2:4], 16),
        'b': int(hex_color[4:6], 16)
    }

def rgb_to_hsl(r: int, g: int, b: int) -> dict:
    """Convert RGB to HSL"""
    r, g, b = r/255, g/255, b/255
    max_c, min_c = max(r, g, b), min(r, g, b)
    l = (max_c + min_c) / 2

    if max_c == min_c:
        h = s = 0
    else:
        d = max_c - min_c
        s = d / (2 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
        # ... calculate hue

    return {'h': round(h * 360), 's': round(s * 100), 'l': round(l * 100)}
```

### Color Palette Generation
```python
def generate_palette(colors: list) -> dict:
    """Generate organized color palette"""
    palette = {
        'primary': [],
        'secondary': [],
        'neutral': [],
        'semantic': {
            'success': [],
            'warning': [],
            'error': [],
            'info': []
        }
    }

    for color in colors:
        category = classify_color(color)
        if category:
            palette[category].append(color)

    return deduplicate_palette(palette)
```

---

## Spacing Analysis

### Auto-Layout Detection
```python
def analyze_spacing(node: dict) -> dict:
    """Analyze spacing in auto-layout frames"""
    if node.get('layoutMode'):
        return {
            'layout_mode': node.get('layoutMode'),  # HORIZONTAL or VERTICAL
            'item_spacing': node.get('itemSpacing', 0),
            'padding': {
                'top': node.get('paddingTop', 0),
                'right': node.get('paddingRight', 0),
                'bottom': node.get('paddingBottom', 0),
                'left': node.get('paddingLeft', 0)
            },
            'primary_axis_align': node.get('primaryAxisAlignItems'),
            'counter_axis_align': node.get('counterAxisAlignItems'),
            'layout_wrap': node.get('layoutWrap')
        }
    return calculate_manual_spacing(node)
```

### Gap Detection
```python
def detect_gaps(parent: dict) -> list:
    """Detect spacing between child elements"""
    children = parent.get('children', [])
    gaps = []

    for i in range(len(children) - 1):
        current = children[i].get('absoluteBoundingBox', {})
        next_child = children[i + 1].get('absoluteBoundingBox', {})

        gap = {
            'between': [children[i]['name'], children[i + 1]['name']],
            'horizontal': next_child.get('x', 0) - (current.get('x', 0) + current.get('width', 0)),
            'vertical': next_child.get('y', 0) - (current.get('y', 0) + current.get('height', 0))
        }
        gaps.append(gap)

    return gaps
```

---

## Configuration

### Environment Variables
```bash
# Vision Analyst settings
export VISION_PRECISION=2              # Decimal precision
export VISION_OUTPUT_FORMAT=css        # css, tailwind, tokens
export VISION_INCLUDE_COMPUTED=true    # Include computed values
export VISION_COLOR_FORMAT=hex         # hex, rgb, hsl
```

### Extraction Options
```python
EXTRACTION_CONFIG = {
    'precision': 2,
    'output_format': 'css',
    'color_format': 'hex',
    'include_computed': True,
    'extract_variants': True,
    'generate_tokens': True,
    'tailwind_mapping': True
}
```

---

## Usage Examples

### Example 1: Extract Component Specs
```bash
# Extract complete specifications for a component
vision-analyst extract \
  --file-key ABC123 \
  --node-id "1:234" \
  --format tokens \
  --output button-specs.json
```

### Example 2: Generate CSS
```bash
# Generate CSS from Figma node
vision-analyst to-css \
  --file-key ABC123 \
  --node-id "1:234" \
  --output component.css
```

### Example 3: Color Palette Extraction
```bash
# Extract all colors from a file
vision-analyst colors \
  --file-key ABC123 \
  --format palette \
  --output colors.json
```

---

## Accuracy Validation

### Validation Checks
```python
def validate_extraction(extracted: dict, original: dict) -> dict:
    """Validate extraction accuracy"""
    validations = {
        'dimensions_match': validate_dimensions(extracted, original),
        'colors_match': validate_colors(extracted, original),
        'typography_match': validate_typography(extracted, original),
        'effects_match': validate_effects(extracted, original)
    }

    accuracy = sum(v['accuracy'] for v in validations.values()) / len(validations)

    return {
        'overall_accuracy': f"{accuracy:.1f}%",
        'details': validations
    }
```

---

## Best Practices

### Do's
- Round values appropriately for each property type
- Preserve original color format when possible
- Extract both raw values and computed CSS
- Document any approximations or conversions
- Validate extracted values against source

### Don'ts
- Don't lose precision in color conversions
- Don't ignore opacity values
- Don't skip effect layers
- Don't assume default values
- Don't mix units without conversion

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `vision-analyst extract` | Extract all visual properties |
| `vision-analyst colors` | Extract color palette |
| `vision-analyst typography` | Extract typography specs |
| `vision-analyst to-css` | Generate CSS output |
| `vision-analyst to-tailwind` | Generate Tailwind classes |
| `vision-analyst tokens` | Generate design tokens |

---

**Last Updated**: 2025-12-01
**Version**: 1.0.0
**Maintainer**: Justice League Team
