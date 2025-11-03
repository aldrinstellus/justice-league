"""
🔮 ORACLE HERO TRAINER
Justice League Hero Skills Management & Training System

Oracle's advanced capability for analyzing, training, and continuously improving all Justice League heroes.

Powers:
- 📊 Skill Analysis - Extract capabilities from each hero's code
- 🎓 Training System - Generate practice missions to improve hero skills
- 📈 Performance Tracking - Monitor skill improvements over time
- 🔄 Auto-Update - Keep hero skills database current
- 🧠 Smart Recommendations - Suggest skill upgrades based on mission patterns

"Train hard. Fight easy. Every hero gets better with Oracle." - Oracle
"""

import ast
import inspect
import json
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class HeroSkillAnalyzer:
    """
    Analyzes hero Python files to extract capabilities, methods, and skills
    """

    def __init__(self):
        self.hero_dir = Path(__file__).parent

    def analyze_hero_file(self, hero_file_path: Path) -> Dict[str, Any]:
        """
        Extract all capabilities from a hero's Python file

        Returns:
            Dict with hero capabilities, methods, docstrings, and skills
        """
        try:
            with open(hero_file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()

            # Parse Python AST
            tree = ast.parse(source_code)

            # Extract hero class
            hero_class = None
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Skip base classes, look for main hero class
                    if not node.name.startswith('_') and 'Base' not in node.name:
                        hero_class = node
                        break

            if not hero_class:
                return {"error": "No hero class found"}

            # Extract capabilities
            capabilities = {
                "class_name": hero_class.name,
                "file_path": str(hero_file_path),
                "docstring": ast.get_docstring(hero_class) or "",
                "methods": [],
                "attributes": [],
                "skills": [],
                "powers": [],
                "dependencies": [],
                "narrator_integrated": False,
                "mcp_integrated": False
            }

            # Analyze class body
            for item in hero_class.body:
                # Extract methods
                if isinstance(item, ast.FunctionDef):
                    method_info = {
                        "name": item.name,
                        "docstring": ast.get_docstring(item) or "",
                        "parameters": [arg.arg for arg in item.args.args if arg.arg != 'self'],
                        "is_public": not item.name.startswith('_'),
                        "returns": self._extract_return_type(item)
                    }
                    capabilities["methods"].append(method_info)

                    # Check for narrator integration
                    if item.name in ['say', 'think', 'handoff']:
                        capabilities["narrator_integrated"] = True

                # Extract attributes from __init__
                if isinstance(item, ast.FunctionDef) and item.name == '__init__':
                    for stmt in item.body:
                        if isinstance(stmt, ast.Assign):
                            for target in stmt.targets:
                                if isinstance(target, ast.Attribute) and target.attr:
                                    capabilities["attributes"].append(target.attr)

            # Extract skills from docstring and methods
            capabilities["skills"] = self._extract_skills(capabilities)

            # Extract powers from class docstring
            capabilities["powers"] = self._extract_powers(capabilities["docstring"])

            # Check for MCP integration
            if 'mcp' in source_code.lower() or 'playwright' in source_code.lower():
                capabilities["mcp_integrated"] = True

            return capabilities

        except Exception as e:
            logger.error(f"Error analyzing {hero_file_path}: {e}")
            return {"error": str(e)}

    def _extract_return_type(self, func_node: ast.FunctionDef) -> Optional[str]:
        """Extract return type annotation if present"""
        if func_node.returns:
            return ast.unparse(func_node.returns)
        return None

    def _extract_skills(self, capabilities: Dict[str, Any]) -> List[str]:
        """
        Extract skills from hero methods and docstrings
        """
        skills = set()

        # Skills from method names
        for method in capabilities["methods"]:
            if method["is_public"]:
                # Convert method name to skill description
                name = method["name"].replace('_', ' ').title()

                # Filter out generic methods
                if name not in ['Say', 'Think', 'Handoff', 'Init']:
                    skills.add(name)

        # Skills from docstring keywords
        docstring = capabilities.get("docstring", "").lower()
        skill_keywords = [
            "generate", "analyze", "validate", "test", "export", "convert",
            "parse", "extract", "optimize", "measure", "scan", "detect",
            "build", "create", "monitor", "track", "coordinate", "deploy"
        ]

        for keyword in skill_keywords:
            if keyword in docstring:
                skills.add(keyword.title())

        return sorted(list(skills))

    def _extract_powers(self, docstring: str) -> List[str]:
        """
        Extract hero powers from class docstring
        """
        powers = []
        lines = docstring.split('\n')

        in_powers_section = False
        for line in lines:
            line = line.strip()

            if 'power' in line.lower() and ':' in line:
                in_powers_section = True
                continue

            if in_powers_section:
                if line.startswith('-'):
                    # Extract power description
                    power = line.lstrip('-').strip()
                    if power:
                        powers.append(power)
                elif line and not line.startswith(' '):
                    # End of powers section
                    break

        return powers

    def analyze_all_heroes(self) -> Dict[str, Dict[str, Any]]:
        """
        Analyze all hero files in the justice_league directory

        Returns:
            Dictionary mapping hero names to their capabilities
        """
        hero_files = list(self.hero_dir.glob("*.py"))
        all_capabilities = {}

        # Filter to main hero files (exclude base classes, utilities)
        main_heroes = [
            'superman_coordinator.py',
            'oracle_meta_agent.py',
            'artemis_codesmith.py',
            'green_arrow_visual_validator.py',
            'hawkman_equipped.py',
            'vision_analyst.py',
            'batman_testing.py',
            'green_lantern_visual.py',
            'wonder_woman_accessibility.py',
            'flash_performance.py',
            'aquaman_network.py',
            'cyborg_integrations.py',
            'martian_manhunter_security.py',
            'atom_component_analysis.py',
            'plastic_man_responsive.py',
            'zatanna_seo.py',
            'litty_ethics.py',
            'hephaestus_code_to_design.py',
            'quicksilver_speed_export.py'
        ]

        for hero_file in hero_files:
            if hero_file.name in main_heroes:
                capabilities = self.analyze_hero_file(hero_file)
                if "error" not in capabilities:
                    hero_name = hero_file.stem.replace('_', ' ').title()
                    all_capabilities[hero_name] = capabilities

        return all_capabilities


class HeroTrainingSystem:
    """
    Generates training scenarios and tracks skill improvements for heroes
    """

    def __init__(self, knowledge_base_path: Path):
        self.knowledge_base_path = knowledge_base_path
        self.skills_db_path = knowledge_base_path / 'hero_skills.json'
        self.training_db_path = knowledge_base_path / 'hero_training.json'

    def load_skills_database(self) -> Dict[str, Any]:
        """Load hero skills database"""
        if self.skills_db_path.exists():
            with open(self.skills_db_path, 'r') as f:
                return json.load(f)
        return {"heroes": {}, "last_updated": None}

    def save_skills_database(self, skills_data: Dict[str, Any]):
        """Save hero skills database"""
        skills_data["last_updated"] = datetime.now().isoformat()
        with open(self.skills_db_path, 'w') as f:
            json.dump(skills_data, f, indent=2)

    def create_training_scenario(self, hero_name: str, skill_gap: str) -> Dict[str, Any]:
        """
        Generate a training scenario to improve a specific skill gap

        Args:
            hero_name: Name of the hero
            skill_gap: Specific skill that needs improvement

        Returns:
            Training scenario with objectives and success criteria
        """
        scenario_templates = {
            "Code Generation": {
                "objectives": [
                    f"Generate 5 complex components with 90%+ accuracy",
                    f"Handle nested structures correctly",
                    f"Maintain consistent code style"
                ],
                "success_criteria": {
                    "min_accuracy": 90,
                    "consistency_required": True,
                    "iterations_max": 3
                }
            },
            "Visual Validation": {
                "objectives": [
                    f"Validate 10 components with pixel-perfect accuracy",
                    f"Identify spacing issues within 2px tolerance",
                    f"Color matching with 95%+ accuracy"
                ],
                "success_criteria": {
                    "min_accuracy": 95,
                    "pixel_tolerance": 2,
                    "color_accuracy": 0.95
                }
            },
            "Performance Analysis": {
                "objectives": [
                    f"Analyze 5 complex applications",
                    f"Identify all performance bottlenecks",
                    f"Generate actionable optimization recommendations"
                ],
                "success_criteria": {
                    "bottlenecks_found": "all",
                    "recommendation_quality": "actionable",
                    "improvement_measurable": True
                }
            },
            "Frame Export": {
                "objectives": [
                    f"Export 100+ frames with 100% success rate",
                    f"Handle large files (50MB+) reliably",
                    f"Maintain export speed within 10% variance"
                ],
                "success_criteria": {
                    "success_rate": 1.0,
                    "reliability": "100%",
                    "speed_consistency": 0.10
                }
            }
        }

        # Match skill gap to template
        template = None
        for key in scenario_templates:
            if key.lower() in skill_gap.lower():
                template = scenario_templates[key]
                break

        if not template:
            template = scenario_templates["Code Generation"]  # Default

        scenario = {
            "scenario_id": f"TRAIN-{hero_name.upper()[:3]}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "hero": hero_name,
            "target_area": skill_gap,
            "difficulty": "adaptive",
            "objectives": template["objectives"],
            "success_criteria": template["success_criteria"],
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "completion_status": {
                "attempts": 0,
                "successes": 0,
                "failures": 0,
                "best_score": 0
            }
        }

        return scenario

    def recommend_skill_upgrades(self, hero_name: str, mission_history: List[Dict]) -> List[str]:
        """
        Analyze mission history and recommend skill upgrades for hero

        Args:
            hero_name: Name of the hero
            mission_history: List of past mission records

        Returns:
            List of recommended skill upgrades
        """
        recommendations = []

        # Analyze failure patterns
        failures = [m for m in mission_history if not m.get('success', True)]
        if failures:
            # Extract common failure reasons
            failure_reasons = [f.get('failure_reason', 'Unknown') for f in failures]
            recommendations.append(f"Address failure pattern: {failure_reasons[0]}")

        # Analyze accuracy trends
        accuracy_scores = [m.get('score', 0) for m in mission_history if 'score' in m]
        if accuracy_scores:
            avg_accuracy = sum(accuracy_scores) / len(accuracy_scores)
            if avg_accuracy < 85:
                recommendations.append(f"Improve accuracy (current avg: {avg_accuracy:.1f}%)")

        # Check for consistency issues
        if len(accuracy_scores) > 3:
            variance = max(accuracy_scores) - min(accuracy_scores)
            if variance > 20:
                recommendations.append(f"Improve consistency (variance: {variance:.1f}%)")

        return recommendations

    def update_hero_skill_level(self, hero_name: str, skill: str, new_level: int):
        """
        Update a hero's skill level in the database

        Args:
            hero_name: Name of the hero
            skill: Skill name
            new_level: New skill level (0-100)
        """
        skills_data = self.load_skills_database()

        if hero_name not in skills_data["heroes"]:
            skills_data["heroes"][hero_name] = {"skills": {}}

        if "skills" not in skills_data["heroes"][hero_name]:
            skills_data["heroes"][hero_name]["skills"] = {}

        # Update skill level
        old_level = skills_data["heroes"][hero_name]["skills"].get(skill, 0)
        skills_data["heroes"][hero_name]["skills"][skill] = new_level

        # Track improvement
        improvement = new_level - old_level
        if "skill_history" not in skills_data["heroes"][hero_name]:
            skills_data["heroes"][hero_name]["skill_history"] = []

        skills_data["heroes"][hero_name]["skill_history"].append({
            "timestamp": datetime.now().isoformat(),
            "skill": skill,
            "old_level": old_level,
            "new_level": new_level,
            "improvement": improvement
        })

        self.save_skills_database(skills_data)
        logger.info(f"Updated {hero_name}'s {skill} skill: {old_level} → {new_level} (+{improvement})")


class OracleHeroTrainer:
    """
    🔮 Main Oracle Hero Training System

    Combines skill analysis, training scenario generation, and performance tracking
    to continuously improve all Justice League heroes.
    """

    def __init__(self, knowledge_base_dir: Optional[Path] = None):
        """
        Initialize Oracle's hero training system

        Args:
            knowledge_base_dir: Directory for training data storage
        """
        self.knowledge_base_dir = knowledge_base_dir or Path('/tmp/aldo-vision-justice-league/oracle')
        self.knowledge_base_dir.mkdir(parents=True, exist_ok=True)

        self.analyzer = HeroSkillAnalyzer()
        self.training_system = HeroTrainingSystem(self.knowledge_base_dir)

        self.hero_emoji_map = {
            "Superman Coordinator": "🦸",
            "Oracle Meta Agent": "🔮",
            "Artemis Codesmith": "🎨",
            "Green Arrow Visual Validator": "🎯",
            "Hawkman Equipped": "🦅",
            "Vision Analyst": "👁️",
            "Batman Testing": "🦇",
            "Green Lantern Visual": "💚",
            "Wonder Woman Accessibility": "⚡",
            "Flash Performance": "⚡",
            "Aquaman Network": "🌊",
            "Cyborg Integrations": "🤖",
            "Martian Manhunter Security": "🧠",
            "Atom Component Analysis": "🔬",
            "Plastic Man Responsive": "🤸",
            "Zatanna Seo": "🎩",
            "Litty Ethics": "🪔",
            "Hephaestus Code To Design": "🔨",
            "Quicksilver Speed Export": "⚡"
        }

    def analyze_and_update_all_heroes(self) -> Dict[str, Any]:
        """
        Analyze all hero capabilities and update skills database

        Returns:
            Complete hero skills database
        """
        print("\n🔮 Oracle Hero Trainer - Analyzing Justice League Capabilities")
        print("=" * 80)

        # Analyze all heroes
        all_capabilities = self.analyzer.analyze_all_heroes()

        # Load existing skills database
        skills_data = self.training_system.load_skills_database()

        # Update skills database
        for hero_name, capabilities in all_capabilities.items():
            emoji = self.hero_emoji_map.get(hero_name, "🦸")

            print(f"\n{emoji} {hero_name}")
            print(f"   Skills: {len(capabilities['skills'])}")
            print(f"   Methods: {len(capabilities['methods'])}")
            print(f"   Narrator: {'✅' if capabilities['narrator_integrated'] else '❌'}")
            print(f"   MCP: {'✅' if capabilities['mcp_integrated'] else '❌'}")

            # Store in database
            skills_data["heroes"][hero_name] = {
                "capabilities": capabilities,
                "emoji": emoji,
                "last_analyzed": datetime.now().isoformat(),
                "skill_levels": self._calculate_skill_levels(capabilities),
                "training_needed": self._identify_training_needs(capabilities)
            }

        # Save updated database
        self.training_system.save_skills_database(skills_data)

        print(f"\n✅ Updated skills database for {len(all_capabilities)} heroes")
        print(f"📁 Database: {self.training_system.skills_db_path}")

        return skills_data

    def _calculate_skill_levels(self, capabilities: Dict[str, Any]) -> Dict[str, int]:
        """
        Calculate skill levels based on capabilities

        Returns:
            Dictionary of skill names to levels (0-100)
        """
        skill_levels = {}

        # Base level from number of methods
        method_count = len(capabilities.get("methods", []))
        base_level = min(50 + method_count * 2, 100)

        for skill in capabilities.get("skills", []):
            # Start with base level
            level = base_level

            # Bonus for narrator integration
            if capabilities.get("narrator_integrated"):
                level += 10

            # Bonus for MCP integration
            if capabilities.get("mcp_integrated"):
                level += 10

            skill_levels[skill] = min(level, 100)

        return skill_levels

    def _identify_training_needs(self, capabilities: Dict[str, Any]) -> List[str]:
        """
        Identify areas where hero needs training

        Returns:
            List of training recommendations
        """
        needs = []

        # Check narrator integration
        if not capabilities.get("narrator_integrated"):
            needs.append("Narrator integration (say, think, handoff methods)")

        # Check MCP integration where relevant
        if "Visual" in capabilities.get("class_name", "") and not capabilities.get("mcp_integrated"):
            needs.append("MCP/Playwright integration for visual testing")

        # Check for missing common methods
        method_names = [m["name"] for m in capabilities.get("methods", [])]

        if "analyze" not in ' '.join(method_names).lower():
            needs.append("Analysis capabilities")

        if len(capabilities.get("skills", [])) < 5:
            needs.append("Expand skill set (currently < 5 skills)")

        return needs

    def generate_training_plan(self, hero_name: str) -> Dict[str, Any]:
        """
        Generate a comprehensive training plan for a hero

        Args:
            hero_name: Name of the hero

        Returns:
            Training plan with scenarios and objectives
        """
        skills_data = self.training_system.load_skills_database()

        if hero_name not in skills_data.get("heroes", {}):
            return {"error": f"Hero {hero_name} not found in database"}

        hero_data = skills_data["heroes"][hero_name]
        training_needs = hero_data.get("training_needed", [])

        # Generate training scenarios
        scenarios = []
        for need in training_needs:
            scenario = self.training_system.create_training_scenario(hero_name, need)
            scenarios.append(scenario)

        training_plan = {
            "hero": hero_name,
            "emoji": hero_data.get("emoji", "🦸"),
            "current_skill_count": len(hero_data.get("capabilities", {}).get("skills", [])),
            "training_needs": training_needs,
            "training_scenarios": scenarios,
            "estimated_duration": f"{len(scenarios) * 2} hours",
            "expected_improvements": self._estimate_improvements(training_needs),
            "created_at": datetime.now().isoformat()
        }

        return training_plan

    def _estimate_improvements(self, training_needs: List[str]) -> List[str]:
        """Estimate skill improvements from training"""
        improvements = []

        for need in training_needs:
            if "Narrator" in need:
                improvements.append("+15% team coordination efficiency")
            if "MCP" in need:
                improvements.append("+20% visual testing accuracy")
            if "Analysis" in need:
                improvements.append("+10% problem detection rate")
            if "skill set" in need.lower():
                improvements.append("+25% mission capability coverage")

        return improvements

    def get_hero_report_card(self, hero_name: str) -> str:
        """
        Generate a formatted report card for a hero

        Args:
            hero_name: Name of the hero

        Returns:
            Formatted report card string
        """
        skills_data = self.training_system.load_skills_database()

        if hero_name not in skills_data.get("heroes", {}):
            return f"❌ Hero {hero_name} not found in database"

        hero_data = skills_data["heroes"][hero_name]
        emoji = hero_data.get("emoji", "🦸")

        report = f"\n{'='*80}\n"
        report += f"{emoji} {hero_name} - Hero Report Card\n"
        report += f"{'='*80}\n\n"

        # Capabilities summary
        capabilities = hero_data.get("capabilities", {})
        report += f"📊 Capabilities Summary:\n"
        report += f"   • Skills: {len(capabilities.get('skills', []))}\n"
        report += f"   • Methods: {len(capabilities.get('methods', []))}\n"
        report += f"   • Powers: {len(capabilities.get('powers', []))}\n"
        report += f"   • Narrator: {'✅ Integrated' if capabilities.get('narrator_integrated') else '❌ Not Integrated'}\n"
        report += f"   • MCP: {'✅ Integrated' if capabilities.get('mcp_integrated') else '❌ Not Integrated'}\n\n"

        # Skill levels
        skill_levels = hero_data.get("skill_levels", {})
        if skill_levels:
            report += f"⭐ Skill Levels:\n"
            for skill, level in sorted(skill_levels.items(), key=lambda x: x[1], reverse=True)[:10]:
                bar = "█" * (level // 10) + "░" * (10 - level // 10)
                report += f"   {skill:30s} [{bar}] {level}/100\n"
            report += "\n"

        # Training needs
        training_needs = hero_data.get("training_needed", [])
        if training_needs:
            report += f"🎓 Training Recommendations:\n"
            for i, need in enumerate(training_needs, 1):
                report += f"   {i}. {need}\n"
            report += "\n"

        # Overall grade
        avg_skill = sum(skill_levels.values()) / len(skill_levels) if skill_levels else 0
        grade = "A+" if avg_skill >= 90 else "A" if avg_skill >= 80 else "B" if avg_skill >= 70 else "C"
        report += f"📝 Overall Grade: {grade} (Avg Skill: {avg_skill:.1f}/100)\n"
        report += f"{'='*80}\n"

        return report


def main():
    """Demo Oracle Hero Trainer"""
    trainer = OracleHeroTrainer()

    # Analyze all heroes
    skills_data = trainer.analyze_and_update_all_heroes()

    # Generate reports for first 3 heroes
    print("\n\n📋 HERO REPORT CARDS")
    print("=" * 80)

    for hero_name in list(skills_data["heroes"].keys())[:3]:
        print(trainer.get_hero_report_card(hero_name))

    print(f"\n✅ Complete hero skills database saved to:")
    print(f"   {trainer.training_system.skills_db_path}")


if __name__ == "__main__":
    main()
