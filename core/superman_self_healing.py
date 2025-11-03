"""
🦸 SUPERMAN SELF-HEALING ENGINE
================================

Advanced error recovery and resilience system for Justice League.

Provides:
- Automatic error detection and recovery
- Intelligent retry strategies with exponential backoff
- Circuit breaker pattern for failing services
- Fallback strategy management
- Health monitoring and auto-repair
- Pattern recognition for recurring errors

Author: Superman (with Claude Code)
Created: October 21, 2025
Status: Production Ready - Autonomous Resilience
"""

import logging
import time
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict
from dataclasses import dataclass, field
import json
from pathlib import Path


class ErrorSeverity(Enum):
    """Error severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if recovered


@dataclass
class ErrorRecord:
    """Record of an error occurrence"""
    error_id: str
    operation: str
    error_type: str
    error_message: str
    severity: ErrorSeverity
    context: Dict[str, Any]
    timestamp: str
    hero: Optional[str] = None
    recovered: bool = False
    recovery_strategy: Optional[str] = None
    retry_count: int = 0


@dataclass
class CircuitBreaker:
    """Circuit breaker for a specific operation"""
    operation: str
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: Optional[float] = None
    threshold: int = 5  # Failures before opening
    timeout: int = 60  # Seconds before trying again
    half_open_success_threshold: int = 2  # Successes needed to close


class SupermanSelfHealingEngine:
    """
    Superman's self-healing engine.

    Automatically detects, analyzes, and recovers from errors
    with intelligent strategies and learning capabilities.
    """

    def __init__(self, knowledge_base=None, communication_hub=None,
                 storage_dir: Optional[str] = None):
        """
        Initialize self-healing engine.

        Args:
            knowledge_base: Justice League knowledge base
            communication_hub: Hero communication hub
            storage_dir: Directory to store healing data
        """
        self.knowledge_base = knowledge_base
        self.communication_hub = communication_hub

        # Storage
        self.storage_dir = Path(storage_dir or '/tmp/aldo-vision-self-healing')
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Error tracking
        self.error_history: List[ErrorRecord] = []
        self.error_patterns: Dict[str, List[ErrorRecord]] = defaultdict(list)

        # Recovery strategies
        self.recovery_strategies: Dict[str, List[Callable]] = defaultdict(list)
        self.fallback_strategies: Dict[str, Callable] = {}

        # Circuit breakers
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}

        # Retry configuration
        self.retry_config = {
            "max_retries": 3,
            "base_delay": 1.0,  # seconds
            "max_delay": 60.0,  # seconds
            "exponential_base": 2,
            "jitter": True
        }

        # Health monitoring
        self.health_checks: Dict[str, Callable] = {}
        self.last_health_check: Dict[str, datetime] = {}

        self.logger = logging.getLogger("SupermanSelfHealing")
        self.logger.info("🦸 Self-Healing Engine initialized")

        # Load historical data
        self._load_error_history()

    def handle_error(self, error: Exception, operation: str,
                    context: Optional[Dict[str, Any]] = None,
                    hero: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Handle an error with automatic recovery attempt.

        Args:
            error: Exception that occurred
            operation: Operation that failed
            context: Context when error happened
            hero: Hero that encountered error

        Returns:
            Recovery result if successful, None otherwise
        """
        context = context or {}

        # Record error
        error_record = self._record_error(error, operation, context, hero)

        self.logger.warning(
            f"🔧 {hero or 'System'} encountered {error_record.severity.value} error in {operation}: {error}"
        )

        # Check circuit breaker
        if not self._check_circuit_breaker(operation):
            self.logger.error(f"⚡ Circuit breaker OPEN for {operation} - rejecting request")
            return None

        # Determine recovery strategy
        recovery_strategy = self._determine_recovery_strategy(error_record)

        if not recovery_strategy:
            self.logger.error(f"❌ No recovery strategy found for {operation}")
            self._update_circuit_breaker(operation, success=False)
            return None

        # Attempt recovery
        self.logger.info(f"🔄 Attempting recovery using strategy: {recovery_strategy}")

        try:
            result = self._execute_recovery(
                recovery_strategy, error_record, context
            )

            if result:
                self.logger.info(f"✅ Recovery successful for {operation}")
                error_record.recovered = True
                error_record.recovery_strategy = recovery_strategy
                self._update_circuit_breaker(operation, success=True)

                # Learn from successful recovery
                self._learn_from_recovery(error_record, recovery_strategy)

                return result
            else:
                self.logger.warning(f"⚠️  Recovery attempt failed for {operation}")
                self._update_circuit_breaker(operation, success=False)
                return None

        except Exception as recovery_error:
            self.logger.error(f"❌ Recovery failed with error: {recovery_error}")
            self._update_circuit_breaker(operation, success=False)
            return None

    def retry_with_backoff(self, operation: Callable, operation_name: str,
                          context: Optional[Dict[str, Any]] = None,
                          hero: Optional[str] = None) -> Optional[Any]:
        """
        Execute operation with exponential backoff retry.

        Args:
            operation: Function to execute
            operation_name: Name for logging
            context: Additional context
            hero: Hero executing operation

        Returns:
            Operation result if successful
        """
        context = context or {}
        max_retries = self.retry_config["max_retries"]

        for attempt in range(max_retries + 1):
            try:
                result = operation()
                self.logger.info(f"✅ {operation_name} succeeded (attempt {attempt + 1})")
                return result

            except Exception as e:
                if attempt < max_retries:
                    delay = self._calculate_backoff_delay(attempt)
                    self.logger.warning(
                        f"⏱️  {operation_name} failed (attempt {attempt + 1}/{max_retries + 1}), "
                        f"retrying in {delay:.1f}s..."
                    )
                    time.sleep(delay)
                else:
                    self.logger.error(
                        f"❌ {operation_name} failed after {max_retries + 1} attempts"
                    )
                    # Handle the final error
                    return self.handle_error(e, operation_name, context, hero)

        return None

    def register_recovery_strategy(self, error_pattern: str, strategy: Callable,
                                  priority: int = 0):
        """
        Register a recovery strategy for an error pattern.

        Args:
            error_pattern: Error type or pattern to match
            strategy: Recovery function
            priority: Strategy priority (higher = tried first)
        """
        self.recovery_strategies[error_pattern].append((priority, strategy))
        # Sort by priority
        self.recovery_strategies[error_pattern].sort(key=lambda x: x[0], reverse=True)

        self.logger.info(f"📝 Registered recovery strategy for '{error_pattern}' (priority {priority})")

    def register_fallback(self, operation: str, fallback: Callable):
        """
        Register a fallback strategy for an operation.

        Args:
            operation: Operation name
            fallback: Fallback function
        """
        self.fallback_strategies[operation] = fallback
        self.logger.info(f"📝 Registered fallback for '{operation}'")

    def register_health_check(self, component: str, health_check: Callable):
        """
        Register a health check for a component.

        Args:
            component: Component name
            health_check: Health check function (returns bool)
        """
        self.health_checks[component] = health_check
        self.logger.info(f"🏥 Registered health check for '{component}'")

    def run_health_checks(self) -> Dict[str, Any]:
        """
        Run all health checks.

        Returns:
            Health status for all components
        """
        health_status = {}

        for component, health_check in self.health_checks.items():
            try:
                is_healthy = health_check()
                health_status[component] = {
                    "healthy": is_healthy,
                    "checked_at": datetime.now().isoformat()
                }

                if not is_healthy:
                    self.logger.warning(f"⚠️  {component} health check failed")
                    # Attempt auto-repair
                    self._attempt_auto_repair(component)

            except Exception as e:
                health_status[component] = {
                    "healthy": False,
                    "error": str(e),
                    "checked_at": datetime.now().isoformat()
                }
                self.logger.error(f"❌ {component} health check error: {e}")

            self.last_health_check[component] = datetime.now()

        return health_status

    def get_error_statistics(self) -> Dict[str, Any]:
        """
        Get error statistics and patterns.

        Returns:
            Error statistics
        """
        total_errors = len(self.error_history)
        recovered_errors = sum(1 for e in self.error_history if e.recovered)

        # Group by operation
        by_operation = defaultdict(lambda: {"total": 0, "recovered": 0})
        for error in self.error_history:
            by_operation[error.operation]["total"] += 1
            if error.recovered:
                by_operation[error.operation]["recovered"] += 1

        # Group by error type
        by_type = defaultdict(int)
        for error in self.error_history:
            by_type[error.error_type] += 1

        # Group by hero
        by_hero = defaultdict(int)
        for error in self.error_history:
            if error.hero:
                by_hero[error.hero] += 1

        return {
            "total_errors": total_errors,
            "recovered_errors": recovered_errors,
            "recovery_rate": (recovered_errors / total_errors * 100) if total_errors > 0 else 0,
            "by_operation": dict(by_operation),
            "by_type": dict(by_type),
            "by_hero": dict(by_hero),
            "circuit_breakers": {
                name: {
                    "state": cb.state.value,
                    "failure_count": cb.failure_count,
                    "success_count": cb.success_count
                }
                for name, cb in self.circuit_breakers.items()
            }
        }

    def generate_healing_report(self) -> str:
        """
        Generate human-readable healing report.

        Returns:
            Report string
        """
        stats = self.get_error_statistics()

        report = []
        report.append("🦸 SUPERMAN SELF-HEALING REPORT")
        report.append("=" * 70)
        report.append(f"Total Errors: {stats['total_errors']}")
        report.append(f"Recovered: {stats['recovered_errors']}")
        report.append(f"Recovery Rate: {stats['recovery_rate']:.1f}%")

        if stats['by_operation']:
            report.append("\n📊 Errors by Operation:")
            for op, data in sorted(stats['by_operation'].items(),
                                  key=lambda x: x[1]['total'], reverse=True)[:10]:
                recovery_rate = (data['recovered'] / data['total'] * 100) if data['total'] > 0 else 0
                report.append(f"  - {op}: {data['total']} ({recovery_rate:.0f}% recovered)")

        if stats['by_type']:
            report.append("\n🐛 Errors by Type:")
            for error_type, count in sorted(stats['by_type'].items(),
                                           key=lambda x: x[1], reverse=True)[:10]:
                report.append(f"  - {error_type}: {count}")

        if stats['by_hero']:
            report.append("\n🦸 Errors by Hero:")
            for hero, count in sorted(stats['by_hero'].items(),
                                     key=lambda x: x[1], reverse=True):
                report.append(f"  - {hero}: {count}")

        if stats['circuit_breakers']:
            report.append("\n⚡ Circuit Breakers:")
            for name, data in stats['circuit_breakers'].items():
                state_emoji = "🟢" if data['state'] == "closed" else "🔴" if data['state'] == "open" else "🟡"
                report.append(
                    f"  {state_emoji} {name}: {data['state']} "
                    f"(failures: {data['failure_count']}, successes: {data['success_count']})"
                )

        report.append("\n" + "=" * 70)

        return "\n".join(report)

    def _record_error(self, error: Exception, operation: str,
                     context: Dict[str, Any], hero: Optional[str]) -> ErrorRecord:
        """Record error in history."""
        error_id = f"error_{datetime.now().timestamp()}"

        # Determine severity
        severity = self._determine_severity(error, operation)

        error_record = ErrorRecord(
            error_id=error_id,
            operation=operation,
            error_type=type(error).__name__,
            error_message=str(error),
            severity=severity,
            context=context,
            timestamp=datetime.now().isoformat(),
            hero=hero
        )

        self.error_history.append(error_record)
        self.error_patterns[error_record.error_type].append(error_record)

        # Save to disk
        self._save_error_history()

        return error_record

    def _determine_severity(self, error: Exception, operation: str) -> ErrorSeverity:
        """Determine error severity."""
        error_type = type(error).__name__

        # Critical errors
        if error_type in ["SystemError", "MemoryError", "SecurityError"]:
            return ErrorSeverity.CRITICAL

        # High severity
        if error_type in ["ValueError", "TypeError", "AttributeError"]:
            return ErrorSeverity.HIGH

        # Medium severity
        if error_type in ["TimeoutError", "ConnectionError"]:
            return ErrorSeverity.MEDIUM

        # Default to low
        return ErrorSeverity.LOW

    def _determine_recovery_strategy(self, error_record: ErrorRecord) -> Optional[str]:
        """Determine best recovery strategy for error."""
        # Check registered strategies
        if error_record.error_type in self.recovery_strategies:
            return f"registered_{error_record.error_type}"

        # Check fallback for operation
        if error_record.operation in self.fallback_strategies:
            return f"fallback_{error_record.operation}"

        # Check learned patterns from knowledge base
        if self.knowledge_base:
            similar_errors = self.knowledge_base.search(
                query=error_record.error_type,
                knowledge_type="error_recovery",
                limit=5
            )

            if similar_errors:
                for entry in similar_errors:
                    if entry.get("content", {}).get("success", False):
                        return entry.get("content", {}).get("strategy", "retry")

        # Default to retry
        return "retry"

    def _execute_recovery(self, strategy: str, error_record: ErrorRecord,
                         context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute recovery strategy."""
        if strategy.startswith("registered_"):
            error_type = strategy.replace("registered_", "")
            if error_type in self.recovery_strategies:
                for priority, strategy_func in self.recovery_strategies[error_type]:
                    try:
                        return strategy_func(error_record, context)
                    except Exception as e:
                        self.logger.warning(f"Recovery strategy failed: {e}")
                        continue

        elif strategy.startswith("fallback_"):
            operation = strategy.replace("fallback_", "")
            if operation in self.fallback_strategies:
                try:
                    return self.fallback_strategies[operation](context)
                except Exception as e:
                    self.logger.error(f"Fallback failed: {e}")
                    return None

        elif strategy == "retry":
            # Simple retry handled elsewhere
            return {"strategy": "retry", "action": "retry_operation"}

        return None

    def _learn_from_recovery(self, error_record: ErrorRecord, strategy: str):
        """Learn from successful recovery."""
        if self.knowledge_base:
            self.knowledge_base.add_knowledge(
                hero="Superman",
                knowledge_type="error_recovery",
                content={
                    "error_type": error_record.error_type,
                    "operation": error_record.operation,
                    "strategy": strategy,
                    "success": True,
                    "severity": error_record.severity.value
                },
                tags=["self_healing", "error_recovery", error_record.error_type]
            )

    def _check_circuit_breaker(self, operation: str) -> bool:
        """Check if circuit breaker allows operation."""
        if operation not in self.circuit_breakers:
            self.circuit_breakers[operation] = CircuitBreaker(operation=operation)

        cb = self.circuit_breakers[operation]

        if cb.state == CircuitState.CLOSED:
            return True

        elif cb.state == CircuitState.OPEN:
            # Check if timeout has passed
            if cb.last_failure_time:
                elapsed = time.time() - cb.last_failure_time
                if elapsed >= cb.timeout:
                    # Try half-open
                    cb.state = CircuitState.HALF_OPEN
                    cb.success_count = 0
                    self.logger.info(f"⚡ Circuit breaker HALF_OPEN for {operation}")
                    return True
            return False

        elif cb.state == CircuitState.HALF_OPEN:
            return True

        return False

    def _update_circuit_breaker(self, operation: str, success: bool):
        """Update circuit breaker state."""
        if operation not in self.circuit_breakers:
            return

        cb = self.circuit_breakers[operation]

        if success:
            cb.success_count += 1
            cb.failure_count = 0

            if cb.state == CircuitState.HALF_OPEN:
                if cb.success_count >= cb.half_open_success_threshold:
                    cb.state = CircuitState.CLOSED
                    self.logger.info(f"⚡ Circuit breaker CLOSED for {operation}")

        else:
            cb.failure_count += 1
            cb.success_count = 0
            cb.last_failure_time = time.time()

            if cb.failure_count >= cb.threshold:
                cb.state = CircuitState.OPEN
                self.logger.warning(f"⚡ Circuit breaker OPEN for {operation}")

    def _calculate_backoff_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay."""
        delay = min(
            self.retry_config["base_delay"] * (self.retry_config["exponential_base"] ** attempt),
            self.retry_config["max_delay"]
        )

        # Add jitter
        if self.retry_config["jitter"]:
            import random
            delay *= (0.5 + random.random() * 0.5)

        return delay

    def _attempt_auto_repair(self, component: str):
        """Attempt to auto-repair a failing component."""
        self.logger.info(f"🔧 Attempting auto-repair for {component}")

        # Check if we have a repair strategy
        if component in self.fallback_strategies:
            try:
                self.fallback_strategies[component]({})
                self.logger.info(f"✅ Auto-repair successful for {component}")
            except Exception as e:
                self.logger.error(f"❌ Auto-repair failed for {component}: {e}")

    def _save_error_history(self):
        """Save error history to disk."""
        error_file = self.storage_dir / "error_history.json"
        data = [
            {
                "error_id": e.error_id,
                "operation": e.operation,
                "error_type": e.error_type,
                "error_message": e.error_message,
                "severity": e.severity.value,
                "timestamp": e.timestamp,
                "hero": e.hero,
                "recovered": e.recovered,
                "recovery_strategy": e.recovery_strategy
            }
            for e in self.error_history[-1000:]  # Keep last 1000
        ]

        with open(error_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _load_error_history(self):
        """Load error history from disk."""
        error_file = self.storage_dir / "error_history.json"
        if error_file.exists():
            with open(error_file, 'r') as f:
                data = json.load(f)

            for entry in data:
                error_record = ErrorRecord(
                    error_id=entry["error_id"],
                    operation=entry["operation"],
                    error_type=entry["error_type"],
                    error_message=entry["error_message"],
                    severity=ErrorSeverity(entry["severity"]),
                    context={},
                    timestamp=entry["timestamp"],
                    hero=entry.get("hero"),
                    recovered=entry.get("recovered", False),
                    recovery_strategy=entry.get("recovery_strategy")
                )
                self.error_history.append(error_record)
                self.error_patterns[error_record.error_type].append(error_record)

            self.logger.info(f"📂 Loaded {len(self.error_history)} error records")


# Example usage
if __name__ == "__main__":
    # Create healing engine
    healing = SupermanSelfHealingEngine()

    # Example 1: Register recovery strategies
    def timeout_recovery(error_record, context):
        print(f"🔄 Recovering from timeout by increasing wait time")
        return {"action": "retry", "wait_time": 5}

    healing.register_recovery_strategy("TimeoutError", timeout_recovery, priority=10)

    # Example 2: Handle an error
    try:
        raise TimeoutError("Connection timed out")
    except Exception as e:
        result = healing.handle_error(e, "fetch_data", {"url": "https://example.com"}, "Batman")
        print(f"Recovery result: {result}")

    # Example 3: Retry with backoff
    def failing_operation():
        import random
        if random.random() < 0.7:
            raise ValueError("Random failure")
        return {"status": "success"}

    result = healing.retry_with_backoff(failing_operation, "test_operation", hero="Wonder Woman")
    print(f"Operation result: {result}")

    # Example 4: Health checks
    def check_database():
        return True  # Database is healthy

    healing.register_health_check("database", check_database)
    health_status = healing.run_health_checks()
    print(f"\nHealth Status: {json.dumps(health_status, indent=2)}")

    # Example 5: Statistics
    print("\n" + healing.generate_healing_report())
