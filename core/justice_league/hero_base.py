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

    def __init__(self, hero_name: str, hero_emoji: str, baseline_dir: Optional[str] = None, narrator: Optional[Any] = None, oracle: Optional[Any] = None):
        """
        Initialize hero with autonomous capabilities.

        Args:
            hero_name: Hero's name (e.g., "Batman", "Wonder Woman")
            hero_emoji: Hero's emoji (e.g., "🦇", "⚡")
            baseline_dir: Directory for storing hero data
            narrator: Optional MissionControlNarrator for enhanced UX
            oracle: Optional Oracle for auto-learning (v2.0)
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

        # Narrative interface (v2.0)
        self.narrator = narrator  # Optional MissionControlNarrator

        # Oracle Auto-Learning (v2.0)
        self.oracle = oracle  # Optional Oracle for auto-learning
        self.learning_session = None  # Set by Superman at mission start

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
    # CRITICAL THINKING & DEBATE
    # ===========================================

    def question_order(self, order: str, reasoning: str,
                      mission_context: Optional[Dict[str, Any]] = None) -> HeroMessage:
        """
        Question an order from Superman with critical thinking.

        Heroes can challenge directions if they have better ideas or concerns.

        Args:
            order: The order/direction received
            reasoning: Hero's reasoning for questioning
            mission_context: Optional mission context

        Returns:
            Message to Superman with question

        Example:
            batman.question_order(
                order="Test the login button",
                reasoning="Found 3 accessibility issues that prevent testing. Should we fix those first?",
                mission_context={"mission_goal": "validate accessibility"}
            )
        """
        msg = HeroMessage(
            from_hero=self.hero_name,
            to_hero="Superman",
            message_type="question_order",
            content={
                "order_received": order,
                "question": reasoning,
                "mission_context": mission_context or {},
                "hero_emoji": self.hero_emoji,
                "requires_response": True
            },
            priority=HeroPriority.HIGH
        )

        self.message_outbox.append(msg)
        self.logger.info(f"{self.hero_emoji} {self.hero_name} questioning order: {reasoning}")

        if self.communication_hub:
            self.communication_hub.route_message(msg)

        return msg

    def propose_alternative(self, current_plan: str, alternative: str,
                           reasoning: str, evidence: Optional[Dict[str, Any]] = None) -> HeroMessage:
        """
        Propose an alternative approach to the current plan.

        Args:
            current_plan: Current approach Superman suggested
            alternative: Hero's proposed alternative
            reasoning: Why the alternative is better
            evidence: Supporting evidence (knowledge base entries, past missions, etc.)

        Returns:
            Message to Superman with proposal

        Example:
            flash.propose_alternative(
                current_plan="Focus only on Core Web Vitals",
                alternative="Test Core Web Vitals AND responsive breakpoints",
                reasoning="Mission goal is 'validate responsive design'. Breakpoint testing is mission-critical.",
                evidence={"workflow": "figma-mcp-claude-playwright", "success_rate": 98}
            )
        """
        msg = HeroMessage(
            from_hero=self.hero_name,
            to_hero="Superman",
            message_type="propose_alternative",
            content={
                "current_plan": current_plan,
                "alternative_plan": alternative,
                "reasoning": reasoning,
                "evidence": evidence or {},
                "hero_emoji": self.hero_emoji
            },
            priority=HeroPriority.HIGH
        )

        self.message_outbox.append(msg)
        self.logger.info(f"{self.hero_emoji} {self.hero_name} proposing alternative: {alternative}")

        if self.communication_hub:
            self.communication_hub.route_message(msg)

        return msg

    def debate_position(self, topic: str, position: str,
                       arguments: List[str], evidence: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Take a position in a hero debate.

        Args:
            topic: What is being debated
            position: Hero's position on the topic
            arguments: List of arguments supporting position
            evidence: Optional evidence supporting arguments

        Returns:
            Debate position data

        Example:
            artemis.debate_position(
                topic="Should we query all breakpoints first?",
                position="Yes, query all breakpoints before implementation",
                arguments=[
                    "Responsive design requires multi-breakpoint analysis",
                    "We caught 3 bugs using this approach before",
                    "Figma MCP workflow recommends this"
                ],
                evidence=[
                    {"type": "knowledge_base", "workflow": "figma-mcp-claude-playwright"},
                    {"type": "past_mission", "success_rate": 98}
                ]
            )
        """
        position_data = {
            "hero": self.hero_name,
            "hero_emoji": self.hero_emoji,
            "topic": topic,
            "position": position,
            "arguments": arguments,
            "evidence": evidence or [],
            "timestamp": datetime.now().isoformat()
        }

        # Send to communication hub for debate tracking
        if self.communication_hub:
            msg = HeroMessage(
                from_hero=self.hero_name,
                to_hero="ALL_HEROES",
                message_type="debate_position",
                content=position_data,
                priority=HeroPriority.HIGH
            )
            self.communication_hub.route_message(msg)

        self.logger.info(f"{self.hero_emoji} {self.hero_name} taking position: {position}")

        return position_data

    # ===========================================
    # NARRATOR-INTEGRATED DEBATE METHODS
    # ===========================================

    def debate_with_sequential_thinking(
        self,
        position: str,
        reasoning_steps: List[str],
        evidence: Optional[str] = None
    ):
        """
        Take a position in debate using sequential thinking (narrator integration)

        Args:
            position: Hero's position statement
            reasoning_steps: List of sequential reasoning steps
            evidence: Optional evidence supporting position

        Example:
            batman.debate_with_sequential_thinking(
                position="Should we proceed knowing we'll exclude keyboard-only users?",
                reasoning_steps=[
                    "Analyzing Figma file structure",
                    "No Focus state detected in component",
                    "WCAG 2.4.7 requires visible focus indicators"
                ],
                evidence="3 CRITICAL violations found"
            )
        """
        if self.narrator:
            self.narrator.debate_position(
                f"{self.hero_emoji} {self.hero_name}",
                position,
                reasoning=reasoning_steps,
                evidence=evidence
            )

    def question_hero(
        self,
        target_hero: str,
        question: str,
        concern: Optional[str] = None
    ):
        """
        Question another hero in the debate (narrator integration)

        Args:
            target_hero: Hero being questioned (emoji + name)
            question: The question
            concern: Optional concern being raised

        Example:
            batman.question_hero(
                "🦸 Superman",
                "Should we proceed knowing we'll exclude keyboard-only users?",
                concern="Mission accessibility requirements"
            )
        """
        if self.narrator:
            self.narrator.debate_question(
                f"{self.hero_emoji} {self.hero_name}",
                target_hero,
                question,
                concern=concern
            )

    def present_evidence(
        self,
        finding: str,
        evidence_type: str = "Technical Evidence"
    ):
        """
        Present evidence in the debate (narrator integration)

        Args:
            finding: The evidence/finding
            evidence_type: Type of evidence

        Example:
            artemis.present_evidence(
                "Figma file has NO Focus state - this is a design gap",
                evidence_type="Design Analysis"
            )
        """
        if self.narrator:
            self.narrator.debate_evidence(
                f"{self.hero_emoji} {self.hero_name}",
                finding,
                evidence_type=evidence_type
            )

    def propose_solution(
        self,
        proposal: str,
        approach: Optional[str] = None
    ):
        """
        Propose a solution in the debate (narrator integration)

        Args:
            proposal: The proposed solution
            approach: Optional approach description

        Example:
            green_arrow.propose_solution(
                "Build with accessible defaults, refine with designer later",
                approach="Accessibility-first development"
            )
        """
        if self.narrator:
            self.narrator.debate_proposal(
                f"{self.hero_emoji} {self.hero_name}",
                proposal,
                approach=approach
            )

    def ask_critical_question(
        self,
        question: str,
        stakes: Optional[str] = None
    ):
        """
        Ask a mission-critical question that reframes the debate (narrator integration)

        Args:
            question: The mission-critical question
            stakes: Optional description of what's at stake

        Example:
            oracle.ask_critical_question(
                "If a student with disabilities cannot use this, have we succeeded?",
                stakes="Mission success criteria"
            )
        """
        if self.narrator:
            self.narrator.debate_critical_question(
                f"{self.hero_emoji} {self.hero_name}",
                question,
                stakes=stakes
            )

    def evaluate_mission_alignment(self, order: str, mission_goals: List[str]) -> Dict[str, Any]:
        """
        Evaluate if an order aligns with mission goals.

        Heroes can identify when orders might not serve the mission's best interest.

        Args:
            order: Order received
            mission_goals: List of mission goals

        Returns:
            Evaluation result with alignment score and reasoning

        Example:
            batman.evaluate_mission_alignment(
                order="Skip accessibility testing to save time",
                mission_goals=["WCAG 2.1 AA compliance", "production-ready validation"]
            )
            # Returns: {"aligned": False, "concerns": ["Skipping accessibility conflicts with WCAG goal"]}
        """
        aligned = True
        concerns = []
        recommendations = []

        # Check if order conflicts with stated mission goals
        order_lower = order.lower()

        for goal in mission_goals:
            goal_lower = goal.lower()

            # Simple keyword matching (can be enhanced with NLP)
            if "accessibility" in goal_lower and "skip" in order_lower and "accessibility" in order_lower:
                aligned = False
                concerns.append(f"Order conflicts with mission goal: {goal}")
                recommendations.append(f"Reconsider skipping {goal}")

            if "responsive" in goal_lower and "single breakpoint" in order_lower:
                aligned = False
                concerns.append(f"Testing single breakpoint may miss responsive issues for goal: {goal}")
                recommendations.append("Test all breakpoints as per mission goal")

        evaluation = {
            "order": order,
            "mission_goals": mission_goals,
            "aligned": aligned,
            "alignment_score": 1.0 if aligned else 0.0,
            "concerns": concerns,
            "recommendations": recommendations,
            "evaluated_by": self.hero_name,
            "timestamp": datetime.now().isoformat()
        }

        # Log mission-critical concerns
        if not aligned:
            self.logger.warning(
                f"{self.hero_emoji} {self.hero_name} detected mission misalignment: {concerns}"
            )

            # Contribute concern to knowledge base
            if self.knowledge_base:
                self.contribute_to_knowledge_base(
                    knowledge_type="mission_misalignment",
                    content=evaluation
                )

        return evaluation

    def investigate_claim(self, claim: str, source: str,
                         context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Investigate a claim instead of accepting it at face value.

        Used by detective heroes (especially Batman) to verify information.

        Args:
            claim: Claim to investigate
            source: Who made the claim
            context: Investigation context

        Returns:
            Investigation results

        Example:
            batman.investigate_claim(
                claim="All buttons are accessible",
                source="Initial report",
                context={"page_url": "https://example.com"}
            )
        """
        investigation = {
            "claim": claim,
            "source": source,
            "investigator": self.hero_name,
            "context": context or {},
            "verified": None,  # To be determined by investigation
            "evidence": [],
            "inconsistencies": [],
            "conclusion": "",
            "timestamp": datetime.now().isoformat()
        }

        self.logger.info(f"{self.hero_emoji} {self.hero_name} investigating claim: '{claim}' from {source}")

        # Check knowledge base for related information
        if self.knowledge_base:
            related_knowledge = self.query_knowledge_base(claim)
            if related_knowledge:
                investigation["evidence"].append({
                    "type": "knowledge_base",
                    "entries": len(related_knowledge),
                    "summary": "Found related patterns in knowledge base"
                })

        # Check past missions for similar claims
        for mission in self.mission_history:
            if claim.lower() in str(mission).lower():
                investigation["evidence"].append({
                    "type": "past_mission",
                    "mission": mission.get("mission_type"),
                    "outcome": mission.get("success")
                })

        # Heroes can override this method with specialized investigation logic
        investigation = self._conduct_specialized_investigation(investigation)

        return investigation

    def _conduct_specialized_investigation(self, investigation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hook for heroes to add specialized investigation logic.

        Override this in hero subclasses (e.g., Batman's detective skills).
        """
        # Default: mark as investigated but not conclusive
        investigation["conclusion"] = f"{self.hero_name} investigated claim. No specialized analysis available."
        investigation["verified"] = None
        return investigation

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

    # ===========================================
    # NARRATIVE INTERFACE (v2.0)
    # ===========================================

    def say(self, message: str, style: str = "friendly", technical_info: Optional[str] = None):
        """
        Convenience method for hero dialogue via narrator.

        Args:
            message: What the hero says
            style: Banter style (tactical, friendly, sequential)
            technical_info: Optional technical detail to show inline

        Example:
            batman.say("All tests passed", style="tactical", technical_info="26 tests, 0 failures")
        """
        if self.narrator:
            hero_label = f"{self.hero_emoji} {self.hero_name}"
            self.narrator.hero_speaks(hero_label, message, style, technical_info)

    def think(self, thought: str, step: Optional[int] = None, category: Optional[str] = None):
        """
        Convenience method for sequential thinking via narrator.

        Args:
            thought: The reasoning step
            step: Step number (auto-increments if None)
            category: Label like "Scanning", "Analyzing", "Hypothesis"

        Example:
            oracle.think("Checking knowledge base for patterns", category="Scanning")
        """
        if self.narrator:
            hero_label = f"{self.hero_emoji} {self.hero_name}"
            self.narrator.hero_thinks(hero_label, thought, step, category)

    def handoff(self, to_hero: str, task: str, context: Optional[Dict[str, Any]] = None):
        """
        Convenience method for hero-to-hero handoff via narrator.

        Args:
            to_hero: Hero receiving task
            task: What needs to be done
            context: Optional context information

        Example:
            superman.handoff("🦅 Hawkman", "Export frames as PNG", {"file_key": "ABC123"})
        """
        if self.narrator:
            from_hero_label = f"{self.hero_emoji} {self.hero_name}"
            self.narrator.team_handoff(from_hero_label, to_hero, task, context)

    # ===========================================
    # ORACLE AUTO-LEARNING HOOKS (v2.0)
    # ===========================================

    def _start_operation(self, operation_name: str, context: Dict[str, Any]):
        """
        Hook called at the start of any hero operation for auto-learning.

        This is the entry point for Oracle's automatic learning system.
        Call this at the beginning of any significant operation.

        Args:
            operation_name: Name of the operation (e.g., "generate_component_code_expert")
            context: Operation context (parameters, config, etc.)

        Example:
            def some_operation(self, param1, param2):
                # Start operation hook
                self._start_operation('some_operation', {
                    'param1': param1,
                    'param2': param2
                })

                # ... operation logic ...
        """
        # Log to learning session if available
        if self.learning_session:
            self.learning_session.log_operation_start(
                hero=self.hero_name,
                operation=operation_name,
                context=context
            )
            self.logger.debug(
                f"{self.hero_emoji} Operation started: {operation_name} "
                f"[Session: {self.learning_session.session_id}]"
            )

    def _complete_operation(self, operation_name: str, result: Dict[str, Any]):
        """
        Hook called at the end of any hero operation for auto-learning.

        This triggers Oracle's learning from the operation results.
        Call this after completing any significant operation.

        Args:
            operation_name: Name of the operation
            result: Operation result including:
                - success: bool (required)
                - score: float (optional, 0-100)
                - error: str (optional, if failed)
                - ... other result data

        Example:
            def some_operation(self, param1, param2):
                self._start_operation('some_operation', {...})

                try:
                    # ... operation logic ...
                    result = {'success': True, 'score': 95, 'data': {...}}

                    # Complete operation hook
                    self._complete_operation('some_operation', result)
                    return result

                except Exception as e:
                    # Error handling with hook
                    error_result = {'success': False, 'error': str(e)}
                    self._complete_operation('some_operation', error_result)
                    raise
        """
        # Log to learning session if available
        if self.learning_session:
            self.learning_session.log_operation_complete(
                hero=self.hero_name,
                operation=operation_name,
                result=result
            )
            self.logger.debug(
                f"{self.hero_emoji} Operation completed: {operation_name} "
                f"[Success: {result.get('success', False)}]"
            )

        # Trigger Oracle auto-learning
        if self.oracle:
            self.oracle.learn_from_operation(
                hero=self.hero_name,
                operation=operation_name,
                result=result,
                session=self.learning_session
            )

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
