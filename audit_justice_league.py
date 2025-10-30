#!/usr/bin/env python3
"""
🔍 JUSTICE LEAGUE FULL AUDIT

Comprehensive audit of all Claude Skills and hero implementations
Ensures documentation matches code and everything is up-to-date

Version: 1.4.0
Date: 2025-10-20
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
import json

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


class JusticeLeagueAuditor:
    """Comprehensive auditor for Justice League heroes"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.skills_dir = self.project_root / '.claude' / 'skills'
        self.heroes_dir = self.project_root / 'core' / 'justice_league'

        self.expected_heroes = [
            'superman',
            'batman',
            'green-lantern',
            'wonder-woman',
            'flash',
            'aquaman',
            'cyborg',
            'atom',
            'green-arrow',
            'martian-manhunter',
            'plastic-man',
            'zatanna',
            'litty'
        ]

        self.audit_results = {
            'total_heroes': 13,
            'skills_found': 0,
            'implementations_found': 0,
            'skills_missing': [],
            'implementations_missing': [],
            'mismatches': [],
            'warnings': [],
            'successes': [],
            'hero_details': {}
        }

    def print_header(self, text: str, char: str = '='):
        """Print section header"""
        print(f"\n{char * 80}")
        print(f"  {text}")
        print(f"{char * 80}\n")

    def print_hero_header(self, hero_name: str, emoji: str = '🦸'):
        """Print hero-specific header"""
        print(f"\n{emoji} {'─' * 75}")
        print(f"  {hero_name.upper()}")
        print(f"{'─' * 77}")

    def audit_skill_file(self, hero_slug: str) -> Dict[str, Any]:
        """Audit a single skill file"""
        skill_file = self.skills_dir / f"{hero_slug}.md"

        result = {
            'hero': hero_slug,
            'skill_exists': skill_file.exists(),
            'skill_path': str(skill_file),
            'file_size': 0,
            'has_description': False,
            'has_usage_examples': False,
            'has_powers': False,
            'has_function_signature': False,
            'content_preview': ''
        }

        if skill_file.exists():
            content = skill_file.read_text()
            result['file_size'] = len(content)
            result['content_preview'] = content[:200]

            # Check for key sections
            result['has_description'] = '## Overview' in content or '## Description' in content
            result['has_usage_examples'] = '## Usage' in content or '## Example' in content
            result['has_powers'] = '## Powers' in content or 'Powers:' in content
            result['has_function_signature'] = '```python' in content or '```typescript' in content

        return result

    def audit_implementation_file(self, hero_slug: str) -> Dict[str, Any]:
        """Audit a single implementation file"""

        # Map skill slug to implementation filename
        filename_map = {
            'superman': 'superman_coordinator.py',
            'batman': 'batman_testing.py',
            'green-lantern': 'green_lantern_visual.py',
            'wonder-woman': 'wonder_woman_accessibility.py',
            'flash': 'flash_performance.py',
            'aquaman': 'aquaman_network.py',
            'cyborg': 'cyborg_integrations.py',
            'atom': 'atom_component_analysis.py',
            'green-arrow': 'green_arrow_testing.py',
            'martian-manhunter': 'martian_manhunter_security.py',
            'plastic-man': 'plastic_man_responsive.py',
            'zatanna': 'zatanna_seo.py',
            'litty': 'litty_ethics.py'
        }

        impl_filename = filename_map.get(hero_slug)
        if not impl_filename:
            return {'hero': hero_slug, 'implementation_exists': False}

        impl_file = self.heroes_dir / impl_filename

        result = {
            'hero': hero_slug,
            'implementation_exists': impl_file.exists(),
            'implementation_path': str(impl_file),
            'file_size': 0,
            'has_class': False,
            'has_main_function': False,
            'has_docstring': False,
            'line_count': 0,
            'class_name': '',
            'function_names': []
        }

        if impl_file.exists():
            content = impl_file.read_text()
            lines = content.split('\n')

            result['file_size'] = len(content)
            result['line_count'] = len(lines)
            result['has_docstring'] = '"""' in content[:500]

            # Find class definitions
            for line in lines:
                if line.strip().startswith('class '):
                    result['has_class'] = True
                    result['class_name'] = line.strip().split('class ')[1].split('(')[0].split(':')[0]
                    break

            # Find function definitions
            functions = []
            for line in lines:
                if line.strip().startswith('def ') and not line.strip().startswith('def _'):
                    func_name = line.strip().split('def ')[1].split('(')[0]
                    functions.append(func_name)

            result['function_names'] = functions[:5]  # First 5 functions
            result['has_main_function'] = len(functions) > 0

        return result

    def check_module_exports(self) -> Dict[str, Any]:
        """Check if all heroes are exported in __init__.py"""
        init_file = self.heroes_dir / '__init__.py'

        result = {
            'init_exists': init_file.exists(),
            'version': 'unknown',
            'hero_count': 0,
            'exported_heroes': [],
            'missing_exports': []
        }

        if init_file.exists():
            content = init_file.read_text()

            # Check version
            if "__version__" in content:
                for line in content.split('\n'):
                    if '__version__' in line:
                        result['version'] = line.split('=')[1].strip().strip("'\"")

            # Check hero count
            if "__heroes__" in content:
                for line in content.split('\n'):
                    if '__heroes__' in line:
                        result['hero_count'] = int(line.split('=')[1].strip())

            # Check exports
            export_map = {
                'superman': 'assemble_justice_league',
                'batman': 'batman_test_interactive_elements',
                'green-lantern': 'green_lantern_store_baseline',
                'wonder-woman': 'wonder_woman_accessibility_analysis',
                'flash': 'flash_profile_performance',
                'aquaman': 'aquaman_analyze_network',
                'cyborg': 'cyborg_connect_systems',
                'atom': 'atom_analyze_components',
                'green-arrow': 'green_arrow_test_league',
                'martian-manhunter': 'martian_manhunter_security_scan',
                'plastic-man': 'plastic_man_responsive_test',
                'zatanna': 'zatanna_seo_analysis',
                'litty': 'litty_validate_ethics'
            }

            for hero, func_name in export_map.items():
                if func_name in content:
                    result['exported_heroes'].append(hero)
                else:
                    result['missing_exports'].append(hero)

        return result

    def test_imports(self) -> Dict[str, Any]:
        """Test if all heroes can be imported"""
        result = {
            'import_successful': True,
            'imported_heroes': [],
            'failed_imports': [],
            'errors': []
        }

        try:
            from core.justice_league import (
                assemble_justice_league,
                batman_test_interactive_elements,
                green_lantern_store_baseline,
                wonder_woman_accessibility_analysis,
                flash_profile_performance,
                aquaman_analyze_network,
                cyborg_connect_systems,
                atom_analyze_components,
                green_arrow_test_league,
                martian_manhunter_security_scan,
                plastic_man_responsive_test,
                zatanna_seo_analysis,
                litty_validate_ethics
            )

            result['imported_heroes'] = [
                'superman', 'batman', 'green-lantern', 'wonder-woman',
                'flash', 'aquaman', 'cyborg', 'atom', 'green-arrow',
                'martian-manhunter', 'plastic-man', 'zatanna', 'litty'
            ]

        except ImportError as e:
            result['import_successful'] = False
            result['errors'].append(str(e))

        return result

    def run_full_audit(self) -> Dict[str, Any]:
        """Run complete audit of all heroes"""

        self.print_header("🔍 JUSTICE LEAGUE FULL AUDIT", '=')
        print("Auditing all 13 heroes: Skills, Implementations, Exports, and Imports\n")

        # 1. Check module exports
        self.print_header("📦 MODULE EXPORTS CHECK", '-')
        exports = self.check_module_exports()

        print(f"✅ __init__.py exists: {exports['init_exists']}")
        print(f"📌 Version: {exports['version']}")
        print(f"🦸 Hero count: {exports['hero_count']}")
        print(f"✅ Exported heroes: {len(exports['exported_heroes'])}/13")

        if exports['missing_exports']:
            print(f"❌ Missing exports: {', '.join(exports['missing_exports'])}")
            self.audit_results['warnings'].append(f"Missing exports: {exports['missing_exports']}")
        else:
            print("✅ All heroes exported correctly!")
            self.audit_results['successes'].append("All heroes exported in __init__.py")

        # 2. Test imports
        self.print_header("🔌 IMPORT TEST", '-')
        imports = self.test_imports()

        if imports['import_successful']:
            print(f"✅ All heroes imported successfully! ({len(imports['imported_heroes'])}/13)")
            self.audit_results['successes'].append("All hero imports working")
        else:
            print(f"❌ Import failed!")
            for error in imports['errors']:
                print(f"   Error: {error}")
            self.audit_results['warnings'].append(f"Import errors: {imports['errors']}")

        # 3. Audit each hero
        self.print_header("🦸 HERO-BY-HERO AUDIT", '=')

        hero_emojis = {
            'superman': '🦸',
            'batman': '🦇',
            'green-lantern': '💚',
            'wonder-woman': '⚡',
            'flash': '⚡',
            'aquaman': '🌊',
            'cyborg': '🤖',
            'atom': '🔬',
            'green-arrow': '🏹',
            'martian-manhunter': '🧠',
            'plastic-man': '🤸',
            'zatanna': '🎩',
            'litty': '🪔'
        }

        for hero_slug in self.expected_heroes:
            emoji = hero_emojis.get(hero_slug, '🦸')
            self.print_hero_header(hero_slug, emoji)

            # Audit skill
            skill_result = self.audit_skill_file(hero_slug)
            impl_result = self.audit_implementation_file(hero_slug)

            # Store results
            self.audit_results['hero_details'][hero_slug] = {
                'skill': skill_result,
                'implementation': impl_result
            }

            # Print results
            print(f"📄 Skill File:")
            if skill_result['skill_exists']:
                print(f"   ✅ EXISTS: {skill_result['skill_path']}")
                print(f"   📏 Size: {skill_result['file_size']} bytes")
                print(f"   {'✅' if skill_result['has_description'] else '❌'} Has description")
                print(f"   {'✅' if skill_result['has_powers'] else '❌'} Has powers section")
                print(f"   {'✅' if skill_result['has_usage_examples'] else '❌'} Has usage examples")
                print(f"   {'✅' if skill_result['has_function_signature'] else '❌'} Has code examples")
                self.audit_results['skills_found'] += 1

                # Check for warnings
                if not skill_result['has_usage_examples']:
                    self.audit_results['warnings'].append(f"{hero_slug}: Skill missing usage examples")
            else:
                print(f"   ❌ MISSING: {skill_result['skill_path']}")
                self.audit_results['skills_missing'].append(hero_slug)

            print(f"\n💻 Implementation File:")
            if impl_result['implementation_exists']:
                print(f"   ✅ EXISTS: {impl_result['implementation_path']}")
                print(f"   📏 Size: {impl_result['file_size']} bytes ({impl_result['line_count']} lines)")
                print(f"   {'✅' if impl_result['has_docstring'] else '❌'} Has docstring")
                print(f"   {'✅' if impl_result['has_class'] else '❌'} Has class definition")
                if impl_result['has_class']:
                    print(f"      Class: {impl_result['class_name']}")
                print(f"   {'✅' if impl_result['has_main_function'] else '❌'} Has main functions")
                if impl_result['function_names']:
                    print(f"      Functions: {', '.join(impl_result['function_names'])}")
                self.audit_results['implementations_found'] += 1
            else:
                print(f"   ❌ MISSING: {impl_result['implementation_path']}")
                self.audit_results['implementations_missing'].append(hero_slug)

            # Check for mismatches
            if skill_result['skill_exists'] and not impl_result['implementation_exists']:
                self.audit_results['mismatches'].append(f"{hero_slug}: Skill exists but implementation missing")
            elif not skill_result['skill_exists'] and impl_result['implementation_exists']:
                self.audit_results['mismatches'].append(f"{hero_slug}: Implementation exists but skill missing")

        return self.audit_results

    def generate_report(self, results: Dict[str, Any]):
        """Generate final audit report"""

        self.print_header("📊 AUDIT SUMMARY REPORT", '=')

        # Overall status
        total_expected = results['total_heroes']
        skills_found = results['skills_found']
        impls_found = results['implementations_found']

        print(f"🦸 Total Heroes Expected: {total_expected}")
        print(f"📄 Skills Found: {skills_found}/{total_expected}")
        print(f"💻 Implementations Found: {impls_found}/{total_expected}")

        # Success rate
        skill_rate = (skills_found / total_expected) * 100
        impl_rate = (impls_found / total_expected) * 100
        overall_rate = ((skills_found + impls_found) / (total_expected * 2)) * 100

        print(f"\n📈 Completion Rates:")
        print(f"   Skills: {skill_rate:.1f}%")
        print(f"   Implementations: {impl_rate:.1f}%")
        print(f"   Overall: {overall_rate:.1f}%")

        # Missing items
        if results['skills_missing']:
            print(f"\n❌ Missing Skills ({len(results['skills_missing'])}):")
            for hero in results['skills_missing']:
                print(f"   - {hero}")

        if results['implementations_missing']:
            print(f"\n❌ Missing Implementations ({len(results['implementations_missing'])}):")
            for hero in results['implementations_missing']:
                print(f"   - {hero}")

        # Mismatches
        if results['mismatches']:
            print(f"\n⚠️  Mismatches ({len(results['mismatches'])}):")
            for mismatch in results['mismatches']:
                print(f"   - {mismatch}")

        # Warnings
        if results['warnings']:
            print(f"\n⚠️  Warnings ({len(results['warnings'])}):")
            for warning in results['warnings']:
                print(f"   - {warning}")

        # Successes
        if results['successes']:
            print(f"\n✅ Successes ({len(results['successes'])}):")
            for success in results['successes']:
                print(f"   - {success}")

        # Final verdict
        self.print_header("🎯 FINAL VERDICT", '=')

        if overall_rate == 100 and not results['mismatches'] and not results['warnings']:
            print("🎉 PERFECT AUDIT! All heroes are fully documented and implemented!")
            print("✅ Justice League v1.4.0 is 100% complete and ready!")
            return True
        elif overall_rate >= 90:
            print("✅ EXCELLENT! Justice League is in great shape!")
            print(f"📊 {overall_rate:.1f}% complete with minor issues to address.")
            return True
        elif overall_rate >= 75:
            print("⚠️  GOOD with room for improvement.")
            print(f"📊 {overall_rate:.1f}% complete. Address warnings and mismatches.")
            return False
        else:
            print("❌ NEEDS ATTENTION! Significant gaps found.")
            print(f"📊 Only {overall_rate:.1f}% complete. Urgent fixes needed.")
            return False

    def save_report_to_file(self, results: Dict[str, Any]):
        """Save audit report to JSON file"""
        report_file = self.project_root / 'AUDIT_REPORT.json'

        report = {
            'version': '1.4.0',
            'audit_date': '2025-10-20',
            'summary': {
                'total_heroes': results['total_heroes'],
                'skills_found': results['skills_found'],
                'implementations_found': results['implementations_found'],
                'skills_missing': results['skills_missing'],
                'implementations_missing': results['implementations_missing'],
                'mismatches': results['mismatches'],
                'warnings': results['warnings'],
                'successes': results['successes']
            },
            'hero_details': results['hero_details']
        }

        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n💾 Full report saved to: {report_file}")


def main():
    """Main audit function"""

    print("\n" + "="*80)
    print("  🔍 JUSTICE LEAGUE COMPREHENSIVE AUDIT")
    print("  Version 1.4.0 | All 13 Heroes")
    print("="*80)

    auditor = JusticeLeagueAuditor()

    # Run full audit
    results = auditor.run_full_audit()

    # Generate report
    success = auditor.generate_report(results)

    # Save report
    auditor.save_report_to_file(results)

    print("\n" + "="*80)
    print("  🔍 AUDIT COMPLETE")
    print("="*80 + "\n")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
