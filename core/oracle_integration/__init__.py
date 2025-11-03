"""
🔗 Oracle Integration Module
Integration between Oracle and Superman coordinator

This module provides:
- Superman-Oracle coordination
- Real-time agent monitoring
- Automated health checks
- Version management coordination
- Cross-system communication
"""

from .superman_connector import SupermanConnector
from .oracle_coordinator import OracleCoordinator

__all__ = ['SupermanConnector', 'OracleCoordinator']
