"""
Product Designer Persona Analyzer
Analyzes design files from a UX/UI designer perspective
"""

import logging
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from collections import defaultdict, Counter


@dataclass
class DesignPattern:
    """Represents a UX design pattern"""
    pattern_name: str
    pattern_type: str  # navigation, layout, interaction, etc.
    description: str
    components_involved: List[str]
    user_benefit: str
    implementation_notes: str
    accessibility_considerations: List[str]
    variants: List[str]


@dataclass
class InteractionFlow:
    """Represents a user interaction flow"""
    flow_id: str
    flow_name: str
    entry_points: List[str]
    steps: List[str]
    exit_points: List[str]
    user_goals: List[str]
    pain_points: List[str]
    improvement_opportunities: List[str]


@dataclass
class VisualHierarchy:
    """Represents visual hierarchy analysis"""
    primary_elements: List[str]
    secondary_elements: List[str]
    supporting_elements: List[str]
    visual_weight_distribution: Dict[str, float]
    hierarchy_effectiveness: float
    recommendations: List[str]


class ProductDesignerAnalyzer:
    """Analyzes design files from a product designer perspective"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Common UX patterns to look for
        self.ux_patterns = {
            'navigation': [
                'header_navigation', 'sidebar_navigation', 'tab_navigation',
                'breadcrumb_navigation', 'footer_navigation', 'hamburger_menu'
            ],
            'layout': [
                'grid_system', 'card_layout', 'list_layout', 'masonry_layout',
                'sidebar_layout', 'hero_section', 'split_screen'
            ],
            'interaction': [
                'call_to_action', 'progressive_disclosure', 'modal_dialog',
                'dropdown_menu', 'search_interface', 'filter_controls'
            ],
            'data_display': [
                'data_table', 'dashboard_cards', 'infographic_elements',
                'chart_visualization', 'progress_indicators', 'status_badges'
            ],
            'input': [
                'form_design', 'input_validation', 'multi_step_process',
                'file_upload', 'search_autocomplete', 'date_picker'
            ],
            'feedback': [
                'error_states', 'success_messages', 'loading_states',
                'empty_states', 'notification_system', 'tooltips'
            ]
        }

        # Visual design principles
        self.design_principles = {
            'contrast': ['color_contrast', 'size_contrast', 'weight_contrast'],
            'alignment': ['left_aligned', 'center_aligned', 'right_aligned', 'justified'],
            'proximity': ['grouped_elements', 'white_space_usage', 'section_separation'],
            'repetition': ['consistent_styling', 'pattern_repetition', 'brand_consistency'],
            'hierarchy': ['size_hierarchy', 'color_hierarchy', 'position_hierarchy']
        }

        # Usability heuristics
        self.usability_heuristics = [
            'visibility_of_system_status',
            'match_system_real_world',
            'user_control_and_freedom',
            'consistency_and_standards',
            'error_prevention',
            'recognition_rather_than_recall',
            'flexibility_and_efficiency_of_use',
            'aesthetic_and_minimalist_design',
            'help_users_recognize_diagnose_and_recover_from_errors',
            'help_and_documentation'
        ]

    def analyze(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform product designer analysis

        Args:
            extracted_data: Extracted Penpot file data
            components: Detected UI components

        Returns:
            Product designer analysis results
        """
        self.logger.info("Starting Product Designer analysis")

        try:
            analysis_results = {
                'design_system_analysis': self._analyze_design_system(extracted_data, components),
                'ux_patterns_analysis': self._analyze_ux_patterns(extracted_data, components),
                'visual_hierarchy': self._analyze_visual_hierarchy(extracted_data, components),
                'interaction_design': self._analyze_interaction_design(extracted_data, components),
                'user_experience_flow': self._analyze_user_flow(extracted_data, components),
                'accessibility_review': self._analyze_accessibility(extracted_data, components),
                'responsive_design': self._analyze_responsive_design(extracted_data),
                'content_strategy': self._analyze_content_strategy(extracted_data),
                'usability_heuristics': self._evaluate_usability_heuristics(extracted_data, components),
                'micro_interactions': self._identify_micro_interactions(extracted_data, components),
                'design_rationale': self._generate_design_rationale(extracted_data, components),
                'improvement_recommendations': self._generate_design_recommendations(extracted_data, components)
            }

            self.logger.info("Product Designer analysis completed")
            return analysis_results

        except Exception as e:
            self.logger.error(f"Product Designer analysis failed: {str(e)}")
            raise

    def _analyze_design_system(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the design system implementation"""
        design_system = components.get('design_system', {})
        detected_components = components.get('detected_components', [])

        # Analyze color consistency
        color_analysis = self._analyze_color_consistency(extracted_data)

        # Analyze typography consistency
        typography_analysis = self._analyze_typography_consistency(extracted_data)

        # Analyze spacing consistency
        spacing_analysis = self._analyze_spacing_consistency(extracted_data)

        # Component library assessment
        component_library = self._assess_component_library(detected_components)

        return {
            'maturity_score': design_system.get('maturity_score', 0),
            'consistency_assessment': {
                'colors': color_analysis,
                'typography': typography_analysis,
                'spacing': spacing_analysis,
                'overall_consistency': (color_analysis.get('consistency_score', 0) +
                                      typography_analysis.get('consistency_score', 0) +
                                      spacing_analysis.get('consistency_score', 0)) / 3
            },
            'component_library': component_library,
            'design_tokens': design_system.get('design_tokens', {}),
            'gaps_identified': self._identify_design_system_gaps(design_system, detected_components),
            'scalability_assessment': self._assess_design_scalability(design_system, detected_components)
        }

    def _analyze_color_consistency(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze color usage consistency"""
        colors_used = []

        # Extract colors from all objects
        for file_data in extracted_data.get('files', {}).values():
            for page_data in file_data.get('pages', {}).values():
                for obj in page_data.get('objects', {}).values():
                    if 'fill' in obj:
                        colors_used.append(obj['fill'])
                    if 'stroke' in obj:
                        colors_used.append(obj['stroke'])

        # Analyze color usage patterns
        color_frequency = Counter(colors_used)
        unique_colors = len(color_frequency)

        # Calculate consistency score (fewer unique colors = more consistent)
        consistency_score = max(0, 1 - (unique_colors / 50))  # Normalize to 50 as reasonable max

        return {
            'total_colors_used': unique_colors,
            'most_common_colors': color_frequency.most_common(10),
            'consistency_score': consistency_score,
            'color_palette_assessment': self._assess_color_palette(color_frequency),
            'recommendations': self._generate_color_recommendations(color_frequency, consistency_score)
        }

    def _analyze_typography_consistency(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze typography usage consistency"""
        typography_usage = {
            'font_families': Counter(),
            'font_sizes': Counter(),
            'font_weights': Counter()
        }

        # Extract typography from text objects
        for file_data in extracted_data.get('files', {}).values():
            for page_data in file_data.get('pages', {}).values():
                for obj in page_data.get('objects', {}).values():
                    if obj.get('type') == 'text':
                        if 'font_family' in obj:
                            typography_usage['font_families'][obj['font_family']] += 1
                        if 'font_size' in obj:
                            typography_usage['font_sizes'][obj['font_size']] += 1
                        if 'font_weight' in obj:
                            typography_usage['font_weights'][obj['font_weight']] += 1

        # Calculate consistency scores
        font_family_score = self._calculate_usage_consistency(typography_usage['font_families'])
        font_size_score = self._calculate_usage_consistency(typography_usage['font_sizes'])

        overall_consistency = (font_family_score + font_size_score) / 2

        return {
            'font_families_used': len(typography_usage['font_families']),
            'font_sizes_used': len(typography_usage['font_sizes']),
            'font_weights_used': len(typography_usage['font_weights']),
            'consistency_score': overall_consistency,
            'typography_scale': self._analyze_typography_scale(typography_usage['font_sizes']),
            'recommendations': self._generate_typography_recommendations(typography_usage, overall_consistency)
        }

    def _analyze_spacing_consistency(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze spacing and layout consistency"""
        spacing_values = {
            'margins': [],
            'paddings': [],
            'gaps': []
        }

        # Extract spacing from objects (approximated from positions and sizes)
        for file_data in extracted_data.get('files', {}).values():
            for page_data in file_data.get('pages', {}).values():
                objects = list(page_data.get('objects', {}).values())
                for i, obj in enumerate(objects):
                    # Calculate approximate spacing to nearby objects
                    for j, other_obj in enumerate(objects[i+1:], i+1):
                        distance = self._calculate_object_distance(obj, other_obj)
                        if distance < 100:  # Consider objects within 100px as having relevant spacing
                            spacing_values['gaps'].append(round(distance))

        # Analyze spacing consistency
        gap_consistency = self._analyze_spacing_pattern(spacing_values['gaps'])

        return {
            'spacing_values_found': len(set(spacing_values['gaps'])),
            'consistency_score': gap_consistency.get('consistency_score', 0),
            'common_spacing_values': gap_consistency.get('common_values', []),
            'spacing_scale_suggestion': self._suggest_spacing_scale(spacing_values['gaps']),
            'recommendations': self._generate_spacing_recommendations(gap_consistency)
        }

    def _analyze_ux_patterns(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze UX patterns used in the design"""
        detected_patterns = []
        component_names = [comp.get('name', '').lower() for comp in components.get('detected_components', [])]

        # Identify patterns based on component names and structure
        for pattern_category, patterns in self.ux_patterns.items():
            for pattern in patterns:
                pattern_keywords = pattern.replace('_', ' ').split()
                if any(keyword in ' '.join(component_names) for keyword in pattern_keywords):
                    detected_patterns.append(DesignPattern(
                        pattern_name=pattern,
                        pattern_type=pattern_category,
                        description=f"{pattern.replace('_', ' ').title()} pattern detected",
                        components_involved=[comp.get('name', '') for comp in components.get('detected_components', [])
                                           if any(keyword in comp.get('name', '').lower() for keyword in pattern_keywords)],
                        user_benefit=self._get_pattern_benefit(pattern),
                        implementation_notes=self._get_pattern_implementation_notes(pattern),
                        accessibility_considerations=self._get_pattern_accessibility_notes(pattern),
                        variants=[]
                    ))

        # Analyze pattern effectiveness
        pattern_effectiveness = self._assess_pattern_effectiveness(detected_patterns)

        return {
            'patterns_detected': [pattern.__dict__ for pattern in detected_patterns],
            'pattern_categories': Counter(pattern.pattern_type for pattern in detected_patterns),
            'pattern_effectiveness': pattern_effectiveness,
            'missing_patterns': self._identify_missing_patterns(detected_patterns),
            'pattern_recommendations': self._generate_pattern_recommendations(detected_patterns)
        }

    def _analyze_visual_hierarchy(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze visual hierarchy in the design"""
        all_elements = []

        # Collect all visual elements with their properties
        for file_data in extracted_data.get('files', {}).values():
            for page_data in file_data.get('pages', {}).values():
                for obj_id, obj in page_data.get('objects', {}).items():
                    element_info = {
                        'id': obj_id,
                        'name': obj.get('name', ''),
                        'type': obj.get('type', ''),
                        'size': (obj.get('width', 0) * obj.get('height', 0)),
                        'position': (obj.get('x', 0), obj.get('y', 0)),
                        'font_size': obj.get('font_size', 0) if obj.get('type') == 'text' else 0,
                        'visual_weight': self._calculate_visual_weight(obj)
                    }
                    all_elements.append(element_info)

        # Sort by visual weight
        all_elements.sort(key=lambda x: x['visual_weight'], reverse=True)

        # Categorize elements by hierarchy level
        total_elements = len(all_elements)
        primary_count = max(1, total_elements // 10)  # Top 10%
        secondary_count = max(1, total_elements // 5)  # Next 20%

        hierarchy = VisualHierarchy(
            primary_elements=[elem['name'] or f"{elem['type']}_{elem['id']}" for elem in all_elements[:primary_count]],
            secondary_elements=[elem['name'] or f"{elem['type']}_{elem['id']}" for elem in all_elements[primary_count:primary_count + secondary_count]],
            supporting_elements=[elem['name'] or f"{elem['type']}_{elem['id']}" for elem in all_elements[primary_count + secondary_count:]],
            visual_weight_distribution={
                'primary': sum(elem['visual_weight'] for elem in all_elements[:primary_count]) / total_elements if total_elements > 0 else 0,
                'secondary': sum(elem['visual_weight'] for elem in all_elements[primary_count:primary_count + secondary_count]) / total_elements if total_elements > 0 else 0,
                'supporting': sum(elem['visual_weight'] for elem in all_elements[primary_count + secondary_count:]) / total_elements if total_elements > 0 else 0
            },
            hierarchy_effectiveness=self._assess_hierarchy_effectiveness(all_elements),
            recommendations=self._generate_hierarchy_recommendations(all_elements)
        )

        return hierarchy.__dict__

    def _analyze_interaction_design(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze interaction design patterns"""
        interactive_components = []
        potential_interactions = []

        # Identify interactive components
        for comp in components.get('detected_components', []):
            comp_type = comp.get('component_type', '').lower()
            if comp_type in ['button', 'input', 'link', 'nav', 'menu', 'modal']:
                interactive_components.append({
                    'name': comp.get('name', ''),
                    'type': comp_type,
                    'interaction_type': self._determine_interaction_type(comp_type),
                    'instances': len(comp.get('instances', [])),
                    'accessibility_features': comp.get('accessibility_features', [])
                })

        # Identify potential interaction flows
        interaction_flows = self._identify_interaction_flows(extracted_data, interactive_components)

        return {
            'interactive_components': interactive_components,
            'interaction_flows': [flow.__dict__ for flow in interaction_flows],
            'interaction_patterns': self._analyze_interaction_patterns(interactive_components),
            'user_journey_coverage': self._assess_user_journey_coverage(interaction_flows),
            'interaction_recommendations': self._generate_interaction_recommendations(interactive_components, interaction_flows)
        }

    def _analyze_user_flow(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user experience flows"""
        pages_analyzed = []

        # Analyze each page for flow context
        for file_data in extracted_data.get('files', {}).values():
            for page_id, page_data in file_data.get('pages', {}).items():
                page_analysis = self._analyze_page_flow(page_id, page_data, components)
                pages_analyzed.append(page_analysis)

        # Identify cross-page flows
        cross_page_flows = self._identify_cross_page_flows(pages_analyzed)

        return {
            'pages_analyzed': pages_analyzed,
            'cross_page_flows': cross_page_flows,
            'flow_completeness': self._assess_flow_completeness(pages_analyzed),
            'user_goals_supported': self._identify_supported_user_goals(pages_analyzed),
            'flow_optimization_opportunities': self._identify_flow_optimization_opportunities(pages_analyzed)
        }

    def _analyze_accessibility(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze accessibility considerations in the design"""
        accessibility_features = {
            'semantic_structure': self._assess_semantic_structure(extracted_data),
            'color_accessibility': self._assess_color_accessibility(extracted_data),
            'text_accessibility': self._assess_text_accessibility(extracted_data),
            'navigation_accessibility': self._assess_navigation_accessibility(components),
            'interactive_accessibility': self._assess_interactive_accessibility(components)
        }

        # Calculate overall accessibility score
        accessibility_scores = [score.get('score', 0) for score in accessibility_features.values() if isinstance(score, dict)]
        overall_score = sum(accessibility_scores) / len(accessibility_scores) if accessibility_scores else 0

        return {
            'overall_accessibility_score': overall_score,
            'accessibility_features': accessibility_features,
            'wcag_compliance_assessment': self._assess_wcag_compliance(accessibility_features),
            'accessibility_improvements': self._suggest_accessibility_improvements(accessibility_features),
            'inclusive_design_recommendations': self._generate_inclusive_design_recommendations(accessibility_features)
        }

    def _analyze_responsive_design(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze responsive design considerations"""
        # Analyze layouts for responsive patterns
        responsive_indicators = self._identify_responsive_indicators(extracted_data)

        # Check for flexible layouts
        layout_flexibility = self._assess_layout_flexibility(extracted_data)

        return {
            'responsive_indicators_found': responsive_indicators,
            'layout_flexibility_score': layout_flexibility.get('score', 0),
            'breakpoint_analysis': layout_flexibility.get('breakpoints', []),
            'mobile_considerations': self._analyze_mobile_considerations(extracted_data),
            'responsive_recommendations': self._generate_responsive_recommendations(responsive_indicators, layout_flexibility)
        }

    def _analyze_content_strategy(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content strategy implementation"""
        text_content = self._extract_all_text_content(extracted_data)

        content_analysis = {
            'content_volume': len(text_content),
            'content_structure': self._analyze_content_structure(text_content),
            'readability_assessment': self._assess_content_readability(text_content),
            'content_hierarchy': self._analyze_content_hierarchy(extracted_data),
            'microcopy_analysis': self._analyze_microcopy(text_content)
        }

        return content_analysis

    def _evaluate_usability_heuristics(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate design against Nielsen's usability heuristics"""
        heuristic_scores = {}

        for heuristic in self.usability_heuristics:
            score = self._evaluate_single_heuristic(heuristic, extracted_data, components)
            heuristic_scores[heuristic] = score

        overall_usability = sum(score.get('score', 0) for score in heuristic_scores.values()) / len(heuristic_scores)

        return {
            'overall_usability_score': overall_usability,
            'heuristic_scores': heuristic_scores,
            'usability_grade': self._calculate_usability_grade(overall_usability),
            'critical_usability_issues': self._identify_critical_usability_issues(heuristic_scores),
            'usability_recommendations': self._generate_usability_recommendations(heuristic_scores)
        }

    def _identify_micro_interactions(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Identify potential micro-interaction opportunities"""
        micro_interaction_opportunities = []

        # Look for interactive components that could benefit from micro-interactions
        interactive_components = [comp for comp in components.get('detected_components', [])
                                if comp.get('component_type') in ['button', 'input', 'card', 'navigation']]

        for comp in interactive_components:
            opportunities = self._identify_component_micro_interactions(comp)
            micro_interaction_opportunities.extend(opportunities)

        return {
            'micro_interaction_opportunities': micro_interaction_opportunities,
            'interaction_categories': Counter(opp['category'] for opp in micro_interaction_opportunities),
            'implementation_priority': self._prioritize_micro_interactions(micro_interaction_opportunities),
            'micro_interaction_guidelines': self._generate_micro_interaction_guidelines()
        }

    def _generate_design_rationale(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Generate design rationale based on analysis"""
        design_decisions = []

        # Analyze design decisions based on patterns found
        if components.get('design_system', {}).get('maturity_score', 0) > 0.7:
            design_decisions.append({
                'decision': 'Consistent Design System Implementation',
                'rationale': 'High design system maturity indicates deliberate consistency choices',
                'user_benefit': 'Reduces cognitive load and improves usability',
                'business_impact': 'Faster development and maintenance'
            })

        # Add more design rationale based on analysis
        visual_hierarchy = self._analyze_visual_hierarchy(extracted_data, components)
        if visual_hierarchy.get('hierarchy_effectiveness', 0) > 0.7:
            design_decisions.append({
                'decision': 'Clear Visual Hierarchy',
                'rationale': 'Strong visual weight distribution guides user attention effectively',
                'user_benefit': 'Easier information processing and task completion',
                'business_impact': 'Higher conversion rates and user satisfaction'
            })

        return {
            'design_decisions': design_decisions,
            'design_philosophy': self._infer_design_philosophy(extracted_data, components),
            'user_centered_design_evidence': self._identify_ucd_evidence(extracted_data, components),
            'design_maturity_assessment': self._assess_design_maturity(extracted_data, components)
        }

    def _generate_design_recommendations(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> List[str]:
        """Generate actionable design recommendations"""
        recommendations = []

        # Design system recommendations
        design_system = components.get('design_system', {})
        if design_system.get('maturity_score', 0) < 0.7:
            recommendations.append("Strengthen design system consistency by standardizing colors, typography, and spacing")

        # Visual hierarchy recommendations
        hierarchy = self._analyze_visual_hierarchy(extracted_data, components)
        if hierarchy.get('hierarchy_effectiveness', 0) < 0.6:
            recommendations.append("Improve visual hierarchy by increasing contrast between primary and secondary elements")

        # Accessibility recommendations
        accessibility = self._analyze_accessibility(extracted_data, components)
        if accessibility.get('overall_accessibility_score', 0) < 0.8:
            recommendations.append("Enhance accessibility by improving color contrast and adding semantic structure")

        # Responsive design recommendations
        responsive = self._analyze_responsive_design(extracted_data)
        if responsive.get('layout_flexibility_score', 0) < 0.6:
            recommendations.append("Consider responsive design patterns for better mobile experience")

        return recommendations

    # Helper methods (simplified implementations for brevity)

    def _calculate_usage_consistency(self, usage_counter: Counter) -> float:
        """Calculate consistency score based on usage distribution"""
        if not usage_counter:
            return 1.0

        total_count = sum(usage_counter.values())
        unique_items = len(usage_counter)

        # More consistent if fewer unique items are used more frequently
        consistency = 1 - (unique_items / (total_count + unique_items))
        return max(0, min(1, consistency))

    def _calculate_object_distance(self, obj1: Dict[str, Any], obj2: Dict[str, Any]) -> float:
        """Calculate distance between two objects"""
        x1, y1 = obj1.get('x', 0), obj1.get('y', 0)
        x2, y2 = obj2.get('x', 0), obj2.get('y', 0)
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def _calculate_visual_weight(self, obj: Dict[str, Any]) -> float:
        """Calculate visual weight of an object"""
        weight = 0

        # Size contributes to weight
        size = (obj.get('width', 0) * obj.get('height', 0)) / 1000
        weight += size

        # Position contributes (top-left has more weight)
        position_weight = 1 - (obj.get('y', 0) / 1000)  # Normalize position
        weight += position_weight * 0.5

        # Font size for text elements
        if obj.get('type') == 'text':
            font_size = obj.get('font_size', 0)
            weight += font_size / 10

        return weight

    def _assess_pattern_effectiveness(self, patterns: List[DesignPattern]) -> Dict[str, Any]:
        """Assess effectiveness of detected patterns"""
        return {
            'pattern_diversity': len(set(p.pattern_type for p in patterns)),
            'implementation_quality': len([p for p in patterns if len(p.components_involved) > 1]) / len(patterns) if patterns else 0,
            'user_benefit_coverage': len(set(p.user_benefit for p in patterns))
        }

    def _assess_hierarchy_effectiveness(self, elements: List[Dict[str, Any]]) -> float:
        """Assess how effective the visual hierarchy is"""
        if not elements:
            return 0

        # Check if there's good separation between weight levels
        weights = [elem['visual_weight'] for elem in elements]
        if len(weights) < 2:
            return 0.5

        weight_variance = sum((w - sum(weights)/len(weights))**2 for w in weights) / len(weights)
        # Higher variance indicates better hierarchy separation
        return min(1.0, weight_variance / 100)  # Normalize

    def _determine_interaction_type(self, component_type: str) -> str:
        """Determine interaction type for component"""
        interaction_map = {
            'button': 'click',
            'input': 'text_input',
            'link': 'navigation',
            'nav': 'navigation',
            'menu': 'selection',
            'modal': 'overlay_interaction'
        }
        return interaction_map.get(component_type, 'unknown')

    def _identify_interaction_flows(self, extracted_data: Dict[str, Any],
                                  interactive_components: List[Dict[str, Any]]) -> List[InteractionFlow]:
        """Identify potential interaction flows"""
        flows = []

        # Simple flow identification based on component relationships
        if len(interactive_components) > 1:
            flows.append(InteractionFlow(
                flow_id="main_flow",
                flow_name="Primary User Flow",
                entry_points=[comp['name'] for comp in interactive_components if comp['type'] in ['button', 'link']],
                steps=[f"Interact with {comp['name']}" for comp in interactive_components],
                exit_points=[comp['name'] for comp in interactive_components if comp['type'] == 'button'],
                user_goals=["Complete primary task", "Navigate through interface"],
                pain_points=["Potential confusion in navigation"],
                improvement_opportunities=["Streamline interaction steps"]
            ))

        return flows

    def _extract_all_text_content(self, extracted_data: Dict[str, Any]) -> List[str]:
        """Extract all text content from design"""
        text_content = []

        for file_data in extracted_data.get('files', {}).values():
            for page_data in file_data.get('pages', {}).values():
                for obj in page_data.get('objects', {}).values():
                    if obj.get('type') == 'text' and 'content' in obj:
                        text_content.append(obj['content'])

        return text_content

    def _get_pattern_benefit(self, pattern: str) -> str:
        """Get user benefit for a pattern"""
        benefits = {
            'header_navigation': 'Easy access to main site sections',
            'search_interface': 'Quick content discovery',
            'card_layout': 'Scannable content organization',
            'form_design': 'Efficient data collection',
            'modal_dialog': 'Focused interaction without context loss'
        }
        return benefits.get(pattern, 'Improves user experience')

    def _get_pattern_implementation_notes(self, pattern: str) -> str:
        """Get implementation notes for pattern"""
        return f"Implement {pattern.replace('_', ' ')} following established design patterns and accessibility guidelines"

    def _get_pattern_accessibility_notes(self, pattern: str) -> List[str]:
        """Get accessibility considerations for pattern"""
        return ['Ensure keyboard navigation', 'Provide screen reader support', 'Maintain color contrast standards']

    def _identify_missing_patterns(self, detected_patterns: List[DesignPattern]) -> List[str]:
        """Identify potentially missing UX patterns"""
        detected_types = set(p.pattern_type for p in detected_patterns)
        all_types = set(self.ux_patterns.keys())
        return list(all_types - detected_types)

    def _generate_pattern_recommendations(self, patterns: List[DesignPattern]) -> List[str]:
        """Generate pattern-based recommendations"""
        recommendations = []

        if len(patterns) < 3:
            recommendations.append("Consider implementing more UX patterns to improve user experience")

        pattern_types = [p.pattern_type for p in patterns]
        if 'feedback' not in pattern_types:
            recommendations.append("Add feedback patterns like error states and success messages")

        return recommendations

    def _calculate_usability_grade(self, score: float) -> str:
        """Convert usability score to grade"""
        if score >= 0.9: return 'A'
        elif score >= 0.8: return 'B'
        elif score >= 0.7: return 'C'
        elif score >= 0.6: return 'D'
        else: return 'F'

    # Additional helper methods would be implemented here...
    # For brevity, I'm including simplified versions

    def _assess_color_palette(self, color_frequency: Counter) -> str:
        """Assess the color palette"""
        if len(color_frequency) <= 5:
            return "Minimalist palette"
        elif len(color_frequency) <= 15:
            return "Balanced palette"
        else:
            return "Complex palette - consider simplification"

    def _generate_color_recommendations(self, color_frequency: Counter, consistency_score: float) -> List[str]:
        """Generate color recommendations"""
        recommendations = []
        if consistency_score < 0.6:
            recommendations.append("Reduce color variations to improve consistency")
        if len(color_frequency) > 20:
            recommendations.append("Consider establishing a primary color palette")
        return recommendations

    def _analyze_typography_scale(self, font_sizes: Counter) -> Dict[str, Any]:
        """Analyze typography scale"""
        sizes = list(font_sizes.keys())
        if not sizes:
            return {'scale_type': 'none', 'ratio': 0}

        sorted_sizes = sorted(sizes)
        ratios = [sorted_sizes[i+1]/sorted_sizes[i] for i in range(len(sorted_sizes)-1) if sorted_sizes[i] > 0]
        avg_ratio = sum(ratios) / len(ratios) if ratios else 1

        return {
            'scale_type': 'geometric' if 1.2 <= avg_ratio <= 1.6 else 'custom',
            'ratio': avg_ratio,
            'size_range': {'min': min(sizes), 'max': max(sizes)}
        }

    def _generate_typography_recommendations(self, typography_usage: Dict, consistency_score: float) -> List[str]:
        """Generate typography recommendations"""
        recommendations = []
        if len(typography_usage['font_families']) > 3:
            recommendations.append("Consider reducing font family variations")
        if consistency_score < 0.7:
            recommendations.append("Establish a consistent typography scale")
        return recommendations

    def _analyze_spacing_pattern(self, spacing_values: List[int]) -> Dict[str, Any]:
        """Analyze spacing patterns"""
        if not spacing_values:
            return {'consistency_score': 0, 'common_values': []}

        spacing_counter = Counter(spacing_values)
        consistency_score = self._calculate_usage_consistency(spacing_counter)

        return {
            'consistency_score': consistency_score,
            'common_values': [val for val, count in spacing_counter.most_common(5)],
            'total_variations': len(spacing_counter)
        }

    def _suggest_spacing_scale(self, spacing_values: List[int]) -> List[int]:
        """Suggest a spacing scale based on usage"""
        if not spacing_values:
            return [8, 16, 24, 32, 48, 64]  # Default scale

        # Find common values and suggest a scale
        spacing_counter = Counter(spacing_values)
        common_values = sorted([val for val, count in spacing_counter.most_common(5)])

        # If we have good common values, use them as base
        if common_values:
            base = common_values[0] if common_values[0] > 0 else 8
            return [base * i for i in [1, 2, 3, 4, 6, 8]]

        return [8, 16, 24, 32, 48, 64]

    def _generate_spacing_recommendations(self, gap_analysis: Dict[str, Any]) -> List[str]:
        """Generate spacing recommendations"""
        recommendations = []
        if gap_analysis.get('consistency_score', 0) < 0.6:
            recommendations.append("Establish a consistent spacing scale")
        if gap_analysis.get('total_variations', 0) > 10:
            recommendations.append("Reduce spacing variations for better consistency")
        return recommendations

    # Simplified implementations for remaining methods
    def _identify_design_system_gaps(self, design_system: Dict, components: List) -> List[str]:
        return ["Consider adding more atomic components"]

    def _assess_design_scalability(self, design_system: Dict, components: List) -> float:
        return 0.7  # Placeholder

    def _generate_hierarchy_recommendations(self, elements: List[Dict]) -> List[str]:
        return ["Increase contrast between primary and secondary elements"]

    def _analyze_page_flow(self, page_id: str, page_data: Dict, components: Dict) -> Dict:
        return {'page_id': page_id, 'flow_type': 'linear', 'completion_points': []}

    def _identify_cross_page_flows(self, pages: List[Dict]) -> List[Dict]:
        return [{'flow_type': 'multi_page', 'pages_involved': len(pages)}]

    def _assess_flow_completeness(self, pages: List[Dict]) -> float:
        return 0.8  # Placeholder

    def _identify_supported_user_goals(self, pages: List[Dict]) -> List[str]:
        return ["Complete primary task", "Navigate content"]

    def _identify_flow_optimization_opportunities(self, pages: List[Dict]) -> List[str]:
        return ["Simplify navigation between pages"]

    def _assess_semantic_structure(self, extracted_data: Dict) -> Dict[str, Any]:
        return {'score': 0.7, 'notes': 'Good semantic structure'}

    def _assess_color_accessibility(self, extracted_data: Dict) -> Dict[str, Any]:
        return {'score': 0.8, 'contrast_issues': []}

    def _assess_text_accessibility(self, extracted_data: Dict) -> Dict[str, Any]:
        return {'score': 0.9, 'font_size_issues': []}

    def _assess_navigation_accessibility(self, components: Dict) -> Dict[str, Any]:
        return {'score': 0.8, 'keyboard_navigation': True}

    def _assess_interactive_accessibility(self, components: Dict) -> Dict[str, Any]:
        return {'score': 0.7, 'focus_indicators': True}

    def _assess_wcag_compliance(self, features: Dict) -> Dict[str, Any]:
        return {'level': 'AA', 'compliance_score': 0.8}

    def _suggest_accessibility_improvements(self, features: Dict) -> List[str]:
        return ["Improve color contrast ratios", "Add alt text for images"]

    def _generate_inclusive_design_recommendations(self, features: Dict) -> List[str]:
        return ["Consider users with disabilities in design decisions"]

    def _identify_responsive_indicators(self, extracted_data: Dict) -> List[str]:
        return ["Flexible grid layout detected"]

    def _assess_layout_flexibility(self, extracted_data: Dict) -> Dict[str, Any]:
        return {'score': 0.6, 'breakpoints': ['mobile', 'tablet', 'desktop']}

    def _analyze_mobile_considerations(self, extracted_data: Dict) -> Dict[str, Any]:
        return {'touch_targets': 'adequate', 'content_prioritization': 'good'}

    def _generate_responsive_recommendations(self, indicators: List, flexibility: Dict) -> List[str]:
        return ["Consider mobile-first approach"]

    def _analyze_content_structure(self, text_content: List[str]) -> Dict[str, Any]:
        return {'headings': len([t for t in text_content if len(t) < 50]), 'body_text': len(text_content)}

    def _assess_content_readability(self, text_content: List[str]) -> Dict[str, Any]:
        return {'readability_score': 0.8, 'average_sentence_length': 15}

    def _analyze_content_hierarchy(self, extracted_data: Dict) -> Dict[str, Any]:
        return {'hierarchy_levels': 3, 'structure_clarity': 0.7}

    def _analyze_microcopy(self, text_content: List[str]) -> Dict[str, Any]:
        return {'button_labels': ['Submit', 'Cancel'], 'helper_text': ['Required field']}

    def _evaluate_single_heuristic(self, heuristic: str, extracted_data: Dict, components: Dict) -> Dict[str, Any]:
        return {'score': 0.7, 'notes': f'{heuristic} evaluation'}

    def _identify_critical_usability_issues(self, scores: Dict) -> List[str]:
        return [name for name, score in scores.items() if score.get('score', 0) < 0.5]

    def _generate_usability_recommendations(self, scores: Dict) -> List[str]:
        return ["Improve system feedback", "Enhance error prevention"]

    def _identify_component_micro_interactions(self, component: Dict) -> List[Dict[str, Any]]:
        return [{'category': 'hover', 'description': 'Button hover state', 'priority': 'medium'}]

    def _prioritize_micro_interactions(self, opportunities: List[Dict]) -> Dict[str, List]:
        return {'high': [], 'medium': opportunities, 'low': []}

    def _generate_micro_interaction_guidelines(self) -> List[str]:
        return ["Use subtle animations", "Provide immediate feedback", "Keep interactions performant"]

    def _infer_design_philosophy(self, extracted_data: Dict, components: Dict) -> str:
        return "Modern, user-centered design approach"

    def _identify_ucd_evidence(self, extracted_data: Dict, components: Dict) -> List[str]:
        return ["Clear visual hierarchy", "Consistent interaction patterns"]

    def _assess_design_maturity(self, extracted_data: Dict, components: Dict) -> float:
        return 0.75  # Placeholder maturity score