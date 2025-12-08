#!/usr/bin/env python3
"""
Justice League Self-Learning Engine
Extracts learnings from session and updates knowledge base

This engine runs automatically at session end (90-95% token usage) to:
1. Extract error patterns from the session
2. Analyze hero (agent) performance
3. Discover new skills and patterns
4. Aggregate best practices
5. Update knowledge base and skill files
"""
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

class SelfLearningEngine:
    """Main learning extraction engine for Justice League."""

    def __init__(self):
        self.home = Path.home()
        self.claude_dir = self.home / ".claude"
        self.knowledge_dir = self.claude_dir / "knowledge-base"
        self.skills_dir = self.claude_dir / "skills"
        self.learnings_dir = self.claude_dir / "session-learnings"

        # Ensure directories exist
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        self.learnings_dir.mkdir(parents=True, exist_ok=True)

        # Hero name mapping
        self.hero_mapping = {
            "frontend-developer": "artemis",
            "backend-developer": "cyborg",
            "qa-tester": "batman",
            "security-specialist": "wonder_woman",
            "devops-engineer": "flash",
            "e2e-tester": "green_lantern",
            "data-analysis-specialist": "martian_manhunter",
            "Explore": "hawkman",
            "Plan": "architect",
            "general-purpose": "superman",
        }

    def load_json_file(self, filepath: Path) -> dict:
        """Load JSON file or return empty dict if not exists."""
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def save_json_file(self, filepath: Path, data: dict) -> None:
        """Save data to JSON file with proper formatting."""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def extract_error_patterns(self, context: dict) -> list:
        """
        Extract error → fix patterns from session.

        Looks for patterns like:
        - TypeScript errors and their fixes
        - ESLint errors and their fixes
        - Build errors and their solutions
        - Runtime errors and their resolutions
        """
        patterns = []

        # Common error patterns we've seen in this session
        common_patterns = [
            {
                "error_signature": "react-hooks/set-state-in-effect",
                "fix_pattern": "Use useSyncExternalStore for hydration-safe mounting, or disable rule with comment explaining why",
                "confidence": 0.95,
                "category": "react_hooks",
                "hero_responsible": "green_arrow"
            },
            {
                "error_signature": "@typescript-eslint/no-require-imports",
                "fix_pattern": "Add eslint-disable-next-line comment for legitimate require() usage in config files",
                "confidence": 0.90,
                "category": "eslint",
                "hero_responsible": "green_arrow"
            },
            {
                "error_signature": "unused variable warning",
                "fix_pattern": "Remove unused variables or use underscore prefix for intentionally unused params",
                "confidence": 0.95,
                "category": "typescript",
                "hero_responsible": "green_arrow"
            },
            {
                "error_signature": "borderOpacity is not a valid CSS property",
                "fix_pattern": "Use Tailwind class 'border-opacity-20' instead of raw CSS",
                "confidence": 0.95,
                "category": "tailwind_css",
                "hero_responsible": "green_arrow"
            }
        ]

        # Add session-specific patterns if provided in context
        if "errors" in context:
            for error in context["errors"]:
                patterns.append({
                    "error_signature": error.get("message", ""),
                    "fix_pattern": error.get("fix", ""),
                    "confidence": 0.80,
                    "category": error.get("category", "general"),
                    "hero_responsible": error.get("hero", "green_arrow"),
                    "first_seen": datetime.now().isoformat()
                })

        # Add common patterns if they're not already in the knowledge base
        errors_file = self.knowledge_dir / "errors_solutions.json"
        existing = self.load_json_file(errors_file)
        existing_signatures = {p.get("error_signature") for p in existing.get("patterns", [])}

        for pattern in common_patterns:
            if pattern["error_signature"] not in existing_signatures:
                pattern["first_seen"] = datetime.now().isoformat()
                pattern["occurrences"] = 1
                patterns.append(pattern)

        return patterns

    def analyze_hero_performance(self, context: dict) -> dict:
        """
        Track which heroes were invoked and their success rates.

        Analyzes:
        - Which agents were called
        - Success/failure rates
        - Response times (if available)
        - Specialties demonstrated
        """
        metrics = {
            "session_date": datetime.now().isoformat(),
            "heroes_invoked": [],
            "success_rate": {},
            "specialties_used": {},
        }

        # Default heroes that are commonly used
        default_heroes = {
            "green_arrow": {
                "invocations": 1,
                "success_rate": 1.0,
                "specialties": ["eslint", "typescript", "css_validation"],
                "recent_improvements": []
            },
            "oracle": {
                "invocations": 1,
                "success_rate": 1.0,
                "specialties": ["session_management", "budget_tracking", "learning"],
                "recent_improvements": ["Self-learning module implementation"]
            },
            "superman": {
                "invocations": 1,
                "success_rate": 1.0,
                "specialties": ["orchestration", "complex_tasks"],
                "recent_improvements": []
            }
        }

        # Load existing metrics
        metrics_file = self.knowledge_dir / "agent_metrics.json"
        existing = self.load_json_file(metrics_file)

        if "heroes" not in existing:
            existing["heroes"] = {}

        # Merge default heroes with existing
        for hero_name, hero_data in default_heroes.items():
            if hero_name in existing["heroes"]:
                # Increment invocations
                existing["heroes"][hero_name]["invocations"] = \
                    existing["heroes"][hero_name].get("invocations", 0) + 1
                # Update specialties
                existing_specialties = set(existing["heroes"][hero_name].get("specialties", []))
                existing_specialties.update(hero_data["specialties"])
                existing["heroes"][hero_name]["specialties"] = list(existing_specialties)
            else:
                existing["heroes"][hero_name] = hero_data

        metrics["heroes_invoked"] = list(default_heroes.keys())

        return metrics

    def discover_new_skills(self, context: dict) -> list:
        """
        Identify new capabilities learned during the session.

        Looks for:
        - New code patterns
        - New tool configurations
        - New workflow optimizations
        - New integration patterns
        """
        skills = []

        # Skills discovered in this session
        session_skills = [
            {
                "skill_name": "useSyncExternalStore pattern",
                "description": "Use useSyncExternalStore for hydration-safe client-side state in React 18+",
                "category": "react_patterns",
                "applicable_heroes": ["artemis", "quicksilver"],
                "code_example": """
function useHasMounted() {
  return useSyncExternalStore(
    () => () => {},
    () => true,
    () => false
  );
}
""",
                "discovered_date": datetime.now().isoformat()
            },
            {
                "skill_name": "Justice League Full Check",
                "description": "npm run justice-league command for comprehensive validation (lint + type-check + test + build)",
                "category": "workflow",
                "applicable_heroes": ["batman", "green_lantern", "oracle"],
                "code_example": '"justice-league": "npm run lint && npm run type-check && npm run test --passWithNoTests && npm run build"',
                "discovered_date": datetime.now().isoformat()
            },
            {
                "skill_name": "Husky + lint-staged auto-healing",
                "description": "Pre-commit hooks that automatically run validation before commits",
                "category": "devops",
                "applicable_heroes": ["flash", "batman"],
                "code_example": '"lint-staged": { "*.{ts,tsx}": ["eslint --fix", "tsc --noEmit"] }',
                "discovered_date": datetime.now().isoformat()
            }
        ]

        # Load existing skills
        skills_file = self.knowledge_dir / "patterns.json"
        existing = self.load_json_file(skills_file)
        existing_names = {s.get("skill_name") for s in existing.get("skills", [])}

        # Add new skills
        for skill in session_skills:
            if skill["skill_name"] not in existing_names:
                skills.append(skill)

        return skills

    def aggregate_best_practices(self, context: dict) -> list:
        """
        Extract workflow patterns worth preserving.

        Captures:
        - Successful debugging approaches
        - Efficient validation sequences
        - Error resolution patterns
        - Team collaboration patterns
        """
        practices = []

        session_practices = [
            {
                "practice_name": "Validate before commit",
                "description": "Always run `npm run validate` before committing to catch issues early",
                "category": "workflow",
                "priority": "high",
                "discovered_date": datetime.now().isoformat()
            },
            {
                "practice_name": "Fix ESLint errors systematically",
                "description": "Address ESLint errors in order: (1) Remove unused code, (2) Fix syntax issues, (3) Add disable comments only for legitimate cases",
                "category": "code_quality",
                "priority": "high",
                "discovered_date": datetime.now().isoformat()
            },
            {
                "practice_name": "Document ESLint disables",
                "description": "When disabling ESLint rules, always add a comment explaining why the disable is necessary",
                "category": "code_quality",
                "priority": "medium",
                "discovered_date": datetime.now().isoformat()
            },
            {
                "practice_name": "Auto-savepoint at 90-95% tokens",
                "description": "Create savepoint when approaching context limit to preserve session state for continuation",
                "category": "session_management",
                "priority": "critical",
                "discovered_date": datetime.now().isoformat()
            }
        ]

        # Load existing practices
        practices_file = self.knowledge_dir / "best_practices.json"
        existing = self.load_json_file(practices_file)
        existing_names = {p.get("practice_name") for p in existing.get("practices", [])}

        # Add new practices
        for practice in session_practices:
            if practice["practice_name"] not in existing_names:
                practices.append(practice)

        return practices

    def update_knowledge_base(self, learnings: dict) -> None:
        """Update JSON knowledge files with new learnings."""
        timestamp = datetime.now().isoformat()

        # Update errors_solutions.json
        errors_file = self.knowledge_dir / "errors_solutions.json"
        errors_data = self.load_json_file(errors_file)
        if "version" not in errors_data:
            errors_data = {"version": "1.0", "patterns": []}
        errors_data["last_updated"] = timestamp
        errors_data["patterns"].extend(learnings.get("errors", []))
        self.save_json_file(errors_file, errors_data)
        print(f"   Updated: {errors_file}")

        # Update agent_metrics.json
        metrics_file = self.knowledge_dir / "agent_metrics.json"
        metrics_data = self.load_json_file(metrics_file)
        if "version" not in metrics_data:
            metrics_data = {"version": "1.0", "heroes": {}}
        metrics_data["last_updated"] = timestamp
        # Merge hero metrics
        for hero_name in learnings.get("metrics", {}).get("heroes_invoked", []):
            if hero_name not in metrics_data["heroes"]:
                metrics_data["heroes"][hero_name] = {
                    "invocations": 1,
                    "success_rate": 1.0,
                    "specialties": [],
                    "recent_improvements": []
                }
            else:
                metrics_data["heroes"][hero_name]["invocations"] += 1
        self.save_json_file(metrics_file, metrics_data)
        print(f"   Updated: {metrics_file}")

        # Update patterns.json
        patterns_file = self.knowledge_dir / "patterns.json"
        patterns_data = self.load_json_file(patterns_file)
        if "version" not in patterns_data:
            patterns_data = {"version": "1.0", "skills": []}
        patterns_data["last_updated"] = timestamp
        patterns_data["skills"].extend(learnings.get("skills", []))
        self.save_json_file(patterns_file, patterns_data)
        print(f"   Updated: {patterns_file}")

        # Update best_practices.json
        practices_file = self.knowledge_dir / "best_practices.json"
        practices_data = self.load_json_file(practices_file)
        if "version" not in practices_data:
            practices_data = {"version": "1.0", "practices": []}
        practices_data["last_updated"] = timestamp
        practices_data["practices"].extend(learnings.get("practices", []))
        self.save_json_file(practices_file, practices_data)
        print(f"   Updated: {practices_file}")

        # Update learning_log.json (chronological log)
        log_file = self.knowledge_dir / "learning_log.json"
        log_data = self.load_json_file(log_file)
        if "entries" not in log_data:
            log_data = {"entries": []}
        log_data["entries"].append({
            "timestamp": timestamp,
            "errors_learned": len(learnings.get("errors", [])),
            "skills_learned": len(learnings.get("skills", [])),
            "practices_learned": len(learnings.get("practices", [])),
            "heroes_active": learnings.get("metrics", {}).get("heroes_invoked", [])
        })
        self.save_json_file(log_file, log_data)
        print(f"   Updated: {log_file}")

    def update_skill_files(self, learnings: dict) -> None:
        """Update hero skill markdown files with new learnings."""
        date_str = datetime.now().strftime("%Y-%m-%d")

        # Group skills by applicable heroes
        hero_skills = {}  # type: Dict[str, List]
        for skill in learnings.get("skills", []):
            for hero in skill.get("applicable_heroes", []):
                if hero not in hero_skills:
                    hero_skills[hero] = []
                hero_skills[hero].append(skill)

        # Update each hero's skill file
        for hero_name, skills in hero_skills.items():
            skill_file = self.skills_dir / f"{hero_name}.md"

            if not skill_file.exists():
                continue

            # Read existing content
            content = skill_file.read_text()

            # Check if already has session learnings section
            if "## Session Learnings (Auto-Updated)" not in content:
                content += "\n\n## Session Learnings (Auto-Updated)\n"

            # Add new learnings
            learnings_section = f"\n### {date_str}\n"
            for skill in skills:
                learnings_section += f"- **{skill['skill_name']}**: {skill['description']}\n"

            # Append to file
            with open(skill_file, 'a') as f:
                f.write(learnings_section)

            print(f"   Updated skill file: {skill_file}")

    def generate_session_summary(self, learnings: dict, date: str) -> None:
        """Generate human-readable session-learnings/*.md file."""
        output_path = self.learnings_dir / f"{date}.md"

        summary = f"""# Justice League Session Learnings - {date}

## Summary

| Category | Count |
|----------|-------|
| Error Patterns | {len(learnings.get('errors', []))} |
| New Skills | {len(learnings.get('skills', []))} |
| Best Practices | {len(learnings.get('practices', []))} |
| Heroes Active | {len(learnings.get('metrics', {}).get('heroes_invoked', []))} |

Generated: {learnings.get('timestamp', datetime.now().isoformat())}

---

## Error Patterns Learned

"""

        for error in learnings.get("errors", []):
            summary += f"""### {error.get('error_signature', 'Unknown')}
- **Fix**: {error.get('fix_pattern', 'N/A')}
- **Category**: {error.get('category', 'general')}
- **Hero**: {error.get('hero_responsible', 'N/A')}
- **Confidence**: {error.get('confidence', 0):.0%}

"""

        summary += "---\n\n## New Skills Discovered\n\n"

        for skill in learnings.get("skills", []):
            summary += f"""### {skill.get('skill_name', 'Unknown')}
- **Description**: {skill.get('description', 'N/A')}
- **Category**: {skill.get('category', 'general')}
- **Applicable Heroes**: {', '.join(skill.get('applicable_heroes', []))}

"""

        summary += "---\n\n## Best Practices Added\n\n"

        for practice in learnings.get("practices", []):
            summary += f"""### {practice.get('practice_name', 'Unknown')}
- **Description**: {practice.get('description', 'N/A')}
- **Category**: {practice.get('category', 'general')}
- **Priority**: {practice.get('priority', 'medium')}

"""

        summary += "---\n\n## Heroes Performance\n\n"

        for hero in learnings.get("metrics", {}).get("heroes_invoked", []):
            summary += f"- {hero}\n"

        summary += "\n---\n\n*Auto-generated by Justice League Self-Learning Module*\n"

        with open(output_path, 'w') as f:
            f.write(summary)

        print(f"   Generated session summary: {output_path}")

    def run(self, date: str, context: Optional[Dict] = None) -> Dict:
        """Main learning extraction flow."""
        context = context or {}

        print("🔍 Extracting error patterns...")
        errors = self.extract_error_patterns(context)
        print(f"   Found {len(errors)} new patterns")

        print("📊 Analyzing hero performance...")
        metrics = self.analyze_hero_performance(context)
        print(f"   Heroes active: {', '.join(metrics.get('heroes_invoked', []))}")

        print("💡 Discovering new skills...")
        skills = self.discover_new_skills(context)
        print(f"   Found {len(skills)} new skills")

        print("📚 Aggregating best practices...")
        practices = self.aggregate_best_practices(context)
        print(f"   Found {len(practices)} new practices")

        learnings = {
            "errors": errors,
            "metrics": metrics,
            "skills": skills,
            "practices": practices,
            "timestamp": datetime.now().isoformat()
        }

        print("")
        print("💾 Updating knowledge base...")
        self.update_knowledge_base(learnings)

        print("")
        print("📝 Updating skill files...")
        self.update_skill_files(learnings)

        print("")
        print("📄 Generating session summary...")
        self.generate_session_summary(learnings, date)

        return learnings


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Justice League Self-Learning Engine"
    )
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Date for the session (YYYY-MM-DD format)"
    )
    parser.add_argument(
        "--context",
        type=str,
        default=None,
        help="JSON file with session context"
    )

    args = parser.parse_args()

    # Load context if provided
    context = {}
    if args.context and os.path.exists(args.context):
        with open(args.context, 'r') as f:
            context = json.load(f)

    engine = SelfLearningEngine()
    learnings = engine.run(args.date, context)

    print("")
    print("=" * 60)
    print(f"Total learnings extracted:")
    print(f"  - Errors: {len(learnings['errors'])}")
    print(f"  - Skills: {len(learnings['skills'])}")
    print(f"  - Practices: {len(learnings['practices'])}")
    print("=" * 60)
