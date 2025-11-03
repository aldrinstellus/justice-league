#!/usr/bin/env python3
"""
🎨 Artemis CLI - Expert Figma-to-Code Converter
================================================

Command-line interface for Artemis, the expert Figma-to-code conversion hero.

Usage:
    python artemis_cli.py <figma_url> <component_name> [options]

Examples:
    # Basic conversion
    python artemis_cli.py "https://figma.com/file/abc/design?node-id=1-2" Settings

    # With options
    python artemis_cli.py "https://figma.com/file/abc/design?node-id=1-2" LoginForm \
        --framework next \
        --language typescript \
        --expert-mode \
        --target-accuracy 98

    # View knowledge base stats
    python artemis_cli.py --stats

Author: Artemis (Expert Edition)
Created: October 23, 2025
Status: Production Ready
"""

import sys
import argparse
import json
from pathlib import Path

# Add core directory to path
sys.path.insert(0, str(Path(__file__).parent / 'core' / 'justice_league'))

from artemis_codesmith import ArtemisCodeSmith
from artemis_knowledge import ArtemisKnowledge


def main():
    parser = argparse.ArgumentParser(
        description='🎨 Artemis - Expert Figma-to-Code Converter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert a Figma design to code
  %(prog)s "https://figma.com/file/abc/design?node-id=1-2" Settings

  # With expert mode (default)
  %(prog)s "https://figma.com/file/abc/design?node-id=1-2" LoginForm --expert-mode

  # Target 100%% accuracy with up to 5 iterations
  %(prog)s "https://figma.com/file/abc/design?node-id=1-2" Dashboard --target-accuracy 100 --max-iterations 5

  # View knowledge base statistics
  %(prog)s --stats

  # View similar conversions
  %(prog)s --similar "https://figma.com/file/abc/design"
        """
    )

    # Positional arguments
    parser.add_argument('figma_url', nargs='?', help='Figma design URL')
    parser.add_argument('component_name', nargs='?', help='Component name')

    # Framework and language options
    parser.add_argument('--framework', choices=['next', 'react'], default='next',
                        help='Framework (default: next)')
    parser.add_argument('--language', choices=['typescript', 'javascript'], default='typescript',
                        help='Language (default: typescript)')

    # Expert mode options
    parser.add_argument('--expert-mode', action='store_true', default=True,
                        help='Enable expert mode with learning (default: True)')
    parser.add_argument('--no-expert-mode', dest='expert_mode', action='store_false',
                        help='Disable expert mode')
    parser.add_argument('--max-iterations', type=int, default=3,
                        help='Maximum refinement iterations (default: 3)')
    parser.add_argument('--target-accuracy', type=float, default=98.0,
                        help='Target accuracy percentage (default: 98.0)')

    # Code generation options
    parser.add_argument('--include-tests', action='store_true', default=True,
                        help='Generate test files (default: True)')
    parser.add_argument('--include-stories', action='store_true', default=True,
                        help='Generate Storybook stories (default: True)')
    parser.add_argument('--accessibility', action='store_true', default=True,
                        help='Include accessibility features (default: True)')
    parser.add_argument('--responsive', action='store_true', default=True,
                        help='Include responsive design (default: True)')

    # Output options
    parser.add_argument('--output-dir', type=str, default='./generated',
                        help='Output directory for generated files (default: ./generated)')
    parser.add_argument('--format', choices=['files', 'json'], default='files',
                        help='Output format (default: files)')

    # Knowledge base options
    parser.add_argument('--stats', action='store_true',
                        help='Show knowledge base statistics')
    parser.add_argument('--similar', type=str, metavar='URL',
                        help='Find similar conversions for a Figma URL')

    args = parser.parse_args()

    # Handle knowledge base queries
    if args.stats:
        show_stats()
        return

    if args.similar:
        show_similar_conversions(args.similar)
        return

    # Validate required arguments
    if not args.figma_url or not args.component_name:
        parser.error('figma_url and component_name are required unless using --stats or --similar')

    # Initialize Artemis
    print("\n" + "=" * 70)
    print("🎨 ARTEMIS CLI - Expert Figma-to-Code Converter")
    print("=" * 70)

    artemis = ArtemisCodeSmith(expert_mode=args.expert_mode)

    # Prepare options
    options = {
        'include_tests': args.include_tests,
        'include_stories': args.include_stories,
        'accessibility': args.accessibility,
        'responsive': args.responsive,
    }

    # Generate code
    if args.expert_mode:
        result = artemis.generate_component_code_expert(
            figma_url=args.figma_url,
            component_name=args.component_name,
            framework=args.framework,
            language=args.language,
            options=options,
            max_iterations=args.max_iterations,
            target_accuracy=args.target_accuracy
        )
    else:
        result = artemis.generate_component_code(
            figma_url=args.figma_url,
            component_name=args.component_name,
            framework=args.framework,
            language=args.language,
            options=options
        )

    # Handle results
    if not result['success']:
        print("\n" + "=" * 70)
        print("❌ CONVERSION FAILED")
        print("=" * 70)
        for error in result.get('errors', []):
            print(f"  • {error}")
        sys.exit(1)

    # Output results
    if args.format == 'json':
        output_json(result)
    else:
        output_files(result, args.output_dir, args.component_name)

    print("\n" + "=" * 70)
    print("✅ CONVERSION COMPLETE")
    print("=" * 70)
    print_summary(result)


def show_stats():
    """Show knowledge base statistics."""
    print("\n" + "=" * 70)
    print("📚 ARTEMIS KNOWLEDGE BASE STATISTICS")
    print("=" * 70)

    knowledge = ArtemisKnowledge()
    stats = knowledge.get_statistics()

    print(f"\n📊 Overview:")
    print(f"  • Total Conversions: {stats.get('total_conversions', 0)}")
    print(f"  • Average Accuracy: {stats.get('average_accuracy', 0):.1f}%")
    print(f"  • Average Iterations: {stats.get('average_iterations', 0):.1f}")
    print(f"  • Patterns Identified: {stats.get('total_patterns_identified', 0)}")

    insights = knowledge.get_expert_insights()
    if insights:
        print(f"\n🎯 Expert Insights:")
        for name, insight in insights.items():
            print(f"\n  {name}:")
            print(f"    Description: {insight.get('description', 'N/A')}")
            print(f"    Frequency: {insight.get('frequency', 'N/A')}")
            print(f"    Confidence: {insight.get('confidence', 0)}%")

    print()


def show_similar_conversions(figma_url: str):
    """Show similar conversions for a Figma URL."""
    print("\n" + "=" * 70)
    print("🔍 SIMILAR CONVERSIONS")
    print("=" * 70)
    print(f"Query: {figma_url}\n")

    knowledge = ArtemisKnowledge()
    similar = knowledge.query_similar_conversions(figma_url=figma_url, limit=5)

    if not similar:
        print("No similar conversions found.\n")
        return

    print(f"Found {len(similar)} similar conversion(s):\n")

    for i, item in enumerate(similar, 1):
        conv = item['conversion']
        score = item['relevance_score']

        print(f"{i}. {conv['component_name']}")
        print(f"   Relevance: {score:.1f}")
        print(f"   Accuracy: {conv['accuracy_final']}%")
        print(f"   Iterations: {conv['iterations']}")
        print(f"   Rating: {conv['expert_rating']}")
        print(f"   Date: {conv['timestamp'][:10]}")
        print()


def output_json(result):
    """Output results as JSON."""
    print("\n" + json.dumps(result, indent=2))


def output_files(result, output_dir: str, component_name: str):
    """Write generated files to disk."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"\n📁 Writing files to: {output_path.absolute()}")

    files = result.get('files', {})
    for file_path, content in files.items():
        full_path = output_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, 'w') as f:
            f.write(content)

        print(f"  ✓ {file_path}")

    # Write install commands
    if result.get('install_commands'):
        install_file = output_path / 'install.sh'
        with open(install_file, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Artemis Generated Install Commands\n\n")
            for cmd in result['install_commands']:
                f.write(f"{cmd}\n")
        install_file.chmod(0o755)
        print(f"  ✓ install.sh (executable)")


def print_summary(result):
    """Print conversion summary."""
    print(f"\n📊 Summary:")
    print(f"  • Files Generated: {len(result.get('files', {}))}")

    if 'expert_rating' in result:
        print(f"  • Expert Rating: {result['expert_rating']}")
        print(f"  • Accuracy: {result.get('accuracy_score', 0)}%")
        print(f"  • Iterations: {result.get('iterations', 1)}")

    if 'issues_solved' in result:
        auto_fixes = len([f for f in result['issues_solved'] if f.get('automatic')])
        total_issues = len(result['issues_solved'])
        print(f"  • Issues Fixed: {auto_fixes}/{total_issues}")

    if 'conversion_id' in result:
        print(f"  • Conversion ID: {result['conversion_id']}")

    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
