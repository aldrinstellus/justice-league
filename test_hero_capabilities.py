#!/usr/bin/env python3
"""
🏹 GREEN ARROW - HERO CAPABILITY AUDIT
Tests if each hero has all the tools/dependencies they need for their job
"""

import sys
from typing import Dict, List, Any

def audit_batman() -> Dict[str, Any]:
    """🦇 Audit Batman's testing capabilities"""
    print("\n🦇 BATMAN - The Testing Detective")
    print("=" * 60)

    capabilities = {
        'hero': 'Batman',
        'role': 'Interactive Testing',
        'tools_needed': [],
        'tools_available': [],
        'missing_tools': [],
        'status': 'unknown'
    }

    # Check if Batman can import
    try:
        from core.justice_league import BatmanTesting
        capabilities['tools_available'].append('✅ BatmanTesting class')
        print("✅ Batman class available")
    except Exception as e:
        capabilities['missing_tools'].append(f'❌ BatmanTesting class: {e}')
        print(f"❌ Batman class failed: {e}")

    # Check Batman's core methods
    try:
        from core.justice_league import BatmanTesting
        batman = BatmanTesting()

        # Check key methods exist
        methods = [
            'test_all_interactive_elements',
            '_extract_interactive_elements',
            '_test_buttons',
            '_test_links',
            '_test_inputs',
            '_test_keyboard_navigation'
        ]

        for method in methods:
            if hasattr(batman, method):
                capabilities['tools_available'].append(f'✅ {method}()')
                print(f"  ✅ {method}()")
            else:
                capabilities['missing_tools'].append(f'❌ {method}()')
                print(f"  ❌ Missing: {method}()")

        # Check what Batman needs to work
        print("\n  🦇 Batman needs:")
        print("    - page_snapshot (DOM snapshot) ⚠️ Provided by caller")
        print("    - mcp_tools (Chrome DevTools) ⚠️ Provided by caller")
        print("      - mcp__chrome_devtools__click")
        print("      - mcp__chrome_devtools__fill")
        print("      - mcp__chrome_devtools__hover")

    except Exception as e:
        capabilities['missing_tools'].append(f'❌ Batman methods: {e}')
        print(f"❌ Batman audit failed: {e}")

    capabilities['status'] = 'ready' if not capabilities['missing_tools'] else 'missing_dependencies'
    return capabilities


def audit_green_lantern() -> Dict[str, Any]:
    """💚 Audit Green Lantern's visual regression capabilities"""
    print("\n💚 GREEN LANTERN - The Visual Guardian")
    print("=" * 60)

    capabilities = {
        'hero': 'Green Lantern',
        'role': 'Visual Regression',
        'tools_needed': [],
        'tools_available': [],
        'missing_tools': [],
        'status': 'unknown'
    }

    # Check Pillow (PIL)
    try:
        from PIL import Image, ImageDraw, ImageFont
        capabilities['tools_available'].append('✅ Pillow (PIL) - Image processing')
        print("✅ Pillow (PIL) available")
    except ImportError:
        capabilities['missing_tools'].append('❌ Pillow (PIL) - pip install Pillow')
        print("❌ Pillow (PIL) missing - pip install Pillow")

    # Check NumPy
    try:
        import numpy as np
        capabilities['tools_available'].append('✅ NumPy - Pixel math')
        print("✅ NumPy available")
    except ImportError:
        capabilities['missing_tools'].append('❌ NumPy - pip install numpy')
        print("❌ NumPy missing - pip install numpy")

    # Check scikit-image (SSIM)
    try:
        from skimage.metrics import structural_similarity as ssim
        capabilities['tools_available'].append('✅ scikit-image - SSIM algorithm')
        print("✅ scikit-image available")
    except ImportError:
        capabilities['missing_tools'].append('❌ scikit-image - pip install scikit-image')
        print("❌ scikit-image missing - pip install scikit-image")

    # Check Green Lantern class
    try:
        from core.justice_league import GreenLanternVisual
        gl = GreenLanternVisual()
        capabilities['tools_available'].append('✅ GreenLanternVisual class')
        print("✅ Green Lantern class available")

        print("\n  💚 Green Lantern needs:")
        print("    - screenshot_path (PNG/JPG image) ⚠️ Provided by caller")

    except Exception as e:
        capabilities['missing_tools'].append(f'❌ GreenLanternVisual: {e}')
        print(f"❌ Green Lantern failed: {e}")

    capabilities['status'] = 'ready' if not capabilities['missing_tools'] else 'missing_dependencies'
    return capabilities


def audit_wonder_woman() -> Dict[str, Any]:
    """⚡ Audit Wonder Woman's accessibility capabilities"""
    print("\n⚡ WONDER WOMAN - The Accessibility Champion")
    print("=" * 60)

    capabilities = {
        'hero': 'Wonder Woman',
        'role': 'Accessibility',
        'tools_needed': [],
        'tools_available': [],
        'missing_tools': [],
        'status': 'unknown'
    }

    # Check world_class_accessibility
    try:
        from core.world_class_accessibility import WorldClassAccessibilityAnalyzer
        capabilities['tools_available'].append('✅ WorldClassAccessibilityAnalyzer')
        print("✅ WorldClassAccessibilityAnalyzer available")
    except ImportError as e:
        capabilities['missing_tools'].append(f'❌ WorldClassAccessibilityAnalyzer: {e}')
        print(f"❌ WorldClassAccessibilityAnalyzer missing: {e}")

    # Check optional: axe-core
    try:
        from axe_selenium_python import Axe
        capabilities['tools_available'].append('✅ axe-selenium-python (optional)')
        print("✅ axe-selenium-python available (Lasso of Truth)")
    except ImportError:
        capabilities['tools_available'].append('⚠️ axe-selenium-python (optional) - pip install axe-selenium-python')
        print("⚠️ axe-selenium-python missing (optional)")

    # Check optional: colormath
    try:
        from colormath.color_objects import sRGBColor
        capabilities['tools_available'].append('✅ colormath (optional)')
        print("✅ colormath available (Bracers of Submission)")
    except ImportError:
        capabilities['tools_available'].append('⚠️ colormath (optional) - pip install colormath')
        print("⚠️ colormath missing (optional)")

    # Check optional: Playwright
    try:
        from playwright.sync_api import sync_playwright
        capabilities['tools_available'].append('✅ Playwright (optional)')
        print("✅ Playwright available (Invisible Jet)")
    except ImportError:
        capabilities['tools_available'].append('⚠️ Playwright (optional) - pip install playwright')
        print("⚠️ Playwright missing (optional)")

    # Check Wonder Woman class
    try:
        from core.justice_league import WonderWomanAccessibility
        ww = WonderWomanAccessibility()
        capabilities['tools_available'].append('✅ WonderWomanAccessibility class')
        print("✅ Wonder Woman class available")

        print("\n  ⚡ Wonder Woman needs:")
        print("    - design_data (extracted components) ⚠️ Provided by caller")

    except Exception as e:
        capabilities['missing_tools'].append(f'❌ WonderWomanAccessibility: {e}')
        print(f"❌ Wonder Woman failed: {e}")

    capabilities['status'] = 'ready' if not capabilities['missing_tools'] else 'missing_dependencies'
    return capabilities


def audit_flash() -> Dict[str, Any]:
    """⚡ Audit Flash's performance capabilities"""
    print("\n⚡ THE FLASH - The Speed Analyzer")
    print("=" * 60)

    capabilities = {
        'hero': 'Flash',
        'role': 'Performance',
        'tools_needed': [],
        'tools_available': [],
        'missing_tools': [],
        'status': 'unknown'
    }

    # Check Flash class
    try:
        from core.justice_league import FlashPerformance
        flash = FlashPerformance()
        capabilities['tools_available'].append('✅ FlashPerformance class')
        print("✅ Flash class available")

        print("\n  ⚡ Flash needs:")
        print("    - mcp_tools (Chrome DevTools) ⚠️ Provided by caller")
        print("      - mcp__chrome_devtools__performance_start_trace()")
        print("      - mcp__chrome_devtools__performance_stop_trace()")
        print("      - mcp__chrome_devtools__performance_analyze_insight()")

    except Exception as e:
        capabilities['missing_tools'].append(f'❌ FlashPerformance: {e}')
        print(f"❌ Flash failed: {e}")

    capabilities['status'] = 'ready' if not capabilities['missing_tools'] else 'missing_dependencies'
    return capabilities


def audit_aquaman() -> Dict[str, Any]:
    """🌊 Audit Aquaman's network capabilities"""
    print("\n🌊 AQUAMAN - The Network Commander")
    print("=" * 60)

    capabilities = {
        'hero': 'Aquaman',
        'role': 'Network',
        'tools_needed': [],
        'tools_available': [],
        'missing_tools': [],
        'status': 'unknown'
    }

    # Check Aquaman class
    try:
        from core.justice_league import AquamanNetwork
        aquaman = AquamanNetwork()
        capabilities['tools_available'].append('✅ AquamanNetwork class')
        print("✅ Aquaman class available")

        print("\n  🌊 Aquaman needs:")
        print("    - mcp_tools (Chrome DevTools) ⚠️ Provided by caller")
        print("      - mcp__chrome_devtools__list_network_requests()")
        print("      - mcp__chrome_devtools__get_network_request()")

    except Exception as e:
        capabilities['missing_tools'].append(f'❌ AquamanNetwork: {e}')
        print(f"❌ Aquaman failed: {e}")

    capabilities['status'] = 'ready' if not capabilities['missing_tools'] else 'missing_dependencies'
    return capabilities


def audit_cyborg() -> Dict[str, Any]:
    """🤖 Audit Cyborg's integration capabilities"""
    print("\n🤖 CYBORG - The Integration Master")
    print("=" * 60)

    capabilities = {
        'hero': 'Cyborg',
        'role': 'Integrations',
        'tools_needed': [],
        'tools_available': [],
        'missing_tools': [],
        'status': 'unknown'
    }

    # Check Cyborg class
    try:
        from core.justice_league import CyborgIntegrations
        cyborg = CyborgIntegrations()
        capabilities['tools_available'].append('✅ CyborgIntegrations class')
        print("✅ Cyborg class available")

        # Check if Penpot connector exists
        try:
            from core.penpot_api_connector import PenpotAPIConnector
            capabilities['tools_available'].append('✅ Penpot API Connector')
            print("✅ Penpot API Connector available")
        except ImportError:
            capabilities['tools_available'].append('⚠️ Penpot API Connector (optional)')
            print("⚠️ Penpot API Connector missing (optional)")

        print("\n  🤖 Cyborg can connect to:")
        print("    ✅ Figma API (needs access_token)")
        print("    ✅ Penpot API (needs api_key)")
        print("    ✅ GitHub API (needs access_token)")
        print("    ✅ Jira API (needs api_token + domain)")
        print("    ✅ Slack Webhooks (needs webhook_url)")

    except Exception as e:
        capabilities['missing_tools'].append(f'❌ CyborgIntegrations: {e}')
        print(f"❌ Cyborg failed: {e}")

    capabilities['status'] = 'ready' if not capabilities['missing_tools'] else 'missing_dependencies'
    return capabilities


def audit_atom() -> Dict[str, Any]:
    """🔬 Audit The Atom's component capabilities"""
    print("\n🔬 THE ATOM - The Component Analyzer")
    print("=" * 60)

    capabilities = {
        'hero': 'The Atom',
        'role': 'Component Analysis',
        'tools_needed': [],
        'tools_available': [],
        'missing_tools': [],
        'status': 'unknown'
    }

    # Check Atom class
    try:
        from core.justice_league import AtomComponentAnalysis
        atom = AtomComponentAnalysis()
        capabilities['tools_available'].append('✅ AtomComponentAnalysis class')
        print("✅ The Atom class available")

        print("\n  🔬 The Atom needs:")
        print("    - components (component library dict) ⚠️ Provided by caller")
        print("    - design_tokens (optional)")

    except Exception as e:
        capabilities['missing_tools'].append(f'❌ AtomComponentAnalysis: {e}')
        print(f"❌ The Atom failed: {e}")

    capabilities['status'] = 'ready' if not capabilities['missing_tools'] else 'missing_dependencies'
    return capabilities


def audit_superman() -> Dict[str, Any]:
    """🦸 Audit Superman's coordination capabilities"""
    print("\n🦸 SUPERMAN - The Coordinator")
    print("=" * 60)

    capabilities = {
        'hero': 'Superman',
        'role': 'Coordination',
        'tools_needed': [],
        'tools_available': [],
        'missing_tools': [],
        'status': 'unknown'
    }

    # Check Superman class
    try:
        from core.justice_league import SupermanCoordinator
        superman = SupermanCoordinator()
        capabilities['tools_available'].append('✅ SupermanCoordinator class')
        print("✅ Superman class available")

        # Check how many heroes Superman can deploy
        heroes_available = superman.heroes_available
        print(f"\n  🦸 Superman can deploy: {heroes_available}/7 heroes")

        if superman.batman:
            print("    ✅ Batman available")
        if superman.green_lantern:
            print("    ✅ Green Lantern available")
        if superman.wonder_woman:
            print("    ✅ Wonder Woman available")
        if superman.flash:
            print("    ✅ Flash available")
        if superman.aquaman:
            print("    ✅ Aquaman available")
        if superman.cyborg:
            print("    ✅ Cyborg available")
        if superman.atom:
            print("    ✅ The Atom available")

        capabilities['tools_available'].append(f'✅ {heroes_available}/7 heroes available')

    except Exception as e:
        capabilities['missing_tools'].append(f'❌ SupermanCoordinator: {e}')
        print(f"❌ Superman failed: {e}")

    capabilities['status'] = 'ready' if not capabilities['missing_tools'] else 'missing_dependencies'
    return capabilities


def audit_green_arrow() -> Dict[str, Any]:
    """🏹 Audit Green Arrow's testing capabilities"""
    print("\n🏹 GREEN ARROW - The Precision Tester")
    print("=" * 60)

    capabilities = {
        'hero': 'Green Arrow',
        'role': 'QA Testing',
        'tools_needed': [],
        'tools_available': [],
        'missing_tools': [],
        'status': 'unknown'
    }

    # Check Green Arrow class
    try:
        from core.justice_league import GreenArrowTesting
        ga = GreenArrowTesting()
        capabilities['tools_available'].append('✅ GreenArrowTesting class')
        print("✅ Green Arrow class available")

        print("\n  🏹 Green Arrow's Quiver:")
        for arrow_type, description in ga.quiver.items():
            print(f"    {description}")

    except Exception as e:
        capabilities['missing_tools'].append(f'❌ GreenArrowTesting: {e}')
        print(f"❌ Green Arrow failed: {e}")

    capabilities['status'] = 'ready' if not capabilities['missing_tools'] else 'missing_dependencies'
    return capabilities


def generate_audit_report(all_capabilities: List[Dict]) -> Dict[str, Any]:
    """Generate final audit report"""

    total_heroes = len(all_capabilities)
    ready_heroes = sum(1 for h in all_capabilities if h['status'] == 'ready')
    missing_deps = sum(1 for h in all_capabilities if h['status'] == 'missing_dependencies')

    report = {
        'total_heroes': total_heroes,
        'ready': ready_heroes,
        'missing_dependencies': missing_deps,
        'readiness_percentage': (ready_heroes / total_heroes * 100) if total_heroes > 0 else 0,
        'heroes': all_capabilities
    }

    return report


if __name__ == '__main__':
    print("=" * 60)
    print("🏹 GREEN ARROW - HERO CAPABILITY AUDIT")
    print("=" * 60)
    print("Testing if each hero has what they need to do their job...")

    # Audit all heroes
    capabilities = [
        audit_superman(),
        audit_batman(),
        audit_green_lantern(),
        audit_wonder_woman(),
        audit_flash(),
        audit_aquaman(),
        audit_cyborg(),
        audit_atom(),
        audit_green_arrow()
    ]

    # Generate report
    report = generate_audit_report(capabilities)

    # Print summary
    print("\n" + "=" * 60)
    print("🏹 AUDIT SUMMARY")
    print("=" * 60)
    print(f"Total Heroes: {report['total_heroes']}")
    print(f"Ready for Duty: {report['ready']}/{report['total_heroes']}")
    print(f"Missing Dependencies: {report['missing_dependencies']}")
    print(f"Readiness: {report['readiness_percentage']:.1f}%")

    print("\n📊 HERO STATUS:")
    for hero_cap in capabilities:
        status_icon = '✅' if hero_cap['status'] == 'ready' else '⚠️'
        print(f"{status_icon} {hero_cap['hero']} ({hero_cap['role']}) - {hero_cap['status']}")

        if hero_cap['missing_tools']:
            print(f"   Missing:")
            for missing in hero_cap['missing_tools']:
                print(f"     {missing}")

    print("\n" + "=" * 60)

    if report['readiness_percentage'] >= 100:
        print("🏹 BULLSEYE! All heroes ready for duty!")
        print("🦸 'Together, we make designs perfect!'")
        sys.exit(0)
    elif report['readiness_percentage'] >= 75:
        print("🏹 Most heroes ready! Some optional tools missing.")
        sys.exit(0)
    else:
        print("🏹 ATTENTION! Critical dependencies missing!")
        sys.exit(1)
