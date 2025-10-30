"""
✅ Oracle Approval Workflow
Human oversight system for fix proposals

This module provides workflow for fix proposal approval:
- Review queue management
- Approval/rejection tracking
- Implementation scheduling
- Post-implementation validation
- Audit trail

"Trust, but verify. Every fix needs human approval." - Oracle
"""

import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
from enum import Enum

logger = logging.getLogger(__name__)


class ApprovalStatus(str):
    """Approval workflow statuses"""
    PENDING_REVIEW = "pending_review"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    APPROVED_WITH_CONDITIONS = "approved_with_conditions"
    REJECTED = "rejected"
    IMPLEMENTED = "implemented"
    VERIFIED = "verified"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class ReviewerRole(str):
    """Reviewer role types"""
    DEVELOPER = "developer"
    LEAD_DEVELOPER = "lead_developer"
    TECH_LEAD = "tech_lead"
    ARCHITECT = "architect"
    ORACLE = "oracle"  # Oracle's automated review


class ApprovalWorkflow:
    """
    ✅ Fix Proposal Approval Workflow

    Manages the approval process for fix proposals:
    1. Proposal submission → Review queue
    2. Human review → Approve/Reject/Request changes
    3. Approved → Testing → Implementation
    4. Implementation → Verification → Close
    5. Complete audit trail maintained
    """

    def __init__(self, workflow_db_path: Optional[str] = None):
        """
        Initialize Approval Workflow

        Args:
            workflow_db_path: Path to workflow database
        """
        self.workflow_db_path = Path(workflow_db_path) if workflow_db_path else Path('/tmp/aldo-vision-justice-league/oracle/approval_workflow.json')
        self.workflow_db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize database
        if not self.workflow_db_path.exists():
            self._init_workflow_db()

        logger.info("✅ Approval Workflow initialized")

    def _init_workflow_db(self):
        """Initialize approval workflow database"""
        initial_data = {
            'workflows': [],
            'review_queue': [],
            'approved_queue': [],
            'implemented_fixes': [],
            'rejected_fixes': [],
            'audit_log': [],
            'last_updated': datetime.now().isoformat(),
            'statistics': {
                'total_submitted': 0,
                'total_approved': 0,
                'total_rejected': 0,
                'total_implemented': 0,
                'avg_review_time_hours': 0.0,
                'success_rate': 0.0
            }
        }

        with open(self.workflow_db_path, 'w') as f:
            json.dump(initial_data, f, indent=2)

    def submit_for_review(self,
                         proposal: Dict[str, Any],
                         submitted_by: str = 'Oracle',
                         priority: str = 'medium') -> Dict[str, Any]:
        """
        ✅ Submit fix proposal for human review

        Args:
            proposal: Fix proposal to submit
            submitted_by: Who is submitting (default: Oracle)
            priority: Priority level (low/medium/high/critical)

        Returns:
            Workflow record
        """
        with open(self.workflow_db_path, 'r') as f:
            data = json.load(f)

        workflow_record = {
            'workflow_id': f"WF-{datetime.now().strftime('%Y%m%d%H%M%S')}-{len(data['workflows'])}",
            'proposal_id': proposal.get('proposal_id'),
            'agent': proposal.get('agent'),
            'issue_type': proposal.get('issue', {}).get('type'),
            'issue_severity': proposal.get('issue', {}).get('severity', 'medium'),
            'submitted_at': datetime.now().isoformat(),
            'submitted_by': submitted_by,
            'priority': priority,
            'status': ApprovalStatus.PENDING_REVIEW,
            'risk_level': proposal.get('risk_assessment', {}).get('overall_risk', 'unknown'),
            'estimated_effort': proposal.get('estimated_effort', 'unknown'),
            'proposal': proposal,
            'review_history': [],
            'current_reviewer': None,
            'approval_decision': None,
            'implementation_result': None,
            'verification_result': None
        }

        # Add to workflows
        data['workflows'].append(workflow_record)

        # Add to review queue
        data['review_queue'].append(workflow_record['workflow_id'])

        # Update statistics
        data['statistics']['total_submitted'] += 1

        # Add audit log entry
        self._add_audit_log(data, workflow_record['workflow_id'], 'submitted', submitted_by,
                           f"Fix proposal submitted for {workflow_record['agent']}")

        data['last_updated'] = datetime.now().isoformat()

        with open(self.workflow_db_path, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"✅ Submitted workflow {workflow_record['workflow_id']} for review")

        return workflow_record

    def assign_reviewer(self,
                       workflow_id: str,
                       reviewer: str,
                       reviewer_role: str = ReviewerRole.DEVELOPER) -> bool:
        """
        Assign a reviewer to a workflow

        Args:
            workflow_id: Workflow ID to assign
            reviewer: Reviewer name
            reviewer_role: Reviewer's role

        Returns:
            True if assigned successfully
        """
        with open(self.workflow_db_path, 'r') as f:
            data = json.load(f)

        for workflow in data['workflows']:
            if workflow['workflow_id'] == workflow_id:
                workflow['current_reviewer'] = reviewer
                workflow['status'] = ApprovalStatus.UNDER_REVIEW
                workflow['review_started_at'] = datetime.now().isoformat()

                workflow['review_history'].append({
                    'action': 'assigned',
                    'reviewer': reviewer,
                    'reviewer_role': reviewer_role,
                    'timestamp': datetime.now().isoformat()
                })

                self._add_audit_log(data, workflow_id, 'assigned', reviewer,
                                   f"Assigned to {reviewer} ({reviewer_role})")

                data['last_updated'] = datetime.now().isoformat()

                with open(self.workflow_db_path, 'w') as f:
                    json.dump(data, f, indent=2)

                logger.info(f"✅ Assigned workflow {workflow_id} to {reviewer}")
                return True

        return False

    def approve_fix(self,
                   workflow_id: str,
                   reviewer: str,
                   comments: Optional[str] = None,
                   conditions: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Approve a fix proposal

        Args:
            workflow_id: Workflow ID to approve
            reviewer: Reviewer name
            comments: Optional approval comments
            conditions: Optional conditions for approval

        Returns:
            Updated workflow record
        """
        with open(self.workflow_db_path, 'r') as f:
            data = json.load(f)

        for workflow in data['workflows']:
            if workflow['workflow_id'] == workflow_id:
                # Determine approval status
                if conditions:
                    workflow['status'] = ApprovalStatus.APPROVED_WITH_CONDITIONS
                else:
                    workflow['status'] = ApprovalStatus.APPROVED

                workflow['approval_decision'] = {
                    'approved': True,
                    'approved_by': reviewer,
                    'approved_at': datetime.now().isoformat(),
                    'comments': comments,
                    'conditions': conditions or [],
                    'decision_type': workflow['status']
                }

                workflow['review_history'].append({
                    'action': 'approved',
                    'reviewer': reviewer,
                    'timestamp': datetime.now().isoformat(),
                    'comments': comments,
                    'conditions': conditions
                })

                # Move to approved queue
                if workflow_id in data['review_queue']:
                    data['review_queue'].remove(workflow_id)
                data['approved_queue'].append(workflow_id)

                # Update statistics
                data['statistics']['total_approved'] += 1

                # Calculate review time
                if 'review_started_at' in workflow:
                    review_time = (
                        datetime.fromisoformat(workflow['approval_decision']['approved_at']) -
                        datetime.fromisoformat(workflow['review_started_at'])
                    )
                    review_hours = review_time.total_seconds() / 3600

                    # Update average review time
                    current_avg = data['statistics']['avg_review_time_hours']
                    total_approved = data['statistics']['total_approved']
                    data['statistics']['avg_review_time_hours'] = round(
                        (current_avg * (total_approved - 1) + review_hours) / total_approved, 2
                    )

                self._add_audit_log(data, workflow_id, 'approved', reviewer,
                                   f"Approved by {reviewer}" + (f" with conditions: {conditions}" if conditions else ""))

                data['last_updated'] = datetime.now().isoformat()

                with open(self.workflow_db_path, 'w') as f:
                    json.dump(data, f, indent=2)

                logger.info(f"✅ Approved workflow {workflow_id} by {reviewer}")

                return workflow

        return {}

    def reject_fix(self,
                  workflow_id: str,
                  reviewer: str,
                  reason: str,
                  suggestions: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Reject a fix proposal

        Args:
            workflow_id: Workflow ID to reject
            reviewer: Reviewer name
            reason: Reason for rejection
            suggestions: Optional suggestions for improvement

        Returns:
            Updated workflow record
        """
        with open(self.workflow_db_path, 'r') as f:
            data = json.load(f)

        for workflow in data['workflows']:
            if workflow['workflow_id'] == workflow_id:
                workflow['status'] = ApprovalStatus.REJECTED

                workflow['approval_decision'] = {
                    'approved': False,
                    'rejected_by': reviewer,
                    'rejected_at': datetime.now().isoformat(),
                    'reason': reason,
                    'suggestions': suggestions or [],
                }

                workflow['review_history'].append({
                    'action': 'rejected',
                    'reviewer': reviewer,
                    'timestamp': datetime.now().isoformat(),
                    'reason': reason,
                    'suggestions': suggestions
                })

                # Move to rejected queue
                if workflow_id in data['review_queue']:
                    data['review_queue'].remove(workflow_id)
                data['rejected_fixes'].append(workflow)

                # Update statistics
                data['statistics']['total_rejected'] += 1

                self._add_audit_log(data, workflow_id, 'rejected', reviewer,
                                   f"Rejected by {reviewer}: {reason}")

                data['last_updated'] = datetime.now().isoformat()

                with open(self.workflow_db_path, 'w') as f:
                    json.dump(data, f, indent=2)

                logger.info(f"❌ Rejected workflow {workflow_id}: {reason}")

                return workflow

        return {}

    def record_implementation(self,
                            workflow_id: str,
                            implemented_by: str,
                            success: bool,
                            details: str,
                            test_results: Optional[Dict[str, Any]] = None) -> bool:
        """
        Record fix implementation results

        Args:
            workflow_id: Workflow ID
            implemented_by: Who implemented the fix
            success: Whether implementation succeeded
            details: Implementation details
            test_results: Optional test results

        Returns:
            True if recorded successfully
        """
        with open(self.workflow_db_path, 'r') as f:
            data = json.load(f)

        for workflow in data['workflows']:
            if workflow['workflow_id'] == workflow_id:
                workflow['implementation_result'] = {
                    'success': success,
                    'implemented_by': implemented_by,
                    'implemented_at': datetime.now().isoformat(),
                    'details': details,
                    'test_results': test_results
                }

                if success:
                    workflow['status'] = ApprovalStatus.IMPLEMENTED

                    # Remove from approved queue
                    if workflow_id in data['approved_queue']:
                        data['approved_queue'].remove(workflow_id)

                    # Update statistics
                    data['statistics']['total_implemented'] += 1

                    self._add_audit_log(data, workflow_id, 'implemented', implemented_by,
                                       f"Successfully implemented by {implemented_by}")
                else:
                    workflow['status'] = ApprovalStatus.FAILED

                    self._add_audit_log(data, workflow_id, 'implementation_failed', implemented_by,
                                       f"Implementation failed: {details}")

                workflow['review_history'].append({
                    'action': 'implemented' if success else 'implementation_failed',
                    'implemented_by': implemented_by,
                    'timestamp': datetime.now().isoformat(),
                    'success': success,
                    'details': details
                })

                data['last_updated'] = datetime.now().isoformat()

                with open(self.workflow_db_path, 'w') as f:
                    json.dump(data, f, indent=2)

                logger.info(f"✅ Recorded implementation for {workflow_id}: {'success' if success else 'failed'}")

                return True

        return False

    def verify_fix(self,
                  workflow_id: str,
                  verified_by: str,
                  verification_passed: bool,
                  verification_details: str) -> bool:
        """
        Verify that implemented fix resolves the issue

        Args:
            workflow_id: Workflow ID
            verified_by: Who verified the fix
            verification_passed: Whether verification passed
            verification_details: Verification details

        Returns:
            True if recorded successfully
        """
        with open(self.workflow_db_path, 'r') as f:
            data = json.load(f)

        for workflow in data['workflows']:
            if workflow['workflow_id'] == workflow_id:
                workflow['verification_result'] = {
                    'passed': verification_passed,
                    'verified_by': verified_by,
                    'verified_at': datetime.now().isoformat(),
                    'details': verification_details
                }

                if verification_passed:
                    workflow['status'] = ApprovalStatus.VERIFIED

                    # Move to implemented fixes
                    data['implemented_fixes'].append(workflow)

                    # Calculate success rate
                    total_implemented = data['statistics']['total_implemented']
                    if total_implemented > 0:
                        successful = len([f for f in data['implemented_fixes']
                                        if f.get('verification_result', {}).get('passed', False)])
                        data['statistics']['success_rate'] = round(successful / total_implemented, 3)

                    self._add_audit_log(data, workflow_id, 'verified', verified_by,
                                       f"Fix verified successfully by {verified_by}")
                else:
                    workflow['status'] = ApprovalStatus.FAILED

                    self._add_audit_log(data, workflow_id, 'verification_failed', verified_by,
                                       f"Verification failed: {verification_details}")

                workflow['review_history'].append({
                    'action': 'verified' if verification_passed else 'verification_failed',
                    'verified_by': verified_by,
                    'timestamp': datetime.now().isoformat(),
                    'passed': verification_passed,
                    'details': verification_details
                })

                data['last_updated'] = datetime.now().isoformat()

                with open(self.workflow_db_path, 'w') as f:
                    json.dump(data, f, indent=2)

                logger.info(f"✅ Verification for {workflow_id}: {'passed' if verification_passed else 'failed'}")

                return True

        return False

    def get_review_queue(self, priority_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get current review queue

        Args:
            priority_filter: Optional priority filter (low/medium/high/critical)

        Returns:
            List of workflows pending review
        """
        with open(self.workflow_db_path, 'r') as f:
            data = json.load(f)

        review_queue = []

        for workflow_id in data.get('review_queue', []):
            for workflow in data['workflows']:
                if workflow['workflow_id'] == workflow_id:
                    if priority_filter is None or workflow.get('priority') == priority_filter:
                        review_queue.append(workflow)

        # Sort by priority and submission time
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        review_queue.sort(key=lambda x: (
            priority_order.get(x.get('priority', 'medium'), 2),
            x.get('submitted_at', '')
        ))

        return review_queue

    def get_approved_queue(self) -> List[Dict[str, Any]]:
        """Get queue of approved fixes ready for implementation"""
        with open(self.workflow_db_path, 'r') as f:
            data = json.load(f)

        approved_queue = []

        for workflow_id in data.get('approved_queue', []):
            for workflow in data['workflows']:
                if workflow['workflow_id'] == workflow_id:
                    approved_queue.append(workflow)

        return approved_queue

    def get_workflow_stats(self) -> Dict[str, Any]:
        """Get workflow statistics"""
        with open(self.workflow_db_path, 'r') as f:
            data = json.load(f)

        stats = data.get('statistics', {})

        # Add current queue sizes
        stats['current_review_queue'] = len(data.get('review_queue', []))
        stats['current_approved_queue'] = len(data.get('approved_queue', []))

        return stats

    def get_workflow_by_id(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow by ID"""
        with open(self.workflow_db_path, 'r') as f:
            data = json.load(f)

        for workflow in data['workflows']:
            if workflow['workflow_id'] == workflow_id:
                return workflow

        return None

    def get_audit_log(self, workflow_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get audit log

        Args:
            workflow_id: Optional filter by workflow ID
            limit: Maximum number of entries to return

        Returns:
            Audit log entries
        """
        with open(self.workflow_db_path, 'r') as f:
            data = json.load(f)

        audit_log = data.get('audit_log', [])

        if workflow_id:
            audit_log = [entry for entry in audit_log if entry.get('workflow_id') == workflow_id]

        # Return most recent entries
        return audit_log[-limit:]

    def _add_audit_log(self,
                      data: Dict[str, Any],
                      workflow_id: str,
                      action: str,
                      user: str,
                      description: str):
        """Add entry to audit log"""
        data['audit_log'].append({
            'workflow_id': workflow_id,
            'action': action,
            'user': user,
            'timestamp': datetime.now().isoformat(),
            'description': description
        })


def generate_workflow_report() -> Dict[str, Any]:
    """
    ✅ Generate comprehensive workflow report

    Returns:
        Complete workflow status report
    """
    workflow = ApprovalWorkflow()

    stats = workflow.get_workflow_stats()
    review_queue = workflow.get_review_queue()
    approved_queue = workflow.get_approved_queue()

    # Categorize review queue by priority
    queue_by_priority = {
        'critical': [w for w in review_queue if w.get('priority') == 'critical'],
        'high': [w for w in review_queue if w.get('priority') == 'high'],
        'medium': [w for w in review_queue if w.get('priority') == 'medium'],
        'low': [w for w in review_queue if w.get('priority') == 'low']
    }

    report = {
        'timestamp': datetime.now().isoformat(),
        'statistics': stats,
        'review_queue': {
            'total': len(review_queue),
            'by_priority': {
                'critical': len(queue_by_priority['critical']),
                'high': len(queue_by_priority['high']),
                'medium': len(queue_by_priority['medium']),
                'low': len(queue_by_priority['low'])
            },
            'oldest_pending': review_queue[0] if review_queue else None
        },
        'approved_queue': {
            'total': len(approved_queue),
            'ready_for_implementation': approved_queue
        },
        'recommendations': []
    }

    # Generate recommendations
    if queue_by_priority['critical']:
        report['recommendations'].append({
            'priority': 'critical',
            'message': f"{len(queue_by_priority['critical'])} critical fix(es) pending review"
        })

    if len(review_queue) > 10:
        report['recommendations'].append({
            'priority': 'high',
            'message': f"Review queue backing up ({len(review_queue)} items) - consider additional reviewers"
        })

    if len(approved_queue) > 0:
        report['recommendations'].append({
            'priority': 'medium',
            'message': f"{len(approved_queue)} approved fix(es) ready for implementation"
        })

    return report
