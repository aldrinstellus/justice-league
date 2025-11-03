#!/usr/bin/env python3
"""
JL-003 Phase 1: Figma Project Inventory & Cost Estimation
Justice League Heroes: Superman (Coordinator), Hawkman (Figma Analysis), Oracle (Cost Tracking)

Analyzes the "Auzmor - Learn - Web&Mobile" Figma project and generates:
1. Complete file inventory with metadata
2. Per-file frame/page/component counts
3. PNG/PDF export cost estimations
4. Total project cost analysis
"""

import os
import sys
import json
import requests
from datetime import datetime
from typing import Dict, List, Any

# Figma API Configuration
FIGMA_TOKEN = os.getenv('FIGMA_ACCESS_TOKEN', 'figd_aPXrH3Rqpm8sdez_nHmmXKHvZ9vcK3sOcJwvhE7s')
FIGMA_API_BASE = 'https://api.figma.com/v1'

# Project Configuration
PROJECT_ID = '9863243'
TEAM_ID = '847347212738816925'

# Quicksilver Export Pricing (per frame)
# Based on Claude Sonnet 4.5 pricing: $3/1M input, $15/1M output
# Average tokens per frame export: ~500 input, ~100 output
COST_PER_FRAME_PNG = 0.0025  # $0.0025 per frame (includes API calls + processing)
COST_PER_FRAME_PDF = 0.0030  # $0.0030 per frame (PNG + PDF compilation)

class FigmaProjectAnalyzer:
    """Hawkman-powered Figma project structural analysis"""

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'X-Figma-Token': token,
            'Content-Type': 'application/json'
        }
        self.inventory = {
            'project_name': 'Auzmor - Learn - Web&Mobile',
            'project_id': PROJECT_ID,
            'team_id': TEAM_ID,
            'analysis_date': datetime.now().isoformat(),
            'total_files': 0,
            'total_frames': 0,
            'total_pages': 0,
            'total_components': 0,
            'files': [],
            'cost_estimation': {}
        }

    def get_project_files(self) -> List[Dict[str, Any]]:
        """🦅 Hawkman: Fetch all files in the Figma project"""
        print(f"\n🦅 Hawkman: Scanning Figma project {PROJECT_ID}...")

        url = f"{FIGMA_API_BASE}/projects/{PROJECT_ID}/files"

        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            files = data.get('files', [])
            print(f"🦅 Hawkman: Found {len(files)} files in project")
            return files

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching project files: {e}")
            return []

    def analyze_file_structure(self, file_key: str, file_name: str) -> Dict[str, Any]:
        """🦅 Hawkman: Analyze individual Figma file structure"""
        print(f"\n🦅 Hawkman: Analyzing file '{file_name}' ({file_key})...")

        url = f"{FIGMA_API_BASE}/files/{file_key}"

        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Count pages, frames, and components
            document = data.get('document', {})
            pages = document.get('children', [])

            file_analysis = {
                'file_key': file_key,
                'file_name': file_name,
                'last_modified': data.get('lastModified', 'Unknown'),
                'version': data.get('version', 'Unknown'),
                'pages': [],
                'total_pages': 0,
                'total_frames': 0,
                'total_components': 0
            }

            # Analyze each page
            for page in pages:
                page_info = self._analyze_page(page)
                file_analysis['pages'].append(page_info)
                file_analysis['total_frames'] += page_info['frame_count']

            file_analysis['total_pages'] = len(pages)

            # Count components
            components = data.get('components', {})
            file_analysis['total_components'] = len(components)

            print(f"  📊 Pages: {file_analysis['total_pages']}, Frames: {file_analysis['total_frames']}, Components: {file_analysis['total_components']}")

            return file_analysis

        except requests.exceptions.RequestException as e:
            print(f"  ❌ Error analyzing file: {e}")
            return {
                'file_key': file_key,
                'file_name': file_name,
                'error': str(e),
                'total_pages': 0,
                'total_frames': 0,
                'total_components': 0
            }

    def _analyze_page(self, page_node: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single page and count frames"""
        page_info = {
            'page_name': page_node.get('name', 'Unnamed'),
            'page_id': page_node.get('id', ''),
            'frame_count': 0,
            'frames': []
        }

        # Count top-level frames in the page
        children = page_node.get('children', [])
        for child in children:
            if child.get('type') == 'FRAME':
                page_info['frame_count'] += 1
                page_info['frames'].append({
                    'name': child.get('name', 'Unnamed'),
                    'id': child.get('id', '')
                })

        return page_info

    def calculate_export_costs(self) -> Dict[str, Any]:
        """🔮 Oracle: Calculate PNG/PDF export costs for the entire project"""
        print(f"\n🔮 Oracle: Calculating export costs...")

        total_frames = self.inventory['total_frames']

        costs = {
            'total_frames': total_frames,
            'png_export': {
                'cost_per_frame': COST_PER_FRAME_PNG,
                'total_cost': round(total_frames * COST_PER_FRAME_PNG, 2)
            },
            'pdf_export': {
                'cost_per_frame': COST_PER_FRAME_PDF,
                'total_cost': round(total_frames * COST_PER_FRAME_PDF, 2)
            },
            'combined_export': {
                'total_cost': round(total_frames * (COST_PER_FRAME_PNG + COST_PER_FRAME_PDF), 2)
            }
        }

        print(f"  💰 PNG Export: ${costs['png_export']['total_cost']} ({total_frames} frames × ${COST_PER_FRAME_PNG})")
        print(f"  💰 PDF Export: ${costs['pdf_export']['total_cost']} ({total_frames} frames × ${COST_PER_FRAME_PDF})")
        print(f"  💰 Combined: ${costs['combined_export']['total_cost']}")

        return costs

    def generate_inventory_report(self) -> str:
        """🔮 Oracle + ⚡ Wonder Woman: Generate comprehensive inventory report"""
        print(f"\n🔮 Oracle: Generating Phase 1 inventory report...")

        report_lines = [
            "# JL-003 Phase 1: Figma Project Inventory",
            "",
            f"**Mission:** Auzmor - Learn - Web&Mobile Design System Consolidation",
            f"**Analysis Date:** {self.inventory['analysis_date']}",
            f"**Analyzed By:** Superman (Coordinator), Hawkman (Figma Analysis), Oracle (Cost Tracking)",
            "",
            "---",
            "",
            "## 📊 Project Summary",
            "",
            f"- **Total Files:** {self.inventory['total_files']}",
            f"- **Total Pages:** {self.inventory['total_pages']}",
            f"- **Total Frames:** {self.inventory['total_frames']}",
            f"- **Total Components:** {self.inventory['total_components']}",
            "",
            "---",
            "",
            "## 💰 Export Cost Estimation",
            "",
            "### PNG Export Only",
            f"- **Cost per Frame:** ${COST_PER_FRAME_PNG}",
            f"- **Total Frames:** {self.inventory['cost_estimation']['total_frames']}",
            f"- **Total Cost:** ${self.inventory['cost_estimation']['png_export']['total_cost']}",
            "",
            "### PDF Export Only",
            f"- **Cost per Frame:** ${COST_PER_FRAME_PDF}",
            f"- **Total Frames:** {self.inventory['cost_estimation']['total_frames']}",
            f"- **Total Cost:** ${self.inventory['cost_estimation']['pdf_export']['total_cost']}",
            "",
            "### Combined PNG + PDF Export",
            f"- **Total Cost:** ${self.inventory['cost_estimation']['combined_export']['total_cost']}",
            "",
            "### Budget Status",
            f"- **Phase 1-2 Budget (November):** $50.00",
            f"- **Estimated Export Cost:** ${self.inventory['cost_estimation']['combined_export']['total_cost']}",
            f"- **Remaining Budget:** ${50.00 - self.inventory['cost_estimation']['combined_export']['total_cost']:.2f}",
            "",
            "---",
            "",
            "## 📁 File Inventory",
            ""
        ]

        # Add file details
        for idx, file_info in enumerate(self.inventory['files'], 1):
            report_lines.extend([
                f"### {idx}. {file_info['file_name']}",
                "",
                f"- **File Key:** `{file_info['file_key']}`",
                f"- **Last Modified:** {file_info.get('last_modified', 'Unknown')}",
                f"- **Version:** {file_info.get('version', 'Unknown')}",
                f"- **Pages:** {file_info['total_pages']}",
                f"- **Frames:** {file_info['total_frames']}",
                f"- **Components:** {file_info['total_components']}",
                ""
            ])

            # Export cost per file
            file_png_cost = file_info['total_frames'] * COST_PER_FRAME_PNG
            file_pdf_cost = file_info['total_frames'] * COST_PER_FRAME_PDF
            file_total_cost = file_png_cost + file_pdf_cost

            report_lines.extend([
                "**Export Costs:**",
                f"- PNG: ${file_png_cost:.2f}",
                f"- PDF: ${file_pdf_cost:.2f}",
                f"- Combined: ${file_total_cost:.2f}",
                ""
            ])

            # Page breakdown
            if file_info.get('pages'):
                report_lines.append("**Pages:**")
                for page in file_info['pages']:
                    report_lines.append(f"  - {page['page_name']}: {page['frame_count']} frames")
                report_lines.append("")

            report_lines.append("---")
            report_lines.append("")

        # Add recommendations
        report_lines.extend([
            "## 🎯 Wonder Woman: Prioritization Recommendations",
            "",
            "### High Priority Files (Q3 2025 - Latest)",
            "These files should be analyzed first as they represent the current design system.",
            "",
            "### Medium Priority Files (Q2 2025)",
            "Recent files that may contain updated patterns.",
            "",
            "### Low Priority Files (Q1 2024 and earlier)",
            "Legacy files - analyze only if needed for historical context.",
            "",
            "---",
            "",
            "## 📋 Next Steps (Phase 2)",
            "",
            "1. ✅ **Phase 1 Complete:** File inventory and cost estimation done",
            "2. ⏳ **Phase 2 (Week 3-4):** Design System Audit",
            "   - Extract color tokens from high-priority files",
            "   - Document typography system",
            "   - Analyze spacing patterns",
            "3. ⏳ **Phase 3 (Week 5-8):** Component Library Documentation",
            "",
            "---",
            "",
            f"**Generated by:** Justice League Mission Control",
            f"**Mission:** JL-003 Phase 1 Discovery & Cataloging",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ""
        ])

        return "\n".join(report_lines)

    def run_full_analysis(self) -> Dict[str, Any]:
        """🦸 Superman: Coordinate full project analysis"""
        print("\n" + "="*70)
        print("🦸 SUPERMAN: Initiating JL-003 Phase 1 Discovery Mission")
        print("="*70)

        # Step 1: Get all project files
        project_files = self.get_project_files()

        if not project_files:
            print("❌ No files found in project. Check project ID and permissions.")
            return self.inventory

        self.inventory['total_files'] = len(project_files)

        # Step 2: Analyze each file
        for file_info in project_files:
            file_key = file_info.get('key', '')
            file_name = file_info.get('name', 'Unnamed')

            if not file_key:
                continue

            analysis = self.analyze_file_structure(file_key, file_name)
            self.inventory['files'].append(analysis)

            # Update totals
            self.inventory['total_pages'] += analysis['total_pages']
            self.inventory['total_frames'] += analysis['total_frames']
            self.inventory['total_components'] += analysis['total_components']

        # Step 3: Calculate costs
        self.inventory['cost_estimation'] = self.calculate_export_costs()

        print("\n" + "="*70)
        print("✅ ANALYSIS COMPLETE")
        print("="*70)

        return self.inventory


def main():
    """Main execution"""
    print("\n🦸 Justice League JL-003 Phase 1: Figma Project Inventory")
    print("="*70)

    # Initialize analyzer
    analyzer = FigmaProjectAnalyzer(FIGMA_TOKEN)

    # Run analysis
    inventory = analyzer.run_full_analysis()

    # Generate report
    report = analyzer.generate_inventory_report()

    # Save outputs
    output_dir = '/Users/admin/Documents/claudecode/justice-league-missions/missions/JL-003-auzmor-learn-web-mobile'

    # Save JSON inventory
    json_path = os.path.join(output_dir, 'phase1-inventory.json')
    with open(json_path, 'w') as f:
        json.dump(inventory, f, indent=2)
    print(f"\n💾 Saved JSON inventory: {json_path}")

    # Save Markdown report
    md_path = os.path.join(output_dir, 'phase1-inventory.md')
    with open(md_path, 'w') as f:
        f.write(report)
    print(f"💾 Saved Markdown report: {md_path}")

    print("\n✅ JL-003 Phase 1 Discovery Complete!")
    print(f"📊 Total Files: {inventory['total_files']}")
    print(f"📄 Total Pages: {inventory['total_pages']}")
    print(f"🖼️  Total Frames: {inventory['total_frames']}")
    print(f"🧩 Total Components: {inventory['total_components']}")
    print(f"💰 Estimated Export Cost: ${inventory['cost_estimation']['combined_export']['total_cost']}")
    print(f"\n📄 Full report: {md_path}")


if __name__ == '__main__':
    main()
