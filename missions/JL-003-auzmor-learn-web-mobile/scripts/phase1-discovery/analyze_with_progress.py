#!/usr/bin/env python3
"""
JL-003 Analysis Mode: File-by-File Analysis with Progress Bar
Oracle: Live progress tracking for all 182 Figma files
"""

import os
import json
import requests
import time
from datetime import datetime

# Figma API Configuration
FIGMA_TOKEN = 'figd_aPXrH3Rqpm8sdez_nHmmXKHvZ9vcK3sOcJwvhE7s'
FIGMA_API_BASE = 'https://api.figma.com/v1'

# Quicksilver Export Pricing
COST_PER_FRAME_PNG = 0.0025
COST_PER_FRAME_PDF = 0.0030

def analyze_file(file_key, file_name):
    """Analyze single file and return structure"""
    headers = {'X-Figma-Token': FIGMA_TOKEN}

    try:
        response = requests.get(
            f"{FIGMA_API_BASE}/files/{file_key}",
            headers=headers,
            timeout=30
        )

        if response.status_code != 200:
            return {'error': f'HTTP {response.status_code}', 'pages': 0, 'frames': 0}

        data = response.json()
        document = data.get('document', {})
        pages = document.get('children', [])

        # Count frames
        total_frames = 0
        for page in pages:
            for child in page.get('children', []):
                if child.get('type') == 'FRAME':
                    total_frames += 1

        return {
            'pages': len(pages),
            'frames': total_frames,
            'components': len(data.get('components', {}))
        }
    except:
        return {'error': 'Failed', 'pages': 0, 'frames': 0}

def progress_bar(current, total, width=50):
    """Generate progress bar"""
    percent = (current / total) * 100
    filled = int(width * current / total)
    bar = '█' * filled + '░' * (width - filled)
    return f"[{bar}] {current}/{total} ({percent:.1f}%)"

# Load files
with open('phase1-files-list.json', 'r') as f:
    data = json.load(f)

files = data['files']
total = len(files)

print("\n" + "="*80)
print("🔮 ORACLE: JL-003 Analysis Mode - File-by-File Processing")
print("="*80)
print(f"📁 Total Files: {total}")
print(f"⏱️  Estimated Time: ~{total * 1.2 / 60:.1f} minutes")
print("="*80)
print()

results = []
total_pages = 0
total_frames = 0
total_components = 0

for idx, file_info in enumerate(files, 1):
    # Progress bar
    print(f"\r{progress_bar(idx-1, total)}  ", end='', flush=True)

    # File info
    name_short = file_info['name'][:50]
    print(f"\n📊 [{idx}/{total}] {name_short}")

    # Analyze
    result = analyze_file(file_info['key'], file_info['name'])

    # Calculate costs
    frames = result.get('frames', 0)
    png_cost = frames * COST_PER_FRAME_PNG
    pdf_cost = frames * COST_PER_FRAME_PDF
    total_cost = png_cost + pdf_cost

    # Store result
    file_result = {
        'file_key': file_info['key'],
        'file_name': file_info['name'],
        'last_modified': file_info.get('last_modified', 'Unknown'),
        'pages': result.get('pages', 0),
        'frames': frames,
        'components': result.get('components', 0),
        'png_cost': round(png_cost, 2),
        'pdf_cost': round(pdf_cost, 2),
        'total_cost': round(total_cost, 2)
    }
    results.append(file_result)

    # Update totals
    total_pages += result.get('pages', 0)
    total_frames += frames
    total_components += result.get('components', 0)

    # Show result
    if 'error' in result:
        print(f"   ❌ {result['error']}")
    else:
        print(f"   ✅ Pages: {result['pages']}, Frames: {frames}, Cost: ${total_cost:.2f}")

    # Rate limiting
    time.sleep(1.2)

# Final progress bar
print(f"\r{progress_bar(total, total)}")
print()
print("="*80)
print("✅ ANALYSIS COMPLETE!")
print("="*80)
print(f"📊 Total Pages: {total_pages:,}")
print(f"🖼️  Total Frames: {total_frames:,}")
print(f"🧩 Total Components: {total_components:,}")
print(f"💰 Total PNG Cost: ${total_frames * COST_PER_FRAME_PNG:.2f}")
print(f"💰 Total PDF Cost: ${total_frames * COST_PER_FRAME_PDF:.2f}")
print(f"💰 Total Combined Cost: ${total_frames * (COST_PER_FRAME_PNG + COST_PER_FRAME_PDF):.2f}")
print("="*80)

# Save results
output = {
    'analysis_date': datetime.now().isoformat(),
    'total_files': total,
    'total_pages': total_pages,
    'total_frames': total_frames,
    'total_components': total_components,
    'total_png_cost': round(total_frames * COST_PER_FRAME_PNG, 2),
    'total_pdf_cost': round(total_frames * COST_PER_FRAME_PDF, 2),
    'total_combined_cost': round(total_frames * (COST_PER_FRAME_PNG + COST_PER_FRAME_PDF), 2),
    'files': results
}

with open('detailed-analysis.json', 'w') as f:
    json.dump(output, f, indent=2)

print("\n💾 Results saved to: detailed-analysis.json")
print()
