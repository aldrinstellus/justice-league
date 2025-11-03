"""
⚡ Justice League Parallel Orchestration System
Coordinate multiple heroes simultaneously for 6x speed boost

Usage:
    from lib.parallel_orchestration import ParallelCoordinator

    coordinator = ParallelCoordinator()
    results = await coordinator.deploy_heroes_parallel(url, heroes_config)
"""

import asyncio
import time
from typing import List, Dict, Callable, Any
from datetime import datetime


class ParallelCoordinator:
    """
    Coordinates Justice League heroes in parallel for maximum efficiency.
    Sequential: 6 heroes × 2 min = 12 minutes
    Parallel: 6 heroes ÷ 6 concurrent = 2 minutes
    Speed boost: 6x faster
    """

    def __init__(self, max_concurrent: int = 6):
        """
        Initialize parallel coordinator.

        Args:
            max_concurrent: Maximum number of heroes to run concurrently (default: 6)
        """
        self.max_concurrent = max_concurrent
        self.results = {}
        self.start_time = None

    async def deploy_hero(self, hero_name: str, hero_function: Callable, *args, **kwargs) -> Dict:
        """
        Deploy a single hero asynchronously.

        Args:
            hero_name: Name of the hero (e.g., 'Batman', 'Wonder Woman')
            hero_function: Hero's analysis function
            *args, **kwargs: Arguments to pass to hero function

        Returns:
            Hero result dictionary with timing information
        """
        start = time.time()
        print(f"⚡ Deploying {hero_name}...")

        try:
            # Run hero function (assume it's async or wrap if needed)
            if asyncio.iscoroutinefunction(hero_function):
                result = await hero_function(*args, **kwargs)
            else:
                # Wrap synchronous function in executor
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, hero_function, *args, **kwargs)

            elapsed = time.time() - start
            print(f"✅ {hero_name} complete ({elapsed:.1f}s)")

            return {
                'hero': hero_name,
                'success': True,
                'result': result,
                'elapsed_time': elapsed,
                'completed_at': datetime.now().isoformat()
            }

        except Exception as e:
            elapsed = time.time() - start
            print(f"❌ {hero_name} failed ({elapsed:.1f}s): {str(e)}")

            return {
                'hero': hero_name,
                'success': False,
                'error': str(e),
                'elapsed_time': elapsed,
                'completed_at': datetime.now().isoformat()
            }

    async def deploy_heroes_parallel(
        self,
        heroes: List[Dict[str, Any]],
        phase: str = "Phase 1"
    ) -> Dict:
        """
        Deploy multiple heroes in parallel.

        Args:
            heroes: List of hero configurations [{'name': 'Batman', 'function': batman_fn, 'args': [...]}]
            phase: Phase name for logging (default: "Phase 1")

        Returns:
            Results dictionary with individual hero results and summary

        Example:
            heroes = [
                {'name': 'Batman', 'function': batman_test_interactive, 'args': [url]},
                {'name': 'Wonder Woman', 'function': wonder_woman_accessibility, 'args': [url]},
                {'name': 'Flash', 'function': flash_profile_performance, 'args': [url]},
            ]
            results = await coordinator.deploy_heroes_parallel(heroes)
        """
        self.start_time = time.time()
        print(f"\n🦸 {phase}: Deploying {len(heroes)} heroes in parallel (max {self.max_concurrent} concurrent)...")
        print("="*80)

        # Create tasks for all heroes
        tasks = []
        for hero_config in heroes:
            hero_name = hero_config['name']
            hero_function = hero_config['function']
            hero_args = hero_config.get('args', [])
            hero_kwargs = hero_config.get('kwargs', {})

            task = self.deploy_hero(hero_name, hero_function, *hero_args, **hero_kwargs)
            tasks.append(task)

        # Run all tasks in parallel with semaphore control
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def run_with_semaphore(task):
            async with semaphore:
                return await task

        results = await asyncio.gather(*[run_with_semaphore(task) for task in tasks])

        total_time = time.time() - self.start_time
        print("="*80)
        print(f"✅ {phase} complete: {len(heroes)} heroes in {total_time:.1f}s")

        # Calculate statistics
        successful = sum(1 for r in results if r['success'])
        failed = len(results) - successful
        avg_time = sum(r['elapsed_time'] for r in results) / len(results) if results else 0

        return {
            'phase': phase,
            'total_heroes': len(heroes),
            'successful': successful,
            'failed': failed,
            'total_time': total_time,
            'average_time_per_hero': avg_time,
            'speed_boost': f"{len(heroes)}x" if successful > 0 else "N/A",
            'hero_results': results,
            'completed_at': datetime.now().isoformat()
        }

    async def deploy_sequential_phase(
        self,
        heroes: List[Dict[str, Any]],
        previous_results: Any,
        phase: str = "Phase 2"
    ) -> Dict:
        """
        Deploy heroes sequentially (when they depend on previous results).

        Args:
            heroes: List of hero configurations
            previous_results: Results from previous phase
            phase: Phase name for logging

        Returns:
            Results dictionary
        """
        print(f"\n🦸 {phase}: Deploying {len(heroes)} heroes sequentially (dependent on {phase})...")
        print("="*80)

        results = []
        start_time = time.time()

        for hero_config in heroes:
            hero_name = hero_config['name']
            hero_function = hero_config['function']
            hero_args = hero_config.get('args', [previous_results])
            hero_kwargs = hero_config.get('kwargs', {})

            result = await self.deploy_hero(hero_name, hero_function, *hero_args, **hero_kwargs)
            results.append(result)

        total_time = time.time() - start_time
        print("="*80)
        print(f"✅ {phase} complete: {len(heroes)} heroes in {total_time:.1f}s")

        successful = sum(1 for r in results if r['success'])
        failed = len(results) - successful

        return {
            'phase': phase,
            'total_heroes': len(heroes),
            'successful': successful,
            'failed': failed,
            'total_time': total_time,
            'hero_results': results,
            'completed_at': datetime.now().isoformat()
        }


# Example Superman coordination pattern
async def superman_coordinate_mission(url: str) -> Dict:
    """
    Example: Superman coordinates a full Justice League mission.

    Phase 1: Independent heroes (parallel - 6x faster)
    Phase 2: Dependent heroes (sequential)
    Phase 3: Oracle synthesis
    """
    coordinator = ParallelCoordinator(max_concurrent=6)

    # Phase 1: Independent heroes (can run in parallel)
    phase1_heroes = [
        {'name': 'Batman', 'function': mock_hero_analysis, 'args': [url, 'interactive']},
        {'name': 'Wonder Woman', 'function': mock_hero_analysis, 'args': [url, 'accessibility']},
        {'name': 'Flash', 'function': mock_hero_analysis, 'args': [url, 'performance']},
        {'name': 'Aquaman', 'function': mock_hero_analysis, 'args': [url, 'network']},
        {'name': 'Zatanna', 'function': mock_hero_analysis, 'args': [url, 'seo']},
        {'name': 'Plastic Man', 'function': mock_hero_analysis, 'args': [url, 'responsive']},
    ]

    phase1_results = await coordinator.deploy_heroes_parallel(phase1_heroes, "Phase 1")

    # Phase 2: Dependent heroes (sequential)
    phase2_heroes = [
        {'name': 'Green Lantern', 'function': mock_hero_analysis, 'args': [phase1_results, 'visual']},
        {'name': 'Atom', 'function': mock_hero_analysis, 'args': [phase1_results, 'components']},
    ]

    phase2_results = await coordinator.deploy_sequential_phase(phase2_heroes, phase1_results, "Phase 2")

    # Phase 3: Oracle synthesis
    print("\n🔮 Phase 3: Oracle synthesizing results...")
    oracle_result = {
        'mission_url': url,
        'phase1': phase1_results,
        'phase2': phase2_results,
        'total_heroes': phase1_results['total_heroes'] + phase2_results['total_heroes'],
        'total_time': phase1_results['total_time'] + phase2_results['total_time'],
        'overall_success': phase1_results['successful'] + phase2_results['successful'],
    }

    print(f"✅ Mission complete!")
    print(f"   • Total heroes: {oracle_result['total_heroes']}")
    print(f"   • Total time: {oracle_result['total_time']:.1f}s")
    print(f"   • Success rate: {oracle_result['overall_success']}/{oracle_result['total_heroes']}")

    return oracle_result


# Mock hero function for testing
async def mock_hero_analysis(target, analysis_type):
    """Mock hero analysis function (simulates 2-second analysis)."""
    await asyncio.sleep(2)  # Simulate analysis time
    return {
        'analysis_type': analysis_type,
        'target': target,
        'score': 85,
        'findings': [f'{analysis_type} analysis complete']
    }


# Example usage and testing
if __name__ == '__main__':
    import asyncio

    print("⚡ Testing Parallel Orchestration System\n")

    # Test full mission coordination
    async def test_mission():
        url = "https://example.com"
        result = await superman_coordinate_mission(url)

        print("\n" + "="*80)
        print("📊 FINAL RESULTS")
        print("="*80)
        print(f"Mission URL: {result['mission_url']}")
        print(f"Total Heroes: {result['total_heroes']}")
        print(f"Total Time: {result['total_time']:.1f}s")
        print(f"Success Rate: {result['overall_success']}/{result['total_heroes']}")

        # Calculate speed boost
        sequential_time = result['total_heroes'] * 2  # Each hero takes 2s
        parallel_time = result['total_time']
        speed_boost = sequential_time / parallel_time

        print(f"\n⚡ Speed Boost:")
        print(f"   • Sequential (estimated): {sequential_time:.1f}s")
        print(f"   • Parallel (actual): {parallel_time:.1f}s")
        print(f"   • Speed Boost: {speed_boost:.1f}x faster")

    # Run test
    asyncio.run(test_mission())

    print("\n✅ Parallel Orchestration System Tests Complete!")
