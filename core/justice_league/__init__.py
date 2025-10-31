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
- 🏹 Green Arrow (QA) - Quality assurance and testing specialist
- 🧠 Martian Manhunter (Security) - Security vulnerability detection specialist
- 🤸 Plastic Man (Responsive) - Responsive design and mobile testing specialist
- 🎩 Zatanna (SEO) - SEO and metadata magic specialist
- 🪔 Litty (Ethics) - User empathy and ethical design validator
- 👁️ Vision Analyst (Visual Analysis) - Dashboard image analysis and measurement extraction specialist
- 💨 Quicksilver (Speed Optimizer) - High-speed parallel Figma operations specialist

"Together, we make designs perfect, secure, responsive, discoverable, ethical, and FAST!"

Architecture: Each hero is a specialized module (~300-600 lines) with focused responsibility.
Superman coordinates all heroes for complete analysis.
Green Arrow tests that everything works!
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
from .green_arrow_testing import green_arrow_test_league, GreenArrowTesting
from .martian_manhunter_security import martian_manhunter_security_scan, MartianManhunterSecurity
from .plastic_man_responsive import plastic_man_responsive_test, PlasticManResponsive
from .zatanna_seo import zatanna_seo_analysis, ZatannaSEO
from .litty_ethics import litty_validate_ethics, LittyEthics
from .artemis_codesmith import ArtemisCodeSmith
from .hephaestus_code_to_design import HephaestusCodeToDesign
from .vision_analyst import VisionAnalyst, vision_analyst
from .quicksilver_speed_export import QuicksilverSpeedExport, export_frames_quicksilver

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

    # Green Arrow (QA Testing)
    'green_arrow_test_league',
    'GreenArrowTesting',

    # Martian Manhunter (Security)
    'martian_manhunter_security_scan',
    'MartianManhunterSecurity',

    # Plastic Man (Responsive Design)
    'plastic_man_responsive_test',
    'PlasticManResponsive',

    # Zatanna (SEO & Metadata)
    'zatanna_seo_analysis',
    'ZatannaSEO',

    # Litty (User Empathy & Ethics)
    'litty_validate_ethics',
    'LittyEthics',

    # Artemis CodeSmith (Figma-to-Code Generator)
    'ArtemisCodeSmith',

    # Hephaestus (Code-to-Design Forger)
    'HephaestusCodeToDesign',

    # Vision Analyst (Visual Analysis)
    'VisionAnalyst',
    'vision_analyst',

    # Quicksilver (Speed Optimizer)
    'QuicksilverSpeedExport',
    'export_frames_quicksilver',
]

__version__ = '1.9.3'
__league__ = 'Justice League of Aldo Vision'
__heroes__ = 19
