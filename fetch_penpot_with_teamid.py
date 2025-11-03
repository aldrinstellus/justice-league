#!/usr/bin/env python3
"""
Fetch Penpot Design with Team ID
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

# IDs from workspace URL
TEAM_ID = "6f980e07-dac6-80e6-8006-fc1ac72d69f6"  # From workspace URL
FILE_ID = "10e879d4-e5a6-801a-8006-ff63c5d92e14"
PAGE_ID = "523f8b68-3ad0-80e5-8006-ff6389e79e54"

print("🎨 PENPOT DESIGN FETCHER (WITH TEAM ID)")
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

# List projects in team
print(f"\n📁 Fetching projects for team: {TEAM_ID}")
projects = connector.list_projects(team_id=TEAM_ID)

if not projects:
    print("❌ No projects found or failed to fetch projects")
else:
    print(f"✅ Found {len(projects)} projects\n")

    # Display projects
    for i, project in enumerate(projects, 1):
        project_id = project.get('id', 'unknown')
        project_name = project.get('name', 'Unnamed')

        print(f"{i}. {project_name}")
        print(f"   ID: {project_id}")

        # Get files in this project
        print(f"   📄 Fetching files...")
        files = connector.list_files(project_id)

        if files:
            print(f"   Found {len(files)} files:")
            for j, file in enumerate(files, 1):
                file_id = file.get('id', 'unknown')
                file_name = file.get('name', 'Unnamed')
                is_target = file_id == FILE_ID
                marker = " 👉 TARGET FILE" if is_target else ""
                print(f"      {j}. {file_name} (ID: {file_id}){marker}")
        else:
            print(f"   No files found in this project")

        print()

# Try to fetch the specific file
print(f"\n🎯 Fetching target file: {FILE_ID}")
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
pages = data.get('pages-index', [])
print(f"\n📑 Pages: {len(pages)}")
for i, page_id in enumerate(pages[:10], 1):
    print(f"   {i}. Page ID: {page_id}")
    if page_id == PAGE_ID:
        print(f"      👉 TARGET PAGE")

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

print("\n✅ FETCH COMPLETE!")
print(f"📂 Design data saved to: {output_path}")
print(f"📊 File size: {output_path.stat().st_size / 1024:.1f} KB")

print("\n🚀 Next steps:")
print("   1. Analyze Penpot structure and styles")
print("   2. Build Penpot-to-React converter")
print("   3. Generate pixel-perfect components")
