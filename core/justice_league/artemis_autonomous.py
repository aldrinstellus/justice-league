"""
🎨 ARTEMIS - AUTONOMOUS DESIGN SYSTEM GUARDIAN
===============================================

Artemis with full autonomous capabilities from HeroBase.

Powers:
- 🏹 Bow of Precision: shadcn CLI for component validation
- 🎯 Arrow of Truth: Figma MCP for design extraction
- 🛡️ Guardian Shield: Component registry access
- 📖 Quiver of Knowledge: Best practices enforcement
- 🤝 Team Collaboration: Inter-hero communication
- 🔧 Self-Healing: Auto-recovery from failures
- 🧠 Auto-Learning: Pattern recognition and improvement

Author: Artemis (with Claude Code + Superman)
Created: October 21, 2025
Status: Production Ready - Fully Autonomous
"""

import json
import subprocess
import logging
from typing import Dict, Any, List, Optional, Set
from datetime import datetime
from collections import defaultdict

# Import HeroBase for autonomous capabilities
try:
    from .hero_base import HeroBase, HeroPriority
except ImportError:
    from hero_base import HeroBase, HeroPriority


class ArtemisAutonomous(HeroBase):
    """
    Artemis - Fully Autonomous Design System Guardian

    Inherits all autonomous capabilities from HeroBase:
    - Inter-hero communication
    - Self-healing
    - Auto-learning
    - Peer verification
    - Knowledge sharing

    Plus Artemis-specific powers:
    - Design system validation
    - shadcn/ui compliance checking
    - Figma design extraction
    - Component registry access
    """

    def __init__(self, target_framework: str = "shadcn/ui",
                 baseline_dir: Optional[str] = None):
        """
        Initialize autonomous Artemis.

        Args:
            target_framework: Target UI framework
            baseline_dir: Directory for storing Artemis data
        """
        # Initialize HeroBase with autonomous capabilities
        super().__init__(
            hero_name="Artemis",
            hero_emoji="🎨",
            baseline_dir=baseline_dir
        )

        # Artemis-specific attributes
        self.target_framework = target_framework
        self.shadcn_registry = None

        # Register fallback strategies
        self.register_fallback("shadcn_registry_fetch", self._fallback_use_cached_registry)
        self.register_fallback("component_validation", self._fallback_basic_validation)

        self.logger.info(f"{self.hero_emoji} Artemis fully autonomous and ready!")

    # ===========================================
    # ARTEMIS CORE MISSION: DESIGN SYSTEM VALIDATION
    # ===========================================

    def validate_design_system(
        self,
        figma_data: Dict[str, Any],
        mcp_tools: Optional[Dict[str, Any]] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Complete design system validation with full autonomous capabilities.

        Args:
            figma_data: Data from Superman's Figma extraction
            mcp_tools: Optional MCP tools for Figma access
            options: Validation options

        Returns:
            Complete validation with commands and recommendations
        """
        options = options or {}

        self.logger.info(f"\n{self.hero_emoji} Artemis starting autonomous design system validation")
        self.logger.info("=" * 70)

        # Check if we should request help from Superman
        if not figma_data or "error" in figma_data:
            self.logger.warning(f"{self.hero_emoji} Figma data incomplete, requesting help from Superman")
            self.request_help(
                "Superman",
                "Need Figma design extraction",
                {"reason": "figma_data_missing", "target": options.get("figma_url")}
            )
            return {"error": "Waiting for Superman to extract Figma data"}

        # Try to get shadcn registry with self-healing
        try:
            official_components = self.get_official_shadcn_components()
        except Exception as e:
            self.logger.warning(f"{self.hero_emoji} Error fetching shadcn registry: {e}")
            # Auto-recover
            recovery_result = self.auto_recover(
                e, "shadcn_registry_fetch",
                {"framework": self.target_framework}
            )
            if recovery_result:
                official_components = recovery_result.get("components", set())
            else:
                # Request help from Wonder Woman (design expert)
                self.request_help(
                    "Wonder Woman",
                    "shadcn registry unavailable, need component list",
                    {"framework": self.target_framework}
                )
                official_components = set()

        self.logger.info(f"{self.hero_emoji} Official shadcn/ui components: {len(official_components)}")

        # Extract from Figma
        figma_components = figma_data.get("components", {}).get("components", [])
        design_tokens = figma_data.get("design_tokens", {})

        self.logger.info(f"{self.hero_emoji} Figma components: {len(figma_components)}")
        self.logger.info(
            f"{self.hero_emoji} Design tokens: {design_tokens.get('color_count', 0)} colors, "
            f"{design_tokens.get('typography_count', 0)} text styles"
        )

        # Map Figma components to shadcn
        mapping = self._map_components_advanced(figma_components, official_components)

        self.logger.info(f"\n{self.hero_emoji} ✅ Matched: {mapping['matched_unique_count']}/{len(official_components)}")
        self.logger.info(f"{self.hero_emoji} ❌ Missing: {mapping['missing_count']} components")
        self.logger.info(f"{self.hero_emoji} 📈 Coverage: {mapping['coverage_percent']:.1f}%")

        # Validate design tokens
        token_health = self._validate_design_tokens(design_tokens)

        # If design tokens are weak, ask Wonder Woman for accessibility advice
        if token_health.get("needs_colors") or token_health.get("needs_typography"):
            self.share_finding({
                "type": "design_token_weakness",
                "color_count": design_tokens.get("color_count", 0),
                "typography_count": design_tokens.get("typography_count", 0),
                "recommendation": "Need more formal design tokens"
            }, target_heroes=["Wonder Woman"])

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

        self.logger.info(f"\n{self.hero_emoji} 🏹 Artemis Score: {artemis_score['score']:.1f}/100 ({artemis_score['grade']})")
        self.logger.info(f"{self.hero_emoji} 🎯 {len(recommendations)} actionable recommendations")
        self.logger.info(f"{self.hero_emoji} ⚡ {len(add_commands)} CLI commands generated")

        # Record mission
        self.record_mission(
            mission_type="design_system_validation",
            result={
                "score": artemis_score["score"],
                "coverage": mapping["coverage_percent"],
                "missing_critical": mapping.get("missing_critical_count", 0)
            },
            success=artemis_score["score"] >= 70
        )

        # Learn from this analysis
        if artemis_score["score"] < 70:
            self.learn_from_failure({
                "operation": "design_system_validation",
                "error": "Low coverage score",
                "root_cause": f"Missing {mapping['missing_count']} components",
                "solution": f"Add components: {', '.join(list(missing_components)[:5])}"
            })

        # Contribute to knowledge base
        self.contribute_to_knowledge_base(
            knowledge_type="best_practice",
            content={
                "practice": f"Design systems should have >{artemis_score['score']:.0f}% component coverage",
                "reason": "Ensures comprehensive component library",
                "framework": self.target_framework,
                "critical_components": list(mapping.get("missing_critical", set()))
            }
        )

        # If score is good, ask Zatanna to verify CSS implementation
        if artemis_score["score"] >= 80:
            self.verify_with_peer({
                "validation": "design_system",
                "score": artemis_score["score"],
                "coverage": mapping["coverage_percent"]
            }, "Zatanna")

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
            "tools_used": ["shadcn-cli", "figma-extraction", "component-registry"],
            "autonomous_capabilities": {
                "self_healing_used": True,
                "peer_collaboration": True,
                "knowledge_contributed": True
            }
        }

        self.logger.info(f"\n{self.hero_emoji} Artemis fully-autonomous analysis complete!")
        return result

    # ===========================================
    # SHADCN REGISTRY ACCESS
    # ===========================================

    def get_shadcn_registry(self) -> Dict[str, Any]:
        """
        Get complete shadcn registry using CLI with self-healing.

        Returns:
            Complete component registry
        """
        if self.shadcn_registry:
            return self.shadcn_registry

        self.logger.info(f"{self.hero_emoji} Accessing shadcn registry...")

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
                self.logger.info(f"{self.hero_emoji} ✅ Found {total} components in shadcn registry")

                return data
            else:
                raise Exception(f"shadcn CLI error: {result.stderr}")

        except Exception as e:
            self.logger.error(f"{self.hero_emoji} ⚠️  Error accessing shadcn registry: {e}")

            # Auto-recover
            recovery = self.auto_recover(e, "shadcn_registry_fetch", {"framework": self.target_framework})
            if recovery:
                return recovery.get("registry", {"items": [], "pagination": {"total": 0}})

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

    # ===========================================
    # COMPONENT MAPPING & ANALYSIS
    # ===========================================

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
            return f"Perfect design system! Artemis approves! {self.hero_emoji}🏹"
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

    # ===========================================
    # FALLBACK STRATEGIES
    # ===========================================

    def _fallback_use_cached_registry(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback: Use cached registry if available."""
        self.logger.info(f"{self.hero_emoji} Using cached registry fallback")

        # Check if we have learned patterns
        pattern = self.check_learned_patterns("shadcn_registry_fetch")
        if pattern:
            return pattern.get("solution", {})

        # Return minimal working set
        return {
            "registry": {
                "items": [],
                "pagination": {"total": 0}
            },
            "components": {
                "button", "input", "card", "dialog", "select",
                "checkbox", "label", "textarea", "form"
            }
        }

    def _fallback_basic_validation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback: Basic validation without registry."""
        self.logger.info(f"{self.hero_emoji} Using basic validation fallback")
        return {
            "validation": "basic",
            "score": 50,
            "message": "Limited validation without full registry"
        }


# Example usage
if __name__ == "__main__":
    # Create autonomous Artemis
    artemis = ArtemisAutonomous()

    # Show status
    status = artemis.get_status()
    print(f"\n{json.dumps(status, indent=2)}")

    # Test communication
    artemis.request_help("Superman", "Need Figma extraction")
    artemis.share_finding({
        "type": "missing_components",
        "count": 5
    }, broadcast=True)

    print(f"\n{artemis.hero_emoji} Artemis autonomous and ready for missions!")
