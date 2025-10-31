#!/usr/bin/env python3
"""
🌳 DEMO: Git Worktrees Parallel Operations
Live demonstration of Justice League parallel deployment

This script shows the team how to use parallel operations with real examples.

Usage:
    python3 demo_parallel_operations.py
"""

import sys
from pathlib import Path
import time

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.justice_league import SupermanCoordinator


def demo_banner():
    """Show demo banner"""
    print("\n" + "="*80)
    print("🌳 GIT WORKTREES PARALLEL OPERATIONS - LIVE DEMO")
    print("="*80)
    print("\nThis demo shows the Justice League's new parallel capabilities.")
    print("Watch as Superman deploys heroes in parallel with isolated worktrees!\n")


def demo_1_sequential_vs_parallel():
    """Demo 1: Show sequential vs parallel performance"""
    print("\n" + "="*80)
    print("DEMO 1: Sequential vs Parallel Performance")
    print("="*80)

    superman = SupermanCoordinator()

    # Simulate 3 Oracle analysis tasks
    missions = [
        {'hero_name': 'oracle', 'task_name': f'demo-analysis-{i}',
         'params': {'file_key': f'demo-file-{i}'}}
        for i in range(3)
    ]

    print("\n🐢 Running SEQUENTIAL execution...")
    start_seq = time.time()

    results_seq = superman.deploy_heroes_parallel(
        missions=missions,
        max_workers=1,        # Force sequential
        use_worktrees=False   # No worktrees needed for sequential
    )

    duration_seq = time.time() - start_seq

    print(f"\n  Duration: {duration_seq:.2f}s")
    print(f"  Successful: {results_seq['successful']}/{results_seq['total_missions']}")

    print("\n⚡ Running PARALLEL execution with git worktrees...")
    start_par = time.time()

    results_par = superman.deploy_heroes_parallel(
        missions=missions,
        max_workers=3,        # Parallel
        use_worktrees=True    # With worktrees
    )

    duration_par = time.time() - start_par

    print(f"\n  Duration: {duration_par:.2f}s")
    print(f"  Successful: {results_par['successful']}/{results_par['total_missions']}")

    # Calculate speedup
    if duration_par > 0:
        speedup = duration_seq / duration_par
        print(f"\n📊 Performance Comparison:")
        print(f"  Sequential: {duration_seq:.2f}s")
        print(f"  Parallel:   {duration_par:.2f}s")
        print(f"  ⚡ Speedup: {speedup:.2f}x")

        if speedup > 1.5:
            print(f"\n  ✅ EXCELLENT: {speedup:.1f}x faster with parallel processing!")
        elif speedup > 1.0:
            print(f"\n  ✅ GOOD: {speedup:.1f}x speedup achieved")
        else:
            print(f"\n  ℹ️  Note: Tasks may be too fast to show significant speedup")
            print(f"     (Oracle operations are very fast - use longer tasks for best results)")


def demo_2_worktree_isolation():
    """Demo 2: Show worktree isolation"""
    print("\n" + "="*80)
    print("DEMO 2: Worktree Isolation - Each Hero Gets Own Workspace")
    print("="*80)

    from core.utils import GitWorktreeManager

    manager = GitWorktreeManager()

    print("\n🌳 Creating 3 isolated worktrees...")

    worktrees = []
    for i in range(3):
        wt = manager.create_worktree(f"demo-workspace-{i}")
        worktrees.append(wt)
        print(f"  ✅ Worktree {i+1}: {wt['path']}")
        print(f"     Branch: {wt['branch']}")
        print(f"     Status: {wt['status']}")

    print("\n📊 All worktrees are isolated - no conflicts!")
    print("   Each hero can work independently without interfering.")

    print("\n🧹 Cleaning up worktrees...")
    cleanup = manager.cleanup_all(force=True)
    print(f"  ✅ Removed: {cleanup['success']}/{cleanup['total']} worktrees")
    print(f"  ✨ Clean slate - no debris left behind!")


def demo_3_context_manager():
    """Demo 3: Show automatic cleanup with context manager"""
    print("\n" + "="*80)
    print("DEMO 3: Context Manager - Automatic Resource Management")
    print("="*80)

    from core.utils import GitWorktreeManager, HeroWorktreeContext

    manager = GitWorktreeManager()

    print("\n🌳 Using context manager for automatic cleanup...")
    print("   (Simulating a hero mission with auto-cleanup)\n")

    with HeroWorktreeContext(manager, "demo-mission") as worktree:
        print(f"  ✅ Worktree created: {worktree['path']}")
        print(f"  🔨 Hero working in isolated workspace...")
        time.sleep(0.5)
        print(f"  ✨ Mission complete!")

    print(f"\n  ✅ Context manager automatically cleaned up worktree")
    print(f"     No manual cleanup needed - completely automatic!")


def demo_4_real_world_example():
    """Demo 4: Real-world batch conversion example"""
    print("\n" + "="*80)
    print("DEMO 4: Real-World Example - Batch Component Conversion")
    print("="*80)

    print("\n📋 Scenario: Convert 4 Figma components")
    print("   Components: Header, Footer, Sidebar, Dashboard")

    print("\n💡 With git worktrees, all 4 convert simultaneously:")
    print("""
    🎨 Artemis #1 → Header    (60s) ║ worktree-1
    🎨 Artemis #2 → Footer    (60s) ║ worktree-2  ← Parallel!
    🎨 Artemis #3 → Sidebar   (60s) ║ worktree-3  ← Parallel!
    🎨 Artemis #4 → Dashboard (60s) ║ worktree-4  ← Parallel!

    Total time: ~65 seconds (vs 240s sequential)
    Speedup: 3.7x FASTER ⚡
    """)

    print("\n📝 Code to run this:")
    print("""
    from core.justice_league import SupermanCoordinator

    superman = SupermanCoordinator()

    missions = [
        {'hero_name': 'artemis', 'task_name': 'convert-header',
         'params': {'figma_url': '...', 'component_name': 'Header'}},
        # ... 3 more components
    ]

    results = superman.deploy_heroes_parallel(
        missions=missions,
        max_workers=4,
        use_worktrees=True
    )
    """)

    print("\n✅ See QUICK_START_PARALLEL_OPERATIONS.md for complete examples!")


def main():
    """Run all demos"""
    demo_banner()

    demos = [
        ("Sequential vs Parallel", demo_1_sequential_vs_parallel),
        ("Worktree Isolation", demo_2_worktree_isolation),
        ("Context Manager", demo_3_context_manager),
        ("Real-World Example", demo_4_real_world_example)
    ]

    for i, (name, demo_func) in enumerate(demos, 1):
        try:
            demo_func()

            if i < len(demos):
                input(f"\n\n⏸️  Press ENTER to continue to Demo {i+1}...")

        except KeyboardInterrupt:
            print("\n\n⏸️  Demo interrupted by user")
            break
        except Exception as e:
            print(f"\n\n❌ Demo error: {e}")
            import traceback
            traceback.print_exc()

    # Final summary
    print("\n" + "="*80)
    print("🎉 DEMO COMPLETE")
    print("="*80)
    print("\n✅ The Justice League is ready for parallel operations!")
    print("\n📚 Next Steps:")
    print("   1. See QUICK_START_PARALLEL_OPERATIONS.md for usage")
    print("   2. See GIT_TREES_OPTIMIZATION_GUIDE.md for details")
    print("   3. Run test_git_worktrees_parallel.py to validate")
    print("\n🚀 Start deploying heroes in parallel today!")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
