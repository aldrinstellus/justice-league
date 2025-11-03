#!/usr/bin/env python3
"""
Analyze Penpot Structure for React Conversion
"""

import json
from pathlib import Path
from collections import defaultdict

print("🔍 PENPOT STRUCTURE ANALYZER")
print("=" * 80)

# Load page data
with open('penpot_page_data.json', 'r') as f:
    page_data = json.load(f)

objects = page_data.get('objects', {})

print(f"\n📊 Loaded {len(objects)} objects")

# Sample different object types
samples = defaultdict(list)

for obj_id, obj in objects.items():
    obj_type = obj.get('type', 'unknown')
    if len(samples[obj_type]) < 2:  # Get 2 samples of each type
        samples[obj_type].append((obj_id, obj))

print("\n" + "="*80)
print("📦 OBJECT TYPE SAMPLES")
print("="*80)

for obj_type, sample_list in sorted(samples.items()):
    print(f"\n🔹 {obj_type.upper()}")
    print("-" * 80)

    for obj_id, obj in sample_list:
        print(f"\nObject ID: {obj_id}")
        print(f"Keys: {list(obj.keys())}")

        # Show key properties
        if 'name' in obj:
            print(f"Name: {obj['name']}")
        if 'width' in obj and 'height' in obj:
            print(f"Size: {obj['width']:.1f}×{obj['height']:.1f}")
        if 'x' in obj and 'y' in obj:
            print(f"Position: ({obj['x']:.1f}, {obj['y']:.1f})")

        # Styling properties
        styling_keys = [
            'fills', 'strokes', 'fill-color', 'fill-opacity',
            'stroke-color', 'stroke-width', 'stroke-opacity',
            'font-family', 'font-size', 'font-weight', 'text-align',
            'typography-ref-id', 'typography-ref-file',
            'opacity', 'blend-mode', 'shadow', 'blur',
            'rx', 'ry', 'r'  # border radius
        ]

        styling = {k: obj[k] for k in styling_keys if k in obj}
        if styling:
            print(f"Styling: {json.dumps(styling, indent=2)}")

        # Layout properties
        layout_keys = [
            'layout', 'layout-flex-dir', 'layout-gap', 'layout-align-items',
            'layout-justify-content', 'layout-padding',
            'layout-grid', 'layout-grid-columns', 'layout-grid-rows'
        ]

        layout = {k: obj[k] for k in layout_keys if k in obj}
        if layout:
            print(f"Layout: {json.dumps(layout, indent=2)}")

        # Hierarchy
        if 'shapes' in obj:
            print(f"Children: {len(obj['shapes'])} shapes")
        if 'parent-id' in obj:
            print(f"Parent: {obj['parent-id']}")

# Analyze frame hierarchy
print("\n" + "="*80)
print("🌳 FRAME HIERARCHY ANALYSIS")
print("="*80)

# Find root frames (frames with no parent or root parent)
root_frames = []
for obj_id, obj in objects.items():
    if obj.get('type') == 'frame':
        parent_id = obj.get('parent-id')
        if not parent_id or parent_id == '00000000-0000-0000-0000-000000000000':
            root_frames.append((obj_id, obj))

print(f"\nFound {len(root_frames)} root frames")

def print_frame_tree(obj_id, obj, objects, indent=0):
    """Recursively print frame hierarchy"""
    prefix = "  " * indent
    name = obj.get('name', 'Unnamed')
    obj_type = obj.get('type', 'unknown')
    width = obj.get('width', 0)
    height = obj.get('height', 0)

    print(f"{prefix}├─ {name} ({obj_type}) [{width:.0f}×{height:.0f}]")

    # Get children
    children_ids = obj.get('shapes', [])
    if children_ids and indent < 3:  # Limit depth
        for child_id in children_ids[:5]:  # Limit to first 5 children
            if child_id in objects:
                child_obj = objects[child_id]
                print_frame_tree(child_id, child_obj, objects, indent + 1)

        if len(children_ids) > 5:
            print(f"{prefix}  └─ ... and {len(children_ids) - 5} more")

# Print first few root frames with their children
for i, (frame_id, frame_obj) in enumerate(root_frames[:3], 1):
    print(f"\n{i}. Root Frame Tree:")
    print_frame_tree(frame_id, frame_obj, objects)

# Analyze text objects
print("\n" + "="*80)
print("📝 TEXT CONTENT ANALYSIS")
print("="*80)

texts = [(obj_id, obj) for obj_id, obj in objects.items() if obj.get('type') == 'text']
print(f"\nFound {len(texts)} text objects")

print("\nSample text content:")
for i, (obj_id, obj) in enumerate(texts[:10], 1):
    content = obj.get('content', {})
    text_value = content.get('children', [{}])[0].get('text', '') if content else ''
    if text_value:
        text_value = text_value[:50]  # Truncate
    print(f"{i}. \"{text_value}\"")

# Analyze colors and typography
print("\n" + "="*80)
print("🎨 DESIGN SYSTEM ANALYSIS")
print("="*80)

# Load file data for colors and typography
with open('penpot_design_data.json', 'r') as f:
    file_data = json.load(f)

data = file_data.get('data', {})
colors = data.get('colors', [])
typographies = data.get('typographies', [])

print(f"\nColor Palette: {len(colors)} colors")
if colors:
    for i, color in enumerate(colors[:10], 1):
        print(f"{i}. {color}")

print(f"\nTypography Styles: {len(typographies)} styles")
if typographies:
    for i, typo in enumerate(typographies[:5], 1):
        print(f"{i}. {typo}")

print("\n✅ ANALYSIS COMPLETE!")
print("\n🔍 Key Findings:")
print("   • Penpot uses SVG-like structure with objects dict")
print("   • Frames represent containers (like divs)")
print("   • Layout properties include Flexbox-like attributes")
print("   • Styling is comprehensive (fills, strokes, typography)")
print("   • Hierarchy is parent-child with 'shapes' array")
print("   • Text content stored in nested structure")
print("   • Design tokens available (colors, typographies)")
print("\n📋 Next Steps for Converter:")
print("   1. Map Penpot object types to React components")
print("   2. Convert layout properties to CSS Flexbox/Grid")
print("   3. Extract and apply styling (colors, fonts, borders)")
print("   4. Build component tree from hierarchy")
print("   5. Handle text content properly")
print("   6. Use shadcn/ui components where appropriate")
