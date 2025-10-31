#!/usr/bin/env python3
"""
Justice League Enhanced Capabilities Training & Validation
===========================================================

Tests and validates all enhanced capabilities after Oracle's self-improvement:
1. Proactive background task monitoring
2. Mission debate participation
3. Sequential thinking presentation
4. Evidence-based position advocacy
5. Cross-hero collaboration

Created: 2025-10-31
Version: 1.0.0
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add parent to path
sys.path.append(str(Path(__file__).parent))


class JusticeLeagueTrainingValidator:
    """Validate Justice League enhanced capabilities"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.data_dir = self.project_root / "data"

        # Load data
        self.capabilities = self._load_capabilities()
        self.patterns = self._load_patterns()

        print("🦸 Justice League Training Validator Initialized")

    def _load_capabilities(self) -> Dict[str, Any]:
        """Load hero capabilities"""
        try:
            with open(self.data_dir / "justice_league_hero_capabilities.json", 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Warning: Could not load capabilities: {e}")
            return {}

    def _load_patterns(self) -> Dict[str, Any]:
        """Load Oracle patterns"""
        try:
            with open(self.data_dir / "oracle_project_patterns.json", 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Warning: Could not load patterns: {e}")
            return {}

    def validate_proactive_monitoring(self) -> Dict[str, Any]:
        """Validate proactive monitoring capability"""
        print("\n📊 Validating Proactive Monitoring Capability")
        print("=" * 70)

        results = {
            "test_name": "Proactive Monitoring",
            "passed": 0,
            "failed": 0,
            "tests": []
        }

        # Test 1: Check methodology exists
        test = {"name": "Methodology exists in Oracle's knowledge base", "passed": False}
        if "methodologies" in self.patterns:
            if "proactive-background-task-monitoring" in self.patterns["methodologies"]:
                test["passed"] = True
                results["passed"] += 1
                print("   ✅ Proactive monitoring methodology found")
            else:
                results["failed"] += 1
                print("   ❌ Methodology not found")
        else:
            results["failed"] += 1
            print("   ❌ No methodologies section")
        results["tests"].append(test)

        # Test 2: Check user preference
        test = {"name": "User preference stored", "passed": False}
        if "user_preferences" in self.patterns:
            if "proactive_monitoring" in self.patterns["user_preferences"]:
                pref = self.patterns["user_preferences"]["proactive_monitoring"]
                if pref.get("priority") == "HIGH":
                    test["passed"] = True
                    results["passed"] += 1
                    print("   ✅ User preference stored (HIGH priority)")
                else:
                    results["failed"] += 1
                    print("   ❌ Priority not HIGH")
            else:
                results["failed"] += 1
                print("   ❌ Preference not found")
        else:
            results["failed"] += 1
            print("   ❌ No user_preferences section")
        results["tests"].append(test)

        # Test 3: Check heroes with proactive reporting
        test = {"name": "Heroes have proactive reporting capability", "passed": False}
        heroes_with_capability = []
        for hero_key, hero_data in self.capabilities.get("heroes", {}).items():
            if "Proactive progress reporting" in hero_data.get("primary_capabilities", []):
                heroes_with_capability.append(hero_data.get("name", hero_key))

        if len(heroes_with_capability) >= 4:  # Quicksilver, Hawkman, Artemis, Vision Analyst
            test["passed"] = True
            results["passed"] += 1
            print(f"   ✅ {len(heroes_with_capability)} heroes have proactive reporting")
            print(f"      Heroes: {', '.join(heroes_with_capability[:5])}")
        else:
            results["failed"] += 1
            print(f"   ❌ Only {len(heroes_with_capability)} heroes have capability")
        results["tests"].append(test)

        # Test 4: Check Oracle has self-improvement capability
        test = {"name": "Oracle has self-improvement capability", "passed": False}
        oracle = self.capabilities.get("heroes", {}).get("oracle", {})
        if "Self-improvement and learning cascade" in oracle.get("primary_capabilities", []):
            test["passed"] = True
            results["passed"] += 1
            print("   ✅ Oracle has self-improvement capability")
        else:
            results["failed"] += 1
            print("   ❌ Oracle missing self-improvement")
        results["tests"].append(test)

        return results

    def validate_mission_debates(self) -> Dict[str, Any]:
        """Validate mission debate capability"""
        print("\n📊 Validating Mission Debate Capability")
        print("=" * 70)

        results = {
            "test_name": "Mission Debates",
            "passed": 0,
            "failed": 0,
            "tests": []
        }

        # Test 1: Check debate preference
        test = {"name": "Mission debate preference exists", "passed": False}
        if "user_preferences" in self.patterns:
            if "always_debate_missions" in self.patterns["user_preferences"]:
                pref = self.patterns["user_preferences"]["always_debate_missions"]
                if pref.get("priority") == "HIGH":
                    test["passed"] = True
                    results["passed"] += 1
                    print("   ✅ Mission debate preference found (HIGH priority)")
                else:
                    results["failed"] += 1
                    print("   ❌ Priority not HIGH")
            else:
                results["failed"] += 1
                print("   ❌ Preference not found")
        else:
            results["failed"] += 1
            print("   ❌ No user_preferences section")
        results["tests"].append(test)

        # Test 2: Check heroes have debate capability
        test = {"name": "Heroes have debate participation capability", "passed": False}
        heroes_with_debate = []
        for hero_key, hero_data in self.capabilities.get("heroes", {}).items():
            if "Mission debate participation" in hero_data.get("primary_capabilities", []):
                heroes_with_debate.append(hero_data.get("name", hero_key))

        if len(heroes_with_debate) >= 18:  # All heroes
            test["passed"] = True
            results["passed"] += 1
            print(f"   ✅ {len(heroes_with_debate)}/18 heroes have debate capability")
        else:
            results["failed"] += 1
            print(f"   ❌ Only {len(heroes_with_debate)}/18 heroes have capability")
        results["tests"].append(test)

        # Test 3: Check debate protocol exists
        test = {"name": "Debate protocol configuration exists", "passed": False}
        if "debate_protocols" in self.capabilities:
            if "mission_assignment" in self.capabilities["debate_protocols"]:
                protocol = self.capabilities["debate_protocols"]["mission_assignment"]
                if protocol.get("enabled") == True:
                    test["passed"] = True
                    results["passed"] += 1
                    print("   ✅ Debate protocol enabled")
                else:
                    results["failed"] += 1
                    print("   ❌ Debate protocol not enabled")
            else:
                results["failed"] += 1
                print("   ❌ Mission assignment protocol not found")
        else:
            results["failed"] += 1
            print("   ❌ No debate_protocols section")
        results["tests"].append(test)

        return results

    def validate_cascade_completeness(self) -> Dict[str, Any]:
        """Validate all heroes received capability cascade"""
        print("\n📊 Validating Capability Cascade Completeness")
        print("=" * 70)

        results = {
            "test_name": "Cascade Completeness",
            "passed": 0,
            "failed": 0,
            "tests": []
        }

        heroes = self.capabilities.get("heroes", {})
        total_heroes = len(heroes)

        # Test 1: All heroes present
        test = {"name": "All 18 heroes present", "passed": False}
        if total_heroes == 18:
            test["passed"] = True
            results["passed"] += 1
            print(f"   ✅ All 18 heroes present in capability registry")
        else:
            results["failed"] += 1
            print(f"   ❌ Only {total_heroes}/18 heroes found")
        results["tests"].append(test)

        # Test 2: Check each hero has enhanced capabilities
        test = {"name": "Each hero has at least one enhanced capability", "passed": False}
        heroes_enhanced = 0
        for hero_key, hero_data in heroes.items():
            capabilities = hero_data.get("primary_capabilities", [])
            # Check if any enhanced capability present
            if any(cap in str(capabilities) for cap in [
                "Mission debate participation",
                "Proactive progress reporting",
                "Self-improvement"
            ]):
                heroes_enhanced += 1

        if heroes_enhanced == total_heroes:
            test["passed"] = True
            results["passed"] += 1
            print(f"   ✅ All {total_heroes} heroes have enhanced capabilities")
        else:
            results["failed"] += 1
            print(f"   ❌ Only {heroes_enhanced}/{total_heroes} heroes enhanced")
        results["tests"].append(test)

        # Test 3: Specific heroes have expected capabilities
        test = {"name": "Key heroes have expected specific capabilities", "passed": False}
        expected = {
            "quicksilver": "Proactive progress reporting",
            "hawkman": "Proactive progress reporting",
            "artemis": "Proactive progress reporting",
            "vision_analyst": "Proactive progress reporting",
            "oracle": "Self-improvement and learning cascade",
            "superman": "Mission debate participation"
        }

        all_correct = True
        for hero_key, expected_cap in expected.items():
            hero = heroes.get(hero_key, {})
            caps = hero.get("primary_capabilities", [])
            if expected_cap not in caps:
                all_correct = False
                print(f"   ❌ {hero.get('name', hero_key)} missing: {expected_cap}")

        if all_correct:
            test["passed"] = True
            results["passed"] += 1
            print(f"   ✅ All key heroes have expected capabilities")
        else:
            results["failed"] += 1
        results["tests"].append(test)

        return results

    def validate_sequential_thinking(self) -> Dict[str, Any]:
        """Validate sequential thinking guidelines"""
        print("\n📊 Validating Sequential Thinking Guidelines")
        print("=" * 70)

        results = {
            "test_name": "Sequential Thinking",
            "passed": 0,
            "failed": 0,
            "tests": []
        }

        # Test 1: Debate protocol has sequential thinking limits
        test = {"name": "Sequential thinking limits defined", "passed": False}
        if "debate_protocols" in self.capabilities:
            protocol = self.capabilities.get("debate_protocols", {}).get("mission_assignment", {})
            limits = protocol.get("sequential_thinking_limits", {})
            if limits.get("per_hero") and limits.get("superman_decision"):
                test["passed"] = True
                results["passed"] += 1
                print(f"   ✅ Limits defined: {limits['per_hero']} per hero")
            else:
                results["failed"] += 1
                print("   ❌ Limits not properly defined")
        else:
            results["failed"] += 1
            print("   ❌ No debate protocols")
        results["tests"].append(test)

        return results

    def run_all_validations(self) -> Dict[str, Any]:
        """Run all validation tests"""
        print("=" * 70)
        print("🦸 JUSTICE LEAGUE ENHANCED CAPABILITIES VALIDATION")
        print("=" * 70)
        print()
        print("Testing all capabilities after Oracle's self-improvement cascade...")
        print()

        all_results = {
            "total_tests": 0,
            "total_passed": 0,
            "total_failed": 0,
            "test_suites": []
        }

        # Run all validations
        validations = [
            self.validate_proactive_monitoring(),
            self.validate_mission_debates(),
            self.validate_cascade_completeness(),
            self.validate_sequential_thinking()
        ]

        for result in validations:
            all_results["test_suites"].append(result)
            all_results["total_tests"] += result["passed"] + result["failed"]
            all_results["total_passed"] += result["passed"]
            all_results["total_failed"] += result["failed"]

        # Summary
        print()
        print("=" * 70)
        print("📊 VALIDATION SUMMARY")
        print("=" * 70)
        print()

        for suite in all_results["test_suites"]:
            total = suite["passed"] + suite["failed"]
            success_rate = (suite["passed"] / total * 100) if total > 0 else 0
            status = "✅" if suite["failed"] == 0 else "⚠️"
            print(f"{status} {suite['test_name']}: {suite['passed']}/{total} passed ({success_rate:.0f}%)")

        print()
        print("=" * 70)
        overall_rate = (all_results["total_passed"] / all_results["total_tests"] * 100) if all_results["total_tests"] > 0 else 0

        if all_results["total_failed"] == 0:
            print("✅ ALL TESTS PASSED")
        else:
            print(f"⚠️ {all_results['total_failed']} TESTS FAILED")

        print(f"📊 Overall: {all_results['total_passed']}/{all_results['total_tests']} ({overall_rate:.0f}%)")
        print("=" * 70)
        print()

        if all_results["total_failed"] == 0:
            print("🎓 Justice League Training: COMPLETE")
            print("⚡ All heroes ready for enhanced operations")
            print("🔮 Oracle's self-improvement cascade: SUCCESSFUL")
        else:
            print("⚠️ Some capabilities need attention")
            print("🔧 Review failed tests above")

        print()

        return all_results


def main():
    """Main execution"""
    validator = JusticeLeagueTrainingValidator()
    results = validator.run_all_validations()

    # Exit with appropriate code
    sys.exit(0 if results["total_failed"] == 0 else 1)


if __name__ == "__main__":
    main()
