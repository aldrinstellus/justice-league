#!/usr/bin/env python3
"""
🔮 ORACLE'S STANDALONE FIGMA FRAME EXPORT
==========================================

Completely standalone script with built-in retry logic.
No dependencies on Superman/Hawkman - pure Figma API with robust error handling.

Features:
- 3 retry attempts with exponential backoff
- 60s timeout for API, 120s for CDN downloads
- Non-interactive mode for CLI automation
- Progress bar with real-time updates
- Hierarchical output: {file_name}/{page_name}/{frame}.png

Usage:
    python3 scripts/export_figma_standalone.py --file-key <KEY>
    python3 scripts/export_figma_standalone.py --url "<FIGMA_URL>"

Created: 2025-10-30 (Oracle Solution)
"""

import argparse
import os
import sys
import time
import json
import requests
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple


def sanitize_filename(name: str) -> str:
    """Sanitize a string to be a valid filename"""
    # Replace invalid characters with underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    # Remove leading/trailing spaces and dots
    name = name.strip('. ')
    # Limit length
    return name[:200]


def extract_file_key_from_url(url: str) -> Optional[str]:
    """Extract Figma file key from URL"""
    match = re.search(r'figma\.com/(?:file|design)/([A-Za-z0-9]+)', url)
    if match:
        return match.group(1)
    return None


def download_with_retry(
    url: str,
    headers: dict,
    max_retries: int = 3,
    timeout: int = 60
) -> Tuple[bool, Optional[bytes], Optional[str]]:
    """Download content with exponential backoff retry logic"""
    last_error = None
    backoff_factor = 2.0

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return (True, response.content, None)

        except requests.exceptions.Timeout:
            last_error = f"Timeout after {timeout}s"
            if attempt < max_retries:
                wait_time = backoff_factor ** (attempt - 1)
                print(f"      ⏳ Timeout (attempt {attempt}/{max_retries}), retry in {wait_time:.0f}s...")
                time.sleep(wait_time)

        except requests.exceptions.RequestException as e:
            last_error = str(e)
            if attempt < max_retries:
                wait_time = backoff_factor ** (attempt - 1)
                print(f"      ⚠️ Error (attempt {attempt}/{max_retries}): {e}, retry in {wait_time:.0f}s...")
                time.sleep(wait_time)

    return (False, None, last_error)


def fetch_figma_structure(file_key: str, figma_token: str) -> Dict:
    """Fetch Figma file structure"""
    headers = {"X-Figma-Token": figma_token}
    url = f"https://api.figma.com/v1/files/{file_key}"

    success, content, error = download_with_retry(url, headers, max_retries=3, timeout=60)

    if not success:
        raise Exception(f"Failed to fetch Figma file structure: {error}")

    try:
        data = json.loads(content)
        return data.get('document', {})
    except Exception as e:
        raise Exception(f"Failed to parse Figma API response: {e}")


def export_frame(
    file_key: str,
    node_id: str,
    node_name: str,
    output_path: str,
    figma_token: str,
    scale: float = 2.0,
    max_retries: int = 3
) -> Tuple[bool, Optional[str]]:
    """Export a single frame as PNG with retry logic"""
    headers = {"X-Figma-Token": figma_token}

    # Step 1: Get image URL from Figma API
    api_url = f"https://api.figma.com/v1/images/{file_key}?ids={node_id}&format=png&scale={scale}"

    success, content, error = download_with_retry(api_url, headers, max_retries=max_retries, timeout=60)

    if not success:
        return (False, f"Failed to get image URL: {error}")

    try:
        data = json.loads(content)
        if 'images' not in data or node_id not in data['images']:
            return (False, "No image URL returned from Figma API")
        image_url = data['images'][node_id]
    except Exception as e:
        return (False, f"Failed to parse API response: {e}")

    # Step 2: Download PNG from CDN (longer timeout for large files)
    success, image_content, error = download_with_retry(
        image_url,
        headers={},  # No auth needed for CDN
        max_retries=max_retries,
        timeout=120  # 2 minutes for large images
    )

    if not success:
        return (False, f"Failed to download PNG: {error}")

    # Step 3: Save to file
    try:
        with open(output_path, 'wb') as f:
            f.write(image_content)
        return (True, None)
    except Exception as e:
        return (False, f"Failed to save file: {e}")


def create_progress_bar(current: int, total: int, width: int = 25) -> str:
    """Create visual progress bar"""
    if total == 0:
        return "░" * width

    filled = int((current / total) * width)
    bar = "█" * filled + "░" * (width - filled)
    percentage = int((current / total) * 100)
    return f"{bar} {current}/{total} ({percentage}%)"


def main():
    parser = argparse.ArgumentParser(
        description="Export Figma frames as PNG (Standalone with retry logic)"
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--file-key', type=str, help='Figma file key')
    input_group.add_argument('--url', type=str, help='Figma file URL')

    parser.add_argument('--output', '-o', type=str, help='Output directory')
    parser.add_argument('--scale', '-s', type=float, default=2.0, help='Export scale (1.0-4.0)')
    parser.add_argument('--token', type=str, help='Figma access token')
    parser.add_argument('--max-retries', type=int, default=3, help='Max retry attempts')

    args = parser.parse_args()

    # Validate scale
    if not (1.0 <= args.scale <= 4.0):
        print(f"❌ Error: Scale must be between 1.0 and 4.0")
        sys.exit(1)

    # Extract file key
    if args.url:
        file_key = extract_file_key_from_url(args.url)
        if not file_key:
            print(f"❌ Error: Could not extract file key from URL")
            sys.exit(1)
    else:
        file_key = args.file_key

    # Get Figma token
    figma_token = args.token or os.getenv('FIGMA_ACCESS_TOKEN')
    if not figma_token:
        print("❌ Error: Figma access token not found!")
        print("   Set FIGMA_ACCESS_TOKEN environment variable or use --token")
        sys.exit(1)

    # Determine output directory
    if args.output:
        output_dir = Path(args.output).resolve()
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        output_dir = Path.cwd() / f"figma-export-{timestamp}"

    output_dir.mkdir(parents=True, exist_ok=True)

    # Banner
    print()
    print("★" + "━" * 68 + "★")
    print()
    print("     🔮 ORACLE'S FIGMA FRAME EXPORT (Standalone + Retry Logic)")
    print()
    print("★" + "━" * 68 + "★")
    print()
    print(f"📁 Output: {output_dir}")
    print(f"📏 Scale: {args.scale}x")
    print(f"🔄 Max retries: {args.max_retries}")
    print()

    start_time = time.time()

    try:
        # Fetch file structure
        print("🔍 Scanning Figma file...")
        file_data = fetch_figma_structure(file_key, figma_token)

        # Extract file name
        file_name = file_data.get('name', 'Figma-Export')
        sanitized_file_name = sanitize_filename(file_name)
        file_dir = output_dir / sanitized_file_name
        file_dir.mkdir(parents=True, exist_ok=True)

        print(f"📄 File: {file_name}")
        print()

        # Find all exportable nodes
        exportable_types = {'FRAME', 'COMPONENT', 'COMPONENT_SET'}
        total_nodes = 0
        pages_with_nodes = []

        if 'children' in file_data:
            for child in file_data['children']:
                if child.get('type') == 'CANVAS':
                    page_name = child.get('name', 'Unnamed-Page')
                    page_nodes = []

                    if 'children' in child:
                        for element in child['children']:
                            if element.get('type') in exportable_types:
                                page_nodes.append({
                                    'name': element.get('name', 'Unnamed'),
                                    'id': element.get('id'),
                                    'type': element.get('type')
                                })
                            elif element.get('type') == 'SECTION':
                                if 'children' in element:
                                    for node in element['children']:
                                        if node.get('type') in exportable_types:
                                            page_nodes.append({
                                                'name': node.get('name', 'Unnamed'),
                                                'id': node.get('id'),
                                                'type': node.get('type')
                                            })

                    if page_nodes:
                        pages_with_nodes.append({
                            'page_name': page_name,
                            'nodes': page_nodes
                        })
                        total_nodes += len(page_nodes)

        if total_nodes == 0:
            print("⚠️ No exportable frames found")
            sys.exit(0)

        print(f"📊 Found {total_nodes} exportable nodes across {len(pages_with_nodes)} pages")
        print()

        # Export all frames
        exported_count = 0
        failed_frames = []
        current_node = 0

        for page_data in pages_with_nodes:
            page_name = page_data['page_name']
            nodes = page_data['nodes']

            sanitized_page_name = sanitize_filename(page_name)
            page_dir = file_dir / sanitized_page_name
            page_dir.mkdir(exist_ok=True)

            print(f"📂 Page: {page_name} ({len(nodes)} items)")

            for node in nodes:
                current_node += 1
                node_name = node['name']
                node_id = node['id']

                # Progress bar
                progress_bar = create_progress_bar(current_node, total_nodes, width=25)
                print(f"\r🦅 Exporting... {progress_bar}", end='', flush=True)

                # Export frame
                sanitized_node_name = sanitize_filename(node_name)
                image_filename = f"{sanitized_node_name}_{node_id}.png"
                image_path = page_dir / image_filename

                success, error = export_frame(
                    file_key, node_id, node_name, str(image_path),
                    figma_token, args.scale, args.max_retries
                )

                if success:
                    exported_count += 1
                else:
                    print(f"\r❌ Failed to export {node_name}: {error}" + " " * 20)
                    failed_frames.append({'name': node_name, 'error': error})

        # Move to new line after progress bar
        print()
        print()

        # Summary
        duration = time.time() - start_time
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        duration_str = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"

        print("=" * 70)
        if exported_count == total_nodes:
            print("✅ Export Complete - 100% Success!")
        else:
            print(f"⚠️ Export Partially Complete - {exported_count}/{total_nodes} frames")
        print("=" * 70)
        print()
        print(f"   Exported: {exported_count}/{total_nodes} frames")
        print(f"   Duration: {duration_str}")
        print(f"   Output: {output_dir}")
        print()

        if failed_frames:
            print("❌ Failed Frames:")
            for frame in failed_frames:
                print(f"   - {frame['name']}: {frame['error']}")
            print()

        print("🎉 Export process complete!")
        print()

    except KeyboardInterrupt:
        print("\n\n⚠️ Export interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
