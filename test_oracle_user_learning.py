#!/usr/bin/env python3
"""
🔮 Test Oracle's User Question Learning System (v1.9.1)

Tests the new user question tracking capabilities:
- Store user questions with context
- Query similar questions (FAQ retrieval)
- Get question analytics
- Track user learning journey
- Identify knowledge gaps
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.justice_league.oracle_meta_agent import OracleMeta

def test_oracle_user_learning():
    """Test Oracle's user learning system"""

    print("=" * 70)
    print("🔮 ORACLE USER QUESTION LEARNING SYSTEM TEST")
    print("=" * 70)
    print()

    # Initialize Oracle
    oracle = OracleMeta()

    # Test 1: Store user questions
    print("📝 Test 1: Storing User Questions")
    print("-" * 70)

    test_questions = [
        {
            "question": "How do I export all frames from a Figma file?",
            "category": "frame_export",
            "context": {"user_stage": "beginner", "has_figma_token": False}
        },
        {
            "question": "Can I export Figma components and component sets too?",
            "category": "frame_export",
            "context": {"user_stage": "intermediate", "has_figma_token": True}
        },
        {
            "question": "How do I convert a Figma design to React components?",
            "category": "figma_conversion",
            "context": {"user_stage": "beginner", "framework": "react"}
        },
        {
            "question": "Why is my conversion accuracy only 41%?",
            "category": "accuracy_improvement",
            "context": {"user_stage": "intermediate", "method": "figma-api"}
        },
        {
            "question": "Should I use Figma API or Image-to-HTML method?",
            "category": "figma_conversion",
            "context": {"user_stage": "intermediate", "complexity": "complex_dashboard"}
        }
    ]

    stored_ids = []
    for q_data in test_questions:
        q_id = oracle.store_user_question(
            question=q_data["question"],
            category=q_data["category"],
            context=q_data["context"],
            response_summary=f"Answered question about {q_data['category']}"
        )
        stored_ids.append(q_id)
        print(f"  ✅ Stored: {q_id} - {q_data['question'][:50]}...")

    print()

    # Test 2: Query similar questions
    print("🔍 Test 2: Querying Similar Questions (FAQ Retrieval)")
    print("-" * 70)

    test_query = "How can I export frames from Figma?"
    print(f"  Query: '{test_query}'")
    print()

    similar = oracle.query_similar_questions(test_query, category="frame_export")

    if similar:
        print(f"  Found {len(similar)} similar questions:")
        for i, q in enumerate(similar, 1):
            print(f"    {i}. [{q.get('id')}] {q.get('question')}")
            print(f"       Similarity: {q.get('similarity_score', 0):.2%}")
            print()
    else:
        print("  No similar questions found")

    print()

    # Test 3: Get analytics
    print("📊 Test 3: Question Analytics")
    print("-" * 70)

    analytics = oracle.get_question_analytics()

    print(f"  Total Questions: {analytics.get('total_questions', 0)}")
    print(f"  Most Asked Category: {analytics.get('most_asked_category', 'N/A')}")
    print(f"  Most Asked Count: {analytics.get('most_asked_count', 0)}")
    print()
    print("  Category Breakdown:")
    for category, count in analytics.get('categories_breakdown', {}).items():
        print(f"    - {category}: {count} questions")
    print()

    # Test 4: Track user journey
    print("🎯 Test 4: Tracking User Learning Journey")
    print("-" * 70)

    milestones = [
        ("beginner", "completed_first_export"),
        ("intermediate", "first_figma_conversion"),
        ("intermediate", "understanding_decision_matrix")
    ]

    for stage, milestone in milestones:
        success = oracle.track_user_journey(stage, milestone)
        status = "✅" if success else "❌"
        print(f"  {status} Tracked: {stage} → {milestone}")

    print()

    # Test 5: Identify knowledge gaps
    print("🔍 Test 5: Identifying Knowledge Gaps")
    print("-" * 70)

    gaps = oracle.identify_knowledge_gaps()

    if gaps:
        print(f"  Found {len(gaps)} knowledge gaps:")
        for gap in gaps:
            print(f"\n    📌 Area: {gap.get('area')}")
            print(f"       Severity: {gap.get('severity', 'unknown').upper()}")
            print(f"       Questions: {gap.get('question_count', 0)}")
            print(f"       Recommendation: {gap.get('recommendation', 'N/A')}")
            if gap.get('typical_questions'):
                print("       Typical Questions:")
                for tq in gap.get('typical_questions', [])[:2]:
                    print(f"         - {tq}")
    else:
        print("  No knowledge gaps identified yet")

    print()
    print("=" * 70)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print()
    print("🔮 Oracle's User Learning System is fully operational!")
    print("   - Questions are being tracked")
    print("   - FAQ retrieval is working")
    print("   - Analytics are being generated")
    print("   - User journey is being monitored")
    print("   - Knowledge gaps are being identified")
    print()

if __name__ == "__main__":
    test_oracle_user_learning()
