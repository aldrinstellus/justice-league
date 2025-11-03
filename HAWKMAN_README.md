# 🦅 Hawkman - Structural Parser Specialist

**Version**: 1.0.0
**Justice League Version**: 1.8.0
**Created**: October 24, 2025
**Author**: Hawkman + Claude Code

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Core Capabilities](#core-capabilities)
- [API Reference](#api-reference)
- [Hawkman vs Artemis](#hawkman-vs-artemis)
- [Usage Examples](#usage-examples)
- [Integration Guide](#integration-guide)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Advanced Topics](#advanced-topics)

---

## Overview

Hawkman is a specialized Justice League agent that converts Figma designs to code through **layer-by-layer structural parsing**. Unlike Artemis (who focuses on component-based conversion), Hawkman provides archaeological precision by traversing the Figma layer hierarchy and adaptively selecting the best output format.

### Key Features

- **🌳 Layer-by-Layer Parsing**: Traverse Figma's hierarchical structure systematically
- **🎯 Adaptive Format Selection**: Automatically choose HTML/CSS, HTML+Tailwind, or React based on complexity
- **🔍 Visual Verification Loop**: Compare rendered output with Figma export and iteratively refine
- **📊 Complexity Analysis**: Intelligently determine parsing depth and output format
- **🧠 Pattern Learning**: Store and reuse successful patterns via Oracle integration
- **⚡ Multiple Output Formats**: Support for HTML/CSS, HTML+Tailwind, and React+Tailwind

### When to Use Hawkman

**Use Hawkman when:**
- You want div-by-div, section-by-section conversion
- The design has clear hierarchical structure
- You need adaptive output format selection
- You want layer-level control over parsing depth
- You're working with complex nested layouts

**Use Artemis when:**
- You have shadcn/ui or component library components
- You want semantic component mapping
- The design is component-centric (buttons, cards, forms)
- You need integration with existing component libraries

---

## Quick Start

### Basic Usage

```python
from core.justice_league.hawkman_structural_parser import parse_figma_to_code

# Simple conversion with auto-detection
result = parse_figma_to_code(
    figma_url="https://www.figma.com/design/YOUR_FILE_KEY/name?node-id=X-Y",
    output_format="auto",  # Let Hawkman decide
    verify=True            # Enable visual verification
)

print(f"Generated Code:\n{result['generated_code']}")
print(f"Accuracy: {result['accuracy_score']}%")
```

### Advanced Usage

```python
from core.justice_league.hawkman_structural_parser import (
    HawkmanStructuralParser,
    OutputFormat,
    ParsingDepth
)

# Create Hawkman instance
hawkman = HawkmanStructuralParser()

# Parse with specific configuration
result = hawkman.parse_figma(
    figma_url="https://www.figma.com/design/YOUR_FILE_KEY/name?node-id=X-Y",
    output_format=OutputFormat.REACT_TAILWIND,  # Force React output
    parsing_depth=ParsingDepth.ADAPTIVE,        # Adaptive depth
    verify=True,                                 # Enable verification
    max_iterations=3                             # Refine up to 3 times
)

print(f"Output Format: {result['output_format']}")
print(f"Iterations Used: {result['parsing_record']['iterations_used']}")
print(f"Final Accuracy: {result['accuracy_score']}%")
```

---

## Core Capabilities

### 1. Figma Layer Traversal

Hawkman systematically traverses the Figma layer hierarchy, respecting the design structure:

```python
# Automatically parse layer hierarchy
hierarchy = hawkman._parse_layer_hierarchy(
    figma_structure=figma_data,
    depth=ParsingDepth.ADAPTIVE
)

# Resulting hierarchy structure:
{
    'name': 'Root',
    'type': 'FRAME',
    'children': [
        {
            'name': 'Header',
            'type': 'FRAME',
            'children': [...]
        }
    ]
}
```

### 2. Adaptive Output Format Selection

Hawkman analyzes design complexity and automatically selects the best output format:

| Complexity | Layer Count | Has Interactivity | Output Format |
|-----------|-------------|-------------------|---------------|
| Simple | ≤ 10 | No | HTML + CSS |
| Moderate | 10-30 | No | HTML + Tailwind |
| Complex | > 30 | Yes | React + Tailwind |

```python
# Complexity thresholds (configurable)
hawkman.complexity_thresholds = {
    'simple': 10,      # HTML/CSS threshold
    'moderate': 30,    # HTML+Tailwind threshold
    'complex': 50      # React threshold
}
```

### 3. Parsing Depth Strategies

Control how deep Hawkman parses the layer hierarchy:

- **FRAME**: Parse only top-level frames (fast, high-level structure)
- **COMPONENT**: Parse until component boundaries detected
- **ELEMENT**: Parse every single element (slow, maximum detail)
- **ADAPTIVE**: Let Hawkman decide based on complexity (recommended)

```python
from core.justice_league.hawkman_structural_parser import ParsingDepth

result = hawkman.parse_figma(
    figma_url=url,
    parsing_depth=ParsingDepth.COMPONENT  # Stop at component boundaries
)
```

### 4. Visual Verification Loop

Hawkman integrates with Green Arrow to verify accuracy:

```
1. Parse Figma → Generate Code
2. Render Code → Capture Screenshot
3. Export Figma → Download Reference Image
4. Compare with Green Arrow → Get Discrepancies
5. If accuracy < 95% → Refine Code → Repeat from step 2
```

```python
result = hawkman.parse_figma(
    figma_url=url,
    verify=True,           # Enable verification
    max_iterations=3       # Maximum refinement iterations
)

# Check verification results
if result['verification_results']:
    discrepancies = result['verification_results']['discrepancies']
    print(f"Found {len(discrepancies)} discrepancies")
```

### 5. Component Boundary Detection

Hawkman automatically detects component boundaries using pattern matching:

```python
# Component indicators (configurable)
component_indicators = [
    'button', 'card', 'modal', 'dialog', 'form',
    'menu', 'nav', 'header', 'footer', 'sidebar'
]

# Automatically stops parsing at these boundaries when using
# ParsingDepth.COMPONENT mode
```

---

## API Reference

### HawkmanStructuralParser Class

#### Constructor

```python
hawkman = HawkmanStructuralParser(
    hero_name: str = "Hawkman",
    hero_emoji: str = "🦅"
)
```

#### Main Methods

##### `parse_figma()`

Parse a Figma design and generate code with optional verification.

```python
def parse_figma(
    self,
    figma_url: str,
    output_format: OutputFormat = OutputFormat.AUTO,
    parsing_depth: ParsingDepth = ParsingDepth.ADAPTIVE,
    verify: bool = True,
    max_iterations: int = 3
) -> Dict[str, Any]:
    """
    Parse Figma design to code with verification loop.

    Args:
        figma_url: Full Figma URL with file key and node ID
        output_format: Desired output format (AUTO for adaptive)
        parsing_depth: How deep to parse layer hierarchy
        verify: Enable visual verification with Green Arrow
        max_iterations: Maximum refinement iterations

    Returns:
        {
            'generated_code': str,          # The generated code
            'layer_hierarchy': dict,        # Parsed layer structure
            'output_format': str,           # Selected output format
            'accuracy_score': float,        # 0-100 accuracy score
            'verification_results': dict,   # Green Arrow results
            'parsing_record': dict          # Metadata and stats
        }
    """
```

##### `analyze_complexity()`

Analyze Figma design complexity without generating code.

```python
def analyze_complexity(
    self,
    figma_url: str
) -> Dict[str, Any]:
    """
    Analyze design complexity and recommend format/depth.

    Returns:
        {
            'layer_count': int,
            'max_depth': int,
            'avg_children': float,
            'has_components': bool,
            'recommended_format': OutputFormat,
            'recommended_depth': ParsingDepth
        }
    """
```

#### Helper Methods (Private)

- `_extract_figma_identifiers(url)`: Extract file key and node ID from URL
- `_fetch_figma_structure(file_key, node_id)`: Fetch Figma layer data
- `_count_layers(structure)`: Count total layers in hierarchy
- `_calculate_max_depth(structure)`: Calculate maximum nesting depth
- `_calculate_avg_children(structure)`: Calculate average children per layer
- `_detect_components(structure)`: Detect if components exist
- `_determine_output_format(structure)`: Select optimal output format
- `_determine_parsing_depth(structure)`: Select optimal parsing depth
- `_parse_layer_hierarchy(structure, depth)`: Parse layers to specified depth
- `_generate_html_css(layer)`: Generate HTML with CSS classes
- `_generate_html_tailwind(layer)`: Generate HTML with Tailwind classes
- `_generate_react_tailwind(layer)`: Generate React component with Tailwind
- `_map_layer_to_tailwind(layer)`: Map Figma layer to Tailwind classes

### Convenience Function

```python
from core.justice_league.hawkman_structural_parser import parse_figma_to_code

result = parse_figma_to_code(
    figma_url: str,
    output_format: str = "auto",  # "html_css", "html_tailwind", "react_tailwind", "auto"
    verify: bool = True
) -> Dict[str, Any]
```

### Enums

#### OutputFormat

```python
from core.justice_league.hawkman_structural_parser import OutputFormat

OutputFormat.AUTO           # Let Hawkman decide
OutputFormat.HTML_CSS       # Pure HTML with CSS classes
OutputFormat.HTML_TAILWIND  # HTML with Tailwind utility classes
OutputFormat.REACT_TAILWIND # React component with Tailwind
```

#### ParsingDepth

```python
from core.justice_league.hawkman_structural_parser import ParsingDepth

ParsingDepth.FRAME      # Top-level frames only
ParsingDepth.COMPONENT  # Parse until component boundaries
ParsingDepth.ELEMENT    # Parse every single element
ParsingDepth.ADAPTIVE   # Let Hawkman decide (recommended)
```

#### FigmaLayerType

```python
from core.justice_league.hawkman_structural_parser import FigmaLayerType

FigmaLayerType.FRAME
FigmaLayerType.GROUP
FigmaLayerType.COMPONENT
FigmaLayerType.INSTANCE
FigmaLayerType.TEXT
FigmaLayerType.RECTANGLE
FigmaLayerType.ELLIPSE
```

---

## Hawkman vs Artemis

### Comparison Table

| Feature | Hawkman 🦅 | Artemis 🏹 |
|---------|-----------|-----------|
| **Approach** | Layer-by-layer structural | Component-based semantic |
| **Best For** | Nested layouts, hierarchical designs | Component libraries, shadcn/ui |
| **Output** | HTML/CSS, HTML+Tailwind, React+Tailwind | React components |
| **Parsing Strategy** | Top-down hierarchy traversal | Component recognition & mapping |
| **Depth Control** | Adaptive (FRAME/COMPONENT/ELEMENT) | Component-level |
| **Format Selection** | Automatic based on complexity | Always React components |
| **Visual Verification** | ✅ Integrated loop with Green Arrow | ✅ Integrated loop with Green Arrow |
| **Use Case** | "Convert this Figma div-by-div" | "Map this to shadcn Button" |
| **Learning** | Pattern-based via Oracle | Component mapping via Oracle |
| **Speed** | Fast for simple layouts | Fast for component-rich designs |

### When to Use Which Agent

```
┌─────────────────────────────────────────────────────────┐
│                 Decision Tree                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Does design use shadcn/ui or component library?       │
│         │                                               │
│         ├─ YES ──→ Use ARTEMIS 🏹                      │
│         │                                               │
│         └─ NO ──→ Is it hierarchical/nested layout?    │
│                         │                               │
│                         ├─ YES ──→ Use HAWKMAN 🦅      │
│                         │                               │
│                         └─ NO ──→ Either works,         │
│                                    prefer HAWKMAN       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Example Scenarios

**Use Hawkman for:**
- Landing pages with sections and divs
- Dashboard layouts with nested cards
- Settings pages with forms and panels
- Blog layouts with structured content
- Multi-column layouts

**Use Artemis for:**
- Component library documentation
- Design systems with shadcn/ui
- Form-heavy applications
- UI kit conversions
- Component gallery pages

---

## Usage Examples

### Example 1: Basic Parsing with Auto-Detection

```python
from core.justice_league.hawkman_structural_parser import parse_figma_to_code

result = parse_figma_to_code(
    figma_url="https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=2-948",
    output_format="auto",
    verify=True
)

print(f"Output Format: {result['output_format']}")
print(f"Accuracy: {result['accuracy_score']}%")
print(result['generated_code'])
```

### Example 2: Force HTML/CSS Output

```python
from core.justice_league.hawkman_structural_parser import (
    HawkmanStructuralParser,
    OutputFormat,
    ParsingDepth
)

hawkman = HawkmanStructuralParser()

result = hawkman.parse_figma(
    figma_url="https://www.figma.com/design/...",
    output_format=OutputFormat.HTML_CSS,
    parsing_depth=ParsingDepth.FRAME,  # Top-level only
    verify=False  # Skip verification for speed
)

print(result['generated_code'])
```

### Example 3: React Component with Full Verification

```python
hawkman = HawkmanStructuralParser()

result = hawkman.parse_figma(
    figma_url="https://www.figma.com/design/...",
    output_format=OutputFormat.REACT_TAILWIND,
    parsing_depth=ParsingDepth.ADAPTIVE,
    verify=True,
    max_iterations=3  # Refine up to 3 times for 95%+ accuracy
)

# Check results
if result['accuracy_score'] >= 95:
    print("✅ Target accuracy achieved!")
    # Save the component
    with open('GeneratedComponent.tsx', 'w') as f:
        f.write(result['generated_code'])
else:
    print(f"⚠️ Accuracy: {result['accuracy_score']}%")
    print("Discrepancies found:")
    for disc in result['verification_results']['discrepancies']:
        print(f"  - {disc}")
```

### Example 4: Analyze Before Converting

```python
hawkman = HawkmanStructuralParser()

# First, analyze the design
analysis = hawkman.analyze_complexity(
    figma_url="https://www.figma.com/design/..."
)

print(f"Total Layers: {analysis['layer_count']}")
print(f"Max Depth: {analysis['max_depth']}")
print(f"Recommended Format: {analysis['recommended_format'].value}")
print(f"Recommended Depth: {analysis['recommended_depth'].value}")

# Then parse with recommendations
result = hawkman.parse_figma(
    figma_url="https://www.figma.com/design/...",
    output_format=analysis['recommended_format'],
    parsing_depth=analysis['recommended_depth'],
    verify=True
)
```

### Example 5: Layer Analysis Only

```python
hawkman = HawkmanStructuralParser()

# Extract identifiers
file_key, node_id = hawkman._extract_figma_identifiers(figma_url)

# Fetch and analyze structure
figma_structure = hawkman._fetch_figma_structure(file_key, node_id)

# Get detailed metrics
layer_count = hawkman._count_layers(figma_structure)
max_depth = hawkman._calculate_max_depth(figma_structure)
avg_children = hawkman._calculate_avg_children(figma_structure)
has_components = hawkman._detect_components(figma_structure)

print(f"Layer Count: {layer_count}")
print(f"Max Depth: {max_depth}")
print(f"Avg Children/Layer: {avg_children:.1f}")
print(f"Has Components: {has_components}")
```

**For complete working examples, see:** `examples/example_hawkman.py`

---

## Integration Guide

### With Green Arrow (Visual Validator)

Hawkman automatically integrates with Green Arrow when `verify=True`:

```python
# Hawkman internally calls:
self.green_arrow.compare_design_to_render(
    figma_image_path=exported_figma_image,
    rendered_image_path=rendered_code_screenshot
)

# Green Arrow returns:
{
    'discrepancies': [
        'Layout spacing differs by 8px',
        'Font weight should be bold (700) not medium (500)',
        ...
    ],
    'accuracy_score': 92.5,
    'visual_diff_path': 'path/to/diff.png'
}
```

No additional configuration needed - Green Arrow is initialized in Hawkman's constructor.

### With Oracle (Pattern Learning)

Hawkman sends successful patterns to Oracle for reuse:

```python
# After successful conversion (≥95% accuracy)
self.oracle.store_pattern({
    'pattern_type': 'layout_structure',
    'figma_structure': simplified_hierarchy,
    'output_format': 'react_tailwind',
    'accuracy_achieved': 97.5,
    'code_template': generated_code_template
})

# Oracle can then suggest patterns for similar structures
suggested_patterns = self.oracle.find_similar_patterns(
    current_structure
)
```

### With Batman (Coordination)

For autonomous operation as part of Justice League workflows:

```python
# Batman can orchestrate Hawkman
batman.coordinate_mission({
    'mission_type': 'figma_to_code_conversion',
    'agent': 'hawkman',
    'params': {
        'figma_url': url,
        'output_format': 'auto',
        'verify': True
    }
})
```

---

## Configuration

### Complexity Thresholds

Customize when Hawkman switches between output formats:

```python
hawkman = HawkmanStructuralParser()

# Default thresholds
hawkman.complexity_thresholds = {
    'simple': 10,      # ≤10 layers → HTML/CSS
    'moderate': 30,    # 10-30 layers → HTML+Tailwind
    'complex': 50      # >30 layers → React+Tailwind
}

# Customize for your needs
hawkman.complexity_thresholds = {
    'simple': 5,       # More aggressive React usage
    'moderate': 15,
    'complex': 25
}
```

### Component Indicators

Customize what layer names trigger component boundary detection:

```python
# Add custom component indicators
hawkman.component_indicators.extend([
    'widget', 'module', 'section', 'panel'
])
```

### Database Locations

Hawkman stores data in three JSON databases:

```python
# Default locations (customizable)
data/hawkman/
├── parsing_history.json    # All parsing attempts and results
├── layer_mappings.json     # Figma layer → Code mappings
└── patterns.json           # Successful patterns for reuse
```

Access in code:

```python
hawkman.parsing_history_db   # Path to parsing_history.json
hawkman.layer_mappings_db    # Path to layer_mappings.json
hawkman.patterns_db          # Path to patterns.json
```

---

## Troubleshooting

### Issue: "Invalid Figma URL"

**Error:**
```
ValueError: Invalid Figma URL format
```

**Solution:**
Ensure URL includes file key and optionally node ID:
```
✅ https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/name?node-id=2-948
✅ https://www.figma.com/file/6Pmf9gCcUccyqbCO9nN6Ts/name?node-id=2-948
❌ https://www.figma.com/6Pmf9gCcUccyqbCO9nN6Ts
```

### Issue: Low Accuracy Score

**Problem:** Accuracy consistently below 95%

**Solutions:**
1. **Increase max_iterations:**
   ```python
   result = hawkman.parse_figma(url, max_iterations=5)
   ```

2. **Try different output format:**
   ```python
   # If auto-selected HTML/CSS, try Tailwind
   result = hawkman.parse_figma(url, output_format=OutputFormat.HTML_TAILWIND)
   ```

3. **Adjust parsing depth:**
   ```python
   # Try more detailed parsing
   result = hawkman.parse_figma(url, parsing_depth=ParsingDepth.ELEMENT)
   ```

4. **Check discrepancies:**
   ```python
   for disc in result['verification_results']['discrepancies']:
       print(disc)  # Identify specific issues
   ```

### Issue: Figma API Not Responding

**Error:**
```
ConnectionError: Failed to fetch Figma structure
```

**Solutions:**
1. Check Figma access token (if using real API)
2. Verify file is accessible/public
3. Check network connectivity
4. For development, mock mode should work without API

### Issue: Generated Code Doesn't Render

**Problem:** HTML/React code has syntax errors

**Solutions:**
1. **Check layer names:** Special characters in Figma layer names may cause issues
   ```python
   # Hawkman sanitizes layer names, but verify output
   print(result['layer_hierarchy'])
   ```

2. **Validate output format:**
   ```python
   # Ensure React code is valid TSX
   if result['output_format'] == 'react_tailwind':
       # Check for proper JSX syntax
       assert 'export default' in result['generated_code']
   ```

3. **Try simpler format first:**
   ```python
   # Start with HTML/CSS to debug structure
   result = hawkman.parse_figma(url, output_format=OutputFormat.HTML_CSS)
   ```

### Issue: Performance is Slow

**Problem:** Parsing takes too long

**Solutions:**
1. **Reduce parsing depth:**
   ```python
   result = hawkman.parse_figma(url, parsing_depth=ParsingDepth.FRAME)
   ```

2. **Disable verification:**
   ```python
   result = hawkman.parse_figma(url, verify=False)  # Much faster
   ```

3. **Analyze complexity first:**
   ```python
   analysis = hawkman.analyze_complexity(url)
   if analysis['layer_count'] > 100:
       print("⚠️ Complex design - may take time")
   ```

---

## Advanced Topics

### Custom Code Generation

Extend Hawkman with custom output formats:

```python
class CustomHawkman(HawkmanStructuralParser):
    def _generate_vue_tailwind(self, layer: Dict[str, Any]) -> str:
        """Generate Vue component with Tailwind"""
        # Your custom Vue generation logic
        pass

    def _determine_output_format(self, structure):
        # Override to include Vue option
        if self.should_use_vue(structure):
            return 'vue_tailwind'
        return super()._determine_output_format(structure)
```

### Batch Processing

Process multiple Figma files:

```python
figma_urls = [
    "https://www.figma.com/design/...",
    "https://www.figma.com/design/...",
    "https://www.figma.com/design/..."
]

results = []
for url in figma_urls:
    result = parse_figma_to_code(url, verify=False)  # Faster without verify
    results.append(result)
    print(f"✅ Processed: {url} ({result['accuracy_score']}%)")

# Analyze batch results
avg_accuracy = sum(r['accuracy_score'] for r in results) / len(results)
print(f"Average Accuracy: {avg_accuracy:.1f}%")
```

### Database Queries

Query Hawkman's parsing history:

```python
import json

# Load parsing history
with open(hawkman.parsing_history_db, 'r') as f:
    history = json.load(f)

# Find high-accuracy parsings
successful_parsings = [
    p for p in history['parsings']
    if p['accuracy_score'] >= 95
]

print(f"Found {len(successful_parsings)} high-accuracy parsings")

# Find optimal format for similar layer counts
similar_parsings = [
    p for p in history['parsings']
    if 20 <= p['layer_count'] <= 30
]

# Most common format for this complexity
from collections import Counter
format_counts = Counter(p['output_format'] for p in similar_parsings)
print(f"Most common format: {format_counts.most_common(1)}")
```

### Integration with CI/CD

Automate Figma-to-code conversion in your pipeline:

```python
# ci_hawkman.py
import sys
from core.justice_league.hawkman_structural_parser import parse_figma_to_code

def main():
    figma_url = sys.argv[1]
    output_file = sys.argv[2]

    result = parse_figma_to_code(
        figma_url=figma_url,
        output_format="react_tailwind",
        verify=True
    )

    if result['accuracy_score'] < 90:
        print(f"❌ FAILED: Accuracy {result['accuracy_score']}% below threshold")
        sys.exit(1)

    with open(output_file, 'w') as f:
        f.write(result['generated_code'])

    print(f"✅ SUCCESS: {output_file} generated with {result['accuracy_score']}% accuracy")
    sys.exit(0)

if __name__ == '__main__':
    main()
```

Usage in CI:
```bash
python ci_hawkman.py "https://www.figma.com/..." src/components/Generated.tsx
```

---

## Testing

Run the comprehensive test suite:

```bash
cd tests
python test_hawkman.py
```

Test coverage includes:
- ✅ Figma URL parsing and validation
- ✅ Layer counting and hierarchy traversal
- ✅ Complexity analysis (depth, children, components)
- ✅ Output format selection logic
- ✅ Parsing depth strategies
- ✅ HTML/CSS generation
- ✅ HTML+Tailwind generation
- ✅ React+Tailwind generation
- ✅ Tailwind class mapping
- ✅ Database operations
- ✅ Component boundary detection
- ✅ Convenience function

---

## Contributing

To extend Hawkman's capabilities:

1. **Add new output formats:** Implement `_generate_YOUR_FORMAT()` method
2. **Improve complexity analysis:** Enhance `_determine_output_format()` logic
3. **Add component detection patterns:** Extend `component_indicators` list
4. **Optimize performance:** Improve `_parse_layer_hierarchy()` efficiency
5. **Submit test cases:** Add tests to `tests/test_hawkman.py`

---

## Version History

### v1.0.0 (October 24, 2025)
- 🦅 Initial release
- ✅ Layer-by-layer Figma parsing
- ✅ Adaptive output format selection (HTML/CSS, HTML+Tailwind, React+Tailwind)
- ✅ Visual verification loop with Green Arrow
- ✅ Pattern learning integration with Oracle
- ✅ Comprehensive test suite
- ✅ Full documentation

---

## Support

**Documentation:** `HAWKMAN_README.md` (this file)
**Examples:** `examples/example_hawkman.py`
**Tests:** `tests/test_hawkman.py`
**Justice League:** `JUSTICE_LEAGUE_README.md`

---

**🦅 Hawkman - Archaeological Precision for Figma-to-Code Conversion**

*Part of the Justice League v1.8.0 - Coordination Protocol v2.0*
