"""
🦸 SUPERMAN COMMUNICATION HUB
================================

Inter-hero communication system allowing heroes to:
- Send messages to each other
- Request help
- Share findings
- Verify each other's work
- Collaborate on complex problems

Author: Superman (with Claude Code)
Created: October 21, 2025
Status: Production Ready
"""

import logging
from typing import Dict, Any, List, Optional
from collections import defaultdict
from datetime import datetime

# Import from hero_base with fallback
try:
    from .justice_league.hero_base import HeroMessage, HeroPriority
except ImportError:
    from justice_league.hero_base import HeroMessage, HeroPriority


class HeroCommunicationHub:
    """
    Central communication hub for Justice League heroes.

    Routes messages between heroes, maintains conversation threads,
    and enables real-time collaboration.
    """

    def __init__(self):
        """Initialize communication hub."""
        self.heroes: Dict[str, Any] = {}  # hero_name -> hero_instance
        self.message_queue: List[HeroMessage] = []
        self.message_history: List[HeroMessage] = []
        self.conversations: Dict[str, List[HeroMessage]] = defaultdict(list)  # conversation_id -> messages
        self.logger = logging.getLogger("SupermanCommunicationHub")
        self.logger.info("🦸 Communication Hub initialized")

    def register_hero(self, hero_name: str, hero_instance: Any):
        """
        Register a hero with the communication hub.

        Args:
            hero_name: Hero's name
            hero_instance: Hero instance (must have HeroBase)
        """
        self.heroes[hero_name] = hero_instance
        hero_instance.communication_hub = self
        self.logger.info(f"✅ Registered {hero_name} with communication hub")

    def route_message(self, message: HeroMessage):
        """
        Route a message to the appropriate hero(es).

        Args:
            message: Message to route
        """
        self.message_queue.append(message)
        self.message_history.append(message)

        # Track conversation
        conversation_id = f"{message.from_hero}_{message.to_hero}"
        self.conversations[conversation_id].append(message)

        self.logger.info(f"📨 Routing {message.message_type} from {message.from_hero} to {message.to_hero}")

        # Broadcast to all heroes
        if message.to_hero == "ALL_HEROES":
            for hero_name, hero_instance in self.heroes.items():
                if hero_name != message.from_hero:
                    hero_instance.receive_message(message)
                    self.logger.info(f"  → Delivered to {hero_name}")
        # Send to specific hero
        elif message.to_hero in self.heroes:
            hero_instance = self.heroes[message.to_hero]
            hero_instance.receive_message(message)
            self.logger.info(f"  → Delivered to {message.to_hero}")
        else:
            self.logger.warning(f"⚠️  Hero '{message.to_hero}' not registered")

    def broadcast(self, from_hero: str, message_type: str, content: Dict[str, Any]):
        """
        Broadcast a message to all heroes.

        Args:
            from_hero: Sending hero
            message_type: Type of message
            content: Message content
        """
        message = HeroMessage(
            from_hero=from_hero,
            to_hero="ALL_HEROES",
            message_type=message_type,
            content=content,
            priority=HeroPriority.MEDIUM
        )
        self.route_message(message)

    def get_conversation(self, hero1: str, hero2: str) -> List[Dict[str, Any]]:
        """
        Get conversation history between two heroes.

        Args:
            hero1: First hero
            hero2: Second hero

        Returns:
            List of messages
        """
        conversation_id_1 = f"{hero1}_{hero2}"
        conversation_id_2 = f"{hero2}_{hero1}"

        messages = []
        messages.extend(self.conversations.get(conversation_id_1, []))
        messages.extend(self.conversations.get(conversation_id_2, []))

        # Sort by timestamp
        messages.sort(key=lambda m: m.timestamp)

        return [m.to_dict() for m in messages]

    def get_all_messages_for_hero(self, hero_name: str) -> List[Dict[str, Any]]:
        """
        Get all messages involving a specific hero.

        Args:
            hero_name: Hero's name

        Returns:
            List of messages
        """
        relevant_messages = [
            msg for msg in self.message_history
            if msg.from_hero == hero_name or msg.to_hero == hero_name or msg.to_hero == "ALL_HEROES"
        ]

        return [m.to_dict() for m in relevant_messages]

    def get_pending_requests(self, hero_name: str) -> List[Dict[str, Any]]:
        """
        Get pending help requests for a hero.

        Args:
            hero_name: Hero's name

        Returns:
            List of pending help requests
        """
        pending = [
            msg for msg in self.message_queue
            if msg.to_hero == hero_name and msg.message_type == "request_help"
        ]

        return [m.to_dict() for m in pending]

    def clear_queue(self):
        """Clear processed messages from queue."""
        self.message_queue.clear()
        self.logger.info("🧹 Message queue cleared")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get communication hub statistics.

        Returns:
            Stats dict
        """
        return {
            "registered_heroes": len(self.heroes),
            "total_messages": len(self.message_history),
            "pending_messages": len(self.message_queue),
            "active_conversations": len(self.conversations),
            "heroes": list(self.heroes.keys()),
            "message_types": self._count_message_types(),
            "most_active_heroes": self._get_most_active_heroes()
        }

    def _count_message_types(self) -> Dict[str, int]:
        """Count messages by type."""
        counts = defaultdict(int)
        for msg in self.message_history:
            counts[msg.message_type] += 1
        return dict(counts)

    def _get_most_active_heroes(self) -> List[Dict[str, Any]]:
        """Get most active heroes by message count."""
        activity = defaultdict(int)
        for msg in self.message_history:
            activity[msg.from_hero] += 1

        sorted_activity = sorted(activity.items(), key=lambda x: x[1], reverse=True)
        return [{"hero": hero, "message_count": count} for hero, count in sorted_activity[:5]]

    def generate_communication_report(self) -> str:
        """
        Generate a human-readable communication report.

        Returns:
            Report string
        """
        stats = self.get_stats()

        report = []
        report.append("🦸 JUSTICE LEAGUE COMMUNICATION REPORT")
        report.append("=" * 70)
        report.append(f"Registered Heroes: {stats['registered_heroes']}")
        report.append(f"Total Messages: {stats['total_messages']}")
        report.append(f"Pending Messages: {stats['pending_messages']}")
        report.append(f"Active Conversations: {stats['active_conversations']}")

        report.append("\n📊 Message Types:")
        for msg_type, count in stats['message_types'].items():
            report.append(f"  - {msg_type}: {count}")

        report.append("\n🏆 Most Active Heroes:")
        for hero_data in stats['most_active_heroes']:
            report.append(f"  - {hero_data['hero']}: {hero_data['message_count']} messages")

        report.append("\n" + "=" * 70)

        return "\n".join(report)


# Example usage
if __name__ == "__main__":
    from justice_league.hero_base import HeroBase

    # Create communication hub
    hub = HeroCommunicationHub()

    # Create heroes
    batman = HeroBase("Batman", "🦇")
    wonder_woman = HeroBase("Wonder Woman", "⚡")
    flash = HeroBase("Flash", "⚡")

    # Register heroes
    hub.register_hero("Batman", batman)
    hub.register_hero("Wonder Woman", wonder_woman)
    hub.register_hero("Flash", flash)

    # Batman requests help from Wonder Woman
    batman.request_help("Wonder Woman", "Check accessibility of button component",
                       {"component_id": "btn-123"})

    # Wonder Woman shares finding with everyone
    wonder_woman.share_finding({
        "type": "accessibility_violation",
        "severity": "critical",
        "issue": "Missing ARIA label"
    }, broadcast=True)

    # Flash verifies with Batman
    flash.verify_with_peer({"test": "performance", "score": 95}, "Batman")

    # Get stats
    print(hub.generate_communication_report())

    # Get conversation between Batman and Wonder Woman
    conversation = hub.get_conversation("Batman", "Wonder Woman")
    print(f"\n📜 Batman ↔ Wonder Woman conversation ({len(conversation)} messages)")
