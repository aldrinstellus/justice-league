"""
🦸 HERO BASE - Foundation for All Justice League Heroes
========================================================

Base class that gives every hero:
- Inter-hero communication
- Self-healing capabilities
- Auto-learning from failures
- Peer verification
- Error recovery
- Knowledge sharing

Author: Superman (with Claude Code)
Created: October 21, 2025
Status: Production Ready - Autonomous Foundation
"""

import logging
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
from enum import Enum
import json
from pathlib import Path


class HeroPriority(Enum):
    """Mission priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class HeroMessage:
    """Message format for inter-hero communication"""

    def __init__(self, from_hero: str, to_hero: str, message_type: str,
                 content: Dict[str, Any], priority: HeroPriority = HeroPriority.MEDIUM):
        self.from_hero = from_hero
        self.to_hero = to_hero
        self.message_type = message_type  # request_help, share_finding, verify_result, error_report
        self.content = content
        self.priority = priority
        self.timestamp = datetime.now().isoformat()
        self.message_id = f"{from_hero}_{to_hero}_{datetime.now().timestamp()}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "from_hero": self.from_hero,
            "to_hero": self.to_hero,
            "message_type": self.message_type,
            "content": self.content,
            "priority": self.priority.value,
            "timestamp": self.timestamp
        }


class HeroBase:
    """
    Base class for all Justice League heroes.

    Provides autonomous capabilities:
    - Inter-hero communication
    - Self-healing
    - Auto-learning
    - Peer verification
    - Error recovery
    """

    def __init__(self, hero_name: str, hero_emoji: str, baseline_dir: Optional[str] = None):
        """
        Initialize hero with autonomous capabilities.

        Args:
            hero_name: Hero's name (e.g., "Batman", "Wonder Woman")
            hero_emoji: Hero's emoji (e.g., "🦇", "⚡")
            baseline_dir: Directory for storing hero data
        """
        self.hero_name = hero_name
        self.hero_emoji = hero_emoji
        self.baseline_dir = Path(baseline_dir or f'/tmp/aldo-vision-{hero_name.lower().replace(" ", "-")}')
        self.baseline_dir.mkdir(parents=True, exist_ok=True)

        # Communication
        self.message_inbox: List[HeroMessage] = []
        self.message_outbox: List[HeroMessage] = []
        self.communication_hub = None  # Set by Superman

        # Learning
        self.mission_history: List[Dict[str, Any]] = []
        self.learned_patterns: List[Dict[str, Any]] = []
        self.failure_log: List[Dict[str, Any]] = []

        # Self-healing
        self.retry_count = 0
        self.max_retries = 3
        self.fallback_strategies: Dict[str, Callable] = {}

        # Knowledge
        self.knowledge_base = None  # Set by Superman

        self.logger = logging.getLogger(f"JusticeLeague.{hero_name}")
        self.logger.info(f"{self.hero_emoji} {self.hero_name} initialized with autonomous capabilities")

    # ===========================================
    # INTER-HERO COMMUNICATION
    # ===========================================

    def request_help(self, from_hero: str, message: str, context: Optional[Dict[str, Any]] = None) -> HeroMessage:
        """
        Request help from another hero.

        Args:
            from_hero: Which hero to ask for help
            message: What help is needed
            context: Additional context

        Returns:
            Message object

        Example:
            Batman requests help from Wonder Woman:
            batman.request_help("Wonder Woman", "Check accessibility of button component",
                              {"component_id": "btn-123", "url": "https://..."})
        """
        msg = HeroMessage(
            from_hero=self.hero_name,
            to_hero=from_hero,
            message_type="request_help",
            content={
                "message": message,
                "context": context or {},
                "requesting_hero_emoji": self.hero_emoji
            },
            priority=HeroPriority.HIGH
        )

        self.message_outbox.append(msg)
        self.logger.info(f"{self.hero_emoji} {self.hero_name} requesting help from {from_hero}: {message}")

        # Send via communication hub if available
        if self.communication_hub:
            self.communication_hub.route_message(msg)

        return msg

    def share_finding(self, finding: Dict[str, Any], broadcast: bool = False,
                     target_heroes: Optional[List[str]] = None):
        """
        Share a finding with other heroes.

        Args:
            finding: What was discovered
            broadcast: Share with all heroes?
            target_heroes: Specific heroes to share with

        Example:
            Wonder Woman shares accessibility issue:
            wonder_woman.share_finding({
                "type": "accessibility_violation",
                "severity": "critical",
                "issue": "Button missing ARIA label",
                "component_id": "btn-123"
            }, broadcast=True)
        """
        if broadcast:
            targets = ["ALL_HEROES"]
        else:
            targets = target_heroes or []

        for target in targets:
            msg = HeroMessage(
                from_hero=self.hero_name,
                to_hero=target,
                message_type="share_finding",
                content={
                    "finding": finding,
                    "hero_emoji": self.hero_emoji
                },
                priority=HeroPriority.MEDIUM
            )
            self.message_outbox.append(msg)

        self.logger.info(f"{self.hero_emoji} {self.hero_name} shared finding with {len(targets)} heroes")

    def verify_with_peer(self, result: Dict[str, Any], peer_hero: str) -> bool:
        """
        Ask another hero to verify this hero's work.

        Args:
            result: Result to verify
            peer_hero: Which hero should verify

        Returns:
            True if verification requested successfully

        Example:
            Flash asks Aquaman to verify network performance:
            flash.verify_with_peer({
                "test": "performance_profile",
                "lcp": 1200,
                "fid": 50
            }, "Aquaman")
        """
        msg = HeroMessage(
            from_hero=self.hero_name,
            to_hero=peer_hero,
            message_type="verify_result",
            content={
                "result": result,
                "verification_type": "peer_review",
                "requesting_hero": self.hero_name
            },
            priority=HeroPriority.HIGH
        )

        self.message_outbox.append(msg)
        self.logger.info(f"{self.hero_emoji} {self.hero_name} requesting verification from {peer_hero}")

        if self.communication_hub:
            self.communication_hub.route_message(msg)

        return True

    def receive_message(self, message: HeroMessage):
        """Receive a message from another hero."""
        self.message_inbox.append(message)
        self.logger.info(f"{self.hero_emoji} {self.hero_name} received {message.message_type} from {message.from_hero}")

        # Auto-process certain message types
        if message.message_type == "request_help":
            self._handle_help_request(message)
        elif message.message_type == "verify_result":
            self._handle_verification_request(message)

    def _handle_help_request(self, message: HeroMessage):
        """Handle incoming help request (to be overridden by heroes)."""
        self.logger.info(f"{self.hero_emoji} Received help request: {message.content.get('message')}")
        # Heroes can override this to provide specialized help

    def _handle_verification_request(self, message: HeroMessage):
        """Handle incoming verification request (to be overridden by heroes)."""
        self.logger.info(f"{self.hero_emoji} Received verification request from {message.from_hero}")
        # Heroes can override this to verify peer work

    # ===========================================
    # SELF-HEALING & ERROR RECOVERY
    # ===========================================

    def auto_recover(self, error: Exception, operation: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Automatically recover from errors.

        Args:
            error: Exception that occurred
            operation: What operation failed
            context: Context when error happened

        Returns:
            Result if recovery successful, None otherwise

        Example:
            try:
                result = hero.some_operation()
            except Exception as e:
                result = hero.auto_recover(e, "some_operation", {"param": value})
        """
        self.retry_count += 1

        self.logger.warning(f"{self.hero_emoji} Error in {operation}: {error} (Retry {self.retry_count}/{self.max_retries})")

        # Log failure
        self.failure_log.append({
            "operation": operation,
            "error": str(error),
            "error_type": type(error).__name__,
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "retry_count": self.retry_count
        })

        # Check if we have retries left
        if self.retry_count >= self.max_retries:
            self.logger.error(f"{self.hero_emoji} Max retries reached for {operation}")
            self.retry_count = 0
            return None

        # Try fallback strategy if available
        if operation in self.fallback_strategies:
            self.logger.info(f"{self.hero_emoji} Using fallback strategy for {operation}")
            try:
                fallback_func = self.fallback_strategies[operation]
                result = fallback_func(context)
                self.retry_count = 0  # Reset on success
                return result
            except Exception as fallback_error:
                self.logger.error(f"{self.hero_emoji} Fallback also failed: {fallback_error}")
                return None

        # Generic retry with exponential backoff
        import time
        wait_time = 2 ** self.retry_count
        self.logger.info(f"{self.hero_emoji} Waiting {wait_time}s before retry...")
        time.sleep(wait_time)

        return None  # Caller should retry the operation

    def register_fallback(self, operation: str, fallback_func: Callable):
        """
        Register a fallback strategy for an operation.

        Args:
            operation: Operation name
            fallback_func: Function to call if operation fails
        """
        self.fallback_strategies[operation] = fallback_func
        self.logger.info(f"{self.hero_emoji} Registered fallback for {operation}")

    # ===========================================
    # AUTO-LEARNING
    # ===========================================

    def learn_from_failure(self, failure: Dict[str, Any]):
        """
        Learn from a failure to avoid it in the future.

        Args:
            failure: Failure details

        Example:
            batman.learn_from_failure({
                "operation": "test_button",
                "error": "Element not found",
                "root_cause": "Dynamic loading",
                "solution": "Add wait for element"
            })
        """
        pattern = {
            "failure": failure,
            "timestamp": datetime.now().isoformat(),
            "learned_by": self.hero_name
        }

        self.learned_patterns.append(pattern)

        # Store to disk for persistence
        patterns_file = self.baseline_dir / "learned_patterns.json"
        with open(patterns_file, 'w') as f:
            json.dump(self.learned_patterns, f, indent=2)

        self.logger.info(f"{self.hero_emoji} Learned new pattern from failure: {failure.get('operation')}")

    def check_learned_patterns(self, operation: str) -> Optional[Dict[str, Any]]:
        """
        Check if we've learned a pattern for this operation.

        Args:
            operation: Operation to check

        Returns:
            Learned pattern if exists
        """
        for pattern in self.learned_patterns:
            if pattern.get("failure", {}).get("operation") == operation:
                self.logger.info(f"{self.hero_emoji} Found learned pattern for {operation}")
                return pattern

        return None

    def record_mission(self, mission_type: str, result: Dict[str, Any], success: bool):
        """
        Record mission for learning.

        Args:
            mission_type: Type of mission
            result: Mission results
            success: Was it successful?
        """
        mission_record = {
            "hero": self.hero_name,
            "mission_type": mission_type,
            "result": result,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }

        self.mission_history.append(mission_record)

        # Store to disk
        history_file = self.baseline_dir / "mission_history.json"
        with open(history_file, 'w') as f:
            json.dump(self.mission_history, f, indent=2)

        self.logger.info(f"{self.hero_emoji} Recorded mission: {mission_type} ({'SUCCESS' if success else 'FAILED'})")

    # ===========================================
    # KNOWLEDGE SHARING
    # ===========================================

    def contribute_to_knowledge_base(self, knowledge_type: str, content: Dict[str, Any]):
        """
        Contribute knowledge to Justice League knowledge base.

        Args:
            knowledge_type: Type of knowledge (best_practice, pattern, solution, etc.)
            content: Knowledge content
        """
        if self.knowledge_base:
            self.knowledge_base.add_knowledge(
                hero=self.hero_name,
                knowledge_type=knowledge_type,
                content=content
            )
            self.logger.info(f"{self.hero_emoji} Contributed {knowledge_type} to knowledge base")

    def query_knowledge_base(self, query: str) -> List[Dict[str, Any]]:
        """
        Query Justice League knowledge base.

        Args:
            query: What to search for

        Returns:
            List of relevant knowledge entries
        """
        if self.knowledge_base:
            results = self.knowledge_base.search(query, requesting_hero=self.hero_name)
            self.logger.info(f"{self.hero_emoji} Queried knowledge base: found {len(results)} results")
            return results
        return []

    # ===========================================
    # UTILITY METHODS
    # ===========================================

    def get_status(self) -> Dict[str, Any]:
        """
        Get hero's current status.

        Returns:
            Status dict with all autonomous capabilities
        """
        return {
            "hero": self.hero_name,
            "emoji": self.hero_emoji,
            "messages_inbox": len(self.message_inbox),
            "messages_outbox": len(self.message_outbox),
            "missions_completed": len(self.mission_history),
            "patterns_learned": len(self.learned_patterns),
            "failures_logged": len(self.failure_log),
            "fallback_strategies": len(self.fallback_strategies),
            "retry_count": self.retry_count,
            "communication_hub_connected": self.communication_hub is not None,
            "knowledge_base_connected": self.knowledge_base is not None
        }

    def __repr__(self) -> str:
        return f"{self.hero_emoji} {self.hero_name} (Autonomous Hero)"


# Example usage for testing
if __name__ == "__main__":
    # Create a hero
    batman = HeroBase("Batman", "🦇")

    # Test communication
    batman.request_help("Wonder Woman", "Check accessibility of this button")
    batman.share_finding({"issue": "Missing alt text", "severity": "high"}, broadcast=True)

    # Test learning
    batman.learn_from_failure({
        "operation": "test_button",
        "error": "Timeout",
        "solution": "Increase wait time"
    })

    # Test recovery
    try:
        raise Exception("Test error")
    except Exception as e:
        batman.auto_recover(e, "test_operation", {"test": True})

    # Get status
    status = batman.get_status()
    print(json.dumps(status, indent=2))
