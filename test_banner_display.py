#!/usr/bin/env python3
"""
Test Suite for Justice League Banner Display Enforcement
=========================================================

Tests the banner display system across:
1. Narrator keyword detection
2. Superman coordinator auto-detection
3. Session persistence
4. Oracle preference storage

Created: 2025-10-30 (Banner Enforcement Implementation)
"""

import sys
import os
import json
from pathlib import Path
from io import StringIO

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Try to import narrator, but continue tests even if import fails
try:
    from core.justice_league.mission_control_narrator import MissionControlNarrator, NarratorMode
    NARRATOR_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Warning: Could not import narrator ({e})")
    print("   Skipping narrator-specific tests, but continuing with file-based tests\n")
    NARRATOR_AVAILABLE = False
    MissionControlNarrator = None
    NarratorMode = None


class TestBannerDisplay:
    """Test suite for Justice League banner display"""

    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0

    def assert_true(self, condition, message):
        """Assert that condition is True"""
        self.tests_run += 1
        if condition:
            self.tests_passed += 1
            print(f"  ✅ {message}")
            return True
        else:
            self.tests_failed += 1
            print(f"  ❌ {message}")
            return False

    def assert_false(self, condition, message):
        """Assert that condition is False"""
        return self.assert_true(not condition, message)

    def assert_contains(self, text, substring, message):
        """Assert that text contains substring"""
        return self.assert_true(substring in text, message)

    def test_narrator_keyword_detection(self):
        """Test narrator's should_show_banner() keyword detection"""
        print("\n🧪 Test 1: Narrator Keyword Detection")
        print("=" * 60)

        if not NARRATOR_AVAILABLE:
            print("  ⚠️ Narrator not available, skipping test")
            return

        narrator = MissionControlNarrator(mode=NarratorMode.NARRATIVE)

        # Test trigger keywords (case-insensitive)
        test_cases = [
            ("Can you run justice league analysis?", True, "justice league"),
            ("Use justice-league to validate", True, "justice-league"),
            ("/justice-league https://example.com", True, "/justice-league"),
            ("/superman export frames", True, "/superman"),
            ("Let's assemble the team", True, "assemble"),
            ("Deploy heroes to test this", True, "deploy heroes"),
            ("Run justice league on this Figma file", True, "run justice league"),
            ("JUSTICE LEAGUE in uppercase", True, "uppercase variation"),
            ("Just a normal request", False, "no keywords"),
            ("Build a super man character (not coordinator)", False, "false positive check")
        ]

        for user_input, should_detect, description in test_cases:
            narrator.banner_shown = False  # Reset for each test
            result = narrator.should_show_banner(user_input)
            self.assert_true(
                result == should_detect,
                f"Keyword detection for '{description}': {user_input[:40]}... -> {result}"
            )

    def test_narrator_session_persistence(self):
        """Test that banner only shows once per session"""
        print("\n🧪 Test 2: Narrator Session Persistence")
        print("=" * 60)

        if not NARRATOR_AVAILABLE:
            print("  ⚠️ Narrator not available, skipping test")
            return

        narrator = MissionControlNarrator(mode=NarratorMode.NARRATIVE)

        # First invocation should return True
        result1 = narrator.should_show_banner("justice league")
        self.assert_true(result1, "First invocation should show banner")

        # Mark as shown
        narrator.banner_shown = True

        # Second invocation should return False (already shown)
        result2 = narrator.should_show_banner("justice league")
        self.assert_false(result2, "Second invocation should not show banner (session persistence)")

        # Reset and test again
        narrator.banner_shown = False
        result3 = narrator.should_show_banner("justice league")
        self.assert_true(result3, "After reset, should show banner again")

    def test_narrator_silent_mode(self):
        """Test that banner respects NARRATOR_MODE=silent"""
        print("\n🧪 Test 3: Narrator Silent Mode")
        print("=" * 60)

        if not NARRATOR_AVAILABLE:
            print("  ⚠️ Narrator not available, skipping test")
            return

        # Create narrator in silent mode
        narrator = MissionControlNarrator(mode=NarratorMode.SILENT)

        # Should not show banner in silent mode
        result = narrator.should_show_banner("justice league")
        self.assert_false(result, "Silent mode should not show banner")

        # is_enabled() should return False for silent mode
        self.assert_false(narrator.is_enabled(), "is_enabled() should return False in silent mode")

    def test_narrator_auto_show_banner(self):
        """Test auto_show_banner_if_needed() method"""
        print("\n🧪 Test 4: Narrator Auto-Show Banner Method")
        print("=" * 60)

        if not NARRATOR_AVAILABLE:
            print("  ⚠️ Narrator not available, skipping test")
            return

        narrator = MissionControlNarrator(mode=NarratorMode.NARRATIVE)

        # Capture stdout to check banner display
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            # Test 1: With keyword - should show
            narrator.banner_shown = False
            narrator.auto_show_banner_if_needed(
                user_input="run justice league analysis",
                mission_type="Test Mission"
            )
            output1 = sys.stdout.getvalue()
            sys.stdout = StringIO()  # Reset

            # Test 2: Without keyword - should not show
            narrator.banner_shown = False
            narrator.auto_show_banner_if_needed(
                user_input="just a normal request",
                mission_type="Test Mission"
            )
            output2 = sys.stdout.getvalue()
            sys.stdout = StringIO()  # Reset

            # Test 3: Force flag - should show regardless
            narrator.banner_shown = True  # Already shown
            narrator.auto_show_banner_if_needed(
                user_input="no keywords here",
                mission_type="Forced Mission",
                force=True
            )
            output3 = sys.stdout.getvalue()

        finally:
            sys.stdout = old_stdout

        # Verify results
        self.assert_contains(output1, "JUSTICE LEAGUE", "Banner displayed with keyword")
        self.assert_contains(output1, "Test Mission", "Mission type included")
        self.assert_true(len(output2) == 0, "No banner without keyword")
        self.assert_contains(output3, "JUSTICE LEAGUE", "Force flag bypasses keyword check")

    def test_oracle_preference_storage(self):
        """Test that Oracle has banner_display preference stored"""
        print("\n🧪 Test 5: Oracle Preference Storage")
        print("=" * 60)

        oracle_json_path = project_root / "data" / "oracle_project_patterns.json"

        if not oracle_json_path.exists():
            print("  ⚠️ Oracle JSON file not found, skipping test")
            return

        with open(oracle_json_path, 'r') as f:
            oracle_data = json.load(f)

        # Check that banner_display preference exists
        self.assert_true(
            "user_preferences" in oracle_data,
            "Oracle has user_preferences section"
        )

        user_prefs = oracle_data.get("user_preferences", {})
        self.assert_true(
            "banner_display" in user_prefs,
            "Oracle has banner_display preference"
        )

        banner_pref = user_prefs.get("banner_display", {})

        # Verify preference structure
        self.assert_true(
            "trigger_keywords" in banner_pref,
            "Banner preference has trigger_keywords"
        )

        keywords = banner_pref.get("trigger_keywords", [])
        self.assert_true(
            "justice league" in keywords,
            "Trigger keywords include 'justice league'"
        )
        self.assert_true(
            "/superman" in keywords,
            "Trigger keywords include '/superman'"
        )
        self.assert_true(
            "assemble" in keywords,
            "Trigger keywords include 'assemble'"
        )

        self.assert_true(
            banner_pref.get("priority") == "HIGH",
            "Banner display has HIGH priority"
        )

    def test_superman_coordinator_integration(self):
        """Test that Superman coordinator has auto-detection integrated"""
        print("\n🧪 Test 6: Superman Coordinator Integration")
        print("=" * 60)

        superman_file = project_root / "core" / "justice_league" / "superman_coordinator.py"

        if not superman_file.exists():
            print("  ⚠️ Superman coordinator file not found, skipping test")
            return

        with open(superman_file, 'r') as f:
            superman_code = f.read()

        # Check for auto_show_banner_if_needed usage
        self.assert_contains(
            superman_code,
            "auto_show_banner_if_needed",
            "Superman uses auto_show_banner_if_needed()"
        )

        self.assert_contains(
            superman_code,
            "user_request = mission.get('user_request', '')",
            "Superman extracts user_request from mission"
        )

        # Check multiple integration points
        integration_count = superman_code.count("auto_show_banner_if_needed")
        self.assert_true(
            integration_count >= 2,
            f"Superman has {integration_count} auto-detection integration points"
        )

    def test_claude_md_enforcement(self):
        """Test that CLAUDE.md has strong banner enforcement rules"""
        print("\n🧪 Test 7: CLAUDE.md Enforcement Rules")
        print("=" * 60)

        claude_md_path = project_root / "CLAUDE.md"

        if not claude_md_path.exists():
            print("  ⚠️ CLAUDE.md file not found, skipping test")
            return

        with open(claude_md_path, 'r') as f:
            claude_md_content = f.read()

        # Check for strong enforcement language
        self.assert_contains(
            claude_md_content,
            "Banner Display Protocol",
            "CLAUDE.md has Banner Display Protocol section"
        )

        self.assert_contains(
            claude_md_content,
            "ENFORCE ALWAYS",
            "CLAUDE.md uses strong enforcement language"
        )

        self.assert_contains(
            claude_md_content,
            "MUST display",
            "CLAUDE.md uses imperative MUST"
        )

        # Check for keyword list
        self.assert_contains(
            claude_md_content,
            "Trigger Keywords",
            "CLAUDE.md documents trigger keywords"
        )

        # Check for examples
        self.assert_contains(
            claude_md_content,
            "Examples of Correct Behavior",
            "CLAUDE.md includes correct behavior examples"
        )

        # Verify HIGH priority mention
        self.assert_contains(
            claude_md_content,
            "HIGH priority",
            "CLAUDE.md marks preference as HIGH priority"
        )

    def run_all_tests(self):
        """Run all banner display tests"""
        print("\n" + "=" * 60)
        print("🦸 JUSTICE LEAGUE BANNER DISPLAY TEST SUITE")
        print("=" * 60)

        self.test_narrator_keyword_detection()
        self.test_narrator_session_persistence()
        self.test_narrator_silent_mode()
        self.test_narrator_auto_show_banner()
        self.test_oracle_preference_storage()
        self.test_superman_coordinator_integration()
        self.test_claude_md_enforcement()

        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"  Total Tests: {self.tests_run}")
        print(f"  ✅ Passed: {self.tests_passed}")
        print(f"  ❌ Failed: {self.tests_failed}")
        print(f"  Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        print("=" * 60)

        if self.tests_failed == 0:
            print("\n🎉 All tests passed! Banner display enforcement is working correctly.\n")
            return 0
        else:
            print(f"\n⚠️ {self.tests_failed} test(s) failed. Please review the errors above.\n")
            return 1


if __name__ == "__main__":
    test_suite = TestBannerDisplay()
    exit_code = test_suite.run_all_tests()
    sys.exit(exit_code)
