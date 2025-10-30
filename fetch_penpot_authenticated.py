#!/usr/bin/env python3
"""
Fetch Penpot Design with Authentication
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

# File details
FILE_ID = "10e879d4-e5a6-801a-8006-ff63c5d92e14"
PAGE_ID = "523f8b68-3ad0-80e5-8006-ff6389e79e54"

print("🎨 PENPOT DESIGN FETCHER (AUTHENTICATED)")
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

# Fetch file data
print(f"\n📥 Fetching file: {FILE_ID}")
file_data = connector.get_file_data(FILE_ID)

if not file_data:
    print("❌ Failed to fetch file data")
    sys.exit(1)

print("✅ File data retrieved!")

# Save to file
output_path = Path("penpot_design_data.json")
with open(output_path, 'w') as f:
    json.dump(file_data, f, indent=2)

print(f"\n💾 Saved to: {output_path}")

# Analyze structure
print("\n" + "="*80)
print("📊 DESIGN ANALYSIS")
print("="*80)

file_name = file_data.get('name', 'Unknown')
print(f"\n📄 File: {file_name}")
print(f"   ID: {FILE_ID}")

# Get pages
data = file_data.get('data', {})
pages = data.get('pages', [])
print(f"\n📑 Pages: {len(pages)}")
for i, page in enumerate(pages, 1):
    page_name = page.get('name', f'Page {i}')
    page_id = page.get('id', 'unknown')
    is_target = page_id == PAGE_ID
    marker = "👉 TARGET" if is_target else ""
    print(f"   {i}. {page_name} ({page_id}) {marker}")

# Get objects
objects = data.get('objects', {})
print(f"\n🎨 Total Objects: {len(objects)}")

# Count by type
type_counts = {}
for obj_id, obj in objects.items():
    obj_type = obj.get('type', 'unknown')
    type_counts[obj_type] = type_counts.get(obj_type, 0) + 1

print(f"\n📦 Object Types:")
for obj_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"   • {obj_type}: {count}")

# Find target page objects
print(f"\n🎯 Analyzing target page: {PAGE_ID}")
target_page = None
for page in pages:
    if page.get('id') == PAGE_ID:
        target_page = page
        break

if target_page:
    page_name = target_page.get('name', 'Unknown')
    print(f"   Page Name: {page_name}")

    # Get frames on this page
    page_frames = []
    for obj_id, obj in objects.items():
        if obj.get('type') == 'frame' and obj.get('parent-id') == PAGE_ID:
            page_frames.append(obj)

    print(f"   Frames: {len(page_frames)}")
    for i, frame in enumerate(page_frames[:5], 1):
        frame_name = frame.get('name', f'Frame {i}')
        frame_id = frame.get('id', 'unknown')
        width = frame.get('width', 0)
        height = frame.get('height', 0)
        print(f"      {i}. {frame_name} ({width:.0f}×{height:.0f}px) - {frame_id}")

print("\n✅ FETCH COMPLETE!")
print(f"📂 Design data saved to: {output_path}")
print(f"📊 File size: {output_path.stat().st_size / 1024:.1f} KB")

print("\n🚀 Next steps:")
print("   1. Build Penpot-to-React converter")
print("   2. Generate components from frames")
print("   3. Validate accuracy")
