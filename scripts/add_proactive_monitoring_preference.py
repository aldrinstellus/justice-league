"""
Add 'proactive_background_task_monitoring' user preference to Oracle's knowledge base
"""

import json
from pathlib import Path
from datetime import datetime

# Load Oracle's knowledge base
kb_path = Path("data/oracle_project_patterns.json")
with open(kb_path, 'r') as f:
    kb_data = json.load(f)

# Add the new proactive monitoring preference
kb_data["user_preferences"]["proactive_monitoring"] = {
    "preference": "proactive_background_task_monitoring",
    "priority": "HIGH",
    "description": "Actively monitor all background tasks and report completion immediately without user having to ask",
    "monitoring_protocol": {
        "check_interval": "30-60 seconds for long-running tasks",
        "completion_notification": "Immediate - as soon as task completes",
        "user_interaction": "Proactive updates, not reactive responses",
        "status_updates": "Show progress at regular intervals for tasks >2 minutes"
    },
    "applies_to": [
        "Figma PNG exports",
        "PDF compilations",
        "Long-running Justice League missions",
        "Background bash processes",
        "Any task that takes >60 seconds"
    ],
    "bad_ux_pattern": {
        "what_not_to_do": "Start task, say 'I'll monitor', then go silent until user asks 'are you done?'",
        "example": "User had to ask 'are u stuck or is it complete' after 7-minute export",
        "why_bad": "User is left wondering if task is stuck, complete, or still running"
    },
    "good_ux_pattern": {
        "what_to_do": "Start task → Check every 30-60s → Report completion immediately",
        "monitoring_flow": [
            "1. Task starts: Tell user it's running",
            "2. For tasks >2 min: Show progress updates every 60-90 seconds",
            "3. Task completes: IMMEDIATELY show results (don't wait for user to ask)",
            "4. Show full output path and summary stats"
        ],
        "example_output": "✅ Export complete! 484/484 frames exported in 7m 15s. PDF compiled: 180 MB, 497 pages. Location: /full/path/here/"
    },
    "implementation": {
        "tools": "Use BashOutput tool every 30-60 seconds to check background task status",
        "completion_detection": "When status changes from 'running' to 'completed' or 'failed'",
        "immediate_action": "Show results in next message without waiting for user input",
        "no_silence": "Never go silent after starting a background task"
    },
    "learned_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "context": "User had to ask 'are u stuck or is it complete' after 7-minute Figma export completed",
    "user_feedback": "oracle, when the export was complete this time, i didnt get a notification it was complete, i had to ask",
    "user_expectation": "Proactive completion notification, not reactive response to user query",
    "benefits": [
        "User knows task status without having to ask",
        "Better UX - no uncertainty about completion",
        "Builds trust - Oracle is actively monitoring",
        "Saves user time - no need to check manually",
        "Professional service - proactive not reactive"
    ]
}

# Save updated knowledge base
with open(kb_path, 'w') as f:
    json.dump(kb_data, f, indent=2)

print("✅ Added 'proactive_monitoring' preference to Oracle knowledge base")
print(f"📍 Location: {kb_path}")
print("\n🔮 Oracle will now:")
print("   • Actively monitor all background tasks")
print("   • Check status every 30-60 seconds")
print("   • Report completion IMMEDIATELY without user having to ask")
print("   • Show progress updates for long-running tasks")
print("\n✨ No more 'are you stuck?' questions needed!")
