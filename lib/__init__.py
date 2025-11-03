"""
🦸 Justice League Library Package
Core modules for self-healing, cost optimization, and advanced intelligence
"""

from .oracle_memory import OracleMemory
from .self_healing import execute_with_retry, retry_decorator, retry_figma_api
from .parallel_orchestration import ParallelCoordinator
from .cost_optimizer import CostOptimizer, BudgetMonitor
from .advanced_intelligence import AutoTester, KBLearner, BudgetForecaster

__all__ = [
    'OracleMemory',
    'execute_with_retry',
    'retry_decorator',
    'retry_figma_api',
    'ParallelCoordinator',
    'CostOptimizer',
    'BudgetMonitor',
    'AutoTester',
    'KBLearner',
    'BudgetForecaster',
]

__version__ = '2.0.0'
