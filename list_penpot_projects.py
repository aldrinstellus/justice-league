#!/usr/bin/env python3
"""
List Penpot Projects and Files
"""

import sys
sys.path.insert(0, '/Users/admin/Documents/claudecode/Projects/aldo-vision')

from core.penpot_api_connector import PenpotAPIConnector
import json

# Credentials
PENPOT_API = "https://design.penpot.app"
USERNAME = "aldrin@atc.xyz"
PASSWORD = "Fishfingers123!"

print("🎨 PENPOT PROJECT LISTER")
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

# List projects
print("\n📁 Fetching projects...")
projects = connector.list_projects()

if not projects:
    print("❌ No projects found or failed to fetch projects")
    sys.exit(1)

print(f"✅ Found {len(projects)} projects\n")

# Display projects
for i, project in enumerate(projects, 1):
    project_id = project.get('id', 'unknown')
    project_name = project.get('name', 'Unnamed')
    team_id = project.get('team-id', 'unknown')

    print(f"{i}. {project_name}")
    print(f"   ID: {project_id}")
    print(f"   Team ID: {team_id}")

    # Get files in this project
    print(f"   📄 Fetching files...")
    files = connector.list_files(project_id)

    if files:
        print(f"   Found {len(files)} files:")
        for j, file in enumerate(files, 1):
            file_id = file.get('id', 'unknown')
            file_name = file.get('name', 'Unnamed')
            print(f"      {j}. {file_name} (ID: {file_id})")
    else:
        print(f"   No files found in this project")

    print()

print("✅ PROJECT LISTING COMPLETE!")
