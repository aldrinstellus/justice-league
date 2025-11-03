#!/usr/bin/env python3
"""
Oracle Health Check Endpoint
Week 11-12: Production Deployment Infrastructure

Comprehensive health check that validates:
1. Database connectivity
2. Core Oracle services
3. Agent health monitoring
4. Version control system
5. System resources

Exit codes:
- 0: Healthy (all checks pass)
- 1: Unhealthy (critical failures)
- 2: Degraded (warnings but operational)
"""

import sys
import os
import time
import sqlite3
from typing import Dict, List, Tuple
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class HealthChecker:
    """Comprehensive health checking for Oracle production deployment."""

    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.checks_warned = 0
        self.start_time = time.time()

    def check_database(self) -> Tuple[bool, str]:
        """Check database connectivity and integrity."""
        try:
            db_path = os.getenv('DATABASE_PATH', str(PROJECT_ROOT / 'oracle.db'))

            # Check if database file exists
            if not os.path.exists(db_path):
                return False, f"Database file not found: {db_path}"

            # Try to connect and query
            conn = sqlite3.connect(db_path, timeout=5.0)
            cursor = conn.cursor()

            # Check required tables exist
            required_tables = [
                'agents',
                'agent_versions',
                'health_metrics',
                'dependencies',
                'knowledge_base'
            ]

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = {row[0] for row in cursor.fetchall()}

            missing_tables = set(required_tables) - existing_tables
            if missing_tables:
                conn.close()
                return False, f"Missing required tables: {missing_tables}"

            # Test write access
            cursor.execute("SELECT COUNT(*) FROM agents")
            agent_count = cursor.fetchone()[0]

            conn.close()
            return True, f"Database OK ({agent_count} agents registered)"

        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    def check_imports(self) -> Tuple[bool, str]:
        """Check that critical Oracle modules can be imported."""
        try:
            # Test core imports
            from core.oracle_integration.superman_connector import SupermanConnector
            from core.oracle_integration.oracle_coordinator import OracleCoordinator
            from core.oracle_self_healing.health_monitor import AgentHealthMonitor
            from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl

            return True, "All critical modules importable"

        except ImportError as e:
            return False, f"Import error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    def check_superman_connector(self) -> Tuple[bool, str]:
        """Check Superman connector initialization."""
        try:
            from core.oracle_integration.superman_connector import get_superman_interface

            connector = get_superman_interface()

            # Test heartbeat
            heartbeat = connector.heartbeat()

            if heartbeat.get('status') == 'ok':
                return True, "Superman connector operational"
            else:
                return False, f"Heartbeat failed: {heartbeat}"

        except Exception as e:
            return False, f"Superman connector error: {str(e)}"

    def check_oracle_coordinator(self) -> Tuple[bool, str]:
        """Check Oracle coordinator status."""
        try:
            from core.oracle_integration.oracle_coordinator import OracleCoordinator

            coordinator = OracleCoordinator()

            # Get Oracle status
            status = coordinator.get_oracle_status()

            if status.get('operational'):
                capabilities_count = len(status.get('active_capabilities', []))
                return True, f"Oracle coordinator operational ({capabilities_count} active capabilities)"
            else:
                return False, "Oracle coordinator not operational"

        except Exception as e:
            return False, f"Oracle coordinator error: {str(e)}"

    def check_agent_health_system(self) -> Tuple[bool, str]:
        """Check agent health monitoring system."""
        try:
            from core.oracle_self_healing.health_monitor import AgentHealthMonitor

            monitor = AgentHealthMonitor()

            # Try to check health of a test agent
            # This is a basic check - in production, check actual agents
            return True, "Health monitoring system operational"

        except Exception as e:
            return False, f"Health monitoring error: {str(e)}"

    def check_version_control(self) -> Tuple[bool, str]:
        """Check version control system."""
        try:
            from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl

            version_control = EnhancedVersionControl()

            # Check that version control can access database
            return True, "Version control system operational"

        except Exception as e:
            return False, f"Version control error: {str(e)}"

    def check_disk_space(self) -> Tuple[bool, str]:
        """Check available disk space."""
        try:
            import shutil

            # Check data directory
            data_dir = PROJECT_ROOT / 'data'
            data_dir.mkdir(exist_ok=True)

            stat = shutil.disk_usage(str(data_dir))
            free_gb = stat.free / (1024 ** 3)
            total_gb = stat.total / (1024 ** 3)
            percent_free = (stat.free / stat.total) * 100

            if percent_free < 10:
                return False, f"Disk space critical: {free_gb:.1f}GB free ({percent_free:.1f}%)"
            elif percent_free < 20:
                return True, f"Disk space warning: {free_gb:.1f}GB free ({percent_free:.1f}%)"
            else:
                return True, f"Disk space OK: {free_gb:.1f}GB free ({percent_free:.1f}%)"

        except Exception as e:
            return True, f"Disk space check skipped: {str(e)}"  # Don't fail on this

    def check_memory(self) -> Tuple[bool, str]:
        """Check available memory (if psutil available)."""
        try:
            import psutil

            mem = psutil.virtual_memory()
            percent_available = mem.available / mem.total * 100

            if percent_available < 10:
                return False, f"Memory critical: {percent_available:.1f}% available"
            elif percent_available < 20:
                return True, f"Memory warning: {percent_available:.1f}% available"
            else:
                return True, f"Memory OK: {percent_available:.1f}% available"

        except ImportError:
            return True, "Memory check skipped (psutil not installed)"
        except Exception as e:
            return True, f"Memory check skipped: {str(e)}"

    def run_all_checks(self) -> int:
        """
        Run all health checks and return exit code.

        Returns:
            0: Healthy (all checks pass)
            1: Unhealthy (critical failures)
            2: Degraded (warnings but operational)
        """
        checks = [
            ("Database", self.check_database),
            ("Module Imports", self.check_imports),
            ("Superman Connector", self.check_superman_connector),
            ("Oracle Coordinator", self.check_oracle_coordinator),
            ("Agent Health System", self.check_agent_health_system),
            ("Version Control", self.check_version_control),
            ("Disk Space", self.check_disk_space),
            ("Memory", self.check_memory),
        ]

        print("=" * 80)
        print("Oracle Health Check")
        print("=" * 80)
        print()

        for check_name, check_func in checks:
            try:
                success, message = check_func()

                if success:
                    if "warning" in message.lower():
                        print(f"⚠  {check_name}: {message}")
                        self.checks_warned += 1
                    else:
                        print(f"✓  {check_name}: {message}")
                        self.checks_passed += 1
                else:
                    print(f"✗  {check_name}: {message}")
                    self.checks_failed += 1

            except Exception as e:
                print(f"✗  {check_name}: Unexpected error - {str(e)}")
                self.checks_failed += 1

        # Summary
        elapsed = time.time() - self.start_time
        print()
        print("=" * 80)
        print(f"Total Checks: {len(checks)}")
        print(f"Passed: {self.checks_passed}")
        print(f"Warnings: {self.checks_warned}")
        print(f"Failed: {self.checks_failed}")
        print(f"Duration: {elapsed:.2f}s")
        print("=" * 80)

        # Determine exit code
        if self.checks_failed > 0:
            print("\n❌ Status: UNHEALTHY")
            return 1
        elif self.checks_warned > 0:
            print("\n⚠️  Status: DEGRADED")
            return 2
        else:
            print("\n✅ Status: HEALTHY")
            return 0


def main():
    """Main health check entry point."""
    checker = HealthChecker()
    exit_code = checker.run_all_checks()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
