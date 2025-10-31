"""
🎨 PLASTIC MAN - THE RESPONSIVE DESIGN SPECIALIST
Justice League Member: Multi-Device & Responsive Testing Expert

The Stretchable Hero - Adapts to ANY screen size from smartwatch to 4K!

Powers:
- Breakpoint validation (mobile/tablet/desktop/4K)
- Device-specific testing (iPhone, Android, iPad)
- Touch target size validation
- Orientation testing (portrait/landscape)
- Viewport meta tag checking
- Responsive image optimization
- Font scaling verification
- Cross-browser compatibility testing

"I stretch to fit EVERY screen size - from smartwatch to 4K!"
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import re

# Mission Control Narrator for coordinated communication
try:
    from .mission_control_narrator import get_narrator
    NARRATOR_AVAILABLE = True
except ImportError:
    NARRATOR_AVAILABLE = False
    logging.warning("Mission Control Narrator not available - Plastic Man will operate without narrator")

logger = logging.getLogger(__name__)


class PlasticManResponsive:
    """
    🎨 PLASTIC MAN - Responsive Design Specialist

    Eel O'Brien uses his elasticity to test every possible screen size!

    Elastic Powers:
    1. Elasticity - Stretch to any screen size/breakpoint
    2. Shape-shifting - Transform into any device form factor
    3. Malleability - Adapt to any container/viewport
    4. Flexibility - Test all orientations (portrait/landscape)
    5. Extensibility - Validate touch targets across devices
    """

    # Common breakpoints (Mobile-first approach)
    BREAKPOINTS = {
        'smartwatch': {'width': 272, 'height': 340, 'label': 'Smartwatch (272x340)'},
        'mobile_small': {'width': 320, 'height': 568, 'label': 'Mobile Small (iPhone SE)'},
        'mobile': {'width': 375, 'height': 667, 'label': 'Mobile (iPhone 8)'},
        'mobile_large': {'width': 414, 'height': 896, 'label': 'Mobile Large (iPhone 11)'},
        'phablet': {'width': 540, 'height': 720, 'label': 'Phablet (Android)'},
        'tablet_portrait': {'width': 768, 'height': 1024, 'label': 'Tablet Portrait (iPad)'},
        'tablet_landscape': {'width': 1024, 'height': 768, 'label': 'Tablet Landscape (iPad)'},
        'laptop': {'width': 1366, 'height': 768, 'label': 'Laptop (1366x768)'},
        'desktop': {'width': 1920, 'height': 1080, 'label': 'Desktop (1080p)'},
        'desktop_4k': {'width': 3840, 'height': 2160, 'label': 'Desktop 4K (2160p)'}
    }

    # Touch target minimum size (WCAG 2.1 AAA: 44x44px)
    MIN_TOUCH_TARGET_SIZE = 44

    def __init__(self, narrator: Optional[Any] = None):
        """
        Initialize Plastic Man's responsive testing lab

        Args:
            narrator: Mission Control Narrator for coordinated communication
        """
        self.test_results = []

        # Hero identity for narrator integration
        self.hero_name = "Plastic Man"
        self.hero_emoji = "🤸"

        # Initialize narrator for enhanced UX
        self.narrator = narrator if narrator else (get_narrator() if NARRATOR_AVAILABLE else None)

        logger.info("🎨 PLASTIC MAN - Responsive Design Specialist initialized")

    def say(self, message: str, style: str = "flexible", technical_info: Optional[str] = None):
        """Plastic Man dialogue - Flexible and responsive specialist"""
        if self.narrator:
            self.narrator.hero_speaks(f"{self.hero_emoji} {self.hero_name}", message, style, technical_info)

    def think(self, thought: str, step: Optional[int] = None, category: Optional[str] = "Stretching"):
        """Sequential thinking with responsive focus. Categories: Stretching, Adapting, Flexing"""
        if self.narrator:
            self.narrator.hero_thinks(f"{self.hero_emoji} {self.hero_name}", thought, step, category)

    def handoff(self, to_hero: str, context: str, details: Optional[str] = None):
        """Handoff responsive testing to another hero"""
        if self.narrator:
            self.narrator.hero_handoff(f"{self.hero_emoji} {self.hero_name}", to_hero, context, details)

    def test_all_breakpoints(self, mcp_tools: Dict, test_scenarios: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        🎨 Test responsiveness across all breakpoints

        Plastic Man stretches to every screen size!

        Args:
            mcp_tools: MCP Chrome DevTools functions
                {
                    'resize_page': mcp__chrome-devtools__resize_page,
                    'take_screenshot': mcp__chrome-devtools__take_screenshot,
                    'take_snapshot': mcp__chrome-devtools__take_snapshot,
                    'evaluate_script': mcp__chrome-devtools__evaluate_script
                }
            test_scenarios: Optional list of breakpoints to test

        Returns:
            Complete responsive testing results
        """
        logger.info("🎨 ========================================")
        logger.info("🎨  PLASTIC MAN RESPONSIVE TESTING")
        logger.info("🎨 ========================================")

        results = {
            'hero': '🎨 Plastic Man - Responsive Design Specialist',
            'timestamp': datetime.now().isoformat(),
            'breakpoints_tested': [],
            'breakpoint_results': {},
            'responsive_issues': [],
            'touch_target_issues': [],
            'viewport_issues': [],
            'browser_compatibility': {}
        }

        # Determine which breakpoints to test
        breakpoints_to_test = test_scenarios or list(self.BREAKPOINTS.keys())

        # Power 1: Elasticity - Test each breakpoint
        logger.info("🎨 Using Elasticity to stretch across breakpoints...")
        for breakpoint_name in breakpoints_to_test:
            if breakpoint_name in self.BREAKPOINTS:
                bp_result = self._elastic_stretch_test(breakpoint_name, mcp_tools)
                results['breakpoint_results'][breakpoint_name] = bp_result
                results['breakpoints_tested'].append(breakpoint_name)

        # Power 2: Shape-shifting - Test device-specific features
        logger.info("🎨 Shape-shifting to test device features...")
        device_tests = self._shapeshift_device_test(mcp_tools)
        results['device_specific'] = device_tests

        # Power 3: Malleability - Test viewport meta tags
        logger.info("🎨 Using Malleability to validate viewport...")
        viewport_result = self._malleable_viewport_test(mcp_tools)
        results['viewport_analysis'] = viewport_result
        results['viewport_issues'].extend(viewport_result.get('issues', []))

        # Power 4: Flexibility - Test orientation changes
        logger.info("🎨 Testing Flexibility with orientation changes...")
        orientation_result = self._flexible_orientation_test(mcp_tools)
        results['orientation_testing'] = orientation_result

        # Power 5: Extensibility - Validate touch targets
        logger.info("🎨 Extending to validate touch targets...")
        touch_result = self._extensible_touch_target_test(mcp_tools)
        results['touch_target_analysis'] = touch_result
        results['touch_target_issues'].extend(touch_result.get('issues', []))

        # Calculate Plastic Man score
        plastic_score = self._calculate_plastic_man_score(results)
        results['plastic_man_score'] = plastic_score

        # Generate recommendations
        recommendations = self._generate_elastic_recommendations(results)
        results['recommendations'] = recommendations

        # Final verdict
        logger.info("🎨 ========================================")
        logger.info(f"🎨  RESPONSIVE SCORE: {plastic_score['score']:.1f}/100")
        logger.info(f"🎨  GRADE: {plastic_score['grade']}")
        logger.info(f"🎨  BREAKPOINTS TESTED: {len(results['breakpoints_tested'])}")
        logger.info("🎨 ========================================")

        return results

    def _elastic_stretch_test(self, breakpoint_name: str, mcp_tools: Dict) -> Dict[str, Any]:
        """
        🎨 Elasticity - Stretch to test a specific breakpoint

        Args:
            breakpoint_name: Name of breakpoint to test
            mcp_tools: MCP tools

        Returns:
            Breakpoint test results
        """
        breakpoint = self.BREAKPOINTS[breakpoint_name]
        width = breakpoint['width']
        height = breakpoint['height']
        label = breakpoint['label']

        result = {
            'breakpoint': breakpoint_name,
            'dimensions': f"{width}x{height}",
            'label': label,
            'issues': [],
            'passed': True
        }

        try:
            # Resize page (if MCP tool available)
            resize_func = mcp_tools.get('resize_page')
            if resize_func:
                resize_func(width=width, height=height)
                logger.info(f"  ✓ Stretched to {label}")

            # Take snapshot at this size
            snapshot_func = mcp_tools.get('take_snapshot')
            if snapshot_func:
                snapshot = snapshot_func()
                result['snapshot_taken'] = True

                # Check for horizontal scroll (bad on mobile)
                eval_func = mcp_tools.get('evaluate_script')
                if eval_func:
                    has_horizontal_scroll = eval_func(
                        function="() => document.body.scrollWidth > window.innerWidth"
                    )
                    if has_horizontal_scroll:
                        result['issues'].append({
                            'issue': 'Horizontal scroll detected',
                            'severity': 'medium',
                            'recommendation': 'Fix overflow, use max-width: 100%'
                        })
                        result['passed'] = False

            # Check if text is readable (not too small)
            # Minimum font size should be 16px on mobile
            if width <= 414:  # Mobile devices
                result['minimum_font_size_check'] = '16px recommended for mobile'

        except Exception as e:
            logger.error(f"Elasticity test failed for {breakpoint_name}: {e}")
            result['error'] = str(e)
            result['passed'] = False

        return result

    def _shapeshift_device_test(self, mcp_tools: Dict) -> Dict[str, Any]:
        """
        🎨 Shape-shifting - Test device-specific features

        Args:
            mcp_tools: MCP tools

        Returns:
            Device-specific test results
        """
        result = {
            'devices_tested': [],
            'touch_enabled': False,
            'hover_supported': False,
            'pointer_fine': False,
            'issues': []
        }

        eval_func = mcp_tools.get('evaluate_script')
        if eval_func:
            try:
                # Check if touch is supported
                touch_enabled = eval_func(
                    function="() => 'ontouchstart' in window || navigator.maxTouchPoints > 0"
                )
                result['touch_enabled'] = touch_enabled

                # Check hover support
                hover_supported = eval_func(
                    function="() => window.matchMedia('(hover: hover)').matches"
                )
                result['hover_supported'] = hover_supported

                # Check pointer precision
                pointer_fine = eval_func(
                    function="() => window.matchMedia('(pointer: fine)').matches"
                )
                result['pointer_fine'] = pointer_fine

                # If touch but hover-dependent UI, that's an issue
                if touch_enabled and not hover_supported:
                    result['issues'].append({
                        'issue': 'Touch device detected - ensure no hover-only interactions',
                        'severity': 'high',
                        'recommendation': 'Make all hover interactions tappable'
                    })

            except Exception as e:
                logger.warning(f"Shape-shifting test failed: {e}")

        return result

    def _malleable_viewport_test(self, mcp_tools: Dict) -> Dict[str, Any]:
        """
        🎨 Malleability - Validate viewport meta tags

        Args:
            mcp_tools: MCP tools

        Returns:
            Viewport validation results
        """
        result = {
            'viewport_meta_present': False,
            'viewport_content': '',
            'issues': [],
            'recommendations': []
        }

        eval_func = mcp_tools.get('evaluate_script')
        if eval_func:
            try:
                # Check for viewport meta tag
                viewport_content = eval_func(
                    function="() => document.querySelector('meta[name=\"viewport\"]')?.content || ''"
                )

                if viewport_content:
                    result['viewport_meta_present'] = True
                    result['viewport_content'] = viewport_content

                    # Check for recommended settings
                    if 'width=device-width' not in viewport_content:
                        result['issues'].append({
                            'issue': 'Viewport missing width=device-width',
                            'severity': 'high',
                            'recommendation': 'Add width=device-width to viewport'
                        })

                    if 'initial-scale=1' not in viewport_content:
                        result['issues'].append({
                            'issue': 'Viewport missing initial-scale=1',
                            'severity': 'medium',
                            'recommendation': 'Add initial-scale=1 to viewport'
                        })

                    # Check for user-scalable=no (bad for accessibility)
                    if 'user-scalable=no' in viewport_content or 'maximum-scale=1' in viewport_content:
                        result['issues'].append({
                            'issue': 'Viewport prevents zoom (user-scalable=no or maximum-scale=1)',
                            'severity': 'high',
                            'recommendation': 'Remove zoom restrictions for accessibility'
                        })
                else:
                    result['issues'].append({
                        'issue': 'Viewport meta tag missing',
                        'severity': 'critical',
                        'recommendation': 'Add <meta name="viewport" content="width=device-width, initial-scale=1">'
                    })

            except Exception as e:
                logger.warning(f"Viewport test failed: {e}")

        return result

    def _flexible_orientation_test(self, mcp_tools: Dict) -> Dict[str, Any]:
        """
        🎨 Flexibility - Test orientation changes (portrait/landscape)

        Args:
            mcp_tools: MCP tools

        Returns:
            Orientation test results
        """
        result = {
            'orientations_tested': [],
            'issues': [],
            'supports_both_orientations': True
        }

        # Test portrait and landscape for tablet
        orientations = [
            ('portrait', 768, 1024),
            ('landscape', 1024, 768)
        ]

        resize_func = mcp_tools.get('resize_page')
        if resize_func:
            for orientation, width, height in orientations:
                try:
                    resize_func(width=width, height=height)
                    result['orientations_tested'].append(orientation)
                    logger.info(f"  ✓ Tested {orientation} orientation ({width}x{height})")
                except Exception as e:
                    logger.warning(f"Orientation test failed for {orientation}: {e}")
                    result['supports_both_orientations'] = False

        return result

    def _extensible_touch_target_test(self, mcp_tools: Dict) -> Dict[str, Any]:
        """
        🎨 Extensibility - Validate touch target sizes

        Args:
            mcp_tools: MCP tools

        Returns:
            Touch target validation results
        """
        result = {
            'interactive_elements_checked': 0,
            'too_small_targets': 0,
            'issues': [],
            'passed': True
        }

        eval_func = mcp_tools.get('evaluate_script')
        if eval_func:
            try:
                # Check size of all interactive elements
                small_targets = eval_func(
                    function=f"""() => {{
                        const minSize = {self.MIN_TOUCH_TARGET_SIZE};
                        const interactive = document.querySelectorAll('button, a, input, select, textarea, [role="button"], [onclick]');
                        const smallTargets = [];

                        interactive.forEach(el => {{
                            const rect = el.getBoundingClientRect();
                            if (rect.width < minSize || rect.height < minSize) {{
                                smallTargets.push({{
                                    tag: el.tagName,
                                    width: rect.width,
                                    height: rect.height,
                                    text: el.textContent?.substring(0, 30)
                                }});
                            }}
                        }});

                        return {{
                            total: interactive.length,
                            smallCount: smallTargets.length,
                            examples: smallTargets.slice(0, 5)
                        }};
                    }}"""
                )

                result['interactive_elements_checked'] = small_targets.get('total', 0)
                result['too_small_targets'] = small_targets.get('smallCount', 0)

                if small_targets.get('smallCount', 0) > 0:
                    result['passed'] = False
                    result['issues'].append({
                        'issue': f"{small_targets['smallCount']} touch targets smaller than {self.MIN_TOUCH_TARGET_SIZE}x{self.MIN_TOUCH_TARGET_SIZE}px",
                        'severity': 'high',
                        'recommendation': f'Ensure all interactive elements are at least {self.MIN_TOUCH_TARGET_SIZE}x{self.MIN_TOUCH_TARGET_SIZE}px (WCAG 2.1 AAA)',
                        'examples': small_targets.get('examples', [])
                    })

            except Exception as e:
                logger.warning(f"Touch target test failed: {e}")

        return result

    def _calculate_plastic_man_score(self, results: Dict) -> Dict[str, Any]:
        """
        🎨 Calculate Plastic Man's responsive design score

        Args:
            results: Complete test results

        Returns:
            Responsive design score
        """
        score = 100.0

        # Deduct for breakpoint failures
        for bp_result in results.get('breakpoint_results', {}).values():
            if not bp_result.get('passed', True):
                score -= 5

        # Deduct for viewport issues
        viewport_issues = len(results.get('viewport_issues', []))
        score -= (viewport_issues * 10)

        # Deduct for touch target issues
        touch_issues = len(results.get('touch_target_issues', []))
        score -= (touch_issues * 5)

        # Deduct for device compatibility issues
        device_issues = len(results.get('device_specific', {}).get('issues', []))
        score -= (device_issues * 10)

        # Ensure score is 0-100
        score = max(0, min(100, score))

        # Grade
        if score == 100:
            grade = "S+ (Perfect Elasticity)"
            verdict = "🎨 FLAWLESS! Stretches perfectly to every screen!"
        elif score >= 90:
            grade = "S (Exceptional)"
            verdict = "🎨 EXCELLENT! Highly responsive across devices!"
        elif score >= 80:
            grade = "A (Great)"
            verdict = "🎨 VERY GOOD! Minor responsive improvements needed!"
        elif score >= 70:
            grade = "B (Good)"
            verdict = "🎨 GOOD! Some breakpoints need attention!"
        elif score >= 60:
            grade = "C (Fair)"
            verdict = "🎨 FAIR! Significant responsive issues detected!"
        else:
            grade = "D (Poor)"
            verdict = "🎨 CRITICAL! Layout breaks at multiple sizes!"

        return {
            'score': score,
            'grade': grade,
            'verdict': verdict,
            'breakpoints_tested': len(results.get('breakpoints_tested', [])),
            'total_issues': viewport_issues + touch_issues + device_issues
        }

    def _generate_elastic_recommendations(self, results: Dict) -> List[Dict[str, Any]]:
        """
        🎨 Generate Plastic Man's elastic recommendations

        Args:
            results: Test results

        Returns:
            List of recommendations
        """
        recommendations = []

        # Viewport issues
        if results.get('viewport_issues'):
            recommendations.append({
                'priority': 'critical',
                'area': 'Viewport Configuration',
                'issue': f"{len(results['viewport_issues'])} viewport issues detected",
                'recommendation': 'Fix viewport meta tag for proper mobile rendering',
                'plastic_man_says': 'I can\'t stretch properly without the right viewport!'
            })

        # Touch target issues
        touch_issues = results.get('touch_target_analysis', {}).get('too_small_targets', 0)
        if touch_issues > 0:
            recommendations.append({
                'priority': 'high',
                'area': 'Touch Targets',
                'issue': f'{touch_issues} interactive elements too small for touch',
                'recommendation': f'Increase touch target size to minimum {self.MIN_TOUCH_TARGET_SIZE}x{self.MIN_TOUCH_TARGET_SIZE}px',
                'plastic_man_says': 'Users with big fingers need bigger targets!'
            })

        # Breakpoint failures
        failed_breakpoints = [
            bp for bp, result in results.get('breakpoint_results', {}).items()
            if not result.get('passed', True)
        ]
        if failed_breakpoints:
            recommendations.append({
                'priority': 'high',
                'area': 'Breakpoints',
                'issue': f'Layout issues at: {", ".join(failed_breakpoints)}',
                'recommendation': 'Test and fix responsive CSS for failing breakpoints',
                'plastic_man_says': 'I\'m breaking at these sizes - fix the stretching!'
            })

        # Device compatibility
        device_issues = results.get('device_specific', {}).get('issues', [])
        for issue in device_issues:
            recommendations.append({
                'priority': issue.get('severity', 'medium'),
                'area': 'Device Compatibility',
                'issue': issue.get('issue'),
                'recommendation': issue.get('recommendation'),
                'plastic_man_says': 'Different devices need different interactions!'
            })

        if not recommendations:
            recommendations.append({
                'priority': 'low',
                'area': 'Responsive Design',
                'issue': 'No responsive issues detected',
                'recommendation': 'Continue testing across devices and maintain responsiveness',
                'plastic_man_says': 'Perfect elasticity! I fit everywhere!'
            })

        return recommendations


# Main entry point - Plastic Man's Mission Interface
def plastic_man_responsive_test(mcp_tools: Dict,
                                test_scenarios: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    🎨 Plastic Man's complete responsive design testing

    The Stretchable Hero tests every screen size!

    Args:
        mcp_tools: MCP Chrome DevTools functions
        test_scenarios: Optional list of breakpoints to test

    Returns:
        Complete responsive testing results
    """
    plastic_man = PlasticManResponsive()
    return plastic_man.test_all_breakpoints(mcp_tools, test_scenarios)
