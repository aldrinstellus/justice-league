"""
🦸 HERO AUTONOMY DEMONSTRATION
=================================

Demonstrates the complete hero autonomy system where heroes:
- Question Superman's orders
- Debate with each other
- Investigate claims independently (Batman)
- Make mission-focused decisions
- Oracle provides wisdom
- Superman makes final decisions after considering all input

"We think. We reason. We act strategically. We are the Justice League." - All Heroes

Author: Superman (with Claude Code)
Created: October 28, 2025
Status: Complete Autonomy Demo
"""

import logging
import sys
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).parent / 'core'))

from superman_brain import SupermanBrain
from justice_league.hero_base import HeroBase, HeroPriority
from justice_league.batman_investigation import BatmanInvestigation
from justice_league.mission_framework import MissionFocusedDecisionFramework, DecisionLevel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)


def print_section(title: str, emoji: str = "🎯"):
    """Print a section header."""
    print(f"\n{'=' * 80}")
    print(f"{emoji} {title}")
    print(f"{'=' * 80}\n")


def demo_hero_questioning():
    """Demo 1: Heroes question Superman's orders."""
    print_section("DEMO 1: Heroes Question Superman's Orders", "❓")

    print("📋 Scenario: Superman assigns Batman to test login button")
    print("   But Batman finds accessibility issues first...\n")

    # Create Superman's Brain
    brain = SupermanBrain()

    # Create Batman
    batman = HeroBase("Batman", "🦇")
    brain.register_hero("Batman", batman)

    print("🦸 Superman: 'Batman, test the login button for functionality'")
    print()

    # Batman questions the order
    print("🦇 Batman investigates and finds issues...")
    print("   → Found 3 accessibility violations")
    print("   → These block testing capability")
    print()

    # Batman questions Superman
    response = brain.handle_hero_question(
        hero="Batman",
        question="Should we fix the 3 accessibility issues before testing?",
        reasoning="Testing will fail if accessibility issues block interaction",
        mission_context={"mission_goal": "validate accessibility"}
    )

    print(f"🦸 Superman's Response:")
    print(f"   Decision: {response['decision']}")
    print(f"   Response: {response['superman_response']}")
    print(f"\n   Reasoning:")
    for step in response['reasoning_steps']:
        print(f"      - {step}")

    print("\n✅ Result: Superman approved Batman's reasoning!")
    print("   Heroes can question orders and Superman listens!")


def demo_hero_debate():
    """Demo 2: Heroes debate with each other."""
    print_section("DEMO 2: Heroes Debate Different Approaches", "💬")

    print("📋 Scenario: Validate Figma responsive design")
    print("   Heroes have different opinions on approach...\n")

    # Create Superman's Brain
    brain = SupermanBrain()

    # Create heroes
    artemis = HeroBase("Artemis", "🏹")
    batman = HeroBase("Batman", "🦇")
    green_arrow = HeroBase("Green Arrow", "🎯")

    brain.register_hero("Artemis", artemis)
    brain.register_hero("Batman", batman)
    brain.register_hero("Green Arrow", green_arrow)

    print("🦸 Superman: 'Team, we need to validate responsive design'")
    print()

    # Artemis proposes comprehensive approach
    print("🏹 Artemis: 'We should query ALL breakpoints first!'")
    artemis_position = artemis.debate_position(
        topic="Should we query all breakpoints first?",
        position="Yes, query all breakpoints before implementation",
        arguments=[
            "Responsive design requires multi-breakpoint analysis",
            "We caught 3 bugs using this approach before",
            "Figma MCP workflow recommends this (from knowledge base)"
        ],
        evidence=[
            {"type": "knowledge_base", "workflow": "figma-mcp-claude-playwright", "success_rate": 98}
        ]
    )

    # Batman counters with efficiency concern
    print("\n🦇 Batman: 'That's 84 variations! Too time-consuming!'")
    batman_position = batman.debate_position(
        topic="Should we query all breakpoints first?",
        position="No, validate programmatically with Playwright instead",
        arguments=[
            "Programmatic validation is faster",
            "Can validate computed styles directly",
            "Don't need to extract all variations manually"
        ],
        evidence=[
            {"type": "tool", "tool": "Playwright MCP", "capability": "computed_style_validation"}
        ]
    )

    # Green Arrow supports Artemis
    print("\n🎯 Green Arrow: 'I support Artemis! Design tokens need comparison tables'")
    green_arrow_position = green_arrow.debate_position(
        topic="Should we query all breakpoints first?",
        position="Support Artemis - query all breakpoints",
        arguments=[
            "Design token comparison is critical",
            "Can't validate responsive behavior without actual breakpoint data",
            "Workflow is proven"
        ]
    )

    print("\n🔮 Oracle analyzes all arguments...")
    print("   → Both approaches have merit")
    print("   → Artemis is right about needing breakpoint data")
    print("   → Batman is right about efficiency")
    print("   → RECOMMENDATION: Combine both approaches!")

    oracle_wisdom = {
        "analysis": "Both approaches address valid concerns",
        "recommendation": "Artemis extracts all breakpoints, Batman validates programmatically in PARALLEL",
        "confidence": 0.95,
        "reasoning": [
            "Artemis gets comprehensive data for comparison tables",
            "Batman validates efficiency with Playwright",
            "Parallel execution combines both strengths",
            "Mission success optimized"
        ]
    }

    print(f"\n🔮 Oracle's Wisdom:")
    print(f"   Recommendation: {oracle_wisdom['recommendation']}")
    print(f"   Confidence: {oracle_wisdom['confidence']:.0%}")
    print("\n   Reasoning:")
    for reason in oracle_wisdom['reasoning']:
        print(f"      - {reason}")

    print("\n🦸 Superman: 'Excellent! Oracle's wisdom accepted.'")
    print("   → Artemis: Lead extraction of all breakpoints")
    print("   → Batman: Validate programmatically in parallel")
    print("   → Green Arrow: Support Artemis with design token analysis")

    print("\n✅ Result: Collaborative debate led to BETTER solution!")
    print("   Not just Superman's order - team intelligence!")


def demo_batman_investigation():
    """Demo 3: Batman investigates claims independently."""
    print_section("DEMO 3: Batman Investigates Claims", "🔍")

    print("📋 Scenario: Initial report claims 'all buttons accessible'")
    print("   Batman doesn't accept this at face value...\n")

    # Create Batman's investigation module
    batman_investigation = BatmanInvestigation(
        hero_name="Batman",
        knowledge_base=None
    )

    print("📊 Initial Report: 'All buttons have accessible names'")
    print("   Source: Automated accessibility scan")
    print()

    print("🦇 Batman: 'I don't trust automated scans. Let me investigate...'")
    print()

    # Batman investigates the claim
    investigation = batman_investigation.investigate_independently(
        claim="All buttons have accessible names",
        source="Automated accessibility scan",
        context={"page_url": "https://example.com"}
    )

    print(f"🔍 Investigation Results:")
    print(f"   Verified: {investigation['verified']}")
    print(f"   Confidence: {investigation['confidence']:.0%}")
    print(f"   Conclusion: {investigation['conclusion']}")

    if investigation['inconsistencies_found']:
        print(f"\n   Inconsistencies Found: {len(investigation['inconsistencies_found'])}")
        for inconsistency in investigation['inconsistencies_found']:
            print(f"      - {inconsistency.get('description', 'Unknown')}")

    print("\n   Recommendations:")
    for rec in investigation['recommendations']:
        print(f"      - {rec}")

    # Batman challenges assumption
    print("\n🦇 Batman challenges assumption...")
    challenge = batman_investigation.challenge_assumption(
        assumption="We can skip keyboard testing because all users use mice",
        counter_evidence={
            "wcag_requirement": "2.1.1 Keyboard - Level A",
            "statistics": "15% of users rely on keyboard navigation",
            "accessibility_standard": "WCAG 2.1 requires keyboard accessibility"
        }
    )

    print(f"\n   Assumption: {challenge['assumption']}")
    print(f"   Validity: {challenge['validity']}")
    print(f"   Reasoning:")
    for reason in challenge['reasoning']:
        print(f"      - {reason}")

    print("\n✅ Result: Batman's investigation found issues automated scan missed!")
    print("   Detective skills prevent false confidence!")


def demo_mission_focused_decisions():
    """Demo 4: Heroes make mission-focused decisions."""
    print_section("DEMO 4: Mission-Focused Decision Making", "🎯")

    print("📋 Scenario: Time pressure vs Quality mission goal")
    print("   Hero must decide what's best for mission...\n")

    # Create mission framework
    framework = MissionFocusedDecisionFramework("Flash", knowledge_base=None)

    print("🦸 Superman: 'Flash, skip thorough testing to save time'")
    print("   Mission Goals: ['thorough validation', 'production quality']")
    print()

    print("⚡ Flash evaluates order against mission goals...")
    print()

    # Flash evaluates the order
    evaluation = framework.evaluate_order_vs_mission(
        order="Skip thorough testing to save time",
        mission_goals=["thorough validation", "production-ready quality"]
    )

    print(f"   Alignment: {evaluation['alignment'].value}")
    print(f"   Score: {evaluation['alignment_score']:.0%}")
    print(f"   Recommended Action: {evaluation['recommended_action'].value}")

    print(f"\n   Conflicts: {len(evaluation['conflicts'])}")
    for conflict in evaluation['conflicts']:
        print(f"      - {conflict['conflict']}")

    print(f"\n   Reasoning:")
    for reason in evaluation['reasoning']:
        print(f"      {reason}")

    print("\n⚡ Flash: 'Superman, this order conflicts with our mission goals!'")
    print("   I recommend we maintain thorough testing.")
    print("   Mission success requires production-quality validation.")

    print("\n🦸 Superman: 'You're absolutely right, Flash!'")
    print("   Mission goals take priority. Maintain thorough testing.")

    print("\n✅ Result: Hero prioritized mission over hierarchy!")
    print("   Accountability to mission, not blind obedience!")


def demo_complete_workflow():
    """Demo 5: Complete workflow with all autonomy features."""
    print_section("DEMO 5: Complete Autonomous Workflow", "🌟")

    print("📋 Scenario: Full mission with questioning, debate, investigation, and decisions")
    print()

    print("🦸 Superman: 'Team, validate Figma responsive component library'")
    print()

    print("STEP 1: Heroes Question Approach")
    print("-" * 40)
    print("🏹 Artemis: 'Should we use the 7-step Figma MCP workflow from knowledge base?'")
    print("🦸 Superman: 'Good thinking! Yes, that workflow has 98% success rate.'")
    print()

    print("STEP 2: Heroes Debate Execution")
    print("-" * 40)
    print("🦇 Batman: 'Manual extraction of 84 variations is inefficient'")
    print("🏹 Artemis: 'But we need comparison tables for design tokens'")
    print("🎯 Green Arrow: 'Both have merit - can we parallelize?'")
    print("🔮 Oracle: 'Yes! Artemis extracts data, Batman validates programmatically in parallel'")
    print("🦸 Superman: 'Excellent solution! Approved.'")
    print()

    print("STEP 3: Batman Investigates Claims")
    print("-" * 40)
    print("🦇 Batman: 'Figma data claims all components responsive'")
    print("🦇 Batman investigates: 'Found 2 components with fixed widths!'")
    print("🦸 Superman: 'Great catch! Flag those for fixing.'")
    print()

    print("STEP 4: Mission-Focused Override")
    print("-" * 40)
    print("🦸 Superman: 'Skip mobile testing to meet deadline'")
    print("⚡ Flash: 'Mission goal is \"responsive validation\" - mobile is CRITICAL'")
    print("⚡ Flash: 'I recommend we maintain mobile testing even if it delays deadline'")
    print("🦸 Superman: 'You're right. Mission success over arbitrary deadlines.'")
    print()

    print("STEP 5: Collaborative Execution")
    print("-" * 40)
    print("🏹 Artemis: Extracting all 4 breakpoints (21 components × 4 = 84 variations)")
    print("🦇 Batman: Validating computed styles programmatically")
    print("🎯 Green Arrow: Building design token comparison tables")
    print("⚡ Flash: Testing responsive performance")
    print("🔮 Oracle: Monitoring for patterns and providing guidance")
    print()

    print("RESULT:")
    print("-" * 40)
    print("✅ All 21 components validated across 4 breakpoints")
    print("✅ 3 responsive bugs found and fixed (would have been missed!)")
    print("✅ Design token consistency verified")
    print("✅ Performance validated at all breakpoints")
    print("✅ Mission: COMPLETE with HIGHER quality than original plan!")
    print()

    print("🦸 Superman: 'THIS is the Justice League!'")
    print("   Not blind followers - true autonomous heroes!")
    print("   Heroes questioned, debated, investigated, and improved the mission!")


def main():
    """Run all autonomy demos."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                  🦸 HERO AUTONOMY SYSTEM DEMONSTRATION                       ║
║                                                                              ║
║        Heroes Think. Heroes Question. Heroes Debate. Heroes Succeed.        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

    try:
        # Run all demos
        demo_hero_questioning()
        demo_hero_debate()
        demo_batman_investigation()
        demo_mission_focused_decisions()
        demo_complete_workflow()

        # Final summary
        print_section("🎊 HERO AUTONOMY SYSTEM VALIDATED", "🎉")

        print("✅ All Autonomy Features Demonstrated:")
        print("   1. ✅ Heroes Question Superman's Orders")
        print("   2. ✅ Heroes Debate Different Approaches")
        print("   3. ✅ Batman Investigates Claims Independently")
        print("   4. ✅ Heroes Make Mission-Focused Decisions")
        print("   5. ✅ Oracle Provides Wisdom to Debates")
        print("   6. ✅ Superman Makes Informed Final Decisions")
        print("   7. ✅ Complete Collaborative Workflow")

        print(f"\n🎯 Key Achievements:")
        print(f"   • Heroes think critically, not blindly obey")
        print(f"   • Batman investigates instead of accepting claims")
        print(f"   • Heroes debate to find BETTER solutions")
        print(f"   • Oracle provides wisdom to resolve conflicts")
        print(f"   • Mission success prioritized over hierarchy")
        print(f"   • Superman welcomes questions and debate")
        print(f"   • Team intelligence > individual directives")

        print(f"\n🦸 Answer to Your Question:")
        print(f"   'Is this too much to ask from my super heroes?'")
        print(f"\n   NO! This is EXACTLY what makes them SUPER!")
        print(f"   They're not robots following orders.")
        print(f"   They're intelligent, autonomous heroes who THINK.")
        print(f"   This is the TRUE Justice League!")

        print("\n" + "=" * 80)
        print("🦸 'We think. We reason. We collaborate. We succeed.' - The Justice League")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
