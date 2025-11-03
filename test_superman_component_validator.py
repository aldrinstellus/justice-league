"""
🧪 Superman Component Library Validator - Test Suite
====================================================

Comprehensive tests for Component Library Validator functionality.

Test Coverage:
1. Basic component validation
2. Variant enumeration
3. Consistency checking
4. Design token validation
5. Coverage reporting

Author: Superman Testing Team
Version: 1.0.0
Created: 2025-10-23
"""

import sys
from pathlib import Path

# Add core directory to path
sys.path.insert(0, str(Path(__file__).parent / "core"))

from superman_component_validator import (
    SupermanComponentValidator,
    validate_library,
    ComponentTestResult,
    ConsistencyCheck,
    DesignTokenUsage,
    ComponentCoverageReport,
    SHADCN_COMPONENTS,
    COMPONENT_VARIANTS,
    DESIGN_TOKENS
)


def test_1_basic_component_validation():
    """
    Test 1: Basic Component Validation
    Validates that the validator can test components and return proper results
    """
    print("\n" + "=" * 70)
    print("TEST 1: Basic Component Validation")
    print("=" * 70)

    validator = SupermanComponentValidator(storage_dir="./test_component_validation")

    # Test a single component
    test_components = ["button"]

    report = validator.validate_component_library(
        library_name="test-library",
        components=test_components,
        validate_tokens=False,
        check_consistency=False
    )

    # Assertions
    assert report.library_name == "test-library", "Library name mismatch"
    assert report.total_components == 1, "Total components should be 1"
    assert report.tested_components == 1, "Tested components should be 1"
    assert report.tested_variants > 0, "Should test at least 1 variant"
    assert report.coverage_percentage >= 0, "Coverage should be >= 0"
    assert report.test_duration > 0, "Test duration should be > 0"

    print(f"✅ Report generated successfully")
    print(f"   Library: {report.library_name}")
    print(f"   Components: {report.tested_components}/{report.total_components}")
    print(f"   Variants tested: {report.tested_variants}")
    print(f"   Coverage: {report.coverage_percentage:.1f}%")
    print(f"   Duration: {report.test_duration:.2f}s")

    print("\n✅ TEST 1 PASSED: Basic validation working correctly")
    return True


def test_2_variant_enumeration():
    """
    Test 2: Variant Enumeration
    Tests that all component variants are properly enumerated and tested
    """
    print("\n" + "=" * 70)
    print("TEST 2: Variant Enumeration")
    print("=" * 70)

    validator = SupermanComponentValidator(storage_dir="./test_component_validation")

    # Test button component with multiple variants
    test_components = ["button", "input", "alert"]

    report = validator.validate_component_library(
        library_name="variant-test",
        components=test_components,
        validate_tokens=False,
        check_consistency=False
    )

    # Calculate expected variants
    expected_variants = 0
    for component in test_components:
        variants = validator._get_component_variants(component)
        expected_variants += len(variants)

    print(f"✅ Variant enumeration:")
    print(f"   Components: {len(test_components)}")
    print(f"   Expected variants: {expected_variants}")
    print(f"   Actual variants tested: {report.tested_variants}")

    # Button should have multiple variants (variant + size + state dimensions)
    button_variants = validator._get_component_variants("button")
    print(f"\n   Button variants found: {len(button_variants)}")
    print(f"   Example variants: {button_variants[:3]}")

    assert len(button_variants) > 1, "Button should have multiple variants"
    assert report.tested_variants == expected_variants, "Should test all enumerated variants"

    print("\n✅ TEST 2 PASSED: Variant enumeration working correctly")
    return True


def test_3_consistency_checking():
    """
    Test 3: Consistency Checking
    Tests that consistency checks work across components
    """
    print("\n" + "=" * 70)
    print("TEST 3: Consistency Checking")
    print("=" * 70)

    validator = SupermanComponentValidator(storage_dir="./test_component_validation")

    # Test multiple components for consistency
    test_components = ["button", "input", "card", "alert", "badge"]

    report = validator.validate_component_library(
        library_name="consistency-test",
        components=test_components,
        validate_tokens=False,
        check_consistency=True  # Enable consistency checking
    )

    print(f"✅ Consistency checks:")
    print(f"   Total checks: {len(report.consistency_checks)}")

    # Verify we have consistency checks
    assert len(report.consistency_checks) > 0, "Should have consistency checks"

    # Check for different types of consistency checks
    check_types = set(check.check_type for check in report.consistency_checks)
    print(f"   Check types: {', '.join(check_types)}")

    expected_check_types = ["spacing", "colors", "typography", "border_radius", "shadows"]
    for expected_type in expected_check_types:
        assert expected_type in check_types, f"Missing {expected_type} consistency check"

    # Count passed vs failed
    passed_checks = sum(1 for check in report.consistency_checks if check.passed)
    failed_checks = sum(1 for check in report.consistency_checks if not check.passed)

    print(f"   Passed: {passed_checks}")
    print(f"   Failed: {failed_checks}")

    # Show example check
    if report.consistency_checks:
        example = report.consistency_checks[0]
        print(f"\n   Example check:")
        print(f"      Type: {example.check_type}")
        print(f"      Passed: {example.passed}")
        print(f"      Details: {example.details}")

    print("\n✅ TEST 3 PASSED: Consistency checking working correctly")
    return True


def test_4_design_token_validation():
    """
    Test 4: Design Token Validation
    Tests that design token usage is properly analyzed
    """
    print("\n" + "=" * 70)
    print("TEST 4: Design Token Validation")
    print("=" * 70)

    validator = SupermanComponentValidator(storage_dir="./test_component_validation")

    # Test with token validation enabled
    test_components = ["button", "badge", "alert"]

    report = validator.validate_component_library(
        library_name="token-test",
        components=test_components,
        validate_tokens=True,  # Enable token validation
        check_consistency=False
    )

    print(f"✅ Design token analysis:")
    print(f"   Total tokens analyzed: {len(report.token_usage)}")

    # Verify we have token usage data
    assert len(report.token_usage) > 0, "Should have token usage data"

    # Group by token type
    by_type = {}
    for token in report.token_usage:
        if token.token_type not in by_type:
            by_type[token.token_type] = []
        by_type[token.token_type].append(token)

    print(f"   Token types:")
    for token_type, tokens in by_type.items():
        used = sum(1 for t in tokens if t.used)
        print(f"      {token_type}: {used}/{len(tokens)} used")

    # Check for different token types
    assert "color" in by_type, "Should have color tokens"
    assert "spacing" in by_type, "Should have spacing tokens"
    assert "typography" in by_type, "Should have typography tokens"

    # Show some used tokens
    used_tokens = [t for t in report.token_usage if t.used][:3]
    print(f"\n   Example used tokens:")
    for token in used_tokens:
        print(f"      {token.token_name}: used by {', '.join(token.components_using)}")

    # Calculate token coverage
    used_count = sum(1 for t in report.token_usage if t.used)
    token_coverage = used_count / len(report.token_usage) * 100

    print(f"\n   Token coverage: {token_coverage:.1f}%")

    print("\n✅ TEST 4 PASSED: Design token validation working correctly")
    return True


def test_5_coverage_reporting():
    """
    Test 5: Coverage Reporting
    Tests complete coverage report generation with all features
    """
    print("\n" + "=" * 70)
    print("TEST 5: Coverage Reporting")
    print("=" * 70)

    validator = SupermanComponentValidator(storage_dir="./test_component_validation")

    # Full validation with all features
    test_components = ["button", "input", "card", "alert", "badge", "select"]

    report = validator.validate_component_library(
        library_name="full-test",
        components=test_components,
        validate_tokens=True,
        check_consistency=True
    )

    print(f"✅ Complete coverage report:")
    print(f"   Library: {report.library_name}")
    print(f"   Components: {report.tested_components}/{report.total_components}")
    print(f"   Variants: {report.tested_variants}/{report.total_variants}")
    print(f"   Passed: {report.passed_tests}")
    print(f"   Failed: {report.failed_tests}")
    print(f"   Coverage: {report.coverage_percentage:.1f}%")
    print(f"   Duration: {report.test_duration:.2f}s")

    # Verify all report sections
    assert report.consistency_checks is not None, "Should have consistency checks"
    assert report.token_usage is not None, "Should have token usage"
    assert report.recommendations is not None, "Should have recommendations"
    assert len(report.recommendations) > 0, "Should have at least 1 recommendation"

    print(f"\n   Consistency checks: {len(report.consistency_checks)}")
    print(f"   Token analysis: {len(report.token_usage)} tokens")
    print(f"   Recommendations: {len(report.recommendations)}")

    # Show recommendations
    print(f"\n   Top recommendations:")
    for i, rec in enumerate(report.recommendations[:3], 1):
        print(f"      {i}. {rec}")

    # Test report retrieval
    summary = validator.get_coverage_summary("full-test")
    assert summary is not None, "Should retrieve saved report"
    assert summary["coverage"] == report.coverage_percentage, "Coverage should match"

    print(f"\n   ✅ Report saved and retrievable")

    # Test convenience function
    print(f"\n   Testing convenience function...")
    quick_report = validate_library(
        library_name="quick-test",
        components=["button", "input"]
    )

    assert quick_report.library_name == "quick-test", "Convenience function should work"
    print(f"   ✅ Convenience function working")

    print("\n✅ TEST 5 PASSED: Coverage reporting working correctly")
    return True


def test_6_component_definitions():
    """
    Bonus Test: Component Definitions
    Verifies that component definitions are comprehensive
    """
    print("\n" + "=" * 70)
    print("BONUS TEST: Component Definitions")
    print("=" * 70)

    print(f"✅ Component library definitions:")
    print(f"   Total shadcn components: {len(SHADCN_COMPONENTS)}")
    print(f"   Components with variants: {len(COMPONENT_VARIANTS)}")

    # Verify we have comprehensive component list
    assert len(SHADCN_COMPONENTS) >= 40, "Should have at least 40 shadcn components"

    # Show component categories
    print(f"\n   Sample components:")
    print(f"      Form: button, input, select, checkbox")
    print(f"      Layout: card, separator, container")
    print(f"      Navigation: tabs, menubar, breadcrumb")
    print(f"      Feedback: alert, dialog, toast")

    # Verify variant definitions
    assert "button" in COMPONENT_VARIANTS, "Button should have variant definition"
    assert "input" in COMPONENT_VARIANTS, "Input should have variant definition"

    button_variants = COMPONENT_VARIANTS["button"]
    print(f"\n   Button variant dimensions: {list(button_variants.keys())}")

    # Verify design tokens
    print(f"\n   Design token categories: {list(DESIGN_TOKENS.keys())}")
    assert "colors" in DESIGN_TOKENS, "Should have color tokens"
    assert "spacing" in DESIGN_TOKENS, "Should have spacing tokens"
    assert "typography" in DESIGN_TOKENS, "Should have typography tokens"

    print("\n✅ BONUS TEST PASSED: Component definitions comprehensive")
    return True


def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "=" * 70)
    print("🦸 SUPERMAN COMPONENT LIBRARY VALIDATOR - TEST SUITE")
    print("=" * 70)
    print("\nRunning comprehensive test suite...")

    tests = [
        ("Basic Component Validation", test_1_basic_component_validation),
        ("Variant Enumeration", test_2_variant_enumeration),
        ("Consistency Checking", test_3_consistency_checking),
        ("Design Token Validation", test_4_design_token_validation),
        ("Coverage Reporting", test_5_coverage_reporting),
        ("Component Definitions", test_6_component_definitions),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result, None))
        except Exception as e:
            print(f"\n❌ TEST FAILED: {name}")
            print(f"   Error: {str(e)}")
            results.append((name, False, str(e)))

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result, _ in results if result)
    total = len(results)

    for name, result, error in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
        if error:
            print(f"         {error}")

    print(f"\n" + "=" * 70)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print("=" * 70)

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Component Library Validator is production-ready!")
        print("\n🦸 Superman says: 'Component validation perfected! Design systems are now bulletproof!'")
        return True
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Review errors above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
