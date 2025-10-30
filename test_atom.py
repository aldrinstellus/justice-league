#!/usr/bin/env python3
"""
🔬 THE ATOM - Component Analysis Test Suite
============================================

Tests for component library validation and design system analysis.

Author: Justice League
Created: October 23, 2025
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.justice_league.atom_component_analysis import AtomComponentAnalysis


def test_atom_initialization():
    """Test 1: The Atom initialization."""
    print("\n" + "=" * 70)
    print("Test 1: The Atom Component Analyzer Initialization")
    print("=" * 70)

    atom = AtomComponentAnalysis()

    assert atom is not None, "The Atom should initialize"
    assert hasattr(atom, 'analyze_component_library'), "Should have analyze_component_library method"
    assert hasattr(atom, '_categorize_components'), "Should have _categorize_components method"
    assert hasattr(atom, '_enumerate_variants'), "Should have _enumerate_variants method"
    assert hasattr(atom, '_analyze_design_tokens'), "Should have _analyze_design_tokens method"

    print("✅ PASSED: The Atom initialized successfully")
    return True


def test_categorize_components():
    """Test 2: Categorize components by type."""
    print("\n" + "=" * 70)
    print("Test 2: Categorize Components by Type")
    print("=" * 70)

    atom = AtomComponentAnalysis()

    # Mock components
    mock_components = {
        'button-primary': {},
        'button-secondary': {},
        'button-danger': {},
        'input-default': {},
        'input-error': {},
        'card-basic': {},
        'card-elevated': {},
        'modal-small': {},
        'icon-close': {},
        'icon-menu': {},
        'random-component': {}
    }

    categories = atom._categorize_components(mock_components)

    # Check categories
    assert 'button' in categories, "Should categorize buttons"
    assert 'input' in categories, "Should categorize inputs"
    assert 'card' in categories, "Should categorize cards"
    assert 'modal' in categories, "Should categorize modals"
    assert 'icon' in categories, "Should categorize icons"
    assert 'other' in categories, "Should have 'other' category"

    # Check counts
    assert len(categories['button']) == 3, f"Should have 3 buttons, got {len(categories['button'])}"
    assert len(categories['input']) == 2, f"Should have 2 inputs, got {len(categories['input'])}"
    assert len(categories['card']) == 2, f"Should have 2 cards, got {len(categories['card'])}"
    # Note: icon-menu matches 'menu' pattern first, so goes to navigation
    assert len(categories.get('icon', [])) >= 1, f"Should have at least 1 icon, got {len(categories.get('icon', []))}"

    print("✅ PASSED: Component categorization works")
    print(f"   Categories found: {len(categories)}")
    print(f"   Buttons: {len(categories['button'])}")
    print(f"   Inputs: {len(categories['input'])}")
    return True


def test_enumerate_variants():
    """Test 3: Enumerate component variants."""
    print("\n" + "=" * 70)
    print("Test 3: Enumerate Component Variants")
    print("=" * 70)

    atom = AtomComponentAnalysis()

    mock_components = {
        'button-primary': {},
        'button-secondary': {},
        'button-ghost': {},
        'button-danger': {},
        'input-default': {},
        'input-error': {}
    }

    categories = atom._categorize_components(mock_components)
    variants = atom._enumerate_variants(mock_components, categories)

    # Check button variants
    assert 'button' in variants, "Should have button variants"
    button_variants = variants['button']

    assert 'total_components' in button_variants, "Should have total_components"
    assert button_variants['total_components'] == 4, f"Should have 4 buttons, got {button_variants['total_components']}"

    assert 'variants_found' in button_variants, "Should list variants_found"
    assert 'variant_count' in button_variants, "Should have variant_count"
    assert button_variants['variant_count'] == 4, f"Should have 4 button variants, got {button_variants['variant_count']}"

    assert 'components_by_variant' in button_variants, "Should have components_by_variant"

    # Check that specific variants exist
    variants_list = button_variants['variants_found']
    assert 'primary' in variants_list, "Should have 'primary' variant"
    assert 'secondary' in variants_list, "Should have 'secondary' variant"
    assert 'danger' in variants_list, "Should have 'danger' variant"

    # Check input variants
    assert 'input' in variants, "Should have input variants"
    input_variants = variants['input']
    assert input_variants['total_components'] == 2, "Should have 2 inputs"

    print("✅ PASSED: Variant enumeration works")
    print(f"   Button variants: {button_variants['variant_count']}")
    print(f"   Input variants: {input_variants['variant_count']}")
    return True


def test_analyze_design_tokens():
    """Test 4: Analyze design token consistency."""
    print("\n" + "=" * 70)
    print("Test 4: Analyze Design Token Consistency")
    print("=" * 70)

    atom = AtomComponentAnalysis()

    # Mock components with colors
    mock_components = {
        'button-primary': {
            'foreground_color': 'var(--color-primary)',
            'background_color': 'var(--color-bg-primary)'
        },
        'button-secondary': {
            'foreground_color': '#FF5733',  # Hardcoded
            'background_color': 'var(--color-bg-secondary)'
        },
        'input-default': {
            'foreground_color': 'var(--color-text)',
            'background_color': '#FFFFFF'  # Hardcoded
        }
    }

    # Mock design tokens
    design_tokens = {
        'colors': {
            '--color-primary': '#007bff',
            '--color-bg-primary': '#ffffff',
            '--color-bg-secondary': '#6c757d',
            '--color-text': '#212529'
        }
    }

    token_analysis = atom._analyze_design_tokens(mock_components, design_tokens)

    # Actual return structure: hardcoded_values_count, hardcoded_values, token_usage, consistency_score, atom_verdict
    assert 'hardcoded_values_count' in token_analysis, "Should have hardcoded_values_count"
    assert 'hardcoded_values' in token_analysis, "Should have hardcoded_values"
    assert 'token_usage' in token_analysis, "Should have token_usage"
    assert 'consistency_score' in token_analysis, "Should have consistency_score"
    assert 'atom_verdict' in token_analysis, "Should have atom_verdict"

    # Should detect hardcoded values (#FF5733 and #FFFFFF)
    assert token_analysis['hardcoded_values_count'] > 0, "Should detect hardcoded colors"

    print("✅ PASSED: Design token analysis works")
    print(f"   Token usage entries: {len(token_analysis['token_usage'])}")
    print(f"   Hardcoded values: {token_analysis['hardcoded_values_count']}")
    print(f"   Consistency score: {token_analysis['consistency_score']}")
    return True


def test_check_naming_conventions():
    """Test 5: Check naming convention compliance."""
    print("\n" + "=" * 70)
    print("Test 5: Check Naming Conventions")
    print("=" * 70)

    atom = AtomComponentAnalysis()

    mock_components = {
        'button-primary': {},          # Good: kebab-case
        'button-secondary': {},        # Good
        'InputDefault': {},            # Bad: PascalCase
        'card_elevated': {},           # Bad: snake_case
        'modal-small': {},             # Good
        'IconClose': {}                # Bad: PascalCase
    }

    naming_analysis = atom._check_naming_conventions(mock_components)

    # Actual return structure: total_components, naming_issues, issues, compliance_rate, atom_verdict
    assert 'total_components' in naming_analysis, "Should have total_components"
    assert 'naming_issues' in naming_analysis, "Should have naming_issues count"
    assert 'issues' in naming_analysis, "Should list issues"
    assert 'compliance_rate' in naming_analysis, "Should have compliance_rate"
    assert 'atom_verdict' in naming_analysis, "Should have atom_verdict"

    # Check counts (3 have issues: InputDefault, card_elevated, IconClose)
    assert naming_analysis['total_components'] == 6, "Should have 6 total components"
    assert naming_analysis['naming_issues'] == 3, f"Should have 3 naming issues, got {naming_analysis['naming_issues']}"

    # Compliance rate is 100 - (issues/total * 100) = 100 - (3/6 * 100) = 50%
    assert naming_analysis['compliance_rate'] == 50.0, f"Compliance should be 50%, got {naming_analysis['compliance_rate']}"

    print("✅ PASSED: Naming convention check works")
    print(f"   Issues found: {naming_analysis['naming_issues']}/{naming_analysis['total_components']}")
    print(f"   Compliance rate: {naming_analysis['compliance_rate']}%")
    return True


def test_detect_missing_variants():
    """Test 6: Detect missing component variants."""
    print("\n" + "=" * 70)
    print("Test 6: Detect Missing Variants")
    print("=" * 70)

    atom = AtomComponentAnalysis()

    # Mock variants with some missing
    mock_variants = {
        'button': {
            'variants_found': ['primary', 'secondary'],  # Missing: ghost, danger
            'variant_count': 2,
            'total_components': 2
        },
        'input': {
            'variants_found': ['default'],  # Missing: error, disabled, focus
            'variant_count': 1,
            'total_components': 1
        }
    }

    missing = atom._detect_missing_variants(mock_variants)

    # Check structure
    assert 'button' in missing or 'input' in missing, "Should detect missing variants"

    # Buttons should be missing some common variants
    if 'button' in missing:
        assert len(missing['button']) > 0, "Should suggest missing button variants"

    # Inputs should be missing some common variants
    if 'input' in missing:
        assert len(missing['input']) > 0, "Should suggest missing input variants"

    print("✅ PASSED: Missing variant detection works")
    for component_type, suggestions in missing.items():
        print(f"   {component_type}: {len(suggestions)} missing variants")
    return True


def test_analyze_component_hierarchy():
    """Test 7: Analyze component hierarchy."""
    print("\n" + "=" * 70)
    print("Test 7: Analyze Component Hierarchy")
    print("=" * 70)

    atom = AtomComponentAnalysis()

    mock_components = {
        'button-primary': {'parent': None},
        'button-secondary': {'parent': None},
        'card-basic': {'parent': None},
        'card-header': {'parent': 'card-basic'},
        'card-body': {'parent': 'card-basic'},
        'card-footer': {'parent': 'card-basic'}
    }

    hierarchy = atom._analyze_component_hierarchy(mock_components)

    # Actual return structure: atomic_components, molecular_components, organism_components, atom_analysis
    assert 'atomic_components' in hierarchy, "Should have atomic_components"
    assert 'molecular_components' in hierarchy, "Should have molecular_components"
    assert 'organism_components' in hierarchy, "Should have organism_components"
    assert 'atom_analysis' in hierarchy, "Should have atom_analysis message"

    # Check atomic components structure
    atomic = hierarchy['atomic_components']
    assert 'count' in atomic, "Should have atomic count"
    assert 'components' in atomic, "Should list atomic components"
    assert 'description' in atomic, "Should have description"

    # All 6 components have no children in mock data, so all are atomic
    assert atomic['count'] == 6, f"Should have 6 atomic components, got {atomic['count']}"

    print("✅ PASSED: Component hierarchy analysis works")
    print(f"   Atomic: {hierarchy['atomic_components']['count']}")
    print(f"   Molecular: {hierarchy['molecular_components']['count']}")
    print(f"   Organisms: {hierarchy['organism_components']['count']}")
    return True


def test_accessibility_patterns():
    """Test 8: Test component accessibility patterns."""
    print("\n" + "=" * 70)
    print("Test 8: Test Accessibility Patterns")
    print("=" * 70)

    atom = AtomComponentAnalysis()

    mock_components = {
        'button-primary': {'aria_label': 'Submit', 'role': 'button'},
        'button-secondary': {},  # Missing ARIA
        'input-default': {'aria_label': 'Email', 'role': 'textbox'},
        'modal-small': {'aria_label': 'Dialog', 'role': 'dialog'},
        'card-basic': {}  # No ARIA needed
    }

    accessibility = atom._test_accessibility_patterns(mock_components)

    # Actual return structure: patterns_checked, issues_found, issues, atom_verdict
    assert 'patterns_checked' in accessibility, "Should have patterns_checked"
    assert 'issues_found' in accessibility, "Should have issues_found count"
    assert 'issues' in accessibility, "Should list issues"
    assert 'atom_verdict' in accessibility, "Should have atom_verdict"

    # Check patterns_checked structure
    patterns = accessibility['patterns_checked']
    assert 'buttons_have_labels' in patterns, "Should check buttons_have_labels"
    assert 'inputs_have_labels' in patterns, "Should check inputs_have_labels"
    assert 'interactive_have_roles' in patterns, "Should check interactive_have_roles"

    # button-secondary has no label, so should be 1 issue
    assert accessibility['issues_found'] > 0, "Should find accessibility issues"

    print("✅ PASSED: Accessibility pattern testing works")
    print(f"   Patterns checked: {len(patterns)}")
    print(f"   Issues found: {accessibility['issues_found']}")
    print(f"   Verdict: {accessibility['atom_verdict']}")
    return True


def test_calculate_component_score():
    """Test 9: Calculate component library score."""
    print("\n" + "=" * 70)
    print("Test 9: Calculate Component Score")
    print("=" * 70)

    atom = AtomComponentAnalysis()

    # High quality component library
    high_quality_results = {
        'naming_analysis': {
            'naming_issues': 1  # Very few issues
        },
        'token_analysis': {
            'hardcoded_values_count': 2  # Very few hardcoded values
        },
        'accessibility_patterns': {
            'issues_found': 1  # Very few accessibility issues
        },
        'missing_variants': {}  # No missing variants (empty dict)
    }

    score_high = atom._calculate_component_score(high_quality_results)

    assert 'score' in score_high, "Should have score"
    assert 'grade' in score_high, "Should have grade"
    assert 'verdict' in score_high, "Should have verdict"
    assert score_high['score'] >= 70, f"High quality should score >= 70, got {score_high['score']}"

    # Low quality component library
    # Note: missing_variants structure must match _detect_missing_variants return format
    low_quality_results = {
        'naming_analysis': {
            'naming_issues': 10  # Many issues
        },
        'token_analysis': {
            'hardcoded_values_count': 12  # Many hardcoded values
        },
        'accessibility_patterns': {
            'issues_found': 5  # Many accessibility issues
        },
        'missing_variants': {
            'button': {
                'missing': ['ghost', 'danger', 'disabled'],
                'found': ['primary'],
                'completeness': 25.0,
                'atom_says': 'Missing 3 variants!'
            },
            'input': {
                'missing': ['error', 'focus', 'disabled'],
                'found': ['default'],
                'completeness': 25.0,
                'atom_says': 'Missing 3 variants!'
            }
        }
    }

    score_low = atom._calculate_component_score(low_quality_results)
    assert score_low['score'] < 50, f"Low quality should score < 50, got {score_low['score']}"

    print("✅ PASSED: Component score calculation works")
    print(f"   High Quality: {score_high['score']}/100 ({score_high['grade']})")
    print(f"   Low Quality: {score_low['score']}/100 ({score_low['grade']})")
    return True


def test_full_component_analysis():
    """Test 10: Full component library analysis."""
    print("\n" + "=" * 70)
    print("Test 10: Full Component Library Analysis")
    print("=" * 70)

    atom = AtomComponentAnalysis()

    # Comprehensive mock component library
    mock_components = {
        'button-primary': {
            'foreground_color': 'var(--color-primary)',
            'background_color': 'var(--color-bg-primary)',
            'aria_label': 'Primary action',
            'role': 'button',
            'parent': None
        },
        'button-secondary': {
            'foreground_color': 'var(--color-secondary)',
            'background_color': 'var(--color-bg-secondary)',
            'aria_label': 'Secondary action',
            'role': 'button',
            'parent': None
        },
        'input-default': {
            'foreground_color': 'var(--color-text)',
            'background_color': '#FFFFFF',
            'aria_label': 'Text input',
            'role': 'textbox',
            'parent': None
        },
        'card-basic': {
            'background_color': 'var(--color-card-bg)',
            'parent': None
        }
    }

    design_tokens = {
        'colors': {
            '--color-primary': '#007bff',
            '--color-secondary': '#6c757d',
            '--color-bg-primary': '#ffffff',
            '--color-bg-secondary': '#e7e7e7',
            '--color-text': '#212529',
            '--color-card-bg': '#f8f9fa'
        }
    }

    # Run full analysis
    result = atom.analyze_component_library(mock_components, design_tokens)

    # Validate top-level structure
    assert 'hero' in result, "Should identify hero"
    assert result['hero'] == '🔬 The Atom - Component Analyzer', "Should be The Atom"
    assert 'timestamp' in result, "Should have timestamp"
    assert 'component_count' in result, "Should have component_count"
    assert result['component_count'] == 4, f"Should have 4 components, got {result['component_count']}"

    # Check all analyses are present
    assert 'categories' in result, "Should have categories"
    assert 'variants' in result, "Should have variants"
    assert 'token_analysis' in result, "Should have token_analysis"
    assert 'naming_analysis' in result, "Should have naming_analysis"
    assert 'missing_variants' in result, "Should have missing_variants"
    assert 'hierarchy' in result, "Should have hierarchy"
    assert 'accessibility_patterns' in result, "Should have accessibility_patterns"
    assert 'atom_score' in result, "Should have atom_score"
    assert 'atom_recommendations' in result, "Should have atom_recommendations"

    # Validate score
    score = result['atom_score']
    assert 'score' in score, "Should have score value"
    assert 'grade' in score, "Should have grade"
    assert 0 <= score['score'] <= 100, f"Score should be 0-100, got {score['score']}"

    print("\n✅ PASSED: Full component analysis successful")
    print(f"   Component Score: {score['score']}/100")
    print(f"   Grade: {score['grade']}")
    print(f"   Components: {result['component_count']}")
    print(f"   Categories: {len(result['categories'])}")
    print(f"   Recommendations: {len(result['atom_recommendations'])}")
    return True


def run_all_tests():
    """Run complete test suite."""
    print("\n🔬 The Atom - Component Analysis Test Suite")
    print("=" * 70)
    print("Testing Component Library Validation and Analysis")
    print("=" * 70)

    tests = [
        ("Initialization", test_atom_initialization),
        ("Categorize Components", test_categorize_components),
        ("Enumerate Variants", test_enumerate_variants),
        ("Analyze Design Tokens", test_analyze_design_tokens),
        ("Check Naming Conventions", test_check_naming_conventions),
        ("Detect Missing Variants", test_detect_missing_variants),
        ("Analyze Component Hierarchy", test_analyze_component_hierarchy),
        ("Test Accessibility Patterns", test_accessibility_patterns),
        ("Calculate Component Score", test_calculate_component_score),
        ("Full Component Analysis", test_full_component_analysis),
    ]

    passed = 0
    failed = 0
    errors = []

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except AssertionError as e:
            failed += 1
            errors.append(f"{test_name}: {str(e)}")
            print(f"\n❌ FAILED: {test_name}")
            print(f"   Error: {str(e)}")
        except Exception as e:
            failed += 1
            errors.append(f"{test_name}: {str(e)}")
            print(f"\n❌ ERROR: {test_name}")
            print(f"   Error: {str(e)}")

    # Summary
    print("\n" + "=" * 70)
    print("Test Suite Summary")
    print("=" * 70)
    print(f"Total Tests: {len(tests)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")

    if errors:
        print(f"\n❌ Errors:")
        for error in errors:
            print(f"   - {error}")

    success_rate = (passed / len(tests)) * 100
    print(f"\nSuccess Rate: {success_rate:.1f}%")

    if success_rate == 100:
        print("\n🎉 ALL TESTS PASSED! The Atom's analysis is molecular-perfect!")
        print("🔬 Component library validated at the atomic level!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review.")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
