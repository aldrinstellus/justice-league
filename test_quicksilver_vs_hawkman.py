#!/usr/bin/env python3
"""
💨🦅 QUICKSILVER VS HAWKMAN - SPEED COMPARISON BENCHMARK
========================================================

Side-by-side performance comparison of:
- 🦅 Hawkman: Reliable sequential export (100% success rate)
- 💨 Quicksilver: Speed-optimized parallel export (2.5-3x faster target)

Usage:
    python3 test_quicksilver_vs_hawkman.py
    python3 test_quicksilver_vs_hawkman.py --file-key YOUR_FILE_KEY
    python3 test_quicksilver_vs_hawkman.py --url "https://www.figma.com/design/..."

Created: 2025-10-31 (Quicksilver v1.0.0)
"""

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import json

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from core.justice_league import QuicksilverSpeedExport, export_frames_quicksilver
from core.justice_league.hawkman_equipped import HawkmanEquipped
from core.justice_league.mission_control_narrator import get_narrator


class PerformanceBenchmark:
    """Benchmark and compare Hawkman vs Quicksilver"""

    def __init__(self, file_key: str, figma_token: Optional[str] = None):
        """
        Initialize benchmark

        Args:
            file_key: Figma file key to test
            figma_token: Figma access token (or use env var)
        """
        self.file_key = file_key
        self.figma_token = figma_token or os.getenv('FIGMA_ACCESS_TOKEN')

        if not self.figma_token:
            raise ValueError("Figma token required. Set FIGMA_ACCESS_TOKEN env var")

        self.narrator = get_narrator()
        self.results = {}

    def show_banner(self):
        """Display benchmark banner"""
        print()
        print("=" * 80)
        print("     💨🦅 QUICKSILVER VS HAWKMAN - PERFORMANCE BENCHMARK")
        print("=" * 80)
        print()
        print(f"   File Key: {self.file_key}")
        print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print("   Testing:")
        print("   - 🦅 Hawkman: Sequential export (baseline)")
        print("   - 💨 Quicksilver: Parallel export (optimized)")
        print()
        print("=" * 80)
        print()

    def benchmark_hawkman(self, output_dir: str) -> Dict[str, Any]:
        """
        Benchmark Hawkman frame export

        Args:
            output_dir: Output directory for PNG files

        Returns:
            Benchmark results dict
        """
        print()
        print("🦅 HAWKMAN BENCHMARK")
        print("-" * 80)
        print()

        try:
            hawkman = HawkmanEquipped(
                figma_token=self.figma_token,
                parsing_data_dir="data/hawkman"
            )

            # Count frames first
            frame_count = hawkman.count_frames(self.file_key)
            print(f"📊 Found {frame_count} frames to export")
            print()

            # Progress tracking
            progress_data = {'current': 0, 'total': frame_count}

            def progress_callback(current, total, frame_name):
                progress_data['current'] = current
                progress_data['total'] = total
                percentage = int((current / total) * 100) if total > 0 else 0
                print(f"\r🦅 Exporting... {current}/{total} ({percentage}%)", end='', flush=True)

            # Benchmark export
            start_time = time.time()

            exported_files = hawkman.export_all_frames_as_png(
                file_key=self.file_key,
                output_dir=output_dir,
                scale=2.0,
                progress_callback=progress_callback
            )

            duration = time.time() - start_time

            # Move to new line after progress bar
            print()
            print()

            return {
                'hero': 'Hawkman',
                'emoji': '🦅',
                'method': 'Sequential',
                'frame_count': frame_count,
                'exported_count': len(exported_files),
                'success_rate': (len(exported_files) / frame_count * 100) if frame_count > 0 else 0,
                'duration_seconds': duration,
                'duration_formatted': self._format_duration(duration),
                'frames_per_second': len(exported_files) / duration if duration > 0 else 0,
                'seconds_per_frame': duration / len(exported_files) if len(exported_files) > 0 else 0,
                'output_dir': output_dir,
                'errors': frame_count - len(exported_files)
            }

        except Exception as e:
            print(f"\n❌ Hawkman benchmark failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                'hero': 'Hawkman',
                'emoji': '🦅',
                'error': str(e),
                'success': False
            }

    def benchmark_quicksilver(self, output_dir: str, max_workers: int = 8) -> Dict[str, Any]:
        """
        Benchmark Quicksilver frame export

        Args:
            output_dir: Output directory for PNG files
            max_workers: Concurrent workers (default: 8)

        Returns:
            Benchmark results dict
        """
        print()
        print("💨 QUICKSILVER BENCHMARK")
        print("-" * 80)
        print()

        try:
            quicksilver = QuicksilverSpeedExport(
                figma_token=self.figma_token,
                parsing_data_dir="data/quicksilver",
                max_workers=max_workers,
                batch_size=15
            )

            # Count frames first
            frame_count = quicksilver.count_frames(self.file_key)
            print(f"📊 Found {frame_count} frames to export")
            print(f"⚡ Using {max_workers} concurrent workers")
            print()

            # Progress tracking
            progress_data = {'current': 0, 'total': frame_count}

            def progress_callback(current, total, frame_name):
                progress_data['current'] = current
                progress_data['total'] = total
                percentage = int((current / total) * 100) if total > 0 else 0
                print(f"\r💨 Exporting... {current}/{total} ({percentage}%)", end='', flush=True)

            # Benchmark export
            start_time = time.time()

            exported_files = quicksilver.export_all_frames_as_png(
                file_key=self.file_key,
                output_dir=output_dir,
                scale=2.0,
                progress_callback=progress_callback
            )

            duration = time.time() - start_time

            # Move to new line after progress bar
            print()
            print()

            return {
                'hero': 'Quicksilver',
                'emoji': '💨',
                'method': f'Parallel ({max_workers} workers)',
                'frame_count': frame_count,
                'exported_count': len(exported_files),
                'success_rate': (len(exported_files) / frame_count * 100) if frame_count > 0 else 0,
                'duration_seconds': duration,
                'duration_formatted': self._format_duration(duration),
                'frames_per_second': len(exported_files) / duration if duration > 0 else 0,
                'seconds_per_frame': duration / len(exported_files) if len(exported_files) > 0 else 0,
                'output_dir': output_dir,
                'errors': frame_count - len(exported_files),
                'max_workers': max_workers
            }

        except Exception as e:
            print(f"\n❌ Quicksilver benchmark failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                'hero': 'Quicksilver',
                'emoji': '💨',
                'error': str(e),
                'success': False
            }

    def compare_results(self, hawkman_results: Dict[str, Any], quicksilver_results: Dict[str, Any]):
        """
        Compare and display results

        Args:
            hawkman_results: Hawkman benchmark results
            quicksilver_results: Quicksilver benchmark results
        """
        print()
        print("=" * 80)
        print("     📊 PERFORMANCE COMPARISON RESULTS")
        print("=" * 80)
        print()

        # Check for errors
        hawkman_success = hawkman_results.get('success', True) and 'error' not in hawkman_results
        quicksilver_success = quicksilver_results.get('success', True) and 'error' not in quicksilver_results

        if not hawkman_success or not quicksilver_success:
            print("❌ One or more benchmarks failed:")
            if not hawkman_success:
                print(f"   🦅 Hawkman: {hawkman_results.get('error', 'Unknown error')}")
            if not quicksilver_success:
                print(f"   💨 Quicksilver: {quicksilver_results.get('error', 'Unknown error')}")
            print()
            return

        # Display side-by-side comparison
        print(f"{'Metric':<30} {'🦅 Hawkman':<25} {'💨 Quicksilver':<25}")
        print("-" * 80)

        # Frame counts
        print(f"{'Total Frames':<30} {hawkman_results['frame_count']:<25} {quicksilver_results['frame_count']:<25}")
        print(f"{'Frames Exported':<30} {hawkman_results['exported_count']:<25} {quicksilver_results['exported_count']:<25}")
        print(f"{'Success Rate':<30} {hawkman_results['success_rate']:.1f}%{'':<20} {quicksilver_results['success_rate']:.1f}%")

        print()

        # Duration
        print(f"{'Export Duration':<30} {hawkman_results['duration_formatted']:<25} {quicksilver_results['duration_formatted']:<25}")
        print(f"{'Frames/Second':<30} {hawkman_results['frames_per_second']:.2f}{'':<21} {quicksilver_results['frames_per_second']:.2f}")
        print(f"{'Seconds/Frame':<30} {hawkman_results['seconds_per_frame']:.2f}{'':<21} {quicksilver_results['seconds_per_frame']:.2f}")

        print()

        # Speedup calculation
        if hawkman_results['duration_seconds'] > 0:
            speedup = hawkman_results['duration_seconds'] / quicksilver_results['duration_seconds']
            time_saved = hawkman_results['duration_seconds'] - quicksilver_results['duration_seconds']

            print(f"{'Speedup':<30} {'1.0x (baseline)':<25} {f'{speedup:.2f}x':<25}")
            print(f"{'Time Saved':<30} {'-':<25} {self._format_duration(time_saved):<25}")

            print()
            print("=" * 80)
            print()

            # Verdict
            if speedup >= 2.5:
                print("✅ EXCELLENT: Quicksilver achieves 2.5x+ speedup target!")
            elif speedup >= 2.0:
                print("✅ GOOD: Quicksilver achieves 2x+ speedup!")
            elif speedup >= 1.5:
                print("⚠️ MODERATE: Quicksilver achieves 1.5x+ speedup (target: 2.5x)")
            else:
                print("❌ BELOW TARGET: Speedup < 1.5x (investigate bottlenecks)")

            print()

            # Success rate comparison
            if quicksilver_results['success_rate'] >= 100:
                print("✅ RELIABILITY: Quicksilver maintains 100% success rate!")
            elif quicksilver_results['success_rate'] >= quicksilver_results['success_rate']:
                print("✅ RELIABILITY: Quicksilver matches Hawkman success rate")
            else:
                print(f"⚠️ RELIABILITY: Quicksilver success rate ({quicksilver_results['success_rate']:.1f}%) below Hawkman ({hawkman_results['success_rate']:.1f}%)")

        print()

        # Method comparison
        print("METHOD COMPARISON:")
        print(f"   🦅 Hawkman: {hawkman_results['method']}")
        print(f"   💨 Quicksilver: {quicksilver_results['method']}")

        print()

        # Output locations
        print("OUTPUT LOCATIONS:")
        print(f"   🦅 Hawkman: {hawkman_results['output_dir']}")
        print(f"   💨 Quicksilver: {quicksilver_results['output_dir']}")

        print()
        print("=" * 80)
        print()

    def _format_duration(self, seconds: float) -> str:
        """Format duration as human-readable string"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"

    def save_benchmark_results(self, hawkman_results: Dict[str, Any], quicksilver_results: Dict[str, Any]):
        """Save benchmark results to JSON file"""
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        results_file = f"benchmark_results_{timestamp}.json"

        results = {
            'timestamp': datetime.now().isoformat(),
            'file_key': self.file_key,
            'hawkman': hawkman_results,
            'quicksilver': quicksilver_results
        }

        # Calculate speedup if both successful
        if 'duration_seconds' in hawkman_results and 'duration_seconds' in quicksilver_results:
            results['speedup'] = hawkman_results['duration_seconds'] / quicksilver_results['duration_seconds']
            results['time_saved_seconds'] = hawkman_results['duration_seconds'] - quicksilver_results['duration_seconds']

        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"📊 Results saved to: {results_file}")
        print()

    def run_benchmark(self, test_quicksilver_only: bool = False, max_workers: int = 8):
        """
        Run complete benchmark

        Args:
            test_quicksilver_only: Only test Quicksilver (skip Hawkman)
            max_workers: Concurrent workers for Quicksilver
        """
        self.show_banner()

        # Create timestamped output directories
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        base_dir = Path(f"benchmark-{timestamp}")
        base_dir.mkdir(exist_ok=True)

        hawkman_dir = str(base_dir / "hawkman-export")
        quicksilver_dir = str(base_dir / "quicksilver-export")

        # Run benchmarks
        if not test_quicksilver_only:
            hawkman_results = self.benchmark_hawkman(hawkman_dir)
        else:
            # Skip Hawkman, create dummy results
            hawkman_results = {
                'hero': 'Hawkman',
                'emoji': '🦅',
                'method': 'Sequential',
                'skipped': True
            }

        quicksilver_results = self.benchmark_quicksilver(quicksilver_dir, max_workers)

        # Compare results
        if not test_quicksilver_only:
            self.compare_results(hawkman_results, quicksilver_results)
            self.save_benchmark_results(hawkman_results, quicksilver_results)
        else:
            print()
            print("=" * 80)
            print("     💨 QUICKSILVER RESULTS (HAWKMAN SKIPPED)")
            print("=" * 80)
            print()
            print(f"Frames Exported: {quicksilver_results.get('exported_count', 0)}/{quicksilver_results.get('frame_count', 0)}")
            print(f"Success Rate: {quicksilver_results.get('success_rate', 0):.1f}%")
            print(f"Duration: {quicksilver_results.get('duration_formatted', 'N/A')}")
            print(f"Speed: {quicksilver_results.get('frames_per_second', 0):.2f} frames/second")
            print()
            print(f"Output: {quicksilver_results['output_dir']}")
            print()
            print("=" * 80)
            print()


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Benchmark Quicksilver vs Hawkman frame export performance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compare both heroes on K-12 POC file (177 frames)
  python3 test_quicksilver_vs_hawkman.py --file-key fubdMARNgA2lVhmzpPg77y

  # Test only Quicksilver (faster testing)
  python3 test_quicksilver_vs_hawkman.py --file-key ABC123 --quicksilver-only

  # Custom worker count
  python3 test_quicksilver_vs_hawkman.py --file-key ABC123 --workers 10

  # Use Figma URL
  python3 test_quicksilver_vs_hawkman.py --url "https://www.figma.com/design/ABC123/..."
        """
    )

    # Input source
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--file-key',
        type=str,
        help='Figma file key'
    )
    input_group.add_argument(
        '--url',
        type=str,
        help='Figma file URL (file key will be extracted)'
    )

    # Options
    parser.add_argument(
        '--quicksilver-only',
        action='store_true',
        help='Only test Quicksilver (skip Hawkman for faster testing)'
    )

    parser.add_argument(
        '--workers',
        type=int,
        default=8,
        help='Concurrent workers for Quicksilver (default: 8)'
    )

    parser.add_argument(
        '--token',
        type=str,
        help='Figma access token (or set FIGMA_ACCESS_TOKEN env var)'
    )

    return parser.parse_args()


def extract_file_key_from_url(url: str) -> Optional[str]:
    """Extract Figma file key from URL"""
    import re
    match = re.search(r'figma\.com/(?:file|design)/([A-Za-z0-9]+)', url)
    if match:
        return match.group(1)
    return None


def main():
    """Main execution function"""
    args = parse_args()

    # Extract file key
    if args.url:
        file_key = extract_file_key_from_url(args.url)
        if not file_key:
            print(f"❌ Error: Could not extract file key from URL: {args.url}")
            sys.exit(1)
    else:
        file_key = args.file_key

    # Get token
    figma_token = args.token or os.getenv('FIGMA_ACCESS_TOKEN')
    if not figma_token:
        print("❌ Error: Figma access token not found!")
        print("   Set FIGMA_ACCESS_TOKEN environment variable or use --token argument")
        sys.exit(1)

    # Run benchmark
    try:
        benchmark = PerformanceBenchmark(file_key, figma_token)
        benchmark.run_benchmark(
            test_quicksilver_only=args.quicksilver_only,
            max_workers=args.workers
        )

    except KeyboardInterrupt:
        print("\n\n⚠️ Benchmark interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
