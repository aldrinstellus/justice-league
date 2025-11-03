#!/usr/bin/env python3
"""
Fetch Penpot Design Data
Extract design from Penpot file for conversion to React code
"""

import requests
import json
from pathlib import Path
import sys

# Penpot file details from user's link
FILE_ID = "10e879d4-e5a6-801a-8006-ff63c5d92e14"
PAGE_ID = "523f8b68-3ad0-80e5-8006-ff6389e79e54"
BOARD_ID = "523f8b68-3ad0-80e5-8006-ff6389e9cff5"
SHARE_ID = "10e879d4-e5a6-801a-8006-ff64694c755e"  # From earlier shared link

PENPOT_API = "https://design.penpot.app"

def fetch_shared_file(share_id: str, file_id: str):
    """Try to fetch file via public share link"""
    print(f"🔍 Attempting to fetch via share link...")
    print(f"   Share ID: {share_id}")
    print(f"   File ID: {file_id}")

    # Try public share endpoint
    url = f"{PENPOT_API}/api/public/share/{share_id}"

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            print("✅ Successfully fetched shared file!")
            return response.json()
        else:
            print(f"❌ Share fetch failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error fetching shared file: {str(e)}")
        return None

def fetch_via_direct_url(file_id: str):
    """Try to fetch file data directly"""
    print(f"\n🔍 Attempting direct API access...")
    print(f"   File ID: {file_id}")

    # Try direct file endpoint (may require auth)
    url = f"{PENPOT_API}/api/rpc/query/file?id={file_id}"

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            print("✅ Successfully fetched file!")
            return response.json()
        elif response.status_code == 401:
            print("⚠️  Authentication required (401)")
            return None
        else:
            print(f"❌ Fetch failed: {response.status_code}")
            if response.text:
                print(f"   Response: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def save_design_data(data, output_path: str):
    """Save fetched design data"""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\n💾 Saved design data to: {output_file}")
    return output_file

def analyze_structure(data):
    """Analyze and display design structure"""
    print("\n" + "="*80)
    print("📊 DESIGN STRUCTURE ANALYSIS")
    print("="*80)

    # File info
    file_name = data.get('name', 'Unknown')
    file_id = data.get('id', 'Unknown')
    print(f"\n📄 File: {file_name}")
    print(f"   ID: {file_id}")

    # Pages
    pages = data.get('data', {}).get('pages', [])
    print(f"\n📑 Pages: {len(pages)}")
    for i, page in enumerate(pages[:5], 1):  # Show first 5
        page_name = page.get('name', f'Page {i}')
        page_id = page.get('id', 'unknown')
        print(f"   {i}. {page_name} ({page_id})")

    # Objects
    objects = data.get('data', {}).get('objects', {})
    print(f"\n🎨 Total Objects: {len(objects)}")

    # Analyze object types
    type_counts = {}
    for obj_id, obj in objects.items():
        obj_type = obj.get('type', 'unknown')
        type_counts[obj_type] = type_counts.get(obj_type, 0) + 1

    print(f"\n📦 Object Types:")
    for obj_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   • {obj_type}: {count}")

    return data

def main():
    print("🎨 PENPOT DESIGN FETCHER")
    print("=" * 80)
    print(f"\n🎯 Target File: {FILE_ID}")
    print(f"   Page: {PAGE_ID}")
    print(f"   Board: {BOARD_ID}")

    # Try share link first
    data = fetch_shared_file(SHARE_ID, FILE_ID)

    # If that fails, try direct access
    if not data:
        data = fetch_via_direct_url(FILE_ID)

    if not data:
        print("\n❌ FAILED TO FETCH DESIGN")
        print("\n💡 Options:")
        print("   1. Provide Penpot credentials to authenticate")
        print("   2. Export design manually from Penpot")
        print("   3. Ensure share link is still active")
        sys.exit(1)

    # Save and analyze
    output_path = "penpot_design_data.json"
    save_design_data(data, output_path)
    analyze_structure(data)

    print("\n✅ FETCH COMPLETE!")
    print(f"\n📂 Design data saved to: {output_path}")
    print("\n🚀 Next steps:")
    print("   1. Run analyzer to understand structure")
    print("   2. Build React converter")
    print("   3. Generate components")

if __name__ == "__main__":
    main()
