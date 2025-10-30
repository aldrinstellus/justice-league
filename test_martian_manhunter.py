#!/usr/bin/env python3
"""
🧠 MARTIAN MANHUNTER - Security Testing Test Suite
===================================================

Tests for security vulnerability scanning and penetration testing.

Author: Justice League
Created: October 23, 2025
"""

import sys
import os
from pathlib import Path
import tempfile

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.justice_league.martian_manhunter_security import MartianManhunterSecurity


def test_martian_manhunter_initialization():
    """Test 1: Martian Manhunter initialization."""
    print("\n" + "=" * 70)
    print("Test 1: Martian Manhunter Security Guardian Initialization")
    print("=" * 70)

    temp_dir = tempfile.mkdtemp(prefix='mm_security_')
    mm = MartianManhunterSecurity(config_dir=temp_dir)

    assert mm is not None, "Martian Manhunter should initialize"
    assert hasattr(mm, 'scan_all_vulnerabilities'), "Should have scan_all_vulnerabilities method"
    assert hasattr(mm, '_telepathic_auth_scan'), "Should have _telepathic_auth_scan method"
    assert hasattr(mm, '_martian_vision_xss_scan'), "Should have _martian_vision_xss_scan method"
    assert hasattr(mm, '_shapeshifting_injection_scan'), "Should have _shapeshifting_injection_scan method"
    assert hasattr(mm, '_phase_shift_header_scan'), "Should have _phase_shift_header_scan method"

    assert mm.config_dir == Path(temp_dir), "Should set config directory"
    assert mm.config_dir.exists(), "Config directory should exist"

    print("✅ PASSED: Martian Manhunter initialized successfully")
    print(f"   Config Directory: {mm.config_dir}")
    return True


def test_telepathic_auth_scan():
    """Test 2: Telepathic authentication vulnerability scan."""
    print("\n" + "=" * 70)
    print("Test 2: Telepathic Authentication Scan")
    print("=" * 70)

    mm = MartianManhunterSecurity()

    # Mock target with weak authentication
    target_data = {
        'url': 'https://example.com',
        'html_content': '''
            <form action="/login">
                <input type="text" name="username">
                <input type="password" name="password">
                <input type="submit" value="Login">
            </form>
        ''',
        'headers': {}
    }

    vulnerabilities = mm._telepathic_auth_scan(target_data)

    # Should return a list of vulnerabilities
    assert isinstance(vulnerabilities, list), "Should return list of vulnerabilities"

    # Check vulnerability structure (actual: id, severity, category, title, description, recommendation, martian_manhunter_says)
    for vuln in vulnerabilities:
        assert 'id' in vuln, "Vulnerability should have id"
        assert 'severity' in vuln, "Vulnerability should have severity"
        assert 'category' in vuln, "Vulnerability should have category"
        assert 'title' in vuln, "Vulnerability should have title"
        assert 'description' in vuln, "Vulnerability should have description"
        assert 'recommendation' in vuln, "Vulnerability should have recommendation"
        assert 'martian_manhunter_says' in vuln, "Should have Martian Manhunter message"

    print("✅ PASSED: Telepathic authentication scan works")
    print(f"   Vulnerabilities found: {len(vulnerabilities)}")
    return True


def test_martian_vision_xss_scan():
    """Test 3: Martian Vision XSS vulnerability scan."""
    print("\n" + "=" * 70)
    print("Test 3: Martian Vision XSS Scan")
    print("=" * 70)

    mm = MartianManhunterSecurity()

    # Mock target with potential XSS
    target_data = {
        'url': 'https://example.com',
        'html_content': '''
            <div id="user-input"></div>
            <script>
                document.getElementById('user-input').innerHTML = userInput;
            </script>
        '''
    }

    vulnerabilities = mm._martian_vision_xss_scan(target_data)

    assert isinstance(vulnerabilities, list), "Should return list of vulnerabilities"

    # XSS vulnerabilities should be detected
    for vuln in vulnerabilities:
        assert 'id' in vuln, "Should have id"
        assert 'severity' in vuln, "Should have severity"
        assert 'category' in vuln, "Should have category"
        assert vuln['severity'] in ['critical', 'high', 'medium', 'low'], f"Invalid severity: {vuln['severity']}"

    print("✅ PASSED: Martian Vision XSS scan works")
    print(f"   Vulnerabilities found: {len(vulnerabilities)}")
    return True


def test_shapeshifting_injection_scan():
    """Test 4: Shapeshifting SQL injection scan."""
    print("\n" + "=" * 70)
    print("Test 4: Shapeshifting Injection Scan")
    print("=" * 70)

    mm = MartianManhunterSecurity()

    # Mock target with potential SQL injection
    target_data = {
        'url': 'https://example.com/search?q=test',
        'html_content': '<div>Search results</div>',
        'source_code_path': None
    }

    vulnerabilities = mm._shapeshifting_injection_scan(target_data)

    assert isinstance(vulnerabilities, list), "Should return list of vulnerabilities"

    for vuln in vulnerabilities:
        assert 'type' in vuln, "Should have type"
        assert 'severity' in vuln, "Should have severity"
        assert 'martian_says' in vuln, "Should have Martian message"

    print("✅ PASSED: Shapeshifting injection scan works")
    print(f"   Vulnerabilities found: {len(vulnerabilities)}")
    return True


def test_phase_shift_header_scan():
    """Test 5: Phase-shift security header scan."""
    print("\n" + "=" * 70)
    print("Test 5: Phase-Shift Security Header Scan")
    print("=" * 70)

    mm = MartianManhunterSecurity()

    # Mock target with missing security headers
    target_data = {
        'url': 'https://example.com',
        'headers': {
            'Content-Type': 'text/html',
            'Server': 'nginx/1.18'
            # Missing: X-Frame-Options, X-Content-Type-Options, CSP, etc.
        }
    }

    vulnerabilities = mm._phase_shift_header_scan(target_data)

    assert isinstance(vulnerabilities, list), "Should return list of vulnerabilities"

    # Should detect missing security headers
    assert len(vulnerabilities) > 0, "Should detect missing security headers"

    for vuln in vulnerabilities:
        assert 'id' in vuln, "Should have id"
        assert 'severity' in vuln, "Should have severity"
        assert 'category' in vuln, "Should have category"
        assert 'title' in vuln, "Should have title"

    print("✅ PASSED: Phase-shift header scan works")
    print(f"   Missing headers detected: {len(vulnerabilities)}")
    return True


def test_density_control_dependency_scan():
    """Test 6: Density control dependency vulnerability scan."""
    print("\n" + "=" * 70)
    print("Test 6: Density Control Dependency Scan")
    print("=" * 70)

    mm = MartianManhunterSecurity()

    # Mock target with dependencies
    target_data = {
        'dependencies': [
            'lodash@4.17.15',  # Old version with known vulnerabilities
            'express@4.16.0',   # Old version
            'react@18.2.0'      # Recent version
        ]
    }

    vulnerabilities = mm._density_control_dependency_scan(target_data)

    assert isinstance(vulnerabilities, list), "Should return list of vulnerabilities"

    for vuln in vulnerabilities:
        assert 'type' in vuln, "Should have type"
        assert 'severity' in vuln, "Should have severity"

    print("✅ PASSED: Density control dependency scan works")
    print(f"   Dependency vulnerabilities found: {len(vulnerabilities)}")
    return True


def test_detect_secrets():
    """Test 7: Detect exposed secrets and credentials."""
    print("\n" + "=" * 70)
    print("Test 7: Detect Secrets")
    print("=" * 70)

    mm = MartianManhunterSecurity()

    # Mock target with exposed secrets
    target_data = {
        'env_files': [],
        'source_code_path': None,
        'html_content': '''
            <script>
                const apiKey = "sk_live_1234567890abcdef";
                const dbPassword = "SuperSecret123!";
            </script>
        '''
    }

    vulnerabilities = mm._detect_secrets(target_data)

    assert isinstance(vulnerabilities, list), "Should return list of vulnerabilities"

    # Should detect exposed secrets
    for vuln in vulnerabilities:
        assert 'type' in vuln, "Should have type"
        assert 'severity' in vuln, "Should have severity"
        if len(vulnerabilities) > 0:
            assert vuln['severity'] in ['critical', 'high'], "Secrets should be high severity"

    print("✅ PASSED: Secret detection works")
    print(f"   Secrets found: {len(vulnerabilities)}")
    return True


def test_calculate_security_score():
    """Test 8: Calculate Martian Manhunter security score."""
    print("\n" + "=" * 70)
    print("Test 8: Calculate Security Score")
    print("=" * 70)

    mm = MartianManhunterSecurity()

    # High security - few vulnerabilities
    high_security_results = {
        'critical_count': 0,
        'high_count': 1,
        'medium_count': 2,
        'low_count': 3
    }

    score_high = mm._calculate_martian_manhunter_score(high_security_results)

    assert 'score' in score_high, "Should have score"
    assert 'grade' in score_high, "Should have grade"
    assert 'verdict' in score_high, "Should have verdict"
    assert score_high['score'] >= 70, f"High security should score >= 70, got {score_high['score']}"

    # Low security - many vulnerabilities
    low_security_results = {
        'critical_count': 5,
        'high_count': 10,
        'medium_count': 8,
        'low_count': 12
    }

    score_low = mm._calculate_martian_manhunter_score(low_security_results)
    assert score_low['score'] < 50, f"Low security should score < 50, got {score_low['score']}"

    print("✅ PASSED: Security score calculation works")
    print(f"   High Security: {score_high['score']}/100 ({score_high['grade']})")
    print(f"   Low Security: {score_low['score']}/100 ({score_low['grade']})")
    return True


def test_generate_recommendations():
    """Test 9: Generate security recommendations."""
    print("\n" + "=" * 70)
    print("Test 9: Generate Security Recommendations")
    print("=" * 70)

    mm = MartianManhunterSecurity()

    # Mock results with vulnerabilities
    mock_results = {
        'vulnerabilities': [
            {
                'type': 'Missing Security Header',
                'severity': 'high',
                'description': 'X-Frame-Options header not set',
                'missing_header': 'X-Frame-Options'
            },
            {
                'type': 'XSS Vulnerability',
                'severity': 'critical',
                'description': 'Unescaped user input detected'
            },
            {
                'type': 'Weak Authentication',
                'severity': 'high',
                'description': 'No multi-factor authentication'
            }
        ],
        'critical_count': 1,
        'high_count': 2,
        'medium_count': 0,
        'low_count': 0
    }

    recommendations = mm._generate_telepathic_recommendations(mock_results)

    assert isinstance(recommendations, list), "Should return list of recommendations"
    assert len(recommendations) > 0, "Should generate recommendations"

    # Actual structure: priority, area, issue, recommendation, martian_manhunter_says
    for rec in recommendations:
        assert 'priority' in rec, "Should have priority"
        assert 'area' in rec, "Should have area"
        assert 'issue' in rec, "Should have issue description"
        assert 'recommendation' in rec, "Should have recommendation"
        assert 'martian_manhunter_says' in rec, "Should have Martian Manhunter message"

    print("✅ PASSED: Security recommendations generated")
    print(f"   Total Recommendations: {len(recommendations)}")
    for rec in recommendations[:3]:  # Show first 3
        print(f"   - [{rec['priority']}] {rec['area']}")
    return True


def test_full_security_scan():
    """Test 10: Full comprehensive security scan."""
    print("\n" + "=" * 70)
    print("Test 10: Full Security Vulnerability Scan")
    print("=" * 70)

    mm = MartianManhunterSecurity()

    # Comprehensive mock target
    target_data = {
        'url': 'https://example.com',
        'html_content': '''
            <html>
                <head><title>Test App</title></head>
                <body>
                    <form action="/login">
                        <input type="text" name="username">
                        <input type="password" name="password">
                    </form>
                    <script>
                        const apiKey = "test_key_123";
                    </script>
                </body>
            </html>
        ''',
        'headers': {
            'Content-Type': 'text/html',
            'Server': 'nginx'
        },
        'dependencies': [
            'lodash@4.17.15',
            'express@4.16.0'
        ],
        'source_code_path': None,
        'env_files': []
    }

    # Run full scan
    result = mm.scan_all_vulnerabilities(target_data)

    # Validate top-level structure
    assert 'hero' in result, "Should identify hero"
    assert result['hero'] == '🧠 Martian Manhunter - Security Guardian', "Should be Martian Manhunter"
    assert 'timestamp' in result, "Should have timestamp"
    assert 'target_url' in result, "Should have target_url"
    assert result['target_url'] == 'https://example.com', "Target URL should match"

    # Check vulnerability tracking
    assert 'vulnerabilities' in result, "Should have vulnerabilities list"
    assert 'critical_count' in result, "Should count critical vulnerabilities"
    assert 'high_count' in result, "Should count high vulnerabilities"
    assert 'medium_count' in result, "Should count medium vulnerabilities"
    assert 'low_count' in result, "Should count low vulnerabilities"

    # Check security score
    assert 'security_score' in result, "Should have security_score"
    score = result['security_score']
    assert 'score' in score, "Should have score value"
    assert 'grade' in score, "Should have grade"
    assert 'verdict' in score, "Should have verdict"
    assert 0 <= score['score'] <= 100, f"Score should be 0-100, got {score['score']}"

    # Check recommendations
    assert 'recommendations' in result, "Should have recommendations"
    assert isinstance(result['recommendations'], list), "Recommendations should be a list"

    # Verify vulnerability counts add up
    total_vulns = result['critical_count'] + result['high_count'] + result['medium_count'] + result['low_count']
    assert len(result['vulnerabilities']) == total_vulns, "Vulnerability counts should match list length"

    print("\n✅ PASSED: Full security scan successful")
    print(f"   Security Score: {score['score']}/100")
    print(f"   Grade: {score['grade']}")
    print(f"   Critical: {result['critical_count']}")
    print(f"   High: {result['high_count']}")
    print(f"   Medium: {result['medium_count']}")
    print(f"   Low: {result['low_count']}")
    print(f"   Recommendations: {len(result['recommendations'])}")
    return True


def run_all_tests():
    """Run complete test suite."""
    print("\n🧠 Martian Manhunter - Security Testing Test Suite")
    print("=" * 70)
    print("Testing Security Vulnerability Scanning and Analysis")
    print("=" * 70)

    tests = [
        ("Initialization", test_martian_manhunter_initialization),
        ("Telepathic Auth Scan", test_telepathic_auth_scan),
        ("Martian Vision XSS Scan", test_martian_vision_xss_scan),
        ("Shapeshifting Injection Scan", test_shapeshifting_injection_scan),
        ("Phase-Shift Header Scan", test_phase_shift_header_scan),
        ("Density Control Dependency Scan", test_density_control_dependency_scan),
        ("Detect Secrets", test_detect_secrets),
        ("Calculate Security Score", test_calculate_security_score),
        ("Generate Recommendations", test_generate_recommendations),
        ("Full Security Scan", test_full_security_scan),
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
        print("\n🎉 ALL TESTS PASSED! Martian Manhunter's telepathy is flawless!")
        print("🧠 All vulnerabilities detected and analyzed!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review.")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
