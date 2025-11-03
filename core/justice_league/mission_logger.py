"""
🔮 MISSION LOGGER - Oracle's Complete Mission Documentation System

Tracks every mission from start to finish:
- User inputs and requests
- Strategy sessions and team decisions
- Hero deployments and actions
- Outcomes (success/failure) with detailed metrics
- Learnings extracted for continuous improvement

Enables self-evolution through comprehensive mission documentation.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class MissionLogger:
    """
    Comprehensive mission tracking and documentation system

    Records:
    - Mission metadata (start time, user request, context)
    - Strategy session (heroes involved, contributions, decision)
    - Execution (heroes deployed, actions taken, duration)
    - Outcomes (success/failure, accuracy, metrics, issues)
    - Learnings (patterns detected, improvements identified)
    """

    def __init__(self, missions_db_path: str):
        """
        Initialize mission logger

        Args:
            missions_db_path: Path to missions database JSON file
        """
        self.missions_db = Path(missions_db_path)
        self.missions_db.parent.mkdir(parents=True, exist_ok=True)

        # Initialize database if it doesn't exist
        if not self.missions_db.exists():
            self._initialize_database()

        self.current_mission: Optional[Dict[str, Any]] = None

    def _initialize_database(self):
        """Initialize empty missions database"""
        initial_data = {
            "missions": [],
            "total_missions": 0,
            "success_count": 0,
            "failure_count": 0,
            "learnings_extracted": 0,
            "skills_evolved": 0
        }

        with open(self.missions_db, 'w') as f:
            json.dump(initial_data, f, indent=2)

    def start_mission(
        self,
        user_request: str,
        mission_type: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Start tracking a new mission

        Args:
            user_request: Original user request/input
            mission_type: Type of mission (conversion, analysis, etc.)
            context: Optional context data

        Returns:
            Mission ID for tracking
        """
        mission_id = f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.current_mission = {
            "mission_id": mission_id,
            "user_request": user_request,
            "mission_type": mission_type,
            "context": context or {},
            "start_time": datetime.now().isoformat(),
            "strategy_session": None,
            "execution": {
                "heroes_deployed": [],
                "actions": [],
                "duration_seconds": 0
            },
            "outcome": None,
            "learnings": []
        }

        logger.info(f"🔮 Oracle: Mission {mission_id} started - {mission_type}")
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
        Log strategy session details

        Args:
            topic: Strategy session topic
            heroes: List of participating heroes
            contributions: List of hero contributions
            decision: Final decision made
            next_steps: Task assignments
        """
        if not self.current_mission:
            logger.warning("No active mission - cannot log strategy session")
            return

        self.current_mission["strategy_session"] = {
            "topic": topic,
            "heroes": heroes,
            "contributions": contributions,
            "decision": decision,
            "next_steps": next_steps,
            "timestamp": datetime.now().isoformat()
        }

        logger.debug(f"Strategy session logged: {topic}")

    def log_hero_deployment(self, hero_name: str, hero_emoji: str, task: str):
        """
        Log hero deployment

        Args:
            hero_name: Name of deployed hero
            hero_emoji: Hero emoji
            task: Task assigned to hero
        """
        if not self.current_mission:
            logger.warning("No active mission - cannot log hero deployment")
            return

        deployment = {
            "hero": f"{hero_emoji} {hero_name}",
            "task": task,
            "timestamp": datetime.now().isoformat()
        }

        self.current_mission["execution"]["heroes_deployed"].append(deployment)
        logger.debug(f"Hero deployed: {hero_emoji} {hero_name} - {task}")

    def log_action(
        self,
        hero: str,
        action: str,
        result: Optional[str] = None,
        metrics: Optional[Dict[str, Any]] = None
    ):
        """
        Log hero action during mission

        Args:
            hero: Hero performing action
            action: Action description
            result: Action result (success/failure/partial)
            metrics: Optional metrics from action
        """
        if not self.current_mission:
            logger.warning("No active mission - cannot log action")
            return

        action_entry = {
            "hero": hero,
            "action": action,
            "result": result,
            "metrics": metrics or {},
            "timestamp": datetime.now().isoformat()
        }

        self.current_mission["execution"]["actions"].append(action_entry)

    def complete_mission(
        self,
        success: bool,
        outcome_details: Dict[str, Any],
        issues_encountered: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Complete mission and record outcome

        Args:
            success: Whether mission succeeded
            outcome_details: Detailed outcome metrics
            issues_encountered: List of issues encountered

        Returns:
            Mission summary with learnings
        """
        if not self.current_mission:
            logger.warning("No active mission to complete")
            return {"error": "No active mission"}

        # Calculate duration
        start_time = datetime.fromisoformat(self.current_mission["start_time"])
        duration_seconds = (datetime.now() - start_time).total_seconds()

        self.current_mission["execution"]["duration_seconds"] = duration_seconds
        self.current_mission["end_time"] = datetime.now().isoformat()

        # Record outcome
        self.current_mission["outcome"] = {
            "success": success,
            "details": outcome_details,
            "issues_encountered": issues_encountered or [],
            "timestamp": datetime.now().isoformat()
        }

        # Extract learnings
        learnings = self._extract_learnings()
        self.current_mission["learnings"] = learnings

        # Save mission to database
        self._save_mission()

        mission_summary = {
            "mission_id": self.current_mission["mission_id"],
            "success": success,
            "duration": duration_seconds,
            "learnings_extracted": len(learnings),
            "heroes_involved": len(self.current_mission["execution"]["heroes_deployed"])
        }

        # Clear current mission
        self.current_mission = None

        logger.info(f"🔮 Oracle: Mission complete - {mission_summary}")
        return mission_summary

    def _extract_learnings(self) -> List[Dict[str, Any]]:
        """
        Extract learnings from completed mission

        Returns:
            List of learnings with actionable insights
        """
        if not self.current_mission:
            return []

        learnings = []
        outcome = self.current_mission.get("outcome", {})
        strategy = self.current_mission.get("strategy_session", {})
        execution = self.current_mission.get("execution", {})

        # Learning 1: Methodology accuracy
        if strategy and outcome:
            decision = strategy.get("decision", {})
            methodology = decision.get("choice", "")
            success = outcome.get("success", False)
            accuracy = outcome.get("details", {}).get("accuracy", 0)

            learnings.append({
                "type": "methodology_effectiveness",
                "decision": methodology,
                "success": success,
                "accuracy": accuracy,
                "insight": f"{'Confirmed' if success else 'Challenged'}: {methodology} for {self.current_mission['mission_type']}",
                "action": f"{'Reinforce' if success else 'Revise'} {methodology} recommendation"
            })

        # Learning 2: Hero performance
        for deployment in execution.get("heroes_deployed", []):
            hero = deployment["hero"]
            # Check if hero had issues
            hero_issues = [issue for issue in outcome.get("issues_encountered", []) if hero in issue]

            learnings.append({
                "type": "hero_performance",
                "hero": hero,
                "task": deployment["task"],
                "issues_count": len(hero_issues),
                "insight": f"{hero} {'performed well' if not hero_issues else f'encountered {len(hero_issues)} issues'}",
                "action": f"{'Maintain' if not hero_issues else 'Improve'} {hero} capabilities for {deployment['task']}"
            })

        # Learning 3: Decision quality
        if strategy and outcome:
            contributions_count = len(strategy.get("contributions", []))
            success = outcome.get("success", False)

            learnings.append({
                "type": "decision_quality",
                "heroes_consulted": contributions_count,
                "decision_led_to_success": success,
                "insight": f"Team decision with {contributions_count} heroes {'succeeded' if success else 'needs improvement'}",
                "action": f"{'Expand' if not success and contributions_count < 3 else 'Maintain'} team consultation"
            })

        return learnings

    def _save_mission(self):
        """Save completed mission to database"""
        if not self.current_mission:
            return

        try:
            with open(self.missions_db, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {
                "missions": [],
                "total_missions": 0,
                "success_count": 0,
                "failure_count": 0,
                "learnings_extracted": 0,
                "skills_evolved": 0
            }

        # Add mission
        data["missions"].append(self.current_mission)
        data["total_missions"] += 1

        # Update stats
        if self.current_mission.get("outcome", {}).get("success"):
            data["success_count"] += 1
        else:
            data["failure_count"] += 1

        data["learnings_extracted"] += len(self.current_mission.get("learnings", []))

        # Save
        with open(self.missions_db, 'w') as f:
            json.dump(data, f, indent=2)

    def get_mission_history(
        self,
        limit: int = 10,
        mission_type: Optional[str] = None,
        success_only: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get mission history

        Args:
            limit: Maximum missions to return
            mission_type: Filter by mission type
            success_only: Only return successful missions

        Returns:
            List of historical missions
        """
        try:
            with open(self.missions_db, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        missions = data.get("missions", [])

        # Filter
        if mission_type:
            missions = [m for m in missions if m.get("mission_type") == mission_type]

        if success_only:
            missions = [m for m in missions if m.get("outcome", {}).get("success")]

        # Sort by timestamp (most recent first) and limit
        missions.sort(key=lambda m: m.get("start_time", ""), reverse=True)
        return missions[:limit]

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get overall mission statistics

        Returns:
            Statistics about all missions
        """
        try:
            with open(self.missions_db, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        total = data.get("total_missions", 0)
        success = data.get("success_count", 0)

        return {
            "total_missions": total,
            "success_count": success,
            "failure_count": data.get("failure_count", 0),
            "success_rate": (success / total * 100) if total > 0 else 0,
            "learnings_extracted": data.get("learnings_extracted", 0),
            "skills_evolved": data.get("skills_evolved", 0)
        }
