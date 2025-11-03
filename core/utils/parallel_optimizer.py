"""
🔮 PARALLEL OPTIMIZER - ORACLE'S DECISION ENGINE
Autonomous decision-making for when to use git worktrees

Oracle analyzes missions and recommends optimal execution strategy:
- Sequential vs Parallel
- Worker count optimization
- Worktree usage decisions
- Performance predictions

Version: 1.0.0
Created: 2025-10-31
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class ExecutionStrategy(Enum):
    """Recommended execution strategy"""
    SEQUENTIAL = "sequential"              # Run one at a time
    PARALLEL_NO_WORKTREES = "parallel"     # Parallel without worktrees
    PARALLEL_WITH_WORKTREES = "optimized"  # Parallel with worktrees (optimal)


@dataclass
class ParallelRecommendation:
    """Oracle's recommendation for mission execution"""
    strategy: ExecutionStrategy
    recommended_workers: int
    use_worktrees: bool
    confidence: float  # 0.0 - 1.0
    reasoning: List[str]
    expected_speedup: float
    estimated_duration: float
    benefits: List[str]
    warnings: List[str]


class ParallelOptimizer:
    """
    🔮 Oracle's Intelligence for Parallel Optimization

    Analyzes missions and decides:
    - Should we parallelize?
    - How many workers?
    - Use worktrees?
    - What speedup to expect?
    """

    # Decision thresholds (learned from testing)
    MIN_TASK_DURATION_FOR_PARALLEL = 30.0  # seconds
    MIN_TASKS_FOR_PARALLEL = 2
    WORKTREE_OVERHEAD = 0.8  # seconds per worktree
    OPTIMAL_WORKERS_DEFAULT = 4
    MAX_WORKERS = 8

    def __init__(self, narrator: Optional[Any] = None):
        """Initialize optimizer"""
        self.narrator = narrator
        self.decision_history: List[Dict[str, Any]] = []

    def analyze_missions(
        self,
        missions: List[Dict[str, Any]],
        estimated_task_duration: Optional[float] = None
    ) -> ParallelRecommendation:
        """
        🔮 Oracle analyzes missions and recommends execution strategy

        Args:
            missions: List of mission dicts
            estimated_task_duration: Optional estimated duration per task (seconds)

        Returns:
            ParallelRecommendation with strategy and reasoning
        """
        num_missions = len(missions)
        reasoning = []
        warnings = []
        benefits = []

        # Step 1: Check if we have enough tasks
        if num_missions < self.MIN_TASKS_FOR_PARALLEL:
            return ParallelRecommendation(
                strategy=ExecutionStrategy.SEQUENTIAL,
                recommended_workers=1,
                use_worktrees=False,
                confidence=0.95,
                reasoning=[
                    f"Only {num_missions} task(s) - sequential is faster",
                    "Parallel overhead > benefit for single tasks"
                ],
                expected_speedup=1.0,
                estimated_duration=estimated_task_duration or 60.0,
                benefits=["Simple execution", "No overhead"],
                warnings=[]
            )

        # Step 2: Estimate task duration if not provided
        if estimated_task_duration is None:
            estimated_task_duration = self._estimate_task_duration(missions)

        reasoning.append(f"Analyzing {num_missions} missions")
        reasoning.append(f"Estimated task duration: {estimated_task_duration:.1f}s")

        # Step 3: Check task duration threshold
        if estimated_task_duration < self.MIN_TASK_DURATION_FOR_PARALLEL:
            reasoning.append(
                f"Tasks too fast ({estimated_task_duration:.1f}s < {self.MIN_TASK_DURATION_FOR_PARALLEL}s threshold)"
            )
            reasoning.append("Overhead would exceed benefit")

            return ParallelRecommendation(
                strategy=ExecutionStrategy.SEQUENTIAL,
                recommended_workers=1,
                use_worktrees=False,
                confidence=0.90,
                reasoning=reasoning,
                expected_speedup=1.0,
                estimated_duration=num_missions * estimated_task_duration,
                benefits=["Minimal overhead"],
                warnings=["Consider batching tasks for parallel execution"]
            )

        # Step 4: Calculate optimal workers
        optimal_workers = min(num_missions, self.OPTIMAL_WORKERS_DEFAULT, self.MAX_WORKERS)
        reasoning.append(f"Optimal workers: {optimal_workers}")

        # Step 5: Decide on worktrees
        use_worktrees = True
        worktree_benefit = self._analyze_worktree_benefit(missions, estimated_task_duration)

        if worktree_benefit < 1.2:  # Less than 20% benefit
            use_worktrees = False
            reasoning.append("Worktree overhead not justified for these tasks")
            warnings.append("Tasks may not benefit from workspace isolation")
        else:
            reasoning.append(f"Worktrees provide {worktree_benefit:.1f}x benefit from isolation")
            benefits.append("Isolated workspaces prevent conflicts")
            benefits.append("Atomic operations per task")

        # Step 6: Calculate expected speedup
        expected_speedup = self._calculate_expected_speedup(
            num_missions,
            optimal_workers,
            estimated_task_duration,
            use_worktrees
        )

        reasoning.append(f"Expected speedup: {expected_speedup:.1f}x")

        # Step 7: Calculate estimated duration
        sequential_duration = num_missions * estimated_task_duration
        parallel_duration = sequential_duration / expected_speedup
        estimated_duration = parallel_duration

        reasoning.append(
            f"Duration: {parallel_duration:.1f}s vs {sequential_duration:.1f}s sequential"
        )

        # Step 8: Build benefits list
        benefits.extend([
            f"{expected_speedup:.1f}x faster execution",
            f"Save {sequential_duration - parallel_duration:.1f}s",
            f"{optimal_workers} heroes working simultaneously"
        ])

        # Step 9: Determine strategy
        if use_worktrees:
            strategy = ExecutionStrategy.PARALLEL_WITH_WORKTREES
            benefits.append("Full workspace isolation with git worktrees")
        else:
            strategy = ExecutionStrategy.PARALLEL_NO_WORKTREES
            warnings.append("No workspace isolation - ensure no file conflicts")

        # Step 10: Calculate confidence
        confidence = self._calculate_confidence(
            num_missions,
            estimated_task_duration,
            expected_speedup
        )

        return ParallelRecommendation(
            strategy=strategy,
            recommended_workers=optimal_workers,
            use_worktrees=use_worktrees,
            confidence=confidence,
            reasoning=reasoning,
            expected_speedup=expected_speedup,
            estimated_duration=estimated_duration,
            benefits=benefits,
            warnings=warnings
        )

    def _estimate_task_duration(self, missions: List[Dict[str, Any]]) -> float:
        """Estimate task duration based on mission type"""
        # Check first mission to determine type
        if not missions:
            return 60.0  # Default 1 minute

        first_mission = missions[0]
        hero_name = first_mission.get('hero_name', '').lower()

        # Hero-specific estimates (learned from experience)
        duration_estimates = {
            'artemis': 60.0,      # Code generation: ~1 minute
            'green_arrow': 45.0,  # Validation: ~45 seconds
            'batman': 50.0,       # Testing: ~50 seconds
            'oracle': 5.0,        # Analysis: ~5 seconds (fast!)
            'wonder_woman': 40.0, # Accessibility: ~40 seconds
            'flash': 35.0,        # Performance: ~35 seconds
            'aquaman': 30.0,      # Network: ~30 seconds
        }

        return duration_estimates.get(hero_name, 60.0)

    def _analyze_worktree_benefit(
        self,
        missions: List[Dict[str, Any]],
        task_duration: float
    ) -> float:
        """
        Analyze benefit of using worktrees

        Returns:
            Benefit multiplier (> 1.0 means beneficial)
        """
        # Worktrees provide benefit through:
        # 1. Preventing I/O conflicts (file writes)
        # 2. Clean git context per task
        # 3. Atomic operations

        # Check if tasks involve file operations
        has_file_operations = any(
            mission.get('hero_name', '').lower() in ['artemis', 'green_arrow']
            for mission in missions
        )

        if not has_file_operations:
            return 1.1  # Minimal benefit

        # Calculate overhead vs benefit
        overhead_ratio = self.WORKTREE_OVERHEAD / task_duration

        if overhead_ratio > 0.1:  # Overhead > 10% of task
            return 1.1  # Not worth it

        # Significant benefit for file-heavy operations
        return 1.5

    def _calculate_expected_speedup(
        self,
        num_tasks: int,
        num_workers: int,
        task_duration: float,
        use_worktrees: bool
    ) -> float:
        """
        Calculate expected speedup based on task characteristics

        Uses Amdahl's Law with overhead adjustment
        """
        # Theoretical max speedup
        theoretical_max = min(num_tasks, num_workers)

        # Parallel efficiency (70-75% observed)
        parallel_efficiency = 0.72

        # Overhead adjustments
        overhead = 0.0

        if use_worktrees:
            # Worktree overhead
            overhead += self.WORKTREE_OVERHEAD * num_workers / task_duration

        # Thread coordination overhead
        overhead += 0.05  # ~5% coordination overhead

        # Actual speedup accounting for efficiency and overhead
        actual_speedup = theoretical_max * parallel_efficiency * (1 - overhead)

        return max(1.0, actual_speedup)  # Never less than 1.0

    def _calculate_confidence(
        self,
        num_tasks: int,
        task_duration: float,
        expected_speedup: float
    ) -> float:
        """Calculate confidence in recommendation"""
        confidence = 0.5  # Base confidence

        # More tasks = higher confidence
        if num_tasks >= 4:
            confidence += 0.2
        elif num_tasks >= 2:
            confidence += 0.1

        # Longer tasks = higher confidence
        if task_duration >= 60.0:
            confidence += 0.2
        elif task_duration >= 30.0:
            confidence += 0.1

        # Higher speedup = higher confidence
        if expected_speedup >= 2.5:
            confidence += 0.2
        elif expected_speedup >= 1.5:
            confidence += 0.1

        return min(0.95, confidence)  # Max 95% confidence

    def record_decision(
        self,
        recommendation: ParallelRecommendation,
        actual_result: Optional[Dict[str, Any]] = None
    ):
        """
        Record decision for learning

        Args:
            recommendation: The recommendation made
            actual_result: Actual execution result (if available)
        """
        decision_record = {
            'timestamp': str(datetime.now()),
            'recommendation': {
                'strategy': recommendation.strategy.value,
                'workers': recommendation.recommended_workers,
                'worktrees': recommendation.use_worktrees,
                'confidence': recommendation.confidence,
                'expected_speedup': recommendation.expected_speedup
            }
        }

        if actual_result:
            decision_record['actual'] = {
                'duration': actual_result.get('duration'),
                'success_rate': actual_result.get('successful', 0) / actual_result.get('total_missions', 1),
                'used_worktrees': actual_result.get('used_worktrees')
            }

        self.decision_history.append(decision_record)

    def show_recommendation(self, rec: ParallelRecommendation):
        """Display recommendation through narrator"""
        if not self.narrator:
            return

        from datetime import datetime

        self.narrator.hero_speaks(
            "🔮 Oracle",
            "Mission analysis complete - recommendation ready",
            style="friendly"
        )

        print("\n" + "="*80)
        print("🔮 ORACLE'S PARALLEL OPTIMIZATION RECOMMENDATION")
        print("="*80)

        print(f"\n📊 Strategy: {rec.strategy.value.upper()}")
        print(f"   Workers: {rec.recommended_workers}")
        print(f"   Worktrees: {'ENABLED' if rec.use_worktrees else 'DISABLED'}")
        print(f"   Confidence: {rec.confidence*100:.0f}%")

        print(f"\n⚡ Expected Performance:")
        print(f"   Speedup: {rec.expected_speedup:.1f}x")
        print(f"   Duration: ~{rec.estimated_duration:.1f}s")

        print(f"\n💡 Reasoning:")
        for reason in rec.reasoning:
            print(f"   • {reason}")

        if rec.benefits:
            print(f"\n✅ Benefits:")
            for benefit in rec.benefits:
                print(f"   • {benefit}")

        if rec.warnings:
            print(f"\n⚠️  Warnings:")
            for warning in rec.warnings:
                print(f"   • {warning}")

        print("="*80 + "\n")
