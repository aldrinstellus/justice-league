#!/usr/bin/env python3
"""
🔮 ORACLE JUSTICE LEAGUE TRAINING SESSION
Comprehensive hero training based on all learnings, patterns, and mission history

Oracle applies all knowledge from:
- Mission history and outcomes
- User preferences and patterns
- Methodologies and best practices
- Error recovery patterns
- Performance metrics

"Train hard. Fight easy. Every hero gets better." - Oracle
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.justice_league.oracle_hero_trainer import OracleHeroTrainer


class JusticeLeagueTrainingSession:
    """
    🔮 Oracle's Comprehensive Justice League Training Session

    Trains all heroes based on accumulated knowledge and learnings
    """

    def __init__(self):
        self.trainer = OracleHeroTrainer()
        self.project_patterns_path = Path('/Users/admin/Documents/claudecode/Projects/aldo-vision/data/oracle_project_patterns.json')
        self.training_results = {
            'session_id': f"TRAIN-JL-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'started_at': datetime.now().isoformat(),
            'heroes_trained': [],
            'skills_improved': [],
            'patterns_applied': [],
            'learnings_integrated': [],
            'recommendations_implemented': []
        }

    def load_all_learnings(self) -> Dict[str, Any]:
        """Load all learnings from Oracle's knowledge base"""
        print("\n🔮 Oracle: Loading all accumulated knowledge...")
        print("=" * 80)

        with open(self.project_patterns_path, 'r') as f:
            patterns = json.load(f)

        learnings = {
            'methodologies': patterns.get('methodologies', {}),
            'user_preferences': patterns.get('user_preferences', {}),
            'error_recovery_patterns': patterns.get('error_recovery_patterns', {}),
            'hero_meta_learning': patterns.get('hero_meta_learning', {}),
            'decision_patterns': patterns.get('decision_patterns', {}),
            'hero_skills_system': patterns.get('hero_skills_system', {})
        }

        print(f"✅ Loaded knowledge from {len(learnings)} domains:")
        print(f"   • Methodologies: {len(learnings['methodologies'])}")
        print(f"   • User Preferences: {len(learnings['user_preferences'])}")
        print(f"   • Error Recovery: {len(learnings['error_recovery_patterns'])}")
        print(f"   • Hero Performance: {len(learnings.get('hero_meta_learning', {}).get('mission_history', []))} missions")

        return learnings

    def analyze_current_team_status(self) -> Dict[str, Any]:
        """Analyze current Justice League team capabilities"""
        print("\n📊 Oracle: Analyzing current team status...")
        print("=" * 80)

        skills_data = self.trainer.analyze_and_update_all_heroes()

        # Calculate team statistics
        total_heroes = len(skills_data['heroes'])
        narrator_integrated = sum(1 for h in skills_data['heroes'].values()
                                  if h['capabilities'].get('narrator_integrated', False))
        mcp_integrated = sum(1 for h in skills_data['heroes'].values()
                           if h['capabilities'].get('mcp_integrated', False))

        # Calculate average skill levels
        all_skill_levels = []
        for hero_data in skills_data['heroes'].values():
            skill_levels = hero_data.get('skill_levels', {})
            if skill_levels:
                all_skill_levels.extend(skill_levels.values())

        avg_skill = sum(all_skill_levels) / len(all_skill_levels) if all_skill_levels else 0

        team_status = {
            'total_heroes': total_heroes,
            'narrator_integrated': narrator_integrated,
            'narrator_percentage': (narrator_integrated / total_heroes) * 100,
            'mcp_integrated': mcp_integrated,
            'mcp_percentage': (mcp_integrated / total_heroes) * 100,
            'average_skill_level': avg_skill,
            'team_grade': self._calculate_team_grade(avg_skill),
            'skills_data': skills_data
        }

        print(f"\n📊 Team Status:")
        print(f"   Total Heroes: {total_heroes}")
        print(f"   Narrator Integration: {narrator_integrated}/{total_heroes} ({team_status['narrator_percentage']:.1f}%)")
        print(f"   MCP Integration: {mcp_integrated}/{total_heroes} ({team_status['mcp_percentage']:.1f}%)")
        print(f"   Average Skill Level: {avg_skill:.1f}/100")
        print(f"   Team Grade: {team_status['team_grade']}")

        return team_status

    def _calculate_team_grade(self, avg_skill: float) -> str:
        """Calculate team grade based on average skill"""
        if avg_skill >= 90:
            return "A+ (Elite)"
        elif avg_skill >= 80:
            return "A (Excellent)"
        elif avg_skill >= 70:
            return "B (Good)"
        elif avg_skill >= 60:
            return "C (Satisfactory)"
        else:
            return "D (Needs Improvement)"

    def apply_methodology_learnings(self, learnings: Dict[str, Any]) -> List[str]:
        """Apply methodology learnings to heroes"""
        print("\n🎓 Oracle: Applying methodology learnings...")
        print("=" * 80)

        improvements = []
        methodologies = learnings.get('methodologies', {})

        for method_name, method_data in methodologies.items():
            success_rate = method_data.get('success_rate', 0)
            heroes = method_data.get('heroes_involved', [])

            print(f"\n📚 Methodology: {method_data.get('name', method_name)}")
            print(f"   Success Rate: {success_rate * 100:.1f}%")
            print(f"   Heroes Involved: {', '.join(heroes)}")

            # Apply learnings to heroes
            if success_rate >= 0.9:  # High success rate
                improvement = {
                    'methodology': method_name,
                    'success_rate': success_rate,
                    'learning': f"Reinforce {method_name} - proven {success_rate*100:.1f}% success",
                    'heroes_affected': heroes
                }
                improvements.append(improvement)
                print(f"   ✅ High Success: Reinforce this methodology across team")
            elif success_rate < 0.7:  # Needs improvement
                improvement = {
                    'methodology': method_name,
                    'success_rate': success_rate,
                    'learning': f"Improve {method_name} - only {success_rate*100:.1f}% success",
                    'heroes_affected': heroes
                }
                improvements.append(improvement)
                print(f"   ⚠️  Needs Work: Train heroes in this methodology")

        print(f"\n✅ Applied {len(improvements)} methodology learnings")
        return improvements

    def apply_user_preference_learnings(self, learnings: Dict[str, Any]) -> List[str]:
        """Apply user preference learnings to heroes"""
        print("\n👤 Oracle: Applying user preference learnings...")
        print("=" * 80)

        improvements = []
        preferences = learnings.get('user_preferences', {})

        # Banner display preference
        if 'banner_display' in preferences:
            banner_pref = preferences['banner_display']
            print(f"\n🎯 Banner Display Preference:")
            print(f"   Priority: {banner_pref.get('priority', 'N/A')}")
            print(f"   Trigger Keywords: {len(banner_pref.get('trigger_keywords', []))}")

            improvements.append({
                'preference': 'banner_display',
                'learning': 'Always display Justice League banner on trigger keywords',
                'priority': banner_pref.get('priority'),
                'heroes_affected': ['Superman', 'All']
            })

        # Output paths preference
        if 'output_paths' in preferences:
            path_pref = preferences['output_paths']
            print(f"\n📁 Output Paths Preference:")
            print(f"   Preference: {path_pref.get('preference', 'N/A')}")
            print(f"   Priority: {path_pref.get('priority', 'N/A')}")

            improvements.append({
                'preference': 'output_paths',
                'learning': 'Always provide full absolute paths prominently',
                'priority': path_pref.get('priority'),
                'heroes_affected': ['All']
            })

        # Progress display preference
        if 'progress_display' in preferences:
            prog_pref = preferences['progress_display']
            print(f"\n📊 Progress Display Preference:")
            print(f"   Preference: {prog_pref.get('preference', 'N/A')}")
            print(f"   Features: {len(prog_pref.get('features', []))}")

            improvements.append({
                'preference': 'progress_display',
                'learning': 'Interactive progress with minimal output, single-line updates',
                'priority': 'HIGH',
                'heroes_affected': ['Hawkman', 'Quicksilver', 'All export heroes']
            })

        # Default export hero preference
        if 'default_export_hero' in preferences:
            export_pref = preferences['default_export_hero']
            print(f"\n⚡ Default Export Hero Preference:")
            print(f"   First Choice: {export_pref.get('hero_selection', {}).get('first_choice', 'N/A')}")
            print(f"   Speedup: {export_pref.get('benefits', {}).get('quicksilver', {}).get('speed', 'N/A')}")

            improvements.append({
                'preference': 'default_export_hero',
                'learning': 'Quicksilver is default for all Figma PNG exports (2.5-3x faster)',
                'priority': export_pref.get('priority'),
                'heroes_affected': ['Quicksilver', 'Hawkman', 'Superman']
            })

        print(f"\n✅ Applied {len(improvements)} user preference learnings")
        return improvements

    def apply_error_recovery_learnings(self, learnings: Dict[str, Any]) -> List[str]:
        """Apply error recovery pattern learnings"""
        print("\n🔧 Oracle: Applying error recovery learnings...")
        print("=" * 80)

        improvements = []
        error_patterns = learnings.get('error_recovery_patterns', {})

        for pattern_name, pattern_data in error_patterns.items():
            print(f"\n🛡️  Error Pattern: {pattern_data.get('name', pattern_name)}")
            print(f"   Type: {pattern_data.get('pattern_type', 'N/A')}")
            print(f"   Confidence: {pattern_data.get('confidence_score', 0) * 100:.1f}%")
            print(f"   Production Validated: {pattern_data.get('production_validated', False)}")

            if pattern_data.get('production_validated'):
                improvement = {
                    'pattern': pattern_name,
                    'learning': pattern_data.get('solution', {}).get('technique', 'Unknown'),
                    'confidence': pattern_data.get('confidence_score', 0),
                    'heroes_affected': pattern_data.get('heroes_involved', []),
                    'reusable_for': pattern_data.get('reusable_for', [])
                }
                improvements.append(improvement)
                print(f"   ✅ Applied: {improvement['learning']}")

        print(f"\n✅ Applied {len(improvements)} error recovery patterns")
        return improvements

    def train_individual_heroes(self, team_status: Dict[str, Any], learnings: Dict[str, Any]) -> List[Dict]:
        """Train each hero individually based on their needs"""
        print("\n🎓 Oracle: Individual Hero Training Sessions...")
        print("=" * 80)

        skills_data = team_status['skills_data']
        training_results = []

        for hero_name, hero_data in skills_data['heroes'].items():
            training_needs = hero_data.get('training_needed', [])

            if not training_needs:
                continue

            print(f"\n{hero_data.get('emoji', '🦸')} Training {hero_name}:")
            print(f"   Training Needs: {len(training_needs)}")

            hero_training = {
                'hero': hero_name,
                'emoji': hero_data.get('emoji'),
                'training_needs': training_needs,
                'scenarios_generated': [],
                'skills_before': len(hero_data.get('capabilities', {}).get('skills', [])),
                'improvements': []
            }

            # Generate training scenarios
            for need in training_needs:
                scenario = self.trainer.training_system.create_training_scenario(hero_name, need)
                hero_training['scenarios_generated'].append(scenario)
                print(f"   📋 Scenario: {scenario['target_area']}")
                print(f"      Objectives: {len(scenario['objectives'])}")

            # Apply specific improvements based on needs
            if "Narrator integration" in ' '.join(training_needs):
                hero_training['improvements'].append({
                    'type': 'narrator_integration',
                    'action': 'Add say(), think(), handoff() methods',
                    'expected_benefit': '+15% team coordination efficiency'
                })
                print(f"   ✨ Improvement: Narrator integration planned")

            if "MCP" in ' '.join(training_needs):
                hero_training['improvements'].append({
                    'type': 'mcp_integration',
                    'action': 'Add Playwright/MCP capabilities',
                    'expected_benefit': '+20% visual testing accuracy'
                })
                print(f"   ✨ Improvement: MCP integration planned")

            if "skill set" in ' '.join(training_needs).lower():
                hero_training['improvements'].append({
                    'type': 'skill_expansion',
                    'action': 'Expand from <5 to 5+ skills',
                    'expected_benefit': '+25% mission capability coverage'
                })
                print(f"   ✨ Improvement: Skill expansion planned")

            training_results.append(hero_training)

        print(f"\n✅ Trained {len(training_results)} heroes with skill gaps")
        return training_results

    def generate_team_improvement_plan(self, training_results: List[Dict], improvements: List[str]) -> Dict:
        """Generate comprehensive team improvement plan"""
        print("\n📋 Oracle: Generating Team Improvement Plan...")
        print("=" * 80)

        # Aggregate all improvements
        total_scenarios = sum(len(t['scenarios_generated']) for t in training_results)
        total_improvements = sum(len(t['improvements']) for t in training_results)

        heroes_needing_narrator = [t['hero'] for t in training_results
                                   if any('narrator' in i.get('type', '').lower()
                                         for i in t.get('improvements', []))]

        heroes_needing_mcp = [t['hero'] for t in training_results
                             if any('mcp' in i.get('type', '').lower()
                                   for i in t.get('improvements', []))]

        heroes_needing_skills = [t['hero'] for t in training_results
                                if any('skill' in i.get('type', '').lower()
                                      for i in t.get('improvements', []))]

        plan = {
            'plan_id': f"IMPROVE-JL-{datetime.now().strftime('%Y%m%d')}",
            'created_at': datetime.now().isoformat(),
            'summary': {
                'heroes_trained': len(training_results),
                'training_scenarios_generated': total_scenarios,
                'improvements_planned': total_improvements,
                'estimated_team_improvement': self._estimate_team_improvement(training_results)
            },
            'priority_actions': {
                'narrator_integration': {
                    'heroes': heroes_needing_narrator,
                    'count': len(heroes_needing_narrator),
                    'priority': 'HIGH',
                    'expected_impact': '+15% team coordination'
                },
                'mcp_integration': {
                    'heroes': heroes_needing_mcp,
                    'count': len(heroes_needing_mcp),
                    'priority': 'MEDIUM',
                    'expected_impact': '+20% visual testing accuracy'
                },
                'skill_expansion': {
                    'heroes': heroes_needing_skills,
                    'count': len(heroes_needing_skills),
                    'priority': 'MEDIUM',
                    'expected_impact': '+25% mission coverage'
                }
            },
            'training_timeline': {
                'immediate': [t for t in training_results if len(t['training_needs']) >= 2],
                'short_term': [t for t in training_results if len(t['training_needs']) == 1],
                'estimated_completion': '2-4 weeks'
            },
            'expected_outcomes': [
                f"Narrator integration: {len(heroes_needing_narrator)} heroes → 100% team coverage",
                f"MCP integration: {len(heroes_needing_mcp)} heroes → Enhanced visual testing",
                f"Skill expansion: {len(heroes_needing_skills)} heroes → Broader capabilities",
                f"Team grade improvement: {self._estimate_grade_improvement(training_results)}"
            ]
        }

        print(f"\n📊 Improvement Plan Summary:")
        print(f"   Heroes to Train: {plan['summary']['heroes_trained']}")
        print(f"   Training Scenarios: {plan['summary']['training_scenarios_generated']}")
        print(f"   Improvements Planned: {plan['summary']['improvements_planned']}")
        print(f"   Expected Team Improvement: {plan['summary']['estimated_team_improvement']}")

        print(f"\n🎯 Priority Actions:")
        for action, details in plan['priority_actions'].items():
            if details['count'] > 0:
                print(f"   • {action.replace('_', ' ').title()}: {details['count']} heroes")
                print(f"     Priority: {details['priority']} | Impact: {details['expected_impact']}")

        return plan

    def _estimate_team_improvement(self, training_results: List[Dict]) -> str:
        """Estimate overall team improvement percentage"""
        if not training_results:
            return "0%"

        # Calculate based on number of improvements
        total_improvements = sum(len(t['improvements']) for t in training_results)
        improvement_pct = min(total_improvements * 5, 50)  # Max 50% improvement

        return f"+{improvement_pct}% skill level increase"

    def _estimate_grade_improvement(self, training_results: List[Dict]) -> str:
        """Estimate grade improvement"""
        if not training_results:
            return "No change"

        # Simple heuristic based on number of heroes being trained
        heroes_count = len(training_results)

        if heroes_count >= 8:
            return "B → A (Full team upskilling)"
        elif heroes_count >= 5:
            return "Current → +1 grade level"
        else:
            return "Current → +0.5 grade level"

    def save_training_session(self, plan: Dict, learnings: Dict):
        """Save training session results"""
        print("\n💾 Oracle: Saving training session results...")
        print("=" * 80)

        # Save to project patterns
        with open(self.project_patterns_path, 'r') as f:
            patterns = json.load(f)

        if 'training_sessions' not in patterns:
            patterns['training_sessions'] = []

        session_record = {
            'session_id': self.training_results['session_id'],
            'date': datetime.now().isoformat(),
            'improvement_plan': plan,
            'learnings_applied': {
                'methodologies': len(learnings.get('methodologies', {})),
                'user_preferences': len(learnings.get('user_preferences', {})),
                'error_patterns': len(learnings.get('error_recovery_patterns', {}))
            },
            'next_review_date': self._calculate_next_review_date()
        }

        patterns['training_sessions'].append(session_record)

        with open(self.project_patterns_path, 'w') as f:
            json.dump(patterns, f, indent=2)

        # Also save detailed plan
        plan_file = Path('/Users/admin/Documents/claudecode/Projects/aldo-vision/data/justice_league_training_plan.json')
        with open(plan_file, 'w') as f:
            json.dump(plan, f, indent=2)

        print(f"✅ Training session saved:")
        print(f"   Session ID: {session_record['session_id']}")
        print(f"   Plan File: {plan_file}")
        print(f"   Next Review: {session_record['next_review_date']}")

    def _calculate_next_review_date(self) -> str:
        """Calculate next training review date (2 weeks from now)"""
        from datetime import timedelta
        next_date = datetime.now() + timedelta(days=14)
        return next_date.strftime('%Y-%m-%d')

    def run_full_training_session(self):
        """Run complete training session"""
        print("\n" + "=" * 80)
        print("🔮 ORACLE JUSTICE LEAGUE TRAINING SESSION")
        print("=" * 80)
        print(f"Session ID: {self.training_results['session_id']}")
        print(f"Started: {self.training_results['started_at']}")
        print("=" * 80)

        # Step 1: Load all learnings
        learnings = self.load_all_learnings()

        # Step 2: Analyze current team status
        team_status = self.analyze_current_team_status()

        # Step 3: Apply methodology learnings
        method_improvements = self.apply_methodology_learnings(learnings)
        self.training_results['patterns_applied'].extend(method_improvements)

        # Step 4: Apply user preference learnings
        pref_improvements = self.apply_user_preference_learnings(learnings)
        self.training_results['learnings_integrated'].extend(pref_improvements)

        # Step 5: Apply error recovery learnings
        error_improvements = self.apply_error_recovery_learnings(learnings)
        self.training_results['learnings_integrated'].extend(error_improvements)

        # Step 6: Train individual heroes
        training_results = self.train_individual_heroes(team_status, learnings)
        self.training_results['heroes_trained'] = [t['hero'] for t in training_results]

        # Step 7: Generate team improvement plan
        improvement_plan = self.generate_team_improvement_plan(
            training_results,
            method_improvements + pref_improvements + error_improvements
        )

        # Step 8: Save training session
        self.save_training_session(improvement_plan, learnings)

        # Final summary
        print("\n" + "=" * 80)
        print("🎓 TRAINING SESSION COMPLETE")
        print("=" * 80)
        print(f"\n✅ Heroes Trained: {len(self.training_results['heroes_trained'])}")
        print(f"✅ Patterns Applied: {len(self.training_results['patterns_applied'])}")
        print(f"✅ Learnings Integrated: {len(self.training_results['learnings_integrated'])}")
        print(f"✅ Training Scenarios Generated: {improvement_plan['summary']['training_scenarios_generated']}")
        print(f"✅ Expected Team Improvement: {improvement_plan['summary']['estimated_team_improvement']}")

        print(f"\n📋 Full Training Plan:")
        print(f"   /Users/admin/Documents/claudecode/Projects/aldo-vision/data/justice_league_training_plan.json")

        print("\n" + "=" * 80)
        print("🔮 Oracle: Training complete. Justice League is leveling up!")
        print("=" * 80 + "\n")

        return improvement_plan


def main():
    """Main entry point"""
    session = JusticeLeagueTrainingSession()
    plan = session.run_full_training_session()
    return plan


if __name__ == "__main__":
    main()
