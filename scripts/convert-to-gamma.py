#!/usr/bin/env python3
"""
Convert Markdown Slides to Gamma.app Presentation

This script reads markdown slide files from a presentation directory and creates
a comprehensive Gamma presentation using the Gamma API.

Global script location: ~/.claude/scripts/convert-to-gamma.py

Usage:
    # From a presentation directory with slides/ folder
    cd /path/to/presentation
    python3 ~/.claude/scripts/convert-to-gamma.py

    # Or with explicit path
    python3 ~/.claude/scripts/convert-to-gamma.py --dir /path/to/presentation

    # Show help
    python3 ~/.claude/scripts/convert-to-gamma.py --help

Requirements:
    - GAMMA_API_KEY in /Users/admin/Documents/claudecode/api/.env
    - slides/ directory with markdown files (01-xxx.md, 02-xxx.md, etc.)
    - python-dotenv and requests packages

Author: Justice League Agentic AI System
"""

import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

# Parse command line arguments FIRST
parser = argparse.ArgumentParser(
    description='Convert markdown slides to Gamma.app presentation',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
    # Run from presentation directory
    cd /path/to/presentation
    python3 ~/.claude/scripts/convert-to-gamma.py

    # Specify directory explicitly
    python3 ~/.claude/scripts/convert-to-gamma.py --dir /path/to/presentation
    python3 ~/.claude/scripts/convert-to-gamma.py -d ~/my-presentation

    # Show this help
    python3 ~/.claude/scripts/convert-to-gamma.py --help
"""
)
parser.add_argument(
    '--dir', '-d',
    type=str,
    help='Presentation directory containing slides/ folder. Defaults to current working directory.',
    default=None
)
parser.add_argument(
    '--title', '-t',
    type=str,
    help='Custom presentation title. Defaults to auto-detect from first slide.',
    default=None
)
parser.add_argument(
    '--slides', '-s',
    type=int,
    help='Number of slides to generate (default: auto-detect based on content)',
    default=35
)
args = parser.parse_args()

# Set presentation directory (from args or current working directory)
PRESENTATION_DIR = Path(args.dir) if args.dir else Path.cwd()
SLIDES_DIR = PRESENTATION_DIR / "slides"

# Validate directory exists
if not PRESENTATION_DIR.exists():
    print(f"❌ Error: Presentation directory not found: {PRESENTATION_DIR}")
    sys.exit(1)

if not SLIDES_DIR.exists():
    print(f"❌ Error: No slides/ folder found in: {PRESENTATION_DIR}")
    print(f"   Expected: {SLIDES_DIR}")
    print(f"\n   Make sure your presentation directory has a 'slides/' subdirectory with markdown files.")
    sys.exit(1)

# Load environment variables from global API folder
ENV_PATHS = [
    "/Users/admin/Documents/claudecode/api/.env",
    "/Users/admin/Documents/claudecode/justice-league-missions/.env",
    Path.home() / ".env",
    PRESENTATION_DIR / ".env",
]

for env_path in ENV_PATHS:
    env_path = Path(env_path)
    if env_path.exists():
        load_dotenv(env_path)

GAMMA_API_KEY = os.getenv("GAMMA_API_KEY")
if not GAMMA_API_KEY:
    print("❌ Error: GAMMA_API_KEY not found")
    print(f"   Searched in: {[str(p) for p in ENV_PATHS]}")
    print(f"\n   Please set GAMMA_API_KEY in one of the above .env files.")
    sys.exit(1)

# API Configuration
GAMMA_API_BASE = "https://public-api.gamma.app/v1.0"
HEADERS = {
    "Content-Type": "application/json",
    "X-API-KEY": GAMMA_API_KEY
}


def read_all_slides():
    """Read all slide markdown files and combine them"""

    # Find all markdown files in slides directory
    slide_files = sorted([f for f in SLIDES_DIR.glob("*.md")])

    if not slide_files:
        print(f"❌ Error: No markdown files found in {SLIDES_DIR}")
        sys.exit(1)

    # Try to extract title from first slide
    presentation_title = args.title or "Presentation"

    combined_content = ""

    print(f"📖 Reading slide files from: {SLIDES_DIR}")
    print(f"   Found {len(slide_files)} slide files")

    for filepath in slide_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

            # Extract title from first slide if not provided
            if presentation_title == "Presentation" and not combined_content:
                lines = content.strip().split('\n')
                for line in lines:
                    if line.startswith('# '):
                        presentation_title = line[2:].strip()
                        break

            # Remove duplicate part header comments
            content = content.replace("# Part ", "\n## Part ")
            combined_content += content + "\n\n---\n\n"

        print(f"  ✅ {filepath.name}")

    print(f"\n✅ Combined {len(slide_files)} slide files")
    print(f"📊 Total content length: {len(combined_content):,} characters")
    print(f"📝 Presentation title: {presentation_title}")

    return combined_content, presentation_title


def create_gamma_presentation(content, title):
    """Create Gamma presentation via API"""

    print("\n🚀 Creating Gamma presentation...")

    # Prepare API request
    payload = {
        "inputText": content,
        "textMode": "preserve",  # Preserve our markdown structure
        "format": "presentation",
        "numCards": args.slides,
        "cardOptions": {
            "dimensions": "16x9"  # Standard presentation aspect ratio
        },
        "additionalInstructions": f"""
This is a professional presentation titled: {title}

Key requirements:
- Preserve all code blocks with syntax highlighting
- Keep all metrics, tables, and performance data
- Maintain technical depth and authenticity
- Format for professional delivery (clear headings, bullet points, visual hierarchy)

Style: Professional, data-driven, authentic
        """.strip()
    }

    # Create generation request
    print("  📤 Sending request to Gamma API...")
    response = requests.post(
        f"{GAMMA_API_BASE}/generations",
        headers=HEADERS,
        json=payload,
        timeout=60
    )

    if response.status_code not in (200, 201):
        print(f"❌ Error creating presentation: {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit(1)

    result = response.json()
    generation_id = result.get("id") or result.get("generationId")

    if not generation_id:
        print(f"❌ Error: No generation ID returned")
        print(f"Response: {json.dumps(result, indent=2)}")
        sys.exit(1)

    print(f"  ✅ Generation started: {generation_id}")

    # Poll for completion
    return poll_generation_status(generation_id)


def poll_generation_status(generation_id, max_wait=300):
    """Poll generation status until complete"""

    print(f"\n⏳ Waiting for generation to complete...")
    print(f"  Generation ID: {generation_id}")

    start_time = time.time()
    poll_interval = 5  # seconds

    while True:
        elapsed = time.time() - start_time

        if elapsed > max_wait:
            print(f"\n❌ Timeout: Generation took longer than {max_wait}s")
            sys.exit(1)

        # Check status
        response = requests.get(
            f"{GAMMA_API_BASE}/generations/{generation_id}",
            headers=HEADERS,
            timeout=30
        )

        if response.status_code != 200:
            print(f"❌ Error checking status: {response.status_code}")
            print(f"Response: {response.text}")
            sys.exit(1)

        status_data = response.json()
        status = status_data.get("status")

        if status == "completed":
            print(f"\n✅ Generation complete! (took {elapsed:.1f}s)")
            return status_data

        elif status == "failed":
            error = status_data.get("error", "Unknown error")
            print(f"\n❌ Generation failed: {error}")
            sys.exit(1)

        else:
            # Still processing
            print(f"  ⏳ Status: {status} ({elapsed:.1f}s elapsed)")
            time.sleep(poll_interval)


def main():
    """Main conversion workflow"""

    print("=" * 70)
    print("  MARKDOWN SLIDES → GAMMA.APP CONVERTER")
    print("=" * 70)
    print(f"\n📁 Working directory: {PRESENTATION_DIR}")
    print(f"📂 Slides directory: {SLIDES_DIR}")

    # Step 1: Read all slides
    content, title = read_all_slides()

    # Step 2: Create Gamma presentation
    result = create_gamma_presentation(content, title)

    # Step 3: Extract presentation URL (check multiple possible keys)
    gamma_url = result.get("gammaUrl") or result.get("url") or result.get("webUrl")
    web_url = result.get("webUrl") or result.get("shareUrl")

    print("\n" + "=" * 70)
    print("  ✅ SUCCESS - PRESENTATION CREATED")
    print("=" * 70)

    print(f"\n📊 **Presentation Details**:")
    print(f"  • Title: {title}")
    print(f"  • Source: {SLIDES_DIR}")

    print(f"\n🔗 **Access URLs**:")
    if gamma_url:
        print(f"  • Gamma Editor: {gamma_url}")
    if web_url:
        print(f"  • Shareable Link: {web_url}")

    print(f"\n🎯 **Next Steps**:")
    print(f"  1. Open the Gamma Editor link above")
    print(f"  2. Review and customize theme/styling if needed")
    print(f"  3. Share the presentation link with your audience")
    print(f"  4. Present live or export as PDF/PPTX")

    print("\n" + "=" * 70)

    # Save result to file
    result_file = PRESENTATION_DIR / "gamma-presentation-result.json"
    with open(result_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"💾 Full result saved to: {result_file}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
