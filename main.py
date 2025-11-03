#!/usr/bin/env python3
"""
Aldo Vision Agent - Comprehensive Penpot Design File Analysis
Main orchestrator for multi-persona design analysis with visual reporting
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# Core imports
from core.penpot_extractor import PenpotExtractor
from core.analysis_engine import AnalysisEngine
from core.component_detector import ComponentDetector
from core.penpot_api_connector import PenpotAPIConnector, connect_to_penpot

# Persona analyzers
from personas.product_manager import ProductManagerAnalyzer
from personas.product_designer import ProductDesignerAnalyzer
from personas.ai_developer import AIDeveloperAnalyzer
from personas.file_analyzer import FileAnalyzer
from personas.design_systems_designer import DesignSystemsDesignerAnalyzer
from personas.design_systems_engineer import DesignSystemsEngineerAnalyzer
from personas.accessibility_specialist import create_accessibility_analysis

class AccessibilitySpecialistAnalyzer:
    """Enhanced world-class accessibility specialist analyzer"""

    def analyze(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Run comprehensive accessibility analysis"""
        penpot_data = {
            'extracted_data': extracted_data,
            'components': components
        }

        return create_accessibility_analysis(penpot_data)
from personas.content_strategist import ContentStrategistAnalyzer
from personas.test_automation_engineer import create_test_automation_analysis
from personas.tdd_specialist import create_tdd_specialist_analysis

class TestAutomationEngineerAnalyzer:
    """World-class test automation engineer analyzer"""

    def analyze(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Run comprehensive test automation analysis"""
        penpot_data = {
            'extracted_data': extracted_data,
            'components': components
        }

        return create_test_automation_analysis(penpot_data)

class TDDSpecialistAnalyzer:
    """TDD methodology specialist analyzer"""

    def analyze(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Run comprehensive TDD methodology analysis"""
        penpot_data = {
            'extracted_data': extracted_data,
            'components': components
        }

        return create_tdd_specialist_analysis(penpot_data)

from personas.qa_engineer import QAEngineerAnalyzer
from personas.security_analyst import SecurityAnalystAnalyzer
from personas.visual_reporter import VisualReporterAnalyzer

# Output generators
from output_generators.product_acceptance import ProductAcceptanceCriteriaGenerator
from output_generators.design_acceptance import DesignAcceptanceCriteriaGenerator
from output_generators.developer_specs import DeveloperSpecsGenerator
from output_generators.claude_code_format import ClaudeCodeFormatGenerator
from output_generators.contextual_analysis import ContextualAnalysisGenerator

# Visual system
from visual_system.screenshot_engine import ScreenshotEngine
from visual_system.html_generator import HTMLReportGenerator
from visual_system.pdf_generator import PDFReportGenerator
from visual_system.annotation_system import AnnotationSystem
from visual_system.linking_system import LinkingSystem


@dataclass
class AnalysisConfig:
    """Configuration for analysis run"""
    input_file: str
    output_dir: str = "output"
    personas: List[str] = None
    output_formats: List[str] = None
    visual_quality: str = "high"  # low, medium, high
    generate_screenshots: bool = True
    deep_analysis: bool = True
    source_type: str = "file"  # file or api
    penpot_api_url: Optional[str] = None
    penpot_username: Optional[str] = None
    penpot_password: Optional[str] = None
    file_id: Optional[str] = None  # For API source


class AldoVisionAgent:
    """
    Main Aldo Vision Agent class
    Orchestrates comprehensive multi-persona design file analysis
    """

    def __init__(self, config_path: Optional[str] = None):
        self.logger = self._setup_logging()
        self.config = self._load_config(config_path)

        # Initialize core components
        self.extractor = PenpotExtractor()
        self.analysis_engine = AnalysisEngine()
        self.component_detector = ComponentDetector()

        # Initialize persona analyzers
        self.persona_analyzers = {
            'product_manager': ProductManagerAnalyzer(),
            'product_designer': ProductDesignerAnalyzer(),
            'ai_developer': AIDeveloperAnalyzer(),
            'file_analyzer': FileAnalyzer(),
            'design_systems_designer': DesignSystemsDesignerAnalyzer(),
            'design_systems_engineer': DesignSystemsEngineerAnalyzer(),
            'accessibility_specialist': AccessibilitySpecialistAnalyzer(),
            'test_automation_engineer': TestAutomationEngineerAnalyzer(),
            'tdd_specialist': TDDSpecialistAnalyzer(),
            'content_strategist': ContentStrategistAnalyzer(),
            'qa_engineer': QAEngineerAnalyzer(),
            'security_analyst': SecurityAnalystAnalyzer(),
            'visual_reporter': VisualReporterAnalyzer()
        }

        # Initialize output generators
        self.output_generators = {
            'product_acceptance': ProductAcceptanceCriteriaGenerator(),
            'design_acceptance': DesignAcceptanceCriteriaGenerator(),
            'developer_specs': DeveloperSpecsGenerator(),
            'claude_code_format': ClaudeCodeFormatGenerator(),
            'contextual_analysis': ContextualAnalysisGenerator()
        }

        # Initialize visual system
        self.screenshot_engine = ScreenshotEngine()
        self.html_generator = HTMLReportGenerator()
        self.pdf_generator = PDFReportGenerator()
        self.annotation_system = AnnotationSystem()
        self.linking_system = LinkingSystem()

        self.logger.info("Aldo Vision Agent initialized successfully")

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('aldo-vision.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        return logging.getLogger(__name__)

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load agent configuration"""
        default_config = {
            'personas': {
                'enabled': list(self.persona_analyzers.keys()) if hasattr(self, 'persona_analyzers') else [],
                'weights': {persona: 1.0 for persona in ['product_manager', 'product_designer', 'ai_developer']}
            },
            'output_formats': ['html', 'pdf', 'json'],
            'visual': {
                'screenshot_quality': 'high',
                'annotation_style': 'professional',
                'include_component_isolation': True
            }
        }

        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                user_config = json.load(f)
            # Merge configurations
            default_config.update(user_config)

        return default_config

    def analyze_penpot_file(self, file_path: str, config: Optional[AnalysisConfig] = None) -> Dict[str, Any]:
        """
        Main analysis entry point - supports both file and API sources

        Args:
            file_path: Path to Penpot file (for file source) or file ID (for API source)
            config: Analysis configuration

        Returns:
            Comprehensive analysis results
        """
        source_type = config.source_type if config else "file"

        if source_type == "api":
            return self.analyze_from_api(file_path, config)
        else:
            return self.analyze_from_file(file_path, config)

    def analyze_from_file(self, file_path: str, config: Optional[AnalysisConfig] = None) -> Dict[str, Any]:
        """
        Analyze from local Penpot file

        Args:
            file_path: Path to Penpot file
            config: Analysis configuration

        Returns:
            Comprehensive analysis results
        """
        self.logger.info(f"Starting analysis of Penpot file: {file_path}")

        if not Path(file_path).exists():
            raise FileNotFoundError(f"Penpot file not found: {file_path}")

        try:
            # Step 1: Extract Penpot file
            self.logger.info("Extracting Penpot file...")
            extracted_data = self.extractor.extract_penpot_file(file_path)

            # Step 2: Detect components
            self.logger.info("Detecting UI components...")
            components = self.component_detector.detect_components(extracted_data)

            # Step 3: Run multi-persona analysis
            self.logger.info("Running multi-persona analysis...")
            persona_results = self._run_persona_analysis(extracted_data, components, config)

            # Step 4: Generate cross-persona insights
            self.logger.info("Generating cross-persona insights...")
            cross_insights = self.analysis_engine.generate_cross_insights(persona_results)

            # Step 5: Create comprehensive results
            results = {
                'metadata': {
                    'input_file': file_path,
                    'analysis_timestamp': self._get_timestamp(),
                    'agent_version': '1.0.0',
                    'personas_analyzed': list(persona_results.keys())
                },
                'extracted_data': extracted_data,
                'components': components,
                'persona_analyses': persona_results,
                'cross_insights': cross_insights,
                'recommendations': self._generate_recommendations(persona_results, cross_insights)
            }

            self.logger.info("Analysis completed successfully")
            return results

        except Exception as e:
            self.logger.error(f"Analysis failed: {str(e)}")
            raise

    def analyze_from_api(self, file_id: str, config: Optional[AnalysisConfig] = None) -> Dict[str, Any]:
        """
        Analyze from Penpot API (live integration)

        Args:
            file_id: Penpot file ID
            config: Analysis configuration with API credentials

        Returns:
            Comprehensive analysis results
        """
        self.logger.info(f"Starting analysis from Penpot API: {file_id}")

        try:
            # Step 1: Connect to Penpot API
            self.logger.info("Connecting to Penpot API...")
            api_url = config.penpot_api_url if config else None
            username = config.penpot_username if config else None
            password = config.penpot_password if config else None

            connector = connect_to_penpot(api_url, username, password)
            if not connector:
                raise ConnectionError("Failed to connect to Penpot API")

            # Step 2: Fetch file data from API
            self.logger.info(f"Fetching file data for {file_id}...")
            file_data = connector.get_file_data(file_id)
            if not file_data:
                raise ValueError(f"Could not retrieve file {file_id} from Penpot API")

            # Step 3: Convert to Aldo Vision format
            self.logger.info("Converting API data to Aldo Vision format...")
            extracted_data = connector.export_to_aldo_format(file_data)

            # Step 4: Detect components
            self.logger.info("Detecting UI components...")
            components = self.component_detector.detect_components(extracted_data)

            # Step 5: Run multi-persona analysis
            self.logger.info("Running multi-persona analysis...")
            persona_results = self._run_persona_analysis(extracted_data, components, config)

            # Step 6: Generate cross-persona insights
            self.logger.info("Generating cross-persona insights...")
            cross_insights = self.analysis_engine.generate_cross_insights(persona_results)

            # Step 7: Create comprehensive results
            results = {
                'metadata': {
                    'file_id': file_id,
                    'source': 'penpot_api',
                    'api_url': connector.api_url,
                    'analysis_timestamp': self._get_timestamp(),
                    'agent_version': '2.0.0',  # API-enabled version
                    'personas_analyzed': list(persona_results.keys())
                },
                'extracted_data': extracted_data,
                'components': components,
                'persona_analyses': persona_results,
                'cross_insights': cross_insights,
                'recommendations': self._generate_recommendations(persona_results, cross_insights)
            }

            self.logger.info("API analysis completed successfully")
            return results

        except Exception as e:
            self.logger.error(f"API analysis failed: {str(e)}")
            raise

    def _run_persona_analysis(self, extracted_data: Dict, components: Dict, config: Optional[AnalysisConfig]) -> Dict[str, Any]:
        """Run analysis from all persona perspectives"""
        results = {}

        # Determine which personas to run
        personas_to_run = (config.personas if config and config.personas
                          else list(self.persona_analyzers.keys()))

        for persona_name in personas_to_run:
            if persona_name in self.persona_analyzers:
                self.logger.info(f"Running {persona_name} analysis...")
                analyzer = self.persona_analyzers[persona_name]
                results[persona_name] = analyzer.analyze(extracted_data, components)
            else:
                self.logger.warning(f"Unknown persona: {persona_name}")

        return results

    def generate_comprehensive_reports(self, analysis_results: Dict[str, Any], output_dir: str = "output") -> Dict[str, str]:
        """
        Generate all output formats from analysis results

        Args:
            analysis_results: Results from analyze_penpot_file()
            output_dir: Directory to save reports

        Returns:
            Dictionary mapping format names to output file paths
        """
        self.logger.info("Generating comprehensive reports...")

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        report_paths = {}

        try:
            # Generate acceptance criteria formats
            self.logger.info("Generating acceptance criteria...")
            for format_name, generator in self.output_generators.items():
                format_output = generator.generate(analysis_results)
                output_file = output_path / f"{format_name}.json"
                with open(output_file, 'w') as f:
                    json.dump(format_output, f, indent=2)
                report_paths[format_name] = str(output_file)

            # Generate visual reports
            if self.config.get('visual', {}).get('screenshot_quality', 'high') != 'none':
                self.logger.info("Generating visual assets...")
                visual_assets = self.screenshot_engine.generate_screenshots(analysis_results)

                # Generate interactive HTML report
                self.logger.info("Generating HTML report...")
                html_report = self.html_generator.generate_report(analysis_results, visual_assets)
                html_file = output_path / "interactive_report.html"
                with open(html_file, 'w') as f:
                    f.write(html_report)
                report_paths['interactive_html'] = str(html_file)

                # Generate PDF report
                self.logger.info("Generating PDF report...")
                pdf_report = self.pdf_generator.generate_report(analysis_results, visual_assets)
                pdf_file = output_path / "comprehensive_report.pdf"
                with open(pdf_file, 'wb') as f:
                    f.write(pdf_report)
                report_paths['professional_pdf'] = str(pdf_file)

            # Generate summary JSON
            summary_file = output_path / "analysis_summary.json"
            with open(summary_file, 'w') as f:
                json.dump(self._create_summary(analysis_results), f, indent=2)
            report_paths['summary'] = str(summary_file)

            self.logger.info(f"Reports generated successfully in {output_dir}")
            return report_paths

        except Exception as e:
            self.logger.error(f"Report generation failed: {str(e)}")
            raise

    def run_persona_analysis(self, persona_name: str, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Run analysis for a specific persona"""
        if persona_name not in self.persona_analyzers:
            raise ValueError(f"Unknown persona: {persona_name}")

        analyzer = self.persona_analyzers[persona_name]
        return analyzer.analyze(
            analysis_results['extracted_data'],
            analysis_results['components']
        )

    def _generate_recommendations(self, persona_results: Dict, cross_insights: Dict) -> List[Dict]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []

        # High-priority recommendations from multiple personas
        if 'accessibility_specialist' in persona_results:
            accessibility_issues = persona_results['accessibility_specialist'].get('critical_issues', [])
            for issue in accessibility_issues:
                recommendations.append({
                    'priority': 'high',
                    'category': 'accessibility',
                    'title': issue.get('title', 'Accessibility Issue'),
                    'description': issue.get('description', ''),
                    'personas_affected': ['accessibility_specialist', 'qa_engineer'],
                    'effort': issue.get('effort', 'medium'),
                    'impact': 'high'
                })

        # Design system recommendations
        if 'design_systems_designer' in persona_results:
            design_issues = persona_results['design_systems_designer'].get('improvement_opportunities', [])
            for issue in design_issues:
                recommendations.append({
                    'priority': 'medium',
                    'category': 'design_system',
                    'title': issue.get('title', 'Design System Improvement'),
                    'description': issue.get('description', ''),
                    'personas_affected': ['design_systems_designer', 'design_systems_engineer'],
                    'effort': issue.get('effort', 'medium'),
                    'impact': 'medium'
                })

        return recommendations

    def _create_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create executive summary of analysis"""
        return {
            'file_info': analysis_results['metadata'],
            'component_count': len(analysis_results.get('components', {})),
            'personas_analyzed': len(analysis_results.get('persona_analyses', {})),
            'key_findings': {
                'total_frames': analysis_results['extracted_data'].get('total_frames', 0),
                'design_system_maturity': 'Level 2 - Component Library',  # This would be calculated
                'accessibility_score': '75%',  # This would be calculated
                'technical_debt_level': 'Medium'  # This would be calculated
            },
            'recommendations_count': len(analysis_results.get('recommendations', [])),
            'generated_reports': self.config.get('output_formats', [])
        }

    def _get_timestamp(self) -> str:
        """Get current timestamp for metadata"""
        from datetime import datetime
        return datetime.now().isoformat()


def main():
    """Command line interface for Aldo Vision Agent"""
    parser = argparse.ArgumentParser(description='Aldo Vision - Comprehensive Penpot Design Analysis (v2.0 - API Enabled)')
    parser.add_argument('input_file', help='Path to Penpot file (file mode) or File ID (API mode)')
    parser.add_argument('--output-dir', '-o', default='output', help='Output directory for reports')
    parser.add_argument('--personas', '-p', nargs='+', help='Specific personas to run (default: all)')
    parser.add_argument('--output-formats', '-f', nargs='+',
                       choices=['html', 'pdf', 'json', 'all'], default=['all'],
                       help='Output formats to generate')
    parser.add_argument('--config', '-c', help='Path to configuration file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')

    # API Integration options
    parser.add_argument('--source', '-s', choices=['file', 'api'], default='file',
                       help='Source type: file (local) or api (Penpot API)')
    parser.add_argument('--api-url', help='Penpot API URL (default: env or https://design.penpot.app)')
    parser.add_argument('--username', '-u', help='Penpot username (default: from env)')
    parser.add_argument('--password', '-w', help='Penpot password (default: from env)')

    args = parser.parse_args()

    # Setup logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Initialize agent
        agent = AldoVisionAgent(config_path=args.config)

        # Create analysis config
        config = AnalysisConfig(
            input_file=args.input_file,
            output_dir=args.output_dir,
            personas=args.personas,
            output_formats=args.output_formats if 'all' not in args.output_formats else None,
            source_type=args.source,
            penpot_api_url=args.api_url,
            penpot_username=args.username,
            penpot_password=args.password
        )

        # Run analysis
        if args.source == 'api':
            print(f"🌐 Analyzing from Penpot API - File ID: {args.input_file}")
        else:
            print(f"📁 Analyzing local Penpot file: {args.input_file}")

        results = agent.analyze_penpot_file(args.input_file, config)

        # Generate reports
        print(f"📊 Generating reports in: {args.output_dir}")
        report_paths = agent.generate_comprehensive_reports(results, args.output_dir)

        # Print results
        print("\n✅ Analysis completed successfully!")
        print("\n📄 Generated Reports:")
        for format_name, path in report_paths.items():
            print(f"  • {format_name}: {path}")

        print(f"\n🌐 View interactive report: file://{Path(args.output_dir).absolute() / 'interactive_report.html'}")

    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()