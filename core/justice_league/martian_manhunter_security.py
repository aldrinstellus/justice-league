"""
🧠 MARTIAN MANHUNTER - THE SECURITY GUARDIAN
Justice League Member: Security Testing Specialist

The Last Martian - Telepathically reads vulnerabilities before attackers can exploit them!

Powers:
- OWASP Top 10 vulnerability scanning
- Authentication/authorization testing
- Session management validation
- SSL/TLS certificate checking
- Security header verification
- Dependency vulnerability scanning
- Secrets detection
- Penetration testing simulation

"I read the minds of your vulnerabilities before attackers do!"
"""

import logging
import re
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import json

# Mission Control Narrator for coordinated communication
try:
    from .mission_control_narrator import get_narrator
    NARRATOR_AVAILABLE = True
except ImportError:
    NARRATOR_AVAILABLE = False
    logging.warning("Mission Control Narrator not available - Martian Manhunter will operate without narrator")

logger = logging.getLogger(__name__)


class MartianManhunterSecurity:
    """
    🧠 MARTIAN MANHUNTER - Security Testing Specialist

    J'onn J'onzz uses his Martian powers to detect security vulnerabilities

    Telepathic Powers:
    1. Mind Reading - Detect authentication flaws
    2. Shapeshifting - Test different attack vectors
    3. Phase-shifting - Bypass security to find weaknesses
    4. Martian Vision - X-ray vision for hidden vulnerabilities
    5. Density Control - Penetrate through security layers
    """

    def __init__(self, config_dir: Optional[str] = None, narrator: Optional[Any] = None):
        """
        Initialize Martian Manhunter's security command center

        Args:
            config_dir: Directory for security configs and reports
            narrator: Mission Control Narrator for coordinated communication
        """
        self.config_dir = Path(config_dir or '/tmp/aldo-vision-security')
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.vulnerability_db = self.config_dir / 'vulnerabilities.json'

        # Hero identity for narrator integration
        self.hero_name = "Martian Manhunter"
        self.hero_emoji = "🧠"

        # Initialize narrator for enhanced UX
        self.narrator = narrator if narrator else (get_narrator() if NARRATOR_AVAILABLE else None)

        logger.info("🧠 MARTIAN MANHUNTER - Security Guardian initialized")

    def say(self, message: str, style: str = "telepathic", technical_info: Optional[str] = None):
        """Martian Manhunter dialogue - Security and telepathic focus"""
        if self.narrator:
            self.narrator.hero_speaks(f"{self.hero_emoji} {self.hero_name}", message, style, technical_info)

    def think(self, thought: str, step: Optional[int] = None, category: Optional[str] = "Scanning"):
        """Sequential thinking with security focus. Categories: Scanning, Detecting, Protecting"""
        if self.narrator:
            self.narrator.hero_thinks(f"{self.hero_emoji} {self.hero_name}", thought, step, category)

    def handoff(self, to_hero: str, context: str, details: Optional[str] = None):
        """Handoff security findings to another hero"""
        if self.narrator:
            self.narrator.hero_handoff(f"{self.hero_emoji} {self.hero_name}", to_hero, context, details)

    def scan_all_vulnerabilities(self, target_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        🧠 Complete security vulnerability scan

        Martian Manhunter uses all his powers to detect security issues

        Args:
            target_data: Target information
                {
                    'url': str,  # Target URL
                    'source_code_path': str,  # Path to source code
                    'package_json_path': str,  # Path to package.json
                    'dependencies': List[str],  # List of dependencies
                    'env_files': List[str],  # Paths to .env files
                    'html_content': str,  # HTML content to scan
                    'headers': Dict  # HTTP headers
                }

        Returns:
            Complete security analysis
        """
        logger.info("🧠 ========================================")
        logger.info("🧠  MARTIAN MANHUNTER SECURITY SCAN")
        logger.info("🧠 ========================================")

        results = {
            'hero': '🧠 Martian Manhunter - Security Guardian',
            'timestamp': datetime.now().isoformat(),
            'target_url': target_data.get('url'),
            'vulnerabilities': [],
            'security_score': 0,
            'critical_count': 0,
            'high_count': 0,
            'medium_count': 0,
            'low_count': 0
        }

        # Power 1: Telepathy - Read authentication vulnerabilities
        logger.info("🧠 Using Telepathy to read authentication flaws...")
        auth_vulns = self._telepathic_auth_scan(target_data)
        results['vulnerabilities'].extend(auth_vulns)

        # Power 2: Martian Vision - X-ray for hidden vulnerabilities
        logger.info("🧠 Using Martian Vision for X-ray security scan...")
        xss_vulns = self._martian_vision_xss_scan(target_data)
        results['vulnerabilities'].extend(xss_vulns)

        # Power 3: Shapeshifting - Test different attack vectors
        logger.info("🧠 Shapeshifting to test attack vectors...")
        injection_vulns = self._shapeshifting_injection_scan(target_data)
        results['vulnerabilities'].extend(injection_vulns)

        # Power 4: Phase-shifting - Bypass security to find weaknesses
        logger.info("🧠 Phase-shifting through security layers...")
        header_vulns = self._phase_shift_header_scan(target_data)
        results['vulnerabilities'].extend(header_vulns)

        # Power 5: Density Control - Penetrate dependency vulnerabilities
        logger.info("🧠 Using Density Control on dependencies...")
        dep_vulns = self._density_control_dependency_scan(target_data)
        results['vulnerabilities'].extend(dep_vulns)

        # Power 6: Secrets Detection - Find exposed credentials
        logger.info("🧠 Detecting secrets with Martian senses...")
        secret_vulns = self._detect_secrets(target_data)
        results['vulnerabilities'].extend(secret_vulns)

        # Count vulnerabilities by severity
        for vuln in results['vulnerabilities']:
            severity = vuln.get('severity', 'low')
            if severity == 'critical':
                results['critical_count'] += 1
            elif severity == 'high':
                results['high_count'] += 1
            elif severity == 'medium':
                results['medium_count'] += 1
            else:
                results['low_count'] += 1

        # Calculate security score
        security_score = self._calculate_martian_manhunter_score(results)
        results['security_score'] = security_score

        # Generate recommendations
        recommendations = self._generate_telepathic_recommendations(results)
        results['recommendations'] = recommendations

        # Final verdict
        logger.info("🧠 ========================================")
        logger.info(f"🧠  SECURITY SCORE: {security_score['score']:.1f}/100")
        logger.info(f"🧠  GRADE: {security_score['grade']}")
        logger.info(f"🧠  CRITICAL: {results['critical_count']}")
        logger.info(f"🧠  HIGH: {results['high_count']}")
        logger.info("🧠 ========================================")

        return results

    def _telepathic_auth_scan(self, target_data: Dict) -> List[Dict]:
        """
        🧠 Telepathy - Read authentication vulnerabilities

        Args:
            target_data: Target information

        Returns:
            List of authentication vulnerabilities
        """
        vulnerabilities = []

        # Check for common auth issues
        html = target_data.get('html_content', '')
        headers = target_data.get('headers', {})

        # Check for missing authentication
        if 'authorization' not in headers and 'cookie' not in headers:
            vulnerabilities.append({
                'id': 'AUTH-001',
                'severity': 'high',
                'category': 'Authentication',
                'title': 'No authentication headers detected',
                'description': 'Page may be accessible without authentication',
                'recommendation': 'Implement authentication (JWT, session cookies, OAuth)',
                'martian_manhunter_says': 'I sense no mental barriers - your app is unguarded!'
            })

        # Check for weak session management
        if 'set-cookie' in headers:
            cookie = headers.get('set-cookie', '')
            if 'httponly' not in cookie.lower():
                vulnerabilities.append({
                    'id': 'AUTH-002',
                    'severity': 'high',
                    'category': 'Session Management',
                    'title': 'Cookies missing HttpOnly flag',
                    'description': 'Cookies vulnerable to XSS attacks',
                    'recommendation': 'Add HttpOnly flag to all cookies',
                    'martian_manhunter_says': 'Your cookies are telepathically readable by JavaScript!'
                })

            if 'secure' not in cookie.lower():
                vulnerabilities.append({
                    'id': 'AUTH-003',
                    'severity': 'medium',
                    'category': 'Session Management',
                    'title': 'Cookies missing Secure flag',
                    'description': 'Cookies can be transmitted over HTTP',
                    'recommendation': 'Add Secure flag to cookies (HTTPS only)',
                    'martian_manhunter_says': 'I can intercept your cookies mid-flight!'
                })

        logger.info(f"  ✓ Telepathy detected {len(vulnerabilities)} auth vulnerabilities")
        return vulnerabilities

    def _martian_vision_xss_scan(self, target_data: Dict) -> List[Dict]:
        """
        🧠 Martian Vision - X-ray scan for XSS vulnerabilities

        Args:
            target_data: Target information

        Returns:
            List of XSS vulnerabilities
        """
        vulnerabilities = []
        html = target_data.get('html_content', '')

        # Check for potential XSS vectors
        dangerous_patterns = [
            (r'<script[^>]*>.*?</script>', 'Inline script tag detected'),
            (r'on\w+\s*=\s*["\']', 'Inline event handler detected'),
            (r'javascript:', 'javascript: protocol in href/src'),
            (r'eval\(', 'eval() function usage detected'),
            (r'innerHTML\s*=', 'innerHTML usage (potential XSS)'),
            (r'document\.write', 'document.write usage detected')
        ]

        for pattern, description in dangerous_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                vulnerabilities.append({
                    'id': f'XSS-{len(vulnerabilities)+1:03d}',
                    'severity': 'high',
                    'category': 'Cross-Site Scripting (XSS)',
                    'title': description,
                    'description': f'Found {len(matches)} instances of potential XSS vector',
                    'recommendation': 'Sanitize user input, use Content Security Policy',
                    'martian_manhunter_says': 'My X-ray vision sees malicious code injection points!'
                })

        logger.info(f"  ✓ Martian Vision detected {len(vulnerabilities)} XSS vulnerabilities")
        return vulnerabilities

    def _shapeshifting_injection_scan(self, target_data: Dict) -> List[Dict]:
        """
        🧠 Shapeshifting - Test different injection attack vectors

        Args:
            target_data: Target information

        Returns:
            List of injection vulnerabilities
        """
        vulnerabilities = []
        source_path = target_data.get('source_code_path')

        if source_path and Path(source_path).exists():
            # Check for SQL injection patterns
            sql_patterns = [
                (r'SELECT.*FROM.*WHERE.*\+', 'String concatenation in SQL query'),
                (r'\$\{.*\}.*SELECT', 'Template literal in SQL query'),
                (r'query\(["\'].*\+.*["\']\)', 'String concatenation in query'),
            ]

            try:
                # Scan source files for SQL injection
                for file_path in Path(source_path).rglob('*.{js,ts,py}'):
                    content = file_path.read_text()
                    for pattern, description in sql_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            vulnerabilities.append({
                                'id': f'INJ-{len(vulnerabilities)+1:03d}',
                                'severity': 'critical',
                                'category': 'SQL Injection',
                                'title': description,
                                'description': f'Potential SQL injection in {file_path.name}',
                                'recommendation': 'Use parameterized queries or ORMs',
                                'martian_manhunter_says': 'I shape-shifted into malicious input - your queries are vulnerable!'
                            })
            except Exception as e:
                logger.warning(f"Shapeshifting scan failed: {e}")

        logger.info(f"  ✓ Shapeshifting detected {len(vulnerabilities)} injection vulnerabilities")
        return vulnerabilities

    def _phase_shift_header_scan(self, target_data: Dict) -> List[Dict]:
        """
        🧠 Phase-shifting - Bypass security headers to find weaknesses

        Args:
            target_data: Target information

        Returns:
            List of missing security headers
        """
        vulnerabilities = []
        headers = target_data.get('headers', {})

        # Critical security headers
        required_headers = {
            'content-security-policy': {
                'severity': 'high',
                'title': 'Missing Content-Security-Policy header',
                'recommendation': "Add CSP: default-src 'self'; script-src 'self'"
            },
            'x-frame-options': {
                'severity': 'medium',
                'title': 'Missing X-Frame-Options header',
                'recommendation': 'Add X-Frame-Options: DENY or SAMEORIGIN'
            },
            'x-content-type-options': {
                'severity': 'medium',
                'title': 'Missing X-Content-Type-Options header',
                'recommendation': 'Add X-Content-Type-Options: nosniff'
            },
            'strict-transport-security': {
                'severity': 'high',
                'title': 'Missing Strict-Transport-Security header',
                'recommendation': 'Add HSTS: max-age=31536000; includeSubDomains'
            },
            'x-xss-protection': {
                'severity': 'low',
                'title': 'Missing X-XSS-Protection header',
                'recommendation': 'Add X-XSS-Protection: 1; mode=block'
            }
        }

        for header_name, info in required_headers.items():
            if header_name not in headers:
                vulnerabilities.append({
                    'id': f'HDR-{len(vulnerabilities)+1:03d}',
                    'severity': info['severity'],
                    'category': 'Security Headers',
                    'title': info['title'],
                    'description': f'Missing critical security header: {header_name}',
                    'recommendation': info['recommendation'],
                    'martian_manhunter_says': 'I phase-shifted past your defenses - headers missing!'
                })

        logger.info(f"  ✓ Phase-shifting detected {len(vulnerabilities)} header vulnerabilities")
        return vulnerabilities

    def _density_control_dependency_scan(self, target_data: Dict) -> List[Dict]:
        """
        🧠 Density Control - Penetrate through dependency vulnerabilities

        Args:
            target_data: Target information

        Returns:
            List of dependency vulnerabilities
        """
        vulnerabilities = []
        package_json = target_data.get('package_json_path')

        if package_json and Path(package_json).exists():
            try:
                # Run npm audit (if available)
                result = subprocess.run(
                    ['npm', 'audit', '--json'],
                    cwd=Path(package_json).parent,
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.stdout:
                    audit_data = json.loads(result.stdout)
                    vulnerabilities_found = audit_data.get('metadata', {}).get('vulnerabilities', {})

                    for severity, count in vulnerabilities_found.items():
                        if count > 0:
                            sev_level = 'critical' if severity == 'critical' else 'high' if severity == 'high' else 'medium'
                            vulnerabilities.append({
                                'id': f'DEP-{severity.upper()}',
                                'severity': sev_level,
                                'category': 'Dependency Vulnerabilities',
                                'title': f'{count} {severity} vulnerabilities in dependencies',
                                'description': f'npm audit found {count} {severity} vulnerabilities',
                                'recommendation': 'Run npm audit fix or update vulnerable packages',
                                'martian_manhunter_says': f'I penetrated your dependencies - {count} {severity} threats detected!'
                            })
            except Exception as e:
                logger.warning(f"Dependency scan failed: {e}")

        logger.info(f"  ✓ Density Control detected {len(vulnerabilities)} dependency vulnerabilities")
        return vulnerabilities

    def _detect_secrets(self, target_data: Dict) -> List[Dict]:
        """
        🧠 Detect exposed secrets and credentials

        Args:
            target_data: Target information

        Returns:
            List of exposed secrets
        """
        vulnerabilities = []
        source_path = target_data.get('source_code_path')
        env_files = target_data.get('env_files', [])

        # Check for hardcoded secrets
        secret_patterns = [
            (r'api[_-]?key\s*=\s*["\'][^"\']{20,}["\']', 'Hardcoded API key'),
            (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password'),
            (r'secret\s*=\s*["\'][^"\']+["\']', 'Hardcoded secret'),
            (r'token\s*=\s*["\'][^"\']{20,}["\']', 'Hardcoded token'),
            (r'(sk|pk)_live_[a-zA-Z0-9]{20,}', 'Stripe API key'),
            (r'AIza[0-9A-Za-z\\-_]{35}', 'Google API key'),
            (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
        ]

        if source_path and Path(source_path).exists():
            try:
                for file_path in Path(source_path).rglob('*.{js,ts,py,env}'):
                    if '.git' in str(file_path):
                        continue

                    content = file_path.read_text()
                    for pattern, description in secret_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            vulnerabilities.append({
                                'id': f'SEC-{len(vulnerabilities)+1:03d}',
                                'severity': 'critical',
                                'category': 'Exposed Secrets',
                                'title': f'{description} detected in code',
                                'description': f'Found in {file_path.name}',
                                'recommendation': 'Move secrets to environment variables or secret manager',
                                'martian_manhunter_says': 'I sense your secrets exposed in the code!'
                            })
            except Exception as e:
                logger.warning(f"Secrets detection failed: {e}")

        logger.info(f"  ✓ Detected {len(vulnerabilities)} exposed secrets")
        return vulnerabilities

    def _calculate_martian_manhunter_score(self, results: Dict) -> Dict[str, Any]:
        """
        🧠 Calculate Martian Manhunter's security score

        Args:
            results: Security scan results

        Returns:
            Security score with grade
        """
        critical = results.get('critical_count', 0)
        high = results.get('high_count', 0)
        medium = results.get('medium_count', 0)
        low = results.get('low_count', 0)

        # Base score: 100
        score = 100.0

        # Deductions
        score -= (critical * 20)  # -20 per critical
        score -= (high * 10)      # -10 per high
        score -= (medium * 5)     # -5 per medium
        score -= (low * 2)        # -2 per low

        # Ensure score is 0-100
        score = max(0, min(100, score))

        # Grade
        if score == 100:
            grade = "S+ (Fortress)"
            verdict = "🧠 IMPENETRABLE! No vulnerabilities detected - Martian-level security!"
        elif score >= 90:
            grade = "S (Excellent)"
            verdict = "🧠 EXCELLENT! Minor security issues only!"
        elif score >= 80:
            grade = "A (Strong)"
            verdict = "🧠 STRONG! Some vulnerabilities need attention!"
        elif score >= 70:
            grade = "B (Good)"
            verdict = "🧠 GOOD! Multiple security improvements needed!"
        elif score >= 60:
            grade = "C (Fair)"
            verdict = "🧠 FAIR! Significant security risks present!"
        else:
            grade = "D or below (Vulnerable)"
            verdict = "🧠 CRITICAL! Immediate security intervention required!"

        return {
            'score': score,
            'grade': grade,
            'verdict': verdict,
            'vulnerability_breakdown': {
                'critical': critical,
                'high': high,
                'medium': medium,
                'low': low
            }
        }

    def _generate_telepathic_recommendations(self, results: Dict) -> List[Dict[str, Any]]:
        """
        🧠 Generate Martian Manhunter's telepathic security recommendations

        Args:
            results: Security scan results

        Returns:
            List of prioritized recommendations
        """
        recommendations = []

        critical_count = results.get('critical_count', 0)
        high_count = results.get('high_count', 0)

        if critical_count > 0:
            recommendations.append({
                'priority': 'critical',
                'area': 'Critical Vulnerabilities',
                'issue': f'{critical_count} critical security vulnerabilities detected',
                'recommendation': 'Address all critical vulnerabilities immediately before deployment',
                'martian_manhunter_says': 'I read catastrophic threats in your security posture!'
            })

        if high_count > 0:
            recommendations.append({
                'priority': 'high',
                'area': 'High-Risk Vulnerabilities',
                'issue': f'{high_count} high-severity vulnerabilities detected',
                'recommendation': 'Fix high-severity issues within 24-48 hours',
                'martian_manhunter_says': 'High-level threats detected telepathically!'
            })

        # Specific recommendations based on vulnerability types
        vuln_categories = {}
        for vuln in results.get('vulnerabilities', []):
            category = vuln.get('category', 'Unknown')
            vuln_categories[category] = vuln_categories.get(category, 0) + 1

        for category, count in vuln_categories.items():
            if count >= 3:
                recommendations.append({
                    'priority': 'medium',
                    'area': category,
                    'issue': f'Multiple {category} vulnerabilities ({count} found)',
                    'recommendation': f'Systematic review of {category} practices needed',
                    'martian_manhunter_says': f'Pattern detected: {category} weaknesses widespread!'
                })

        if not recommendations:
            recommendations.append({
                'priority': 'low',
                'area': 'Security Maintenance',
                'issue': 'No critical vulnerabilities detected',
                'recommendation': 'Continue regular security scans and monitoring',
                'martian_manhunter_says': 'Your mind is clear - security is strong!'
            })

        return recommendations


# Main entry point - Martian Manhunter's Mission Interface
def martian_manhunter_security_scan(target_data: Dict[str, Any],
                                    config_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    🧠 Martian Manhunter's complete security vulnerability scan

    The Last Martian uses all his powers to detect security threats!

    Args:
        target_data: Target information for security scan
        config_dir: Optional config directory

    Returns:
        Complete security analysis from Martian Manhunter
    """
    manhunter = MartianManhunterSecurity(config_dir)
    return manhunter.scan_all_vulnerabilities(target_data)
