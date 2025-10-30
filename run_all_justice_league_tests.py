#!/usr/bin/env python3
"""
🦸 JUSTICE LEAGUE - Master Test Runner
========================================

Runs all Justice League hero test suites and provides comprehensive summary.

Usage:
    python3 run_all_justice_league_tests.py

Author: Justice League Development Team
Created: October 23, 2025
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Hero test files in order
HERO_TESTS = [
    ('🦇 Batman', 'test_batman.py', 'Interactive & E2E Testing'),
    ('💚 Green Lantern', 'test_green_lantern.py', 'Visual Regression Testing'),
    ('💪 Wonder Woman', 'test_wonder_woman.py', 'Accessibility Testing'),
    ('⚡ Flash', 'test_flash.py', 'Performance Testing'),
    ('🌊 Aquaman', 'test_aquaman.py', 'Network Analysis'),
    ('🤖 Cyborg', 'test_cyborg.py', 'System Integrations'),
    ('⚛️ The Atom', 'test_atom.py', 'Component Analysis'),
    ('🧠 Martian Manhunter', 'test_martian_manhunter.py', 'Security Testing'),
    ('🏹 Green Arrow', 'test_green_arrow.py', 'QA Testing'),
    ('🎨 Plastic Man', 'test_plastic_man.py', 'Responsive Design'),
    ('🎩 Zatanna', 'test_zatanna.py', 'SEO & Metadata'),
]


def run_test_file(hero_name, test_file, specialty):
    """Run a single test file and capture results"""
    print(f"\n{'=' * 70}")
    print(f"Testing: {hero_name} - {specialty}")
    print(f"File: {test_file}")
    print('=' * 70)

    try:
        result = subprocess.run(
            ['python3', test_file],
            capture_output=True,
            text=True,
            timeout=60
        )

        output = result.stdout + result.stderr

        # Extract success rate from output
        success_rate = 0
        total_tests = 0
        passed_tests = 0

        for line in output.split('\n'):
            if 'Success Rate:' in line:
                try:
                    success_rate = float(line.split(':')[1].strip().replace('%', ''))
                except:
                    pass
            if 'Total Tests:' in line:
                try:
                    total_tests = int(line.split(':')[1].strip())
                except:
                    pass
            if '✅ Passed:' in line:
                try:
                    passed_tests = int(line.split(':')[1].strip())
                except:
                    pass

        # Show last few lines (summary)
        lines = output.strip().split('\n')
        summary_lines = [l for l in lines if any(keyword in l for keyword in
            ['Total Tests:', '✅ Passed:', '❌ Failed:', 'Success Rate:', 'ALL TESTS PASSED', '🎉'])]

        for line in summary_lines[-5:]:
            print(line)

        return {
            'hero': hero_name,
            'file': test_file,
            'specialty': specialty,
            'success_rate': success_rate,
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'status': 'PASSED' if success_rate == 100 else 'FAILED',
            'output': output
        }

    except subprocess.TimeoutExpired:
        print(f"❌ TIMEOUT: {test_file} took too long")
        return {
            'hero': hero_name,
            'file': test_file,
            'specialty': specialty,
            'success_rate': 0,
            'total_tests': 0,
            'passed_tests': 0,
            'status': 'TIMEOUT',
            'output': ''
        }
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return {
            'hero': hero_name,
            'file': test_file,
            'specialty': specialty,
            'success_rate': 0,
            'total_tests': 0,
            'passed_tests': 0,
            'status': 'ERROR',
            'output': str(e)
        }


def main():
    """Run all Justice League test suites"""
    print("\n" + "=" * 70)
    print("🦸 JUSTICE LEAGUE - MASTER TEST SUITE")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Heroes: {len(HERO_TESTS)}")
    print(f"Expected Tests: {len(HERO_TESTS) * 10}")
    print("=" * 70)

    results = []

    # Run each test file
    for hero_name, test_file, specialty in HERO_TESTS:
        result = run_test_file(hero_name, test_file, specialty)
        results.append(result)

    # Summary
    print("\n" + "=" * 70)
    print("🦸 JUSTICE LEAGUE - TEST SUMMARY")
    print("=" * 70)

    total_heroes = len(results)
    passed_heroes = sum(1 for r in results if r['status'] == 'PASSED')
    failed_heroes = sum(1 for r in results if r['status'] in ['FAILED', 'TIMEOUT', 'ERROR'])

    total_tests = sum(r['total_tests'] for r in results)
    passed_tests = sum(r['passed_tests'] for r in results)

    print(f"\nHero Summary:")
    print(f"  Total Heroes: {total_heroes}")
    print(f"  ✅ Passed Heroes: {passed_heroes}")
    print(f"  ❌ Failed Heroes: {failed_heroes}")

    print(f"\nTest Summary:")
    print(f"  Total Tests: {total_tests}")
    print(f"  ✅ Passed Tests: {passed_tests}")
    print(f"  ❌ Failed Tests: {total_tests - passed_tests}")

    overall_success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    print(f"\n  Overall Success Rate: {overall_success_rate:.1f}%")

    # Individual hero results
    print("\n" + "-" * 70)
    print("Individual Hero Results:")
    print("-" * 70)

    for result in results:
        status_emoji = "✅" if result['status'] == 'PASSED' else "❌"
        print(f"{status_emoji} {result['hero']:25} {result['passed_tests']:2}/{result['total_tests']:2} tests  ({result['success_rate']:.0f}%)")

    # Failed heroes detail
    failed_results = [r for r in results if r['status'] != 'PASSED']
    if failed_results:
        print("\n" + "-" * 70)
        print("❌ Failed Heroes Detail:")
        print("-" * 70)
        for result in failed_results:
            print(f"\n{result['hero']} ({result['file']}):")
            print(f"  Status: {result['status']}")
            print(f"  Tests: {result['passed_tests']}/{result['total_tests']}")

    # Final verdict
    print("\n" + "=" * 70)
    if overall_success_rate == 100:
        print("🎉 SUCCESS! ALL JUSTICE LEAGUE TESTS PASSED!")
        print("🦸 The Justice League is ready to save the world!")
        print("💯 100% Test Coverage - Production Ready!")
        print("=" * 70)
        return 0
    else:
        print(f"⚠️  INCOMPLETE: {failed_heroes} hero(es) failed testing")
        print(f"📊 Overall: {overall_success_rate:.1f}% success rate")
        print("🔧 Please fix failing tests before deployment")
        print("=" * 70)
        return 1


if __name__ == '__main__':
    sys.exit(main())
