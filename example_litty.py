#!/usr/bin/env python3
"""
Example: Using Litty - The Conscience Keeper

This example shows how to use Litty to validate ethical design
and user empathy on a website.
"""

import sys
sys.path.insert(0, '/Users/admin/Documents/claudecode/Projects/aldo-vision')

from core.justice_league import litty_validate_ethics, LittyEthics


def create_mock_mcp_tools():
    """
    Create mock MCP tools for testing without a real browser.

    In production, replace this with real MCP Chrome DevTools integration.
    """
    def mock_evaluate_script(function: str):
        """Simulate browser JavaScript evaluation"""
        # Simulate finding various issues based on what JS is being executed

        # Dark patterns check
        if 'confirmshaming' in function or 'urgency' in function:
            return {
                'confirmshaming': {'count': 1, 'examples': ["No thanks, I don't want to save"]},
                'urgency': {'count': 2, 'examples': ['Only 2 left!', 'Hurry!']},
                'hidden_costs': {'count': 3},
                'misdirection': {'count': 2}
            }

        # User respect check
        elif 'disrespects_found' in function or 'disrespects' in function:
            return {
                'disrespects_found': 3,
                'details': [
                    {'type': 'autoplay_video', 'severity': 'high'},
                    {'type': 'excessive_modals', 'count': 5},
                    {'type': 'cookie_dark_pattern', 'severity': 'high'}
                ]
            }

        # Cognitive load check
        elif 'choices' in function or 'navigation' in function:
            return {
                'too_many_choices': 15,
                'navigation_complexity': 'high',
                'primary_actions_unclear': True
            }

        # Accessibility check
        elif 'contrast' in function or 'aria' in function:
            return {
                'contrast_issues': 5,
                'missing_alt_text': 3,
                'missing_aria_labels': 8,
                'small_click_targets': 10
            }

        # Text size check
        elif 'fontSize' in function or 'textSize' in function:
            return 11  # Small text (minimum should be 16px)

        # Language check
        elif 'jargon' in function or 'language' in function:
            return {
                'jargon_count': 5,
                'confusing_terms': ['synergy', 'leverage', 'paradigm'],
                'readability_score': 45  # Low (should be 60+)
            }

        # Default return
        else:
            return {}

    def mock_take_snapshot():
        """Simulate page content snapshot"""
        return {
            'text': '''
            Welcome to Our Amazing Store!

            ONLY 2 LEFT IN STOCK - HURRY!

            Special offer: Buy now and save 50%!
            (Conditions apply, shipping not included)

            Subscribe to our newsletter: [X] I agree to receive emails

            Click here to accept cookies and continue browsing.
            '''
        }

    def mock_take_screenshot(**kwargs):
        """Simulate screenshot capture"""
        return '/tmp/mock_screenshot.png'

    return {
        'evaluate_script': mock_evaluate_script,
        'take_snapshot': mock_take_snapshot,
        'take_screenshot': mock_take_screenshot
    }


def main():
    """Main example function"""

    print("\n" + "="*70)
    print("🪔 LITTY - THE CONSCIENCE KEEPER")
    print("Ethics & User Empathy Validator from Kerala, India")
    print("="*70 + "\n")

    # Create Litty instance to show her capabilities
    litty = LittyEthics()

    print("📋 Litty's Profile:")
    print(f"  Name:        {litty.name}")
    print(f"  Title:       {litty.title}")
    print(f"  Origin:      {litty.origin}")
    print(f"  Emoji:       {litty.emoji}")
    print()

    print("💪 Powers:")
    print(f"  • Detects {len(litty.dark_patterns)} dark patterns")
    print(f"  • Champions {len(litty.user_personas)} user personas")
    print(f"  • Validates 6 ethical dimensions")
    print()

    print("🇮🇳 Malayalam Guilt Phrases:")
    for severity, phrase in litty.guilt_phrases.items():
        print(f"  {severity.upper():8s}: {phrase}")
    print()

    print("👥 User Personas:")
    for persona_key, persona_data in litty.user_personas.items():
        name = persona_data.get('name', persona_key)
        age = persona_data.get('age', 'N/A')
        print(f"  • {name} ({age})")
    print()

    # Now run actual ethics validation
    print("🔍 Analyzing Mock E-commerce Website...")
    print("-" * 70)

    mcp_tools = create_mock_mcp_tools()

    result = litty_validate_ethics(
        url="https://mock-ecommerce-example.com",
        mcp_tools=mcp_tools
    )

    # Display results
    print()
    print("📊 ETHICS ANALYSIS RESULTS")
    print("=" * 70)
    print()

    print(f"🎯 Overall Ethics Score: {result['ethics_score']}/100")
    print(f"📝 Grade: {result['grade']}")
    print()

    # Show checks performed
    print("🔍 Checks Performed:")
    checks = result.get('checks', {})
    for check_name, check_data in checks.items():
        status = "✅" if isinstance(check_data, dict) and check_data.get('passed') else "⚠️"
        print(f"  {status} {check_name.replace('_', ' ').title()}")
    print()

    # Show dark patterns detected
    if 'dark_patterns' in checks:
        dark_patterns = checks['dark_patterns']
        detected = dark_patterns.get('detected', [])
        if detected:
            print(f"🎭 Dark Patterns Detected ({len(detected)}):")
            for pattern in detected[:5]:  # Show first 5
                print(f"  ❌ {pattern}")
            if len(detected) > 5:
                print(f"  ... and {len(detected) - 5} more")
            print()

    # Show guilt trips
    guilt_trips = result.get('guilt_trips', [])
    if guilt_trips:
        print(f"😢 Guilt Trips ({len(guilt_trips)}):")
        for i, trip in enumerate(guilt_trips[:3], 1):  # Show first 3
            if isinstance(trip, dict):
                severity = trip.get('severity', 'medium')
                message = trip.get('message', trip.get('guilt', ''))
                print(f"  {i}. [{severity.upper()}] {message}")
            else:
                # Trip is just a string
                print(f"  {i}. {trip}")
        if len(guilt_trips) > 3:
            print(f"  ... and {len(guilt_trips) - 3} more")
        print()

    # Show user stories
    user_stories = result.get('user_stories', [])
    if user_stories:
        print(f"📖 User Impact Stories ({len(user_stories)}):")
        for story in user_stories[:3]:  # Show first 3
            persona = story.get('persona', 'User')
            impact = story.get('impact', 'No impact specified')
            print(f"  • {persona}: {impact}")
        if len(user_stories) > 3:
            print(f"  ... and {len(user_stories) - 3} more")
        print()

    # Show recommendations
    recommendations = result.get('recommendations', [])
    if recommendations:
        print(f"💡 Recommendations ({len(recommendations)}):")
        for rec in recommendations[:5]:  # Show first 5
            print(f"  • {rec}")
        if len(recommendations) > 5:
            print(f"  ... and {len(recommendations) - 5} more")
        print()

    print("=" * 70)
    print()
    print("✅ Analysis Complete!")
    print()
    print('"Eda mone! Make your designs more human!" 🪔')
    print()


if __name__ == '__main__':
    main()
