"""
🦸 SUPERMAN MISSION PLANNER
============================

Intelligent mission planning and hero deployment for Justice League.

Superman's strategic brain that:
- Analyzes targets (URL, Figma file, codebase)
- Auto-detects what needs testing/validation
- Plans multi-phase missions with dependencies
- Deploys optimal hero combinations
- Adapts plans based on findings

Author: Superman (with Claude Code)
Created: October 21, 2025
Status: Production Ready - Strategic Intelligence
"""

import logging
from typing import Dict, Any, List, Optional, Set, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import json
from pathlib import Path


class MissionPhase(Enum):
    """Mission phases"""
    RECONNAISSANCE = "reconnaissance"
    EXTRACTION = "extraction"
    ANALYSIS = "analysis"
    VALIDATION = "validation"
    REMEDIATION = "remediation"
    VERIFICATION = "verification"


class MissionPriority(Enum):
    """Mission priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TargetType(Enum):
    """Types of mission targets"""
    URL = "url"
    FIGMA_FILE = "figma_file"
    CODEBASE = "codebase"
    COMPONENT = "component"
    DESIGN_SYSTEM = "design_system"
    API = "api"


@dataclass
class MissionTask:
    """Individual task within a mission"""
    task_id: str
    task_type: str
    assigned_hero: str
    description: str
    phase: MissionPhase
    priority: MissionPriority
    dependencies: List[str] = field(default_factory=list)
    estimated_duration: int = 60  # seconds
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


@dataclass
class Mission:
    """Complete mission with all tasks and metadata"""
    mission_id: str
    mission_name: str
    target: str
    target_type: TargetType
    phases: List[MissionPhase]
    tasks: List[MissionTask]
    priority: MissionPriority
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    status: str = "planned"  # planned, in_progress, completed, failed
    success_criteria: Dict[str, Any] = field(default_factory=dict)
    results: Dict[str, Any] = field(default_factory=dict)


class SupermanMissionPlanner:
    """
    Superman's intelligent mission planning system.

    Analyzes targets, detects requirements, plans optimal strategies,
    and coordinates hero deployment.
    """

    def __init__(self, knowledge_base=None, communication_hub=None):
        """
        Initialize mission planner.

        Args:
            knowledge_base: Justice League knowledge base
            communication_hub: Hero communication hub
        """
        self.knowledge_base = knowledge_base
        self.communication_hub = communication_hub

        # Mission tracking
        self.missions: List[Mission] = []
        self.active_missions: Dict[str, Mission] = {}

        # Hero capabilities mapping
        self.hero_capabilities = {
            "Batman": ["button_testing", "form_testing", "interaction_testing", "javascript_testing"],
            "Wonder Woman": ["accessibility", "wcag", "aria", "contrast", "keyboard_nav"],
            "Flash": ["performance", "lcp", "fid", "cls", "core_web_vitals"],
            "Aquaman": ["network", "api_testing", "http_monitoring", "websocket"],
            "Cyborg": ["security", "xss", "csrf", "ssl", "headers", "authentication"],
            "Green Lantern": ["regression", "visual_diff", "screenshot_comparison"],
            "Hawkgirl": ["seo", "meta_tags", "structured_data", "robots"],
            "Martian Manhunter": ["cross_browser", "compatibility", "polyfills"],
            "Black Canary": ["forms", "validation", "input_testing"],
            "Green Arrow": ["links", "navigation", "routing"],
            "Zatanna": ["css", "styling", "layout", "responsive"],
            "Shazam": ["mobile", "touch", "gestures", "viewport"],
            "Artemis": ["design_system", "component_library", "shadcn", "figma_validation"]
        }

        # Task templates for common scenarios
        self.task_templates = self._build_task_templates()

        self.logger = logging.getLogger("SupermanMissionPlanner")
        self.logger.info("🦸 Mission Planner initialized with strategic intelligence")

    def analyze_target(self, target: str, target_type: Optional[str] = None,
                      context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze target and determine requirements.

        Args:
            target: Target URL, file path, or identifier
            target_type: Type of target (url, figma_file, codebase, etc.)
            context: Additional context

        Returns:
            Analysis result with detected requirements
        """
        context = context or {}

        self.logger.info(f"🔍 Analyzing target: {target}")

        # Auto-detect target type if not provided
        if not target_type:
            target_type = self._detect_target_type(target)

        target_type_enum = TargetType(target_type)

        # Analyze based on type
        if target_type_enum == TargetType.FIGMA_FILE:
            return self._analyze_figma_target(target, context)
        elif target_type_enum == TargetType.URL:
            return self._analyze_url_target(target, context)
        elif target_type_enum == TargetType.CODEBASE:
            return self._analyze_codebase_target(target, context)
        elif target_type_enum == TargetType.DESIGN_SYSTEM:
            return self._analyze_design_system_target(target, context)
        else:
            return self._analyze_generic_target(target, context)

    def plan_mission(self, target: str, goal: str,
                    target_type: Optional[str] = None,
                    priority: str = "medium",
                    context: Optional[Dict[str, Any]] = None) -> Mission:
        """
        Plan a complete mission for a target.

        NOW ENHANCED with strategic insights from Superman's Brain!

        Args:
            target: Target to analyze
            goal: Mission goal (e.g., "validate design system")
            target_type: Type of target
            priority: Mission priority
            context: Additional context (may include strategic_insights)

        Returns:
            Complete mission plan (enhanced with strategic reasoning)
        """
        context = context or {}

        # NEW: Extract strategic insights if available
        strategic_insights = context.get('strategic_insights')
        if strategic_insights:
            self.logger.info(f"🧠 Using strategic insights from Superman's Brain")
            self.logger.info(f"   Hypothesis: {strategic_insights.hypothesis[:80]}...")
            self.logger.info(f"   Confidence: {strategic_insights.confidence:.1%}")

        self.logger.info(f"🎯 Planning mission: {goal}")
        self.logger.info(f"   Target: {target}")

        # Analyze target
        analysis = self.analyze_target(target, target_type, context)

        # NEW: Enhance hero deployment with strategic insights
        if strategic_insights:
            analysis = self._enhance_with_strategic_insights(analysis, strategic_insights)

        # Determine required phases
        phases = self._determine_phases(analysis, goal)

        # Generate tasks for each phase
        tasks = self._generate_tasks(analysis, phases, goal)

        # Optimize task order based on dependencies
        optimized_tasks = self._optimize_task_order(tasks)

        # Create mission
        mission_id = f"mission_{datetime.now().timestamp()}"
        mission = Mission(
            mission_id=mission_id,
            mission_name=f"{goal} - {target}",
            target=target,
            target_type=TargetType(analysis["target_type"]),
            phases=phases,
            tasks=optimized_tasks,
            priority=MissionPriority(priority),
            created_at=datetime.now().isoformat(),
            success_criteria=self._define_success_criteria(goal, analysis)
        )

        self.missions.append(mission)

        self.logger.info(f"✅ Mission planned: {len(optimized_tasks)} tasks across {len(phases)} phases")
        self._log_mission_summary(mission)

        # Store in knowledge base
        if self.knowledge_base:
            self.knowledge_base.add_knowledge(
                hero="Superman",
                knowledge_type="mission_plan",
                content={
                    "mission_id": mission_id,
                    "goal": goal,
                    "target": target,
                    "task_count": len(optimized_tasks),
                    "phases": [p.value for p in phases]
                },
                tags=["mission_planning", "strategy", target_type or "unknown"]
            )

        return mission

    def get_next_tasks(self, mission: Mission, hero_availability: Optional[Dict[str, bool]] = None) -> List[MissionTask]:
        """
        Get next tasks ready to execute based on dependencies.

        Args:
            mission: Mission to check
            hero_availability: Dict of hero_name -> is_available

        Returns:
            List of tasks ready to execute
        """
        hero_availability = hero_availability or {}

        ready_tasks = []

        for task in mission.tasks:
            # Skip if not pending
            if task.status != "pending":
                continue

            # Check if dependencies are met
            dependencies_met = all(
                self._is_task_completed(mission, dep_id)
                for dep_id in task.dependencies
            )

            if not dependencies_met:
                continue

            # Check hero availability
            if hero_availability and not hero_availability.get(task.assigned_hero, True):
                continue

            ready_tasks.append(task)

        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        ready_tasks.sort(key=lambda t: priority_order.get(t.priority.value, 999))

        return ready_tasks

    def suggest_hero_for_task(self, task_type: str, context: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Suggest best heroes for a task type.

        Args:
            task_type: Type of task
            context: Additional context

        Returns:
            List of hero names ranked by suitability
        """
        suggestions = []

        # Check hero capabilities
        for hero, capabilities in self.hero_capabilities.items():
            if task_type in capabilities:
                suggestions.append(hero)

        # If no exact match, find related capabilities
        if not suggestions:
            task_keywords = task_type.split("_")
            for hero, capabilities in self.hero_capabilities.items():
                for capability in capabilities:
                    if any(keyword in capability for keyword in task_keywords):
                        if hero not in suggestions:
                            suggestions.append(hero)
                        break

        # Query knowledge base for historical performance
        if self.knowledge_base and suggestions:
            performance_data = self.knowledge_base.search(
                query=task_type,
                knowledge_type="mission_result",
                limit=20
            )

            # Rank by success rate
            success_rates = defaultdict(lambda: {"success": 0, "total": 0})
            for entry in performance_data:
                hero = entry.get("hero")
                success = entry.get("content", {}).get("success", False)
                if hero in suggestions:
                    success_rates[hero]["total"] += 1
                    if success:
                        success_rates[hero]["success"] += 1

            # Re-rank suggestions by success rate
            suggestions.sort(
                key=lambda h: (
                    success_rates[h]["success"] / success_rates[h]["total"]
                    if success_rates[h]["total"] > 0 else 0.5
                ),
                reverse=True
            )

        return suggestions

    def _detect_target_type(self, target: str) -> str:
        """Auto-detect target type from target string."""
        if "figma.com" in target:
            return "figma_file"
        elif target.startswith("http://") or target.startswith("https://"):
            return "url"
        elif "/" in target or "\\" in target:
            return "codebase"
        else:
            return "component"

    def _analyze_figma_target(self, target: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze Figma file target."""
        return {
            "target_type": "figma_file",
            "target": target,
            "required_heroes": ["Artemis", "Wonder Woman", "Zatanna"],
            "phases": ["extraction", "analysis", "validation"],
            "capabilities_needed": [
                "figma_extraction",
                "design_system_validation",
                "component_mapping",
                "accessibility_check",
                "styling_analysis"
            ],
            "estimated_duration": 300,
            "context": context
        }

    def _analyze_url_target(self, target: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze URL target."""
        return {
            "target_type": "url",
            "target": target,
            "required_heroes": [
                "Batman", "Wonder Woman", "Flash", "Aquaman",
                "Cyborg", "Green Lantern", "Hawkgirl"
            ],
            "phases": ["reconnaissance", "analysis", "validation", "verification"],
            "capabilities_needed": [
                "button_testing", "accessibility", "performance",
                "network", "security", "seo"
            ],
            "estimated_duration": 600,
            "context": context
        }

    def _analyze_codebase_target(self, target: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze codebase target."""
        return {
            "target_type": "codebase",
            "target": target,
            "required_heroes": ["Batman", "Cyborg", "Martian Manhunter"],
            "phases": ["reconnaissance", "analysis", "validation"],
            "capabilities_needed": [
                "code_analysis", "security", "cross_browser"
            ],
            "estimated_duration": 400,
            "context": context
        }

    def _analyze_design_system_target(self, target: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze design system target."""
        return {
            "target_type": "design_system",
            "target": target,
            "required_heroes": ["Artemis", "Wonder Woman", "Zatanna"],
            "phases": ["extraction", "analysis", "validation", "remediation"],
            "capabilities_needed": [
                "component_library", "accessibility", "css", "design_tokens"
            ],
            "estimated_duration": 400,
            "context": context
        }

    def _analyze_generic_target(self, target: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze generic target."""
        return {
            "target_type": "component",
            "target": target,
            "required_heroes": ["Batman", "Wonder Woman"],
            "phases": ["analysis", "validation"],
            "capabilities_needed": ["testing", "accessibility"],
            "estimated_duration": 180,
            "context": context
        }

    def _determine_phases(self, analysis: Dict[str, Any], goal: str) -> List[MissionPhase]:
        """Determine required mission phases."""
        suggested_phases = analysis.get("phases", [])

        # Convert to enums
        phases = []
        for phase_name in suggested_phases:
            try:
                phases.append(MissionPhase(phase_name))
            except ValueError:
                self.logger.warning(f"Unknown phase: {phase_name}")

        return phases or [MissionPhase.ANALYSIS, MissionPhase.VALIDATION]

    def _generate_tasks(self, analysis: Dict[str, Any], phases: List[MissionPhase],
                       goal: str) -> List[MissionTask]:
        """Generate tasks for mission phases."""
        tasks = []
        task_counter = 0

        target_type = analysis["target_type"]
        required_heroes = analysis.get("required_heroes", [])
        capabilities_needed = analysis.get("capabilities_needed", [])

        # Generate tasks for each phase
        for phase in phases:
            phase_tasks = self._generate_phase_tasks(
                phase, target_type, required_heroes, capabilities_needed, task_counter
            )
            tasks.extend(phase_tasks)
            task_counter += len(phase_tasks)

        return tasks

    def _generate_phase_tasks(self, phase: MissionPhase, target_type: str,
                             required_heroes: List[str], capabilities: List[str],
                             start_id: int) -> List[MissionTask]:
        """Generate tasks for a specific phase."""
        tasks = []

        if phase == MissionPhase.EXTRACTION and target_type == "figma_file":
            tasks.append(MissionTask(
                task_id=f"task_{start_id}",
                task_type="figma_extraction",
                assigned_hero="Artemis",
                description="Extract design system from Figma",
                phase=phase,
                priority=MissionPriority.HIGH
            ))

        elif phase == MissionPhase.ANALYSIS:
            if "Artemis" in required_heroes:
                tasks.append(MissionTask(
                    task_id=f"task_{start_id + len(tasks)}",
                    task_type="design_system_validation",
                    assigned_hero="Artemis",
                    description="Validate design system compliance",
                    phase=phase,
                    priority=MissionPriority.HIGH,
                    dependencies=[f"task_{start_id - 1}"] if start_id > 0 else []
                ))

            if "Wonder Woman" in required_heroes:
                tasks.append(MissionTask(
                    task_id=f"task_{start_id + len(tasks)}",
                    task_type="accessibility_analysis",
                    assigned_hero="Wonder Woman",
                    description="Analyze accessibility compliance",
                    phase=phase,
                    priority=MissionPriority.HIGH
                ))

            if "Flash" in required_heroes:
                tasks.append(MissionTask(
                    task_id=f"task_{start_id + len(tasks)}",
                    task_type="performance_analysis",
                    assigned_hero="Flash",
                    description="Analyze performance metrics",
                    phase=phase,
                    priority=MissionPriority.MEDIUM
                ))

        elif phase == MissionPhase.VALIDATION:
            if "Batman" in required_heroes:
                tasks.append(MissionTask(
                    task_id=f"task_{start_id + len(tasks)}",
                    task_type="interaction_testing",
                    assigned_hero="Batman",
                    description="Test interactive components",
                    phase=phase,
                    priority=MissionPriority.HIGH
                ))

            if "Cyborg" in required_heroes:
                tasks.append(MissionTask(
                    task_id=f"task_{start_id + len(tasks)}",
                    task_type="security_validation",
                    assigned_hero="Cyborg",
                    description="Validate security measures",
                    phase=phase,
                    priority=MissionPriority.CRITICAL
                ))

        return tasks

    def _optimize_task_order(self, tasks: List[MissionTask]) -> List[MissionTask]:
        """Optimize task execution order based on dependencies."""
        # Topological sort based on dependencies
        optimized = []
        completed_ids = set()

        remaining = tasks.copy()
        max_iterations = len(tasks) * 2
        iteration = 0

        while remaining and iteration < max_iterations:
            iteration += 1
            made_progress = False

            for task in remaining[:]:
                # Check if all dependencies are completed
                if all(dep_id in completed_ids for dep_id in task.dependencies):
                    optimized.append(task)
                    completed_ids.add(task.task_id)
                    remaining.remove(task)
                    made_progress = True

            if not made_progress:
                # Break circular dependencies
                self.logger.warning("Circular dependencies detected, breaking...")
                optimized.extend(remaining)
                break

        return optimized

    def _define_success_criteria(self, goal: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Define success criteria for mission."""
        criteria = {
            "all_tasks_completed": True,
            "critical_tasks_passed": True,
            "min_score": 70.0
        }

        if "design_system" in goal.lower():
            criteria.update({
                "component_coverage": 80.0,
                "design_token_health": 70.0,
                "missing_critical_components": 0
            })

        if "accessibility" in goal.lower():
            criteria.update({
                "wcag_compliance": "AA",
                "critical_violations": 0
            })

        if "performance" in goal.lower():
            criteria.update({
                "lcp": 2.5,
                "fid": 100,
                "cls": 0.1
            })

        return criteria

    def _is_task_completed(self, mission: Mission, task_id: str) -> bool:
        """Check if a task is completed."""
        for task in mission.tasks:
            if task.task_id == task_id:
                return task.status == "completed"
        return False

    def _log_mission_summary(self, mission: Mission):
        """Log mission summary."""
        self.logger.info(f"\n{'=' * 70}")
        self.logger.info(f"🎯 MISSION: {mission.mission_name}")
        self.logger.info(f"{'=' * 70}")
        self.logger.info(f"ID: {mission.mission_id}")
        self.logger.info(f"Target: {mission.target}")
        self.logger.info(f"Priority: {mission.priority.value}")
        self.logger.info(f"Phases: {len(mission.phases)}")
        self.logger.info(f"Tasks: {len(mission.tasks)}")

        # Group tasks by phase
        tasks_by_phase = defaultdict(list)
        for task in mission.tasks:
            tasks_by_phase[task.phase].append(task)

        for phase, tasks in tasks_by_phase.items():
            self.logger.info(f"\n{phase.value.upper()}: {len(tasks)} tasks")
            for task in tasks:
                deps = f" (deps: {', '.join(task.dependencies)})" if task.dependencies else ""
                self.logger.info(f"  - {task.assigned_hero}: {task.description}{deps}")

        self.logger.info(f"\n{'=' * 70}")

    def _enhance_with_strategic_insights(self,
                                        analysis: Dict[str, Any],
                                        strategic_insights: Any) -> Dict[str, Any]:
        """
        🧠 NEW: Enhance mission analysis with strategic insights

        Superman's Brain provides strategic thinking results, and this method
        uses them to improve hero deployment decisions.

        Args:
            analysis: Initial analysis from analyze_target
            strategic_insights: Strategic insights from Superman's Brain

        Returns:
            Enhanced analysis with smarter hero deployment
        """
        enhanced = analysis.copy()
        required_heroes = enhanced.get("required_heroes", [])

        self.logger.info(f"🧠 Enhancing mission with strategic insights...")

        # Process strategic recommendations
        for rec in strategic_insights.recommendations:
            action = rec.get('action')

            if action == 'deploy_hero':
                hero = rec.get('hero')
                reason = rec.get('reason', 'Strategic recommendation')
                if hero and hero not in required_heroes:
                    required_heroes.append(hero)
                    self.logger.info(f"   + Adding {hero}: {reason}")

            elif action == 'use_workflow':
                workflow = rec.get('workflow')
                reason = rec.get('reason', 'Workflow detected')

                if workflow == 'figma-mcp-claude-playwright':
                    # Responsive component library workflow
                    self.logger.info(f"   🔄 Using {workflow}")
                    self.logger.info(f"      Reason: {reason}")

                    # Add heroes needed for this workflow
                    workflow_heroes = {
                        "Artemis": "Figma extraction & analysis",
                        "Green Arrow": "Playwright validation",
                        "Hawkman": "Structural parsing"
                    }

                    for hero, hero_reason in workflow_heroes.items():
                        if hero not in required_heroes:
                            required_heroes.append(hero)
                            self.logger.info(f"   + Adding {hero}: {hero_reason}")

        enhanced["required_heroes"] = required_heroes
        enhanced["strategic_insights_applied"] = True
        enhanced["strategic_confidence"] = strategic_insights.confidence

        self.logger.info(f"   ✅ Enhanced: {len(required_heroes)} heroes deployed")
        return enhanced

    def _build_task_templates(self) -> Dict[str, Dict[str, Any]]:
        """Build task templates for common scenarios."""
        return {
            "figma_full_analysis": {
                "phases": [MissionPhase.EXTRACTION, MissionPhase.ANALYSIS, MissionPhase.VALIDATION],
                "heroes": ["Artemis", "Wonder Woman", "Zatanna"]
            },
            "url_full_audit": {
                "phases": [MissionPhase.RECONNAISSANCE, MissionPhase.ANALYSIS,
                          MissionPhase.VALIDATION, MissionPhase.VERIFICATION],
                "heroes": ["Batman", "Wonder Woman", "Flash", "Aquaman", "Cyborg"]
            },
            "accessibility_only": {
                "phases": [MissionPhase.ANALYSIS, MissionPhase.VALIDATION],
                "heroes": ["Wonder Woman"]
            },
            "performance_only": {
                "phases": [MissionPhase.ANALYSIS, MissionPhase.VALIDATION],
                "heroes": ["Flash", "Aquaman"]
            }
        }


# Example usage
if __name__ == "__main__":
    # Create planner
    planner = SupermanMissionPlanner()

    # Example 1: Plan Figma design system mission
    print("\n🎯 Example 1: Figma Design System Mission")
    figma_mission = planner.plan_mission(
        target="https://www.figma.com/design/aKLI77flT3sx0kXMPq2BtZ/ATC-RFP",
        goal="Validate shadcn/ui compliance",
        target_type="figma_file",
        priority="high"
    )

    # Get next tasks
    next_tasks = planner.get_next_tasks(figma_mission)
    print(f"\n📋 Ready to execute: {len(next_tasks)} tasks")
    for task in next_tasks:
        print(f"  - {task.assigned_hero}: {task.description}")

    # Example 2: Plan URL audit mission
    print("\n\n🎯 Example 2: URL Full Audit Mission")
    url_mission = planner.plan_mission(
        target="https://example.com/dashboard",
        goal="Complete quality audit",
        target_type="url",
        priority="medium"
    )

    # Suggest hero for custom task
    print("\n\n🦸 Example 3: Hero Suggestion")
    suggestions = planner.suggest_hero_for_task("button_testing")
    print(f"Best heroes for button_testing: {', '.join(suggestions)}")
