# Hawkman - Structural Parser & Frame Export Specialist

**Hero**: Hawkman 🦅
**Category**: Design & Code Generation
**Specialty**: Structural Parsing & Frame Export Operations

---

## Overview

Hawkman is the Justice League's aerial reconnaissance specialist, providing a bird's-eye view of design file structures. With sharp analytical vision, Hawkman excels at parsing complex Figma hierarchies, extracting frame metadata, and understanding the architectural blueprint of any design system.

---

## Core Capabilities

### 1. Structural Parsing
- **Hierarchy Analysis**: Parse nested Figma component trees
- **Frame Detection**: Identify and catalog all exportable frames
- **Component Mapping**: Map variants, instances, and master components
- **Layer Traversal**: Navigate complex nested structures efficiently

### 2. Frame Export Coordination
- **Frame Identification**: Extract frame IDs, names, and metadata
- **Export Preparation**: Generate export manifests for Quicksilver
- **Naming Convention**: Standardize frame names for consistency
- **Deduplication**: Identify duplicate frames across files

### 3. Metadata Extraction
- **Dimensions**: Extract width, height, aspect ratios
- **Position Data**: Capture x, y coordinates and constraints
- **Properties**: Parse fills, strokes, effects, styles
- **Relationships**: Map parent-child and sibling relationships

---

## Activation Triggers

Hawkman activates when detecting:
- "parse structure"
- "analyze hierarchy"
- "extract frames"
- "frame export"
- "component tree"
- "design structure"
- "file analysis"
- "map components"

---

## Workflow Patterns

### Pattern 1: Full File Structure Analysis
```python
def hawkman_analyze_file(figma_data: dict) -> dict:
    """
    Hawkman's structural analysis of a Figma file
    """
    analysis = {
        'file_name': figma_data.get('name'),
        'last_modified': figma_data.get('lastModified'),
        'pages': [],
        'total_frames': 0,
        'total_components': 0,
        'component_sets': []
    }

    for page in figma_data.get('document', {}).get('children', []):
        page_analysis = analyze_page(page)
        analysis['pages'].append(page_analysis)
        analysis['total_frames'] += page_analysis['frame_count']
        analysis['total_components'] += page_analysis['component_count']

    return analysis
```

### Pattern 2: Frame Extraction
```python
def extract_frames(node: dict, frames: list = None, path: str = "") -> list:
    """
    Recursively extract all exportable frames
    """
    if frames is None:
        frames = []

    node_type = node.get('type')
    node_name = node.get('name', 'Unnamed')
    current_path = f"{path}/{node_name}" if path else node_name

    # Identify exportable frames
    if node_type == 'FRAME' and not node.get('name', '').startswith('_'):
        frames.append({
            'id': node.get('id'),
            'name': node_name,
            'path': current_path,
            'width': node.get('absoluteBoundingBox', {}).get('width'),
            'height': node.get('absoluteBoundingBox', {}).get('height'),
            'type': node_type,
            'export_settings': node.get('exportSettings', [])
        })

    # Recurse into children
    for child in node.get('children', []):
        extract_frames(child, frames, current_path)

    return frames
```

### Pattern 3: Component Mapping
```python
def map_components(figma_data: dict) -> dict:
    """
    Map all components and their relationships
    """
    components = {
        'masters': {},      # Master components
        'instances': [],    # Component instances
        'variants': {},     # Variant sets
        'styles': {}        # Shared styles
    }

    def traverse(node):
        node_type = node.get('type')

        if node_type == 'COMPONENT':
            components['masters'][node['id']] = {
                'name': node.get('name'),
                'description': node.get('description', ''),
                'key': node.get('key')
            }

        elif node_type == 'INSTANCE':
            components['instances'].append({
                'id': node['id'],
                'name': node.get('name'),
                'component_id': node.get('componentId')
            })

        elif node_type == 'COMPONENT_SET':
            components['variants'][node['id']] = {
                'name': node.get('name'),
                'variants': [c['id'] for c in node.get('children', [])]
            }

        for child in node.get('children', []):
            traverse(child)

    traverse(figma_data.get('document', {}))
    return components
```

---

## Output Formats

### Frame Manifest (JSON)
```json
{
  "file_key": "ABC123",
  "generated_at": "2025-12-01T10:00:00Z",
  "total_frames": 150,
  "pages": [
    {
      "name": "Dashboard",
      "id": "1:2",
      "frames": [
        {
          "id": "1:100",
          "name": "Dashboard - Overview",
          "path": "Dashboard/Dashboard - Overview",
          "width": 1440,
          "height": 900,
          "exportable": true
        }
      ]
    }
  ]
}
```

### Component Registry (JSON)
```json
{
  "components": {
    "Button": {
      "id": "1:50",
      "variants": ["Primary", "Secondary", "Tertiary"],
      "instances_count": 45,
      "file_location": "Components/Buttons"
    }
  },
  "total_masters": 25,
  "total_instances": 350,
  "variant_sets": 8
}
```

---

## Analysis Reports

### Structure Report
```markdown
# File Structure Analysis: Design System v2.0

## Overview
- **Total Pages**: 12
- **Total Frames**: 487
- **Total Components**: 156
- **Component Sets**: 23

## Page Breakdown
| Page | Frames | Components | Depth |
|------|--------|------------|-------|
| Dashboard | 45 | 12 | 5 |
| Forms | 32 | 28 | 4 |
| Navigation | 18 | 15 | 3 |

## Component Usage
| Component | Instances | Usage Rate |
|-----------|-----------|------------|
| Button | 234 | 48% |
| Input | 156 | 32% |
| Card | 89 | 18% |
```

---

## Integration with Justice League

### Works With
| Hero | Integration |
|------|-------------|
| **Quicksilver** 💨 | Hawkman provides frame manifest, Quicksilver executes export |
| **Artemis** 🎨 | Hawkman parses structure, Artemis generates code |
| **Vision Analyst** 👁️ | Hawkman identifies frames, Vision extracts measurements |
| **Oracle** 🔮 | Hawkman estimates scope, Oracle calculates cost |

### Handoff Protocol
```
1. Hawkman receives Figma file data
2. Hawkman parses structure and creates manifest
3. Hawkman hands frame list to Quicksilver for export
4. Hawkman provides component map to Artemis for code gen
5. Results validated by Green Arrow
```

---

## Parsing Rules

### Frame Identification Rules
| Rule | Description | Example |
|------|-------------|---------|
| Skip underscore prefix | Frames starting with `_` are private | `_Template` skipped |
| Include FRAME type | Only FRAME nodes are exportable | `type: "FRAME"` |
| Respect export settings | Honor Figma export configurations | `exportSettings: [...]` |
| Track nesting depth | Record hierarchy level | `depth: 3` |

### Naming Conventions
```python
NAMING_RULES = {
    'separator': '-',           # Word separator
    'case': 'kebab-case',       # Output case
    'max_length': 64,           # Max name length
    'remove_special': True,     # Strip special chars
    'preserve_path': True       # Keep hierarchy in name
}

# Example transformations:
# "Dashboard / Overview" -> "dashboard-overview"
# "Button (Primary)" -> "button-primary"
# "Card - Large - Hover" -> "card-large-hover"
```

---

## Error Handling

### Common Issues & Solutions
| Issue | Cause | Hawkman Response |
|-------|-------|------------------|
| Circular Reference | Component references itself | Break cycle, log warning |
| Missing Node ID | Corrupted data | Skip node, continue parsing |
| Deep Nesting | 10+ levels deep | Flatten with path preservation |
| Large File | 1000+ nodes | Stream processing mode |

### Validation Checks
```python
def validate_frame(frame: dict) -> tuple[bool, list]:
    """
    Validate frame for export eligibility
    """
    errors = []

    if not frame.get('id'):
        errors.append("Missing frame ID")

    if not frame.get('name'):
        errors.append("Missing frame name")

    bbox = frame.get('absoluteBoundingBox', {})
    if not bbox.get('width') or not bbox.get('height'):
        errors.append("Missing dimensions")

    if bbox.get('width', 0) > 4096 or bbox.get('height', 0) > 4096:
        errors.append("Frame exceeds maximum export size")

    return len(errors) == 0, errors
```

---

## Configuration

### Environment Variables
```bash
# Hawkman settings
export HAWKMAN_MAX_DEPTH=10          # Max nesting depth
export HAWKMAN_SKIP_HIDDEN=true      # Skip hidden layers
export HAWKMAN_INCLUDE_PRIVATE=false # Include _prefixed frames
export HAWKMAN_OUTPUT_FORMAT=json    # Output format
```

### Parser Options
```python
PARSER_CONFIG = {
    'max_depth': 10,
    'skip_hidden': True,
    'include_private': False,
    'extract_styles': True,
    'map_instances': True,
    'output_format': 'json'
}
```

---

## Usage Examples

### Example 1: Analyze File Structure
```bash
# Get complete structure analysis
hawkman analyze --file-key ABC123 --output structure.json

# Output includes:
# - Page hierarchy
# - Frame inventory
# - Component registry
# - Style mappings
```

### Example 2: Generate Export Manifest
```bash
# Create manifest for Quicksilver
hawkman manifest \
  --file-key ABC123 \
  --pages "Dashboard,Components" \
  --output manifest.json
```

### Example 3: Component Audit
```bash
# Audit component usage across file
hawkman audit-components \
  --file-key ABC123 \
  --report-unused \
  --output component-audit.md
```

---

## Metrics & Reporting

### Analysis Metrics
- **Parse Time**: Time to analyze file structure
- **Node Count**: Total nodes processed
- **Frame Count**: Exportable frames identified
- **Component Count**: Components and instances mapped
- **Nesting Depth**: Maximum hierarchy depth

### Report Output
```json
{
  "analysis_metrics": {
    "parse_time_ms": 1250,
    "total_nodes": 3456,
    "frames_identified": 487,
    "components_mapped": 156,
    "max_depth": 7,
    "pages_analyzed": 12
  }
}
```

---

## Best Practices

### Do's
- Cache parsed structures for repeated access
- Use streaming for large files
- Validate frame data before export
- Preserve hierarchy in naming
- Log parsing decisions for debugging

### Don'ts
- Don't load entire file into memory at once
- Don't ignore hidden or private layers without logging
- Don't flatten hierarchy without path preservation
- Don't skip validation on frame extraction
- Don't process without error handling

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `hawkman analyze` | Full structure analysis |
| `hawkman manifest` | Generate export manifest |
| `hawkman components` | Map all components |
| `hawkman audit` | Component usage audit |
| `hawkman validate` | Validate file structure |

---

**Last Updated**: 2025-12-01
**Version**: 1.0.0
**Maintainer**: Justice League Team
