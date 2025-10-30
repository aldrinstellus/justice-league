"""
🎯 SATISFACTION ANALYZER - Oracle's User Happiness Inference Engine

Infers user satisfaction from context clues without interrupting the workflow.

Part of Oracle v2.0 Auto-Learning System - analyzes multiple signals to determine
if the user is happy with Justice League operations.

"The best feedback is what users don't say - it's what they do." - Oracle
"""

from typing import Dict, List, Any
from datetime import datetime


class SatisfactionAnalyzer:
    """
    🎯 SATISFACTION ANALYZER

    Infers user satisfaction from context signals without explicit feedback.

    Analyzes multiple signals:
    - Mission success/failure
    - Accuracy scores
    - Error frequency and severity
    - Completion time
    - Retry attempts
    - Follow-up question sentiment

    Returns satisfaction score (0-1), confidence level, and assessment.
    """

    # Negative keywords indicating dissatisfaction
    NEGATIVE_KEYWORDS = [
        'why', 'wrong', 'failed', 'error', 'issue', 'problem',
        'broken', 'not working', 'doesn\'t work', 'can\'t', 'cannot',
        'fix', 'help', 'stuck', 'confused', 'bad', 'poor'
    ]

    # Positive keywords indicating satisfaction
    POSITIVE_KEYWORDS = [
        'perfect', 'excellent', 'great', 'good', 'nice', 'love',
        'awesome', 'amazing', 'works', 'thank', 'thanks'
    ]

    @staticmethod
    def analyze_satisfaction(session: Any) -> Dict[str, Any]:
        """
        Infer user satisfaction from learning session context

        Args:
            session: LearningSession instance with complete interaction data

        Returns:
            {
                'score': 0.0-1.0,  # Overall satisfaction score
                'confidence': 0.0-1.0,  # Confidence in assessment
                'assessment': 'happy' | 'neutral' | 'unhappy',
                'signals': List[str]  # Evidence for the assessment
            }

        Example:
            >>> analysis = SatisfactionAnalyzer.analyze_satisfaction(session)
            >>> analysis['score']  # 0.85
            >>> analysis['assessment']  # 'happy'
            >>> analysis['signals']  # ['Mission completed successfully', 'High accuracy (94%)', ...]
        """
        signals = []
        score = 0.5  # Neutral baseline
        confidence_factors = []

        # Signal 1: Mission Success (Weight: High)
        success = session.results.get('success', False)
        if success:
            score += 0.25
            signals.append("✅ Mission completed successfully")
            confidence_factors.append(0.9)
        else:
            score -= 0.30
            signals.append("❌ Mission failed")
            confidence_factors.append(0.95)  # Failure is a strong signal

        # Signal 2: Accuracy/Quality Score (Weight: High)
        accuracy = SatisfactionAnalyzer._extract_accuracy(session)
        if accuracy is not None:
            if accuracy >= 90:
                score += 0.20
                signals.append(f"✅ High accuracy achieved ({accuracy}%)")
                confidence_factors.append(0.85)
            elif accuracy >= 75:
                score += 0.10
                signals.append(f"⚠️ Acceptable accuracy ({accuracy}%)")
                confidence_factors.append(0.70)
            elif accuracy < 70:
                score -= 0.20
                signals.append(f"❌ Low accuracy ({accuracy}%)")
                confidence_factors.append(0.80)

        # Signal 3: Error Frequency (Weight: High)
        error_count = len(session.errors_encountered)
        if error_count == 0:
            score += 0.15
            signals.append("✅ No errors encountered")
            confidence_factors.append(0.75)
        elif error_count <= 2:
            score -= 0.10
            signals.append(f"⚠️ Few errors ({error_count})")
            confidence_factors.append(0.65)
        else:
            score -= 0.25
            signals.append(f"❌ Multiple errors ({error_count})")
            confidence_factors.append(0.85)

        # Signal 4: Completion Time (Weight: Medium)
        duration = session.get_duration_seconds()
        if duration < 120:  # Under 2 minutes
            score += 0.10
            signals.append("✅ Quick completion")
            confidence_factors.append(0.60)
        elif duration > 600:  # Over 10 minutes
            score -= 0.05
            signals.append("⏱️ Long duration")
            confidence_factors.append(0.50)

        # Signal 5: Retry Attempts (Weight: Medium)
        if session.retry_count == 0:
            score += 0.10
            signals.append("✅ No retries needed")
            confidence_factors.append(0.70)
        elif session.retry_count > 2:
            score -= 0.20
            signals.append(f"❌ Multiple retries ({session.retry_count})")
            confidence_factors.append(0.80)

        # Signal 6: Follow-up Question Sentiment (Weight: Medium)
        if session.follow_up_questions:
            sentiment = SatisfactionAnalyzer._analyze_question_sentiment(
                session.follow_up_questions
            )
            if sentiment == 'negative':
                score -= 0.15
                signals.append("❌ Negative follow-up questions")
                confidence_factors.append(0.75)
            elif sentiment == 'positive':
                score += 0.10
                signals.append("✅ Positive follow-up sentiment")
                confidence_factors.append(0.70)

        # Signal 7: Operation Success Rate (Weight: Medium)
        if session.hero_operations:
            success_rate = sum(
                1 for op in session.hero_operations if op.get('success', False)
            ) / len(session.hero_operations)

            if success_rate >= 0.9:
                score += 0.10
                signals.append(f"✅ High operation success rate ({success_rate*100:.0f}%)")
                confidence_factors.append(0.70)
            elif success_rate < 0.5:
                score -= 0.15
                signals.append(f"❌ Low operation success rate ({success_rate*100:.0f}%)")
                confidence_factors.append(0.75)

        # Normalize score to 0-1 range
        score = max(0.0, min(1.0, score))

        # Calculate confidence (average of all confidence factors)
        confidence = sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.5

        # Determine assessment
        if score >= 0.70:
            assessment = 'happy'
        elif score >= 0.40:
            assessment = 'neutral'
        else:
            assessment = 'unhappy'

        return {
            'score': score,
            'confidence': confidence,
            'assessment': assessment,
            'signals': signals
        }

    @staticmethod
    def _extract_accuracy(session: Any) -> float:
        """Extract accuracy/quality score from session results"""
        # Check direct accuracy score
        if 'accuracy_score' in session.results:
            return session.results['accuracy_score']

        # Check overall score
        if 'overall_score' in session.results:
            return session.results['overall_score']

        # Check justice league score
        if 'justice_league_score' in session.results:
            jl_score = session.results['justice_league_score']
            if isinstance(jl_score, dict) and 'overall_score' in jl_score:
                return jl_score['overall_score']

        # Calculate average from hero operations
        if session.hero_operations:
            scores = []
            for op in session.hero_operations:
                result = op.get('result', {})
                if 'score' in result:
                    scores.append(result['score'])
                elif 'accuracy_score' in result:
                    scores.append(result['accuracy_score'])

            if scores:
                return sum(scores) / len(scores)

        return None

    @staticmethod
    def _analyze_question_sentiment(questions: List[str]) -> str:
        """
        Analyze sentiment of follow-up questions

        Returns:
            'negative' | 'neutral' | 'positive'
        """
        if not questions:
            return 'neutral'

        negative_count = 0
        positive_count = 0

        for question in questions:
            question_lower = question.lower()

            # Check for negative keywords
            if any(keyword in question_lower for keyword in SatisfactionAnalyzer.NEGATIVE_KEYWORDS):
                negative_count += 1

            # Check for positive keywords
            if any(keyword in question_lower for keyword in SatisfactionAnalyzer.POSITIVE_KEYWORDS):
                positive_count += 1

        # Determine overall sentiment
        if negative_count > positive_count:
            return 'negative'
        elif positive_count > negative_count:
            return 'positive'
        else:
            return 'neutral'

    @staticmethod
    def should_ask_question(satisfaction_analysis: Dict[str, Any]) -> bool:
        """
        Determine if Oracle should ask the user for explicit feedback

        Only asks when confidence is low (< 60%) or when satisfaction is ambiguous

        Args:
            satisfaction_analysis: Result from analyze_satisfaction()

        Returns:
            True if Oracle should ask, False otherwise
        """
        confidence = satisfaction_analysis.get('confidence', 0)
        score = satisfaction_analysis.get('score', 0.5)

        # Low confidence - unclear if user is happy
        if confidence < 0.60:
            return True

        # Ambiguous satisfaction (near neutral boundary)
        if 0.35 <= score <= 0.55:
            return True

        return False

    @staticmethod
    def generate_followup_question(session: Any, satisfaction_analysis: Dict[str, Any]) -> str:
        """
        Generate intelligent follow-up question based on session context

        Args:
            session: LearningSession instance
            satisfaction_analysis: Result from analyze_satisfaction()

        Returns:
            Contextual question string
        """
        score = satisfaction_analysis.get('score', 0.5)
        assessment = satisfaction_analysis.get('assessment', 'neutral')

        # If ambiguous accuracy
        accuracy = SatisfactionAnalyzer._extract_accuracy(session)
        if accuracy and 70 <= accuracy < 80:
            return (
                f"I see we achieved {accuracy:.0f}% accuracy. Were you satisfied with this result, "
                "or were you hoping for higher? This helps me learn what 'success' means for you."
            )

        # If mission succeeded but confidence is low
        if session.results.get('success') and assessment == 'neutral':
            return (
                "The mission completed successfully, but I'm not sure if it met your expectations. "
                "Was this what you were looking for?"
            )

        # If mission failed
        if not session.results.get('success'):
            error_types = set(e.get('error', {}).get('type', 'unknown') for e in session.errors_encountered)
            if len(error_types) == 1:
                error_type = list(error_types)[0]
                return (
                    f"The conversion encountered {error_type} errors. "
                    "Would a different approach (like Image-to-HTML) work better for this case?"
                )
            else:
                return (
                    "The mission didn't work as expected. Was it:\n"
                    "  1. Wrong layout/structure\n"
                    "  2. Missing functionality\n"
                    "  3. Styling issues\n"
                    "  4. Something else?\n"
                    "This helps me prevent similar issues."
                )

        # Generic fallback
        return (
            f"I've completed the {session.mission_type} operation. "
            "Did the result meet your expectations? Your feedback helps me improve."
        )
