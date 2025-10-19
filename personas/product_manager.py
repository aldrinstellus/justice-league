"""
Product Manager Persona Analyzer
Analyzes design files from a product management perspective
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class UserStory:
    """Represents a user story with acceptance criteria"""
    id: str
    title: str
    user_story: str
    acceptance_criteria: List[str]
    definition_of_done: List[str]
    business_rules: List[str]
    priority: str
    effort_estimate: str


@dataclass
class BusinessRequirement:
    """Represents a business requirement"""
    id: str
    title: str
    description: str
    rationale: str
    success_criteria: List[str]
    stakeholders: List[str]
    priority: str


class ProductManagerAnalyzer:
    """Analyzes design files from a product manager perspective"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def analyze(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform product manager analysis

        Args:
            extracted_data: Extracted Penpot file data
            components: Detected UI components

        Returns:
            Product management analysis results
        """
        self.logger.info("Starting Product Manager analysis")

        try:
            analysis_results = {
                'business_context': self._analyze_business_context(extracted_data),
                'user_journey_analysis': self._analyze_user_journey(extracted_data, components),
                'user_stories': self._generate_user_stories(extracted_data, components),
                'business_requirements': self._extract_business_requirements(extracted_data),
                'feature_prioritization': self._analyze_feature_priority(extracted_data, components),
                'stakeholder_impact': self._analyze_stakeholder_impact(extracted_data),
                'roi_analysis': self._analyze_roi_potential(extracted_data, components),
                'success_metrics': self._define_success_metrics(extracted_data),
                'risk_assessment': self._assess_project_risks(extracted_data, components),
                'recommendations': self._generate_pm_recommendations(extracted_data, components)
            }

            self.logger.info("Product Manager analysis completed")
            return analysis_results

        except Exception as e:
            self.logger.error(f"Product Manager analysis failed: {str(e)}")
            raise

    def _analyze_business_context(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the business context of the design"""
        file_summary = self._get_file_summary(extracted_data)
        text_content = self._extract_text_content(extracted_data)

        # Infer business context from file name and content
        business_context = {
            'domain': self._infer_business_domain(file_summary, text_content),
            'target_users': self._identify_target_users(text_content),
            'business_goals': self._infer_business_goals(text_content),
            'industry_context': self._analyze_industry_context(file_summary, text_content),
            'competitive_landscape': self._assess_competitive_context(text_content)
        }

        return business_context

    def _infer_business_domain(self, file_summary: Dict, text_content: List[str]) -> str:
        """Infer the business domain from design content"""
        file_name = file_summary.get('file_name', '').lower()
        all_text = ' '.join(text_content).lower()

        # Domain detection patterns
        if 'wisconsin' in file_name or 'dnr' in all_text or 'natural resources' in all_text:
            return 'Government - Natural Resources Management'
        elif 'grant' in all_text or 'funding' in all_text or 'application' in all_text:
            return 'Government - Grant Management'
        elif 'e-commerce' in all_text or 'shop' in all_text or 'cart' in all_text:
            return 'E-commerce'
        elif 'healthcare' in all_text or 'medical' in all_text or 'patient' in all_text:
            return 'Healthcare'
        elif 'financial' in all_text or 'banking' in all_text or 'payment' in all_text:
            return 'Financial Services'
        else:
            return 'General Business Application'

    def _identify_target_users(self, text_content: List[str]) -> List[str]:
        """Identify target user groups from content"""
        all_text = ' '.join(text_content).lower()

        users = []
        if 'applicant' in all_text:
            users.append('Grant Applicants')
        if 'admin' in all_text or 'administrator' in all_text:
            users.append('System Administrators')
        if 'reviewer' in all_text or 'approval' in all_text:
            users.append('Application Reviewers')
        if 'staff' in all_text:
            users.append('Staff Users')
        if 'public' in all_text or 'citizen' in all_text:
            users.append('General Public')

        return users if users else ['General Users']

    def _infer_business_goals(self, text_content: List[str]) -> List[str]:
        """Infer business goals from content analysis"""
        all_text = ' '.join(text_content).lower()

        goals = []
        if 'application' in all_text and 'submit' in all_text:
            goals.append('Streamline application submission process')
        if 'efficiency' in all_text or 'faster' in all_text:
            goals.append('Improve operational efficiency')
        if 'digital' in all_text or 'online' in all_text:
            goals.append('Digital transformation initiative')
        if 'compliance' in all_text or 'regulation' in all_text:
            goals.append('Ensure regulatory compliance')
        if 'user' in all_text and ('experience' in all_text or 'friendly' in all_text):
            goals.append('Enhance user experience')

        return goals if goals else ['Improve business processes']

    def _analyze_user_journey(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user journey through the application"""
        text_content = self._extract_text_content(extracted_data)

        journey_analysis = {
            'entry_points': self._identify_entry_points(components, text_content),
            'key_workflows': self._identify_key_workflows(text_content, components),
            'decision_points': self._identify_decision_points(components, text_content),
            'potential_friction': self._identify_friction_points(components, text_content),
            'success_paths': self._map_success_paths(text_content, components),
            'error_scenarios': self._identify_error_scenarios(components, text_content)
        }

        return journey_analysis

    def _generate_user_stories(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate user stories based on design analysis"""
        text_content = self._extract_text_content(extracted_data)
        business_context = self._analyze_business_context(extracted_data)

        user_stories = []

        # Generate primary user stories based on identified functionality
        if any('grant' in text.lower() for text in text_content):
            user_stories.append({
                'id': 'US-001',
                'title': 'Grant Application Submission',
                'user_story': 'As a grant applicant, I want to submit my funding application online, so that I can efficiently apply for government grants',
                'acceptance_criteria': [
                    'Given I am on the application form page',
                    'When I fill out all required fields with valid information',
                    'Then I can successfully submit my application',
                    'And I receive a confirmation with application ID',
                    'And the system validates all business rules before submission'
                ],
                'definition_of_done': [
                    'Form validation works for all input fields',
                    'File upload supports specified formats',
                    'Confirmation email sent to applicant',
                    'Application data stored with audit trail',
                    'Accessibility compliance verified'
                ],
                'business_rules': [
                    'Grant amount cannot exceed maximum threshold',
                    'Required documents must be uploaded',
                    'Application deadline must be enforced',
                    'Duplicate applications are prevented'
                ],
                'priority': 'High',
                'effort_estimate': '8 story points'
            })

        # Generate supporting user stories
        if any(comp.get('type') == 'input' for comp in components.get('ui_elements', {}).values()):
            user_stories.append({
                'id': 'US-002',
                'title': 'Form Data Validation',
                'user_story': 'As an applicant, I want to receive immediate feedback on form errors, so that I can correct issues before submission',
                'acceptance_criteria': [
                    'Given I am filling out the application form',
                    'When I enter invalid data in any field',
                    'Then I see clear error messages immediately',
                    'And the error messages explain how to fix the issue',
                    'And the form prevents submission until all errors are resolved'
                ],
                'definition_of_done': [
                    'Client-side validation implemented',
                    'Server-side validation as backup',
                    'Error messages are user-friendly',
                    'Accessibility requirements met for error states'
                ],
                'business_rules': [
                    'Validation occurs on field blur and form submission',
                    'Error messages follow government style guidelines',
                    'Required field indicators are clearly visible'
                ],
                'priority': 'High',
                'effort_estimate': '5 story points'
            })

        return user_stories

    def _extract_business_requirements(self, extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract high-level business requirements"""
        text_content = self._extract_text_content(extracted_data)

        requirements = []

        # Analyze for government compliance requirements
        if any('wisconsin' in text.lower() for text in text_content):
            requirements.append({
                'id': 'BR-001',
                'title': 'Government Accessibility Compliance',
                'description': 'System must meet Section 508 accessibility standards for government applications',
                'rationale': 'Legal requirement for government digital services',
                'success_criteria': [
                    'WCAG 2.1 AA compliance achieved',
                    'Screen reader compatibility verified',
                    'Keyboard navigation fully functional'
                ],
                'stakeholders': ['Legal Team', 'Accessibility Specialist', 'End Users'],
                'priority': 'High'
            })

        # Analyze for data handling requirements
        if any('application' in text.lower() for text in text_content):
            requirements.append({
                'id': 'BR-002',
                'title': 'Secure Data Handling',
                'description': 'Application data must be securely collected, stored, and transmitted',
                'rationale': 'Protect sensitive applicant information and maintain trust',
                'success_criteria': [
                    'Data encryption in transit and at rest',
                    'Audit trail for all data access',
                    'Regular security assessments passed'
                ],
                'stakeholders': ['Security Team', 'IT Operations', 'Legal Team'],
                'priority': 'High'
            })

        return requirements

    def _analyze_feature_priority(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze and prioritize features based on design emphasis"""
        component_usage = components.get('component_inventory', {}).get('components', {})
        text_content = self._extract_text_content(extracted_data)

        priority_analysis = {
            'high_priority': [],
            'medium_priority': [],
            'low_priority': [],
            'future_enhancements': []
        }

        # Prioritize based on component usage frequency
        for comp_name, usage_count in component_usage.items():
            if usage_count > 5:  # Frequently used components are likely high priority
                priority_analysis['high_priority'].append({
                    'feature': comp_name,
                    'usage_frequency': usage_count,
                    'rationale': 'Frequently used component indicates core functionality'
                })
            elif usage_count > 2:
                priority_analysis['medium_priority'].append({
                    'feature': comp_name,
                    'usage_frequency': usage_count,
                    'rationale': 'Moderately used component for secondary features'
                })

        # Analyze text content for priority indicators
        if any('required' in text.lower() for text in text_content):
            priority_analysis['high_priority'].append({
                'feature': 'Required Field Validation',
                'rationale': 'Essential for data quality and business rules'
            })

        return priority_analysis

    def _analyze_stakeholder_impact(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze impact on different stakeholder groups"""
        business_context = self._analyze_business_context(extracted_data)

        stakeholder_impact = {
            'primary_stakeholders': [],
            'secondary_stakeholders': [],
            'impact_matrix': {}
        }

        # Identify stakeholders based on business domain
        domain = business_context.get('domain', '')
        if 'government' in domain.lower():
            stakeholder_impact['primary_stakeholders'] = [
                'Grant Applicants',
                'Government Staff',
                'Department Leadership'
            ]
            stakeholder_impact['secondary_stakeholders'] = [
                'IT Support',
                'Legal/Compliance Team',
                'Auditors'
            ]

        # Define impact for each stakeholder
        for stakeholder in stakeholder_impact['primary_stakeholders']:
            stakeholder_impact['impact_matrix'][stakeholder] = {
                'benefits': self._identify_stakeholder_benefits(stakeholder, extracted_data),
                'concerns': self._identify_stakeholder_concerns(stakeholder, extracted_data),
                'success_criteria': self._define_stakeholder_success(stakeholder, extracted_data)
            }

        return stakeholder_impact

    def _analyze_roi_potential(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze potential return on investment"""
        return {
            'efficiency_gains': {
                'time_savings': 'Estimated 40% reduction in application processing time',
                'cost_reduction': 'Reduced manual processing overhead',
                'error_reduction': 'Automated validation reduces data entry errors'
            },
            'user_satisfaction': {
                'improved_experience': 'Online submission vs paper forms',
                'accessibility': 'Better access for users with disabilities',
                'convenience': '24/7 availability for applications'
            },
            'operational_benefits': {
                'scalability': 'Handle increased application volume',
                'compliance': 'Built-in compliance with government standards',
                'reporting': 'Automated data collection and reporting'
            },
            'quantifiable_metrics': {
                'application_completion_rate': 'Target: >85%',
                'processing_time_reduction': 'Target: 40% improvement',
                'user_satisfaction_score': 'Target: >4.2/5'
            }
        }

    def _define_success_metrics(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Define success metrics for the product"""
        return {
            'user_metrics': {
                'application_completion_rate': {
                    'target': '85%',
                    'measurement': 'Completed applications / Started applications',
                    'frequency': 'Monthly'
                },
                'time_to_complete': {
                    'target': '<30 minutes average',
                    'measurement': 'Time from start to submission',
                    'frequency': 'Continuous'
                },
                'user_satisfaction': {
                    'target': '4.2/5 or higher',
                    'measurement': 'Post-submission survey',
                    'frequency': 'Quarterly'
                }
            },
            'business_metrics': {
                'processing_efficiency': {
                    'target': '40% improvement',
                    'measurement': 'Time from submission to initial review',
                    'frequency': 'Monthly'
                },
                'error_rate': {
                    'target': '<5% of submissions',
                    'measurement': 'Applications requiring correction',
                    'frequency': 'Monthly'
                },
                'cost_per_application': {
                    'target': '30% reduction',
                    'measurement': 'Total processing cost / applications',
                    'frequency': 'Quarterly'
                }
            },
            'technical_metrics': {
                'system_availability': {
                    'target': '99.5% uptime',
                    'measurement': 'System monitoring',
                    'frequency': 'Daily'
                },
                'page_load_time': {
                    'target': '<3 seconds',
                    'measurement': 'Performance monitoring',
                    'frequency': 'Continuous'
                }
            }
        }

    # Helper methods
    def _get_file_summary(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get file summary information"""
        manifest = extracted_data.get('manifest', {})
        return {
            'file_name': manifest.get('files', [{}])[0].get('name', 'Unknown'),
            'total_objects': extracted_data.get('total_objects', 0)
        }

    def _extract_text_content(self, extracted_data: Dict[str, Any]) -> List[str]:
        """Extract all text content from the design"""
        text_content = []
        for file_data in extracted_data.get('files', {}).values():
            for page_data in file_data.get('pages', {}).values():
                for obj_data in page_data.get('objects', {}).values():
                    # Extract text from text objects
                    if obj_data.get('type') == 'text':
                        content = obj_data.get('content', {})
                        if isinstance(content, dict) and 'children' in content:
                            text = self._extract_text_from_children(content['children'])
                            if text.strip():
                                text_content.append(text.strip())

                    # Extract names
                    name = obj_data.get('name', '')
                    if name and not name.startswith('692df9ea-') and name not in ['Text', 'Frame']:
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

    def _identify_entry_points(self, components: Dict, text_content: List[str]) -> List[str]:
        """Identify application entry points"""
        entry_points = ['Main application form']
        if any('login' in text.lower() for text in text_content):
            entry_points.append('Authentication page')
        if any('dashboard' in text.lower() for text in text_content):
            entry_points.append('User dashboard')
        return entry_points

    def _identify_key_workflows(self, text_content: List[str], components: Dict) -> List[str]:
        """Identify key user workflows"""
        workflows = []
        if any('application' in text.lower() for text in text_content):
            workflows.append('Grant application submission workflow')
        if any('review' in text.lower() for text in text_content):
            workflows.append('Application review workflow')
        if any('upload' in text.lower() for text in text_content):
            workflows.append('Document upload workflow')
        return workflows if workflows else ['Primary user workflow']

    def _identify_decision_points(self, components: Dict, text_content: List[str]) -> List[str]:
        """Identify key decision points in user journey"""
        decision_points = []
        if any('amount' in text.lower() for text in text_content):
            decision_points.append('Grant amount selection')
        if any('category' in text.lower() for text in text_content):
            decision_points.append('Application category choice')
        return decision_points if decision_points else ['Form completion decision']

    def _identify_friction_points(self, components: Dict, text_content: List[str]) -> List[str]:
        """Identify potential friction points"""
        friction_points = []
        if len(text_content) > 50:  # Many text elements might indicate complexity
            friction_points.append('Form complexity - many fields to complete')
        if any('required' in text.lower() for text in text_content):
            friction_points.append('Required field validation')
        return friction_points if friction_points else ['Potential user onboarding complexity']

    def _map_success_paths(self, text_content: List[str], components: Dict) -> List[str]:
        """Map successful user paths"""
        success_paths = []
        if any('submit' in text.lower() for text in text_content):
            success_paths.append('Complete form → Submit → Receive confirmation')
        if any('save' in text.lower() for text in text_content):
            success_paths.append('Save draft → Complete later → Submit')
        return success_paths if success_paths else ['Standard completion path']

    def _identify_error_scenarios(self, components: Dict, text_content: List[str]) -> List[str]:
        """Identify potential error scenarios"""
        error_scenarios = []
        if any('validation' in text.lower() for text in text_content):
            error_scenarios.append('Form validation errors')
        if any('upload' in text.lower() for text in text_content):
            error_scenarios.append('File upload failures')
        return error_scenarios if error_scenarios else ['General input errors']

    def _identify_stakeholder_benefits(self, stakeholder: str, extracted_data: Dict) -> List[str]:
        """Identify benefits for specific stakeholder"""
        benefits = {
            'Grant Applicants': [
                'Online submission convenience',
                'Real-time validation feedback',
                '24/7 availability'
            ],
            'Government Staff': [
                'Reduced manual processing',
                'Automated data collection',
                'Improved data quality'
            ],
            'Department Leadership': [
                'Better reporting capabilities',
                'Improved efficiency metrics',
                'Enhanced public service'
            ]
        }
        return benefits.get(stakeholder, ['Improved system efficiency'])

    def _identify_stakeholder_concerns(self, stakeholder: str, extracted_data: Dict) -> List[str]:
        """Identify concerns for specific stakeholder"""
        concerns = {
            'Grant Applicants': [
                'System reliability during deadlines',
                'Technical support availability',
                'Data security and privacy'
            ],
            'Government Staff': [
                'Training requirements',
                'System integration with existing tools',
                'Change management'
            ],
            'Department Leadership': [
                'Implementation timeline',
                'Budget and resource requirements',
                'Compliance with regulations'
            ]
        }
        return concerns.get(stakeholder, ['General system concerns'])

    def _define_stakeholder_success(self, stakeholder: str, extracted_data: Dict) -> List[str]:
        """Define success criteria for specific stakeholder"""
        success_criteria = {
            'Grant Applicants': [
                'Can complete application in <30 minutes',
                'Receives immediate confirmation of submission',
                'Can track application status'
            ],
            'Government Staff': [
                'Processing time reduced by 40%',
                'Data quality improved',
                'Fewer support requests'
            ],
            'Department Leadership': [
                'Increased application completion rates',
                'Positive user feedback scores',
                'Operational cost reduction'
            ]
        }
        return success_criteria.get(stakeholder, ['System operates effectively'])

    def _assess_project_risks(self, extracted_data: Dict, components: Dict) -> Dict[str, Any]:
        """Assess project risks from PM perspective"""
        return {
            'high_risk': [
                'Government compliance requirements',
                'Integration with legacy systems',
                'Peak load during application deadlines'
            ],
            'medium_risk': [
                'User adoption and training',
                'Data migration from existing systems',
                'Third-party service dependencies'
            ],
            'low_risk': [
                'Basic UI/UX implementation',
                'Standard security measures',
                'Regular system maintenance'
            ],
            'mitigation_strategies': [
                'Early compliance review and testing',
                'Phased rollout approach',
                'Comprehensive user training program',
                'Robust load testing and capacity planning'
            ]
        }

    def _generate_pm_recommendations(self, extracted_data: Dict, components: Dict) -> List[Dict[str, Any]]:
        """Generate product manager recommendations"""
        return [
            {
                'category': 'User Experience',
                'priority': 'High',
                'recommendation': 'Implement progressive form saving to prevent data loss',
                'rationale': 'Government forms are often complex and time-consuming',
                'implementation_effort': 'Medium',
                'expected_impact': 'Significant reduction in form abandonment'
            },
            {
                'category': 'Business Value',
                'priority': 'High',
                'recommendation': 'Add application status tracking for applicants',
                'rationale': 'Reduces support requests and improves transparency',
                'implementation_effort': 'Medium',
                'expected_impact': 'Improved user satisfaction and reduced support load'
            },
            {
                'category': 'Compliance',
                'priority': 'High',
                'recommendation': 'Implement comprehensive audit logging',
                'rationale': 'Required for government accountability and compliance',
                'implementation_effort': 'High',
                'expected_impact': 'Meets regulatory requirements'
            }
        ]