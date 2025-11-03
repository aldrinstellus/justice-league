#!/usr/bin/env python3
"""
🦅 HAWKMAN EXAMPLE - Layer-by-Layer Figma Parsing
==================================================

This example demonstrates Hawkman's structural parsing capabilities:
1. Parse Figma file layer by layer
2. Adaptive output format selection (HTML/CSS or React)
3. Visual verification with Green Arrow
4. Iterative refinement for 95%+ accuracy

Author: Hawkman + Claude Code
Created: October 24, 2025
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.justice_league.hawkman_structural_parser import (
    HawkmanStructuralParser,
    OutputFormat,
    ParsingDepth,
    parse_figma_to_code
)


def example_basic_parsing():
    """Example 1: Basic Figma parsing with auto-detection"""
    print("=" * 80)
    print("🦅 EXAMPLE 1: Basic Parsing with Auto-Detection")
    print("=" * 80)

    figma_url = "https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=2-948"

    # Simple usage with convenience function
    result = parse_figma_to_code(
        figma_url=figma_url,
        output_format="auto",  # Let Hawkman decide
        verify=True            # Enable visual verification
    )

    print(f"\n✅ Parsing Complete!")
    print(f"📊 Output Format: {result['output_format']}")
    print(f"🎯 Accuracy Score: {result['accuracy_score']}%")
    print(f"\n📝 Generated Code Preview:")
    print("-" * 80)
    print(result['generated_code'][:500])  # First 500 characters
    print("-" * 80)

    return result


def example_html_css_output():
    """Example 2: Force HTML/CSS output"""
    print("\n" + "=" * 80)
    print("🦅 EXAMPLE 2: HTML/CSS Output (Simple Layouts)")
    print("=" * 80)

    hawkman = HawkmanStructuralParser()

    result = hawkman.parse_figma(
        figma_url="https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=2-948",
        output_format=OutputFormat.HTML_CSS,
        parsing_depth=ParsingDepth.FRAME,  # Top-level frames only
        verify=False  # Skip verification for speed
    )

    print(f"\n✅ HTML/CSS Generation Complete!")
    print(f"📁 Layer Count: {result['parsing_record']['layer_count']}")
    print(f"\n📝 Generated HTML:")
    print("-" * 80)
    print(result['generated_code'])
    print("-" * 80)

    return result


def example_react_tailwind_output():
    """Example 3: React + Tailwind output with verification"""
    print("\n" + "=" * 80)
    print("🦅 EXAMPLE 3: React + Tailwind with Verification")
    print("=" * 80)

    hawkman = HawkmanStructuralParser()

    result = hawkman.parse_figma(
        figma_url="https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=2-948",
        output_format=OutputFormat.REACT_TAILWIND,
        parsing_depth=ParsingDepth.ADAPTIVE,  # Let Hawkman decide depth
        verify=True,                           # Enable verification
        max_iterations=3                       # Refine up to 3 times
    )

    print(f"\n✅ React Component Generated!")
    print(f"📊 Format: {result['output_format']}")
    print(f"🎯 Final Accuracy: {result['accuracy_score']}%")
    print(f"🔄 Iterations Used: {result['parsing_record']['iterations_used']}")

    if result['accuracy_score'] >= 95:
        print(f"🏆 EXCELLENT - Target accuracy achieved!")
    elif result['accuracy_score'] >= 90:
        print(f"✅ GOOD - Acceptable accuracy")
    else:
        print(f"⚠️  NEEDS WORK - Accuracy below target")

    print(f"\n📝 Generated React Component:")
    print("-" * 80)
    print(result['generated_code'])
    print("-" * 80)

    if result['verification_results']:
        discrepancies = result['verification_results'].get('discrepancies', [])
        print(f"\n🔍 Identified {len(discrepancies)} discrepancies")
        for i, disc in enumerate(discrepancies[:5], 1):  # Show first 5
            print(f"  {i}. {disc}")

    return result


def example_adaptive_depth():
    """Example 4: Adaptive depth parsing"""
    print("\n" + "=" * 80)
    print("🦅 EXAMPLE 4: Adaptive Depth Parsing")
    print("=" * 80)

    hawkman = HawkmanStructuralParser()

    result = hawkman.parse_figma(
        figma_url="https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=2-948",
        output_format=OutputFormat.AUTO,
        parsing_depth=ParsingDepth.ADAPTIVE,
        verify=True
    )

    print(f"\n✅ Adaptive Parsing Complete!")
    print(f"📊 Auto-Selected Format: {result['output_format']}")
    print(f"🎯 Accuracy: {result['accuracy_score']}%")
    print(f"🌳 Layer Hierarchy:")
    print_layer_hierarchy(result['layer_hierarchy'], indent=2)

    return result


def print_layer_hierarchy(layer: dict, indent: int = 0):
    """Helper function to print layer hierarchy"""
    indent_str = "  " * indent
    layer_type = layer.get('type', 'UNKNOWN')
    layer_name = layer.get('name', 'Unnamed')
    children_count = len(layer.get('children', []))

    print(f"{indent_str}└─ {layer_type}: {layer_name} ({children_count} children)")

    for child in layer.get('children', []):
        print_layer_hierarchy(child, indent + 1)


def example_layer_analysis():
    """Example 5: Just analyze layers without code generation"""
    print("\n" + "=" * 80)
    print("🦅 EXAMPLE 5: Layer Analysis (No Code Generation)")
    print("=" * 80)

    hawkman = HawkmanStructuralParser()

    # Extract identifiers
    figma_url = "https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=2-948"
    file_key, node_id = hawkman._extract_figma_identifiers(figma_url)

    # Fetch structure
    figma_structure = hawkman._fetch_figma_structure(file_key, node_id)

    # Analyze complexity
    layer_count = hawkman._count_layers(figma_structure)
    max_depth = hawkman._calculate_max_depth(figma_structure)
    avg_children = hawkman._calculate_avg_children(figma_structure)
    has_components = hawkman._detect_components(figma_structure)

    print(f"\n📊 Layer Analysis Results:")
    print(f"  Total Layers: {layer_count}")
    print(f"  Maximum Depth: {max_depth}")
    print(f"  Avg Children/Layer: {avg_children:.1f}")
    print(f"  Has Components: {has_components}")

    # Recommend format and depth
    recommended_format = hawkman._determine_output_format(figma_structure)
    recommended_depth = hawkman._determine_parsing_depth(figma_structure)

    print(f"\n💡 Recommendations:")
    print(f"  Recommended Format: {recommended_format.value}")
    print(f"  Recommended Depth: {recommended_depth.value}")

    return {
        'layer_count': layer_count,
        'max_depth': max_depth,
        'avg_children': avg_children,
        'has_components': has_components,
        'recommended_format': recommended_format,
        'recommended_depth': recommended_depth
    }


def main():
    """Run all examples"""
    print("\n🦅 HAWKMAN STRUCTURAL PARSER - EXAMPLES")
    print("=" * 80)
    print("Archaeological Precision for Figma-to-Code Conversion")
    print("=" * 80)

    try:
        # Example 1: Basic parsing
        example_basic_parsing()

        # Example 2: HTML/CSS output
        example_html_css_output()

        # Example 3: React + Tailwind with verification
        example_react_tailwind_output()

        # Example 4: Adaptive depth
        example_adaptive_depth()

        # Example 5: Just layer analysis
        example_layer_analysis()

        print("\n" + "=" * 80)
        print("✅ ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 80)

        print("\n📚 Next Steps:")
        print("  1. Review generated code in the examples above")
        print("  2. Check parsing history: data/hawkman/parsing_history.json")
        print("  3. Integrate Hawkman with your Figma workflow")
        print("  4. Use verify=True for production accuracy")

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
