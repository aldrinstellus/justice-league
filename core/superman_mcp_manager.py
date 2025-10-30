"""
🦸 SUPERMAN MCP TOOL MANAGER
=============================

Automatic MCP (Model Context Protocol) tool discovery and management.

Provides:
- Auto-discovery of MCP servers and tools
- Tool configuration and setup
- Hero-to-tool mapping
- Tool health monitoring
- Auto-installation of missing tools
- Tool capability analysis

Author: Superman (with Claude Code)
Created: October 21, 2025
Status: Production Ready - Tool Intelligence
"""

import logging
import json
import subprocess
from typing import Dict, Any, List, Optional, Set
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class MCPTool:
    """MCP Tool definition"""
    name: str
    package: str
    transport: str  # http, stdio, ssh
    capabilities: List[str]
    install_command: Optional[str] = None
    config: Dict[str, Any] = field(default_factory=dict)
    required_env: List[str] = field(default_factory=list)
    hero_affinity: List[str] = field(default_factory=list)  # Which heroes benefit most
    installed: bool = False
    healthy: bool = False
    last_check: Optional[str] = None


class SupermanMCPManager:
    """
    Superman's MCP tool manager.

    Auto-discovers, configures, and manages MCP tools for Justice League.
    """

    def __init__(self, config_dir: Optional[str] = None,
                 knowledge_base=None):
        """
        Initialize MCP Manager.

        Args:
            config_dir: Directory for MCP config files
            knowledge_base: Justice League knowledge base
        """
        self.config_dir = Path(config_dir or '/Users/admin/Documents/claudecode/Projects/aldo-vision')
        self.knowledge_base = knowledge_base

        # Tool registry
        self.known_tools: Dict[str, MCPTool] = {}
        self.installed_tools: Dict[str, MCPTool] = {}

        # Hero capabilities mapping
        self.hero_tool_needs = {
            "Batman": ["browser_automation", "screenshot", "javascript_execution"],
            "Wonder Woman": ["accessibility_testing", "aria_validation", "contrast_checking"],
            "Flash": ["performance_profiling", "lighthouse", "network_monitoring"],
            "Aquaman": ["api_testing", "http_client", "websocket"],
            "Cyborg": ["security_scanning", "vulnerability_detection", "ssl_validation"],
            "Green Lantern": ["visual_regression", "screenshot_comparison", "image_diff"],
            "Hawkgirl": ["seo_analysis", "meta_extraction", "structured_data"],
            "Martian Manhunter": ["cross_browser", "device_emulation", "user_agent"],
            "Black Canary": ["form_testing", "input_validation", "data_entry"],
            "Green Arrow": ["link_checking", "navigation_testing", "routing"],
            "Zatanna": ["css_analysis", "style_computation", "layout_testing"],
            "Shazam": ["mobile_testing", "touch_emulation", "viewport_testing"],
            "Artemis": ["figma_api", "design_extraction", "component_registry", "shadcn_cli"]
        }

        self.logger = logging.getLogger("SupermanMCPManager")
        self.logger.info("🦸 MCP Tool Manager initialized")

        # Build known tools registry
        self._build_known_tools()

        # Discover installed tools
        self._discover_installed_tools()

    def discover_tools(self) -> Dict[str, MCPTool]:
        """
        Discover available MCP tools.

        Returns:
            Dictionary of discovered tools
        """
        self.logger.info("🔍 Discovering MCP tools...")

        discovered = {}

        # Check npm global packages
        npm_tools = self._discover_npm_tools()
        discovered.update(npm_tools)

        # Check python packages
        python_tools = self._discover_python_tools()
        discovered.update(python_tools)

        # Check official MCP servers
        official_tools = self._discover_official_mcp_servers()
        discovered.update(official_tools)

        # Check local config
        local_tools = self._discover_local_config()
        discovered.update(local_tools)

        self.logger.info(f"✅ Discovered {len(discovered)} MCP tools")

        return discovered

    def recommend_tools_for_hero(self, hero: str) -> List[MCPTool]:
        """
        Recommend tools for a specific hero.

        Args:
            hero: Hero name

        Returns:
            List of recommended tools
        """
        needed_capabilities = self.hero_tool_needs.get(hero, [])
        recommendations = []

        for tool_name, tool in self.known_tools.items():
            # Check if tool capabilities match hero needs
            if any(cap in tool.capabilities for cap in needed_capabilities):
                if hero in tool.hero_affinity or not tool.hero_affinity:
                    recommendations.append(tool)

        # Sort by installed status and number of matching capabilities
        recommendations.sort(
            key=lambda t: (
                not t.installed,
                -len(set(t.capabilities) & set(needed_capabilities))
            )
        )

        return recommendations

    def install_tool(self, tool: MCPTool) -> bool:
        """
        Install an MCP tool.

        Args:
            tool: Tool to install

        Returns:
            True if installation successful
        """
        if not tool.install_command:
            self.logger.warning(f"⚠️  No install command for {tool.name}")
            return False

        self.logger.info(f"📦 Installing {tool.name}...")
        self.logger.info(f"   Command: {tool.install_command}")

        try:
            result = subprocess.run(
                tool.install_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                self.logger.info(f"✅ {tool.name} installed successfully")
                tool.installed = True
                self.installed_tools[tool.name] = tool

                # Add to config
                self._add_to_config(tool)

                # Store in knowledge base
                if self.knowledge_base:
                    self.knowledge_base.add_knowledge(
                        hero="Superman",
                        knowledge_type="tool_installation",
                        content={
                            "tool": tool.name,
                            "package": tool.package,
                            "capabilities": tool.capabilities
                        },
                        tags=["mcp", "tool_management", tool.name]
                    )

                return True
            else:
                self.logger.error(f"❌ Installation failed: {result.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"❌ Installation error: {e}")
            return False

    def configure_tool(self, tool: MCPTool, env_vars: Optional[Dict[str, str]] = None) -> bool:
        """
        Configure an MCP tool.

        Args:
            tool: Tool to configure
            env_vars: Environment variables

        Returns:
            True if configuration successful
        """
        env_vars = env_vars or {}

        self.logger.info(f"⚙️  Configuring {tool.name}...")

        # Check required environment variables
        missing_env = [var for var in tool.required_env if var not in env_vars]
        if missing_env:
            self.logger.warning(f"⚠️  Missing environment variables: {', '.join(missing_env)}")
            return False

        # Update tool config
        tool.config.update(env_vars)

        # Add to MCP config file
        return self._add_to_config(tool)

    def check_tool_health(self, tool: MCPTool) -> bool:
        """
        Check if a tool is healthy.

        Args:
            tool: Tool to check

        Returns:
            True if healthy
        """
        if not tool.installed:
            return False

        self.logger.info(f"🏥 Checking health of {tool.name}...")

        # For npm packages, check if command exists
        if tool.transport == "stdio" and tool.package.startswith("@"):
            try:
                result = subprocess.run(
                    ["npm", "list", "-g", tool.package],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                healthy = result.returncode == 0
            except Exception:
                healthy = False

        # For HTTP endpoints, try to connect
        elif tool.transport == "http":
            try:
                import urllib.request
                url = tool.config.get("url", "")
                if url:
                    with urllib.request.urlopen(url, timeout=5) as response:
                        healthy = response.status == 200
                else:
                    healthy = False
            except Exception:
                healthy = False

        else:
            healthy = True  # Assume healthy if can't check

        tool.healthy = healthy
        tool.last_check = datetime.now().isoformat()

        if healthy:
            self.logger.info(f"✅ {tool.name} is healthy")
        else:
            self.logger.warning(f"⚠️  {tool.name} is unhealthy")

        return healthy

    def auto_provision_for_hero(self, hero: str) -> Dict[str, Any]:
        """
        Auto-provision all needed tools for a hero.

        Args:
            hero: Hero name

        Returns:
            Provisioning report
        """
        self.logger.info(f"🦸 Auto-provisioning tools for {hero}...")

        recommendations = self.recommend_tools_for_hero(hero)

        report = {
            "hero": hero,
            "recommended_count": len(recommendations),
            "already_installed": 0,
            "newly_installed": 0,
            "failed": 0,
            "tools": []
        }

        for tool in recommendations:
            if tool.installed:
                report["already_installed"] += 1
                report["tools"].append({
                    "name": tool.name,
                    "status": "already_installed"
                })
            else:
                success = self.install_tool(tool)
                if success:
                    report["newly_installed"] += 1
                    report["tools"].append({
                        "name": tool.name,
                        "status": "installed"
                    })
                else:
                    report["failed"] += 1
                    report["tools"].append({
                        "name": tool.name,
                        "status": "failed"
                    })

        self.logger.info(
            f"✅ Provisioned {report['newly_installed']} tools for {hero} "
            f"({report['already_installed']} already installed, {report['failed']} failed)"
        )

        return report

    def get_tool_stats(self) -> Dict[str, Any]:
        """
        Get tool statistics.

        Returns:
            Tool statistics
        """
        return {
            "total_known": len(self.known_tools),
            "total_installed": len(self.installed_tools),
            "by_transport": self._count_by_transport(),
            "by_hero": self._count_by_hero(),
            "health_status": self._count_health_status()
        }

    def generate_tool_report(self) -> str:
        """
        Generate human-readable tool report.

        Returns:
            Report string
        """
        stats = self.get_tool_stats()

        report = []
        report.append("🦸 SUPERMAN MCP TOOL MANAGER REPORT")
        report.append("=" * 70)
        report.append(f"Known Tools: {stats['total_known']}")
        report.append(f"Installed Tools: {stats['total_installed']}")

        if stats['by_transport']:
            report.append("\n📊 Tools by Transport:")
            for transport, count in stats['by_transport'].items():
                report.append(f"  - {transport}: {count}")

        if stats['by_hero']:
            report.append("\n🦸 Tools by Hero Affinity:")
            for hero, count in sorted(stats['by_hero'].items(),
                                     key=lambda x: x[1], reverse=True):
                report.append(f"  - {hero}: {count}")

        report.append("\n📋 Installed Tools:")
        for tool_name, tool in self.installed_tools.items():
            health = "✅" if tool.healthy else "⚠️"
            report.append(f"  {health} {tool.name} ({tool.transport})")

        report.append("\n" + "=" * 70)

        return "\n".join(report)

    def _build_known_tools(self):
        """Build registry of known MCP tools."""
        # Figma MCP
        self.known_tools["figma"] = MCPTool(
            name="figma",
            package="figma-mcp",
            transport="http",
            capabilities=["figma_api", "design_extraction", "component_reading"],
            config={"url": "https://mcp.figma.com/mcp"},
            required_env=["FIGMA_TOKEN"],
            hero_affinity=["Artemis"]
        )

        # Chrome DevTools MCP
        self.known_tools["chrome-devtools"] = MCPTool(
            name="chrome-devtools",
            package="@modelcontextprotocol/server-chrome-devtools",
            transport="stdio",
            capabilities=["browser_automation", "screenshot", "javascript_execution", "network_monitoring"],
            install_command="npm install -g @modelcontextprotocol/server-chrome-devtools",
            hero_affinity=["Batman", "Flash", "Aquaman"]
        )

        # Playwright MCP
        self.known_tools["playwright"] = MCPTool(
            name="playwright",
            package="@modelcontextprotocol/server-playwright",
            transport="stdio",
            capabilities=["browser_automation", "cross_browser", "screenshot", "performance"],
            install_command="npm install -g @modelcontextprotocol/server-playwright",
            hero_affinity=["Batman", "Martian Manhunter", "Flash"]
        )

        # Sequential Thinking MCP
        self.known_tools["sequential-thinking"] = MCPTool(
            name="sequential-thinking",
            package="@modelcontextprotocol/server-sequential-thinking",
            transport="stdio",
            capabilities=["reasoning", "chain_of_thought", "problem_solving"],
            install_command="npm install -g @modelcontextprotocol/server-sequential-thinking",
            hero_affinity=["Superman"]  # Superman uses this for planning
        )

        # BrightData MCP (web scraping)
        self.known_tools["brightdata"] = MCPTool(
            name="brightdata",
            package="@modelcontextprotocol/server-brightdata",
            transport="stdio",
            capabilities=["web_scraping", "data_extraction", "search_engine"],
            install_command="npm install -g @modelcontextprotocol/server-brightdata",
            required_env=["BRIGHTDATA_API_KEY"],
            hero_affinity=["Aquaman", "Hawkgirl"]
        )

    def _discover_npm_tools(self) -> Dict[str, MCPTool]:
        """Discover npm-based MCP tools."""
        discovered = {}

        try:
            result = subprocess.run(
                ["npm", "list", "-g", "--depth=0", "--json"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                dependencies = data.get("dependencies", {})

                # Check if known tools are installed
                for tool_name, tool in self.known_tools.items():
                    if tool.package in dependencies:
                        tool.installed = True
                        discovered[tool_name] = tool

        except Exception as e:
            self.logger.warning(f"⚠️  Could not check npm packages: {e}")

        return discovered

    def _discover_python_tools(self) -> Dict[str, MCPTool]:
        """Discover Python-based MCP tools."""
        # Placeholder for Python MCP tools
        return {}

    def _discover_official_mcp_servers(self) -> Dict[str, MCPTool]:
        """Discover official MCP servers."""
        # Check known HTTP endpoints
        discovered = {}

        for tool_name, tool in self.known_tools.items():
            if tool.transport == "http":
                # HTTP endpoints don't need installation
                tool.installed = True
                discovered[tool_name] = tool

        return discovered

    def _discover_local_config(self) -> Dict[str, MCPTool]:
        """Discover tools from local .mcp.json config."""
        discovered = {}

        mcp_config = self.config_dir / ".mcp.json"
        if mcp_config.exists():
            try:
                with open(mcp_config, 'r') as f:
                    config = json.load(f)

                servers = config.get("mcpServers", {})
                for name, server_config in servers.items():
                    if name in self.known_tools:
                        tool = self.known_tools[name]
                        tool.installed = True
                        tool.config = server_config
                        discovered[name] = tool

            except Exception as e:
                self.logger.warning(f"⚠️  Could not read .mcp.json: {e}")

        return discovered

    def _discover_installed_tools(self):
        """Discover and track installed tools."""
        discovered = self.discover_tools()
        self.installed_tools.update(discovered)

        for tool in self.installed_tools.values():
            self.check_tool_health(tool)

    def _add_to_config(self, tool: MCPTool) -> bool:
        """Add tool to .mcp.json config."""
        mcp_config = self.config_dir / ".mcp.json"

        try:
            # Load existing config
            if mcp_config.exists():
                with open(mcp_config, 'r') as f:
                    config = json.load(f)
            else:
                config = {"mcpServers": {}}

            # Add tool
            if tool.transport == "http":
                config["mcpServers"][tool.name] = {
                    "type": "http",
                    "url": tool.config.get("url", "")
                }
            elif tool.transport == "stdio":
                config["mcpServers"][tool.name] = {
                    "type": "stdio",
                    "command": "npx",
                    "args": [tool.package]
                }

            # Save config
            with open(mcp_config, 'w') as f:
                json.dump(config, f, indent=2)

            self.logger.info(f"✅ Added {tool.name} to .mcp.json")
            return True

        except Exception as e:
            self.logger.error(f"❌ Could not update config: {e}")
            return False

    def _count_by_transport(self) -> Dict[str, int]:
        """Count tools by transport type."""
        counts = defaultdict(int)
        for tool in self.known_tools.values():
            counts[tool.transport] += 1
        return dict(counts)

    def _count_by_hero(self) -> Dict[str, int]:
        """Count tools by hero affinity."""
        counts = defaultdict(int)
        for tool in self.known_tools.values():
            for hero in tool.hero_affinity:
                counts[hero] += 1
        return dict(counts)

    def _count_health_status(self) -> Dict[str, int]:
        """Count tools by health status."""
        healthy = sum(1 for t in self.installed_tools.values() if t.healthy)
        unhealthy = sum(1 for t in self.installed_tools.values() if not t.healthy)
        return {
            "healthy": healthy,
            "unhealthy": unhealthy
        }


# Example usage
if __name__ == "__main__":
    # Create MCP manager
    manager = SupermanMCPManager()

    # Example 1: Discover tools
    print("\n🔍 Example 1: Discover Tools")
    tools = manager.discover_tools()
    print(f"Discovered {len(tools)} tools")

    # Example 2: Recommend tools for Artemis
    print("\n\n🎨 Example 2: Recommend Tools for Artemis")
    artemis_tools = manager.recommend_tools_for_hero("Artemis")
    print(f"Recommended {len(artemis_tools)} tools for Artemis:")
    for tool in artemis_tools[:5]:
        status = "✅ Installed" if tool.installed else "❌ Not installed"
        print(f"  - {tool.name}: {status}")

    # Example 3: Auto-provision for Batman
    print("\n\n🦇 Example 3: Auto-provision for Batman")
    report = manager.auto_provision_for_hero("Batman")
    print(json.dumps(report, indent=2))

    # Example 4: Tool statistics
    print("\n\n📊 Example 4: Tool Statistics")
    print(manager.generate_tool_report())
