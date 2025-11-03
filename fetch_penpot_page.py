#!/usr/bin/env python3
"""
Fetch Penpot Page Data with Objects
"""

import sys
sys.path.insert(0, '/Users/admin/Documents/claudecode/Projects/aldo-vision')

from core.penpot_api_connector import PenpotAPIConnector
import json
from pathlib import Path

# Credentials
PENPOT_API = "https://design.penpot.app"
USERNAME = "aldrin@atc.xyz"
PASSWORD = "Fishfingers123!"

# IDs
FILE_ID = "10e879d4-e5a6-801a-8006-ff63c5d92e14"
PAGE_ID = "523f8b68-3ad0-80e5-8006-ff6389e79e54"

print("🎨 PENPOT PAGE DATA FETCHER")
print("=" * 80)

# Initialize connector
print("\n🔐 Authenticating with Penpot...")
connector = PenpotAPIConnector(
    api_url=PENPOT_API,
    username=USERNAME,
    password=PASSWORD
)

# Authenticate
if not connector.authenticate():
    print("❌ Authentication failed!")
    sys.exit(1)

print("✅ Successfully authenticated!")

# Fetch page data
print(f"\n📥 Fetching page: {PAGE_ID}")
print(f"   From file: {FILE_ID}")

page_data = connector.get_page_data(FILE_ID, PAGE_ID)

if not page_data:
    print("❌ Failed to fetch page data")
    sys.exit(1)

print("✅ Page data retrieved!")

# Save to file
output_path = Path("penpot_page_data.json")
with open(output_path, 'w') as f:
    json.dump(page_data, f, indent=2)

print(f"\n💾 Saved to: {output_path}")

# Analyze page structure
print("\n" + "="*80)
print("📊 PAGE ANALYSIS")
print("="*80)

page_name = page_data.get('name', 'Unknown')
page_id = page_data.get('id', 'Unknown')

print(f"\n📄 Page: {page_name}")
print(f"   ID: {page_id}")

# Get objects
objects = page_data.get('objects', {})
print(f"\n🎨 Total Objects: {len(objects)}")

# Count by type
type_counts = {}
for obj_id, obj in objects.items():
    obj_type = obj.get('type', 'unknown')
    type_counts[obj_type] = type_counts.get(obj_type, 0) + 1

print(f"\n📦 Object Types:")
for obj_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"   • {obj_type}: {count}")

# Find frames (top-level components)
frames = []
for obj_id, obj in objects.items():
    if obj.get('type') == 'frame':
        frames.append(obj)

print(f"\n🖼️  Frames: {len(frames)}")
if frames:
    print("\n   Top frames:")
    for i, frame in enumerate(frames[:10], 1):
        frame_name = frame.get('name', f'Frame {i}')
        frame_id = frame.get('id', 'unknown')
        width = frame.get('width', 0)
        height = frame.get('height', 0)
        children_ids = frame.get('shapes', [])
        print(f"   {i}. {frame_name}")
        print(f"      Size: {width:.0f}×{height:.0f}px")
        print(f"      ID: {frame_id}")
        print(f"      Children: {len(children_ids)}")

print("\n✅ PAGE FETCH COMPLETE!")
print(f"📂 Page data saved to: {output_path}")
print(f"📊 File size: {output_path.stat().st_size / 1024:.1f} KB")

print("\n🚀 Ready to convert to React!")
print("   Next: Build Penpot-to-React converter")
