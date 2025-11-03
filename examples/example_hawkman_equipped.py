#!/usr/bin/env python3
"""
🦅 HAWKMAN EQUIPPED - Production Example
=========================================

This example demonstrates the fully equipped Hawkman with all MCP integrations:
- Real Figma API for data fetching
- Chrome DevTools MCP for rendering
- Green Arrow for visual validation
- shadcn/ui component support
- Automatic refinement for pixel-perfect accuracy

Prerequisites:
1. Figma access token in FIGMA_ACCESS_TOKEN env var
2. preview-app dev server running on port 3005
3. Chrome DevTools MCP client available

Usage:
    # Set environment variable
    export FIGMA_ACCESS_TOKEN="your_token_here"

    # Ensure preview-app is running
    cd preview-app && npm run dev

    # Run example
    python examples/example_hawkman_equipped.py
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.justice_league.hawkman_equipped import (
    HawkmanEquipped,
    OutputFormat,
    parse_figma_equipped
)


def example_with_mcp_client():
    """
    Example 1: Full integration with Chrome DevTools MCP

    This shows how to use Hawkman with all MCP tools for pixel-perfect conversion.
    """
    print("=" * 80)
    print("🦅 EXAMPLE 1: Full MCP Integration")
    print("=" * 80)

    # Get Figma token from environment
    figma_token = os.getenv('FIGMA_ACCESS_TOKEN')
    if not figma_token:
        print("❌ FIGMA_ACCESS_TOKEN not set. Please set environment variable:")
        print("   export FIGMA_ACCESS_TOKEN='your_token_here'")
        return

    # Initialize Chrome DevTools MCP client (you would get this from Claude Code's MCP tools)
    # For this example, we'll show the structure
    try:
        # In actual usage, you'd get this from Claude Code's environment
        # chrome_mcp = mcp_tools['chrome-devtools']

        print("\n⚠️ This example requires Chrome DevTools MCP client")
        print("In production, you would:")
        print("1. Get chrome_mcp from Claude Code's MCP tools")
        print("2. Pass it to HawkmanEquipped")
        print("\nExample code:")
        print("""
from core.justice_league.hawkman_equipped import HawkmanEquipped

# Initialize with MCP client
hawkman = HawkmanEquipped(
    figma_token=figma_token,
    chrome_mcp_client=chrome_mcp  # From Claude Code MCP tools
)

# Parse with full verification
result = hawkman.parse_figma_equipped(
    figma_url="https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=2-948",
    output_format=OutputFormat.AUTO,
    verify=True,
    max_iterations=3
)

print(f"Generated Format: {result['output_format']}")
print(f"Final Accuracy: {result['accuracy_score']}%")
print(f"Iterations Used: {result['iterations_used']}")
print(f"\\nGenerated Code:\\n{result['generated_code']}")
""")

    except Exception as e:
        print(f"❌ Error: {e}")


def example_without_verification():
    """
    Example 2: Quick conversion without visual verification

    Useful for rapid prototyping when you don't need pixel-perfect accuracy.
    """
    print("\n" + "=" * 80)
    print("🦅 EXAMPLE 2: Quick Conversion (No Verification)")
    print("=" * 80)

    figma_token = os.getenv('FIGMA_ACCESS_TOKEN')
    if not figma_token:
        print("❌ FIGMA_ACCESS_TOKEN not set")
        return

    print("\nThis would fetch from Figma API and generate code without rendering:")
    print("""
hawkman = HawkmanEquipped(figma_token=figma_token)

# Quick generation without verification
result = hawkman.parse_figma_equipped(
    figma_url="https://www.figma.com/design/YOUR_FILE/name?node-id=X-Y",
    output_format=OutputFormat.REACT_SHADCN,  # Force shadcn/ui
    verify=False  # Skip visual verification
)

# Code is generated immediately without refinement loop
print(result['generated_code'])
""")


def example_convenience_function():
    """
    Example 3: Using convenience function

    Simplest way to use Hawkman Equipped.
    """
    print("\n" + "=" * 80)
    print("🦅 EXAMPLE 3: Convenience Function")
    print("=" * 80)

    print("\nSimplest usage with convenience function:")
    print("""
from core.justice_league.hawkman_equipped import parse_figma_equipped

# One-line usage
result = parse_figma_equipped(
    figma_url="https://www.figma.com/design/YOUR_FILE/name?node-id=X-Y",
    figma_token="your_token",  # Or use FIGMA_ACCESS_TOKEN env var
    chrome_mcp_client=chrome_mcp,
    output_format="auto",  # or "react_shadcn", "react_tailwind", "html_tailwind"
    verify=True
)

# Save to file
with open('generated_component.tsx', 'w') as f:
    f.write(result['generated_code'])

print(f"✅ Component saved with {result['accuracy_score']}% accuracy")
""")


def example_format_comparison():
    """
    Example 4: Compare different output formats

    See how the same Figma design converts to different formats.
    """
    print("\n" + "=" * 80)
    print("🦅 EXAMPLE 4: Format Comparison")
    print("=" * 80)

    print("\nGenerate the same design in multiple formats:")
    print("""
figma_url = "https://www.figma.com/design/YOUR_FILE/name?node-id=X-Y"

formats_to_try = [
    OutputFormat.HTML_CSS,
    OutputFormat.HTML_TAILWIND,
    OutputFormat.REACT_TAILWIND,
    OutputFormat.REACT_SHADCN
]

for fmt in formats_to_try:
    result = hawkman.parse_figma_equipped(
        figma_url=figma_url,
        output_format=fmt,
        verify=False
    )

    # Save each format
    filename = f"output_{fmt.value}.{'tsx' if 'react' in fmt.value else 'html'}"
    with open(filename, 'w') as f:
        f.write(result['generated_code'])

    print(f"✅ {fmt.value}: {filename}")
""")


def example_production_workflow():
    """
    Example 5: Complete production workflow

    Full workflow with verification, refinement, and quality checks.
    """
    print("\n" + "=" * 80)
    print("🦅 EXAMPLE 5: Production Workflow")
    print("=" * 80)

    print("\nComplete production-ready workflow:")
    print("""
# 1. Initialize Hawkman
hawkman = HawkmanEquipped(
    figma_token=os.getenv('FIGMA_ACCESS_TOKEN'),
    chrome_mcp_client=chrome_mcp,
    preview_app_port=3005
)

# 2. Parse with verification
result = hawkman.parse_figma_equipped(
    figma_url="https://www.figma.com/design/YOUR_FILE/name?node-id=X-Y",
    output_format=OutputFormat.AUTO,  # Let Hawkman decide
    verify=True,
    max_iterations=3  # Allow up to 3 refinement iterations
)

# 3. Quality checks
if result['accuracy_score'] >= 95:
    print("✅ EXCELLENT - Target accuracy achieved!")

    # Save production component
    output_file = f"src/components/{result['component_name']}.tsx"
    with open(output_file, 'w') as f:
        f.write(result['generated_code'])

    print(f"✅ Saved to: {output_file}")
    print(f"📊 Format: {result['output_format']}")
    print(f"🎯 Accuracy: {result['accuracy_score']}%")
    print(f"🔄 Iterations: {result['iterations_used']}")

elif result['accuracy_score'] >= 90:
    print("⚠️ GOOD - Acceptable accuracy, manual review recommended")
    print("Discrepancies found:")
    for disc in result['verification_results']['discrepancies'][:5]:
        print(f"  - {disc}")
else:
    print("❌ NEEDS WORK - Accuracy below 90%")
    print("Consider:")
    print("  1. Simplifying the Figma design")
    print("  2. Trying a different output format")
    print("  3. Manual refinement needed")
""")


def example_shadcn_components():
    """
    Example 6: shadcn/ui component detection

    Hawkman automatically detects and uses shadcn/ui components.
    """
    print("\n" + "=" * 80)
    print("🦅 EXAMPLE 6: shadcn/ui Component Detection")
    print("=" * 80)

    print("\nHawkman automatically detects shadcn/ui components:")
    print("""
# When your Figma has layers named:
# - "Primary Button"
# - "User Card"
# - "Email Input"
# - "Dropdown Menu"

result = hawkman.parse_figma_equipped(
    figma_url="https://www.figma.com/design/YOUR_FILE/name?node-id=X-Y",
    output_format=OutputFormat.REACT_SHADCN
)

# Generated code will use shadcn/ui components:
# import { Button, Card, Input, DropdownMenu } from '@/components/ui'
#
# <Card>
#   <Input type="email" />
#   <Button>Submit</Button>
#   <DropdownMenu>...</DropdownMenu>
# </Card>

print("🎨 shadcn/ui components detected and used!")
""")


def show_setup_instructions():
    """Show setup instructions for first-time users"""
    print("\n" + "=" * 80)
    print("📋 SETUP INSTRUCTIONS")
    print("=" * 80)

    print("""
To use Hawkman Equipped in production:

1. Get Figma Access Token:
   - Go to https://www.figma.com/settings
   - Scroll to "Personal access tokens"
   - Generate new token
   - Set environment variable:
     export FIGMA_ACCESS_TOKEN="figd_YOUR_TOKEN_HERE"

2. Start preview-app dev server:
   cd preview-app
   npm run dev
   # Should run on http://localhost:3005

3. Ensure Chrome DevTools MCP is available:
   # In Claude Code, MCP tools are automatically available
   # You can access chrome_mcp from the MCP tools

4. Run Hawkman:
   from core.justice_league.hawkman_equipped import HawkmanEquipped

   hawkman = HawkmanEquipped(
       figma_token=os.getenv('FIGMA_ACCESS_TOKEN'),
       chrome_mcp_client=chrome_mcp
   )

   result = hawkman.parse_figma_equipped(
       figma_url="YOUR_FIGMA_URL",
       verify=True
   )

5. Output Formats Available:
   - HTML_CSS: Pure HTML with CSS classes
   - HTML_TAILWIND: HTML with Tailwind utility classes
   - REACT_TAILWIND: React components with Tailwind
   - REACT_SHADCN: React with shadcn/ui components (NEW!)
   - AUTO: Let Hawkman choose based on complexity

6. Complexity Thresholds:
   - ≤10 layers → HTML/CSS
   - 10-30 layers → HTML + Tailwind
   - 30-50 layers → React + Tailwind
   - >50 layers or has components → React + shadcn/ui
""")


def main():
    """Run all examples"""
    print("\n🦅 HAWKMAN EQUIPPED - PRODUCTION EXAMPLES")
    print("=" * 80)
    print("Fully Integrated Layer-by-Layer Figma Parser")
    print("=" * 80)

    try:
        # Show setup first
        show_setup_instructions()

        # Run examples
        example_with_mcp_client()
        example_without_verification()
        example_convenience_function()
        example_format_comparison()
        example_production_workflow()
        example_shadcn_components()

        print("\n" + "=" * 80)
        print("✅ ALL EXAMPLES SHOWN")
        print("=" * 80)

        print("\n📚 Next Steps:")
        print("  1. Set FIGMA_ACCESS_TOKEN environment variable")
        print("  2. Start preview-app dev server (npm run dev)")
        print("  3. Get Chrome DevTools MCP client from Claude Code")
        print("  4. Run your first equipped parsing!")
        print("\n🦅 Hawkman is ready for pixel-perfect Figma-to-Code conversion!")

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
