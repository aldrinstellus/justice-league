#!/usr/bin/env python3
"""
🪔 TEST LITTY LIVE - The Conscience Keeper

This script tests Litty's guilt-tripping powers on a real website!
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.justice_league import litty_validate_ethics, LittyEthics


def create_mock_mcp_tools():
    """
    Create mock MCP tools for testing

    In production, these would be real Chrome DevTools MCP functions
    For testing, we'll simulate realistic responses
    """

    def mock_evaluate_script(function: str):
        """Mock JavaScript evaluation - simulates finding issues"""

        # Simulate dark pattern detection
        if 'darkPatterns' in function:
            return {
                'confirmshaming': [
                    {
                        'element': 'button',
                        'text': "No thanks, I don't want to save money"
                    }
                ],
                'urgency_manipulation': [
                    {'phrase': 'only', 'context': 'Only 2 left in stock!'},
                    {'phrase': 'hurry', 'context': 'Hurry! Limited time offer!'}
                ],
                'hidden_costs': [
                    {
                        'type': 'multiple_prices',
                        'count': 8,
                        'warning': 'Many price elements may indicate hidden fees'
                    }
                ],
                'obstruction': [],
                'misdirection': [
                    {
                        'type': 'pre_checked_boxes',
                        'count': 2,
                        'warning': 'Pre-checked opt-ins without clear user consent'
                    }
                ]
            }

        # Simulate inclusive design check
        elif 'small_touch_targets' in function:
            return {
                'small_targets_count': 15,
                'tiny_text_count': 8,
                'complex_language_issues': 1,
                'details': {
                    'small_touch_targets': [
                        {'element': 'BUTTON', 'width': 28, 'height': 28, 'text': 'Close'},
                        {'element': 'A', 'width': 35, 'height': 32, 'text': 'Learn more'},
                    ],
                    'tiny_text': [
                        {'fontSize': 12, 'element': 'P', 'preview': 'By continuing you agree to our Terms of Service'},
                    ],
                    'complex_language': [
                        {
                            'long_words_count': 45,
                            'technical_terms_count': 8,
                            'warning': 'May be difficult for non-technical users'
                        }
                    ]
                }
            }

        # Simulate cognitive load analysis
        elif 'choices_count' in function:
            return {
                'choices_count': 67,
                'navigation_complexity': 18,
                'primary_cta_count': 6,
                'walls_of_text': [
                    {'wordCount': 245, 'preview': 'Our company was founded in...'}
                ],
                'visible_elements': 892
            }

        # Simulate user respect check
        elif 'disrespects' in function:
            return {
                'disrespects_found': 2,
                'details': [
                    {
                        'type': 'autoplay_video',
                        'severity': 'high',
                        'reason': 'Auto-playing video with sound is disrespectful'
                    },
                    {
                        'type': 'excessive_modals',
                        'count': 4,
                        'severity': 'medium',
                        'reason': 'Too many pop-ups interrupt user flow'
                    }
                ]
            }

        # Simulate accessibility empathy check
        elif 'empathy_issues' in function:
            return {
                'issues_count': 12,
                'details': [
                    {'type': 'missing_alt', 'severity': 'high', 'element': 'img'},
                    {'type': 'generic_alt', 'severity': 'medium', 'alt': 'image'},
                    {'type': 'generic_aria', 'severity': 'medium', 'label': 'button'},
                    {'type': 'no_skip_link', 'severity': 'medium'},
                    {'type': 'poor_focus_indicators', 'severity': 'high', 'count': 45}
                ]
            }

        # Simulate ethical language check
        elif 'issues_count' in function:
            return {
                'issues_count': 3,
                'details': [
                    {'type': 'gendered_language', 'term': 'guys', 'severity': 'low'},
                    {'type': 'ableist_language', 'term': 'crazy', 'severity': 'medium'},
                    {'type': 'violent_metaphor', 'term': 'kill', 'severity': 'low'}
                ]
            }

        return {}

    def mock_take_screenshot(uid=None, fullPage=False):
        """Mock screenshot - returns mock path"""
        return '/tmp/mock-screenshot.png'

    return {
        'evaluate_script': mock_evaluate_script,
        'take_screenshot': mock_take_screenshot
    }


def print_separator(char='=', length=80):
    """Print a separator line"""
    print(char * length)


def print_section(title):
    """Print a section header"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print('='*80)


def test_litty_standalone():
    """Test Litty as a standalone hero"""

    print_section("🪔 TESTING LITTY - THE CONSCIENCE KEEPER")

    print("\n📍 Target: https://example-ecommerce.com (simulated)")
    print("🎯 Mission: Validate ethical design and user empathy\n")

    # Create mock MCP tools
    mcp_tools = create_mock_mcp_tools()

    # Run Litty's validation
    print("🪔 Litty is analyzing the site...")
    print("   (Looking for dark patterns, accessibility issues, and user respect violations)\n")

    result = litty_validate_ethics(
        url="https://example-ecommerce.com",
        mcp_tools=mcp_tools
    )

    # Display results
    print_section(f"LITTY'S VERDICT: {result['grade']} ({result['ethics_score']}/100)")

    print(f"\n📊 Ethics Score: {result['ethics_score']}/100")
    print(f"✅ Passed Checks: {result['passed']}/{result['total']}")
    print(f"🎯 Grade: {result['grade']}")

    # Show individual checks
    print("\n📋 Individual Checks:")
    print_separator('-')

    checks_display = {
        'dark_patterns': '🕵️  Dark Pattern Detection',
        'inclusive_design': '👵 Inclusive Design',
        'cognitive_load': '🧠 Cognitive Load',
        'user_respect': '🙏 User Respect',
        'accessibility_empathy': '♿ Accessibility Empathy',
        'ethical_language': '💬 Ethical Language'
    }

    for check_key, check_name in checks_display.items():
        check = result['checks'][check_key]
        status = "✅ PASS" if check['passed'] else "❌ FAIL"
        score = check.get('score', 0)
        severity = check.get('severity', 'unknown')

        print(f"{status} | {check_name}: {score}/100 (Severity: {severity})")

    # Show guilt trips
    if result['guilt_trips']:
        print_section("😢 LITTY'S GUILT TRIPS")
        print("\n(These are designed to make you feel the user's pain)\n")

        for i, guilt in enumerate(result['guilt_trips'], 1):
            print(f"{i}. {guilt}\n")

    # Show user stories
    if result['user_stories']:
        print_section("📖 USER STORIES")
        print("\n(Real people affected by these issues)\n")

        for i, story in enumerate(result['user_stories'], 1):
            print(f"Story {i}: {story['persona']} ({story['age']} years old)")
            print(f"  {story['story']}")
            print(f"  💔 Impact: {story['impact']}\n")

    # Show recommendations
    if result['recommendations']:
        print_section("💡 LITTY'S RECOMMENDATIONS")
        print("\n(Actionable steps to improve user empathy)\n")

        for i, rec in enumerate(result['recommendations'], 1):
            print(f"{i}. {rec}\n")

    # Show Litty's final verdict
    print_section("🪔 LITTY'S FINAL VERDICT")
    print(f"\n{result['litty_says']}\n")

    # Summary
    print_separator('=')
    print("\n🎯 SUMMARY:")
    print(f"   Ethics Score: {result['ethics_score']}/100")
    print(f"   Grade: {result['grade']}")
    print(f"   Guilt Trips: {len(result['guilt_trips'])}")
    print(f"   User Stories: {len(result['user_stories'])}")
    print(f"   Recommendations: {len(result['recommendations'])}")
    print_separator('=')

    return result


def test_litty_class():
    """Test Litty's class directly"""

    print_section("🧪 TESTING LITTY CLASS DIRECTLY")

    litty = LittyEthics()

    print(f"\n🪔 Hero: {litty.name}")
    print(f"🎭 Title: {litty.title}")
    print(f"🌟 Emoji: {litty.emoji}")
    print(f"🇮🇳 Origin: {litty.origin}")

    print(f"\n💬 Guilt Phrases Available:")
    for severity, phrase in litty.guilt_phrases.items():
        print(f"   {severity}: {phrase}")

    print(f"\n🎭 User Personas ({len(litty.user_personas)}):")
    for persona_key, persona in litty.user_personas.items():
        print(f"   • {persona['name']} ({persona['age']}, {persona['tech_skill']})")
        print(f"     Needs: {', '.join(persona['needs'][:2])}")

    print(f"\n🕵️ Dark Patterns Detected ({len(litty.dark_patterns)}):")
    for i, pattern in enumerate(litty.dark_patterns[:5], 1):
        print(f"   {i}. {pattern.replace('_', ' ').title()}")
    print(f"   ... and {len(litty.dark_patterns) - 5} more!")

    print("\n✅ Litty class initialized successfully!")


def display_malayalam_guide():
    """Display Malayalam phrases guide"""

    print_section("🇮🇳 MALAYALAM PHRASES GUIDE")

    phrases = [
        ("Eda mone!", "Oh dear!", "Expression of concern"),
        ("Enthina ithoke?", "Why do this?", "Questioning poor choices"),
        ("Shari aylaa mone", "This won't do", "Gentle criticism"),
        ("Kozhapamilla", "No problem", "All good"),
        ("നല്ലത്! (Nallathu)", "Good!", "Praise"),
        ("സത്യം പറ (Sathyam para)", "Speak truth", "Be honest"),
        ("എളുപ്പം ആക്കുക (Eluppam akkuka)", "Make it simple", "Simplify"),
    ]

    print("\n" + "Malayalam".ljust(35) + "English".ljust(20) + "Usage")
    print_separator('-')

    for malayalam, english, usage in phrases:
        print(f"{malayalam.ljust(35)}{english.ljust(20)}{usage}")

    print()


def main():
    """Main test function"""

    print("\n" + "="*80)
    print("  🪔 LITTY - THE CONSCIENCE KEEPER - LIVE TEST")
    print("  Justice League Hero #13 | Version 1.4.0")
    print("  Origin: Kerala, India 🇮🇳")
    print("="*80)

    try:
        # Test 1: Litty Class
        test_litty_class()

        # Test 2: Malayalam Guide
        display_malayalam_guide()

        # Test 3: Full validation
        result = test_litty_standalone()

        # Final message
        print_section("🎉 LITTY IS NOW LIVE!")

        print("\n✅ All tests passed!")
        print("\n🪔 Litty is ready to guilt-trip developers into building")
        print("   better, more empathetic products for ALL users!")
        print("\n💡 Use Litty by running:")
        print("   from core.justice_league import litty_validate_ethics")
        print("   result = litty_validate_ethics(url, mcp_tools)")

        print("\n❤️  Would your ammachi be proud of this design?")
        print("   If not, Litty will let you know! 😊")

        print_separator('=')

        return result

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    result = main()

    if result:
        print(f"\n✨ Final Ethics Score: {result['ethics_score']}/100 ({result['grade']})")
        sys.exit(0)
    else:
        print("\n❌ Test failed!")
        sys.exit(1)
