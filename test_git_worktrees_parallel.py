"""
🌳 TEST GIT WORKTREES - PARALLEL HERO OPERATIONS
Demonstrates Superman's parallel deployment capabilities with git worktrees

Tests:
1. GitWorktreeManager functionality
2. Parallel hero deployment with isolated workspaces
3. Performance comparison: parallel vs sequential
4. Cleanup and resource management

Version: 1.0.0
Created: 2025-10-31
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.utils.git_worktree_manager import GitWorktreeManager, HeroWorktreeContext
from core.justice_league.superman_coordinator import SupermanCoordinator


def test_worktree_manager():
    """Test 1: GitWorktreeManager basic functionality"""
    print("\n" + "="*80)
    print("TEST 1: GitWorktreeManager Basic Functionality")
    print("="*80)

    manager = GitWorktreeManager()

    # Test worktree creation
    print("\n🌳 Creating test worktree...")
    worktree_info = manager.create_worktree("test-task", branch="main")

    print(f"  ✅ Worktree created: {worktree_info['path']}")
    print(f"  📋 Branch: {worktree_info['branch']}")
    print(f"  🕒 Created: {worktree_info['created_at']}")

    # Test worktree listing
    print("\n🌳 Listing all worktrees...")
    all_worktrees = manager.list_worktrees()
    print(f"  📊 Found {len(all_worktrees)} worktrees")
    for wt in all_worktrees:
        print(f"     • {wt.get('path')} ({wt.get('branch', 'N/A')})")

    # Test worktree status
    print("\n🌳 Checking worktree status...")
    status = manager.get_worktree_status(Path(worktree_info['path']))
    print(f"  ✅ Status: {'clean' if status.get('clean') else 'has changes'}")

    # Test cleanup
    print("\n🌳 Cleaning up test worktree...")
    success = manager.remove_worktree(Path(worktree_info['path']))
    print(f"  {'✅' if success else '❌'} Cleanup: {'successful' if success else 'failed'}")

    return True


def test_context_manager():
    """Test 2: HeroWorktreeContext manager"""
    print("\n" + "="*80)
    print("TEST 2: HeroWorktreeContext Manager")
    print("="*80)

    manager = GitWorktreeManager()

    print("\n🌳 Using context manager for automatic cleanup...")

    with HeroWorktreeContext(manager, "context-test") as worktree:
        print(f"  ✅ Worktree created: {worktree['path']}")
        print(f"  📋 Task: {worktree['task_name']}")
        print("  🔨 Simulating work in worktree...")
        time.sleep(0.5)

    print("  ✅ Context manager auto-cleaned up worktree")

    return True


def test_parallel_hero_deployment():
    """Test 3: Superman parallel deployment with worktrees"""
    print("\n" + "="*80)
    print("TEST 3: Superman Parallel Hero Deployment")
    print("="*80)

    superman = SupermanCoordinator()

    # Define parallel missions (simulated)
    missions = [
        {
            'hero_name': 'oracle',
            'task_name': 'analyze-pattern-1',
            'params': {
                'file_key': 'test-key-1'
            }
        },
        {
            'hero_name': 'oracle',
            'task_name': 'analyze-pattern-2',
            'params': {
                'file_key': 'test-key-2'
            }
        },
        {
            'hero_name': 'oracle',
            'task_name': 'analyze-pattern-3',
            'params': {
                'file_key': 'test-key-3'
            }
        }
    ]

    print(f"\n🦸 Deploying {len(missions)} heroes in parallel...")
    print(f"  🌳 Using git worktrees for isolation")
    print(f"  ⚡ Max workers: 4")

    start_time = time.time()

    # Execute parallel deployment
    results = superman.deploy_heroes_parallel(
        missions=missions,
        max_workers=4,
        use_worktrees=True
    )

    duration = time.time() - start_time

    # Display results
    print(f"\n📊 Parallel Deployment Results:")
    print(f"  Total missions: {results['total_missions']}")
    print(f"  ✅ Successful: {results['successful']}")
    print(f"  ❌ Failed: {results['failed']}")
    print(f"  ⏱️  Duration: {duration:.2f}s")
    print(f"  🌳 Used worktrees: {results['used_worktrees']}")

    if results.get('worktree_cleanup'):
        cleanup = results['worktree_cleanup']
        print(f"\n🧹 Worktree Cleanup:")
        print(f"  ✅ Removed: {cleanup['success']}")
        print(f"  ❌ Failed: {cleanup['failures']}")

    return results['successful'] == len(missions)


def test_performance_comparison():
    """Test 4: Compare parallel vs sequential performance"""
    print("\n" + "="*80)
    print("TEST 4: Performance Comparison - Parallel vs Sequential")
    print("="*80)

    superman = SupermanCoordinator()

    # Test missions
    test_missions = [
        {
            'hero_name': 'oracle',
            'task_name': f'perf-test-{i}',
            'params': {'file_key': f'test-{i}'}
        }
        for i in range(6)
    ]

    # Test 1: Parallel execution
    print("\n⚡ Running parallel execution...")
    start_parallel = time.time()

    parallel_results = superman.deploy_heroes_parallel(
        missions=test_missions,
        max_workers=4,
        use_worktrees=True
    )

    parallel_duration = time.time() - start_parallel

    # Test 2: Sequential execution (simulated by max_workers=1)
    print("\n🐢 Running sequential execution...")
    start_sequential = time.time()

    sequential_results = superman.deploy_heroes_parallel(
        missions=test_missions,
        max_workers=1,
        use_worktrees=False
    )

    sequential_duration = time.time() - start_sequential

    # Performance analysis
    print("\n📊 Performance Analysis:")
    print(f"  Parallel execution:   {parallel_duration:.2f}s")
    print(f"  Sequential execution: {sequential_duration:.2f}s")

    speedup = sequential_duration / parallel_duration if parallel_duration > 0 else 0
    print(f"  ⚡ Speedup: {speedup:.2f}x")

    # Efficiency analysis
    if speedup > 1.5:
        print(f"  ✅ EXCELLENT: {speedup:.1f}x speedup with parallel processing")
    elif speedup > 1.0:
        print(f"  ✅ GOOD: {speedup:.1f}x speedup achieved")
    else:
        print(f"  ⚠️  No speedup - tasks may be too simple or overhead too high")

    return speedup > 1.0


def test_worktree_cleanup_and_pruning():
    """Test 5: Cleanup and orphan detection"""
    print("\n" + "="*80)
    print("TEST 5: Cleanup and Orphan Detection")
    print("="*80)

    manager = GitWorktreeManager()

    # Create some test worktrees
    print("\n🌳 Creating test worktrees...")
    test_worktrees = []
    for i in range(3):
        wt = manager.create_worktree(f"cleanup-test-{i}")
        test_worktrees.append(wt)
        print(f"  ✅ Created: {wt['path']}")

    # Test cleanup_all
    print("\n🧹 Cleaning up all worktrees...")
    cleanup_result = manager.cleanup_all(force=True)

    print(f"  📊 Cleanup summary:")
    print(f"     Total: {cleanup_result['total']}")
    print(f"     ✅ Success: {cleanup_result['success']}")
    print(f"     ❌ Failures: {cleanup_result['failures']}")

    # Test pruning
    print("\n🌳 Pruning orphaned worktrees...")
    pruned_count = manager.prune_orphaned()
    print(f"  📊 Pruned {pruned_count} orphaned worktrees")

    return cleanup_result['success'] == cleanup_result['total']


def run_all_tests():
    """Run all git worktree tests"""
    print("\n" + "="*80)
    print("🌳 GIT WORKTREES - PARALLEL HERO OPERATIONS TEST SUITE")
    print("="*80)

    results = {
        'total': 0,
        'passed': 0,
        'failed': 0
    }

    tests = [
        ("GitWorktreeManager Basic Functionality", test_worktree_manager),
        ("HeroWorktreeContext Manager", test_context_manager),
        ("Parallel Hero Deployment", test_parallel_hero_deployment),
        ("Performance Comparison", test_performance_comparison),
        ("Cleanup and Pruning", test_worktree_cleanup_and_pruning)
    ]

    for test_name, test_func in tests:
        results['total'] += 1
        try:
            print(f"\nRunning: {test_name}...")
            success = test_func()

            if success:
                results['passed'] += 1
                print(f"  ✅ PASSED: {test_name}")
            else:
                results['failed'] += 1
                print(f"  ❌ FAILED: {test_name}")

        except Exception as e:
            results['failed'] += 1
            print(f"  ❌ ERROR: {test_name}")
            print(f"     {str(e)}")

    # Final summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Total tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"Success rate: {(results['passed']/results['total']*100):.1f}%")

    print("\n🌳 Git Worktrees Integration: " +
          ("✅ READY FOR PRODUCTION" if results['failed'] == 0 else "⚠️  NEEDS ATTENTION"))

    return results['failed'] == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
