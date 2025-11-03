#!/usr/bin/env python3
"""
🪔 Litty Autonomous Agent - Example

Demonstrates Litty as a true autonomous agent with:
- LLM-powered reasoning and planning
- Self-correction capabilities
- Independent decision-making
- Tool execution with retries

This is Justice League v2.0 - True Autonomous Agents!
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.justice_league_v2.agents.litty_agent import LittyAgent


async def main():
    """Main example function"""

    print("\n" + "="*70)
    print("🪔 LITTY AUTONOMOUS AGENT - Justice League v2.0")
    print("True autonomous agent with LLM-powered reasoning")
    print("="*70 + "\n")

    # Check for API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("⚠️  No ANTHROPIC_API_KEY found in environment")
        print("📝 Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        print("\n💡 Running in demo mode (no actual LLM calls)")
        print("-"*70 + "\n")

    # Create autonomous Litty agent
    print("🤖 Initializing Litty as autonomous agent...")
    litty = LittyAgent(api_key=api_key if api_key else None)

    print(f"✅ {litty.name} ({litty.role}) ready!")
    print(f"📊 Tools available: {len(litty.tools)}")
    print(f"🧠 Model: {litty.model}")
    print()

    # Show agent stats
    stats = litty.get_stats()
    print("📈 Agent Statistics:")
    for key, value in stats.items():
        print(f"  • {key}: {value}")
    print()

    # Show registered tools
    print("🔧 Registered Tools:")
    for tool_name in litty.tools.keys():
        print(f"  • {tool_name}")
    print()

    # Execute autonomous mission
    print("🎯 Executing Autonomous Mission")
    print("-"*70)

    if not api_key:
        print("\n⚠️  Demo Mode: Showing what autonomous agent WOULD do")
        print("   (Set ANTHROPIC_API_KEY for full autonomous operation)\n")

        # Show demo reasoning
        print("💭 Litty's Autonomous Reasoning Process:")
        print()
        print("1. PLANNING PHASE:")
        print("   'Let me think about how to validate ethics for this site...'")
        print("   'I should check dark patterns first, then accessibility,'")
        print("   'then generate guilt trips for found issues.'")
        print()
        print("2. EXECUTION PHASE:")
        print("   'Detecting dark patterns...'")
        print("   'Found confirmshaming and hidden costs!'")
        print("   'Generating guilt trips for affected personas...'")
        print()
        print("3. SELF-CORRECTION (if needed):")
        print("   'Hmm, that tool failed. Let me try alternative approach...'")
        print("   'Retrying with different parameters...'")
        print()

    mission = {
        'url': 'https://example-ecommerce.com',
        'goal': 'validate ethical design',
        'focus_areas': ['dark_patterns', 'accessibility', 'user_empathy']
    }

    print(f"\n🎯 Mission: {mission['goal']}")
    print(f"🌐 Target: {mission['url']}")
    print(f"🔍 Focus: {', '.join(mission['focus_areas'])}")
    print()

    if api_key:
        print("🤖 Agent is thinking and planning...")
        print("   (This will use Claude API for reasoning)")
        print()

    try:
        result = await litty.execute_mission(mission)

        # Display results
        print("\n" + "="*70)
        print("📊 MISSION RESULTS")
        print("="*70 + "\n")

        print(f"🎯 Ethics Score: {result['ethics_score']}/100")
        print(f"📝 Grade: {result['grade']}")
        print(f"🎭 Dark Patterns Found: {len(result.get('dark_patterns_found', []))}")
        print()

        if result.get('dark_patterns_found'):
            print("🎭 Dark Patterns Detected:")
            for pattern in result['dark_patterns_found']:
                print(f"  ❌ {pattern}")
            print()

        if result.get('guilt_trips'):
            print(f"😢 Guilt Trips Generated ({len(result['guilt_trips'])}):")
            for i, guilt in enumerate(result['guilt_trips'], 1):
                print(f"  {i}. {guilt}")
            print()

        if result.get('user_stories'):
            print(f"📖 User Impact Stories ({len(result['user_stories'])}):")
            for i, story in enumerate(result['user_stories'], 1):
                print(f"  {i}. {story}")
            print()

        if result.get('recommendations'):
            print(f"💡 Recommendations ({len(result['recommendations'])}):")
            for i, rec in enumerate(result['recommendations'], 1):
                print(f"  {i}. {rec}")
            print()

        if api_key and result.get('agent_reasoning'):
            print("🧠 Agent's Reasoning:")
            reasoning = result['agent_reasoning']
            if 'planning' in reasoning:
                print("\n  Planning Phase:")
                print(f"  {reasoning['planning'][:200]}...")
            if 'analysis' in reasoning:
                print("\n  Analysis Phase:")
                print(f"  {reasoning['analysis'][:200]}...")
            print()

        if result.get('self_corrections'):
            print(f"🔄 Self-Corrections Made: {len(result['self_corrections'])}")
            for correction in result['self_corrections']:
                print(f"  • Attempt {correction.get('attempt')}: {correction.get('reasoning', 'N/A')[:100]}...")
            print()

        print("="*70)
        print()

        # Show updated stats
        stats = litty.get_stats()
        print("📈 Updated Agent Statistics:")
        print(f"  • Missions completed: {stats['missions_completed']}")
        print(f"  • Memory size: {stats['memory_size']}")
        print()

        print("✅ Mission Complete!")
        print()
        print('"Eda mone! I\'ve analyzed the site and found the issues!" 🪔')
        print()

        if not api_key:
            print("💡 TIP: Set ANTHROPIC_API_KEY to see full autonomous reasoning")
            print("   The agent will actually think, plan, and self-correct using Claude!")
            print()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    # Run async main
    asyncio.run(main())
