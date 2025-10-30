"""
🎯 MISSION-FOCUSED DECISION FRAMEWORK
========================================

Heroes make decisions based on what's best for mission success,
not just hierarchy or blind obedience.

This framework empowers heroes to:
- Evaluate if orders serve mission goals
- Override orders when mission requires it (with justification)
- Document reasoning for accountability
- Make evidence-based mission-critical decisions

"The mission comes first. Not authority, not hierarchy. The mission." - Superman

Author: Superman (with Claude Code)
Created: October 28, 2025
Status: Production Ready - True Autonomy
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class MissionAlignment(Enum):
    """Mission alignment levels"""
    FULLY_ALIGNED = "fully_aligned"
    PARTIALLY_ALIGNED = "partially_aligned"
    MISALIGNED = "misaligned"
    UNKNOWN = "unknown"


class DecisionLevel(Enum):
    """Decision making levels"""
    FOLLOW_ORDER = "follow_order"
    QUESTION_ORDER = "question_order"
    PROPOSE_ALTERNATIVE = "propose_alternative"
    OVERRIDE_ORDER = "override_order"


class MissionFocusedDecisionFramework:
    """
    Framework for mission-focused decision making.

    Heroes use this to evaluate orders against mission goals and
    make decisions that prioritize mission success.
    """

    def __init__(self, hero_name: str, knowledge_base: Optional[Any] = None):
        """
        Initialize mission framework.

        Args:
            hero_name: Hero's name
            knowledge_base: Optional knowledge base for context
        """
        self.hero_name = hero_name
        self.knowledge_base = knowledge_base
        self.decision_history: List[Dict[str, Any]] = []
        self.overrides: List[Dict[str, Any]] = []
        self.logger = logging.getLogger(f"JusticeLeague.{hero_name}.MissionFramework")

    def evaluate_order_vs_mission(self, order: str, mission_goals: List[str],
                                  context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Evaluate if an order aligns with mission goals.

        Args:
            order: Order received from Superman
            mission_goals: List of mission goals
            context: Optional context

        Returns:
            Evaluation with alignment level and recommendations

        Example:
            framework.evaluate_order_vs_mission(
                order="Skip accessibility testing to save time",
                mission_goals=["WCAG 2.1 AA compliance", "production-ready validation"],
                context={"deadline": "tight", "priority": "high"}
            )
        """
        self.logger.info(f"🎯 Evaluating order against mission goals...")
        self.logger.info(f"   Order: {order}")
        self.logger.info(f"   Mission Goals: {mission_goals}")

        evaluation = {
            "order": order,
            "mission_goals": mission_goals,
            "context": context or {},
            "evaluated_by": self.hero_name,
            "timestamp": datetime.now().isoformat(),
            "alignment": MissionAlignment.UNKNOWN,
            "alignment_score": 0.0,
            "conflicts": [],
            "supports": [],
            "concerns": [],
            "recommended_action": DecisionLevel.FOLLOW_ORDER,
            "reasoning": []
        }

        # Analyze alignment
        alignment_analysis = self._analyze_alignment(order, mission_goals)
        evaluation.update(alignment_analysis)

        # Determine recommended action
        recommended_action = self._determine_action(evaluation)
        evaluation["recommended_action"] = recommended_action

        # Generate reasoning
        reasoning = self._generate_reasoning(evaluation)
        evaluation["reasoning"] = reasoning

        # Log decision
        self.decision_history.append(evaluation)

        self.logger.info(f"   Alignment: {evaluation['alignment'].value}")
        self.logger.info(f"   Score: {evaluation['alignment_score']:.0%}")
        self.logger.info(f"   Recommended Action: {evaluation['recommended_action'].value}")

        return evaluation

    def justify_override(self, hero: str, order: str, override_reason: str,
                        mission_impact: str, evidence: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Justify overriding an order for mission success.

        Heroes can override orders if mission requires it, with full accountability.

        Args:
            hero: Hero overriding
            order: Original order
            override_reason: Why override is necessary
            mission_impact: How override serves mission better
            evidence: Supporting evidence

        Returns:
            Override justification

        Example:
            framework.justify_override(
                hero="Flash",
                order="Focus only on Core Web Vitals",
                override_reason="Mission goal is 'validate responsive design' - breakpoint testing is mission-critical",
                mission_impact="Without responsive testing, we miss mission-critical bugs",
                evidence={"past_bugs": 3, "workflow": "figma-mcp-claude-playwright"}
            )
        """
        self.logger.warning(f"⚠️ {hero} overriding order for mission success")
        self.logger.warning(f"   Original Order: {order}")
        self.logger.warning(f"   Reason: {override_reason}")

        override = {
            "override_id": f"override_{datetime.now().timestamp()}",
            "hero": hero,
            "original_order": order,
            "override_reason": override_reason,
            "mission_impact": mission_impact,
            "evidence": evidence or {},
            "timestamp": datetime.now().isoformat(),
            "approval_required": True,
            "approved_by": None,
            "approved_at": None,
            "status": "pending_review"
        }

        self.overrides.append(override)

        self.logger.warning(f"   Override logged for review: {override['override_id']}")

        return override

    def document_decision(self, hero: str, decision: str, reasoning: List[str],
                         outcome: Optional[str] = None) -> Dict[str, Any]:
        """
        Document a mission-focused decision for accountability.

        Args:
            hero: Hero making decision
            decision: What was decided
            reasoning: Reasoning steps
            outcome: Optional outcome (if known)

        Returns:
            Decision record
        """
        record = {
            "decision_id": f"decision_{datetime.now().timestamp()}",
            "hero": hero,
            "decision": decision,
            "reasoning": reasoning,
            "outcome": outcome,
            "timestamp": datetime.now().isoformat()
        }

        self.decision_history.append(record)

        # Store in knowledge base for learning
        if self.knowledge_base:
            self.knowledge_base.add_knowledge(
                hero=hero,
                knowledge_type="mission_decision",
                content=record,
                tags=["decision", "mission_focused", "autonomy"]
            )

        self.logger.info(f"📝 Decision documented: {decision}")

        return record

    def get_decision_history(self, hero: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get decision history, optionally filtered by hero.

        Args:
            hero: Optional hero to filter by

        Returns:
            Decision history
        """
        if hero:
            return [d for d in self.decision_history if d.get("hero") == hero or d.get("evaluated_by") == hero]
        return self.decision_history

    def get_override_history(self) -> List[Dict[str, Any]]:
        """Get history of order overrides."""
        return self.overrides

    # =========================================
    # INTERNAL ANALYSIS METHODS
    # =========================================

    def _analyze_alignment(self, order: str, mission_goals: List[str]) -> Dict[str, Any]:
        """Analyze how order aligns with mission goals."""
        order_lower = order.lower()
        conflicts = []
        supports = []
        concerns = []

        for goal in mission_goals:
            goal_lower = goal.lower()

            # Check for direct conflicts
            if self._check_conflict(order_lower, goal_lower):
                conflicts.append({
                    "goal": goal,
                    "conflict": f"Order conflicts with goal: {goal}",
                    "severity": "high"
                })

            # Check for support
            elif self._check_support(order_lower, goal_lower):
                supports.append({
                    "goal": goal,
                    "support": f"Order directly supports goal: {goal}"
                })

            # Check for concerns
            concerns_found = self._check_concerns(order_lower, goal_lower)
            if concerns_found:
                concerns.extend(concerns_found)

        # Calculate alignment score
        total_goals = len(mission_goals)
        aligned_goals = len(supports)
        conflicted_goals = len(conflicts)

        if total_goals == 0:
            alignment_score = 0.0
            alignment = MissionAlignment.UNKNOWN
        elif conflicted_goals > 0:
            alignment_score = max(0.0, (aligned_goals - conflicted_goals) / total_goals)
            alignment = MissionAlignment.MISALIGNED if alignment_score < 0.3 else MissionAlignment.PARTIALLY_ALIGNED
        elif aligned_goals == total_goals:
            alignment_score = 1.0
            alignment = MissionAlignment.FULLY_ALIGNED
        else:
            alignment_score = aligned_goals / total_goals
            alignment = MissionAlignment.PARTIALLY_ALIGNED if alignment_score >= 0.5 else MissionAlignment.UNKNOWN

        return {
            "alignment": alignment,
            "alignment_score": alignment_score,
            "conflicts": conflicts,
            "supports": supports,
            "concerns": concerns
        }

    def _check_conflict(self, order: str, goal: str) -> bool:
        """Check if order conflicts with goal."""
        conflict_patterns = [
            # Accessibility conflicts
            ("skip" in order and "accessibility" in order, "accessibility" in goal or "wcag" in goal),
            ("ignore" in order and "accessibility" in order, "accessibility" in goal),

            # Responsive design conflicts
            ("single breakpoint" in order, "responsive" in goal),
            ("desktop only" in order, "responsive" in goal or "mobile" in goal),

            # Testing conflicts
            ("skip" in order and "test" in order, "validation" in goal or "testing" in goal),

            # Quality conflicts
            ("rush" in order or "quick" in order, "quality" in goal or "thorough" in goal),
        ]

        for order_condition, goal_condition in conflict_patterns:
            if order_condition and goal_condition:
                return True

        return False

    def _check_support(self, order: str, goal: str) -> bool:
        """Check if order supports goal."""
        # Extract key terms from goal
        goal_terms = [term.strip() for term in goal.split() if len(term) > 3]

        # Check if order mentions goal terms
        for term in goal_terms:
            if term.lower() in order:
                return True

        return False

    def _check_concerns(self, order: str, goal: str) -> List[Dict[str, str]]:
        """Check for concerns between order and goal."""
        concerns = []

        # Concern: Time pressure affecting quality goal
        if ("fast" in order or "quick" in order or "rush" in order) and "quality" in goal:
            concerns.append({
                "type": "time_vs_quality",
                "concern": "Time pressure may compromise quality goal",
                "severity": "medium"
            })

        # Concern: Limited scope affecting comprehensive goal
        if "only" in order and ("comprehensive" in goal or "complete" in goal):
            concerns.append({
                "type": "scope_limitation",
                "concern": "Limited scope may not achieve comprehensive goal",
                "severity": "medium"
            })

        return concerns

    def _determine_action(self, evaluation: Dict[str, Any]) -> DecisionLevel:
        """Determine recommended action based on evaluation."""
        alignment = evaluation["alignment"]
        conflicts = len(evaluation["conflicts"])
        concerns = len(evaluation["concerns"])

        if alignment == MissionAlignment.MISALIGNED or conflicts > 0:
            if conflicts > 1:
                return DecisionLevel.OVERRIDE_ORDER
            else:
                return DecisionLevel.PROPOSE_ALTERNATIVE

        elif alignment == MissionAlignment.PARTIALLY_ALIGNED or concerns > 0:
            return DecisionLevel.QUESTION_ORDER

        elif alignment == MissionAlignment.FULLY_ALIGNED:
            return DecisionLevel.FOLLOW_ORDER

        else:
            return DecisionLevel.QUESTION_ORDER

    def _generate_reasoning(self, evaluation: Dict[str, Any]) -> List[str]:
        """Generate human-readable reasoning."""
        reasoning = []

        alignment = evaluation["alignment"]
        action = evaluation["recommended_action"]

        # Alignment reasoning
        if alignment == MissionAlignment.FULLY_ALIGNED:
            reasoning.append(f"✅ Order fully aligns with all mission goals ({evaluation['alignment_score']:.0%})")

        elif alignment == MissionAlignment.PARTIALLY_ALIGNED:
            reasoning.append(f"⚠️ Order partially aligns with mission ({evaluation['alignment_score']:.0%} alignment)")

        elif alignment == MissionAlignment.MISALIGNED:
            reasoning.append(f"❌ Order misaligned with mission goals ({evaluation['alignment_score']:.0%} alignment)")

        # Conflicts
        if evaluation["conflicts"]:
            reasoning.append(f"🚨 {len(evaluation['conflicts'])} conflict(s) detected:")
            for conflict in evaluation["conflicts"]:
                reasoning.append(f"   - {conflict['conflict']}")

        # Supports
        if evaluation["supports"]:
            reasoning.append(f"✅ {len(evaluation['supports'])} goal(s) directly supported")

        # Concerns
        if evaluation["concerns"]:
            reasoning.append(f"⚠️ {len(evaluation['concerns'])} concern(s):")
            for concern in evaluation["concerns"]:
                reasoning.append(f"   - {concern['concern']}")

        # Action reasoning
        if action == DecisionLevel.OVERRIDE_ORDER:
            reasoning.append("💥 RECOMMENDED: Override order - mission success requires different approach")

        elif action == DecisionLevel.PROPOSE_ALTERNATIVE:
            reasoning.append("💡 RECOMMENDED: Propose alternative that better serves mission goals")

        elif action == DecisionLevel.QUESTION_ORDER:
            reasoning.append("❓ RECOMMENDED: Question order to clarify mission alignment")

        else:
            reasoning.append("✅ RECOMMENDED: Follow order - aligned with mission goals")

        return reasoning


# Example usage
if __name__ == "__main__":
    # Create framework
    framework = MissionFocusedDecisionFramework("Batman")

    # Test 1: Misaligned order
    print("\n🎯 TEST 1: Misaligned Order")
    print("=" * 70)

    evaluation = framework.evaluate_order_vs_mission(
        order="Skip accessibility testing to save time",
        mission_goals=["WCAG 2.1 AA compliance", "production-ready validation"]
    )

    print(f"Alignment: {evaluation['alignment'].value}")
    print(f"Score: {evaluation['alignment_score']:.0%}")
    print(f"Action: {evaluation['recommended_action'].value}")
    print("\nReasoning:")
    for r in evaluation['reasoning']:
        print(f"  {r}")

    # Test 2: Aligned order
    print("\n\n🎯 TEST 2: Aligned Order")
    print("=" * 70)

    evaluation2 = framework.evaluate_order_vs_mission(
        order="Validate all components meet WCAG 2.1 AA standards",
        mission_goals=["WCAG 2.1 AA compliance", "accessibility validation"]
    )

    print(f"Alignment: {evaluation2['alignment'].value}")
    print(f"Score: {evaluation2['alignment_score']:.0%}")
    print(f"Action: {evaluation2['recommended_action'].value}")

    # Test 3: Override justification
    print("\n\n🎯 TEST 3: Override Justification")
    print("=" * 70)

    override = framework.justify_override(
        hero="Flash",
        order="Focus only on Core Web Vitals",
        override_reason="Mission requires responsive design validation",
        mission_impact="Without breakpoint testing, we miss mission-critical responsive bugs",
        evidence={"past_bugs_found": 3, "workflow": "figma-mcp-claude-playwright"}
    )

    print(f"Override ID: {override['override_id']}")
    print(f"Reason: {override['override_reason']}")
    print(f"Mission Impact: {override['mission_impact']}")
    print(f"Status: {override['status']}")
