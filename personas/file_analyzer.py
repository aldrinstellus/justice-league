"""
File Analyzer Persona
Analyzes design files from a technical file structure and architecture perspective
"""

import logging
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict, Counter
from pathlib import Path
import hashlib


@dataclass
class FileStructureAnalysis:
    """Analysis of file structure and organization"""
    total_files: int
    file_types: Dict[str, int]
    directory_structure: Dict[str, Any]
    naming_conventions: Dict[str, Any]
    organization_score: float
    complexity_metrics: Dict[str, Any]


@dataclass
class ArchitecturalPattern:
    """Detected architectural pattern in the design file"""
    pattern_name: str
    pattern_type: str
    confidence: float
    evidence: List[str]
    implications: List[str]
    recommendations: List[str]


@dataclass
class DataIntegrityAnalysis:
    """Analysis of data integrity and consistency"""
    consistency_score: float
    missing_references: List[str]
    circular_dependencies: List[str]
    orphaned_elements: List[str]
    duplicate_content: List[str]
    validation_errors: List[str]


@dataclass
class PerformanceProfile:
    """Performance characteristics of the design file"""
    file_size_breakdown: Dict[str, int]
    loading_bottlenecks: List[str]
    optimization_opportunities: List[str]
    memory_usage_estimate: Dict[str, Any]
    rendering_complexity: Dict[str, Any]


class FileAnalyzer:
    """Analyzes design files from a technical file structure perspective"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # File structure patterns
        self.structure_patterns = {
            'atomic_design': {
                'atoms': ['button', 'input', 'icon', 'text'],
                'molecules': ['search-bar', 'form-field', 'nav-item'],
                'organisms': ['header', 'footer', 'sidebar', 'form'],
                'templates': ['page-template', 'layout'],
                'pages': ['homepage', 'dashboard', 'profile']
            },
            'feature_based': {
                'features': ['authentication', 'dashboard', 'settings'],
                'shared': ['components', 'utils', 'assets'],
                'core': ['api', 'types', 'constants']
            },
            'mvc_pattern': {
                'models': ['data', 'schemas', 'entities'],
                'views': ['components', 'pages', 'layouts'],
                'controllers': ['handlers', 'services', 'managers']
            }
        }

        # File type categories
        self.file_categories = {
            'design': ['penpot', 'figma', 'sketch', 'xd'],
            'assets': ['png', 'jpg', 'svg', 'gif', 'webp'],
            'code': ['js', 'ts', 'jsx', 'tsx', 'vue', 'svelte'],
            'styles': ['css', 'scss', 'sass', 'less', 'stylus'],
            'config': ['json', 'yaml', 'toml', 'ini', 'env'],
            'documentation': ['md', 'txt', 'doc', 'pdf']
        }

        # Performance thresholds
        self.performance_thresholds = {
            'file_size_warning': 10 * 1024 * 1024,  # 10MB
            'object_count_warning': 1000,
            'nesting_depth_warning': 10,
            'reference_count_warning': 500
        }

        # Quality metrics
        self.quality_metrics = {
            'naming_consistency': 0.8,
            'structure_organization': 0.7,
            'reference_integrity': 0.9,
            'performance_score': 0.6
        }

    def analyze(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform file analyzer analysis

        Args:
            extracted_data: Extracted Penpot file data
            components: Detected UI components

        Returns:
            File analyzer analysis results
        """
        self.logger.info("Starting File Analyzer analysis")

        try:
            analysis_results = {
                'file_structure_analysis': self._analyze_file_structure(extracted_data),
                'architectural_patterns': self._detect_architectural_patterns(extracted_data, components),
                'data_integrity_analysis': self._analyze_data_integrity(extracted_data),
                'performance_profile': self._create_performance_profile(extracted_data, components),
                'naming_analysis': self._analyze_naming_conventions(extracted_data),
                'dependency_analysis': self._analyze_dependencies(extracted_data),
                'version_analysis': self._analyze_version_information(extracted_data),
                'metadata_analysis': self._analyze_metadata_quality(extracted_data),
                'scalability_assessment': self._assess_scalability(extracted_data, components),
                'maintenance_analysis': self._analyze_maintenance_aspects(extracted_data, components),
                'migration_readiness': self._assess_migration_readiness(extracted_data),
                'technical_debt_analysis': self._analyze_technical_debt(extracted_data, components),
                'optimization_recommendations': self._generate_optimization_recommendations(extracted_data, components),
                'file_health_score': self._calculate_file_health_score(extracted_data, components)
            }

            self.logger.info("File Analyzer analysis completed")
            return analysis_results

        except Exception as e:
            self.logger.error(f"File Analyzer analysis failed: {str(e)}")
            raise

    def _analyze_file_structure(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the overall file structure and organization"""

        # Count files and analyze structure
        files_data = extracted_data.get('files', {})
        total_files = len(files_data)

        # Analyze directory structure
        directory_structure = self._build_directory_structure(files_data)

        # Analyze file types and distribution
        file_types = self._analyze_file_types(files_data)

        # Assess naming conventions
        naming_analysis = self._assess_naming_conventions(files_data)

        # Calculate organization score
        organization_score = self._calculate_organization_score(directory_structure, naming_analysis)

        # Analyze complexity metrics
        complexity_metrics = self._calculate_complexity_metrics(files_data)

        structure_analysis = FileStructureAnalysis(
            total_files=total_files,
            file_types=file_types,
            directory_structure=directory_structure,
            naming_conventions=naming_analysis,
            organization_score=organization_score,
            complexity_metrics=complexity_metrics
        )

        return {
            'structure_summary': structure_analysis.__dict__,
            'organization_recommendations': self._generate_organization_recommendations(structure_analysis),
            'structure_quality': self._assess_structure_quality(structure_analysis),
            'scalability_indicators': self._identify_scalability_indicators(structure_analysis)
        }

    def _detect_architectural_patterns(self, extracted_data: Dict[str, Any],
                                     components: Dict[str, Any]) -> Dict[str, Any]:
        """Detect architectural patterns in the design file"""

        detected_patterns = []

        # Detect atomic design pattern
        atomic_pattern = self._detect_atomic_design_pattern(extracted_data, components)
        if atomic_pattern:
            detected_patterns.append(atomic_pattern)

        # Detect component-based architecture
        component_pattern = self._detect_component_architecture(extracted_data, components)
        if component_pattern:
            detected_patterns.append(component_pattern)

        # Detect layered architecture
        layered_pattern = self._detect_layered_architecture(extracted_data)
        if layered_pattern:
            detected_patterns.append(layered_pattern)

        # Detect modular architecture
        modular_pattern = self._detect_modular_architecture(extracted_data, components)
        if modular_pattern:
            detected_patterns.append(modular_pattern)

        # Assess pattern quality
        pattern_quality = self._assess_pattern_quality(detected_patterns)

        return {
            'detected_patterns': [pattern.__dict__ for pattern in detected_patterns],
            'pattern_quality': pattern_quality,
            'architecture_maturity': self._assess_architecture_maturity(detected_patterns),
            'pattern_conflicts': self._identify_pattern_conflicts(detected_patterns),
            'architectural_recommendations': self._generate_architectural_recommendations(detected_patterns)
        }

    def _analyze_data_integrity(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data integrity and consistency"""

        # Check for missing references
        missing_references = self._find_missing_references(extracted_data)

        # Detect circular dependencies
        circular_dependencies = self._detect_circular_dependencies(extracted_data)

        # Find orphaned elements
        orphaned_elements = self._find_orphaned_elements(extracted_data)

        # Identify duplicate content
        duplicate_content = self._find_duplicate_content(extracted_data)

        # Validate data structure
        validation_errors = self._validate_data_structure(extracted_data)

        # Calculate consistency score
        consistency_score = self._calculate_consistency_score(
            missing_references, circular_dependencies, orphaned_elements, validation_errors
        )

        integrity_analysis = DataIntegrityAnalysis(
            consistency_score=consistency_score,
            missing_references=missing_references,
            circular_dependencies=circular_dependencies,
            orphaned_elements=orphaned_elements,
            duplicate_content=duplicate_content,
            validation_errors=validation_errors
        )

        return {
            'integrity_summary': integrity_analysis.__dict__,
            'critical_issues': self._identify_critical_integrity_issues(integrity_analysis),
            'repair_recommendations': self._generate_repair_recommendations(integrity_analysis),
            'data_quality_score': self._calculate_data_quality_score(integrity_analysis)
        }

    def _create_performance_profile(self, extracted_data: Dict[str, Any],
                                  components: Dict[str, Any]) -> Dict[str, Any]:
        """Create performance profile of the design file"""

        # Analyze file size breakdown
        file_size_breakdown = self._analyze_file_sizes(extracted_data)

        # Identify loading bottlenecks
        loading_bottlenecks = self._identify_loading_bottlenecks(extracted_data, components)

        # Find optimization opportunities
        optimization_opportunities = self._find_optimization_opportunities(extracted_data, components)

        # Estimate memory usage
        memory_usage_estimate = self._estimate_memory_usage(extracted_data, components)

        # Assess rendering complexity
        rendering_complexity = self._assess_rendering_complexity(extracted_data, components)

        performance_profile = PerformanceProfile(
            file_size_breakdown=file_size_breakdown,
            loading_bottlenecks=loading_bottlenecks,
            optimization_opportunities=optimization_opportunities,
            memory_usage_estimate=memory_usage_estimate,
            rendering_complexity=rendering_complexity
        )

        return {
            'performance_summary': performance_profile.__dict__,
            'performance_score': self._calculate_performance_score(performance_profile),
            'optimization_priority': self._prioritize_optimizations(performance_profile),
            'performance_recommendations': self._generate_performance_recommendations(performance_profile)
        }

    def _analyze_naming_conventions(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze naming conventions used in the file"""

        # Collect all names from the file
        all_names = self._collect_all_names(extracted_data)

        # Analyze naming patterns
        naming_patterns = self._analyze_naming_patterns(all_names)

        # Check consistency
        consistency_analysis = self._analyze_naming_consistency(all_names)

        # Identify violations
        naming_violations = self._identify_naming_violations(all_names)

        # Assess internationalization
        i18n_analysis = self._analyze_internationalization_naming(all_names)

        return {
            'total_names_analyzed': len(all_names),
            'naming_patterns': naming_patterns,
            'consistency_analysis': consistency_analysis,
            'naming_violations': naming_violations,
            'i18n_analysis': i18n_analysis,
            'naming_recommendations': self._generate_naming_recommendations(consistency_analysis, naming_violations),
            'naming_quality_score': self._calculate_naming_quality_score(consistency_analysis, naming_violations)
        }

    def _analyze_dependencies(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze dependencies within the file"""

        # Build dependency graph
        dependency_graph = self._build_dependency_graph(extracted_data)

        # Analyze dependency complexity
        complexity_analysis = self._analyze_dependency_complexity(dependency_graph)

        # Find dependency cycles
        cycles = self._find_dependency_cycles(dependency_graph)

        # Identify critical dependencies
        critical_dependencies = self._identify_critical_dependencies(dependency_graph)

        # Assess dependency health
        dependency_health = self._assess_dependency_health(dependency_graph, cycles)

        return {
            'dependency_graph': self._serialize_dependency_graph(dependency_graph),
            'complexity_metrics': complexity_analysis,
            'circular_dependencies': cycles,
            'critical_dependencies': critical_dependencies,
            'dependency_health_score': dependency_health,
            'dependency_recommendations': self._generate_dependency_recommendations(dependency_graph, cycles),
            'refactoring_opportunities': self._identify_refactoring_opportunities(dependency_graph)
        }

    def _analyze_version_information(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze version information and compatibility"""

        # Extract version information
        version_info = self._extract_version_information(extracted_data)

        # Check compatibility
        compatibility_analysis = self._analyze_compatibility(version_info)

        # Assess update requirements
        update_requirements = self._assess_update_requirements(version_info)

        # Identify version conflicts
        version_conflicts = self._identify_version_conflicts(version_info)

        return {
            'version_information': version_info,
            'compatibility_analysis': compatibility_analysis,
            'update_requirements': update_requirements,
            'version_conflicts': version_conflicts,
            'migration_path': self._suggest_migration_path(version_info, compatibility_analysis),
            'version_recommendations': self._generate_version_recommendations(version_info, compatibility_analysis)
        }

    def _analyze_metadata_quality(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze quality of metadata throughout the file"""

        # Extract all metadata
        metadata_collection = self._collect_metadata(extracted_data)

        # Assess metadata completeness
        completeness_analysis = self._assess_metadata_completeness(metadata_collection)

        # Check metadata consistency
        consistency_analysis = self._analyze_metadata_consistency(metadata_collection)

        # Validate metadata format
        format_validation = self._validate_metadata_formats(metadata_collection)

        # Assess metadata utility
        utility_analysis = self._assess_metadata_utility(metadata_collection)

        return {
            'metadata_summary': {
                'total_metadata_items': len(metadata_collection),
                'completeness_score': completeness_analysis.get('score', 0),
                'consistency_score': consistency_analysis.get('score', 0),
                'format_compliance': format_validation.get('compliance_rate', 0),
                'utility_score': utility_analysis.get('score', 0)
            },
            'metadata_analysis': {
                'completeness': completeness_analysis,
                'consistency': consistency_analysis,
                'format_validation': format_validation,
                'utility': utility_analysis
            },
            'metadata_recommendations': self._generate_metadata_recommendations(
                completeness_analysis, consistency_analysis, format_validation
            ),
            'metadata_quality_score': self._calculate_metadata_quality_score(
                completeness_analysis, consistency_analysis, format_validation, utility_analysis
            )
        }

    def _assess_scalability(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Assess scalability characteristics of the design file"""

        # Analyze current scale metrics
        current_scale = self._analyze_current_scale(extracted_data, components)

        # Project scalability limits
        scalability_limits = self._project_scalability_limits(current_scale)

        # Identify scalability bottlenecks
        bottlenecks = self._identify_scalability_bottlenecks(extracted_data, components)

        # Assess horizontal scalability
        horizontal_scalability = self._assess_horizontal_scalability(extracted_data, components)

        # Assess vertical scalability
        vertical_scalability = self._assess_vertical_scalability(extracted_data)

        return {
            'current_scale_metrics': current_scale,
            'projected_limits': scalability_limits,
            'scalability_bottlenecks': bottlenecks,
            'horizontal_scalability': horizontal_scalability,
            'vertical_scalability': vertical_scalability,
            'scalability_score': self._calculate_scalability_score(
                current_scale, bottlenecks, horizontal_scalability, vertical_scalability
            ),
            'scaling_recommendations': self._generate_scaling_recommendations(
                bottlenecks, horizontal_scalability, vertical_scalability
            )
        }

    def _analyze_maintenance_aspects(self, extracted_data: Dict[str, Any],
                                   components: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze maintenance aspects of the design file"""

        # Assess maintainability metrics
        maintainability_metrics = self._calculate_maintainability_metrics(extracted_data, components)

        # Identify maintenance risks
        maintenance_risks = self._identify_maintenance_risks(extracted_data, components)

        # Assess documentation quality
        documentation_quality = self._assess_documentation_quality(extracted_data)

        # Analyze change impact patterns
        change_impact = self._analyze_change_impact_patterns(extracted_data, components)

        # Assess testing coverage potential
        testing_coverage = self._assess_testing_coverage_potential(extracted_data, components)

        return {
            'maintainability_metrics': maintainability_metrics,
            'maintenance_risks': maintenance_risks,
            'documentation_quality': documentation_quality,
            'change_impact_analysis': change_impact,
            'testing_coverage_potential': testing_coverage,
            'maintenance_score': self._calculate_maintenance_score(
                maintainability_metrics, maintenance_risks, documentation_quality
            ),
            'maintenance_recommendations': self._generate_maintenance_recommendations(
                maintainability_metrics, maintenance_risks, documentation_quality
            )
        }

    def _assess_migration_readiness(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess readiness for migration to different formats or versions"""

        # Analyze format compatibility
        format_compatibility = self._analyze_format_compatibility(extracted_data)

        # Assess migration complexity
        migration_complexity = self._assess_migration_complexity(extracted_data)

        # Identify migration blockers
        migration_blockers = self._identify_migration_blockers(extracted_data)

        # Estimate migration effort
        migration_effort = self._estimate_migration_effort(extracted_data, migration_complexity)

        # Generate migration plan
        migration_plan = self._generate_migration_plan(extracted_data, migration_complexity, migration_blockers)

        return {
            'format_compatibility': format_compatibility,
            'migration_complexity': migration_complexity,
            'migration_blockers': migration_blockers,
            'effort_estimation': migration_effort,
            'migration_plan': migration_plan,
            'readiness_score': self._calculate_migration_readiness_score(
                format_compatibility, migration_complexity, migration_blockers
            ),
            'migration_recommendations': self._generate_migration_recommendations(
                format_compatibility, migration_blockers, migration_effort
            )
        }

    def _analyze_technical_debt(self, extracted_data: Dict[str, Any],
                              components: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze technical debt in the design file"""

        # Identify structural debt
        structural_debt = self._identify_structural_debt(extracted_data, components)

        # Assess documentation debt
        documentation_debt = self._assess_documentation_debt(extracted_data)

        # Find design inconsistencies
        design_inconsistencies = self._find_design_inconsistencies(extracted_data, components)

        # Identify deprecated patterns
        deprecated_patterns = self._identify_deprecated_patterns(extracted_data, components)

        # Calculate debt impact
        debt_impact = self._calculate_debt_impact(
            structural_debt, documentation_debt, design_inconsistencies, deprecated_patterns
        )

        return {
            'structural_debt': structural_debt,
            'documentation_debt': documentation_debt,
            'design_inconsistencies': design_inconsistencies,
            'deprecated_patterns': deprecated_patterns,
            'debt_impact_analysis': debt_impact,
            'debt_prioritization': self._prioritize_technical_debt(
                structural_debt, documentation_debt, design_inconsistencies, deprecated_patterns
            ),
            'debt_reduction_plan': self._create_debt_reduction_plan(
                structural_debt, documentation_debt, design_inconsistencies, deprecated_patterns
            ),
            'technical_debt_score': self._calculate_technical_debt_score(debt_impact)
        }

    def _generate_optimization_recommendations(self, extracted_data: Dict[str, Any],
                                             components: Dict[str, Any]) -> List[str]:
        """Generate actionable optimization recommendations"""
        recommendations = []

        # File structure optimizations
        file_count = len(extracted_data.get('files', {}))
        if file_count > 100:
            recommendations.append("Consider restructuring large file collections into logical groups")

        # Performance optimizations
        total_objects = sum(
            sum(len(page.get('objects', {})) for page in file_data.get('pages', {}).values())
            for file_data in extracted_data.get('files', {}).values()
        )
        if total_objects > 1000:
            recommendations.append("High object count detected - consider component consolidation")

        # Naming consistency
        recommendations.append("Establish and enforce consistent naming conventions across all elements")

        # Dependency management
        recommendations.append("Implement dependency management strategy to reduce coupling")

        # Documentation improvements
        recommendations.append("Enhance metadata and documentation for better maintainability")

        # Architecture improvements
        recommendations.append("Consider implementing atomic design principles for better organization")

        return recommendations

    def _calculate_file_health_score(self, extracted_data: Dict[str, Any],
                                   components: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall file health score"""

        # Individual component scores
        structure_score = self._calculate_structure_health_score(extracted_data)
        integrity_score = self._calculate_integrity_health_score(extracted_data)
        performance_score = self._calculate_performance_health_score(extracted_data, components)
        maintainability_score = self._calculate_maintainability_health_score(extracted_data, components)

        # Weighted overall score
        weights = {
            'structure': 0.25,
            'integrity': 0.30,
            'performance': 0.25,
            'maintainability': 0.20
        }

        overall_score = (
            structure_score * weights['structure'] +
            integrity_score * weights['integrity'] +
            performance_score * weights['performance'] +
            maintainability_score * weights['maintainability']
        )

        # Determine health grade
        health_grade = self._determine_health_grade(overall_score)

        return {
            'overall_score': overall_score,
            'health_grade': health_grade,
            'component_scores': {
                'structure': structure_score,
                'integrity': integrity_score,
                'performance': performance_score,
                'maintainability': maintainability_score
            },
            'score_weights': weights,
            'health_assessment': self._generate_health_assessment(overall_score, health_grade),
            'improvement_priorities': self._identify_improvement_priorities({
                'structure': structure_score,
                'integrity': integrity_score,
                'performance': performance_score,
                'maintainability': maintainability_score
            })
        }

    # Helper methods (simplified implementations for brevity)

    def _build_directory_structure(self, files_data: Dict[str, Any]) -> Dict[str, Any]:
        """Build directory structure representation"""
        structure = {}
        for file_id, file_data in files_data.items():
            structure[file_id] = {
                'pages': len(file_data.get('pages', {})),
                'objects': file_data.get('objects_count', 0),
                'type': 'design_file'
            }
        return structure

    def _analyze_file_types(self, files_data: Dict[str, Any]) -> Dict[str, int]:
        """Analyze distribution of file types"""
        file_types = {'design_files': len(files_data)}
        return file_types

    def _assess_naming_conventions(self, files_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess naming convention consistency"""
        all_names = []
        for file_data in files_data.values():
            for page_data in file_data.get('pages', {}).values():
                for obj in page_data.get('objects', {}).values():
                    if 'name' in obj:
                        all_names.append(obj['name'])

        # Analyze patterns
        patterns = {
            'camelCase': sum(1 for name in all_names if re.match(r'^[a-z][a-zA-Z0-9]*$', name)),
            'snake_case': sum(1 for name in all_names if re.match(r'^[a-z][a-z0-9_]*$', name)),
            'kebab-case': sum(1 for name in all_names if re.match(r'^[a-z][a-z0-9\-]*$', name))
        }

        total_names = len(all_names)
        consistency_score = max(patterns.values()) / total_names if total_names > 0 else 0

        return {
            'total_names': total_names,
            'patterns': patterns,
            'consistency_score': consistency_score,
            'dominant_pattern': max(patterns.keys(), key=lambda k: patterns[k]) if patterns else 'none'
        }

    def _calculate_organization_score(self, directory_structure: Dict[str, Any],
                                    naming_analysis: Dict[str, Any]) -> float:
        """Calculate file organization score"""
        # Simple scoring based on structure depth and naming consistency
        structure_score = min(1.0, len(directory_structure) / 10)  # Normalize to 0-1
        naming_score = naming_analysis.get('consistency_score', 0)

        return (structure_score + naming_score) / 2

    def _calculate_complexity_metrics(self, files_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate complexity metrics"""
        total_objects = sum(
            sum(len(page.get('objects', {})) for page in file_data.get('pages', {}).values())
            for file_data in files_data.values()
        )

        return {
            'total_objects': total_objects,
            'files_count': len(files_data),
            'avg_objects_per_file': total_objects / len(files_data) if files_data else 0,
            'complexity_level': 'high' if total_objects > 1000 else 'medium' if total_objects > 100 else 'low'
        }

    def _detect_atomic_design_pattern(self, extracted_data: Dict[str, Any],
                                    components: Dict[str, Any]) -> Optional[ArchitecturalPattern]:
        """Detect atomic design pattern"""
        detected_components = components.get('detected_components', [])
        categories = Counter(comp.get('category', 'unknown') for comp in detected_components)

        # Check if atomic design categories are present
        atomic_categories = ['atoms', 'molecules', 'organisms', 'templates', 'pages']
        present_categories = [cat for cat in atomic_categories if cat in categories]

        if len(present_categories) >= 3:
            return ArchitecturalPattern(
                pattern_name='Atomic Design',
                pattern_type='component_architecture',
                confidence=len(present_categories) / len(atomic_categories),
                evidence=[f"Found {categories[cat]} {cat}" for cat in present_categories],
                implications=['Scalable component hierarchy', 'Consistent design language'],
                recommendations=['Complete missing atomic levels', 'Establish clear component guidelines']
            )

        return None

    def _detect_component_architecture(self, extracted_data: Dict[str, Any],
                                     components: Dict[str, Any]) -> Optional[ArchitecturalPattern]:
        """Detect component-based architecture"""
        detected_components = components.get('detected_components', [])
        reusable_components = [comp for comp in detected_components if len(comp.get('instances', [])) > 1]

        if len(reusable_components) >= 3:
            return ArchitecturalPattern(
                pattern_name='Component-Based Architecture',
                pattern_type='reusability_architecture',
                confidence=len(reusable_components) / len(detected_components) if detected_components else 0,
                evidence=[f"Found {len(reusable_components)} reusable components"],
                implications=['Code reusability', 'Consistent UI patterns'],
                recommendations=['Increase component reuse', 'Establish component library']
            )

        return None

    def _find_missing_references(self, extracted_data: Dict[str, Any]) -> List[str]:
        """Find missing references in the data"""
        missing_refs = []
        # Simplified implementation
        return missing_refs

    def _detect_circular_dependencies(self, extracted_data: Dict[str, Any]) -> List[str]:
        """Detect circular dependencies"""
        circular_deps = []
        # Simplified implementation
        return circular_deps

    def _find_orphaned_elements(self, extracted_data: Dict[str, Any]) -> List[str]:
        """Find orphaned elements"""
        orphaned = []
        # Simplified implementation
        return orphaned

    def _find_duplicate_content(self, extracted_data: Dict[str, Any]) -> List[str]:
        """Find duplicate content"""
        duplicates = []
        content_hashes = {}

        for file_data in extracted_data.get('files', {}).values():
            for page_data in file_data.get('pages', {}).values():
                for obj_id, obj in page_data.get('objects', {}).items():
                    # Create hash of object properties
                    obj_str = json.dumps(obj, sort_keys=True)
                    obj_hash = hashlib.md5(obj_str.encode()).hexdigest()

                    if obj_hash in content_hashes:
                        duplicates.append(f"Duplicate: {obj_id} matches {content_hashes[obj_hash]}")
                    else:
                        content_hashes[obj_hash] = obj_id

        return duplicates

    def _validate_data_structure(self, extracted_data: Dict[str, Any]) -> List[str]:
        """Validate data structure integrity"""
        validation_errors = []

        # Check required fields
        if 'files' not in extracted_data:
            validation_errors.append("Missing 'files' key in root data")

        for file_id, file_data in extracted_data.get('files', {}).items():
            if 'pages' not in file_data:
                validation_errors.append(f"Missing 'pages' key in file {file_id}")

        return validation_errors

    def _calculate_consistency_score(self, missing_refs: List[str], circular_deps: List[str],
                                   orphaned: List[str], validation_errors: List[str]) -> float:
        """Calculate data consistency score"""
        total_issues = len(missing_refs) + len(circular_deps) + len(orphaned) + len(validation_errors)
        # Simple scoring: fewer issues = higher score
        return max(0, 1 - (total_issues / 100))  # Normalize to 0-1

    def _analyze_file_sizes(self, extracted_data: Dict[str, Any]) -> Dict[str, int]:
        """Analyze file size breakdown"""
        # Simplified size estimation based on content
        sizes = {}
        for file_id, file_data in extracted_data.get('files', {}).items():
            # Estimate size based on object count
            object_count = file_data.get('objects_count', 0)
            estimated_size = object_count * 1024  # 1KB per object (rough estimate)
            sizes[file_id] = estimated_size

        return sizes

    def _identify_loading_bottlenecks(self, extracted_data: Dict[str, Any],
                                    components: Dict[str, Any]) -> List[str]:
        """Identify potential loading bottlenecks"""
        bottlenecks = []

        # Check for large files
        for file_id, file_data in extracted_data.get('files', {}).items():
            object_count = file_data.get('objects_count', 0)
            if object_count > self.performance_thresholds['object_count_warning']:
                bottlenecks.append(f"File {file_id} has {object_count} objects (high)")

        return bottlenecks

    def _find_optimization_opportunities(self, extracted_data: Dict[str, Any],
                                       components: Dict[str, Any]) -> List[str]:
        """Find optimization opportunities"""
        opportunities = []

        # Check component reusability
        detected_components = components.get('detected_components', [])
        single_use_components = [comp for comp in detected_components if len(comp.get('instances', [])) == 1]

        if len(single_use_components) > 5:
            opportunities.append(f"Found {len(single_use_components)} single-use components that could be generalized")

        # Check for duplicate objects
        duplicate_count = len(self._find_duplicate_content(extracted_data))
        if duplicate_count > 0:
            opportunities.append(f"Remove {duplicate_count} duplicate objects")

        return opportunities

    def _estimate_memory_usage(self, extracted_data: Dict[str, Any],
                             components: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate memory usage"""
        total_objects = sum(
            sum(len(page.get('objects', {})) for page in file_data.get('pages', {}).values())
            for file_data in extracted_data.get('files', {}).values()
        )

        # Rough estimates
        estimated_memory = {
            'objects_memory': total_objects * 100,  # 100 bytes per object
            'metadata_memory': len(extracted_data.get('files', {})) * 50,  # 50 bytes per file
            'total_estimated': total_objects * 100 + len(extracted_data.get('files', {})) * 50
        }

        return estimated_memory

    def _assess_rendering_complexity(self, extracted_data: Dict[str, Any],
                                   components: Dict[str, Any]) -> Dict[str, Any]:
        """Assess rendering complexity"""
        total_objects = sum(
            sum(len(page.get('objects', {})) for page in file_data.get('pages', {}).values())
            for file_data in extracted_data.get('files', {}).values()
        )

        complexity_level = 'low'
        if total_objects > 1000:
            complexity_level = 'high'
        elif total_objects > 100:
            complexity_level = 'medium'

        return {
            'total_render_objects': total_objects,
            'complexity_level': complexity_level,
            'estimated_render_time': total_objects * 0.001  # 1ms per object estimate
        }

    # Additional helper methods with simplified implementations

    def _collect_all_names(self, extracted_data: Dict[str, Any]) -> List[str]:
        """Collect all names from the file"""
        names = []
        for file_data in extracted_data.get('files', {}).values():
            for page_data in file_data.get('pages', {}).values():
                for obj in page_data.get('objects', {}).values():
                    if 'name' in obj and obj['name']:
                        names.append(obj['name'])
        return names

    def _analyze_naming_patterns(self, names: List[str]) -> Dict[str, Any]:
        """Analyze naming patterns"""
        patterns = {
            'camelCase': sum(1 for name in names if re.match(r'^[a-z][a-zA-Z0-9]*$', name)),
            'PascalCase': sum(1 for name in names if re.match(r'^[A-Z][a-zA-Z0-9]*$', name)),
            'snake_case': sum(1 for name in names if re.match(r'^[a-z][a-z0-9_]*$', name)),
            'kebab-case': sum(1 for name in names if re.match(r'^[a-z][a-z0-9\-]*$', name)),
            'UPPER_CASE': sum(1 for name in names if re.match(r'^[A-Z][A-Z0-9_]*$', name))
        }
        return patterns

    def _analyze_naming_consistency(self, names: List[str]) -> Dict[str, Any]:
        """Analyze naming consistency"""
        if not names:
            return {'consistency_score': 1.0, 'dominant_pattern': 'none'}

        patterns = self._analyze_naming_patterns(names)
        total = len(names)
        max_pattern = max(patterns.values())

        return {
            'consistency_score': max_pattern / total,
            'dominant_pattern': max(patterns.keys(), key=lambda k: patterns[k]),
            'pattern_distribution': patterns
        }

    def _identify_naming_violations(self, names: List[str]) -> List[str]:
        """Identify naming violations"""
        violations = []
        for name in names:
            if len(name) < 2:
                violations.append(f"Name too short: '{name}'")
            if len(name) > 50:
                violations.append(f"Name too long: '{name[:20]}...'")
            if re.search(r'[^a-zA-Z0-9_\-]', name):
                violations.append(f"Invalid characters in name: '{name}'")
        return violations

    def _analyze_internationalization_naming(self, names: List[str]) -> Dict[str, Any]:
        """Analyze internationalization aspects of naming"""
        non_ascii_names = [name for name in names if not name.isascii()]
        return {
            'non_ascii_names': len(non_ascii_names),
            'i18n_ready': len(non_ascii_names) == 0,
            'examples': non_ascii_names[:5]
        }

    # Continue with more simplified helper method implementations...

    def _build_dependency_graph(self, extracted_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Build dependency graph (simplified)"""
        return {}  # Placeholder

    def _calculate_structure_health_score(self, extracted_data: Dict[str, Any]) -> float:
        """Calculate structure health score"""
        return 0.8  # Placeholder

    def _calculate_integrity_health_score(self, extracted_data: Dict[str, Any]) -> float:
        """Calculate integrity health score"""
        return 0.9  # Placeholder

    def _calculate_performance_health_score(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> float:
        """Calculate performance health score"""
        return 0.7  # Placeholder

    def _calculate_maintainability_health_score(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> float:
        """Calculate maintainability health score"""
        return 0.75  # Placeholder

    def _determine_health_grade(self, score: float) -> str:
        """Determine health grade from score"""
        if score >= 0.9: return 'A'
        elif score >= 0.8: return 'B'
        elif score >= 0.7: return 'C'
        elif score >= 0.6: return 'D'
        else: return 'F'

    def _generate_health_assessment(self, score: float, grade: str) -> str:
        """Generate health assessment description"""
        assessments = {
            'A': 'Excellent file health with minimal issues',
            'B': 'Good file health with minor improvements needed',
            'C': 'Fair file health with some issues to address',
            'D': 'Poor file health requiring attention',
            'F': 'Critical file health issues requiring immediate action'
        }
        return assessments.get(grade, 'Unknown health status')

    def _identify_improvement_priorities(self, scores: Dict[str, float]) -> List[str]:
        """Identify improvement priorities based on component scores"""
        sorted_scores = sorted(scores.items(), key=lambda x: x[1])
        return [f"Improve {area} (score: {score:.2f})" for area, score in sorted_scores[:2]]

    # Additional placeholder methods for completeness
    def _generate_organization_recommendations(self, structure: FileStructureAnalysis) -> List[str]:
        return ["Improve file organization", "Establish naming conventions"]

    def _assess_structure_quality(self, structure: FileStructureAnalysis) -> str:
        return "good" if structure.organization_score > 0.7 else "needs_improvement"

    def _identify_scalability_indicators(self, structure: FileStructureAnalysis) -> List[str]:
        return ["Component reusability", "Modular structure"]

    def _detect_layered_architecture(self, extracted_data: Dict[str, Any]) -> Optional[ArchitecturalPattern]:
        return None  # Placeholder

    def _detect_modular_architecture(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Optional[ArchitecturalPattern]:
        return None  # Placeholder

    def _assess_pattern_quality(self, patterns: List[ArchitecturalPattern]) -> Dict[str, Any]:
        return {"quality_score": 0.8, "pattern_consistency": "good"}

    def _assess_architecture_maturity(self, patterns: List[ArchitecturalPattern]) -> float:
        return len(patterns) / 5  # Simple scoring

    def _identify_pattern_conflicts(self, patterns: List[ArchitecturalPattern]) -> List[str]:
        return []  # Placeholder

    def _generate_architectural_recommendations(self, patterns: List[ArchitecturalPattern]) -> List[str]:
        return ["Establish consistent architectural patterns"]

    # Continue with remaining placeholder implementations...
    def _identify_critical_integrity_issues(self, integrity: DataIntegrityAnalysis) -> List[str]:
        return [issue for issue in integrity.validation_errors if "critical" in issue.lower()]

    def _generate_repair_recommendations(self, integrity: DataIntegrityAnalysis) -> List[str]:
        recommendations = []
        if integrity.missing_references:
            recommendations.append("Fix missing references")
        if integrity.circular_dependencies:
            recommendations.append("Resolve circular dependencies")
        return recommendations

    def _calculate_data_quality_score(self, integrity: DataIntegrityAnalysis) -> float:
        return integrity.consistency_score

    def _calculate_performance_score(self, profile: PerformanceProfile) -> float:
        # Simple scoring based on bottlenecks
        bottleneck_count = len(profile.loading_bottlenecks)
        return max(0, 1 - (bottleneck_count / 10))

    def _prioritize_optimizations(self, profile: PerformanceProfile) -> List[str]:
        return sorted(profile.optimization_opportunities, key=len)

    def _generate_performance_recommendations(self, profile: PerformanceProfile) -> List[str]:
        return ["Optimize large files", "Reduce object complexity"]

    def _generate_naming_recommendations(self, consistency: Dict[str, Any], violations: List[str]) -> List[str]:
        recommendations = []
        if consistency.get('consistency_score', 0) < 0.8:
            recommendations.append("Establish consistent naming conventions")
        if violations:
            recommendations.append("Fix naming violations")
        return recommendations

    def _calculate_naming_quality_score(self, consistency: Dict[str, Any], violations: List[str]) -> float:
        consistency_score = consistency.get('consistency_score', 0)
        violation_penalty = min(0.5, len(violations) / 20)
        return max(0, consistency_score - violation_penalty)

    # Additional simplified methods for dependency analysis
    def _analyze_dependency_complexity(self, graph: Dict[str, List[str]]) -> Dict[str, Any]:
        return {"complexity": "medium", "node_count": len(graph)}

    def _find_dependency_cycles(self, graph: Dict[str, List[str]]) -> List[str]:
        return []  # Placeholder

    def _identify_critical_dependencies(self, graph: Dict[str, List[str]]) -> List[str]:
        return []  # Placeholder

    def _assess_dependency_health(self, graph: Dict[str, List[str]], cycles: List[str]) -> float:
        return 0.8  # Placeholder

    def _serialize_dependency_graph(self, graph: Dict[str, List[str]]) -> Dict[str, Any]:
        return {"nodes": len(graph), "edges": sum(len(deps) for deps in graph.values())}

    def _generate_dependency_recommendations(self, graph: Dict[str, List[str]], cycles: List[str]) -> List[str]:
        return ["Reduce coupling", "Eliminate cycles"]

    def _identify_refactoring_opportunities(self, graph: Dict[str, List[str]]) -> List[str]:
        return ["Extract common dependencies"]

    # Version analysis methods
    def _extract_version_information(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"format_version": "1.0", "tool_version": "unknown"}

    def _analyze_compatibility(self, version_info: Dict[str, Any]) -> Dict[str, Any]:
        return {"compatible": True, "issues": []}

    def _assess_update_requirements(self, version_info: Dict[str, Any]) -> Dict[str, Any]:
        return {"update_needed": False, "urgency": "low"}

    def _identify_version_conflicts(self, version_info: Dict[str, Any]) -> List[str]:
        return []

    def _suggest_migration_path(self, version_info: Dict[str, Any], compatibility: Dict[str, Any]) -> List[str]:
        return ["No migration needed"]

    def _generate_version_recommendations(self, version_info: Dict[str, Any], compatibility: Dict[str, Any]) -> List[str]:
        return ["Keep current version"]

    # Metadata analysis methods
    def _collect_metadata(self, extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        metadata = []
        for file_data in extracted_data.get('files', {}).values():
            if file_data.get('metadata'):
                metadata.append(file_data['metadata'])
        return metadata

    def _assess_metadata_completeness(self, metadata_collection: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"score": 0.7, "missing_fields": ["description"]}

    def _analyze_metadata_consistency(self, metadata_collection: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"score": 0.8, "inconsistencies": []}

    def _validate_metadata_formats(self, metadata_collection: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"compliance_rate": 0.9, "format_errors": []}

    def _assess_metadata_utility(self, metadata_collection: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"score": 0.6, "utility_assessment": "moderate"}

    def _generate_metadata_recommendations(self, *args) -> List[str]:
        return ["Add missing metadata fields", "Standardize metadata formats"]

    def _calculate_metadata_quality_score(self, *args) -> float:
        return 0.75

    # Remaining simplified method implementations would continue here...
    # For brevity, I'll provide placeholders for the remaining methods

    def _analyze_current_scale(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        return {"files": len(extracted_data.get('files', {})), "components": len(components.get('detected_components', []))}

    def _project_scalability_limits(self, current_scale: Dict[str, Any]) -> Dict[str, Any]:
        return {"projected_limit": "1000 files", "timeline": "2 years"}

    def _identify_scalability_bottlenecks(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> List[str]:
        return ["Large file sizes", "Deep nesting"]

    def _assess_horizontal_scalability(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        return {"scalability": "good", "recommendations": ["Modularize components"]}

    def _assess_vertical_scalability(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"scalability": "limited", "constraints": ["Memory usage"]}

    def _calculate_scalability_score(self, *args) -> float:
        return 0.7

    def _generate_scaling_recommendations(self, *args) -> List[str]:
        return ["Implement component splitting", "Optimize file structure"]

    # Continue with maintenance, migration, and technical debt methods...
    def _calculate_maintainability_metrics(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        return {"maintainability_index": 0.8, "cyclomatic_complexity": "medium"}

    def _identify_maintenance_risks(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> List[str]:
        return ["Tight coupling", "Large file sizes"]

    def _assess_documentation_quality(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"quality_score": 0.6, "coverage": "partial"}

    def _analyze_change_impact_patterns(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        return {"impact_level": "medium", "affected_components": 5}

    def _assess_testing_coverage_potential(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        return {"testable_components": 10, "coverage_potential": "high"}

    def _calculate_maintenance_score(self, *args) -> float:
        return 0.75

    def _generate_maintenance_recommendations(self, *args) -> List[str]:
        return ["Improve documentation", "Reduce coupling"]

    # Migration readiness methods
    def _analyze_format_compatibility(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"compatibility_score": 0.9, "supported_formats": ["figma", "sketch"]}

    def _assess_migration_complexity(self, extracted_data: Dict[str, Any]) -> str:
        return "medium"

    def _identify_migration_blockers(self, extracted_data: Dict[str, Any]) -> List[str]:
        return ["Custom properties", "Complex animations"]

    def _estimate_migration_effort(self, extracted_data: Dict[str, Any], complexity: str) -> Dict[str, Any]:
        return {"effort": "40 hours", "complexity": complexity}

    def _generate_migration_plan(self, *args) -> List[str]:
        return ["Phase 1: Prepare data", "Phase 2: Convert format", "Phase 3: Validate"]

    def _calculate_migration_readiness_score(self, *args) -> float:
        return 0.8

    def _generate_migration_recommendations(self, *args) -> List[str]:
        return ["Address blockers first", "Plan phased migration"]

    # Technical debt methods
    def _identify_structural_debt(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> List[str]:
        return ["Inconsistent component structure", "Missing abstractions"]

    def _assess_documentation_debt(self, extracted_data: Dict[str, Any]) -> List[str]:
        return ["Missing component descriptions", "Outdated metadata"]

    def _find_design_inconsistencies(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> List[str]:
        return ["Inconsistent naming", "Style variations"]

    def _identify_deprecated_patterns(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> List[str]:
        return ["Old layout patterns", "Deprecated component types"]

    def _calculate_debt_impact(self, *args) -> Dict[str, Any]:
        return {"impact_score": 0.6, "maintenance_cost": "high"}

    def _prioritize_technical_debt(self, *args) -> List[str]:
        return ["Fix structural issues first", "Update documentation", "Address inconsistencies"]

    def _create_debt_reduction_plan(self, *args) -> List[str]:
        return ["Month 1: Structural fixes", "Month 2: Documentation", "Month 3: Consistency"]

    def _calculate_technical_debt_score(self, debt_impact: Dict[str, Any]) -> float:
        return 1 - debt_impact.get('impact_score', 0.5)