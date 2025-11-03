#!/usr/bin/env python3
"""
Example: Running Aldo Vision Analysis
Demonstrates how to use the Aldo Vision agent for comprehensive design analysis
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add the parent directory to the path so we can import the main module
sys.path.append(str(Path(__file__).parent.parent))

from main import AldoVisionAgent, AnalysisConfig


def example_basic_analysis():
    """
    Example 1: Basic analysis with default settings
    """
    print("🎯 Example 1: Basic Analysis")
    print("=" * 50)

    # Initialize the agent
    agent = AldoVisionAgent()

    # Path to your Penpot file (update this path)
    penpot_file = "path/to/your/design.penpot"

    # Check if file exists (for demo purposes, we'll use a placeholder)
    if not os.path.exists(penpot_file):
        print(f"⚠️  Demo file not found: {penpot_file}")
        print("💡 This example shows how the analysis would work with a real file")
        return

    try:
        # Run the analysis
        print(f"🔍 Analyzing file: {penpot_file}")
        results = agent.analyze_penpot_file(penpot_file)

        # Generate reports
        print("📊 Generating comprehensive reports...")
        report_paths = agent.generate_comprehensive_reports(results, "output/basic_analysis")

        # Display results
        print("\n✅ Analysis Complete!")
        print("\n📄 Generated Reports:")
        for format_name, path in report_paths.items():
            print(f"  • {format_name}: {path}")

        # Show key insights
        print(f"\n🎯 Key Insights:")
        print(f"  • Total components: {len(results.get('components', {}).get('component_inventory', {}).get('components', {}))}")
        print(f"  • Personas analyzed: {len(results.get('persona_analyses', {}))}")
        print(f"  • Recommendations: {len(results.get('recommendations', []))}")

    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")


def example_custom_configuration():
    """
    Example 2: Analysis with custom configuration
    """
    print("\n🎯 Example 2: Custom Configuration Analysis")
    print("=" * 50)

    # Create custom configuration
    custom_config = {
        "personas": {
            "enabled": [
                "product_manager",
                "design_systems_designer",
                "accessibility_specialist"
            ],
            "weights": {
                "product_manager": 1.0,
                "design_systems_designer": 0.9,
                "accessibility_specialist": 0.8
            }
        },
        "output_formats": ["html", "json"],
        "visual": {
            "screenshot_quality": "high",
            "annotation_style": "professional",
            "theme": "government"
        }
    }

    # Save configuration to file
    config_path = "examples/custom_config.json"
    with open(config_path, 'w') as f:
        json.dump(custom_config, f, indent=2)

    # Initialize agent with custom config
    agent = AldoVisionAgent(config_path=config_path)

    # Create analysis configuration
    analysis_config = AnalysisConfig(
        input_file="path/to/design.penpot",
        output_dir="output/custom_analysis",
        personas=["product_manager", "design_systems_designer", "accessibility_specialist"],
        output_formats=["html", "json"],
        visual_quality="high"
    )

    print("🔍 Configuration created:")
    print(f"  • Personas: {', '.join(analysis_config.personas)}")
    print(f"  • Output formats: {', '.join(analysis_config.output_formats)}")
    print(f"  • Visual quality: {analysis_config.visual_quality}")

    # Note: We won't run the actual analysis in this example since we don't have a real file
    print("💡 Use this configuration with: python main.py design.penpot -c examples/custom_config.json")


def example_programmatic_usage():
    """
    Example 3: Programmatic usage with custom analysis
    """
    print("\n🎯 Example 3: Programmatic Usage")
    print("=" * 50)

    # Initialize agent
    agent = AldoVisionAgent()

    # Simulate analysis results (in real usage, you'd get these from analyze_penpot_file)
    mock_results = create_mock_analysis_results()

    # Work with specific persona results
    print("🔍 Extracting persona insights:")

    # Product Manager insights
    if 'product_manager' in mock_results.get('persona_analyses', {}):
        pm_analysis = mock_results['persona_analyses']['product_manager']
        user_stories = pm_analysis.get('user_stories', [])
        print(f"\n📋 Product Manager Analysis:")
        print(f"  • User stories identified: {len(user_stories)}")
        if user_stories:
            print(f"  • Example story: {user_stories[0].get('title', 'N/A')}")

    # Design Systems analysis
    if 'design_systems_designer' in mock_results.get('persona_analyses', {}):
        ds_analysis = mock_results['persona_analyses']['design_systems_designer']
        component_audit = ds_analysis.get('component_library_audit', {})
        print(f"\n🧩 Design Systems Analysis:")
        print(f"  • Total components: {component_audit.get('total_components', 0)}")
        print(f"  • Reusable components: {len(component_audit.get('reusable_components', []))}")

    # Generate specific output formats
    print(f"\n📊 Generating output formats:")

    # Product acceptance criteria
    pac_generator = agent.output_generators['product_acceptance']
    acceptance_criteria = pac_generator.generate(mock_results)
    print(f"  • User stories generated: {len(acceptance_criteria.get('user_stories', []))}")

    # Design acceptance criteria
    dac_generator = agent.output_generators['design_acceptance']
    design_criteria = dac_generator.generate(mock_results)
    print(f"  • Design specifications generated: ✓")

    # Claude Code ready format
    claude_generator = agent.output_generators['claude_code_format']
    claude_format = claude_generator.generate(mock_results)
    print(f"  • Claude Code format generated: ✓")

    # Save results
    output_dir = Path("output/programmatic_example")
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "acceptance_criteria.json", 'w') as f:
        json.dump(acceptance_criteria, f, indent=2)

    with open(output_dir / "claude_code_format.json", 'w') as f:
        json.dump(claude_format, f, indent=2)

    print(f"\n✅ Results saved to {output_dir}")


def example_batch_processing():
    """
    Example 4: Batch processing multiple files
    """
    print("\n🎯 Example 4: Batch Processing")
    print("=" * 50)

    # Simulate multiple Penpot files
    design_files = [
        "designs/main_app.penpot",
        "designs/admin_panel.penpot",
        "designs/mobile_app.penpot"
    ]

    # Initialize agent
    agent = AldoVisionAgent()

    print(f"📁 Processing {len(design_files)} design files:")

    for i, file_path in enumerate(design_files, 1):
        print(f"\n🔍 [{i}/{len(design_files)}] Processing: {Path(file_path).name}")

        # Create output directory for this file
        file_name = Path(file_path).stem
        output_dir = f"output/batch_processing/{file_name}"

        # In a real scenario, you would run:
        # results = agent.analyze_penpot_file(file_path)
        # reports = agent.generate_comprehensive_reports(results, output_dir)

        print(f"  • Analysis: ✓ (simulated)")
        print(f"  • Reports: ✓ (would be saved to {output_dir})")

        # Simulate processing metrics
        print(f"  • Components found: {15 + i * 5}")
        print(f"  • Recommendations: {8 + i * 2}")

    print(f"\n✅ Batch processing complete!")
    print(f"📊 All reports saved to output/batch_processing/")


def create_mock_analysis_results():
    """Create mock analysis results for demonstration"""
    return {
        'metadata': {
            'input_file': 'example_design.penpot',
            'analysis_timestamp': datetime.now().isoformat(),
            'agent_version': '1.0.0',
            'personas_analyzed': ['product_manager', 'design_systems_designer', 'accessibility_specialist']
        },
        'components': {
            'component_inventory': {
                'components': {
                    'V1-Button': 15,
                    'Input-Field': 8,
                    'V1-Tables/cell': 25,
                    'Text': 45
                },
                'reusable_components': ['V1-Button', 'Input-Field', 'V1-Tables/cell'],
                'one_off_elements': ['Custom-Header', 'Footer-Logo']
            }
        },
        'persona_analyses': {
            'product_manager': {
                'user_stories': [
                    {
                        'id': 'US-001',
                        'title': 'Grant Application Submission',
                        'user_story': 'As a grant applicant, I want to submit my application online...',
                        'priority': 'High',
                        'effort_estimate': '8 story points'
                    }
                ],
                'business_requirements': [
                    {
                        'id': 'BR-001',
                        'title': 'Accessibility Compliance',
                        'priority': 'High'
                    }
                ],
                'roi_analysis': {
                    'efficiency_gains': {
                        'time_savings': '40% reduction in processing time'
                    }
                }
            },
            'design_systems_designer': {
                'component_library_audit': {
                    'total_components': 4,
                    'reusable_components': [
                        {'name': 'V1-Button', 'usage_count': 15, 'consistency_score': 0.9},
                        {'name': 'Input-Field', 'usage_count': 8, 'consistency_score': 0.85}
                    ]
                },
                'design_system_maturity': {
                    'current_level': 'Level 2',
                    'current_level_description': 'Component library'
                }
            },
            'accessibility_specialist': {
                'wcag_compliance_audit': {
                    'level_aa_violations': ['Color contrast issues', 'Missing alt text'],
                    'compliance_score': 0.75
                }
            }
        },
        'recommendations': [
            {
                'category': 'Accessibility',
                'priority': 'High',
                'title': 'Improve Color Contrast',
                'description': 'Update color combinations to meet WCAG AA standards',
                'implementation_effort': 'Medium',
                'expected_impact': 'High - Ensures legal compliance'
            },
            {
                'category': 'Design System',
                'priority': 'Medium',
                'title': 'Implement Design Tokens',
                'description': 'Create systematic design tokens for colors, spacing, and typography',
                'implementation_effort': 'High',
                'expected_impact': 'Medium - Improves consistency and scalability'
            }
        ]
    }


def main():
    """Run all examples"""
    print("🚀 Aldo Vision Agent - Usage Examples")
    print("=" * 60)
    print("This script demonstrates various ways to use the Aldo Vision agent")
    print("for comprehensive Penpot design file analysis.\n")

    # Run examples
    example_basic_analysis()
    example_custom_configuration()
    example_programmatic_usage()
    example_batch_processing()

    print("\n" + "=" * 60)
    print("🎉 Examples Complete!")
    print("\nNext Steps:")
    print("1. Update file paths to point to your actual .penpot files")
    print("2. Run: python main.py your-design.penpot")
    print("3. View the generated interactive HTML report")
    print("4. Explore the JSON outputs for integration with other tools")
    print("\nFor more information, see USAGE.md and README.md")


if __name__ == "__main__":
    main()