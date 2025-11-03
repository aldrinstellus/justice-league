#!/usr/bin/env python3
"""
Check Penpot API Endpoints
"""

import requests
import json

PENPOT_API = "https://design.penpot.app"

print("🔍 PENPOT API CHECKER")
print("=" * 80)

# Try to get API documentation
print("\n📚 Fetching API documentation...")

# Try different endpoints
endpoints = [
    "/api/doc",
    "/api/openapi.json",
    "/api/openapi",
    "/api/rpc/doc"
]

for endpoint in endpoints:
    url = f"{PENPOT_API}{endpoint}"
    print(f"\n🔗 Trying: {url}")

    try:
        response = requests.get(url, timeout=10)
        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            print(f"   ✅ Success!")

            # Try to parse as JSON
            try:
                data = response.json()
                print(f"   Response type: {type(data)}")

                if isinstance(data, dict):
                    print(f"   Keys: {list(data.keys())[:10]}")
                elif isinstance(data, list):
                    print(f"   Items: {len(data)}")
                    if data:
                        print(f"   First item type: {type(data[0])}")
                        if isinstance(data[0], str):
                            print(f"   First few items: {data[:5]}")

                # Save to file
                output_file = f"penpot_api_doc_{endpoint.replace('/', '_')}.json"
                with open(output_file, 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"   💾 Saved to: {output_file}")

            except Exception as e:
                print(f"   Not JSON format: {str(e)}")
                print(f"   Content preview: {response.text[:200]}")

        elif response.status_code == 404:
            print(f"   ❌ Not Found")
        elif response.status_code == 401:
            print(f"   🔒 Authentication Required")
        else:
            print(f"   ⚠️  Status {response.status_code}")

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

print("\n" + "=" * 80)
print("✅ API CHECK COMPLETE!")
