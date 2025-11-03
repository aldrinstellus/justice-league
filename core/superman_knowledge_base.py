"""
🦸 SUPERMAN KNOWLEDGE BASE
============================

Persistent knowledge storage and retrieval for Justice League.

Heroes can:
- Store learned patterns
- Share best practices
- Query previous solutions
- Build collective intelligence
- Learn from mission history

Author: Superman (with Claude Code)
Created: October 21, 2025
Status: Production Ready
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class KnowledgeEntry:
    """Represents a single piece of knowledge."""

    def __init__(self, hero: str, knowledge_type: str, content: Dict[str, Any],
                 tags: Optional[List[str]] = None):
        self.hero = hero
        self.knowledge_type = knowledge_type  # best_practice, pattern, solution, learning, etc.
        self.content = content
        self.tags = tags or []
        self.timestamp = datetime.now().isoformat()
        self.entry_id = f"{hero}_{knowledge_type}_{datetime.now().timestamp()}"
        self.usefulness_score = 0  # Incremented when knowledge is used
        self.times_accessed = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "hero": self.hero,
            "knowledge_type": self.knowledge_type,
            "content": self.content,
            "tags": self.tags,
            "timestamp": self.timestamp,
            "usefulness_score": self.usefulness_score,
            "times_accessed": self.times_accessed
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KnowledgeEntry':
        entry = cls(
            hero=data["hero"],
            knowledge_type=data["knowledge_type"],
            content=data["content"],
            tags=data.get("tags", [])
        )
        entry.entry_id = data["entry_id"]
        entry.timestamp = data["timestamp"]
        entry.usefulness_score = data.get("usefulness_score", 0)
        entry.times_accessed = data.get("times_accessed", 0)
        return entry


class JusticeLeagueKnowledgeBase:
    """
    Central knowledge repository for Justice League.

    Stores and retrieves knowledge from all hero missions,
    enabling collective learning and continuous improvement.
    """

    def __init__(self, storage_dir: Optional[str] = None):
        """
        Initialize knowledge base.

        Args:
            storage_dir: Directory to store knowledge
        """
        self.storage_dir = Path(storage_dir or '/tmp/aldo-vision-knowledge-base')
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.knowledge_file = self.storage_dir / "justice_league_knowledge.json"
        self.knowledge: List[KnowledgeEntry] = []

        # Indices for fast lookup
        self.by_hero: Dict[str, List[KnowledgeEntry]] = defaultdict(list)
        self.by_type: Dict[str, List[KnowledgeEntry]] = defaultdict(list)
        self.by_tag: Dict[str, List[KnowledgeEntry]] = defaultdict(list)

        self.logger = logging.getLogger("SupermanKnowledgeBase")

        # Load existing knowledge
        self._load()
        self.logger.info(f"🦸 Knowledge Base initialized with {len(self.knowledge)} entries")

    def add_knowledge(self, hero: str, knowledge_type: str, content: Dict[str, Any],
                     tags: Optional[List[str]] = None):
        """
        Add new knowledge to the base.

        Args:
            hero: Contributing hero
            knowledge_type: Type of knowledge
            content: Knowledge content
            tags: Optional tags for categorization

        Example:
            kb.add_knowledge(
                hero="Batman",
                knowledge_type="best_practice",
                content={
                    "practice": "Wait for dynamic elements before testing",
                    "reason": "Prevents flaky tests",
                    "applies_to": ["button_testing", "form_testing"]
                },
                tags=["testing", "reliability", "dynamic_content"]
            )
        """
        entry = KnowledgeEntry(hero, knowledge_type, content, tags)
        self.knowledge.append(entry)

        # Update indices
        self.by_hero[hero].append(entry)
        self.by_type[knowledge_type].append(entry)
        for tag in entry.tags:
            self.by_tag[tag].append(entry)

        # Save to disk
        self._save()

        self.logger.info(f"📚 Added {knowledge_type} from {hero} (ID: {entry.entry_id})")

    def search(self, query: str, requesting_hero: Optional[str] = None,
              knowledge_type: Optional[str] = None,
              tags: Optional[List[str]] = None,
              limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search knowledge base.

        Args:
            query: Search query
            requesting_hero: Hero making the request
            knowledge_type: Filter by type
            tags: Filter by tags
            limit: Max results

        Returns:
            List of relevant knowledge entries
        """
        results = []

        # Filter by type if specified
        if knowledge_type:
            candidates = self.by_type.get(knowledge_type, [])
        else:
            candidates = self.knowledge

        # Filter by tags if specified
        if tags:
            tagged_entries = set()
            for tag in tags:
                tagged_entries.update(self.by_tag.get(tag, []))
            candidates = [e for e in candidates if e in tagged_entries]

        # Search in content
        query_lower = query.lower()
        for entry in candidates:
            content_str = json.dumps(entry.content).lower()
            if query_lower in content_str or query_lower in " ".join(entry.tags):
                # Increment access counter
                entry.times_accessed += 1
                results.append(entry.to_dict())

        # Sort by usefulness score and recent access
        results.sort(key=lambda x: (x['usefulness_score'], x['times_accessed']), reverse=True)

        self.logger.info(f"🔍 Search '{query}' returned {len(results[:limit])} results (requested by {requesting_hero})")

        # Save updated access counts
        self._save()

        return results[:limit]

    def mark_useful(self, entry_id: str, usefulness_increase: int = 1):
        """
        Mark knowledge as useful (upvote).

        Args:
            entry_id: Knowledge entry ID
            usefulness_increase: How much to increase score
        """
        for entry in self.knowledge:
            if entry.entry_id == entry_id:
                entry.usefulness_score += usefulness_increase
                self._save()
                self.logger.info(f"⭐ Knowledge {entry_id} marked as useful (+{usefulness_increase})")
                return

    def get_by_hero(self, hero: str) -> List[Dict[str, Any]]:
        """Get all knowledge contributed by a hero."""
        entries = self.by_hero.get(hero, [])
        return [e.to_dict() for e in entries]

    def get_by_type(self, knowledge_type: str) -> List[Dict[str, Any]]:
        """Get all knowledge of a specific type."""
        entries = self.by_type.get(knowledge_type, [])
        return [e.to_dict() for e in entries]

    def get_top_knowledge(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most useful knowledge."""
        sorted_knowledge = sorted(self.knowledge,
                                 key=lambda e: e.usefulness_score,
                                 reverse=True)
        return [e.to_dict() for e in sorted_knowledge[:limit]]

    def get_recent_knowledge(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recent knowledge."""
        sorted_knowledge = sorted(self.knowledge,
                                 key=lambda e: e.timestamp,
                                 reverse=True)
        return [e.to_dict() for e in sorted_knowledge[:limit]]

    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        return {
            "total_entries": len(self.knowledge),
            "by_hero": {hero: len(entries) for hero, entries in self.by_hero.items()},
            "by_type": {ktype: len(entries) for ktype, entries in self.by_type.items()},
            "total_tags": len(self.by_tag),
            "most_accessed": self.get_top_knowledge(5),
            "recent_entries": self.get_recent_knowledge(5)
        }

    def generate_report(self) -> str:
        """Generate knowledge base report."""
        stats = self.get_stats()

        report = []
        report.append("🦸 JUSTICE LEAGUE KNOWLEDGE BASE REPORT")
        report.append("=" * 70)
        report.append(f"Total Knowledge Entries: {stats['total_entries']}")

        report.append("\n📊 Knowledge by Hero:")
        for hero, count in stats['by_hero'].items():
            report.append(f"  - {hero}: {count} entries")

        report.append("\n📚 Knowledge by Type:")
        for ktype, count in stats['by_type'].items():
            report.append(f"  - {ktype}: {count} entries")

        report.append(f"\n🏷️  Total Tags: {stats['total_tags']}")

        report.append("\n⭐ Top 5 Most Useful Knowledge:")
        for i, entry in enumerate(stats['most_accessed'], 1):
            report.append(f"{i}. [{entry['knowledge_type']}] from {entry['hero']}")
            report.append(f"   Score: {entry['usefulness_score']}, Accessed: {entry['times_accessed']} times")

        report.append("\n" + "=" * 70)

        return "\n".join(report)

    def _save(self):
        """Save knowledge to disk."""
        data = [e.to_dict() for e in self.knowledge]
        with open(self.knowledge_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _load(self):
        """Load knowledge from disk."""
        if self.knowledge_file.exists():
            with open(self.knowledge_file, 'r') as f:
                data = json.load(f)

            for entry_data in data:
                entry = KnowledgeEntry.from_dict(entry_data)
                self.knowledge.append(entry)

                # Rebuild indices
                self.by_hero[entry.hero].append(entry)
                self.by_type[entry.knowledge_type].append(entry)
                for tag in entry.tags:
                    self.by_tag[tag].append(entry)


# Example usage
if __name__ == "__main__":
    kb = JusticeLeagueKnowledgeBase()

    # Batman adds best practice
    kb.add_knowledge(
        hero="Batman",
        knowledge_type="best_practice",
        content={
            "practice": "Always wait for dynamic content before testing",
            "reason": "Prevents flaky tests and false failures",
            "applies_to": ["button_testing", "form_validation"]
        },
        tags=["testing", "reliability", "dynamic_content"]
    )

    # Wonder Woman adds accessibility pattern
    kb.add_knowledge(
        hero="Wonder Woman",
        knowledge_type="pattern",
        content={
            "issue": "Low contrast ratio",
            "solution": "Check contrast ratio >= 4.5:1 for normal text",
            "wcag_criterion": "1.4.3"
        },
        tags=["accessibility", "wcag", "color_contrast"]
    )

    # Flash adds performance solution
    kb.add_knowledge(
        hero="Flash",
        knowledge_type="solution",
        content={
            "problem": "Slow LCP (>2.5s)",
            "solution": "Optimize images, use CDN, implement lazy loading",
            "expected_improvement": "LCP < 2.5s"
        },
        tags=["performance", "lcp", "core_web_vitals"]
    )

    # Search knowledge
    results = kb.search("testing", requesting_hero="Green Arrow")
    print(f"Found {len(results)} results for 'testing'")

    # Get stats
    print("\n" + kb.generate_report())
