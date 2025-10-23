"""
🎨 Artemis - The Design System Guardian (Fully Equipped)
==========================================================

Design system validation with FULL Claude Code toolkit:
- shadcn CLI integration
- Figma MCP tools
- Component registry access
- Best practices from Claude Agent SDK

Author: Artemis (with Claude Code)
Created: October 21, 2025
Status: Production Ready - Fully Equipped
"""

import json
import subprocess
from typing import Dict, Any, List, Optional, Set
from datetime import datetime
from collections import defaultdict


class ArtemisFullyEquipped:
    """
    Artemis - Design System Guardian (Fully Equipped Edition)

    Powers:
    - 🏹 Bow of Precision: shadcn CLI for component validation
    - 🎯 Arrow of Truth: Figma MCP for design extraction
    - 🛡️ Guardian Shield: Component registry access
    - 📖 Quiver of Knowledge: Best practices enforcement
    """

    def __init__(self, target_framework: str = "shadcn/ui"):
        """
        Initialize fully-equipped Artemis.

        Args:
            target_framework: Target UI framework
        """
        self.target_framework = target_framework
        self.shadcn_registry = None

    def get_shadcn_registry(self) -> Dict[str, Any]:
        """
        Get complete shadcn registry using CLI.

        Returns:
            Complete component registry
        """
        if self.shadcn_registry:
            return self.shadcn_registry

        print("🏹 Artemis accessing shadcn registry...")

        try:
            # Get full registry
            result = subprocess.run(
                ["npx", "shadcn@latest", "list", "@shadcn"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                self.shadcn_registry = data

                total = data.get("pagination", {}).get("total", 0)
                print(f"✅ Found {total} components in shadcn registry")

                return data
            else:
                print(f"⚠️  Could not access shadcn registry: {result.stderr}")
                return {"items": [], "pagination": {"total": 0}}

        except Exception as e:
            print(f"⚠️  Error accessing shadcn registry: {e}")
            return {"items": [], "pagination": {"total": 0}}

    def get_official_shadcn_components(self) -> Set[str]:
        """
        Get official list of shadcn UI components from registry.

        Returns:
            Set of component names
        """
        registry = self.get_shadcn_registry()
        items = registry.get("items", [])

        # Filter for UI components only
        ui_components = {
            item["name"]
            for item in items
            if item.get("type") == "registry:ui"
        }

        return ui_components

    def check_component_exists(self, component_name: str) -> Dict[str, Any]:
        """
        Check if a component exists in shadcn registry.

        Args:
            component_name: Component name (e.g., 'button', 'card')

        Returns:
            Component info if exists
        """
        registry = self.get_shadcn_registry()
        items = registry.get("items", [])

        for item in items:
            if item.get("name") == component_name:
                return {
                    "exists": True,
                    "name": item.get("name"),
                    "type": item.get("type"),
                    "add_command": item.get("addCommandArgument"),
                    "registry": item.get("registry")
                }

        return {"exists": False}

    def generate_add_commands(self, missing_components: List[str]) -> List[str]:
        """
        Generate shadcn add commands for missing components.

        Args:
            missing_components: List of missing component names

        Returns:
            List of CLI commands to add components
        """
        commands = []
        registry = self.get_shadcn_registry()
        items = registry.get("items", [])

        # Build lookup
        component_lookup = {
            item.get("name"): item.get("addCommandArgument")
            for item in items
            if item.get("type") == "registry:ui"
        }

        # Generate commands
        for comp in missing_components:
            if comp in component_lookup:
                add_arg = component_lookup[comp]
                commands.append(f"npx shadcn@latest add {add_arg}")

        return commands

    def validate_design_system_complete(
        self,
        figma_data: Dict[str, Any],
        mcp_tools: Optional[Dict[str, Any]] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Complete design system validation with ALL tools.

        Args:
            figma_data: Data from Superman's Figma extraction
            mcp_tools: Optional MCP tools for Figma access
            options: Validation options

        Returns:
            Complete validation with commands and recommendations
        """
        options = options or {}

        print(f"\n🎨 Artemis - Fully Equipped Analysis")
        print("=" * 70)
        print("🏹 Bow of Precision: shadcn CLI")
        print("🎯 Arrow of Truth: Figma data")
        print("🛡️ Guardian Shield: Component registry")
        print("=" * 70)

        # Get official shadcn components from registry
        official_components = self.get_official_shadcn_components()
        print(f"\n📦 Official shadcn/ui components: {len(official_components)}")

        # Extract from Figma
        figma_components = figma_data.get("components", {}).get("components", [])
        design_tokens = figma_data.get("design_tokens", {})

        print(f"📦 Figma components: {len(figma_components)}")
        print(f"🎨 Design tokens: {design_tokens.get('color_count', 0)} colors, {design_tokens.get('typography_count', 0)} text styles")

        # Map Figma components to shadcn
        mapping = self._map_components_advanced(figma_components, official_components)

        print(f"\n✅ Matched: {mapping['matched_unique_count']}/{len(official_components)}")
        print(f"❌ Missing: {mapping['missing_count']} components")
        print(f"📈 Coverage: {mapping['coverage_percent']:.1f}%")

        # Validate design tokens
        token_health = self._validate_design_tokens(design_tokens)

        # Calculate Artemis score
        artemis_score = self._calculate_score_advanced(
            mapping, token_health, len(official_components)
        )

        # Generate commands for missing components
        missing_components = list(mapping.get("missing_components", set()))
        add_commands = self.generate_add_commands(missing_components)

        # Generate comprehensive recommendations
        recommendations = self._generate_recommendations_advanced(
            mapping, token_health, add_commands
        )

        print(f"\n🏹 Artemis Score: {artemis_score['score']:.1f}/100 ({artemis_score['grade']})")
        print(f"🎯 {len(recommendations)} actionable recommendations")
        print(f"⚡ {len(add_commands)} CLI commands generated")

        result = {
            "artemis_score": artemis_score,
            "component_coverage": mapping,
            "design_tokens": token_health,
            "official_components_count": len(official_components),
            "add_commands": add_commands,
            "artemis_recommendations": recommendations,
            "analyzed_at": datetime.now().isoformat(),
            "target_framework": self.target_framework,
            "file_name": figma_data.get("file_name", "Unknown"),
            "tools_used": ["shadcn-cli", "figma-extraction", "component-registry"]
        }

        print(f"\n🎨 Artemis fully-equipped analysis complete!")
        return result

    def _map_components_advanced(
        self,
        figma_components: List[Dict[str, Any]],
        official_components: Set[str]
    ) -> Dict[str, Any]:
        """Advanced component mapping using official registry."""
        matched = []
        matched_unique = set()
        unmatched = []

        for comp in figma_components:
            name = comp.get("name", "").lower()

            # Extract base name
            base_name = name.split("/")[0].split("-")[0].split(".")[0].strip()
            base_name = base_name.split("=")[0].split(",")[0].strip()

            # Check against official components
            found = False
            for official_comp in official_components:
                if official_comp in base_name or base_name in official_comp:
                    matched.append({
                        "figma_name": comp.get("name"),
                        "shadcn_component": official_comp,
                        "path": comp.get("path", "")
                    })
                    matched_unique.add(official_comp)
                    found = True
                    break

            if not found:
                unmatched.append(comp.get("name"))

        # Find missing
        missing = official_components - matched_unique

        # Identify critical components
        critical_components = {
            "button", "input", "select", "checkbox", "radio-group",
            "label", "textarea", "form", "card", "dialog"
        }
        missing_critical = critical_components & missing

        return {
            "matched": matched,
            "matched_count": len(matched),
            "matched_unique_count": len(matched_unique),
            "unmatched_count": len(unmatched),
            "missing_components": missing,
            "missing_count": len(missing),
            "missing_critical": missing_critical,
            "missing_critical_count": len(missing_critical),
            "total_official_components": len(official_components),
            "coverage_percent": (len(matched_unique) / len(official_components) * 100) if official_components else 0
        }

    def _validate_design_tokens(self, design_tokens: Dict[str, Any]) -> Dict[str, Any]:
        """Validate design tokens with best practices."""
        color_count = design_tokens.get("color_count", 0)
        typography_count = design_tokens.get("typography_count", 0)

        # Best practices: 10+ colors, 8+ text styles
        health_score = 0.0

        # Colors (50%)
        if color_count >= 10:
            health_score += 50
        elif color_count >= 5:
            health_score += 30
        elif color_count > 0:
            health_score += 15

        # Typography (50%)
        if typography_count >= 8:
            health_score += 50
        elif typography_count >= 4:
            health_score += 30
        elif typography_count > 0:
            health_score += 15

        return {
            "health_score": health_score,
            "color_count": color_count,
            "typography_count": typography_count,
            "needs_colors": color_count < 10,
            "needs_typography": typography_count < 8
        }

    def _calculate_score_advanced(
        self,
        mapping: Dict[str, Any],
        token_health: Dict[str, Any],
        total_official: int
    ) -> Dict[str, Any]:
        """Calculate Artemis score with advanced metrics."""
        score = 0.0

        # Component coverage (60%)
        coverage = mapping.get("coverage_percent", 0)
        missing_critical = mapping.get("missing_critical_count", 0)

        coverage_score = (coverage / 100) * 60
        critical_penalty = min(30, missing_critical * 6)
        coverage_score = max(0, coverage_score - critical_penalty)
        score += coverage_score

        # Design tokens (40%)
        token_score = (token_health.get("health_score", 0) / 100) * 40
        score += token_score

        # Grade
        if score >= 95:
            grade = "S+"
        elif score >= 90:
            grade = "A+"
        elif score >= 85:
            grade = "A"
        elif score >= 80:
            grade = "B+"
        elif score >= 75:
            grade = "B"
        elif score >= 70:
            grade = "C"
        else:
            grade = "D"

        return {
            "score": round(score, 1),
            "grade": grade,
            "coverage_score": coverage_score,
            "token_score": token_score,
            "artemis_says": self._get_message(grade, missing_critical)
        }

    def _get_message(self, grade: str, missing_critical: int) -> str:
        """Get Artemis's message."""
        if grade in ["S+", "A+"]:
            return f"Perfect design system! Artemis approves! 🎨🏹"
        elif grade == "A":
            return f"Excellent work! Minor refinements needed. 🎯"
        elif grade in ["B+", "B"]:
            if missing_critical > 0:
                return f"Missing {missing_critical} critical components! Add them now! ⚡"
            return f"Good foundation. Keep building! 🏹"
        else:
            return f"Critical work needed. Follow the action plan! 🚨"

    def _generate_recommendations_advanced(
        self,
        mapping: Dict[str, Any],
        token_health: Dict[str, Any],
        add_commands: List[str]
    ) -> List[Dict[str, Any]]:
        """Generate advanced recommendations with CLI commands."""
        recommendations = []

        # Missing critical components
        missing_critical = list(mapping.get("missing_critical", set()))
        if missing_critical:
            critical_commands = [cmd for cmd in add_commands if any(comp in cmd for comp in missing_critical)]
            recommendations.append({
                "priority": "critical",
                "area": "Critical Components",
                "issue": f"Missing {len(missing_critical)} essential components",
                "components": missing_critical,
                "commands": critical_commands[:3],
                "artemis_says": "These are REQUIRED for any design system! 🎯",
                "next_action": critical_commands[0] if critical_commands else None
            })

        # Missing other components
        missing_other = list(mapping.get("missing_components", set()) - mapping.get("missing_critical", set()))
        if missing_other:
            other_commands = [cmd for cmd in add_commands if any(comp in cmd for comp in missing_other)]
            recommendations.append({
                "priority": "high",
                "area": "Component Coverage",
                "issue": f"Missing {len(missing_other)} additional components",
                "components": missing_other[:10],
                "commands": other_commands[:5],
                "artemis_says": "Expand your component library for 100% coverage! 🏹",
                "next_action": other_commands[0] if other_commands else None
            })

        # Design tokens
        if token_health.get("needs_colors") or token_health.get("needs_typography"):
            recommendations.append({
                "priority": "high",
                "area": "Design Tokens",
                "issue": "Design tokens incomplete",
                "components": [],
                "commands": [],
                "artemis_says": "Create formal color and typography styles in Figma! 🎨",
                "next_action": "Open Figma and create color/text styles"
            })

        return recommendations


# Main entry point
def artemis_full_analysis(
    figma_url: str,
    figma_token: str,
    mcp_tools: Optional[Dict[str, Any]] = None,
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Complete Artemis analysis with full toolkit.

    Args:
        figma_url: Figma file URL
        figma_token: Figma token
        mcp_tools: Optional MCP tools
        options: Analysis options

    Returns:
        Complete analysis with actionable commands
    """
    # Import Superman's Figma integration
    try:
        from ..superman_figma_integration import analyze_figma_design
    except ImportError:
        from core.superman_figma_integration import analyze_figma_design

    print("🎨 Artemis - Fully Equipped Design System Guardian")
    print("=" * 70)

    # Get Figma data from Superman
    print("\n🦸 Requesting Figma extraction from Superman...")
    figma_data = analyze_figma_design(figma_token, figma_url)

    if "error" in figma_data:
        return figma_data

    # Run fully-equipped analysis
    artemis = ArtemisFullyEquipped("shadcn/ui")
    result = artemis.validate_design_system_complete(figma_data, mcp_tools, options)

    return result


if __name__ == "__main__":
    # Test with ATC RFP
    token = "<FIGMA_ACCESS_TOKEN>"
    url = "https://www.figma.com/design/aKLI77flT3sx0kXMPq2BtZ/ATC-RFP---T1---Oneworxs"

    result = artemis_full_analysis(url, token)

    print("\n" + "=" * 70)
    print("🏹 ARTEMIS FULLY-EQUIPPED REPORT")
    print("=" * 70)
    print(json.dumps(result, indent=2, default=str))
