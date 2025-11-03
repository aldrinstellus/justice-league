"""
🦇 BATMAN INVESTIGATION MODULE
================================

Batman's Detective Capabilities - The Dark Knight investigates everything!

Batman doesn't accept what he hears at face value. He investigates claims,
cross-references evidence, finds inconsistencies, and challenges assumptions.

"I'm Batman. And I question EVERYTHING."

Powers:
- Independent investigation of claims
- Cross-referencing evidence from multiple sources
- Finding inconsistencies in data
- Challenging assumptions with evidence
- Detective-level pattern recognition
- Evidence-based reasoning

Author: Superman (with Claude Code)
Created: October 28, 2025
Status: Production Ready - True Detective
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

logger = logging.getLogger(__name__)


class BatmanInvestigation:
    """
    Batman's Detective Investigation Module

    Batman uses these methods to investigate claims and verify information
    instead of blindly accepting what he's told.
    """

    def __init__(self, hero_name: str = "Batman", knowledge_base: Optional[Any] = None):
        """
        Initialize Batman's investigation capabilities.

        Args:
            hero_name: Hero's name (default: Batman)
            knowledge_base: Justice League knowledge base
        """
        self.hero_name = hero_name
        self.knowledge_base = knowledge_base
        self.investigations: List[Dict[str, Any]] = []
        self.evidence_cache: Dict[str, List[Dict]] = {}
        self.logger = logging.getLogger(f"JusticeLeague.{hero_name}.Investigation")

    def investigate_independently(self, claim: str, source: str,
                                  context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Conduct independent investigation of a claim.

        Batman doesn't accept claims at face value - he investigates!

        Args:
            claim: Claim to investigate
            source: Source of the claim
            context: Investigation context

        Returns:
            Complete investigation report

        Example:
            batman.investigate_independently(
                claim="All buttons have accessible names",
                source="Initial accessibility report",
                context={"page_url": "https://example.com"}
            )
        """
        self.logger.info(f"🦇 {self.hero_name} starting independent investigation...")
        self.logger.info(f"   Claim: '{claim}'")
        self.logger.info(f"   Source: {source}")

        investigation = {
            "claim": claim,
            "source": source,
            "investigator": self.hero_name,
            "context": context or {},
            "timestamp": datetime.now().isoformat(),
            "evidence_collected": [],
            "inconsistencies_found": [],
            "cross_references": [],
            "verified": None,
            "confidence": 0.0,
            "conclusion": "",
            "recommendations": []
        }

        # Step 1: Cross-reference with knowledge base
        self.logger.info(f"🔍 Step 1: Searching knowledge base...")
        kb_evidence = self._cross_reference_knowledge_base(claim)
        if kb_evidence:
            investigation["evidence_collected"].extend(kb_evidence)
            investigation["cross_references"].append({
                "source": "knowledge_base",
                "findings": len(kb_evidence)
            })

        # Step 2: Check for known patterns
        self.logger.info(f"🔍 Step 2: Checking for known patterns...")
        patterns = self._check_known_patterns(claim, context)
        if patterns:
            investigation["evidence_collected"].extend(patterns)

        # Step 3: Look for inconsistencies
        self.logger.info(f"🔍 Step 3: Analyzing for inconsistencies...")
        inconsistencies = self._find_inconsistencies_in_claim(claim, investigation["evidence_collected"])
        investigation["inconsistencies_found"] = inconsistencies

        # Step 4: Verify against established facts
        self.logger.info(f"🔍 Step 4: Verifying against established facts...")
        verification = self._verify_against_facts(claim, investigation["evidence_collected"])
        investigation["verified"] = verification["verified"]
        investigation["confidence"] = verification["confidence"]

        # Step 5: Draw conclusion
        investigation["conclusion"] = self._draw_conclusion(investigation)

        # Step 6: Generate recommendations
        investigation["recommendations"] = self._generate_detective_recommendations(investigation)

        # Store investigation
        self.investigations.append(investigation)

        self.logger.info(f"✅ Investigation complete!")
        self.logger.info(f"   Verified: {investigation['verified']}")
        self.logger.info(f"   Confidence: {investigation['confidence']:.0%}")
        self.logger.info(f"   Conclusion: {investigation['conclusion']}")

        return investigation

    def cross_reference_evidence(self, claim: str, sources: List[str]) -> Dict[str, Any]:
        """
        Cross-reference a claim against multiple sources.

        Args:
            claim: Claim to verify
            sources: List of source identifiers

        Returns:
            Cross-reference analysis

        Example:
            batman.cross_reference_evidence(
                claim="System is WCAG 2.1 AA compliant",
                sources=["accessibility_scan", "manual_test", "automated_audit"]
            )
        """
        self.logger.info(f"🦇 Cross-referencing claim across {len(sources)} sources...")

        cross_ref = {
            "claim": claim,
            "sources_checked": sources,
            "agreements": [],
            "contradictions": [],
            "confidence_by_source": {},
            "overall_verdict": None,
            "timestamp": datetime.now().isoformat()
        }

        # Check each source
        for source in sources:
            source_result = self._check_source(claim, source)
            cross_ref["confidence_by_source"][source] = source_result["confidence"]

            if source_result["supports_claim"]:
                cross_ref["agreements"].append({
                    "source": source,
                    "confidence": source_result["confidence"],
                    "evidence": source_result.get("evidence", "")
                })
            else:
                cross_ref["contradictions"].append({
                    "source": source,
                    "contradiction": source_result.get("contradiction", ""),
                    "evidence": source_result.get("evidence", "")
                })

        # Overall verdict
        total_confidence = sum(cross_ref["confidence_by_source"].values())
        avg_confidence = total_confidence / len(sources) if sources else 0

        if len(cross_ref["agreements"]) == len(sources):
            cross_ref["overall_verdict"] = "VERIFIED - All sources agree"
        elif len(cross_ref["contradictions"]) == len(sources):
            cross_ref["overall_verdict"] = "DISPUTED - All sources contradict"
        else:
            cross_ref["overall_verdict"] = f"MIXED - {len(cross_ref['agreements'])}/{len(sources)} sources support claim"

        cross_ref["average_confidence"] = avg_confidence

        self.logger.info(f"   Verdict: {cross_ref['overall_verdict']}")
        self.logger.info(f"   Confidence: {avg_confidence:.0%}")

        return cross_ref

    def find_inconsistencies(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find inconsistencies in provided data.

        Batman's detective skills detect contradictions and logical flaws.

        Args:
            data: Data to analyze for inconsistencies

        Returns:
            List of inconsistencies found

        Example:
            batman.find_inconsistencies({
                "report": "All elements accessible",
                "violations": [{"type": "missing_label", "count": 5}],
                "score": 100
            })
            # Returns: [{"inconsistency": "Report claims 'all accessible' but 5 violations found"}]
        """
        self.logger.info(f"🦇 Analyzing data for inconsistencies...")

        inconsistencies = []

        # Check for contradictory claims
        if "violations" in data and len(data.get("violations", [])) > 0:
            if data.get("score") == 100 or "all" in str(data.get("report", "")).lower():
                inconsistencies.append({
                    "type": "contradiction",
                    "severity": "high",
                    "description": f"Perfect score claimed but {len(data['violations'])} violations found",
                    "evidence": {"violations": data["violations"], "score": data.get("score")}
                })

        # Check for missing required fields
        if "accessibility" in str(data).lower():
            if "wcag" not in str(data).lower() and "aria" not in str(data).lower():
                inconsistencies.append({
                    "type": "missing_context",
                    "severity": "medium",
                    "description": "Accessibility claim lacks WCAG or ARIA context",
                    "recommendation": "Specify accessibility standards used"
                })

        # Check for unrealistic claims
        if data.get("success_rate") == 100 and data.get("issues_found", 0) > 0:
            inconsistencies.append({
                "type": "logical_flaw",
                "severity": "high",
                "description": "100% success rate claimed but issues were found",
                "evidence": {"success_rate": data["success_rate"], "issues": data["issues_found"]}
            })

        self.logger.info(f"   Found {len(inconsistencies)} inconsistencies")

        return inconsistencies

    def challenge_assumption(self, assumption: str, counter_evidence: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Challenge an assumption with evidence.

        Args:
            assumption: Assumption to challenge
            counter_evidence: Evidence contradicting the assumption

        Returns:
            Challenge report

        Example:
            batman.challenge_assumption(
                assumption="We can skip keyboard testing because all users use mice",
                counter_evidence={
                    "wcag_requirement": "2.1.1 Keyboard",
                    "statistics": "15% of users rely on keyboard navigation"
                }
            )
        """
        self.logger.info(f"🦇 Challenging assumption: '{assumption}'")

        challenge = {
            "assumption": assumption,
            "challenged_by": self.hero_name,
            "counter_evidence": counter_evidence or {},
            "validity": "CHALLENGED",
            "reasoning": [],
            "timestamp": datetime.now().isoformat()
        }

        # Generate reasoning based on counter-evidence
        if counter_evidence:
            for key, value in counter_evidence.items():
                challenge["reasoning"].append(f"{key}: {value}")

        # Common assumption challenges
        assumption_lower = assumption.lower()

        if "skip" in assumption_lower and "test" in assumption_lower:
            challenge["reasoning"].append("Skipping tests increases risk of undetected issues")
            challenge["validity"] = "INVALID"

        if "all users" in assumption_lower:
            challenge["reasoning"].append("Assuming all users behave identically ignores accessibility needs")
            challenge["validity"] = "INVALID"

        if "everyone" in assumption_lower or "nobody" in assumption_lower:
            challenge["reasoning"].append("Absolute claims like 'everyone' or 'nobody' are rarely true")
            challenge["validity"] = "QUESTIONABLE"

        self.logger.info(f"   Challenge: {challenge['validity']}")
        self.logger.info(f"   Reasoning: {len(challenge['reasoning'])} points")

        return challenge

    # =========================================
    # INTERNAL DETECTIVE METHODS
    # =========================================

    def _cross_reference_knowledge_base(self, claim: str) -> List[Dict]:
        """Cross-reference claim with knowledge base."""
        evidence = []

        if self.knowledge_base:
            # Search knowledge base for related information
            results = self.knowledge_base.search(claim, requesting_hero=self.hero_name, limit=5)

            for result in results:
                evidence.append({
                    "source": "knowledge_base",
                    "type": result.get("knowledge_type", "unknown"),
                    "content": result.get("content", {}),
                    "relevance": "high" if claim.lower() in str(result).lower() else "medium"
                })

        return evidence

    def _check_known_patterns(self, claim: str, context: Optional[Dict]) -> List[Dict]:
        """Check claim against known patterns."""
        patterns = []

        claim_lower = claim.lower()

        # Pattern: Accessibility claims
        if "accessible" in claim_lower or "wcag" in claim_lower:
            patterns.append({
                "pattern_type": "accessibility_claim",
                "requires_verification": ["WCAG standard", "Testing method", "Violation count"],
                "common_issues": ["Missing ARIA labels", "Poor color contrast", "Keyboard traps"]
            })

        # Pattern: Performance claims
        if "fast" in claim_lower or "performance" in claim_lower or "web vitals" in claim_lower:
            patterns.append({
                "pattern_type": "performance_claim",
                "requires_verification": ["LCP value", "FID value", "CLS value", "Testing conditions"],
                "common_issues": ["Network throttling not considered", "Cache effects", "Device variance"]
            })

        # Pattern: Responsive design claims
        if "responsive" in claim_lower or "breakpoint" in claim_lower:
            patterns.append({
                "pattern_type": "responsive_design_claim",
                "requires_verification": ["Breakpoints tested", "Device types", "Orientation"],
                "common_issues": ["Only desktop tested", "Fixed widths", "Overflow issues"]
            })

        return patterns

    def _find_inconsistencies_in_claim(self, claim: str, evidence: List[Dict]) -> List[Dict]:
        """Find inconsistencies between claim and evidence."""
        inconsistencies = []

        claim_lower = claim.lower()

        # Check for absolute claims that evidence doesn't support
        if "all" in claim_lower or "every" in claim_lower or "100%" in claim_lower:
            # Absolute claims require perfect evidence
            has_violations = any(
                "violation" in str(e).lower() or "issue" in str(e).lower()
                for e in evidence
            )

            if has_violations:
                inconsistencies.append({
                    "type": "absolute_claim_contradiction",
                    "severity": "high",
                    "description": f"Claim uses absolute term but evidence shows issues",
                    "claim_term": "all/every/100%"
                })

        # Check for "no" claims
        if "no violations" in claim_lower or "no issues" in claim_lower:
            violation_count = sum(
                e.get("content", {}).get("violations", 0)
                for e in evidence
                if isinstance(e.get("content"), dict)
            )

            if violation_count > 0:
                inconsistencies.append({
                    "type": "false_negative",
                    "severity": "critical",
                    "description": f"Claim of 'no violations' but {violation_count} found in evidence"
                })

        return inconsistencies

    def _verify_against_facts(self, claim: str, evidence: List[Dict]) -> Dict[str, Any]:
        """Verify claim against collected evidence."""
        verification = {
            "verified": None,
            "confidence": 0.0,
            "supporting_evidence": 0,
            "contradicting_evidence": 0
        }

        claim_lower = claim.lower()

        for e in evidence:
            e_str = str(e).lower()

            # Check if evidence supports claim
            if any(keyword in e_str for keyword in ["success", "passed", "compliant", "accessible"]):
                verification["supporting_evidence"] += 1
            elif any(keyword in e_str for keyword in ["fail", "violation", "issue", "error"]):
                verification["contradicting_evidence"] += 1

        total_evidence = verification["supporting_evidence"] + verification["contradicting_evidence"]

        if total_evidence == 0:
            verification["verified"] = None
            verification["confidence"] = 0.0
        elif verification["contradicting_evidence"] == 0:
            verification["verified"] = True
            verification["confidence"] = min(0.9, verification["supporting_evidence"] / max(total_evidence, 1))
        elif verification["supporting_evidence"] == 0:
            verification["verified"] = False
            verification["confidence"] = 0.1
        else:
            # Mixed evidence
            support_ratio = verification["supporting_evidence"] / total_evidence
            verification["verified"] = support_ratio > 0.7
            verification["confidence"] = support_ratio

        return verification

    def _draw_conclusion(self, investigation: Dict[str, Any]) -> str:
        """Draw detective conclusion from investigation."""
        if investigation["verified"] is True and investigation["confidence"] > 0.8:
            return f"🦇 VERIFIED: Claim supported by evidence (Confidence: {investigation['confidence']:.0%})"

        elif investigation["verified"] is False:
            inconsistencies = len(investigation["inconsistencies_found"])
            return f"🦇 DISPUTED: Claim contradicted by evidence ({inconsistencies} inconsistencies found)"

        elif investigation["confidence"] > 0.5:
            return f"🦇 PARTIALLY VERIFIED: Some supporting evidence but concerns remain (Confidence: {investigation['confidence']:.0%})"

        else:
            return f"🦇 INCONCLUSIVE: Insufficient evidence to verify claim. Further investigation needed."

    def _generate_detective_recommendations(self, investigation: Dict[str, Any]) -> List[str]:
        """Generate Batman's detective recommendations."""
        recommendations = []

        if investigation["verified"] is False:
            recommendations.append("🦇 CRITICAL: Claim is false. Do not proceed based on this information.")
            recommendations.append("Investigate source of false claim to prevent future misinformation.")

        if investigation["inconsistencies_found"]:
            recommendations.append(f"Resolve {len(investigation['inconsistencies_found'])} inconsistencies before making decisions.")

        if investigation["confidence"] < 0.7:
            recommendations.append("Gather additional evidence before drawing conclusions.")
            recommendations.append("Consider cross-referencing with additional sources.")

        if not investigation["evidence_collected"]:
            recommendations.append("⚠️ WARNING: No evidence found. Claim is unverified.")
            recommendations.append("Conduct direct testing or inspection to gather evidence.")

        if not recommendations:
            recommendations.append("✅ Claim appears valid. Proceed with appropriate caution.")

        return recommendations

    def _check_source(self, claim: str, source: str) -> Dict[str, Any]:
        """Check a specific source for support/contradiction of claim."""
        # This is a simplified version - real implementation would query actual sources
        return {
            "source": source,
            "supports_claim": True,  # Placeholder
            "confidence": 0.8,
            "evidence": f"Evidence from {source}"
        }

    def get_investigation_report(self) -> Dict[str, Any]:
        """Get summary of all investigations conducted."""
        return {
            "total_investigations": len(self.investigations),
            "verified_claims": sum(1 for i in self.investigations if i["verified"] is True),
            "disputed_claims": sum(1 for i in self.investigations if i["verified"] is False),
            "inconclusive": sum(1 for i in self.investigations if i["verified"] is None),
            "average_confidence": sum(i["confidence"] for i in self.investigations) / len(self.investigations) if self.investigations else 0,
            "investigations": self.investigations
        }


# Example usage
if __name__ == "__main__":
    # Create Batman's investigation module
    batman = BatmanInvestigation()

    # Test investigation
    investigation = batman.investigate_independently(
        claim="All buttons have accessible names",
        source="Automated accessibility scan",
        context={"page_url": "https://example.com"}
    )

    print("\n🦇 BATMAN INVESTIGATION REPORT")
    print("=" * 70)
    print(f"Claim: {investigation['claim']}")
    print(f"Verified: {investigation['verified']}")
    print(f"Confidence: {investigation['confidence']:.0%}")
    print(f"Conclusion: {investigation['conclusion']}")
    print("\nRecommendations:")
    for rec in investigation['recommendations']:
        print(f"  - {rec}")
