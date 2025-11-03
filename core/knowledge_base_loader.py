"""
🧠 Knowledge Base Loader for Justice League

Provides heroes access to global best practices during analysis.
Each hero can query their specific domain knowledge.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Any
import json

class KnowledgeBaseLoader:
    """
    Load and query the Justice League global knowledge base.

    Heroes can reference best practices, checklists, and examples
    during their analysis.
    """

    def __init__(self, kb_path: Optional[str] = None):
        """
        Initialize knowledge base loader.

        Args:
            kb_path: Path to knowledge base directory
        """
        if kb_path is None:
            # Default to knowledge_base directory in project root
            project_root = Path(__file__).parent.parent
            kb_path = project_root / 'knowledge_base'

        self.kb_path = Path(kb_path)
        self.best_practices_file = self.kb_path / 'GLOBAL_BEST_PRACTICES.md'

        # Hero-specific knowledge sections
        self.hero_sections = {
            'litty': '🪔 Ethical Design (Litty)',
            'wonder_woman': '⚡ Accessibility (Wonder Woman)',
            'flash': '⚡ Performance (Flash)',
            'batman': '🦇 Interactive Elements (Batman)',
            'atom': '🔬 Component Design (Atom)',
            'plastic_man': '🤸 Responsive Design (Plastic Man)',
            'martian_manhunter': '🧠 Security (Martian Manhunter)',
            'zatanna': '🎩 SEO (Zatanna)',
            'aquaman': '🌊 Network Optimization (Aquaman)',
            'green_lantern': '💚 Visual Consistency (Green Lantern)',
            'green_arrow': '🏹 Testing (Green Arrow)',
            'cyborg': '🤖 Integrations (Cyborg)'
        }

    def get_hero_knowledge(self, hero_name: str) -> Dict[str, Any]:
        """
        Get knowledge base section for a specific hero.

        Args:
            hero_name: Hero identifier (e.g., 'litty', 'flash')

        Returns:
            Dict with hero's knowledge including:
            - best_practices: List of practices
            - checklist: Items to validate
            - examples: Code examples
        """
        hero_key = hero_name.lower().replace(' ', '_')

        if hero_key not in self.hero_sections:
            return {
                'error': f'Unknown hero: {hero_name}',
                'available_heroes': list(self.hero_sections.keys())
            }

        # Parse hero's section from markdown
        knowledge = self._parse_hero_section(hero_key)

        return knowledge

    def _parse_hero_section(self, hero_key: str) -> Dict[str, Any]:
        """Parse hero's section from GLOBAL_BEST_PRACTICES.md"""

        if not self.best_practices_file.exists():
            return {
                'error': 'Knowledge base not found',
                'path': str(self.best_practices_file)
            }

        # Read the markdown file
        with open(self.best_practices_file, 'r') as f:
            content = f.read()

        section_name = self.hero_sections[hero_key]

        # Extract hero's section
        section_start = f'## {section_name}'

        if section_start not in content:
            return {
                'error': f'Section not found: {section_name}'
            }

        # Find section boundaries
        start_idx = content.index(section_start)

        # Find next hero section (##) or end of file
        next_section_idx = content.find('\n## ', start_idx + len(section_start))
        if next_section_idx == -1:
            section_content = content[start_idx:]
        else:
            section_content = content[start_idx:next_section_idx]

        # Parse section
        knowledge = {
            'hero': hero_key,
            'section': section_name,
            'best_practices': self._extract_best_practices(section_content),
            'checklist': self._extract_checklist(section_content),
            'examples': self._extract_code_examples(section_content),
            'guidelines': self._extract_guidelines(section_content),
            'raw_content': section_content
        }

        return knowledge

    def _extract_best_practices(self, content: str) -> List[str]:
        """Extract ✅ DO and ❌ AVOID items"""
        practices = []

        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('✅') or line.strip().startswith('❌'):
                practices.append(line.strip())

        return practices

    def _extract_checklist(self, content: str) -> List[str]:
        """Extract checklist items (- [ ])"""
        checklist = []

        lines = content.split('\n')
        for line in lines:
            if '- [ ]' in line:
                # Clean up the checklist item
                item = line.replace('- [ ]', '').strip()
                if item:
                    checklist.append(item)

        return checklist

    def _extract_code_examples(self, content: str) -> List[Dict[str, str]]:
        """Extract code blocks"""
        examples = []

        in_code_block = False
        current_example = {'language': '', 'code': ''}

        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('```'):
                if not in_code_block:
                    # Start of code block
                    in_code_block = True
                    lang = line.strip().replace('```', '')
                    current_example = {'language': lang or 'text', 'code': ''}
                else:
                    # End of code block
                    in_code_block = False
                    if current_example['code'].strip():
                        examples.append(current_example)
                    current_example = {'language': '', 'code': ''}
            elif in_code_block:
                current_example['code'] += line + '\n'

        return examples

    def _extract_guidelines(self, content: str) -> List[str]:
        """Extract **Guidelines**: sections"""
        guidelines = []

        lines = content.split('\n')
        in_guidelines = False

        for line in lines:
            if '**Guidelines**' in line or '**Guidelines:**' in line:
                in_guidelines = True
                continue

            if in_guidelines:
                # Stop at next section or empty line
                if line.startswith('#') or (line.strip() == '' and len(guidelines) > 0):
                    in_guidelines = False
                elif line.strip().startswith('-'):
                    guidelines.append(line.strip())

        return guidelines

    def get_dark_patterns_list(self) -> List[Dict[str, str]]:
        """Get Litty's dark patterns list"""
        litty_knowledge = self.get_hero_knowledge('litty')

        # Parse dark patterns table from content
        dark_patterns = []

        if 'raw_content' in litty_knowledge:
            content = litty_knowledge['raw_content']

            # Find dark patterns table
            if '| Pattern |' in content:
                lines = content.split('\n')
                in_table = False

                for line in lines:
                    if '| Pattern |' in line:
                        in_table = True
                        continue

                    if in_table and line.startswith('|'):
                        # Skip separator line
                        if '---' in line:
                            continue

                        # Parse table row
                        parts = [p.strip() for p in line.split('|') if p.strip()]
                        if len(parts) >= 3:
                            # Remove bold markdown formatting from pattern name
                            pattern_name = parts[0].replace('**', '').strip()
                            dark_patterns.append({
                                'pattern': pattern_name,
                                'description': parts[1],
                                'example': parts[2]
                            })
                    elif in_table and not line.startswith('|'):
                        break

        return dark_patterns

    def get_wcag_guidelines(self) -> Dict[str, Any]:
        """Get Wonder Woman's WCAG guidelines"""
        ww_knowledge = self.get_hero_knowledge('wonder_woman')

        wcag = {
            'font_size': '16px minimum',
            'contrast': {
                'normal_text': '4.5:1',
                'large_text': '3:1',
                'ui_components': '3:1'
            },
            'keyboard': 'All interactive elements accessible',
            'aria': 'Proper ARIA attributes required',
            'alt_text': 'All images must have alt text or alt=""',
            'checklist': ww_knowledge.get('checklist', [])
        }

        return wcag

    def get_core_web_vitals(self) -> Dict[str, Dict[str, str]]:
        """Get Flash's Core Web Vitals targets"""
        flash_knowledge = self.get_hero_knowledge('flash')

        cwv = {
            'LCP': {
                'good': '≤2.5s',
                'needs_improvement': '2.5-4.0s',
                'poor': '>4.0s',
                'name': 'Largest Contentful Paint'
            },
            'FID': {
                'good': '≤100ms',
                'needs_improvement': '100-300ms',
                'poor': '>300ms',
                'name': 'First Input Delay'
            },
            'CLS': {
                'good': '≤0.1',
                'needs_improvement': '0.1-0.25',
                'poor': '>0.25',
                'name': 'Cumulative Layout Shift'
            },
            'INP': {
                'good': '≤200ms',
                'needs_improvement': '200-500ms',
                'poor': '>500ms',
                'name': 'Interaction to Next Paint'
            }
        }

        return cwv

    def get_minimum_standards(self) -> Dict[str, str]:
        """Get minimum pass/fail standards across all heroes"""
        return {
            'ethics': 'No dark patterns',
            'accessibility': 'WCAG 2.1 Level AA',
            'performance_lcp': 'LCP < 2.5s',
            'performance_fid': 'FID < 100ms',
            'performance_cls': 'CLS < 0.1',
            'font_size': '≥16px body text',
            'color_contrast': '4.5:1 (normal text)',
            'touch_targets': '≥44x44px',
            'security': 'HTTPS, no known vulnerabilities',
            'seo': 'Title, meta description, H1'
        }

    def validate_against_kb(self, hero_name: str, findings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate findings against knowledge base standards.

        Args:
            hero_name: Which hero is validating
            findings: Analysis results to validate

        Returns:
            Validation result with pass/fail and recommendations
        """
        hero_knowledge = self.get_hero_knowledge(hero_name)

        validation = {
            'hero': hero_name,
            'checklist_items': hero_knowledge.get('checklist', []),
            'items_checked': [],
            'items_failed': [],
            'recommendations': [],
            'score': 0
        }

        # Each hero can implement specific validation logic
        # For now, return structure for integration

        return validation

    def get_quick_reference(self) -> Dict[str, str]:
        """Get quick reference summary"""
        return {
            'litty': 'No dark patterns',
            'wonder_woman': 'WCAG 2.1 AA',
            'flash': 'LCP < 2.5s',
            'batman': 'All functional',
            'atom': 'Consistent',
            'plastic_man': 'Mobile-first',
            'martian_manhunter': 'OWASP Top 10',
            'zatanna': 'Meta tags complete',
            'aquaman': 'Compressed & cached',
            'green_lantern': 'Design tokens used',
            'green_arrow': '>80% coverage',
            'cyborg': 'API documented'
        }


# Singleton instance
_kb_loader = None

def get_knowledge_base() -> KnowledgeBaseLoader:
    """Get global knowledge base instance"""
    global _kb_loader

    if _kb_loader is None:
        _kb_loader = KnowledgeBaseLoader()

    return _kb_loader


# Convenience functions for heroes
def get_litty_knowledge() -> Dict[str, Any]:
    """Get Litty's ethical design knowledge"""
    return get_knowledge_base().get_hero_knowledge('litty')

def get_wonder_woman_knowledge() -> Dict[str, Any]:
    """Get Wonder Woman's accessibility knowledge"""
    return get_knowledge_base().get_hero_knowledge('wonder_woman')

def get_flash_knowledge() -> Dict[str, Any]:
    """Get Flash's performance knowledge"""
    return get_knowledge_base().get_hero_knowledge('flash')

def get_dark_patterns() -> List[Dict[str, str]]:
    """Get list of all 15 dark patterns"""
    return get_knowledge_base().get_dark_patterns_list()

def get_wcag_guidelines() -> Dict[str, Any]:
    """Get WCAG 2.1 AA guidelines"""
    return get_knowledge_base().get_wcag_guidelines()

def get_core_web_vitals() -> Dict[str, Dict[str, str]]:
    """Get Core Web Vitals targets"""
    return get_knowledge_base().get_core_web_vitals()
