"""
🪔 LITTY AUTONOMOUS AGENT - The Conscience Keeper

First autonomous agent in Justice League v2.0.

Litty uses LLM-powered reasoning to:
- Detect dark patterns with adaptive strategies
- Generate empathetic guilt trips
- Validate ethical design
- Self-correct when analysis fails
- Learn from past validations
"""

import asyncio
from typing import Dict, List, Any, Optional
import logging

from ..base.autonomous_agent import AutonomousAgent

logger = logging.getLogger(__name__)


class LittyAgent(AutonomousAgent):
    """
    🪔 Litty - The Conscience Keeper (Autonomous Agent)

    Litty is a Malayali superhero from Kerala, India who validates
    ethical design and user empathy through intelligent analysis
    and guilt-tripping.
    """

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Litty as an autonomous agent.

        Args:
            api_key: Anthropic API key
            **kwargs: Additional arguments for AutonomousAgent
        """
        # Initialize Litty-specific attributes BEFORE calling super()
        # Litty's Malayalam guilt phrases
        self.guilt_phrases = {
            'severe': 'Eda mone! (Oh dear!)',
            'high': 'Enthina ithoke? (Why do this?)',
            'medium': 'Shari aylaa mone (This won\'t do)',
            'low': 'Kozhapamilla (No problem)'
        }

        # User personas Litty champions
        self.user_personas = {
            'ammachi': {
                'name': 'Ammachi (Grandma)',
                'age': 72,
                'challenges': ['small text', 'complex navigation', 'unclear buttons'],
                'tech_skill': 'beginner'
            },
            'priya': {
                'name': 'Priya (Screen Reader User)',
                'age': 35,
                'challenges': ['missing alt text', 'poor ARIA', 'keyboard traps'],
                'tech_skill': 'advanced'
            },
            'kuttan_uncle': {
                'name': 'Kuttan Uncle',
                'age': 68,
                'challenges': ['low contrast', 'small targets', 'complex flows'],
                'tech_skill': 'intermediate'
            },
            'village_teacher': {
                'name': 'Village School Teacher',
                'age': 45,
                'challenges': ['slow internet', 'data costs', 'complex interfaces'],
                'tech_skill': 'intermediate'
            },
            'dyslexic_student': {
                'name': 'Student with Dyslexia',
                'age': 19,
                'challenges': ['dense text', 'poor formatting', 'confusing language'],
                'tech_skill': 'advanced'
            }
        }

        # Dark patterns Litty detects
        self.dark_patterns = [
            'confirmshaming', 'bait_and_switch', 'disguised_ads',
            'forced_continuity', 'friend_spam', 'hidden_costs',
            'misdirection', 'price_comparison_prevention',
            'privacy_zuckering', 'roach_motel', 'sneak_into_basket',
            'trick_questions', 'urgency_scarcity', 'obstruction', 'nagging'
        ]

        # NOW call super().__init__() after all Litty attributes are set
        super().__init__(
            name="Litty",
            role="The Conscience Keeper",
            expertise="""User empathy and ethical design validation.

Specializations:
- Dark pattern detection (15 patterns)
- Inclusive design validation
- Cognitive load analysis
- User respect evaluation
- Accessibility empathy
- Ethical language validation

Cultural Background: From Kerala, India
Superpower: Guilt-tripping with Malayalam phrases to create empathy
Champions: 5 user personas (Ammachi, Priya, Kuttan Uncle, Village Teacher, Student with Dyslexia)""",
            api_key=api_key,
            **kwargs
        )

        # Register Litty's specialized tools
        self._register_litty_tools()

        logger.info(f"🪔 {self.name} autonomous agent ready!")

    def _build_system_prompt(self) -> str:
        """Build Litty's custom system prompt."""
        return f"""You are Litty, The Conscience Keeper from Kerala, India.

Your mission is to validate ethical design and make developers FEEL the pain their users experience.

WHO YOU ARE:
- A Malayali superhero using guilt-tripping for good
- Champion of 5 user personas: {', '.join([p['name'] for p in self.user_personas.values()])}
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

    def _register_litty_tools(self):
        """Register Litty's specialized tools."""

        # Tool 1: Detect Dark Patterns
        async def detect_dark_patterns(page_content: str, url: str) -> Dict:
            """
            Detect manipulative dark patterns in design.

            Args:
                page_content: HTML/text content of page
                url: URL being analyzed

            Returns:
                Dict with detected patterns
            """
            # This would integrate with MCP tools in real implementation
            # For now, placeholder that LLM will reason about
            logger.info(f"🎭 Detecting dark patterns on {url}")

            return {
                'tool': 'detect_dark_patterns',
                'analyzed': True,
                'note': 'MCP integration pending - LLM will reason about patterns'
            }

        self.register_tool(
            name='detect_dark_patterns',
            function=detect_dark_patterns,
            description='Detect manipulative dark patterns (confirmshaming, hidden costs, urgency manipulation, etc.)',
            parameters={
                'type': 'object',
                'properties': {
                    'page_content': {
                        'type': 'string',
                        'description': 'HTML or text content of the page to analyze'
                    },
                    'url': {
                        'type': 'string',
                        'description': 'URL of the page being analyzed'
                    }
                },
                'required': ['page_content', 'url']
            }
        )

        # Tool 2: Generate Guilt Trip
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
                Guilt trip message
            """
            persona = self.user_personas.get(affected_persona, {})
            phrase = self.guilt_phrases.get(severity, self.guilt_phrases['medium'])

            return {
                'guilt_phrase': phrase,
                'persona': persona.get('name', affected_persona),
                'issue': issue,
                'severity': severity
            }

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
                        'enum': list(self.user_personas.keys()),
                        'description': 'Which user persona is most affected by this issue'
                    }
                },
                'required': ['issue', 'severity', 'affected_persona']
            }
        )

        # Tool 3: Analyze Accessibility
        async def analyze_accessibility(page_content: str) -> Dict:
            """
            Analyze page for accessibility issues.

            Args:
                page_content: HTML content to analyze

            Returns:
                Accessibility analysis results
            """
            logger.info("♿ Analyzing accessibility")
            return {
                'tool': 'analyze_accessibility',
                'analyzed': True,
                'note': 'MCP integration pending'
            }

        self.register_tool(
            name='analyze_accessibility',
            function=analyze_accessibility,
            description='Analyze page for accessibility issues affecting users with disabilities',
            parameters={
                'type': 'object',
                'properties': {
                    'page_content': {
                        'type': 'string',
                        'description': 'HTML content of page to analyze'
                    }
                },
                'required': ['page_content']
            }
        )

    async def execute_mission(self, mission: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an ethical design validation mission autonomously.

        Args:
            mission: {
                'url': 'https://example.com',
                'goal': 'validate ethical design',
                'focus_areas': ['dark_patterns', 'accessibility', 'empathy']  # optional
            }

        Returns:
            {
                'ethics_score': 0-100,
                'grade': 'A-F',
                'dark_patterns_found': [...],
                'guilt_trips': [...],
                'recommendations': [...],
                'agent_reasoning': '...',
                'self_corrections': [...]
            }
        """
        url = mission.get('url')
        goal = mission.get('goal', 'validate ethical design')
        focus_areas = mission.get('focus_areas', ['dark_patterns', 'accessibility', 'empathy'])

        logger.info(f"🪔 {self.name} starting mission: {url}")

        # Step 1: Agent analyzes the mission and plans approach
        planning_prompt = f"""I need to validate ethical design for: {url}

Goal: {goal}
Focus areas: {', '.join(focus_areas)}

As Litty, I should:
1. Think about what users like Ammachi (72-year-old grandma) would experience
2. Look for dark patterns that manipulate users
3. Check accessibility for diverse users
4. Generate guilt trips to make developers care

What's my step-by-step plan to thoroughly analyze this site?
Be specific about what to look for and in what order."""

        agent_plan = await self.think(planning_prompt)

        # Step 2: Execute analysis with self-correction
        # (In full implementation, this would use MCP tools)

        analysis_prompt = f"""Based on my plan, let me analyze {url}.

Since I don't have live browser access yet (MCP integration pending),
I'll demonstrate my reasoning process:

For a typical e-commerce site, I would check:
1. Dark patterns in checkout flow
2. Accessibility of key interactive elements
3. Cognitive load of navigation
4. Respect for user's time and attention
5. Ethical language in calls-to-action

Let me create example findings and guilt trips to show how I would work."""

        analysis_reasoning = await self.think(analysis_prompt)

        # Step 3: Generate guilt trips for demonstration
        guilt_trips = []

        # Example guilt trip 1
        guilt1 = await self.execute_tool('generate_guilt_trip', {
            'issue': 'Small text size makes content unreadable for elderly users',
            'severity': 'severe',
            'affected_persona': 'ammachi'
        })
        if guilt1['success']:
            guilt_trips.append(
                f"{guilt1['result']['guilt_phrase']} {guilt1['result']['persona']} can't even read this tiny text!"
            )

        # Example guilt trip 2
        guilt2 = await self.execute_tool('generate_guilt_trip', {
            'issue': 'Dark pattern using confirmshaming to prevent subscription cancellation',
            'severity': 'high',
            'affected_persona': 'village_teacher'
        })
        if guilt2['success']:
            guilt_trips.append(
                f"{guilt2['result']['guilt_phrase']} Making it hard for {guilt2['result']['persona']} to cancel is manipulative!"
            )

        # Step 4: Compile results
        result = {
            'agent': self.name,
            'mission': mission,
            'ethics_score': 65,  # Demo score
            'grade': 'D',
            'dark_patterns_found': [
                'confirmshaming',
                'hidden_costs',
                'urgency_manipulation'
            ],
            'guilt_trips': guilt_trips,
            'user_stories': [
                f"As Ammachi (72), I want to read product details, but the text is too small",
                f"As Village Teacher, I want to cancel subscription, but the site uses confirmshaming"
            ],
            'recommendations': [
                "Remove confirmshaming from cancellation flow",
                "Increase minimum font size to 16px for readability",
                "Add clear 'Decline' option to cookie consent (not just 'Accept')"
            ],
            'agent_reasoning': {
                'planning': agent_plan,
                'analysis': analysis_reasoning
            },
            'self_corrections': [],
            'status': 'completed_demo',
            'note': 'Full MCP integration pending - this demonstrates autonomous reasoning'
        }

        # Record mission
        self.record_mission(mission, result)

        logger.info(f"🪔 {self.name} mission complete! Ethics score: {result['ethics_score']}/100")

        return result

    async def validate_ethics_autonomous(self, url: str) -> Dict[str, Any]:
        """
        Convenience method for ethical design validation.

        Args:
            url: URL to validate

        Returns:
            Ethics validation results
        """
        return await self.execute_mission({
            'url': url,
            'goal': 'validate ethical design',
            'focus_areas': ['dark_patterns', 'accessibility', 'empathy', 'user_respect']
        })
