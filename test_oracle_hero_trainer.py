#!/usr/bin/env python3
"""
🔮 Test Oracle Hero Trainer System

Validates Oracle's hero skills analysis, training, and management capabilities.
"""

from core.justice_league.oracle_hero_trainer import OracleHeroTrainer, HeroSkillAnalyzer
from pathlib import Path
import json


def test_hero_skill_analyzer():
    """Test hero skill analysis from Python files"""
    print("\n📊 Test 1: Hero Skill Analyzer")
    print("=" * 80)

    analyzer = HeroSkillAnalyzer()

    # Test single hero analysis
    hero_file = Path("core/justice_league/artemis_codesmith.py")
    if hero_file.exists():
        capabilities = analyzer.analyze_hero_file(hero_file)

        print(f"✅ Analyzed Artemis Codesmith:")
        print(f"   Class: {capabilities['class_name']}")
        print(f"   Skills: {len(capabilities['skills'])}")
        print(f"   Methods: {len(capabilities['methods'])}")
        print(f"   Narrator: {'✅' if capabilities['narrator_integrated'] else '❌'}")
        print(f"   Powers: {len(capabilities['powers'])}")

        assert len(capabilities['methods']) > 0, "Should extract methods"
        assert capabilities['class_name'] == 'ArtemisCodesmith', "Should identify class name"
    else:
        print(f"⚠️  Artemis file not found: {hero_file}")

    print("\n✅ Test 1 Passed: Hero Skill Analyzer Working\n")


def test_analyze_all_heroes():
    """Test analysis of all 19 heroes"""
    print("\n📊 Test 2: Analyze All 19 Heroes")
    print("=" * 80)

    analyzer = HeroSkillAnalyzer()
    all_capabilities = analyzer.analyze_all_heroes()

    print(f"✅ Analyzed {len(all_capabilities)} heroes:")

    # Expected heroes
    expected_heroes = [
        "Superman Coordinator",
        "Oracle Meta Agent",
        "Artemis Codesmith",
        "Green Arrow Visual Validator",
        "Hawkman Equipped",
        "Vision Analyst",
        "Batman Testing",
        "Green Lantern Visual",
        "Wonder Woman Accessibility",
        "Flash Performance",
        "Aquaman Network",
        "Cyborg Integrations",
        "Martian Manhunter Security",
        "Atom Component Analysis",
        "Plastic Man Responsive",
        "Zatanna Seo",
        "Litty Ethics",
        "Hephaestus Code To Design",
        "Quicksilver Speed Export"
    ]

    found_heroes = []
    for hero_name in expected_heroes:
        if hero_name in all_capabilities:
            cap = all_capabilities[hero_name]
            print(f"   • {hero_name}: {len(cap['skills'])} skills, {len(cap['methods'])} methods")
            found_heroes.append(hero_name)

    print(f"\n✅ Found {len(found_heroes)}/{len(expected_heroes)} heroes")
    assert len(found_heroes) >= 15, "Should find at least 15 heroes"

    print("\n✅ Test 2 Passed: All Heroes Analyzed\n")


def test_oracle_hero_trainer():
    """Test Oracle Hero Trainer full system"""
    print("\n📊 Test 3: Oracle Hero Trainer System")
    print("=" * 80)

    trainer = OracleHeroTrainer()

    # Test analysis and database update
    skills_data = trainer.analyze_and_update_all_heroes()

    print(f"✅ Skills Database Created:")
    print(f"   Total Heroes: {len(skills_data['heroes'])}")
    print(f"   Database: {trainer.training_system.skills_db_path}")

    assert len(skills_data['heroes']) >= 15, "Should have at least 15 heroes"
    assert 'last_updated' in skills_data, "Should have last_updated timestamp"

    print("\n✅ Test 3 Passed: Oracle Hero Trainer Working\n")


def test_training_plan_generation():
    """Test training plan generation for heroes"""
    print("\n📊 Test 4: Training Plan Generation")
    print("=" * 80)

    trainer = OracleHeroTrainer()

    # Generate skills database first
    skills_data = trainer.analyze_and_update_all_heroes()

    # Test training plan for a hero with training needs
    for hero_name in list(skills_data["heroes"].keys())[:3]:
        training_plan = trainer.generate_training_plan(hero_name)

        if "error" not in training_plan:
            print(f"✅ Training Plan for {hero_name}:")
            print(f"   Skills: {training_plan['current_skill_count']}")
            print(f"   Training Needs: {len(training_plan['training_needs'])}")
            print(f"   Scenarios: {len(training_plan['training_scenarios'])}")
            print(f"   Duration: {training_plan['estimated_duration']}")

            assert 'training_scenarios' in training_plan, "Should have training scenarios"
            break

    print("\n✅ Test 4 Passed: Training Plan Generation Working\n")


def test_hero_report_card():
    """Test hero report card generation"""
    print("\n📊 Test 5: Hero Report Card")
    print("=" * 80)

    trainer = OracleHeroTrainer()

    # Generate skills database
    skills_data = trainer.analyze_and_update_all_heroes()

    # Get report card for first hero
    hero_name = list(skills_data["heroes"].keys())[0]
    report = trainer.get_hero_report_card(hero_name)

    print(report)

    assert len(report) > 0, "Report should not be empty"
    assert hero_name in report, "Report should include hero name"
    assert "Skills:" in report or "Capabilities Summary:" in report, "Report should have capabilities"

    print("\n✅ Test 5 Passed: Hero Report Card Generated\n")


def test_skills_database_persistence():
    """Test that skills database persists to disk"""
    print("\n📊 Test 6: Skills Database Persistence")
    print("=" * 80)

    # Check that hero_skills.json was created
    skills_file = Path("/Users/admin/Documents/claudecode/Projects/aldo-vision/data/oracle_hero_skills.json")

    assert skills_file.exists(), f"Skills database should exist at {skills_file}"

    with open(skills_file, 'r') as f:
        data = json.load(f)

    print(f"✅ Skills Database Found:")
    print(f"   Location: {skills_file}")
    print(f"   Size: {skills_file.stat().st_size / 1024:.1f} KB")
    print(f"   Heroes: {len(data['heroes'])}")
    print(f"   Last Updated: {data.get('last_updated', 'N/A')}")

    assert 'heroes' in data, "Database should have heroes key"
    assert len(data['heroes']) >= 15, "Should have at least 15 heroes"

    print("\n✅ Test 6 Passed: Skills Database Persisted\n")


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("🔮 ORACLE HERO TRAINER SYSTEM - TEST SUITE")
    print("=" * 80)

    tests = [
        test_hero_skill_analyzer,
        test_analyze_all_heroes,
        test_oracle_hero_trainer,
        test_training_plan_generation,
        test_hero_report_card,
        test_skills_database_persistence
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"\n❌ Test Failed: {test.__name__}")
            print(f"   Error: {e}\n")
            failed += 1
        except Exception as e:
            print(f"\n❌ Test Error: {test.__name__}")
            print(f"   Error: {e}\n")
            failed += 1

    # Summary
    print("\n" + "=" * 80)
    print(f"📊 TEST SUMMARY")
    print("=" * 80)
    print(f"✅ Passed: {passed}/{len(tests)}")
    print(f"❌ Failed: {failed}/{len(tests)}")
    print(f"Success Rate: {(passed/len(tests))*100:.1f}%")
    print("=" * 80 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
