"""
🔮 ORACLE SELF-LEARNING EXTENSION
Self-evolution and continuous improvement system

Features:
- Mission documentation and tracking
- Learning extraction from outcomes
- Hero skill evolution based on learnings
- Team feedback for continuous improvement
- Self-healing through pattern detection
"""

import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

from .mission_logger import MissionLogger

logger = logging.getLogger(__name__)


class OracleSelfLearning:
    """
    Extension methods for Oracle's self-learning capabilities

    Integrates with OracleMeta to provide:
    - Complete mission tracking
    - Learning extraction
    - Hero skill evolution
    - Team feedback loops
    """

    def __init__(self, oracle_instance):
        """
        Initialize self-learning system

        Args:
            oracle_instance: Parent OracleMeta instance
        """
        self.oracle = oracle_instance

        # Mission tracking
        missions_db_path = self.oracle.knowledge_base_dir / 'missions.json'
        self.mission_logger = MissionLogger(str(missions_db_path))

        # Hero skills database
        self.hero_skills_db = self.oracle.knowledge_base_dir / 'hero_skills.json'
        if not self.hero_skills_db.exists():
            self._initialize_hero_skills()

    def _initialize_hero_skills(self):
        """Initialize hero skills database"""
        initial_data = {
            "heroes": {},
            "skills_evolved": 0,
            "last_evolution": None
        }

        with open(self.hero_skills_db, 'w') as f:
            json.dump(initial_data, f, indent=2)

    def start_mission(
        self,
        user_request: str,
        mission_type: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Start tracking a mission

        Args:
            user_request: Original user input/request
            mission_type: Type of mission
            context: Optional context data

        Returns:
            Mission ID
        """
        if self.oracle.narrator:
            self.oracle.say("Mission documentation started", style="friendly",
                          technical_info=mission_type)
            self.oracle.think("Recording user request and context", category="Learning")

        mission_id = self.mission_logger.start_mission(
            user_request=user_request,
            mission_type=mission_type,
            context=context
        )

        return mission_id

    def log_strategy_session(
        self,
        topic: str,
        heroes: List[str],
        contributions: List[Dict[str, Any]],
        decision: Dict[str, Any],
        next_steps: Dict[str, str]
    ):
        """
        Log team strategy session

        Args:
            topic: Session topic
            heroes: Participating heroes
            contributions: Hero contributions
            decision: Final decision
            next_steps: Task assignments
        """
        self.mission_logger.log_strategy_session(
            topic=topic,
            heroes=heroes,
            contributions=contributions,
            decision=decision,
            next_steps=next_steps
        )

        if self.oracle.narrator:
            self.oracle.think("Strategy session documented for learning", category="Tracking")

    def complete_mission_and_learn(
        self,
        success: bool,
        outcome_details: Dict[str, Any],
        issues_encountered: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Complete mission, extract learnings, and evolve

        Args:
            success: Whether mission succeeded
            outcome_details: Detailed outcome metrics
            issues_encountered: List of issues

        Returns:
            Learning summary with evolution results
        """
        if self.oracle.narrator:
            self.oracle.say("Analyzing mission outcomes", style="friendly")
            self.oracle.think("Extracting learnings from mission results", category="Learning")

        # Complete mission and get learnings
        summary = self.mission_logger.complete_mission(
            success=success,
            outcome_details=outcome_details,
            issues_encountered=issues_encountered
        )

        # Get the completed mission for analysis
        missions = self.mission_logger.get_mission_history(limit=1)
        if not missions:
            return {"error": "No mission found"}

        completed_mission = missions[0]
        learnings = completed_mission.get("learnings", [])

        if self.oracle.narrator:
            self.oracle.think(f"Extracted {len(learnings)} learnings from mission",
                            category="Pattern Recognition")

        # Analyze learnings and evolve
        evolution_results = self._evolve_from_learnings(learnings, completed_mission)

        # Provide feedback to team
        feedback = self._generate_team_feedback(learnings, evolution_results)

        if self.oracle.narrator:
            self.oracle.say(f"Mission learning complete", style="friendly",
                          technical_info=f"{len(learnings)} learnings, {evolution_results['skills_added']} skills evolved")

        return {
            **summary,
            "learnings": learnings,
            "evolution": evolution_results,
            "team_feedback": feedback
        }

    def _evolve_from_learnings(
        self,
        learnings: List[Dict[str, Any]],
        mission: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evolve hero skills based on learnings

        Args:
            learnings: Extracted learnings from mission
            mission: Complete mission data

        Returns:
            Evolution results
        """
        skills_added = 0
        patterns_updated = 0
        methodologies_refined = 0

        # Load hero skills
        try:
            with open(self.hero_skills_db, 'r') as f:
                skills_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            skills_data = {"heroes": {}, "skills_evolved": 0}

        # Process each learning
        for learning in learnings:
            learning_type = learning.get("type")

            if learning_type == "methodology_effectiveness":
                # Update methodology patterns
                methodologies_refined += self._refine_methodology(learning, mission)

            elif learning_type == "hero_performance":
                # Evolve hero skills
                skills_added += self._add_hero_skill(learning, skills_data)

            elif learning_type == "decision_quality":
                # Update decision-making patterns
                patterns_updated += self._update_decision_patterns(learning)

        # Save evolved skills
        skills_data["skills_evolved"] += skills_added
        skills_data["last_evolution"] = datetime.now().isoformat()

        with open(self.hero_skills_db, 'w') as f:
            json.dump(skills_data, f, indent=2)

        if self.oracle.narrator and (skills_added > 0 or methodologies_refined > 0):
            self.oracle.think(f"Team evolved: +{skills_added} skills, {methodologies_refined} methodologies refined",
                            category="Evolving")

        return {
            "skills_added": skills_added,
            "patterns_updated": patterns_updated,
            "methodologies_refined": methodologies_refined
        }

    def _refine_methodology(
        self,
        learning: Dict[str, Any],
        mission: Dict[str, Any]
    ) -> int:
        """
        Refine methodology based on learning

        Args:
            learning: Methodology effectiveness learning
            mission: Mission data

        Returns:
            Number of methodologies refined
        """
        methodology = learning.get("decision", "")
        success = learning.get("success", False)
        accuracy = learning.get("accuracy", 0)

        # Update methodology in project patterns
        try:
            with open(self.oracle.project_patterns_db, 'r') as f:
                patterns = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

        methodologies = patterns.get("methodologies", {})

        # Find matching methodology
        for method_key, method_data in methodologies.items():
            if methodology.lower() in method_key.lower():
                # Update confidence based on success
                current_confidence = method_data.get("confidence", 0.5)

                if success:
                    # Increase confidence
                    new_confidence = min(1.0, current_confidence + 0.05)
                    method_data["confidence"] = new_confidence
                    method_data["success_count"] = method_data.get("success_count", 0) + 1
                else:
                    # Decrease confidence
                    new_confidence = max(0.0, current_confidence - 0.1)
                    method_data["confidence"] = new_confidence
                    method_data["failure_count"] = method_data.get("failure_count", 0) + 1

                # Update accuracy range if provided
                if accuracy > 0:
                    method_data["last_accuracy"] = accuracy

                # Save
                with open(self.oracle.project_patterns_db, 'w') as f:
                    json.dump(patterns, f, indent=2)

                return 1

        return 0

    def _add_hero_skill(
        self,
        learning: Dict[str, Any],
        skills_data: Dict[str, Any]
    ) -> int:
        """
        Add skill to hero based on learning

        Args:
            learning: Hero performance learning
            skills_data: Hero skills database

        Returns:
            Number of skills added
        """
        hero = learning.get("hero", "")
        issues_count = learning.get("issues_count", 0)
        action = learning.get("action", "")

        if issues_count == 0:
            # Hero performed well - no new skills needed
            return 0

        # Extract hero name
        hero_name = hero.split()[-1] if " " in hero else hero

        # Initialize hero skills if not exists
        if hero_name not in skills_data["heroes"]:
            skills_data["heroes"][hero_name] = {
                "skills": [],
                "improvements_needed": []
            }

        # Add improvement needed
        improvement = {
            "description": action,
            "identified_at": datetime.now().isoformat(),
            "priority": "HIGH" if issues_count > 2 else "MEDIUM"
        }

        skills_data["heroes"][hero_name]["improvements_needed"].append(improvement)

        return 1

    def _update_decision_patterns(self, learning: Dict[str, Any]) -> int:
        """
        Update decision-making patterns

        Args:
            learning: Decision quality learning

        Returns:
            Number of patterns updated
        """
        heroes_consulted = learning.get("heroes_consulted", 0)
        success = learning.get("decision_led_to_success", False)

        # Update consultation patterns in project patterns
        try:
            with open(self.oracle.project_patterns_db, 'r') as f:
                patterns = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

        # Create or update decision patterns
        if "decision_patterns" not in patterns:
            patterns["decision_patterns"] = {
                "optimal_hero_count": 2,
                "consultation_history": []
            }

        # Add to history
        patterns["decision_patterns"]["consultation_history"].append({
            "heroes_consulted": heroes_consulted,
            "success": success,
            "timestamp": datetime.now().isoformat()
        })

        # Calculate optimal hero count from history
        history = patterns["decision_patterns"]["consultation_history"]
        if len(history) >= 3:
            # Calculate average for successful decisions
            successful = [h for h in history if h.get("success")]
            if successful:
                avg_heroes = sum(h["heroes_consulted"] for h in successful) / len(successful)
                patterns["decision_patterns"]["optimal_hero_count"] = round(avg_heroes)

        # Save
        with open(self.oracle.project_patterns_db, 'w') as f:
            json.dump(patterns, f, indent=2)

        return 1

    def _generate_team_feedback(
        self,
        learnings: List[Dict[str, Any]],
        evolution: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate feedback for the team

        Args:
            learnings: Extracted learnings
            evolution: Evolution results

        Returns:
            Team feedback summary
        """
        feedback = {
            "summary": f"Mission complete. Extracted {len(learnings)} learnings.",
            "evolution_summary": f"Team evolved: +{evolution['skills_added']} skills, {evolution['methodologies_refined']} methodologies refined",
            "key_insights": [],
            "recommendations": []
        }

        # Extract key insights
        for learning in learnings:
            insight = learning.get("insight", "")
            if insight:
                feedback["key_insights"].append(insight)

            action = learning.get("action", "")
            if action:
                feedback["recommendations"].append(action)

        return feedback

    def show_team_feedback(
        self,
        feedback: Dict[str, Any],
        learnings: List[Dict[str, Any]]
    ):
        """
        Display team feedback through narrator

        Args:
            feedback: Feedback summary
            learnings: Learnings list
        """
        if not self.oracle.narrator:
            return

        self.oracle.say("", style="friendly")  # Blank line
        self.oracle.say("🔮 ORACLE TEAM FEEDBACK", style="tactical")
        self.oracle.say("=" * 78, style="friendly")

        # Summary
        self.oracle.say(feedback["summary"], style="friendly")
        self.oracle.say(feedback["evolution_summary"], style="friendly")

        # Key insights
        if feedback["key_insights"]:
            self.oracle.say("", style="friendly")
            self.oracle.say("📊 Key Insights:", style="friendly")
            for insight in feedback["key_insights"]:
                self.oracle.say(f"  • {insight}", style="friendly")

        # Recommendations
        if feedback["recommendations"]:
            self.oracle.say("", style="friendly")
            self.oracle.say("💡 Recommendations for Next Mission:", style="friendly")
            for rec in feedback["recommendations"]:
                self.oracle.say(f"  • {rec}", style="friendly")

        self.oracle.say("=" * 78, style="friendly")

    def get_learning_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about learning and evolution

        Returns:
            Learning statistics
        """
        # Mission stats
        mission_stats = self.mission_logger.get_statistics()

        # Hero skills stats
        try:
            with open(self.hero_skills_db, 'r') as f:
                skills_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            skills_data = {"skills_evolved": 0}

        return {
            **mission_stats,
            "heroes_with_improvements": len(skills_data.get("heroes", {})),
            "total_skills_evolved": skills_data.get("skills_evolved", 0)
        }
