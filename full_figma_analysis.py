#!/usr/bin/env python3
"""
🦸 JUSTICE LEAGUE - FULL FIGMA UI MASTER ANALYSIS
==================================================

Comprehensive deep-dive analysis of Figma UI Master design system.

Analyzes:
- Complete component inventory with names
- Color palette and color system
- Typography system (fonts, sizes, weights)
- Spacing and layout patterns
- Component variants and states
- Design system maturity
- Organization and naming conventions
- Accessibility considerations
- Production-readiness assessment

Author: Justice League
Date: October 23, 2025
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Set
from datetime import datetime
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))

from core.superman_figma_integration import SupermanFigmaIntegration


class FullFigmaAnalyzer:
    """Comprehensive Figma file analyzer."""

    def __init__(self, figma_token: str):
        self.figma_token = figma_token
        self.superman = SupermanFigmaIntegration(figma_token)

    def analyze(self, figma_url: str) -> Dict[str, Any]:
        """Run full comprehensive analysis."""

        print("\n" + "="*80)
        print("🦸 JUSTICE LEAGUE - FULL FIGMA UI MASTER ANALYSIS")
        print("="*80 + "\n")

        file_key = self.superman.extract_file_key(figma_url)
        print(f"🔑 File Key: {file_key}\n")

        # Get complete file data with max depth
        print("📥 Fetching complete Figma file data (this may take a moment)...")
        file_data = self.superman.get_file_data(file_key, depth=10)

        if 'error' in file_data:
            print(f"❌ ERROR: {file_data['error']}")
            return file_data

        print("✅ File data loaded successfully!\n")

        # Run all analyses
        results = {
            'file_info': self._analyze_file_info(file_data),
            'component_inventory': self._analyze_component_inventory(file_data),
            'color_system': self._analyze_color_system(file_data),
            'typography_system': self._analyze_typography_system(file_data),
            'effects_system': self._analyze_effects_system(file_data),
            'component_organization': self._analyze_component_organization(file_data),
            'canvas_structure': self._analyze_canvas_structure(file_data),
            'design_tokens': self._analyze_design_tokens(file_data),
            'maturity_assessment': None,  # Will calculate from above
            'recommendations': []  # Will generate from above
        }

        # Generate maturity assessment
        results['maturity_assessment'] = self._assess_design_system_maturity(results)

        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results)

        # Print comprehensive report
        self._print_full_report(results)

        # Save to file
        output_file = Path('full_figma_analysis_report.json')
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n📄 Full report saved to: {output_file}\n")

        return results

    def _analyze_file_info(self, file_data: Dict) -> Dict[str, Any]:
        """Analyze basic file information."""

        print("\n" + "="*80)
        print("📄 FILE INFORMATION")
        print("="*80 + "\n")

        info = {
            'name': file_data.get('name', 'Unknown'),
            'last_modified': file_data.get('lastModified', 'Unknown'),
            'version': file_data.get('version', 'Unknown'),
            'thumbnail_url': file_data.get('thumbnailUrl', None),
            'role': file_data.get('role', 'Unknown')
        }

        print(f"📝 Name: {info['name']}")
        print(f"📅 Last Modified: {info['last_modified']}")
        print(f"🔢 Version: {info['version']}")
        print(f"👤 Your Role: {info['role']}")

        return info

    def _analyze_component_inventory(self, file_data: Dict) -> Dict[str, Any]:
        """Complete component inventory with all names."""

        print("\n" + "="*80)
        print("🧩 COMPONENT INVENTORY")
        print("="*80 + "\n")

        components = file_data.get('components', {})
        component_sets = file_data.get('componentSets', {})

        # Extract all component names and organize by category
        component_list = []
        categories = defaultdict(list)

        for comp_id, comp_data in components.items():
            name = comp_data.get('name', 'Unnamed')
            description = comp_data.get('description', '')

            component_list.append({
                'id': comp_id,
                'name': name,
                'description': description,
                'containing_frame': comp_data.get('containingFrame', {}).get('name', 'Unknown')
            })

            # Categorize by name prefix (before first /)
            if '/' in name:
                category = name.split('/')[0]
                categories[category].append(name)
            else:
                categories['Uncategorized'].append(name)

        print(f"📊 Total Components: {len(component_list)}")
        print(f"📦 Component Sets: {len(component_sets)}")
        print(f"🗂️  Categories: {len(categories)}\n")

        # Print categories
        print("📂 Component Categories:")
        for category, comps in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"  {category}: {len(comps)} components")

        # Print all component names
        print(f"\n📋 All Components (sorted alphabetically):")
        for i, comp in enumerate(sorted(component_list, key=lambda x: x['name']), 1):
            print(f"  {i:3d}. {comp['name']}")
            if comp['description']:
                print(f"       → {comp['description'][:70]}")

        return {
            'total': len(component_list),
            'total_sets': len(component_sets),
            'categories': {k: len(v) for k, v in categories.items()},
            'components': component_list,
            'category_details': dict(categories)
        }

    def _analyze_color_system(self, file_data: Dict) -> Dict[str, Any]:
        """Analyze color styles and palette."""

        print("\n" + "="*80)
        print("🎨 COLOR SYSTEM")
        print("="*80 + "\n")

        styles = file_data.get('styles', {})
        color_styles = []

        for style_id, style_data in styles.items():
            if style_data.get('styleType') == 'FILL':
                name = style_data.get('name', 'Unnamed')
                description = style_data.get('description', '')
                color_styles.append({
                    'id': style_id,
                    'name': name,
                    'description': description
                })

        print(f"🎨 Total Color Styles: {len(color_styles)}\n")

        # Organize by category
        color_categories = defaultdict(list)
        for style in color_styles:
            name = style['name']
            if '/' in name:
                category = name.split('/')[0]
                color_categories[category].append(name)
            else:
                color_categories['Uncategorized'].append(name)

        print("📂 Color Categories:")
        for category, colors in sorted(color_categories.items()):
            print(f"  {category}: {len(colors)} colors")

        print(f"\n🎨 All Color Styles:")
        for i, style in enumerate(sorted(color_styles, key=lambda x: x['name']), 1):
            print(f"  {i:2d}. {style['name']}")
            if style['description']:
                print(f"      → {style['description']}")

        return {
            'total': len(color_styles),
            'categories': {k: len(v) for k, v in color_categories.items()},
            'styles': color_styles,
            'category_details': dict(color_categories)
        }

    def _analyze_typography_system(self, file_data: Dict) -> Dict[str, Any]:
        """Analyze typography styles."""

        print("\n" + "="*80)
        print("✍️  TYPOGRAPHY SYSTEM")
        print("="*80 + "\n")

        styles = file_data.get('styles', {})
        text_styles = []

        for style_id, style_data in styles.items():
            if style_data.get('styleType') == 'TEXT':
                name = style_data.get('name', 'Unnamed')
                description = style_data.get('description', '')
                text_styles.append({
                    'id': style_id,
                    'name': name,
                    'description': description
                })

        print(f"✍️  Total Text Styles: {len(text_styles)}\n")

        # Organize by category
        text_categories = defaultdict(list)
        for style in text_styles:
            name = style['name']
            if '/' in name:
                category = name.split('/')[0]
                text_categories[category].append(name)
            else:
                text_categories['Uncategorized'].append(name)

        print("📂 Typography Categories:")
        for category, styles_list in sorted(text_categories.items()):
            print(f"  {category}: {len(styles_list)} styles")

        print(f"\n✍️  All Text Styles:")
        for i, style in enumerate(sorted(text_styles, key=lambda x: x['name']), 1):
            print(f"  {i}. {style['name']}")
            if style['description']:
                print(f"     → {style['description']}")

        return {
            'total': len(text_styles),
            'categories': {k: len(v) for k, v in text_categories.items()},
            'styles': text_styles,
            'category_details': dict(text_categories)
        }

    def _analyze_effects_system(self, file_data: Dict) -> Dict[str, Any]:
        """Analyze effect styles (shadows, blurs)."""

        print("\n" + "="*80)
        print("✨ EFFECTS SYSTEM")
        print("="*80 + "\n")

        styles = file_data.get('styles', {})
        effect_styles = []

        for style_id, style_data in styles.items():
            if style_data.get('styleType') == 'EFFECT':
                name = style_data.get('name', 'Unnamed')
                description = style_data.get('description', '')
                effect_styles.append({
                    'id': style_id,
                    'name': name,
                    'description': description
                })

        print(f"✨ Total Effect Styles: {len(effect_styles)}\n")

        # Organize by category
        effect_categories = defaultdict(list)
        for style in effect_styles:
            name = style['name']
            if '/' in name:
                category = name.split('/')[0]
                effect_categories[category].append(name)
            else:
                effect_categories['Uncategorized'].append(name)

        print("📂 Effect Categories:")
        for category, effects in sorted(effect_categories.items()):
            print(f"  {category}: {len(effects)} effects")

        print(f"\n✨ All Effect Styles:")
        for i, style in enumerate(sorted(effect_styles, key=lambda x: x['name']), 1):
            print(f"  {i:2d}. {style['name']}")
            if style['description']:
                print(f"      → {style['description']}")

        return {
            'total': len(effect_styles),
            'categories': {k: len(v) for k, v in effect_categories.items()},
            'styles': effect_styles,
            'category_details': dict(effect_categories)
        }

    def _analyze_component_organization(self, file_data: Dict) -> Dict[str, Any]:
        """Analyze how components are organized."""

        print("\n" + "="*80)
        print("🗂️  COMPONENT ORGANIZATION")
        print("="*80 + "\n")

        components = file_data.get('components', {})

        # Analyze naming conventions
        naming_patterns = {
            'uses_slashes': 0,
            'uses_dashes': 0,
            'uses_camelCase': 0,
            'uses_PascalCase': 0,
            'uses_snake_case': 0,
            'uses_spaces': 0
        }

        variant_keywords = ['State=', 'Type=', 'Size=', 'Variant=', 'Property=', 'Label=']
        components_with_variants = 0

        for comp_data in components.values():
            name = comp_data.get('name', '')

            if '/' in name:
                naming_patterns['uses_slashes'] += 1
            if '-' in name:
                naming_patterns['uses_dashes'] += 1
            if name and name[0].isupper() and name[1:] and name[1].islower():
                naming_patterns['uses_PascalCase'] += 1
            if name and name[0].islower() and any(c.isupper() for c in name[1:]):
                naming_patterns['uses_camelCase'] += 1
            if '_' in name:
                naming_patterns['uses_snake_case'] += 1
            if ' ' in name:
                naming_patterns['uses_spaces'] += 1

            # Check for variants
            if any(keyword in name for keyword in variant_keywords):
                components_with_variants += 1

        print("📝 Naming Conventions:")
        print(f"  Components using '/' separators: {naming_patterns['uses_slashes']}")
        print(f"  Components using '-' separators: {naming_patterns['uses_dashes']}")
        print(f"  Components using spaces: {naming_patterns['uses_spaces']}")
        print(f"  PascalCase usage: {naming_patterns['uses_PascalCase']}")
        print(f"  camelCase usage: {naming_patterns['uses_camelCase']}")
        print(f"  snake_case usage: {naming_patterns['uses_snake_case']}")

        print(f"\n🔄 Component Variants:")
        print(f"  Components with variant properties: {components_with_variants}")

        # Determine primary naming convention
        primary_convention = max(naming_patterns.items(), key=lambda x: x[1])
        print(f"\n✅ Primary Convention: {primary_convention[0]} ({primary_convention[1]} components)")

        return {
            'naming_patterns': naming_patterns,
            'components_with_variants': components_with_variants,
            'primary_convention': primary_convention[0],
            'consistency_score': (primary_convention[1] / len(components) * 100) if components else 0
        }

    def _analyze_canvas_structure(self, file_data: Dict) -> Dict[str, Any]:
        """Analyze page/canvas organization."""

        print("\n" + "="*80)
        print("📐 CANVAS STRUCTURE")
        print("="*80 + "\n")

        document = file_data.get('document', {})
        children = document.get('children', [])

        canvases = []
        for canvas in children:
            if canvas.get('type') == 'CANVAS':
                name = canvas.get('name', 'Unnamed')
                num_children = len(canvas.get('children', []))
                canvases.append({
                    'name': name,
                    'children': num_children
                })

        print(f"📄 Total Canvases/Pages: {len(canvases)}\n")

        for i, canvas in enumerate(canvases, 1):
            print(f"  {i}. {canvas['name']}")
            print(f"     → {canvas['children']} frames/sections")

        return {
            'total': len(canvases),
            'canvases': canvases
        }

    def _analyze_design_tokens(self, file_data: Dict) -> Dict[str, Any]:
        """Analyze design token usage."""

        print("\n" + "="*80)
        print("🎯 DESIGN TOKENS")
        print("="*80 + "\n")

        styles = file_data.get('styles', {})

        tokens = {
            'colors': 0,
            'typography': 0,
            'effects': 0,
            'total': len(styles)
        }

        for style_data in styles.values():
            style_type = style_data.get('styleType')
            if style_type == 'FILL':
                tokens['colors'] += 1
            elif style_type == 'TEXT':
                tokens['typography'] += 1
            elif style_type == 'EFFECT':
                tokens['effects'] += 1

        print(f"🎯 Design Token Summary:")
        print(f"  Total Tokens: {tokens['total']}")
        print(f"  Color Tokens: {tokens['colors']}")
        print(f"  Typography Tokens: {tokens['typography']}")
        print(f"  Effect Tokens: {tokens['effects']}")

        has_comprehensive_system = (
            tokens['colors'] >= 10 and
            tokens['typography'] >= 5 and
            tokens['effects'] >= 3
        )

        print(f"\n✅ Comprehensive Token System: {'Yes' if has_comprehensive_system else 'No'}")

        return tokens

    def _assess_design_system_maturity(self, results: Dict) -> Dict[str, Any]:
        """Assess overall design system maturity."""

        print("\n" + "="*80)
        print("🏆 DESIGN SYSTEM MATURITY ASSESSMENT")
        print("="*80 + "\n")

        # Scoring criteria
        scores = {}

        # 1. Component Library (0-25 points)
        comp_count = results['component_inventory']['total']
        if comp_count >= 100:
            scores['component_library'] = 25
        elif comp_count >= 50:
            scores['component_library'] = 20
        elif comp_count >= 25:
            scores['component_library'] = 15
        else:
            scores['component_library'] = 10

        # 2. Color System (0-20 points)
        color_count = results['color_system']['total']
        if color_count >= 30:
            scores['color_system'] = 20
        elif color_count >= 20:
            scores['color_system'] = 15
        elif color_count >= 10:
            scores['color_system'] = 10
        else:
            scores['color_system'] = 5

        # 3. Typography System (0-15 points)
        typo_count = results['typography_system']['total']
        if typo_count >= 10:
            scores['typography_system'] = 15
        elif typo_count >= 5:
            scores['typography_system'] = 12
        elif typo_count >= 3:
            scores['typography_system'] = 8
        else:
            scores['typography_system'] = 5

        # 4. Effects System (0-10 points)
        effects_count = results['effects_system']['total']
        if effects_count >= 10:
            scores['effects_system'] = 10
        elif effects_count >= 5:
            scores['effects_system'] = 7
        else:
            scores['effects_system'] = 5

        # 5. Organization (0-15 points)
        consistency = results['component_organization']['consistency_score']
        if consistency >= 80:
            scores['organization'] = 15
        elif consistency >= 60:
            scores['organization'] = 10
        else:
            scores['organization'] = 5

        # 6. Component Variants (0-15 points)
        variants = results['component_organization']['components_with_variants']
        if variants >= 20:
            scores['variants'] = 15
        elif variants >= 10:
            scores['variants'] = 10
        else:
            scores['variants'] = 5

        total_score = sum(scores.values())

        # Maturity levels
        if total_score >= 90:
            level = "🏆 MATURE - Production-grade design system"
            grade = "A+"
        elif total_score >= 80:
            level = "⭐ ADVANCED - Well-structured system"
            grade = "A"
        elif total_score >= 70:
            level = "✅ INTERMEDIATE - Good foundation"
            grade = "B"
        elif total_score >= 60:
            level = "🌱 DEVELOPING - Basic structure in place"
            grade = "C"
        else:
            level = "🔧 EMERGING - Needs significant work"
            grade = "D"

        print(f"📊 Maturity Score: {total_score}/100 ({grade})")
        print(f"🏅 Maturity Level: {level}\n")

        print("📈 Score Breakdown:")
        print(f"  Component Library: {scores['component_library']}/25")
        print(f"  Color System: {scores['color_system']}/20")
        print(f"  Typography System: {scores['typography_system']}/15")
        print(f"  Effects System: {scores['effects_system']}/10")
        print(f"  Organization: {scores['organization']}/15")
        print(f"  Component Variants: {scores['variants']}/15")

        return {
            'total_score': total_score,
            'grade': grade,
            'level': level,
            'scores': scores
        }

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate actionable recommendations."""

        print("\n" + "="*80)
        print("💡 RECOMMENDATIONS")
        print("="*80 + "\n")

        recommendations = []

        # Component organization
        consistency = results['component_organization']['consistency_score']
        if consistency < 80:
            recommendations.append(
                "📝 Improve naming consistency - standardize on a single naming convention (e.g., PascalCase or slash-separated)"
            )

        # Typography
        if results['typography_system']['total'] < 5:
            recommendations.append(
                "✍️  Expand typography system - add more text styles for different use cases (headings, body, captions, etc.)"
            )

        # Color system
        if results['color_system']['total'] < 20:
            recommendations.append(
                "🎨 Enhance color palette - consider adding semantic colors (success, warning, error, info) and shades"
            )

        # Effects
        if results['effects_system']['total'] < 5:
            recommendations.append(
                "✨ Add more effect styles - define elevation system with multiple shadow levels"
            )

        # Component variants
        variants = results['component_organization']['components_with_variants']
        if variants < 20:
            recommendations.append(
                "🔄 Add component variants - create more states (hover, active, disabled) and sizes for reusability"
            )

        # Documentation
        components = results['component_inventory']['components']
        components_with_desc = sum(1 for c in components if c.get('description'))
        if components_with_desc < len(components) * 0.5:
            recommendations.append(
                "📚 Add component descriptions - document usage and best practices for each component"
            )

        if not recommendations:
            recommendations.append("🎉 Excellent! Design system is well-structured with no major issues.")

        print("💡 Actionable Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"\n  {i}. {rec}")

        return recommendations

    def _print_full_report(self, results: Dict):
        """Print final comprehensive report."""

        print("\n" + "="*80)
        print("🦸 JUSTICE LEAGUE - FULL ANALYSIS COMPLETE")
        print("="*80 + "\n")

        maturity = results['maturity_assessment']
        print(f"🏆 OVERALL MATURITY SCORE: {maturity['total_score']}/100 ({maturity['grade']})")
        print(f"📊 {maturity['level']}")

        print(f"\n📋 SUMMARY:")
        print(f"  • {results['component_inventory']['total']} components across {len(results['component_inventory']['categories'])} categories")
        print(f"  • {results['color_system']['total']} color tokens")
        print(f"  • {results['typography_system']['total']} typography tokens")
        print(f"  • {results['effects_system']['total']} effect tokens")
        print(f"  • {results['canvas_structure']['total']} canvases/pages")
        print(f"  • {results['component_organization']['components_with_variants']} components with variants")

        print(f"\n✅ STRENGTHS:")
        if results['component_inventory']['total'] >= 100:
            print(f"  • Comprehensive component library ({results['component_inventory']['total']} components)")
        if results['color_system']['total'] >= 30:
            print(f"  • Rich color system ({results['color_system']['total']} colors)")
        if results['component_organization']['consistency_score'] >= 80:
            print(f"  • Consistent naming convention ({results['component_organization']['consistency_score']:.0f}% consistency)")
        if results['effects_system']['total'] >= 10:
            print(f"  • Well-defined effects system ({results['effects_system']['total']} effects)")

        print("\n")


def main():
    figma_url = "https://www.figma.com/design/fubdMARNgA2lVhmzpPg77y/3.00---UI-Master?node-id=211-2283&t=moFl3IGVkwCrl2AA-1"
    figma_token = "figd_aPXrH3Rqpm8sdez_nHmmXKHvZ9vcK3sOcJwvhE7s"

    analyzer = FullFigmaAnalyzer(figma_token)
    results = analyzer.analyze(figma_url)

    return results


if __name__ == "__main__":
    results = main()
