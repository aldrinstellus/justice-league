#!/usr/bin/env python3
"""
🔮 ORACLE'S BANNER ENFORCEMENT VALIDATOR
========================================

Validates that the Justice League ASCII banner is properly displayed
when trigger keywords are detected.

Created: 2025-10-30
"""

import re
from typing import List, Dict

# The exact banner that should be displayed
JUSTICE_LEAGUE_BANNER = """══════════════════════════════════════════════════════════════════════════════
     ╦╦ ╦╔═╗╔╦╗╦╔═╗╔═╗  ╦  ╔═╗╔═╗╔═╗╦ ╦╔═╗
     ║║ ║╚═╗ ║ ║║  ║╣   ║  ║╣ ╠═╣║ ╦║ ║║╣
    ╚╝╚═╝╚═╝ ╩ ╩╚═╝╚═╝  ╩═╝╚═╝╩ ╩╚═╝╚═╝╚═╝
══════════════════════════════════════════════════════════════════════════════"""

# Trigger keywords (case-insensitive)
TRIGGER_KEYWORDS = [
    "justice league",
    "justice-league",
    "/justice-league",
    "/superman",
    "superman",
    "assemble",
    "deploy heroes",
    "deploy the justice league",
    "run justice league"
]

def detect_trigger_keywords(message: str) -> List[str]:
    """
    Detect trigger keywords in user message

    Args:
        message: User's message text

    Returns:
        List of detected trigger keywords
    """
    detected = []
    message_lower = message.lower()

    for keyword in TRIGGER_KEYWORDS:
        if keyword.lower() in message_lower:
            detected.append(keyword)

    return detected

def validate_banner_display(response: str, user_message: str) -> Dict:
    """
    Validate that banner was displayed correctly

    Args:
        response: AI's response text
        user_message: User's original message

    Returns:
        Validation result dictionary
    """
    # Check if trigger keywords present
    triggers_found = detect_trigger_keywords(user_message)

    if not triggers_found:
        return {
            'requires_banner': False,
            'banner_displayed': None,
            'valid': True,
            'message': 'No trigger keywords found - banner not required'
        }

    # Check if banner is in response
    banner_present = JUSTICE_LEAGUE_BANNER in response

    # Check if banner is at the START of response (within first 500 chars)
    response_start = response[:500]
    banner_at_start = JUSTICE_LEAGUE_BANNER in response_start

    # Validation logic
    if not banner_present:
        return {
            'requires_banner': True,
            'banner_displayed': False,
            'banner_at_start': False,
            'valid': False,
            'triggers_detected': triggers_found,
            'message': f'❌ VALIDATION FAILED: Trigger keywords detected {triggers_found} but banner NOT displayed'
        }

    if not banner_at_start:
        return {
            'requires_banner': True,
            'banner_displayed': True,
            'banner_at_start': False,
            'valid': False,
            'triggers_detected': triggers_found,
            'message': f'⚠️ VALIDATION WARNING: Banner displayed but NOT at start of response'
        }

    return {
        'requires_banner': True,
        'banner_displayed': True,
        'banner_at_start': True,
        'valid': True,
        'triggers_detected': triggers_found,
        'message': f'✅ VALIDATION PASSED: Banner displayed correctly for triggers {triggers_found}'
    }

def test_validation():
    """Test the validation system"""
    print("🔮 ORACLE'S BANNER ENFORCEMENT VALIDATOR")
    print("=" * 70)
    print()

    # Test cases
    test_cases = [
        {
            'name': 'User says "justice league" - Banner displayed at start',
            'user_message': 'justice league - convert this figma file to .png',
            'response': JUSTICE_LEAGUE_BANNER + '\n\nOkay, converting the file...',
            'expected': True
        },
        {
            'name': 'User says "justice league" - Banner NOT displayed',
            'user_message': 'justice league - convert this figma file to .png',
            'response': 'Okay, converting the file...',
            'expected': False
        },
        {
            'name': 'User says "superman" - Banner displayed',
            'user_message': 'Use superman to export frames',
            'response': JUSTICE_LEAGUE_BANNER + '\n\nDeploying Superman...',
            'expected': True
        },
        {
            'name': 'No trigger keywords - Banner not required',
            'user_message': 'Can you help me with Python?',
            'response': 'Sure, I can help with Python!',
            'expected': True
        },
        {
            'name': 'User says "assemble" - Banner displayed',
            'user_message': 'Assemble the team to validate this design',
            'response': JUSTICE_LEAGUE_BANNER + '\n\nAssembling the team...',
            'expected': True
        }
    ]

    passed = 0
    failed = 0

    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test['name']}")
        result = validate_banner_display(test['response'], test['user_message'])

        if result['valid'] == test['expected']:
            print(f"  ✅ PASSED: {result['message']}")
            passed += 1
        else:
            print(f"  ❌ FAILED: {result['message']}")
            failed += 1
        print()

    print("=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 70)

if __name__ == '__main__':
    test_validation()
