"""
💾 Oracle Persistent Memory System
Never forget user preferences, project patterns, and optimization history

Usage:
    from lib.oracle_memory import OracleMemory

    # Initialize
    memory = OracleMemory()

    # Store preferences
    memory.set_user_preference('path_format', 'absolute')
    memory.set_project_pattern('figma_analysis_mode', 'individual')

    # Retrieve
    path_format = memory.get_user_preference('path_format')

    # Save to disk
    memory.save()
"""

import json
import os
from datetime import datetime
from typing import Any, Optional, Dict
from pathlib import Path


class OracleMemory:
    """
    Persistent memory system for Oracle.
    Stores and retrieves user preferences, project patterns, and optimization history.
    """

    def __init__(self, memory_file: Optional[str] = None):
        """
        Initialize Oracle memory system.

        Args:
            memory_file: Path to memory JSON file (default: oracle-memory.json in mission folder)
        """
        if memory_file is None:
            # Default location: justice-league-missions/oracle-memory.json
            base_path = Path(__file__).parent.parent
            memory_file = base_path / "oracle-memory.json"

        self.memory_file = str(memory_file)
        self.memory = self._load_or_create()

    def _load_or_create(self) -> Dict:
        """Load existing memory or create new default memory."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    memory = json.load(f)
                print(f"💾 Oracle memory loaded from: {self.memory_file}")
                return memory
            except Exception as e:
                print(f"⚠️ Warning: Could not load memory file: {e}")
                print("💾 Creating new memory...")

        # Default memory structure
        default_memory = {
            "version": "2.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),

            "user_preferences": {
                "path_format": "absolute",  # User wants full absolute paths
                "summary_structure": "cost_first",  # Cost at top of summaries
                "tracking_system": "simple",  # Simple tracking (Estimate → Work → Invoice)
                "github_repo": "https://github.com/aldrinstellus/justice-league",  # Never ask again
                "budget_conscious": True,  # Always check budget first
            },

            "project_patterns": {
                "figma_analysis_mode": "individual",  # No sampling, analyze every file
                "progress_display": "live",  # Real-time progress bars
                "cost_calculation": "per_file",  # Individual file costs
                "rate_limiting": 1.2,  # Seconds between Figma API calls
                "quicksilver_preferred": True,  # Prefer Quicksilver for exports
            },

            "optimization_history": {
                "haiku_usage_rate": 0.30,  # 30% of tasks use Haiku
                "sonnet_usage_rate": 0.70,  # 70% of tasks use Sonnet
                "caching_enabled": True,  # Prompt caching active
                "batch_api_usage": 0.0,  # Not yet used
                "savings_achieved": 0.60,  # 60% cost savings on average
                "quality_maintained": 0.94,  # 9.4/10 quality score
            },

            "mission_history": {
                "total_missions": 1,  # JL-001 completed
                "completed_missions": 1,
                "active_missions": 1,  # JL-003
                "success_rate": 1.0,  # 100% success rate
                "average_cost_per_mission": 45.23,  # From JL-001
            },

            "learned_patterns": {
                # Oracle learns from each interaction
                "corrections_given": [],  # Track user corrections to learn from
                "successful_strategies": [],  # Track what works well
                "failed_strategies": [],  # Track what doesn't work
            },

            "standing_instructions": [
                "ALWAYS use full absolute paths (never relative)",
                "ALWAYS put costs first in summaries (cost-first structure)",
                "NEVER ask for GitHub repo URL (permanently stored)",
                "ALWAYS check budget before starting work",
                "ALWAYS generate estimate before work begins",
                "ALWAYS generate invoice after work completes",
            ]
        }

        print(f"💾 Created new Oracle memory at: {self.memory_file}")
        return default_memory

    def save(self) -> bool:
        """
        Save memory to disk.

        Returns:
            True if successful, False otherwise
        """
        try:
            self.memory['last_updated'] = datetime.now().isoformat()

            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)

            print(f"💾 Oracle memory saved to: {self.memory_file}")
            return True

        except Exception as e:
            print(f"❌ Error saving memory: {e}")
            return False

    # ==================== User Preferences ====================

    def get_user_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference value."""
        return self.memory['user_preferences'].get(key, default)

    def set_user_preference(self, key: str, value: Any) -> None:
        """Set user preference value."""
        self.memory['user_preferences'][key] = value
        print(f"✅ User preference updated: {key} = {value}")

    def get_all_user_preferences(self) -> Dict:
        """Get all user preferences."""
        return self.memory['user_preferences'].copy()

    # ==================== Project Patterns ====================

    def get_project_pattern(self, key: str, default: Any = None) -> Any:
        """Get project pattern value."""
        return self.memory['project_patterns'].get(key, default)

    def set_project_pattern(self, key: str, value: Any) -> None:
        """Set project pattern value."""
        self.memory['project_patterns'][key] = value
        print(f"✅ Project pattern updated: {key} = {value}")

    def get_all_project_patterns(self) -> Dict:
        """Get all project patterns."""
        return self.memory['project_patterns'].copy()

    # ==================== Optimization History ====================

    def get_optimization_stat(self, key: str, default: Any = None) -> Any:
        """Get optimization statistic."""
        return self.memory['optimization_history'].get(key, default)

    def set_optimization_stat(self, key: str, value: Any) -> None:
        """Set optimization statistic."""
        self.memory['optimization_history'][key] = value
        print(f"✅ Optimization stat updated: {key} = {value}")

    def update_model_usage(self, model: str) -> None:
        """
        Update model usage statistics.

        Args:
            model: 'haiku' or 'sonnet'
        """
        if model.lower() == 'haiku':
            current_rate = self.get_optimization_stat('haiku_usage_rate', 0.30)
            self.set_optimization_stat('haiku_usage_rate', min(current_rate + 0.01, 1.0))
        elif model.lower() == 'sonnet':
            current_rate = self.get_optimization_stat('sonnet_usage_rate', 0.70)
            self.set_optimization_stat('sonnet_usage_rate', min(current_rate + 0.01, 1.0))

    # ==================== Mission History ====================

    def get_mission_stat(self, key: str, default: Any = None) -> Any:
        """Get mission statistic."""
        return self.memory['mission_history'].get(key, default)

    def record_mission_completion(self, mission_id: str, cost: float, success: bool = True) -> None:
        """
        Record a completed mission.

        Args:
            mission_id: Mission identifier (e.g., 'JL-003')
            cost: Actual cost of mission
            success: Whether mission was successful
        """
        total = self.get_mission_stat('total_missions', 0) + 1
        completed = self.get_mission_stat('completed_missions', 0) + (1 if success else 0)

        self.memory['mission_history']['total_missions'] = total
        self.memory['mission_history']['completed_missions'] = completed
        self.memory['mission_history']['success_rate'] = completed / total if total > 0 else 0.0

        # Update average cost
        current_avg = self.get_mission_stat('average_cost_per_mission', 0.0)
        current_count = completed - 1
        new_avg = ((current_avg * current_count) + cost) / completed if completed > 0 else cost
        self.memory['mission_history']['average_cost_per_mission'] = new_avg

        print(f"✅ Mission {mission_id} recorded: ${cost:.2f}, Success: {success}")

    # ==================== Learning System ====================

    def record_correction(self, correction: str) -> None:
        """
        Record a user correction to learn from.

        Args:
            correction: Description of what was corrected
        """
        self.memory['learned_patterns']['corrections_given'].append({
            'correction': correction,
            'timestamp': datetime.now().isoformat()
        })
        print(f"📚 Correction recorded: {correction}")

    def record_successful_strategy(self, strategy: str, context: str) -> None:
        """
        Record a successful strategy.

        Args:
            strategy: Name of strategy
            context: Context where it was successful
        """
        self.memory['learned_patterns']['successful_strategies'].append({
            'strategy': strategy,
            'context': context,
            'timestamp': datetime.now().isoformat()
        })
        print(f"✅ Successful strategy recorded: {strategy}")

    def record_failed_strategy(self, strategy: str, reason: str) -> None:
        """
        Record a failed strategy to avoid in future.

        Args:
            strategy: Name of strategy
            reason: Why it failed
        """
        self.memory['learned_patterns']['failed_strategies'].append({
            'strategy': strategy,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        })
        print(f"❌ Failed strategy recorded: {strategy}")

    # ==================== Standing Instructions ====================

    def get_standing_instructions(self) -> list:
        """Get all standing instructions."""
        return self.memory['standing_instructions'].copy()

    def add_standing_instruction(self, instruction: str) -> None:
        """Add a new standing instruction."""
        if instruction not in self.memory['standing_instructions']:
            self.memory['standing_instructions'].append(instruction)
            print(f"✅ Standing instruction added: {instruction}")

    # ==================== Quick Access ====================

    def get_github_repo(self) -> str:
        """Get GitHub repository URL (never ask user again)."""
        return self.get_user_preference('github_repo', '')

    def is_budget_conscious(self) -> bool:
        """Check if Oracle should be budget-conscious."""
        return self.get_user_preference('budget_conscious', True)

    def get_preferred_path_format(self) -> str:
        """Get preferred path format (absolute vs relative)."""
        return self.get_user_preference('path_format', 'absolute')

    def get_summary_structure(self) -> str:
        """Get preferred summary structure (cost_first vs standard)."""
        return self.get_user_preference('summary_structure', 'cost_first')

    # ==================== Display ====================

    def display_memory_summary(self) -> None:
        """Display a summary of Oracle's memory."""
        print("\n" + "="*80)
        print("💾 ORACLE MEMORY SUMMARY")
        print("="*80)

        print(f"\n📅 Created: {self.memory['created_at']}")
        print(f"📅 Last Updated: {self.memory['last_updated']}")
        print(f"🔮 Version: {self.memory['version']}")

        print("\n👤 USER PREFERENCES:")
        for key, value in self.memory['user_preferences'].items():
            print(f"  • {key}: {value}")

        print("\n📊 PROJECT PATTERNS:")
        for key, value in self.memory['project_patterns'].items():
            print(f"  • {key}: {value}")

        print("\n⚡ OPTIMIZATION HISTORY:")
        for key, value in self.memory['optimization_history'].items():
            print(f"  • {key}: {value}")

        print("\n🎯 MISSION HISTORY:")
        for key, value in self.memory['mission_history'].items():
            print(f"  • {key}: {value}")

        print("\n📚 STANDING INSTRUCTIONS:")
        for i, instruction in enumerate(self.memory['standing_instructions'], 1):
            print(f"  {i}. {instruction}")

        print("\n" + "="*80)


# Example usage and testing
if __name__ == '__main__':
    print("💾 Testing Oracle Memory System\n")

    # Initialize memory
    memory = OracleMemory()

    # Display initial state
    memory.display_memory_summary()

    # Test updating preferences
    print("\n📝 Testing preference updates...")
    memory.set_user_preference('test_preference', 'test_value')
    memory.set_project_pattern('test_pattern', True)
    memory.set_optimization_stat('test_stat', 0.95)

    # Test learning system
    print("\n📚 Testing learning system...")
    memory.record_correction("User reminded me to use full absolute paths")
    memory.record_successful_strategy("cost-first summary", "Figma analysis reports")

    # Test mission tracking
    print("\n🎯 Testing mission tracking...")
    memory.record_mission_completion("JL-003-Phase1", 12.34, success=True)

    # Save to disk
    print("\n💾 Saving memory to disk...")
    memory.save()

    # Test loading
    print("\n💾 Testing memory reload...")
    memory2 = OracleMemory()
    print(f"\n✅ GitHub Repo: {memory2.get_github_repo()}")
    print(f"✅ Path Format: {memory2.get_preferred_path_format()}")
    print(f"✅ Summary Structure: {memory2.get_summary_structure()}")

    print("\n✅ Oracle Memory System Tests Complete!")
