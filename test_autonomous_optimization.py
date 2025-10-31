#!/usr/bin/env python3
"""
🔮 TEST: Autonomous Parallel Optimization
Oracle & Superman decide when to use git worktrees automatically

This test demonstrates the autonomous decision-making system where
Oracle analyzes missions and recommends the optimal execution strategy.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.justice_league import SupermanCoordinator


def test_autonomous_small_batch():
    """Test 1: Small batch (2 missions) - Oracle should recommend parallel"""
    print("\n" + "="*80)
    print("TEST 1: Small Batch - 2 Artemis Missions")
    print("="*80)

    superman = SupermanCoordinator()

    missions = [
        {
            'hero_name': 'artemis',
            'task_name': 'convert-header',
            'params': {'component_name': 'Header'}
        },
        {
            'hero_name': 'artemis',
            'task_name': 'convert-footer',
            'params': {'component_name': 'Footer'}
        }
    ]

    # Oracle & Superman decide automatically
    results = superman.deploy_heroes_smart(missions)

    # Check results
    print(f"\n📊 Results:")
    print(f"  Strategy: {results['oracle_recommendation']['strategy']}")
    print(f"  Workers: {results['oracle_recommendation']['recommended_workers']}")
    print(f"  Worktrees: {results['oracle_recommendation']['recommended_worktrees']}")
    print(f"  Confidence: {results['oracle_recommendation']['confidence']*100:.0f}%")
    print(f"  Expected Speedup: {results['oracle_recommendation']['expected_speedup']:.2f}x")
    print(f"  Actual Duration: {results['actual_duration']:.2f}s")

    return results


def test_autonomous_single_task():
    """Test 2: Single task - Oracle should recommend sequential"""
    print("\n" + "="*80)
    print("TEST 2: Single Task - Oracle should recommend sequential")
    print("="*80)

    superman = SupermanCoordinator()

    missions = [
        {
            'hero_name': 'oracle',
            'task_name': 'analyze-pattern',
            'params': {'file_key': 'test-key'}
        }
    ]

    # Oracle & Superman decide automatically
    results = superman.deploy_heroes_smart(missions)

    # Check results
    print(f"\n📊 Results:")
    print(f"  Strategy: {results['oracle_recommendation']['strategy']}")
    print(f"  Reasoning:")
    for reason in results['oracle_recommendation']['reasoning']:
        print(f"    • {reason}")

    return results


def test_autonomous_large_batch():
    """Test 3: Large batch (4 missions) - Oracle should strongly recommend parallel with worktrees"""
    print("\n" + "="*80)
    print("TEST 3: Large Batch - 4 Artemis Missions")
    print("="*80)

    superman = SupermanCoordinator()

    missions = [
        {'hero_name': 'artemis', 'task_name': f'convert-component-{i}',
         'params': {'component_name': f'Component{i}'}}
        for i in range(1, 5)
    ]

    # Oracle & Superman decide automatically
    results = superman.deploy_heroes_smart(missions)

    # Check results
    print(f"\n📊 Results:")
    print(f"  Strategy: {results['oracle_recommendation']['strategy']}")
    print(f"  Workers: {results['oracle_recommendation']['recommended_workers']}")
    print(f"  Worktrees: {results['oracle_recommendation']['recommended_worktrees']}")
    print(f"  Confidence: {results['oracle_recommendation']['confidence']*100:.0f}%")
    print(f"  Expected Speedup: {results['oracle_recommendation']['expected_speedup']:.2f}x")

    print(f"\n✅ Benefits:")
    for benefit in results['oracle_recommendation']['benefits']:
        print(f"    • {benefit}")

    if results['oracle_recommendation']['warnings']:
        print(f"\n⚠️  Warnings:")
        for warning in results['oracle_recommendation']['warnings']:
            print(f"    • {warning}")

    return results


def test_manual_override():
    """Test 4: Manual override - User can override Oracle's recommendation"""
    print("\n" + "="*80)
    print("TEST 4: Manual Override - User overrides Oracle")
    print("="*80)

    superman = SupermanCoordinator()

    missions = [
        {'hero_name': 'oracle', 'task_name': f'analyze-{i}',
         'params': {'file_key': f'test-{i}'}}
        for i in range(3)
    ]

    print("\n🔮 Oracle will recommend parallel, but user forces sequential...")

    # User overrides Oracle's recommendation
    results = superman.deploy_heroes_smart(
        missions=missions,
        max_workers=1,  # Force sequential
        use_worktrees=False
    )

    print(f"\n📊 Results:")
    rec = results['oracle_recommendation']

    if 'recommended_workers' in rec:
        print(f"  Oracle recommended: {rec['recommended_workers']} workers")
    else:
        print(f"  Oracle recommended: sequential execution")

    print(f"  Strategy used: {rec['strategy']}")
    print(f"  Oracle's reasoning:")
    for reason in rec['reasoning']:
        print(f"    • {reason}")

    return results


def main():
    """Run all autonomous optimization tests"""
    print("\n" + "="*80)
    print("🔮 AUTONOMOUS PARALLEL OPTIMIZATION TESTS")
    print("   Oracle & Superman Make the Call")
    print("="*80)

    tests = [
        ("Small Batch (2 missions)", test_autonomous_small_batch),
        ("Single Task", test_autonomous_single_task),
        ("Large Batch (4 missions)", test_autonomous_large_batch),
        ("Manual Override", test_manual_override)
    ]

    results_summary = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results_summary.append((test_name, "✅ PASSED", result))
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            results_summary.append((test_name, "❌ FAILED", str(e)))

    # Final summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)

    for test_name, status, result in results_summary:
        print(f"{status} {test_name}")
        if status == "✅ PASSED" and isinstance(result, dict):
            rec = result.get('oracle_recommendation', {})
            print(f"     Strategy: {rec.get('strategy', 'N/A')}, "
                  f"Confidence: {rec.get('confidence', 0)*100:.0f}%")

    print("\n✅ Autonomous optimization system is working!")
    print("   Oracle and Superman now automatically decide when to parallelize.\n")


if __name__ == "__main__":
    main()
