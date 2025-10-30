"""
🔄 Enhanced Version Control System
Advanced versioning with git integration, migrations, and dependency tracking

This module provides:
- Semantic versioning (MAJOR.MINOR.PATCH)
- Git integration for version history
- Automated rollback with safety checks
- Migration script generation
- Dependency tracking
- Breaking change detection

"Every change is tracked. Every version is recoverable. Time is on our side." - Oracle
"""

import logging
import json
import subprocess
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
from enum import Enum
import shutil
import re

logger = logging.getLogger(__name__)


class VersionChangeType(str):
    """Types of version changes"""
    MAJOR = "major"          # Breaking changes (1.0.0 → 2.0.0)
    MINOR = "minor"          # New features (1.0.0 → 1.1.0)
    PATCH = "patch"          # Bug fixes (1.0.0 → 1.0.1)


class RollbackSafety(str):
    """Rollback safety levels"""
    SAFE = "safe"            # No data loss, reversible
    CAUTION = "caution"      # Possible data loss
    DANGEROUS = "dangerous"  # Breaking changes, data loss likely


class EnhancedVersionControl:
    """
    🔄 Enhanced Version Control System

    Provides comprehensive version management for all Justice League agents:
    - Semantic versioning with automatic incrementing
    - Git integration for complete history
    - Safe rollback with validation
    - Migration script generation
    - Dependency tracking between agents
    """

    def __init__(self, oracle_kb_dir: Optional[str] = None, git_enabled: bool = True):
        """
        Initialize Enhanced Version Control

        Args:
            oracle_kb_dir: Path to Oracle's knowledge base
            git_enabled: Whether to use git integration
        """
        self.kb_dir = Path(oracle_kb_dir) if oracle_kb_dir else Path('/tmp/aldo-vision-justice-league/oracle')
        self.versions_db = self.kb_dir / 'agent_versions.json'
        self.migrations_dir = self.kb_dir / 'migrations'
        self.backups_dir = self.kb_dir / 'version_backups'
        self.git_enabled = git_enabled

        # Create directories
        self.migrations_dir.mkdir(parents=True, exist_ok=True)
        self.backups_dir.mkdir(parents=True, exist_ok=True)

        # Initialize version database if needed
        if not self.versions_db.exists():
            self._init_versions_db()

        logger.info(f"🔄 Enhanced Version Control initialized (git: {git_enabled})")

    def _init_versions_db(self):
        """Initialize versions database"""
        initial_data = {
            'agents': {},
            'version_history': [],
            'rollbacks': [],
            'migrations': [],
            'dependencies': {},
            'last_updated': datetime.now().isoformat()
        }

        with open(self.versions_db, 'w') as f:
            json.dump(initial_data, f, indent=2)

    def create_version(self,
                      agent_name: str,
                      change_type: str = VersionChangeType.PATCH,
                      changes: str = '',
                      breaking_changes: Optional[List[str]] = None,
                      dependencies: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        🔄 Create new version for an agent

        Args:
            agent_name: Agent to version
            change_type: Type of change (major/minor/patch)
            changes: Description of changes
            breaking_changes: List of breaking changes
            dependencies: Dict of {agent_name: version_required}

        Returns:
            Version record
        """
        with open(self.versions_db, 'r') as f:
            data = json.load(f)

        # Get current version or start at 1.0.0
        if agent_name in data['agents']:
            current_version = data['agents'][agent_name]['current_version']
        else:
            current_version = '0.0.0'
            data['agents'][agent_name] = {
                'current_version': current_version,
                'versions': [],
                'dependencies': {}
            }

        # Calculate new version
        new_version = self._increment_version(current_version, change_type)

        # Create backup of current agent file
        backup_path = self._create_backup(agent_name, current_version)

        # Calculate code hash
        agent_file = Path(f'core/justice_league/{agent_name}.py')
        code_hash = self._calculate_file_hash(agent_file) if agent_file.exists() else None

        # Create version record
        version_record = {
            'version': new_version,
            'previous_version': current_version,
            'agent': agent_name,
            'change_type': change_type,
            'changes': changes,
            'breaking_changes': breaking_changes or [],
            'dependencies': dependencies or {},
            'created_at': datetime.now().isoformat(),
            'code_hash': code_hash,
            'backup_path': str(backup_path) if backup_path else None,
            'git_commit': None,
            'migration_required': len(breaking_changes or []) > 0
        }

        # Git integration
        if self.git_enabled:
            git_commit = self._create_git_commit(agent_name, new_version, changes)
            version_record['git_commit'] = git_commit

        # Store version
        data['agents'][agent_name]['current_version'] = new_version
        data['agents'][agent_name]['versions'].append(version_record)
        data['version_history'].append({
            'agent': agent_name,
            'version': new_version,
            'timestamp': datetime.now().isoformat()
        })

        # Update dependencies
        if dependencies:
            data['dependencies'][agent_name] = dependencies

        data['last_updated'] = datetime.now().isoformat()

        with open(self.versions_db, 'w') as f:
            json.dump(data, f, indent=2)

        # Generate migration if needed
        if version_record['migration_required']:
            migration = self._generate_migration(agent_name, current_version, new_version, breaking_changes)
            version_record['migration_script'] = migration

        logger.info(f"🔄 Created version {new_version} for {agent_name} ({change_type})")

        return version_record

    def _increment_version(self, current: str, change_type: str) -> str:
        """Increment version using semantic versioning"""
        major, minor, patch = map(int, current.split('.'))

        if change_type == VersionChangeType.MAJOR:
            return f"{major + 1}.0.0"
        elif change_type == VersionChangeType.MINOR:
            return f"{major}.{minor + 1}.0"
        else:  # PATCH
            return f"{major}.{minor}.{patch + 1}"

    def _create_backup(self, agent_name: str, version: str) -> Optional[Path]:
        """Create backup of agent file"""
        agent_file = Path(f'core/justice_league/{agent_name}.py')

        if not agent_file.exists():
            return None

        backup_name = f"{agent_name}_v{version.replace('.', '_')}.py"
        backup_path = self.backups_dir / backup_name

        shutil.copy2(agent_file, backup_path)

        logger.info(f"🔄 Created backup: {backup_path}")

        return backup_path

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file"""
        if not file_path.exists():
            return ''

        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def _create_git_commit(self, agent_name: str, version: str, changes: str) -> Optional[str]:
        """Create git commit for version (if git available)"""
        try:
            # Check if git is available
            result = subprocess.run(['git', 'rev-parse', '--git-dir'],
                                  capture_output=True, text=True)
            if result.returncode != 0:
                logger.warning("Git not available or not in git repository")
                return None

            # Create commit
            commit_msg = f"[{agent_name}] v{version}: {changes}"

            # Stage the agent file
            subprocess.run(['git', 'add', f'core/justice_league/{agent_name}.py'],
                         capture_output=True)

            # Create commit
            result = subprocess.run(['git', 'commit', '-m', commit_msg],
                                  capture_output=True, text=True)

            if result.returncode == 0:
                # Get commit hash
                result = subprocess.run(['git', 'rev-parse', 'HEAD'],
                                      capture_output=True, text=True)
                commit_hash = result.stdout.strip()

                logger.info(f"🔄 Created git commit: {commit_hash[:8]}")
                return commit_hash
            else:
                logger.warning(f"Git commit failed: {result.stderr}")
                return None

        except Exception as e:
            logger.warning(f"Git integration error: {e}")
            return None

    def rollback_version(self,
                        agent_name: str,
                        target_version: str,
                        force: bool = False) -> Dict[str, Any]:
        """
        🔄 Rollback agent to previous version

        Args:
            agent_name: Agent to rollback
            target_version: Version to rollback to
            force: Force rollback even if unsafe

        Returns:
            Rollback result
        """
        with open(self.versions_db, 'r') as f:
            data = json.load(f)

        if agent_name not in data['agents']:
            return {
                'success': False,
                'error': f'Agent {agent_name} not found in version database'
            }

        agent_data = data['agents'][agent_name]
        current_version = agent_data['current_version']

        # Find target version
        target_record = next(
            (v for v in agent_data['versions'] if v['version'] == target_version),
            None
        )

        if not target_record:
            return {
                'success': False,
                'error': f'Version {target_version} not found for {agent_name}'
            }

        # Safety check
        safety_assessment = self._assess_rollback_safety(
            agent_name,
            current_version,
            target_version,
            agent_data['versions']
        )

        if safety_assessment['safety_level'] == RollbackSafety.DANGEROUS and not force:
            return {
                'success': False,
                'error': 'Rollback is dangerous - use force=True to override',
                'safety_assessment': safety_assessment
            }

        # Perform rollback
        rollback_result = {
            'agent': agent_name,
            'from_version': current_version,
            'to_version': target_version,
            'rollback_at': datetime.now().isoformat(),
            'safety_level': safety_assessment['safety_level'],
            'forced': force,
            'success': False
        }

        # Restore backup
        if target_record.get('backup_path'):
            backup_path = Path(target_record['backup_path'])
            if backup_path.exists():
                agent_file = Path(f'core/justice_league/{agent_name}.py')
                shutil.copy2(backup_path, agent_file)
                rollback_result['success'] = True
                rollback_result['method'] = 'backup_restore'

                logger.info(f"🔄 Restored {agent_name} from backup: {backup_path}")
            else:
                rollback_result['error'] = 'Backup file not found'

        # Git rollback
        elif self.git_enabled and target_record.get('git_commit'):
            git_success = self._git_rollback(agent_name, target_record['git_commit'])
            rollback_result['success'] = git_success
            rollback_result['method'] = 'git_checkout'

            if not git_success:
                rollback_result['error'] = 'Git rollback failed'
        else:
            rollback_result['error'] = 'No backup or git commit available'

        # Update version database
        if rollback_result['success']:
            agent_data['current_version'] = target_version

            # Record rollback
            data['rollbacks'].append(rollback_result)
            data['last_updated'] = datetime.now().isoformat()

            with open(self.versions_db, 'w') as f:
                json.dump(data, f, indent=2)

        logger.info(f"🔄 Rollback {agent_name}: {current_version} → {target_version} ({'success' if rollback_result['success'] else 'failed'})")

        return rollback_result

    def _assess_rollback_safety(self,
                                agent_name: str,
                                from_version: str,
                                to_version: str,
                                version_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess safety of rollback operation"""
        assessment = {
            'safety_level': RollbackSafety.SAFE,
            'warnings': [],
            'breaking_changes_detected': [],
            'data_loss_risk': False
        }

        # Find versions between current and target
        from_idx = next((i for i, v in enumerate(version_history) if v['version'] == from_version), -1)
        to_idx = next((i for i, v in enumerate(version_history) if v['version'] == to_version), -1)

        if from_idx < 0 or to_idx < 0:
            assessment['warnings'].append('Version indices not found')
            return assessment

        # Check versions being rolled back
        rolled_back_versions = version_history[to_idx + 1:from_idx + 1]

        for version in rolled_back_versions:
            # Check for breaking changes
            if version.get('breaking_changes'):
                assessment['breaking_changes_detected'].extend(version['breaking_changes'])
                assessment['safety_level'] = RollbackSafety.DANGEROUS
                assessment['data_loss_risk'] = True

            # Check for major version changes
            if version.get('change_type') == VersionChangeType.MAJOR:
                assessment['warnings'].append(f"Rolling back major version {version['version']}")
                if assessment['safety_level'] == RollbackSafety.SAFE:
                    assessment['safety_level'] = RollbackSafety.CAUTION

            # Check for migrations
            if version.get('migration_required'):
                assessment['warnings'].append(f"Version {version['version']} required migration")
                if assessment['safety_level'] != RollbackSafety.DANGEROUS:
                    assessment['safety_level'] = RollbackSafety.CAUTION

        return assessment

    def _git_rollback(self, agent_name: str, commit_hash: str) -> bool:
        """Rollback using git checkout"""
        try:
            agent_file = f'core/justice_league/{agent_name}.py'

            result = subprocess.run(
                ['git', 'checkout', commit_hash, '--', agent_file],
                capture_output=True, text=True
            )

            return result.returncode == 0

        except Exception as e:
            logger.error(f"Git rollback error: {e}")
            return False

    def _generate_migration(self,
                          agent_name: str,
                          from_version: str,
                          to_version: str,
                          breaking_changes: List[str]) -> str:
        """Generate migration script for breaking changes"""
        migration_name = f"migrate_{agent_name}_{from_version.replace('.', '_')}_to_{to_version.replace('.', '_')}.py"
        migration_path = self.migrations_dir / migration_name

        migration_script = f'''"""
Migration: {agent_name} {from_version} → {to_version}
Generated: {datetime.now().isoformat()}

Breaking Changes:
{chr(10).join(f"- {change}" for change in breaking_changes)}
"""

def migrate_forward():
    """
    Apply migration to upgrade from {from_version} to {to_version}
    """
    print(f"Migrating {agent_name} forward: {from_version} → {to_version}")

    # TODO: Implement forward migration steps
    # Example:
    # - Update data structures
    # - Modify configuration
    # - Transform stored data

    pass


def migrate_backward():
    """
    Rollback migration to downgrade from {to_version} to {from_version}
    """
    print(f"Migrating {agent_name} backward: {to_version} → {from_version}")

    # TODO: Implement backward migration steps
    # Example:
    # - Restore previous data structures
    # - Revert configuration changes
    # - Transform data back to old format

    pass


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python {migration_name} [forward|backward]")
        sys.exit(1)

    direction = sys.argv[1]

    if direction == 'forward':
        migrate_forward()
    elif direction == 'backward':
        migrate_backward()
    else:
        print("Invalid direction. Use 'forward' or 'backward'")
        sys.exit(1)
'''

        with open(migration_path, 'w') as f:
            f.write(migration_script)

        # Record migration
        with open(self.versions_db, 'r') as f:
            data = json.load(f)

        data['migrations'].append({
            'agent': agent_name,
            'from_version': from_version,
            'to_version': to_version,
            'migration_file': str(migration_path),
            'created_at': datetime.now().isoformat()
        })

        with open(self.versions_db, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"🔄 Generated migration script: {migration_path}")

        return str(migration_path)

    def get_version_history(self, agent_name: str) -> List[Dict[str, Any]]:
        """Get complete version history for an agent"""
        with open(self.versions_db, 'r') as f:
            data = json.load(f)

        if agent_name not in data['agents']:
            return []

        return data['agents'][agent_name]['versions']

    def get_current_version(self, agent_name: str) -> Optional[str]:
        """Get current version of an agent"""
        with open(self.versions_db, 'r') as f:
            data = json.load(f)

        if agent_name not in data['agents']:
            return None

        return data['agents'][agent_name]['current_version']

    def check_dependencies(self, agent_name: str) -> Dict[str, Any]:
        """
        Check if agent's dependencies are satisfied

        Returns:
            Dependency check result
        """
        with open(self.versions_db, 'r') as f:
            data = json.load(f)

        dependencies = data.get('dependencies', {}).get(agent_name, {})

        check_result = {
            'agent': agent_name,
            'dependencies_satisfied': True,
            'dependency_checks': [],
            'warnings': []
        }

        for dep_agent, required_version in dependencies.items():
            current_version = self.get_current_version(dep_agent)

            if current_version is None:
                check_result['dependencies_satisfied'] = False
                check_result['dependency_checks'].append({
                    'dependency': dep_agent,
                    'required': required_version,
                    'current': None,
                    'satisfied': False,
                    'issue': 'Dependency not found'
                })
            else:
                satisfied = self._version_satisfies(current_version, required_version)

                check_result['dependency_checks'].append({
                    'dependency': dep_agent,
                    'required': required_version,
                    'current': current_version,
                    'satisfied': satisfied
                })

                if not satisfied:
                    check_result['dependencies_satisfied'] = False
                    check_result['warnings'].append(
                        f"{dep_agent} v{current_version} does not satisfy requirement v{required_version}"
                    )

        return check_result

    def _version_satisfies(self, current: str, required: str) -> bool:
        """Check if current version satisfies requirement"""
        # Simple version comparison (major.minor.patch)
        # In production, could use more sophisticated semver logic

        curr_parts = list(map(int, current.split('.')))
        req_parts = list(map(int, required.split('.')))

        # Current must be >= required
        for curr, req in zip(curr_parts, req_parts):
            if curr > req:
                return True
            elif curr < req:
                return False

        return True  # Equal versions

    def get_rollback_history(self) -> List[Dict[str, Any]]:
        """Get history of all rollbacks"""
        with open(self.versions_db, 'r') as f:
            data = json.load(f)

        return data.get('rollbacks', [])


def version_control_report() -> Dict[str, Any]:
    """
    🔄 Generate version control status report

    Returns:
        Complete version control status
    """
    vc = EnhancedVersionControl()

    with open(vc.versions_db, 'r') as f:
        data = json.load(f)

    report = {
        'generated_at': datetime.now().isoformat(),
        'total_agents': len(data.get('agents', {})),
        'total_versions': len(data.get('version_history', [])),
        'total_rollbacks': len(data.get('rollbacks', [])),
        'total_migrations': len(data.get('migrations', [])),
        'agents': {},
        'recent_versions': data.get('version_history', [])[-10:],
        'recent_rollbacks': data.get('rollbacks', [])[-5:]
    }

    for agent_name, agent_data in data.get('agents', {}).items():
        report['agents'][agent_name] = {
            'current_version': agent_data.get('current_version'),
            'total_versions': len(agent_data.get('versions', [])),
            'has_dependencies': bool(data.get('dependencies', {}).get(agent_name))
        }

    return report
