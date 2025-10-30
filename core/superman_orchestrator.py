"""
🦸 SUPERMAN SMART MISSION ORCHESTRATOR
=======================================

Intelligent mission orchestration and hero coordination.

Coordinates:
- Mission execution across multiple heroes
- Hero workload balancing
- Parallel task execution
- Dependency management
- Progress monitoring
- Dynamic re-planning based on results

Author: Superman (with Claude Code)
Created: October 21, 2025
Status: Production Ready - Strategic Orchestration
"""

import logging
import time
from typing import Dict, Any, List, Optional, Callable, Set
from datetime import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
from dataclasses import dataclass, field

# Import Superman's systems
try:
    from .superman_mission_planner import Mission, MissionTask, MissionPhase, SupermanMissionPlanner
    from .superman_communication import HeroCommunicationHub
    from .superman_knowledge_base import JusticeLeagueKnowledgeBase
    from .superman_self_healing import SupermanSelfHealingEngine
except ImportError:
    from superman_mission_planner import Mission, MissionTask, MissionPhase, SupermanMissionPlanner
    from superman_communication import HeroCommunicationHub
    from superman_knowledge_base import JusticeLeagueKnowledgeBase
    from superman_self_healing import SupermanSelfHealingEngine


@dataclass
class HeroStatus:
    """Track hero status"""
    hero_name: str
    available: bool = True
    current_task: Optional[str] = None
    tasks_completed: int = 0
    tasks_failed: int = 0
    last_active: Optional[str] = None


class SupermanSmartOrchestrator:
    """
    Superman's intelligent mission orchestration system.

    Coordinates multiple heroes, manages parallel execution,
    handles dependencies, and adapts to changing conditions.
    """

    def __init__(
        self,
        communication_hub: Optional[HeroCommunicationHub] = None,
        knowledge_base: Optional[JusticeLeagueKnowledgeBase] = None,
        self_healing: Optional[SupermanSelfHealingEngine] = None,
        mission_planner: Optional[SupermanMissionPlanner] = None,
        max_parallel_tasks: int = 5
    ):
        """
        Initialize orchestrator.

        Args:
            communication_hub: Hero communication hub
            knowledge_base: Knowledge base
            self_healing: Self-healing engine
            mission_planner: Mission planner
            max_parallel_tasks: Maximum parallel task execution
        """
        self.communication_hub = communication_hub or HeroCommunicationHub()
        self.knowledge_base = knowledge_base or JusticeLeagueKnowledgeBase()
        self.self_healing = self_healing or SupermanSelfHealingEngine()
        self.mission_planner = mission_planner or SupermanMissionPlanner(
            knowledge_base=self.knowledge_base,
            communication_hub=self.communication_hub
        )

        self.max_parallel_tasks = max_parallel_tasks

        # Hero tracking
        self.heroes: Dict[str, HeroStatus] = {}
        self.hero_instances: Dict[str, Any] = {}

        # Mission tracking
        self.active_missions: Dict[str, Mission] = {}
        self.completed_missions: List[Mission] = []

        # Execution
        self.executor = ThreadPoolExecutor(max_workers=max_parallel_tasks)
        self.task_futures: Dict[str, Future] = {}

        self.logger = logging.getLogger("SupermanOrchestrator")
        self.logger.info("🦸 Smart Orchestrator initialized")

    def register_hero(self, hero_name: str, hero_instance: Any):
        """
        Register a hero with the orchestrator.

        Args:
            hero_name: Hero's name
            hero_instance: Hero instance
        """
        self.heroes[hero_name] = HeroStatus(hero_name=hero_name)
        self.hero_instances[hero_name] = hero_instance

        # Register with communication hub
        self.communication_hub.register_hero(hero_name, hero_instance)

        # Set knowledge base and communication hub on hero
        if hasattr(hero_instance, 'knowledge_base'):
            hero_instance.knowledge_base = self.knowledge_base
        if hasattr(hero_instance, 'communication_hub'):
            hero_instance.communication_hub = self.communication_hub

        self.logger.info(f"✅ Registered {hero_name} with orchestrator")

    def execute_mission(
        self,
        mission: Mission,
        execute_func: Optional[Callable[[MissionTask], Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Execute a complete mission with intelligent orchestration.

        Args:
            mission: Mission to execute
            execute_func: Optional custom execution function

        Returns:
            Mission results
        """
        self.logger.info(f"\n{'=' * 70}")
        self.logger.info(f"🦸 MISSION START: {mission.mission_name}")
        self.logger.info(f"{'=' * 70}")

        mission.status = "in_progress"
        mission.started_at = datetime.now().isoformat()
        self.active_missions[mission.mission_id] = mission

        # Track phase completion
        phase_results = defaultdict(list)

        try:
            # Execute mission phase by phase
            for phase in mission.phases:
                self.logger.info(f"\n🎯 PHASE: {phase.value.upper()}")
                self.logger.info(f"-" * 70)

                phase_tasks = [t for t in mission.tasks if t.phase == phase]

                if not phase_tasks:
                    self.logger.info(f"   No tasks for {phase.value}")
                    continue

                # Execute tasks in this phase
                phase_result = self._execute_phase(
                    mission, phase, phase_tasks, execute_func
                )

                phase_results[phase.value].extend(phase_result)

                # Check if phase failed critically
                critical_failures = [
                    r for r in phase_result
                    if r.get("status") == "failed" and r.get("task_priority") == "critical"
                ]

                if critical_failures:
                    self.logger.error(
                        f"❌ Critical failures in {phase.value}, "
                        f"considering mission abort..."
                    )

                    # Ask Superman's judgment
                    should_continue = self._should_continue_after_failure(
                        mission, phase, critical_failures
                    )

                    if not should_continue:
                        self.logger.error("🚨 Mission aborted due to critical failures")
                        mission.status = "failed"
                        return self._compile_mission_results(mission, phase_results)

            # Mission complete
            mission.status = "completed"
            mission.completed_at = datetime.now().isoformat()

            self.logger.info(f"\n{'=' * 70}")
            self.logger.info(f"✅ MISSION COMPLETE: {mission.mission_name}")
            self.logger.info(f"{'=' * 70}")

            # Compile and return results
            results = self._compile_mission_results(mission, phase_results)

            # Learn from mission
            self._learn_from_mission(mission, results)

            # Store completed mission
            self.completed_missions.append(mission)
            del self.active_missions[mission.mission_id]

            return results

        except Exception as e:
            self.logger.error(f"❌ Mission error: {e}")
            mission.status = "failed"

            # Try to recover
            recovery = self.self_healing.handle_error(
                e, "mission_execution",
                {"mission_id": mission.mission_id},
                "Superman"
            )

            if recovery:
                self.logger.info("🔄 Mission recovery successful, retrying...")
                return self.execute_mission(mission, execute_func)

            return self._compile_mission_results(mission, phase_results)

    def _execute_phase(
        self,
        mission: Mission,
        phase: MissionPhase,
        phase_tasks: List[MissionTask],
        execute_func: Optional[Callable]
    ) -> List[Dict[str, Any]]:
        """Execute all tasks in a phase."""
        results = []
        remaining_tasks = phase_tasks.copy()

        while remaining_tasks:
            # Get tasks ready to execute (dependencies met)
            ready_tasks = []
            for task in remaining_tasks:
                dependencies_met = all(
                    self._is_task_completed(mission, dep_id)
                    for dep_id in task.dependencies
                )

                if dependencies_met:
                    # Check hero availability
                    hero_status = self.heroes.get(task.assigned_hero)
                    if hero_status and hero_status.available:
                        ready_tasks.append(task)

            if not ready_tasks:
                if remaining_tasks:
                    self.logger.warning(
                        f"⚠️  No tasks ready (waiting on dependencies or heroes)"
                    )
                    time.sleep(1)
                    continue
                else:
                    break

            # Execute ready tasks (up to max parallel)
            batch = ready_tasks[:self.max_parallel_tasks]

            self.logger.info(f"   ⚡ Executing {len(batch)} tasks in parallel:")
            for task in batch:
                self.logger.info(f"      - {task.assigned_hero}: {task.description}")

            # Execute batch
            batch_results = self._execute_task_batch(batch, execute_func)

            # Process results
            for task, result in zip(batch, batch_results):
                task.result = result
                task.status = result.get("status", "completed")
                task.completed_at = datetime.now().isoformat()

                # Update hero status
                hero_status = self.heroes.get(task.assigned_hero)
                if hero_status:
                    hero_status.available = True
                    hero_status.current_task = None
                    hero_status.last_active = datetime.now().isoformat()

                    if task.status == "completed":
                        hero_status.tasks_completed += 1
                    else:
                        hero_status.tasks_failed += 1

                # Remove from remaining
                remaining_tasks.remove(task)
                results.append({
                    "task_id": task.task_id,
                    "hero": task.assigned_hero,
                    "description": task.description,
                    "status": task.status,
                    "task_priority": task.priority.value,
                    "result": result
                })

        return results

    def _execute_task_batch(
        self,
        tasks: List[MissionTask],
        execute_func: Optional[Callable]
    ) -> List[Dict[str, Any]]:
        """Execute a batch of tasks in parallel."""
        # Mark heroes as busy
        for task in tasks:
            hero_status = self.heroes.get(task.assigned_hero)
            if hero_status:
                hero_status.available = False
                hero_status.current_task = task.task_id

            task.status = "in_progress"
            task.started_at = datetime.now().isoformat()

        # Execute in parallel
        futures = []
        for task in tasks:
            if execute_func:
                future = self.executor.submit(self._execute_task_safe, task, execute_func)
            else:
                future = self.executor.submit(self._execute_task_default, task)

            futures.append(future)
            self.task_futures[task.task_id] = future

        # Wait for completion
        results = []
        for future in as_completed(futures):
            try:
                result = future.result(timeout=300)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Task execution error: {e}")
                results.append({
                    "status": "failed",
                    "error": str(e)
                })

        return results

    def _execute_task_safe(
        self,
        task: MissionTask,
        execute_func: Callable
    ) -> Dict[str, Any]:
        """Execute task with error handling."""
        try:
            result = execute_func(task)
            return result
        except Exception as e:
            self.logger.error(f"❌ Task {task.task_id} failed: {e}")

            # Try self-healing
            recovery = self.self_healing.handle_error(
                e, task.task_type,
                {"task_id": task.task_id},
                task.assigned_hero
            )

            if recovery:
                return {"status": "completed", "recovery_used": True, "result": recovery}

            return {"status": "failed", "error": str(e)}

    def _execute_task_default(self, task: MissionTask) -> Dict[str, Any]:
        """Default task execution (simulation)."""
        self.logger.info(f"   🔄 {task.assigned_hero} executing: {task.description}")

        # Simulate work
        time.sleep(0.5)

        return {
            "status": "completed",
            "task_type": task.task_type,
            "hero": task.assigned_hero,
            "simulation": True
        }

    def _is_task_completed(self, mission: Mission, task_id: str) -> bool:
        """Check if a task is completed."""
        for task in mission.tasks:
            if task.task_id == task_id:
                return task.status == "completed"
        return False

    def _should_continue_after_failure(
        self,
        mission: Mission,
        phase: MissionPhase,
        failures: List[Dict[str, Any]]
    ) -> bool:
        """Decide if mission should continue after failures."""
        # Check mission priority
        if mission.priority.value == "critical":
            self.logger.warning("Mission is critical, attempting recovery...")
            return True

        # Check number of failures
        if len(failures) > len(mission.tasks) // 2:
            self.logger.error("Too many failures, aborting...")
            return False

        # Check if failures are recoverable
        recoverable = all(
            f.get("result", {}).get("recovery_used")
            for f in failures
        )

        if recoverable:
            self.logger.info("All failures recovered, continuing...")
            return True

        # Ask knowledge base for similar situations
        if self.knowledge_base:
            similar = self.knowledge_base.search(
                query="mission_failure_recovery",
                limit=5
            )

            success_rate = sum(
                1 for s in similar
                if s.get("content", {}).get("continued_after_failure")
            ) / len(similar) if similar else 0

            if success_rate > 0.5:
                self.logger.info("Historical data suggests continuing...")
                return True

        # Default: abort if multiple critical failures
        return False

    def _compile_mission_results(
        self,
        mission: Mission,
        phase_results: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Compile complete mission results."""
        all_results = []
        for phase, results in phase_results.items():
            all_results.extend(results)

        completed_tasks = sum(1 for r in all_results if r.get("status") == "completed")
        failed_tasks = sum(1 for r in all_results if r.get("status") == "failed")

        return {
            "mission_id": mission.mission_id,
            "mission_name": mission.mission_name,
            "status": mission.status,
            "started_at": mission.started_at,
            "completed_at": mission.completed_at,
            "total_tasks": len(mission.tasks),
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "success_rate": (completed_tasks / len(mission.tasks) * 100) if mission.tasks else 0,
            "phase_results": dict(phase_results),
            "all_results": all_results
        }

    def _learn_from_mission(self, mission: Mission, results: Dict[str, Any]):
        """Learn from completed mission."""
        # Store in knowledge base
        if self.knowledge_base:
            self.knowledge_base.add_knowledge(
                hero="Superman",
                knowledge_type="mission_result",
                content={
                    "mission_type": mission.target_type.value,
                    "success_rate": results["success_rate"],
                    "total_tasks": results["total_tasks"],
                    "completed": results["completed_tasks"],
                    "failed": results["failed_tasks"]
                },
                tags=["mission", "orchestration", mission.target_type.value]
            )

        # Learn from failures
        for result in results["all_results"]:
            if result.get("status") == "failed":
                hero = result.get("hero", "Unknown")
                if hasattr(self.hero_instances.get(hero), 'learn_from_failure'):
                    self.hero_instances[hero].learn_from_failure({
                        "operation": result.get("task_id"),
                        "error": result.get("result", {}).get("error"),
                        "root_cause": "task_execution_failure"
                    })

    def get_orchestration_stats(self) -> Dict[str, Any]:
        """Get orchestration statistics."""
        return {
            "registered_heroes": len(self.heroes),
            "active_missions": len(self.active_missions),
            "completed_missions": len(self.completed_missions),
            "hero_status": {
                name: {
                    "available": status.available,
                    "tasks_completed": status.tasks_completed,
                    "tasks_failed": status.tasks_failed,
                    "current_task": status.current_task
                }
                for name, status in self.heroes.items()
            }
        }

    def generate_orchestration_report(self) -> str:
        """Generate human-readable orchestration report."""
        stats = self.get_orchestration_stats()

        report = []
        report.append("🦸 SUPERMAN ORCHESTRATION REPORT")
        report.append("=" * 70)
        report.append(f"Registered Heroes: {stats['registered_heroes']}")
        report.append(f"Active Missions: {stats['active_missions']}")
        report.append(f"Completed Missions: {stats['completed_missions']}")

        if stats['hero_status']:
            report.append("\n🦸 Hero Status:")
            for hero, status in stats['hero_status'].items():
                available = "✅ Available" if status['available'] else "⏳ Busy"
                report.append(
                    f"  {available} {hero}: "
                    f"{status['tasks_completed']} completed, "
                    f"{status['tasks_failed']} failed"
                )

        report.append("\n" + "=" * 70)

        return "\n".join(report)


# Example usage
if __name__ == "__main__":
    from justice_league.hero_base import HeroBase

    # Create orchestrator
    orchestrator = SupermanSmartOrchestrator()

    # Create and register heroes
    batman = HeroBase("Batman", "🦇")
    wonder_woman = HeroBase("Wonder Woman", "⚡")
    flash = HeroBase("Flash", "⚡")

    orchestrator.register_hero("Batman", batman)
    orchestrator.register_hero("Wonder Woman", wonder_woman)
    orchestrator.register_hero("Flash", flash)

    # Create mission
    mission = orchestrator.mission_planner.plan_mission(
        target="https://example.com/dashboard",
        goal="Complete quality audit",
        target_type="url",
        priority="high"
    )

    # Execute mission
    print("\n🎯 Executing Mission...")
    results = orchestrator.execute_mission(mission)

    print(f"\n📊 Mission Results:")
    print(f"Status: {results['status']}")
    print(f"Success Rate: {results['success_rate']:.1f}%")
    print(f"Completed: {results['completed_tasks']}/{results['total_tasks']}")

    # Show orchestration stats
    print("\n" + orchestrator.generate_orchestration_report())
