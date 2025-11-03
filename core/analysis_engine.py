#!/usr/bin/env python3
"""
Analysis Engine - Core orchestration for multi-persona design analysis
Generates cross-persona insights and recommendations
"""

import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import re
from datetime import datetime


@dataclass
class InsightPattern:
    """Represents a cross-persona insight pattern"""
    pattern_type: str
    confidence: float
    supporting_personas: List[str]
    insight: str
    recommendations: List[str]
    priority: str  # high, medium, low


@dataclass
class ConflictResolution:
    """Represents resolution of conflicting persona insights"""
    conflict_type: str
    personas_involved: List[str]
    conflict_description: str
    resolution_strategy: str
    recommended_approach: str


class AnalysisEngine:
    """
    Core analysis engine that orchestrates multi-persona analysis
    and generates cross-insights, conflict resolution, and strategic recommendations
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Define insight pattern categories
        self.insight_categories = {
            'technical_architecture': ['ai_developer', 'design_systems_engineer', 'file_analyzer'],
            'user_experience': ['product_designer', 'content_strategist', 'accessibility_specialist'],
            'business_value': ['product_manager', 'security_analyst'],
            'implementation_quality': ['qa_engineer', 'test_automation_engineer', 'tdd_specialist'],
            'design_systems': ['design_systems_designer', 'design_systems_engineer', 'visual_reporter']
        }

        # Common conflict resolution strategies
        self.conflict_strategies = {
            'accessibility_vs_aesthetics': 'prioritize_accessibility_with_aesthetic_compromise',
            'performance_vs_features': 'implement_progressive_enhancement',
            'security_vs_usability': 'implement_secure_by_design_with_ux_optimization',
            'technical_debt_vs_delivery': 'balanced_approach_with_documentation',
            'design_consistency_vs_innovation': 'controlled_innovation_within_system'
        }

    def generate_cross_insights(self, persona_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate cross-persona insights by analyzing patterns, conflicts, and synergies

        Args:
            persona_results: Results from all persona analyses

        Returns:
            Comprehensive cross-insights analysis
        """
        self.logger.info("Generating cross-persona insights...")

        try:
            # Extract key themes from all persona analyses
            common_themes = self._extract_common_themes(persona_results)

            # Identify insight patterns
            insight_patterns = self._identify_insight_patterns(persona_results, common_themes)

            # Detect conflicts and generate resolutions
            conflicts = self._detect_conflicts(persona_results)
            conflict_resolutions = self._generate_conflict_resolutions(conflicts)

            # Generate strategic recommendations
            strategic_recommendations = self._generate_strategic_recommendations(
                persona_results, insight_patterns, conflict_resolutions
            )

            # Calculate confidence scores
            confidence_analysis = self._calculate_confidence_analysis(persona_results, insight_patterns)

            # Priority matrix
            priority_matrix = self._generate_priority_matrix(insight_patterns, strategic_recommendations)

            cross_insights = {
                'analysis_summary': {
                    'total_personas_analyzed': len(persona_results),
                    'common_themes_identified': len(common_themes),
                    'insight_patterns_found': len(insight_patterns),
                    'conflicts_detected': len(conflicts),
                    'strategic_recommendations': len(strategic_recommendations)
                },
                'common_themes': common_themes,
                'insight_patterns': [pattern.__dict__ for pattern in insight_patterns],
                'conflicts_and_resolutions': [
                    {
                        'conflict': conflict.__dict__,
                        'resolution': resolution.__dict__
                    } for conflict, resolution in zip(conflicts, conflict_resolutions)
                ],
                'strategic_recommendations': strategic_recommendations,
                'confidence_analysis': confidence_analysis,
                'priority_matrix': priority_matrix,
                'implementation_roadmap': self._generate_implementation_roadmap(strategic_recommendations)
            }

            self.logger.info(f"Generated {len(insight_patterns)} cross-insights")
            return cross_insights

        except Exception as e:
            self.logger.error(f"Failed to generate cross-insights: {str(e)}")
            raise

    def _extract_common_themes(self, persona_results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract common themes across all persona analyses"""
        theme_mentions = defaultdict(list)
        theme_frequencies = defaultdict(int)

        # Common design/UX themes
        design_themes = [
            'accessibility', 'usability', 'consistency', 'scalability',
            'performance', 'security', 'maintainability', 'user_experience',
            'responsive_design', 'component_reusability', 'design_system',
            'information_architecture', 'visual_hierarchy', 'interaction_patterns'
        ]

        for persona_name, analysis in persona_results.items():
            if not isinstance(analysis, dict):
                continue

            # Convert analysis to searchable text
            analysis_text = json.dumps(analysis).lower()

            for theme in design_themes:
                if theme.replace('_', ' ') in analysis_text or theme in analysis_text:
                    theme_mentions[theme].append(persona_name)
                    theme_frequencies[theme] += analysis_text.count(theme)

        # Identify themes mentioned by multiple personas
        common_themes = {}
        for theme, personas in theme_mentions.items():
            if len(personas) >= 2:  # At least 2 personas mention this theme
                common_themes[theme] = {
                    'mentioned_by_personas': personas,
                    'frequency': theme_frequencies[theme],
                    'consensus_level': len(personas) / len(persona_results)
                }

        return common_themes

    def _identify_insight_patterns(self, persona_results: Dict[str, Any],
                                 common_themes: Dict[str, Any]) -> List[InsightPattern]:
        """Identify patterns across persona insights"""
        patterns = []

        # Pattern 1: High-consensus themes become high-priority patterns
        for theme, data in common_themes.items():
            if data['consensus_level'] >= 0.6:  # 60% or more personas agree
                patterns.append(InsightPattern(
                    pattern_type='high_consensus_theme',
                    confidence=data['consensus_level'],
                    supporting_personas=data['mentioned_by_personas'],
                    insight=f"Strong consensus on {theme.replace('_', ' ')} importance across {len(data['mentioned_by_personas'])} personas",
                    recommendations=[
                        f"Prioritize {theme.replace('_', ' ')} in implementation",
                        f"Ensure cross-team alignment on {theme.replace('_', ' ')} standards",
                        f"Create detailed guidelines for {theme.replace('_', ' ')}"
                    ],
                    priority='high'
                ))

        # Pattern 2: Technical architecture alignment
        tech_personas = ['ai_developer', 'design_systems_engineer', 'file_analyzer']
        tech_insights = self._extract_category_insights(persona_results, tech_personas)
        if tech_insights:
            patterns.append(InsightPattern(
                pattern_type='technical_architecture_alignment',
                confidence=0.8,
                supporting_personas=tech_personas,
                insight="Technical personas align on architecture patterns and implementation approach",
                recommendations=tech_insights,
                priority='high'
            ))

        # Pattern 3: User experience coherence
        ux_personas = ['product_designer', 'content_strategist', 'accessibility_specialist']
        ux_insights = self._extract_category_insights(persona_results, ux_personas)
        if ux_insights:
            patterns.append(InsightPattern(
                pattern_type='user_experience_coherence',
                confidence=0.8,
                supporting_personas=ux_personas,
                insight="UX-focused personas show coherent user experience strategy",
                recommendations=ux_insights,
                priority='high'
            ))

        return patterns

    def _extract_category_insights(self, persona_results: Dict[str, Any],
                                 personas: List[str]) -> List[str]:
        """Extract key insights from specific persona category"""
        insights = []

        for persona in personas:
            if persona in persona_results:
                analysis = persona_results[persona]
                if isinstance(analysis, dict):
                    # Extract recommendations or key points
                    if 'recommendations' in analysis:
                        if isinstance(analysis['recommendations'], list):
                            insights.extend(analysis['recommendations'][:2])  # Top 2
                    elif 'key_insights' in analysis:
                        if isinstance(analysis['key_insights'], list):
                            insights.extend(analysis['key_insights'][:2])
                    elif 'summary' in analysis:
                        insights.append(analysis['summary'])

        return list(set(insights))  # Remove duplicates

    def _detect_conflicts(self, persona_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect potential conflicts between persona recommendations"""
        conflicts = []

        # Define potential conflict scenarios
        conflict_patterns = [
            {
                'type': 'accessibility_vs_aesthetics',
                'personas': ['accessibility_specialist', 'product_designer'],
                'keywords': ['contrast', 'color', 'visual', 'aesthetic', 'compliant']
            },
            {
                'type': 'performance_vs_features',
                'personas': ['ai_developer', 'product_manager'],
                'keywords': ['performance', 'features', 'optimization', 'functionality']
            },
            {
                'type': 'security_vs_usability',
                'personas': ['security_analyst', 'product_designer'],
                'keywords': ['security', 'authentication', 'privacy', 'user-friendly']
            }
        ]

        for pattern in conflict_patterns:
            persona_data = {}
            for persona in pattern['personas']:
                if persona in persona_results:
                    persona_data[persona] = persona_results[persona]

            if len(persona_data) >= 2:
                # Check for conflicting recommendations
                conflict = self._analyze_potential_conflict(persona_data, pattern)
                if conflict:
                    conflicts.append(conflict)

        return conflicts

    def _analyze_potential_conflict(self, persona_data: Dict[str, Any],
                                  pattern: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze if personas have conflicting recommendations"""
        # Simplified conflict detection - in real implementation,
        # this would use NLP to detect semantic conflicts

        recommendations = {}
        for persona, data in persona_data.items():
            if isinstance(data, dict) and 'recommendations' in data:
                recommendations[persona] = data.get('recommendations', [])

        if len(recommendations) >= 2:
            # For now, assume conflict exists if both personas have recommendations
            # In practice, you'd analyze semantic similarity/conflict
            return {
                'type': pattern['type'],
                'personas_involved': list(recommendations.keys()),
                'conflict_description': f"Potential {pattern['type'].replace('_', ' ')} conflict detected",
                'persona_positions': recommendations
            }

        return None

    def _generate_conflict_resolutions(self, conflicts: List[Dict[str, Any]]) -> List[ConflictResolution]:
        """Generate resolutions for detected conflicts"""
        resolutions = []

        for conflict in conflicts:
            conflict_type = conflict.get('type', 'unknown')
            strategy = self.conflict_strategies.get(conflict_type, 'balanced_approach_with_stakeholder_input')

            resolutions.append(ConflictResolution(
                conflict_type=conflict_type,
                personas_involved=conflict['personas_involved'],
                conflict_description=conflict['conflict_description'],
                resolution_strategy=strategy,
                recommended_approach=self._get_resolution_approach(conflict_type, strategy)
            ))

        return resolutions

    def _get_resolution_approach(self, conflict_type: str, strategy: str) -> str:
        """Get specific approach for conflict resolution"""
        approaches = {
            'accessibility_vs_aesthetics': 'Implement accessible design that maintains visual appeal through careful color choices, typography, and layout',
            'performance_vs_features': 'Use progressive enhancement and lazy loading to deliver core functionality quickly while loading advanced features on demand',
            'security_vs_usability': 'Implement security measures with clear user communication and streamlined workflows',
            'technical_debt_vs_delivery': 'Document technical decisions and plan refactoring in subsequent iterations',
            'design_consistency_vs_innovation': 'Create innovation within established design system constraints'
        }

        return approaches.get(conflict_type, 'Collaborate with stakeholders to find balanced solution')

    def _generate_strategic_recommendations(self, persona_results: Dict[str, Any],
                                          insight_patterns: List[InsightPattern],
                                          conflict_resolutions: List[ConflictResolution]) -> List[Dict[str, Any]]:
        """Generate high-level strategic recommendations"""
        recommendations = []

        # High-priority pattern-based recommendations
        for pattern in insight_patterns:
            if pattern.priority == 'high':
                recommendations.append({
                    'category': 'strategic_priority',
                    'title': f"Address {pattern.pattern_type.replace('_', ' ').title()}",
                    'description': pattern.insight,
                    'action_items': pattern.recommendations,
                    'supporting_evidence': f"Supported by {len(pattern.supporting_personas)} persona analyses",
                    'priority': pattern.priority,
                    'confidence': pattern.confidence
                })

        # Conflict resolution recommendations
        for resolution in conflict_resolutions:
            recommendations.append({
                'category': 'conflict_resolution',
                'title': f"Resolve {resolution.conflict_type.replace('_', ' ').title()}",
                'description': resolution.conflict_description,
                'action_items': [resolution.recommended_approach],
                'supporting_evidence': f"Conflict between {', '.join(resolution.personas_involved)}",
                'priority': 'high',
                'confidence': 0.7
            })

        # Implementation readiness recommendation
        recommendations.append({
            'category': 'implementation_readiness',
            'title': 'Ensure Implementation Readiness',
            'description': 'Prepare development team with comprehensive specifications and guidelines',
            'action_items': [
                'Create detailed component specifications',
                'Establish design system documentation',
                'Set up testing and quality assurance processes',
                'Plan phased implementation approach'
            ],
            'supporting_evidence': 'Based on comprehensive multi-persona analysis',
            'priority': 'medium',
            'confidence': 0.8
        })

        return recommendations

    def _calculate_confidence_analysis(self, persona_results: Dict[str, Any],
                                     insight_patterns: List[InsightPattern]) -> Dict[str, Any]:
        """Calculate confidence metrics for the analysis"""
        total_personas = len(persona_results)
        high_confidence_patterns = [p for p in insight_patterns if p.confidence >= 0.8]

        return {
            'overall_confidence': sum(p.confidence for p in insight_patterns) / len(insight_patterns) if insight_patterns else 0,
            'persona_coverage': total_personas / 11,  # Assuming 11 total personas
            'high_confidence_insights': len(high_confidence_patterns),
            'consensus_strength': sum(len(p.supporting_personas) for p in insight_patterns) / (len(insight_patterns) * total_personas) if insight_patterns and total_personas else 0,
            'analysis_completeness': total_personas / 11 * 100  # Percentage of personas analyzed
        }

    def _generate_priority_matrix(self, insight_patterns: List[InsightPattern],
                                strategic_recommendations: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Generate priority matrix for insights and recommendations"""
        priority_matrix = {
            'high': [],
            'medium': [],
            'low': []
        }

        # Add patterns to matrix
        for pattern in insight_patterns:
            priority_matrix[pattern.priority].append({
                'type': 'insight_pattern',
                'title': pattern.pattern_type.replace('_', ' ').title(),
                'confidence': pattern.confidence,
                'supporting_personas': len(pattern.supporting_personas)
            })

        # Add strategic recommendations to matrix
        for rec in strategic_recommendations:
            priority = rec.get('priority', 'medium')
            priority_matrix[priority].append({
                'type': 'strategic_recommendation',
                'title': rec['title'],
                'confidence': rec.get('confidence', 0.7),
                'category': rec['category']
            })

        return priority_matrix

    def _generate_implementation_roadmap(self, strategic_recommendations: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Generate phased implementation roadmap"""
        roadmap = {
            'phase_1_foundation': [],
            'phase_2_core_features': [],
            'phase_3_optimization': []
        }

        # Sort recommendations by priority and assign to phases
        high_priority = [r for r in strategic_recommendations if r.get('priority') == 'high']
        medium_priority = [r for r in strategic_recommendations if r.get('priority') == 'medium']
        low_priority = [r for r in strategic_recommendations if r.get('priority') == 'low']

        # Phase 1: High-priority items
        roadmap['phase_1_foundation'] = [
            {
                'title': rec['title'],
                'category': rec['category'],
                'estimated_effort': 'high' if rec['category'] == 'conflict_resolution' else 'medium'
            } for rec in high_priority
        ]

        # Phase 2: Medium-priority items
        roadmap['phase_2_core_features'] = [
            {
                'title': rec['title'],
                'category': rec['category'],
                'estimated_effort': 'medium'
            } for rec in medium_priority
        ]

        # Phase 3: Low-priority and optimization items
        roadmap['phase_3_optimization'] = [
            {
                'title': rec['title'],
                'category': rec['category'],
                'estimated_effort': 'low'
            } for rec in low_priority
        ]

        return roadmap

    def validate_analysis_quality(self, cross_insights: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the quality and completeness of cross-insights analysis"""
        quality_metrics = {
            'completeness_score': 0,
            'confidence_score': cross_insights.get('confidence_analysis', {}).get('overall_confidence', 0),
            'insights_depth': len(cross_insights.get('insight_patterns', [])),
            'strategic_value': len(cross_insights.get('strategic_recommendations', [])),
            'validation_notes': []
        }

        # Check completeness
        required_sections = ['common_themes', 'insight_patterns', 'strategic_recommendations', 'priority_matrix']
        present_sections = sum(1 for section in required_sections if section in cross_insights and cross_insights[section])
        quality_metrics['completeness_score'] = present_sections / len(required_sections)

        # Add validation notes
        if quality_metrics['completeness_score'] < 0.8:
            quality_metrics['validation_notes'].append('Analysis may be incomplete - some sections missing')

        if quality_metrics['confidence_score'] < 0.6:
            quality_metrics['validation_notes'].append('Low confidence score - consider additional persona analysis')

        if quality_metrics['insights_depth'] < 3:
            quality_metrics['validation_notes'].append('Limited insight patterns identified - may need deeper analysis')

        return quality_metrics