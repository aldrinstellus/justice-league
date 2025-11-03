#!/usr/bin/env python3
"""
🦸 Justice League Skill File Validator
Validates all skill files follow the correct structure and format
"""

import os
import sys
from pathlib import Path

def validate_skill_file(skill_path: Path) -> tuple[bool, list[str]]:
    """
    Validate a single skill file.

    Returns:
        (is_valid, errors)
    """
    errors = []

    try:
        with open(skill_path, 'r') as f:
            content = f.read()

        # Required sections
        required_sections = [
            "## Role",
            "## Catchphrase",
            "## Primary Function",
            "## Tools Available",
            "## Strengths",
            "## Weaknesses (OPTIMIZED TO ZERO)",
            "## Use Cases",
            "## Success Metrics",
            "## Special Abilities"
        ]

        for section in required_sections:
            if section not in content:
                errors.append(f"Missing required section: {section}")

        # Check for strengths (should have at least 5)
        # Count bullet points or subsections in Strengths section
        strengths_section = content.split("## Strengths")[1].split("## Weaknesses")[0] if "## Strengths" in content else ""
        # Try both formats: "### " (subsections) or "- **" (bullet points)
        strength_count = strengths_section.count("### ") + strengths_section.count("- **")

        if strength_count < 5:
            errors.append(f"Too few strengths: found {strength_count}, expected at least 5")

        # Check for eliminated weaknesses pattern (should have at least one)
        weaknesses_section = content.split("## Weaknesses")[1].split("## Use Cases")[0] if "## Weaknesses" in content and "## Use Cases" in content else ""
        has_elimination = "~~" in weaknesses_section and "**ELIMINATED**" in weaknesses_section

        if not has_elimination:
            errors.append("Weaknesses should show elimination pattern: ~~weakness~~ → **ELIMINATED**")

        # Check for grading table or metrics (lenient - either format acceptable)
        has_metrics = "| Score | Grade |" in content or "Justice League Score" in content or "Grade:" in content

        if not has_metrics:
            errors.append("Missing success metrics (grading table or score description)")

        return (len(errors) == 0, errors)

    except Exception as e:
        return (False, [f"Error reading file: {str(e)}"])


def main():
    """Main validation function."""
    print("🦸 Validating Justice League Skill Files\n")

    # Find skills directory
    base_path = Path(__file__).parent.parent
    skills_dir = base_path / ".claude" / "skills"

    if not skills_dir.exists():
        print(f"❌ Skills directory not found: {skills_dir}")
        return 1

    # Get all skill files (exclude README.md)
    skill_files = [f for f in skills_dir.glob("*.md") if f.name != "README.md"]

    if not skill_files:
        print(f"⚠️  No skill files found in {skills_dir}")
        return 1

    print(f"📁 Found {len(skill_files)} skill files\n")

    all_valid = True
    for skill_file in sorted(skill_files):
        print(f"Validating: {skill_file.name}...")
        is_valid, errors = validate_skill_file(skill_file)

        if is_valid:
            print(f"  ✅ Valid\n")
        else:
            print(f"  ❌ Invalid:")
            for error in errors:
                print(f"     • {error}")
            print()
            all_valid = False

    if all_valid:
        print("✅ All skill files are valid!")
        return 0
    else:
        print("❌ Some skill files have validation errors")
        return 1


if __name__ == '__main__':
    sys.exit(main())
