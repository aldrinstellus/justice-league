#!/usr/bin/env python3
"""
🦸 JUSTICE LEAGUE - Figma UI Master Analysis
============================================

Comprehensive analysis of Figma UI Master design system:
https://www.figma.com/design/fubdMARNgA2lVhmzpPg77y/3.00---UI-Master?node-id=211-2283

Deployed Heroes:
- 🦸 Superman (Figma Integration & Coordination)
- 🎨 Artemis CodeSmith (Component Analysis)
- 🔬 The Atom (Component Structure)
- ✅ Component Validator (Design System Validation)
- 🤖 Cyborg (Integration Analysis)

Author: Justice League
Date: October 23, 2025
"""

import sys
import json
import os
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# Add core to path
sys.path.insert(0, str(Path(__file__).parent))

from core.superman_figma_integration import SupermanFigmaIntegration
from core.superman_component_validator import SupermanComponentValidator


class JusticeLeagueFigmaAnalyzer:
    """
    Justice League Figma Design System Analyzer

    Coordinates multiple heroes to provide comprehensive Figma analysis.
    """

    def __init__(self, figma_token: str = None):
        """
        Initialize Justice League for Figma analysis.

        Args:
            figma_token: Figma Personal Access Token
        """
        # Get token from environment or use provided
        self.figma_token = figma_token or os.environ.get('FIGMA_ACCESS_TOKEN', 'figd_aPXrH3Rqpm8sdez_nHmmXKHvZ9vcK3sOcJwvhE7s')

        # Initialize heroes
        print("\n🦸 ========================================")
        print("🦸  ASSEMBLING JUSTICE LEAGUE FOR FIGMA")
        print("🦸 ========================================\n")

        self.superman = SupermanFigmaIntegration(self.figma_token)
        self.validator = SupermanComponentValidator()

        print("✅ 🦸 Superman (Figma Integration) - READY")
        print("✅ 🔬 Component Validator - READY")
        print("✅ 🎨 Artemis Analysis Module - READY")

    def analyze_figma_file(self, figma_url: str) -> Dict[str, Any]:
        """
        Comprehensive Figma file analysis.

        Args:
            figma_url: Figma file URL

        Returns:
            Complete Justice League analysis
        """
        print(f"\n📋 TARGET: {figma_url}")
        print(f"🕐 TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        results = {
            'mission': '🦸 Justice League Figma Analysis',
            'timestamp': datetime.now().isoformat(),
            'target_url': figma_url,
            'heroes_deployed': [],
            'analyses': {}
        }

        # Extract file key
        file_key = self.superman.extract_file_key(figma_url)
        print(f"🔑 File Key: {file_key}")

        # Extract node ID if present
        node_id = None
        if 'node-id=' in figma_url:
            node_id = figma_url.split('node-id=')[1].split('&')[0]
            print(f"🎯 Node ID: {node_id}")

        print("\n" + "="*60)
        print("PHASE 1: SUPERMAN - FIGMA DATA EXTRACTION")
        print("="*60 + "\n")

        # Get file data
        file_data = self.superman.get_file_data(file_key, depth=3)

        if 'error' in file_data:
            print(f"❌ ERROR: {file_data['error']}")
            print(f"💡 {file_data.get('superman_says', 'Check your Figma token!')}")
            results['analyses']['superman_extraction'] = {
                'status': 'error',
                'error': file_data['error']
            }
            return results

        # Analyze file structure
        superman_analysis = self._analyze_with_superman(file_data, file_key, node_id)
        results['analyses']['superman_extraction'] = superman_analysis
        results['heroes_deployed'].append('🦸 Superman')

        print("\n" + "="*60)
        print("PHASE 2: ARTEMIS - COMPONENT ANALYSIS")
        print("="*60 + "\n")

        # Analyze components
        artemis_analysis = self._analyze_with_artemis(file_data, file_key)
        results['analyses']['artemis_components'] = artemis_analysis
        results['heroes_deployed'].append('🎨 Artemis')

        print("\n" + "="*60)
        print("PHASE 3: COMPONENT VALIDATOR - DESIGN SYSTEM")
        print("="*60 + "\n")

        # Validate design system
        validator_analysis = self._analyze_with_validator(file_data)
        results['analyses']['component_validator'] = validator_analysis
        results['heroes_deployed'].append('✅ Component Validator')

        print("\n" + "="*60)
        print("PHASE 4: THE ATOM - COMPONENT STRUCTURE")
        print("="*60 + "\n")

        # Analyze component structure
        atom_analysis = self._analyze_with_atom(file_data)
        results['analyses']['atom_structure'] = atom_analysis
        results['heroes_deployed'].append('🔬 The Atom')

        # Calculate overall score
        results['justice_league_score'] = self._calculate_jl_score(results)

        return results

    def _analyze_with_superman(self, file_data: Dict, file_key: str, node_id: str = None) -> Dict[str, Any]:
        """Superman's Figma extraction analysis."""

        print("🦸 Superman analyzing Figma file structure...")

        document = file_data.get('document', {})
        name = file_data.get('name', 'Unknown')
        last_modified = file_data.get('lastModified', 'Unknown')
        version = file_data.get('version', 'Unknown')

        print(f"📄 File Name: {name}")
        print(f"📅 Last Modified: {last_modified}")
        print(f"🔢 Version: {version}")

        # Count nodes
        def count_nodes(node, node_types=None):
            if node_types is None:
                node_types = {}

            node_type = node.get('type', 'UNKNOWN')
            node_types[node_type] = node_types.get(node_type, 0) + 1

            for child in node.get('children', []):
                count_nodes(child, node_types)

            return node_types

        node_types = count_nodes(document)

        print(f"\n📊 Node Statistics:")
        for node_type, count in sorted(node_types.items(), key=lambda x: x[1], reverse=True):
            print(f"  {node_type}: {count}")

        # Extract styles
        styles = file_data.get('styles', {})
        print(f"\n🎨 Styles Found: {len(styles)}")

        # Extract components
        components = file_data.get('components', {})
        print(f"🧩 Components Found: {len(components)}")

        if components:
            print(f"\n📋 Component List (showing first 10):")
            for i, (comp_id, comp_data) in enumerate(list(components.items())[:10]):
                comp_name = comp_data.get('name', 'Unnamed')
                comp_desc = comp_data.get('description', 'No description')
                print(f"  {i+1}. {comp_name}")
                if comp_desc and comp_desc != 'No description':
                    print(f"     → {comp_desc[:60]}...")

        return {
            'status': 'success',
            'file_name': name,
            'last_modified': last_modified,
            'version': version,
            'total_nodes': sum(node_types.values()),
            'node_types': node_types,
            'total_styles': len(styles),
            'total_components': len(components),
            'components': list(components.keys())[:20],  # First 20 component IDs
            'score': 100.0,
            'superman_says': f"✅ Extracted {len(components)} components from '{name}'!"
        }

    def _analyze_with_artemis(self, file_data: Dict, file_key: str) -> Dict[str, Any]:
        """Artemis CodeSmith component analysis."""

        print("🎨 Artemis analyzing components and design patterns...")

        components = file_data.get('components', {})

        if not components:
            print("⚠️ No components found in Figma file")
            return {
                'status': 'warning',
                'components_found': 0,
                'score': 50.0,
                'artemis_says': "No components found. This might be a pure design file."
            }

        # Analyze component types and patterns
        component_analysis = {
            'buttons': [],
            'inputs': [],
            'cards': [],
            'icons': [],
            'layouts': [],
            'other': []
        }

        for comp_id, comp_data in components.items():
            comp_name = comp_data.get('name', '').lower()

            if 'button' in comp_name or 'btn' in comp_name:
                component_analysis['buttons'].append(comp_data.get('name'))
            elif 'input' in comp_name or 'text field' in comp_name or 'textfield' in comp_name:
                component_analysis['inputs'].append(comp_data.get('name'))
            elif 'card' in comp_name:
                component_analysis['cards'].append(comp_data.get('name'))
            elif 'icon' in comp_name:
                component_analysis['icons'].append(comp_data.get('name'))
            elif 'layout' in comp_name or 'container' in comp_name or 'frame' in comp_name:
                component_analysis['layouts'].append(comp_data.get('name'))
            else:
                component_analysis['other'].append(comp_data.get('name'))

        print(f"\n📊 Component Breakdown:")
        print(f"  🔘 Buttons: {len(component_analysis['buttons'])}")
        print(f"  📝 Inputs: {len(component_analysis['inputs'])}")
        print(f"  🎴 Cards: {len(component_analysis['cards'])}")
        print(f"  ✨ Icons: {len(component_analysis['icons'])}")
        print(f"  📐 Layouts: {len(component_analysis['layouts'])}")
        print(f"  ➕ Other: {len(component_analysis['other'])}")

        # Show examples
        if component_analysis['buttons']:
            print(f"\n🔘 Button Components (showing first 5):")
            for btn in component_analysis['buttons'][:5]:
                print(f"  - {btn}")

        # Calculate Artemis score
        score = 100.0
        total_components = len(components)

        # Scoring based on component diversity
        unique_types = sum(1 for v in component_analysis.values() if v)
        if unique_types < 3:
            score -= 20
            print(f"\n⚠️ Limited component diversity (only {unique_types} types)")

        return {
            'status': 'success',
            'total_components': total_components,
            'component_breakdown': {k: len(v) for k, v in component_analysis.items()},
            'component_types': unique_types,
            'score': score,
            'artemis_says': f"✅ Analyzed {total_components} components with {unique_types} distinct types!"
        }

    def _analyze_with_validator(self, file_data: Dict) -> Dict[str, Any]:
        """Component Validator design system analysis."""

        print("✅ Component Validator checking design system consistency...")

        styles = file_data.get('styles', {})
        components = file_data.get('components', {})

        # Analyze color styles
        color_styles = [s for s in styles.values() if s.get('styleType') == 'FILL']
        text_styles = [s for s in styles.values() if s.get('styleType') == 'TEXT']
        effect_styles = [s for s in styles.values() if s.get('styleType') == 'EFFECT']

        print(f"\n🎨 Style Analysis:")
        print(f"  Color Styles: {len(color_styles)}")
        print(f"  Text Styles: {len(text_styles)}")
        print(f"  Effect Styles: {len(effect_styles)}")

        # Check for design token usage
        has_colors = len(color_styles) > 0
        has_typography = len(text_styles) > 0
        has_effects = len(effect_styles) > 0

        consistency_checks = {
            'has_color_system': has_colors,
            'has_typography_system': has_typography,
            'has_effect_system': has_effects,
            'has_component_library': len(components) > 0
        }

        # Calculate score
        score = sum(consistency_checks.values()) * 25.0

        print(f"\n✅ Design System Checks:")
        print(f"  Color System: {'✅' if has_colors else '❌'}")
        print(f"  Typography System: {'✅' if has_typography else '❌'}")
        print(f"  Effect System: {'✅' if has_effects else '❌'}")
        print(f"  Component Library: {'✅' if len(components) > 0 else '❌'}")

        # Recommendations
        recommendations = []
        if not has_colors:
            recommendations.append("💡 Add color styles for consistent color usage")
        if not has_typography:
            recommendations.append("💡 Define text styles for typography consistency")
        if not has_effects:
            recommendations.append("💡 Create effect styles for shadows and other effects")

        if recommendations:
            print(f"\n💡 Recommendations:")
            for rec in recommendations:
                print(f"  {rec}")

        return {
            'status': 'success',
            'total_styles': len(styles),
            'color_styles': len(color_styles),
            'text_styles': len(text_styles),
            'effect_styles': len(effect_styles),
            'consistency_checks': consistency_checks,
            'score': score,
            'recommendations': recommendations,
            'validator_says': f"✅ Design system scored {score}/100!"
        }

    def _analyze_with_atom(self, file_data: Dict) -> Dict[str, Any]:
        """The Atom's component structure analysis."""

        print("🔬 The Atom analyzing component structure and relationships...")

        components = file_data.get('components', {})

        # Analyze component naming conventions
        naming_analysis = {
            'has_prefixes': False,
            'uses_slashes': False,
            'consistent_casing': True
        }

        if components:
            names = [c.get('name', '') for c in components.values()]

            # Check for prefixes (icon/, button/, etc.)
            naming_analysis['uses_slashes'] = any('/' in name for name in names)

            # Check for consistent casing
            if names:
                first_has_capital = names[0][0].isupper() if names[0] else False
                naming_analysis['consistent_casing'] = all(
                    (name[0].isupper() if name else False) == first_has_capital
                    for name in names
                )

            print(f"\n📋 Naming Convention Analysis:")
            print(f"  Uses '/' separators: {'✅' if naming_analysis['uses_slashes'] else '❌'}")
            print(f"  Consistent casing: {'✅' if naming_analysis['consistent_casing'] else '❌'}")

        # Calculate score
        score = 70.0
        if naming_analysis['uses_slashes']:
            score += 15.0
        if naming_analysis['consistent_casing']:
            score += 15.0

        return {
            'status': 'success',
            'total_components': len(components),
            'naming_analysis': naming_analysis,
            'score': score,
            'atom_says': f"✅ Component structure scored {score}/100!"
        }

    def _calculate_jl_score(self, results: Dict) -> Dict[str, Any]:
        """Calculate overall Justice League score."""

        analyses = results.get('analyses', {})

        scores = []
        for analysis in analyses.values():
            if isinstance(analysis, dict) and 'score' in analysis:
                scores.append(analysis['score'])

        if not scores:
            overall_score = 0.0
            grade = 'F'
        else:
            overall_score = sum(scores) / len(scores)

            # Grade calculation
            if overall_score >= 98:
                grade = 'S+'
            elif overall_score >= 90:
                grade = 'S'
            elif overall_score >= 85:
                grade = 'A'
            elif overall_score >= 80:
                grade = 'B'
            elif overall_score >= 70:
                grade = 'C'
            elif overall_score >= 60:
                grade = 'D'
            else:
                grade = 'F'

        return {
            'overall_score': round(overall_score, 1),
            'grade': grade,
            'hero_scores': {
                'superman': analyses.get('superman_extraction', {}).get('score', 0),
                'artemis': analyses.get('artemis_components', {}).get('score', 0),
                'validator': analyses.get('component_validator', {}).get('score', 0),
                'atom': analyses.get('atom_structure', {}).get('score', 0)
            }
        }

    def print_final_report(self, results: Dict[str, Any]):
        """Print final Justice League report."""

        print("\n" + "="*60)
        print("🦸 JUSTICE LEAGUE FINAL REPORT")
        print("="*60 + "\n")

        jl_score = results.get('justice_league_score', {})
        overall_score = jl_score.get('overall_score', 0)
        grade = jl_score.get('grade', 'F')

        print(f"⭐ OVERALL SCORE: {overall_score}/100 ({grade})")
        print(f"🦸 Heroes Deployed: {len(results.get('heroes_deployed', []))}")
        print(f"📅 Timestamp: {results.get('timestamp', 'Unknown')}")

        print(f"\n🦸 Individual Hero Scores:")
        for hero, score in jl_score.get('hero_scores', {}).items():
            print(f"  {hero.title()}: {score}/100")

        print(f"\n📊 Key Findings:")

        # Superman findings
        superman = results.get('analyses', {}).get('superman_extraction', {})
        if superman:
            print(f"\n  🦸 Superman:")
            print(f"    - Components: {superman.get('total_components', 0)}")
            print(f"    - Styles: {superman.get('total_styles', 0)}")
            print(f"    - Total Nodes: {superman.get('total_nodes', 0)}")
            print(f"    - {superman.get('superman_says', '')}")

        # Artemis findings
        artemis = results.get('analyses', {}).get('artemis_components', {})
        if artemis:
            print(f"\n  🎨 Artemis:")
            print(f"    - Total Components: {artemis.get('total_components', 0)}")
            print(f"    - Component Types: {artemis.get('component_types', 0)}")
            breakdown = artemis.get('component_breakdown', {})
            if breakdown:
                for comp_type, count in breakdown.items():
                    if count > 0:
                        print(f"    - {comp_type.title()}: {count}")
            print(f"    - {artemis.get('artemis_says', '')}")

        # Validator findings
        validator = results.get('analyses', {}).get('component_validator', {})
        if validator:
            print(f"\n  ✅ Component Validator:")
            print(f"    - Color Styles: {validator.get('color_styles', 0)}")
            print(f"    - Text Styles: {validator.get('text_styles', 0)}")
            print(f"    - Effect Styles: {validator.get('effect_styles', 0)}")
            recommendations = validator.get('recommendations', [])
            if recommendations:
                print(f"    - Recommendations:")
                for rec in recommendations:
                    print(f"      {rec}")
            print(f"    - {validator.get('validator_says', '')}")

        # Atom findings
        atom = results.get('analyses', {}).get('atom_structure', {})
        if atom:
            print(f"\n  🔬 The Atom:")
            naming = atom.get('naming_analysis', {})
            print(f"    - Uses '/' separators: {'✅' if naming.get('uses_slashes') else '❌'}")
            print(f"    - Consistent casing: {'✅' if naming.get('consistent_casing') else '❌'}")
            print(f"    - {atom.get('atom_says', '')}")

        print("\n" + "="*60)
        print("🦸 JUSTICE LEAGUE ANALYSIS COMPLETE!")
        print("="*60 + "\n")

        # Save to file
        output_file = Path('figma_analysis_report.json')
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"📄 Full report saved to: {output_file}")


def main():
    """Main execution."""

    figma_url = "https://www.figma.com/design/fubdMARNgA2lVhmzpPg77y/3.00---UI-Master?node-id=211-2283&t=moFl3IGVkwCrl2AA-1"

    print("\n🦸 ========================================")
    print("🦸  JUSTICE LEAGUE - FIGMA ANALYSIS")
    print("🦸 ========================================")
    print(f"\n🎯 Target: {figma_url}\n")

    # Initialize analyzer
    analyzer = JusticeLeagueFigmaAnalyzer()

    # Analyze Figma file
    results = analyzer.analyze_figma_file(figma_url)

    # Print final report
    analyzer.print_final_report(results)

    return results


if __name__ == "__main__":
    results = main()
