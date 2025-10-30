#!/usr/bin/env python3
"""
🦸 JUSTICE LEAGUE - PRODUCT UI ANALYSIS
========================================

Analyzing product screens, pages, and user flows (NOT design system components).

Focus:
- Product pages and screens
- User flows and journeys
- Feature completeness
- Screen layouts and patterns
- UI/UX consistency across product
- Navigation structure
- User personas and roles

Author: Justice League
Date: October 23, 2025
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))

from core.superman_figma_integration import SupermanFigmaIntegration


class ProductUIAnalyzer:
    """Analyze product UI/UX, not design system."""

    def __init__(self, figma_token: str):
        self.figma_token = figma_token
        self.superman = SupermanFigmaIntegration(figma_token)

    def analyze_product(self, figma_url: str) -> Dict[str, Any]:
        """Analyze as a product UI file."""

        print("\n" + "="*80)
        print("🦸 JUSTICE LEAGUE - PRODUCT UI ANALYSIS")
        print("="*80 + "\n")

        file_key = self.superman.extract_file_key(figma_url)
        print(f"🔑 File Key: {file_key}\n")

        print("📥 Fetching product UI data...")
        file_data = self.superman.get_file_data(file_key, depth=5)

        if 'error' in file_data:
            print(f"❌ ERROR: {file_data['error']}")
            return file_data

        print("✅ Product data loaded!\n")

        results = {
            'product_info': self._analyze_product_info(file_data),
            'pages_and_screens': self._analyze_pages_and_screens(file_data),
            'user_roles': self._analyze_user_roles(file_data),
            'feature_areas': self._analyze_feature_areas(file_data),
            'navigation_structure': self._analyze_navigation(file_data),
            'user_flows': self._analyze_user_flows(file_data),
            'ui_patterns': self._analyze_ui_patterns(file_data),
            'completeness': None  # Will calculate
        }

        results['completeness'] = self._assess_product_completeness(results)
        results['recommendations'] = self._generate_product_recommendations(results)

        self._print_product_report(results)

        output_file = Path('product_ui_analysis.json')
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n📄 Analysis saved to: {output_file}\n")

        return results

    def _analyze_product_info(self, file_data: Dict) -> Dict[str, Any]:
        """Basic product information."""

        print("\n" + "="*80)
        print("📱 PRODUCT INFORMATION")
        print("="*80 + "\n")

        info = {
            'name': file_data.get('name', 'Unknown'),
            'last_modified': file_data.get('lastModified', 'Unknown'),
            'version': file_data.get('version', 'Unknown'),
        }

        print(f"📝 Product Name: {info['name']}")
        print(f"📅 Last Modified: {info['last_modified']}")
        print(f"🔢 Version: {info['version']}")

        # Detect product type from name and content
        name_lower = info['name'].lower()
        if 'lms' in name_lower or 'learn' in name_lower or 'course' in name_lower or 'edu' in name_lower:
            product_type = 'Learning Management System (LMS)'
        elif 'school' in name_lower or 'student' in name_lower or 'teacher' in name_lower:
            product_type = 'Education Platform'
        elif 'dash' in name_lower:
            product_type = 'Dashboard Application'
        else:
            product_type = 'Web Application'

        info['product_type'] = product_type
        print(f"🎯 Product Type: {product_type}")

        return info

    def _analyze_pages_and_screens(self, file_data: Dict) -> Dict[str, Any]:
        """Analyze all pages/canvases and their screens."""

        print("\n" + "="*80)
        print("📄 PAGES & SCREENS")
        print("="*80 + "\n")

        document = file_data.get('document', {})
        canvases = document.get('children', [])

        pages = []
        total_screens = 0

        for canvas in canvases:
            if canvas.get('type') == 'CANVAS':
                page_name = canvas.get('name', 'Unnamed')
                frames = canvas.get('children', [])

                # Count actual screens (top-level frames)
                screen_list = []
                for frame in frames:
                    if frame.get('type') in ['FRAME', 'SECTION']:
                        screen_name = frame.get('name', 'Unnamed')
                        screen_list.append({
                            'name': screen_name,
                            'type': frame.get('type'),
                            'width': frame.get('absoluteBoundingBox', {}).get('width', 0),
                            'height': frame.get('absoluteBoundingBox', {}).get('height', 0)
                        })

                total_screens += len(screen_list)

                pages.append({
                    'name': page_name,
                    'screen_count': len(screen_list),
                    'screens': screen_list
                })

        print(f"📊 Total Pages: {len(pages)}")
        print(f"📱 Total Screens: {total_screens}\n")

        print("📂 Page Breakdown:")
        for i, page in enumerate(pages, 1):
            print(f"\n  {i}. {page['name']}")
            print(f"     Screens: {page['screen_count']}")

            if page['screens']:
                print(f"     Top screens:")
                for j, screen in enumerate(page['screens'][:5], 1):
                    dims = f"{screen['width']:.0f}×{screen['height']:.0f}" if screen['width'] > 0 else 'auto'
                    print(f"       {j}. {screen['name']} ({dims})")

                if len(page['screens']) > 5:
                    print(f"       ... and {len(page['screens']) - 5} more")

        return {
            'total_pages': len(pages),
            'total_screens': total_screens,
            'pages': pages
        }

    def _analyze_user_roles(self, file_data: Dict) -> Dict[str, Any]:
        """Detect user roles from page/screen names."""

        print("\n" + "="*80)
        print("👥 USER ROLES & PERSONAS")
        print("="*80 + "\n")

        document = file_data.get('document', {})
        canvases = document.get('children', [])

        role_keywords = {
            'student': [],
            'teacher': [],
            'admin': [],
            'parent': [],
            'counselor': [],
        }

        all_names = []

        # Collect all page and screen names
        for canvas in canvases:
            if canvas.get('type') == 'CANVAS':
                page_name = canvas.get('name', '').lower()
                all_names.append(page_name)

                for frame in canvas.get('children', []):
                    if frame.get('type') in ['FRAME', 'SECTION']:
                        screen_name = frame.get('name', '').lower()
                        all_names.append(screen_name)

        # Detect roles
        detected_roles = []
        for role, screens in role_keywords.items():
            for name in all_names:
                if role in name:
                    screens.append(name)

            if screens:
                detected_roles.append(role)

        print(f"👥 Detected User Roles: {len(detected_roles)}")
        if detected_roles:
            for role in detected_roles:
                count = sum(1 for n in all_names if role in n)
                print(f"  • {role.title()}: {count} screens/pages")
        else:
            print("  • No specific roles detected (generic product)")

        return {
            'detected_roles': detected_roles,
            'role_screens': {k: len(v) for k, v in role_keywords.items() if v}
        }

    def _analyze_feature_areas(self, file_data: Dict) -> Dict[str, Any]:
        """Identify feature areas from page names."""

        print("\n" + "="*80)
        print("🎯 FEATURE AREAS")
        print("="*80 + "\n")

        document = file_data.get('document', {})
        canvases = document.get('children', [])

        # Common feature keywords
        features = {
            'dashboard': 0,
            'home': 0,
            'courses': 0,
            'calendar': 0,
            'messages': 0,
            'inbox': 0,
            'grades': 0,
            'attendance': 0,
            'analytics': 0,
            'settings': 0,
            'profile': 0,
            'notifications': 0,
            'discussions': 0,
            'assignments': 0,
            'resources': 0,
            'modules': 0,
            'groups': 0,
        }

        for canvas in canvases:
            if canvas.get('type') == 'CANVAS':
                page_name = canvas.get('name', '').lower()

                for feature in features.keys():
                    if feature in page_name:
                        features[feature] += 1

                # Check frames too
                for frame in canvas.get('children', []):
                    if frame.get('type') in ['FRAME', 'SECTION']:
                        screen_name = frame.get('name', '').lower()
                        for feature in features.keys():
                            if feature in screen_name:
                                features[feature] += 1

        detected_features = {k: v for k, v in features.items() if v > 0}

        print(f"🎯 Detected Features: {len(detected_features)}")
        for feature, count in sorted(detected_features.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {feature.title()}: {count} occurrences")

        return {
            'total_features': len(detected_features),
            'features': detected_features
        }

    def _analyze_navigation(self, file_data: Dict) -> Dict[str, Any]:
        """Analyze navigation structure."""

        print("\n" + "="*80)
        print("🧭 NAVIGATION STRUCTURE")
        print("="*80 + "\n")

        # Look for navbar, sidebar, menu components
        components = file_data.get('components', {})

        nav_components = []
        for comp_id, comp_data in components.items():
            name = comp_data.get('name', '').lower()
            if any(keyword in name for keyword in ['nav', 'sidebar', 'menu', 'header', 'footer']):
                nav_components.append(comp_data.get('name'))

        print(f"🧭 Navigation Components: {len(nav_components)}")
        if nav_components:
            for i, comp in enumerate(nav_components[:10], 1):
                print(f"  {i}. {comp}")
            if len(nav_components) > 10:
                print(f"  ... and {len(nav_components) - 10} more")

        return {
            'nav_component_count': len(nav_components),
            'nav_components': nav_components
        }

    def _analyze_user_flows(self, file_data: Dict) -> Dict[str, Any]:
        """Analyze user flows from page organization."""

        print("\n" + "="*80)
        print("🔄 USER FLOWS")
        print("="*80 + "\n")

        # Detect common flows
        flows = {
            'authentication': ['login', 'signup', 'register', 'forgot password', 'reset'],
            'onboarding': ['welcome', 'onboarding', 'getting started', 'tutorial'],
            'core_workflow': ['dashboard', 'home', 'main'],
            'settings': ['settings', 'preferences', 'profile', 'account'],
        }

        document = file_data.get('document', {})
        canvases = document.get('children', [])

        detected_flows = {}
        all_names = []

        for canvas in canvases:
            if canvas.get('type') == 'CANVAS':
                page_name = canvas.get('name', '').lower()
                all_names.append(page_name)

                for frame in canvas.get('children', []):
                    if frame.get('type') in ['FRAME', 'SECTION']:
                        screen_name = frame.get('name', '').lower()
                        all_names.append(screen_name)

        for flow_name, keywords in flows.items():
            matches = []
            for name in all_names:
                if any(keyword in name for keyword in keywords):
                    matches.append(name)

            if matches:
                detected_flows[flow_name] = len(matches)

        print(f"🔄 Detected User Flows: {len(detected_flows)}")
        for flow, count in detected_flows.items():
            print(f"  • {flow.replace('_', ' ').title()}: {count} screens")

        return {
            'detected_flows': detected_flows
        }

    def _analyze_ui_patterns(self, file_data: Dict) -> Dict[str, Any]:
        """Analyze common UI patterns."""

        print("\n" + "="*80)
        print("🎨 UI PATTERNS")
        print("="*80 + "\n")

        components = file_data.get('components', {})

        patterns = {
            'cards': 0,
            'modals': 0,
            'forms': 0,
            'tables': 0,
            'lists': 0,
            'buttons': 0,
            'inputs': 0,
            'dropdowns': 0,
            'tabs': 0,
            'badges': 0,
            'avatars': 0,
        }

        for comp_data in components.values():
            name = comp_data.get('name', '').lower()

            for pattern in patterns.keys():
                if pattern[:-1] in name or pattern in name:  # Handle singular/plural
                    patterns[pattern] += 1

        detected_patterns = {k: v for k, v in patterns.items() if v > 0}

        print(f"🎨 UI Patterns Used: {len(detected_patterns)}")
        for pattern, count in sorted(detected_patterns.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {pattern.title()}: {count} components")

        return detected_patterns

    def _assess_product_completeness(self, results: Dict) -> Dict[str, Any]:
        """Assess product design completeness."""

        print("\n" + "="*80)
        print("📊 PRODUCT COMPLETENESS ASSESSMENT")
        print("="*80 + "\n")

        scores = {}

        # 1. Screen Coverage (0-30 points)
        screen_count = results['pages_and_screens']['total_screens']
        if screen_count >= 50:
            scores['screen_coverage'] = 30
        elif screen_count >= 30:
            scores['screen_coverage'] = 25
        elif screen_count >= 20:
            scores['screen_coverage'] = 20
        elif screen_count >= 10:
            scores['screen_coverage'] = 15
        else:
            scores['screen_coverage'] = 10

        # 2. Feature Completeness (0-25 points)
        feature_count = results['feature_areas']['total_features']
        if feature_count >= 10:
            scores['feature_completeness'] = 25
        elif feature_count >= 7:
            scores['feature_completeness'] = 20
        elif feature_count >= 5:
            scores['feature_completeness'] = 15
        else:
            scores['feature_completeness'] = 10

        # 3. User Role Coverage (0-20 points)
        role_count = len(results['user_roles']['detected_roles'])
        if role_count >= 3:
            scores['role_coverage'] = 20
        elif role_count >= 2:
            scores['role_coverage'] = 15
        elif role_count >= 1:
            scores['role_coverage'] = 10
        else:
            scores['role_coverage'] = 5

        # 4. User Flows (0-15 points)
        flow_count = len(results['user_flows']['detected_flows'])
        if flow_count >= 4:
            scores['user_flows'] = 15
        elif flow_count >= 3:
            scores['user_flows'] = 12
        elif flow_count >= 2:
            scores['user_flows'] = 8
        else:
            scores['user_flows'] = 5

        # 5. Navigation Structure (0-10 points)
        nav_count = results['navigation_structure']['nav_component_count']
        if nav_count >= 5:
            scores['navigation'] = 10
        elif nav_count >= 3:
            scores['navigation'] = 7
        else:
            scores['navigation'] = 5

        total_score = sum(scores.values())

        if total_score >= 90:
            level = "🏆 COMPREHENSIVE - Production-ready product"
            grade = "A+"
        elif total_score >= 80:
            level = "⭐ COMPLETE - Well-developed product"
            grade = "A"
        elif total_score >= 70:
            level = "✅ SOLID - Good feature coverage"
            grade = "B"
        elif total_score >= 60:
            level = "🌱 DEVELOPING - Core features present"
            grade = "C"
        else:
            level = "🔧 EARLY STAGE - Needs more screens"
            grade = "D"

        print(f"📊 Completeness Score: {total_score}/100 ({grade})")
        print(f"🏅 Product Stage: {level}\n")

        print("📈 Score Breakdown:")
        print(f"  Screen Coverage: {scores['screen_coverage']}/30")
        print(f"  Feature Completeness: {scores['feature_completeness']}/25")
        print(f"  User Role Coverage: {scores['role_coverage']}/20")
        print(f"  User Flows: {scores['user_flows']}/15")
        print(f"  Navigation: {scores['navigation']}/10")

        return {
            'total_score': total_score,
            'grade': grade,
            'level': level,
            'scores': scores
        }

    def _generate_product_recommendations(self, results: Dict) -> List[str]:
        """Generate product-specific recommendations."""

        print("\n" + "="*80)
        print("💡 RECOMMENDATIONS")
        print("="*80 + "\n")

        recommendations = []

        # Screen coverage
        screen_count = results['pages_and_screens']['total_screens']
        if screen_count < 20:
            recommendations.append(
                f"📱 Add more screens - currently {screen_count} screens, aim for 30+ for comprehensive product"
            )

        # User roles
        role_count = len(results['user_roles']['detected_roles'])
        if role_count < 2:
            recommendations.append(
                "👥 Define multiple user roles - consider different user personas and their specific needs"
            )

        # Features
        feature_count = results['feature_areas']['total_features']
        if feature_count < 8:
            recommendations.append(
                f"🎯 Expand feature set - currently {feature_count} features, consider adding complementary features"
            )

        # User flows
        flow_count = len(results['user_flows']['detected_flows'])
        if flow_count < 3:
            recommendations.append(
                "🔄 Map out complete user flows - ensure authentication, onboarding, and core workflows are designed"
            )

        # Navigation
        nav_count = results['navigation_structure']['nav_component_count']
        if nav_count < 3:
            recommendations.append(
                "🧭 Strengthen navigation - add consistent navigation patterns across all screens"
            )

        if not recommendations:
            recommendations.append("🎉 Product design is comprehensive! Focus on refining interactions and details.")

        print("💡 Actionable Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"\n  {i}. {rec}")

        return recommendations

    def _print_product_report(self, results: Dict):
        """Print final product analysis report."""

        print("\n" + "="*80)
        print("🦸 JUSTICE LEAGUE - PRODUCT ANALYSIS COMPLETE")
        print("="*80 + "\n")

        completeness = results['completeness']
        print(f"🏆 COMPLETENESS SCORE: {completeness['total_score']}/100 ({completeness['grade']})")
        print(f"📊 {completeness['level']}")

        print(f"\n📋 PRODUCT SUMMARY:")
        print(f"  • {results['pages_and_screens']['total_pages']} pages")
        print(f"  • {results['pages_and_screens']['total_screens']} screens")
        print(f"  • {results['feature_areas']['total_features']} feature areas")
        print(f"  • {len(results['user_roles']['detected_roles'])} user roles")
        print(f"  • {results['navigation_structure']['nav_component_count']} navigation components")

        print("\n")


def main():
    figma_url = "https://www.figma.com/design/fubdMARNgA2lVhmzpPg77y/3.00---UI-Master?node-id=0-1&t=kCuy701fY4EDM3Dd-1"
    figma_token = "figd_aPXrH3Rqpm8sdez_nHmmXKHvZ9vcK3sOcJwvhE7s"

    analyzer = ProductUIAnalyzer(figma_token)
    results = analyzer.analyze_product(figma_url)

    return results


if __name__ == "__main__":
    results = main()
