#!/usr/bin/env python3
"""
Figma Frame PNG Export Script
==============================

This script exports all top-level frames from a Figma file as PNG images.

Usage:
    # Using Figma file key
    python3 scripts/export_figma_frames.py --file-key 6Pmf9gCcUccyqbCO9nN6Ts

    # Using Figma URL
    python3 scripts/export_figma_frames.py --url "https://www.figma.com/file/6Pmf9gCcUccyqbCO9nN6Ts/Dashboard"

    # Custom output directory
    python3 scripts/export_figma_frames.py --file-key 6Pmf9gCcUccyqbCO9nN6Ts --output exports/my-frames/

    # Custom scale (1.0-4.0, default 2.0)
    python3 scripts/export_figma_frames.py --file-key 6Pmf9gCcUccyqbCO9nN6Ts --scale 3.0

Coordination:
    - 🦸 Superman coordinates the mission
    - 🦅 Hawkman performs the frame exports
    - 🔮 Oracle tracks export metadata (optional)

Output:
    PNG files saved with format: {frame-name}_{node-id}.png

Created: 2025-10-30
Version: 1.0.0
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


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Export all frames from a Figma file as PNG images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export using file key
  python3 scripts/export_figma_frames.py --file-key 6Pmf9gCcUccyqbCO9nN6Ts

  # Export using Figma URL
  python3 scripts/export_figma_frames.py --url "https://www.figma.com/file/ABC123/My-Design"

  # Custom output directory and scale
  python3 scripts/export_figma_frames.py --file-key ABC123 --output exports/ --scale 3.0

Output:
  Frames will be saved as: {frame-name}_{node-id}.png
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
        help='Output directory for PNG files (default: data/hawkman/figma_exports/)'
    )

    parser.add_argument(
        '--scale',
        '-s',
        type=float,
        default=2.0,
        help='Export scale from 1.0 to 4.0 (default: 2.0)'
    )

    # Figma token
    parser.add_argument(
        '--token',
        type=str,
        help='Figma access token (or set FIGMA_ACCESS_TOKEN env var)'
    )

    return parser.parse_args()


def validate_scale(scale: float) -> bool:
    """Validate scale is within acceptable range"""
    return 1.0 <= scale <= 4.0


def get_output_directory(interactive: bool = True) -> str:
    """
    Prompt user for output directory (interactive mode) or use default

    Args:
        interactive: If True, prompt user for folder name

    Returns:
        Absolute path to output directory
    """
    if not interactive:
        # Default folder with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d")
        default_folder = f"figma-export-{timestamp}"
        return str(Path.cwd() / default_folder)

    # Interactive mode: ask user for folder name
    print()
    timestamp = datetime.now().strftime("%Y-%m-%d")
    default_folder = f"figma-export-{timestamp}"

    user_input = input(f"📁 Where do you want to save these frames?\n   (default: {default_folder}): ").strip()

    folder_name = user_input if user_input else default_folder

    # Convert to absolute path
    if Path(folder_name).is_absolute():
        output_path = Path(folder_name)
    else:
        output_path = Path.cwd() / folder_name

    return str(output_path)


def create_progress_bar(current: int, total: int, width: int = 20) -> str:
    """
    Create a visual progress bar

    Args:
        current: Current progress
        total: Total items
        width: Width of progress bar in characters

    Returns:
        Progress bar string
    """
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
    if not validate_scale(args.scale):
        print(f"❌ Error: Scale must be between 1.0 and 4.0 (got {args.scale})")
        sys.exit(1)

    # Check for Figma token
    figma_token = args.token or os.getenv('FIGMA_ACCESS_TOKEN')
    if not figma_token:
        print("❌ Error: Figma access token not found!")
        print("   Set FIGMA_ACCESS_TOKEN environment variable or use --token argument")
        print("\n   Example:")
        print("   export FIGMA_ACCESS_TOKEN='figd_...'")
        sys.exit(1)

    # Set token in environment for Hawkman
    os.environ['FIGMA_ACCESS_TOKEN'] = figma_token

    # Show Justice League banner
    narrator = get_narrator()
    narrator.show_justice_league_banner(mission_type="Figma Frame PNG Export")

    # Determine output directory (interactive or CLI-provided)
    if args.output:
        # Non-interactive: use provided output
        output_dir = args.output
        print(f"📁 Output Directory: {output_dir}")
    else:
        # Interactive: ask user for folder name
        output_dir = get_output_directory(interactive=True)

    # Convert to absolute path for Oracle preference
    output_dir_abs = str(Path(output_dir).resolve())

    print()
    print(f"✅ Output directory: {output_dir_abs}")
    print()

    # Initialize Superman
    try:
        superman = SupermanCoordinator()
    except Exception as e:
        print(f"❌ Failed to initialize Superman: {e}")
        sys.exit(1)

    # Progress tracking variables
    start_time = time.time()
    progress_data = {'current': 0, 'total': 0}

    def progress_callback(current: int, total: int, frame_name: str):
        """Callback for progress updates - shows clean single-line progress"""
        progress_data['current'] = current
        progress_data['total'] = total
        progress_bar = create_progress_bar(current, total, width=25)
        # Use \r to overwrite same line
        print(f"\r🦅 Exporting frames... {progress_bar}", end='', flush=True)

    # Build mission with progress callback
    mission = {
        'file_key': args.file_key if args.file_key else None,
        'figma_url': args.url if args.url else None,
        'output_dir': output_dir_abs,
        'scale': args.scale,
        'progress_callback': progress_callback,
        'show_count_first': True  # Pre-count frames
    }

    # Deploy Hawkman
    try:
        print("🔍 Scanning Figma file...")
        result = superman._deploy_hawkman_frame_export(mission)

        if not result:
            print("\n❌ Error: Hawkman not available or deployment failed")
            sys.exit(1)

        # Print newline to complete progress bar line
        if progress_data['total'] > 0:
            print()  # Move to new line after progress bar

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

            # 🦇 BATMAN VERIFICATION: Show completeness check
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
                    print(f"   Exported: {exported} files ❌")
                    print(f"   Missing: {verification.get('missing_count', 0)} frames")
                    print()
                    print(f"   🦇 {verification.get('batman_verdict', 'Verification incomplete')}")

                    # Interactive prompt - user wants to decide what to do
                    print()
                    print("❓ What would you like to do?")
                    print("   [A] Accept as-is (continue with partial export)")
                    print("   [F] Fail (exit with error)")
                    choice = input("   Your choice (A/F): ").strip().upper()

                    if choice == 'F':
                        print()
                        print("❌ Export failed - user chose to reject incomplete export")
                        sys.exit(1)
                    elif choice == 'A':
                        print()
                        print("✅ Accepted partial export - continuing...")
                    else:
                        print()
                        print("⚠️  Invalid choice - defaulting to Accept")

            print()
            print(f"   Output directory: {output_dir_abs}")
            print(f"   Total size: ~{result.get('frames_exported', 0) * 0.38:.0f} MB (estimated)")
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
        print("\n\n⚠️  Export interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
