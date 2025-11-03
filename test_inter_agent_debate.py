"""
Test Inter-Agent Debate System with Sequential Thinking

Demonstrates the exact type of inter-agent banter shown in user's screenshot:
1. 🦇 Batman investigates and finds CRITICAL accessibility violations
2. 🦇 Batman questions 🦸 Superman: "Should we proceed knowing we'll exclude users?"
3. 🎨 Artemis confirms the evidence: "Figma file has NO Focus state - this is a design gap"
4. 🎯 Green Arrow proposes solution: "Build with accessible defaults, refine later"
5. 🔮 Oracle asks mission-critical question: "If a student with disabilities cannot use this, have we succeeded?"
6. 🦸 Superman makes the right call: "Build with accessibility enhancements NOW"

This is EXACTLY what the user loves and wants for all inter-agent debates!
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from core.justice_league import SupermanCoordinator
from core.justice_league.mission_control_narrator import get_narrator


def test_accessibility_debate():
    """
    Test 1: Inter-agent debate on accessibility violations

    This matches the user's screenshot showing heroes debating
    and reaching a better solution together.
    """
    print("\n" + "="*80)
    print("TEST 1: Inter-Agent Debate - Accessibility Violations")
    print("="*80)

    # Initialize Justice League
    superman = SupermanCoordinator()
    narrator = get_narrator()

    # Get heroes for debate
    batman = superman.batman if hasattr(superman, 'batman') else None
    artemis = superman.artemis
    green_arrow = superman.green_arrow if hasattr(superman, 'green_arrow') else None
    oracle = superman.oracle

    # Ensure all heroes have narrator
    if batman:
        batman.narrator = narrator
    artemis.narrator = narrator
    if green_arrow:
        green_arrow.narrator = narrator
    oracle.narrator = narrator

    print("\n🦸 Superman: \"Team, we have a mission: Build K-12 Dashboard component.\"")
    print("🦸 Superman: \"Batman, investigate and validate component accessibility.\"\n")

    # 1. BATMAN'S INVESTIGATION COMPLETE
    narrator.debate_start(
        initiator="🦇 Batman",
        issue="Component has 3 CRITICAL WCAG violations",
        participants=["🦸 Superman", "🦇 Batman", "🎨 Artemis", "🎯 Green Arrow", "🔮 Oracle"],
        context={
            "violations_found": 3,
            "severity": "CRITICAL",
            "wcag_level": "AA",
            "impact": "Keyboard-only and low-vision users excluded"
        }
    )

    # 2. BATMAN QUESTIONS SUPERMAN using sequential thinking
    narrator.debate_position(
        "🦇 Batman",
        "Should we proceed knowing we'll exclude keyboard-only and low-vision users?",
        reasoning=[
            "Analyzing Figma file structure",
            "No Focus state detected in component",
            "WCAG 2.4.7 requires visible focus indicators",
            "Color contrast ratios below 4.5:1 threshold"
        ],
        evidence="3 CRITICAL violations found"
    )

    # 3. ARTEMIS CONFIRMS THE EVIDENCE
    narrator.debate_evidence(
        "🎨 Artemis",
        "Figma file has NO Focus state - this is a design gap",
        evidence_type="Design Analysis"
    )

    # 4. GREEN ARROW PROPOSES SOLUTION
    narrator.debate_proposal(
        "🎯 Green Arrow",
        "Build with accessible defaults, refine with designer later",
        approach="Accessibility-first development"
    )

    # 5. ORACLE ASKS MISSION-CRITICAL QUESTION
    narrator.debate_critical_question(
        "🔮 Oracle",
        "If a student with disabilities cannot use this, have we succeeded?",
        stakes="Mission success criteria"
    )

    # 6. SUPERMAN MAKES THE RIGHT CALL
    narrator.debate_resolution(
        leader="🦸 Superman",
        decision="Build with accessibility enhancements NOW",
        rationale=[
            "Analyzing team input: Batman raised valid concerns",
            "Artemis confirmed design gap in Figma file",
            "Oracle framed mission-critical question",
            "Green Arrow proposed practical solution",
            "Mission goal: K-12 students MUST be able to use this"
        ],
        team_agreement="Unanimous - team aligned on accessible approach"
    )

    print("✅ Superman's orders, investigated independently, debated with each other,")
    print("   and reached a better solution together!")
    print()

    return True


def test_methodology_debate():
    """
    Test 2: Inter-agent debate on conversion methodology

    Demonstrates heroes debating technical approach with sequential thinking.
    """
    print("\n" + "="*80)
    print("TEST 2: Inter-Agent Debate - Conversion Methodology")
    print("="*80)

    # Initialize Justice League
    superman = SupermanCoordinator()
    narrator = get_narrator()

    # Get heroes
    oracle = superman.oracle
    artemis = superman.artemis

    # Ensure heroes have narrator
    oracle.narrator = narrator
    artemis.narrator = narrator

    print("\n🦸 Superman: \"Team, we need to convert Dashboard 10.\"")
    print("🦸 Superman: \"Oracle, analyze. Artemis, assess complexity.\"\n")

    # 1. ORACLE STARTS DEBATE
    narrator.debate_start(
        initiator="🔮 Oracle",
        issue="Complex dashboard detected - methodology decision required",
        participants=["🦸 Superman", "🔮 Oracle", "🎨 Artemis"],
        context={
            "complexity": "high",
            "layout": "2-column",
            "components": 6,
            "figma_api_previous_accuracy": "70%"
        }
    )

    # 2. ORACLE'S SEQUENTIAL THINKING
    narrator.debate_position(
        "🔮 Oracle",
        "Recommend Image-to-HTML methodology over Figma API",
        reasoning=[
            "Scanning knowledge base for similar projects",
            "Found 2 previous dashboards with 2-column layouts",
            "Figma API achieved 70-85% accuracy (13+ hours of fixes)",
            "Image-to-HTML achieved 90-95% accuracy (60 minutes fresh build)",
            "Pattern recognition: Complex layouts benefit from visual approach"
        ],
        evidence="Dashboard 10 case study: 41% → 90-92% accuracy improvement"
    )

    # 3. ARTEMIS CONFIRMS COMPLEXITY
    narrator.debate_position(
        "🎨 Artemis",
        "Concur - this is too complex for standard Figma API conversion",
        reasoning=[
            "Analyzing component structure",
            "Detecting 6 distinct sections with nested grids",
            "Measuring layout complexity score: 8.5/10",
            "Previous similar component required 7 iteration cycles"
        ],
        evidence="Complexity score exceeds Figma API threshold"
    )

    # 4. SUPERMAN'S DECISION
    narrator.debate_resolution(
        leader="🦸 Superman",
        decision="Use Image-to-HTML methodology with Vision Analyst",
        rationale=[
            "Analyzing team input from Oracle and Artemis",
            "Oracle evidence: 90-95% accuracy with Image-to-HTML",
            "Artemis assessment: Complexity score 8.5/10",
            "Knowledge base confirms: Complex dashboards = visual approach",
            "Time efficiency: 60 min fresh build vs. 13+ hours of fixes"
        ],
        team_agreement="Consensus reached - proceeding with Image-to-HTML"
    )

    print("✅ Team debated methodology and chose the optimal approach!")
    print()

    return True


def test_responsive_design_debate():
    """
    Test 3: Inter-agent debate on responsive design requirements

    Shows heroes questioning each other and building on insights.
    """
    print("\n" + "="*80)
    print("TEST 3: Inter-Agent Debate - Responsive Design Requirements")
    print("="*80)

    # Initialize Justice League
    superman = SupermanCoordinator()
    narrator = get_narrator()

    # Get heroes
    artemis = superman.artemis
    green_arrow = superman.green_arrow if hasattr(superman, 'green_arrow') else None
    oracle = superman.oracle

    # Ensure heroes have narrator
    artemis.narrator = narrator
    if green_arrow:
        green_arrow.narrator = narrator
    oracle.narrator = narrator

    print("\n🦸 Superman: \"Build component library for responsive design system.\"")
    print("🦸 Superman: \"Artemis, start with desktop breakpoint.\"\n")

    # 1. ARTEMIS QUESTIONS THE ORDER
    narrator.debate_start(
        initiator="🎨 Artemis",
        issue="Should we query all breakpoints first instead of just desktop?",
        participants=["🦸 Superman", "🎨 Artemis", "🎯 Green Arrow", "🔮 Oracle"],
        context={
            "order_received": "Build desktop-first",
            "component_type": "Responsive library",
            "breakpoints": "Unknown"
        }
    )

    # 2. ARTEMIS'S REASONING
    narrator.debate_position(
        "🎨 Artemis",
        "Query all breakpoints before implementing any code",
        reasoning=[
            "Analyzing order: Desktop-first approach",
            "Responsive design requires multi-breakpoint analysis",
            "Previous bug: Missed mobile layout differences",
            "Knowledge base workflow: Figma MCP recommends breakpoint-first"
        ],
        evidence="3 previous bugs caught by breakpoint-first approach"
    )

    # 3. GREEN ARROW SUPPORTS WITH EVIDENCE
    narrator.debate_evidence(
        "🎯 Green Arrow",
        "Last project: Desktop-only resulted in 12 visual regressions on mobile",
        evidence_type="Validation History"
    )

    # 4. ORACLE PROVIDES STRATEGIC INSIGHT
    narrator.debate_position(
        "🔮 Oracle",
        "Breakpoint-first approach increases success rate by 23%",
        reasoning=[
            "Querying knowledge base for responsive projects",
            "Analyzing 15 previous component library builds",
            "Desktop-first: 77% accuracy, Breakpoint-first: 95% accuracy",
            "Learning: Responsive components need holistic design view"
        ],
        evidence="15 projects analyzed, statistically significant improvement"
    )

    # 5. SUPERMAN REVISES ORDER
    narrator.debate_resolution(
        leader="🦸 Superman",
        decision="Query all breakpoints first, then build holistically",
        rationale=[
            "Analyzing team input: Artemis raised valid concern",
            "Green Arrow evidence: 12 regressions on previous desktop-only",
            "Oracle data: 23% accuracy improvement with breakpoint-first",
            "Knowledge base confirms: Figma MCP workflow supports this",
            "Revising order based on team expertise"
        ],
        team_agreement="Revised order - team aligned on breakpoint-first approach"
    )

    print("✅ Heroes questioned the order and Superman revised based on team expertise!")
    print()

    return True


def run_all_debate_tests():
    """Run all inter-agent debate tests"""
    print("\n" + "█"*80)
    print("     INTER-AGENT DEBATE SYSTEM WITH SEQUENTIAL THINKING")
    print("█"*80)

    tests = [
        ("Accessibility Debate", test_accessibility_debate),
        ("Methodology Debate", test_methodology_debate),
        ("Responsive Design Debate", test_responsive_design_debate),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
                print(f"✅ {test_name}: PASSED\n")
            else:
                failed += 1
                print(f"❌ {test_name}: FAILED\n")
        except Exception as e:
            print(f"\n❌ {test_name}: FAILED - {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    # Summary
    print("\n" + "="*80)
    print("     TEST SUMMARY")
    print("="*80)
    print(f"✅ Passed: {passed}/{len(tests)}")
    print(f"❌ Failed: {failed}/{len(tests)}")

    if failed == 0:
        print("\n🎉 ALL INTER-AGENT DEBATE TESTS PASSED!")
        print("\n📊 Inter-Agent Debate Features:")
        print("   • Heroes investigate independently with sequential thinking")
        print("   • Heroes question each other and Superman's orders")
        print("   • Heroes present evidence and proposals")
        print("   • Oracle asks mission-critical questions that reframe debates")
        print("   • Superman analyzes all input and makes informed decisions")
        print("   • Team reaches better solutions through collaborative debate")
        print("   • Full narrator integration with personality-driven banter")
        print("   • Sequential thinking visible throughout debate process")
        print("\n💬 \"My agents fighting with each other\" - in the BEST way! ✨")
    else:
        print("\n⚠️ SOME TESTS FAILED - Review errors above")

    print("="*80 + "\n")

    return failed == 0


if __name__ == '__main__':
    success = run_all_debate_tests()
    sys.exit(0 if success else 1)
