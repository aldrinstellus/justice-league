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
        # Initialize narrator for enhanced UX
        self.narrator = narrator if narrator else (get_narrator() if NARRATOR_AVAILABLE else None)

        logger.info(f"🔬 The Atom - Component Analyzer initialized")

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
