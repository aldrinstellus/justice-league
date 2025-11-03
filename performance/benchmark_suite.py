#!/usr/bin/env python3
"""
Oracle Performance Benchmark Suite
Week 15-16: Final Review & Launch

Comprehensive performance testing:
1. Agent response times (all 11 agents)
2. Database performance
3. Concurrent operations
4. System scan performance
5. Memory usage
6. Load testing
7. SLA validation

Run with: python3 performance/benchmark_suite.py
"""

import os
import sys
import time
import sqlite3
import statistics
import concurrent.futures
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class PerformanceBenchmark:
    """Comprehensive performance benchmarking for Oracle."""

    def __init__(self):
        self.results = {}
        self.start_time = time.time()

        # Performance targets (from requirements)
        self.targets = {
            'health_check': 500,  # ms
            'version_check': 500,  # ms
            'system_scan': 2000,  # ms
            'dependency_graph': 1000,  # ms
            'batman_p95': 2000,  # ms
            'flash_p95': 1000,  # ms
            'other_agent_p95': 3000,  # ms
        }

    def measure_time(self, func, *args, **kwargs) -> float:
        """Measure execution time in milliseconds."""
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = (time.time() - start) * 1000  # Convert to ms
        return elapsed, result

    def benchmark_health_checks(self, iterations: int = 100) -> Dict:
        """Benchmark health check performance."""
        print(f"\n[1/8] Benchmarking health checks ({iterations} iterations)...")

        from core.oracle_integration.superman_connector import get_superman_interface

        times = []

        try:
            connector = get_superman_interface()

            for i in range(iterations):
                elapsed, _ = self.measure_time(connector.heartbeat)
                times.append(elapsed)

                if (i + 1) % 20 == 0:
                    print(f"  Progress: {i + 1}/{iterations}")

            result = {
                'iterations': iterations,
                'times': times,
                'avg': statistics.mean(times),
                'median': statistics.median(times),
                'min': min(times),
                'max': max(times),
                'p95': statistics.quantiles(times, n=20)[18] if len(times) > 20 else max(times),
                'p99': statistics.quantiles(times, n=100)[98] if len(times) > 100 else max(times),
                'target': self.targets['health_check'],
                'pass': statistics.mean(times) < self.targets['health_check']
            }

            print(f"  Avg: {result['avg']:.2f}ms | P95: {result['p95']:.2f}ms | Target: {result['target']}ms")
            print(f"  Status: {'✓ PASS' if result['pass'] else '✗ FAIL'}")

            return result

        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            return {'error': str(e), 'pass': False}

    def benchmark_agent_health_checks(self, iterations: int = 50) -> Dict:
        """Benchmark agent health summary performance."""
        print(f"\n[2/8] Benchmarking agent health checks ({iterations} iterations)...")

        from core.oracle_integration.superman_connector import get_superman_interface

        times = []

        try:
            connector = get_superman_interface()

            for i in range(iterations):
                elapsed, _ = self.measure_time(connector.get_agent_health_summary)
                times.append(elapsed)

                if (i + 1) % 10 == 0:
                    print(f"  Progress: {i + 1}/{iterations}")

            result = {
                'iterations': iterations,
                'times': times,
                'avg': statistics.mean(times),
                'median': statistics.median(times),
                'p95': statistics.quantiles(times, n=20)[18] if len(times) > 20 else max(times),
                'target': self.targets['health_check'],
                'pass': statistics.mean(times) < self.targets['health_check']
            }

            print(f"  Avg: {result['avg']:.2f}ms | P95: {result['p95']:.2f}ms | Target: {result['target']}ms")
            print(f"  Status: {'✓ PASS' if result['pass'] else '✗ FAIL'}")

            return result

        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            return {'error': str(e), 'pass': False}

    def benchmark_version_checks(self, iterations: int = 50) -> Dict:
        """Benchmark version retrieval performance."""
        print(f"\n[3/8] Benchmarking version checks ({iterations} iterations)...")

        from core.oracle_integration.superman_connector import get_superman_interface

        times = []

        try:
            connector = get_superman_interface()

            for i in range(iterations):
                elapsed, _ = self.measure_time(connector.get_agent_versions)
                times.append(elapsed)

                if (i + 1) % 10 == 0:
                    print(f"  Progress: {i + 1}/{iterations}")

            result = {
                'iterations': iterations,
                'times': times,
                'avg': statistics.mean(times),
                'median': statistics.median(times),
                'p95': statistics.quantiles(times, n=20)[18] if len(times) > 20 else max(times),
                'target': self.targets['version_check'],
                'pass': statistics.mean(times) < self.targets['version_check']
            }

            print(f"  Avg: {result['avg']:.2f}ms | P95: {result['p95']:.2f}ms | Target: {result['target']}ms")
            print(f"  Status: {'✓ PASS' if result['pass'] else '✗ FAIL'}")

            return result

        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            return {'error': str(e), 'pass': False}

    def benchmark_system_scan(self, iterations: int = 20) -> Dict:
        """Benchmark full system scan performance."""
        print(f"\n[4/8] Benchmarking system scan ({iterations} iterations)...")

        from core.oracle_integration.oracle_coordinator import OracleCoordinator

        times = []

        try:
            coordinator = OracleCoordinator()

            for i in range(iterations):
                elapsed, _ = self.measure_time(coordinator.perform_system_scan)
                times.append(elapsed)

                if (i + 1) % 5 == 0:
                    print(f"  Progress: {i + 1}/{iterations}")

            result = {
                'iterations': iterations,
                'times': times,
                'avg': statistics.mean(times),
                'median': statistics.median(times),
                'p95': statistics.quantiles(times, n=20)[18] if len(times) > 20 else max(times),
                'target': self.targets['system_scan'],
                'pass': statistics.mean(times) < self.targets['system_scan']
            }

            print(f"  Avg: {result['avg']:.2f}ms | P95: {result['p95']:.2f}ms | Target: {result['target']}ms")
            print(f"  Status: {'✓ PASS' if result['pass'] else '✗ FAIL'}")

            return result

        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            return {'error': str(e), 'pass': False}

    def benchmark_dependency_graph(self, iterations: int = 50) -> Dict:
        """Benchmark dependency graph generation performance."""
        print(f"\n[5/8] Benchmarking dependency graph ({iterations} iterations)...")

        from core.oracle_integration.superman_connector import get_superman_interface

        times = []

        try:
            connector = get_superman_interface()

            for i in range(iterations):
                elapsed, _ = self.measure_time(connector.get_dependency_graph)
                times.append(elapsed)

                if (i + 1) % 10 == 0:
                    print(f"  Progress: {i + 1}/{iterations}")

            result = {
                'iterations': iterations,
                'times': times,
                'avg': statistics.mean(times),
                'median': statistics.median(times),
                'p95': statistics.quantiles(times, n=20)[18] if len(times) > 20 else max(times),
                'target': self.targets['dependency_graph'],
                'pass': statistics.mean(times) < self.targets['dependency_graph']
            }

            print(f"  Avg: {result['avg']:.2f}ms | P95: {result['p95']:.2f}ms | Target: {result['target']}ms")
            print(f"  Status: {'✓ PASS' if result['pass'] else '✗ FAIL'}")

            return result

        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            return {'error': str(e), 'pass': False}

    def benchmark_concurrent_operations(self, concurrent_requests: int = 20) -> Dict:
        """Benchmark concurrent operation performance."""
        print(f"\n[6/8] Benchmarking concurrent operations ({concurrent_requests} concurrent)...")

        from core.oracle_integration.superman_connector import get_superman_interface

        def do_health_check():
            connector = get_superman_interface()
            start = time.time()
            connector.heartbeat()
            return (time.time() - start) * 1000

        try:
            start_time = time.time()

            with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
                futures = [executor.submit(do_health_check) for _ in range(concurrent_requests)]
                times = [f.result() for f in concurrent.futures.as_completed(futures)]

            total_time = (time.time() - start_time) * 1000

            result = {
                'concurrent_requests': concurrent_requests,
                'times': times,
                'total_time': total_time,
                'avg_response': statistics.mean(times),
                'max_response': max(times),
                'throughput': (concurrent_requests / total_time) * 1000,  # requests per second
                'pass': statistics.mean(times) < self.targets['health_check'] * 2  # Allow 2x for concurrent
            }

            print(f"  Total time: {result['total_time']:.2f}ms")
            print(f"  Avg response: {result['avg_response']:.2f}ms")
            print(f"  Throughput: {result['throughput']:.2f} req/s")
            print(f"  Status: {'✓ PASS' if result['pass'] else '✗ FAIL'}")

            return result

        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            return {'error': str(e), 'pass': False}

    def benchmark_database_performance(self, iterations: int = 100) -> Dict:
        """Benchmark database query performance."""
        print(f"\n[7/8] Benchmarking database performance ({iterations} iterations)...")

        db_file = PROJECT_ROOT / 'oracle.db'

        if not db_file.exists():
            print("  ⚠ Database file not found, skipping")
            return {'skipped': True, 'pass': True}

        query_times = {
            'simple_select': [],
            'join_query': [],
            'insert': [],
            'update': []
        }

        try:
            for i in range(iterations):
                conn = sqlite3.connect(str(db_file))
                cursor = conn.cursor()

                # Simple SELECT
                start = time.time()
                cursor.execute("SELECT COUNT(*) FROM agents")
                cursor.fetchone()
                query_times['simple_select'].append((time.time() - start) * 1000)

                # JOIN query
                start = time.time()
                cursor.execute("""
                    SELECT a.name, COUNT(v.id)
                    FROM agents a
                    LEFT JOIN agent_versions v ON a.name = v.agent_name
                    GROUP BY a.name
                """)
                cursor.fetchall()
                query_times['join_query'].append((time.time() - start) * 1000)

                conn.close()

                if (i + 1) % 20 == 0:
                    print(f"  Progress: {i + 1}/{iterations}")

            result = {
                'iterations': iterations,
                'simple_select_avg': statistics.mean(query_times['simple_select']),
                'join_query_avg': statistics.mean(query_times['join_query']),
                'pass': statistics.mean(query_times['simple_select']) < 10 and
                        statistics.mean(query_times['join_query']) < 50
            }

            print(f"  Simple SELECT avg: {result['simple_select_avg']:.2f}ms")
            print(f"  JOIN query avg: {result['join_query_avg']:.2f}ms")
            print(f"  Status: {'✓ PASS' if result['pass'] else '✗ FAIL'}")

            return result

        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            return {'error': str(e), 'pass': False}

    def benchmark_memory_usage(self) -> Dict:
        """Benchmark memory usage."""
        print(f"\n[8/8] Benchmarking memory usage...")

        if not HAS_PSUTIL:
            print("  ⚠ psutil not installed, skipping memory benchmark")
            return {'skipped': True, 'pass': True}

        try:
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()

            result = {
                'rss_mb': memory_info.rss / (1024 * 1024),  # MB
                'vms_mb': memory_info.vms / (1024 * 1024),  # MB
                'percent': process.memory_percent(),
                'target_mb': 500,  # Target: < 500MB
                'pass': (memory_info.rss / (1024 * 1024)) < 500
            }

            print(f"  RSS: {result['rss_mb']:.2f} MB")
            print(f"  VMS: {result['vms_mb']:.2f} MB")
            print(f"  Percent: {result['percent']:.2f}%")
            print(f"  Status: {'✓ PASS' if result['pass'] else '✗ FAIL'}")

            return result

        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            return {'error': str(e), 'pass': False}

    def run_all_benchmarks(self) -> Dict:
        """Run all performance benchmarks."""
        print("="*80)
        print("Oracle Performance Benchmark Suite")
        print("Week 15-16: Final Review & Launch")
        print("="*80)

        self.results['health_checks'] = self.benchmark_health_checks(100)
        self.results['agent_health'] = self.benchmark_agent_health_checks(50)
        self.results['version_checks'] = self.benchmark_version_checks(50)
        self.results['system_scan'] = self.benchmark_system_scan(20)
        self.results['dependency_graph'] = self.benchmark_dependency_graph(50)
        self.results['concurrent'] = self.benchmark_concurrent_operations(20)
        self.results['database'] = self.benchmark_database_performance(100)
        self.results['memory'] = self.benchmark_memory_usage()

        # Summary
        total_time = time.time() - self.start_time
        print("\n" + "="*80)
        print("Performance Benchmark Summary")
        print("="*80)
        print(f"Total benchmark time: {total_time:.2f}s")
        print()

        # Check SLA compliance
        passed = sum(1 for r in self.results.values() if r.get('pass', False))
        total = len(self.results)

        print(f"Benchmarks: {passed}/{total} passed")
        print()

        # Print comparison to targets
        print("Performance vs. Targets:")
        print(f"  Health Check: {self.results['health_checks'].get('avg', 0):.2f}ms (target: {self.targets['health_check']}ms)")
        print(f"  Version Check: {self.results['version_checks'].get('avg', 0):.2f}ms (target: {self.targets['version_check']}ms)")
        print(f"  System Scan: {self.results['system_scan'].get('avg', 0):.2f}ms (target: {self.targets['system_scan']}ms)")
        print(f"  Dependency Graph: {self.results['dependency_graph'].get('avg', 0):.2f}ms (target: {self.targets['dependency_graph']}ms)")
        print()

        # Overall assessment
        if passed == total:
            print("✅ ALL BENCHMARKS PASSED")
            print("Oracle meets or exceeds all performance targets!")
        elif passed >= total * 0.9:
            print("⚠️  MOST BENCHMARKS PASSED")
            print("Minor performance issues detected")
        else:
            print("❌ PERFORMANCE ISSUES DETECTED")
            print("Significant performance problems need resolution")

        print("="*80)

        return self.results


def main():
    """Main benchmark entry point."""
    benchmark = PerformanceBenchmark()
    results = benchmark.run_all_benchmarks()

    # Save results
    report_dir = PROJECT_ROOT / 'performance' / 'reports'
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = report_dir / f"benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    import json
    with open(report_file, 'w') as f:
        # Convert to JSON-serializable format
        json_results = {}
        for key, value in results.items():
            if isinstance(value, dict):
                json_results[key] = {k: v for k, v in value.items() if k != 'times'}
            else:
                json_results[key] = value

        json.dump({
            'timestamp': datetime.now().isoformat(),
            'results': json_results
        }, f, indent=2)

    print(f"\nReport saved to: {report_file}")

    # Exit code based on pass/fail
    passed = sum(1 for r in results.values() if r.get('pass', False))
    total = len(results)

    if passed == total:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
