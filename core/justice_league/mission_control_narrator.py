"""
🎬 MISSION CONTROL NARRATOR v2.0
Justice League Narrative System - Makes the team come alive!

Transforms technical logs into engaging superhero team banter with:
- Sequential thinking display (Oracle's reasoning process)
- Team coordination dialogue (hero handoffs)
- Progress bars with personality
- Tactical commands + friendly banter mix

"Watch the Justice League think, coordinate, and accomplish missions!" 🦸‍♂️
"""

import os
import sys
from typing import Optional, Dict, Any, List
from enum import Enum


class NarratorMode(Enum):
    """Narrator verbosity modes"""
    NARRATIVE = "narrative"   # Default: Full banter + sequential thinking + technical info
    TECHNICAL = "technical"   # Legacy: logger.info() style (for developers)
    SILENT = "silent"         # Minimal: Essential output only (for CI/CD)
    DEBUG = "debug"           # Everything: Full logs + banter (for troubleshooting)


class BanterStyle(Enum):
    """Different banter personality styles"""
    TACTICAL = "tactical"     # Mission briefing: "Batman, verify. Oracle, track."
    FRIENDLY = "friendly"     # Casual: "Nice work! How's it looking?"
    SEQUENTIAL = "sequential" # Thinking: "[Step 1] [Step 2] [Hypothesis]"


class MissionControlNarrator:
    """
    🎬 Central narrative system for Justice League operations

    Provides engaging team banter and sequential thinking display
    while technical work happens in the background.

    Features:
    - Hero dialogue (tactical, friendly, sequential)
    - Sequential thinking display (Oracle's reasoning)
    - Progress bars with commentary
    - Team handoffs and coordination
    - Mission milestones and phase transitions
    """

    def __init__(self, mode: str = "narrative"):
        """
        Initialize Mission Control Narrator

        Args:
            mode: Narrator mode (narrative, technical, silent, debug)
        """
        # Parse mode from string or enum
        if isinstance(mode, str):
            try:
                self.mode = NarratorMode(mode.lower())
            except ValueError:
                self.mode = NarratorMode.NARRATIVE
        else:
            self.mode = mode

        self.conversation_log = []
        self.step_counter = {}  # Track sequential thinking steps per hero
        self.last_progress = None  # Track last progress update
        self.banner_shown = False  # Track if banner was already shown in this session

    def is_enabled(self) -> bool:
        """Check if narrator is enabled (not silent)"""
        return self.mode != NarratorMode.SILENT

    def is_verbose(self) -> bool:
        """Check if verbose output (narrative or debug)"""
        return self.mode in [NarratorMode.NARRATIVE, NarratorMode.DEBUG]

    def show_justice_league_banner(self, mission_type: str = "", force: bool = False):
        """
        Display the JUSTICE LEAGUE banner when system is invoked

        Args:
            mission_type: Optional mission description
            force: If True, show banner even if already shown in this session (default: False)
        """
        if not self.is_enabled():
            return

        # Prevent duplicate banners in same session (unless forced)
        if self.banner_shown and not force:
            return

        banner = """
══════════════════════════════════════════════════════════════════════════════
     ╦╦ ╦╔═╗╔╦╗╦╔═╗╔═╗  ╦  ╔═╗╔═╗╔═╗╦ ╦╔═╗
     ║║ ║╚═╗ ║ ║║  ║╣   ║  ║╣ ╠═╣║ ╦║ ║║╣
    ╚╝╚═╝╚═╝ ╩ ╩╚═╝╚═╝  ╩═╝╚═╝╩ ╩╚═╝╚═╝╚═╝
══════════════════════════════════════════════════════════════════════════════
        """
        print(banner)

        if mission_type:
            mission_line = f"     🦸 MISSION: {mission_type}"
            print(mission_line.center(78))
            print("═" * 78)

        print()  # Blank line after banner

        # Mark banner as shown for this session
        self.banner_shown = True

    def should_show_banner(self, user_input: str = "") -> bool:
        """
        Determine if banner should be displayed based on trigger keywords

        Args:
            user_input: User's request text (optional)

        Returns:
            True if banner should be shown based on keyword detection

        Trigger Keywords (case-insensitive):
            - "justice league", "justice-league"
            - "/justice-league", "/superman"
            - "superman" (when referring to coordinator)
            - "assemble", "deploy heroes", "deploy the justice league"
            - "run justice league"
        """
        if not self.is_enabled():
            return False

        # Already shown in this session? Don't show again
        if self.banner_shown:
            return False

        # No user input provided? Default to showing banner
        if not user_input:
            return True

        # Keyword detection (case-insensitive)
        trigger_keywords = [
            "justice league",
            "justice-league",
            "/justice-league",
            "/superman",
            "superman",
            "assemble",
            "deploy heroes",
            "deploy the justice league",
            "run justice league"
        ]

        user_input_lower = user_input.lower()

        # Check if any trigger keyword is in user input
        for keyword in trigger_keywords:
            if keyword in user_input_lower:
                return True

        return False

    def auto_show_banner_if_needed(
        self,
        user_input: str = "",
        mission_type: str = "",
        force: bool = False
    ):
        """
        Automatically show banner if trigger keywords detected in user input

        This method combines keyword detection with banner display for convenience.
        Use this at the start of Justice League operations to ensure banner
        displays when user mentions Justice League keywords.

        Args:
            user_input: User's request text to scan for keywords
            mission_type: Optional mission description to display with banner
            force: If True, show banner even if already shown (default: False)

        Example:
            narrator.auto_show_banner_if_needed(
                user_input="Can you run justice league analysis?",
                mission_type="Design System Analysis"
            )
        """
        # Force override bypasses keyword detection
        if force:
            self.show_justice_league_banner(mission_type=mission_type, force=True)
            return

        # Check if banner should be shown based on keywords
        if self.should_show_banner(user_input):
            self.show_justice_league_banner(mission_type=mission_type)

    def hero_speaks(
        self,
        hero: str,
        message: str,
        style: str = "friendly",
        technical_info: Optional[str] = None
    ):
        """
        Hero says something to the team

        Args:
            hero: Hero emoji + name (e.g., "🦸 Superman")
            message: What the hero says
            style: Banter style (tactical, friendly, sequential)
            technical_info: Optional technical detail to show inline

        Example:
            narrator.hero_speaks("🦸 Superman", "Team, we've got a mission", style="tactical")
            # Output: 🦸 Superman: "Team, we've got a mission"
        """
        if not self.is_enabled():
            return

        # Format message based on style
        if style == "tactical":
            formatted = f"{hero}: {message}"
        elif style == "friendly":
            formatted = f'{hero}: "{message}"'
        else:
            formatted = f"{hero}: {message}"

        # Add technical info if in balanced mode and provided
        if technical_info and self.mode == NarratorMode.NARRATIVE:
            formatted += f" [{technical_info}]"

        print(formatted)
        self.conversation_log.append({
            "hero": hero,
            "message": message,
            "style": style,
            "technical_info": technical_info
        })

    def hero_thinks(
        self,
        hero: str,
        thought: str,
        step: Optional[int] = None,
        category: Optional[str] = None
    ):
        """
        Hero's internal reasoning (sequential thinking)

        Args:
            hero: Hero emoji + name
            thought: The reasoning step
            step: Step number (auto-increments if None)
            category: Label like "Scanning", "Analyzing", "Hypothesis", etc.

        Example:
            narrator.hero_thinks("🔮 Oracle", "Checking knowledge base", step=1)
            # Output: 🔮 Oracle: [Step 1] Checking knowledge base...
        """
        if not self.is_verbose():
            return

        # Auto-increment step counter if not provided
        if step is None:
            if hero not in self.step_counter:
                self.step_counter[hero] = 0
            self.step_counter[hero] += 1
            step = self.step_counter[hero]

        # Format based on category
        if category:
            prefix = f"[{category}]"
        else:
            prefix = f"[Step {step}]"

        formatted = f"{hero}: {prefix} {thought}"
        print(formatted)

        self.conversation_log.append({
            "hero": hero,
            "thought": thought,
            "step": step,
            "category": category
        })

    def team_handoff(
        self,
        from_hero: str,
        to_hero: str,
        task: str,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        One hero hands off to another

        Args:
            from_hero: Hero initiating handoff
            to_hero: Hero receiving task
            task: What needs to be done
            context: Optional context information

        Example:
            narrator.team_handoff("🦸 Superman", "🦇 Batman", "Verify completeness")
            # Output: 🦸 Superman → 🦇 Batman: Verify completeness
        """
        if not self.is_verbose():
            return

        formatted = f"{from_hero} → {to_hero}: {task}"

        # Add context if provided
        if context and self.mode == NarratorMode.NARRATIVE:
            context_str = ", ".join(f"{k}={v}" for k, v in context.items())
            formatted += f" [{context_str}]"

        print(formatted)
        self.conversation_log.append({
            "from": from_hero,
            "to": to_hero,
            "task": task,
            "context": context
        })

    def progress_with_commentary(
        self,
        current: int,
        total: int,
        hero: str = "Progress",
        commentary: Optional[str] = None,
        bar_width: int = 21
    ):
        """
        Progress bar with personality

        Args:
            current: Current progress count
            total: Total items
            hero: Hero doing the work
            commentary: Optional commentary at milestones
            bar_width: Width of progress bar (default 21 chars)

        Example:
            narrator.progress_with_commentary(89, 177, "🦅 Hawkman", "Halfway there!")
            # Output: 🦅 Hawkman: [Halfway there!] ████████████░░░░░░░░░ 89/177 (50%)
        """
        if not self.is_enabled():
            return

        # Calculate progress
        percentage = int((current / total) * 100) if total > 0 else 0
        filled = int((current / total) * bar_width) if total > 0 else 0
        bar = "█" * filled + "░" * (bar_width - filled)

        # Format output
        if commentary:
            output = f"\r{hero}: [{commentary}] {bar} {current}/{total} ({percentage}%)"
        else:
            output = f"\r{hero}: {bar} {current}/{total} ({percentage}%)"

        # Print with carriage return (overwrites previous line)
        print(output, end='', flush=True)
        self.last_progress = (current, total)

        # Newline when complete
        if current >= total:
            print()  # Move to next line

            # Reset step counter for this hero (for next sequential thinking)
            if hero in self.step_counter:
                self.step_counter[hero] = 0

    def mission_milestone(self, milestone: str, symbol: str = "="):
        """
        Major milestone in mission (visual separator)

        Args:
            milestone: Milestone description
            symbol: Character for border (default "=")

        Example:
            narrator.mission_milestone("🦅 FIGMA FRAME PNG EXPORT MISSION")
            # Output:
            # ======================================================================
            #   🦅 FIGMA FRAME PNG EXPORT MISSION
            # ======================================================================
        """
        if not self.is_verbose():
            return

        border = symbol * 70
        print()
        print(border)
        print(f"  {milestone}")
        print(border)
        print()

        self.conversation_log.append({
            "type": "milestone",
            "milestone": milestone
        })

    def section_divider(self, compact: bool = False):
        """
        Visual section divider

        Args:
            compact: If True, uses shorter divider
        """
        if not self.is_verbose():
            return

        if compact:
            print("-" * 40)
        else:
            print()

    def technical_detail(self, label: str, value: str):
        """
        Show technical detail (always visible, even in narrative mode)

        Args:
            label: Label for the detail
            value: The value

        Example:
            narrator.technical_detail("Output directory", "/absolute/path/...")
            # Output:    Output directory: /absolute/path/...
        """
        if not self.is_enabled():
            return

        print(f"   {label}: {value}")

    def completion_summary(
        self,
        status: str,
        details: Dict[str, Any]
    ):
        """
        Mission completion summary

        Args:
            status: Status emoji and text (e.g., "✅ MISSION COMPLETE")
            details: Dictionary of completion details

        Example:
            narrator.completion_summary("✅ MISSION COMPLETE", {
                "frames_exported": 177,
                "duration": "18m 42s",
                "output": "/absolute/path/"
            })
        """
        if not self.is_enabled():
            return

        print()
        print("=" * 70)
        print(f"  {status}")
        print("=" * 70)

        for key, value in details.items():
            # Format key: convert underscore to space, title case
            formatted_key = key.replace("_", " ").title()
            print(f"   {formatted_key}: {value}")

        self.conversation_log.append({
            "type": "completion",
            "status": status,
            "details": details
        })

    def get_conversation_log(self) -> List[Dict[str, Any]]:
        """Get full conversation log (for replay or analysis)"""
        return self.conversation_log

    def clear_log(self):
        """Clear conversation log"""
        self.conversation_log = []
        self.step_counter = {}

    def strategy_session_start(self, leader: str, topic: str, heroes: List[str]):
        """
        Start a team strategy session where heroes debate and collaborate

        Args:
            leader: Hero leading the session (usually Superman)
            topic: What the team is discussing
            heroes: List of heroes participating

        Example:
            narrator.strategy_session_start(
                "🦸 Superman",
                "Best methodology for dashboard conversion",
                ["🔮 Oracle", "🎨 Artemis", "👁️ Vision Analyst"]
            )
        """
        if not self.is_verbose():
            return

        print()
        print("=" * 78)
        print(f"  {leader}: STRATEGY SESSION")
        print("=" * 78)
        print(f"  Topic: {topic}")
        print(f"  Participants: {', '.join(heroes)}")
        print("=" * 78)
        print()

    def strategy_contribution(
        self,
        hero: str,
        perspective: str,
        reasoning: Optional[List[str]] = None,
        recommendation: Optional[str] = None
    ):
        """
        Record a hero's contribution to the strategy session

        Args:
            hero: Hero contributing
            perspective: Their main perspective or finding
            reasoning: Optional list of sequential thinking steps
            recommendation: Optional recommendation

        Example:
            narrator.strategy_contribution(
                "🔮 Oracle",
                "Found 2 similar dashboards in knowledge base",
                reasoning=[
                    "Scanning knowledge base for similar projects",
                    "Image-to-HTML achieved 90-95% accuracy on complex dashboards"
                ],
                recommendation="Use Image-to-HTML methodology"
            )
        """
        if not self.is_verbose():
            return

        # Show hero's main perspective
        print(f"{hero}: {perspective}")

        # Show sequential thinking if provided
        if reasoning:
            for i, thought in enumerate(reasoning, 1):
                category = "Analyzing" if i < len(reasoning) else "Conclusion"
                print(f"{hero}: [{category}] {thought}")

        # Show recommendation if provided
        if recommendation:
            print(f"{hero}: 💡 Recommendation: {recommendation}")

        print()

    def strategy_decision(
        self,
        leader: str,
        decision: str,
        analysis: Optional[List[str]] = None,
        next_steps: Optional[Dict[str, str]] = None
    ):
        """
        Leader announces final decision after analyzing team input

        Args:
            leader: Hero making the decision (usually Superman)
            decision: The final decision
            analysis: Optional sequential thinking leading to decision
            next_steps: Optional dict of {hero: task} assignments

        Example:
            narrator.strategy_decision(
                "🦸 Superman",
                "Using Image-to-HTML methodology",
                analysis=[
                    "Analyzing team input: 3 heroes, 2 recommendations",
                    "Oracle data: 90-95% accuracy with Image-to-HTML",
                    "Vision Analyst: Complex layout requires measurements"
                ],
                next_steps={
                    "👁️ Vision Analyst": "Extract dashboard measurements",
                    "🎨 Artemis": "Build fresh HTML/CSS from measurements",
                    "🎯 Green Arrow": "Validate visual accuracy"
                }
            )
        """
        if not self.is_verbose():
            return

        print("─" * 78)
        print(f"{leader}: DECISION")
        print("─" * 78)

        # Show sequential thinking if provided
        if analysis:
            for i, thought in enumerate(analysis, 1):
                category = "Strategizing" if i < len(analysis) else "Commanding"
                print(f"{leader}: [{category}] {thought}")
            print()

        # Show final decision
        print(f"{leader}: ✅ {decision}")
        print()

        # Show next steps if provided
        if next_steps:
            print(f"{leader}: 📋 Team Assignments:")
            for hero, task in next_steps.items():
                print(f"  • {hero}: {task}")
            print()

        print("=" * 78)
        print()

    def debate_start(
        self,
        initiator: str,
        issue: str,
        participants: List[str],
        context: Optional[Dict[str, Any]] = None
    ):
        """
        Start an inter-agent debate on a specific issue

        Args:
            initiator: Hero who raises the issue
            issue: The issue being debated
            participants: List of heroes participating in debate
            context: Optional context information

        Example:
            narrator.debate_start(
                "🦇 Batman",
                "Component has 3 CRITICAL WCAG violations",
                ["🦸 Superman", "🦇 Batman", "🎨 Artemis", "🎯 Green Arrow", "🔮 Oracle"]
            )
        """
        if not self.is_verbose():
            return

        print()
        print("🔥" * 39)
        print(f"  {initiator}: INVESTIGATION COMPLETE")
        print("🔥" * 39)
        print()
        print(f"{initiator}: {issue}")
        print()

        if context:
            print("📋 Context:")
            for key, value in context.items():
                formatted_key = key.replace("_", " ").title()
                print(f"  • {formatted_key}: {value}")
            print()

        self.conversation_log.append({
            "type": "debate_start",
            "initiator": initiator,
            "issue": issue,
            "participants": participants,
            "context": context
        })

    def debate_position(
        self,
        hero: str,
        position: str,
        reasoning: Optional[List[str]] = None,
        evidence: Optional[str] = None
    ):
        """
        Hero takes a position in the debate with sequential thinking

        Args:
            hero: Hero taking position
            position: Their position statement
            reasoning: Optional list of sequential reasoning steps
            evidence: Optional evidence supporting position

        Example:
            narrator.debate_position(
                "🦇 Batman",
                "Should we proceed knowing we'll exclude keyboard-only users?",
                reasoning=[
                    "Analyzing Figma file structure",
                    "No Focus state detected in component",
                    "WCAG 2.4.7 requires visible focus indicators"
                ],
                evidence="3 CRITICAL violations found"
            )
        """
        if not self.is_verbose():
            return

        # Show sequential thinking if provided
        if reasoning:
            for i, thought in enumerate(reasoning, 1):
                category = "Investigating" if i < len(reasoning) else "Questioning"
                self.hero_thinks(hero, thought, category=category)

        # Show position
        formatted = f"{hero}: {position}"
        if evidence:
            formatted += f" [{evidence}]"

        print(formatted)
        print()

        self.conversation_log.append({
            "type": "debate_position",
            "hero": hero,
            "position": position,
            "reasoning": reasoning,
            "evidence": evidence
        })

    def debate_question(
        self,
        from_hero: str,
        to_hero: str,
        question: str,
        concern: Optional[str] = None
    ):
        """
        Hero questions another hero in the debate

        Args:
            from_hero: Hero asking the question
            to_hero: Hero being questioned
            question: The question
            concern: Optional concern being raised

        Example:
            narrator.debate_question(
                "🦇 Batman",
                "🦸 Superman",
                "Should we proceed knowing we'll exclude keyboard-only users?",
                concern="Mission accessibility requirements"
            )
        """
        if not self.is_verbose():
            return

        formatted = f"{from_hero} → {to_hero}: {question}"
        if concern:
            formatted += f" [⚠️ {concern}]"

        print(formatted)
        print()

        self.conversation_log.append({
            "type": "debate_question",
            "from": from_hero,
            "to": to_hero,
            "question": question,
            "concern": concern
        })

    def debate_evidence(
        self,
        hero: str,
        finding: str,
        evidence_type: str = "Technical Evidence"
    ):
        """
        Hero presents evidence in the debate

        Args:
            hero: Hero presenting evidence
            finding: The evidence/finding
            evidence_type: Type of evidence (default: "Technical Evidence")

        Example:
            narrator.debate_evidence(
                "🎨 Artemis",
                "Figma file has NO Focus state - this is a design gap",
                evidence_type="Design Analysis"
            )
        """
        if not self.is_verbose():
            return

        print(f"{hero}: [{evidence_type}] {finding}")
        print()

        self.conversation_log.append({
            "type": "debate_evidence",
            "hero": hero,
            "finding": finding,
            "evidence_type": evidence_type
        })

    def debate_proposal(
        self,
        hero: str,
        proposal: str,
        approach: Optional[str] = None
    ):
        """
        Hero proposes a solution in the debate

        Args:
            hero: Hero making proposal
            proposal: The proposed solution
            approach: Optional approach description

        Example:
            narrator.debate_proposal(
                "🎯 Green Arrow",
                "Build with accessible defaults, refine with designer later",
                approach="Accessibility-first development"
            )
        """
        if not self.is_verbose():
            return

        print(f"{hero}: 💡 Proposal: {proposal}")
        if approach:
            print(f"  Approach: {approach}")
        print()

        self.conversation_log.append({
            "type": "debate_proposal",
            "hero": hero,
            "proposal": proposal,
            "approach": approach
        })

    def debate_critical_question(
        self,
        hero: str,
        question: str,
        stakes: Optional[str] = None
    ):
        """
        Hero asks a mission-critical question that reframes the debate

        Args:
            hero: Hero asking (usually Oracle)
            question: The mission-critical question
            stakes: Optional description of what's at stake

        Example:
            narrator.debate_critical_question(
                "🔮 Oracle",
                "If a student with disabilities cannot use this, have we succeeded?",
                stakes="Mission success criteria"
            )
        """
        if not self.is_verbose():
            return

        print(f"{hero}: ⚡ MISSION-CRITICAL QUESTION:")
        print(f"  \"{question}\"")
        if stakes:
            print(f"  Stakes: {stakes}")
        print()

        self.conversation_log.append({
            "type": "debate_critical_question",
            "hero": hero,
            "question": question,
            "stakes": stakes
        })

    def debate_resolution(
        self,
        leader: str,
        decision: str,
        rationale: Optional[List[str]] = None,
        team_agreement: Optional[str] = None
    ):
        """
        Leader resolves the debate with final decision

        Args:
            leader: Hero making decision (usually Superman)
            decision: The final decision
            rationale: Optional sequential thinking leading to decision
            team_agreement: Optional note about team consensus

        Example:
            narrator.debate_resolution(
                "🦸 Superman",
                "Build with accessibility enhancements NOW",
                rationale=[
                    "Analyzing team input: Batman raised valid concerns",
                    "Artemis confirmed design gap",
                    "Oracle framed mission-critical question",
                    "Green Arrow proposed practical solution"
                ],
                team_agreement="Unanimous - team aligned on accessible approach"
            )
        """
        if not self.is_verbose():
            return

        print("─" * 78)
        print(f"{leader}: DECISION")
        print("─" * 78)

        # Show sequential thinking if provided
        if rationale:
            for i, thought in enumerate(rationale, 1):
                category = "Analyzing Team Input" if i < len(rationale) else "Deciding"
                self.hero_thinks(leader, thought, category=category)
            print()

        # Show final decision
        print(f"{leader}: ✅ {decision}")
        print()

        # Show team agreement if provided
        if team_agreement:
            print(f"  Team Status: {team_agreement}")
            print()

        print("=" * 78)
        print()

        self.conversation_log.append({
            "type": "debate_resolution",
            "leader": leader,
            "decision": decision,
            "rationale": rationale,
            "team_agreement": team_agreement
        })

    def reset_step_counter(self, hero: Optional[str] = None):
        """
        Reset sequential thinking step counter

        Args:
            hero: Specific hero to reset, or None for all
        """
        if hero:
            self.step_counter[hero] = 0
        else:
            self.step_counter = {}


# Singleton instance for easy access
_global_narrator: Optional[MissionControlNarrator] = None


def get_narrator(mode: Optional[str] = None) -> MissionControlNarrator:
    """
    Get or create global narrator instance

    Args:
        mode: Narrator mode (overrides existing if provided)

    Returns:
        Global MissionControlNarrator instance
    """
    global _global_narrator

    if _global_narrator is None or mode is not None:
        # Get mode from environment if not specified
        if mode is None:
            mode = os.getenv('NARRATOR_MODE', 'narrative')

        _global_narrator = MissionControlNarrator(mode=mode)

    return _global_narrator


def reset_narrator():
    """Reset global narrator (useful for testing)"""
    global _global_narrator
    _global_narrator = None
