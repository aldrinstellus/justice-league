"""
🤖 AUTONOMOUS AGENT BASE CLASS

Foundation for all Justice League autonomous agents with:
- LLM-powered reasoning and planning
- Self-correction on failures
- Tool execution with retries
- Learning from past missions
- Inter-agent collaboration
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import logging

# Try to import Anthropic - graceful fallback if not installed
try:
    from anthropic import Anthropic, AsyncAnthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    Anthropic = None
    AsyncAnthropic = None

logger = logging.getLogger(__name__)


class AutonomousAgent:
    """
    Base class for autonomous Justice League agents.

    Each agent has:
    - Unique identity and expertise
    - LLM-powered reasoning
    - Self-correction capabilities
    - Tool execution framework
    - Memory and learning
    """

    def __init__(
        self,
        name: str,
        role: str,
        expertise: str,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-20250514",
        max_retries: int = 3
    ):
        """
        Initialize autonomous agent.

        Args:
            name: Agent name (e.g., "Litty")
            role: Agent role (e.g., "The Conscience Keeper")
            expertise: What the agent specializes in
            api_key: Anthropic API key (or set ANTHROPIC_API_KEY env var)
            model: Claude model to use
            max_retries: Maximum self-correction attempts
        """
        self.name = name
        self.role = role
        self.expertise = expertise
        self.model = model
        self.max_retries = max_retries

        # Initialize Anthropic clients (if available)
        if ANTHROPIC_AVAILABLE and api_key:
            self.client = Anthropic(api_key=api_key)
            self.async_client = AsyncAnthropic(api_key=api_key)
        elif ANTHROPIC_AVAILABLE:
            try:
                self.client = Anthropic()  # Try to use env var
                self.async_client = AsyncAnthropic()
            except:
                self.client = None
                self.async_client = None
        else:
            self.client = None
            self.async_client = None
            logger.warning(f"{name}: Anthropic library not installed - running in demo mode")

        # Agent state
        self.tools: Dict[str, Callable] = {}
        self.memory: List[Dict[str, Any]] = []
        self.mission_history: List[Dict[str, Any]] = []

        # System prompt (to be customized by each agent)
        self.system_prompt = self._build_system_prompt()

        logger.info(f"🤖 {self.name} ({self.role}) initialized")

    def _build_system_prompt(self) -> str:
        """
        Build the system prompt for this agent.
        Override in subclasses for agent-specific prompts.
        """
        return f"""You are {self.name}, {self.role} in the Justice League.

Your expertise: {self.expertise}

Your mission: Analyze websites and applications to provide expert insights in your domain.

You have access to specialized tools. Think step-by-step:
1. Analyze the situation
2. Plan your approach
3. Execute tools strategically
4. If something fails, self-correct and try alternatives
5. Provide comprehensive results

Be thorough, adaptive, and don't give up when you encounter obstacles.
Always explain your reasoning."""

    def register_tool(self, name: str, function: Callable, description: str, parameters: Dict):
        """
        Register a tool that this agent can use.

        Args:
            name: Tool name
            function: Python function to execute
            description: What the tool does
            parameters: JSON schema for parameters
        """
        self.tools[name] = {
            'function': function,
            'description': description,
            'parameters': parameters
        }
        logger.debug(f"{self.name} registered tool: {name}")

    def get_tool_definitions(self) -> List[Dict]:
        """Get tool definitions in Anthropic format."""
        return [
            {
                'name': name,
                'description': tool['description'],
                'input_schema': tool['parameters']
            }
            for name, tool in self.tools.items()
        ]

    async def think(self, prompt: str, context: Optional[Dict] = None) -> str:
        """
        Use LLM to think about a problem.

        Args:
            prompt: What to think about
            context: Additional context

        Returns:
            Agent's thoughts/reasoning
        """
        if not self.async_client:
            # Demo mode - return simulated reasoning
            logger.info(f"💭 {self.name} thinking (demo mode)...")
            return f"[Demo Mode] {self.name} would reason: {prompt[:100]}..."

        messages = [{
            'role': 'user',
            'content': prompt
        }]

        if context:
            messages[0]['content'] = f"{prompt}\n\nContext: {json.dumps(context, indent=2)}"

        response = await self.async_client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=self.system_prompt,
            messages=messages
        )

        reasoning = response.content[0].text
        logger.info(f"💭 {self.name} thinking: {reasoning[:200]}...")
        return reasoning

    async def execute_tool(self, tool_name: str, parameters: Dict) -> Dict[str, Any]:
        """
        Execute a tool with the given parameters.

        Args:
            tool_name: Name of tool to execute
            parameters: Tool parameters

        Returns:
            Tool execution result
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not registered with {self.name}")

        tool = self.tools[tool_name]
        function = tool['function']

        logger.info(f"🔧 {self.name} executing tool: {tool_name}")

        try:
            # Execute tool (sync or async)
            if asyncio.iscoroutinefunction(function):
                result = await function(**parameters)
            else:
                result = function(**parameters)

            return {
                'success': True,
                'result': result,
                'tool': tool_name
            }

        except Exception as e:
            logger.error(f"❌ Tool '{tool_name}' failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'tool': tool_name
            }

    async def execute_with_self_correction(
        self,
        task: str,
        tool_name: str,
        parameters: Dict,
        validation_fn: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Execute a tool with automatic self-correction on failure.

        Args:
            task: Description of what we're trying to do
            tool_name: Tool to execute
            parameters: Tool parameters
            validation_fn: Optional function to validate results

        Returns:
            Execution result with self-correction attempts
        """
        corrections = []

        for attempt in range(self.max_retries):
            logger.info(f"🎯 {self.name} attempt {attempt + 1}/{self.max_retries}: {task}")

            # Execute tool
            result = await self.execute_tool(tool_name, parameters)

            # Check if execution succeeded
            if not result['success']:
                # Ask LLM to suggest correction
                correction_prompt = f"""The tool '{tool_name}' failed with error: {result['error']}

Task: {task}
Parameters used: {json.dumps(parameters, indent=2)}

What went wrong and how should I correct my approach?
Provide specific parameter changes or alternative strategy."""

                correction_reasoning = await self.think(correction_prompt)
                corrections.append({
                    'attempt': attempt + 1,
                    'error': result['error'],
                    'reasoning': correction_reasoning
                })

                # TODO: Parse LLM suggestion and update parameters
                # For now, continue to next attempt
                continue

            # Validate results if validation function provided
            if validation_fn and not validation_fn(result['result']):
                validation_prompt = f"""Tool executed successfully but results look incorrect.

Task: {task}
Results: {json.dumps(result['result'], indent=2)}

What might be wrong with these results? How should I adjust my approach?"""

                correction_reasoning = await self.think(validation_prompt)
                corrections.append({
                    'attempt': attempt + 1,
                    'issue': 'validation_failed',
                    'reasoning': correction_reasoning
                })

                continue

            # Success!
            return {
                'success': True,
                'result': result['result'],
                'attempts': attempt + 1,
                'corrections': corrections
            }

        # All retries exhausted
        return {
            'success': False,
            'error': 'Max retries exceeded',
            'attempts': self.max_retries,
            'corrections': corrections
        }

    async def execute_mission(self, mission: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a mission autonomously.

        This is the main entry point. Override in subclasses.

        Args:
            mission: Mission parameters

        Returns:
            Mission results
        """
        raise NotImplementedError(f"{self.name} must implement execute_mission()")

    def save_to_memory(self, key: str, value: Any):
        """Save information to agent's memory."""
        self.memory.append({
            'timestamp': datetime.now().isoformat(),
            'key': key,
            'value': value
        })

    def recall_from_memory(self, key: str) -> Optional[Any]:
        """Recall information from agent's memory."""
        for entry in reversed(self.memory):
            if entry['key'] == key:
                return entry['value']
        return None

    def record_mission(self, mission: Dict[str, Any], result: Dict[str, Any]):
        """Record a completed mission for learning."""
        self.mission_history.append({
            'timestamp': datetime.now().isoformat(),
            'mission': mission,
            'result': result
        })

    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics."""
        return {
            'name': self.name,
            'role': self.role,
            'missions_completed': len(self.mission_history),
            'tools_available': len(self.tools),
            'memory_size': len(self.memory)
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name} ({self.role})>"
