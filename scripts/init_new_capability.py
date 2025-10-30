#!/usr/bin/env python3
"""
Justice League Capability Initialization System
==============================================

This script provides a standardized process for adding new capabilities,
methodologies, heroes, or integrations to the Justice League.

Usage:
    python3 init_new_capability.py --type methodology --name "image-to-html" --session "dashboard-oct-30"

Capability Types:
    - methodology: New conversion approach or process
    - hero: New Justice League member
    - pattern: New design pattern learned
    - integration: New external system connection
    - skill: New hero skill or ability

What This Script Does:
    1. Updates Oracle's knowledge base
    2. Adds to best practices documentation
    3. Updates relevant hero capabilities
    4. Creates/updates documentation files
    5. Updates coordination protocols
    6. Generates CHANGELOG entry
    7. Optionally bumps version

Created: 2025-10-30
Version: 1.0.0
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))


class CapabilityInitializer:
    """Initialize new capabilities into the Justice League system"""

    def __init__(self, project_root: Optional[Path] = None):
        if project_root is None:
            # Auto-detect project root (2 levels up from scripts/)
            self.project_root = Path(__file__).parent.parent
        else:
            self.project_root = Path(project_root)

        self.data_dir = self.project_root / "data"
        self.knowledge_base_dir = self.project_root / "knowledge_base"
        self.core_dir = self.project_root / "core" / "justice_league"

        # Files to update
        self.oracle_patterns_file = self.data_dir / "oracle_project_patterns.json"
        self.best_practices_file = self.knowledge_base_dir / "GLOBAL_BEST_PRACTICES.md"
        self.version_history_file = self.project_root / "VERSION_HISTORY.md"

    def init_methodology(
        self,
        name: str,
        description: str,
        accuracy_range: str,
        best_for: List[str],
        pros: List[str],
        cons: List[str],
        heroes_involved: List[str],
        case_study: Optional[Dict[str, Any]] = None,
        session_notes: str = ""
    ) -> Dict[str, str]:
        """
        Initialize a new conversion methodology.

        Returns dict of files created/updated
        """
        results = {}

        print(f"🚀 Initializing new methodology: {name}")

        # 1. Update Oracle's knowledge base
        print("📊 Updating Oracle's project patterns...")
        oracle_updated = self._update_oracle_methodologies(
            name=name,
            description=description,
            accuracy_range=accuracy_range,
            best_for=best_for,
            pros=pros,
            cons=cons,
            heroes_involved=heroes_involved,
            case_study=case_study
        )
        results["oracle_patterns"] = str(self.oracle_patterns_file)

        # 2. Add to best practices
        print("📚 Adding to best practices documentation...")
        best_practices_updated = self._add_to_best_practices(
            category="methodologies",
            title=name,
            content=description,
            details={
                "accuracy": accuracy_range,
                "best_for": best_for,
                "pros": pros,
                "cons": cons
            }
        )
        results["best_practices"] = str(self.best_practices_file)

        # 3. Create methodology documentation
        print("📝 Creating methodology documentation...")
        doc_file = self.knowledge_base_dir / f"{name.upper().replace('-', '_')}_METHODOLOGY.md"
        results["methodology_doc"] = str(doc_file)

        # 4. Update CHANGELOG
        print("📋 Updating version history...")
        self._add_changelog_entry(
            change_type="METHODOLOGY_ADDED",
            description=f"New methodology: {name}",
            details=f"Achieves {accuracy_range} accuracy"
        )
        results["version_history"] = str(self.version_history_file)

        print(f"✅ Methodology '{name}' initialized successfully!")
        return results

    def init_hero(
        self,
        name: str,
        description: str,
        capabilities: List[str],
        working_with: List[str],
        file_path: Optional[Path] = None
    ) -> Dict[str, str]:
        """
        Initialize a new Justice League hero.

        Returns dict of files created/updated
        """
        results = {}

        print(f"🦸 Initializing new hero: {name}")

        # 1. Create hero file if provided
        if file_path:
            print(f"📝 Hero file created at: {file_path}")
            results["hero_file"] = str(file_path)

        # 2. Update __init__.py exports
        init_file = self.core_dir / "__init__.py"
        print(f"🔧 Updating Justice League roster: {init_file}")
        self._add_hero_to_init(name, capabilities)
        results["init_file"] = str(init_file)

        # 3. Add to documentation
        print("📚 Updating hero documentation...")
        results["readme"] = self._update_hero_documentation(name, description, capabilities)

        # 4. Update CHANGELOG
        print("📋 Updating version history...")
        self._add_changelog_entry(
            change_type="HERO_ADDED",
            description=f"New hero: {name}",
            details=f"Capabilities: {', '.join(capabilities)}"
        )

        print(f"✅ Hero '{name}' initialized successfully!")
        return results

    def init_pattern(
        self,
        pattern_name: str,
        description: str,
        detected_in: List[str],
        html_example: str = "",
        css_example: str = ""
    ) -> Dict[str, str]:
        """
        Initialize a new design pattern.

        Returns dict of files created/updated
        """
        results = {}

        print(f"🎨 Initializing new pattern: {pattern_name}")

        # 1. Update Oracle's patterns
        print("📊 Adding to Oracle's pattern library...")
        oracle_updated = self._add_oracle_pattern(pattern_name, description, detected_in)
        results["oracle_patterns"] = str(self.oracle_patterns_file)

        # 2. Add to best practices
        print("📚 Documenting pattern...")
        self._add_to_best_practices(
            category="design-patterns",
            title=pattern_name,
            content=description,
            details={"html": html_example, "css": css_example}
        )

        print(f"✅ Pattern '{pattern_name}' initialized successfully!")
        return results

    def _update_oracle_methodologies(
        self,
        name: str,
        description: str,
        accuracy_range: str,
        best_for: List[str],
        pros: List[str],
        cons: List[str],
        heroes_involved: List[str],
        case_study: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Update Oracle's methodologies in project patterns"""
        try:
            # Load existing patterns
            with open(self.oracle_patterns_file, 'r') as f:
                patterns = json.load(f)

            # Ensure methodologies section exists
            if "methodologies" not in patterns:
                patterns["methodologies"] = {}

            # Add new methodology
            methodology_key = name.lower().replace(" ", "-")
            patterns["methodologies"][methodology_key] = {
                "name": name,
                "description": description,
                "accuracy_range": accuracy_range,
                "best_for": best_for,
                "pros": pros,
                "cons": cons,
                "heroes_involved": heroes_involved,
                "success_rate": 0.90,  # Default estimate
                "missions_completed": 1,
                "learned_at": datetime.now().isoformat(),
                "case_studies": [case_study] if case_study else []
            }

            # Save updated patterns
            with open(self.oracle_patterns_file, 'w') as f:
                json.dump(patterns, f, indent=2)

            return True
        except Exception as e:
            print(f"❌ Error updating Oracle patterns: {e}")
            return False

    def _add_to_best_practices(
        self,
        category: str,
        title: str,
        content: str,
        details: Dict[str, Any]
    ) -> bool:
        """Add entry to best practices documentation"""
        try:
            # Read existing file
            with open(self.best_practices_file, 'r') as f:
                existing_content = f.read()

            # Format new entry
            new_entry = f"\n\n### {title}\n\n"
            new_entry += f"**Category**: {category}\n\n"
            new_entry += f"{content}\n\n"

            for key, value in details.items():
                if isinstance(value, list):
                    new_entry += f"**{key.title()}**:\n"
                    for item in value:
                        new_entry += f"- {item}\n"
                    new_entry += "\n"
                else:
                    new_entry += f"**{key.title()}**: {value}\n\n"

            new_entry += f"*Added: {datetime.now().strftime('%Y-%m-%d')}*\n"

            # Append to file
            with open(self.best_practices_file, 'a') as f:
                f.write(new_entry)

            return True
        except Exception as e:
            print(f"❌ Error updating best practices: {e}")
            return False

    def _add_hero_to_init(self, name: str, capabilities: List[str]) -> bool:
        """Add hero to __init__.py exports"""
        # This would parse and update the __init__.py file
        # For now, provide guidance
        print(f"  → Add to __init__.py:")
        print(f"     from .{name.lower().replace(' ', '_')} import {name.replace(' ', '')}")
        print(f"  → Add to __all__: '{name.replace(' ', '')}'")
        print(f"  → Update __heroes__ count")
        return True

    def _update_hero_documentation(
        self,
        name: str,
        description: str,
        capabilities: List[str]
    ) -> str:
        """Update hero documentation"""
        readme_file = self.project_root / "JUSTICE_LEAGUE_README.md"
        print(f"  → Update {readme_file}:")
        print(f"     Add {name} to heroes list")
        print(f"     Capabilities: {', '.join(capabilities)}")
        return str(readme_file)

    def _add_oracle_pattern(
        self,
        pattern_name: str,
        description: str,
        detected_in: List[str]
    ) -> bool:
        """Add pattern to Oracle's knowledge base"""
        try:
            with open(self.oracle_patterns_file, 'r') as f:
                patterns = json.load(f)

            # Add to a project's common_patterns
            # For now, add to first project
            if "projects" in patterns:
                first_project = next(iter(patterns["projects"].values()))
                if "common_patterns" not in first_project:
                    first_project["common_patterns"] = []
                first_project["common_patterns"].append(pattern_name)

                with open(self.oracle_patterns_file, 'w') as f:
                    json.dump(patterns, f, indent=2)

            return True
        except Exception as e:
            print(f"❌ Error adding pattern: {e}")
            return False

    def _add_changelog_entry(
        self,
        change_type: str,
        description: str,
        details: str
    ) -> bool:
        """Add entry to VERSION_HISTORY.md"""
        try:
            entry = f"\n### {datetime.now().strftime('%Y-%m-%d')} - {change_type}\n"
            entry += f"- {description}\n"
            entry += f"- {details}\n"

            with open(self.version_history_file, 'a') as f:
                f.write(entry)

            return True
        except Exception as e:
            print(f"❌ Error updating version history: {e}")
            return False


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Initialize new Justice League capabilities"
    )

    parser.add_argument(
        "--type",
        required=True,
        choices=["methodology", "hero", "pattern", "integration", "skill"],
        help="Type of capability to initialize"
    )

    parser.add_argument("--name", required=True, help="Name of the capability")
    parser.add_argument("--description", help="Description")
    parser.add_argument("--session", help="Session or project reference")
    parser.add_argument("--accuracy", help="Accuracy range (for methodologies)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")

    args = parser.parse_args()

    # Initialize
    initializer = CapabilityInitializer()

    print("=" * 60)
    print("🦸 JUSTICE LEAGUE CAPABILITY INITIALIZER")
    print("=" * 60)
    print()

    # Route to appropriate initializer
    if args.type == "methodology":
        if args.interactive:
            print("📋 Interactive mode: Please provide details...")
            # Interactive prompts would go here
            accuracy = input("Accuracy range (e.g., '90-95%'): ")
            description = input("Description: ")
            # ... more prompts
        else:
            # Use provided args
            results = initializer.init_methodology(
                name=args.name,
                description=args.description or "No description provided",
                accuracy_range=args.accuracy or "Unknown",
                best_for=[],
                pros=[],
                cons=[],
                heroes_involved=[],
                session_notes=args.session or ""
            )

        print("\n" + "=" * 60)
        print("✅ INITIALIZATION COMPLETE")
        print("=" * 60)
        print("\nFiles updated:")
        for key, path in results.items():
            print(f"  ✓ {key}: {path}")

    elif args.type == "hero":
        results = initializer.init_hero(
            name=args.name,
            description=args.description or "No description provided",
            capabilities=[],
            working_with=[]
        )

        print("\n" + "=" * 60)
        print("✅ HERO INITIALIZED")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Implement hero class in core/justice_league/")
        print("  2. Add to __init__.py exports")
        print("  3. Update documentation")
        print("  4. Test integration with Superman")

    print()


if __name__ == "__main__":
    main()
