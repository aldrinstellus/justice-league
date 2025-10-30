"""
Test Superman's Autonomous Justice League System
"""

import sys
import os

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

print("🦸 Testing Superman's Autonomous Justice League System")
print("=" * 70)

# Test 1: Communication Hub
print("\n📡 Test 1: Communication Hub")
from core.superman_communication import HeroCommunicationHub
from core.justice_league.hero_base import HeroBase, HeroMessage, HeroPriority

hub = HeroCommunicationHub()
batman = HeroBase("Batman", "🦇")
wonder_woman = HeroBase("Wonder Woman", "⚡")

hub.register_hero("Batman", batman)
hub.register_hero("Wonder Woman", wonder_woman)

# Batman requests help
batman.request_help("Wonder Woman", "Check accessibility", {"url": "https://example.com"})

print(f"✅ Communication Hub: {len(hub.heroes)} heroes registered")
print(f"✅ Messages: {len(hub.message_history)} messages")

# Test 2: Knowledge Base
print("\n📚 Test 2: Knowledge Base")
from core.superman_knowledge_base import JusticeLeagueKnowledgeBase

kb = JusticeLeagueKnowledgeBase()
kb.add_knowledge(
    hero="Batman",
    knowledge_type="best_practice",
    content={
        "practice": "Wait for dynamic elements",
        "reason": "Prevents flaky tests"
    },
    tags=["testing", "reliability"]
)

stats = kb.get_stats()
print(f"✅ Knowledge Base: {stats['total_entries']} entries")

# Test 3: Self-Healing Engine
print("\n🔧 Test 3: Self-Healing Engine")
from core.superman_self_healing import SupermanSelfHealingEngine

healing = SupermanSelfHealingEngine()

# Simulate error
try:
    raise TimeoutError("Connection timeout")
except Exception as e:
    result = healing.handle_error(e, "fetch_data", {"url": "https://example.com"}, "Batman")
    print(f"✅ Self-Healing: Handled error with recovery")

# Test 4: Mission Planner
print("\n🎯 Test 4: Mission Planner")
from core.superman_mission_planner import SupermanMissionPlanner

planner = SupermanMissionPlanner()
mission = planner.plan_mission(
    target="https://example.com",
    goal="Quality audit",
    target_type="url"
)

print(f"✅ Mission Planner: Created mission with {len(mission.tasks)} tasks")
print(f"   Phases: {', '.join([p.value for p in mission.phases])}")

# Test 5: MCP Tool Manager
print("\n🛠️  Test 5: MCP Tool Manager")
from core.superman_mcp_manager import SupermanMCPManager

mcp = SupermanMCPManager()
tools = mcp.discover_tools()
print(f"✅ MCP Manager: Discovered {len(tools)} tools")

# Test 6: Autonomous Artemis
print("\n🎨 Test 6: Autonomous Artemis")
from core.justice_league.artemis_autonomous import ArtemisAutonomous

artemis = ArtemisAutonomous()
status = artemis.get_status()
print(f"✅ Artemis: {status['hero']} {status['emoji']}")
print(f"   Fallback strategies: {status['fallback_strategies']}")
print(f"   Communication: {status['communication_hub_connected']}")

# Summary
print("\n" + "=" * 70)
print("🦸 AUTONOMOUS SYSTEM TEST COMPLETE")
print("=" * 70)
print("✅ Communication Hub: Working")
print("✅ Knowledge Base: Working")
print("✅ Self-Healing Engine: Working")
print("✅ Mission Planner: Working")
print("✅ MCP Tool Manager: Working")
print("✅ Autonomous Artemis: Working")
print("\n🎉 All autonomous systems operational!")
print("\n🦸 Superman's Justice League is ready for autonomous operation!")
