#!/usr/bin/env python3
"""
🎨 Artemis CodeSmith Test Suite
================================

Tests for Figma-to-Code generation capability.

Author: Justice League
Created: October 23, 2025
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.justice_league.artemis_codesmith import ArtemisCodeSmith


def test_codesmith_initialization():
    """Test 1: Artemis CodeSmith initialization."""
    print("\n" + "=" * 70)
    print("Test 1: Artemis CodeSmith Initialization")
    print("=" * 70)

    codesmith = ArtemisCodeSmith()

    assert codesmith is not None, "CodeSmith should initialize"
    assert hasattr(codesmith, 'generate_component_code'), "Should have generate_component_code method"
    assert hasattr(codesmith, 'generate_full_page'), "Should have generate_full_page method"

    print("✅ PASSED: Artemis CodeSmith initialized successfully")
    return True


def test_figma_url_parsing():
    """Test 2: Figma URL parsing."""
    print("\n" + "=" * 70)
    print("Test 2: Figma URL Parsing")
    print("=" * 70)

    codesmith = ArtemisCodeSmith()

    # Test URL with node ID
    file_id, node_id = codesmith._parse_figma_url(
        "https://www.figma.com/file/abc123xyz/MyDesign?node-id=1-2"
    )

    assert file_id == "abc123xyz", f"Expected 'abc123xyz', got '{file_id}'"
    assert node_id == "1-2", f"Expected '1-2', got '{node_id}'"

    # Test URL without node ID
    file_id2, node_id2 = codesmith._parse_figma_url(
        "https://www.figma.com/file/xyz789/AnotherDesign"
    )

    assert file_id2 == "xyz789", f"Expected 'xyz789', got '{file_id2}'"
    assert node_id2 is None, f"Expected None, got '{node_id2}'"

    print("✅ PASSED: Figma URL parsing works correctly")
    return True


def test_component_generation():
    """Test 3: Component code generation."""
    print("\n" + "=" * 70)
    print("Test 3: Component Code Generation")
    print("=" * 70)

    codesmith = ArtemisCodeSmith()

    result = codesmith.generate_component_code(
        figma_url="https://www.figma.com/file/test123/TestDesign?node-id=1-2",
        component_name="TestComponent",
        framework="next",
        language="typescript",
        options={
            'include_tests': True,
            'include_stories': True,
            'accessibility': True,
            'responsive': True,
        }
    )

    # Verify result structure
    assert result['success'], f"Generation should succeed, got errors: {result.get('errors')}"
    assert 'files' in result, "Result should contain 'files'"
    assert 'artemis_score' in result, "Result should contain 'artemis_score'"
    assert result['artemis_score'] > 0, f"Artemis score should be > 0, got {result['artemis_score']}"

    # Verify files generated
    files = result['files']
    assert len(files) >= 1, f"Should generate at least 1 file, got {len(files)}"

    # Check for component file
    component_files = [f for f in files.keys() if 'TestComponent' in f and '.tsx' in f]
    assert len(component_files) >= 1, "Should generate component .tsx file"

    # Check for test file
    test_files = [f for f in files.keys() if 'test.tsx' in f]
    assert len(test_files) >= 1, "Should generate test file when include_tests=True"

    # Check for story file
    story_files = [f for f in files.keys() if 'stories.tsx' in f]
    assert len(story_files) >= 1, "Should generate story file when include_stories=True"

    print(f"\n✅ PASSED: Generated {len(files)} files with Artemis Score: {result['artemis_score']}/100")

    # Print generated files
    print(f"\n📁 Generated Files:")
    for file_path in files.keys():
        print(f"   - {file_path}")

    return True


def test_artemis_score_calculation():
    """Test 4: Artemis Score calculation."""
    print("\n" + "=" * 70)
    print("Test 4: Artemis Score Calculation")
    print("=" * 70)

    codesmith = ArtemisCodeSmith()

    # Test with all quality factors
    code_result_high = {
        'files': {
            'comp.tsx': 'code',
            'comp.test.tsx': 'test',
            'comp.stories.tsx': 'story'
        },
        'quality_report': {
            'typescript_strict': True,
            'accessibility': True,
            'responsive': True,
            'test_coverage': True
        }
    }

    score_high = codesmith._calculate_artemis_score(code_result_high)
    assert score_high >= 90, f"High quality should score >= 90, got {score_high}"

    # Test with minimal quality
    code_result_low = {
        'files': {'comp.jsx': 'code'},
        'quality_report': {
            'typescript_strict': False,
            'accessibility': False,
            'responsive': False,
            'test_coverage': False
        }
    }

    score_low = codesmith._calculate_artemis_score(code_result_low)
    assert score_low < 50, f"Low quality should score < 50, got {score_low}"

    print(f"✅ PASSED: Artemis Score calculation works")
    print(f"   High Quality Score: {score_high}/100")
    print(f"   Low Quality Score:  {score_low}/100")

    return True


def test_dependency_extraction():
    """Test 5: Dependency extraction."""
    print("\n" + "=" * 70)
    print("Test 5: Dependency Extraction")
    print("=" * 70)

    codesmith = ArtemisCodeSmith()

    mapping = {
        'components': [
            {'name': 'Button'},
            {'name': 'Input'},
            {'name': 'Label'}
        ]
    }

    deps = codesmith._extract_dependencies(mapping)

    # Check core dependencies
    assert 'react' in deps, "Should include react"
    assert 'react-dom' in deps, "Should include react-dom"
    assert 'tailwind-merge' in deps, "Should include tailwind-merge"
    assert '@radix-ui/react-slot' in deps, "Should include @radix-ui/react-slot"

    print(f"✅ PASSED: Extracted {len(deps)} dependencies")
    print(f"\n📦 Dependencies:")
    for dep in sorted(deps):
        print(f"   - {dep}")

    return True


def test_code_template_generation():
    """Test 6: Code template generation."""
    print("\n" + "=" * 70)
    print("Test 6: Code Template Generation")
    print("=" * 70)

    codesmith = ArtemisCodeSmith()

    # Test TypeScript component template
    ts_component = codesmith._generate_component_template(
        component_name="TestComponent",
        mapping={'components': [{'name': 'Button'}]},
        language="typescript",
        options={}
    )

    assert 'import React from' in ts_component, "Should have React import"
    assert 'interface TestComponentProps' in ts_component, "Should have TypeScript interface"
    assert 'export function TestComponent' in ts_component, "Should export component"
    assert 'className' in ts_component, "Should support className prop"

    # Test JavaScript component template
    js_component = codesmith._generate_component_template(
        component_name="TestComponent",
        mapping={'components': []},
        language="javascript",
        options={}
    )

    assert 'import React from' in js_component, "JS should have React import"
    assert 'export function TestComponent' in js_component, "JS should export component"
    assert 'interface' not in js_component, "JS should not have TypeScript interface"

    print("✅ PASSED: Code template generation works for TypeScript and JavaScript")

    return True


def test_full_integration():
    """Test 7: Full integration test."""
    print("\n" + "=" * 70)
    print("Test 7: Full Integration Test")
    print("=" * 70)

    codesmith = ArtemisCodeSmith()

    # Generate complete component with all options
    result = codesmith.generate_component_code(
        figma_url="https://www.figma.com/file/full-test/FullTest?node-id=100-200",
        component_name="LoginForm",
        framework="next",
        language="typescript",
        options={
            'include_types': True,
            'include_props': True,
            'include_state': False,
            'accessibility': True,
            'responsive': True,
            'include_tests': True,
            'include_stories': True,
        }
    )

    assert result['success'], "Full integration should succeed"
    assert result['artemis_score'] > 80, f"Should have high score, got {result['artemis_score']}"
    assert len(result['files']) >= 3, f"Should generate 3+ files, got {len(result['files'])}"

    print(f"\n✅ PASSED: Full integration test successful")
    print(f"   Artemis Score: {result['artemis_score']}/100")
    print(f"   Files Generated: {len(result['files'])}")
    print(f"   Dependencies: {len(result['dependencies'])}")

    return True


def run_all_tests():
    """Run complete test suite."""
    print("\n🎨 Artemis CodeSmith Test Suite")
    print("=" * 70)
    print("Testing Figma-to-Code Generation Capability")
    print("=" * 70)

    tests = [
        ("Initialization", test_codesmith_initialization),
        ("Figma URL Parsing", test_figma_url_parsing),
        ("Component Generation", test_component_generation),
        ("Artemis Score Calculation", test_artemis_score_calculation),
        ("Dependency Extraction", test_dependency_extraction),
        ("Code Template Generation", test_code_template_generation),
        ("Full Integration", test_full_integration),
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
        print("\n🎉 ALL TESTS PASSED! Artemis CodeSmith is ready!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review.")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
