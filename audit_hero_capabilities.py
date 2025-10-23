#!/usr/bin/env python3
"""
🔍 JUSTICE LEAGUE CAPABILITY AUDIT
Comprehensive audit of all heroes to ensure they have the tools and skills to do their jobs.
"""

import os
import sys
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Tuple

class JusticeLeagueAuditor:
    """Audits all Justice League heroes for capability completeness"""

    def __init__(self):
        self.audit_results = {}
        self.project_root = Path(__file__).parent
        self.heroes_path = self.project_root / 'core' / 'justice_league'

    def audit_all_heroes(self) -> Dict[str, Any]:
        """Comprehensive audit of all 9 heroes"""
        print("🔍 JUSTICE LEAGUE CAPABILITY AUDIT")
        print("=" * 80)
        print()

        heroes = [
            ('Superman', 'superman_coordinator', self._audit_superman),
            ('Batman', 'batman_testing', self._audit_batman),
            ('Green Lantern', 'green_lantern_visual', self._audit_green_lantern),
            ('Wonder Woman', 'wonder_woman_accessibility', self._audit_wonder_woman),
            ('Flash', 'flash_performance', self._audit_flash),
            ('Aquaman', 'aquaman_network', self._audit_aquaman),
            ('Cyborg', 'cyborg_integrations', self._audit_cyborg),
            ('The Atom', 'atom_component_analysis', self._audit_atom),
            ('Green Arrow', 'green_arrow_testing', self._audit_green_arrow)
        ]

        total_missing = 0
        total_capabilities = 0

        for hero_name, module_name, audit_func in heroes:
            print(f"\n🦸 {hero_name.upper()}")
            print("-" * 80)

            # Load module
            module = self._load_hero_module(module_name)
            if not module:
                print(f"❌ CRITICAL: Module {module_name}.py not found!")
                self.audit_results[hero_name] = {
                    'status': 'MISSING_MODULE',
                    'missing_capabilities': [],
                    'score': 0
                }
                continue

            # Run hero-specific audit
            result = audit_func(module)
            self.audit_results[hero_name] = result

            # Display results
            print(f"Status: {result['status']}")
            print(f"Capabilities Present: {result['present_count']}/{result['total_count']}")
            print(f"Score: {result['score']:.1f}/100")

            if result['missing_capabilities']:
                print(f"\n⚠️  MISSING CAPABILITIES ({len(result['missing_capabilities'])}):")
                for missing in result['missing_capabilities']:
                    print(f"   - {missing['name']}: {missing['description']}")
            else:
                print("✅ All capabilities present!")

            if result['warnings']:
                print(f"\n⚡ WARNINGS ({len(result['warnings'])}):")
                for warning in result['warnings']:
                    print(f"   - {warning}")

            total_missing += len(result['missing_capabilities'])
            total_capabilities += result['total_count']

        # Summary
        print("\n" + "=" * 80)
        print("📊 AUDIT SUMMARY")
        print("=" * 80)
        print(f"Total Heroes Audited: {len(heroes)}")
        print(f"Total Capabilities Checked: {total_capabilities}")
        print(f"Total Missing Capabilities: {total_missing}")
        print(f"Overall Readiness: {((total_capabilities - total_missing) / total_capabilities * 100):.1f}%")

        if total_missing == 0:
            print("\n✅ ALL HEROES ARE FULLY OPERATIONAL!")
            print("🦸 The Justice League is ready for action!")
        else:
            print(f"\n⚠️  {total_missing} capabilities need attention")
            print("Recommendations will follow...")

        return self.audit_results

    def _load_hero_module(self, module_name: str):
        """Load a hero module dynamically"""
        module_path = self.heroes_path / f"{module_name}.py"
        if not module_path.exists():
            return None

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def _check_capability(self, module, attr_name: str, attr_type: str = 'any') -> bool:
        """Check if a capability exists in the module"""
        if not hasattr(module, attr_name):
            return False

        attr = getattr(module, attr_name)

        if attr_type == 'class':
            return isinstance(attr, type)
        elif attr_type == 'function':
            return callable(attr)

        return True

    def _audit_superman(self, module) -> Dict[str, Any]:
        """Audit Superman's coordination capabilities"""
        required = [
            ('SupermanCoordinator', 'class', 'Main coordination class'),
            ('assemble_justice_league', 'function', 'Main league assembly function'),
        ]

        missing = []
        warnings = []
        present = 0

        # Check class exists
        if self._check_capability(module, 'SupermanCoordinator', 'class'):
            present += 1
            cls = getattr(module, 'SupermanCoordinator')

            # Check required methods
            required_methods = [
                'assemble_justice_league',
                '_calculate_justice_league_score',
                '_deploy_batman',
                '_deploy_green_lantern',
                '_deploy_wonder_woman',
                '_deploy_flash',
                '_deploy_aquaman',
                '_deploy_cyborg',
                '_deploy_atom'
            ]

            for method in required_methods:
                if hasattr(cls, method):
                    present += 1
                else:
                    missing.append({
                        'name': f'SupermanCoordinator.{method}',
                        'description': f'Method to coordinate heroes',
                        'type': 'method'
                    })
        else:
            missing.append({
                'name': 'SupermanCoordinator',
                'description': 'Main coordination class',
                'type': 'class'
            })

        # Check standalone function
        if self._check_capability(module, 'assemble_justice_league', 'function'):
            present += 1
        else:
            missing.append({
                'name': 'assemble_justice_league',
                'description': 'Standalone league assembly function',
                'type': 'function'
            })

        total = len(required) + len(required_methods)
        score = (present / total * 100) if total > 0 else 0

        return {
            'status': 'READY' if not missing else 'INCOMPLETE',
            'present_count': present,
            'total_count': total,
            'missing_capabilities': missing,
            'warnings': warnings,
            'score': score
        }

    def _audit_batman(self, module) -> Dict[str, Any]:
        """Audit Batman's testing capabilities"""
        missing = []
        warnings = []
        present = 0

        # Check class
        if self._check_capability(module, 'BatmanTesting', 'class'):
            present += 1
            cls = getattr(module, 'BatmanTesting')

            # Required testing methods
            required_methods = [
                'test_all_interactive_elements',
                '_test_buttons',
                '_test_links',
                '_test_inputs',
                '_test_forms',
                '_test_keyboard_navigation',
                '_test_focus_management',
                '_extract_interactive_elements',
                '_calculate_batman_score',
                '_generate_batman_recommendations'
            ]

            for method in required_methods:
                if hasattr(cls, method):
                    present += 1
                else:
                    missing.append({
                        'name': f'BatmanTesting.{method}',
                        'description': f'Testing method for interactive elements',
                        'type': 'method'
                    })
        else:
            missing.append({
                'name': 'BatmanTesting',
                'description': 'Main testing class',
                'type': 'class'
            })

        # Check standalone function
        if self._check_capability(module, 'batman_test_interactive', 'function'):
            present += 1
        else:
            missing.append({
                'name': 'batman_test_interactive',
                'description': 'Standalone testing function',
                'type': 'function'
            })

        # Check MCP integration
        if not missing:
            # Batman needs MCP Chrome DevTools
            warnings.append("Requires MCP Chrome DevTools (click, fill, take_snapshot)")

        total = 12  # 1 class + 10 methods + 1 function
        score = (present / total * 100) if total > 0 else 0

        return {
            'status': 'READY' if not missing else 'INCOMPLETE',
            'present_count': present,
            'total_count': total,
            'missing_capabilities': missing,
            'warnings': warnings,
            'score': score
        }

    def _audit_green_lantern(self, module) -> Dict[str, Any]:
        """Audit Green Lantern's visual regression capabilities"""
        missing = []
        warnings = []
        present = 0

        if self._check_capability(module, 'GreenLanternVisual', 'class'):
            present += 1
            cls = getattr(module, 'GreenLanternVisual')

            required_methods = [
                'compare_to_baseline',
                'create_baseline',
                'batch_compare',
                '_calculate_ssim',
                '_generate_diff_image',
                '_calculate_green_lantern_score',
                '_generate_willpower_recommendations',
                '_load_baseline',
                '_save_baseline'
            ]

            for method in required_methods:
                if hasattr(cls, method):
                    present += 1
                else:
                    missing.append({
                        'name': f'GreenLanternVisual.{method}',
                        'description': 'Visual regression method',
                        'type': 'method'
                    })
        else:
            missing.append({
                'name': 'GreenLanternVisual',
                'description': 'Main visual regression class',
                'type': 'class'
            })

        if self._check_capability(module, 'green_lantern_visual_regression', 'function'):
            present += 1
        else:
            missing.append({
                'name': 'green_lantern_visual_regression',
                'description': 'Standalone visual regression function',
                'type': 'function'
            })

        # Check dependencies
        try:
            from PIL import Image
            from skimage.metrics import structural_similarity as ssim
            import numpy as np
        except ImportError as e:
            warnings.append(f"Missing dependency: {e.name}")

        total = 11  # 1 class + 9 methods + 1 function
        score = (present / total * 100) if total > 0 else 0

        return {
            'status': 'READY' if not missing else 'INCOMPLETE',
            'present_count': present,
            'total_count': total,
            'missing_capabilities': missing,
            'warnings': warnings,
            'score': score
        }

    def _audit_wonder_woman(self, module) -> Dict[str, Any]:
        """Audit Wonder Woman's accessibility capabilities"""
        missing = []
        warnings = []
        present = 0

        if self._check_capability(module, 'WonderWomanAccessibility', 'class'):
            present += 1
            cls = getattr(module, 'WonderWomanAccessibility')

            required_methods = [
                'champion_accessibility_analysis',
                '_wield_lasso_of_truth',
                '_analyze_colors_with_bracers',
                '_deploy_invisible_jet',
                '_amazon_vision_analysis',
                '_calculate_champion_score',
                '_create_battle_plan',
                '_calculate_wcag_scores'
            ]

            for method in required_methods:
                if hasattr(cls, method):
                    present += 1
                else:
                    missing.append({
                        'name': f'WonderWomanAccessibility.{method}',
                        'description': 'Accessibility analysis method',
                        'type': 'method'
                    })
        else:
            missing.append({
                'name': 'WonderWomanAccessibility',
                'description': 'Main accessibility class',
                'type': 'class'
            })

        if self._check_capability(module, 'wonder_woman_accessibility_analysis', 'function'):
            present += 1
        else:
            missing.append({
                'name': 'wonder_woman_accessibility_analysis',
                'description': 'Standalone accessibility function',
                'type': 'function'
            })

        # Check optional but recommended tools
        optional_tools = []
        try:
            from colormath.color_objects import sRGBColor, LabColor
            from colormath.color_conversions import convert_color
            from colormath.color_diff import delta_e_cie2000
        except ImportError:
            optional_tools.append("colormath (for advanced color analysis)")

        if optional_tools:
            warnings.append(f"Optional tools available: {', '.join(optional_tools)}")

        total = 10  # 1 class + 8 methods + 1 function
        score = (present / total * 100) if total > 0 else 0

        return {
            'status': 'READY' if not missing else 'INCOMPLETE',
            'present_count': present,
            'total_count': total,
            'missing_capabilities': missing,
            'warnings': warnings,
            'score': score
        }

    def _audit_flash(self, module) -> Dict[str, Any]:
        """Audit Flash's performance capabilities"""
        missing = []
        warnings = []
        present = 0

        if self._check_capability(module, 'FlashPerformance', 'class'):
            present += 1
            cls = getattr(module, 'FlashPerformance')

            required_methods = [
                'profile_performance',
                '_extract_core_web_vitals',
                '_calculate_speed_score',
                '_generate_lightning_recommendations',
                '_check_for_regression',
                '_store_baseline',
                '_load_baseline'
            ]

            for method in required_methods:
                if hasattr(cls, method):
                    present += 1
                else:
                    missing.append({
                        'name': f'FlashPerformance.{method}',
                        'description': 'Performance profiling method',
                        'type': 'method'
                    })
        else:
            missing.append({
                'name': 'FlashPerformance',
                'description': 'Main performance class',
                'type': 'class'
            })

        if self._check_capability(module, 'flash_profile_performance', 'function'):
            present += 1
        else:
            missing.append({
                'name': 'flash_profile_performance',
                'description': 'Standalone performance function',
                'type': 'function'
            })

        warnings.append("Requires MCP Chrome DevTools Performance API")

        total = 9  # 1 class + 7 methods + 1 function
        score = (present / total * 100) if total > 0 else 0

        return {
            'status': 'READY' if not missing else 'INCOMPLETE',
            'present_count': present,
            'total_count': total,
            'missing_capabilities': missing,
            'warnings': warnings,
            'score': score
        }

    def _audit_aquaman(self, module) -> Dict[str, Any]:
        """Audit Aquaman's network capabilities"""
        missing = []
        warnings = []
        present = 0

        if self._check_capability(module, 'AquamanNetwork', 'class'):
            present += 1
            cls = getattr(module, 'AquamanNetwork')

            required_methods = [
                'analyze_network_traffic',
                '_analyze_request_types',
                '_analyze_timing_waterfall',
                '_detect_blocking_resources',
                '_identify_critical_path',
                '_analyze_cache_efficiency',
                '_track_third_party_resources',
                '_calculate_aquaman_score',
                '_generate_ocean_recommendations'
            ]

            for method in required_methods:
                if hasattr(cls, method):
                    present += 1
                else:
                    missing.append({
                        'name': f'AquamanNetwork.{method}',
                        'description': 'Network analysis method',
                        'type': 'method'
                    })
        else:
            missing.append({
                'name': 'AquamanNetwork',
                'description': 'Main network analysis class',
                'type': 'class'
            })

        if self._check_capability(module, 'aquaman_analyze_network', 'function'):
            present += 1
        else:
            missing.append({
                'name': 'aquaman_analyze_network',
                'description': 'Standalone network function',
                'type': 'function'
            })

        warnings.append("Requires MCP Chrome DevTools Network API")

        total = 11  # 1 class + 9 methods + 1 function
        score = (present / total * 100) if total > 0 else 0

        return {
            'status': 'READY' if not missing else 'INCOMPLETE',
            'present_count': present,
            'total_count': total,
            'missing_capabilities': missing,
            'warnings': warnings,
            'score': score
        }

    def _audit_cyborg(self, module) -> Dict[str, Any]:
        """Audit Cyborg's integration capabilities"""
        missing = []
        warnings = []
        present = 0

        if self._check_capability(module, 'CyborgIntegrations', 'class'):
            present += 1
            cls = getattr(module, 'CyborgIntegrations')

            required_methods = [
                'connect_all_systems',
                '_connect_figma',
                '_connect_penpot',
                '_connect_github',
                '_connect_jira',
                '_connect_slack',
                'extract_figma_file',
                'extract_penpot_file',
                '_calculate_integration_score'
            ]

            for method in required_methods:
                if hasattr(cls, method):
                    present += 1
                else:
                    missing.append({
                        'name': f'CyborgIntegrations.{method}',
                        'description': 'Integration method',
                        'type': 'method'
                    })
        else:
            missing.append({
                'name': 'CyborgIntegrations',
                'description': 'Main integrations class',
                'type': 'class'
            })

        if self._check_capability(module, 'cyborg_connect_systems', 'function'):
            present += 1
        else:
            missing.append({
                'name': 'cyborg_connect_systems',
                'description': 'Standalone connection function',
                'type': 'function'
            })

        # Check for requests library
        try:
            import requests
        except ImportError:
            warnings.append("Missing dependency: requests (for API calls)")

        total = 11  # 1 class + 9 methods + 1 function
        score = (present / total * 100) if total > 0 else 0

        return {
            'status': 'READY' if not missing else 'INCOMPLETE',
            'present_count': present,
            'total_count': total,
            'missing_capabilities': missing,
            'warnings': warnings,
            'score': score
        }

    def _audit_atom(self, module) -> Dict[str, Any]:
        """Audit The Atom's component analysis capabilities"""
        missing = []
        warnings = []
        present = 0

        if self._check_capability(module, 'AtomComponentAnalysis', 'class'):
            present += 1
            cls = getattr(module, 'AtomComponentAnalysis')

            required_methods = [
                'analyze_component_library',
                '_categorize_components',
                '_enumerate_variants',
                '_detect_missing_variants',
                '_analyze_design_tokens',
                '_check_naming_conventions',
                '_analyze_component_hierarchy',
                '_calculate_atom_score',
                '_generate_molecular_recommendations'
            ]

            for method in required_methods:
                if hasattr(cls, method):
                    present += 1
                else:
                    missing.append({
                        'name': f'AtomComponentAnalysis.{method}',
                        'description': 'Component analysis method',
                        'type': 'method'
                    })
        else:
            missing.append({
                'name': 'AtomComponentAnalysis',
                'description': 'Main component analysis class',
                'type': 'class'
            })

        if self._check_capability(module, 'atom_analyze_components', 'function'):
            present += 1
        else:
            missing.append({
                'name': 'atom_analyze_components',
                'description': 'Standalone component function',
                'type': 'function'
            })

        total = 11  # 1 class + 9 methods + 1 function
        score = (present / total * 100) if total > 0 else 0

        return {
            'status': 'READY' if not missing else 'INCOMPLETE',
            'present_count': present,
            'total_count': total,
            'missing_capabilities': missing,
            'warnings': warnings,
            'score': score
        }

    def _audit_green_arrow(self, module) -> Dict[str, Any]:
        """Audit Green Arrow's QA testing capabilities"""
        missing = []
        warnings = []
        present = 0

        if self._check_capability(module, 'GreenArrowTesting', 'class'):
            present += 1
            cls = getattr(module, 'GreenArrowTesting')

            required_methods = [
                'test_justice_league',
                '_fire_standard_arrow',
                '_fire_explosive_arrow',
                '_fire_net_arrow',
                '_fire_fire_arrow',
                '_fire_boxing_glove_arrow',
                '_fire_trick_arrow',
                '_fire_emp_arrow',
                '_calculate_test_score',
                '_generate_precision_recommendations'
            ]

            for method in required_methods:
                if hasattr(cls, method):
                    present += 1
                else:
                    missing.append({
                        'name': f'GreenArrowTesting.{method}',
                        'description': 'Testing arrow method',
                        'type': 'method'
                    })
        else:
            missing.append({
                'name': 'GreenArrowTesting',
                'description': 'Main QA testing class',
                'type': 'class'
            })

        if self._check_capability(module, 'green_arrow_test_league', 'function'):
            present += 1
        else:
            missing.append({
                'name': 'green_arrow_test_league',
                'description': 'Standalone testing function',
                'type': 'function'
            })

        total = 12  # 1 class + 10 methods + 1 function
        score = (present / total * 100) if total > 0 else 0

        return {
            'status': 'READY' if not missing else 'INCOMPLETE',
            'present_count': present,
            'total_count': total,
            'missing_capabilities': missing,
            'warnings': warnings,
            'score': score
        }


if __name__ == '__main__':
    auditor = JusticeLeagueAuditor()
    results = auditor.audit_all_heroes()

    # Exit with appropriate code
    total_missing = sum(len(r['missing_capabilities']) for r in results.values())
    sys.exit(0 if total_missing == 0 else 1)
