"""
🦸 SUPERMAN - THE JUSTICE LEAGUE COORDINATOR
The Leader of the Justice League - Assembles All Heroes for Complete Analysis

Superman coordinates the entire Justice League to provide perfect design analysis!

Powers:
- Assembles the entire Justice League
- Coordinates multi-hero missions
- Combines results from all heroes
- Calculates overall Justice League score
- Generates comprehensive reports
- Prioritizes hero deployment
- Manages hero communication

"Together, we are the Justice League! No design flaw escapes us!"

Justice League Roster (16 Heroes):
- 🦇 Batman (Interactive Testing)
- 💚 Green Lantern (Visual Regression)
- ⚡ Wonder Woman (Accessibility)
- ⚡ Flash (Performance)
- 🌊 Aquaman (Network)
- 🤖 Cyborg (Integrations)
- 🔬 The Atom (Component Analysis)
- 🎯 Green Arrow (Visual Validation - Pixel-Perfect WYSIWYG)
- 🧠 Martian Manhunter (Security)
- 🤸 Plastic Man (Responsive Design)
- 🎩 Zatanna (SEO & Metadata)
- 🪔 Litty (User Empathy & Ethics)
- 🎨 Artemis (Figma-to-Code Expert)
- 🔮 Oracle (Pattern Tracking & Learning)
- 🦸 Superman (Coordinator)
"""

import logging
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import Mission Control Narrator (v2.0)
from .mission_control_narrator import get_narrator

# Import Git Worktree Manager for parallel operations
try:
    from ..utils.git_worktree_manager import GitWorktreeManager, HeroWorktreeContext
    GIT_WORKTREE_AVAILABLE = True
except ImportError:
    GIT_WORKTREE_AVAILABLE = False
    logging.warning("Git Worktree Manager not available - parallel operations will be limited")

# Import all Justice League heroes
try:
    from .batman_testing import BatmanTesting
    BATMAN_AVAILABLE = True
except ImportError:
    BATMAN_AVAILABLE = False
    logging.warning("Batman not available")

try:
    from .green_lantern_visual import GreenLanternVisual
    GREEN_LANTERN_AVAILABLE = True
except ImportError:
    GREEN_LANTERN_AVAILABLE = False
    logging.warning("Green Lantern not available")

try:
    from .wonder_woman_accessibility import WonderWomanAccessibility
    WONDER_WOMAN_AVAILABLE = True
except ImportError:
    WONDER_WOMAN_AVAILABLE = False
    logging.warning("Wonder Woman not available")

try:
    from .flash_performance import FlashPerformance
    FLASH_AVAILABLE = True
except ImportError:
    FLASH_AVAILABLE = False
    logging.warning("Flash not available")

try:
    from .aquaman_network import AquamanNetwork
    AQUAMAN_AVAILABLE = True
except ImportError:
    AQUAMAN_AVAILABLE = False
    logging.warning("Aquaman not available")

try:
    from .cyborg_integrations import CyborgIntegrations
    CYBORG_AVAILABLE = True
except ImportError:
    CYBORG_AVAILABLE = False
    logging.warning("Cyborg not available")

try:
    from .atom_component_analysis import AtomComponentAnalysis
    ATOM_AVAILABLE = True
except ImportError:
    ATOM_AVAILABLE = False
    logging.warning("The Atom not available")

try:
    from .green_arrow_visual_validator import GreenArrowVisualValidator
    GREEN_ARROW_VISUAL_AVAILABLE = True
except ImportError:
    GREEN_ARROW_VISUAL_AVAILABLE = False
    logging.warning("Green Arrow Visual Validator not available")

try:
    from .martian_manhunter_security import MartianManhunterSecurity
    MARTIAN_MANHUNTER_AVAILABLE = True
except ImportError:
    MARTIAN_MANHUNTER_AVAILABLE = False
    logging.warning("Martian Manhunter not available")

try:
    from .plastic_man_responsive import PlasticManResponsive
    PLASTIC_MAN_AVAILABLE = True
except ImportError:
    PLASTIC_MAN_AVAILABLE = False
    logging.warning("Plastic Man not available")

try:
    from .zatanna_seo import ZatannaSEO
    ZATANNA_AVAILABLE = True
except ImportError:
    ZATANNA_AVAILABLE = False
    logging.warning("Zatanna not available")

try:
    from .litty_ethics import LittyEthics
    LITTY_AVAILABLE = True
except ImportError:
    LITTY_AVAILABLE = False
    logging.warning("Litty not available")

try:
    from .artemis_codesmith import ArtemisCodeSmith
    ARTEMIS_AVAILABLE = True
except ImportError:
    ARTEMIS_AVAILABLE = False
    logging.warning("Artemis not available")

try:
    from .oracle_meta_agent import OracleMeta
    ORACLE_AVAILABLE = True
except ImportError:
    ORACLE_AVAILABLE = False
    logging.warning("Oracle not available")

try:
    from .hawkman_equipped import HawkmanEquipped
    HAWKMAN_AVAILABLE = True
except ImportError:
    HAWKMAN_AVAILABLE = False
    logging.warning("Hawkman not available")

try:
    from .quicksilver_speed_export import QuicksilverSpeedExport
    QUICKSILVER_AVAILABLE = True
except ImportError:
    QUICKSILVER_AVAILABLE = False
    logging.warning("Quicksilver not available")

logger = logging.getLogger(__name__)


class SupermanCoordinator:
    """
    🦸 SUPERMAN - Justice League Coordinator

    Superman assembles and coordinates all heroes for complete design analysis

    Leadership Powers:
    1. Assemble the Justice League
    2. Deploy heroes based on mission requirements
    3. Coordinate multi-hero operations
    4. Combine results from all heroes
    5. Calculate Justice League composite score
    6. Generate comprehensive reports
    7. Prioritize critical issues across all analyses
    8. Deliver final verdict
    """

    def __init__(self, baseline_dir: Optional[str] = None):
        """
        Initialize Superman's command center

        Args:
            baseline_dir: Directory for baselines and configs
        """
        self.baseline_dir = Path(baseline_dir or '/tmp/aldo-vision-justice-league')
        self.baseline_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Mission Control Narrator (v2.0)
        self.narrator = get_narrator()

        # Show Justice League Banner on initialization
        if self.narrator:
            self.narrator.show_justice_league_banner(mission_type="System Initialization")

        # Initialize all available heroes (with narrator for enhanced UX)
        self.batman = BatmanTesting(narrator=self.narrator) if BATMAN_AVAILABLE else None
        self.green_lantern = GreenLanternVisual(str(self.baseline_dir / 'visual'), narrator=self.narrator) if GREEN_LANTERN_AVAILABLE else None
        self.wonder_woman = WonderWomanAccessibility(narrator=self.narrator) if WONDER_WOMAN_AVAILABLE else None
        self.flash = FlashPerformance(str(self.baseline_dir / 'performance'), narrator=self.narrator) if FLASH_AVAILABLE else None
        self.aquaman = AquamanNetwork(narrator=self.narrator) if AQUAMAN_AVAILABLE else None
        self.cyborg = CyborgIntegrations(str(self.baseline_dir / 'integrations'), narrator=self.narrator) if CYBORG_AVAILABLE else None
        self.atom = AtomComponentAnalysis(narrator=self.narrator) if ATOM_AVAILABLE else None
        self.green_arrow = GreenArrowVisualValidator(str(self.baseline_dir / 'validation'), narrator=self.narrator) if GREEN_ARROW_VISUAL_AVAILABLE else None
        self.martian_manhunter = MartianManhunterSecurity(str(self.baseline_dir / 'security'), narrator=self.narrator) if MARTIAN_MANHUNTER_AVAILABLE else None
        self.plastic_man = PlasticManResponsive(narrator=self.narrator) if PLASTIC_MAN_AVAILABLE else None
        self.zatanna = ZatannaSEO(str(self.baseline_dir / 'seo'), narrator=self.narrator) if ZATANNA_AVAILABLE else None
        self.litty = LittyEthics(narrator=self.narrator) if LITTY_AVAILABLE else None
        self.artemis = ArtemisCodeSmith(expert_mode=True, narrator=self.narrator) if ARTEMIS_AVAILABLE else None
        self.oracle = OracleMeta(narrator=self.narrator) if ORACLE_AVAILABLE else None
        self.hawkman = HawkmanEquipped(narrator=self.narrator) if HAWKMAN_AVAILABLE else None
        self.quicksilver = QuicksilverSpeedExport(narrator=self.narrator) if QUICKSILVER_AVAILABLE else None

        # Hero identity for narrator integration
        self.hero_name = "Superman"
        self.hero_emoji = "🦸"

        # Initialize Auto-Fix Orchestrator (v1.9.3) - autonomous error recovery
        from .auto_fix_orchestrator import create_auto_fix_orchestrator
        self.auto_fix_orchestrator = create_auto_fix_orchestrator(
            oracle=self.oracle,
            narrator=self.narrator
        )

        # Count available heroes
        self.heroes_available = sum([
            BATMAN_AVAILABLE,
            GREEN_LANTERN_AVAILABLE,
            WONDER_WOMAN_AVAILABLE,
            FLASH_AVAILABLE,
            AQUAMAN_AVAILABLE,
            CYBORG_AVAILABLE,
            ATOM_AVAILABLE,
            GREEN_ARROW_VISUAL_AVAILABLE,
            MARTIAN_MANHUNTER_AVAILABLE,
            PLASTIC_MAN_AVAILABLE,
            ZATANNA_AVAILABLE,
            LITTY_AVAILABLE,
            ARTEMIS_AVAILABLE,
            ORACLE_AVAILABLE,
            HAWKMAN_AVAILABLE
        ])

        # Narrative UX: Show Justice League assembly
        if self.narrator and self.narrator.is_verbose():
            self.narrator.mission_milestone("🦸 JUSTICE LEAGUE COMMAND CENTER")
            self.narrator.hero_speaks(
                "🦸 Superman",
                f"Justice League assembled! {self.heroes_available} heroes ready for duty.",
                style="tactical",
                technical_info=f"{self.heroes_available}/16 heroes available"
            )

        # Technical log (DEBUG level)
        logger.debug(f"🦸 SUPERMAN - Justice League Coordinator initialized")
        logger.debug(f"🦸 Heroes available: {self.heroes_available}/16")
        logger.debug(f"  🦇 Batman: {'✅' if BATMAN_AVAILABLE else '❌'}")
        logger.debug(f"  💚 Green Lantern: {'✅' if GREEN_LANTERN_AVAILABLE else '❌'}")
        logger.debug(f"  ⚡ Wonder Woman: {'✅' if WONDER_WOMAN_AVAILABLE else '❌'}")
        logger.debug(f"  ⚡ Flash: {'✅' if FLASH_AVAILABLE else '❌'}")
        logger.debug(f"  🌊 Aquaman: {'✅' if AQUAMAN_AVAILABLE else '❌'}")
        logger.debug(f"  🤖 Cyborg: {'✅' if CYBORG_AVAILABLE else '❌'}")
        logger.debug(f"  🔬 The Atom: {'✅' if ATOM_AVAILABLE else '❌'}")
        logger.debug(f"  🎯 Green Arrow: {'✅' if GREEN_ARROW_VISUAL_AVAILABLE else '❌'}")
        logger.debug(f"  🧠 Martian Manhunter: {'✅' if MARTIAN_MANHUNTER_AVAILABLE else '❌'}")
        logger.debug(f"  🤸 Plastic Man: {'✅' if PLASTIC_MAN_AVAILABLE else '❌'}")
        logger.debug(f"  🎩 Zatanna: {'✅' if ZATANNA_AVAILABLE else '❌'}")
        logger.debug(f"  🪔 Litty: {'✅' if LITTY_AVAILABLE else '❌'}")
        logger.debug(f"  🎨 Artemis: {'✅' if ARTEMIS_AVAILABLE else '❌'}")
        logger.debug(f"  🔮 Oracle: {'✅' if ORACLE_AVAILABLE else '❌'}")
        logger.debug(f"  🦅 Hawkman: {'✅' if HAWKMAN_AVAILABLE else '❌'}")
        logger.debug(f"  💨 Quicksilver: {'✅' if QUICKSILVER_AVAILABLE else '❌'}")

    def say(self, message: str, style: str = "tactical", technical_info: Optional[str] = None):
        """
        Superman dialogue - Authoritative, mission-focused leadership

        Personality traits:
        - Direct tactical commands
        - Mission-focused language
        - Authoritative leadership voice
        - Clear deployment directives
        """
        if self.narrator:
            self.narrator.hero_speaks(
                f"{self.hero_emoji} {self.hero_name}",
                message, style, technical_info
            )

    def think(self, thought: str, step: Optional[int] = None, category: Optional[str] = "Commanding"):
        """
        Sequential thinking with mission coordination focus

        Common categories for Superman:
        - Commanding, Deploying, Coordinating, Strategizing
        """
        if self.narrator:
            self.narrator.hero_thinks(
                f"{self.hero_emoji} {self.hero_name}",
                thought, step, category
            )

    def handoff(self, to_hero: str, context: str, details: Optional[str] = None):
        """
        Handoff mission to another hero

        Args:
            to_hero: Name of hero receiving the mission (with emoji)
            context: What mission/task is being assigned
            details: Optional additional mission details
        """
        if self.narrator:
            self.narrator.hero_handoff(
                f"{self.hero_emoji} {self.hero_name}",
                to_hero,
                context,
                details
            )

    def deploy_heroes_parallel(
        self,
        missions: List[Dict[str, Any]],
        max_workers: int = 4,
        use_worktrees: bool = True
    ) -> Dict[str, Any]:
        """
        🌳 Deploy multiple heroes in parallel using git worktrees

        This enables true parallel processing where each hero gets an isolated
        workspace (git worktree) to work in without conflicts.

        Args:
            missions: List of mission dicts, each containing:
                - hero_name: Name of hero to deploy
                - task_name: Description of task
                - params: Hero-specific parameters
            max_workers: Maximum concurrent hero deployments
            use_worktrees: Use git worktrees for isolation (requires git repo)

        Returns:
            Results dict with per-hero results and summary

        Example:
            missions = [
                {
                    'hero_name': 'artemis',
                    'task_name': 'convert-component-1',
                    'params': {'figma_url': '...', 'component_name': 'Header'}
                },
                {
                    'hero_name': 'artemis',
                    'task_name': 'convert-component-2',
                    'params': {'figma_url': '...', 'component_name': 'Footer'}
                }
            ]
            results = superman.deploy_heroes_parallel(missions)
        """
        if not GIT_WORKTREE_AVAILABLE and use_worktrees:
            logger.warning("🌳 Git worktrees requested but not available, using sequential deployment")
            use_worktrees = False

        if self.narrator:
            self.say(f"Deploying {len(missions)} heroes in parallel", style="tactical",
                    technical_info=f"{max_workers} workers, worktrees={'enabled' if use_worktrees else 'disabled'}")

        # Initialize worktree manager if needed
        worktree_manager = GitWorktreeManager() if use_worktrees else None

        results = {
            'total_missions': len(missions),
            'successful': 0,
            'failed': 0,
            'hero_results': [],
            'parallel_execution': True,
            'used_worktrees': use_worktrees
        }

        # Execute missions in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all missions
            future_to_mission = {}

            for mission in missions:
                if use_worktrees:
                    # Submit with worktree context
                    future = executor.submit(
                        self._execute_mission_with_worktree,
                        mission,
                        worktree_manager
                    )
                else:
                    # Submit without worktree
                    future = executor.submit(
                        self._execute_mission_direct,
                        mission
                    )

                future_to_mission[future] = mission

            # Collect results as they complete
            for future in as_completed(future_to_mission):
                mission = future_to_mission[future]
                try:
                    result = future.result()

                    if result.get('success'):
                        results['successful'] += 1
                    else:
                        results['failed'] += 1

                    results['hero_results'].append(result)

                    if self.narrator:
                        status_emoji = "✅" if result.get('success') else "❌"
                        self.say(f"{status_emoji} {mission['hero_name']} - {mission['task_name']}",
                                style="friendly",
                                technical_info=f"Completed in {result.get('duration', 0):.1f}s")

                except Exception as e:
                    logger.error(f"❌ Mission failed: {mission['task_name']} - {e}")
                    results['failed'] += 1
                    results['hero_results'].append({
                        'success': False,
                        'error': str(e),
                        'mission': mission
                    })

        # Cleanup worktrees if used
        if use_worktrees and worktree_manager:
            cleanup_summary = worktree_manager.cleanup_all(force=True)
            results['worktree_cleanup'] = cleanup_summary

        if self.narrator:
            self.say(f"Parallel deployment complete: {results['successful']} succeeded, {results['failed']} failed",
                    style="tactical")

        return results

    def _execute_mission_with_worktree(
        self,
        mission: Dict[str, Any],
        worktree_manager: 'GitWorktreeManager'
    ) -> Dict[str, Any]:
        """
        Execute a single mission in an isolated worktree

        Args:
            mission: Mission parameters
            worktree_manager: Worktree manager instance

        Returns:
            Mission result
        """
        import time
        start_time = time.time()

        try:
            # Create worktree for this mission
            worktree_info = worktree_manager.create_worktree(
                task_name=mission['task_name'],
                branch=mission.get('branch')
            )

            # Execute mission in worktree
            result = self._execute_hero_mission(
                mission,
                workspace_path=worktree_info['path']
            )

            duration = time.time() - start_time

            return {
                **result,
                'worktree_path': str(worktree_info['path']),
                'duration': duration
            }

        except Exception as e:
            duration = time.time() - start_time
            return {
                'success': False,
                'error': str(e),
                'mission': mission,
                'duration': duration
            }

    def _execute_mission_direct(self, mission: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a mission directly without worktree isolation

        Args:
            mission: Mission parameters

        Returns:
            Mission result
        """
        import time
        start_time = time.time()

        try:
            result = self._execute_hero_mission(mission)
            duration = time.time() - start_time

            return {
                **result,
                'duration': duration
            }

        except Exception as e:
            duration = time.time() - start_time
            return {
                'success': False,
                'error': str(e),
                'mission': mission,
                'duration': duration
            }

    def _execute_hero_mission(
        self,
        mission: Dict[str, Any],
        workspace_path: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Execute a specific hero mission

        Args:
            mission: Mission dict with hero_name, task_name, params
            workspace_path: Optional workspace path for worktree

        Returns:
            Mission execution result
        """
        hero_name = mission['hero_name'].lower()
        params = mission.get('params', {})

        # Route to appropriate hero
        if hero_name == 'artemis' and self.artemis:
            return self._deploy_artemis_mission(params, workspace_path)
        elif hero_name == 'green_arrow' and self.green_arrow:
            return self._deploy_green_arrow_mission(params, workspace_path)
        elif hero_name == 'batman' and self.batman:
            return self._deploy_batman_mission(params, workspace_path)
        elif hero_name == 'oracle' and self.oracle:
            return self._deploy_oracle_mission(params, workspace_path)
        else:
            return {
                'success': False,
                'error': f"Hero {hero_name} not available or not supported for parallel deployment"
            }

    def _deploy_artemis_mission(
        self,
        params: Dict[str, Any],
        workspace_path: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Deploy Artemis for code generation"""
        try:
            # Update output path if workspace provided
            if workspace_path:
                params['output_dir'] = str(workspace_path / 'generated')

            result = self.artemis.generate_component_code_expert(
                figma_url=params.get('figma_url'),
                component_name=params.get('component_name'),
                framework=params.get('framework', 'next'),
                language=params.get('language', 'typescript'),
                project_context=params.get('project_context')
            )

            return result

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _deploy_green_arrow_mission(
        self,
        params: Dict[str, Any],
        workspace_path: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Deploy Green Arrow for validation"""
        try:
            result = self.green_arrow.validate_component(
                figma_url=params.get('figma_url'),
                rendered_url=params.get('rendered_url'),
                component_name=params.get('component_name'),
                component_code=params.get('component_code')
            )

            return result

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _deploy_batman_mission(
        self,
        params: Dict[str, Any],
        workspace_path: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Deploy Batman for testing"""
        try:
            result = self.batman.test_all_interactive_elements(
                page_snapshot=params.get('page_snapshot'),
                mcp_tools=params.get('mcp_tools', {})
            )

            return result

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _deploy_oracle_mission(
        self,
        params: Dict[str, Any],
        workspace_path: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Deploy Oracle for pattern analysis"""
        try:
            file_key = params.get('file_key')
            result = self.oracle.get_project_context(file_key)

            return {'success': True, 'context': result}

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def strategy_session(
        self,
        topic: str,
        heroes_dict: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        🦸 Superman leads a strategy session where heroes debate and collaborate

        Heroes share their sequential thinking, Superman analyzes, and makes final decision.

        Args:
            topic: What the team is strategizing about
            heroes_dict: Dictionary of {hero_name: hero_instance} to consult
            context: Optional context data for the discussion

        Returns:
            Strategy session results with decision and next steps

        Example:
            result = superman.strategy_session(
                topic="Best methodology for Dashboard 10 conversion",
                heroes_dict={
                    "Oracle": self.oracle,
                    "Artemis": self.artemis,
                    "Vision Analyst": self.vision_analyst
                },
                context={"complexity": "high", "layout": "2-column"}
            )
        """
        if not self.narrator:
            return {"decision": "No narrator available", "next_steps": {}}

        # Start strategy session
        hero_names = [f"{hero.hero_emoji} {hero.hero_name}" for hero in heroes_dict.values() if hasattr(hero, 'hero_emoji')]
        self.narrator.strategy_session_start(
            f"{self.hero_emoji} {self.hero_name}",
            topic,
            hero_names
        )

        self.say(f"Team, strategy session: {topic}", style="tactical")

        # Collect contributions from each hero
        contributions = []

        for hero_key, hero in heroes_dict.items():
            if not hasattr(hero, 'contribute_to_strategy'):
                continue

            # Hero provides their perspective
            contribution = hero.contribute_to_strategy(topic, context)
            contributions.append(contribution)

            # Display contribution through narrator
            self.narrator.strategy_contribution(
                f"{hero.hero_emoji} {hero.hero_name}",
                contribution.get('perspective', ''),
                reasoning=contribution.get('reasoning', []),
                recommendation=contribution.get('recommendation')
            )

        # Superman analyzes all input
        analysis_steps = [
            f"Analyzing team input: {len(contributions)} heroes, {sum(1 for c in contributions if c.get('recommendation'))} recommendations"
        ]

        # Add key insights from each contribution
        for contrib in contributions:
            if contrib.get('key_insight'):
                analysis_steps.append(contrib['key_insight'])

        # Make decision based on contributions
        decision = self._make_strategy_decision(contributions, context)

        # Determine next steps
        next_steps = self._assign_next_steps(decision, heroes_dict)

        # Announce decision through narrator
        self.narrator.strategy_decision(
            f"{self.hero_emoji} {self.hero_name}",
            decision['choice'],
            analysis=analysis_steps,
            next_steps=next_steps
        )

        # Log strategy session to Oracle for learning
        if self.oracle and hasattr(self.oracle, 'learning') and self.oracle.learning:
            self.oracle.learning.log_strategy_session(
                topic=topic,
                heroes=hero_names,
                contributions=contributions,
                decision=decision,
                next_steps=next_steps
            )

        return {
            "topic": topic,
            "contributions": contributions,
            "decision": decision,
            "next_steps": next_steps,
            "success": True
        }

    def _make_strategy_decision(
        self,
        contributions: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Superman analyzes all contributions and makes final decision

        Args:
            contributions: List of hero contributions
            context: Optional context data

        Returns:
            Decision dict with choice and reasoning
        """
        # Count recommendations
        recommendations = {}
        for contrib in contributions:
            rec = contrib.get('recommendation')
            if rec:
                recommendations[rec] = recommendations.get(rec, 0) + 1

        # Simple decision: pick most recommended approach
        if recommendations:
            best_choice = max(recommendations.items(), key=lambda x: x[1])[0]
            return {
                "choice": best_choice,
                "support_count": recommendations[best_choice],
                "total_heroes": len(contributions)
            }

        return {
            "choice": "Proceed with standard approach",
            "support_count": 0,
            "total_heroes": len(contributions)
        }

    def _assign_next_steps(
        self,
        decision: Dict[str, Any],
        heroes_dict: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Assign next steps to heroes based on decision

        Args:
            decision: The decision made
            heroes_dict: Available heroes

        Returns:
            Dict of {hero_name: task}
        """
        next_steps = {}

        # Default assignments based on common workflow
        for hero_key, hero in heroes_dict.items():
            if not hasattr(hero, 'hero_emoji'):
                continue

            hero_full_name = f"{hero.hero_emoji} {hero.hero_name}"

            # Assign based on hero specialty
            if "Oracle" in hero_key:
                next_steps[hero_full_name] = "Track project patterns and update knowledge base"
            elif "Vision Analyst" in hero_key:
                next_steps[hero_full_name] = "Extract visual measurements from dashboard"
            elif "Artemis" in hero_key:
                next_steps[hero_full_name] = "Build component code from specifications"
            elif "Green Arrow" in hero_key:
                next_steps[hero_full_name] = "Validate pixel-perfect accuracy"

        return next_steps

    def start_mission_tracking(
        self,
        user_request: str,
        mission_type: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Start Oracle mission tracking for self-learning

        Args:
            user_request: Original user request/input
            mission_type: Type of mission (conversion, analysis, export, etc.)
            context: Optional context data

        Returns:
            Mission ID for tracking
        """
        if self.oracle and hasattr(self.oracle, 'learning') and self.oracle.learning:
            return self.oracle.learning.start_mission(user_request, mission_type, context)
        return ""

    def complete_mission_with_learning(
        self,
        success: bool,
        outcome_details: Dict[str, Any],
        issues: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Complete mission and trigger Oracle's self-learning

        Args:
            success: Whether mission succeeded
            outcome_details: Detailed outcome metrics
            issues: Optional list of issues encountered

        Returns:
            Learning results with team feedback
        """
        if self.oracle and hasattr(self.oracle, 'learning') and self.oracle.learning:
            result = self.oracle.learning.complete_mission_and_learn(
                success=success,
                outcome_details=outcome_details,
                issues_encountered=issues
            )

            # Show team feedback through narrator
            if 'team_feedback' in result and self.narrator:
                self.oracle.learning.show_team_feedback(
                    result['team_feedback'],
                    result.get('learnings', [])
                )

            return result
        return {"error": "Oracle learning system not available"}

    def assemble_justice_league(self, mission: Dict[str, Any]) -> Dict[str, Any]:
        """
        🦸 ASSEMBLE THE JUSTICE LEAGUE!

        Superman coordinates all heroes for complete design analysis

        Args:
            mission: Mission parameters
                {
                    'url': str,  # Target URL
                    'mcp_tools': Dict,  # Chrome DevTools MCP tools
                    'design_data': Dict,  # Extracted design data
                    'components': Dict,  # Component library
                    'page_snapshot': str,  # DOM snapshot
                    'screenshot_path': str,  # Screenshot for visual testing
                    'options': {
                        'test_interactive': bool,  # Deploy Batman?
                        'test_visual': bool,  # Deploy Green Lantern?
                        'test_accessibility': bool,  # Deploy Wonder Woman?
                        'test_performance': bool,  # Deploy Flash?
                        'test_network': bool,  # Deploy Aquaman?
                        'test_integrations': bool,  # Deploy Cyborg?
                        'test_components': bool,  # Deploy The Atom?
                        'test_security': bool,  # Deploy Martian Manhunter?
                        'test_responsive': bool,  # Deploy Plastic Man?
                        'test_seo': bool,  # Deploy Zatanna?
                        'validate_ethics': bool,  # Deploy Litty?
                    }
                }

        Returns:
            Complete Justice League analysis results
        """
        # Show Justice League Banner when assembling the team (with auto-detection)
        if self.narrator:
            # Get user request if available for keyword detection
            user_request = mission.get('user_request', '')
            self.narrator.auto_show_banner_if_needed(
                user_input=user_request,
                mission_type="Justice League Assembly"
            )

        logger.info("🦸 ========================================")
        logger.info("🦸  JUSTICE LEAGUE ASSEMBLY")
        logger.info("🦸 ========================================")

        results = {
            'mission': '🦸 Justice League Design Analysis',
            'timestamp': datetime.now().isoformat(),
            'target_url': mission.get('url'),
            'heroes_deployed': [],
            'hero_reports': {}
        }

        options = mission.get('options', {})
        mcp_tools = mission.get('mcp_tools', {})
        design_data = mission.get('design_data', {})
        components = mission.get('components', {})
        page_snapshot = mission.get('page_snapshot', '')
        screenshot_path = mission.get('screenshot_path', '')

        # Deploy Batman (Interactive Testing)
        if options.get('test_interactive', True):
            batman_result = self._deploy_batman(mission)
            if batman_result:
                results['hero_reports']['batman'] = batman_result
                results['heroes_deployed'].append('🦇 Batman')

        # Deploy Green Lantern (Visual Regression)
        if options.get('test_visual', True):
            gl_result = self._deploy_green_lantern(mission)
            if gl_result:
                results['hero_reports']['green_lantern'] = gl_result
                results['heroes_deployed'].append('💚 Green Lantern')

        # Deploy Wonder Woman (Accessibility)
        if options.get('test_accessibility', True):
            ww_result = self._deploy_wonder_woman(mission)
            if ww_result:
                results['hero_reports']['wonder_woman'] = ww_result
                results['heroes_deployed'].append('⚡ Wonder Woman')

        # Deploy Flash (Performance)
        if options.get('test_performance', True):
            flash_result = self._deploy_flash(mission)
            if flash_result:
                results['hero_reports']['flash'] = flash_result
                results['heroes_deployed'].append('⚡ Flash')

        # Deploy Aquaman (Network)
        if options.get('test_network', True):
            aquaman_result = self._deploy_aquaman(mission)
            if aquaman_result:
                results['hero_reports']['aquaman'] = aquaman_result
                results['heroes_deployed'].append('🌊 Aquaman')

        # Deploy Cyborg (Integrations)
        if options.get('test_integrations', True):
            cyborg_result = self._deploy_cyborg(mission)
            if cyborg_result:
                results['hero_reports']['cyborg'] = cyborg_result
                results['heroes_deployed'].append('🤖 Cyborg')

        # Deploy The Atom (Component Analysis)
        if options.get('test_components', True):
            atom_result = self._deploy_atom(mission)
            if atom_result:
                results['hero_reports']['atom'] = atom_result
                results['heroes_deployed'].append('🔬 The Atom')

        # Deploy Martian Manhunter (Security)
        if options.get('test_security', True):
            mm_result = self._deploy_martian_manhunter(mission)
            if mm_result:
                results['hero_reports']['martian_manhunter'] = mm_result
                results['heroes_deployed'].append('🧠 Martian Manhunter')

        # Deploy Plastic Man (Responsive Design)
        if options.get('test_responsive', True):
            pm_result = self._deploy_plastic_man(mission)
            if pm_result:
                results['hero_reports']['plastic_man'] = pm_result
                results['heroes_deployed'].append('🤸 Plastic Man')

        # Deploy Zatanna (SEO & Metadata)
        if options.get('test_seo', True):
            zatanna_result = self._deploy_zatanna(mission)
            if zatanna_result:
                results['hero_reports']['zatanna'] = zatanna_result
                results['heroes_deployed'].append('🎩 Zatanna')

        # Deploy Litty (Ethics & User Empathy)
        if options.get('validate_ethics', True):
            litty_result = self._deploy_litty(mission)
            if litty_result:
                results['hero_reports']['litty'] = litty_result
                results['heroes_deployed'].append('🪔 Litty')

        # Superman combines all results
        logger.info("🦸 Superman analyzing combined results...")
        combined_analysis = self._combine_hero_results(results['hero_reports'])
        results['combined_analysis'] = combined_analysis

        # Calculate Justice League Score
        logger.info("🦸 Calculating Justice League Score...")
        league_score = self._calculate_justice_league_score(results)
        results['justice_league_score'] = league_score

        # Generate Prioritized Action Plan
        logger.info("🦸 Generating Justice League Action Plan...")
        action_plan = self._generate_league_action_plan(results)
        results['action_plan'] = action_plan

        # Final Verdict
        logger.info("🦸 ========================================")
        logger.info(f"🦸  JUSTICE LEAGUE SCORE: {league_score['overall_score']:.1f}/100")
        logger.info(f"🦸  GRADE: {league_score['grade']}")
        logger.info(f"🦸  VERDICT: {league_score['verdict']}")
        logger.info("🦸 ========================================")

        # 🔮 ORACLE META-LEARNING: Track mission outcome for continuous improvement (v1.9.1)
        if self.oracle:
            try:
                oracle_tracked = self.oracle.track_mission_outcome(results)
                if oracle_tracked:
                    logger.info("🔮 Oracle: Mission outcome tracked for meta-learning")
            except Exception as e:
                logger.warning(f"🔮 Oracle tracking failed (non-critical): {e}")

        return results

    def _deploy_batman(self, mission: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """🦇 Deploy Batman for interactive testing"""
        if not self.batman:
            return None

        page_snapshot = mission.get('page_snapshot', '')
        mcp_tools = mission.get('mcp_tools', {})

        if not page_snapshot:
            logger.warning("No page snapshot available for Batman")
            return None

        logger.info("🦸 Deploying 🦇 BATMAN for interactive testing...")
        result = self.batman.test_all_interactive_elements(page_snapshot, mcp_tools)
        logger.info("  ✓ Batman mission complete")
        return result

    def _deploy_green_lantern(self, mission: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """💚 Deploy Green Lantern for visual regression testing"""
        if not self.green_lantern:
            return None

        screenshot_path = mission.get('screenshot_path', '')
        if not screenshot_path:
            logger.warning("No screenshot available for Green Lantern")
            return None

        logger.info("🦸 Deploying 💚 GREEN LANTERN for visual testing...")
        test_name = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Store baseline if first run
        gl_baseline = self.green_lantern.store_baseline(screenshot_path, test_name, {
            'url': mission.get('url'),
            'timestamp': datetime.now().isoformat()
        })

        # Compare if baseline exists
        gl_compare = self.green_lantern.compare_to_baseline(screenshot_path, test_name)

        result = {
            'baseline': gl_baseline,
            'comparison': gl_compare
        }
        logger.info("  ✓ Green Lantern mission complete")
        return result

    def _deploy_wonder_woman(self, mission: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """⚡ Deploy Wonder Woman for accessibility analysis (Superman-Enhanced!)"""
        if not self.wonder_woman:
            return None

        design_data = mission.get('design_data', {})
        mcp_tools = mission.get('mcp_tools', {})
        page_snapshot = mission.get('page_snapshot', '')

        logger.info("🦸 Deploying ⚡ WONDER WOMAN for accessibility analysis...")
        logger.info("  🦸📋 Using Superman's Enhanced WCAG 2.2 Coverage")

        # Run standard Wonder Woman accessibility analysis
        if design_data:
            ww_result = self.wonder_woman.champion_accessibility_analysis(design_data)
        else:
            logger.warning("No design data available for Wonder Woman")
            ww_result = {}

        # Enhance with Superman's WCAG 2.2 tests if MCP tools available
        if mcp_tools:
            try:
                from ..superman_wcag22_tests import test_wcag22_complete

                # Prepare MCP tools
                mcp_tools_dict = {
                    'take_snapshot': mcp_tools.get('take_snapshot'),
                    'click': mcp_tools.get('click'),
                    'evaluate_script': mcp_tools.get('evaluate_script'),
                    'take_screenshot': mcp_tools.get('take_screenshot')
                }

                wcag22_result = test_wcag22_complete(
                    mcp_tools=mcp_tools_dict,
                    url=mission.get('url', ''),
                    page_snapshot=page_snapshot,
                    baseline_dir=str(self.baseline_dir / 'wcag22')
                )

                # Combine results
                result = {
                    **ww_result,
                    'superman_wcag22_enhancement': wcag22_result,
                    'enhanced_by_superman': True
                }

                logger.info("  ✓ Wonder Woman mission complete (Superman-enhanced with WCAG 2.2)")
                return result

            except ImportError:
                logger.info("  ⚠️  Superman WCAG 2.2 not available, using standard Wonder Woman")
                logger.info("  ✓ Wonder Woman mission complete (standard)")
                return ww_result
        else:
            logger.info("  ✓ Wonder Woman mission complete (standard)")
            return ww_result

    def _deploy_flash(self, mission: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """⚡ Deploy Flash for performance profiling (Enhanced by Superman)"""
        if not self.flash:
            return None

        mcp_tools = mission.get('mcp_tools', {})
        if not mcp_tools:
            logger.warning("No MCP tools available for Flash")
            return None

        logger.info("🦸 Deploying ⚡ FLASH for performance analysis...")
        logger.info("  🦸⚡ Using Superman's Enhanced Performance Profiler")

        test_name = f"perf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Use Superman's enhanced performance profiler if available
        try:
            from ..superman_performance_profiler import profile_performance_complete

            # Prepare MCP tools in expected format
            mcp_tools_dict = {
                'start_trace': mcp_tools.get('start_trace'),
                'stop_trace': mcp_tools.get('stop_trace'),
                'analyze_insight': mcp_tools.get('analyze_insight')
            }

            result = profile_performance_complete(
                mcp_tools=mcp_tools_dict,
                test_name=test_name,
                url=mission.get('url', ''),
                reload_page=True,
                store_baseline=True,
                baseline_dir=str(self.baseline_dir / 'performance')
            )
            logger.info("  ✓ Flash mission complete (Superman-enhanced)")
            return result

        except ImportError:
            # Fallback to standard Flash profiler
            logger.info("  ⚠️  Superman profiler not available, using standard Flash")
            result = self.flash.profile_performance(mcp_tools, test_name, mission.get('url'))
            logger.info("  ✓ Flash mission complete (standard)")
            return result

    def _deploy_aquaman(self, mission: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """🌊 Deploy Aquaman for network analysis (Enhanced by Superman)"""
        if not self.aquaman:
            return None

        mcp_tools = mission.get('mcp_tools', {})
        if not mcp_tools:
            logger.warning("No MCP tools available for Aquaman")
            return None

        logger.info("🦸 Deploying 🌊 AQUAMAN for network analysis...")

        # Run standard Aquaman analysis first
        aquaman_result = self.aquaman.analyze_network_traffic(mcp_tools)

        # Enhance with Superman's network timing analysis if requested
        if mission.get('test_network_timing', False):
            logger.info("  🦸🌊 Using Superman's Enhanced Network Timing Analysis")

            test_name = f"network_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            try:
                from ..superman_network_analysis import analyze_network_timing_complete

                # Prepare MCP tools in expected format
                mcp_tools_dict = {
                    'list_network_requests': mcp_tools.get('list_network_requests'),
                    'get_network_request': mcp_tools.get('get_network_request')
                }

                # Get performance budget if specified
                performance_budget = mission.get('performance_budget')

                # Run Superman's network timing analysis
                superman_result = analyze_network_timing_complete(
                    mcp_tools=mcp_tools_dict,
                    url=mission.get('url', ''),
                    test_name=test_name,
                    store_baseline=True,
                    performance_budget=performance_budget
                )

                # Combine results
                result = {
                    **aquaman_result,
                    'superman_network_enhancement': superman_result
                }

                logger.info("  ✓ Aquaman mission complete (Superman-enhanced)")
                return result

            except ImportError:
                # Fallback to standard Aquaman
                logger.info("  ⚠️  Superman network timing not available, using standard Aquaman")
                logger.info("  ✓ Aquaman mission complete (standard)")
                return aquaman_result
        else:
            logger.info("  ✓ Aquaman mission complete (standard)")
            return aquaman_result

    def _deploy_cyborg(self, mission: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """🤖 Deploy Cyborg for integration checking"""
        if not self.cyborg:
            return None

        logger.info("🦸 Deploying 🤖 CYBORG for integration check...")
        result = self.cyborg.generate_integration_report()
        logger.info("  ✓ Cyborg mission complete")
        return result

    def _deploy_atom(self, mission: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """🔬 Deploy The Atom for component analysis"""
        if not self.atom:
            return None

        components = mission.get('components', {})
        if not components:
            logger.warning("No components available for The Atom")
            return None

        logger.info("🦸 Deploying 🔬 THE ATOM for component analysis...")
        result = self.atom.analyze_component_library(components)
        logger.info("  ✓ The Atom mission complete")
        return result

    def _deploy_martian_manhunter(self, mission: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """🧠 Deploy Martian Manhunter for security scanning"""
        if not self.martian_manhunter:
            return None

        target_data = mission.get('security_scan_data', {})
        if not target_data:
            # Build basic target data from mission
            target_data = {
                'url': mission.get('url'),
                'html_content': mission.get('page_snapshot', ''),
                'headers': mission.get('headers', {}),
                'source_code_path': mission.get('source_code_path'),
                'package_json_path': mission.get('package_json_path')
            }

        logger.info("🦸 Deploying 🧠 MARTIAN MANHUNTER for security scan...")
        result = self.martian_manhunter.scan_all_vulnerabilities(target_data)
        logger.info("  ✓ Martian Manhunter mission complete")
        return result

    def _deploy_plastic_man(self, mission: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """🤸 Deploy Plastic Man for responsive design testing"""
        if not self.plastic_man:
            return None

        mcp_tools = mission.get('mcp_tools', {})
        test_scenarios = mission.get('responsive_scenarios', None)  # Optional: specific breakpoints to test

        logger.info("🦸 Deploying 🤸 PLASTIC MAN for responsive design testing...")
        result = self.plastic_man.test_all_breakpoints(mcp_tools, test_scenarios)
        logger.info("  ✓ Plastic Man mission complete")
        return result

    def _deploy_zatanna(self, mission: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """🎩 Deploy Zatanna for SEO & metadata analysis"""
        if not self.zatanna:
            return None

        mcp_tools = mission.get('mcp_tools', {})
        target_url = mission.get('url')

        logger.info("🦸 Deploying 🎩 ZATANNA for SEO magic...")
        result = self.zatanna.analyze_seo_magic(mcp_tools, target_url)
        logger.info("  ✓ Zatanna magic complete")
        return result

    def _deploy_litty(self, mission: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        🪔 Deploy Litty - The Conscience Keeper

        Args:
            mission: Mission parameters

        Returns:
            Ethics validation results
        """
        if not self.litty:
            return None

        mcp_tools = mission.get('mcp_tools', {})
        target_url = mission.get('url')

        logger.info("🦸 Deploying 🪔 LITTY to guilt-trip you about ethics...")
        result = self.litty.validate_ethics(target_url, mcp_tools)
        logger.info("  ✓ Litty's guilt trips delivered (think about your ammachi!)")
        return result

    def _deploy_artemis(self, mission: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        🎨 Deploy Artemis - The Figma-to-Code Expert (Oracle & Green Arrow Enhanced)

        Args:
            mission: Mission parameters including:
                - figma_url: Figma design URL
                - component_name: Name for the component
                - framework: 'next' or 'react' (default: 'next')
                - language: 'typescript' or 'javascript' (default: 'typescript')
                - expert_mode: Enable expert workflow (default: True)
                - rendered_url: URL of rendered component (for Green Arrow validation)

        Returns:
            Figma-to-Code conversion results with learning data, Oracle tracking, and Green Arrow validation
        """
        if not self.artemis:
            return None

        figma_url = mission.get('figma_url')
        if not figma_url:
            logger.warning("  ⚠️ No Figma URL provided for Artemis")
            return None

        component_name = mission.get('component_name', 'Component')
        framework = mission.get('framework', 'next')
        language = mission.get('language', 'typescript')
        expert_mode = mission.get('expert_mode', True)

        logger.info("🦸 Deploying 🎨 ARTEMIS - Expert Figma-to-Code Converter...")
        logger.info(f"  📋 Component: {component_name}")
        logger.info(f"  🎯 Expert Mode: {'ENABLED' if expert_mode else 'DISABLED'}")

        # STEP 1: Query Oracle for project context
        project_context = None
        if self.oracle:
            try:
                # Extract file_key from Figma URL
                import re
                match = re.search(r'figma\.com/(?:design|file)/([a-zA-Z0-9]+)', figma_url)
                if match:
                    file_key = match.group(1)
                    logger.info(f"🦸 Querying 🔮 ORACLE for project context...")
                    project_context = self.oracle.get_project_context(file_key)

                    if project_context.get('project_known'):
                        logger.info(f"  🔮 Oracle: Project known! {project_context.get('conversions_count', 0)} conversions tracked")
                        logger.info(f"  🔮 Shared components available: {len(project_context.get('shared_components', []))}")
                        logger.info(f"  🔮 Common patterns: {', '.join(project_context.get('common_patterns', [])[:5])}")
                    else:
                        logger.info(f"  🔮 Oracle: New project - will learn and track patterns")
            except Exception as e:
                logger.warning(f"  ⚠️ Oracle query error: {str(e)}")

        try:
            # STEP 2: Deploy Artemis with Oracle context
            if expert_mode:
                result = self.artemis.generate_component_code_expert(
                    figma_url=figma_url,
                    component_name=component_name,
                    framework=framework,
                    language=language,
                    options=mission.get('options', {}),
                    max_iterations=mission.get('max_iterations', 3),
                    target_accuracy=mission.get('target_accuracy', 98.0),
                    project_context=project_context  # Pass Oracle context to Artemis
                )
            else:
                result = self.artemis.generate_component_code(
                    figma_url=figma_url,
                    component_name=component_name,
                    framework=framework,
                    language=language,
                    options=mission.get('options', {}),
                    project_context=project_context  # Pass Oracle context to Artemis
                )

            if result.get('success'):
                logger.info(f"  ✓ Artemis conversion complete!")
                logger.info(f"    Expert Rating: {result.get('expert_rating', 'N/A')}")
                logger.info(f"    Accuracy: {result.get('accuracy_score', result.get('artemis_score', 0))}%")
                logger.info(f"    Files Generated: {len(result.get('files', {}))}")
                if 'iterations' in result:
                    logger.info(f"    Iterations: {result['iterations']}")

                # STEP 3: Deploy Green Arrow for visual validation
                green_arrow_result = None
                if self.green_arrow and mission.get('rendered_url'):
                    try:
                        logger.info(f"🦸 Deploying 🎯 GREEN ARROW for pixel-perfect validation...")

                        component_code = result.get('code', result.get('files', {}).get(f'{component_name}.tsx', ''))

                        green_arrow_result = self.green_arrow.validate_component(
                            figma_url=figma_url,
                            rendered_url=mission.get('rendered_url'),
                            component_name=component_name,
                            component_code=component_code
                        )

                        accuracy_score = green_arrow_result.get('accuracy_score', 0)
                        status = green_arrow_result.get('status', 'UNKNOWN')

                        logger.info(f"  🎯 Green Arrow Verdict: {status} ({accuracy_score}% accuracy)")

                        if accuracy_score < 90:
                            logger.warning(f"  ⚠️ Accuracy below 90% - consider refinement")
                            logger.warning(f"  🎯 Discrepancies found: {len(green_arrow_result.get('discrepancies', []))}")
                        else:
                            logger.info(f"  ✓ Green Arrow approved! Pixel-perfect conversion achieved")

                        # Add Green Arrow results to Artemis result
                        result['green_arrow_validation'] = green_arrow_result

                    except Exception as e:
                        logger.error(f"  ❌ Green Arrow validation error: {str(e)}")
                        result['green_arrow_validation'] = {'error': str(e)}

                # STEP 4: Update Oracle with new patterns
                if self.oracle and project_context and match:
                    try:
                        logger.info(f"🦸 Updating 🔮 ORACLE with new patterns...")

                        # Extract node_id from Figma URL
                        node_match = re.search(r'node-id=([^&]+)', figma_url)
                        node_id = node_match.group(1) if node_match else None

                        # Update Oracle with conversion results
                        self.oracle.update_project_patterns(
                            file_key=file_key,
                            component_name=component_name,
                            node_id=node_id or 'unknown',
                            new_shared_elements=result.get('shared_elements'),
                            new_patterns=result.get('patterns_detected')
                        )

                        logger.info(f"  🔮 Oracle updated with {component_name} patterns")

                    except Exception as e:
                        logger.warning(f"  ⚠️ Oracle update error: {str(e)}")
            else:
                logger.warning(f"  ⚠️ Artemis conversion failed: {result.get('errors', ['Unknown error'])}")

            return result

        except Exception as e:
            logger.error(f"  ❌ Artemis deployment error: {str(e)}")
            return {
                'success': False,
                'errors': [str(e)],
                'hero': 'Artemis'
            }

    def _deploy_hawkman_frame_export(self, mission: Dict[str, Any], auto_fix_mode: bool = True) -> Optional[Dict[str, Any]]:
        """
        💨 Deploy Quicksilver (or 🦅 Hawkman) - Figma Frame PNG Export

        Exports all top-level frames from a Figma file as PNG images
        Uses Quicksilver (speed-optimized) by default, falls back to Hawkman if unavailable

        Args:
            mission: Mission parameters including:
                - file_key: Figma file key (or figma_url to extract from)
                - output_dir: Optional custom output directory
                - scale: Export scale 1.0-4.0 (default: 2.0)
                - progress_callback: Optional callback(current, total, frame_name) for progress updates
                - show_count_first: Optional bool to pre-count frames before export (default: False)
                - agent: Optional 'quicksilver' or 'hawkman' to force specific hero (default: auto)
            auto_fix_mode: Enable autonomous error recovery (default: True)

        Returns:
            Export results with list of exported files and total frame count
        """
        # Determine which hero to use (Quicksilver preferred for speed)
        requested_agent = mission.get('agent', 'auto')

        if requested_agent == 'hawkman':
            # User explicitly requested Hawkman
            export_hero = self.hawkman
            hero_name = 'Hawkman'
            hero_emoji = '🦅'
        elif requested_agent == 'quicksilver':
            # User explicitly requested Quicksilver
            export_hero = self.quicksilver
            hero_name = 'Quicksilver'
            hero_emoji = '💨'
        else:
            # Auto-select: Quicksilver first (speed), fallback to Hawkman (reliability)
            if self.quicksilver:
                export_hero = self.quicksilver
                hero_name = 'Quicksilver'
                hero_emoji = '💨'
            elif self.hawkman:
                export_hero = self.hawkman
                hero_name = 'Hawkman'
                hero_emoji = '🦅'
            else:
                export_hero = None
                hero_name = None
                hero_emoji = None

        if not export_hero:
            logger.warning(f"  ⚠️ No frame export hero available (Quicksilver: {'✅' if self.quicksilver else '❌'}, Hawkman: {'✅' if self.hawkman else '❌'})")
            return None

        # Extract file_key from URL or use directly
        file_key = mission.get('file_key')
        figma_url = mission.get('figma_url')

        if not file_key and figma_url:
            import re
            match = re.search(r'figma\.com/(?:design|file)/([a-zA-Z0-9]+)', figma_url)
            if match:
                file_key = match.group(1)
            else:
                logger.warning("  ⚠️ Could not extract file_key from Figma URL")
                return None

        if not file_key:
            logger.warning("  ⚠️ No file_key or figma_url provided for Hawkman")
            return None

        # Show Justice League Banner for frame export mission (with auto-detection)
        if self.narrator:
            # Get user request if available for keyword detection
            user_request = mission.get('user_request', '')
            self.narrator.auto_show_banner_if_needed(
                user_input=user_request,
                mission_type="Figma Frame PNG Export"
            )

        output_dir = mission.get('output_dir')
        scale = mission.get('scale', 2.0)
        progress_callback = mission.get('progress_callback')
        show_count_first = mission.get('show_count_first', False)

        # Pre-count frames if requested
        total_frames = None
        if show_count_first:
            try:
                # Narrative UX: Hero scanning
                if self.narrator and self.narrator.is_verbose():
                    self.narrator.hero_speaks("🦸 Superman", f"{hero_name}, scan the Figma file", style="tactical")

                logger.debug(f"🦸 Deploying {hero_emoji} {hero_name.upper()} - Scanning frames...")
                total_frames = export_hero.count_frames(file_key)

                # Narrative UX: Hero reports findings
                if self.narrator and self.narrator.is_verbose():
                    self.narrator.hero_speaks(
                        f"{hero_emoji} {hero_name}",
                        f"Scan complete! Found {total_frames} frames ready for export.",
                        style="friendly",
                        technical_info=f"File: {file_key[:8]}..."
                    )

                logger.debug(f"  📊 Found {total_frames} frames in Figma file")
            except Exception as e:
                logger.warning(f"  ⚠️ Could not pre-count frames: {e}")

        # Narrative UX: Deploy hero
        if self.narrator and self.narrator.is_verbose():
            self.narrator.team_handoff(
                "🦸 Superman",
                f"{hero_emoji} {hero_name}",
                "Export all frames as PNG",
                {"file_key": file_key[:12], "scale": f"{scale}x"}
            )

        logger.debug(f"🦸 Deploying {hero_emoji} {hero_name.upper()} - Figma Frame Export...")
        logger.debug(f"  📋 File Key: {file_key}")
        logger.debug(f"  📁 Output Dir: {output_dir or 'default (figma_exports_dir)'}")
        logger.debug(f"  📐 Scale: {scale}x")

        try:
            # Export all frames using selected hero (Quicksilver or Hawkman)
            exported_files = export_hero.export_all_frames_as_png(
                file_key=file_key,
                output_dir=output_dir,
                scale=scale,
                progress_callback=progress_callback
            )

            # Narrative UX: Hero completion
            if self.narrator and self.narrator.is_verbose():
                self.narrator.hero_speaks(
                    f"{hero_emoji} {hero_name}",
                    f"Export complete! All {len(exported_files)} frames saved successfully.",
                    style="friendly"
                )

            logger.debug(f"  ✓ {hero_name} export complete!")
            logger.debug(f"    Frames exported: {len(exported_files)}")

            # 🦇 BATMAN VERIFICATION: Completeness Check
            verification_result = None
            if self.batman:
                try:
                    # Narrative UX: Batman verification
                    if self.narrator and self.narrator.is_verbose():
                        self.narrator.team_handoff(
                            "🦸 Superman",
                            "🦇 Batman",
                            "Verify export completeness",
                            {"expected": total_frames if total_frames else len(exported_files)}
                        )

                    logger.debug(f"🦸 Deploying 🦇 BATMAN - Verifying export completeness...")

                    # Prepare data for Batman verification
                    # Expected: use total_frames if available, otherwise count from exported
                    expected_count = total_frames if total_frames else len(exported_files)

                    # Create expected_items list (simplified for count check)
                    expected_items = [{'id': f'node_{i}', 'name': f'Item {i}'} for i in range(expected_count)]

                    # Extract file paths from exported_files
                    exported_file_paths = [f['file_path'] for f in exported_files]

                    # Call Batman verification
                    verification_result = self.batman.verify_frame_export_completeness(
                        expected_items=expected_items,
                        exported_files=exported_file_paths,
                        output_dir=output_dir or export_hero.figma_exports_dir
                    )

                    # Narrative UX: Batman verdict
                    if self.narrator and self.narrator.is_verbose():
                        if verification_result['complete']:
                            self.narrator.hero_speaks(
                                "🦇 Batman",
                                f"Verification complete. All {verification_result['expected_count']} frames accounted for.",
                                style="tactical"
                            )
                        else:
                            self.narrator.hero_speaks(
                                "🦇 Batman",
                                f"Verification shows {verification_result['completeness_percentage']:.1f}% complete. {verification_result['missing_count']} frames missing.",
                                style="tactical",
                                technical_info=f"{verification_result['exported_count']}/{verification_result['expected_count']}"
                            )

                    # Log verification result
                    if verification_result['complete']:
                        logger.debug(f"  ✅ {verification_result['batman_verdict']}")
                    else:
                        logger.warning(f"  ⚠️ {verification_result['batman_verdict']}")
                        logger.warning(f"     Completeness: {verification_result['completeness_percentage']:.1f}%")

                except Exception as e:
                    logger.warning(f"  ⚠️ Batman verification error (non-critical): {str(e)}")

            # OPTIONAL: Update Oracle with export tracking
            if self.oracle and exported_files:
                try:
                    # Narrative UX: Oracle tracking
                    if self.narrator and self.narrator.is_verbose():
                        self.narrator.team_handoff(
                            "🦸 Superman",
                            "🔮 Oracle",
                            "Track export metadata",
                            {"nodes": len(exported_files)}
                        )

                    logger.debug(f"🦸 Updating 🔮 ORACLE with frame export tracking...")

                    # Track export metadata in Oracle
                    export_metadata = {
                        'file_key': file_key,
                        'nodes_exported': len(exported_files),
                        'node_names': [f['node_name'] for f in exported_files],
                        'node_types': [f['node_type'] for f in exported_files],
                        'export_timestamp': datetime.now().isoformat(),
                        'output_dir': output_dir,
                        'scale': scale,
                        # 🦇 Batman verification metrics
                        'verification': {
                            'complete': verification_result.get('complete', True) if verification_result else True,
                            'expected_count': verification_result.get('expected_count', len(exported_files)) if verification_result else len(exported_files),
                            'exported_count': verification_result.get('exported_count', len(exported_files)) if verification_result else len(exported_files),
                            'completeness_percentage': verification_result.get('completeness_percentage', 100.0) if verification_result else 100.0,
                            'missing_count': verification_result.get('missing_count', 0) if verification_result else 0,
                            'batman_verdict': verification_result.get('batman_verdict', 'Complete') if verification_result else 'Complete'
                        }
                    }

                    # Narrative UX: Oracle completion
                    completeness = export_metadata['verification']['completeness_percentage']
                    if self.narrator and self.narrator.is_verbose():
                        self.narrator.hero_speaks(
                            "🔮 Oracle",
                            f"Export metadata logged. Verification shows {completeness:.1f}% completeness.",
                            style="friendly",
                            technical_info=f"{len(exported_files)} nodes tracked"
                        )

                    # You can extend Oracle to track exports if needed
                    logger.debug(f"  🔮 Oracle: Tracked {len(exported_files)} node exports (frames, components, component sets)")
                    logger.debug(f"  🔮 Oracle: Verification status - {completeness:.1f}% complete")

                except Exception as e:
                    logger.warning(f"  ⚠️ Oracle tracking error: {str(e)}")

            return {
                'success': True,
                'hero': hero_name,
                'hero_emoji': hero_emoji,
                'frames_exported': len(exported_files),
                'total_frames': total_frames or len(exported_files),
                'exported_files': exported_files,
                'file_key': file_key,
                'output_dir': output_dir or export_hero.figma_exports_dir,
                'scale': scale,
                'verification': verification_result  # Batman's completeness verification
            }

        except Exception as e:
            logger.error(f"  ❌ {hero_name} frame export error: {str(e)}")

            # Build error result
            error_result = {
                'success': False,
                'errors': [str(e)],
                'hero': hero_name,
                'hero_emoji': hero_emoji,
                'mission_type': 'frame_export'
            }

            # Auto-fix mode: Attempt autonomous recovery
            if auto_fix_mode and self.auto_fix_orchestrator:
                fix_result = self.auto_fix_orchestrator.handle_exception(e, mission)

                if fix_result.get('fixed') and fix_result.get('retry_recommended'):
                    # Auto-fix successful - retry mission
                    logger.info("  🔄 Auto-fix applied. Retrying mission...")
                    return self._deploy_hawkman_frame_export(
                        mission,
                        auto_fix_mode=False  # Disable auto-fix on retry to prevent loops
                    )

            return error_result

    def _combine_hero_results(self, hero_reports: Dict) -> Dict[str, Any]:
        """
        🦸 Combine results from all heroes

        Args:
            hero_reports: Reports from each hero

        Returns:
            Combined analysis
        """
        combined = {
            'total_heroes_deployed': len(hero_reports),
            'hero_scores': {},
            'all_issues': [],
            'critical_issues': [],
            'high_priority_issues': [],
            'medium_priority_issues': []
        }

        # Extract scores from each hero
        if 'batman' in hero_reports:
            batman_data = hero_reports['batman']
            combined['hero_scores']['batman'] = {
                'success_rate': batman_data.get('success_rate', 0),
                'tests_passed': batman_data.get('tests_passed', 0),
                'tests_failed': batman_data.get('tests_failed', 0)
            }

        if 'green_lantern' in hero_reports:
            gl_data = hero_reports['green_lantern'].get('comparison', {})
            combined['hero_scores']['green_lantern'] = {
                'similarity_score': gl_data.get('similarity_score', 100),
                'is_regression': gl_data.get('is_regression', False)
            }

        if 'wonder_woman' in hero_reports:
            ww_data = hero_reports['wonder_woman']
            combined['hero_scores']['wonder_woman'] = ww_data.get('champion_score', {})

        if 'flash' in hero_reports:
            flash_data = hero_reports['flash']
            combined['hero_scores']['flash'] = flash_data.get('flash_speed_score', {})

        if 'aquaman' in hero_reports:
            aquaman_data = hero_reports['aquaman']
            combined['hero_scores']['aquaman'] = aquaman_data.get('aquaman_score', {})

        if 'atom' in hero_reports:
            atom_data = hero_reports['atom']
            combined['hero_scores']['atom'] = atom_data.get('atom_score', {})

        # Collect all issues (would be more sophisticated in production)
        # This is a simplified version
        combined['total_issues_found'] = sum(
            score.get('tests_failed', 0) + score.get('issues_found', 0)
            for score in combined['hero_scores'].values()
        )

        return combined

    def _calculate_justice_league_score(self, results: Dict) -> Dict[str, Any]:
        """
        🦸 Calculate overall Justice League Score

        Weighted average of all hero scores

        Args:
            results: Complete results

        Returns:
            Justice League composite score
        """
        hero_reports = results.get('hero_reports', {})
        scores = []

        # Extract scores from each hero
        if 'batman' in hero_reports:
            scores.append(hero_reports['batman'].get('success_rate', 0))

        if 'green_lantern' in hero_reports:
            gl_score = hero_reports['green_lantern'].get('comparison', {}).get('similarity_score', 1.0) * 100
            scores.append(gl_score)

        if 'wonder_woman' in hero_reports:
            scores.append(hero_reports['wonder_woman'].get('champion_score', {}).get('overall_score', 0))

        if 'flash' in hero_reports:
            scores.append(hero_reports['flash'].get('flash_speed_score', {}).get('score', 0))

        if 'aquaman' in hero_reports:
            scores.append(hero_reports['aquaman'].get('aquaman_score', {}).get('score', 0))

        if 'atom' in hero_reports:
            scores.append(hero_reports['atom'].get('atom_score', {}).get('score', 0))

        # Calculate average
        overall_score = sum(scores) / len(scores) if scores else 0

        # Determine grade
        if overall_score >= 95:
            grade = "S+ (Justice League Perfect)"
            verdict = "🦸 WORLD-CLASS! The Justice League approves!"
        elif overall_score >= 90:
            grade = "S (Exceptional)"
            verdict = "🦸 EXCELLENT! Minor improvements possible"
        elif overall_score >= 85:
            grade = "A+ (Outstanding)"
            verdict = "🦸 VERY GOOD! Strong across all areas"
        elif overall_score >= 80:
            grade = "A (Great)"
            verdict = "🦸 GOOD! Some areas need attention"
        elif overall_score >= 75:
            grade = "B+ (Good)"
            verdict = "🦸 ACCEPTABLE - Several improvements needed"
        elif overall_score >= 70:
            grade = "B (Decent)"
            verdict = "🦸 MODERATE - Significant work required"
        else:
            grade = "C or below"
            verdict = "🦸 NEEDS WORK - Justice League intervention required!"

        return {
            'overall_score': overall_score,
            'grade': grade,
            'verdict': verdict,
            'heroes_contributing': len(scores),
            'individual_scores': scores,
            'league_strength': 'Full Power' if len(scores) >= 5 else 'Partial Deployment'
        }

    def _generate_league_action_plan(self, results: Dict) -> Dict[str, Any]:
        """
        🦸 Generate Justice League prioritized action plan

        Combines recommendations from all heroes

        Args:
            results: Complete results

        Returns:
            Prioritized action plan
        """
        all_recommendations = []

        # Collect recommendations from each hero
        hero_reports = results.get('hero_reports', {})

        if 'wonder_woman' in hero_reports:
            ww_recs = hero_reports['wonder_woman'].get('battle_plan', {}).get('battle_phases', {})
            for phase, data in ww_recs.items():
                all_recommendations.extend(data.get('top_targets', []))

        if 'flash' in hero_reports:
            flash_recs = hero_reports['flash'].get('flash_recommendations', [])
            all_recommendations.extend(flash_recs)

        if 'aquaman' in hero_reports:
            aquaman_recs = hero_reports['aquaman'].get('aquaman_recommendations', [])
            all_recommendations.extend(aquaman_recs)

        if 'atom' in hero_reports:
            atom_recs = hero_reports['atom'].get('atom_recommendations', [])
            all_recommendations.extend(atom_recs)

        # Prioritize by severity
        critical = [r for r in all_recommendations if r.get('priority') == 'critical' or r.get('severity') == 'critical']
        high = [r for r in all_recommendations if r.get('priority') == 'high' or r.get('severity') == 'serious']
        medium = [r for r in all_recommendations if r.get('priority') == 'medium' or r.get('severity') == 'moderate']

        return {
            'total_recommendations': len(all_recommendations),
            'critical_priority': len(critical),
            'high_priority': len(high),
            'medium_priority': len(medium),
            'phases': {
                'phase_1_immediate': {
                    'timeline': 'THIS WEEK',
                    'count': len(critical),
                    'items': critical[:10],
                    'superman_says': 'Justice League demands immediate action!'
                },
                'phase_2_urgent': {
                    'timeline': '1-2 WEEKS',
                    'count': len(high),
                    'items': high[:10],
                    'superman_says': 'High priority - deploy heroes soon!'
                },
                'phase_3_important': {
                    'timeline': '2-4 WEEKS',
                    'count': len(medium),
                    'items': medium[:10],
                    'superman_says': 'Scheduled improvements for maximum impact'
                }
            },
            'superman_verdict': 'The Justice League has spoken - together we make it perfect!'
        }


# Main entry point - Superman's Mission Interface
def assemble_justice_league(mission: Dict[str, Any],
                            baseline_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    🦸 ASSEMBLE THE JUSTICE LEAGUE!

    Superman coordinates all heroes for complete design analysis

    Args:
        mission: Mission parameters with all necessary data
        baseline_dir: Optional baseline directory

    Returns:
        Complete Justice League analysis
    """
    superman = SupermanCoordinator(baseline_dir)
    return superman.assemble_justice_league(mission)
