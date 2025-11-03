"""
🔌 MCP Integration Manager
Monitors and integrates Model Context Protocol (MCP) servers

Oracle uses this module to:
- Track MCP server capabilities
- Monitor for updates
- Integrate new MCP features
- Update agent implementations when MCP servers change

Supported MCP Servers:
- Claude Code SDK
- Figma MCP
- Penpot MCP
- Chrome DevTools MCP
- BrightData MCP
- Sequential Thinking MCP
- Custom MCP servers

"Stay current with the protocol. Adapt to new capabilities." - Oracle
"""

import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import subprocess
import hashlib

logger = logging.getLogger(__name__)


class MCPIntegrationManager:
    """
    🔌 MCP Integration Manager

    Manages all MCP server integrations:
    - Monitors MCP server updates
    - Tracks available capabilities
    - Detects new features
    - Proposes agent updates when MCP changes
    """

    # Known MCP servers and their capabilities
    MCP_SERVERS = {
        'claude-code-sdk': {
            'name': 'Claude Code SDK',
            'description': 'Official SDK for Claude Code development',
            'capabilities': ['code_generation', 'refactoring', 'analysis'],
            'version_command': 'claude-code --version',
            'config_path': '~/.claude/mcp_config.json'
        },
        'figma-mcp': {
            'name': 'Figma MCP',
            'description': 'Figma design file access and manipulation',
            'capabilities': ['design_access', 'component_extraction', 'style_analysis'],
            'version_command': None,
            'config_path': '~/.claude/mcp_config.json'
        },
        'penpot-mcp': {
            'name': 'Penpot MCP',
            'description': 'Open-source design tool integration',
            'capabilities': ['design_access', 'component_export', 'collaboration'],
            'version_command': None,
            'config_path': '~/.claude/mcp_config.json'
        },
        'chrome-devtools-mcp': {
            'name': 'Chrome DevTools MCP',
            'description': 'Browser automation and testing',
            'capabilities': [
                'page_navigation', 'screenshot', 'snapshot', 'click', 'fill',
                'evaluate_script', 'network_monitoring', 'performance_trace'
            ],
            'version_command': None,
            'config_path': '~/.claude/mcp_config.json'
        },
        'brightdata-mcp': {
            'name': 'BrightData MCP',
            'description': 'Web scraping and data extraction',
            'capabilities': ['web_scraping', 'search_engine', 'batch_scraping'],
            'version_command': None,
            'config_path': '~/.claude/mcp_config.json'
        },
        'sequential-thinking-mcp': {
            'name': 'Sequential Thinking MCP',
            'description': 'Advanced reasoning and problem-solving',
            'capabilities': ['chain_of_thought', 'problem_decomposition', 'solution_verification'],
            'version_command': None,
            'config_path': '~/.claude/mcp_config.json'
        },
        'tailwindcss-mcp': {
            'name': 'Tailwind CSS MCP',
            'description': 'Tailwind CSS class suggestions, utilities, and design system',
            'capabilities': [
                'class_suggestions', 'utility_lookup', 'color_palette',
                'spacing_system', 'responsive_design', 'dark_mode',
                'custom_config', 'plugin_support', 'jit_mode'
            ],
            'version_command': 'npx tailwindcss-mcp-server --version',
            'config_path': '~/.claude/mcp_config.json'
        },
        'shadcn-ui': {
            'name': 'shadcn/ui Component Library',
            'description': 'shadcn/ui component registry and documentation',
            'capabilities': [
                'component_registry', 'component_installation', 'component_customization',
                'accessibility_features', 'radix_ui_primitives', 'variant_support',
                'theme_customization', 'cli_integration', 'typescript_support'
            ],
            'version_command': 'npx shadcn@latest --version',
            'config_path': '~/.claude/mcp_config.json'
        }
    }

    def __init__(self, mcp_db_path: Optional[str] = None):
        """
        Initialize MCP Integration Manager

        Args:
            mcp_db_path: Path to MCP capabilities database
        """
        self.mcp_db_path = Path(mcp_db_path) if mcp_db_path else Path('/tmp/aldo-vision-justice-league/oracle/mcp_capabilities.json')
        self.mcp_db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize database
        if not self.mcp_db_path.exists():
            self._init_mcp_database()

        # Load current capabilities
        self.capabilities = self._load_capabilities()

        logger.info(f"🔌 MCP Integration Manager initialized")
        logger.info(f"🔌 Tracking {len(self.MCP_SERVERS)} MCP servers")

    def _init_mcp_database(self):
        """Initialize MCP capabilities database"""
        initial_data = {
            'servers': {},
            'last_updated': datetime.now().isoformat(),
            'update_history': []
        }

        # Populate with known servers
        for server_id, server_info in self.MCP_SERVERS.items():
            initial_data['servers'][server_id] = {
                **server_info,
                'capabilities_hash': self._hash_capabilities(server_info['capabilities']),
                'last_checked': datetime.now().isoformat(),
                'status': 'unknown',
                'updates_available': False
            }

        with open(self.mcp_db_path, 'w') as f:
            json.dump(initial_data, f, indent=2)

    def _load_capabilities(self) -> Dict:
        """Load MCP capabilities from database"""
        with open(self.mcp_db_path, 'r') as f:
            return json.load(f)

    def _save_capabilities(self):
        """Save MCP capabilities to database"""
        self.capabilities['last_updated'] = datetime.now().isoformat()
        with open(self.mcp_db_path, 'w') as f:
            json.dump(self.capabilities, f, indent=2)

    def _hash_capabilities(self, capabilities: List[str]) -> str:
        """Generate hash of capabilities for change detection"""
        cap_str = ','.join(sorted(capabilities))
        return hashlib.md5(cap_str.encode()).hexdigest()

    def check_mcp_updates(self) -> Dict[str, Any]:
        """
        🔌 Check all MCP servers for updates

        Returns:
            Update report with any changes detected
        """
        update_report = {
            'checked_at': datetime.now().isoformat(),
            'servers_checked': 0,
            'updates_found': 0,
            'new_capabilities': [],
            'deprecated_capabilities': [],
            'recommendations': []
        }

        for server_id, server_data in self.capabilities['servers'].items():
            update_report['servers_checked'] += 1

            # Check if server is available
            server_status = self._check_server_status(server_id, server_data)
            server_data['status'] = server_status['status']
            server_data['last_checked'] = datetime.now().isoformat()

            if server_status['status'] == 'available':
                # Check for capability changes
                current_capabilities = self._detect_server_capabilities(server_id)

                if current_capabilities:
                    current_hash = self._hash_capabilities(current_capabilities)
                    previous_hash = server_data.get('capabilities_hash', '')

                    if current_hash != previous_hash:
                        # Capabilities changed!
                        update_report['updates_found'] += 1
                        server_data['updates_available'] = True

                        # Detect what changed
                        new_caps = set(current_capabilities) - set(server_data['capabilities'])
                        deprecated_caps = set(server_data['capabilities']) - set(current_capabilities)

                        if new_caps:
                            update_report['new_capabilities'].extend([
                                {'server': server_id, 'capability': cap} for cap in new_caps
                            ])

                        if deprecated_caps:
                            update_report['deprecated_capabilities'].extend([
                                {'server': server_id, 'capability': cap} for cap in deprecated_caps
                            ])

                        # Update stored capabilities
                        server_data['capabilities'] = current_capabilities
                        server_data['capabilities_hash'] = current_hash

                        # Record update
                        self.capabilities['update_history'].append({
                            'server': server_id,
                            'timestamp': datetime.now().isoformat(),
                            'new_capabilities': list(new_caps),
                            'deprecated_capabilities': list(deprecated_caps)
                        })

                        logger.info(f"🔌 UPDATE DETECTED: {server_id} has {len(new_caps)} new capabilities, {len(deprecated_caps)} deprecated")

        # Generate recommendations
        if update_report['updates_found'] > 0:
            update_report['recommendations'].append({
                'priority': 'high',
                'action': 'Review MCP updates and update affected agents',
                'affected_servers': update_report['updates_found']
            })

        # Save changes
        self._save_capabilities()

        logger.info(f"🔌 MCP update check complete: {update_report['updates_found']} updates found")

        return update_report

    def _check_server_status(self, server_id: str, server_data: Dict) -> Dict[str, str]:
        """Check if an MCP server is available and responding"""
        status = {
            'status': 'unknown',
            'message': ''
        }

        try:
            # For now, assume servers are available if they're in our config
            # In production, this would actually check the server
            config_path = Path(server_data.get('config_path', '~/.claude/mcp_config.json')).expanduser()

            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)

                # Check if server is configured
                if server_id in str(config) or server_data['name'] in str(config):
                    status['status'] = 'available'
                    status['message'] = 'Server configured and available'
                else:
                    status['status'] = 'not_configured'
                    status['message'] = 'Server not found in MCP config'
            else:
                status['status'] = 'config_not_found'
                status['message'] = 'MCP config file not found'

        except Exception as e:
            status['status'] = 'error'
            status['message'] = str(e)

        return status

    def _detect_server_capabilities(self, server_id: str) -> Optional[List[str]]:
        """
        Detect current capabilities of an MCP server

        In production, this would query the server's capability endpoint
        For now, returns the known capabilities
        """
        if server_id in self.MCP_SERVERS:
            return self.MCP_SERVERS[server_id]['capabilities'].copy()
        return None

    def get_server_capabilities(self, server_id: str) -> Dict[str, Any]:
        """
        🔌 Get capabilities for a specific MCP server

        Args:
            server_id: MCP server identifier

        Returns:
            Server capabilities and status
        """
        if server_id not in self.capabilities['servers']:
            return {
                'error': f'Server {server_id} not found',
                'available_servers': list(self.capabilities['servers'].keys())
            }

        server_data = self.capabilities['servers'][server_id]

        return {
            'server_id': server_id,
            'name': server_data['name'],
            'description': server_data['description'],
            'capabilities': server_data['capabilities'],
            'status': server_data.get('status', 'unknown'),
            'last_checked': server_data.get('last_checked', 'never'),
            'updates_available': server_data.get('updates_available', False)
        }

    def get_all_capabilities(self) -> Dict[str, List[str]]:
        """Get all capabilities across all MCP servers"""
        all_caps = {}

        for server_id, server_data in self.capabilities['servers'].items():
            all_caps[server_id] = server_data.get('capabilities', [])

        return all_caps

    def recommend_mcp_for_task(self, task_description: str) -> List[Dict[str, Any]]:
        """
        🔌 Recommend which MCP servers to use for a task

        Args:
            task_description: Description of the task

        Returns:
            List of recommended MCP servers with reasoning
        """
        recommendations = []

        # Simple keyword matching (could be enhanced with ML)
        task_lower = task_description.lower()

        for server_id, server_data in self.capabilities['servers'].items():
            relevance_score = 0

            # Check if any capabilities match the task
            for capability in server_data.get('capabilities', []):
                if capability.replace('_', ' ') in task_lower:
                    relevance_score += 10

            # Check description
            if any(word in task_lower for word in server_data['description'].lower().split()):
                relevance_score += 5

            if relevance_score > 0:
                recommendations.append({
                    'server_id': server_id,
                    'name': server_data['name'],
                    'relevance_score': relevance_score,
                    'recommended_capabilities': server_data['capabilities'],
                    'reasoning': f"Matches task requirements with score {relevance_score}"
                })

        # Sort by relevance
        recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)

        logger.info(f"🔌 Generated {len(recommendations)} MCP recommendations for task")

        return recommendations

    def generate_mcp_report(self) -> Dict[str, Any]:
        """
        🔌 Generate comprehensive MCP integration report

        Returns:
            Complete MCP status and recommendations
        """
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_servers': len(self.capabilities['servers']),
            'available_servers': 0,
            'unavailable_servers': 0,
            'servers_with_updates': 0,
            'total_capabilities': 0,
            'servers': {},
            'recent_updates': [],
            'recommendations': []
        }

        for server_id, server_data in self.capabilities['servers'].items():
            status = server_data.get('status', 'unknown')

            if status == 'available':
                report['available_servers'] += 1
            else:
                report['unavailable_servers'] += 1

            if server_data.get('updates_available', False):
                report['servers_with_updates'] += 1

            report['total_capabilities'] += len(server_data.get('capabilities', []))

            report['servers'][server_id] = {
                'name': server_data['name'],
                'status': status,
                'capabilities_count': len(server_data.get('capabilities', [])),
                'updates_available': server_data.get('updates_available', False),
                'last_checked': server_data.get('last_checked', 'never')
            }

        # Get recent updates
        report['recent_updates'] = self.capabilities.get('update_history', [])[-10:]

        # Generate recommendations
        if report['servers_with_updates'] > 0:
            report['recommendations'].append({
                'priority': 'high',
                'issue': f"{report['servers_with_updates']} MCP servers have updates",
                'action': 'Review and integrate new MCP capabilities'
            })

        if report['unavailable_servers'] > 0:
            report['recommendations'].append({
                'priority': 'medium',
                'issue': f"{report['unavailable_servers']} MCP servers unavailable",
                'action': 'Check MCP server configuration and connectivity'
            })

        logger.info(f"🔌 MCP report: {report['available_servers']}/{report['total_servers']} servers available")

        return report

    def propose_agent_update_for_mcp(self,
                                    server_id: str,
                                    new_capabilities: List[str],
                                    affected_agents: List[str]) -> Dict[str, Any]:
        """
        🔌 Propose agent updates when MCP capabilities change

        Args:
            server_id: MCP server that changed
            new_capabilities: New capabilities added
            affected_agents: List of agents that use this MCP server

        Returns:
            Update proposal for review
        """
        proposal = {
            'proposal_id': f"MCP-UPDATE-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'created_at': datetime.now().isoformat(),
            'mcp_server': server_id,
            'new_capabilities': new_capabilities,
            'affected_agents': affected_agents,
            'proposed_changes': [],
            'testing_required': True,
            'risk_level': 'medium',
            'requires_approval': True
        }

        # Generate proposed changes for each agent
        for agent_name in affected_agents:
            proposal['proposed_changes'].append({
                'agent': agent_name,
                'change_type': 'mcp_integration_update',
                'description': f"Add support for {len(new_capabilities)} new MCP capabilities",
                'new_capabilities': new_capabilities,
                'estimated_effort': 'medium',
                'backward_compatible': True
            })

        logger.info(f"🔌 Generated MCP update proposal: {proposal['proposal_id']}")

        return proposal


# Main entry function
def check_all_mcp_servers() -> Dict[str, Any]:
    """
    🔌 Check all MCP servers for updates and generate report

    Returns:
        Complete MCP status report
    """
    manager = MCPIntegrationManager()

    # Check for updates
    update_report = manager.check_mcp_updates()

    # Generate comprehensive report
    mcp_report = manager.generate_mcp_report()

    return {
        'update_check': update_report,
        'mcp_status': mcp_report
    }
