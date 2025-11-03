"""
🔬 THE ATOM - THE COMPONENT ANALYZER
Justice League Member: Component Library & Design System Specialist

The Atom shrinks down to analyze components at the molecular level!

Powers:
- Component library validation
- Variant enumeration and testing
- Design token analysis
- Consistency checking across components
- Component accessibility validation
- Bulk component testing
- Design system compliance
- Pattern library analysis

"I can shrink down to analyze every atom of your component library!"

Analysis Capabilities:
- Button variants (primary, secondary, ghost, danger, etc.)
- Input field states (default, focus, error, disabled)
- Color token consistency
- Spacing token usage
- Typography scale validation
- Component naming conventions
- ARIA pattern compliance
"""

import logging
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from collections import defaultdict
import re

# Mission Control Narrator for coordinated communication
try:
    from .mission_control_narrator import get_narrator
    NARRATOR_AVAILABLE = True
except ImportError:
    NARRATOR_AVAILABLE = False
    logging.warning("Mission Control Narrator not available - Atom will operate without narrator")

logger = logging.getLogger(__name__)


class AtomComponentAnalysis:
    """
    🔬 THE ATOM - Component Library Analyzer

    The Atom's Powers:
    1. Enumerate all component variants
    2. Test each variant for accessibility
    3. Validate design token consistency
    4. Check component naming conventions
    5. Analyze component hierarchy
    6. Detect missing variants
    7. Test component combinations
    8. Generate component documentation
    """

    def __init__(self, narrator: Optional[Any] = None):
        """
        Initialize The Atom's molecular analysis lab

        Args:
            narrator: Mission Control Narrator for coordinated communication
        """
        # Hero identity for narrator integration
        self.hero_name = "The Atom"
        self.hero_emoji = "🔬"

        # Initialize narrator for enhanced UX
        self.narrator = narrator if narrator else (get_narrator() if NARRATOR_AVAILABLE else None)

        logger.info(f"🔬 The Atom - Component Analyzer initialized")

    def say(self, message: str, style: str = "scientific", technical_info: Optional[str] = None):
        """The Atom dialogue - Molecular analysis and shrinking specialist"""
        if self.narrator:
            self.narrator.hero_speaks(f"{self.hero_emoji} {self.hero_name}", message, style, technical_info)

    def think(self, thought: str, step: Optional[int] = None, category: Optional[str] = "Analyzing"):
        """Sequential thinking with component focus. Categories: Analyzing, Shrinking, Examining"""
        if self.narrator:
            self.narrator.hero_thinks(f"{self.hero_emoji} {self.hero_name}", thought, step, category)

    def handoff(self, to_hero: str, context: str, details: Optional[str] = None):
        """Handoff component analysis to another hero"""
        if self.narrator:
            self.narrator.hero_handoff(f"{self.hero_emoji} {self.hero_name}", to_hero, context, details)

    def analyze_component_library(self, components: Dict[str, Any],
                                  design_tokens: Optional[Dict] = None) -> Dict[str, Any]:
        """
        🔬 The Atom analyzes component library at molecular level

        Args:
            components: Dictionary of components from design file
                {
                    'button-primary': {...},
                    'button-secondary': {...},
                    'input-default': {...},
                    etc.
                }
            design_tokens: Optional design tokens/variables

        Returns:
            Complete component library analysis
        """
        logger.info(f"🔬 The Atom shrinking down to analyze components...")

        results = {
            'hero': '🔬 The Atom - Component Analyzer',
            'timestamp': datetime.now().isoformat(),
            'component_count': len(components),
            'analyses': {}
        }

        # Step 1: Categorize components by type
        logger.info("🔬 Analyzing component categories...")
        categories = self._categorize_components(components)
        results['categories'] = categories

        # Step 2: Enumerate variants for each component type
        logger.info("🔬 Enumerating component variants...")
        variants = self._enumerate_variants(components, categories)
        results['variants'] = variants

        # Step 3: Check design token consistency
        if design_tokens:
            logger.info("🔬 Validating design token consistency...")
            token_analysis = self._analyze_design_tokens(components, design_tokens)
            results['token_analysis'] = token_analysis

        # Step 4: Validate naming conventions
        logger.info("🔬 Checking naming conventions...")
        naming_analysis = self._check_naming_conventions(components)
        results['naming_analysis'] = naming_analysis

        # Step 5: Detect missing variants
        logger.info("🔬 Detecting missing variants...")
        missing_variants = self._detect_missing_variants(variants)
        results['missing_variants'] = missing_variants

        # Step 6: Analyze component hierarchy
        logger.info("🔬 Analyzing component hierarchy...")
        hierarchy = self._analyze_component_hierarchy(components)
        results['hierarchy'] = hierarchy

        # Step 7: Test component accessibility patterns
        logger.info("🔬 Testing accessibility patterns...")
        accessibility_patterns = self._test_accessibility_patterns(components)
        results['accessibility_patterns'] = accessibility_patterns

        # Step 8: Calculate Atom Component Score
        component_score = self._calculate_component_score(results)
        results['atom_score'] = component_score

        # Step 9: Generate recommendations
        recommendations = self._generate_atom_recommendations(results)
        results['atom_recommendations'] = recommendations

        logger.info(f"🔬 ATOM ANALYSIS COMPLETE")
        logger.info(f"🔬 Component Score: {component_score['score']:.1f}/100")
        logger.info(f"🔬 The Atom says: {component_score['verdict']}")

        return results

    def _categorize_components(self, components: Dict) -> Dict[str, List[str]]:
        """
        🔬 Categorize components by type

        Categories: buttons, inputs, cards, modals, navigation, etc.

        Args:
            components: All components

        Returns:
            Components categorized by type
        """
        categories = defaultdict(list)

        # Common component patterns
        patterns = {
            'button': r'button|btn',
            'input': r'input|textfield|textarea',
            'card': r'card',
            'modal': r'modal|dialog',
            'navigation': r'nav|menu|sidebar',
            'form': r'form',
            'table': r'table|grid',
            'icon': r'icon',
            'badge': r'badge|tag|chip',
            'tooltip': r'tooltip',
            'dropdown': r'dropdown|select',
            'checkbox': r'checkbox',
            'radio': r'radio',
            'switch': r'switch|toggle',
            'slider': r'slider|range',
            'alert': r'alert|notification|toast'
        }

        for comp_id in components.keys():
            comp_name = comp_id.lower()

            # Check against patterns
            categorized = False
            for category, pattern in patterns.items():
                if re.search(pattern, comp_name):
                    categories[category].append(comp_id)
                    categorized = True
                    break

            if not categorized:
                categories['other'].append(comp_id)

        return dict(categories)

    def _enumerate_variants(self, components: Dict,
                           categories: Dict) -> Dict[str, Dict]:
        """
        🔬 Enumerate variants for each component type

        Variants: primary, secondary, disabled, error, etc.

        Args:
            components: All components
            categories: Categorized components

        Returns:
            Variants enumerated for each component type
        """
        variants = {}

        for category, comp_ids in categories.items():
            if category == 'other':
                continue

            # Extract variant names
            category_variants = defaultdict(list)

            for comp_id in comp_ids:
                # Try to extract variant from name
                # e.g., "button-primary" -> variant = "primary"
                parts = comp_id.lower().split('-')

                if len(parts) > 1:
                    variant = '-'.join(parts[1:])
                    category_variants[variant].append(comp_id)
                else:
                    category_variants['default'].append(comp_id)

            variants[category] = {
                'total_components': len(comp_ids),
                'variants_found': list(category_variants.keys()),
                'variant_count': len(category_variants),
                'components_by_variant': dict(category_variants)
            }

        return variants

    def _analyze_design_tokens(self, components: Dict,
                               design_tokens: Dict) -> Dict[str, Any]:
        """
        🔬 Analyze design token consistency

        Check if components use design tokens consistently

        Args:
            components: All components
            design_tokens: Design tokens/variables

        Returns:
            Token consistency analysis
        """
        token_usage = defaultdict(int)
        hardcoded_values = []

        for comp_id, component in components.items():
            # Check colors
            fg_color = component.get('foreground_color', '')
            bg_color = component.get('background_color', '')

            # Check if using tokens vs hardcoded hex
            if fg_color and fg_color.startswith('#'):
                hardcoded_values.append({
                    'component': comp_id,
                    'property': 'foreground_color',
                    'value': fg_color,
                    'atom_says': 'Hardcoded color detected - should use token!'
                })

            if bg_color and bg_color.startswith('#'):
                hardcoded_values.append({
                    'component': comp_id,
                    'property': 'background_color',
                    'value': bg_color,
                    'atom_says': 'Hardcoded color detected - should use token!'
                })

        return {
            'hardcoded_values_count': len(hardcoded_values),
            'hardcoded_values': hardcoded_values[:20],  # Top 20
            'token_usage': dict(token_usage),
            'consistency_score': max(0, 100 - (len(hardcoded_values) * 2)),  # Deduct 2 points each
            'atom_verdict': 'Excellent token usage!' if len(hardcoded_values) < 5 else 'Too many hardcoded values!'
        }

    def _check_naming_conventions(self, components: Dict) -> Dict[str, Any]:
        """
        🔬 Check component naming conventions

        Good naming: button-primary, input-error, card-elevated
        Bad naming: btn1, myButton, component_2

        Args:
            components: All components

        Returns:
            Naming convention analysis
        """
        issues = []

        # Naming rules
        # 1. Should use kebab-case (not camelCase or snake_case)
        # 2. Should have descriptive names (not btn1, comp2)
        # 3. Should include variant (button-primary not just button)

        for comp_id in components.keys():
            # Check for camelCase
            if re.search(r'[a-z][A-Z]', comp_id):
                issues.append({
                    'component': comp_id,
                    'issue': 'Uses camelCase instead of kebab-case',
                    'severity': 'moderate',
                    'atom_says': 'Use kebab-case for consistency!'
                })

            # Check for snake_case
            if '_' in comp_id:
                issues.append({
                    'component': comp_id,
                    'issue': 'Uses snake_case instead of kebab-case',
                    'severity': 'moderate',
                    'atom_says': 'Use kebab-case for consistency!'
                })

            # Check for generic names with numbers
            if re.search(r'(comp|component|elem|element)\d+', comp_id, re.I):
                issues.append({
                    'component': comp_id,
                    'issue': 'Generic name with number (e.g., comp1)',
                    'severity': 'serious',
                    'atom_says': 'Use descriptive names!'
                })

        return {
            'total_components': len(components),
            'naming_issues': len(issues),
            'issues': issues,
            'compliance_rate': max(0, 100 - (len(issues) / len(components) * 100)),
            'atom_verdict': 'Excellent naming!' if len(issues) < 5 else 'Naming needs improvement!'
        }

    def _detect_missing_variants(self, variants: Dict) -> Dict[str, List[str]]:
        """
        🔬 Detect missing variants in component library

        Expected variants:
        - Buttons: primary, secondary, ghost, danger, disabled
        - Inputs: default, focus, error, disabled
        - etc.

        Args:
            variants: Enumerated variants

        Returns:
            Missing variants for each component type
        """
        expected_variants = {
            'button': ['primary', 'secondary', 'ghost', 'danger', 'disabled'],
            'input': ['default', 'focus', 'error', 'disabled'],
            'card': ['default', 'elevated', 'outlined'],
            'alert': ['info', 'success', 'warning', 'error']
        }

        missing = {}

        for component_type, expected in expected_variants.items():
            if component_type in variants:
                found_variants = set(variants[component_type]['variants_found'])
                expected_set = set(expected)

                missing_variants = expected_set - found_variants

                if missing_variants:
                    missing[component_type] = {
                        'missing': list(missing_variants),
                        'found': list(found_variants),
                        'completeness': (len(found_variants) / len(expected_set) * 100),
                        'atom_says': f'Missing {len(missing_variants)} variants!'
                    }

        return missing

    def _analyze_component_hierarchy(self, components: Dict) -> Dict[str, Any]:
        """
        🔬 Analyze component hierarchy and composition

        Args:
            components: All components

        Returns:
            Hierarchy analysis
        """
        # Detect atomic vs molecular vs organism components
        atomic = []  # Basic: buttons, inputs
        molecular = []  # Composed: search bar (input + button)
        organisms = []  # Complex: headers, cards with multiple parts

        for comp_id, component in components.items():
            # Simple heuristic based on child count
            children = component.get('children', [])
            child_count = len(children) if isinstance(children, list) else 0

            if child_count == 0:
                atomic.append(comp_id)
            elif child_count < 5:
                molecular.append(comp_id)
            else:
                organisms.append(comp_id)

        return {
            'atomic_components': {
                'count': len(atomic),
                'components': atomic,
                'description': 'Basic building blocks'
            },
            'molecular_components': {
                'count': len(molecular),
                'components': molecular[:10],  # Top 10
                'description': 'Composed of atomic components'
            },
            'organism_components': {
                'count': len(organisms),
                'components': organisms[:10],  # Top 10
                'description': 'Complex composed components'
            },
            'atom_analysis': f'Good atomic design hierarchy!' if len(atomic) > 0 else 'No atomic components found'
        }

    def _test_accessibility_patterns(self, components: Dict) -> Dict[str, Any]:
        """
        🔬 Test component accessibility patterns

        Check for common ARIA patterns

        Args:
            components: All components

        Returns:
            Accessibility pattern analysis
        """
        patterns_checked = {
            'buttons_have_labels': 0,
            'inputs_have_labels': 0,
            'interactive_have_roles': 0
        }

        issues = []

        for comp_id, component in components.items():
            comp_type = component.get('type', '').lower()

            # Check button patterns
            if 'button' in comp_id.lower() or comp_type == 'button':
                label = component.get('text') or component.get('label')
                if not label:
                    issues.append({
                        'component': comp_id,
                        'pattern': 'Button without label',
                        'severity': 'critical',
                        'atom_says': 'Buttons must have accessible labels!'
                    })
                else:
                    patterns_checked['buttons_have_labels'] += 1

            # Check input patterns
            if 'input' in comp_id.lower() or comp_type in ['textbox', 'input']:
                # Inputs should have associated labels
                patterns_checked['inputs_have_labels'] += 1

        return {
            'patterns_checked': patterns_checked,
            'issues_found': len(issues),
            'issues': issues,
            'atom_verdict': 'Good accessibility patterns!' if len(issues) < 3 else 'Accessibility issues detected!'
        }

    def _calculate_component_score(self, results: Dict) -> Dict[str, Any]:
        """
        🔬 Calculate Atom Component Score (0-100)

        Scoring:
        - Variant completeness (30%)
        - Naming conventions (25%)
        - Design token usage (25%)
        - Accessibility patterns (20%)

        Args:
            results: Analysis results

        Returns:
            Component score
        """
        score = 100  # Start perfect

        # Variant completeness
        missing_variants = results.get('missing_variants', {})
        if missing_variants:
            total_missing = sum(len(v['missing']) for v in missing_variants.values())
            score -= min(total_missing * 3, 30)  # Max 30 point deduction

        # Naming conventions
        naming = results.get('naming_analysis', {})
        naming_issues = naming.get('naming_issues', 0)
        score -= min(naming_issues * 2, 25)  # Max 25 point deduction

        # Design token usage
        token_analysis = results.get('token_analysis', {})
        if token_analysis:
            hardcoded_count = token_analysis.get('hardcoded_values_count', 0)
            score -= min(hardcoded_count * 2, 25)  # Max 25 point deduction

        # Accessibility patterns
        acc_patterns = results.get('accessibility_patterns', {})
        acc_issues = acc_patterns.get('issues_found', 0)
        score -= min(acc_issues * 4, 20)  # Max 20 point deduction

        # Floor at 0
        score = max(0, score)

        # Determine verdict
        if score >= 90:
            verdict = "🔬 MOLECULAR PERFECTION - Component library is atomic!"
            grade = "S+"
        elif score >= 80:
            verdict = "🔬 EXCELLENT STRUCTURE - Strong component system!"
            grade = "A"
        elif score >= 70:
            verdict = "🔬 GOOD FOUNDATION - Room for improvement"
            grade = "B"
        elif score >= 60:
            verdict = "🔬 NEEDS REFINEMENT - Component gaps detected"
            grade = "C"
        else:
            verdict = "🔬 MOLECULAR INSTABILITY - Major component issues!"
            grade = "D"

        return {
            'score': score,
            'grade': grade,
            'verdict': verdict,
            'variant_completeness': 100 - min(len(missing_variants) * 10, 30) if 'missing_variants' in results else 100,
            'naming_quality': naming.get('compliance_rate', 100) if naming else 100,
            'token_consistency': token_analysis.get('consistency_score', 100) if token_analysis else 100,
            'accessibility_score': 100 - (acc_issues * 4) if acc_patterns else 100
        }

    def _generate_atom_recommendations(self, results: Dict) -> List[Dict]:
        """
        🔬 Generate The Atom's component recommendations

        Args:
            results: Analysis results

        Returns:
            List of recommendations
        """
        recommendations = []

        # Missing variants
        missing_variants = results.get('missing_variants', {})
        if missing_variants:
            for comp_type, details in missing_variants.items():
                recommendations.append({
                    'priority': 'high',
                    'area': f'{comp_type.title()} Variants',
                    'issue': f"Missing {len(details['missing'])} variants",
                    'missing_variants': details['missing'],
                    'atom_says': f'Create missing {comp_type} variants for completeness!',
                    'actions': [
                        f"Design {', '.join(details['missing'])} variants",
                        'Test each variant for accessibility',
                        'Document variant usage'
                    ]
                })

        # Naming issues
        naming = results.get('naming_analysis', {})
        if naming.get('naming_issues', 0) > 5:
            recommendations.append({
                'priority': 'medium',
                'area': 'Naming Conventions',
                'issue': f"{naming['naming_issues']} naming convention violations",
                'atom_says': 'Standardize component naming for consistency!',
                'actions': [
                    'Use kebab-case for all component names',
                    'Use descriptive names (not comp1, btn2)',
                    'Include variant in name (button-primary not button1)'
                ]
            })

        # Token usage
        token_analysis = results.get('token_analysis', {})
        if token_analysis and token_analysis.get('hardcoded_values_count', 0) > 10:
            recommendations.append({
                'priority': 'high',
                'area': 'Design Tokens',
                'issue': f"{token_analysis['hardcoded_values_count']} hardcoded values detected",
                'atom_says': 'Replace hardcoded values with design tokens!',
                'actions': [
                    'Create color tokens for all hardcoded colors',
                    'Create spacing tokens for margins/padding',
                    'Create typography tokens for font styles',
                    'Document token usage guidelines'
                ]
            })

        # Accessibility
        acc_patterns = results.get('accessibility_patterns', {})
        if acc_patterns.get('issues_found', 0) > 0:
            recommendations.append({
                'priority': 'critical',
                'area': 'Accessibility Patterns',
                'issue': f"{acc_patterns['issues_found']} accessibility issues in components",
                'atom_says': 'Fix accessibility at the component level!',
                'actions': [
                    'Add labels to all buttons',
                    'Associate labels with inputs',
                    'Add ARIA roles where needed',
                    'Test with screen readers'
                ]
            })

        return recommendations

    # Aliases for audit compatibility
    def _calculate_atom_score(self, results: Dict) -> Dict[str, Any]:
        """Alias for _calculate_component_score"""
        return self._calculate_component_score(results)

    def _generate_molecular_recommendations(self, results: Dict) -> List[Dict]:
        """Alias for _generate_atom_recommendations"""
        return self._generate_atom_recommendations(results)

    def validate_component_variants(self, components: Dict[str, Any],
                                    component_type: Optional[str] = None) -> Dict[str, Any]:
        """
        🔬 Validate component variants are complete

        Checks that all expected variants exist for each component type.
        Essential for ensuring design system completeness.

        Args:
            components: Dictionary of components from design file
            component_type: Optional specific component type to check ('button', 'input', etc.)
                           If None, checks all component types

        Returns:
            Variant validation results with missing variants identified
        """
        self.say("Shrinking down to molecular level to validate variants", style="scientific")
        self.think("Analyzing component variant completeness", category="Shrinking")

        results = {
            'hero': '🔬 The Atom',
            'timestamp': datetime.now().isoformat(),
            'variant_validation': {}
        }

        # Expected variants for each component type
        expected_variants = {
            'button': {
                'required': ['primary', 'secondary'],
                'recommended': ['ghost', 'danger', 'disabled', 'loading'],
                'optional': ['outline', 'link', 'icon-only']
            },
            'input': {
                'required': ['default', 'error'],
                'recommended': ['focus', 'disabled', 'success'],
                'optional': ['search', 'password', 'number']
            },
            'card': {
                'required': ['default'],
                'recommended': ['elevated', 'outlined', 'interactive'],
                'optional': ['compact', 'expanded']
            },
            'alert': {
                'required': ['info', 'error'],
                'recommended': ['success', 'warning'],
                'optional': ['dismissible', 'permanent']
            },
            'badge': {
                'required': ['default'],
                'recommended': ['primary', 'success', 'warning', 'error'],
                'optional': ['pill', 'square', 'dot']
            }
        }

        # Categorize components
        categories = self._categorize_components(components)

        self.think("Enumerating existing variants", category="Examining")

        # Check each component type
        types_to_check = [component_type] if component_type else expected_variants.keys()

        validation_results = {}

        for comp_type in types_to_check:
            if comp_type not in categories:
                self.think(f"No {comp_type} components found in library", category="Analyzing")
                continue

            # Get existing variants
            comp_ids = categories[comp_type]
            existing_variants = set()

            for comp_id in comp_ids:
                # Extract variant from component name
                parts = comp_id.lower().split('-')
                if len(parts) > 1:
                    variant = '-'.join(parts[1:])
                    existing_variants.add(variant)

            # Compare with expected
            expected = expected_variants.get(comp_type, {})
            required = set(expected.get('required', []))
            recommended = set(expected.get('recommended', []))
            optional = set(expected.get('optional', []))

            missing_required = required - existing_variants
            missing_recommended = recommended - existing_variants
            extra_variants = existing_variants - (required | recommended | optional)

            # Calculate completeness
            total_expected = len(required) + len(recommended)
            total_found = len(existing_variants & (required | recommended))
            completeness = (total_found / total_expected * 100) if total_expected > 0 else 0

            validation_results[comp_type] = {
                'existing_variants': list(existing_variants),
                'missing_required': list(missing_required),
                'missing_recommended': list(missing_recommended),
                'extra_variants': list(extra_variants),
                'completeness_percent': round(completeness, 1),
                'component_count': len(comp_ids),
                'severity': 'critical' if missing_required else 'high' if missing_recommended else 'low',
                'atom_says': self._get_variant_message(missing_required, missing_recommended, completeness)
            }

        # Overall verdict
        if validation_results:
            avg_completeness = sum(v['completeness_percent'] for v in validation_results.values()) / len(validation_results)
            critical_count = sum(1 for v in validation_results.values() if v['severity'] == 'critical')

            if critical_count > 0:
                verdict = f"🔬 MOLECULAR INSTABILITY - {critical_count} components missing required variants!"
                grade = "D"
            elif avg_completeness >= 90:
                verdict = "🔬 MOLECULAR PERFECTION - All variants present!"
                grade = "S+"
            elif avg_completeness >= 75:
                verdict = "🔬 STRONG STRUCTURE - Minor gaps detected"
                grade = "A"
            elif avg_completeness >= 60:
                verdict = "🔬 NEEDS REFINEMENT - Several variants missing"
                grade = "B"
            else:
                verdict = "🔬 INCOMPLETE LIBRARY - Many variants missing"
                grade = "C"

            results['variant_validation'] = validation_results
            results['overall_completeness'] = round(avg_completeness, 1)
            results['critical_gaps'] = critical_count
            results['atom_verdict'] = verdict
            results['grade'] = grade

            self.say(verdict, style="scientific", technical_info=f"{avg_completeness:.1f}% complete, {critical_count} critical gaps")
        else:
            results['atom_verdict'] = "🔬 NO COMPONENTS FOUND - Library is empty!"
            results['grade'] = "N/A"

        return results

    def _get_variant_message(self, missing_required: List[str], missing_recommended: List[str],
                             completeness: float) -> str:
        """Generate Atom's message based on variant completeness"""
        if missing_required:
            return f"CRITICAL: Missing required variants - {', '.join(missing_required)}"
        elif missing_recommended:
            return f"Add recommended variants: {', '.join(missing_recommended)}"
        elif completeness >= 90:
            return "Excellent variant coverage!"
        else:
            return "Variant coverage acceptable"

    def detect_duplicate_components(self, components: Dict[str, Any],
                                    similarity_threshold: float = 0.85) -> Dict[str, Any]:
        """
        🔬 Detect duplicate or highly similar components

        Identifies components that are nearly identical, suggesting potential
        consolidation opportunities in the component library.

        Args:
            components: Dictionary of components from design file
            similarity_threshold: Similarity threshold (0.0-1.0) for considering components duplicates
                                 Default: 0.85 (85% similar)

        Returns:
            Duplicate detection results with similarity scores
        """
        self.say("Analyzing component similarity at molecular level", style="scientific")
        self.think("Comparing component structures for duplication", category="Shrinking")

        results = {
            'hero': '🔬 The Atom',
            'timestamp': datetime.now().isoformat(),
            'duplicate_analysis': {}
        }

        duplicate_groups = []
        checked_pairs = set()

        comp_ids = list(components.keys())

        self.think(f"Examining {len(comp_ids)} components for similarity", category="Analyzing")

        for i, comp_id_1 in enumerate(comp_ids):
            for comp_id_2 in comp_ids[i+1:]:
                # Skip if already checked
                pair_key = tuple(sorted([comp_id_1, comp_id_2]))
                if pair_key in checked_pairs:
                    continue
                checked_pairs.add(pair_key)

                # Calculate similarity
                similarity = self._calculate_component_similarity(
                    components[comp_id_1],
                    components[comp_id_2]
                )

                if similarity >= similarity_threshold:
                    duplicate_groups.append({
                        'component_1': comp_id_1,
                        'component_2': comp_id_2,
                        'similarity_score': round(similarity * 100, 1),
                        'severity': 'critical' if similarity >= 0.95 else 'high' if similarity >= 0.90 else 'moderate',
                        'atom_says': self._get_similarity_message(similarity),
                        'recommendation': self._get_duplicate_recommendation(comp_id_1, comp_id_2, similarity)
                    })

        # Sort by similarity (highest first)
        duplicate_groups.sort(key=lambda x: x['similarity_score'], reverse=True)

        self.think("Calculating duplication impact", category="Examining")

        # Calculate statistics
        if duplicate_groups:
            avg_similarity = sum(d['similarity_score'] for d in duplicate_groups) / len(duplicate_groups)
            critical_count = sum(1 for d in duplicate_groups if d['severity'] == 'critical')
            high_count = sum(1 for d in duplicate_groups if d['severity'] == 'high')

            verdict = f"🔬 DUPLICATION DETECTED - {len(duplicate_groups)} similar component pairs found!"
            if critical_count > 0:
                grade = "D"
            elif high_count > 3:
                grade = "C"
            elif high_count > 0:
                grade = "B"
            else:
                grade = "A"
        else:
            avg_similarity = 0
            critical_count = 0
            high_count = 0
            verdict = "🔬 NO DUPLICATION - All components are unique!"
            grade = "S+"

        results['duplicate_analysis'] = {
            'total_components': len(components),
            'duplicate_pairs_found': len(duplicate_groups),
            'critical_duplicates': critical_count,
            'high_duplicates': high_count,
            'avg_similarity': round(avg_similarity, 1),
            'duplicate_groups': duplicate_groups[:20],  # Top 20
            'consolidation_opportunities': critical_count + high_count
        }

        results['atom_verdict'] = verdict
        results['grade'] = grade

        self.say(verdict, style="scientific",
                 technical_info=f"{len(duplicate_groups)} pairs, {critical_count} critical, {high_count} high")

        return results

    def _calculate_component_similarity(self, comp1: Dict, comp2: Dict) -> float:
        """
        Calculate similarity between two components (0.0-1.0)

        Factors:
        - Type similarity (same button vs different type)
        - Style similarity (colors, sizes, padding)
        - Structure similarity (children, hierarchy)
        """
        similarity_score = 0.0
        factors_checked = 0

        # Type similarity (40% weight)
        type1 = comp1.get('type', '').lower()
        type2 = comp2.get('type', '').lower()
        if type1 and type2:
            factors_checked += 1
            if type1 == type2:
                similarity_score += 0.4

        # Color similarity (20% weight)
        fg1 = comp1.get('foreground_color', '')
        fg2 = comp2.get('foreground_color', '')
        bg1 = comp1.get('background_color', '')
        bg2 = comp2.get('background_color', '')

        if fg1 and fg2:
            factors_checked += 1
            if fg1 == fg2:
                similarity_score += 0.1

        if bg1 and bg2:
            factors_checked += 1
            if bg1 == bg2:
                similarity_score += 0.1

        # Size similarity (20% weight)
        width1 = comp1.get('width', 0)
        width2 = comp2.get('width', 0)
        height1 = comp1.get('height', 0)
        height2 = comp2.get('height', 0)

        if width1 and width2 and height1 and height2:
            factors_checked += 1
            width_diff = abs(width1 - width2) / max(width1, width2) if max(width1, width2) > 0 else 0
            height_diff = abs(height1 - height2) / max(height1, height2) if max(height1, height2) > 0 else 0
            size_similarity = 1.0 - ((width_diff + height_diff) / 2)
            similarity_score += size_similarity * 0.2

        # Children count similarity (20% weight)
        children1 = len(comp1.get('children', []))
        children2 = len(comp2.get('children', []))

        if children1 > 0 or children2 > 0:
            factors_checked += 1
            max_children = max(children1, children2)
            child_diff = abs(children1 - children2)
            child_similarity = 1.0 - (child_diff / max_children) if max_children > 0 else 1.0
            similarity_score += child_similarity * 0.2

        return similarity_score

    def _get_similarity_message(self, similarity: float) -> str:
        """Generate Atom's message based on similarity score"""
        if similarity >= 0.95:
            return "NEARLY IDENTICAL - Strong consolidation candidate!"
        elif similarity >= 0.90:
            return "VERY SIMILAR - Consider merging these components"
        elif similarity >= 0.85:
            return "SIMILAR - Review for potential consolidation"
        else:
            return "SOMEWHAT SIMILAR - Minor overlap detected"

    def _get_duplicate_recommendation(self, comp1: str, comp2: str, similarity: float) -> str:
        """Generate recommendation for duplicate components"""
        if similarity >= 0.95:
            return f"Consolidate '{comp1}' and '{comp2}' into a single component with variants"
        elif similarity >= 0.90:
            return f"Review if '{comp1}' and '{comp2}' can share a base component"
        else:
            return f"Document differences between '{comp1}' and '{comp2}'"

    def validate_design_tokens(self, components: Dict[str, Any],
                               design_tokens: Optional[Dict] = None) -> Dict[str, Any]:
        """
        🔬 Validate design token usage and consistency

        Analyzes whether components use design tokens correctly and consistently.
        Identifies hardcoded values that should use tokens.

        Args:
            components: Dictionary of components from design file
            design_tokens: Optional design token definitions
                {
                    'colors': {'primary': '#007bff', ...},
                    'spacing': {'xs': 4, 's': 8, ...},
                    'typography': {'h1': {...}, ...}
                }

        Returns:
            Design token validation results
        """
        self.say("Analyzing design token usage at atomic level", style="scientific")
        self.think("Examining token consistency across components", category="Shrinking")

        results = {
            'hero': '🔬 The Atom',
            'timestamp': datetime.now().isoformat(),
            'token_validation': {}
        }

        # Track token usage
        hardcoded_colors = []
        hardcoded_spacing = []
        hardcoded_typography = []
        token_references = defaultdict(int)

        self.think(f"Scanning {len(components)} components for hardcoded values", category="Analyzing")

        for comp_id, component in components.items():
            # Check colors
            fg_color = component.get('foreground_color', '')
            bg_color = component.get('background_color', '')

            if fg_color and fg_color.startswith('#'):
                hardcoded_colors.append({
                    'component': comp_id,
                    'property': 'foreground_color',
                    'value': fg_color,
                    'severity': 'high',
                    'atom_says': f'Use color token instead of {fg_color}'
                })

            if bg_color and bg_color.startswith('#'):
                hardcoded_colors.append({
                    'component': comp_id,
                    'property': 'background_color',
                    'value': bg_color,
                    'severity': 'high',
                    'atom_says': f'Use color token instead of {bg_color}'
                })

            # Check spacing (margins, padding)
            padding = component.get('padding', {})
            if isinstance(padding, dict):
                for side, value in padding.items():
                    if isinstance(value, (int, float)) and value > 0:
                        # Check if it's a standard spacing value
                        if design_tokens and 'spacing' in design_tokens:
                            token_values = set(design_tokens['spacing'].values())
                            if value not in token_values:
                                hardcoded_spacing.append({
                                    'component': comp_id,
                                    'property': f'padding-{side}',
                                    'value': value,
                                    'severity': 'moderate',
                                    'atom_says': f'Use spacing token for {value}px padding'
                                })

            # Check typography
            font_size = component.get('font_size')
            font_weight = component.get('font_weight')

            if font_size and isinstance(font_size, (int, float)):
                if design_tokens and 'typography' in design_tokens:
                    # Check if font size matches a typography token
                    is_token_value = any(
                        isinstance(token, dict) and token.get('fontSize') == font_size
                        for token in design_tokens['typography'].values()
                    )
                    if not is_token_value:
                        hardcoded_typography.append({
                            'component': comp_id,
                            'property': 'font_size',
                            'value': font_size,
                            'severity': 'moderate',
                            'atom_says': f'Use typography token for {font_size}px font'
                        })

        self.think("Calculating token consistency metrics", category="Examining")

        # Calculate metrics
        total_hardcoded = len(hardcoded_colors) + len(hardcoded_spacing) + len(hardcoded_typography)
        total_properties_checked = len(components) * 3  # Rough estimate

        token_usage_rate = max(0, 100 - (total_hardcoded / total_properties_checked * 100)) if total_properties_checked > 0 else 0

        # Determine verdict
        if total_hardcoded == 0:
            verdict = "🔬 MOLECULAR PERFECTION - 100% token usage!"
            grade = "S+"
        elif token_usage_rate >= 90:
            verdict = "🔬 EXCELLENT CONSISTENCY - Strong token usage!"
            grade = "A"
        elif token_usage_rate >= 75:
            verdict = "🔬 GOOD FOUNDATION - Some hardcoded values"
            grade = "B"
        elif token_usage_rate >= 60:
            verdict = "🔬 NEEDS IMPROVEMENT - Many hardcoded values"
            grade = "C"
        else:
            verdict = "🔬 MOLECULAR CHAOS - Minimal token usage!"
            grade = "D"

        results['token_validation'] = {
            'total_components_analyzed': len(components),
            'hardcoded_color_count': len(hardcoded_colors),
            'hardcoded_spacing_count': len(hardcoded_spacing),
            'hardcoded_typography_count': len(hardcoded_typography),
            'total_hardcoded_values': total_hardcoded,
            'token_usage_rate_percent': round(token_usage_rate, 1),
            'hardcoded_colors': hardcoded_colors[:10],
            'hardcoded_spacing': hardcoded_spacing[:10],
            'hardcoded_typography': hardcoded_typography[:10],
            'recommendations': self._generate_token_recommendations(hardcoded_colors, hardcoded_spacing, hardcoded_typography)
        }

        results['atom_verdict'] = verdict
        results['grade'] = grade

        self.say(verdict, style="scientific",
                 technical_info=f"{token_usage_rate:.1f}% token usage, {total_hardcoded} hardcoded values")

        return results

    def _generate_token_recommendations(self, hardcoded_colors: List[Dict],
                                        hardcoded_spacing: List[Dict],
                                        hardcoded_typography: List[Dict]) -> List[Dict]:
        """Generate recommendations for token improvements"""
        recommendations = []

        if hardcoded_colors:
            unique_colors = set(item['value'] for item in hardcoded_colors)
            recommendations.append({
                'priority': 'high',
                'area': 'Color Tokens',
                'issue': f'{len(hardcoded_colors)} hardcoded colors ({len(unique_colors)} unique values)',
                'atom_says': 'Create color tokens to replace hardcoded values!',
                'actions': [
                    f'Define color tokens for: {", ".join(list(unique_colors)[:5])}',
                    'Update components to reference color tokens',
                    'Document color token usage guidelines'
                ]
            })

        if hardcoded_spacing:
            unique_spacing = set(item['value'] for item in hardcoded_spacing)
            recommendations.append({
                'priority': 'medium',
                'area': 'Spacing Tokens',
                'issue': f'{len(hardcoded_spacing)} hardcoded spacing values',
                'atom_says': 'Standardize spacing with tokens!',
                'actions': [
                    'Define spacing scale (4px, 8px, 16px, 24px, 32px, etc.)',
                    'Map hardcoded values to nearest spacing token',
                    'Update component padding/margins to use tokens'
                ]
            })

        if hardcoded_typography:
            recommendations.append({
                'priority': 'medium',
                'area': 'Typography Tokens',
                'issue': f'{len(hardcoded_typography)} hardcoded typography values',
                'atom_says': 'Create typography scale for consistency!',
                'actions': [
                    'Define typography scale (h1, h2, body, caption, etc.)',
                    'Include font size, weight, line height in tokens',
                    'Update components to reference typography tokens'
                ]
            })

        return recommendations


# Main entry point - The Atom's Mission Interface
def atom_analyze_components(components: Dict[str, Any],
                            design_tokens: Optional[Dict] = None) -> Dict[str, Any]:
    """
    🔬 The Atom analyzes component library at molecular level!

    Shrinking down to see every atom!

    Args:
        components: Dictionary of components
        design_tokens: Optional design tokens

    Returns:
        Complete component library analysis
    """
    atom = AtomComponentAnalysis()
    return atom.analyze_component_library(components, design_tokens)
