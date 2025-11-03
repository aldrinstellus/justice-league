"""
🌳 GIT WORKTREE MANAGER
Utility for managing git worktrees for parallel Justice League operations

Enables:
- Parallel hero deployments in isolated workspaces
- Clean context switching between tasks
- Atomic commits per operation
- Efficient cleanup and resource management

Version: 1.0.0
Created: 2025-10-31
"""

import logging
import subprocess
import shutil
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
import tempfile

logger = logging.getLogger(__name__)


class GitWorktreeManager:
    """
    🌳 Git Worktree Manager for parallel Justice League operations

    Manages creation, tracking, and cleanup of git worktrees for isolated
    hero workspaces.

    Features:
    - Create temporary worktrees for parallel tasks
    - Track active worktrees per mission
    - Automatic cleanup on completion
    - Error recovery and orphan detection
    - Integration with Oracle for tracking
    """

    def __init__(self, repo_root: Optional[Path] = None):
        """
        Initialize Git Worktree Manager

        Args:
            repo_root: Repository root directory (auto-detected if None)
        """
        self.repo_root = repo_root or self._find_repo_root()
        self.active_worktrees: Dict[str, Dict[str, Any]] = {}

        logger.info(f"🌳 GitWorktreeManager initialized at {self.repo_root}")

    def _find_repo_root(self) -> Path:
        """Find git repository root"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--show-toplevel'],
                capture_output=True,
                text=True,
                check=True
            )
            return Path(result.stdout.strip())
        except subprocess.CalledProcessError:
            # Fallback to current directory
            return Path.cwd()

    def create_worktree(
        self,
        task_name: str,
        branch: Optional[str] = None,
        base_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Create a new worktree for a task

        Args:
            task_name: Name of the task (e.g., "artemis-component-conversion")
            branch: Git branch to check out (default: current branch)
            base_dir: Base directory for worktrees (default: temp directory)

        Returns:
            Worktree information dict with path, branch, task_name
        """
        # Generate worktree path
        if base_dir is None:
            base_dir = Path(tempfile.gettempdir()) / "justice-league-worktrees"

        base_dir.mkdir(parents=True, exist_ok=True)

        # Sanitize task name for filesystem
        safe_task_name = task_name.replace(' ', '-').replace('/', '-')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        worktree_name = f"{safe_task_name}-{timestamp}"
        worktree_path = base_dir / worktree_name

        # Determine branch/commit
        if branch is None:
            # Get current commit SHA (works even if branch is checked out elsewhere)
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            commit_sha = result.stdout.strip()

            # Get branch name for tracking
            branch_result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )
            branch = branch_result.stdout.strip() or 'detached'
        else:
            commit_sha = branch  # Use branch name if explicitly provided

        try:
            # Create worktree using commit SHA (allows creation even if branch is checked out)
            logger.info(f"🌳 Creating worktree: {worktree_path}")
            subprocess.run(
                ['git', 'worktree', 'add', '--detach', str(worktree_path), commit_sha],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
                text=True
            )

            # Track worktree
            worktree_info = {
                'path': worktree_path,
                'branch': branch,
                'task_name': task_name,
                'created_at': datetime.now().isoformat(),
                'status': 'active'
            }

            self.active_worktrees[str(worktree_path)] = worktree_info

            logger.info(f"✅ Worktree created successfully: {worktree_path}")
            return worktree_info

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to create worktree: {e}")
            raise

    def remove_worktree(self, worktree_path: Path, force: bool = False) -> bool:
        """
        Remove a worktree

        Args:
            worktree_path: Path to the worktree
            force: Force removal even if dirty

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"🌳 Removing worktree: {worktree_path}")

            cmd = ['git', 'worktree', 'remove', str(worktree_path)]
            if force:
                cmd.append('--force')

            subprocess.run(
                cmd,
                cwd=self.repo_root,
                check=True,
                capture_output=True
            )

            # Remove from tracking
            if str(worktree_path) in self.active_worktrees:
                del self.active_worktrees[str(worktree_path)]

            logger.info(f"✅ Worktree removed: {worktree_path}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to remove worktree: {e}")
            return False

    def cleanup_all(self, force: bool = False) -> Dict[str, Any]:
        """
        Clean up all active worktrees

        Args:
            force: Force cleanup even if dirty

        Returns:
            Cleanup summary with counts
        """
        logger.info(f"🌳 Cleaning up {len(self.active_worktrees)} worktrees...")

        success_count = 0
        failure_count = 0

        for worktree_path in list(self.active_worktrees.keys()):
            if self.remove_worktree(Path(worktree_path), force=force):
                success_count += 1
            else:
                failure_count += 1

        summary = {
            'total': success_count + failure_count,
            'success': success_count,
            'failures': failure_count
        }

        logger.info(f"✅ Cleanup complete: {success_count} removed, {failure_count} failed")
        return summary

    def list_worktrees(self) -> List[Dict[str, Any]]:
        """
        List all git worktrees (including those not managed by this instance)

        Returns:
            List of worktree information dicts
        """
        try:
            result = subprocess.run(
                ['git', 'worktree', 'list', '--porcelain'],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )

            worktrees = []
            current_worktree = {}

            for line in result.stdout.split('\n'):
                if not line:
                    if current_worktree:
                        worktrees.append(current_worktree)
                        current_worktree = {}
                    continue

                if line.startswith('worktree '):
                    current_worktree['path'] = line.replace('worktree ', '')
                elif line.startswith('HEAD '):
                    current_worktree['head'] = line.replace('HEAD ', '')
                elif line.startswith('branch '):
                    current_worktree['branch'] = line.replace('branch refs/heads/', '')
                elif line == 'bare':
                    current_worktree['bare'] = True
                elif line == 'detached':
                    current_worktree['detached'] = True

            return worktrees

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to list worktrees: {e}")
            return []

    def get_worktree_status(self, worktree_path: Path) -> Dict[str, Any]:
        """
        Get status of a worktree

        Args:
            worktree_path: Path to worktree

        Returns:
            Status information dict
        """
        try:
            # Check git status
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=worktree_path,
                capture_output=True,
                text=True
            )

            has_changes = bool(result.stdout.strip())

            # Get current branch
            branch_result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=worktree_path,
                capture_output=True,
                text=True
            )

            return {
                'path': str(worktree_path),
                'has_changes': has_changes,
                'branch': branch_result.stdout.strip(),
                'clean': not has_changes
            }

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to get worktree status: {e}")
            return {'error': str(e)}

    def prune_orphaned(self) -> int:
        """
        Prune orphaned worktree administrative files

        Returns:
            Number of pruned worktrees
        """
        try:
            logger.info("🌳 Pruning orphaned worktrees...")
            result = subprocess.run(
                ['git', 'worktree', 'prune', '--verbose'],
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )

            # Count pruned entries
            pruned_count = result.stdout.count('Removing worktrees/')
            logger.info(f"✅ Pruned {pruned_count} orphaned worktrees")

            return pruned_count

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to prune worktrees: {e}")
            return 0


class HeroWorktreeContext:
    """
    Context manager for hero worktree operations

    Automatically creates and cleans up worktree for a hero task

    Usage:
        with HeroWorktreeContext(manager, "artemis-conversion") as worktree:
            # Work in worktree['path']
            artemis.generate_component(worktree['path'])
        # Automatic cleanup
    """

    def __init__(
        self,
        manager: GitWorktreeManager,
        task_name: str,
        branch: Optional[str] = None,
        cleanup_on_error: bool = True
    ):
        """
        Initialize context manager

        Args:
            manager: GitWorktreeManager instance
            task_name: Task name for the worktree
            branch: Git branch (default: current)
            cleanup_on_error: Clean up even if error occurs
        """
        self.manager = manager
        self.task_name = task_name
        self.branch = branch
        self.cleanup_on_error = cleanup_on_error
        self.worktree_info = None

    def __enter__(self) -> Dict[str, Any]:
        """Create worktree on context entry"""
        self.worktree_info = self.manager.create_worktree(
            self.task_name,
            self.branch
        )
        return self.worktree_info

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up worktree on context exit"""
        if self.worktree_info:
            path = self.worktree_info['path']

            # Determine if cleanup should proceed
            should_cleanup = exc_type is None or self.cleanup_on_error

            if should_cleanup:
                self.manager.remove_worktree(path, force=True)
            else:
                logger.warning(f"⚠️ Keeping worktree due to error: {path}")


# Convenience functions for Justice League heroes

def create_hero_worktree(
    hero_name: str,
    task_name: str,
    branch: Optional[str] = None
) -> Dict[str, Any]:
    """
    Quick worktree creation for a hero

    Args:
        hero_name: Name of the hero (e.g., "Artemis")
        task_name: Task description
        branch: Git branch

    Returns:
        Worktree info dict
    """
    manager = GitWorktreeManager()
    full_task_name = f"{hero_name.lower()}-{task_name}"
    return manager.create_worktree(full_task_name, branch)


def cleanup_hero_worktrees() -> Dict[str, Any]:
    """
    Clean up all hero worktrees

    Returns:
        Cleanup summary
    """
    manager = GitWorktreeManager()
    return manager.cleanup_all(force=True)
