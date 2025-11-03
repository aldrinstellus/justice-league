#!/usr/bin/env python3
"""
🦸 Justice League Hero Count Validator
Ensures hero count is consistent across all documentation files
"""

import os
import sys
import re
from pathlib import Path

def count_heroes_in_skills_dir() -> int:
    """Count actual skill files (excluding README.md)."""
    base_path = Path(__file__).parent.parent
    skills_dir = base_path / ".claude" / "skills"

    if not skills_dir.exists():
        return 0

    skill_files = [f for f in skills_dir.glob("*.md") if f.name != "README.md"]
    return len(skill_files)


def check_file_for_hero_count(file_path: Path, expected_count: int) -> tuple[bool, list[str]]:
    """
    Check a file for hero count references.

    Returns:
        (is_consistent, errors)
    """
    if not file_path.exists():
        return (True, [])  # Skip missing files

    errors = []

    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Patterns to check
        patterns = [
            (r'(\d+)\s+heroes', 'X heroes'),
            (r'(\d+)\s+specialized\s+heroes', 'X specialized heroes'),
            (r'(\d+)\s+hero', 'X hero'),
            (r'consists\s+of\s+(\d+)', 'consists of X'),
            (r'all\s+(\d+)', 'all X'),
        ]

        for pattern, description in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                count = int(match)
                if count != expected_count and count in range(10, 20):  # Only check numbers in reasonable range
                    errors.append(f"Found '{description}' with count {count}, expected {expected_count}")

        return (len(errors) == 0, errors)

    except Exception as e:
        return (False, [f"Error reading file: {str(e)}"])


def main():
    """Main validation function."""
    print("🦸 Validating Justice League Hero Count Consistency\n")

    # Count actual heroes
    actual_count = count_heroes_in_skills_dir()
    print(f"📊 Actual hero count (from skill files): {actual_count}\n")

    if actual_count == 0:
        print("❌ No skill files found!")
        return 1

    # Files to check
    base_path = Path(__file__).parent.parent
    files_to_check = [
        base_path / ".claude" / "skills" / "README.md",
        base_path / "CLAUDE.md",
        base_path / "justice-league-heroes.md",
        base_path / "AGENT_WORKFLOW_GUIDE.md",
        base_path / "knowledge_base" / "README.md",
    ]

    all_consistent = True
    for file_path in files_to_check:
        if not file_path.exists():
            print(f"⚠️  Skipping missing file: {file_path.name}")
            continue

        print(f"Checking: {file_path.name}...")
        is_consistent, errors = check_file_for_hero_count(file_path, actual_count)

        if is_consistent:
            print(f"  ✅ Consistent (expected {actual_count} heroes)\n")
        else:
            print(f"  ❌ Inconsistent:")
            for error in errors:
                print(f"     • {error}")
            print()
            all_consistent = False

    if all_consistent:
        print(f"✅ All files have consistent hero count: {actual_count}")
        return 0
    else:
        print(f"❌ Some files have inconsistent hero counts (expected {actual_count})")
        return 1


if __name__ == '__main__':
    sys.exit(main())
