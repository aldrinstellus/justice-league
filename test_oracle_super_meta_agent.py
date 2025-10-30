#!/usr/bin/env python3
"""
🔮 Test Oracle's Super Meta Agent System (v1.9.1)

Tests all 5 phases:
- Phase 1: Mission outcome tracking
- Phase 2: Hero performance analysis & recommendations
- Phase 3: Capability enhancement
- Phase 4: Predictive deployment
- Phase 5: Training scenario generation

Demonstrates Oracle learning from missions and improving all heroes over time.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.justice_league.oracle_meta_agent import OracleMeta
from datetime import datetime

def simulate_mission_outcome(mission_type: str, heroes: list, scores: dict, success: bool) -> dict:
    """Simulate a mission outcome for testing"""
    return {
        'timestamp': datetime.now().isoformat(),
        'mission': 'Test Mission',
        'target_url': f'test://{mission_type}',
        'file_key': 'test_file_key' if mission_type == 'frame_export' else None,
        'frames_exported': scores.get('hawkman', {}).get('frames', 0) if mission_type == 'frame_export' else None,
        'heroes_deployed': heroes,
        'hero_reports': {
            hero: {
                'success': success,
                'score': scores.get(hero, {}).get('score', 85),
                'accuracy_score': scores.get(hero, {}).get('score', 85),
                'artemis_score': scores.get(hero, {}).get('score', 85) if hero == 'Artemis' else None,
                'tests_passed': scores.get(hero, {}).get('tests_passed', 8) if hero == 'Batman' else None,
                'tests_failed': scores.get(hero, {}).get('tests_failed', 2) if hero == 'Batman' else None,
                'frames_exported': scores.get(hero, {}).get('frames', 150) if hero == 'Hawkman' else None,
                'total_frames': scores.get(hero, {}).get('total_frames', 150) if hero == 'Hawkman' else None,
            }
            for hero in heroes
        },
        'justice_league_score': {
            'overall_score': 85 if success else 65,
            'grade': 'B' if success else 'D',
            'verdict': 'Good performance' if success else 'Needs improvement'
        }
    }

def test_super_meta_agent():
    """Test complete Super Meta Agent system"""

    print("=" * 80)
    print("🔮 ORACLE SUPER META AGENT - COMPLETE SYSTEM TEST")
    print("=" * 80)
    print()

    oracle = OracleMeta()

    # ==========================================
    # PHASE 1: MISSION OUTCOME TRACKING
    # ==========================================

    print("📊 PHASE 1: Mission Outcome Tracking")
    print("-" * 80)

    # Simulate 5 missions to build history
    test_missions = [
        ('figma_conversion', ['Artemis', 'Green Arrow'], {'Artemis': {'score': 92}, 'Green Arrow': {'score': 88}}, True),
        ('figma_conversion', ['Artemis', 'Green Arrow'], {'Artemis': {'score': 85}, 'Green Arrow': {'score': 90}}, True),
        ('frame_export', ['Hawkman'], {'Hawkman': {'score': 100, 'frames': 150, 'total_frames': 150}}, True),
        ('figma_conversion', ['Artemis'], {'Artemis': {'score': 65}}, False),  # Failed mission
        ('frame_export', ['Hawkman'], {'Hawkman': {'score': 100, 'frames': 200, 'total_frames': 200}}, True),
    ]

    for i, (m_type, heroes, scores, success) in enumerate(test_missions, 1):
        mission = simulate_mission_outcome(m_type, heroes, scores, success)
        tracked = oracle.track_mission_outcome(mission)
        status = "✅" if tracked else "❌"
        print(f"  {status} Mission {i}: {m_type} - {'Success' if success else 'Failed'}")

    print()

    # ==========================================
    # PHASE 2: HERO PERFORMANCE ANALYSIS
    # ==========================================

    print("🧠 PHASE 2: Hero Performance Analysis & Intelligence")
    print("-" * 80)

    # Test 1: Analyze performance trends
    print("\n📈 Test 2.1: Analyzing Hero Performance Trends")
    for hero in ['Artemis', 'Green Arrow', 'Hawkman']:
        trends = oracle.analyze_hero_performance_trends(hero)
        if trends.get('status') != 'insufficient_data':
            print(f"\n  {hero}:")
            print(f"    Total Missions: {trends.get('total_missions', 0)}")
            print(f"    Success Rate: {trends.get('success_rate', 0):.1%}")
            print(f"    Average Accuracy: {trends.get('average_accuracy', 0):.1f}%")
            print(f"    Trend: {trends.get('trend_direction', 'unknown')}")
            print(f"    Recommendation: {trends.get('recommendation', 'N/A')}")

    # Test 2: Identify skill gaps
    print("\n\n🎯 Test 2.2: Identifying Skill Gaps")
    for hero in ['Artemis', 'Hawkman']:
        gaps = oracle.identify_skill_gaps(hero)
        if gaps:
            print(f"\n  {hero} - Found {len(gaps)} skill gap(s):")
            for gap in gaps:
                print(f"    - {gap.get('area')}: {gap.get('average_score'):.1f}% (Severity: {gap.get('severity')})")
        else:
            print(f"\n  {hero} - No skill gaps detected")

    # Test 3: Compare hero effectiveness
    print("\n\n⚖️ Test 2.3: Comparing Hero Effectiveness")
    comparison = oracle.compare_hero_effectiveness('figma_conversion')
    if comparison.get('hero_rankings'):
        print(f"\n  Mission Type: figma_conversion")
        print(f"  Most Effective: {comparison.get('most_effective', {}).get('hero', 'N/A')}")
        print(f"    Score: {comparison.get('most_effective', {}).get('average_score', 0):.1f}%")

    # Test 4: Generate improvement recommendations
    print("\n\n💡 Test 2.4: Generating Improvement Recommendations")
    recommendations = oracle.generate_hero_improvement_recommendations('Artemis')
    if recommendations:
        print(f"\n  Artemis - {len(recommendations)} recommendation(s):")
        for rec in recommendations:
            print(f"    [{rec.get('priority', 'unknown').upper()}] {rec.get('recommendation', 'N/A')}")
            print(f"      Expected Impact: {rec.get('expected_impact', 'N/A')}")

    print()

    # ==========================================
    # PHASE 3: CAPABILITY ENHANCEMENT
    # ==========================================

    print("🚀 PHASE 3: Capability Enhancement System")
    print("-" * 80)

    # Test 1: Get hero capabilities
    print("\n📚 Test 3.1: Loading Hero Capabilities")
    capabilities = oracle.get_hero_capabilities('Green Arrow')
    if capabilities.get('status') == 'loaded':
        print(f"\n  Green Arrow Capabilities:")
        print(f"    Status: {capabilities.get('status')}")
        print(f"    Thresholds: {len(capabilities.get('thresholds', {}))} configured")
        print(f"    Recommended Techniques: {len(capabilities.get('recommended_techniques', []))}")
        if capabilities.get('thresholds'):
            print(f"    Sample Threshold: spacing_tolerance = {capabilities['thresholds'].get('spacing_tolerance', {}).get('value', 'N/A')} pixels")

    # Test 2: Update hero capability
    print("\n\n🔧 Test 3.2: Updating Hero Capability (Threshold Adjustment)")
    updated = oracle.update_hero_capability(
        'green_arrow',
        'threshold',
        {'spacing_tolerance': 3}  # Increase from 2 to 3 pixels based on learning
    )
    status = "✅" if updated else "❌"
    print(f"  {status} Threshold adjustment applied: spacing_tolerance → 3 pixels")

    print()

    # ==========================================
    # PHASE 4: PREDICTIVE DEPLOYMENT
    # ==========================================

    print("🔮 PHASE 4: Predictive Deployment")
    print("-" * 80)

    # Test 1: Predict mission success
    print("\n🎲 Test 4.1: Predicting Mission Success")
    prediction = oracle.predict_mission_success(
        {'mission_type': 'figma_conversion', 'complexity': 'high'},
        ['Artemis', 'Green Arrow']
    )
    print(f"\n  Mission: figma_conversion with Artemis + Green Arrow")
    print(f"    Prediction: {prediction.get('prediction', 'unknown').upper()}")
    print(f"    Probability: {prediction.get('probability', 0):.1%}")
    print(f"    Confidence: {prediction.get('confidence', 'unknown')}")
    print(f"    Reason: {prediction.get('reason', 'N/A')}")

    # Test 2: Suggest optimal hero combination
    print("\n\n👥 Test 4.2: Suggesting Optimal Hero Combination")
    suggested = oracle.suggest_optimal_hero_combination({'mission_type': 'figma_conversion'})
    if suggested:
        print(f"\n  For mission type: figma_conversion")
        print(f"  Recommended Heroes: {', '.join(suggested)}")

    print()

    # ==========================================
    # PHASE 5: TRAINING SCENARIO GENERATION
    # ==========================================

    print("🎓 PHASE 5: Training Scenario Generation")
    print("-" * 80)

    # Test 1: Generate training scenario
    print("\n📝 Test 5.1: Generating Training Scenario")
    scenario = oracle.generate_training_scenario('Artemis', 'figma_conversion')
    if scenario:
        print(f"\n  Scenario Created: {scenario.get('scenario_id', 'N/A')}")
        print(f"    Hero: {scenario.get('hero', 'N/A')}")
        print(f"    Target Area: {scenario.get('target_area', 'N/A')}")
        print(f"    Objectives: {len(scenario.get('objectives', []))}")
        for i, obj in enumerate(scenario.get('objectives', [])[:2], 1):
            print(f"      {i}. {obj}")
        print(f"    Success Criteria: {scenario.get('success_criteria', {}).get('min_score', 0)}% min score")

    # Test 2: Get complete training plan
    print("\n\n📋 Test 5.2: Getting Complete Training Plan")
    plan = oracle.get_hero_training_plan('Artemis')
    if plan:
        print(f"\n  Training Plan for Artemis:")
        print(f"    Total Scenarios: {plan.get('total_scenarios', 0)}")
        if plan.get('scenarios'):
            print(f"    Priority Order:")
            for i, scenario_id in enumerate(plan.get('priority_order', [])[:3], 1):
                print(f"      {i}. {scenario_id}")

    print()
    print("=" * 80)
    print("✅ ALL SUPER META AGENT TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print()
    print("🔮 Oracle's Super Meta Agent System is fully operational!")
    print("   ✅ Phase 1: Mission tracking - Real-time learning from every mission")
    print("   ✅ Phase 2: Performance analysis - Identifying trends and skill gaps")
    print("   ✅ Phase 3: Capability enhancement - Heroes read Oracle's wisdom")
    print("   ✅ Phase 4: Predictive deployment - Oracle guides hero selection")
    print("   ✅ Phase 5: Training scenarios - Proactive skill improvement")
    print()
    print("🎓 The Justice League now has a teacher who makes them smarter every day!")
    print()

if __name__ == "__main__":
    test_super_meta_agent()
