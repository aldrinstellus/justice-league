"""
Add 'always_debate_missions' user preference to Oracle's knowledge base
"""

import json
from pathlib import Path
from datetime import datetime

# Load Oracle's knowledge base
kb_path = Path("data/oracle_project_patterns.json")
with open(kb_path, 'r') as f:
    kb_data = json.load(f)

# Add the new debate preference
kb_data["user_preferences"]["mission_debates"] = {
    "preference": "always_debate_missions",
    "priority": "HIGH",
    "description": "All Justice League missions must include full team debate with sequential thinking before execution",
    "debate_requirements": {
        "who_participates": [
            "Oracle (always - provides capability analysis and data)",
            "All heroes relevant to mission type",
            "Superman (always - decision maker)"
        ],
        "sequential_thinking": {
            "heroes": "3-7 steps each when presenting positions",
            "superman": "5-7 steps when making final decision",
            "oracle": "3-5 steps during capability analysis"
        },
        "conversation_style": "full_dialogue",
        "show_evidence": True,
        "show_questions": True,
        "show_proposals": True
    },
    "mission_flow": [
        "1. Superman announces mission to team",
        "2. Oracle queries hero capability database",
        "3. Oracle provides capability analysis with context",
        "4. Relevant heroes present positions with sequential thinking",
        "5. Heroes question each other's proposals",
        "6. Heroes provide evidence and benchmarks",
        "7. Oracle asks mission-critical question to reframe debate",
        "8. Superman analyzes all input with sequential thinking",
        "9. Superman makes informed decision",
        "10. Team confirms consensus",
        "11. Selected hero executes mission"
    ],
    "output_format": {
        "style": "live_conversation",
        "not_summaries": True,
        "show_emoji_heroes": True,
        "show_technical_details": True,
        "example": "🦇 Batman: [Sequential Thinking - Step 1] Analyzing component...\n🎨 Artemis: [Question to Batman] What about mobile breakpoints?\n🔮 Oracle: ⚡ MISSION-CRITICAL QUESTION: Which approach ensures accessibility?\n🦸 Superman: [Decision] Based on team analysis..."
    },
    "learned_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "context": "User request: 'i want them to debate for every mission i give justice-league, as they are a team'",
    "user_quote": "yes, make it happen for every mission",
    "applies_to": [
        "All Justice League missions",
        "Figma frame exports",
        "Component conversions",
        "Visual validation",
        "Performance testing",
        "Accessibility testing",
        "Every hero deployment decision"
    ],
    "benefits": [
        "Better decisions through collaboration",
        "Multiple perspectives prevent blind spots",
        "Evidence-based mission planning",
        "Transparent reasoning process visible to user",
        "Team learns from each debate",
        "User sees HOW decisions are made, not just WHAT was decided"
    ]
}

# Save updated knowledge base
with open(kb_path, 'w') as f:
    json.dump(kb_data, f, indent=2)

print("✅ Added 'mission_debates' preference to Oracle knowledge base")
print(f"📍 Location: {kb_path}")
print("\n🔮 Oracle will now trigger full team debates for every mission")
print("💬 User will see complete conversations, not summaries")
print("🎯 Sequential thinking visible for all participants")
