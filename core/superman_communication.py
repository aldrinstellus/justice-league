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

    # ===========================================
    # DEBATE SUPPORT
    # ===========================================

    def start_debate(self, topic: str, participants: List[str],
                    mission_context: Optional[Dict[str, Any]] = None,
                    facilitator: str = "Oracle") -> str:
        """
        Start a formal debate among heroes.

        Args:
            topic: What is being debated
            participants: List of participating heroes
            mission_context: Optional mission context
            facilitator: Who facilitates (default: Oracle)

        Returns:
            Debate ID

        Example:
            hub.start_debate(
                topic="Should we query all breakpoints first?",
                participants=["Artemis", "Batman", "Green Arrow"],
                mission_context={"mission_goal": "validate responsive design"}
            )
        """
        debate_id = f"debate_{datetime.now().timestamp()}"

        debate = {
            "debate_id": debate_id,
            "topic": topic,
            "participants": participants,
            "facilitator": facilitator,
            "mission_context": mission_context or {},
            "started_at": datetime.now().isoformat(),
            "status": "active",
            "positions": [],
            "arguments": [],
            "oracle_wisdom": None,
            "resolution": None,
            "resolved_at": None
        }

        # Store debate (using message history structure)
        if not hasattr(self, 'active_debates'):
            self.active_debates: Dict[str, Dict] = {}

        self.active_debates[debate_id] = debate

        self.logger.info(f"🎯 Debate started: '{topic}'")
        self.logger.info(f"   Participants: {', '.join(participants)}")
        self.logger.info(f"   Facilitator: {facilitator}")

        # Notify participants
        for participant in participants:
            msg = HeroMessage(
                from_hero="Superman",
                to_hero=participant,
                message_type="debate_invitation",
                content={
                    "debate_id": debate_id,
                    "topic": topic,
                    "facilitator": facilitator,
                    "mission_context": mission_context
                },
                priority=HeroPriority.HIGH
            )
            self.route_message(msg)

        return debate_id

    def present_argument(self, debate_id: str, hero: str, position: str,
                        reasoning: List[str], evidence: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Hero presents argument in debate.

        Args:
            debate_id: Debate ID
            hero: Hero presenting argument
            position: Their position
            reasoning: List of reasoning points
            evidence: Supporting evidence

        Returns:
            Argument data

        Example:
            hub.present_argument(
                debate_id="debate_123",
                hero="Artemis",
                position="Query all breakpoints first",
                reasoning=[
                    "Responsive design requires multi-breakpoint analysis",
                    "We caught 3 bugs using this approach before"
                ],
                evidence=[{"type": "knowledge_base", "workflow": "figma-mcp-claude-playwright"}]
            )
        """
        if not hasattr(self, 'active_debates') or debate_id not in self.active_debates:
            self.logger.error(f"Debate {debate_id} not found")
            return {}

        argument = {
            "argument_id": f"arg_{datetime.now().timestamp()}",
            "debate_id": debate_id,
            "hero": hero,
            "position": position,
            "reasoning": reasoning,
            "evidence": evidence or [],
            "timestamp": datetime.now().isoformat()
        }

        self.active_debates[debate_id]["arguments"].append(argument)

        self.logger.info(f"💬 {hero} presented argument in debate '{self.active_debates[debate_id]['topic']}'")
        self.logger.info(f"   Position: {position}")

        # Broadcast argument to all participants
        msg = HeroMessage(
            from_hero=hero,
            to_hero="ALL_HEROES",
            message_type="debate_argument",
            content=argument,
            priority=HeroPriority.HIGH
        )
        self.route_message(msg)

        return argument

    def counter_argument(self, debate_id: str, hero: str, original_arg_id: str,
                        counter_position: str, reasoning: List[str]) -> Dict[str, Any]:
        """
        Hero presents counter-argument to another hero's position.

        Args:
            debate_id: Debate ID
            hero: Hero presenting counter
            original_arg_id: ID of argument being countered
            counter_position: Counter position
            reasoning: Reasoning for counter

        Returns:
            Counter-argument data
        """
        if not hasattr(self, 'active_debates') or debate_id not in self.active_debates:
            self.logger.error(f"Debate {debate_id} not found")
            return {}

        counter = {
            "counter_id": f"counter_{datetime.now().timestamp()}",
            "debate_id": debate_id,
            "hero": hero,
            "counters_argument": original_arg_id,
            "counter_position": counter_position,
            "reasoning": reasoning,
            "timestamp": datetime.now().isoformat()
        }

        self.active_debates[debate_id]["arguments"].append(counter)

        self.logger.info(f"🔁 {hero} presented counter-argument")

        # Broadcast counter-argument
        msg = HeroMessage(
            from_hero=hero,
            to_hero="ALL_HEROES",
            message_type="debate_counter",
            content=counter,
            priority=HeroPriority.HIGH
        )
        self.route_message(msg)

        return counter

    def oracle_provide_wisdom(self, debate_id: str, oracle_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Oracle provides wisdom to help resolve debate.

        Args:
            debate_id: Debate ID
            oracle_analysis: Oracle's analysis of all arguments

        Returns:
            Oracle wisdom data

        Example:
            hub.oracle_provide_wisdom(
                debate_id="debate_123",
                oracle_analysis={
                    "analysis": "Both approaches have merit",
                    "recommendation": "Combine approaches - extract all breakpoints, validate in parallel",
                    "confidence": 0.95
                }
            )
        """
        if not hasattr(self, 'active_debates') or debate_id not in self.active_debates:
            self.logger.error(f"Debate {debate_id} not found")
            return {}

        wisdom = {
            "provided_by": "Oracle",
            "debate_id": debate_id,
            "analysis": oracle_analysis.get("analysis", ""),
            "recommendation": oracle_analysis.get("recommendation", ""),
            "confidence": oracle_analysis.get("confidence", 0.0),
            "reasoning": oracle_analysis.get("reasoning", []),
            "timestamp": datetime.now().isoformat()
        }

        self.active_debates[debate_id]["oracle_wisdom"] = wisdom

        self.logger.info(f"🔮 Oracle provided wisdom to debate")
        self.logger.info(f"   Recommendation: {wisdom['recommendation']}")

        # Broadcast Oracle's wisdom
        msg = HeroMessage(
            from_hero="Oracle",
            to_hero="ALL_HEROES",
            message_type="oracle_wisdom",
            content=wisdom,
            priority=HeroPriority.CRITICAL
        )
        self.route_message(msg)

        return wisdom

    def resolve_debate(self, debate_id: str, resolution: str,
                      decided_by: str = "Superman",
                      resolution_reasoning: Optional[str] = None) -> Dict[str, Any]:
        """
        Resolve a debate with final decision.

        Args:
            debate_id: Debate ID
            resolution: Final resolution/decision
            decided_by: Who made final decision
            resolution_reasoning: Reasoning for decision

        Returns:
            Resolution data
        """
        if not hasattr(self, 'active_debates') or debate_id not in self.active_debates:
            self.logger.error(f"Debate {debate_id} not found")
            return {}

        debate = self.active_debates[debate_id]

        resolution_data = {
            "resolution": resolution,
            "decided_by": decided_by,
            "reasoning": resolution_reasoning,
            "resolved_at": datetime.now().isoformat(),
            "debate_duration_minutes": self._calculate_debate_duration(debate),
            "arguments_considered": len(debate["arguments"]),
            "oracle_wisdom_used": debate["oracle_wisdom"] is not None
        }

        debate["resolution"] = resolution_data
        debate["status"] = "resolved"
        debate["resolved_at"] = resolution_data["resolved_at"]

        self.logger.info(f"✅ Debate resolved by {decided_by}")
        self.logger.info(f"   Resolution: {resolution}")

        # Broadcast resolution
        msg = HeroMessage(
            from_hero=decided_by,
            to_hero="ALL_HEROES",
            message_type="debate_resolution",
            content=resolution_data,
            priority=HeroPriority.CRITICAL
        )
        self.route_message(msg)

        # Move to completed debates
        if not hasattr(self, 'completed_debates'):
            self.completed_debates: List[Dict] = []

        self.completed_debates.append(debate)
        del self.active_debates[debate_id]

        return resolution_data

    def get_debate_status(self, debate_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a debate."""
        if hasattr(self, 'active_debates') and debate_id in self.active_debates:
            return self.active_debates[debate_id]

        if hasattr(self, 'completed_debates'):
            for debate in self.completed_debates:
                if debate["debate_id"] == debate_id:
                    return debate

        return None

    def _calculate_debate_duration(self, debate: Dict[str, Any]) -> float:
        """Calculate debate duration in minutes."""
        from datetime import datetime as dt

        start = dt.fromisoformat(debate["started_at"])
        end = dt.now()

        duration_seconds = (end - start).total_seconds()
        return round(duration_seconds / 60, 2)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get communication hub statistics.

        Returns:
            Stats dict
        """
        stats = {
            "registered_heroes": len(self.heroes),
            "total_messages": len(self.message_history),
            "pending_messages": len(self.message_queue),
            "active_conversations": len(self.conversations),
            "heroes": list(self.heroes.keys()),
            "message_types": self._count_message_types(),
            "most_active_heroes": self._get_most_active_heroes()
        }

        # Add debate stats if debates exist
        if hasattr(self, 'active_debates'):
            stats["active_debates"] = len(self.active_debates)
        if hasattr(self, 'completed_debates'):
            stats["completed_debates"] = len(self.completed_debates)

        return stats

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
