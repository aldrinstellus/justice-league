#!/usr/bin/env python3
"""
Justice League Hero Skills Updater
Updates hero skill markdown files with session learnings

This script is called by extract-learnings.py to propagate learnings
to relevant hero skill files in ~/.claude/skills/
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any


class HeroSkillsUpdater:
    """Updates hero skill files with new learnings."""

    def __init__(self):
        self.home = Path.home()
        self.skills_dir = self.home / ".claude" / "skills"
        self.knowledge_dir = self.home / ".claude" / "knowledge-base"

        # Hero file mapping (hero_name -> skill_file_name)
        self.hero_files = {
            "oracle": "oracle.md",
            "superman": "superman.md",
            "green_arrow": "green-arrow.md",
            "batman": "batman.md",
            "artemis": "artemis.md",
            "flash": "flash.md",
            "wonder_woman": "wonder-woman.md",
            "aquaman": "aquaman.md",
            "cyborg": "cyborg.md",
            "hawkman": "hawkman.md",
            "martian_manhunter": "martian-manhunter.md",
            "green_lantern": "green-lantern.md",
            "atom": "atom.md",
            "architect": "architect.md",
            "quicksilver": "quicksilver.md",
            "plastic_man": "plastic-man.md",
            "zatanna": "zatanna.md",
            "litty": "litty.md",
            "aldrin": "aldrin.md",
            "product_manager": "product-manager.md",
            "vision_analyst": "vision-analyst.md",
        }

    def get_skill_file(self, hero_name: str) -> Path | None:
        """Get the path to a hero's skill file."""
        # Try direct mapping first
        if hero_name in self.hero_files:
            skill_file = self.skills_dir / self.hero_files[hero_name]
            if skill_file.exists():
                return skill_file

        # Try variations
        variations = [
            f"{hero_name}.md",
            f"{hero_name.replace('_', '-')}.md",
            f"{hero_name.replace('-', '_')}.md",
        ]

        for variant in variations:
            skill_file = self.skills_dir / variant
            if skill_file.exists():
                return skill_file

        return None

    def format_learnings_section(self, date: str, learnings: list) -> str:
        """Format learnings into markdown section."""
        section = f"\n### {date}\n"

        for learning in learnings:
            learning_type = learning.get("type", "skill")
            name = learning.get("name", "Unknown")
            description = learning.get("description", "")

            if learning_type == "error":
                section += f"- **Error Pattern**: {name}\n"
                section += f"  - Fix: {description}\n"
            elif learning_type == "practice":
                section += f"- **Best Practice**: {name}\n"
                section += f"  - {description}\n"
            else:  # skill
                section += f"- **New Skill**: {name}\n"
                section += f"  - {description}\n"

        return section

    def update_hero_skill(self, hero_name: str, learnings: list, date: str) -> bool:
        """Update a hero's skill file with new learnings."""
        skill_file = self.get_skill_file(hero_name)

        if not skill_file:
            print(f"   Skill file not found for hero: {hero_name}")
            return False

        # Read existing content
        content = skill_file.read_text()

        # Check if already has session learnings section
        session_header = "## Session Learnings (Auto-Updated)"
        if session_header not in content:
            content += f"\n\n{session_header}\n"

        # Format and add new learnings
        learnings_section = self.format_learnings_section(date, learnings)

        # Append to file
        with open(skill_file, 'a') as f:
            f.write(learnings_section)

        print(f"   Updated: {skill_file}")
        return True

    def update_all_heroes(self, learnings_data: dict, date: str) -> dict:
        """Update all relevant hero skill files with learnings."""
        results = {
            "updated": [],
            "skipped": [],
            "errors": []
        }

        # Group learnings by hero
        hero_learnings: dict[str, list] = {}

        # Process error patterns
        for error in learnings_data.get("errors", []):
            hero = error.get("hero_responsible", "green_arrow")
            if hero not in hero_learnings:
                hero_learnings[hero] = []
            hero_learnings[hero].append({
                "type": "error",
                "name": error.get("error_signature", "Unknown"),
                "description": error.get("fix_pattern", "")
            })

        # Process skills
        for skill in learnings_data.get("skills", []):
            for hero in skill.get("applicable_heroes", []):
                if hero not in hero_learnings:
                    hero_learnings[hero] = []
                hero_learnings[hero].append({
                    "type": "skill",
                    "name": skill.get("skill_name", "Unknown"),
                    "description": skill.get("description", "")
                })

        # Process best practices (assign to oracle by default)
        for practice in learnings_data.get("practices", []):
            hero = "oracle"
            if hero not in hero_learnings:
                hero_learnings[hero] = []
            hero_learnings[hero].append({
                "type": "practice",
                "name": practice.get("practice_name", "Unknown"),
                "description": practice.get("description", "")
            })

        # Update each hero's skill file
        for hero_name, learnings in hero_learnings.items():
            try:
                if self.update_hero_skill(hero_name, learnings, date):
                    results["updated"].append(hero_name)
                else:
                    results["skipped"].append(hero_name)
            except Exception as e:
                results["errors"].append(f"{hero_name}: {str(e)}")

        return results

    def load_learnings_from_json(self, filepath: Path) -> dict:
        """Load learnings from a JSON file."""
        if filepath.exists():
            with open(filepath, 'r') as f:
                return json.load(f)
        return {}


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Update hero skill files with learnings"
    )
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Date for the learnings (YYYY-MM-DD format)"
    )
    parser.add_argument(
        "--learnings-file",
        type=str,
        default=None,
        help="Path to JSON file with learnings data"
    )

    args = parser.parse_args()

    updater = HeroSkillsUpdater()

    # Load learnings
    if args.learnings_file:
        learnings = updater.load_learnings_from_json(Path(args.learnings_file))
    else:
        # Load from knowledge base
        knowledge_dir = Path.home() / ".claude" / "knowledge-base"
        learnings = {
            "errors": updater.load_learnings_from_json(
                knowledge_dir / "errors_solutions.json"
            ).get("patterns", []),
            "skills": updater.load_learnings_from_json(
                knowledge_dir / "patterns.json"
            ).get("skills", []),
            "practices": updater.load_learnings_from_json(
                knowledge_dir / "best_practices.json"
            ).get("practices", [])
        }

    # Update all heroes
    print("Updating hero skill files...")
    results = updater.update_all_heroes(learnings, args.date)

    print(f"\nResults:")
    print(f"  Updated: {', '.join(results['updated']) or 'None'}")
    print(f"  Skipped: {', '.join(results['skipped']) or 'None'}")
    if results['errors']:
        print(f"  Errors: {', '.join(results['errors'])}")


if __name__ == "__main__":
    main()
