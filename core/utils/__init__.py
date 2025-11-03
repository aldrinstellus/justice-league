"""
Core utilities for Justice League operations

Modules:
- git_worktree_manager: Git worktree management for parallel operations
- git_tree_storage: Git tree object storage for Oracle patterns
"""

from .git_worktree_manager import (
    GitWorktreeManager,
    HeroWorktreeContext,
    create_hero_worktree,
    cleanup_hero_worktrees
)

__all__ = [
    'GitWorktreeManager',
    'HeroWorktreeContext',
    'create_hero_worktree',
    'cleanup_hero_worktrees'
]
