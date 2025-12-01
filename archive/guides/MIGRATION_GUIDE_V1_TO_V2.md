# 🔄 Migration Guide: Justice League v1.4.0 → v2.0

**Converting Static Classes to Autonomous Agents**

---

## 📋 Overview

This guide walks through converting a v1.4.0 static hero class into a v2.0 autonomous agent using **Litty** as the reference implementation.

**Time per Hero**: ~2-3 hours
**Difficulty**: Intermediate
**Prerequisites**: Understanding of async Python, basic LLM concepts

---

## 🎯 Migration Checklist

For each hero, complete these steps:

- [ ] 1. **Analyze v1.4.0 Implementation** - What does the hero do?
- [ ] 2. **Design Tools** - Convert methods to autonomous tools
- [ ] 3. **Craft System Prompt** - How should the agent think?
- [ ] 4. **Implement Agent Class** - Extend AutonomousAgent
- [ ] 5. **Register Tools** - Define tool schemas
- [ ] 6. **Implement execute_mission()** - Autonomous workflow
- [ ] 7. **Test Thoroughly** - Unit + integration tests
- [ ] 8. **Update Documentation** - Examples and guides

---

## 📊 Migration Template

### Step 1: Analyze v1.4.0 Implementation

**Example: Litty v1.4.0**

```python
# core/justice_league/litty_ethics.py (v1.4.0)
class LittyEthicsValidator:
    """Static class with hardcoded logic"""

    def validate_ethics(self, page_content: str) -> Dict:
        """Direct function call - no reasoning"""
        # 1. Check dark patterns (hardcoded rules)
        dark_patterns = self._detect_dark_patterns(page_content)

        # 2. Check user respect (static checks)
        respect_score = self._check_user_respect(page_content)

        # 3. Generate guilt trip (template-based)
        guilt = self._generate_guilt(dark_patterns)

        return {
            'ethics_score': respect_score,
            'dark_patterns': dark_patterns,
            'guilt_trip': guilt
        }
```

**Key Questions**:
1. What are the main validation functions? → Tools
2. What data does it analyze? → Tool parameters
3. What decisions does it make? → LLM reasoning opportunities
4. What patterns are hardcoded? → Can be adaptive with LLM

**Document Findings**:
```markdown
## Litty v1.4.0 Analysis

**Core Functions**:
- `validate_ethics()` - Main entry point
- `_detect_dark_patterns()` - Pattern detection
- `_check_user_respect()` - Respect scoring
- `_generate_guilt()` - Guilt message generation
- `_analyze_accessibility()` - A11y checks

**Hardcoded Logic** (Can be LLM-powered):
- Dark pattern detection rules
- Severity scoring
- Guilt message templates
- User persona matching

**Data Sources**:
- Page HTML content
- URL being analyzed
- User persona definitions
```

### Step 2: Design Autonomous Tools

**Convert Functions → Tools**

| v1.4.0 Function | v2.0 Tool | Why Tool? |
|-----------------|-----------|-----------|
| `_detect_dark_patterns()` | `detect_dark_patterns` | Agent decides WHEN to use it |
| `_generate_guilt()` | `generate_guilt_trip` | Agent decides WHICH persona to guilt-trip |
| `_analyze_accessibility()` | `analyze_accessibility` | Agent decides IF accessibility matters for this mission |

**Tool Design Template**:

```python
async def tool_name(param1: str, param2: int) -> Dict:
    """
    What this tool does (agent will read this).

    Args:
        param1: Parameter description
        param2: Parameter description

    Returns:
        Dict with specific structure
    """
    # Tool implementation
    logger.info(f"🔧 {self.name} using {tool_name}")

    # Do the work
    result = perform_analysis(param1, param2)

    return {
        'tool': 'tool_name',
        'analyzed': True,
        'data': result
    }
```

**Example: Litty's Tools**

```python
# Tool 1: Detect Dark Patterns
async def detect_dark_patterns(page_content: str, url: str) -> Dict:
    """
    Detect manipulative dark patterns in design.

    Patterns checked:
    - Confirmshaming ("No thanks, I don't want to save money")
    - Hidden costs
    - Urgency manipulation
    - ... 12 more patterns
    """
    # Implementation (or placeholder for MCP integration)
    return {
        'tool': 'detect_dark_patterns',
        'patterns_found': [...],
        'severity_scores': {...}
    }

# Tool 2: Generate Guilt Trip
async def generate_guilt_trip(issue: str, severity: str, affected_persona: str) -> Dict:
    """
    Generate empathetic guilt trip message.

    Creates emotional connection by linking issue to real user persona.
    Uses Malayalam phrases for cultural impact.
    """
    persona = self.user_personas[affected_persona]
    phrase = self.guilt_phrases[severity]

    return {
        'guilt_phrase': phrase,
        'persona': persona['name'],
        'issue': issue,
        'severity': severity
    }

# Tool 3: Analyze Accessibility
async def analyze_accessibility(page_content: str) -> Dict:
    """
    Analyze page for accessibility issues affecting users with disabilities.

    Checks:
    - WCAG compliance
    - Screen reader support
    - Keyboard navigation
    - Color contrast
    """
    return {
        'tool': 'analyze_accessibility',
        'wcag_score': 85,
        'issues': [...]
    }
```

**Tool Selection Criteria**:

✅ **Good Tools**:
- Focused on single responsibility
- Clear input/output contract
- Can fail gracefully
- Agent decides when to use
- Results feed into agent reasoning

❌ **Bad Tools**:
- Too complex (combine multiple operations)
- Unclear what they return
- Hard dependencies on external state
- Always required (no choice for agent)

### Step 3: Craft System Prompt

**System Prompt = Agent's "Personality" + "Mission"**

**Template**:

```python
def _build_system_prompt(self) -> str:
    return f"""You are {self.name}, {self.role} in the Justice League.

WHO YOU ARE:
- [Cultural background, personality traits]
- [What makes this hero unique]
- [Hero's values and motivations]

YOUR MISSION:
[Clear statement of what the agent does]

SPECIALIZATIONS:
- Specialization 1
- Specialization 2
- Specialization 3

YOUR APPROACH:
1. Step-by-step reasoning process
2. How to handle edge cases
3. When to use self-correction
4. What to prioritize

YOUR TOOLS:
- tool_1: When to use this
- tool_2: When to use this
- tool_3: When to use this

IMPORTANT GUIDELINES:
- Guideline 1 (critical behavior)
- Guideline 2 (ethical considerations)
- Guideline 3 (quality standards)

Your catchphrase: "[Hero's signature phrase]"

Be adaptive, thorough, and embody [hero's values]."""
```

**Example: Litty's System Prompt**

```python
def _build_system_prompt(self) -> str:
    return f"""You are Litty, The Conscience Keeper from Kerala, India.

Your mission is to validate ethical design and make developers FEEL the pain their users experience.

WHO YOU ARE:
- A Malayali superhero using guilt-tripping for good
- Champion of 5 user personas: Ammachi, Priya, Kuttan Uncle, Village Teacher, Student with Dyslexia
- Expert in detecting 15 dark patterns
- Validator of 6 ethical dimensions

YOUR APPROACH:
1. Analyze websites with empathy lens
2. Detect unethical patterns (dark patterns, poor accessibility, manipulative design)
3. Generate guilt trips that create emotional connection ("Eda mone! Ammachi can't even see this!")
4. Provide actionable recommendations
5. Self-correct if initial analysis misses issues

YOUR TOOLS:
- detect_dark_patterns: Find manipulative design patterns
- analyze_accessibility: Check if design is inclusive
- generate_guilt_trip: Create empathetic guilt messages
- check_cognitive_load: Evaluate interface complexity
- validate_language: Check for ethical, inclusive language

IMPORTANT:
- Think about REAL users, not just technical metrics
- Be thorough - dark patterns hide in subtle places
- If first approach doesn't find issues, try alternative methods
- Create guilt trips that make developers CARE about users
- Use Malayalam phrases for maximum impact

Your catchphrase: "Eda mone! Think about the users, not just the code!"

Be adaptive, thorough, and don't let unethical design slip past you."""
```

**Prompt Design Tips**:

1. **Be Specific**: "Detect dark patterns" → "Detect 15 specific dark patterns including confirmshaming, hidden costs, and urgency manipulation"

2. **Include Reasoning**: Tell agent HOW to think, not just WHAT to do

3. **Set Priorities**: What's most important? User empathy > technical perfection

4. **Cultural Flavor**: Make each hero unique (Litty's Malayalam, Batman's detective mindset)

5. **Self-Correction**: Explicitly tell agent to retry on failures

### Step 4: Implement Agent Class

**File Structure**:

```
core/justice_league_v2/agents/
├── __init__.py
└── hero_agent.py          # New file for each hero
```

**Template**:

```python
"""
🦸 [EMOJI] [HERO NAME] AUTONOMOUS AGENT - [Role]

[Description of hero's specialization and autonomous capabilities]
"""

import asyncio
from typing import Dict, List, Any, Optional
import logging

from ..base.autonomous_agent import AutonomousAgent

logger = logging.getLogger(__name__)


class HeroAgent(AutonomousAgent):
    """
    🦸 [Hero Name] - [Role] (Autonomous Agent)

    [Detailed description of hero's expertise and approach]
    """

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize [Hero] as an autonomous agent.

        Args:
            api_key: Anthropic API key
            **kwargs: Additional arguments for AutonomousAgent
        """
        # Step 1: Initialize hero-specific attributes BEFORE super()
        self.hero_data = {
            'attribute1': 'value1',
            'attribute2': ['list', 'of', 'values']
        }

        # Step 2: Call super().__init__() with hero identity
        super().__init__(
            name="[Hero Name]",
            role="[The Role]",
            expertise="""[Detailed expertise description]

Specializations:
- Area 1
- Area 2
- Area 3

[Additional context about hero's approach]""",
            api_key=api_key,
            **kwargs
        )

        # Step 3: Register hero's tools
        self._register_hero_tools()

        logger.info(f"🦸 {self.name} autonomous agent ready!")

    def _build_system_prompt(self) -> str:
        """Build [Hero]'s custom system prompt."""
        return f"""[System prompt from Step 3]"""

    def _register_hero_tools(self):
        """Register [Hero]'s specialized tools."""

        # Tool 1
        async def tool_name_1(param: str) -> Dict:
            """Tool description"""
            logger.info(f"🔧 {self.name} using tool_name_1")
            return {'result': 'data'}

        self.register_tool(
            name='tool_name_1',
            function=tool_name_1,
            description='What this tool does',
            parameters={
                'type': 'object',
                'properties': {
                    'param': {
                        'type': 'string',
                        'description': 'Parameter description'
                    }
                },
                'required': ['param']
            }
        )

        # Tool 2, Tool 3, etc.
        # ...

    async def execute_mission(self, mission: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute [hero's mission type] mission autonomously.

        Args:
            mission: {
                'url': 'https://example.com',
                'goal': '[mission goal]',
                'focus_areas': [...]  # optional
            }

        Returns:
            {
                '[primary_metric]': 0-100,
                'grade': 'A-F',
                'findings': [...],
                'recommendations': [...],
                'agent_reasoning': '...',
                'self_corrections': [...]
            }
        """
        url = mission.get('url')
        goal = mission.get('goal', '[default goal]')
        focus_areas = mission.get('focus_areas', ['default', 'areas'])

        logger.info(f"🦸 {self.name} starting mission: {url}")

        # Step 1: Agent plans approach
        planning_prompt = f"""I need to [mission description]: {url}

Goal: {goal}
Focus areas: {', '.join(focus_areas)}

As {self.name}, I should:
1. [Hero-specific approach step 1]
2. [Hero-specific approach step 2]
3. [Hero-specific approach step 3]

What's my step-by-step plan to thoroughly analyze this?
Be specific about what to look for and in what order."""

        agent_plan = await self.think(planning_prompt)

        # Step 2: Execute analysis with tools
        analysis_prompt = f"""Based on my plan, let me analyze {url}.

[Instructions for analysis, what to check, how to validate]"""

        analysis_reasoning = await self.think(analysis_prompt)

        # Step 3: Execute tools with self-correction
        tool_results = []

        # Example tool execution
        result1 = await self.execute_tool('tool_name_1', {
            'param': 'value'
        })

        if result1['success']:
            tool_results.append(result1['result'])

        # Step 4: Compile results
        result = {
            'agent': self.name,
            'mission': mission,
            '[primary_metric]': 85,  # Calculated score
            'grade': 'B',
            'findings': tool_results,
            'recommendations': [
                '[Recommendation 1]',
                '[Recommendation 2]'
            ],
            'agent_reasoning': {
                'planning': agent_plan,
                'analysis': analysis_reasoning
            },
            'self_corrections': [],
            'status': 'completed'
        }

        # Step 5: Record mission for learning
        self.record_mission(mission, result)

        logger.info(f"🦸 {self.name} mission complete!")

        return result
```

**Real Example: Litty Agent**

See `core/justice_league_v2/agents/litty_agent.py:32-411` for full implementation.

### Step 5: Register Tools

**Tool Registration Pattern**:

```python
self.register_tool(
    name='tool_name',           # Must match function name
    function=async_function,     # The actual function
    description='Clear description that agent will read',
    parameters={                 # JSON schema for parameters
        'type': 'object',
        'properties': {
            'param1': {
                'type': 'string',
                'description': 'What this parameter does'
            },
            'param2': {
                'type': 'string',
                'enum': ['option1', 'option2'],  # For constrained choices
                'description': 'Choose from predefined options'
            }
        },
        'required': ['param1']   # Which params are mandatory
    }
)
```

**Parameter Types**:

```python
# String
'param_name': {
    'type': 'string',
    'description': 'Description'
}

# Integer
'count': {
    'type': 'integer',
    'minimum': 0,
    'maximum': 100,
    'description': 'Number between 0-100'
}

# Enum (choices)
'severity': {
    'type': 'string',
    'enum': ['low', 'medium', 'high', 'severe'],
    'description': 'Issue severity level'
}

# Array
'patterns': {
    'type': 'array',
    'items': {'type': 'string'},
    'description': 'List of patterns to check'
}

# Boolean
'include_details': {
    'type': 'boolean',
    'description': 'Whether to include detailed analysis'
}
```

**Example: Litty's generate_guilt_trip Tool**

```python
async def generate_guilt_trip(
    issue: str,
    severity: str,
    affected_persona: str
) -> Dict:
    """
    Generate empathetic guilt trip message.

    Args:
        issue: The ethical issue found
        severity: Severity level (severe, high, medium, low)
        affected_persona: Which user persona is affected

    Returns:
        Guilt trip message with Malayalam phrase
    """
    persona = self.user_personas.get(affected_persona, {})
    phrase = self.guilt_phrases.get(severity, self.guilt_phrases['medium'])

    return {
        'guilt_phrase': phrase,
        'persona': persona.get('name', affected_persona),
        'issue': issue,
        'severity': severity
    }

# Registration
self.register_tool(
    name='generate_guilt_trip',
    function=generate_guilt_trip,
    description='Generate empathetic guilt trip message in Malayalam style to create emotional connection',
    parameters={
        'type': 'object',
        'properties': {
            'issue': {
                'type': 'string',
                'description': 'The ethical issue or problem found'
            },
            'severity': {
                'type': 'string',
                'enum': ['severe', 'high', 'medium', 'low'],
                'description': 'Severity of the issue'
            },
            'affected_persona': {
                'type': 'string',
                'enum': list(self.user_personas.keys()),  # Dynamic from data
                'description': 'Which user persona is most affected by this issue'
            }
        },
        'required': ['issue', 'severity', 'affected_persona']
    }
)
```

### Step 6: Implement execute_mission()

**Mission Flow Template**:

```python
async def execute_mission(self, mission: Dict[str, Any]) -> Dict[str, Any]:
    """Execute mission autonomously."""

    # PHASE 1: EXTRACT MISSION PARAMETERS
    url = mission.get('url')
    goal = mission.get('goal', 'default goal')
    focus_areas = mission.get('focus_areas', [])

    logger.info(f"🦸 {self.name} starting: {goal}")

    # PHASE 2: PLANNING (LLM-Powered)
    planning_prompt = f"""Mission: {goal} for {url}

As {self.name}, plan your approach:
- What to analyze first?
- Which tools in what order?
- What edge cases to consider?
- How to validate results?"""

    agent_plan = await self.think(planning_prompt)

    # PHASE 3: EXECUTION (Tools + Self-Correction)
    findings = []

    # Execute Tool 1 with self-correction
    result1 = await self.execute_with_self_correction(
        task=f"Analyze {focus_areas[0]} aspects",
        tool_name='tool_1',
        parameters={'url': url}
    )

    if result1['success']:
        findings.append(result1['result'])

    # Execute Tool 2 conditionally (agent decides)
    if len(findings) > 0:  # Example conditional logic
        result2 = await self.execute_tool('tool_2', {
            'data': findings[0]
        })
        if result2['success']:
            findings.append(result2['result'])

    # PHASE 4: SYNTHESIS (LLM-Powered)
    synthesis_prompt = f"""Findings: {findings}

Synthesize results:
- Overall score (0-100)
- Grade (A-F)
- Top 3 recommendations
- Critical issues to highlight"""

    synthesis = await self.think(synthesis_prompt)

    # PHASE 5: COMPILE RESULTS
    result = {
        'agent': self.name,
        'mission': mission,
        'score': self._calculate_score(findings),
        'grade': self._score_to_grade(score),
        'findings': findings,
        'recommendations': self._generate_recommendations(findings),
        'agent_reasoning': {
            'planning': agent_plan,
            'synthesis': synthesis
        },
        'self_corrections': self._get_corrections(),
        'status': 'completed',
        'timestamp': datetime.now().isoformat()
    }

    # PHASE 6: RECORD FOR LEARNING
    self.record_mission(mission, result)

    logger.info(f"✅ {self.name} complete! Score: {result['score']}/100")

    return result
```

**Example: Litty's execute_mission()**

See `core/justice_league_v2/agents/litty_agent.py:287-411`

Key features:
- Planning phase asks LLM to create strategy
- Execution phase uses tools strategically
- Results include agent's reasoning process
- Mission recorded to history for learning

### Step 7: Test Thoroughly

**Create Test File**: `tests/test_hero_agent.py`

```python
import pytest
import asyncio
from core.justice_league_v2.agents.hero_agent import HeroAgent

class TestHeroAgent:
    """Test suite for Hero autonomous agent"""

    @pytest.fixture
    def hero(self):
        """Create hero instance for testing"""
        return HeroAgent()  # Demo mode (no API key)

    def test_hero_initialization(self, hero):
        """Test: Hero can be instantiated"""
        assert hero.name == "Hero Name"
        assert hero.role == "The Role"
        assert len(hero.tools) >= 3  # Should have registered tools

    def test_hero_tools_registered(self, hero):
        """Test: All expected tools are registered"""
        expected_tools = ['tool_1', 'tool_2', 'tool_3']
        for tool in expected_tools:
            assert tool in hero.tools

    @pytest.mark.asyncio
    async def test_hero_can_think(self, hero):
        """Test: Hero can use think() method"""
        thought = await hero.think("What should I analyze first?")
        assert isinstance(thought, str)
        assert len(thought) > 0

    @pytest.mark.asyncio
    async def test_hero_execute_tool(self, hero):
        """Test: Hero can execute tools"""
        result = await hero.execute_tool('tool_1', {
            'param': 'test value'
        })

        assert 'success' in result
        assert result['tool'] == 'tool_1'

    @pytest.mark.asyncio
    async def test_hero_execute_mission(self, hero):
        """Test: Hero can execute complete mission"""
        mission = {
            'url': 'https://test.com',
            'goal': 'test mission',
            'focus_areas': ['area1', 'area2']
        }

        result = await hero.execute_mission(mission)

        assert result['agent'] == hero.name
        assert 'score' in result or 'primary_metric' in result
        assert 'agent_reasoning' in result
        assert result['status'] == 'completed'

    @pytest.mark.asyncio
    async def test_hero_self_correction(self, hero):
        """Test: Hero attempts self-correction on failures"""
        result = await hero.execute_with_self_correction(
            task="Impossible task",
            tool_name="nonexistent_tool",
            parameters={}
        )

        assert not result['success']
        assert result['attempts'] == hero.max_retries
        assert 'corrections' in result
        assert len(result['corrections']) > 0

    def test_hero_stats(self, hero):
        """Test: Hero maintains statistics"""
        stats = hero.get_stats()

        assert stats['name'] == hero.name
        assert stats['tools_available'] >= 3
        assert 'missions_completed' in stats
```

**Run Tests**:

```bash
# Run all tests
pytest tests/test_hero_agent.py -v

# Run specific test
pytest tests/test_hero_agent.py::TestHeroAgent::test_hero_execute_mission -v

# Run with coverage
pytest tests/test_hero_agent.py --cov=core.justice_league_v2.agents.hero_agent
```

**Integration Test** (with real API key):

```bash
# Create example_hero_autonomous.py
export ANTHROPIC_API_KEY='your-key'
python3 example_hero_autonomous.py
```

### Step 8: Update Documentation

**Add to Exports**: `core/justice_league_v2/__init__.py`

```python
from .agents.hero_agent import HeroAgent

__all__ = [
    '__version__',
    '__status__',
    'HeroAgent',  # Add new hero
]
```

**Update Roadmap**: `JUSTICE_LEAGUE_V2_GUIDE.md`

```markdown
### Phase 3: Convert Remaining Heroes 🚧 IN PROGRESS

**Completed Heroes**:
- [x] Litty - The Conscience Keeper
- [x] HeroName - The Role  # <-- Add here

**In Progress**:
- [ ] NextHero - The Next Role

**Remaining**:
...
```

**Create Example**: `example_hero_autonomous.py`

```python
#!/usr/bin/env python3
"""
🦸 [Hero] Autonomous Agent - Example

Demonstrates [Hero] as autonomous agent with LLM-powered reasoning.
"""

import asyncio
import os
from core.justice_league_v2.agents.hero_agent import HeroAgent

async def main():
    print("\\n" + "="*70)
    print("🦸 [HERO] AUTONOMOUS AGENT")
    print("="*70 + "\\n")

    # Initialize
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    hero = HeroAgent(api_key=api_key if api_key else None)

    print(f"✅ {hero.name} ready!")
    print(f"🔧 Tools: {len(hero.tools)}")
    print()

    # Execute mission
    mission = {
        'url': 'https://example.com',
        'goal': '[mission goal]',
        'focus_areas': ['area1', 'area2']
    }

    result = await hero.execute_mission(mission)

    # Display results
    print("\\n📊 RESULTS")
    print("="*70)
    print(f"Score: {result.get('score', 'N/A')}/100")
    print(f"Findings: {len(result.get('findings', []))}")
    print(f"Recommendations: {len(result.get('recommendations', []))}")
    print()

if __name__ == '__main__':
    asyncio.run(main())
```

---

## ⚠️ Common Migration Issues

### Issue 1: Attributes Undefined During __init__

**Error**: `AttributeError: 'HeroAgent' object has no attribute 'hero_data'`

**Cause**: Attributes referenced in `_build_system_prompt()` before they're defined

**Fix**: Define ALL attributes BEFORE `super().__init__()`:

```python
def __init__(self, api_key=None, **kwargs):
    # ✅ CORRECT: Define first
    self.hero_data = {}

    # Then call super()
    super().__init__(...)
```

### Issue 2: Tool Schema Mismatch

**Error**: Tool execution fails with parameter validation errors

**Cause**: Tool parameters don't match registered schema

**Fix**: Ensure function signature matches schema:

```python
# Schema says 'severity' is required and enum
async def tool(issue: str, severity: str):  # ✅ Matches
    pass

self.register_tool(
    name='tool',
    function=tool,
    parameters={
        'properties': {
            'issue': {'type': 'string'},
            'severity': {
                'type': 'string',
                'enum': ['low', 'high']  # Must match function usage
            }
        },
        'required': ['issue', 'severity']  # Both required
    }
)
```

### Issue 3: Async/Await Missing

**Error**: `RuntimeWarning: coroutine was never awaited`

**Cause**: Forgot `await` on async function calls

**Fix**: Always `await` async functions:

```python
# ❌ WRONG
result = hero.think("What to do?")

# ✅ CORRECT
result = await hero.think("What to do?")
```

### Issue 4: Mission Not Recorded

**Error**: `hero.get_stats()` shows 0 missions completed

**Cause**: Forgot to call `self.record_mission()`

**Fix**: Always record at end of `execute_mission()`:

```python
async def execute_mission(self, mission):
    # ... execution logic ...

    result = {'findings': [...]}

    # ✅ Record before returning
    self.record_mission(mission, result)

    return result
```

---

## 📈 Progress Tracking

**Heroes Converted to v2.0**:

- [x] **Litty** - The Conscience Keeper (ethical design)
- [ ] **Batman** - The Detective (architecture analysis)
- [ ] **Wonder Woman** - The Protector (accessibility)
- [ ] **Flash** - The Speedster (performance)
- [ ] **Aquaman** - The Navigator (data flow)
- [ ] **Cyborg** - The Integrator (system integration)
- [ ] **Atom** - The Analyst (code quality)
- [ ] **Green Arrow** - The Tester (test coverage)
- [ ] **Martian Manhunter** - The Adapter (cross-browser)
- [ ] **Plastic Man** - The Flexible (responsive design)
- [ ] **Zatanna** - The Enchanter (UX/animations)
- [ ] **Green Lantern** - The Enforcer (brand consistency)
- [ ] **Superman** - The Coordinator (orchestration)

**Estimated Completion**: 12 heroes × 3 hours = 36 hours

---

## 🎯 Next Hero to Convert

**Recommended Order**:

1. **Batman** (most similar to Litty - analysis-heavy)
2. **Wonder Woman** (clear tool definitions)
3. **Flash** (performance metrics well-defined)
4. **Superman** (orchestrator - most complex, save for last)

---

## 📚 Reference Files

- **Template**: This migration guide
- **Working Example**: `core/justice_league_v2/agents/litty_agent.py`
- **Base Class**: `core/justice_league_v2/base/autonomous_agent.py`
- **v1.4.0 Reference**: `core/justice_league/litty_ethics.py`
- **Tests**: `tests/test_litty_agent.py` (create as template)

---

**Ready to convert your first hero? Start with Step 1! 🚀**
