"""
Test-Driven Development Process Manager for Aldo Vision Agent
Comprehensive TDD methodology integration for agent development and design analysis

This module provides:
- TDD workflow orchestration for agent persona development
- Test-first design analysis recommendations
- TDD methodology guidance for analyzed applications
- Continuous integration with testing cycles
- TDD metrics and quality measurement
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import re
from pathlib import Path

class TDDPhase(Enum):
    RED = "red"           # Write failing test
    GREEN = "green"       # Write minimal code to pass
    REFACTOR = "refactor" # Improve code quality

class TestType(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    ACCEPTANCE = "acceptance"
    CONTRACT = "contract"
    VISUAL = "visual"
    PERFORMANCE = "performance"

class TDDMaturity(Enum):
    BEGINNER = "beginner"     # Basic TDD practices
    INTERMEDIATE = "intermediate"  # Solid TDD with some advanced practices
    ADVANCED = "advanced"     # Full TDD mastery with complex scenarios
    EXPERT = "expert"        # TDD coaching and methodology improvement

@dataclass
class TDDTestCase:
    name: str
    type: TestType
    phase: TDDPhase
    description: str
    preconditions: List[str]
    test_code: str
    implementation_guidance: str
    refactoring_opportunities: List[str]
    acceptance_criteria: List[str]
    estimated_effort: str

@dataclass
class TDDWorkflow:
    feature_name: str
    user_story: str
    acceptance_criteria: List[str]
    test_cases: List[TDDTestCase]
    tdd_cycle_count: int
    estimated_duration: str
    complexity_score: int

@dataclass
class TDDMetrics:
    test_coverage: float
    cycle_time: Dict[str, float]  # red, green, refactor phase times
    test_pass_rate: float
    refactoring_frequency: float
    code_quality_score: float
    technical_debt_reduction: float

class TDDProcessManager:
    def __init__(self):
        self.tdd_patterns = self._load_tdd_patterns()
        self.testing_frameworks = self._load_testing_frameworks()
        self.quality_metrics = self._load_quality_metrics()
        self.workflow_templates = self._load_workflow_templates()

    def analyze_design_for_tdd(self, penpot_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze design from TDD perspective and provide comprehensive TDD strategy
        """
        analysis = {
            "executive_summary": self._generate_tdd_executive_summary(penpot_data),
            "tdd_strategy": self._create_comprehensive_tdd_strategy(penpot_data),
            "test_first_design_analysis": self._analyze_design_for_testability(penpot_data),
            "tdd_workflow_recommendations": self._generate_tdd_workflows(penpot_data),
            "testing_pyramid_design": self._design_testing_pyramid(penpot_data),
            "bdd_integration": self._create_bdd_integration_plan(penpot_data),
            "tdd_tooling_stack": self._recommend_tdd_tooling(penpot_data),
            "quality_gates": self._define_quality_gates(penpot_data),
            "tdd_coaching_plan": self._create_tdd_coaching_plan(penpot_data),
            "continuous_improvement": self._design_tdd_improvement_process(penpot_data),
            "implementation_roadmap": self._create_tdd_implementation_roadmap(penpot_data)
        }

        return analysis

    def _generate_tdd_executive_summary(self, penpot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary of TDD implementation strategy"""

        components_count = self._count_testable_components(penpot_data)
        complexity_score = self._calculate_tdd_complexity(penpot_data)

        return {
            "tdd_readiness_assessment": {
                "overall_complexity": complexity_score,
                "testability_score": "High (85%)",
                "tdd_adoption_feasibility": "Excellent - Design supports test-first development",
                "estimated_test_coverage_potential": {
                    "unit_tests": "95%+",
                    "integration_tests": "85%+",
                    "acceptance_tests": "100% of user stories",
                    "visual_tests": "90%+ of UI components"
                },
                "critical_tdd_focus_areas": [
                    "Component-driven development with isolated testing",
                    "API-first design with contract testing",
                    "User story acceptance criteria with BDD scenarios",
                    "Visual component testing with state variations",
                    "Performance budgets with TDD validation"
                ]
            },
            "tdd_methodology_recommendations": {
                "primary_approach": "Outside-In TDD (Acceptance Test Driven Development)",
                "secondary_approach": "Inside-Out TDD for complex algorithms",
                "bdd_integration": "Gherkin scenarios for user story validation",
                "visual_tdd": "Component-driven development with Storybook TDD"
            },
            "business_impact": {
                "development_velocity": "40-60% increase after initial learning curve",
                "bug_reduction": "70-90% reduction in production defects",
                "code_maintainability": "Significant improvement in code readability and structure",
                "team_confidence": "Higher confidence in refactoring and feature changes",
                "documentation": "Living documentation through comprehensive test suites"
            },
            "implementation_timeline": {
                "tdd_foundation_setup": "2-3 weeks",
                "team_training_program": "4-6 weeks",
                "initial_feature_development": "8-12 weeks (with learning curve)",
                "tdd_maturity_achievement": "6-12 months",
                "roi_break_even_point": "3-4 months"
            },
            "success_metrics": {
                "test_coverage": ">95% line coverage, >90% branch coverage",
                "cycle_time": "Red-Green-Refactor cycles <30 minutes",
                "defect_rate": "<0.5 defects per 1000 lines of code",
                "refactoring_confidence": "Monthly refactoring sessions without fear",
                "team_adoption": "100% of features developed using TDD"
            }
        }

    def _create_comprehensive_tdd_strategy(self, penpot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive TDD strategy tailored to the analyzed design"""

        return {
            "tdd_methodology_framework": {
                "outside_in_tdd": {
                    "description": "Start with acceptance tests, work inward to implementation",
                    "use_cases": [
                        "User-facing features with clear acceptance criteria",
                        "API endpoints with defined contracts",
                        "Complex user workflows with multiple steps"
                    ],
                    "workflow": [
                        "1. Write failing acceptance test (RED)",
                        "2. Write minimal integration tests to support acceptance (RED)",
                        "3. Write unit tests for individual components (RED)",
                        "4. Implement minimal code to pass unit tests (GREEN)",
                        "5. Refactor unit implementations (REFACTOR)",
                        "6. Verify integration tests pass (GREEN)",
                        "7. Verify acceptance test passes (GREEN)",
                        "8. Refactor entire feature (REFACTOR)"
                    ],
                    "tools": ["Cucumber", "Jest", "Testing Library", "Cypress"]
                },
                "inside_out_tdd": {
                    "description": "Start with unit tests, build up to integration",
                    "use_cases": [
                        "Complex algorithms and business logic",
                        "Utility functions and data transformations",
                        "Core domain models and entities"
                    ],
                    "workflow": [
                        "1. Write failing unit test (RED)",
                        "2. Write minimal code to pass (GREEN)",
                        "3. Refactor implementation (REFACTOR)",
                        "4. Repeat for all units",
                        "5. Write integration tests",
                        "6. Write acceptance tests"
                    ],
                    "tools": ["Jest", "Vitest", "Testing Library"]
                },
                "component_driven_tdd": {
                    "description": "TDD specifically for React/Vue component development",
                    "use_cases": [
                        "UI component libraries",
                        "Interactive user interface elements",
                        "Visual state management"
                    ],
                    "workflow": [
                        "1. Write component specification in Storybook",
                        "2. Write failing component tests (RED)",
                        "3. Implement minimal component (GREEN)",
                        "4. Refactor component implementation (REFACTOR)",
                        "5. Add visual regression tests",
                        "6. Verify accessibility tests pass"
                    ],
                    "tools": ["Storybook", "Testing Library", "Chromatic", "axe-core"]
                }
            },
            "tdd_cycles_and_rhythms": {
                "micro_cycles": {
                    "duration": "5-30 minutes",
                    "focus": "Single test case implementation",
                    "phases": {
                        "red": "2-5 minutes - Write specific failing test",
                        "green": "5-15 minutes - Minimal implementation",
                        "refactor": "3-10 minutes - Code improvement"
                    },
                    "discipline": [
                        "Write only enough test to fail",
                        "Write only enough code to pass",
                        "Refactor without changing behavior"
                    ]
                },
                "feature_cycles": {
                    "duration": "2-8 hours",
                    "focus": "Complete feature implementation",
                    "phases": {
                        "planning": "30 minutes - Break down into testable units",
                        "implementation": "6-7 hours - Multiple micro-cycles",
                        "integration": "30 minutes - Feature-level testing"
                    }
                },
                "release_cycles": {
                    "duration": "1-4 weeks",
                    "focus": "Releasable increment",
                    "activities": [
                        "Code coverage analysis and improvement",
                        "Performance test validation",
                        "Acceptance criteria verification",
                        "Technical debt refactoring"
                    ]
                }
            },
            "test_doubles_strategy": {
                "mocks": {
                    "use_case": "Verify interactions with dependencies",
                    "examples": ["API calls", "Event handlers", "Database operations"],
                    "tools": ["Jest mocks", "Sinon.js", "MSW"]
                },
                "stubs": {
                    "use_case": "Control dependency responses",
                    "examples": ["External service responses", "Configuration values"],
                    "tools": ["Jest spies", "Test fixtures"]
                },
                "fakes": {
                    "use_case": "Simplified working implementations",
                    "examples": ["In-memory database", "Local file system"],
                    "tools": ["sqlite3 :memory:", "temp directories"]
                },
                "dummies": {
                    "use_case": "Parameter filling for required arguments",
                    "examples": ["Unused callback functions", "Required but ignored parameters"],
                    "implementation": "Simple placeholder objects"
                }
            },
            "refactoring_patterns": {
                "extract_method": {
                    "trigger": "Long methods or repeated code blocks",
                    "safety": "Comprehensive unit test coverage",
                    "process": "Extract with tests, verify behavior unchanged"
                },
                "extract_class": {
                    "trigger": "Classes with multiple responsibilities",
                    "safety": "Interface-based testing approach",
                    "process": "Create new class, move methods with tests"
                },
                "rename_variables": {
                    "trigger": "Unclear naming or domain understanding changes",
                    "safety": "IDE refactoring tools with test verification",
                    "process": "Rename, run tests, commit immediately"
                },
                "simplify_conditionals": {
                    "trigger": "Complex boolean expressions",
                    "safety": "Branch coverage in unit tests",
                    "process": "Extract guard clauses, use early returns"
                }
            }
        }

    def _analyze_design_for_testability(self, penpot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the design from a testability perspective"""

        components = self._extract_components_for_testing(penpot_data)
        user_flows = self._identify_user_flows(penpot_data)

        return {
            "component_testability_analysis": {
                "highly_testable_components": [
                    {
                        "component": "Form Components",
                        "testability_score": 9.5,
                        "reasons": [
                            "Clear input/output boundaries",
                            "Predictable state changes",
                            "Easy to isolate and mock dependencies",
                            "Validation logic can be unit tested"
                        ],
                        "tdd_approach": "Inside-out TDD with validation-first testing",
                        "test_scenarios": [
                            "Valid input handling",
                            "Invalid input validation",
                            "Form submission behavior",
                            "Error state management"
                        ]
                    },
                    {
                        "component": "Data Display Components",
                        "testability_score": 9.0,
                        "reasons": [
                            "Pure functions for data transformation",
                            "No side effects in rendering logic",
                            "Easy to provide test data",
                            "Visual states are predictable"
                        ],
                        "tdd_approach": "Component-driven TDD with Storybook",
                        "test_scenarios": [
                            "Data rendering accuracy",
                            "Empty state handling",
                            "Loading state display",
                            "Error state presentation"
                        ]
                    }
                ],
                "moderately_testable_components": [
                    {
                        "component": "Interactive Widgets",
                        "testability_score": 7.5,
                        "reasons": [
                            "Complex user interactions",
                            "Multiple state transitions",
                            "Event handling complexity"
                        ],
                        "improvement_suggestions": [
                            "Extract business logic from event handlers",
                            "Use state machines for complex interactions",
                            "Separate presentation from interaction logic"
                        ]
                    }
                ],
                "challenging_testable_components": [
                    {
                        "component": "Third-party Integrations",
                        "testability_score": 6.0,
                        "challenges": [
                            "External dependency management",
                            "Network timing issues",
                            "Authentication complexity"
                        ],
                        "tdd_strategies": [
                            "Contract testing with Pact",
                            "Service virtualization",
                            "Facade pattern for external APIs"
                        ]
                    }
                ]
            },
            "user_flow_testability": {
                "critical_paths": [
                    {
                        "flow": "User Registration and Onboarding",
                        "testability": "High",
                        "tdd_approach": "Outside-in with Cucumber scenarios",
                        "acceptance_criteria": [
                            "User can create account with valid email",
                            "User receives confirmation email",
                            "User can complete profile setup",
                            "User can access main application features"
                        ],
                        "test_pyramid": {
                            "acceptance": "4 scenarios covering happy path and edge cases",
                            "integration": "12 tests for API endpoints and database operations",
                            "unit": "35 tests for validation, formatting, and business rules"
                        }
                    },
                    {
                        "flow": "Data Creation and Management",
                        "testability": "High",
                        "tdd_approach": "Feature-driven with extensive mocking",
                        "test_complexity": "Medium - requires test data management",
                        "automation_strategy": "Factory pattern for test data generation"
                    }
                ],
                "secondary_flows": [
                    {
                        "flow": "Settings and Configuration",
                        "testability": "Medium",
                        "challenges": ["Complex state persistence", "Cross-feature dependencies"],
                        "tdd_recommendations": [
                            "Test configuration objects in isolation",
                            "Mock local storage and session persistence",
                            "Use dependency injection for configuration services"
                        ]
                    }
                ]
            },
            "testability_improvements": {
                "architectural_recommendations": [
                    {
                        "pattern": "Hexagonal Architecture",
                        "benefit": "Clear separation between business logic and external concerns",
                        "implementation": "Ports and adapters for all external dependencies"
                    },
                    {
                        "pattern": "Dependency Injection",
                        "benefit": "Easy mocking and test double injection",
                        "implementation": "Constructor injection with interface abstractions"
                    },
                    {
                        "pattern": "Command Query Separation",
                        "benefit": "Predictable side effects and easier testing",
                        "implementation": "Separate read and write operations"
                    }
                ],
                "code_quality_guidelines": [
                    "Functions should have single responsibility",
                    "Minimize external dependencies in pure functions",
                    "Use immutable data structures where possible",
                    "Implement clear error handling strategies",
                    "Avoid deep nesting in conditional logic"
                ]
            }
        }

    def _generate_tdd_workflows(self, penpot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specific TDD workflows for identified features"""

        workflows = []

        # Example workflow for a form component identified in the design
        form_workflow = TDDWorkflow(
            feature_name="User Profile Form",
            user_story="As a user, I want to update my profile information so that other users can see accurate details about me",
            acceptance_criteria=[
                "User can edit first name, last name, email, and bio fields",
                "Form validates email format before submission",
                "User receives confirmation when profile is updated successfully",
                "User sees appropriate error messages for validation failures"
            ],
            test_cases=[
                TDDTestCase(
                    name="Email validation test",
                    type=TestType.UNIT,
                    phase=TDDPhase.RED,
                    description="Verify email validation rejects invalid formats",
                    preconditions=["Email validator function exists"],
                    test_code="""
describe('Email Validator', () => {
  test('should reject invalid email format', () => {
    const validator = new EmailValidator();
    expect(validator.isValid('invalid-email')).toBe(false);
    expect(validator.isValid('test@')).toBe(false);
    expect(validator.isValid('@example.com')).toBe(false);
  });

  test('should accept valid email format', () => {
    const validator = new EmailValidator();
    expect(validator.isValid('user@example.com')).toBe(true);
    expect(validator.isValid('test.user+tag@domain.co.uk')).toBe(true);
  });
});""",
                    implementation_guidance="Create EmailValidator class with regex-based validation",
                    refactoring_opportunities=["Extract regex patterns", "Add custom error messages"],
                    acceptance_criteria=["All email formats validated correctly"],
                    estimated_effort="30 minutes"
                ),
                TDDTestCase(
                    name="Form submission integration test",
                    type=TestType.INTEGRATION,
                    phase=TDDPhase.RED,
                    description="Verify form submission calls API with correct data",
                    preconditions=["API client exists", "Form component exists"],
                    test_code="""
describe('Profile Form Submission', () => {
  test('should call API with form data when valid', async () => {
    const mockApiClient = jest.fn().mockResolvedValue({ success: true });
    const form = new ProfileForm(mockApiClient);

    const formData = {
      firstName: 'John',
      lastName: 'Doe',
      email: 'john@example.com',
      bio: 'Software developer'
    };

    await form.submit(formData);

    expect(mockApiClient).toHaveBeenCalledWith('/api/profile', {
      method: 'PUT',
      body: JSON.stringify(formData)
    });
  });
});""",
                    implementation_guidance="Implement form submission with API integration",
                    refactoring_opportunities=["Extract API client interface", "Add retry logic"],
                    acceptance_criteria=["Form submits valid data to correct endpoint"],
                    estimated_effort="45 minutes"
                )
            ],
            tdd_cycle_count=8,
            estimated_duration="4-6 hours",
            complexity_score=6
        )

        workflows.append(form_workflow)

        return {
            "feature_workflows": [workflow.__dict__ for workflow in workflows],
            "workflow_templates": {
                "simple_component": {
                    "phases": ["Unit tests", "Component tests", "Integration tests"],
                    "estimated_cycles": "3-5",
                    "complexity": "Low"
                },
                "complex_feature": {
                    "phases": ["Acceptance tests", "Integration tests", "Unit tests", "Visual tests"],
                    "estimated_cycles": "8-15",
                    "complexity": "High"
                },
                "api_endpoint": {
                    "phases": ["Contract tests", "Integration tests", "Unit tests", "Security tests"],
                    "estimated_cycles": "5-10",
                    "complexity": "Medium"
                }
            },
            "workflow_optimization": {
                "parallel_development": "Multiple developers can work on different layers simultaneously",
                "continuous_integration": "Each TDD cycle can be integrated and tested",
                "feedback_loops": "Short cycles provide rapid feedback on design decisions"
            }
        }

    def _design_testing_pyramid(self, penpot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Design optimal testing pyramid for the analyzed application"""

        return {
            "testing_pyramid_structure": {
                "unit_tests": {
                    "percentage": 70,
                    "quantity_estimate": "200-300 tests",
                    "focus_areas": [
                        "Pure functions and utility methods",
                        "Business logic and validation rules",
                        "Data transformation and formatting",
                        "Component prop handling and state management"
                    ],
                    "tdd_approach": "Inside-out TDD with rapid cycles",
                    "execution_time": "<5 seconds for full suite",
                    "tools": ["Jest", "Vitest", "Testing Library"],
                    "coverage_target": "95% line coverage, 90% branch coverage"
                },
                "integration_tests": {
                    "percentage": 20,
                    "quantity_estimate": "50-80 tests",
                    "focus_areas": [
                        "API endpoint integration",
                        "Database operations and queries",
                        "External service interactions",
                        "Component integration and data flow"
                    ],
                    "tdd_approach": "Outside-in TDD with service mocking",
                    "execution_time": "<30 seconds for full suite",
                    "tools": ["Supertest", "MSW", "Testing Library"],
                    "coverage_target": "80% of integration points"
                },
                "end_to_end_tests": {
                    "percentage": 10,
                    "quantity_estimate": "15-25 tests",
                    "focus_areas": [
                        "Critical user journeys",
                        "Cross-browser compatibility",
                        "Authentication and authorization flows",
                        "Payment and transaction processes"
                    ],
                    "tdd_approach": "Acceptance Test Driven Development (ATDD)",
                    "execution_time": "<5 minutes for critical path suite",
                    "tools": ["Playwright", "Cypress", "Cucumber"],
                    "coverage_target": "100% of critical user stories"
                }
            },
            "specialized_testing_layers": {
                "visual_regression_tests": {
                    "purpose": "Prevent UI regressions and maintain design consistency",
                    "scope": "All UI components and key user interface states",
                    "tdd_integration": "Component-driven TDD with visual snapshots",
                    "automation_level": "Fully automated with manual review for changes",
                    "tools": ["Chromatic", "Percy", "BackstopJS"]
                },
                "accessibility_tests": {
                    "purpose": "Ensure WCAG compliance and inclusive design",
                    "scope": "All interactive components and user flows",
                    "tdd_integration": "Accessibility-first development with axe-core",
                    "automation_level": "Automated scanning with manual validation",
                    "tools": ["axe-core", "Pa11y", "Lighthouse"]
                },
                "performance_tests": {
                    "purpose": "Validate performance budgets and user experience",
                    "scope": "Critical pages and resource-intensive operations",
                    "tdd_integration": "Performance budget TDD with Lighthouse CI",
                    "automation_level": "Automated with CI/CD integration",
                    "tools": ["Lighthouse CI", "WebPageTest", "Bundle analyzers"]
                },
                "security_tests": {
                    "purpose": "Identify vulnerabilities and security issues",
                    "scope": "Authentication, data validation, and user permissions",
                    "tdd_integration": "Security-driven development with threat modeling",
                    "automation_level": "Automated scanning with manual penetration testing",
                    "tools": ["OWASP ZAP", "Snyk", "ESLint security plugins"]
                }
            },
            "test_data_strategy": {
                "test_data_pyramid": {
                    "unit_level": {
                        "approach": "Minimal, focused test data for specific scenarios",
                        "generation": "Factory functions and builders",
                        "isolation": "Each test creates its own data",
                        "cleanup": "Automatic cleanup after each test"
                    },
                    "integration_level": {
                        "approach": "Realistic data that represents actual usage patterns",
                        "generation": "Database seeding with referential integrity",
                        "isolation": "Test database or transaction rollback",
                        "cleanup": "Database reset between test suites"
                    },
                    "e2e_level": {
                        "approach": "Production-like data with anonymized sensitive information",
                        "generation": "Data migration from staging environment",
                        "isolation": "Separate test environment with dedicated data",
                        "cleanup": "Environment refresh for consistent baseline"
                    }
                }
            },
            "feedback_optimization": {
                "fast_feedback_loop": {
                    "unit_tests": "Immediate feedback during development",
                    "integration_tests": "Quick validation of component interactions",
                    "static_analysis": "Code quality issues caught before testing"
                },
                "comprehensive_feedback": {
                    "visual_tests": "UI consistency validation",
                    "e2e_tests": "User experience validation",
                    "performance_tests": "Non-functional requirement validation"
                },
                "feedback_prioritization": {
                    "blocking_issues": "Unit test failures, critical E2E failures",
                    "warning_issues": "Performance regressions, accessibility warnings",
                    "informational": "Code coverage metrics, visual diff notifications"
                }
            }
        }

    def _create_bdd_integration_plan(self, penpot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create Behavior Driven Development integration plan"""

        return {
            "bdd_framework_integration": {
                "gherkin_scenarios": {
                    "purpose": "Living documentation that describes system behavior",
                    "audience": ["Product managers", "Developers", "QA engineers", "Business stakeholders"],
                    "structure": {
                        "feature_files": "High-level feature descriptions",
                        "scenario_outlines": "Parameterized test scenarios",
                        "step_definitions": "Implementation of Gherkin steps",
                        "hooks": "Setup and teardown for test scenarios"
                    }
                },
                "three_amigos_process": {
                    "participants": ["Product Owner", "Developer", "Tester"],
                    "meeting_cadence": "Before each feature development",
                    "activities": [
                        "Review user stories and acceptance criteria",
                        "Write Gherkin scenarios collaboratively",
                        "Identify edge cases and error conditions",
                        "Define test data requirements"
                    ],
                    "deliverables": [
                        "Agreed Gherkin scenarios",
                        "Test data specifications",
                        "Definition of done criteria"
                    ]
                }
            },
            "example_bdd_scenarios": {
                "user_profile_management": """
Feature: User Profile Management
  As a registered user
  I want to manage my profile information
  So that other users can see accurate details about me

  Background:
    Given I am logged in as a registered user
    And I am on the profile management page

  Scenario: Successfully update profile information
    Given my profile has the following information:
      | Field      | Value               |
      | First Name | John                |
      | Last Name  | Doe                 |
      | Email      | john.doe@email.com  |
      | Bio        | Software Developer  |
    When I update my first name to "Jonathan"
    And I update my bio to "Senior Software Developer"
    And I click the "Save Changes" button
    Then I should see a "Profile updated successfully" message
    And my profile should display "Jonathan" as first name
    And my profile should display "Senior Software Developer" as bio

  Scenario Outline: Email validation during profile update
    Given my current email is "john.doe@email.com"
    When I try to update my email to "<new_email>"
    And I click the "Save Changes" button
    Then I should see "<result>"

    Examples:
      | new_email           | result                                    |
      | jane.doe@email.com  | Profile updated successfully              |
      | invalid-email       | Please enter a valid email address       |
      | existing@email.com  | This email address is already in use     |
      |                     | Email address is required                 |

  Scenario: Handle server error during profile update
    Given the profile update service is unavailable
    When I update my first name to "Jonathan"
    And I click the "Save Changes" button
    Then I should see an error message "Unable to save changes. Please try again later."
    And my original profile information should remain unchanged
""",
                "data_search_and_filtering": """
Feature: Data Search and Filtering
  As a user
  I want to search and filter data efficiently
  So that I can find the information I need quickly

  Scenario: Basic search functionality
    Given there are 100 items in the system
    And some items contain "javascript" in their title
    When I search for "javascript"
    Then I should see only items that contain "javascript" in the title
    And the results should be sorted by relevance
    And I should see a count of matching items

  Scenario: Advanced filtering with multiple criteria
    Given there are items with various categories and dates
    When I filter by category "Technology"
    And I filter by date range "2024-01-01" to "2024-12-31"
    And I search for "programming"
    Then I should see only items that:
      | Criteria    | Value                           |
      | Category    | Technology                      |
      | Date        | Between 2024-01-01 and 2024-12-31 |
      | Content     | Contains "programming"           |
"""
            },
            "bdd_tooling_recommendations": {
                "cucumber_js": {
                    "pros": ["Industry standard", "Excellent documentation", "Wide community support"],
                    "cons": ["Can be verbose", "Learning curve for Gherkin"],
                    "best_for": "Teams with business stakeholder involvement"
                },
                "jest_cucumber": {
                    "pros": ["Lightweight", "Jest integration", "Easy setup"],
                    "cons": ["Less feature-rich than full Cucumber"],
                    "best_for": "Development teams focused on technical scenarios"
                },
                "playwright_bdd": {
                    "pros": ["Modern testing", "Cross-browser support", "Built-in debugging"],
                    "cons": ["Newer ecosystem", "Less community resources"],
                    "best_for": "Teams prioritizing end-to-end testing"
                }
            },
            "living_documentation": {
                "automated_reports": {
                    "feature_coverage": "Track which features have BDD scenarios",
                    "scenario_execution": "Show which scenarios pass/fail in each build",
                    "step_reusability": "Identify commonly used steps for refactoring"
                },
                "stakeholder_communication": {
                    "executive_dashboard": "High-level feature completion status",
                    "product_owner_reports": "Detailed scenario outcomes and edge cases",
                    "developer_insights": "Technical debt and refactoring opportunities"
                }
            }
        }

    def _recommend_tdd_tooling(self, penpot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend comprehensive TDD tooling stack"""

        return {
            "core_testing_frameworks": {
                "javascript_typescript": {
                    "unit_testing": {
                        "primary": {
                            "tool": "Jest",
                            "pros": ["Mature ecosystem", "Built-in mocking", "Snapshot testing"],
                            "cons": ["Can be slow on large codebases"],
                            "configuration": {
                                "coverage_threshold": "95% lines, 90% branches",
                                "test_match": "**/__tests__/**/*.test.{js,ts}",
                                "setup_files": "['<rootDir>/src/test-setup.js']"
                            }
                        },
                        "alternative": {
                            "tool": "Vitest",
                            "pros": ["Faster execution", "Better TypeScript support", "Vite integration"],
                            "cons": ["Newer ecosystem", "Less community resources"]
                        }
                    },
                    "component_testing": {
                        "tool": "Testing Library",
                        "approach": "Test behavior, not implementation",
                        "principles": [
                            "Query by accessibility attributes",
                            "Test user interactions",
                            "Avoid testing internal state"
                        ]
                    },
                    "e2e_testing": {
                        "tool": "Playwright",
                        "advantages": [
                            "Cross-browser testing",
                            "Built-in test generator",
                            "Excellent debugging tools",
                            "Network interception"
                        ]
                    }
                },
                "python": {
                    "unit_testing": {
                        "tool": "pytest",
                        "advantages": [
                            "Fixture system for test setup",
                            "Parametrized testing",
                            "Plugin ecosystem"
                        ]
                    },
                    "bdd_integration": {
                        "tool": "pytest-bdd",
                        "integration": "Seamless Gherkin scenario execution"
                    }
                }
            },
            "tdd_productivity_tools": {
                "test_runners": {
                    "watch_mode": {
                        "tools": ["Jest --watch", "Vitest --watch", "pytest-watch"],
                        "benefit": "Immediate feedback on code changes",
                        "configuration": "Run only affected tests for speed"
                    },
                    "parallel_execution": {
                        "tools": ["Jest --parallel", "pytest-xdist"],
                        "benefit": "Faster test execution on multi-core systems"
                    }
                },
                "code_coverage": {
                    "tools": ["Istanbul/NYC", "c8", "Coverage.py"],
                    "integration": "CI/CD pipeline integration",
                    "reporting": ["HTML reports", "JSON for programmatic analysis", "LCOV for IDE integration"]
                },
                "mutation_testing": {
                    "tools": ["Stryker", "Mutmut"],
                    "purpose": "Test the quality of your tests",
                    "frequency": "Weekly or before major releases"
                }
            },
            "development_environment": {
                "ide_integration": {
                    "vscode_extensions": [
                        "Jest Runner - Run individual tests",
                        "Test Explorer - Visual test management",
                        "Coverage Gutters - Inline coverage display",
                        "GitLens - Test history and blame information"
                    ],
                    "jetbrains_plugins": [
                        "Built-in test runner integration",
                        "Coverage visualization",
                        "Refactoring safety with test verification"
                    ]
                },
                "debugging_tools": {
                    "test_debugging": "Node.js inspector integration with breakpoints",
                    "browser_debugging": "Playwright debug mode with browser dev tools",
                    "visual_debugging": "Screenshot capture on test failures"
                }
            },
            "ci_cd_integration": {
                "github_actions": {
                    "workflow_template": """
name: TDD Workflow
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run test:unit
      - run: npm run test:integration
      - run: npm run test:e2e
      - uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info
""",
                    "features": ["Parallel test execution", "Coverage reporting", "Test result caching"]
                },
                "quality_gates": {
                    "coverage_threshold": "95% line coverage required for merge",
                    "test_success_rate": "100% test pass rate required",
                    "performance_budgets": "No performance regression allowed"
                }
            }
        }

    def _define_quality_gates(self, penpot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Define comprehensive quality gates for TDD process"""

        return {
            "commit_level_gates": {
                "pre_commit_hooks": {
                    "linting": {
                        "tools": ["ESLint", "Prettier", "TypeScript compiler"],
                        "purpose": "Code style and syntax consistency",
                        "failure_action": "Block commit until resolved"
                    },
                    "unit_tests": {
                        "scope": "Tests affected by changed files",
                        "performance": "Must complete within 30 seconds",
                        "coverage": "No decrease in coverage allowed"
                    },
                    "security_scanning": {
                        "tools": ["ESLint security plugin", "audit-check"],
                        "purpose": "Catch security vulnerabilities early"
                    }
                }
            },
            "pull_request_gates": {
                "test_suite_execution": {
                    "unit_tests": {
                        "requirement": "100% pass rate",
                        "coverage": "95% line coverage, 90% branch coverage",
                        "performance": "Must complete within 2 minutes"
                    },
                    "integration_tests": {
                        "requirement": "100% pass rate",
                        "scope": "All integration points verified",
                        "performance": "Must complete within 5 minutes"
                    },
                    "visual_regression": {
                        "requirement": "No unintended visual changes",
                        "approval": "Visual changes require manual approval",
                        "scope": "All UI components and critical pages"
                    }
                },
                "code_quality_metrics": {
                    "complexity_analysis": {
                        "cyclomatic_complexity": "< 10 per function",
                        "cognitive_complexity": "< 15 per function",
                        "nesting_depth": "< 4 levels"
                    },
                    "maintainability_index": {
                        "minimum_score": "70/100",
                        "calculation": "Based on complexity, lines of code, and Halstead volume"
                    },
                    "technical_debt": {
                        "sonarqube_rating": "A or B rating required",
                        "code_smells": "< 10 new code smells",
                        "duplication": "< 3% code duplication"
                    }
                }
            },
            "release_gates": {
                "comprehensive_testing": {
                    "full_test_suite": {
                        "unit_tests": "100% pass rate with 95% coverage",
                        "integration_tests": "100% pass rate",
                        "e2e_tests": "100% pass rate for critical paths",
                        "performance_tests": "All budgets within limits"
                    },
                    "accessibility_validation": {
                        "automated_scans": "No WCAG AA violations",
                        "manual_testing": "Key workflows tested with screen readers",
                        "keyboard_navigation": "All features accessible via keyboard"
                    },
                    "security_validation": {
                        "vulnerability_scanning": "No high or critical vulnerabilities",
                        "dependency_audit": "All dependencies up to date and secure",
                        "penetration_testing": "Annual or after major features"
                    }
                },
                "business_validation": {
                    "acceptance_criteria": {
                        "feature_completion": "All user stories meet acceptance criteria",
                        "stakeholder_approval": "Product owner sign-off required",
                        "user_testing": "Positive feedback from user acceptance testing"
                    }
                }
            },
            "continuous_monitoring": {
                "production_quality_gates": {
                    "error_rates": {
                        "javascript_errors": "< 0.1% of page views",
                        "api_errors": "< 0.5% of requests",
                        "crash_rate": "< 0.01% of user sessions"
                    },
                    "performance_monitoring": {
                        "core_web_vitals": "75th percentile within 'Good' thresholds",
                        "api_response_times": "95th percentile < 500ms",
                        "availability": "> 99.9% uptime"
                    },
                    "user_experience": {
                        "user_satisfaction": "NPS score > 50",
                        "feature_adoption": "New features used by > 20% of users within 30 days",
                        "support_tickets": "< 5% increase after releases"
                    }
                }
            },
            "quality_gate_enforcement": {
                "automation_tools": {
                    "github_branch_protection": "Require status checks before merge",
                    "sonarqube_quality_gates": "Automated quality gate evaluation",
                    "deployment_gates": "Azure DevOps release gates or similar"
                },
                "escalation_procedures": {
                    "gate_failures": {
                        "immediate": "Notify developer and team lead",
                        "repeated_failures": "Code review and pair programming",
                        "persistent_issues": "Architectural review and technical debt planning"
                    }
                },
                "metrics_dashboard": {
                    "real_time_visibility": "Quality gate status visible to all team members",
                    "historical_trends": "Track quality improvements over time",
                    "team_performance": "Identify areas for process improvement"
                }
            }
        }

    def _create_tdd_coaching_plan(self, penpot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive TDD coaching and training plan"""

        return {
            "team_assessment": {
                "current_skill_levels": {
                    "beginner": {
                        "characteristics": [
                            "Limited or no TDD experience",
                            "Writes tests after implementation",
                            "Focuses on code coverage rather than behavior"
                        ],
                        "learning_objectives": [
                            "Understand TDD principles and benefits",
                            "Practice basic red-green-refactor cycles",
                            "Write meaningful unit tests"
                        ],
                        "training_approach": "Hands-on workshops with simple examples"
                    },
                    "intermediate": {
                        "characteristics": [
                            "Some TDD experience but inconsistent application",
                            "Understands unit testing but struggles with integration",
                            "Limited refactoring skills"
                        ],
                        "learning_objectives": [
                            "Consistent TDD application across all features",
                            "Master test doubles and mocking",
                            "Confident refactoring with test safety net"
                        ],
                        "training_approach": "Code reviews and pair programming sessions"
                    },
                    "advanced": {
                        "characteristics": [
                            "Solid TDD practitioners",
                            "Can lead by example",
                            "Ready to mentor others"
                        ],
                        "learning_objectives": [
                            "Advanced TDD patterns and techniques",
                            "Coaching and mentoring skills",
                            "Process improvement and team leadership"
                        ],
                        "training_approach": "Coaching the coaches, advanced workshops"
                    }
                }
            },
            "training_curriculum": {
                "week_1_foundations": {
                    "topics": [
                        "TDD principles and philosophy",
                        "Red-Green-Refactor cycle",
                        "Writing your first failing test",
                        "Minimal implementation strategies"
                    ],
                    "hands_on_exercises": [
                        "FizzBuzz kata with strict TDD",
                        "String calculator kata",
                        "Roman numerals converter"
                    ],
                    "assessment": "Complete a simple kata using TDD principles"
                },
                "week_2_unit_testing_mastery": {
                    "topics": [
                        "Test structure and organization",
                        "Assertion strategies and best practices",
                        "Test doubles: mocks, stubs, spies",
                        "Testing edge cases and error conditions"
                    ],
                    "hands_on_exercises": [
                        "Banking account kata with edge cases",
                        "Shopping cart with external dependencies",
                        "User authentication with mocking"
                    ],
                    "assessment": "Build a component with comprehensive unit tests"
                },
                "week_3_integration_and_e2e": {
                    "topics": [
                        "Integration testing strategies",
                        "API testing with TDD",
                        "Database integration testing",
                        "End-to-end test design"
                    ],
                    "hands_on_exercises": [
                        "REST API development with TDD",
                        "Database CRUD operations with testing",
                        "User workflow automation"
                    ],
                    "assessment": "Complete feature with full test pyramid"
                },
                "week_4_advanced_techniques": {
                    "topics": [
                        "Refactoring with confidence",
                        "Legacy code and testing",
                        "Property-based testing",
                        "Performance testing integration"
                    ],
                    "hands_on_exercises": [
                        "Refactor existing code with test coverage",
                        "Add tests to legacy codebase",
                        "Property-based testing examples"
                    ],
                    "assessment": "Refactor complex legacy code using TDD"
                }
            },
            "practical_application": {
                "pair_programming_sessions": {
                    "frequency": "2-3 sessions per week during training",
                    "duration": "2-4 hours per session",
                    "structure": [
                        "Driver-navigator rotation every 30 minutes",
                        "Focus on TDD technique application",
                        "Real project work with TDD principles",
                        "Immediate feedback and discussion"
                    ],
                    "pairing_strategy": {
                        "expert_beginner": "Accelerated learning with guidance",
                        "intermediate_intermediate": "Collaborative problem solving",
                        "mixed_groups": "Knowledge sharing and perspective diversity"
                    }
                },
                "code_review_process": {
                    "tdd_specific_checklist": [
                        "Are tests written before implementation?",
                        "Do tests drive the design of the code?",
                        "Is the test-to-code ratio appropriate?",
                        "Are refactoring opportunities identified?",
                        "Is the red-green-refactor cycle evident?"
                    ],
                    "review_guidelines": [
                        "Focus on TDD process adherence",
                        "Suggest alternative test approaches",
                        "Identify refactoring opportunities",
                        "Celebrate good TDD examples"
                    ]
                }
            },
            "coaching_methodologies": {
                "mob_programming": {
                    "purpose": "Collective learning and knowledge sharing",
                    "structure": "Entire team works on same problem with TDD",
                    "roles": [
                        "Driver: Types the code",
                        "Navigator: Guides the approach",
                        "Observers: Learn and contribute ideas"
                    ],
                    "rotation": "Every 15-30 minutes for engagement"
                },
                "kata_sessions": {
                    "purpose": "Practice TDD techniques in safe environment",
                    "recommended_katas": [
                        "Bowling Game - Classic TDD example",
                        "Mars Rover - Object design and TDD",
                        "Gilded Rose - Legacy code and refactoring",
                        "Potter Kata - Complex business rules"
                    ],
                    "session_structure": [
                        "15 minutes: Problem explanation and setup",
                        "45 minutes: TDD implementation",
                        "15 minutes: Retrospective and discussion"
                    ]
                },
                "retrospectives": {
                    "tdd_specific_questions": [
                        "Where did TDD help us discover better designs?",
                        "What TDD practices are we struggling with?",
                        "How can we improve our red-green-refactor rhythm?",
                        "What prevented us from using TDD effectively?"
                    ],
                    "improvement_actions": [
                        "Identify TDD skill gaps and training needs",
                        "Adjust team practices based on feedback",
                        "Celebrate TDD success stories",
                        "Address tooling and environment issues"
                    ]
                }
            },
            "progress_measurement": {
                "skill_assessment_metrics": {
                    "technical_skills": [
                        "Test-first development consistency",
                        "Quality of test cases and coverage",
                        "Refactoring confidence and frequency",
                        "Ability to work with legacy code"
                    ],
                    "behavioral_indicators": [
                        "Automatically reaches for tests before coding",
                        "Comfortable with small, incremental changes",
                        "Seeks feedback early and often",
                        "Embraces refactoring as continuous improvement"
                    ]
                },
                "team_maturity_indicators": {
                    "process_adoption": [
                        "Percentage of features developed with TDD",
                        "Test coverage metrics and trends",
                        "Refactoring frequency and success rate",
                        "Code review quality and TDD focus"
                    ],
                    "cultural_changes": [
                        "TDD discussions in daily standups",
                        "Team members helping each other with TDD",
                        "Proactive identification of testing opportunities",
                        "Resistance to non-TDD approaches"
                    ]
                }
            }
        }

    def _design_tdd_improvement_process(self, penpot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Design continuous improvement process for TDD practices"""

        return {
            "continuous_improvement_framework": {
                "measurement_and_metrics": {
                    "quantitative_metrics": {
                        "test_coverage": {
                            "line_coverage": "Target: >95%",
                            "branch_coverage": "Target: >90%",
                            "function_coverage": "Target: >95%",
                            "trend_tracking": "Weekly measurement with improvement goals"
                        },
                        "tdd_cycle_metrics": {
                            "red_phase_duration": "Average time to write failing test",
                            "green_phase_duration": "Average time to make test pass",
                            "refactor_phase_duration": "Average time spent refactoring",
                            "cycle_completion_rate": "Percentage of features using full TDD cycle"
                        },
                        "quality_indicators": {
                            "defect_rate": "Production bugs per 1000 lines of code",
                            "time_to_fix": "Average time to resolve issues",
                            "refactoring_safety": "Success rate of refactoring efforts",
                            "test_maintenance": "Time spent maintaining tests vs writing new ones"
                        }
                    },
                    "qualitative_assessments": {
                        "developer_confidence": {
                            "measurement": "Monthly survey with confidence ratings",
                            "areas": ["Refactoring", "Adding features", "Bug fixing", "Code reviews"],
                            "target": "Average confidence score >8/10"
                        },
                        "code_review_quality": {
                            "tdd_adherence": "Percentage of reviews mentioning TDD practices",
                            "design_discussions": "Quality of design conversations in reviews",
                            "learning_opportunities": "Knowledge sharing in review comments"
                        }
                    }
                },
                "feedback_loops": {
                    "daily_practices": {
                        "stand_up_integration": [
                            "Share TDD challenges and successes",
                            "Discuss complex testing scenarios",
                            "Identify pairing opportunities for TDD learning"
                        ],
                        "continuous_code_review": [
                            "Focus on TDD process in addition to code quality",
                            "Share alternative testing approaches",
                            "Celebrate excellent TDD examples"
                        ]
                    },
                    "weekly_practices": {
                        "tdd_retrospectives": {
                            "format": "15-minute focused retrospective on TDD practices",
                            "questions": [
                                "What TDD technique worked well this week?",
                                "Where did we struggle with test-first development?",
                                "What testing tools or techniques should we explore?"
                            ],
                            "outcomes": "Action items for TDD practice improvement"
                        },
                        "kata_sessions": {
                            "purpose": "Practice TDD in a safe, learning environment",
                            "structure": "Rotate through different coding challenges",
                            "learning_focus": "Different TDD techniques and patterns"
                        }
                    },
                    "monthly_practices": {
                        "metrics_review": {
                            "participants": "Entire development team",
                            "data_analysis": "Review TDD metrics and identify trends",
                            "goal_setting": "Adjust TDD improvement goals based on data",
                            "process_refinement": "Update TDD practices based on learnings"
                        },
                        "external_learning": {
                            "conference_talks": "Watch TDD-related conference presentations",
                            "book_club": "Read and discuss TDD and testing books",
                            "community_engagement": "Participate in TDD communities and forums"
                        }
                    }
                }
            },
            "process_evolution": {
                "maturity_stages": {
                    "stage_1_adoption": {
                        "timeline": "Months 1-3",
                        "focus": "Basic TDD skill building and habit formation",
                        "success_criteria": [
                            "All team members complete TDD training",
                            "50% of new features developed with TDD",
                            "Test coverage increases to 80%+"
                        ],
                        "common_challenges": [
                            "Resistance to slowing down initially",
                            "Difficulty writing tests first",
                            "Over-engineering test scenarios"
                        ]
                    },
                    "stage_2_integration": {
                        "timeline": "Months 4-8",
                        "focus": "Consistent TDD application and team collaboration",
                        "success_criteria": [
                            "80% of new features developed with TDD",
                            "Test coverage maintains 90%+",
                            "Team members comfortable pair programming with TDD"
                        ],
                        "optimization_areas": [
                            "Test organization and maintainability",
                            "Integration testing strategies",
                            "Refactoring techniques and confidence"
                        ]
                    },
                    "stage_3_mastery": {
                        "timeline": "Months 9-18",
                        "focus": "Advanced TDD techniques and process optimization",
                        "success_criteria": [
                            "95% of new features developed with TDD",
                            "Significant reduction in production defects",
                            "Team members mentoring others in TDD practices"
                        ],
                        "advanced_practices": [
                            "Property-based testing integration",
                            "Mutation testing for test quality verification",
                            "Advanced refactoring patterns and techniques"
                        ]
                    },
                    "stage_4_innovation": {
                        "timeline": "18+ months",
                        "focus": "TDD process innovation and organizational influence",
                        "activities": [
                            "Develop custom TDD tools and practices",
                            "Mentor other teams in TDD adoption",
                            "Contribute to TDD community and knowledge base",
                            "Experiment with emerging testing technologies"
                        ]
                    }
                },
                "adaptation_strategies": {
                    "technology_evolution": {
                        "new_frameworks": "Adapt TDD practices to new technology stacks",
                        "tool_improvements": "Evaluate and integrate better testing tools",
                        "language_features": "Leverage new language features for better testing"
                    },
                    "team_changes": {
                        "new_members": "Onboard new team members with TDD mentoring",
                        "role_evolution": "Adapt TDD practices as team roles change",
                        "scaling_up": "Maintain TDD practices as team grows"
                    },
                    "project_complexity": {
                        "legacy_integration": "Develop strategies for TDD with legacy code",
                        "distributed_systems": "Apply TDD to microservices and distributed architectures",
                        "performance_critical": "Balance TDD with performance requirements"
                    }
                }
            },
            "knowledge_management": {
                "documentation_practices": {
                    "tdd_playbook": {
                        "content": "Team-specific TDD guidelines and best practices",
                        "maintenance": "Updated quarterly based on team learnings",
                        "accessibility": "Available to all team members and new hires"
                    },
                    "pattern_library": {
                        "testing_patterns": "Common testing scenarios and solutions",
                        "refactoring_patterns": "Safe refactoring techniques with examples",
                        "anti_patterns": "Common mistakes and how to avoid them"
                    }
                },
                "knowledge_sharing": {
                    "internal_presentations": [
                        "Monthly TDD technique sharing sessions",
                        "Complex problem solving with TDD examples",
                        "Tool demonstrations and evaluations"
                    ],
                    "external_engagement": [
                        "Conference presentations on TDD experiences",
                        "Blog posts about TDD lessons learned",
                        "Open source contributions to testing tools"
                    ]
                }
            }
        }

    def _create_tdd_implementation_roadmap(self, penpot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed implementation roadmap for TDD adoption"""

        return {
            "implementation_phases": {
                "phase_0_preparation": {
                    "timeline": "Weeks 1-2",
                    "objective": "Establish foundation for TDD adoption",
                    "activities": [
                        {
                            "task": "Team TDD readiness assessment",
                            "duration": "1 day",
                            "owner": "Tech Lead",
                            "deliverable": "Current skill assessment and learning plan"
                        },
                        {
                            "task": "Tool evaluation and selection",
                            "duration": "3 days",
                            "owner": "Senior Developer",
                            "deliverable": "Recommended testing stack and configuration"
                        },
                        {
                            "task": "Development environment setup",
                            "duration": "2 days",
                            "owner": "DevOps Engineer",
                            "deliverable": "Configured testing environment for all developers"
                        },
                        {
                            "task": "Initial training material preparation",
                            "duration": "3 days",
                            "owner": "TDD Coach/Consultant",
                            "deliverable": "Customized training curriculum and materials"
                        }
                    ],
                    "success_criteria": [
                        "All team members have configured testing environment",
                        "Testing tools selected and approved",
                        "Training schedule established",
                        "Management commitment secured"
                    ]
                },
                "phase_1_foundation_training": {
                    "timeline": "Weeks 3-6",
                    "objective": "Build fundamental TDD skills across the team",
                    "activities": [
                        {
                            "task": "TDD principles workshop",
                            "duration": "2 days",
                            "format": "Interactive workshop with hands-on exercises",
                            "participants": "Entire development team",
                            "outcome": "Understanding of red-green-refactor cycle"
                        },
                        {
                            "task": "Unit testing mastery sessions",
                            "duration": "1 week (daily 2-hour sessions)",
                            "format": "Pair programming and code katas",
                            "focus": "Writing effective unit tests and test doubles"
                        },
                        {
                            "task": "Integration testing workshop",
                            "duration": "1 day",
                            "format": "Group exercises with real project scenarios",
                            "focus": "API testing and database integration"
                        },
                        {
                            "task": "First TDD feature implementation",
                            "duration": "1 week",
                            "format": "Guided implementation with coaching support",
                            "outcome": "Complete feature developed using TDD"
                        }
                    ],
                    "success_criteria": [
                        "All team members complete basic TDD training",
                        "Each developer implements at least one feature using TDD",
                        "Test coverage reaches 70% for new code",
                        "Team demonstrates red-green-refactor cycle proficiency"
                    ]
                },
                "phase_2_practice_integration": {
                    "timeline": "Weeks 7-14",
                    "objective": "Integrate TDD into daily development workflow",
                    "activities": [
                        {
                            "task": "Daily TDD practice with real features",
                            "duration": "6 weeks",
                            "approach": "Pair programming with rotating pairs",
                            "coaching": "Weekly TDD coaching sessions"
                        },
                        {
                            "task": "Code review process enhancement",
                            "duration": "1 week setup + ongoing",
                            "focus": "Include TDD adherence in review criteria",
                            "training": "Review guidelines and checklist creation"
                        },
                        {
                            "task": "CI/CD pipeline integration",
                            "duration": "1 week",
                            "deliverable": "Automated testing in deployment pipeline",
                            "owner": "DevOps Engineer with team support"
                        },
                        {
                            "task": "Testing strategy refinement",
                            "duration": "2 weeks",
                            "outcome": "Documented testing pyramid and guidelines",
                            "process": "Team collaboration and consensus building"
                        }
                    ],
                    "success_criteria": [
                        "60% of new features developed using TDD",
                        "Test coverage consistently above 85%",
                        "Reduced debugging time and fewer production issues",
                        "Team comfort with refactoring increases significantly"
                    ]
                },
                "phase_3_advanced_techniques": {
                    "timeline": "Weeks 15-22",
                    "objective": "Master advanced TDD techniques and patterns",
                    "activities": [
                        {
                            "task": "BDD integration workshop",
                            "duration": "2 days",
                            "focus": "Gherkin scenarios and stakeholder collaboration",
                            "outcome": "Living documentation with BDD tests"
                        },
                        {
                            "task": "Legacy code TDD techniques",
                            "duration": "1 week",
                            "approach": "Working with existing codebase",
                            "techniques": "Characterization tests and seam identification"
                        },
                        {
                            "task": "Performance testing integration",
                            "duration": "1 week",
                            "focus": "TDD with performance budgets",
                            "tools": "Lighthouse CI and performance assertions"
                        },
                        {
                            "task": "Visual testing with TDD",
                            "duration": "1 week",
                            "approach": "Component-driven development",
                            "tools": "Storybook and visual regression testing"
                        },
                        {
                            "task": "Advanced refactoring patterns",
                            "duration": "2 weeks",
                            "content": "Complex refactoring with test safety nets",
                            "practice": "Large-scale code improvements"
                        }
                    ],
                    "success_criteria": [
                        "85% of new features developed using TDD",
                        "Team comfortable with advanced testing patterns",
                        "Successful integration of BDD practices",
                        "Significant improvement in code quality metrics"
                    ]
                },
                "phase_4_optimization_mastery": {
                    "timeline": "Weeks 23-30",
                    "objective": "Optimize TDD process and achieve team mastery",
                    "activities": [
                        {
                            "task": "Process optimization analysis",
                            "duration": "1 week",
                            "focus": "Identify bottlenecks and improvement opportunities",
                            "method": "Metrics analysis and team feedback"
                        },
                        {
                            "task": "Custom tooling development",
                            "duration": "3 weeks",
                            "purpose": "Address team-specific testing needs",
                            "examples": "Test generators, custom matchers, reporting tools"
                        },
                        {
                            "task": "Mentoring program establishment",
                            "duration": "1 week setup + ongoing",
                            "purpose": "Enable knowledge transfer to other teams",
                            "structure": "Internal TDD champions and coaching rotation"
                        },
                        {
                            "task": "Advanced quality metrics implementation",
                            "duration": "2 weeks",
                            "focus": "Mutation testing and quality measurement",
                            "outcome": "Comprehensive quality dashboard"
                        }
                    ],
                    "success_criteria": [
                        "95% of new features developed using TDD",
                        "Team members confidently mentor others",
                        "Custom tooling improves team productivity",
                        "TDD process is fully integrated and optimized"
                    ]
                }
            },
            "resource_allocation": {
                "team_time_investment": {
                    "initial_training": "20% of development time for first 6 weeks",
                    "integration_period": "15% of development time for weeks 7-14",
                    "advanced_training": "10% of development time for weeks 15-22",
                    "optimization": "5% of development time for weeks 23-30",
                    "ongoing_maintenance": "5% of development time for continuous improvement"
                },
                "external_resources": {
                    "tdd_consultant": {
                        "duration": "12 weeks part-time engagement",
                        "cost": "$8,000-$15,000",
                        "value": "Accelerated learning and best practice implementation"
                    },
                    "training_materials": {
                        "books_and_resources": "$500-$1,000",
                        "online_courses": "$2,000-$5,000",
                        "conference_attendance": "$5,000-$10,000"
                    },
                    "tooling_costs": {
                        "testing_tools": "$200-$500/month",
                        "ci_cd_enhancements": "$300-$800/month",
                        "monitoring_tools": "$100-$300/month"
                    }
                }
            },
            "risk_mitigation": {
                "common_adoption_risks": [
                    {
                        "risk": "Initial productivity decrease",
                        "probability": "High",
                        "impact": "Medium",
                        "mitigation": "Set realistic expectations, focus on long-term benefits",
                        "timeline": "Expect 20-30% initial slowdown for 4-6 weeks"
                    },
                    {
                        "risk": "Team resistance to change",
                        "probability": "Medium",
                        "impact": "High",
                        "mitigation": "Involve team in decision-making, demonstrate quick wins",
                        "strategy": "Identify early adopters as change champions"
                    },
                    {
                        "risk": "Over-testing and analysis paralysis",
                        "probability": "Medium",
                        "impact": "Medium",
                        "mitigation": "Clear guidelines on when and what to test",
                        "prevention": "Regular coaching and code review feedback"
                    },
                    {
                        "risk": "Tool complexity and setup issues",
                        "probability": "Low",
                        "impact": "High",
                        "mitigation": "Thorough tool evaluation and setup automation",
                        "contingency": "Have backup tool options ready"
                    }
                ],
                "success_factors": [
                    "Strong leadership commitment and support",
                    "Dedicated coaching and mentoring resources",
                    "Gradual adoption with celebration of milestones",
                    "Integration with existing development practices",
                    "Regular measurement and adjustment of approach"
                ]
            },
            "success_measurement": {
                "short_term_indicators": {
                    "weeks_1_8": [
                        "Training completion rates",
                        "First TDD features implemented",
                        "Test coverage improvements",
                        "Team confidence surveys"
                    ]
                },
                "medium_term_indicators": {
                    "weeks_9_20": [
                        "Consistent TDD application rates",
                        "Code quality metric improvements",
                        "Refactoring frequency and success",
                        "Reduced debugging time"
                    ]
                },
                "long_term_indicators": {
                    "weeks_21_plus": [
                        "Production defect reduction",
                        "Development velocity improvement",
                        "Team satisfaction and confidence",
                        "Knowledge transfer to other teams"
                    ]
                }
            }
        }

    # Helper methods for data analysis and calculation
    def _count_testable_components(self, penpot_data: Dict[str, Any]) -> int:
        """Count components that are suitable for TDD approach"""
        try:
            extracted_data = penpot_data.get('extracted_data', {})
            components = extracted_data.get('components', [])
            return len(components)
        except:
            return 0

    def _calculate_tdd_complexity(self, penpot_data: Dict[str, Any]) -> str:
        """Calculate TDD complexity based on design analysis"""
        component_count = self._count_testable_components(penpot_data)
        # Mock complexity calculation based on component count
        if component_count > 50:
            return "High"
        elif component_count > 20:
            return "Medium"
        else:
            return "Low"

    def _extract_components_for_testing(self, penpot_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract component information optimized for testing analysis"""
        try:
            extracted_data = penpot_data.get('extracted_data', {})
            return extracted_data.get('components', [])
        except:
            return []

    def _identify_user_flows(self, penpot_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify user flows that can benefit from TDD approach"""
        # Mock user flow identification based on design patterns
        return [
            {"name": "User Registration", "complexity": "Medium", "testability": "High"},
            {"name": "Data Management", "complexity": "High", "testability": "High"},
            {"name": "Settings Configuration", "complexity": "Medium", "testability": "Medium"}
        ]

    # Data loading methods (would be implemented with real data sources)
    def _load_tdd_patterns(self) -> Dict[str, Any]:
        return {"red_green_refactor": {}, "outside_in": {}, "inside_out": {}}

    def _load_testing_frameworks(self) -> Dict[str, Any]:
        return {"jest": {}, "vitest": {}, "playwright": {}}

    def _load_quality_metrics(self) -> Dict[str, Any]:
        return {"coverage": {}, "complexity": {}, "maintainability": {}}

    def _load_workflow_templates(self) -> Dict[str, Any]:
        return {"component": {}, "feature": {}, "api": {}}

def create_tdd_analysis(penpot_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point for TDD process analysis
    """
    manager = TDDProcessManager()
    return manager.analyze_design_for_tdd(penpot_data)

# Export for use in main analysis pipeline
__all__ = ['create_tdd_analysis', 'TDDProcessManager', 'TDDTestCase', 'TDDWorkflow', 'TDDMetrics']