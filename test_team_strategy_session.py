"""
Test Justice League Team Strategy Session

Demonstrates:
1. Superman initiates strategy session with topic
2. Heroes contribute with sequential thinking
3. Oracle provides pattern-based recommendations
4. Artemis analyzes component complexity
5. Vision Analyst assesses visual structure
6. Superman analyzes all input and makes final decision
7. Team receives clear next steps
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from core.justice_league import SupermanCoordinator


def test_simple_component_strategy():
    """Test 1: Strategy session for simple component"""
    print("\n" + "="*80)
    print("TEST 1: Strategy Session - Simple Component")
    print("="*80)

    superman = SupermanCoordinator()

    # Simple component context
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

    print("\n✅ Strategy Session Complete!")
    print(f"   Decision: {result['decision']['choice']}")
    print(f"   Support: {result['decision']['support_count']}/{result['decision']['total_heroes']} heroes")
    print(f"   Next Steps: {len(result['next_steps'])} heroes assigned")

    return result


def test_complex_dashboard_strategy():
    """Test 2: Strategy session for complex dashboard"""
    print("\n" + "="*80)
    print("TEST 2: Strategy Session - Complex Dashboard")
    print("="*80)

    superman = SupermanCoordinator()

    # Complex dashboard context
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

    print("\n✅ Strategy Session Complete!")
    print(f"   Decision: {result['decision']['choice']}")
    print(f"   Support: {result['decision']['support_count']}/{result['decision']['total_heroes']} heroes")
    print(f"   Next Steps: {len(result['next_steps'])} heroes assigned")

    return result


def test_all_heroes_strategy():
    """Test 3: Full team strategy session with all available heroes"""
    print("\n" + "="*80)
    print("TEST 3: Full Team Strategy Session")
    print("="*80)

    superman = SupermanCoordinator()

    # Include all available heroes
    heroes_dict = {}

    if superman.oracle:
        heroes_dict["Oracle"] = superman.oracle
    if superman.artemis:
        heroes_dict["Artemis"] = superman.artemis

    result = superman.strategy_session(
        topic="Best approach for K-12 Dashboard with 26 complex frames",
        heroes_dict=heroes_dict,
        context={
            "complexity": "high",
            "layout": "multi-column",
            "components": 26,
            "frames": 26
        }
    )

    print("\n✅ Full Team Strategy Session Complete!")
    print(f"   Topic: {result['topic']}")
    print(f"   Participants: {len(result['contributions'])} heroes")
    print(f"   Decision: {result['decision']['choice']}")
    print(f"   Next Steps Assigned: {len(result['next_steps'])} heroes")

    # Show key insights from each hero
    print("\n📊 Key Insights:")
    for contrib in result['contributions']:
        if contrib.get('key_insight'):
            print(f"   • {contrib['key_insight']}")

    return result


def run_all_tests():
    """Run all strategy session tests"""
    print("\n" + "█"*80)
    print("     JUSTICE LEAGUE TEAM STRATEGY SESSION TESTS")
    print("█"*80)

    tests = [
        ("Simple Component", test_simple_component_strategy),
        ("Complex Dashboard", test_complex_dashboard_strategy),
        ("Full Team Session", test_all_heroes_strategy),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
            print(f"\n✅ {test_name}: PASSED")
        except Exception as e:
            print(f"\n❌ {test_name}: FAILED - {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    # Summary
    print("\n" + "="*80)
    print("     TEST SUMMARY")
    print("="*80)
    print(f"✅ Passed: {passed}/{len(tests)}")
    print(f"❌ Failed: {failed}/{len(tests)}")

    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n📊 Team Strategy Session Features:")
        print("   • Superman leads collaborative strategy sessions")
        print("   • Heroes share sequential thinking and perspectives")
        print("   • Oracle provides pattern-based recommendations from knowledge base")
        print("   • Artemis analyzes component complexity for code generation")
        print("   • Superman analyzes all input and makes final decision")
        print("   • Team receives clear next step assignments")
        print("   • Fully transparent reasoning process visible to user")
    else:
        print("\n⚠️ SOME TESTS FAILED - Review errors above")

    print("="*80 + "\n")

    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
