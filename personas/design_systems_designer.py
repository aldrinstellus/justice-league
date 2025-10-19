"""
Design Systems Designer Persona Analyzer
Analyzes design files from a design systems perspective
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class ComponentAnalysis:
    """Analysis of a design component"""
    name: str
    usage_count: int
    variants: List[str]
    consistency_score: float
    scalability_issues: List[str]
    recommendations: List[str]


@dataclass
class DesignToken:
    """Represents a design token"""
    name: str
    value: str
    category: str
    usage_locations: List[str]
    consistency: float


class DesignSystemsDesignerAnalyzer:
    """Analyzes design files from a design systems designer perspective"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def analyze(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform design systems analysis

        Args:
            extracted_data: Extracted Penpot file data
            components: Detected UI components

        Returns:
            Design systems analysis results
        """
        self.logger.info("Starting Design Systems Designer analysis")

        try:
            analysis_results = {
                'component_library_audit': self._audit_component_library(extracted_data, components),
                'design_language_analysis': self._analyze_design_language(extracted_data),
                'design_token_analysis': self._analyze_design_tokens(extracted_data),
                'component_consistency': self._analyze_component_consistency(extracted_data, components),
                'scalability_assessment': self._assess_scalability(extracted_data, components),
                'design_system_maturity': self._assess_design_system_maturity(extracted_data, components),
                'reusability_opportunities': self._identify_reusability_opportunities(extracted_data, components),
                'naming_conventions': self._analyze_naming_conventions(extracted_data, components),
                'visual_hierarchy_analysis': self._analyze_visual_hierarchy(extracted_data),
                'improvement_recommendations': self._generate_design_system_recommendations(extracted_data, components)
            }

            self.logger.info("Design Systems Designer analysis completed")
            return analysis_results

        except Exception as e:
            self.logger.error(f"Design Systems Designer analysis failed: {str(e)}")
            raise

    def _audit_component_library(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Audit the existing component library"""
        component_inventory = components.get('component_inventory', {}).get('components', {})

        audit = {
            'total_components': len(component_inventory),
            'reusable_components': [],
            'one_off_components': [],
            'component_categories': defaultdict(list),
            'missing_variants': [],
            'component_health_score': 0.0
        }

        # Analyze each component
        for comp_name, usage_count in component_inventory.items():
            component_analysis = ComponentAnalysis(
                name=comp_name,
                usage_count=usage_count,
                variants=self._identify_component_variants(comp_name, extracted_data),
                consistency_score=self._calculate_component_consistency(comp_name, extracted_data),
                scalability_issues=self._identify_scalability_issues(comp_name, extracted_data),
                recommendations=self._generate_component_recommendations(comp_name, usage_count)
            )

            if usage_count > 1:
                audit['reusable_components'].append({
                    'name': comp_name,
                    'usage_count': usage_count,
                    'variants': component_analysis.variants,
                    'consistency_score': component_analysis.consistency_score,
                    'category': self._categorize_component(comp_name)
                })
            else:
                audit['one_off_components'].append(comp_name)

            # Categorize components
            category = self._categorize_component(comp_name)
            audit['component_categories'][category].append(comp_name)

        # Calculate overall health score
        if audit['reusable_components']:
            total_consistency = sum(comp['consistency_score'] for comp in audit['reusable_components'])
            audit['component_health_score'] = total_consistency / len(audit['reusable_components'])

        # Identify missing variants
        audit['missing_variants'] = self._identify_missing_variants(audit['reusable_components'])

        return audit

    def _analyze_design_language(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the overall design language consistency"""

        design_language = {
            'visual_consistency': {
                'color_usage': self._analyze_color_consistency(extracted_data),
                'typography_usage': self._analyze_typography_consistency(extracted_data),
                'spacing_patterns': self._analyze_spacing_patterns(extracted_data),
                'border_radius_usage': self._analyze_border_radius_consistency(extracted_data)
            },
            'component_relationships': {
                'hierarchy_clarity': self._assess_hierarchy_clarity(extracted_data),
                'composition_patterns': self._identify_composition_patterns(extracted_data),
                'interaction_consistency': self._analyze_interaction_consistency(extracted_data)
            },
            'brand_alignment': {
                'color_palette_adherence': self._assess_color_palette_adherence(extracted_data),
                'typography_scale_usage': self._assess_typography_scale_usage(extracted_data),
                'visual_style_consistency': self._assess_visual_style_consistency(extracted_data)
            }
        }

        return design_language

    def _analyze_design_tokens(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze design tokens usage and opportunities"""

        tokens_analysis = {
            'existing_tokens': {
                'colors': self._extract_color_tokens(extracted_data),
                'typography': self._extract_typography_tokens(extracted_data),
                'spacing': self._extract_spacing_tokens(extracted_data),
                'shadows': self._extract_shadow_tokens(extracted_data)
            },
            'token_opportunities': {
                'colors_to_tokenize': self._identify_color_tokenization_opportunities(extracted_data),
                'spacing_to_tokenize': self._identify_spacing_tokenization_opportunities(extracted_data),
                'typography_to_tokenize': self._identify_typography_tokenization_opportunities(extracted_data)
            },
            'token_usage_consistency': self._calculate_token_usage_consistency(extracted_data),
            'recommended_token_structure': self._recommend_token_structure(extracted_data)
        }

        return tokens_analysis

    def _analyze_component_consistency(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze consistency across similar components"""

        consistency_analysis = {
            'button_consistency': self._analyze_button_consistency(extracted_data),
            'input_consistency': self._analyze_input_consistency(extracted_data),
            'text_consistency': self._analyze_text_consistency(extracted_data),
            'layout_consistency': self._analyze_layout_consistency(extracted_data),
            'overall_consistency_score': 0.0,
            'inconsistency_hotspots': []
        }

        # Calculate overall consistency score
        consistency_scores = [
            consistency_analysis['button_consistency'].get('score', 0),
            consistency_analysis['input_consistency'].get('score', 0),
            consistency_analysis['text_consistency'].get('score', 0),
            consistency_analysis['layout_consistency'].get('score', 0)
        ]

        consistency_analysis['overall_consistency_score'] = sum(consistency_scores) / len(consistency_scores)

        # Identify hotspots
        consistency_analysis['inconsistency_hotspots'] = self._identify_inconsistency_hotspots(extracted_data)

        return consistency_analysis

    def _assess_scalability(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Assess design system scalability"""

        scalability_assessment = {
            'current_scalability_level': self._determine_scalability_level(extracted_data, components),
            'component_composition': {
                'atomic_components': self._identify_atomic_components(extracted_data, components),
                'molecular_components': self._identify_molecular_components(extracted_data, components),
                'organism_components': self._identify_organism_components(extracted_data, components)
            },
            'extensibility_analysis': {
                'easy_to_extend': [],
                'difficult_to_extend': [],
                'extension_recommendations': []
            },
            'multi_brand_readiness': self._assess_multi_brand_readiness(extracted_data),
            'responsive_scalability': self._assess_responsive_scalability(extracted_data)
        }

        return scalability_assessment

    def _assess_design_system_maturity(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the maturity level of the design system"""

        maturity_levels = {
            'Level 1': 'Ad-hoc styles',
            'Level 2': 'Component library',
            'Level 3': 'Design system',
            'Level 4': 'Systematic design',
            'Level 5': 'Optimized system'
        }

        current_level = self._determine_maturity_level(extracted_data, components)

        maturity_assessment = {
            'current_level': current_level,
            'current_level_description': maturity_levels[current_level],
            'maturity_indicators': {
                'has_consistent_components': len(components.get('component_inventory', {}).get('reusable_components', [])) > 5,
                'uses_design_tokens': self._has_design_tokens(extracted_data),
                'has_naming_conventions': self._has_naming_conventions(extracted_data, components),
                'documentation_present': self._has_documentation_indicators(extracted_data),
                'systematic_spacing': self._has_systematic_spacing(extracted_data)
            },
            'next_level_requirements': self._get_next_level_requirements(current_level),
            'improvement_roadmap': self._create_maturity_roadmap(current_level, extracted_data, components)
        }

        return maturity_assessment

    # Helper methods for component analysis
    def _identify_component_variants(self, comp_name: str, extracted_data: Dict[str, Any]) -> List[str]:
        """Identify variants of a component"""
        variants = []

        # Look for common variant patterns
        if 'button' in comp_name.lower():
            variants = ['primary', 'secondary', 'tertiary', 'ghost', 'danger']
        elif 'input' in comp_name.lower():
            variants = ['default', 'error', 'success', 'disabled', 'focused']
        elif 'text' in comp_name.lower():
            variants = ['heading', 'body', 'caption', 'label']

        return variants

    def _calculate_component_consistency(self, comp_name: str, extracted_data: Dict[str, Any]) -> float:
        """Calculate consistency score for a component"""
        # Placeholder implementation - would analyze actual component instances
        # for styling consistency across usage
        base_score = 0.8

        # Penalize if component name suggests inconsistency
        if 'copy' in comp_name.lower() or 'duplicate' in comp_name.lower():
            base_score -= 0.2

        # Bonus for systematic naming
        if comp_name.startswith('V1-'):
            base_score += 0.1

        return min(1.0, max(0.0, base_score))

    def _categorize_component(self, comp_name: str) -> str:
        """Categorize component by type"""
        name_lower = comp_name.lower()

        if 'button' in name_lower:
            return 'Interactive'
        elif any(term in name_lower for term in ['input', 'field', 'form']):
            return 'Form Controls'
        elif any(term in name_lower for term in ['text', 'heading', 'label']):
            return 'Typography'
        elif any(term in name_lower for term in ['table', 'list', 'grid']):
            return 'Data Display'
        elif any(term in name_lower for term in ['card', 'container', 'wrapper']):
            return 'Layout'
        elif any(term in name_lower for term in ['nav', 'menu', 'breadcrumb']):
            return 'Navigation'
        else:
            return 'Other'

    def _identify_missing_variants(self, reusable_components: List[Dict]) -> List[Dict]:
        """Identify missing component variants"""
        missing_variants = []

        for component in reusable_components:
            comp_name = component['name']
            existing_variants = component.get('variants', [])

            if 'button' in comp_name.lower():
                expected_variants = ['primary', 'secondary', 'disabled', 'loading']
                missing = [v for v in expected_variants if v not in existing_variants]
                if missing:
                    missing_variants.append({
                        'component': comp_name,
                        'missing_variants': missing
                    })

        return missing_variants

    def _analyze_color_consistency(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze color usage consistency"""
        colors_found = []

        # Extract colors from all objects
        for file_data in extracted_data.get('files', {}).values():
            for page_data in file_data.get('pages', {}).values():
                for obj_data in page_data.get('objects', {}).values():
                    # Look for fill colors
                    fills = obj_data.get('fills', [])
                    for fill in fills:
                        if isinstance(fill, dict) and fill.get('color'):
                            colors_found.append(fill['color'])

        # Analyze color consistency
        unique_colors = list(set(colors_found))
        color_frequency = {color: colors_found.count(color) for color in unique_colors}

        return {
            'total_unique_colors': len(unique_colors),
            'most_used_colors': sorted(color_frequency.items(), key=lambda x: x[1], reverse=True)[:10],
            'color_consistency_score': min(1.0, 10 / max(1, len(unique_colors))),  # Prefer fewer unique colors
            'recommended_palette': self._recommend_color_palette(unique_colors, color_frequency)
        }

    def _analyze_typography_consistency(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze typography usage consistency"""
        font_families = []
        font_sizes = []

        # Extract typography information
        for file_data in extracted_data.get('files', {}).values():
            for page_data in file_data.get('pages', {}).values():
                for obj_data in page_data.get('objects', {}).values():
                    if obj_data.get('type') == 'text':
                        # Extract font family
                        font_family = obj_data.get('fontFamily', '')
                        if font_family:
                            font_families.append(font_family)

                        # Extract font size
                        font_size = obj_data.get('fontSize', 0)
                        if font_size:
                            font_sizes.append(font_size)

        unique_families = list(set(font_families))
        unique_sizes = sorted(list(set(font_sizes)))

        return {
            'font_families_used': unique_families,
            'font_sizes_used': unique_sizes,
            'typography_consistency_score': self._calculate_typography_consistency_score(unique_families, unique_sizes),
            'recommended_type_scale': self._recommend_type_scale(unique_sizes)
        }

    def _calculate_typography_consistency_score(self, families: List[str], sizes: List[int]) -> float:
        """Calculate typography consistency score"""
        # Prefer 2-3 font families max
        family_score = 1.0 if len(families) <= 3 else max(0.0, 1.0 - (len(families) - 3) * 0.2)

        # Prefer systematic size scale (fewer unique sizes)
        size_score = 1.0 if len(sizes) <= 8 else max(0.0, 1.0 - (len(sizes) - 8) * 0.1)

        return (family_score + size_score) / 2

    def _determine_maturity_level(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> str:
        """Determine current design system maturity level"""
        indicators = {
            'has_reusable_components': len(components.get('component_inventory', {}).get('reusable_components', [])) > 3,
            'has_naming_conventions': self._has_naming_conventions(extracted_data, components),
            'has_consistent_colors': self._has_consistent_colors(extracted_data),
            'has_systematic_spacing': self._has_systematic_spacing(extracted_data),
            'has_design_tokens': self._has_design_tokens(extracted_data)
        }

        true_count = sum(indicators.values())

        if true_count >= 4:
            return 'Level 3'  # Design system
        elif true_count >= 2:
            return 'Level 2'  # Component library
        else:
            return 'Level 1'  # Ad-hoc styles

    def _has_naming_conventions(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> bool:
        """Check if naming conventions are used"""
        component_names = list(components.get('component_inventory', {}).get('components', {}).keys())

        # Check for systematic naming patterns
        systematic_patterns = ['V1-', 'btn-', 'input-', 'text-']
        has_systematic = any(
            any(pattern in name for pattern in systematic_patterns)
            for name in component_names
        )

        return has_systematic

    def _has_consistent_colors(self, extracted_data: Dict[str, Any]) -> bool:
        """Check if colors are used consistently"""
        color_analysis = self._analyze_color_consistency(extracted_data)
        return color_analysis['color_consistency_score'] > 0.7

    def _has_systematic_spacing(self, extracted_data: Dict[str, Any]) -> bool:
        """Check if spacing follows a system"""
        # This would analyze actual spacing values in a real implementation
        return True  # Placeholder

    def _has_design_tokens(self, extracted_data: Dict[str, Any]) -> bool:
        """Check if design tokens are being used"""
        # Look for evidence of design tokens
        manifest = extracted_data.get('manifest', {})
        features = manifest.get('files', [{}])[0].get('features', [])
        return 'design-tokens/v1' in features

    def _get_next_level_requirements(self, current_level: str) -> List[str]:
        """Get requirements for reaching the next maturity level"""
        requirements = {
            'Level 1': [
                'Create reusable component library',
                'Establish naming conventions',
                'Define color palette'
            ],
            'Level 2': [
                'Implement design tokens',
                'Create component variants',
                'Establish spacing system',
                'Document component guidelines'
            ],
            'Level 3': [
                'Optimize component APIs',
                'Implement multi-brand theming',
                'Advanced composition patterns',
                'Performance optimization'
            ]
        }

        return requirements.get(current_level, [])

    def _generate_design_system_recommendations(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate design system improvement recommendations"""
        recommendations = []

        # Component library recommendations
        component_inventory = components.get('component_inventory', {})
        reusable_count = len(component_inventory.get('reusable_components', []))

        if reusable_count < 5:
            recommendations.append({
                'category': 'Component Library',
                'priority': 'High',
                'title': 'Expand Reusable Component Library',
                'description': f'Currently only {reusable_count} reusable components. Aim for 10+ core components.',
                'impact': 'High - Improves consistency and development speed',
                'effort': 'Medium',
                'implementation_steps': [
                    'Audit existing one-off components for reusability',
                    'Create standardized button, input, and text components',
                    'Define component variant system'
                ]
            })

        # Design tokens recommendation
        if not self._has_design_tokens(extracted_data):
            recommendations.append({
                'category': 'Design Tokens',
                'priority': 'High',
                'title': 'Implement Design Token System',
                'description': 'Establish design tokens for colors, typography, and spacing',
                'impact': 'High - Enables theming and maintains consistency',
                'effort': 'High',
                'implementation_steps': [
                    'Define color token structure',
                    'Create typography scale tokens',
                    'Establish spacing system tokens',
                    'Implement token usage in components'
                ]
            })

        # Consistency recommendations
        color_analysis = self._analyze_color_consistency(extracted_data)
        if color_analysis['color_consistency_score'] < 0.7:
            recommendations.append({
                'category': 'Visual Consistency',
                'priority': 'Medium',
                'title': 'Improve Color Consistency',
                'description': f'Found {color_analysis["total_unique_colors"]} unique colors. Consolidate to a defined palette.',
                'impact': 'Medium - Improves brand consistency',
                'effort': 'Medium',
                'implementation_steps': [
                    'Define primary color palette (8-12 colors)',
                    'Audit and replace inconsistent color usage',
                    'Create color usage guidelines'
                ]
            })

        return recommendations

    # Placeholder implementations for additional analysis methods
    def _analyze_spacing_patterns(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze spacing patterns - placeholder implementation"""
        return {
            'consistent_spacing_usage': True,
            'spacing_scale_detected': ['4px', '8px', '12px', '16px', '20px', '24px', '32px'],
            'spacing_consistency_score': 0.85
        }

    def _analyze_border_radius_consistency(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze border radius consistency - placeholder implementation"""
        return {
            'border_radius_values': ['0px', '4px', '6px', '8px'],
            'consistency_score': 0.9
        }

    def _extract_color_tokens(self, extracted_data: Dict[str, Any]) -> List[DesignToken]:
        """Extract color tokens - placeholder implementation"""
        return [
            DesignToken('primary-blue', '#3b82f6', 'color', ['buttons', 'links'], 0.9),
            DesignToken('neutral-gray', '#64748b', 'color', ['text', 'borders'], 0.8)
        ]

    def _extract_typography_tokens(self, extracted_data: Dict[str, Any]) -> List[DesignToken]:
        """Extract typography tokens - placeholder implementation"""
        return [
            DesignToken('font-family-primary', 'DM Sans', 'typography', ['headings', 'body'], 0.95),
            DesignToken('font-size-base', '16px', 'typography', ['body-text'], 1.0)
        ]

    def _extract_spacing_tokens(self, extracted_data: Dict[str, Any]) -> List[DesignToken]:
        """Extract spacing tokens - placeholder implementation"""
        return [
            DesignToken('spacing-base', '16px', 'spacing', ['margins', 'padding'], 0.9),
            DesignToken('spacing-small', '8px', 'spacing', ['tight-spacing'], 0.8)
        ]

    def _extract_shadow_tokens(self, extracted_data: Dict[str, Any]) -> List[DesignToken]:
        """Extract shadow tokens - placeholder implementation"""
        return [
            DesignToken('shadow-sm', '0 1px 3px rgba(0,0,0,0.1)', 'shadow', ['cards'], 0.8)
        ]

    def _recommend_color_palette(self, colors: List[str], frequency: Dict[str, int]) -> List[str]:
        """Recommend optimized color palette"""
        # Return most frequently used colors as recommended palette
        sorted_colors = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        return [color for color, _ in sorted_colors[:8]]  # Recommend top 8 colors

    def _recommend_type_scale(self, sizes: List[int]) -> List[int]:
        """Recommend systematic typography scale"""
        # Return a systematic scale based on found sizes
        if not sizes:
            return [12, 14, 16, 18, 20, 24, 32, 48]

        base_size = 16  # Common base size
        return [int(base_size * (1.25 ** i)) for i in range(-2, 6)]  # Major third scale

    # Additional placeholder methods for complete analysis
    def _assess_hierarchy_clarity(self, extracted_data: Dict[str, Any]) -> float:
        """Assess visual hierarchy clarity - placeholder"""
        return 0.8

    def _identify_composition_patterns(self, extracted_data: Dict[str, Any]) -> List[str]:
        """Identify component composition patterns - placeholder"""
        return ['Card + Button composition', 'Form + Input composition']

    def _analyze_interaction_consistency(self, extracted_data: Dict[str, Any]) -> float:
        """Analyze interaction consistency - placeholder"""
        return 0.85

    def _identify_scalability_issues(self, comp_name: str, extracted_data: Dict[str, Any]) -> List[str]:
        """Identify component scalability issues - placeholder"""
        return [] if 'V1-' in comp_name else ['Inconsistent naming']

    def _generate_component_recommendations(self, comp_name: str, usage_count: int) -> List[str]:
        """Generate component-specific recommendations - placeholder"""
        if usage_count == 1:
            return ['Consider making this component reusable']
        elif usage_count > 10:
            return ['High usage - ensure variants are well-defined']
        return []

    # Continue with other placeholder methods as needed...