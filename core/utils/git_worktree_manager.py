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
        base_dir: Optional[Path] = None,
        auto_prune: bool = True,
        create_branch: bool = True
    ) -> Dict[str, Any]:
        """
        Create a new worktree for a task (BEST PRACTICES ENFORCED)

        CRITICAL WORKFLOW (from GIT-WORKTREE-BEST-PRACTICES.md):
        1. Auto-prunes stale worktrees before creation (if auto_prune=True)
        2. Creates feature branch if not exists (if create_branch=True)
        3. Creates worktree linked to branch (NOT detached HEAD)
        4. Verifies branch is checked out correctly
        5. Returns verification data for post-creation checks

        Args:
            task_name: Name of the task (e.g., "artemis-component-conversion")
            branch: Git branch name (default: feat/{task_name})
            base_dir: Base directory for worktrees (default: temp directory)
            auto_prune: Automatically prune stale worktrees before creating (recommended)
            create_branch: Create branch if it doesn't exist (recommended)

        Returns:
            Worktree information dict with path, branch, task_name, and verification data
        """
        # STEP 1: Auto-prune stale worktrees (Best Practice)
        if auto_prune:
            logger.info("🧹 Auto-pruning stale worktrees before creation...")
            self.prune_orphaned()

        # Generate worktree path
        if base_dir is None:
            base_dir = Path(tempfile.gettempdir()) / "justice-league-worktrees"

        base_dir.mkdir(parents=True, exist_ok=True)

        # Sanitize task name for filesystem
        safe_task_name = task_name.replace(' ', '-').replace('/', '-')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        worktree_name = f"{safe_task_name}-{timestamp}"
        worktree_path = base_dir / worktree_name

        # STEP 2: Determine branch (create feat/ branch if not specified)
        if branch is None:
            branch = f"feat/{safe_task_name}"
            logger.info(f"🌿 Auto-generating branch name: {branch}")

        # STEP 3: Create branch if needed and requested
        base_branch = 'main'
        if create_branch:
            # Check if branch exists
            branch_check = subprocess.run(
                ['git', 'show-ref', '--verify', '--quiet', f'refs/heads/{branch}'],
                cwd=self.repo_root,
                capture_output=True
            )

            if branch_check.returncode != 0:
                # Branch doesn't exist - create it from main
                logger.info(f"🌿 Creating new branch: {branch} from {base_branch}")
                subprocess.run(
                    ['git', 'branch', branch, base_branch],
                    cwd=self.repo_root,
                    check=True,
                    capture_output=True,
                    text=True
                )

        try:
            # STEP 4: Create worktree WITH branch (NOT detached HEAD)
            logger.info(f"🌳 Creating worktree: {worktree_path} on branch: {branch}")
            subprocess.run(
                ['git', 'worktree', 'add', str(worktree_path), branch],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
                text=True
            )

            # STEP 5: VERIFY branch is checked out (CRITICAL!)
            verification = self._verify_worktree_branch(worktree_path, branch)

            # Track worktree
            worktree_info = {
                'path': worktree_path,
                'branch': branch,
                'task_name': task_name,
                'created_at': datetime.now().isoformat(),
                'status': 'active',
                'verification': verification,
                'base_branch': base_branch
            }

            self.active_worktrees[str(worktree_path)] = worktree_info

            # Log verification results
            if verification['branch_correct']:
                logger.info(f"✅ Worktree created and verified: {worktree_path} on {branch}")
            else:
                logger.warning(f"⚠️ Worktree created but verification FAILED: {verification}")

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

    def _verify_worktree_branch(self, worktree_path: Path, expected_branch: str) -> Dict[str, Any]:
        """
        Verify that worktree is on the correct branch (BEST PRACTICE CHECK)

        This is CRITICAL - detects the common issue where work ends up on main
        instead of the feature branch.

        Args:
            worktree_path: Path to worktree
            expected_branch: Expected branch name

        Returns:
            Verification results dict
        """
        try:
            # Check current branch
            branch_result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=worktree_path,
                capture_output=True,
                text=True,
                check=True
            )
            current_branch = branch_result.stdout.strip()

            # Check commits ahead of main
            commits_result = subprocess.run(
                ['git', 'log', 'main..HEAD', '--oneline'],
                cwd=worktree_path,
                capture_output=True,
                text=True
            )
            commits_ahead = len([line for line in commits_result.stdout.split('\n') if line.strip()])

            # Check for detached HEAD
            is_detached = not bool(current_branch)

            verification = {
                'current_branch': current_branch,
                'expected_branch': expected_branch,
                'branch_correct': current_branch == expected_branch,
                'is_detached': is_detached,
                'commits_ahead_of_main': commits_ahead,
                'status': 'VERIFIED' if (current_branch == expected_branch and not is_detached) else 'FAILED'
            }

            return verification

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to verify worktree branch: {e}")
            return {
                'status': 'ERROR',
                'error': str(e)
            }

    def verify_commits(self, base_branch: str = 'main') -> Dict[str, Any]:
        """
        Verify all active worktrees have commits ahead of base branch

        This is the CRITICAL check that prevents the "work on main" issue.
        Run this BEFORE merging to ensure work is actually on feature branches.

        Args:
            base_branch: Base branch to compare against (default: 'main')

        Returns:
            Verification summary with list of worktrees and their status
        """
        logger.info(f"🔍 Verifying all worktrees have commits ahead of {base_branch}...")

        results = []
        failed_worktrees = []

        for worktree_path, info in self.active_worktrees.items():
            path = Path(worktree_path)

            if not path.exists():
                results.append({
                    'path': worktree_path,
                    'status': 'MISSING',
                    'error': 'Worktree directory not found'
                })
                failed_worktrees.append(worktree_path)
                continue

            try:
                # Get current branch
                branch_result = subprocess.run(
                    ['git', 'branch', '--show-current'],
                    cwd=path,
                    capture_output=True,
                    text=True,
                    check=True
                )
                current_branch = branch_result.stdout.strip()

                # Count commits ahead
                commits_result = subprocess.run(
                    ['git', 'log', f'{base_branch}..HEAD', '--oneline'],
                    cwd=path,
                    capture_output=True,
                    text=True
                )
                commits_ahead = len([line for line in commits_result.stdout.split('\n') if line.strip()])

                # Get latest commit
                latest_result = subprocess.run(
                    ['git', 'log', '--oneline', '-1'],
                    cwd=path,
                    capture_output=True,
                    text=True
                )
                latest_commit = latest_result.stdout.strip()

                # Check for uncommitted changes
                status_result = subprocess.run(
                    ['git', 'status', '--porcelain'],
                    cwd=path,
                    capture_output=True,
                    text=True
                )
                uncommitted_changes = len([line for line in status_result.stdout.split('\n') if line.strip()])

                # Determine status
                if commits_ahead == 0:
                    status = 'NO_COMMITS'
                    failed_worktrees.append(worktree_path)
                elif uncommitted_changes > 0:
                    status = 'UNCOMMITTED_CHANGES'
                    failed_worktrees.append(worktree_path)
                else:
                    status = 'READY_TO_MERGE'

                results.append({
                    'path': worktree_path,
                    'task_name': info.get('task_name', 'unknown'),
                    'branch': current_branch,
                    'commits_ahead': commits_ahead,
                    'uncommitted_changes': uncommitted_changes,
                    'latest_commit': latest_commit,
                    'status': status
                })

            except subprocess.CalledProcessError as e:
                results.append({
                    'path': worktree_path,
                    'status': 'ERROR',
                    'error': str(e)
                })
                failed_worktrees.append(worktree_path)

        summary = {
            'total_worktrees': len(self.active_worktrees),
            'ready_to_merge': sum(1 for r in results if r.get('status') == 'READY_TO_MERGE'),
            'failed': len(failed_worktrees),
            'worktrees': results,
            'failed_worktrees': failed_worktrees,
            'all_verified': len(failed_worktrees) == 0
        }

        if summary['all_verified']:
            logger.info(f"✅ All {summary['total_worktrees']} worktrees verified - ready to merge")
        else:
            logger.warning(f"⚠️ {summary['failed']} worktrees FAILED verification!")

        return summary


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
