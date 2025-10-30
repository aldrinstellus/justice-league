#!/usr/bin/env python3
"""
Setup script for Figma API access and token configuration
"""

import os
import sys
from pathlib import Path

def check_figma_token():
    """Check if Figma API token is configured"""
    token = os.environ.get('FIGMA_ACCESS_TOKEN')

    if not token:
        print("❌ FIGMA_ACCESS_TOKEN not found in environment variables")
        print("\n📋 To get your Figma Personal Access Token:")
        print("   1. Go to https://www.figma.com/settings")
        print("   2. Scroll to 'Personal Access Tokens' section")
        print("   3. Click 'Create a new personal access token'")
        print("   4. Give it a name (e.g., 'Aldo Vision Conversion')")
        print("   5. Copy the generated token")
        print("\n🔧 To set the token:")
        print("   Option 1 (Session): export FIGMA_ACCESS_TOKEN='your-token-here'")
        print("   Option 2 (Permanent): Add to ~/.zshrc or ~/.bashrc")
        print("   Option 3 (Project): Create .env file in this directory")
        return None

    print(f"✅ FIGMA_ACCESS_TOKEN found: {token[:10]}...{token[-4:]}")
    return token

def test_figma_connection(token: str, file_key: str = "fubdMARNgA2lVhmzpPg77y"):
    """Test Figma API connection"""
    import requests

    print(f"\n🔍 Testing Figma API connection...")
    print(f"   File Key: {file_key}")

    url = f"https://api.figma.com/v1/files/{file_key}"
    headers = {"X-Figma-Token": token}

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Successfully connected to Figma!")
            print(f"   File Name: {data.get('name', 'Unknown')}")
            print(f"   Last Modified: {data.get('lastModified', 'Unknown')}")
            return True
        elif response.status_code == 403:
            print("❌ Access denied - Check if your token has the correct permissions")
            return False
        elif response.status_code == 404:
            print("❌ File not found - Check if the file key is correct")
            return False
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(f"   {response.text}")
            return False

    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def get_figma_node_info(token: str, file_key: str, node_id: str):
    """Get information about specific Figma node"""
    import requests

    print(f"\n📊 Fetching node information...")
    print(f"   Node ID: {node_id}")

    url = f"https://api.figma.com/v1/files/{file_key}/nodes?ids={node_id}"
    headers = {"X-Figma-Token": token}

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            nodes = data.get('nodes', {})

            if node_id in nodes:
                node = nodes[node_id]
                doc = node.get('document', {})

                print(f"✅ Node found!")
                print(f"   Name: {doc.get('name', 'Unknown')}")
                print(f"   Type: {doc.get('type', 'Unknown')}")

                if 'absoluteBoundingBox' in doc:
                    bbox = doc['absoluteBoundingBox']
                    print(f"   Size: {bbox.get('width', 0):.0f}x{bbox.get('height', 0):.0f}px")

                return doc
            else:
                print(f"❌ Node {node_id} not found in file")
                return None
        else:
            print(f"❌ Failed to fetch node: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Failed to fetch node info: {str(e)}")
        return None

def main():
    print("=" * 80)
    print("🔮 FIGMA API SETUP & VERIFICATION")
    print("=" * 80)

    # Check token
    token = check_figma_token()

    if not token:
        print("\n⚠️  Please set FIGMA_ACCESS_TOKEN environment variable and try again")
        sys.exit(1)

    # Test connection
    file_key = "fubdMARNgA2lVhmzpPg77y"
    node_id = "3215-58693"

    if test_figma_connection(token, file_key):
        # Get node info
        node_info = get_figma_node_info(token, file_key, node_id)

        if node_info:
            print("\n" + "=" * 80)
            print("✅ SETUP COMPLETE - Ready for conversion!")
            print("=" * 80)
            print(f"\n📋 Target Design:")
            print(f"   URL: https://www.figma.com/design/{file_key}?node-id={node_id}")
            print(f"   Name: {node_info.get('name', 'Unknown')}")
            print(f"   Type: {node_info.get('type', 'Unknown')}")
            print("\n🚀 Next Steps:")
            print("   1. Run: python3 convert_figma_to_html.py")
            print("   2. Generated files will be in: ./new-conversion/")
            sys.exit(0)

    print("\n❌ Setup failed - Please fix the issues above and try again")
    sys.exit(1)

if __name__ == "__main__":
    main()
