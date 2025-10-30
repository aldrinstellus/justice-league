#!/usr/bin/env python3
"""
Download image assets from Figma API
"""

import os
import json
import requests
from pathlib import Path

# Configuration
FIGMA_TOKEN = os.environ.get('FIGMA_ACCESS_TOKEN')
if not FIGMA_TOKEN:
    raise ValueError("FIGMA_ACCESS_TOKEN environment variable not set. Please set it before running this script.")
FILE_KEY = "fubdMARNgA2lVhmzpPg77y"
OUTPUT_DIR = Path("html/assets/images")

def get_image_refs():
    """Extract all image references from Figma data"""
    with open('figma_dashboard10_raw.json', 'r') as f:
        data = json.load(f)

    image_refs = set()

    def find_images(node):
        """Recursively find all image references"""
        fills = node.get('fills', [])
        for fill in fills:
            if fill.get('type') == 'IMAGE':
                image_ref = fill.get('imageRef')
                if image_ref:
                    image_refs.add(image_ref)

        for child in node.get('children', []):
            find_images(child)

    # Start recursion
    nodes = data.get('nodes', {})
    for node_id, node_data in nodes.items():
        document = node_data.get('document', {})
        find_images(document)

    return list(image_refs)

def download_images(image_refs):
    """Download images from Figma"""
    print(f"📥 Found {len(image_refs)} images to download")

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Get image URLs from Figma API
    print("🔗 Getting image URLs from Figma...")
    ids = ','.join(image_refs)
    url = f"https://api.figma.com/v1/images/{FILE_KEY}?ids={ids}&format=png&scale=2"
    headers = {"X-Figma-Token": FIGMA_TOKEN}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to get image URLs: {response.status_code}")
        print(response.text)
        return

    image_urls = response.json().get('images', {})

    # Download each image
    print(f"💾 Downloading {len(image_urls)} images...")
    for i, (node_id, image_url) in enumerate(image_urls.items(), 1):
        if not image_url:
            print(f"   ⚠️  No URL for {node_id}")
            continue

        # Find the image ref for this node
        image_ref = None
        for ref in image_refs:
            if node_id in ref or ref in node_id:
                image_ref = ref
                break

        if not image_ref:
            # Use node_id as fallback
            image_ref = node_id

        output_file = OUTPUT_DIR / f"{image_ref}.png"

        try:
            img_response = requests.get(image_url, timeout=30)
            if img_response.status_code == 200:
                with open(output_file, 'wb') as f:
                    f.write(img_response.content)
                print(f"   ✅ [{i}/{len(image_urls)}] Downloaded: {output_file.name}")
            else:
                print(f"   ❌ [{i}/{len(image_urls)}] Failed: {output_file.name}")
        except Exception as e:
            print(f"   ❌ [{i}/{len(image_urls)}] Error: {str(e)}")

    print(f"\n✅ Downloaded {len(list(OUTPUT_DIR.glob('*.png')))} images to {OUTPUT_DIR}")

def main():
    print("=" * 80)
    print("📥 FIGMA ASSET DOWNLOADER")
    print("=" * 80)

    # Get image references
    image_refs = get_image_refs()

    if not image_refs:
        print("⚠️  No images found in Figma data")
        return

    # Download images
    download_images(image_refs)

    print("\n" + "=" * 80)
    print("✅ ASSET DOWNLOAD COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
