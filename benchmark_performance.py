#!/usr/bin/env python3
"""
⚡ PERFORMANCE BENCHMARK
Quick validation that autonomous optimization maintains/improves speed
"""

import sys
import time
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.justice_league import SupermanCoordinator


def benchmark_overhead():
    """Measure Oracle's decision overhead"""
    print("\n" + "="*80)
    print("BENCHMARK 1: Oracle Decision Overhead")
    print("="*80)

    superman = SupermanCoordinator()

    missions = [
        {'hero_name': 'artemis', 'task_name': f'benchmark-{i}', 'params': {}}
        for i in range(4)
    ]

    # Measure decision time
    start = time.time()
    from core.utils.parallel_optimizer import ParallelOptimizer
    optimizer = ParallelOptimizer()
    recommendation = optimizer.analyze_missions(missions)
    decision_time = time.time() - start

    print(f"\n📊 Decision Time: {decision_time*1000:.2f}ms")
    print(f"   Strategy: {recommendation.strategy.value}")
    print(f"   Workers: {recommendation.recommended_workers}")
    print(f"   Confidence: {recommendation.confidence*100:.0f}%")
    print(f"\n✅ Decision overhead: {decision_time*1000:.2f}ms")

    if decision_time < 0.1:
        print(f"   ✅ EXCELLENT - Negligible overhead (<100ms)")
    elif decision_time < 0.5:
        print(f"   ✅ GOOD - Low overhead (<500ms)")
    else:
        print(f"   ⚠️  Consider optimization - overhead >{decision_time*1000:.0f}ms")

    return decision_time


def benchmark_method_comparison():
    """Compare manual vs autonomous method speed"""
    print("\n" + "="*80)
    print("BENCHMARK 2: Method Call Speed Comparison")
    print("="*80)

    superman = SupermanCoordinator()

    missions = [
        {'hero_name': 'oracle', 'task_name': f'speed-test-{i}',
         'params': {'file_key': f'test-{i}'}}
        for i in range(3)
    ]

    # Test 1: Manual method
    print("\n⚙️  Testing deploy_heroes_parallel() (manual)...")
    start_manual = time.time()
    results_manual = superman.deploy_heroes_parallel(
        missions=missions,
        max_workers=3,
        use_worktrees=False  # Faster for short tasks
    )
    time_manual = time.time() - start_manual

    print(f"   Duration: {time_manual:.3f}s")
    print(f"   Success: {results_manual['successful']}/{results_manual['total_missions']}")

    # Test 2: Autonomous method
    print("\n🔮 Testing deploy_heroes_smart() (autonomous)...")
    start_smart = time.time()
    results_smart = superman.deploy_heroes_smart(
        missions=missions,
        show_recommendation=False  # Skip display for speed
    )
    time_smart = time.time() - start_smart

    print(f"   Duration: {time_smart:.3f}s")
    print(f"   Success: {results_smart['successful']}/{results_smart['total_missions']}")

    # Compare
    overhead_pct = ((time_smart - time_manual) / time_manual * 100) if time_manual > 0 else 0

    print(f"\n📊 Comparison:")
    print(f"   Manual:     {time_manual:.3f}s")
    print(f"   Autonomous: {time_smart:.3f}s")
    print(f"   Overhead:   {overhead_pct:.1f}%")

    if overhead_pct < 5:
        print(f"   ✅ EXCELLENT - Negligible overhead (<5%)")
    elif overhead_pct < 10:
        print(f"   ✅ GOOD - Low overhead (<10%)")
    elif overhead_pct < 20:
        print(f"   ✅ ACCEPTABLE - Moderate overhead (<20%)")
    else:
        print(f"   ⚠️  High overhead (>{overhead_pct:.0f}%)")

    return time_manual, time_smart


def benchmark_import_speed():
    """Measure module import time"""
    print("\n" + "="*80)
    print("BENCHMARK 3: Import Speed")
    print("="*80)

    import importlib
    import sys

    modules_to_test = [
        'core.justice_league.superman_coordinator',
        'core.utils.parallel_optimizer',
        'core.utils.git_worktree_manager'
    ]

    total_time = 0

    for module_name in modules_to_test:
        # Remove from cache to force reload
        if module_name in sys.modules:
            del sys.modules[module_name]

        start = time.time()
        module = importlib.import_module(module_name)
        import_time = time.time() - start
        total_time += import_time

        print(f"   {module_name.split('.')[-1]}: {import_time*1000:.2f}ms")

    print(f"\n📊 Total import time: {total_time*1000:.2f}ms")

    if total_time < 0.5:
        print(f"   ✅ EXCELLENT - Fast imports (<500ms)")
    elif total_time < 1.0:
        print(f"   ✅ GOOD - Reasonable import time (<1s)")
    else:
        print(f"   ⚠️  Slow imports (>{total_time:.1f}s)")

    return total_time


def main():
    """Run all benchmarks"""
    print("\n" + "="*80)
    print("⚡ PERFORMANCE BENCHMARK - AUTONOMOUS OPTIMIZATION")
    print("   Validating speed and ensuring no regressions")
    print("="*80)

    results = {}

    try:
        # Benchmark 1: Decision overhead
        decision_time = benchmark_overhead()
        results['decision_overhead'] = decision_time

        # Benchmark 2: Method comparison
        time_manual, time_smart = benchmark_method_comparison()
        results['manual_time'] = time_manual
        results['smart_time'] = time_smart

        # Benchmark 3: Import speed
        import_time = benchmark_import_speed()
        results['import_time'] = import_time

        # Final summary
        print("\n" + "="*80)
        print("📊 BENCHMARK SUMMARY")
        print("="*80)

        overhead_pct = ((results['smart_time'] - results['manual_time']) /
                       results['manual_time'] * 100) if results['manual_time'] > 0 else 0

        print(f"\n✅ Decision Overhead: {results['decision_overhead']*1000:.2f}ms")
        print(f"✅ Import Time: {results['import_time']*1000:.2f}ms")
        print(f"✅ Method Overhead: {overhead_pct:.1f}%")

        # Overall assessment
        all_good = (
            results['decision_overhead'] < 0.1 and
            results['import_time'] < 1.0 and
            overhead_pct < 10
        )

        print(f"\n{'='*80}")
        if all_good:
            print("🎉 PERFORMANCE: ✅ EXCELLENT")
            print("   All benchmarks within acceptable limits")
            print("   No performance degradation detected")
            print("   Autonomous optimization adds negligible overhead")
        else:
            print("⚠️  PERFORMANCE: NEEDS ATTENTION")
            if results['decision_overhead'] >= 0.1:
                print(f"   - Decision time high: {results['decision_overhead']*1000:.0f}ms")
            if results['import_time'] >= 1.0:
                print(f"   - Import time high: {results['import_time']*1000:.0f}ms")
            if overhead_pct >= 10:
                print(f"   - Method overhead high: {overhead_pct:.1f}%")

        print("="*80 + "\n")

        return 0 if all_good else 1

    except Exception as e:
        print(f"\n❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
