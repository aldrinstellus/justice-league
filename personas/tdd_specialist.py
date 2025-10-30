"""
TDD Specialist Persona
Expert Test-Driven Development Methodology and Process Analysis

This persona provides comprehensive TDD guidance including:
- Complete TDD process design and implementation strategies
- Team coaching and training programs for TDD adoption
- Advanced TDD patterns and techniques
- Integration with existing development workflows
- Continuous improvement and maturity assessment
"""

from typing import Dict, List, Any
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from tdd.tdd_process_manager import create_tdd_analysis

class TDDSpecialistAnalyzer:
    """TDD Specialist persona that provides comprehensive TDD methodology guidance"""

    def __init__(self):
        self.expertise_areas = [
            "Red-Green-Refactor Cycle Mastery",
            "Outside-In and Inside-Out TDD Approaches",
            "BDD Integration and Living Documentation",
            "TDD Coaching and Team Transformation",
            "Legacy Code TDD Techniques",
            "Advanced Testing Patterns and Refactoring",
            "TDD Process Optimization and Metrics"
        ]

    def analyze(self, extracted_data: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive TDD analysis from specialist perspective
        """
        penpot_data = {
            'extracted_data': extracted_data,
            'components': components
        }

        # Get comprehensive TDD analysis
        base_analysis = create_tdd_analysis(penpot_data)

        # Add TDD specialist specific insights
        specialist_insights = self._add_specialist_insights(penpot_data, base_analysis)

        # Combine base analysis with specialist insights
        return {
            **base_analysis,
            "tdd_specialist_insights": specialist_insights,
            "specialist_recommendations": self._generate_specialist_recommendations(penpot_data),
            "advanced_tdd_patterns": self._analyze_advanced_patterns(penpot_data),
            "team_transformation_strategy": self._create_transformation_strategy(penpot_data)
        }

    def _add_specialist_insights(self, penpot_data: Dict[str, Any], base_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Add TDD specialist specific insights to the base analysis"""

        return {
            "methodology_deep_dive": {
                "red_green_refactor_mastery": {
                    "red_phase_optimization": {
                        "principle": "Write the smallest possible test that fails for the right reason",
                        "common_mistakes": [
                            "Writing too comprehensive tests initially",
                            "Testing implementation details instead of behavior",
                            "Not ensuring the test fails for the expected reason"
                        ],
                        "advanced_techniques": [
                            "Triangulation to drive better abstractions",
                            "Fake it till you make it for rapid feedback",
                            "Use obvious implementation when the solution is clear"
                        ],
                        "time_management": "2-5 minutes maximum per red phase"
                    },
                    "green_phase_optimization": {
                        "principle": "Write the simplest code that makes the test pass",
                        "discipline_points": [
                            "Resist the urge to write 'better' code immediately",
                            "Embrace duplication temporarily",
                            "Focus on making tests pass, not perfect code"
                        ],
                        "advanced_strategies": [
                            "Sliming - return hard-coded values initially",
                            "Triangulation - use multiple examples to drive generalization",
                            "Transformation Priority Premise - prefer simpler transformations"
                        ]
                    },
                    "refactor_phase_mastery": {
                        "safety_principles": [
                            "Never refactor without green tests",
                            "Make small, incremental changes",
                            "Run tests after each refactoring step"
                        ],
                        "refactoring_catalog": [
                            "Extract Method - break down large methods",
                            "Extract Class - separate responsibilities",
                            "Introduce Parameter Object - reduce parameter lists",
                            "Replace Magic Number with Symbolic Constant"
                        ],
                        "when_to_refactor": [
                            "Code duplication appears (Rule of Three)",
                            "Methods become too long (>20 lines as guideline)",
                            "Classes have too many responsibilities",
                            "Complex conditional logic emerges"
                        ]
                    }
                },
                "tdd_rhythm_and_flow": {
                    "micro_rhythms": {
                        "pomodoro_integration": "25-minute focused TDD sessions",
                        "pair_programming_rhythm": "Driver-navigator switches every 15-30 minutes",
                        "energy_management": "Take breaks when getting stuck for >15 minutes"
                    },
                    "flow_state_optimization": {
                        "distraction_elimination": [
                            "Turn off notifications during TDD sessions",
                            "Use dedicated TDD workspace/branch",
                            "Prepare test data and environment in advance"
                        ],
                        "momentum_building": [
                            "Start with easiest test to build confidence",
                            "Keep a list of next tests to maintain focus",
                            "Celebrate small wins and completed cycles"
                        ]
                    }
                }
            },
            "advanced_tdd_philosophy": {
                "design_emergence": {
                    "principle": "Let tests drive the design, don't impose preconceived structure",
                    "practices": [
                        "Start with the simplest possible test",
                        "Allow abstractions to emerge naturally",
                        "Resist over-engineering in early stages",
                        "Use refactoring to improve design continuously"
                    ],
                    "design_feedback": "Tests act as first client of your API design"
                },
                "behavior_vs_implementation": {
                    "testing_philosophy": "Test the 'what' not the 'how'",
                    "behavioral_focus": [
                        "Test public interfaces and contracts",
                        "Focus on input-output relationships",
                        "Avoid testing private methods directly",
                        "Test the effect, not the mechanism"
                    ],
                    "refactoring_safety": "Behavior-focused tests enable fearless refactoring"
                }
            },
            "tdd_antipatterns_and_solutions": {
                "testing_antipatterns": {
                    "the_liar": {
                        "problem": "Test passes but doesn't test what it claims to test",
                        "solution": "Ensure test fails when expected behavior is broken",
                        "prevention": "Always see the test fail before making it pass"
                    },
                    "the_giant": {
                        "problem": "Tests that try to test too much at once",
                        "solution": "Break into smaller, focused tests",
                        "prevention": "One assertion per test as starting guideline"
                    },
                    "the_mockery": {
                        "problem": "Over-use of mocks leading to brittle tests",
                        "solution": "Use mocks judiciously, prefer real objects when feasible",
                        "prevention": "Mock roles, not objects; mock dependencies, not subjects"
                    },
                    "the_inspector": {
                        "problem": "Tests that examine internal state instead of behavior",
                        "solution": "Focus on public interface and observable effects",
                        "prevention": "Test through public methods only"
                    }
                },
                "development_antipatterns": {
                    "write_tests_later": {
                        "problem": "Writing implementation first, then tests",
                        "consequences": "Tests become implementation-dependent, miss design feedback",
                        "solution": "Strict discipline: no production code without failing test"
                    },
                    "big_design_up_front": {
                        "problem": "Planning entire architecture before starting TDD",
                        "consequences": "Reduces benefits of emergent design",
                        "solution": "Start with high-level design, let details emerge through TDD"
                    }
                }
            }
        }

    def _generate_specialist_recommendations(self, penpot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate TDD specialist specific recommendations"""

        return {
            "immediate_actions": [
                {
                    "priority": "Critical",
                    "action": "Establish TDD discipline and rhythm",
                    "timeline": "Week 1",
                    "details": "Start every coding session with a failing test. No exceptions.",
                    "success_metric": "100% of new code written test-first"
                },
                {
                    "priority": "High",
                    "action": "Set up continuous testing environment",
                    "timeline": "Week 1-2",
                    "details": "Configure IDE with automatic test running on file save",
                    "success_metric": "Tests run automatically within 5 seconds of code changes"
                },
                {
                    "priority": "High",
                    "action": "Create TDD kata practice routine",
                    "timeline": "Ongoing",
                    "details": "Daily 30-minute kata sessions to build TDD muscle memory",
                    "success_metric": "Complete one kata per week using strict TDD"
                }
            ],
            "weekly_practices": [
                {
                    "practice": "TDD Retrospectives",
                    "frequency": "Weekly",
                    "duration": "30 minutes",
                    "focus": "What TDD techniques worked well? Where did we struggle?",
                    "outcome": "Continuous improvement of TDD practices"
                },
                {
                    "practice": "Pair Programming with TDD Focus",
                    "frequency": "3 sessions per week",
                    "duration": "2-4 hours",
                    "approach": "One person navigates TDD process, other implements",
                    "benefit": "Knowledge sharing and technique refinement"
                }
            ],
            "monthly_assessments": [
                {
                    "assessment": "TDD Maturity Evaluation",
                    "method": "Code review analysis and team self-assessment",
                    "metrics": ["Test-first adherence", "Refactoring confidence", "Design quality"],
                    "action_plan": "Address gaps with targeted training and coaching"
                }
            ]
        }

    def _analyze_advanced_patterns(self, penpot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze opportunities for advanced TDD patterns"""

        return {
            "state_based_vs_interaction_testing": {
                "state_based_testing": {
                    "when_to_use": "Testing the state changes in your system",
                    "example_scenarios": [
                        "User account balance after transaction",
                        "Form validation state after input",
                        "Cache contents after operations"
                    ],
                    "advantages": ["More robust to implementation changes", "Clearer test intent"],
                    "pattern_example": """
# State-based testing example
def test_account_balance_after_deposit():
    account = Account(initial_balance=100)
    account.deposit(50)
    assert account.balance == 150
"""
                },
                "interaction_testing": {
                    "when_to_use": "Testing communication between objects",
                    "example_scenarios": [
                        "Email service called with correct parameters",
                        "Database save method invoked",
                        "Event listener triggered with proper data"
                    ],
                    "advantages": ["Verifies system behavior", "Catches integration issues"],
                    "pattern_example": """
# Interaction-based testing example
def test_notification_sent_on_account_creation():
    email_service = Mock()
    user_service = UserService(email_service)

    user_service.create_user("john@example.com")

    email_service.send_welcome_email.assert_called_once_with("john@example.com")
"""
                }
            },
            "property_based_testing_integration": {
                "concept": "Generate test cases automatically based on properties",
                "benefits": [
                    "Discovers edge cases you wouldn't think of",
                    "Provides high confidence through many test cases",
                    "Documents system invariants clearly"
                ],
                "implementation_with_tdd": [
                    "Start with example-based TDD for core functionality",
                    "Add property-based tests for invariants and edge cases",
                    "Use property tests to verify refactoring safety"
                ],
                "tools": ["Hypothesis (Python)", "fast-check (JavaScript)", "QuickCheck (Haskell)"]
            },
            "mutation_testing": {
                "purpose": "Test the quality of your tests by mutating code",
                "tdd_integration": [
                    "Run mutation tests after completing TDD cycles",
                    "Use mutation score to identify weak test coverage",
                    "Improve tests when mutations aren't caught"
                ],
                "interpretation": [
                    "High mutation score indicates strong test suite",
                    "Surviving mutants reveal weak or missing tests",
                    "Focus on behavior verification, not just code coverage"
                ]
            },
            "hexagonal_architecture_tdd": {
                "pattern": "Ports and Adapters architecture with TDD",
                "benefits": [
                    "Easy to mock external dependencies",
                    "Clear separation between business logic and infrastructure",
                    "Enables true unit testing of business logic"
                ],
                "tdd_approach": [
                    "Start with business logic using TDD",
                    "Create port interfaces driven by tests",
                    "Implement adapters with integration tests",
                    "Test entire system with acceptance tests"
                ]
            }
        }

    def _create_transformation_strategy(self, penpot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive team transformation strategy"""

        return {
            "organizational_change_management": {
                "stakeholder_alignment": {
                    "engineering_leadership": {
                        "key_messages": [
                            "TDD improves code quality and reduces long-term maintenance costs",
                            "Initial productivity decrease (20-30%) followed by significant gains",
                            "Better architecture emerges from test-driven design"
                        ],
                        "success_metrics": [
                            "Defect rate reduction by 60-90%",
                            "Development velocity increase after initial learning curve",
                            "Developer confidence and job satisfaction improvement"
                        ]
                    },
                    "product_management": {
                        "key_messages": [
                            "More predictable delivery through better quality",
                            "Reduced time spent on bug fixes and maintenance",
                            "Living documentation through comprehensive test suites"
                        ],
                        "collaboration_points": [
                            "Involve PMs in acceptance criteria definition",
                            "Use BDD scenarios for shared understanding",
                            "Demonstrate working software more frequently"
                        ]
                    },
                    "quality_assurance": {
                        "role_evolution": [
                            "Shift from bug finding to prevention",
                            "Focus on exploratory testing and user experience",
                            "Collaborate on test strategy and automation"
                        ],
                        "new_responsibilities": [
                            "Review and improve automated test coverage",
                            "Design user acceptance test scenarios",
                            "Performance and security testing specialization"
                        ]
                    }
                },
                "change_resistance_management": {
                    "common_objections": {
                        "too_slow": {
                            "response": "Initial slowdown leads to significant long-term speed gains",
                            "evidence": "Studies show 40-90% defect reduction and faster feature delivery",
                            "mitigation": "Start with simple features to build confidence and momentum"
                        },
                        "unnecessary_overhead": {
                            "response": "Tests become living documentation and design feedback tool",
                            "evidence": "Better code design emerges from testable architecture",
                            "mitigation": "Demonstrate design improvements through TDD examples"
                        },
                        "difficult_to_test": {
                            "response": "Difficulty testing reveals design problems, not testing problems",
                            "evidence": "Testable code is well-designed code with clear responsibilities",
                            "mitigation": "Provide training on designing for testability"
                        }
                    },
                    "adoption_strategies": {
                        "start_small": "Begin with new features or components rather than retrofitting",
                        "find_champions": "Identify early adopters who can demonstrate success",
                        "measure_progress": "Track metrics that show improvement over time",
                        "celebrate_wins": "Highlight successes and learning opportunities"
                    }
                }
            },
            "skill_development_program": {
                "competency_framework": {
                    "novice": {
                        "skills": ["Basic test writing", "Understanding TDD cycle"],
                        "development_focus": "Build TDD habits and discipline",
                        "mentoring_needs": "Close guidance and pair programming",
                        "timeline": "0-3 months"
                    },
                    "advanced_beginner": {
                        "skills": ["Consistent TDD application", "Basic refactoring"],
                        "development_focus": "Improve test design and refactoring skills",
                        "mentoring_needs": "Regular code reviews and feedback",
                        "timeline": "3-8 months"
                    },
                    "competent": {
                        "skills": ["Advanced testing patterns", "Design emergence"],
                        "development_focus": "Master complex scenarios and integration testing",
                        "mentoring_needs": "Peer learning and advanced workshops",
                        "timeline": "8-18 months"
                    },
                    "proficient": {
                        "skills": ["TDD coaching", "Process improvement"],
                        "development_focus": "Help others and optimize team practices",
                        "mentoring_needs": "Leadership training and external learning",
                        "timeline": "18+ months"
                    }
                },
                "learning_pathways": {
                    "hands_on_practice": {
                        "code_katas": [
                            "Bowling Game - Classic TDD example",
                            "Roman Numerals - Algorithm design with TDD",
                            "Mars Rover - Object-oriented design",
                            "Gilded Rose - Legacy code refactoring"
                        ],
                        "real_project_application": [
                            "Implement one new feature per week using TDD",
                            "Refactor one existing component using test-first approach",
                            "Add characterization tests to legacy code"
                        ]
                    },
                    "knowledge_building": {
                        "recommended_reading": [
                            "Test Driven Development by Kent Beck",
                            "Growing Object-Oriented Software, Guided by Tests by Freeman & Pryce",
                            "Refactoring by Martin Fowler",
                            "Clean Code by Robert Martin"
                        ],
                        "online_resources": [
                            "TDD workshops and screencasts",
                            "Conference talks on TDD practices",
                            "Community forums and discussion groups"
                        ]
                    }
                }
            },
            "sustainability_mechanisms": {
                "process_integration": {
                    "definition_of_done": "Include 'developed using TDD' in DoD checklist",
                    "code_review_guidelines": "Review TDD adherence alongside code quality",
                    "hiring_practices": "Include TDD skills in job requirements and interviews"
                },
                "continuous_improvement": {
                    "retrospective_focus": "Regular discussion of TDD practices and challenges",
                    "metrics_tracking": "Monitor TDD adoption rates and quality improvements",
                    "external_benchmarking": "Compare practices with industry leaders and standards"
                },
                "knowledge_preservation": {
                    "documentation": "Maintain team TDD playbook with examples and guidelines",
                    "mentoring_program": "Ensure knowledge transfer to new team members",
                    "community_engagement": "Participate in external TDD communities and conferences"
                }
            }
        }

def create_tdd_specialist_analysis(penpot_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point for TDD specialist analysis
    """
    specialist = TDDSpecialistAnalyzer()
    return specialist.analyze(penpot_data.get('extracted_data', {}), penpot_data.get('components', {}))

# Export for use in main analysis pipeline
__all__ = ['create_tdd_specialist_analysis', 'TDDSpecialistAnalyzer']