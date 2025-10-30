#!/usr/bin/env python3
"""
🦸 Justice League - Figma to Code Conversion
Coordination Protocol v2.0: Oracle → Artemis → Green Arrow → Oracle

Mission: Convert Figma frame to pixel-perfect React component
Target: https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=2-948
"""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.justice_league.superman_coordinator import SupermanCoordinator
from core.justice_league.artemis_codesmith import ArtemisCodeSmith
from core.justice_league.oracle_meta_agent import OracleMeta
from core.justice_league.green_arrow_visual_validator import GreenArrowVisualValidator
from core.justice_league.mission_control_narrator import get_narrator

def main():
    # Initialize narrator and show banner
    narrator = get_narrator()
    narrator.show_justice_league_banner(mission_type="Figma → Code Conversion")

    # Mission parameters
    figma_url = "https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=2-948"
    file_key = "6Pmf9gCcUccyqbCO9nN6Ts"
    node_id = "2-948"
    component_name = "PocTestComponent"

    print(f"\n📋 Mission Details:")
    print(f"   Figma URL: {figma_url}")
    print(f"   File Key: {file_key}")
    print(f"   Node ID: {node_id}")
    print(f"   Component: {component_name}")
    print(f"   Target Accuracy: 99%+")
    print()

    # Initialize Superman Coordinator
    print("🦸 Step 0: Initializing Superman Coordinator...")
    superman = SupermanCoordinator()
    print(f"   ✅ Superman ready with {superman.heroes_available} heroes")
    print()

    # STEP 1: Query Oracle for existing patterns
    print("🔮 Step 1: Querying Oracle for project patterns...")
    oracle = OracleMeta()
    project_context = oracle.get_project_context(file_key)

    if project_context:
        print(f"   ✅ Found {len(project_context.get('shared_components', []))} shared components")
        print(f"   ✅ Found {len(project_context.get('design_tokens', {}))} design tokens")
    else:
        print("   ℹ️  No existing patterns found - this is the first component")
    print()

    # STEP 2: Deploy Artemis with Oracle context
    print("🎨 Step 2: Deploying Artemis for code generation...")
    artemis = ArtemisCodeSmith()

    result = artemis.generate_component_code_expert(
        figma_url=figma_url,
        component_name=component_name,
        framework="next",
        language="typescript",
        options={
            "use_shadcn": True,
            "use_tailwind": True,
            "export_assets": True,
            "generate_tests": False,
        },
        project_context=project_context,
        max_iterations=3,
        target_accuracy=99.0
    )

    print(f"   ✅ Code generated with {result.get('accuracy', 0)}% accuracy")
    print(f"   ✅ Shared elements: {len(result.get('shared_elements', []))}")
    print()

    # Save generated component
    output_dir = Path(__file__).parent / "generated"
    output_dir.mkdir(exist_ok=True)

    component_file = output_dir / f"{component_name}.tsx"
    with open(component_file, 'w') as f:
        f.write(result.get('component_code', ''))

    print(f"   💾 Component saved: {component_file}")
    print()

    # STEP 3: Deploy Green Arrow for WYSIWYG validation
    print("🎯 Step 3: Deploying Green Arrow for WYSIWYG validation...")
    print("   ⚠️  Note: Full validation requires rendered page URL")
    print("   ℹ️  Green Arrow will validate when component is rendered")
    print()

    # STEP 4: Update Oracle with new patterns
    print("🔮 Step 4: Updating Oracle with learned patterns...")
    oracle.update_project_patterns(
        file_key=file_key,
        component_name=component_name,
        node_id=node_id,
        new_shared_elements=result.get('shared_elements', []),
        new_patterns=result.get('patterns_detected', {})
    )
    print("   ✅ Oracle updated with new patterns")
    print()

    # Summary
    print("=" * 80)
    print("✅ MISSION COMPLETE - JUSTICE LEAGUE COORDINATION PROTOCOL v2.0")
    print("=" * 80)
    print(f"📊 Final Results:")
    print(f"   Accuracy: {result.get('accuracy', 0)}%")
    print(f"   Grade: {result.get('grade', 'N/A')}")
    print(f"   Component: {component_file}")
    print(f"   Shared Elements: {len(result.get('shared_elements', []))}")
    print(f"   Patterns Learned: {len(result.get('patterns_detected', {}))}")
    print()
    print("🎯 Next Steps:")
    print("   1. Review generated component")
    print("   2. Render component in preview app")
    print("   3. Run Green Arrow validation for 100% accuracy check")
    print("=" * 80)

    # Save full result
    result_file = output_dir / f"{component_name}_result.json"
    with open(result_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\n📄 Full result saved: {result_file}")

    return result

if __name__ == "__main__":
    try:
        result = main()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
