#!/usr/bin/env python3
"""
🔍 INDIVIDUAL HERO PERSONA AUDIT

Deep dive audit of each Justice League hero to ensure 100% completeness
Tests: Skills, Implementation, Functions, Classes, Exports, and Functionality

Version: 1.4.0
Date: 2025-10-20
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
import inspect

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


class HeroPersonaAuditor:
    """Deep audit of individual hero personas"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.skills_dir = self.project_root / '.claude' / 'skills'
        self.heroes_dir = self.project_root / 'core' / 'justice_league'
        self.audit_results = {}

    def print_header(self, text: str, emoji: str = '🦸', char: str = '='):
        """Print section header"""
        print(f"\n{emoji} {char * 75}")
        print(f"  {text}")
        print(f"{char * 77}\n")

    def audit_hero(self, hero_name: str, hero_config: Dict) -> Dict[str, Any]:
        """Comprehensive audit of a single hero"""

        result = {
            'hero': hero_name,
            'emoji': hero_config['emoji'],
            'status': 'PASS',
            'tests_passed': 0,
            'tests_total': 0,
            'issues': [],
            'warnings': [],
            'successes': []
        }

        self.print_header(f"{hero_name.upper()} - {hero_config['title']}", hero_config['emoji'])

        # Test 1: Skill File Exists
        result['tests_total'] += 1
        skill_path = self.skills_dir / f"{hero_config['slug']}.md"
        if skill_path.exists():
            result['tests_passed'] += 1
            print(f"✅ Skill File: {skill_path.name}")
            result['successes'].append("Skill file exists")

            # Read skill content
            skill_content = skill_path.read_text()

            # Test 1a: Has Usage Section
            result['tests_total'] += 1
            if '## Usage' in skill_content or '## Example' in skill_content:
                result['tests_passed'] += 1
                print("   ✅ Has usage examples")
            else:
                result['warnings'].append("Missing usage examples section")
                print("   ⚠️  Missing usage examples section")

            # Test 1b: Has Code Examples
            result['tests_total'] += 1
            if '```python' in skill_content or '```typescript' in skill_content:
                result['tests_passed'] += 1
                print("   ✅ Has code examples")
            else:
                result['warnings'].append("Missing code examples")
                print("   ⚠️  Missing code examples")

            # Test 1c: Has Catchphrase
            result['tests_total'] += 1
            if 'Catchphrase' in skill_content or 'catchphrase' in skill_content:
                result['tests_passed'] += 1
                print("   ✅ Has catchphrase")
            else:
                result['warnings'].append("Missing catchphrase")
                print("   ⚠️  Missing catchphrase")

        else:
            result['issues'].append(f"Skill file missing: {skill_path}")
            result['status'] = 'FAIL'
            print(f"❌ Skill File: NOT FOUND - {skill_path}")

        # Test 2: Implementation File Exists
        result['tests_total'] += 1
        impl_path = self.heroes_dir / hero_config['impl_file']
        if impl_path.exists():
            result['tests_passed'] += 1
            print(f"\n✅ Implementation: {impl_path.name}")
            result['successes'].append("Implementation file exists")

            # Read implementation
            impl_content = impl_path.read_text()

            # Test 2a: Has Docstring
            result['tests_total'] += 1
            if '"""' in impl_content[:1000]:
                result['tests_passed'] += 1
                print("   ✅ Has module docstring")
            else:
                result['warnings'].append("Missing module docstring")
                print("   ⚠️  Missing module docstring")

            # Test 2b: Has Class Definition
            result['tests_total'] += 1
            if f"class {hero_config['class_name']}" in impl_content:
                result['tests_passed'] += 1
                print(f"   ✅ Has class: {hero_config['class_name']}")
            else:
                result['issues'].append(f"Class {hero_config['class_name']} not found")
                result['status'] = 'FAIL'
                print(f"   ❌ Class {hero_config['class_name']} not found")

            # Test 2c: Has Main Function
            result['tests_total'] += 1
            if f"def {hero_config['main_function']}" in impl_content:
                result['tests_passed'] += 1
                print(f"   ✅ Has function: {hero_config['main_function']}()")
            else:
                result['issues'].append(f"Function {hero_config['main_function']} not found")
                result['status'] = 'FAIL'
                print(f"   ❌ Function {hero_config['main_function']}() not found")

        else:
            result['issues'].append(f"Implementation file missing: {impl_path}")
            result['status'] = 'FAIL'
            print(f"❌ Implementation: NOT FOUND - {impl_path}")

        # Test 3: Can Import Module
        result['tests_total'] += 1
        try:
            module = __import__(f"core.justice_league.{hero_config['impl_file'][:-3]}",
                               fromlist=[hero_config['class_name']])
            result['tests_passed'] += 1
            print(f"\n✅ Import: Module imported successfully")
            result['successes'].append("Module can be imported")

            # Test 3a: Class is Available
            result['tests_total'] += 1
            if hasattr(module, hero_config['class_name']):
                result['tests_passed'] += 1
                hero_class = getattr(module, hero_config['class_name'])
                print(f"   ✅ Class available: {hero_config['class_name']}")

                # Test 3b: Can Instantiate Class
                result['tests_total'] += 1
                try:
                    if hero_name == "Superman":
                        hero_instance = hero_class()
                    elif hero_name in ["Green Lantern", "Flash", "Cyborg", "Martian Manhunter", "Zatanna"]:
                        hero_instance = hero_class('/tmp/test')
                    else:
                        hero_instance = hero_class()

                    result['tests_passed'] += 1
                    print(f"   ✅ Can instantiate: {hero_config['class_name']}()")
                    result['successes'].append("Class can be instantiated")

                    # Test 3c: Has Expected Methods
                    result['tests_total'] += 1
                    expected_methods = hero_config.get('expected_methods', [])
                    missing_methods = []
                    for method in expected_methods:
                        if not hasattr(hero_instance, method):
                            missing_methods.append(method)

                    if not missing_methods:
                        result['tests_passed'] += 1
                        print(f"   ✅ Has all expected methods ({len(expected_methods)})")
                    else:
                        result['warnings'].append(f"Missing methods: {missing_methods}")
                        print(f"   ⚠️  Missing methods: {', '.join(missing_methods)}")

                except Exception as e:
                    result['issues'].append(f"Cannot instantiate class: {e}")
                    print(f"   ❌ Cannot instantiate: {e}")
            else:
                result['issues'].append(f"Class {hero_config['class_name']} not in module")
                print(f"   ❌ Class not available: {hero_config['class_name']}")

            # Test 3d: Main Function Available
            result['tests_total'] += 1
            if hasattr(module, hero_config['main_function']):
                result['tests_passed'] += 1
                print(f"   ✅ Function available: {hero_config['main_function']}()")

                # Test signature
                func = getattr(module, hero_config['main_function'])
                sig = inspect.signature(func)
                print(f"      Signature: {hero_config['main_function']}{sig}")
            else:
                result['issues'].append(f"Function {hero_config['main_function']} not in module")
                print(f"   ❌ Function not available: {hero_config['main_function']}()")

        except ImportError as e:
            result['issues'].append(f"Import error: {e}")
            result['status'] = 'FAIL'
            print(f"❌ Import: Failed - {e}")

        # Test 4: Check __init__.py exports
        result['tests_total'] += 1
        init_file = self.heroes_dir / '__init__.py'
        if init_file.exists():
            init_content = init_file.read_text()
            if hero_config['main_function'] in init_content:
                result['tests_passed'] += 1
                print(f"\n✅ Export: {hero_config['main_function']} in __all__")
            else:
                result['issues'].append(f"Function {hero_config['main_function']} not exported")
                result['status'] = 'FAIL'
                print(f"❌ Export: {hero_config['main_function']} not in __all__")

            # Check class export
            result['tests_total'] += 1
            if hero_config['class_name'] in init_content:
                result['tests_passed'] += 1
                print(f"   ✅ Class: {hero_config['class_name']} in __all__")
            else:
                result['warnings'].append(f"Class {hero_config['class_name']} not exported")
                print(f"   ⚠️  Class: {hero_config['class_name']} not in __all__")

        # Test 5: Integration with Superman
        result['tests_total'] += 1
        superman_file = self.heroes_dir / 'superman_coordinator.py'
        if superman_file.exists():
            superman_content = superman_file.read_text()
            if hero_config['impl_file'][:-3] in superman_content:
                result['tests_passed'] += 1
                print(f"\n✅ Superman Integration: Hero referenced in coordinator")
            else:
                result['warnings'].append("Not referenced in Superman coordinator")
                print(f"   ⚠️  Superman Integration: Not referenced in coordinator")

        # Calculate pass rate
        pass_rate = (result['tests_passed'] / result['tests_total']) * 100 if result['tests_total'] > 0 else 0

        # Print Summary
        print(f"\n{'─' * 77}")
        print(f"📊 SUMMARY:")
        print(f"   Tests Passed: {result['tests_passed']}/{result['tests_total']} ({pass_rate:.1f}%)")
        print(f"   Status: {result['status']}")

        if result['successes']:
            print(f"\n✅ Successes ({len(result['successes'])}):")
            for success in result['successes']:
                print(f"   • {success}")

        if result['warnings']:
            print(f"\n⚠️  Warnings ({len(result['warnings'])}):")
            for warning in result['warnings']:
                print(f"   • {warning}")

        if result['issues']:
            print(f"\n❌ Issues ({len(result['issues'])}):")
            for issue in result['issues']:
                print(f"   • {issue}")

        self.audit_results[hero_name] = result
        return result


def main():
    """Main audit function"""

    print("\n" + "="*80)
    print("  🔍 INDIVIDUAL HERO PERSONA AUDIT")
    print("  Deep Testing All 13 Heroes")
    print("="*80)

    auditor = HeroPersonaAuditor()

    # Hero configurations
    heroes = {
        "Superman": {
            "emoji": "🦸",
            "title": "The Coordinator",
            "slug": "superman",
            "impl_file": "superman_coordinator.py",
            "class_name": "SupermanCoordinator",
            "main_function": "assemble_justice_league",
            "expected_methods": ["assemble_justice_league", "_deploy_batman", "_deploy_litty"]
        },
        "Batman": {
            "emoji": "🦇",
            "title": "The Testing Detective",
            "slug": "batman",
            "impl_file": "batman_testing.py",
            "class_name": "BatmanTesting",
            "main_function": "batman_test_interactive_elements",
            "expected_methods": ["test_all_interactive_elements", "_test_buttons", "_test_links"]
        },
        "Green Lantern": {
            "emoji": "💚",
            "title": "The Visual Guardian",
            "slug": "green-lantern",
            "impl_file": "green_lantern_visual.py",
            "class_name": "GreenLanternVisual",
            "main_function": "green_lantern_store_baseline",
            "expected_methods": ["store_baseline", "compare_to_baseline", "list_baselines"]
        },
        "Wonder Woman": {
            "emoji": "⚡",
            "title": "The Accessibility Champion",
            "slug": "wonder-woman",
            "impl_file": "wonder_woman_accessibility.py",
            "class_name": "WonderWomanAccessibility",
            "main_function": "wonder_woman_accessibility_analysis",
            "expected_methods": ["champion_accessibility_analysis", "_check_wcag_compliance"]
        },
        "Flash": {
            "emoji": "⚡",
            "title": "The Speed Analyzer",
            "slug": "flash",
            "impl_file": "flash_performance.py",
            "class_name": "FlashPerformance",
            "main_function": "flash_profile_performance",
            "expected_methods": ["profile_performance", "_analyze_core_web_vitals"]
        },
        "Aquaman": {
            "emoji": "🌊",
            "title": "The Network Commander",
            "slug": "aquaman",
            "impl_file": "aquaman_network.py",
            "class_name": "AquamanNetwork",
            "main_function": "aquaman_analyze_network",
            "expected_methods": ["analyze_network_traffic", "_analyze_requests"]
        },
        "Cyborg": {
            "emoji": "🤖",
            "title": "The Integration Master",
            "slug": "cyborg",
            "impl_file": "cyborg_integrations.py",
            "class_name": "CyborgIntegrations",
            "main_function": "cyborg_connect_systems",
            "expected_methods": ["connect_all_systems", "extract_from_figma", "extract_from_penpot"]
        },
        "The Atom": {
            "emoji": "🔬",
            "title": "The Component Analyzer",
            "slug": "atom",
            "impl_file": "atom_component_analysis.py",
            "class_name": "AtomComponentAnalysis",
            "main_function": "atom_analyze_components",
            "expected_methods": ["analyze_component_library", "_analyze_single_component"]
        },
        "Green Arrow": {
            "emoji": "🏹",
            "title": "The Precision Tester",
            "slug": "green-arrow",
            "impl_file": "green_arrow_testing.py",
            "class_name": "GreenArrowTesting",
            "main_function": "green_arrow_test_league",
            "expected_methods": ["test_justice_league", "_test_hero"]
        },
        "Martian Manhunter": {
            "emoji": "🧠",
            "title": "The Security Guardian",
            "slug": "martian-manhunter",
            "impl_file": "martian_manhunter_security.py",
            "class_name": "MartianManhunterSecurity",
            "main_function": "martian_manhunter_security_scan",
            "expected_methods": ["scan_all_vulnerabilities", "_scan_injection", "_scan_xss"]
        },
        "Plastic Man": {
            "emoji": "🤸",
            "title": "The Responsive Design Specialist",
            "slug": "plastic-man",
            "impl_file": "plastic_man_responsive.py",
            "class_name": "PlasticManResponsive",
            "main_function": "plastic_man_responsive_test",
            "expected_methods": ["test_all_breakpoints", "_test_single_breakpoint"]
        },
        "Zatanna": {
            "emoji": "🎩",
            "title": "The SEO Magician",
            "slug": "zatanna",
            "impl_file": "zatanna_seo.py",
            "class_name": "ZatannaSEO",
            "main_function": "zatanna_seo_analysis",
            "expected_methods": ["analyze_seo_magic", "_analyze_meta_tags", "_analyze_structured_data"]
        },
        "Litty": {
            "emoji": "🪔",
            "title": "The Conscience Keeper",
            "slug": "litty",
            "impl_file": "litty_ethics.py",
            "class_name": "LittyEthics",
            "main_function": "litty_validate_ethics",
            "expected_methods": ["validate_ethics", "_detect_dark_patterns", "_generate_guilt_trips"]
        }
    }

    # Audit each hero
    for hero_name, config in heroes.items():
        auditor.audit_hero(hero_name, config)

    # Final Summary
    print("\n" + "="*80)
    print("  📊 FINAL AUDIT SUMMARY")
    print("="*80 + "\n")

    total_heroes = len(heroes)
    passed_heroes = sum(1 for r in auditor.audit_results.values() if r['status'] == 'PASS')
    total_tests = sum(r['tests_total'] for r in auditor.audit_results.values())
    passed_tests = sum(r['tests_passed'] for r in auditor.audit_results.values())

    print(f"🦸 Heroes Audited: {total_heroes}")
    print(f"✅ Heroes Passed: {passed_heroes}/{total_heroes}")
    print(f"📊 Tests Run: {passed_tests}/{total_tests} ({(passed_tests/total_tests*100):.1f}%)")

    print(f"\n{'Hero':<20} {'Tests':<15} {'Status':<10} {'Issues'}")
    print("─"*80)

    for hero_name, result in auditor.audit_results.items():
        tests_str = f"{result['tests_passed']}/{result['tests_total']}"
        status_icon = "✅" if result['status'] == 'PASS' else "❌"
        issues_count = len(result['issues']) + len(result['warnings'])

        print(f"{result['emoji']} {hero_name:<18} {tests_str:<15} {status_icon} {result['status']:<8} {issues_count}")

    # Overall verdict
    print("\n" + "="*80)
    if passed_heroes == total_heroes and passed_tests == total_tests:
        print("  🎉 PERFECT! All heroes passed 100% of tests!")
        print("  ✅ Justice League v1.4.0 is production-ready!")
        success = True
    elif passed_heroes == total_heroes:
        print(f"  ✅ All heroes passed, but with {total_tests - passed_tests} minor warnings")
        print("  👍 Justice League v1.4.0 is functional!")
        success = True
    else:
        print(f"  ⚠️  {total_heroes - passed_heroes} heroes have critical issues")
        print("  ❌ Requires attention before production deployment")
        success = False

    print("="*80 + "\n")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
