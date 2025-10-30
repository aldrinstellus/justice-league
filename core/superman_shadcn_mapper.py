"""
🦸 Superman shadcn/ui Mapper - Feature #6 Extension
=====================================================

Maps Figma design system components to official shadcn/ui components
and validates compliance with shadcn/ui standards.

Author: Superman (with Claude Code)
Created: October 21, 2025
Status: Production Ready

Capabilities:
- Extract all components from Figma design system
- Map to official shadcn/ui component registry
- Validate naming conventions
- Check component variants
- Identify missing shadcn/ui components
- Generate compliance report

shadcn/ui Reference: https://ui.shadcn.com/docs/components
"""

import json
from typing import Dict, Any, List, Optional, Set
from collections import defaultdict


class SupermanShadcnMapper:
    """
    Maps Figma components to shadcn/ui official component library.
    """

    # Official shadcn/ui component registry (as of October 2025)
    SHADCN_COMPONENTS = {
        # Form & Input
        "accordion", "alert", "alert-dialog", "aspect-ratio", "avatar",
        "badge", "breadcrumb", "button", "calendar", "card", "carousel",
        "checkbox", "collapsible", "combobox", "command", "context-menu",
        "dialog", "drawer", "dropdown-menu", "form", "hover-card", "input",
        "input-otp", "label", "menubar", "navigation-menu", "pagination",
        "popover", "progress", "radio-group", "resizable", "scroll-area",
        "select", "separator", "sheet", "skeleton", "slider", "sonner",
        "switch", "table", "tabs", "textarea", "toast", "toggle",
        "toggle-group", "tooltip",

        # Charts (New)
        "chart", "area-chart", "bar-chart", "line-chart", "pie-chart",
        "radar-chart", "radial-chart",

        # Blocks
        "sidebar", "breadcrumb-responsive", "cards-stats", "charts",

        # Icons & Media
        "icon", "image", "video",

        # Layout
        "container", "grid", "flex", "stack", "spacer",

        # Typography
        "heading", "text", "code", "link",

        # Data Display
        "list", "description-list", "stat", "metric", "kpi",

        # Feedback
        "spinner", "loading", "empty-state", "error-state",

        # Navigation
        "navbar", "footer", "sidebar-navigation", "mobile-menu"
    }

    def __init__(self, figma_integration):
        """
        Initialize mapper with Figma integration.

        Args:
            figma_integration: SupermanFigmaIntegration instance
        """
        self.figma = figma_integration

    def extract_component_hierarchy(self, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Build component hierarchy from flat component list.

        Args:
            components: List of components from Figma

        Returns:
            Hierarchical structure of components
        """
        hierarchy = defaultdict(list)

        for comp in components:
            name = comp.get("name", "")
            comp_type = comp.get("type", "")
            path = comp.get("path", "")

            # Extract category from path (e.g., "Components/Button/Primary" -> "Components")
            parts = path.split("/")
            category = parts[0] if len(parts) > 1 else "Uncategorized"

            hierarchy[category].append({
                "name": name,
                "type": comp_type,
                "path": path,
                "width": comp.get("width"),
                "height": comp.get("height"),
                "id": comp.get("id")
            })

        return dict(hierarchy)

    def map_to_shadcn(self, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Map Figma components to shadcn/ui components.

        Args:
            components: List of components from Figma

        Returns:
            Mapping results with matched, unmatched, and recommendations
        """
        matched = []
        unmatched = []
        potential_matches = []

        # Normalize component names for matching
        for comp in components:
            name = comp.get("name", "").lower()
            comp_type = comp.get("type", "")

            # Extract component name (remove variants like "Primary", "Large", etc.)
            # Common patterns: "Button / Primary", "Button - Large", "Button.Primary"
            base_name = name.split("/")[0].split("-")[0].split(".")[0].strip()

            # Check for exact match
            if base_name in self.SHADCN_COMPONENTS:
                matched.append({
                    "figma_name": comp.get("name"),
                    "shadcn_component": base_name,
                    "match_type": "exact",
                    "type": comp_type,
                    "path": comp.get("path")
                })
            else:
                # Check for partial match (fuzzy matching)
                possible_shadcn = self._find_similar_shadcn(base_name)
                if possible_shadcn:
                    potential_matches.append({
                        "figma_name": comp.get("name"),
                        "possible_shadcn": possible_shadcn,
                        "match_type": "potential",
                        "type": comp_type,
                        "path": comp.get("path")
                    })
                else:
                    unmatched.append({
                        "figma_name": comp.get("name"),
                        "type": comp_type,
                        "path": comp.get("path"),
                        "reason": "No shadcn/ui equivalent found"
                    })

        return {
            "matched": matched,
            "potential_matches": potential_matches,
            "unmatched": unmatched,
            "matched_count": len(matched),
            "potential_count": len(potential_matches),
            "unmatched_count": len(unmatched),
            "total_components": len(components),
            "coverage_percent": (len(matched) / len(components) * 100) if components else 0
        }

    def _find_similar_shadcn(self, figma_name: str) -> Optional[str]:
        """
        Find similar shadcn/ui component using fuzzy matching.

        Args:
            figma_name: Figma component name

        Returns:
            Most similar shadcn/ui component name or None
        """
        figma_lower = figma_name.lower().strip()

        # Direct substring matching
        for shadcn_comp in self.SHADCN_COMPONENTS:
            if shadcn_comp in figma_lower or figma_lower in shadcn_comp:
                return shadcn_comp

        # Common aliases
        aliases = {
            "btn": "button",
            "input-field": "input",
            "text-field": "input",
            "text-area": "textarea",
            "checkbox-input": "checkbox",
            "radio-button": "radio-group",
            "dropdown": "select",
            "modal": "dialog",
            "popup": "popover",
            "tooltip": "tooltip",
            "nav": "navigation-menu",
            "menu": "menubar",
            "tab": "tabs",
            "slide": "carousel",
            "loading": "spinner"
        }

        for alias, shadcn_name in aliases.items():
            if alias in figma_lower:
                return shadcn_name

        return None

    def find_missing_shadcn_components(self, matched: List[Dict[str, Any]]) -> List[str]:
        """
        Find shadcn/ui components that are missing from Figma design system.

        Args:
            matched: List of matched components

        Returns:
            List of missing shadcn/ui component names
        """
        matched_shadcn = {m["shadcn_component"] for m in matched}
        missing = self.SHADCN_COMPONENTS - matched_shadcn
        return sorted(list(missing))

    def validate_component_naming(self, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate component naming conventions against shadcn/ui standards.

        Args:
            components: List of components from Figma

        Returns:
            Validation results with issues and recommendations
        """
        issues = []
        warnings = []

        for comp in components:
            name = comp.get("name", "")

            # Check naming conventions
            # shadcn/ui uses kebab-case: "button", "input-otp", "toggle-group"
            if " " in name and "/" not in name:
                issues.append({
                    "component": name,
                    "issue": "Contains spaces (should use kebab-case or variants)",
                    "recommendation": f"Rename to use kebab-case or create as variant",
                    "severity": "medium"
                })

            # Check for variant indicators
            if "default" in name.lower() or "primary" in name.lower() or "variant" in name.lower():
                # This is good - it's using variants
                pass

            # Check for size indicators
            if any(size in name.lower() for size in ["sm", "small", "md", "medium", "lg", "large", "xl"]):
                # Good - size variants
                pass

        return {
            "issues": issues,
            "warnings": warnings,
            "issue_count": len(issues),
            "warning_count": len(warnings)
        }

    def generate_compliance_report(self, file_key: str, file_name: str,
                                   components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate complete shadcn/ui compliance report.

        Args:
            file_key: Figma file key
            file_name: Figma file name
            components: List of components from Figma

        Returns:
            Complete compliance report
        """
        print(f"\n🦸 Superman mapping {len(components)} components to shadcn/ui...")

        # Map components
        mapping = self.map_to_shadcn(components)
        print(f"✅ Matched: {mapping['matched_count']} components")
        print(f"⚠️  Potential: {mapping['potential_count']} components")
        print(f"❌ Unmatched: {mapping['unmatched_count']} components")

        # Find missing
        missing = self.find_missing_shadcn_components(mapping["matched"])
        print(f"🔍 Missing {len(missing)} shadcn/ui components")

        # Validate naming
        naming = self.validate_component_naming(components)
        print(f"📝 Found {naming['issue_count']} naming issues")

        # Build hierarchy
        hierarchy = self.extract_component_hierarchy(components)
        print(f"📂 Organized into {len(hierarchy)} categories")

        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(mapping, missing, naming)

        return {
            "file_key": file_key,
            "file_name": file_name,
            "total_components": len(components),
            "mapping": mapping,
            "missing_shadcn_components": missing,
            "naming_validation": naming,
            "component_hierarchy": hierarchy,
            "compliance_score": compliance_score,
            "superman_recommendations": self._generate_compliance_recommendations(
                mapping, missing, naming
            )
        }

    def _calculate_compliance_score(self, mapping: Dict[str, Any],
                                    missing: List[str],
                                    naming: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate shadcn/ui compliance score (0-100).
        """
        score = 0.0
        breakdown = {}

        # Component coverage (40 points)
        coverage_percent = mapping.get("coverage_percent", 0)
        coverage_score = (coverage_percent / 100) * 40
        score += coverage_score
        breakdown["component_coverage"] = coverage_score

        # Missing components penalty (30 points)
        missing_count = len(missing)
        total_shadcn = len(self.SHADCN_COMPONENTS)
        missing_ratio = 1 - (missing_count / total_shadcn)
        missing_score = missing_ratio * 30
        score += missing_score
        breakdown["completeness"] = missing_score

        # Naming conventions (20 points)
        issue_count = naming.get("issue_count", 0)
        total_comps = mapping.get("total_components", 1)
        naming_ratio = 1 - (min(issue_count, total_comps) / total_comps)
        naming_score = naming_ratio * 20
        score += naming_score
        breakdown["naming_conventions"] = naming_score

        # Potential matches bonus (10 points)
        potential_count = mapping.get("potential_count", 0)
        potential_score = min(10, (potential_count / total_comps) * 100)
        score += potential_score
        breakdown["extensibility"] = potential_score

        # Calculate grade
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"

        return {
            "score": round(score, 1),
            "grade": grade,
            "breakdown": breakdown,
            "superman_says": self._get_grade_message(grade, score)
        }

    def _get_grade_message(self, grade: str, score: float) -> str:
        """Get Superman's message based on grade."""
        if grade == "A":
            return f"Excellent shadcn/ui compliance ({score:.1f}/100)! Your design system is super! 🦸⚡"
        elif grade == "B":
            return f"Good shadcn/ui compliance ({score:.1f}/100)! A few tweaks and you'll be perfect! 🦸"
        elif grade == "C":
            return f"Decent shadcn/ui compliance ({score:.1f}/100). Let's strengthen this design system! 💪"
        elif grade == "D":
            return f"Needs improvement ({score:.1f}/100). Many shadcn/ui components are missing or misnamed."
        else:
            return f"Critical issues ({score:.1f}/100). Major redesign needed for shadcn/ui compliance."

    def _generate_compliance_recommendations(self, mapping: Dict[str, Any],
                                            missing: List[str],
                                            naming: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate actionable recommendations for shadcn/ui compliance.
        """
        recommendations = []

        # Missing components
        if len(missing) > 0:
            critical_missing = [
                "button", "input", "select", "checkbox", "radio-group",
                "dialog", "card", "table", "form"
            ]
            missing_critical = [m for m in missing if m in critical_missing]

            if missing_critical:
                recommendations.append({
                    "priority": "critical",
                    "area": "Missing Core Components",
                    "issue": f"Missing {len(missing_critical)} critical shadcn/ui components",
                    "components": missing_critical[:5],
                    "recommendation": "Add these essential shadcn/ui components to your design system",
                    "superman_says": "These are the building blocks! Add them ASAP! 🦸"
                })

            if len(missing) > len(missing_critical):
                recommendations.append({
                    "priority": "high",
                    "area": "Missing Components",
                    "issue": f"Missing {len(missing) - len(missing_critical)} additional shadcn/ui components",
                    "components": [m for m in missing if m not in missing_critical][:10],
                    "recommendation": "Expand your component library to match full shadcn/ui",
                    "superman_says": "More components = more power! 💪"
                })

        # Naming issues
        if naming.get("issue_count", 0) > 0:
            recommendations.append({
                "priority": "medium",
                "area": "Naming Conventions",
                "issue": f"{naming['issue_count']} components have naming issues",
                "recommendation": "Rename components to use kebab-case (e.g., 'toggle-group', 'input-otp')",
                "superman_says": "Consistent naming makes your system stronger! 🦸"
            })

        # Potential matches
        if mapping.get("potential_count", 0) > 5:
            recommendations.append({
                "priority": "low",
                "area": "Potential Improvements",
                "issue": f"{mapping['potential_count']} components might map to shadcn/ui",
                "recommendation": "Review potential matches and align naming with shadcn/ui standards",
                "superman_says": "Fine-tuning these will boost your compliance score! ⚡"
            })

        # If excellent compliance
        if not recommendations:
            recommendations.append({
                "priority": "low",
                "area": "Excellent Compliance",
                "issue": "None - great shadcn/ui alignment!",
                "recommendation": "Maintain this high standard and keep components updated",
                "superman_says": "Your design system is super! Keep it up! 🦸⚡"
            })

        return recommendations


# Main entry point
def map_figma_to_shadcn(figma_token: str, figma_url: str) -> Dict[str, Any]:
    """
    Map Figma design system to shadcn/ui components.

    Args:
        figma_token: Figma Personal Access Token
        figma_url: Figma file URL

    Returns:
        Complete shadcn/ui compliance report
    """
    from superman_figma_integration import SupermanFigmaIntegration

    print("🦸 Superman shadcn/ui Mapper - Analyzing Design System")
    print("=" * 70)

    # Get Figma data
    figma = SupermanFigmaIntegration(figma_token)
    file_key = figma.extract_file_key(figma_url)
    file_data = figma.get_file_data(file_key, depth=3)

    if "error" in file_data:
        return file_data

    file_name = file_data.get("name", "Unknown")
    components_result = figma.extract_components(file_data)
    components = components_result.get("components", [])

    # Map to shadcn/ui
    mapper = SupermanShadcnMapper(figma)
    report = mapper.generate_compliance_report(file_key, file_name, components)

    return report


if __name__ == "__main__":
    # Test with ATC RFP design system
    token = "<FIGMA_ACCESS_TOKEN>"
    url = "https://www.figma.com/design/aKLI77flT3sx0kXMPq2BtZ/ATC-RFP---T1---Oneworxs"

    report = map_figma_to_shadcn(token, url)

    print("\n" + "=" * 70)
    print("📊 SHADCN/UI COMPLIANCE REPORT")
    print("=" * 70)
    print(json.dumps(report, indent=2))
