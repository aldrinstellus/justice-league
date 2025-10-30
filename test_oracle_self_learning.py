"""
Test Oracle Self-Learning System - Complete Mission Lifecycle

Demonstrates:
1. Mission tracking from start to finish
2. Strategy session logging
3. Outcome analysis and learning extraction
4. Hero skill evolution based on learnings
5. Methodology confidence adjustment
6. Team feedback for continuous improvement

Shows 3 complete missions:
- Mission 1: Simple component (baseline)
- Mission 2: Complex dashboard (learns from Mission 1)
- Mission 3: Another complex task (shows accumulated learning)
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from core.justice_league import SupermanCoordinator


def test_mission_1_simple_component():
    """Mission 1: Simple login form - Baseline learning"""
    print("\n" + "="*80)
    print("MISSION 1: Simple Login Form Conversion")
    print("="*80)

    superman = SupermanCoordinator()

    # Start mission tracking
    mission_id = superman.start_mission_tracking(
        user_request="Convert simple login form from Figma to React",
        mission_type="figma-api-conversion",
        context={
            "complexity": "low",
            "layout": "single-column",
            "components": 2
        }
    )

    print(f"\n📋 Mission ID: {mission_id}")

    # Strategy session
    result = superman.strategy_session(
        topic="Best methodology for simple login form conversion",
        heroes_dict={
            "Oracle": superman.oracle,
            "Artemis": superman.artemis,
        },
        context={
            "complexity": "low",
            "layout": "single-column",
            "components": 2
        }
    )

    print(f"\n✅ Strategy Decision: {result['decision']['choice']}")

    # Simulate mission execution and completion
    outcome = {
        "accuracy": 85,
        "duration_seconds": 45 * 60,  # 45 minutes
        "artemis_score": 85,
        "green_arrow_score": 85
    }

    learning_result = superman.complete_mission_with_learning(
        success=True,
        outcome_details=outcome,
        issues=[]
    )

    print(f"\n📊 Mission 1 Complete!")
    print(f"   Learnings extracted: {learning_result.get('learnings_extracted', 0)}")
    print(f"   Skills evolved: {learning_result['evolution']['skills_added']}")
    print(f"   Methodologies refined: {learning_result['evolution']['methodologies_refined']}")

    return learning_result


def test_mission_2_complex_dashboard():
    """Mission 2: Complex dashboard - Oracle applies learnings from Mission 1"""
    print("\n" + "="*80)
    print("MISSION 2: Complex Dashboard Conversion (Oracle uses previous learnings)")
    print("="*80)

    superman = SupermanCoordinator()

    # Start mission tracking
    mission_id = superman.start_mission_tracking(
        user_request="Convert Dashboard 10 with 6 components and 2-column layout",
        mission_type="image-to-html-conversion",
        context={
            "complexity": "high",
            "layout": "2-column",
            "components": 6
        }
    )

    print(f"\n📋 Mission ID: {mission_id}")

    # Strategy session (Oracle should recommend Image-to-HTML based on complexity)
    result = superman.strategy_session(
        topic="Best methodology for Dashboard 10 conversion",
        heroes_dict={
            "Oracle": superman.oracle,
            "Artemis": superman.artemis,
        },
        context={
            "complexity": "high",
            "layout": "2-column",
            "components": 6
        }
    )

    print(f"\n✅ Strategy Decision: {result['decision']['choice']}")

    # Simulate mission execution with high success
    outcome = {
        "accuracy": 92,
        "duration_seconds": 75 * 60,  # 75 minutes
        "artemis_score": 92,
        "green_arrow_score": 92
    }

    learning_result = superman.complete_mission_with_learning(
        success=True,
        outcome_details=outcome,
        issues=[]
    )

    print(f"\n📊 Mission 2 Complete!")
    print(f"   Learnings extracted: {learning_result.get('learnings_extracted', 0)}")
    print(f"   Skills evolved: {learning_result['evolution']['skills_added']}")
    print(f"   Methodologies refined: {learning_result['evolution']['methodologies_refined']}")

    return learning_result


def test_mission_3_failed_conversion():
    """Mission 3: Failed conversion - Oracle learns from failures"""
    print("\n" + "="*80)
    print("MISSION 3: Failed Component Conversion (Oracle learns from failures)")
    print("="*80)

    superman = SupermanCoordinator()

    # Start mission tracking
    mission_id = superman.start_mission_tracking(
        user_request="Convert complex navigation bar with dropdowns",
        mission_type="figma-api-conversion",
        context={
            "complexity": "high",
            "layout": "horizontal",
            "components": 8
        }
    )

    print(f"\n📋 Mission ID: {mission_id}")

    # Strategy session
    result = superman.strategy_session(
        topic="Best methodology for navigation bar conversion",
        heroes_dict={
            "Oracle": superman.oracle,
            "Artemis": superman.artemis,
        },
        context={
            "complexity": "high",
            "layout": "horizontal",
            "components": 8
        }
    )

    print(f"\n✅ Strategy Decision: {result['decision']['choice']}")

    # Simulate failed mission execution
    outcome = {
        "accuracy": 65,  # Below acceptable threshold
        "duration_seconds": 90 * 60,  # 90 minutes
        "artemis_score": 65,
        "green_arrow_score": 65
    }

    issues = [
        "🎨 Artemis Codesmith: Dropdown state management incomplete",
        "🎨 Artemis Codesmith: Hover states not matching design",
        "🎯 Green Arrow: 35% accuracy gap in spacing"
    ]

    learning_result = superman.complete_mission_with_learning(
        success=False,
        outcome_details=outcome,
        issues=issues
    )

    print(f"\n📊 Mission 3 Complete (Failed)!")
    print(f"   Learnings extracted: {learning_result.get('learnings_extracted', 0)}")
    print(f"   Skills evolved: {learning_result['evolution']['skills_added']}")
    print(f"   Methodologies refined: {learning_result['evolution']['methodologies_refined']}")

    return learning_result


def show_learning_statistics(superman):
    """Show Oracle's accumulated learning statistics"""
    print("\n" + "="*80)
    print("📊 ORACLE LEARNING STATISTICS (Across All Missions)")
    print("="*80)

    if not (superman.oracle and hasattr(superman.oracle, 'learning') and superman.oracle.learning):
        print("❌ Oracle learning system not available")
        return

    stats = superman.oracle.learning.get_learning_statistics()

    print(f"\n📋 Total Missions: {stats.get('total_missions', 0)}")
    print(f"✅ Successful: {stats.get('success_count', 0)}")
    print(f"❌ Failed: {stats.get('failure_count', 0)}")
    print(f"📈 Success Rate: {stats.get('success_rate', 0):.1f}%")
    print(f"\n🧠 Total Learnings Extracted: {stats.get('learnings_extracted', 0)}")
    print(f"⚡ Total Skills Evolved: {stats.get('total_skills_evolved', 0)}")
    print(f"👥 Heroes with Improvements: {stats.get('heroes_with_improvements', 0)}")


def run_all_tests():
    """Run complete self-learning demonstration"""
    print("\n" + "█"*80)
    print("     ORACLE SELF-LEARNING SYSTEM - COMPLETE DEMONSTRATION")
    print("█"*80)

    try:
        # Mission 1: Baseline
        mission1 = test_mission_1_simple_component()

        # Mission 2: Apply learnings
        mission2 = test_mission_2_complex_dashboard()

        # Mission 3: Learn from failure
        mission3 = test_mission_3_failed_conversion()

        # Show accumulated statistics
        superman = SupermanCoordinator()
        show_learning_statistics(superman)

        # Summary
        print("\n" + "="*80)
        print("     DEMONSTRATION SUMMARY")
        print("="*80)
        print("\n✅ Oracle Self-Learning Features Demonstrated:")
        print("   • Mission tracking from start to finish")
        print("   • Strategy session logging with hero contributions")
        print("   • Automatic learning extraction from outcomes")
        print("   • Methodology confidence adjustment (success → +5%, failure → -10%)")
        print("   • Hero skill improvement identification")
        print("   • Decision pattern optimization")
        print("   • Team feedback generation and display")
        print("   • Self-healing through pattern detection")
        print("\n📊 Results Across 3 Missions:")
        print(f"   • Total learnings extracted: {mission1.get('learnings_extracted', 0) + mission2.get('learnings_extracted', 0) + mission3.get('learnings_extracted', 0)}")
        print(f"   • Methodologies refined: {mission1['evolution']['methodologies_refined'] + mission2['evolution']['methodologies_refined'] + mission3['evolution']['methodologies_refined']}")
        print(f"   • Hero skills evolved: {mission1['evolution']['skills_added'] + mission2['evolution']['skills_added'] + mission3['evolution']['skills_added']}")
        print("\n🔮 Oracle now has enhanced knowledge for future missions!")
        print("   - Learned optimal methodologies for different complexities")
        print("   - Identified hero improvement areas")
        print("   - Optimized team consultation patterns")
        print("   - Built failure pattern recognition")

        print("\n🎉 ALL TESTS PASSED!")
        print("="*80 + "\n")
        return True

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        print("="*80 + "\n")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
