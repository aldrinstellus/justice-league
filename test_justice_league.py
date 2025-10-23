#!/usr/bin/env python3
"""
🦸 JUSTICE LEAGUE TEST SUITE
Test the assembled Justice League on a real website
"""

from core.justice_league import assemble_justice_league, SupermanCoordinator

def test_superman_coordinator():
    """Test Superman can initialize and coordinate"""
    print("🦸 Testing Superman Coordinator initialization...")

    superman = SupermanCoordinator()
    print(f"  ✓ Superman initialized")
    print(f"  ✓ Heroes available: {superman.heroes_available}/7")

    return superman

def test_basic_mission():
    """Test a basic Justice League mission (without MCP tools)"""
    print("\n🦸 Testing basic Justice League mission...")

    # Simple mission without MCP tools (to test structure)
    mission = {
        'url': 'https://ui.shadcn.com/examples/dashboard',
        'mcp_tools': {},  # Empty for now
        'design_data': {
            'components': {
                'button-primary': {
                    'type': 'button',
                    'text': 'Click me',
                    'foreground_color': '#FFFFFF',
                    'background_color': '#3B82F6'
                }
            }
        },
        'components': {
            'button-primary': {
                'type': 'button',
                'text': 'Click me'
            }
        },
        'page_snapshot': '',  # Empty for now
        'screenshot_path': '',  # Empty for now
        'options': {
            'test_interactive': False,  # Skip Batman (needs snapshot)
            'test_visual': False,  # Skip GL (needs screenshot)
            'test_accessibility': True,  # Test Wonder Woman
            'test_performance': False,  # Skip Flash (needs MCP)
            'test_network': False,  # Skip Aquaman (needs MCP)
            'test_integrations': True,  # Test Cyborg
            'test_components': True,  # Test The Atom
        }
    }

    # Assemble the Justice League!
    results = assemble_justice_league(mission)

    print(f"\n🦸 JUSTICE LEAGUE MISSION RESULTS:")
    print(f"  Heroes deployed: {len(results['heroes_deployed'])}")
    for hero in results['heroes_deployed']:
        print(f"    - {hero}")

    print(f"\n  Justice League Score: {results['justice_league_score']['overall_score']:.1f}/100")
    print(f"  Grade: {results['justice_league_score']['grade']}")
    print(f"  Verdict: {results['justice_league_score']['verdict']}")

    return results

def test_individual_heroes():
    """Test each hero can be called individually"""
    print("\n🦸 Testing individual hero deployments...")

    # Test Batman (needs snapshot)
    print("\n🦇 Testing Batman...")
    from core.justice_league import BatmanTesting
    batman = BatmanTesting()
    print("  ✓ Batman initialized (needs DOM snapshot for actual testing)")

    # Test Green Lantern
    print("\n💚 Testing Green Lantern...")
    from core.justice_league import GreenLanternVisual
    gl = GreenLanternVisual()
    baselines = gl.list_baselines()
    print(f"  ✓ Green Lantern initialized - {len(baselines)} baselines stored")

    # Test Wonder Woman
    print("\n⚡ Testing Wonder Woman...")
    from core.justice_league import WonderWomanAccessibility
    ww = WonderWomanAccessibility()
    print("  ✓ Wonder Woman initialized")

    # Test Flash
    print("\n⚡ Testing Flash...")
    from core.justice_league import FlashPerformance
    flash = FlashPerformance()
    print("  ✓ Flash initialized (needs MCP tools for actual profiling)")

    # Test Aquaman
    print("\n🌊 Testing Aquaman...")
    from core.justice_league import AquamanNetwork
    aquaman = AquamanNetwork()
    print("  ✓ Aquaman initialized (needs MCP tools for network analysis)")

    # Test Cyborg
    print("\n🤖 Testing Cyborg...")
    from core.justice_league import CyborgIntegrations
    cyborg = CyborgIntegrations()
    report = cyborg.generate_integration_report()
    print(f"  ✓ Cyborg initialized - {len(report['available_integrations'])} integrations available")

    # Test The Atom
    print("\n🔬 Testing The Atom...")
    from core.justice_league import AtomComponentAnalysis
    atom = AtomComponentAnalysis()

    # Test with sample components
    sample_components = {
        'button-primary': {'type': 'button', 'text': 'Primary'},
        'button-secondary': {'type': 'button', 'text': 'Secondary'},
        'input-default': {'type': 'textbox'}
    }

    atom_results = atom.analyze_component_library(sample_components)
    print(f"  ✓ The Atom analyzed {atom_results['component_count']} components")
    print(f"  ✓ Component Score: {atom_results['atom_score']['score']:.1f}/100")

if __name__ == '__main__':
    print("=" * 60)
    print("🦸 JUSTICE LEAGUE TEST SUITE")
    print("=" * 60)

    # Test 1: Superman initialization
    superman = test_superman_coordinator()

    # Test 2: Individual heroes
    test_individual_heroes()

    # Test 3: Basic mission
    results = test_basic_mission()

    print("\n" + "=" * 60)
    print("🦸 ALL TESTS COMPLETE!")
    print("=" * 60)
    print("\n✅ Justice League is ready for action!")
    print("🦸 'Together, we make designs perfect!'")
