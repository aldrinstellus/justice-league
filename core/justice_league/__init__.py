"""
🦸 JUSTICE LEAGUE - Aldo Vision's Superhero Team
Each hero has specialized powers for design analysis

Members:
- 🦸 Superman (Coordinator) - Assembles and coordinates all heroes
- 🦇 Batman (Testing) - Interactive element testing specialist
- 💚 Green Lantern (Visual) - Visual regression guardian
- ⚡ Wonder Woman (Accessibility) - Accessibility champion
- ⚡ Flash (Performance) - Speed and performance analyzer
- 🌊 Aquaman (Network) - Network traffic commander
- 🤖 Cyborg (Integrations) - External API integration master
- 🔬 The Atom (Components) - Component library analyzer

"Together, we make designs perfect!"

Architecture: Each hero is a specialized module (~300-500 lines) with focused responsibility.
Superman coordinates all heroes for complete analysis.
"""

# Import all Justice League heroes
from .batman_testing import batman_test_interactive_elements, BatmanTesting
from .green_lantern_visual import (
    green_lantern_store_baseline,
    green_lantern_compare_screenshots,
    green_lantern_list_baselines,
    green_lantern_delete_baseline,
    GreenLanternVisual
)
from .wonder_woman_accessibility import (
    wonder_woman_accessibility_analysis,
    WonderWomanAccessibility
)
from .flash_performance import flash_profile_performance, FlashPerformance
from .aquaman_network import aquaman_analyze_network, AquamanNetwork
from .cyborg_integrations import (
    cyborg_connect_systems,
    cyborg_extract_figma,
    cyborg_extract_penpot,
    cyborg_integration_report,
    CyborgIntegrations
)
from .atom_component_analysis import atom_analyze_components, AtomComponentAnalysis
from .superman_coordinator import assemble_justice_league, SupermanCoordinator

__all__ = [
    # Batman (Interactive Testing)
    'batman_test_interactive_elements',
    'BatmanTesting',

    # Green Lantern (Visual Regression)
    'green_lantern_store_baseline',
    'green_lantern_compare_screenshots',
    'green_lantern_list_baselines',
    'green_lantern_delete_baseline',
    'GreenLanternVisual',

    # Wonder Woman (Accessibility)
    'wonder_woman_accessibility_analysis',
    'WonderWomanAccessibility',

    # Flash (Performance)
    'flash_profile_performance',
    'FlashPerformance',

    # Aquaman (Network)
    'aquaman_analyze_network',
    'AquamanNetwork',

    # Cyborg (Integrations)
    'cyborg_connect_systems',
    'cyborg_extract_figma',
    'cyborg_extract_penpot',
    'cyborg_integration_report',
    'CyborgIntegrations',

    # The Atom (Component Analysis)
    'atom_analyze_components',
    'AtomComponentAnalysis',

    # Superman (Coordinator)
    'assemble_justice_league',
    'SupermanCoordinator',
]

__version__ = '1.0.0'
__league__ = 'Justice League of Aldo Vision'
__heroes__ = 8
