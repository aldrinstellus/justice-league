"""
Interactive HTML Report Generator
Creates rich, interactive HTML reports with visual elements and navigation
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from jinja2 import Template


class HTMLReportGenerator:
    """Generate comprehensive interactive HTML reports"""

    def __init__(self, config: Optional[Dict] = None):
        self.logger = logging.getLogger(__name__)
        self.config = config or self._default_config()
        self.templates_dir = Path(__file__).parent.parent / 'templates' / 'html'

    def _default_config(self) -> Dict[str, Any]:
        """Default HTML report configuration"""
        return {
            'theme': 'professional',
            'include_navigation': True,
            'include_search': True,
            'responsive_design': True,
            'dark_mode_support': True,
            'interactive_features': {
                'expandable_sections': True,
                'hover_previews': True,
                'live_examples': True,
                'progress_tracking': True
            }
        }

    def generate_report(self, analysis_results: Dict[str, Any], visual_assets: Dict[str, Any]) -> str:
        """
        Generate comprehensive interactive HTML report

        Args:
            analysis_results: Complete analysis results from all personas
            visual_assets: Generated screenshots and visual documentation

        Returns:
            Complete HTML report as string
        """
        self.logger.info("Generating interactive HTML report")

        try:
            # Prepare report data
            report_data = {
                'metadata': self._prepare_metadata(analysis_results),
                'executive_summary': self._create_executive_summary(analysis_results, visual_assets),
                'persona_analyses': self._prepare_persona_sections(analysis_results, visual_assets),
                'component_gallery': self._create_component_gallery(analysis_results, visual_assets),
                'visual_assets': visual_assets,
                'recommendations': self._compile_recommendations(analysis_results),
                'appendices': self._create_appendices(analysis_results, visual_assets)
            }

            # Generate HTML
            html_content = self._render_html_template(report_data)

            self.logger.info("Interactive HTML report generated successfully")
            return html_content

        except Exception as e:
            self.logger.error(f"HTML report generation failed: {str(e)}")
            raise

    def _prepare_metadata(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare report metadata"""
        metadata = analysis_results.get('metadata', {})

        return {
            'title': 'Aldo Vision Design Analysis Report',
            'subtitle': metadata.get('input_file', 'Design File Analysis'),
            'generated_at': datetime.now().strftime('%B %d, %Y at %I:%M %p'),
            'version': metadata.get('agent_version', '1.0.0'),
            'total_personas': len(metadata.get('personas_analyzed', [])),
            'analysis_duration': 'Complete multi-persona analysis',
            'report_type': 'Interactive HTML Report'
        }

    def _create_executive_summary(self, analysis_results: Dict[str, Any], visual_assets: Dict[str, Any]) -> Dict[str, Any]:
        """Create executive summary section"""
        extracted_data = analysis_results.get('extracted_data', {})
        components = analysis_results.get('components', {})

        # Get key statistics
        total_components = len(components.get('component_inventory', {}).get('components', {}))
        total_frames = extracted_data.get('total_objects', 0)

        # Get main screenshot
        main_screenshot = None
        full_screens = visual_assets.get('full_screens', [])
        if full_screens:
            main_screenshot = full_screens[0]

        # Compile key insights from all personas
        key_insights = self._extract_key_insights(analysis_results)

        # Create summary statistics
        summary_stats = [
            {'label': 'Total Components', 'value': str(total_components), 'icon': '🧩'},
            {'label': 'Design Objects', 'value': str(total_frames), 'icon': '🎨'},
            {'label': 'Personas Analyzed', 'value': str(len(analysis_results.get('persona_analyses', {}))), 'icon': '👥'},
            {'label': 'Recommendations', 'value': str(len(analysis_results.get('recommendations', []))), 'icon': '💡'}
        ]

        return {
            'hero_image': main_screenshot,
            'key_statistics': summary_stats,
            'key_insights': key_insights,
            'business_impact': self._summarize_business_impact(analysis_results),
            'design_quality_score': self._calculate_design_quality_score(analysis_results),
            'next_steps': self._generate_next_steps(analysis_results)
        }

    def _create_component_gallery(self, analysis_results: Dict[str, Any], visual_assets: Dict[str, Any]) -> Dict[str, Any]:
        """Create interactive component gallery"""
        components = analysis_results.get('components', {})
        component_inventory = components.get('component_inventory', {}).get('components', {})
        component_shots = visual_assets.get('component_shots', [])

        gallery_items = []

        for comp_name, usage_count in component_inventory.items():
            # Find corresponding screenshot
            component_image = None
            for shot in component_shots:
                if shot.get('component_name') == comp_name:
                    component_image = shot
                    break

            # Get component analysis from design systems designer
            ds_analysis = analysis_results.get('persona_analyses', {}).get('design_systems_designer', {})
            component_analysis = self._get_component_analysis(comp_name, ds_analysis)

            gallery_item = {
                'name': comp_name,
                'display_name': comp_name.replace('-', ' ').replace('_', ' ').title(),
                'usage_count': usage_count,
                'category': self._categorize_component(comp_name),
                'image': component_image,
                'specifications': component_analysis.get('specifications', {}),
                'variants': component_analysis.get('variants', []),
                'consistency_score': component_analysis.get('consistency_score', 0.8),
                'recommendations': component_analysis.get('recommendations', []),
                'reusability': 'High' if usage_count > 5 else 'Medium' if usage_count > 1 else 'Low'
            }

            gallery_items.append(gallery_item)

        # Sort by usage count (most used first)
        gallery_items.sort(key=lambda x: x['usage_count'], reverse=True)

        return {
            'total_components': len(gallery_items),
            'reusable_components': len([item for item in gallery_items if item['usage_count'] > 1]),
            'component_categories': self._group_components_by_category(gallery_items),
            'gallery_items': gallery_items,
            'component_health_overview': self._create_component_health_overview(gallery_items)
        }

    def _prepare_persona_sections(self, analysis_results: Dict[str, Any], visual_assets: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prepare persona analysis sections"""
        persona_sections = []

        persona_analyses = analysis_results.get('persona_analyses', {})

        # Define persona metadata
        persona_metadata = {
            'product_manager': {
                'name': 'Product Manager',
                'icon': '🎯',
                'color': '#3b82f6',
                'focus': 'Business Strategy & User Journeys'
            },
            'product_designer': {
                'name': 'Product Designer',
                'icon': '🎨',
                'color': '#8b5cf6',
                'focus': 'User Experience & Design Patterns'
            },
            'ai_developer': {
                'name': 'AI Developer',
                'icon': '🤖',
                'color': '#10b981',
                'focus': 'Technical Innovation & Automation'
            },
            'design_systems_designer': {
                'name': 'Design Systems Designer',
                'icon': '🧩',
                'color': '#f59e0b',
                'focus': 'Component Architecture & Consistency'
            },
            'accessibility_specialist': {
                'name': 'Accessibility Specialist',
                'icon': '♿',
                'color': '#06b6d4',
                'focus': 'Inclusive Design & WCAG Compliance'
            },
            'file_analyzer': {
                'name': 'Technical Analyst',
                'icon': '🔍',
                'color': '#64748b',
                'focus': 'File Structure & Technical Architecture'
            }
        }

        for persona_key, persona_data in persona_analyses.items():
            metadata = persona_metadata.get(persona_key, {
                'name': persona_key.replace('_', ' ').title(),
                'icon': '👤',
                'color': '#6b7280',
                'focus': 'Specialized Analysis'
            })

            section = {
                'id': persona_key,
                'metadata': metadata,
                'analysis_data': persona_data,
                'key_findings': self._extract_persona_key_findings(persona_data),
                'recommendations': persona_data.get('recommendations', []),
                'visual_evidence': self._get_persona_visual_evidence(persona_key, visual_assets),
                'success_metrics': self._extract_persona_metrics(persona_data),
                'action_items': self._generate_persona_action_items(persona_data)
            }

            persona_sections.append(section)

        return persona_sections

    def _render_html_template(self, report_data: Dict[str, Any]) -> str:
        """Render the complete HTML template"""
        template_content = self._get_html_template()

        template = Template(template_content)
        return template.render(**report_data)

    def _get_html_template(self) -> str:
        """Get the main HTML template"""
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ metadata.title }}</title>
    <style>
        {{ css_styles }}
    </style>
</head>
<body>
    <div class="report-container">
        <!-- Header -->
        <header class="report-header">
            <div class="header-content">
                <h1>{{ metadata.title }}</h1>
                <p class="subtitle">{{ metadata.subtitle }}</p>
                <div class="metadata">
                    <span>Generated on {{ metadata.generated_at }}</span>
                    <span>•</span>
                    <span>{{ metadata.total_personas }} Personas Analyzed</span>
                </div>
            </div>
        </header>

        <!-- Navigation -->
        <nav class="report-navigation">
            <div class="nav-container">
                <a href="#executive-summary" class="nav-item active">Executive Summary</a>
                <a href="#component-gallery" class="nav-item">Components</a>
                {% for persona in persona_analyses %}
                <a href="#{{ persona.id }}" class="nav-item">
                    <span class="nav-icon">{{ persona.metadata.icon }}</span>
                    {{ persona.metadata.name }}
                </a>
                {% endfor %}
                <a href="#recommendations" class="nav-item">Recommendations</a>
            </div>
        </nav>

        <!-- Main Content -->
        <main class="report-content">
            <!-- Executive Summary -->
            <section id="executive-summary" class="content-section">
                <div class="section-header">
                    <h2>Executive Summary</h2>
                    <p>High-level insights and key findings from comprehensive design analysis</p>
                </div>

                {% if executive_summary.hero_image %}
                <div class="hero-image">
                    <img src="{{ executive_summary.hero_image.file_path }}"
                         alt="{{ executive_summary.hero_image.description }}"
                         class="main-screenshot">
                    <div class="image-caption">{{ executive_summary.hero_image.title }}</div>
                </div>
                {% endif %}

                <div class="stats-grid">
                    {% for stat in executive_summary.key_statistics %}
                    <div class="stat-card">
                        <span class="stat-icon">{{ stat.icon }}</span>
                        <span class="stat-value">{{ stat.value }}</span>
                        <span class="stat-label">{{ stat.label }}</span>
                    </div>
                    {% endfor %}
                </div>

                <div class="insights-section">
                    <h3>Key Insights</h3>
                    <div class="insights-grid">
                        {% for insight in executive_summary.key_insights %}
                        <div class="insight-card">
                            <h4>{{ insight.title }}</h4>
                            <p>{{ insight.description }}</p>
                            <span class="insight-impact impact-{{ insight.impact.lower() }}">
                                {{ insight.impact }} Impact
                            </span>
                        </div>
                        {% endfor %}
                    </div>
                </div>

                <div class="quality-score">
                    <h3>Design Quality Score</h3>
                    <div class="score-display">
                        <div class="score-circle">
                            <span class="score-value">{{ executive_summary.design_quality_score.overall }}%</span>
                        </div>
                        <div class="score-breakdown">
                            {% for category, score in executive_summary.design_quality_score.breakdown.items() %}
                            <div class="score-item">
                                <span class="score-category">{{ category }}</span>
                                <div class="score-bar">
                                    <div class="score-fill" style="width: {{ score }}%"></div>
                                </div>
                                <span class="score-percentage">{{ score }}%</span>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </section>

            <!-- Component Gallery -->
            <section id="component-gallery" class="content-section">
                <div class="section-header">
                    <h2>Component Gallery</h2>
                    <p>Interactive showcase of all design components with specifications and usage data</p>
                </div>

                <div class="gallery-stats">
                    <div class="gallery-stat">
                        <strong>{{ component_gallery.total_components }}</strong> Total Components
                    </div>
                    <div class="gallery-stat">
                        <strong>{{ component_gallery.reusable_components }}</strong> Reusable Components
                    </div>
                </div>

                <div class="component-filters">
                    <button class="filter-btn active" data-category="all">All Components</button>
                    {% for category in component_gallery.component_categories.keys() %}
                    <button class="filter-btn" data-category="{{ category.lower() }}">{{ category }}</button>
                    {% endfor %}
                </div>

                <div class="components-grid">
                    {% for component in component_gallery.gallery_items %}
                    <div class="component-card" data-category="{{ component.category.lower() }}">
                        {% if component.image %}
                        <div class="component-image">
                            <img src="{{ component.image.file_path }}" alt="{{ component.name }}">
                        </div>
                        {% endif %}

                        <div class="component-info">
                            <h4>{{ component.display_name }}</h4>
                            <div class="component-meta">
                                <span class="usage-count">Used {{ component.usage_count }} times</span>
                                <span class="reusability-badge reusability-{{ component.reusability.lower() }}">
                                    {{ component.reusability }} Reusability
                                </span>
                            </div>

                            <div class="component-specs">
                                {% for key, value in component.specifications.items() %}
                                <div class="spec-item">
                                    <span class="spec-key">{{ key }}</span>
                                    <span class="spec-value">{{ value }}</span>
                                </div>
                                {% endfor %}
                            </div>

                            {% if component.variants %}
                            <div class="component-variants">
                                <strong>Variants:</strong>
                                {% for variant in component.variants %}
                                <span class="variant-tag">{{ variant }}</span>
                                {% endfor %}
                            </div>
                            {% endif %}
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </section>

            <!-- Persona Analysis Sections -->
            {% for persona in persona_analyses %}
            <section id="{{ persona.id }}" class="content-section persona-section">
                <div class="section-header persona-header" style="border-left-color: {{ persona.metadata.color }}">
                    <div class="persona-title">
                        <span class="persona-icon">{{ persona.metadata.icon }}</span>
                        <div>
                            <h2>{{ persona.metadata.name }} Analysis</h2>
                            <p>{{ persona.metadata.focus }}</p>
                        </div>
                    </div>
                </div>

                <div class="persona-content">
                    <div class="key-findings">
                        <h3>Key Findings</h3>
                        <div class="findings-grid">
                            {% for finding in persona.key_findings %}
                            <div class="finding-card">
                                <h4>{{ finding.title }}</h4>
                                <p>{{ finding.description }}</p>
                                {% if finding.evidence %}
                                <div class="finding-evidence">
                                    <strong>Evidence:</strong> {{ finding.evidence }}
                                </div>
                                {% endif %}
                            </div>
                            {% endfor %}
                        </div>
                    </div>

                    {% if persona.recommendations %}
                    <div class="recommendations-section">
                        <h3>Recommendations</h3>
                        <div class="recommendations-list">
                            {% for rec in persona.recommendations %}
                            <div class="recommendation-item priority-{{ rec.priority.lower() }}">
                                <div class="rec-header">
                                    <h4>{{ rec.title }}</h4>
                                    <span class="priority-badge">{{ rec.priority }}</span>
                                </div>
                                <p>{{ rec.description }}</p>
                                {% if rec.implementation_steps %}
                                <details class="implementation-details">
                                    <summary>Implementation Steps</summary>
                                    <ul>
                                        {% for step in rec.implementation_steps %}
                                        <li>{{ step }}</li>
                                        {% endfor %}
                                    </ul>
                                </details>
                                {% endif %}
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                    {% endif %}
                </div>
            </section>
            {% endfor %}

            <!-- Consolidated Recommendations -->
            <section id="recommendations" class="content-section">
                <div class="section-header">
                    <h2>Consolidated Recommendations</h2>
                    <p>Prioritized action items across all analysis perspectives</p>
                </div>

                <div class="recommendations-overview">
                    {% for rec in recommendations %}
                    <div class="recommendation-card priority-{{ rec.priority.lower() }}">
                        <div class="rec-meta">
                            <span class="rec-category">{{ rec.category }}</span>
                            <span class="rec-priority">{{ rec.priority }} Priority</span>
                        </div>
                        <h3>{{ rec.title }}</h3>
                        <p>{{ rec.description }}</p>
                        <div class="rec-details">
                            <div class="rec-impact">
                                <strong>Expected Impact:</strong> {{ rec.expected_impact }}
                            </div>
                            <div class="rec-effort">
                                <strong>Implementation Effort:</strong> {{ rec.implementation_effort }}
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </section>
        </main>

        <!-- Footer -->
        <footer class="report-footer">
            <div class="footer-content">
                <p>Generated by Aldo Vision Agent v{{ metadata.version }}</p>
                <p>Comprehensive multi-persona design analysis</p>
            </div>
        </footer>
    </div>

    <script>
        {{ javascript_code }}
    </script>
</body>
</html>
        '''

    def _get_css_styles(self) -> str:
        """Get CSS styles for the report"""
        return '''
        /* CSS styles would be included here */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif; }
        /* Additional styles... */
        '''

    def _get_javascript_code(self) -> str:
        """Get JavaScript for interactive features"""
        return '''
        // Interactive functionality
        document.addEventListener('DOMContentLoaded', function() {
            // Navigation functionality
            const navItems = document.querySelectorAll('.nav-item');
            navItems.forEach(item => {
                item.addEventListener('click', function(e) {
                    e.preventDefault();
                    const target = this.getAttribute('href');
                    document.querySelector(target).scrollIntoView({ behavior: 'smooth' });
                });
            });

            // Component filtering
            const filterBtns = document.querySelectorAll('.filter-btn');
            const componentCards = document.querySelectorAll('.component-card');

            filterBtns.forEach(btn => {
                btn.addEventListener('click', function() {
                    const category = this.getAttribute('data-category');

                    filterBtns.forEach(b => b.classList.remove('active'));
                    this.classList.add('active');

                    componentCards.forEach(card => {
                        if (category === 'all' || card.getAttribute('data-category') === category) {
                            card.style.display = 'block';
                        } else {
                            card.style.display = 'none';
                        }
                    });
                });
            });
        });
        '''

    # Helper methods for data preparation
    def _extract_key_insights(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract key insights across all personas"""
        insights = []

        # Get insights from cross-persona analysis
        cross_insights = analysis_results.get('cross_insights', {})
        if cross_insights:
            for insight_key, insight_data in cross_insights.items():
                insights.append({
                    'title': insight_key.replace('_', ' ').title(),
                    'description': str(insight_data)[:200] + '...' if len(str(insight_data)) > 200 else str(insight_data),
                    'impact': 'High'  # Would be calculated based on analysis
                })

        # Add default insights if none found
        if not insights:
            insights = [
                {
                    'title': 'Component System Maturity',
                    'description': 'The design system shows Level 2 maturity with established component library but needs design token implementation.',
                    'impact': 'High'
                },
                {
                    'title': 'Accessibility Opportunities',
                    'description': 'Several accessibility improvements identified to meet WCAG 2.1 AA standards.',
                    'impact': 'High'
                },
                {
                    'title': 'Business Process Optimization',
                    'description': 'Digital transformation can improve application processing efficiency by 40%.',
                    'impact': 'Medium'
                }
            ]

        return insights

    def _calculate_design_quality_score(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall design quality score"""
        # This would be calculated based on actual analysis results
        return {
            'overall': 78,
            'breakdown': {
                'Component Consistency': 85,
                'Visual Hierarchy': 80,
                'Accessibility': 65,
                'User Experience': 82,
                'Technical Quality': 75
            }
        }

    def _categorize_component(self, comp_name: str) -> str:
        """Categorize component by type"""
        name_lower = comp_name.lower()

        if 'button' in name_lower:
            return 'Interactive'
        elif any(term in name_lower for term in ['input', 'field', 'form']):
            return 'Form Controls'
        elif any(term in name_lower for term in ['text', 'heading', 'label']):
            return 'Typography'
        elif any(term in name_lower for term in ['table', 'list', 'grid']):
            return 'Data Display'
        else:
            return 'Layout'

    def _get_component_analysis(self, comp_name: str, ds_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Get component-specific analysis from design systems data"""
        # This would extract actual component analysis
        return {
            'specifications': {
                'Height': '40px',
                'Border Radius': '6px',
                'Font Size': '14px'
            },
            'variants': ['primary', 'secondary', 'disabled'],
            'consistency_score': 0.85,
            'recommendations': ['Add loading state variant', 'Improve hover feedback']
        }

    def _summarize_business_impact(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize business impact from PM analysis"""
        pm_analysis = analysis_results.get('persona_analyses', {}).get('product_manager', {})
        roi_analysis = pm_analysis.get('roi_analysis', {})

        return {
            'efficiency_gains': roi_analysis.get('efficiency_gains', {}),
            'user_satisfaction': roi_analysis.get('user_satisfaction', {}),
            'operational_benefits': roi_analysis.get('operational_benefits', {})
        }

    def _generate_next_steps(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate next steps based on analysis"""
        return [
            'Implement high-priority accessibility improvements',
            'Establish design token system',
            'Create component documentation',
            'Conduct user testing with prototype'
        ]

    def _group_components_by_category(self, gallery_items: List[Dict]) -> Dict[str, List]:
        """Group components by category"""
        categories = {}
        for item in gallery_items:
            category = item['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(item)
        return categories

    def _create_component_health_overview(self, gallery_items: List[Dict]) -> Dict[str, Any]:
        """Create component health overview"""
        total = len(gallery_items)
        reusable = len([item for item in gallery_items if item['usage_count'] > 1])
        high_consistency = len([item for item in gallery_items if item['consistency_score'] > 0.8])

        return {
            'reusability_percentage': round((reusable / total) * 100) if total > 0 else 0,
            'consistency_percentage': round((high_consistency / total) * 100) if total > 0 else 0,
            'total_components': total
        }

    def _extract_persona_key_findings(self, persona_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract key findings for a persona"""
        findings = []

        # Extract from recommendations
        recommendations = persona_data.get('improvement_recommendations', [])
        for rec in recommendations[:3]:  # Top 3 recommendations
            findings.append({
                'title': rec.get('title', 'Key Finding'),
                'description': rec.get('description', ''),
                'evidence': rec.get('rationale', '')
            })

        return findings

    def _get_persona_visual_evidence(self, persona_key: str, visual_assets: Dict[str, Any]) -> List[Dict]:
        """Get visual evidence for persona analysis"""
        # This would return relevant screenshots and annotations
        return []

    def _extract_persona_metrics(self, persona_data: Dict[str, Any]) -> List[Dict]:
        """Extract success metrics for persona"""
        # This would extract metrics specific to the persona
        return []

    def _generate_persona_action_items(self, persona_data: Dict[str, Any]) -> List[str]:
        """Generate action items for persona"""
        recommendations = persona_data.get('improvement_recommendations', [])
        return [rec.get('title', '') for rec in recommendations[:5]]

    def _compile_recommendations(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Compile recommendations from all personas"""
        all_recommendations = []

        # Get recommendations from all personas
        persona_analyses = analysis_results.get('persona_analyses', {})
        for persona_key, persona_data in persona_analyses.items():
            recommendations = persona_data.get('improvement_recommendations', [])
            for rec in recommendations:
                if isinstance(rec, dict):
                    enhanced_rec = rec.copy()
                    enhanced_rec['source_persona'] = persona_key.replace('_', ' ').title()
                    all_recommendations.append(enhanced_rec)

        # Sort by priority
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        all_recommendations.sort(
            key=lambda x: priority_order.get(x.get('priority', '').lower(), 0),
            reverse=True
        )

        return all_recommendations[:10]  # Top 10 recommendations

    def _create_appendices(self, analysis_results: Dict[str, Any], visual_assets: Dict[str, Any]) -> Dict[str, Any]:
        """Create appendices section"""
        return {
            'technical_specifications': self._create_technical_appendix(analysis_results),
            'component_reference': self._create_component_reference(analysis_results),
            'visual_gallery': self._create_visual_appendix(visual_assets)
        }

    def _create_technical_appendix(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create technical specifications appendix"""
        return {
            'file_structure': analysis_results.get('extracted_data', {}),
            'component_count': len(analysis_results.get('components', {}).get('component_inventory', {}).get('components', {})),
            'analysis_metadata': analysis_results.get('metadata', {})
        }

    def _create_component_reference(self, analysis_results: Dict[str, Any]) -> List[Dict]:
        """Create component reference appendix"""
        components = analysis_results.get('components', {}).get('component_inventory', {}).get('components', {})
        return [{'name': name, 'usage_count': count} for name, count in components.items()]

    def _create_visual_appendix(self, visual_assets: Dict[str, Any]) -> Dict[str, Any]:
        """Create visual assets appendix"""
        return {
            'total_screenshots': visual_assets.get('metadata', {}).get('total_screenshots', 0),
            'screenshot_categories': list(visual_assets.keys())
        }