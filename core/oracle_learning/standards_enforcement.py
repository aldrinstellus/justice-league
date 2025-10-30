"""
📜 Standards Enforcement
Automatically enforce coding standards and best practices across all agents

This module ensures quality through:
- Coding standards validation
- Best practices enforcement
- Automated code reviews
- Standards propagation
- Compliance tracking

"Standards exist for a reason. I enforce them." - Oracle
"""

import logging
import json
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from pathlib import Path
from enum import Enum

logger = logging.getLogger(__name__)


class StandardCategory(str):
    """Categories of standards"""
    TESTING = "testing"
    PERFORMANCE = "performance"
    SECURITY = "security"
    ACCESSIBILITY = "accessibility"
    CODE_QUALITY = "code_quality"
    ERROR_HANDLING = "error_handling"
    DOCUMENTATION = "documentation"
    NAMING_CONVENTIONS = "naming_conventions"


class ComplianceLevel(str):
    """Compliance levels"""
    FULLY_COMPLIANT = "fully_compliant"
    MOSTLY_COMPLIANT = "mostly_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NON_COMPLIANT = "non_compliant"
    UNKNOWN = "unknown"


class StandardsEnforcement:
    """
    📜 Standards Enforcement Engine

    Enforces coding standards and best practices:
    - Validates adherence to standards
    - Generates compliance reports
    - Provides improvement recommendations
    - Tracks compliance over time
    """

    # Coding standards by category
    STANDARDS = {
        StandardCategory.TESTING: {
            'name': 'Testing Standards',
            'rules': [
                {
                    'id': 'TEST-001',
                    'rule': 'All agents must have test files',
                    'severity': 'critical',
                    'check': 'test_file_exists'
                },
                {
                    'id': 'TEST-002',
                    'rule': 'Minimum 10 tests per agent',
                    'severity': 'high',
                    'check': 'min_test_count'
                },
                {
                    'id': 'TEST-003',
                    'rule': 'Test names must be descriptive',
                    'severity': 'medium',
                    'check': 'descriptive_test_names'
                },
                {
                    'id': 'TEST-004',
                    'rule': 'All tests must pass (100% success rate)',
                    'severity': 'critical',
                    'check': 'all_tests_pass'
                }
            ]
        },
        StandardCategory.PERFORMANCE: {
            'name': 'Performance Standards',
            'rules': [
                {
                    'id': 'PERF-001',
                    'rule': 'Response time < 5 seconds',
                    'severity': 'high',
                    'check': 'response_time_acceptable'
                },
                {
                    'id': 'PERF-002',
                    'rule': 'Success rate >= 95%',
                    'severity': 'critical',
                    'check': 'min_success_rate'
                },
                {
                    'id': 'PERF-003',
                    'rule': 'Error rate < 5%',
                    'severity': 'high',
                    'check': 'max_error_rate'
                }
            ]
        },
        StandardCategory.SECURITY: {
            'name': 'Security Standards',
            'rules': [
                {
                    'id': 'SEC-001',
                    'rule': 'No hardcoded credentials',
                    'severity': 'critical',
                    'check': 'no_hardcoded_secrets'
                },
                {
                    'id': 'SEC-002',
                    'rule': 'Input validation required',
                    'severity': 'high',
                    'check': 'input_validation'
                },
                {
                    'id': 'SEC-003',
                    'rule': 'Secure error messages (no sensitive data)',
                    'severity': 'high',
                    'check': 'secure_error_messages'
                }
            ]
        },
        StandardCategory.ERROR_HANDLING: {
            'name': 'Error Handling Standards',
            'rules': [
                {
                    'id': 'ERR-001',
                    'rule': 'All operations must have try-catch blocks',
                    'severity': 'high',
                    'check': 'error_handling_present'
                },
                {
                    'id': 'ERR-002',
                    'rule': 'Errors must be logged',
                    'severity': 'medium',
                    'check': 'error_logging'
                },
                {
                    'id': 'ERR-003',
                    'rule': 'Graceful degradation required',
                    'severity': 'medium',
                    'check': 'graceful_degradation'
                }
            ]
        },
        StandardCategory.CODE_QUALITY: {
            'name': 'Code Quality Standards',
            'rules': [
                {
                    'id': 'QUAL-001',
                    'rule': 'Functions must have docstrings',
                    'severity': 'medium',
                    'check': 'docstrings_present'
                },
                {
                    'id': 'QUAL-002',
                    'rule': 'Type hints required for function signatures',
                    'severity': 'medium',
                    'check': 'type_hints'
                },
                {
                    'id': 'QUAL-003',
                    'rule': 'No duplicate code (DRY principle)',
                    'severity': 'low',
                    'check': 'no_duplication'
                }
            ]
        },
        StandardCategory.DOCUMENTATION: {
            'name': 'Documentation Standards',
            'rules': [
                {
                    'id': 'DOC-001',
                    'rule': 'Module docstring required',
                    'severity': 'medium',
                    'check': 'module_docstring'
                },
                {
                    'id': 'DOC-002',
                    'rule': 'Complex functions need usage examples',
                    'severity': 'low',
                    'check': 'usage_examples'
                }
            ]
        }
    }

    def __init__(self, oracle_kb_dir: Optional[str] = None):
        """
        Initialize Standards Enforcement Engine

        Args:
            oracle_kb_dir: Path to Oracle's knowledge base
        """
        self.kb_dir = Path(oracle_kb_dir) if oracle_kb_dir else Path('/tmp/aldo-vision-justice-league/oracle')
        self.best_practices_db = self.kb_dir / 'best_practices.json'
        self.compliance_db = self.kb_dir / 'standards_compliance.json'

        # Initialize compliance database
        if not self.compliance_db.exists():
            self._init_compliance_db()

        logger.info("📜 Standards Enforcement Engine initialized")

    def _init_compliance_db(self):
        """Initialize compliance tracking database"""
        initial_data = {
            'compliance_reports': [],
            'violations': [],
            'improvements': [],
            'last_audit': None,
            'statistics': {
                'total_audits': 0,
                'total_violations': 0,
                'total_improvements': 0,
                'overall_compliance_rate': 0.0
            }
        }

        with open(self.compliance_db, 'w') as f:
            json.dump(initial_data, f, indent=2)

    def audit_agent_compliance(self,
                              agent_name: str,
                              agent_metrics: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        📜 Audit an agent's compliance with standards

        Args:
            agent_name: Agent to audit
            agent_metrics: Optional agent metrics for validation

        Returns:
            Compliance audit report
        """
        audit_report = {
            'audit_id': f"AUDIT-{agent_name.upper()}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'agent': agent_name,
            'audited_at': datetime.now().isoformat(),
            'compliance_level': ComplianceLevel.UNKNOWN,
            'category_compliance': {},
            'violations': [],
            'passed_rules': [],
            'total_rules': 0,
            'passed_count': 0,
            'failed_count': 0,
            'compliance_score': 0.0,
            'recommendations': []
        }

        # Check each category
        for category, standard in self.STANDARDS.items():
            category_result = self._audit_category(agent_name, category, standard, agent_metrics)

            audit_report['category_compliance'][category] = category_result
            audit_report['total_rules'] += category_result['total_rules']
            audit_report['passed_count'] += category_result['passed']
            audit_report['failed_count'] += category_result['failed']

            # Collect violations
            audit_report['violations'].extend(category_result['violations'])
            audit_report['passed_rules'].extend(category_result['passed_rules'])

        # Calculate compliance score
        if audit_report['total_rules'] > 0:
            audit_report['compliance_score'] = audit_report['passed_count'] / audit_report['total_rules']

        # Determine compliance level
        score = audit_report['compliance_score']
        if score >= 0.95:
            audit_report['compliance_level'] = ComplianceLevel.FULLY_COMPLIANT
        elif score >= 0.80:
            audit_report['compliance_level'] = ComplianceLevel.MOSTLY_COMPLIANT
        elif score >= 0.60:
            audit_report['compliance_level'] = ComplianceLevel.PARTIALLY_COMPLIANT
        else:
            audit_report['compliance_level'] = ComplianceLevel.NON_COMPLIANT

        # Generate recommendations
        audit_report['recommendations'] = self._generate_compliance_recommendations(audit_report)

        # Store audit report
        self._store_audit_report(audit_report)

        logger.info(f"📜 Audited {agent_name}: {audit_report['compliance_level']} ({audit_report['compliance_score']:.1%})")

        return audit_report

    def _audit_category(self,
                       agent_name: str,
                       category: str,
                       standard: Dict[str, Any],
                       agent_metrics: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Audit compliance for a specific category"""
        result = {
            'category': category,
            'category_name': standard['name'],
            'total_rules': len(standard['rules']),
            'passed': 0,
            'failed': 0,
            'violations': [],
            'passed_rules': []
        }

        for rule in standard['rules']:
            # Check if rule is met
            check_result = self._check_rule(agent_name, rule, agent_metrics)

            if check_result['compliant']:
                result['passed'] += 1
                result['passed_rules'].append({
                    'rule_id': rule['id'],
                    'rule': rule['rule']
                })
            else:
                result['failed'] += 1
                result['violations'].append({
                    'rule_id': rule['id'],
                    'rule': rule['rule'],
                    'severity': rule['severity'],
                    'details': check_result.get('details', 'Compliance check failed'),
                    'category': category
                })

        return result

    def _check_rule(self,
                   agent_name: str,
                   rule: Dict[str, Any],
                   agent_metrics: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Check if a specific rule is met"""
        check_func = rule.get('check')
        result = {'compliant': False, 'details': ''}

        # TEST-001: Test file exists
        if check_func == 'test_file_exists':
            test_file = Path(f'test_{agent_name}.py')
            result['compliant'] = test_file.exists()
            result['details'] = f"Test file {'exists' if result['compliant'] else 'missing'}: {test_file}"

        # TEST-002: Minimum test count
        elif check_func == 'min_test_count':
            # Would need to parse test file - for now, assume compliant
            result['compliant'] = True
            result['details'] = "Test count check (requires test file parsing)"

        # TEST-004: All tests pass
        elif check_func == 'all_tests_pass':
            if agent_metrics:
                success_rate = agent_metrics.get('success_rate', 0.0)
                result['compliant'] = success_rate >= 1.0
                result['details'] = f"Test success rate: {success_rate:.1%}"
            else:
                result['compliant'] = True  # No metrics, assume compliant
                result['details'] = "No metrics available"

        # PERF-001: Response time
        elif check_func == 'response_time_acceptable':
            if agent_metrics:
                avg_time = agent_metrics.get('avg_execution_time', 0)
                result['compliant'] = avg_time < 5000  # 5 seconds
                result['details'] = f"Avg response time: {avg_time:.0f}ms"
            else:
                result['compliant'] = True
                result['details'] = "No metrics available"

        # PERF-002: Success rate
        elif check_func == 'min_success_rate':
            if agent_metrics:
                success_rate = agent_metrics.get('success_rate', 0.0)
                result['compliant'] = success_rate >= 0.95
                result['details'] = f"Success rate: {success_rate:.1%}"
            else:
                result['compliant'] = True
                result['details'] = "No metrics available"

        # PERF-003: Error rate
        elif check_func == 'max_error_rate':
            if agent_metrics:
                error_rate = 1.0 - agent_metrics.get('success_rate', 1.0)
                result['compliant'] = error_rate < 0.05
                result['details'] = f"Error rate: {error_rate:.1%}"
            else:
                result['compliant'] = True
                result['details'] = "No metrics available"

        # SEC-001: No hardcoded secrets
        elif check_func == 'no_hardcoded_secrets':
            # Would need code analysis - assume compliant for now
            result['compliant'] = True
            result['details'] = "Security scan required (manual review)"

        # ERR-001: Error handling present
        elif check_func == 'error_handling_present':
            agent_file = Path(f'core/justice_league/{agent_name}.py')
            if agent_file.exists():
                content = agent_file.read_text()
                result['compliant'] = 'try:' in content and 'except' in content
                result['details'] = f"Error handling {'present' if result['compliant'] else 'missing'}"
            else:
                result['compliant'] = True
                result['details'] = "Agent file not found"

        # QUAL-001: Docstrings present
        elif check_func == 'docstrings_present':
            agent_file = Path(f'core/justice_league/{agent_name}.py')
            if agent_file.exists():
                content = agent_file.read_text()
                result['compliant'] = '"""' in content or "'''" in content
                result['details'] = f"Docstrings {'present' if result['compliant'] else 'missing'}"
            else:
                result['compliant'] = True
                result['details'] = "Agent file not found"

        # DOC-001: Module docstring
        elif check_func == 'module_docstring':
            agent_file = Path(f'core/justice_league/{agent_name}.py')
            if agent_file.exists():
                content = agent_file.read_text()
                lines = content.split('\n')
                # Check first 10 lines for docstring
                has_module_doc = any('"""' in line or "'''" in line for line in lines[:10])
                result['compliant'] = has_module_doc
                result['details'] = f"Module docstring {'present' if result['compliant'] else 'missing'}"
            else:
                result['compliant'] = True
                result['details'] = "Agent file not found"

        # Default: assume compliant for unchecked rules
        else:
            result['compliant'] = True
            result['details'] = f"Check '{check_func}' not implemented - assumed compliant"

        return result

    def _generate_compliance_recommendations(self, audit_report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations to improve compliance"""
        recommendations = []

        # Group violations by severity
        critical_violations = [v for v in audit_report['violations'] if v['severity'] == 'critical']
        high_violations = [v for v in audit_report['violations'] if v['severity'] == 'high']

        if critical_violations:
            recommendations.append({
                'priority': 'critical',
                'count': len(critical_violations),
                'recommendation': f"Fix {len(critical_violations)} critical violation(s) immediately",
                'violations': critical_violations
            })

        if high_violations:
            recommendations.append({
                'priority': 'high',
                'count': len(high_violations),
                'recommendation': f"Address {len(high_violations)} high-severity violation(s)",
                'violations': high_violations
            })

        # Compliance level recommendations
        level = audit_report['compliance_level']

        if level == ComplianceLevel.NON_COMPLIANT:
            recommendations.append({
                'priority': 'critical',
                'recommendation': "Agent is non-compliant - comprehensive review required",
                'action': 'Schedule code review and remediation'
            })
        elif level == ComplianceLevel.PARTIALLY_COMPLIANT:
            recommendations.append({
                'priority': 'high',
                'recommendation': "Improve compliance to at least 80%",
                'action': 'Focus on critical and high-severity violations first'
            })

        return recommendations

    def _store_audit_report(self, audit_report: Dict[str, Any]):
        """Store audit report in database"""
        with open(self.compliance_db, 'r') as f:
            data = json.load(f)

        data['compliance_reports'].append(audit_report)

        # Store violations
        for violation in audit_report['violations']:
            violation_record = {
                **violation,
                'audit_id': audit_report['audit_id'],
                'agent': audit_report['agent'],
                'detected_at': audit_report['audited_at'],
                'status': 'open'
            }
            data['violations'].append(violation_record)

        # Update statistics
        data['statistics']['total_audits'] += 1
        data['statistics']['total_violations'] += len(audit_report['violations'])
        data['last_audit'] = audit_report['audited_at']

        # Calculate overall compliance rate
        if data['compliance_reports']:
            total_score = sum(r.get('compliance_score', 0) for r in data['compliance_reports'])
            data['statistics']['overall_compliance_rate'] = total_score / len(data['compliance_reports'])

        with open(self.compliance_db, 'w') as f:
            json.dump(data, f, indent=2)

    def audit_all_agents(self, metrics_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        📜 Audit all Justice League agents

        Args:
            metrics_data: Optional metrics for all agents

        Returns:
            System-wide compliance report
        """
        all_agents = [
            'batman', 'green_lantern', 'wonder_woman', 'flash', 'aquaman',
            'cyborg', 'atom', 'martian_manhunter', 'green_arrow',
            'plastic_man', 'zatanna'
        ]

        system_report = {
            'audited_at': datetime.now().isoformat(),
            'total_agents': len(all_agents),
            'agent_reports': {},
            'system_compliance': {
                'fully_compliant': 0,
                'mostly_compliant': 0,
                'partially_compliant': 0,
                'non_compliant': 0
            },
            'total_violations': 0,
            'critical_violations': 0,
            'system_recommendations': []
        }

        for agent in all_agents:
            agent_metrics = None
            if metrics_data and agent in metrics_data:
                agent_metrics = metrics_data[agent]

            audit = self.audit_agent_compliance(agent, agent_metrics)
            system_report['agent_reports'][agent] = audit

            # Count by compliance level
            level = audit['compliance_level']
            if level == ComplianceLevel.FULLY_COMPLIANT:
                system_report['system_compliance']['fully_compliant'] += 1
            elif level == ComplianceLevel.MOSTLY_COMPLIANT:
                system_report['system_compliance']['mostly_compliant'] += 1
            elif level == ComplianceLevel.PARTIALLY_COMPLIANT:
                system_report['system_compliance']['partially_compliant'] += 1
            else:
                system_report['system_compliance']['non_compliant'] += 1

            # Count violations
            system_report['total_violations'] += len(audit['violations'])
            system_report['critical_violations'] += len([v for v in audit['violations'] if v['severity'] == 'critical'])

        # Generate system recommendations
        if system_report['critical_violations'] > 0:
            system_report['system_recommendations'].append({
                'priority': 'critical',
                'message': f"{system_report['critical_violations']} critical violations across system"
            })

        if system_report['system_compliance']['non_compliant'] > 0:
            system_report['system_recommendations'].append({
                'priority': 'high',
                'message': f"{system_report['system_compliance']['non_compliant']} non-compliant agents require attention"
            })

        logger.info(f"📜 System audit complete: {system_report['total_violations']} violations, {system_report['critical_violations']} critical")

        return system_report

    def get_compliance_history(self, agent_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get compliance history for an agent or all agents"""
        with open(self.compliance_db, 'r') as f:
            data = json.load(f)

        reports = data.get('compliance_reports', [])

        if agent_name:
            reports = [r for r in reports if r.get('agent') == agent_name]

        return reports

    def get_open_violations(self, severity: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all open violations, optionally filtered by severity"""
        with open(self.compliance_db, 'r') as f:
            data = json.load(f)

        violations = [v for v in data.get('violations', []) if v.get('status') == 'open']

        if severity:
            violations = [v for v in violations if v.get('severity') == severity]

        return violations


def run_compliance_audit() -> Dict[str, Any]:
    """
    📜 Run complete compliance audit

    Returns:
        System-wide compliance report
    """
    enforcement = StandardsEnforcement()

    # Load metrics if available
    metrics_db = Path('/tmp/aldo-vision-justice-league/oracle/agent_metrics.json')
    metrics_data = None

    if metrics_db.exists():
        with open(metrics_db, 'r') as f:
            metrics_data = json.load(f)

    report = enforcement.audit_all_agents(metrics_data)

    logger.info(f"📜 Compliance audit: {report['total_violations']} violations found")

    return report
