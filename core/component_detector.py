#!/usr/bin/env python3
"""
Component Detector - Advanced UI component identification and classification
Analyzes Penpot extracted data to identify, classify, and catalog UI components
"""

import json
import logging
import re
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict, Counter
import uuid


@dataclass
class ComponentSignature:
    """Signature for identifying component patterns"""
    name_patterns: List[str]
    type_patterns: List[str]
    property_patterns: Dict[str, Any]
    structural_patterns: List[str]
    confidence_threshold: float


@dataclass
class DetectedComponent:
    """Represents a detected UI component"""
    id: str
    name: str
    component_type: str
    category: str
    instances: List[Dict[str, Any]]
    properties: Dict[str, Any]
    usage_pattern: str
    reusability_score: float
    complexity_score: float
    design_tokens: Dict[str, Any]
    relationships: List[str]
    accessibility_features: List[str]


class ComponentDetector:
    """
    Advanced component detection and classification system
    Identifies UI components, patterns, and design system elements
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Component type signatures for pattern matching
        self.component_signatures = self._initialize_component_signatures()

        # Design system categories
        self.design_categories = {
            'atoms': ['button', 'input', 'icon', 'text', 'image', 'divider'],
            'molecules': ['search-bar', 'form-field', 'card-header', 'navigation-item'],
            'organisms': ['header', 'footer', 'sidebar', 'form', 'card', 'modal', 'table'],
            'templates': ['layout', 'page', 'section', 'grid'],
            'pages': ['dashboard', 'profile', 'settings', 'login']
        }

        # Common UI patterns
        self.ui_patterns = {
            'navigation': ['nav', 'menu', 'breadcrumb', 'tab', 'pagination'],
            'data_display': ['table', 'list', 'grid', 'chart', 'card'],
            'input': ['form', 'button', 'input', 'select', 'checkbox', 'radio'],
            'feedback': ['alert', 'notification', 'tooltip', 'modal', 'toast'],
            'layout': ['header', 'footer', 'sidebar', 'container', 'section']
        }

    def detect_components(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main component detection entry point

        Args:
            extracted_data: Data from PenpotExtractor

        Returns:
            Comprehensive component analysis
        """
        self.logger.info("Starting component detection...")

        try:
            # Analyze all objects to identify potential components
            all_objects = self._collect_all_objects(extracted_data)

            # Detect individual components
            detected_components = self._detect_individual_components(all_objects)

            # Analyze component patterns and relationships
            component_patterns = self._analyze_component_patterns(detected_components)

            # Identify design system structure
            design_system = self._analyze_design_system(detected_components, component_patterns)

            # Extract design tokens
            design_tokens = self._extract_design_tokens(all_objects, detected_components)

            # Analyze component reusability
            reusability_analysis = self._analyze_reusability(detected_components)

            # Generate component catalog
            component_catalog = self._generate_component_catalog(detected_components, design_system)

            # Quality assessment
            quality_assessment = self._assess_component_quality(detected_components, design_system)

            component_analysis = {
                'summary': {
                    'total_objects_analyzed': len(all_objects),
                    'components_detected': len(detected_components),
                    'component_types': len(set(comp.component_type for comp in detected_components)),
                    'design_system_coverage': len(design_system.get('categories_found', [])),
                    'reusability_score': reusability_analysis.get('average_reusability', 0)
                },
                'detected_components': [comp.__dict__ for comp in detected_components],
                'component_patterns': component_patterns,
                'design_system': design_system,
                'design_tokens': design_tokens,
                'reusability_analysis': reusability_analysis,
                'component_catalog': component_catalog,
                'quality_assessment': quality_assessment,
                'recommendations': self._generate_component_recommendations(detected_components, design_system, quality_assessment)
            }

            self.logger.info(f"Detected {len(detected_components)} components across {len(design_system.get('categories_found', []))} design categories")
            return component_analysis

        except Exception as e:
            self.logger.error(f"Component detection failed: {str(e)}")
            raise

    def _initialize_component_signatures(self) -> Dict[str, ComponentSignature]:
        """Initialize component detection signatures"""
        return {
            'button': ComponentSignature(
                name_patterns=['btn', 'button', 'cta', 'action'],
                type_patterns=['rectangle', 'group'],
                property_patterns={'clickable': True, 'has_text': True},
                structural_patterns=['rounded_corners', 'background_fill'],
                confidence_threshold=0.7
            ),
            'input': ComponentSignature(
                name_patterns=['input', 'field', 'textbox', 'search'],
                type_patterns=['rectangle', 'text'],
                property_patterns={'editable': True, 'border': True},
                structural_patterns=['border', 'placeholder_text'],
                confidence_threshold=0.8
            ),
            'card': ComponentSignature(
                name_patterns=['card', 'tile', 'panel'],
                type_patterns=['group', 'rectangle'],
                property_patterns={'has_children': True, 'background': True},
                structural_patterns=['border', 'shadow', 'padding'],
                confidence_threshold=0.6
            ),
            'navigation': ComponentSignature(
                name_patterns=['nav', 'menu', 'tab', 'breadcrumb'],
                type_patterns=['group'],
                property_patterns={'has_multiple_items': True, 'horizontal_layout': True},
                structural_patterns=['list_structure', 'links'],
                confidence_threshold=0.7
            ),
            'modal': ComponentSignature(
                name_patterns=['modal', 'dialog', 'popup', 'overlay'],
                type_patterns=['group'],
                property_patterns={'overlay': True, 'centered': True},
                structural_patterns=['backdrop', 'close_button'],
                confidence_threshold=0.8
            )
        }

    def _collect_all_objects(self, extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Collect all objects from extracted data"""
        all_objects = []

        for file_id, file_data in extracted_data.get('files', {}).items():
            for page_id, page_data in file_data.get('pages', {}).items():
                for object_id, object_data in page_data.get('objects', {}).items():
                    # Enrich object with context
                    enriched_object = {
                        **object_data,
                        'context': {
                            'file_id': file_id,
                            'page_id': page_id,
                            'object_id': object_id
                        }
                    }
                    all_objects.append(enriched_object)

        return all_objects

    def _detect_individual_components(self, all_objects: List[Dict[str, Any]]) -> List[DetectedComponent]:
        """Detect individual components from objects"""
        detected_components = []
        processed_objects = set()

        # Group similar objects
        object_groups = self._group_similar_objects(all_objects)

        for group_id, objects in object_groups.items():
            if len(objects) < 1:  # Skip empty groups
                continue

            # Analyze group to determine if it's a component
            component_analysis = self._analyze_object_group(objects)

            if component_analysis['is_component']:
                component = DetectedComponent(
                    id=str(uuid.uuid4()),
                    name=component_analysis['suggested_name'],
                    component_type=component_analysis['type'],
                    category=component_analysis['category'],
                    instances=[obj['context'] for obj in objects],
                    properties=component_analysis['properties'],
                    usage_pattern=component_analysis['usage_pattern'],
                    reusability_score=component_analysis['reusability_score'],
                    complexity_score=component_analysis['complexity_score'],
                    design_tokens=component_analysis['design_tokens'],
                    relationships=[],
                    accessibility_features=component_analysis['accessibility_features']
                )
                detected_components.append(component)

                # Mark objects as processed
                for obj in objects:
                    processed_objects.add(obj['context']['object_id'])

        # Process remaining individual objects
        for obj in all_objects:
            if obj['context']['object_id'] not in processed_objects:
                individual_analysis = self._analyze_individual_object(obj)
                if individual_analysis['is_component']:
                    component = DetectedComponent(
                        id=str(uuid.uuid4()),
                        name=individual_analysis['suggested_name'],
                        component_type=individual_analysis['type'],
                        category=individual_analysis['category'],
                        instances=[obj['context']],
                        properties=individual_analysis['properties'],
                        usage_pattern='single_use',
                        reusability_score=0.1,
                        complexity_score=individual_analysis['complexity_score'],
                        design_tokens=individual_analysis['design_tokens'],
                        relationships=[],
                        accessibility_features=individual_analysis['accessibility_features']
                    )
                    detected_components.append(component)

        return detected_components

    def _group_similar_objects(self, all_objects: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group similar objects that might be the same component"""
        groups = defaultdict(list)

        for obj in all_objects:
            # Create signature based on object properties
            signature = self._create_object_signature(obj)
            groups[signature].append(obj)

        # Filter groups to only those with multiple instances or high component probability
        filtered_groups = {}
        for sig, objects in groups.items():
            if len(objects) > 1 or self._has_component_characteristics(objects[0]):
                filtered_groups[sig] = objects

        return filtered_groups

    def _create_object_signature(self, obj: Dict[str, Any]) -> str:
        """Create a signature for object grouping"""
        # Extract key properties for signature
        obj_type = obj.get('type', 'unknown')
        name = obj.get('name', '').lower()

        # Normalize name patterns
        name_normalized = re.sub(r'\d+', 'N', name)  # Replace numbers with N
        name_normalized = re.sub(r'[_-]+', '_', name_normalized)  # Normalize separators

        # Create signature from key properties
        signature_parts = [
            obj_type,
            name_normalized,
            str(obj.get('width', 0) // 10),  # Approximate width
            str(obj.get('height', 0) // 10)  # Approximate height
        ]

        return '_'.join(signature_parts)

    def _has_component_characteristics(self, obj: Dict[str, Any]) -> bool:
        """Check if single object has component characteristics"""
        name = obj.get('name', '').lower()
        obj_type = obj.get('type', '')

        # Check against component signatures
        for comp_type, signature in self.component_signatures.items():
            if any(pattern in name for pattern in signature.name_patterns):
                return True
            if obj_type in signature.type_patterns:
                return True

        return False

    def _analyze_object_group(self, objects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze a group of similar objects"""
        if not objects:
            return {'is_component': False}

        representative = objects[0]
        name = representative.get('name', 'unnamed')
        obj_type = representative.get('type', 'unknown')

        # Determine component type
        component_type = self._classify_component_type(representative)

        # Calculate reusability score based on instance count
        reusability_score = min(len(objects) / 10, 1.0)  # Max score of 1.0

        # Analyze complexity
        complexity_score = self._calculate_complexity_score(representative)

        # Extract design tokens
        design_tokens = self._extract_object_design_tokens(representative)

        # Determine usage pattern
        usage_pattern = self._determine_usage_pattern(objects)

        # Check accessibility features
        accessibility_features = self._detect_accessibility_features(representative)

        return {
            'is_component': True,
            'suggested_name': self._suggest_component_name(name, component_type),
            'type': component_type,
            'category': self._categorize_component(component_type),
            'properties': self._extract_component_properties(representative),
            'usage_pattern': usage_pattern,
            'reusability_score': reusability_score,
            'complexity_score': complexity_score,
            'design_tokens': design_tokens,
            'accessibility_features': accessibility_features
        }

    def _analyze_individual_object(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze individual object for component potential"""
        name = obj.get('name', '').lower()

        # Check if it matches any component signatures
        for comp_type, signature in self.component_signatures.items():
            if any(pattern in name for pattern in signature.name_patterns):
                return {
                    'is_component': True,
                    'suggested_name': self._suggest_component_name(name, comp_type),
                    'type': comp_type,
                    'category': self._categorize_component(comp_type),
                    'properties': self._extract_component_properties(obj),
                    'complexity_score': self._calculate_complexity_score(obj),
                    'design_tokens': self._extract_object_design_tokens(obj),
                    'accessibility_features': self._detect_accessibility_features(obj)
                }

        return {'is_component': False}

    def _classify_component_type(self, obj: Dict[str, Any]) -> str:
        """Classify the type of component"""
        name = obj.get('name', '').lower()
        obj_type = obj.get('type', '')

        # Check against known patterns
        for comp_type, signature in self.component_signatures.items():
            score = 0

            # Check name patterns
            for pattern in signature.name_patterns:
                if pattern in name:
                    score += 0.4

            # Check type patterns
            if obj_type in signature.type_patterns:
                score += 0.3

            if score >= signature.confidence_threshold:
                return comp_type

        # Fallback classification
        if 'button' in name or 'btn' in name:
            return 'button'
        elif 'input' in name or 'field' in name:
            return 'input'
        elif 'card' in name or 'panel' in name:
            return 'card'
        else:
            return obj_type or 'component'

    def _categorize_component(self, component_type: str) -> str:
        """Categorize component using atomic design methodology"""
        for category, types in self.design_categories.items():
            if component_type in types:
                return category
        return 'molecules'  # Default category

    def _suggest_component_name(self, original_name: str, component_type: str) -> str:
        """Suggest a clean component name"""
        # Remove common prefixes/suffixes
        cleaned = re.sub(r'^(v\d+[-_]?|component[-_]?|comp[-_]?)', '', original_name, flags=re.IGNORECASE)
        cleaned = re.sub(r'[-_]\d+$', '', cleaned)  # Remove trailing numbers

        # If name is too generic, use component type
        if not cleaned or len(cleaned) < 2:
            return component_type.title()

        # Convert to proper case
        return cleaned.replace('_', ' ').replace('-', ' ').title()

    def _extract_component_properties(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant properties from object"""
        return {
            'type': obj.get('type'),
            'width': obj.get('width'),
            'height': obj.get('height'),
            'name': obj.get('name'),
            'visible': obj.get('visible', True),
            'locked': obj.get('locked', False),
            'has_children': bool(obj.get('children')),
            'position': {
                'x': obj.get('x', 0),
                'y': obj.get('y', 0)
            }
        }

    def _calculate_complexity_score(self, obj: Dict[str, Any]) -> float:
        """Calculate component complexity score"""
        score = 0.1  # Base score

        # Add complexity for children
        children = obj.get('children', [])
        score += len(children) * 0.1

        # Add complexity for properties
        properties = obj.get('properties', {})
        score += len(properties) * 0.05

        # Cap at 1.0
        return min(score, 1.0)

    def _extract_object_design_tokens(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Extract design tokens from object"""
        tokens = {}

        # Colors
        if 'fill' in obj:
            tokens['colors'] = {'fill': obj['fill']}
        if 'stroke' in obj:
            tokens.setdefault('colors', {})['stroke'] = obj['stroke']

        # Typography
        if obj.get('type') == 'text':
            tokens['typography'] = {
                'font_family': obj.get('font_family'),
                'font_size': obj.get('font_size'),
                'font_weight': obj.get('font_weight'),
                'line_height': obj.get('line_height')
            }

        # Spacing
        tokens['spacing'] = {
            'width': obj.get('width'),
            'height': obj.get('height')
        }

        # Effects
        if 'shadow' in obj or 'blur' in obj:
            tokens['effects'] = {
                'shadow': obj.get('shadow'),
                'blur': obj.get('blur')
            }

        return tokens

    def _determine_usage_pattern(self, objects: List[Dict[str, Any]]) -> str:
        """Determine how the component is typically used"""
        if len(objects) > 10:
            return 'heavily_reused'
        elif len(objects) > 3:
            return 'moderately_reused'
        elif len(objects) > 1:
            return 'lightly_reused'
        else:
            return 'single_use'

    def _detect_accessibility_features(self, obj: Dict[str, Any]) -> List[str]:
        """Detect accessibility features in component"""
        features = []

        name = obj.get('name', '').lower()

        # Check for accessibility hints in naming
        if 'alt' in name or 'aria' in name:
            features.append('aria_labels')
        if 'role' in name:
            features.append('semantic_roles')
        if 'focus' in name:
            features.append('focus_management')

        # Check object properties for accessibility indicators
        if obj.get('visible') is False:
            features.append('screen_reader_only')

        return features

    def _analyze_component_patterns(self, components: List[DetectedComponent]) -> Dict[str, Any]:
        """Analyze patterns across detected components"""
        patterns = {
            'most_common_types': Counter(comp.component_type for comp in components).most_common(5),
            'reusability_distribution': self._calculate_reusability_distribution(components),
            'complexity_analysis': self._analyze_complexity_patterns(components),
            'naming_patterns': self._analyze_naming_patterns(components),
            'category_distribution': Counter(comp.category for comp in components)
        }

        return patterns

    def _calculate_reusability_distribution(self, components: List[DetectedComponent]) -> Dict[str, float]:
        """Calculate distribution of component reusability"""
        if not components:
            return {}

        reusability_scores = [comp.reusability_score for comp in components]

        return {
            'high_reusability': sum(1 for score in reusability_scores if score > 0.7) / len(components),
            'medium_reusability': sum(1 for score in reusability_scores if 0.3 <= score <= 0.7) / len(components),
            'low_reusability': sum(1 for score in reusability_scores if score < 0.3) / len(components),
            'average_reusability': sum(reusability_scores) / len(reusability_scores)
        }

    def _analyze_complexity_patterns(self, components: List[DetectedComponent]) -> Dict[str, Any]:
        """Analyze complexity patterns across components"""
        if not components:
            return {}

        complexity_scores = [comp.complexity_score for comp in components]

        return {
            'average_complexity': sum(complexity_scores) / len(complexity_scores),
            'complexity_distribution': {
                'simple': sum(1 for score in complexity_scores if score < 0.3) / len(components),
                'moderate': sum(1 for score in complexity_scores if 0.3 <= score <= 0.7) / len(components),
                'complex': sum(1 for score in complexity_scores if score > 0.7) / len(components)
            },
            'most_complex_components': sorted(components, key=lambda c: c.complexity_score, reverse=True)[:3]
        }

    def _analyze_naming_patterns(self, components: List[DetectedComponent]) -> Dict[str, Any]:
        """Analyze naming patterns in components"""
        names = [comp.name for comp in components]

        return {
            'naming_consistency': self._calculate_naming_consistency(names),
            'common_prefixes': self._find_common_prefixes(names),
            'common_suffixes': self._find_common_suffixes(names),
            'naming_conventions': self._detect_naming_conventions(names)
        }

    def _calculate_naming_consistency(self, names: List[str]) -> float:
        """Calculate naming consistency score"""
        if len(names) < 2:
            return 1.0

        # Simplified consistency check based on case patterns
        case_patterns = [self._get_case_pattern(name) for name in names]
        most_common_pattern = Counter(case_patterns).most_common(1)[0][0]
        consistency = case_patterns.count(most_common_pattern) / len(names)

        return consistency

    def _get_case_pattern(self, name: str) -> str:
        """Detect case pattern in name"""
        if name.isupper():
            return 'UPPER_CASE'
        elif name.islower():
            return 'lower_case'
        elif '_' in name:
            return 'snake_case'
        elif '-' in name:
            return 'kebab-case'
        elif any(c.isupper() for c in name[1:]):
            return 'camelCase'
        else:
            return 'unknown'

    def _find_common_prefixes(self, names: List[str]) -> List[Tuple[str, int]]:
        """Find common prefixes in component names"""
        prefixes = defaultdict(int)

        for name in names:
            words = re.split(r'[_\-\s]+', name.lower())
            if words:
                prefixes[words[0]] += 1

        return [(prefix, count) for prefix, count in prefixes.items() if count > 1]

    def _find_common_suffixes(self, names: List[str]) -> List[Tuple[str, int]]:
        """Find common suffixes in component names"""
        suffixes = defaultdict(int)

        for name in names:
            words = re.split(r'[_\-\s]+', name.lower())
            if words:
                suffixes[words[-1]] += 1

        return [(suffix, count) for suffix, count in suffixes.items() if count > 1]

    def _detect_naming_conventions(self, names: List[str]) -> List[str]:
        """Detect naming conventions used"""
        conventions = []

        if any('_' in name for name in names):
            conventions.append('snake_case')
        if any('-' in name for name in names):
            conventions.append('kebab-case')
        if any(any(c.isupper() for c in name[1:]) for name in names):
            conventions.append('camelCase')

        return conventions

    def _analyze_design_system(self, components: List[DetectedComponent],
                             patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze design system structure and maturity"""
        categories_found = list(set(comp.category for comp in components))

        # Calculate design system maturity
        maturity_score = self._calculate_design_system_maturity(components, patterns)

        # Identify missing atomic design levels
        missing_categories = [cat for cat in self.design_categories.keys()
                            if cat not in categories_found]

        return {
            'categories_found': categories_found,
            'missing_categories': missing_categories,
            'maturity_score': maturity_score,
            'component_distribution': Counter(comp.category for comp in components),
            'design_token_coverage': self._analyze_design_token_coverage(components),
            'consistency_score': patterns.get('naming_patterns', {}).get('naming_consistency', 0),
            'recommendations': self._generate_design_system_recommendations(components, categories_found, missing_categories)
        }

    def _calculate_design_system_maturity(self, components: List[DetectedComponent],
                                        patterns: Dict[str, Any]) -> float:
        """Calculate overall design system maturity"""
        scores = []

        # Component coverage score
        coverage_score = len(set(comp.category for comp in components)) / len(self.design_categories)
        scores.append(coverage_score)

        # Reusability score
        reusability_score = patterns.get('reusability_distribution', {}).get('average_reusability', 0)
        scores.append(reusability_score)

        # Naming consistency score
        naming_score = patterns.get('naming_patterns', {}).get('naming_consistency', 0)
        scores.append(naming_score)

        return sum(scores) / len(scores)

    def _analyze_design_token_coverage(self, components: List[DetectedComponent]) -> Dict[str, Any]:
        """Analyze design token usage across components"""
        token_categories = defaultdict(int)

        for comp in components:
            for category in comp.design_tokens.keys():
                token_categories[category] += 1

        total_components = len(components)
        coverage = {}

        for category, count in token_categories.items():
            coverage[category] = count / total_components if total_components > 0 else 0

        return coverage

    def _generate_design_system_recommendations(self, components: List[DetectedComponent],
                                              found_categories: List[str],
                                              missing_categories: List[str]) -> List[str]:
        """Generate design system improvement recommendations"""
        recommendations = []

        if missing_categories:
            recommendations.append(f"Consider developing {', '.join(missing_categories)} components to complete atomic design hierarchy")

        # Check for low reusability
        low_reuse_components = [comp for comp in components if comp.reusability_score < 0.3]
        if low_reuse_components:
            recommendations.append(f"Review {len(low_reuse_components)} components with low reusability scores")

        # Check naming consistency
        if len(set(comp.name.split()[0] for comp in components if comp.name)) > len(components) * 0.7:
            recommendations.append("Establish consistent naming conventions for components")

        return recommendations

    def _extract_design_tokens(self, all_objects: List[Dict[str, Any]],
                             components: List[DetectedComponent]) -> Dict[str, Any]:
        """Extract design tokens from all objects and components"""
        tokens = {
            'colors': defaultdict(int),
            'typography': defaultdict(int),
            'spacing': defaultdict(int),
            'effects': defaultdict(int)
        }

        # Extract from all objects
        for obj in all_objects:
            obj_tokens = self._extract_object_design_tokens(obj)

            # Count token usage
            for category, token_data in obj_tokens.items():
                if isinstance(token_data, dict):
                    for key, value in token_data.items():
                        if value:
                            tokens[category][f"{key}_{value}"] += 1

        # Convert to regular dicts and sort by usage
        design_tokens = {}
        for category, token_counts in tokens.items():
            sorted_tokens = sorted(token_counts.items(), key=lambda x: x[1], reverse=True)
            design_tokens[category] = sorted_tokens[:10]  # Top 10 most used

        return design_tokens

    def _analyze_reusability(self, components: List[DetectedComponent]) -> Dict[str, Any]:
        """Analyze component reusability patterns"""
        if not components:
            return {'average_reusability': 0}

        reusability_scores = [comp.reusability_score for comp in components]

        return {
            'average_reusability': sum(reusability_scores) / len(reusability_scores),
            'highly_reusable': [comp.name for comp in components if comp.reusability_score > 0.7],
            'poorly_reusable': [comp.name for comp in components if comp.reusability_score < 0.3],
            'reuse_opportunities': self._identify_reuse_opportunities(components)
        }

    def _identify_reuse_opportunities(self, components: List[DetectedComponent]) -> List[str]:
        """Identify opportunities to improve component reuse"""
        opportunities = []

        # Find similar components that could be unified
        similar_groups = defaultdict(list)
        for comp in components:
            key = f"{comp.component_type}_{comp.category}"
            similar_groups[key].append(comp)

        for group_key, group_components in similar_groups.items():
            if len(group_components) > 1:
                opportunities.append(f"Consider unifying {len(group_components)} similar {group_key.replace('_', ' ')} components")

        return opportunities

    def _generate_component_catalog(self, components: List[DetectedComponent],
                                  design_system: Dict[str, Any]) -> Dict[str, Any]:
        """Generate component catalog for documentation"""
        catalog = {}

        # Group by category
        for category in design_system['categories_found']:
            category_components = [comp for comp in components if comp.category == category]
            catalog[category] = [
                {
                    'name': comp.name,
                    'type': comp.component_type,
                    'instances': len(comp.instances),
                    'reusability_score': comp.reusability_score,
                    'complexity_score': comp.complexity_score,
                    'design_tokens': list(comp.design_tokens.keys()),
                    'accessibility_features': comp.accessibility_features
                }
                for comp in category_components
            ]

        return catalog

    def _assess_component_quality(self, components: List[DetectedComponent],
                                design_system: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall component quality"""
        if not components:
            return {'overall_score': 0}

        # Quality metrics
        avg_reusability = sum(comp.reusability_score for comp in components) / len(components)
        consistency_score = design_system.get('consistency_score', 0)
        maturity_score = design_system.get('maturity_score', 0)

        # Accessibility coverage
        accessibility_coverage = sum(1 for comp in components if comp.accessibility_features) / len(components)

        overall_score = (avg_reusability + consistency_score + maturity_score + accessibility_coverage) / 4

        return {
            'overall_score': overall_score,
            'reusability_score': avg_reusability,
            'consistency_score': consistency_score,
            'maturity_score': maturity_score,
            'accessibility_coverage': accessibility_coverage,
            'quality_grade': self._calculate_quality_grade(overall_score)
        }

    def _calculate_quality_grade(self, score: float) -> str:
        """Convert quality score to letter grade"""
        if score >= 0.9:
            return 'A'
        elif score >= 0.8:
            return 'B'
        elif score >= 0.7:
            return 'C'
        elif score >= 0.6:
            return 'D'
        else:
            return 'F'

    def _generate_component_recommendations(self, components: List[DetectedComponent],
                                          design_system: Dict[str, Any],
                                          quality_assessment: Dict[str, Any]) -> List[str]:
        """Generate actionable component recommendations"""
        recommendations = []

        # Quality-based recommendations
        overall_score = quality_assessment.get('overall_score', 0)
        if overall_score < 0.7:
            recommendations.append("Component quality is below recommended threshold - focus on improving reusability and consistency")

        # Reusability recommendations
        if quality_assessment.get('reusability_score', 0) < 0.6:
            recommendations.append("Low component reusability detected - consider consolidating similar components")

        # Accessibility recommendations
        if quality_assessment.get('accessibility_coverage', 0) < 0.8:
            recommendations.append("Improve accessibility features across components - consider adding ARIA labels and semantic roles")

        # Design system recommendations
        if design_system.get('maturity_score', 0) < 0.7:
            recommendations.extend(design_system.get('recommendations', []))

        return recommendations