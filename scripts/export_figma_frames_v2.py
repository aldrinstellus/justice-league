#!/usr/bin/env python3
"""
🔮 ORACLE'S ENHANCED FIGMA FRAME EXPORT (v2.0)
================================================

Enhanced with:
- Retry logic with exponential backoff (3 attempts per frame)
- Increased timeouts (60s API, 120s CDN)
- Non-interactive mode (auto-accept partial exports in CLI)
- Better error handling and recovery

Usage:
    python3 scripts/export_figma_frames_v2.py --file-key <KEY>
    python3 scripts/export_figma_frames_v2.py --url "<FIGMA_URL>"
    python3 scripts/export_figma_frames_v2.py --file-key <KEY> --output <DIR>

Created: 2025-10-30 (Oracle Enhanced)
"""

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from core.justice_league import SupermanCoordinator
from core.justice_league.mission_control_narrator import get_narrator
from core.justice_league.hawkman_retry_patch import export_frame_with_retry


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Export all frames from a Figma file as PNG images (Enhanced with retry logic)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export using file key
  python3 scripts/export_figma_frames_v2.py --file-key 6Pmf9gCcUccyqbCO9nN6Ts

  # Export using Figma URL
  python3 scripts/export_figma_frames_v2.py --url "https://www.figma.com/file/ABC123/My-Design"

  # Custom output directory
  python3 scripts/export_figma_frames_v2.py --file-key ABC123 --output exports/

  # Custom scale and max retries
  python3 scripts/export_figma_frames_v2.py --file-key ABC123 --scale 3.0 --max-retries 5

Output:
  Frames will be saved as: {file_name}/{page_name}/{frame-name}_{node-id}.png
        """
    )

    # Input source (file key or URL)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--file-key',
        type=str,
        help='Figma file key (e.g., 6Pmf9gCcUccyqbCO9nN6Ts)'
    )
    input_group.add_argument(
        '--url',
        type=str,
        help='Figma file URL (file key will be extracted)'
    )

    # Output options
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        help='Output directory for PNG files (default: auto-generated with timestamp)'
    )

    parser.add_argument(
        '--scale',
        '-s',
        type=float,
        default=2.0,
        help='Export scale from 1.0 to 4.0 (default: 2.0)'
    )

    parser.add_argument(
        '--max-retries',
        type=int,
        default=3,
        help='Maximum retry attempts per frame (default: 3)'
    )

    # Figma token
    parser.add_argument(
        '--token',
        type=str,
        help='Figma access token (or set FIGMA_ACCESS_TOKEN env var)'
    )

    # Non-interactive mode
    parser.add_argument(
        '--non-interactive',
        action='store_true',
        help='Non-interactive mode: auto-accept partial exports'
    )

    return parser.parse_args()


def extract_file_key_from_url(url: str) -> Optional[str]:
    """Extract Figma file key from URL"""
    import re
    # Match: https://www.figma.com/file/{FILE_KEY}/...
    # Or: https://www.figma.com/design/{FILE_KEY}/...
    match = re.search(r'figma\.com/(?:file|design)/([A-Za-z0-9]+)', url)
    if match:
        return match.group(1)
    return None


def create_progress_bar(current: int, total: int, width: int = 25) -> str:
    """Create a visual progress bar"""
    if total == 0:
        return "░" * width

    filled = int((current / total) * width)
    bar = "█" * filled + "░" * (width - filled)
    percentage = int((current / total) * 100)
    return f"{bar} {current}/{total} ({percentage}%)"


def main():
    """Main execution function"""
    args = parse_args()

    # Validate scale
    if not (1.0 <= args.scale <= 4.0):
        print(f"❌ Error: Scale must be between 1.0 and 4.0 (got {args.scale})")
        sys.exit(1)

    # Extract file key from URL if provided
    if args.url:
        file_key = extract_file_key_from_url(args.url)
        if not file_key:
            print(f"❌ Error: Could not extract file key from URL: {args.url}")
            sys.exit(1)
    else:
        file_key = args.file_key

    # Check for Figma token
    figma_token = args.token or os.getenv('FIGMA_ACCESS_TOKEN')
    if not figma_token:
        print("❌ Error: Figma access token not found!")
        print("   Set FIGMA_ACCESS_TOKEN environment variable or use --token argument")
        print("\n   Example:")
        print("   export FIGMA_ACCESS_TOKEN='figd_...'")
        sys.exit(1)

    # Set token in environment
    os.environ['FIGMA_ACCESS_TOKEN'] = figma_token

    # Show Justice League banner
    narrator = get_narrator()
    narrator.show_justice_league_banner(mission_type="Enhanced Figma Frame PNG Export (v2.0)")

    # Determine output directory
    if args.output:
        output_dir = args.output
        print(f"📁 Output Directory: {output_dir}")
    else:
        # Auto-generate with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        output_dir = f"figma-export-{timestamp}"
        print(f"📁 Output Directory: {output_dir} (auto-generated)")

    # Convert to absolute path
    output_dir_abs = str(Path(output_dir).resolve())
    Path(output_dir_abs).mkdir(parents=True, exist_ok=True)

    print(f"✅ Output directory: {output_dir_abs}")
    print(f"🔄 Max retries per frame: {args.max_retries}")
    print(f"📏 Export scale: {args.scale}x")
    print()

    # Initialize Superman
    try:
        superman = SupermanCoordinator()
    except Exception as e:
        print(f"❌ Failed to initialize Superman: {e}")
        sys.exit(1)

    # Progress tracking
    start_time = time.time()
    progress_data = {'current': 0, 'total': 0, 'failed': []}

    def progress_callback(current: int, total: int, frame_name: str):
        """Progress callback with clean single-line updates"""
        progress_data['current'] = current
        progress_data['total'] = total
        progress_bar = create_progress_bar(current, total, width=25)
        print(f"\r🦅 Exporting frames... {progress_bar}", end='', flush=True)

    # Build mission with enhanced retry configuration
    mission = {
        'file_key': file_key,
        'output_dir': output_dir_abs,
        'scale': args.scale,
        'max_retries': args.max_retries,  # Pass retry config to Superman
        'progress_callback': progress_callback,
        'show_count_first': True
    }

    # Deploy mission
    try:
        print("🔍 Scanning Figma file...")
        result = superman._deploy_hawkman_frame_export(mission)

        if not result:
            print("\n❌ Error: Hawkman not available or deployment failed")
            sys.exit(1)

        # Move to new line after progress bar
        if progress_data['total'] > 0:
            print()

        # Calculate duration
        duration = time.time() - start_time
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        duration_str = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"

        print()
        print("=" * 70)

        if result.get('success'):
            print("✅ Export Complete!")
            print("=" * 70)
            print()
            print(f"   Frames exported: {result.get('frames_exported', 0)}")

            # Completeness check
            verification = result.get('verification')
            if verification:
                print()
                print("📊 Completeness Check:")
                expected = verification.get('expected_count', 0)
                exported = verification.get('exported_count', 0)

                if verification.get('complete'):
                    print(f"   Expected: {expected} frames")
                    print(f"   Exported: {exported} files ✅")
                else:
                    print(f"   Expected: {expected} frames")
                    print(f"   Exported: {exported} files ⚠️")
                    print(f"   Missing: {verification.get('missing_count', 0)} frames")
                    print()
                    print(f"   🦇 {verification.get('batman_verdict', 'Verification incomplete')}")

                    # Auto-accept in non-interactive mode
                    if args.non_interactive:
                        print()
                        print("🤖 Non-interactive mode: Auto-accepting partial export")
                    else:
                        # Interactive prompt
                        print()
                        print("❓ Accept partial export? (Y/n): ", end='', flush=True)
                        try:
                            choice = input().strip().upper()
                            if choice == 'N':
                                print()
                                print("❌ Export rejected by user")
                                sys.exit(1)
                        except EOFError:
                            print()
                            print("🤖 Non-interactive context detected: Auto-accepting")

            print()
            print(f"   Output directory: {output_dir_abs}")
            print(f"   Duration: {duration_str}")
            print()
            print("🎉 All frames exported successfully!")

        else:
            print("❌ Export Failed!")
            print("=" * 70)
            errors = result.get('errors', ['Unknown error'])
            for error in errors:
                print(f"   Error: {error}")
            sys.exit(1)

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
