#!/usr/bin/env python3
"""
JL-003 Phase 1 Deep Analysis: Individual File Analysis for Quicksilver Export
Oracle + Hawkman: Analyze each of the 182 Figma files for exact structure and export costs

This script:
1. Analyzes each file individually to count pages, frames, sections
2. Calculates PNG/PDF export costs per file
3. Generates comprehensive export plan with folder structure
4. Provides total cost estimation
"""

import os
import sys
import json
import requests
import time
from datetime import datetime
from typing import Dict, List, Any

# Figma API Configuration
FIGMA_TOKEN = os.getenv('FIGMA_ACCESS_TOKEN', 'figd_aPXrH3Rqpm8sdez_nHmmXKHvZ9vcK3sOcJwvhE7s')
FIGMA_API_BASE = 'https://api.figma.com/v1'

# Quicksilver Export Pricing
COST_PER_FRAME_PNG = 0.0025  # $0.0025 per frame
COST_PER_FRAME_PDF = 0.0030  # $0.0030 per frame

class DetailedFileAnalyzer:
    """Hawkman-powered detailed file analysis for Quicksilver export planning"""

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'X-Figma-Token': token,
            'Content-Type': 'application/json'
        }
        self.analysis_results = []
        self.total_pages = 0
        self.total_frames = 0
        self.total_sections = 0

    def analyze_file_structure(self, file_key: str, file_name: str, file_modified: str) -> Dict[str, Any]:
        """Analyze individual file structure in detail"""

        print(f"📊 Analyzing: {file_name[:60]}...")

        try:
            # Get file structure
            response = requests.get(
                f"{FIGMA_API_BASE}/files/{file_key}",
                headers=self.headers,
                timeout=30
            )

            if response.status_code != 200:
                print(f"   ❌ Error {response.status_code}: {response.text[:100]}")
                return {
                    'file_key': file_key,
                    'file_name': file_name,
                    'last_modified': file_modified,
                    'error': f"HTTP {response.status_code}",
                    'pages': 0,
                    'frames': 0,
                    'sections': 0,
                    'components': 0
                }

            data = response.json()
            document = data.get('document', {})
            pages = document.get('children', [])

            # Detailed page analysis
            page_details = []
            total_frames = 0
            total_sections = 0

            for page in pages:
                page_info = self._analyze_page_detailed(page)
                page_details.append(page_info)
                total_frames += page_info['frames']
                total_sections += page_info['sections']

            # Component count
            components_count = len(data.get('components', {}))

            # Build result
            result = {
                'file_key': file_key,
                'file_name': file_name,
                'last_modified': file_modified,
                'pages': len(pages),
                'frames': total_frames,
                'sections': total_sections,
                'components': components_count,
                'page_details': page_details,
                'png_cost': round(total_frames * COST_PER_FRAME_PNG, 2),
                'pdf_cost': round(total_frames * COST_PER_FRAME_PDF, 2),
                'total_cost': round(total_frames * (COST_PER_FRAME_PNG + COST_PER_FRAME_PDF), 2),
                'export_folder': self._generate_folder_name(file_name)
            }

            print(f"   ✅ Pages: {len(pages)}, Frames: {total_frames}, Sections: {total_sections}, Cost: ${result['total_cost']}")

            return result

        except requests.exceptions.Timeout:
            print(f"   ⏱️  Timeout - file too large or slow response")
            return {
                'file_key': file_key,
                'file_name': file_name,
                'last_modified': file_modified,
                'error': 'Timeout',
                'pages': 0,
                'frames': 0,
                'sections': 0,
                'components': 0
            }
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}")
            return {
                'file_key': file_key,
                'file_name': file_name,
                'last_modified': file_modified,
                'error': str(e)[:200],
                'pages': 0,
                'frames': 0,
                'sections': 0,
                'components': 0
            }

    def _analyze_page_detailed(self, page_node: Dict[str, Any]) -> Dict[str, Any]:
        """Detailed page analysis with frame and section counting"""

        page_info = {
            'page_name': page_node.get('name', 'Unnamed'),
            'page_id': page_node.get('id', ''),
            'frames': 0,
            'sections': 0,
            'frame_list': []
        }

        # Analyze all children
        children = page_node.get('children', [])

        for child in children:
            child_type = child.get('type', '')

            # Count frames
            if child_type == 'FRAME':
                page_info['frames'] += 1
                page_info['frame_list'].append({
                    'name': child.get('name', 'Unnamed'),
                    'id': child.get('id', ''),
                    'width': child.get('absoluteBoundingBox', {}).get('width', 0),
                    'height': child.get('absoluteBoundingBox', {}).get('height', 0)
                })

            # Count sections
            elif child_type == 'SECTION':
                page_info['sections'] += 1
                # Sections can contain frames, recurse
                section_frames = self._count_frames_in_node(child)
                page_info['frames'] += section_frames

        return page_info

    def _count_frames_in_node(self, node: Dict[str, Any]) -> int:
        """Recursively count frames within a node (e.g., sections)"""
        count = 0

        if node.get('type') == 'FRAME':
            count = 1

        for child in node.get('children', []):
            count += self._count_frames_in_node(child)

        return count

    def _generate_folder_name(self, file_name: str) -> str:
        """Generate safe folder name for export"""
        # Remove special characters, replace spaces with hyphens
        safe_name = file_name.replace('/', '-').replace('\\', '-')
        safe_name = safe_name.replace('|', '-').replace(':', '-')
        safe_name = safe_name.replace('?', '').replace('*', '')
        safe_name = safe_name.replace('"', '').replace('<', '').replace('>', '')
        safe_name = safe_name.strip()

        # Limit length
        if len(safe_name) > 100:
            safe_name = safe_name[:100]

        return safe_name

    def analyze_all_files(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze all files with progress tracking"""

        total_files = len(files)
        print(f"\n🦅 Hawkman: Starting detailed analysis of {total_files} files...")
        print(f"⏱️  Estimated time: ~{total_files * 2} seconds (with rate limiting)")
        print()

        for idx, file_info in enumerate(files, 1):
            print(f"[{idx}/{total_files}] ", end='')

            result = self.analyze_file_structure(
                file_info['key'],
                file_info['name'],
                file_info.get('last_modified', 'Unknown')
            )

            self.analysis_results.append(result)

            # Update totals
            self.total_pages += result.get('pages', 0)
            self.total_frames += result.get('frames', 0)
            self.total_sections += result.get('sections', 0)

            # Rate limiting: 1 request per second to be safe
            if idx < total_files:
                time.sleep(1.2)

        print()
        print("="*80)
        print("✅ Analysis Complete!")
        print(f"📊 Total Pages: {self.total_pages}")
        print(f"🖼️  Total Frames: {self.total_frames}")
        print(f"📁 Total Sections: {self.total_sections}")
        print("="*80)

        return self.analysis_results

    def generate_cost_report(self) -> str:
        """Generate comprehensive cost report"""

        total_png_cost = sum(r.get('png_cost', 0) for r in self.analysis_results)
        total_pdf_cost = sum(r.get('pdf_cost', 0) for r in self.analysis_results)
        total_combined_cost = sum(r.get('total_cost', 0) for r in self.analysis_results)

        # Sort files by cost (highest first)
        sorted_by_cost = sorted(
            self.analysis_results,
            key=lambda x: x.get('total_cost', 0),
            reverse=True
        )

        report = f"""# JL-003 Detailed File Analysis & Export Cost Report

**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Analyzed By:** Oracle (Coordinator) + Hawkman (Figma Analysis)
**Total Files Analyzed:** {len(self.analysis_results)}

---

## 📊 Executive Summary

### Project Totals
- **Total Pages:** {self.total_pages:,}
- **Total Frames:** {self.total_frames:,}
- **Total Sections:** {self.total_sections}

### Export Costs
- **PNG Export:** ${total_png_cost:.2f} ({self.total_frames:,} frames × ${COST_PER_FRAME_PNG})
- **PDF Export:** ${total_pdf_cost:.2f} ({self.total_frames:,} frames × ${COST_PER_FRAME_PDF})
- **Combined PNG + PDF:** ${total_combined_cost:.2f}

---

## 💰 Top 20 Most Expensive Files (by export cost)

"""

        for idx, file_data in enumerate(sorted_by_cost[:20], 1):
            report += f"""
### {idx}. {file_data['file_name']}
- **File Key:** `{file_data['file_key']}`
- **Last Modified:** {file_data.get('last_modified', 'Unknown')[:10]}
- **Structure:** {file_data.get('pages', 0)} pages, {file_data.get('frames', 0)} frames, {file_data.get('sections', 0)} sections
- **Components:** {file_data.get('components', 0)}
- **Export Cost:** ${file_data.get('total_cost', 0):.2f} (PNG: ${file_data.get('png_cost', 0):.2f}, PDF: ${file_data.get('pdf_cost', 0):.2f})
- **Export Folder:** `{file_data.get('export_folder', 'N/A')}/`
"""

        report += """

---

## 📁 Complete File-by-File Breakdown

"""

        # Group by year
        files_by_year = {}
        for file_data in self.analysis_results:
            year = file_data.get('last_modified', 'Unknown')[:4]
            if year not in files_by_year:
                files_by_year[year] = []
            files_by_year[year].append(file_data)

        for year in sorted(files_by_year.keys(), reverse=True):
            files = files_by_year[year]
            year_frames = sum(f.get('frames', 0) for f in files)
            year_cost = sum(f.get('total_cost', 0) for f in files)

            report += f"""
### {year} Files ({len(files)} files, {year_frames} frames, ${year_cost:.2f} total cost)

| File Name | Pages | Frames | Sections | Cost | Export Folder |
|-----------|-------|--------|----------|------|---------------|
"""

            for file_data in sorted(files, key=lambda x: x.get('last_modified', ''), reverse=True):
                name_short = file_data['file_name'][:50] + ('...' if len(file_data['file_name']) > 50 else '')
                report += f"| {name_short} | {file_data.get('pages', 0)} | {file_data.get('frames', 0)} | {file_data.get('sections', 0)} | ${file_data.get('total_cost', 0):.2f} | `{file_data.get('export_folder', 'N/A')}/` |\n"

            report += "\n"

        report += f"""
---

## 🎯 Quicksilver Export Strategy

### Recommended Phased Approach

**Phase 1: High-Value Files** (Top 20 by frame count)
- Files: 20
- Estimated Frames: ~{sum(sorted_by_cost[i].get('frames', 0) for i in range(min(20, len(sorted_by_cost))))}
- Estimated Cost: ~${sum(sorted_by_cost[i].get('total_cost', 0) for i in range(min(20, len(sorted_by_cost)))):.2f}
- Timeline: 1-2 days

**Phase 2: Recent Files** (2024-2025)
- Files: {len([f for f in self.analysis_results if f.get('last_modified', '').startswith(('2024', '2025'))])}
- Estimated Frames: {sum(f.get('frames', 0) for f in self.analysis_results if f.get('last_modified', '').startswith(('2024', '2025')))}
- Estimated Cost: ${sum(f.get('total_cost', 0) for f in self.analysis_results if f.get('last_modified', '').startswith(('2024', '2025'))):.2f}
- Timeline: 3-5 days

**Phase 3: Complete Project** (All 182 files)
- Files: {len(self.analysis_results)}
- Estimated Frames: {self.total_frames:,}
- Estimated Cost: ${total_combined_cost:.2f}
- Timeline: 7-10 days

### Quicksilver Export Command Template

```bash
# Export single file
python3 export_figma_png.py <FILE_KEY> --output exports/<EXPORT_FOLDER>/ --scale 2

# Example for top file:
python3 export_figma_png.py {sorted_by_cost[0]['file_key']} --output exports/{sorted_by_cost[0].get('export_folder', 'file-1')}/ --scale 2
```

---

**Generated by:** Justice League Mission Control
**Mission:** JL-003 Phase 1 Detailed File Analysis
**Total Analysis Time:** ~{len(self.analysis_results) * 1.2:.0f} seconds
"""

        return report


def main():
    """Main execution"""

    print("\n" + "="*80)
    print("🔮 ORACLE + 🦅 HAWKMAN: JL-003 Detailed File Analysis")
    print("="*80)
    print()

    # Load file list
    print("📂 Loading file list from Phase 1 inventory...")
    with open('phase1-files-list.json', 'r') as f:
        data = json.load(f)

    files = data['files']
    print(f"✅ Loaded {len(files)} files")
    print()

    # Initialize analyzer
    analyzer = DetailedFileAnalyzer(FIGMA_TOKEN)

    # Analyze all files
    results = analyzer.analyze_all_files(files)

    # Generate report
    print("\n📝 Generating comprehensive cost report...")
    report = analyzer.generate_cost_report()

    # Save outputs
    print("\n💾 Saving results...")

    # Save JSON
    json_output = {
        'analysis_date': datetime.now().isoformat(),
        'total_files': len(results),
        'total_pages': analyzer.total_pages,
        'total_frames': analyzer.total_frames,
        'total_sections': analyzer.total_sections,
        'total_png_cost': sum(r.get('png_cost', 0) for r in results),
        'total_pdf_cost': sum(r.get('pdf_cost', 0) for r in results),
        'total_combined_cost': sum(r.get('total_cost', 0) for r in results),
        'files': results
    }

    with open('detailed-analysis.json', 'w') as f:
        json.dump(json_output, f, indent=2)
    print(f"   ✅ JSON: detailed-analysis.json")

    # Save markdown report
    with open('detailed-analysis-report.md', 'w') as f:
        f.write(report)
    print(f"   ✅ Markdown Report: detailed-analysis-report.md")

    print()
    print("="*80)
    print("✅ DETAILED ANALYSIS COMPLETE")
    print("="*80)
    print(f"📊 Total Frames: {analyzer.total_frames:,}")
    print(f"💰 Total Cost: ${sum(r.get('total_cost', 0) for r in results):.2f}")
    print()
    print("📄 Review the detailed report: detailed-analysis-report.md")
    print("="*80)


if __name__ == '__main__':
    main()
