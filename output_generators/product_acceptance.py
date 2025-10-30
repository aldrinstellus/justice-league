"""
Product Acceptance Criteria Generator
Converts analysis results into structured product acceptance criteria
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class AcceptanceCriterion:
    """Individual acceptance criterion"""
    id: str
    given: str
    when: str
    then: str
    additional_details: Optional[str] = None


@dataclass
class UserStory:
    """Complete user story with acceptance criteria"""
    id: str
    title: str
    user_story: str
    acceptance_criteria: List[AcceptanceCriterion]
    definition_of_done: List[str]
    business_rules: List[str]
    priority: str
    effort_estimate: str
    epic: str
    feature: str
    tags: List[str]


@dataclass
class Epic:
    """Epic containing multiple user stories"""
    id: str
    title: str
    description: str
    business_value: str
    user_stories: List[str]  # Story IDs
    success_metrics: List[str]


class ProductAcceptanceCriteriaGenerator:
    """Generate structured product acceptance criteria from analysis results"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive product acceptance criteria

        Args:
            analysis_results: Complete analysis results from all personas

        Returns:
            Structured acceptance criteria in multiple formats
        """
        self.logger.info("Generating product acceptance criteria")

        try:
            # Extract relevant data from analysis results
            pm_analysis = analysis_results.get('persona_analyses', {}).get('product_manager', {})
            design_analysis = analysis_results.get('persona_analyses', {}).get('product_designer', {})
            extracted_data = analysis_results.get('extracted_data', {})
            components = analysis_results.get('components', {})

            # Generate structured acceptance criteria
            acceptance_criteria = {
                'metadata': self._generate_metadata(analysis_results),
                'epics': self._generate_epics(pm_analysis, extracted_data, components),
                'user_stories': self._generate_user_stories(pm_analysis, design_analysis, extracted_data, components),
                'business_rules': self._extract_business_rules(pm_analysis, extracted_data),
                'success_metrics': self._define_success_metrics(pm_analysis),
                'constraints': self._identify_constraints(analysis_results),
                'assumptions': self._document_assumptions(analysis_results),
                'testing_scenarios': self._generate_testing_scenarios(analysis_results),
                'implementation_notes': self._generate_implementation_notes(analysis_results)
            }

            self.logger.info("Product acceptance criteria generation completed")
            return acceptance_criteria

        except Exception as e:
            self.logger.error(f"Product acceptance criteria generation failed: {str(e)}")
            raise

    def _generate_metadata(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate metadata for the acceptance criteria document"""
        return {
            'document_type': 'Product Acceptance Criteria',
            'version': '1.0.0',
            'generated_at': datetime.now().isoformat(),
            'source_file': analysis_results.get('metadata', {}).get('input_file', 'Unknown'),
            'project_name': self._extract_project_name(analysis_results),
            'stakeholders': self._identify_stakeholders(analysis_results),
            'total_user_stories': 0,  # Will be updated after generation
            'total_acceptance_criteria': 0,  # Will be updated after generation
            'priority_breakdown': {'high': 0, 'medium': 0, 'low': 0}
        }

    def _generate_epics(self, pm_analysis: Dict[str, Any], extracted_data: Dict[str, Any], components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate epics from analysis results"""
        epics = []

        # Main application epic
        main_epic = Epic(
            id='EP-001',
            title='Grant Application Management System',
            description='Complete system for managing grant applications from submission to approval',
            business_value='Streamline grant application process, reduce processing time by 40%, improve user experience',
            user_stories=[],  # Will be populated when stories are created
            success_metrics=[
                'Application completion rate > 85%',
                'Processing time reduced by 40%',
                'User satisfaction score > 4.2/5',
                'System uptime > 99.5%'
            ]
        )
        epics.append(asdict(main_epic))

        # User management epic (if applicable)
        if self._has_user_management_features(extracted_data, components):
            user_epic = Epic(
                id='EP-002',
                title='User Management and Authentication',
                description='User account creation, authentication, and profile management',
                business_value='Secure user access, personalized experience, application tracking',
                user_stories=[],
                success_metrics=[
                    'Account creation success rate > 95%',
                    'Authentication failure rate < 2%',
                    'Password reset completion rate > 90%'
                ]
            )
            epics.append(asdict(user_epic))

        # Document management epic
        document_epic = Epic(
            id='EP-003',
            title='Document Management and File Handling',
            description='Secure upload, validation, and management of application documents',
            business_value='Ensure complete applications, reduce manual document processing',
            user_stories=[],
            success_metrics=[
                'File upload success rate > 98%',
                'Document validation accuracy > 99%',
                'File corruption incidents < 0.1%'
            ]
        )
        epics.append(asdict(document_epic))

        return epics

    def _generate_user_stories(self, pm_analysis: Dict[str, Any], design_analysis: Dict[str, Any], extracted_data: Dict[str, Any], components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate detailed user stories with acceptance criteria"""
        user_stories = []

        # Extract existing user stories from PM analysis
        existing_stories = pm_analysis.get('user_stories', [])

        # Enhance with additional stories based on component analysis
        component_based_stories = self._generate_component_based_stories(components, extracted_data)

        # Combine and enhance stories
        all_stories = existing_stories + component_based_stories

        story_counter = 1
        for story_data in all_stories:
            enhanced_story = self._enhance_user_story(story_data, story_counter, design_analysis)
            user_stories.append(enhanced_story)
            story_counter += 1

        # Generate additional critical stories
        critical_stories = self._generate_critical_user_stories(extracted_data, components)
        for story_data in critical_stories:
            enhanced_story = self._enhance_user_story(story_data, story_counter, design_analysis)
            user_stories.append(enhanced_story)
            story_counter += 1

        return user_stories

    def _enhance_user_story(self, story_data: Dict[str, Any], story_number: int, design_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance a user story with detailed acceptance criteria"""
        story_id = story_data.get('id', f'US-{story_number:03d}')

        # Convert acceptance criteria to structured format
        acceptance_criteria = []
        criteria_list = story_data.get('acceptance_criteria', [])

        for i, criterion_text in enumerate(criteria_list):
            if criterion_text.startswith('Given'):
                # Parse Given-When-Then format
                parts = criterion_text.split('When')
                given_part = parts[0].replace('Given', '').strip()

                if len(parts) > 1:
                    then_parts = parts[1].split('Then')
                    when_part = then_parts[0].strip()
                    then_part = then_parts[1].strip() if len(then_parts) > 1 else 'System responds appropriately'
                else:
                    when_part = 'User performs expected action'
                    then_part = 'System responds appropriately'

                acceptance_criteria.append(AcceptanceCriterion(
                    id=f'{story_id}-AC-{i+1:02d}',
                    given=given_part,
                    when=when_part,
                    then=then_part
                ))
            else:
                # Convert non-standard format to Given-When-Then
                acceptance_criteria.append(AcceptanceCriterion(
                    id=f'{story_id}-AC-{i+1:02d}',
                    given='User is in the application',
                    when=f'User {criterion_text.lower()}',
                    then='System behaves as expected'
                ))

        # Add design-specific acceptance criteria
        if design_analysis:
            design_criteria = self._generate_design_acceptance_criteria(story_data, design_analysis)
            acceptance_criteria.extend(design_criteria)

        # Create enhanced user story
        enhanced_story = UserStory(
            id=story_id,
            title=story_data.get('title', f'User Story {story_number}'),
            user_story=story_data.get('user_story', ''),
            acceptance_criteria=[asdict(ac) for ac in acceptance_criteria],
            definition_of_done=story_data.get('definition_of_done', []),
            business_rules=story_data.get('business_rules', []),
            priority=story_data.get('priority', 'Medium'),
            effort_estimate=story_data.get('effort_estimate', 'TBD'),
            epic=self._assign_epic(story_data),
            feature=self._assign_feature(story_data),
            tags=self._generate_story_tags(story_data)
        )

        return asdict(enhanced_story)

    def _generate_component_based_stories(self, components: Dict[str, Any], extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate user stories based on component analysis"""
        stories = []

        component_inventory = components.get('component_inventory', {}).get('components', {})

        # File upload story if upload components detected
        if any('upload' in comp.lower() for comp in component_inventory.keys()):
            stories.append({
                'title': 'Document Upload and Validation',
                'user_story': 'As an applicant, I want to upload required documents, so that I can complete my grant application',
                'acceptance_criteria': [
                    'Given I am on the document upload section',
                    'When I select valid files (PDF, JPEG, Docx, Xlsx)',
                    'Then the files are uploaded successfully',
                    'And I see confirmation of successful upload',
                    'And the system validates file formats and sizes'
                ],
                'definition_of_done': [
                    'Multiple file formats supported',
                    'File size validation implemented',
                    'Progress indicators shown during upload',
                    'Error handling for failed uploads'
                ],
                'business_rules': [
                    'Maximum file size: 10MB per file',
                    'Supported formats: PDF, JPEG, Docx, Xlsx',
                    'Virus scanning on all uploaded files'
                ],
                'priority': 'High',
                'effort_estimate': '5 story points'
            })

        # Table/data display story if table components detected
        if any('table' in comp.lower() for comp in component_inventory.keys()):
            stories.append({
                'title': 'Application Data Display and Management',
                'user_story': 'As a staff member, I want to view application data in organized tables, so that I can efficiently review submissions',
                'acceptance_criteria': [
                    'Given I have access to the application review interface',
                    'When I navigate to the applications list',
                    'Then I see applications displayed in a sortable table',
                    'And I can filter applications by status, date, or amount',
                    'And I can access individual application details'
                ],
                'definition_of_done': [
                    'Sortable columns implemented',
                    'Filtering functionality working',
                    'Pagination for large datasets',
                    'Export functionality available'
                ],
                'business_rules': [
                    'Only authorized staff can view application data',
                    'Audit trail maintained for all access',
                    'Data display follows government accessibility standards'
                ],
                'priority': 'Medium',
                'effort_estimate': '8 story points'
            })

        return stories

    def _generate_critical_user_stories(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate critical user stories not covered by existing analysis"""
        critical_stories = []

        # Error handling story
        critical_stories.append({
            'title': 'Error Handling and User Feedback',
            'user_story': 'As an applicant, I want to receive clear feedback when errors occur, so that I can correct issues and complete my application',
            'acceptance_criteria': [
                'Given an error occurs during form submission',
                'When the system detects the error',
                'Then I see a clear, actionable error message',
                'And the error message explains how to fix the issue',
                'And my form data is preserved where possible'
            ],
            'definition_of_done': [
                'Error messages are user-friendly',
                'Form data preservation implemented',
                'Error logging for support purposes',
                'Accessibility compliance for error states'
            ],
            'business_rules': [
                'Error messages must not expose sensitive system information',
                'All errors must be logged for monitoring',
                'Critical errors require immediate notification'
            ],
            'priority': 'High',
            'effort_estimate': '5 story points'
        })

        # Accessibility story
        critical_stories.append({
            'title': 'Accessibility Compliance',
            'user_story': 'As a user with disabilities, I want the application to be fully accessible, so that I can independently complete my grant application',
            'acceptance_criteria': [
                'Given I am using assistive technology',
                'When I navigate through the application',
                'Then all content is accessible via screen reader',
                'And all interactive elements are keyboard navigable',
                'And color contrast meets WCAG AA standards'
            ],
            'definition_of_done': [
                'WCAG 2.1 AA compliance achieved',
                'Automated accessibility testing integrated',
                'Manual accessibility testing completed',
                'Accessibility statement published'
            ],
            'business_rules': [
                'Must comply with Section 508 requirements',
                'All form fields must have proper labels',
                'Focus indicators must be visible'
            ],
            'priority': 'High',
            'effort_estimate': '13 story points'
        })

        return critical_stories

    def _generate_design_acceptance_criteria(self, story_data: Dict[str, Any], design_analysis: Dict[str, Any]) -> List[AcceptanceCriterion]:
        """Generate design-specific acceptance criteria"""
        design_criteria = []

        story_title = story_data.get('title', '').lower()

        if 'form' in story_title or 'input' in story_title:
            design_criteria.append(AcceptanceCriterion(
                id=f"{story_data.get('id', 'US-000')}-DC-01",
                given='I am interacting with form elements',
                when='I focus on input fields',
                then='I see clear visual focus indicators',
                additional_details='Focus indicators must meet WCAG contrast requirements'
            ))

        if 'button' in story_title or 'submit' in story_title:
            design_criteria.append(AcceptanceCriterion(
                id=f"{story_data.get('id', 'US-000')}-DC-02",
                given='I am using interactive buttons',
                when='I hover over or click buttons',
                then='I see appropriate visual feedback',
                additional_details='Button states: default, hover, active, disabled, loading'
            ))

        return design_criteria

    def _extract_business_rules(self, pm_analysis: Dict[str, Any], extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract and structure business rules"""
        business_rules = []

        # Extract rules from PM analysis
        pm_rules = pm_analysis.get('business_requirements', [])
        for req in pm_rules:
            success_criteria = req.get('success_criteria', [])
            for criterion in success_criteria:
                business_rules.append({
                    'id': f"BR-{len(business_rules) + 1:03d}",
                    'category': 'Compliance',
                    'rule': criterion,
                    'source': req.get('title', 'Business Requirement'),
                    'priority': req.get('priority', 'Medium'),
                    'enforcement': 'System must enforce this rule'
                })

        # Add domain-specific rules
        text_content = self._extract_text_content(extracted_data)

        # Grant amount rules
        if any('100' in text and 'k' in text for text in text_content):
            business_rules.append({
                'id': f"BR-{len(business_rules) + 1:03d}",
                'category': 'Grant Management',
                'rule': 'Maximum grant amount cannot exceed $100,000 for RTP funding',
                'source': 'Grant Program Requirements',
                'priority': 'High',
                'enforcement': 'System must validate grant amounts before submission'
            })

        # File format rules
        if any('pdf' in text.lower() or 'jpeg' in text.lower() for text in text_content):
            business_rules.append({
                'id': f"BR-{len(business_rules) + 1:03d}",
                'category': 'Document Management',
                'rule': 'Only PDF, JPEG, Docx, and Xlsx file formats are accepted',
                'source': 'Document Upload Requirements',
                'priority': 'High',
                'enforcement': 'System must validate file formats on upload'
            })

        return business_rules

    def _define_success_metrics(self, pm_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Define measurable success metrics"""
        metrics = []

        pm_metrics = pm_analysis.get('success_metrics', {})

        for category, category_metrics in pm_metrics.items():
            for metric_name, metric_data in category_metrics.items():
                if isinstance(metric_data, dict):
                    metrics.append({
                        'id': f"SM-{len(metrics) + 1:03d}",
                        'category': category.replace('_', ' ').title(),
                        'metric_name': metric_name.replace('_', ' ').title(),
                        'target': metric_data.get('target', 'TBD'),
                        'measurement': metric_data.get('measurement', 'TBD'),
                        'frequency': metric_data.get('frequency', 'Monthly'),
                        'owner': 'Product Manager',
                        'priority': 'Medium'
                    })

        return metrics

    def _generate_testing_scenarios(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate testing scenarios from acceptance criteria"""
        scenarios = []

        # Extract QA analysis if available
        qa_analysis = analysis_results.get('persona_analyses', {}).get('qa_engineer', {})

        # Generate high-level testing scenarios
        scenarios.extend([
            {
                'id': 'TS-001',
                'category': 'End-to-End',
                'scenario': 'Complete Grant Application Submission',
                'description': 'User completes entire grant application from start to submission',
                'preconditions': ['User has account', 'User has required documents'],
                'steps': [
                    'Navigate to application form',
                    'Fill out all required fields',
                    'Upload required documents',
                    'Review application',
                    'Submit application'
                ],
                'expected_outcome': 'Application submitted successfully with confirmation',
                'priority': 'High'
            },
            {
                'id': 'TS-002',
                'category': 'Error Handling',
                'scenario': 'Invalid File Upload',
                'description': 'User attempts to upload unsupported file format',
                'preconditions': ['User is on document upload section'],
                'steps': [
                    'Attempt to upload .exe file',
                    'Observe system response'
                ],
                'expected_outcome': 'Clear error message displayed, file rejected',
                'priority': 'High'
            },
            {
                'id': 'TS-003',
                'category': 'Accessibility',
                'scenario': 'Keyboard Navigation',
                'description': 'Complete form using only keyboard navigation',
                'preconditions': ['Screen reader or keyboard-only navigation'],
                'steps': [
                    'Navigate form using Tab key',
                    'Fill out fields using keyboard',
                    'Submit form using keyboard'
                ],
                'expected_outcome': 'All functionality accessible via keyboard',
                'priority': 'High'
            }
        ])

        return scenarios

    # Helper methods
    def _extract_project_name(self, analysis_results: Dict[str, Any]) -> str:
        """Extract project name from analysis results"""
        manifest = analysis_results.get('extracted_data', {}).get('manifest', {})
        files = manifest.get('files', [])
        if files:
            return files[0].get('name', 'Unknown Project')
        return 'Design Analysis Project'

    def _identify_stakeholders(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Identify project stakeholders from analysis"""
        pm_analysis = analysis_results.get('persona_analyses', {}).get('product_manager', {})
        stakeholder_analysis = pm_analysis.get('stakeholder_impact', {})

        stakeholders = []
        stakeholders.extend(stakeholder_analysis.get('primary_stakeholders', []))
        stakeholders.extend(stakeholder_analysis.get('secondary_stakeholders', []))

        return list(set(stakeholders)) if stakeholders else ['Product Owner', 'Development Team', 'End Users']

    def _has_user_management_features(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> bool:
        """Check if the application has user management features"""
        text_content = self._extract_text_content(extracted_data)
        return any('login' in text.lower() or 'account' in text.lower() or 'user' in text.lower()
                  for text in text_content)

    def _extract_text_content(self, extracted_data: Dict[str, Any]) -> List[str]:
        """Extract all text content from extracted data"""
        text_content = []
        for file_data in extracted_data.get('files', {}).values():
            for page_data in file_data.get('pages', {}).values():
                for obj_data in page_data.get('objects', {}).values():
                    if obj_data.get('type') == 'text':
                        # Extract text content
                        content = obj_data.get('content', {})
                        if isinstance(content, dict) and 'children' in content:
                            text = self._extract_text_from_children(content['children'])
                            if text.strip():
                                text_content.append(text.strip())

                    # Extract component names
                    name = obj_data.get('name', '')
                    if name and not name.startswith('692df9ea-'):
                        text_content.append(name)

        return text_content

    def _extract_text_from_children(self, children: List) -> str:
        """Recursively extract text from content children"""
        text = ""
        for child in children:
            if isinstance(child, dict):
                if child.get('type') == 'text':
                    text += child.get('text', '')
                elif 'children' in child:
                    text += self._extract_text_from_children(child['children'])
        return text

    def _assign_epic(self, story_data: Dict[str, Any]) -> str:
        """Assign story to appropriate epic"""
        title = story_data.get('title', '').lower()

        if any(word in title for word in ['login', 'account', 'authentication', 'user']):
            return 'EP-002'  # User Management Epic
        elif any(word in title for word in ['document', 'upload', 'file']):
            return 'EP-003'  # Document Management Epic
        else:
            return 'EP-001'  # Main Application Epic

    def _assign_feature(self, story_data: Dict[str, Any]) -> str:
        """Assign story to appropriate feature"""
        title = story_data.get('title', '').lower()

        if 'form' in title or 'application' in title:
            return 'Application Form'
        elif 'upload' in title or 'document' in title:
            return 'Document Management'
        elif 'validation' in title or 'error' in title:
            return 'Data Validation'
        elif 'accessibility' in title:
            return 'Accessibility'
        else:
            return 'Core Functionality'

    def _generate_story_tags(self, story_data: Dict[str, Any]) -> List[str]:
        """Generate tags for the story"""
        tags = []

        title = story_data.get('title', '').lower()
        priority = story_data.get('priority', '').lower()

        # Priority tags
        tags.append(f'priority-{priority}')

        # Functional tags
        if 'form' in title:
            tags.append('forms')
        if 'upload' in title:
            tags.append('file-handling')
        if 'accessibility' in title:
            tags.append('accessibility')
        if 'error' in title:
            tags.append('error-handling')
        if 'validation' in title:
            tags.append('validation')

        # Technical tags
        if any(word in title for word in ['api', 'integration', 'data']):
            tags.append('backend')
        if any(word in title for word in ['ui', 'interface', 'display']):
            tags.append('frontend')

        return tags

    def _identify_constraints(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify project constraints"""
        constraints = []

        # Technical constraints
        constraints.append({
            'id': 'CON-001',
            'type': 'Technical',
            'constraint': 'Must integrate with existing government database systems',
            'impact': 'High',
            'mitigation': 'Use standardized APIs and data formats'
        })

        # Compliance constraints
        constraints.append({
            'id': 'CON-002',
            'type': 'Compliance',
            'constraint': 'Must meet Section 508 accessibility requirements',
            'impact': 'High',
            'mitigation': 'Implement WCAG 2.1 AA standards from project start'
        })

        # Performance constraints
        constraints.append({
            'id': 'CON-003',
            'type': 'Performance',
            'constraint': 'Must handle peak loads during application deadline periods',
            'impact': 'Medium',
            'mitigation': 'Implement load balancing and capacity planning'
        })

        return constraints

    def _document_assumptions(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Document key project assumptions"""
        assumptions = []

        assumptions.extend([
            {
                'id': 'ASM-001',
                'assumption': 'Users have basic computer literacy and internet access',
                'risk_if_false': 'High support burden and low adoption',
                'validation_method': 'User research and usability testing'
            },
            {
                'id': 'ASM-002',
                'assumption': 'Existing government systems can provide required integration APIs',
                'risk_if_false': 'Project delays and additional development work',
                'validation_method': 'Technical architecture review with IT department'
            },
            {
                'id': 'ASM-003',
                'assumption': 'Application volume will not exceed 10,000 submissions per month',
                'risk_if_false': 'Performance issues and system overload',
                'validation_method': 'Historical data analysis and capacity planning'
            }
        ])

        return assumptions

    def _generate_implementation_notes(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate implementation guidance notes"""
        return {
            'development_approach': 'Agile development with 2-week sprints',
            'testing_strategy': 'Test-driven development with comprehensive automated testing',
            'deployment_strategy': 'Phased rollout with pilot user group',
            'monitoring_requirements': 'Comprehensive logging, error tracking, and performance monitoring',
            'documentation_requirements': [
                'Technical API documentation',
                'User training materials',
                'System administration guide',
                'Accessibility compliance documentation'
            ],
            'risk_mitigation': [
                'Early prototype validation with stakeholders',
                'Regular security reviews',
                'Performance testing throughout development',
                'Comprehensive backup and disaster recovery planning'
            ]
        }