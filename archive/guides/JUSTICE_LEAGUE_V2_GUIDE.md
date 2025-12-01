# 🦸 Justice League v2.0 - Autonomous Agent Architecture

**Status**: Development - Pilot Agent (Litty) Complete
**Version**: 2.0.0-alpha
**Date**: 2025-10-20

---

## 🎯 What's New in v2.0?

Justice League v2.0 represents a **fundamental architecture shift** from static Python classes to **true autonomous agents** powered by LLM reasoning.

### v1.4.0 vs. v2.0 Comparison

| Feature | v1.4.0 (Static Classes) | v2.0 (Autonomous Agents) |
|---------|-------------------------|--------------------------|
| **Intelligence** | Hardcoded logic | LLM-powered reasoning (Claude) |
| **Decision Making** | Pre-programmed rules | Adaptive planning with context |
| **Error Handling** | Try/catch blocks | Self-correction with retry loops |
| **Tool Execution** | Direct function calls | Strategic tool selection |
| **Learning** | None | Memory and mission history |
| **Independence** | Requires Superman coordination | Can operate autonomously |
| **Claude Skills** | ✅ All 13 heroes | ✅ All 13 heroes (maintained) |
| **Orchestration** | ✅ Superman coordinator | ✅ Superman as autonomous orchestrator |

### Key Capabilities

**v2.0 Autonomous Agents Can:**

1. **Think and Plan** - Use LLM to reason about missions and plan approaches
2. **Self-Correct** - Detect failures and automatically try alternative strategies
3. **Learn** - Remember past missions and improve over time
4. **Communicate** - Share knowledge with other agents (planned)
5. **Adapt** - Adjust strategies based on context and results

---

## 🏗️ Architecture Overview

### Directory Structure

```
aldo-vision/
├── core/
│   ├── justice_league/           # v1.4.0 - Static classes (PRODUCTION)
│   │   ├── batman_architecture.py
│   │   ├── litty_ethics.py
│   │   └── superman_coordinator.py
│   │
│   └── justice_league_v2/        # v2.0 - Autonomous agents (DEVELOPMENT)
│       ├── __init__.py
│       ├── base/
│       │   ├── __init__.py
│       │   └── autonomous_agent.py    # Foundation for all agents
│       └── agents/
│           ├── __init__.py
│           └── litty_agent.py         # ✅ First autonomous agent
│
├── requirements.txt              # v1.4.0 dependencies
├── requirements_v2.txt           # v2.0 dependencies (NEW)
├── example_litty.py             # v1.4.0 usage
└── example_litty_autonomous.py  # v2.0 usage (NEW)
```

### Core Components

#### 1. AutonomousAgent Base Class

**Location**: `core/justice_league_v2/base/autonomous_agent.py`

**Purpose**: Foundation for all autonomous agents with:
- LLM integration (Anthropic Claude API)
- Reasoning and planning capabilities
- Self-correction with retry loops
- Tool registration and execution
- Memory and learning framework

**Key Methods**:

```python
class AutonomousAgent:
    async def think(prompt: str) -> str:
        """Use LLM to reason about a problem"""
        # Returns agent's thoughts/reasoning

    async def execute_tool(tool_name: str, parameters: Dict) -> Dict:
        """Execute a registered tool"""
        # Returns tool execution result

    async def execute_with_self_correction(task: str, tool_name: str,
                                          parameters: Dict) -> Dict:
        """Execute tool with automatic retries on failure"""
        # Returns result with self-correction attempts

    async def execute_mission(mission: Dict) -> Dict:
        """Main entry point - execute mission autonomously"""
        # Override in subclasses
```

#### 2. LittyAgent - Pilot Implementation

**Location**: `core/justice_league_v2/agents/litty_agent.py`

**Status**: ✅ Complete and tested

**Specialization**: Ethical design validation with Malayalam guilt-tripping

**Registered Tools**:
- `detect_dark_patterns` - Find manipulative design patterns
- `generate_guilt_trip` - Create empathetic guilt messages
- `analyze_accessibility` - Check inclusive design

**User Personas**:
- Ammachi (72-year-old grandma)
- Priya (screen reader user)
- Kuttan Uncle (68-year-old)
- Village School Teacher
- Student with Dyslexia

**Dark Patterns Detected**: 15 patterns including confirmshaming, hidden costs, urgency manipulation

---

## 🚀 Installation and Setup

### Step 1: Install Dependencies

```bash
# Navigate to project
cd /Users/admin/Documents/claudecode/Projects/aldo-vision

# Install v2.0 requirements
pip3 install -r requirements_v2.txt
```

**New Dependencies for v2.0**:
- `anthropic>=0.18.0` - Claude API for LLM reasoning
- `aiohttp>=3.9.0` - Async HTTP for tool calls

### Step 2: Set Up Anthropic API Key

**Option A: Environment Variable** (Recommended)
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

**Option B: Pass to Agent Constructor**
```python
litty = LittyAgent(api_key='your-key-here')
```

**Get API Key**: [console.anthropic.com](https://console.anthropic.com/)

### Step 3: Verify Installation

```bash
# Run autonomous Litty example
python3 example_litty_autonomous.py
```

**Expected Output**:
```
🪔 LITTY AUTONOMOUS AGENT - Justice League v2.0
True autonomous agent with LLM-powered reasoning
======================================================================

🤖 Initializing Litty as autonomous agent...
✅ Litty (The Conscience Keeper) ready!
📊 Tools available: 3
🧠 Model: claude-sonnet-4-20250514
```

---

## 📖 Usage Guide

### Basic Usage: Autonomous Litty Agent

```python
import asyncio
from core.justice_league_v2.agents.litty_agent import LittyAgent

async def main():
    # Initialize autonomous agent
    litty = LittyAgent(api_key='your-key-here')

    # Define mission
    mission = {
        'url': 'https://example.com',
        'goal': 'validate ethical design',
        'focus_areas': ['dark_patterns', 'accessibility', 'empathy']
    }

    # Execute autonomously (agent plans and executes)
    result = await litty.execute_mission(mission)

    # Review results
    print(f"Ethics Score: {result['ethics_score']}/100")
    print(f"Grade: {result['grade']}")
    print(f"Dark Patterns: {result['dark_patterns_found']}")
    print(f"Guilt Trips: {result['guilt_trips']}")
    print(f"Agent Reasoning: {result['agent_reasoning']}")

asyncio.run(main())
```

### Advanced Usage: With Self-Correction

```python
# Execute specific tool with automatic retries
result = await litty.execute_with_self_correction(
    task="Detect dark patterns on checkout page",
    tool_name="detect_dark_patterns",
    parameters={
        'page_content': html_content,
        'url': 'https://example.com/checkout'
    }
)

if result['success']:
    print(f"Found patterns: {result['result']}")
    print(f"Attempts needed: {result['attempts']}")
    print(f"Self-corrections: {result['corrections']}")
```

### Demo Mode (No API Key Required)

```python
# Works without API key - simulates autonomous behavior
litty = LittyAgent()  # No api_key provided

result = await litty.execute_mission(mission)
# Outputs demo reasoning and example results
```

---

## 🛠️ How Autonomous Agents Work

### Execution Flow

```
1. MISSION RECEIVED
   └─> Agent receives mission parameters
       └─> URL, goal, focus areas

2. PLANNING PHASE (LLM-Powered)
   └─> Agent uses think() to reason about approach
       └─> "What users would be affected?"
       └─> "What dark patterns to check first?"
       └─> "In what order should I execute tools?"

3. EXECUTION PHASE
   └─> Agent executes tools strategically
       └─> Tool 1: detect_dark_patterns
       └─> Tool 2: analyze_accessibility
       └─> Tool 3: generate_guilt_trip

4. SELF-CORRECTION (If Failures Occur)
   └─> Tool failed? Agent thinks about why
       └─> LLM suggests alternative approach
       └─> Retry with adjusted parameters
       └─> Max 3 attempts per tool

5. RESULTS COMPILATION
   └─> Agent compiles findings
       └─> Ethics score, grade, recommendations
       └─> Agent reasoning documented
       └─> Self-corrections logged

6. MISSION RECORDING
   └─> Save to mission history for learning
       └─> Future missions can reference past learnings
```

### Example: Litty's Autonomous Reasoning

**Mission**: Validate ethics for e-commerce site

**Planning Prompt** (sent to LLM):
```
I need to validate ethical design for: https://example-ecommerce.com

Goal: validate ethical design
Focus areas: dark_patterns, accessibility, empathy

As Litty, I should:
1. Think about what users like Ammachi (72-year-old grandma) would experience
2. Look for dark patterns that manipulate users
3. Check accessibility for diverse users
4. Generate guilt trips to make developers care

What's my step-by-step plan to thoroughly analyze this site?
Be specific about what to look for and in what order.
```

**LLM Response** (agent's plan):
```
Here's my strategic approach:

1. First, analyze the checkout flow for dark patterns:
   - Confirmshaming ("No thanks, I don't want to save money")
   - Hidden costs that appear at final step
   - Forced continuity (auto-renewal without clear notice)

2. Then check accessibility for Ammachi and Priya:
   - Text size for elderly users
   - Alt text for screen readers
   - Keyboard navigation for Priya

3. Generate guilt trips for each issue found:
   - Link to affected persona
   - Use appropriate Malayalam phrase based on severity
   - Create emotional connection to user pain

4. If initial tools fail, try alternative methods:
   - Different selectors for dark pattern detection
   - Multiple accessibility checkers
   - Adjust severity thresholds
```

**Execution**: Agent follows plan, executes tools, handles failures

---

## 🔧 Creating New Autonomous Agents

### Template Pattern (Follow Litty)

```python
from typing import Dict, Any, Optional
from ..base.autonomous_agent import AutonomousAgent

class YourHeroAgent(AutonomousAgent):
    """
    🦸 Your Hero - The [Role]

    [Description of hero's specialization]
    """

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        # 1. Initialize hero-specific attributes BEFORE super()
        self.hero_data = {
            'special_power': 'X-ray vision',
            'nemesis': 'Lex Luthor'
        }

        # 2. Call super().__init__() with hero identity
        super().__init__(
            name="Your Hero",
            role="The [Role]",
            expertise="""Your hero's expertise.

Specializations:
- Area 1
- Area 2
- Area 3""",
            api_key=api_key,
            **kwargs
        )

        # 3. Register hero-specific tools
        self._register_hero_tools()

    def _build_system_prompt(self) -> str:
        """Build custom system prompt for this hero."""
        return f"""You are {self.name}, {self.role}.

Your mission: [Describe hero's mission]

YOUR APPROACH:
1. Step 1
2. Step 2
3. Step 3

YOUR TOOLS:
- tool_1: Description
- tool_2: Description

Be thorough and adaptive."""

    def _register_hero_tools(self):
        """Register hero's specialized tools."""

        async def hero_tool_1(param1: str) -> Dict:
            """Tool 1 description"""
            # Tool implementation
            return {'result': 'data'}

        self.register_tool(
            name='hero_tool_1',
            function=hero_tool_1,
            description='What this tool does',
            parameters={
                'type': 'object',
                'properties': {
                    'param1': {
                        'type': 'string',
                        'description': 'Parameter description'
                    }
                },
                'required': ['param1']
            }
        )

    async def execute_mission(self, mission: Dict[str, Any]) -> Dict[str, Any]:
        """Execute hero's mission autonomously."""

        # 1. Plan approach
        plan = await self.think(f"Plan for mission: {mission}")

        # 2. Execute tools with self-correction
        result1 = await self.execute_with_self_correction(
            task="Task description",
            tool_name="hero_tool_1",
            parameters={'param1': 'value'}
        )

        # 3. Compile results
        mission_result = {
            'agent': self.name,
            'mission': mission,
            'findings': result1,
            'agent_reasoning': plan,
            'status': 'completed'
        }

        # 4. Record for learning
        self.record_mission(mission, mission_result)

        return mission_result
```

---

## 🎯 Roadmap to Full v2.0

### Phase 1: Foundation ✅ COMPLETE

- [x] Create AutonomousAgent base class
- [x] Implement LLM integration
- [x] Add self-correction framework
- [x] Build tool execution system
- [x] Add memory and learning foundation

### Phase 2: Pilot Agent ✅ COMPLETE

- [x] Convert Litty to LittyAgent
- [x] Test autonomous reasoning
- [x] Verify self-correction
- [x] Create usage examples
- [x] Document architecture

### Phase 3: Convert Remaining Heroes 🚧 IN PROGRESS

**Next Heroes to Convert** (Priority Order):

1. **Batman** - Architecture analysis
   - Tools: analyze_structure, check_patterns, validate_scalability

2. **Wonder Woman** - Accessibility validation
   - Tools: check_wcag, test_screen_reader, validate_aria

3. **Flash** - Performance analysis
   - Tools: measure_speed, analyze_bottlenecks, optimize_load

4. **Aquaman** - Data flow analysis
   - Tools: trace_data, validate_privacy, check_security

5. **Cyborg** - Integration testing
   - Tools: test_api, validate_integration, check_dependencies

6. Atom - Code quality
7. Green Arrow - Testing coverage
8. Martian Manhunter - Cross-browser
9. Plastic Man - Responsiveness
10. Zatanna - Animation/UX
11. Green Lantern - Brand consistency

### Phase 4: Superman Orchestrator Agent 🔮 PLANNED

- [ ] Convert Superman to autonomous orchestrator
- [ ] Implement intelligent hero selection (LLM-powered)
- [ ] Dynamic mission planning
- [ ] Inter-agent communication protocol
- [ ] Result synthesis and recommendations

### Phase 5: Advanced Capabilities 🔮 PLANNED

- [ ] Persistent memory across sessions
- [ ] Agent learning from mission history
- [ ] Knowledge sharing between agents
- [ ] Collaborative multi-agent missions
- [ ] Web UI for mission control

---

## 📊 Testing Autonomous Agents

### Unit Tests

```python
import pytest
from core.justice_league_v2.agents.litty_agent import LittyAgent

@pytest.mark.asyncio
async def test_litty_autonomous_mission():
    """Test Litty can execute mission autonomously"""
    litty = LittyAgent()  # Demo mode

    mission = {
        'url': 'https://test.com',
        'goal': 'validate ethics'
    }

    result = await litty.execute_mission(mission)

    assert result['agent'] == 'Litty'
    assert 'ethics_score' in result
    assert 'agent_reasoning' in result

@pytest.mark.asyncio
async def test_self_correction():
    """Test agent self-corrects on failures"""
    litty = LittyAgent()

    # This will fail but agent should attempt corrections
    result = await litty.execute_with_self_correction(
        task="Impossible task",
        tool_name="nonexistent_tool",
        parameters={}
    )

    assert not result['success']
    assert result['attempts'] == litty.max_retries
    assert len(result['corrections']) > 0
```

### Integration Tests

```bash
# Test with real API key
export ANTHROPIC_API_KEY='your-key'
python3 example_litty_autonomous.py
```

**Expected Behavior**:
- Agent thinks and plans using LLM
- Agent executes tools strategically
- Agent self-corrects on failures
- Results include agent reasoning

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'anthropic'"

**Solution**:
```bash
pip3 install anthropic>=0.18.0
```

**Or Run in Demo Mode**:
```python
# Works without anthropic library
litty = LittyAgent()  # No api_key needed
```

### Issue: "Agent not reasoning (demo mode)"

**Cause**: No ANTHROPIC_API_KEY set

**Solution**:
```bash
export ANTHROPIC_API_KEY='sk-ant-...'
```

### Issue: "AttributeError during agent initialization"

**Cause**: Agent-specific attributes defined after `super().__init__()`

**Solution**: Move all `self.*` assignments BEFORE calling `super().__init__()`:

```python
def __init__(self, api_key: Optional[str] = None):
    # 1. Initialize attributes FIRST
    self.my_data = {}

    # 2. THEN call super()
    super().__init__(name="Hero", ...)
```

### Issue: "Tool execution fails repeatedly"

**Check**:
1. Tool parameters match schema
2. Tool function handles edge cases
3. Max retries set appropriately
4. Review agent's self-correction reasoning

---

## 💡 Best Practices

### 1. Design Effective System Prompts

**Good**:
```python
"""You are Litty, The Conscience Keeper.

Your mission: Make developers FEEL the user pain.

YOUR APPROACH:
1. Think about real users (Ammachi, Priya)
2. Detect unethical patterns
3. Generate empathetic guilt trips

Be thorough - dark patterns hide in subtle places."""
```

**Bad**:
```python
"""You are Litty. Analyze websites."""  # Too vague
```

### 2. Register Clear Tool Descriptions

**Good**:
```python
self.register_tool(
    name='detect_dark_patterns',
    description='Detect manipulative dark patterns (confirmshaming, hidden costs, urgency manipulation, etc.)',
    # ...
)
```

**Bad**:
```python
self.register_tool(
    name='detect',  # Ambiguous name
    description='Detect stuff',  # Vague description
    # ...
)
```

### 3. Implement Robust Self-Correction

**Good**:
```python
async def execute_mission(self, mission):
    # Use self-correction wrapper
    result = await self.execute_with_self_correction(
        task="Clear task description",
        tool_name="tool_name",
        parameters=params
    )

    if not result['success']:
        # Fallback strategy
        alternative_result = await self.think("What else can I try?")
```

**Bad**:
```python
async def execute_mission(self, mission):
    # Direct execution without self-correction
    result = await self.execute_tool("tool", params)
    # No handling if it fails
```

### 4. Document Agent Reasoning

**Always Include**:
```python
return {
    'findings': [...],
    'agent_reasoning': {
        'planning': plan_thoughts,
        'analysis': analysis_thoughts,
        'decisions': decision_reasoning
    },
    'self_corrections': corrections
}
```

---

## 🔗 Related Documentation

- **v1.4.0 Production Guide**: `QUICKSTART.md`
- **Architecture Analysis**: `ARCHITECTURE_ANALYSIS.md`
- **Production Deployment**: `PRODUCTION_DEPLOYMENT_REPORT.md`
- **Base Agent Class**: `core/justice_league_v2/base/autonomous_agent.py`
- **Litty Agent Source**: `core/justice_league_v2/agents/litty_agent.py`

---

## 🤝 Contributing

### Converting a Hero to Autonomous Agent

1. **Choose Hero** from roadmap priority list
2. **Study Litty** - Use `litty_agent.py` as template
3. **Identify Tools** - What specialized tools does hero need?
4. **Write System Prompt** - How should hero think and plan?
5. **Implement Mission Logic** - Autonomous execution flow
6. **Test Thoroughly** - Unit tests + integration tests
7. **Document** - Update this guide with new hero

### Questions or Issues?

File issues or questions in project documentation or contact maintainers.

---

**Built with ❤️ by Justice League v2.0 Team**

*"Eda mone! Think about the users, not just the code!"* 🪔
