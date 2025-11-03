"""
🎨 Artemis - The Design System Guardian
========================================

Design system validation, shadcn/ui compliance, and design token management.

Author: Artemis (with Claude Code)
Created: October 21, 2025
Status: Production Ready
"""

import json
from typing import Dict, Any, List, Optional, Set
from datetime import datetime
from collections import defaultdict


class ArtemisDesignGuardian:
    """
    Artemis - Design System Guardian

    Validates design systems, checks shadcn/ui compliance, manages design tokens,
    and ensures Figma-to-code consistency.
    """

    # Official shadcn/ui component registry (October 2025)
    SHADCN_COMPONENTS = {
        # Form & Input
        "accordion", "alert", "alert-dialog", "avatar", "badge", "button",
        "calendar", "checkbox", "combobox", "command", "dialog", "drawer",
        "dropdown-menu", "form", "hover-card", "input", "input-otp", "label",
        "menubar", "navigation-menu", "pagination", "popover", "radio-group",
        "scroll-area", "select", "separator", "sheet", "switch", "textarea",
        "toggle", "toggle-group", "tooltip",

        # Data Display
        "card", "table", "tabs", "breadcrumb",

        # Feedback
        "progress", "skeleton", "toast", "sonner",

        # Charts
        "chart", "area-chart", "bar-chart", "line-chart", "pie-chart",
        "radar-chart", "radial-chart",

        # Layout
        "aspect-ratio", "collapsible", "resizable",

        # Navigation
        "sidebar", "context-menu"
    }

    # Critical components every design system MUST have
    CRITICAL_COMPONENTS = {
        "button", "input", "select", "checkbox", "radio-group",
        "label", "textarea", "form", "card", "dialog"
    }

    def __init__(self, target_framework: str = "shadcn/ui"):
        """
        Initialize Artemis.

        Args:
            target_framework: Target UI framework ('shadcn/ui', 'material-ui', etc.)
        """
        self.target_framework = target_framework

        # Map framework to component registry
        if target_framework == "shadcn/ui":
            self.component_registry = self.SHADCN_COMPONENTS
        else:
            self.component_registry = self.SHADCN_COMPONENTS  # Default to shadcn

    def validate_design_system(self, figma_data: Dict[str, Any],
                               options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Complete design system validation (main entry point).

        Args:
            figma_data: Data from Superman's Figma extraction
            options: Validation options

        Returns:
            Complete validation results with Artemis score
        """
        options = options or {}

        print(f"\n🎨 Artemis analyzing design system...")
        print(f"Target Framework: {self.target_framework}")
        print("=" * 70)

        # Extract components and tokens from Figma data
        components = figma_data.get("components", {}).get("components", [])
        design_tokens = figma_data.get("design_tokens", {})

        print(f"\n📦 Found {len(components)} components in Figma")
        print(f"🎨 Found {design_tokens.get('color_count', 0)} color styles")
        print(f"📝 Found {design_tokens.get('typography_count', 0)} text styles")

        # Component mapping
        mapping = self._map_components(components)
        print(f"\n✅ Matched {mapping['matched_count']} components")
        print(f"❌ Missing {mapping['missing_count']} critical components")

        # Design token validation
        token_health = self._validate_design_tokens(design_tokens)
        print(f"\n🎨 Design Token Health: {token_health['health_score']:.1f}/100")

        # Naming validation
        naming = self._validate_naming(components)
        print(f"📝 Naming Compliance: {naming['compliance_score']:.1f}/100")

        # Variant validation
        variants = self._validate_variants(components, mapping)
        print(f"🔄 Variant Completeness: {variants['completeness_score']:.1f}/100")

        # Calculate Artemis score
        artemis_score = self._calculate_artemis_score(
            mapping, token_health, naming, variants
        )
        print(f"\n🏹 Artemis Score: {artemis_score['score']:.1f}/100 ({artemis_score['grade']})")

        # Generate recommendations
        recommendations = self._generate_recommendations(
            mapping, token_health, naming, variants
        )
        print(f"🎯 Generated {len(recommendations)} recommendations")

        # Build complete result
        result = {
            "artemis_score": artemis_score,
            "component_coverage": mapping,
            "design_tokens": token_health,
            "naming_compliance": naming,
            "variant_completeness": variants,
            "artemis_recommendations": recommendations,
            "analyzed_at": datetime.now().isoformat(),
            "target_framework": self.target_framework,
            "file_name": figma_data.get("file_name", "Unknown"),
            "file_key": figma_data.get("file_key", "Unknown")
        }

        print(f"\n🎨 Artemis analysis complete!")
        return result

    def _map_components(self, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Map Figma components to target framework."""
        matched = []
        matched_unique = set()
        unmatched = []

        for comp in components:
            name = comp.get("name", "").lower()

            # Extract base name (remove variants)
            base_name = name.split("/")[0].split("-")[0].split(".")[0].strip()
            base_name = base_name.split("=")[0].split(",")[0].strip()

            # Check if matches framework
            found = False
            for framework_comp in self.component_registry:
                if framework_comp in base_name or base_name in framework_comp:
                    matched.append({
                        "figma_name": comp.get("name"),
                        "framework_component": framework_comp,
                        "path": comp.get("path", "")
                    })
                    matched_unique.add(framework_comp)
                    found = True
                    break

            if not found:
                unmatched.append(comp.get("name"))

        # Find missing components
        missing = self.component_registry - matched_unique
        missing_critical = self.CRITICAL_COMPONENTS - matched_unique

        return {
            "matched": matched,
            "matched_count": len(matched),
            "matched_unique_count": len(matched_unique),
            "unmatched": unmatched[:100],  # Limit to first 100
            "unmatched_count": len(unmatched),
            "missing_components": sorted(list(missing)),
            "missing_count": len(missing),
            "missing_critical": sorted(list(missing_critical)),
            "missing_critical_count": len(missing_critical),
            "total_framework_components": len(self.component_registry),
            "coverage_percent": (len(matched_unique) / len(self.component_registry)) * 100
        }

    def _validate_design_tokens(self, design_tokens: Dict[str, Any]) -> Dict[str, Any]:
        """Validate design token completeness and consistency."""
        color_count = design_tokens.get("color_count", 0)
        typography_count = design_tokens.get("typography_count", 0)
        effect_count = design_tokens.get("effect_count", 0)

        # Calculate health score
        health_score = 0.0

        # Colors (40 points)
        if color_count >= 10:
            color_score = 40
        elif color_count >= 5:
            color_score = 30
        elif color_count > 0:
            color_score = 20
        else:
            color_score = 0
        health_score += color_score

        # Typography (40 points)
        if typography_count >= 10:
            typography_score = 40
        elif typography_count >= 5:
            typography_score = 30
        elif typography_count > 0:
            typography_score = 20
        else:
            typography_score = 0
        health_score += typography_score

        # Effects (20 points)
        if effect_count >= 5:
            effect_score = 20
        elif effect_count > 0:
            effect_score = 10
        else:
            effect_score = 0
        health_score += effect_score

        return {
            "health_score": health_score,
            "color_count": color_count,
            "typography_count": typography_count,
            "effect_count": effect_count,
            "color_score": color_score,
            "typography_score": typography_score,
            "effect_score": effect_score,
            "issues": self._identify_token_issues(color_count, typography_count, effect_count)
        }

    def _identify_token_issues(self, colors: int, typography: int, effects: int) -> List[str]:
        """Identify design token issues."""
        issues = []

        if colors == 0:
            issues.append("No color styles defined - create brand palette")
        elif colors < 5:
            issues.append(f"Only {colors} color styles - expand to 10+ for complete palette")

        if typography == 0:
            issues.append("No text styles defined - create typography system")
        elif typography < 5:
            issues.append(f"Only {typography} text styles - expand to 10+ for complete typography")

        if effects == 0:
            issues.append("No effect styles - consider adding shadows/elevations")

        return issues

    def _validate_naming(self, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate component naming conventions."""
        issues = []
        total = len(components)

        for comp in components:
            name = comp.get("name", "")

            # Check for spaces (should use kebab-case or variants)
            if " " in name and "/" not in name and "=" not in name:
                issues.append(f"{name}: Contains spaces (use kebab-case)")

        compliance_score = ((total - len(issues)) / total * 100) if total > 0 else 100

        return {
            "compliance_score": compliance_score,
            "total_components": total,
            "issues_count": len(issues),
            "issues": issues[:20]  # Limit to first 20
        }

    def _validate_variants(self, components: List[Dict[str, Any]],
                          mapping: Dict[str, Any]) -> Dict[str, Any]:
        """Validate component variant completeness."""

        # Count variants per component type
        variant_counts = defaultdict(int)
        for match in mapping.get("matched", []):
            framework_comp = match.get("framework_component")
            variant_counts[framework_comp] += 1

        # Calculate completeness
        # Good: 3+ variants per component
        # Acceptable: 1-2 variants
        # Missing: 0 variants

        total_components = mapping.get("matched_unique_count", 0)
        components_with_variants = sum(1 for count in variant_counts.values() if count >= 2)

        completeness_score = (components_with_variants / total_components * 100) if total_components > 0 else 0

        return {
            "completeness_score": completeness_score,
            "variant_counts": dict(variant_counts),
            "components_with_variants": components_with_variants,
            "total_components": total_components
        }

    def _calculate_artemis_score(self, mapping: Dict[str, Any],
                                 token_health: Dict[str, Any],
                                 naming: Dict[str, Any],
                                 variants: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate Artemis Score (0-100).

        Breakdown:
        - Component Coverage: 40 points
        - Design Token Health: 30 points
        - Naming Compliance: 20 points
        - Variant Completeness: 10 points
        """
        score = 0.0
        breakdown = {}

        # Component coverage (40 points)
        coverage_percent = mapping.get("coverage_percent", 0)
        coverage_score = (coverage_percent / 100) * 40

        # Penalty for missing critical components
        missing_critical = mapping.get("missing_critical_count", 0)
        critical_penalty = min(20, missing_critical * 4)  # -4 points per missing critical
        coverage_score = max(0, coverage_score - critical_penalty)

        score += coverage_score
        breakdown["component_coverage"] = coverage_score

        # Design token health (30 points)
        token_score = (token_health.get("health_score", 0) / 100) * 30
        score += token_score
        breakdown["design_token_health"] = token_score

        # Naming compliance (20 points)
        naming_score = (naming.get("compliance_score", 0) / 100) * 20
        score += naming_score
        breakdown["naming_compliance"] = naming_score

        # Variant completeness (10 points)
        variant_score = (variants.get("completeness_score", 0) / 100) * 10
        score += variant_score
        breakdown["variant_completeness"] = variant_score

        # Calculate grade
        if score >= 98:
            grade = "S+"
        elif score >= 95:
            grade = "S"
        elif score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        else:
            grade = "D"

        return {
            "score": round(score, 1),
            "grade": grade,
            "breakdown": breakdown,
            "artemis_says": self._get_grade_message(grade, score, mapping)
        }

    def _get_grade_message(self, grade: str, score: float, mapping: Dict[str, Any]) -> str:
        """Get Artemis's message based on grade."""
        missing_critical = mapping.get("missing_critical_count", 0)

        if grade == "S+" or grade == "S":
            return f"Perfect design system ({score:.1f}/100)! Artemis is proud! 🎨🏹"
        elif grade == "A":
            return f"Excellent design system ({score:.1f}/100)! Minor improvements needed. 🎯"
        elif grade == "B":
            return f"Good foundation ({score:.1f}/100). Add missing components! 🏹"
        elif grade == "C":
            if missing_critical > 0:
                return f"Missing {missing_critical} critical components! Add them ASAP! ⚠️"
            return f"Needs improvement ({score:.1f}/100). Strengthen your design system! 💪"
        else:
            return f"Critical issues ({score:.1f}/100). Major work needed! 🚨"

    def _generate_recommendations(self, mapping: Dict[str, Any],
                                 token_health: Dict[str, Any],
                                 naming: Dict[str, Any],
                                 variants: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations."""
        recommendations = []

        # Missing critical components
        missing_critical = mapping.get("missing_critical", [])
        if missing_critical:
            recommendations.append({
                "priority": "critical",
                "area": "Components",
                "issue": f"Missing {len(missing_critical)} critical components",
                "recommendation": f"Add these immediately: {', '.join(missing_critical[:5])}",
                "components_affected": missing_critical,
                "impact": "Blocks basic UI functionality",
                "artemis_says": f"Every design system needs these {len(missing_critical)} critical components! 🎯",
                "action": f"npx shadcn@latest add {' '.join(missing_critical[:3])}"
            })

        # Missing other components
        missing_other = [c for c in mapping.get("missing_components", []) if c not in missing_critical]
        if missing_other and len(missing_other) > 0:
            recommendations.append({
                "priority": "high",
                "area": "Components",
                "issue": f"Missing {len(missing_other)} additional components",
                "recommendation": f"Expand component library: {', '.join(missing_other[:5])}",
                "components_affected": missing_other[:10],
                "impact": "Limits design system completeness",
                "artemis_says": "More components = more power! 🏹",
                "action": f"npx shadcn@latest add {' '.join(missing_other[:3])}"
            })

        # Design token issues
        token_issues = token_health.get("issues", [])
        if token_issues:
            recommendations.append({
                "priority": "high",
                "area": "Design Tokens",
                "issue": "; ".join(token_issues[:2]),
                "recommendation": "Create formal color and typography styles in Figma",
                "components_affected": [],
                "impact": "Improves consistency and scalability",
                "artemis_says": "Design tokens are the foundation of great design systems! 🎨"
            })

        # Naming issues
        if naming.get("compliance_score", 100) < 80:
            recommendations.append({
                "priority": "medium",
                "area": "Naming Conventions",
                "issue": f"{naming.get('issues_count', 0)} components have naming issues",
                "recommendation": "Rename components to use kebab-case (e.g., 'toggle-group', 'input-otp')",
                "components_affected": [],
                "impact": "Improves code consistency and maintainability",
                "artemis_says": "Consistent naming = precise aim! 🎯"
            })

        # Variant issues
        if variants.get("completeness_score", 0) < 50:
            recommendations.append({
                "priority": "medium",
                "area": "Component Variants",
                "issue": "Many components lack proper variants",
                "recommendation": "Create size, state, and color variants for each component",
                "components_affected": [],
                "impact": "Increases design system flexibility",
                "artemis_says": "Variants give your components versatility! 🏹"
            })

        # If excellent
        if not recommendations:
            recommendations.append({
                "priority": "low",
                "area": "Excellence",
                "issue": "None - design system is excellent!",
                "recommendation": "Maintain this high standard",
                "components_affected": [],
                "impact": "Continued design system health",
                "artemis_says": "Your design system is battle-ready! 🎨🏹"
            })

        return recommendations


# Main entry point
def artemis_design_system_analysis(figma_url: str, figma_token: str,
                                   target_framework: str = "shadcn/ui",
                                   options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Complete design system analysis (main entry point).

    Args:
        figma_url: Figma file URL
        figma_token: Figma Personal Access Token
        target_framework: Target UI framework
        options: Analysis options

    Returns:
        Complete Artemis analysis
    """
    # Import Superman's Figma integration
    try:
        from ..superman_figma_integration import analyze_figma_design
    except ImportError:
        from core.superman_figma_integration import analyze_figma_design

    print("🎨 Artemis - Design System Guardian")
    print("=" * 70)

    # Get Figma data from Superman
    print("\n🦸 Requesting Figma extraction from Superman...")
    figma_data = analyze_figma_design(figma_token, figma_url)

    if "error" in figma_data:
        return figma_data

    # Run Artemis analysis
    artemis = ArtemisDesignGuardian(target_framework)
    result = artemis.validate_design_system(figma_data, options)

    return result


if __name__ == "__main__":
    # Test with ATC RFP design system
    token = "<FIGMA_ACCESS_TOKEN>"
    url = "https://www.figma.com/design/aKLI77flT3sx0kXMPq2BtZ/ATC-RFP---T1---Oneworxs"

    result = artemis_design_system_analysis(url, token)

    print("\n" + "=" * 70)
    print("📊 ARTEMIS DESIGN SYSTEM REPORT")
    print("=" * 70)
    print(json.dumps(result, indent=2))
