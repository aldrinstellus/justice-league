"""
PDF Report Generator
Generates professional PDF reports from analysis results with charts, layouts, and styling
"""

import logging
import io
import base64
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, Image, KeepTogether, Flowable
    )
    from reportlab.graphics.shapes import Drawing, Rect, Circle, String
    from reportlab.graphics.charts.piecharts import Pie
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics.charts.linecharts import HorizontalLineChart
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    Flowable = object  # Dummy class when reportlab is not available
    logging.warning("ReportLab not available. PDF generation will use alternative methods.")


@dataclass
class PDFConfig:
    """Configuration for PDF generation"""
    page_size: str = 'A4'
    margin_top: float = 1.0
    margin_bottom: float = 1.0
    margin_left: float = 1.0
    margin_right: float = 1.0
    font_name: str = 'Helvetica'
    font_size: int = 10
    include_charts: bool = True
    include_code_samples: bool = True
    watermark: Optional[str] = None


@dataclass
class ReportSection:
    """Represents a section in the PDF report"""
    title: str
    content: Any
    section_type: str  # text, table, chart, code, image
    level: int = 1  # Header level (1-6)
    page_break_before: bool = False
    keep_with_next: bool = False


class CustomFlowable(Flowable):
    """Custom flowable for special PDF elements"""

    def __init__(self, width, height, content_func, **kwargs):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.content_func = content_func
        self.kwargs = kwargs

    def draw(self):
        """Draw the custom content"""
        self.content_func(self.canv, self.width, self.height, **self.kwargs)


class PDFReportGenerator:
    """
    Professional PDF report generator with charts, tables, and advanced formatting
    """

    def __init__(self, config: Optional[PDFConfig] = None):
        self.logger = logging.getLogger(__name__)
        self.config = config or PDFConfig()

        if not REPORTLAB_AVAILABLE:
            self.logger.warning("ReportLab not available. Using fallback PDF generation.")

        # Initialize styles
        self.styles = self._create_styles()

        # Color scheme
        self.colors = {
            'primary': colors.Color(0.15, 0.4, 0.9),  # #2563eb
            'secondary': colors.Color(0.4, 0.45, 0.55),  # #64748b
            'success': colors.Color(0.06, 0.72, 0.51),  # #10b981
            'warning': colors.Color(0.96, 0.62, 0.04),  # #f59e0b
            'danger': colors.Color(0.94, 0.27, 0.27),  # #ef4444
            'background': colors.Color(0.97, 0.98, 0.99),  # #f8fafc
            'text': colors.Color(0.12, 0.16, 0.23),  # #1e293b
            'text_light': colors.Color(0.4, 0.45, 0.55),  # #64748b
        }

    def generate_report(self, analysis_results: Dict[str, Any], output_path: str) -> str:
        """
        Generate comprehensive PDF report

        Args:
            analysis_results: Complete analysis results
            output_path: Path where PDF should be saved

        Returns:
            Path to generated PDF file
        """
        self.logger.info(f"Generating PDF report: {output_path}")

        try:
            if REPORTLAB_AVAILABLE:
                return self._generate_with_reportlab(analysis_results, output_path)
            else:
                return self._generate_fallback_pdf(analysis_results, output_path)

        except Exception as e:
            self.logger.error(f"PDF generation failed: {str(e)}")
            raise

    def _generate_with_reportlab(self, analysis_results: Dict[str, Any], output_path: str) -> str:
        """Generate PDF using ReportLab"""

        # Create document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4 if self.config.page_size == 'A4' else letter,
            topMargin=self.config.margin_top * inch,
            bottomMargin=self.config.margin_bottom * inch,
            leftMargin=self.config.margin_left * inch,
            rightMargin=self.config.margin_right * inch
        )

        # Build content
        story = []

        # Title page
        story.extend(self._create_title_page(analysis_results))
        story.append(PageBreak())

        # Table of contents
        story.extend(self._create_table_of_contents(analysis_results))
        story.append(PageBreak())

        # Executive summary
        story.extend(self._create_executive_summary(analysis_results))
        story.append(PageBreak())

        # Analysis overview
        story.extend(self._create_analysis_overview(analysis_results))
        story.append(PageBreak())

        # Component analysis
        story.extend(self._create_component_analysis(analysis_results))
        story.append(PageBreak())

        # Persona insights
        story.extend(self._create_persona_insights(analysis_results))
        story.append(PageBreak())

        # Cross-insights and recommendations
        story.extend(self._create_cross_insights(analysis_results))
        story.append(PageBreak())

        # Implementation roadmap
        story.extend(self._create_implementation_roadmap(analysis_results))
        story.append(PageBreak())

        # Technical specifications
        if self.config.include_code_samples:
            story.extend(self._create_technical_specifications(analysis_results))
            story.append(PageBreak())

        # Quality assessment
        story.extend(self._create_quality_assessment(analysis_results))
        story.append(PageBreak())

        # Appendices
        story.extend(self._create_appendices(analysis_results))

        # Build PDF
        doc.build(story)

        self.logger.info(f"PDF report generated successfully: {output_path}")
        return output_path

    def _generate_fallback_pdf(self, analysis_results: Dict[str, Any], output_path: str) -> str:
        """Generate PDF using fallback method (basic text-based PDF)"""
        self.logger.info("Using fallback PDF generation method")

        # Create a simple HTML to PDF conversion or text-based PDF
        html_content = self._create_html_report(analysis_results)

        # In a real implementation, you might use:
        # - weasyprint
        # - pdfkit (wkhtmltopdf wrapper)
        # - html2pdf libraries
        # For now, we'll create a simple text file with PDF extension

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self._create_text_report(analysis_results))

        return output_path

    def _create_styles(self) -> Dict[str, Any]:
        """Create custom paragraph styles"""
        if not REPORTLAB_AVAILABLE:
            return {}

        styles = getSampleStyleSheet()

        # Custom styles
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=self.colors['primary'],
            alignment=TA_CENTER
        ))

        styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=12,
            spaceBefore=20,
            textColor=self.colors['primary']
        ))

        styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=6,
            spaceBefore=12,
            textColor=self.colors['text']
        ))

        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=self.colors['text'],
            alignment=TA_JUSTIFY
        ))

        styles.add(ParagraphStyle(
            name='CustomCode',
            parent=styles['Code'],
            fontSize=9,
            fontName='Courier',
            leftIndent=20,
            backgroundColor=self.colors['background']
        ))

        styles.add(ParagraphStyle(
            name='CustomCaption',
            parent=styles['Normal'],
            fontSize=8,
            textColor=self.colors['text_light'],
            alignment=TA_CENTER,
            spaceAfter=12
        ))

        return styles

    def _create_title_page(self, analysis_results: Dict[str, Any]) -> List[Any]:
        """Create title page elements"""
        elements = []

        if not REPORTLAB_AVAILABLE:
            return elements

        # Title
        title = analysis_results.get('metadata', {}).get('title', 'Design Analysis Report')
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph(title, self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.5*inch))

        # Subtitle
        subtitle = f"Comprehensive Multi-Persona Analysis Report"
        elements.append(Paragraph(subtitle, self.styles['CustomHeading2']))
        elements.append(Spacer(1, 1*inch))

        # Key metrics summary
        metadata = analysis_results.get('_metadata', {})
        summary_data = [
            ['Analysis Date:', datetime.now().strftime('%B %d, %Y')],
            ['Components Detected:', str(len(analysis_results.get('components', {}).get('detected_components', [])))],
            ['Personas Analyzed:', str(len(analysis_results.get('persona_analyses', {})))],
            ['Confidence Score:', f"{metadata.get('confidence_score', 0):.1%}"],
            ['Implementation Complexity:', metadata.get('implementation_complexity', 'Medium')],
        ]

        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, self.colors['primary']),
            ('BACKGROUND', (0, 0), (0, -1), self.colors['background']),
        ]))

        elements.append(summary_table)
        elements.append(Spacer(1, 1*inch))

        # Generated by
        elements.append(Paragraph("Generated by Aldo Vision Agent v1.0", self.styles['CustomCaption']))

        return elements

    def _create_table_of_contents(self, analysis_results: Dict[str, Any]) -> List[Any]:
        """Create table of contents"""
        elements = []

        if not REPORTLAB_AVAILABLE:
            return elements

        elements.append(Paragraph("Table of Contents", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 0.3*inch))

        toc_data = [
            ['1. Executive Summary', '3'],
            ['2. Analysis Overview', '4'],
            ['3. Component Analysis', '5'],
            ['4. Persona Insights', '7'],
            ['5. Cross-Insights & Recommendations', '12'],
            ['6. Implementation Roadmap', '14'],
            ['7. Technical Specifications', '16'],
            ['8. Quality Assessment', '18'],
            ['Appendices', '20'],
        ]

        toc_table = Table(toc_data, colWidths=[5*inch, 1*inch])
        toc_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        elements.append(toc_table)

        return elements

    def _create_executive_summary(self, analysis_results: Dict[str, Any]) -> List[Any]:
        """Create executive summary section"""
        elements = []

        if not REPORTLAB_AVAILABLE:
            return elements

        elements.append(Paragraph("Executive Summary", self.styles['CustomHeading1']))

        # Overview paragraph
        components_count = len(analysis_results.get('components', {}).get('detected_components', []))
        personas_count = len(analysis_results.get('persona_analyses', {}))

        summary_text = f"""
        This comprehensive design analysis report examines {components_count} UI components
        through the perspectives of {personas_count} different professional roles, providing
        actionable insights for implementation, optimization, and strategic planning.
        """

        elements.append(Paragraph(summary_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.2*inch))

        # Key findings
        elements.append(Paragraph("Key Findings", self.styles['CustomHeading2']))

        findings = self._extract_key_findings(analysis_results)
        for finding in findings:
            elements.append(Paragraph(f"• {finding}", self.styles['CustomBody']))

        elements.append(Spacer(1, 0.2*inch))

        # Strategic recommendations
        elements.append(Paragraph("Strategic Recommendations", self.styles['CustomHeading2']))

        recommendations = self._extract_top_recommendations(analysis_results)
        for i, rec in enumerate(recommendations[:5], 1):
            elements.append(Paragraph(f"{i}. {rec}", self.styles['CustomBody']))

        return elements

    def _create_analysis_overview(self, analysis_results: Dict[str, Any]) -> List[Any]:
        """Create analysis overview section"""
        elements = []

        if not REPORTLAB_AVAILABLE:
            return elements

        elements.append(Paragraph("Analysis Overview", self.styles['CustomHeading1']))

        # Analysis methodology
        elements.append(Paragraph("Methodology", self.styles['CustomHeading2']))
        methodology_text = """
        This analysis employs a multi-persona approach, examining the design through the
        lens of 11 different professional perspectives including Product Manager, Product
        Designer, AI Developer, Accessibility Specialist, and others. Each persona
        contributes unique insights that are then synthesized into cross-functional
        recommendations.
        """
        elements.append(Paragraph(methodology_text, self.styles['CustomBody']))

        # Analysis scope
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("Analysis Scope", self.styles['CustomHeading2']))

        scope_data = [
            ['Design Files Analyzed:', '1'],
            ['UI Components Detected:', str(len(analysis_results.get('components', {}).get('detected_components', [])))],
            ['Persona Perspectives:', str(len(analysis_results.get('persona_analyses', {})))],
            ['Analysis Categories:', 'Technical, Design, Business, Quality'],
            ['Output Formats Generated:', '4 (HTML, PDF, JSON, Claude Code)'],
        ]

        scope_table = Table(scope_data, colWidths=[2.5*inch, 2.5*inch])
        scope_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, self.colors['primary']),
            ('BACKGROUND', (0, 0), (0, -1), self.colors['background']),
        ]))

        elements.append(scope_table)

        # Quality metrics chart
        if self.config.include_charts:
            elements.append(Spacer(1, 0.3*inch))
            elements.append(Paragraph("Quality Metrics Overview", self.styles['CustomHeading2']))

            quality_chart = self._create_quality_metrics_chart(analysis_results)
            if quality_chart:
                elements.append(quality_chart)

        return elements

    def _create_component_analysis(self, analysis_results: Dict[str, Any]) -> List[Any]:
        """Create component analysis section"""
        elements = []

        if not REPORTLAB_AVAILABLE:
            return elements

        elements.append(Paragraph("Component Analysis", self.styles['CustomHeading1']))

        components = analysis_results.get('components', {}).get('detected_components', [])

        if not components:
            elements.append(Paragraph("No components detected in the analysis.", self.styles['CustomBody']))
            return elements

        # Component summary
        elements.append(Paragraph("Component Summary", self.styles['CustomHeading2']))

        summary_text = f"""
        The analysis identified {len(components)} distinct UI components across various
        categories. These components show varying levels of reusability and complexity,
        providing opportunities for design system consolidation and optimization.
        """
        elements.append(Paragraph(summary_text, self.styles['CustomBody']))

        # Component details table
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("Component Details", self.styles['CustomHeading2']))

        # Create table with component details
        table_data = [['Component', 'Type', 'Instances', 'Reusability', 'Complexity']]

        for component in components[:10]:  # Show top 10 components
            table_data.append([
                component.get('name', 'Unnamed')[:20],  # Truncate long names
                component.get('component_type', 'Unknown')[:15],
                str(len(component.get('instances', []))),
                f"{component.get('reusability_score', 0):.1f}",
                f"{component.get('complexity_score', 0):.1f}"
            ])

        component_table = Table(table_data, colWidths=[1.5*inch, 1*inch, 0.8*inch, 0.8*inch, 0.8*inch])
        component_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(component_table)

        # Component reusability chart
        if self.config.include_charts:
            elements.append(Spacer(1, 0.3*inch))
            reusability_chart = self._create_reusability_chart(components)
            if reusability_chart:
                elements.append(reusability_chart)
                elements.append(Paragraph("Component Reusability Distribution", self.styles['CustomCaption']))

        return elements

    def _create_persona_insights(self, analysis_results: Dict[str, Any]) -> List[Any]:
        """Create persona insights section"""
        elements = []

        if not REPORTLAB_AVAILABLE:
            return elements

        elements.append(Paragraph("Persona Insights", self.styles['CustomHeading1']))

        persona_analyses = analysis_results.get('persona_analyses', {})

        if not persona_analyses:
            elements.append(Paragraph("No persona analyses available.", self.styles['CustomBody']))
            return elements

        # Overview
        overview_text = f"""
        The multi-persona analysis approach provides comprehensive insights from
        {len(persona_analyses)} different professional perspectives, ensuring that
        technical, design, business, and quality considerations are all addressed.
        """
        elements.append(Paragraph(overview_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.2*inch))

        # Individual persona summaries
        for persona_name, analysis in persona_analyses.items():
            elements.append(Paragraph(f"{persona_name.replace('_', ' ').title()}", self.styles['CustomHeading2']))

            # Extract key insights from persona analysis
            insights = self._extract_persona_insights(analysis)
            for insight in insights[:3]:  # Show top 3 insights per persona
                elements.append(Paragraph(f"• {insight}", self.styles['CustomBody']))

            elements.append(Spacer(1, 0.1*inch))

        return elements

    def _create_cross_insights(self, analysis_results: Dict[str, Any]) -> List[Any]:
        """Create cross-insights and recommendations section"""
        elements = []

        if not REPORTLAB_AVAILABLE:
            return elements

        elements.append(Paragraph("Cross-Insights & Recommendations", self.styles['CustomHeading1']))

        cross_insights = analysis_results.get('cross_insights', {})

        # Strategic recommendations
        recommendations = cross_insights.get('strategic_recommendations', [])
        if recommendations:
            elements.append(Paragraph("Strategic Recommendations", self.styles['CustomHeading2']))

            for i, rec in enumerate(recommendations[:5], 1):
                title = rec.get('title', 'Recommendation')
                description = rec.get('description', 'No description available')
                elements.append(Paragraph(f"{i}. <b>{title}</b>", self.styles['CustomBody']))
                elements.append(Paragraph(f"   {description}", self.styles['CustomBody']))
                elements.append(Spacer(1, 0.1*inch))

        # Priority matrix
        priority_matrix = cross_insights.get('priority_matrix', {})
        if priority_matrix:
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph("Implementation Priority Matrix", self.styles['CustomHeading2']))

            for priority, items in priority_matrix.items():
                if items:
                    elements.append(Paragraph(f"{priority.title()} Priority ({len(items)} items)", self.styles['CustomHeading2']))
                    for item in items[:3]:  # Show top 3 per priority
                        title = item.get('title', 'Item') if isinstance(item, dict) else str(item)
                        elements.append(Paragraph(f"• {title}", self.styles['CustomBody']))

        return elements

    def _create_implementation_roadmap(self, analysis_results: Dict[str, Any]) -> List[Any]:
        """Create implementation roadmap section"""
        elements = []

        if not REPORTLAB_AVAILABLE:
            return elements

        elements.append(Paragraph("Implementation Roadmap", self.styles['CustomHeading1']))

        # Check for roadmap in multiple possible locations
        roadmap = None
        cross_insights = analysis_results.get('cross_insights', {})
        ai_analysis = analysis_results.get('persona_analyses', {}).get('ai_developer', {})

        roadmap = (cross_insights.get('implementation_roadmap') or
                  ai_analysis.get('implementation_roadmap') or
                  {})

        if roadmap:
            # Extract phases
            phases = []
            for key, value in roadmap.items():
                if isinstance(value, dict) and 'duration' in str(value):
                    phases.append((key, value))

            if phases:
                elements.append(Paragraph("Implementation Phases", self.styles['CustomHeading2']))

                phase_data = [['Phase', 'Duration', 'Focus', 'Key Deliverables']]

                for phase_name, phase_info in phases:
                    if isinstance(phase_info, dict):
                        duration = phase_info.get('duration', 'TBD')
                        focus = phase_info.get('focus', 'General development')
                        deliverables = phase_info.get('deliverables', [])
                        deliverables_str = ', '.join(deliverables[:2]) if deliverables else 'TBD'

                        phase_data.append([
                            phase_name.replace('_', ' ').title(),
                            duration,
                            focus[:30] + '...' if len(focus) > 30 else focus,
                            deliverables_str[:30] + '...' if len(deliverables_str) > 30 else deliverables_str
                        ])

                if len(phase_data) > 1:  # Has data beyond header
                    roadmap_table = Table(phase_data, colWidths=[1.2*inch, 1*inch, 1.5*inch, 2*inch])
                    roadmap_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 9),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP')
                    ]))

                    elements.append(roadmap_table)

        # Timeline estimate
        metadata = analysis_results.get('_metadata', {})
        timeline = metadata.get('estimated_development_time', {})
        if timeline:
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph("Timeline Estimate", self.styles['CustomHeading2']))

            timeline_text = f"""
            Based on the component analysis and complexity assessment, the estimated
            development timeline is {timeline.get('development_weeks', 'TBD')} weeks with
            {timeline.get('total_hours', 'TBD')} total development hours.
            """
            elements.append(Paragraph(timeline_text, self.styles['CustomBody']))

        return elements

    def _create_technical_specifications(self, analysis_results: Dict[str, Any]) -> List[Any]:
        """Create technical specifications section"""
        elements = []

        if not REPORTLAB_AVAILABLE or not self.config.include_code_samples:
            return elements

        elements.append(Paragraph("Technical Specifications", self.styles['CustomHeading1']))

        # Technology recommendations
        ai_analysis = analysis_results.get('persona_analyses', {}).get('ai_developer', {})
        tech_architecture = ai_analysis.get('technical_architecture', {})

        if tech_architecture:
            elements.append(Paragraph("Recommended Technology Stack", self.styles['CustomHeading2']))

            # Extract technology recommendations
            tech_recommendations = tech_architecture.get('technology_recommendations', {})
            if tech_recommendations:
                for category, technologies in tech_recommendations.items():
                    if technologies:
                        tech_list = ', '.join(technologies) if isinstance(technologies, list) else str(technologies)
                        elements.append(Paragraph(f"<b>{category.replace('_', ' ').title()}:</b> {tech_list}", self.styles['CustomBody']))

        # Component specifications
        claude_code_output = analysis_results.get('claude_code_format', {})
        component_specs = claude_code_output.get('component_specifications', [])

        if component_specs:
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph("Component Specifications", self.styles['CustomHeading2']))

            for spec in component_specs[:3]:  # Show top 3 component specs
                spec_info = spec.get('specification', {})
                comp_name = spec_info.get('name', 'Component')
                comp_description = spec_info.get('description', 'No description available')

                elements.append(Paragraph(f"<b>{comp_name}</b>", self.styles['CustomHeading2']))
                elements.append(Paragraph(comp_description, self.styles['CustomBody']))

                # Props interface
                props = spec_info.get('props_interface', {})
                if props:
                    elements.append(Paragraph("Props:", self.styles['CustomBody']))
                    props_text = ', '.join([f"{k}: {v}" for k, v in props.items()])
                    elements.append(Paragraph(props_text, self.styles['CustomCode']))

                elements.append(Spacer(1, 0.1*inch))

        return elements

    def _create_quality_assessment(self, analysis_results: Dict[str, Any]) -> List[Any]:
        """Create quality assessment section"""
        elements = []

        if not REPORTLAB_AVAILABLE:
            return elements

        elements.append(Paragraph("Quality Assessment", self.styles['CustomHeading1']))

        # Overall quality metrics
        quality_assessment = analysis_results.get('components', {}).get('quality_assessment', {})

        if quality_assessment:
            overall_score = quality_assessment.get('overall_score', 0)
            quality_grade = quality_assessment.get('quality_grade', 'N/A')

            elements.append(Paragraph("Overall Quality Score", self.styles['CustomHeading2']))
            elements.append(Paragraph(f"Grade: <b>{quality_grade}</b> (Score: {overall_score:.2f})", self.styles['CustomBody']))

            # Component scores
            component_scores = quality_assessment.get('component_scores', {})
            if component_scores:
                elements.append(Spacer(1, 0.2*inch))
                elements.append(Paragraph("Quality Breakdown", self.styles['CustomHeading2']))

                score_data = [['Metric', 'Score', 'Grade']]
                for metric, score in component_scores.items():
                    grade = self._score_to_grade(score)
                    score_data.append([
                        metric.replace('_', ' ').title(),
                        f"{score:.2f}",
                        grade
                    ])

                score_table = Table(score_data, colWidths=[2*inch, 1*inch, 1*inch])
                score_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))

                elements.append(score_table)

        # Improvement recommendations
        improvement_areas = quality_assessment.get('improvement_areas', [])
        if improvement_areas:
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph("Improvement Areas", self.styles['CustomHeading2']))

            for area in improvement_areas:
                elements.append(Paragraph(f"• {area}", self.styles['CustomBody']))

        return elements

    def _create_appendices(self, analysis_results: Dict[str, Any]) -> List[Any]:
        """Create appendices section"""
        elements = []

        if not REPORTLAB_AVAILABLE:
            return elements

        elements.append(Paragraph("Appendices", self.styles['CustomHeading1']))

        # Appendix A: Detailed component list
        components = analysis_results.get('components', {}).get('detected_components', [])
        if components:
            elements.append(Paragraph("Appendix A: Complete Component List", self.styles['CustomHeading2']))

            for i, component in enumerate(components, 1):
                comp_name = component.get('name', f'Component {i}')
                comp_type = component.get('component_type', 'Unknown')
                instances = len(component.get('instances', []))

                elements.append(Paragraph(f"{i}. <b>{comp_name}</b> ({comp_type}) - {instances} instances", self.styles['CustomBody']))

        # Appendix B: Persona analysis details
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("Appendix B: Persona Analysis Summary", self.styles['CustomHeading2']))

        persona_analyses = analysis_results.get('persona_analyses', {})
        for persona_name, analysis in persona_analyses.items():
            persona_title = persona_name.replace('_', ' ').title()
            elements.append(Paragraph(f"<b>{persona_title}</b>: Analysis completed with insights on component structure, implementation patterns, and optimization opportunities.", self.styles['CustomBody']))

        # Appendix C: Glossary
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("Appendix C: Glossary", self.styles['CustomHeading2']))

        glossary_terms = [
            ("Component", "A reusable UI element with defined properties and behavior"),
            ("Reusability Score", "Metric indicating how frequently a component is used across the design"),
            ("Complexity Score", "Metric indicating the implementation difficulty of a component"),
            ("Design System", "A collection of reusable components and guidelines for consistent design"),
            ("Atomic Design", "Methodology for creating design systems with atoms, molecules, organisms, templates, and pages")
        ]

        for term, definition in glossary_terms:
            elements.append(Paragraph(f"<b>{term}:</b> {definition}", self.styles['CustomBody']))

        return elements

    def _create_quality_metrics_chart(self, analysis_results: Dict[str, Any]) -> Optional[Any]:
        """Create quality metrics chart"""
        if not REPORTLAB_AVAILABLE:
            return None

        try:
            # Create a simple bar chart for quality metrics
            quality_assessment = analysis_results.get('components', {}).get('quality_assessment', {})
            component_scores = quality_assessment.get('component_scores', {})

            if not component_scores:
                return None

            drawing = Drawing(400, 200)
            chart = VerticalBarChart()
            chart.x = 50
            chart.y = 50
            chart.height = 125
            chart.width = 300

            chart.data = [list(component_scores.values())]
            chart.categoryAxis.categoryNames = [name.replace('_', ' ').title() for name in component_scores.keys()]
            chart.valueAxis.valueMin = 0
            chart.valueAxis.valueMax = 1

            chart.bars[0].fillColor = self.colors['primary']

            drawing.add(chart)
            return drawing

        except Exception as e:
            self.logger.error(f"Failed to create quality metrics chart: {e}")
            return None

    def _create_reusability_chart(self, components: List[Dict[str, Any]]) -> Optional[Any]:
        """Create component reusability chart"""
        if not REPORTLAB_AVAILABLE:
            return None

        try:
            # Create pie chart for reusability distribution
            reusability_scores = [comp.get('reusability_score', 0) for comp in components]

            # Categorize reusability
            high_reuse = sum(1 for score in reusability_scores if score > 0.7)
            medium_reuse = sum(1 for score in reusability_scores if 0.3 <= score <= 0.7)
            low_reuse = sum(1 for score in reusability_scores if score < 0.3)

            if high_reuse + medium_reuse + low_reuse == 0:
                return None

            drawing = Drawing(300, 200)
            pie = Pie()
            pie.x = 50
            pie.y = 50
            pie.width = 200
            pie.height = 100

            pie.data = [high_reuse, medium_reuse, low_reuse]
            pie.labels = ['High Reuse', 'Medium Reuse', 'Low Reuse']
            pie.slices.strokeWidth = 0.5
            pie.slices[0].fillColor = self.colors['success']
            pie.slices[1].fillColor = self.colors['warning']
            pie.slices[2].fillColor = self.colors['danger']

            drawing.add(pie)
            return drawing

        except Exception as e:
            self.logger.error(f"Failed to create reusability chart: {e}")
            return None

    def _create_html_report(self, analysis_results: Dict[str, Any]) -> str:
        """Create HTML version of the report for fallback PDF generation"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Design Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2563eb; }}
                h2 {{ color: #1e293b; margin-top: 30px; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f8fafc; }}
            </style>
        </head>
        <body>
            <h1>Design Analysis Report</h1>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

            <h2>Analysis Summary</h2>
            <p>Components analyzed: {len(analysis_results.get('components', {}).get('detected_components', []))}</p>
            <p>Personas analyzed: {len(analysis_results.get('persona_analyses', {}))}</p>

            <h2>Component Details</h2>
            <table>
                <tr><th>Component</th><th>Type</th><th>Instances</th></tr>
        """

        # Add component details
        components = analysis_results.get('components', {}).get('detected_components', [])
        for component in components[:10]:
            html_content += f"""
                <tr>
                    <td>{component.get('name', 'Unnamed')}</td>
                    <td>{component.get('component_type', 'Unknown')}</td>
                    <td>{len(component.get('instances', []))}</td>
                </tr>
            """

        html_content += """
            </table>

            <h2>Recommendations</h2>
            <ul>
        """

        # Add recommendations
        cross_insights = analysis_results.get('cross_insights', {})
        recommendations = cross_insights.get('strategic_recommendations', [])
        for rec in recommendations[:5]:
            title = rec.get('title', 'Recommendation') if isinstance(rec, dict) else str(rec)
            html_content += f"<li>{title}</li>"

        html_content += """
            </ul>
        </body>
        </html>
        """

        return html_content

    def _create_text_report(self, analysis_results: Dict[str, Any]) -> str:
        """Create text version of the report for basic fallback"""
        report_lines = [
            "DESIGN ANALYSIS REPORT",
            "=" * 50,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "EXECUTIVE SUMMARY",
            "-" * 20,
        ]

        # Add summary information
        components_count = len(analysis_results.get('components', {}).get('detected_components', []))
        personas_count = len(analysis_results.get('persona_analyses', {}))

        report_lines.extend([
            f"Components Detected: {components_count}",
            f"Personas Analyzed: {personas_count}",
            "",
            "COMPONENT ANALYSIS",
            "-" * 20,
        ])

        # Add component details
        components = analysis_results.get('components', {}).get('detected_components', [])
        for i, component in enumerate(components[:10], 1):
            name = component.get('name', 'Unnamed')
            comp_type = component.get('component_type', 'Unknown')
            instances = len(component.get('instances', []))
            report_lines.append(f"{i:2d}. {name} ({comp_type}) - {instances} instances")

        # Add recommendations
        report_lines.extend([
            "",
            "STRATEGIC RECOMMENDATIONS",
            "-" * 30,
        ])

        cross_insights = analysis_results.get('cross_insights', {})
        recommendations = cross_insights.get('strategic_recommendations', [])
        for i, rec in enumerate(recommendations[:5], 1):
            title = rec.get('title', 'Recommendation') if isinstance(rec, dict) else str(rec)
            report_lines.append(f"{i}. {title}")

        report_lines.extend([
            "",
            "END OF REPORT",
            "=" * 50
        ])

        return '\n'.join(report_lines)

    # Helper methods

    def _extract_key_findings(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Extract key findings from analysis results"""
        findings = []

        components_count = len(analysis_results.get('components', {}).get('detected_components', []))
        if components_count > 0:
            findings.append(f"Identified {components_count} distinct UI components with varying reusability patterns")

        quality_assessment = analysis_results.get('components', {}).get('quality_assessment', {})
        if quality_assessment:
            overall_score = quality_assessment.get('overall_score', 0)
            findings.append(f"Overall design system quality score: {overall_score:.1%}")

        cross_insights = analysis_results.get('cross_insights', {})
        if cross_insights.get('strategic_recommendations'):
            rec_count = len(cross_insights['strategic_recommendations'])
            findings.append(f"Generated {rec_count} strategic recommendations for implementation")

        return findings

    def _extract_top_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Extract top recommendations from analysis"""
        recommendations = []

        cross_insights = analysis_results.get('cross_insights', {})
        strategic_recs = cross_insights.get('strategic_recommendations', [])

        for rec in strategic_recs[:5]:
            if isinstance(rec, dict):
                title = rec.get('title', 'Unnamed recommendation')
                recommendations.append(title)
            else:
                recommendations.append(str(rec))

        return recommendations

    def _extract_persona_insights(self, analysis: Dict[str, Any]) -> List[str]:
        """Extract key insights from persona analysis"""
        insights = []

        # Try to extract insights from common keys
        for key in ['recommendations', 'key_insights', 'summary', 'findings']:
            if key in analysis:
                value = analysis[key]
                if isinstance(value, list):
                    insights.extend(value[:3])
                    break
                elif isinstance(value, str):
                    insights.append(value)
                    break

        # Fallback to generic insight
        if not insights:
            insights.append("Analysis completed with detailed findings and recommendations")

        return insights

    def _score_to_grade(self, score: float) -> str:
        """Convert numeric score to letter grade"""
        if score >= 0.9: return 'A'
        elif score >= 0.8: return 'B'
        elif score >= 0.7: return 'C'
        elif score >= 0.6: return 'D'
        else: return 'F'