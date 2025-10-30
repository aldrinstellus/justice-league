#!/usr/bin/env python3
"""
Test script for Figma frame export functionality
Tests the complete pipeline: Superman → Hawkman → Oracle
"""

import os
import sys
from pathlib import Path

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from core.justice_league import SupermanCoordinator


def test_frame_export():
    """Test the complete frame export pipeline"""

    print("=" * 70)
    print("🧪 TESTING FIGMA FRAME EXPORT PIPELINE")
    print("=" * 70)
    print()

    # Check for Figma token
    figma_token = os.getenv('FIGMA_ACCESS_TOKEN')
    if not figma_token:
        print("❌ FIGMA_ACCESS_TOKEN not found in environment")
        print("   Please set it in .env file or environment")
        return False

    print(f"✅ Figma token found: {figma_token[:10]}...")
    print()

    # Test file key (using a public Figma design community file)
    # You can replace this with your own file key
    test_file_key = "6Pmf9gCcUccyqbCO9nN6Ts"  # Replace with actual file key

    print(f"📋 Test File Key: {test_file_key}")
    print()

    # Initialize Superman
    print("🦸 Step 1: Initialize Superman Coordinator")
    try:
        superman = SupermanCoordinator()
        print("   ✅ Superman initialized successfully")

        # Check if Hawkman is available
        if not superman.hawkman:
            print("   ❌ Hawkman not available")
            return False
        print("   ✅ Hawkman is available")

        # Check if Oracle is available
        if superman.oracle:
            print("   ✅ Oracle is available (will track exports)")
        else:
            print("   ⚠️  Oracle not available (tracking disabled)")

        print()

    except Exception as e:
        print(f"   ❌ Failed to initialize Superman: {e}")
        return False

    # Test mission configuration
    print("🦸 Step 2: Configure Export Mission")
    mission = {
        'file_key': test_file_key,
        'output_dir': 'test_exports',  # Custom test directory
        'scale': 2.0
    }
    print(f"   File Key: {mission['file_key']}")
    print(f"   Output Dir: {mission['output_dir']}")
    print(f"   Scale: {mission['scale']}x")
    print()

    # Deploy Hawkman
    print("🦸 Step 3: Deploy Hawkman for Frame Export")
    try:
        result = superman._deploy_hawkman_frame_export(mission)

        if not result:
            print("   ❌ Deployment failed - Hawkman returned None")
            return False

        print()

    except Exception as e:
        print(f"   ❌ Deployment error: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Check results
    print("🦸 Step 4: Verify Results")
    if result.get('success'):
        frames_exported = result.get('frames_exported', 0)
        exported_files = result.get('exported_files', [])
        output_dir = result.get('output_dir')

        print(f"   ✅ Export successful!")
        print(f"   📊 Frames exported: {frames_exported}")
        print(f"   📁 Output directory: {output_dir}")
        print()

        # 🦇 BATMAN VERIFICATION CHECK
        print("🦸 Step 5: Check Batman Verification")
        verification = result.get('verification')
        if verification:
            expected = verification.get('expected_count', 0)
            exported = verification.get('exported_count', 0)
            complete = verification.get('complete', False)
            completeness = verification.get('completeness_percentage', 0)

            if complete:
                print(f"   ✅ Batman Verification: PASSED")
                print(f"      Expected: {expected} | Exported: {exported} | Completeness: {completeness:.1f}%")
            else:
                print(f"   ⚠️  Batman Verification: INCOMPLETE")
                print(f"      Expected: {expected} | Exported: {exported} | Completeness: {completeness:.1f}%")
                print(f"      Missing: {verification.get('missing_count', 0)} frames")
                print(f"      Verdict: {verification.get('batman_verdict', 'N/A')}")
        else:
            print(f"   ⚠️  Batman Verification: NOT AVAILABLE (Batman not initialized)")
        print()

        if exported_files:
            print("   📸 Exported frames:")
            for i, file_info in enumerate(exported_files, 1):
                frame_name = file_info['frame_name']
                node_id = file_info['node_id']
                file_path = file_info['file_path']

                # Check if file exists
                exists = Path(file_path).exists()
                status = "✅" if exists else "❌"

                print(f"   {i}. {status} {frame_name} (ID: {node_id})")
                print(f"      └─ {file_path}")
            print()

        print("=" * 70)
        print("✅ TEST PASSED - Frame export pipeline working correctly!")
        print("=" * 70)
        return True

    else:
        print(f"   ❌ Export failed")
        errors = result.get('errors', ['Unknown error'])
        for error in errors:
            print(f"      Error: {error}")
        print()
        print("=" * 70)
        print("❌ TEST FAILED")
        print("=" * 70)
        return False


if __name__ == "__main__":
    success = test_frame_export()
    sys.exit(0 if success else 1)
