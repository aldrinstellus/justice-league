#!/usr/bin/env python3
"""
🎩 ZATANNA - SEO & Metadata Test Suite
========================================

Tests for SEO validation and metadata optimization capabilities.
Zatanna speaks backwards to cast magical SEO spells!

Author: Justice League
Created: October 23, 2025
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.justice_league.zatanna_seo import ZatannaSEO


def test_zatanna_initialization():
    """Test 1: Zatanna SEO initialization."""
    print("\n" + "=" * 70)
    print("Test 1: Zatanna SEO Initialization")
    print("=" * 70)

    zatanna = ZatannaSEO()

    assert zatanna is not None, "Zatanna should initialize"
    assert hasattr(zatanna, 'analyze_seo_magic'), "Should have analyze_seo_magic method"
    assert hasattr(zatanna, '_backwards_spell_meta_reveal'), "Should have _backwards_spell_meta_reveal method"
    assert hasattr(zatanna, '_backwards_spell_structured_data'), "Should have _backwards_spell_structured_data method"
    assert hasattr(zatanna, '_backwards_spell_crawlability'), "Should have _backwards_spell_crawlability method"

    # Check magic spells
    assert hasattr(zatanna, 'MAGIC_SPELLS'), "Should have MAGIC_SPELLS"
    assert 'meta_reveal' in zatanna.MAGIC_SPELLS, "Should have meta_reveal spell"
    assert 'structured_data' in zatanna.MAGIC_SPELLS, "Should have structured_data spell"
    assert 'crawlability' in zatanna.MAGIC_SPELLS, "Should have crawlability spell"

    # Check SEO constants
    assert zatanna.TITLE_MIN_LENGTH == 30, "Title min length should be 30"
    assert zatanna.TITLE_MAX_LENGTH == 60, "Title max length should be 60"
    assert zatanna.DESCRIPTION_MIN_LENGTH == 120, "Description min length should be 120"
    assert zatanna.DESCRIPTION_MAX_LENGTH == 160, "Description max length should be 160"
    assert zatanna.H1_MAX_COUNT == 1, "Should have exactly 1 H1"

    print("✅ PASSED: Zatanna initialized successfully")
    print(f"   Magic Spells: {len(zatanna.MAGIC_SPELLS)}")
    print(f"   Supported Schemas: {len(zatanna.SUPPORTED_SCHEMAS)}")
    return True


def test_magic_spells_configuration():
    """Test 2: Magic spells configuration (backwards!)."""
    print("\n" + "=" * 70)
    print("Test 2: Magic Spells Configuration")
    print("=" * 70)

    zatanna = ZatannaSEO()

    # Validate backwards spell format
    assert zatanna.MAGIC_SPELLS['meta_reveal'] == '!sgat atem laeveR', "Spell should be backwards"
    assert zatanna.MAGIC_SPELLS['structured_data'] == '!atad derutcurts dniFsuoicam', "Should be backwards"
    assert zatanna.MAGIC_SPELLS['crawlability'] == '!ytilibwalwarckcehC', "Should be backwards"
    assert zatanna.MAGIC_SPELLS['seo_score'] == '!erocs OES etaluclaC', "Should be backwards"
    assert zatanna.MAGIC_SPELLS['magic_fix'] == '!seussi OES xiFcigaM', "Should be backwards"

    # All spells should start with ! and be backwards
    for spell_name, spell_text in zatanna.MAGIC_SPELLS.items():
        assert spell_text.startswith('!'), f"{spell_name} spell should start with !"

    # Check supported schemas
    assert 'Organization' in zatanna.SUPPORTED_SCHEMAS, "Should support Organization"
    assert 'Product' in zatanna.SUPPORTED_SCHEMAS, "Should support Product"
    assert 'Article' in zatanna.SUPPORTED_SCHEMAS, "Should support Article"

    print("✅ PASSED: All magic spells configured correctly")
    print(f"   Total Spells: {len(zatanna.MAGIC_SPELLS)}")
    print(f"   Example: '{zatanna.MAGIC_SPELLS['meta_reveal']}'")
    return True


def test_validate_title():
    """Test 3: Title tag validation."""
    print("\n" + "=" * 70)
    print("Test 3: Title Tag Validation")
    print("=" * 70)

    zatanna = ZatannaSEO()

    # Perfect title
    good_title = "Perfect Title Tag for SEO Testing Example"
    result_good = zatanna._validate_title(good_title)

    assert 'valid' in result_good, "Should have valid"
    assert 'length' in result_good, "Should have length"
    assert 'issues' in result_good, "Should have issues"

    assert result_good['valid'] is True, "Good title should be valid"
    assert result_good['length'] == len(good_title), f"Should calculate correct length, got {result_good['length']}"
    assert len(result_good['issues']) == 0, "Good title should have no issues"

    # Too short title
    short_title = "Too Short"
    result_short = zatanna._validate_title(short_title)
    assert result_short['valid'] is False, "Short title should be invalid"
    assert len(result_short['issues']) > 0, "Should have issues"

    # Too long title
    long_title = "This is a very long title tag that exceeds the maximum recommended length for SEO"
    result_long = zatanna._validate_title(long_title)
    assert result_long['valid'] is False, "Long title should be invalid"

    # Missing title
    empty_title = ""
    result_empty = zatanna._validate_title(empty_title)
    assert result_empty['valid'] is False, "Empty title should be invalid"

    print("✅ PASSED: Title validation works")
    print(f"   Good Title: {result_good['length']} chars, valid={result_good['valid']}")
    print(f"   Short Title: {result_short['length']} chars, valid={result_short['valid']}")
    return True


def test_validate_description():
    """Test 4: Meta description validation."""
    print("\n" + "=" * 70)
    print("Test 4: Meta Description Validation")
    print("=" * 70)

    zatanna = ZatannaSEO()

    # Perfect description (145 chars)
    good_desc = "This is a perfect meta description for SEO testing that provides a clear and concise summary of the page content in the ideal length range."
    result_good = zatanna._validate_description(good_desc)

    assert 'valid' in result_good, "Should have valid"
    assert 'length' in result_good, "Should have length"
    assert 'issues' in result_good, "Should have issues"

    assert result_good['valid'] is True, "Good description should be valid"
    assert 120 <= result_good['length'] <= 160, f"Should be in range, got {result_good['length']}"
    assert len(result_good['issues']) == 0, "Good description should have no issues"

    # Too short
    short_desc = "Too short description"
    result_short = zatanna._validate_description(short_desc)
    assert result_short['valid'] is False, "Short description should be invalid"

    # Too long
    long_desc = "A" * 200
    result_long = zatanna._validate_description(long_desc)
    assert result_long['valid'] is False, "Long description should be invalid"

    print("✅ PASSED: Description validation works")
    print(f"   Good Description: {result_good['length']} chars")
    print(f"   Short Description: {result_short['length']} chars")
    return True


def test_validate_canonical():
    """Test 5: Canonical URL validation."""
    print("\n" + "=" * 70)
    print("Test 5: Canonical URL Validation")
    print("=" * 70)

    zatanna = ZatannaSEO()

    # Valid canonical
    valid_canonical = "https://example.com/page"
    result_valid = zatanna._validate_canonical(valid_canonical)

    assert 'valid' in result_valid, "Should have valid"
    assert 'issues' in result_valid, "Should have issues"

    assert result_valid['valid'] is True, "Valid canonical should pass"
    assert len(result_valid['issues']) == 0, "Should have no issues"

    # Missing canonical
    empty_canonical = ""
    result_empty = zatanna._validate_canonical(empty_canonical)
    assert result_empty['valid'] is False, "Empty canonical should fail"

    # Relative canonical (should be absolute)
    relative_canonical = "/page/path"
    result_relative = zatanna._validate_canonical(relative_canonical)
    assert result_relative['valid'] is False, "Relative canonical should fail"

    print("✅ PASSED: Canonical validation works")
    print(f"   Valid: {result_valid['valid']}")
    print(f"   Empty: {result_empty['valid']}")
    print(f"   Relative: {result_relative['valid']}")
    return True


def test_validate_open_graph():
    """Test 6: Open Graph tags validation."""
    print("\n" + "=" * 70)
    print("Test 6: Open Graph Tags Validation")
    print("=" * 70)

    zatanna = ZatannaSEO()

    # Complete Open Graph tags
    complete_og = {
        'title': 'Page Title',
        'description': 'Page description',
        'image': 'https://example.com/image.jpg',
        'url': 'https://example.com/page'
    }
    result_complete = zatanna._validate_open_graph(complete_og)

    assert 'valid' in result_complete, "Should have valid"
    assert 'present_tags' in result_complete, "Should have present_tags"
    assert 'issues' in result_complete, "Should have issues"

    assert result_complete['valid'] is True, "Complete OG should be valid"
    assert result_complete['present_tags'] == 4, "Should have 4 tags"
    assert len(result_complete['issues']) == 0, "Should have no issues"

    # Incomplete Open Graph
    incomplete_og = {'title': 'Only Title'}
    result_incomplete = zatanna._validate_open_graph(incomplete_og)

    assert result_incomplete['valid'] is False, "Incomplete OG should be invalid"
    assert len(result_incomplete['issues']) > 0, "Should have issues"

    # Empty Open Graph
    empty_og = {}
    result_empty = zatanna._validate_open_graph(empty_og)
    assert len(result_empty['issues']) == 4, "Should have 4 missing required tags"

    print("✅ PASSED: Open Graph validation works")
    print(f"   Complete: {result_complete['present_tags']} tags, valid={result_complete['valid']}")
    print(f"   Incomplete: {result_incomplete['present_tags']} tag, valid={result_incomplete['valid']}")
    return True


def test_validate_twitter_card():
    """Test 7: Twitter Card validation."""
    print("\n" + "=" * 70)
    print("Test 7: Twitter Card Validation")
    print("=" * 70)

    zatanna = ZatannaSEO()

    # Complete Twitter Card
    complete_twitter = {
        'card': 'summary_large_image',
        'title': 'Page Title',
        'description': 'Page description',
        'image': 'https://example.com/image.jpg'
    }
    result_complete = zatanna._validate_twitter_card(complete_twitter)

    assert 'valid' in result_complete, "Should have valid"
    assert 'present_tags' in result_complete, "Should have present_tags"
    assert 'issues' in result_complete, "Should have issues"

    assert result_complete['valid'] is True, "Complete Twitter Card should be valid"
    assert len(result_complete['issues']) == 0, "Should have no issues"

    # Missing required tags
    incomplete_twitter = {'description': 'Only description'}
    result_incomplete = zatanna._validate_twitter_card(incomplete_twitter)

    assert result_incomplete['valid'] is False, "Incomplete Twitter Card should be invalid"
    assert len(result_incomplete['issues']) >= 2, "Should have at least 2 issues (card, title)"

    print("✅ PASSED: Twitter Card validation works")
    print(f"   Complete: valid={result_complete['valid']}")
    print(f"   Incomplete: {len(result_incomplete['issues'])} issues")
    return True


def test_validate_viewport():
    """Test 8: Viewport meta tag validation."""
    print("\n" + "=" * 70)
    print("Test 8: Viewport Meta Tag Validation")
    print("=" * 70)

    zatanna = ZatannaSEO()

    # Good viewport
    good_viewport = "width=device-width, initial-scale=1"
    result_good = zatanna._validate_viewport(good_viewport)

    assert 'valid' in result_good, "Should have valid"
    assert 'issues' in result_good, "Should have issues"

    assert result_good['valid'] is True, "Good viewport should be valid"
    assert len(result_good['issues']) == 0, "Should have no issues"

    # Missing width=device-width
    bad_viewport = "initial-scale=1"
    result_bad = zatanna._validate_viewport(bad_viewport)
    assert result_bad['valid'] is False, "Bad viewport should be invalid"

    # Missing viewport
    empty_viewport = ""
    result_empty = zatanna._validate_viewport(empty_viewport)
    assert result_empty['valid'] is False, "Empty viewport should be invalid"

    print("✅ PASSED: Viewport validation works")
    print(f"   Good: valid={result_good['valid']}")
    print(f"   Bad: valid={result_bad['valid']}")
    return True


def test_calculate_zatanna_score():
    """Test 9: Calculate Zatanna SEO score."""
    print("\n" + "=" * 70)
    print("Test 9: Calculate Zatanna SEO Score")
    print("=" * 70)

    zatanna = ZatannaSEO()

    # Perfect SEO (no issues)
    perfect_results = {
        'issues': []
    }

    score_perfect = zatanna._calculate_zatanna_score(perfect_results)

    assert 'score' in score_perfect, "Should have score"
    assert 'grade' in score_perfect, "Should have grade"
    assert 'verdict' in score_perfect, "Should have verdict"
    assert 'breakdown' in score_perfect, "Should have breakdown"

    assert score_perfect['score'] == 100, f"Perfect SEO should score 100, got {score_perfect['score']}"
    assert score_perfect['grade'] == 'S+', "Perfect SEO should be S+ grade"
    assert score_perfect['breakdown']['total_issues'] == 0, "Should have 0 issues"

    # Poor SEO (multiple issues)
    poor_results = {
        'issues': [
            {'severity': 'critical', 'issue': 'noindex'},
            {'severity': 'critical', 'issue': 'missing viewport'},
            {'severity': 'high', 'issue': 'missing title'},
            {'severity': 'high', 'issue': 'missing description'},
            {'severity': 'high', 'issue': 'missing H1'},
            {'severity': 'medium', 'issue': 'missing canonical'},
            {'severity': 'medium', 'issue': 'missing OG tags'},
            {'severity': 'low', 'issue': 'broken links'}
        ]
    }

    score_poor = zatanna._calculate_zatanna_score(poor_results)

    # Score calculation: 100 - (2*15 + 3*10 + 2*5 + 1*2) = 100 - (30 + 30 + 10 + 2) = 28
    expected_score = 100 - (2 * 15) - (3 * 10) - (2 * 5) - (1 * 2)
    assert score_poor['score'] == expected_score, f"Score should be {expected_score}, got {score_poor['score']}"
    assert score_poor['score'] < 60, f"Poor SEO should score < 60, got {score_poor['score']}"
    assert score_poor['breakdown']['critical_issues'] == 2, "Should have 2 critical issues"
    assert score_poor['breakdown']['high_issues'] == 3, "Should have 3 high issues"
    assert score_poor['breakdown']['medium_issues'] == 2, "Should have 2 medium issues"
    assert score_poor['breakdown']['low_issues'] == 1, "Should have 1 low issue"

    print("✅ PASSED: Scoring works correctly")
    print(f"   Perfect: {score_perfect['score']}/100 ({score_perfect['grade']})")
    print(f"   Poor: {score_poor['score']}/100 ({score_poor['grade']})")
    print(f"   Perfect Verdict: {score_perfect['verdict']}")
    return True


def test_generate_magic_recommendations():
    """Test 10: Generate magical SEO recommendations."""
    print("\n" + "=" * 70)
    print("Test 10: Generate Magic Recommendations")
    print("=" * 70)

    zatanna = ZatannaSEO()

    # Results with various issues
    results_with_issues = {
        'issues': [
            {'category': 'Meta Tags', 'severity': 'critical', 'issue': 'Missing title tag'},
            {'category': 'Meta Tags', 'severity': 'high', 'issue': 'Missing meta description'},
            {'category': 'Headings', 'severity': 'high', 'issue': 'Missing H1 tag'},
            {'category': 'Images', 'severity': 'medium', 'issue': '5 images missing alt text'},
            {'category': 'Mobile', 'severity': 'medium', 'issue': 'Missing viewport meta tag'}
        ],
        'core_web_vitals_impact': {
            'recommendations': [
                'Add async or defer attributes to non-critical scripts',
                'Add explicit width/height to images to prevent CLS'
            ]
        }
    }

    recommendations = zatanna._generate_magic_recommendations(results_with_issues)

    assert isinstance(recommendations, list), "Should return list of recommendations"
    assert len(recommendations) > 0, "Should have recommendations for issues"

    # Check recommendation structure
    for rec in recommendations:
        assert 'priority' in rec, "Should have priority"
        assert 'category' in rec, "Should have category"
        assert 'issue' in rec, "Should have issue"
        assert 'magic_spell' in rec, "Should have magic_spell (backwards!)"
        assert 'recommendation' in rec, "Should have recommendation"

        # Magic spells should be backwards (start with !)
        assert rec['magic_spell'].startswith('!'), "Magic spell should be backwards (start with !)"

    # Check priority ordering (CRITICAL first)
    first_rec = recommendations[0]
    assert first_rec['priority'] == 'CRITICAL', "First recommendation should be CRITICAL"

    # Results without issues
    perfect_results = {
        'issues': [],
        'core_web_vitals_impact': {
            'recommendations': []
        }
    }

    recommendations_perfect = zatanna._generate_magic_recommendations(perfect_results)
    # Even perfect results might have CWV recommendations, so just check it's a list
    assert isinstance(recommendations_perfect, list), "Should return list even for perfect results"

    print("✅ PASSED: Recommendation generation works")
    print(f"   With Issues: {len(recommendations)} recommendations")
    print(f"   First Priority: {first_rec['priority']}")
    print(f"   Example Spell: '{first_rec['magic_spell']}'")
    return True


def run_all_tests():
    """Run complete test suite."""
    print("\n🎩 Zatanna - SEO & Metadata Test Suite")
    print("=" * 70)
    print("Testing SEO Validation and Metadata Optimization")
    print("=" * 70)

    tests = [
        ("Initialization", test_zatanna_initialization),
        ("Magic Spells Configuration", test_magic_spells_configuration),
        ("Validate Title", test_validate_title),
        ("Validate Description", test_validate_description),
        ("Validate Canonical", test_validate_canonical),
        ("Validate Open Graph", test_validate_open_graph),
        ("Validate Twitter Card", test_validate_twitter_card),
        ("Validate Viewport", test_validate_viewport),
        ("Calculate Zatanna Score", test_calculate_zatanna_score),
        ("Generate Magic Recommendations", test_generate_magic_recommendations),
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
        print("\n🎉 ALL TESTS PASSED! Zatanna's magic is perfect!")
        print("🎩 !tcefrepsi OES ruoY (Your SEO is perfect!)")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review.")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
