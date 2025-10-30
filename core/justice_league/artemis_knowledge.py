"""
🎨 Artemis Knowledge System - Expert Memory & Learning
=======================================================

The memory core that makes Artemis an expert through continuous learning.

Stores every Figma-to-code conversion with full context, patterns, and lessons learned.
Enables semantic search, pattern recognition, and continuous improvement.

Author: Artemis (Expert Edition)
Created: October 23, 2025
Status: Production Ready
"""

import json
import hashlib
from typing import Dict, Any, List, Optional, Set
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class ArtemisKnowledge:
    """
    🎨 Artemis Knowledge System

    The expert memory system that stores and retrieves conversion learnings.

    Powers:
    - 📚 Conversion Memory: Store every conversion with full context
    - 🔍 Semantic Search: Find similar past conversions
    - 📊 Pattern Library: Build library of proven patterns
    - 🎯 Error Encyclopedia: Track issues and solutions
    - 📈 Success Metrics: Monitor improvement over time
    """

    def __init__(self, knowledge_dir: str = "/Users/admin/Documents/claudecode/Projects/aldo-vision/data"):
        """
        Initialize Artemis Knowledge System.

        Args:
            knowledge_dir: Directory for knowledge base storage
        """
        self.knowledge_dir = Path(knowledge_dir)
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)

        self.knowledge_file = self.knowledge_dir / "artemis_knowledge_base.json"
        self.patterns_file = self.knowledge_dir / "artemis_patterns.json"
        self.component_library_file = self.knowledge_dir / "artemis_component_library.json"
        self.tailwind_knowledge_file = self.knowledge_dir / "artemis_tailwind_knowledge.json"

        # Load existing knowledge
        self.knowledge = self._load_knowledge()
        self.patterns = self._load_patterns()
        self.component_library = self._load_component_library()
        self.tailwind_knowledge = self._load_tailwind_knowledge()

        print(f"🎨 Artemis Knowledge System initialized")
        print(f"   📚 Conversions stored: {len(self.knowledge.get('conversions', []))}")
        print(f"   🎯 Patterns learned: {len(self.patterns)}")
        print(f"   🧩 Component Library: {self.component_library.get('library_name', 'None')}")
        print(f"   🎨 Tailwind Knowledge: Loaded")

    def _load_knowledge(self) -> Dict[str, Any]:
        """Load knowledge base from disk."""
        if self.knowledge_file.exists():
            with open(self.knowledge_file, 'r') as f:
                return json.load(f)
        return {
            "conversions": [],
            "expert_insights": {},
            "statistics": {
                "total_conversions": 0,
                "average_accuracy": 0,
                "average_iterations": 0,
                "total_patterns_identified": 0
            }
        }

    def _load_patterns(self) -> Dict[str, Any]:
        """Load pattern library from disk."""
        if self.patterns_file.exists():
            with open(self.patterns_file, 'r') as f:
                return json.load(f)
        return {}

    def _load_component_library(self) -> Dict[str, Any]:
        """Load component library knowledge (shadcn/ui)."""
        if self.component_library_file.exists():
            with open(self.component_library_file, 'r') as f:
                return json.load(f)
        return {"library_name": "Unknown"}

    def _load_tailwind_knowledge(self) -> Dict[str, Any]:
        """Load Tailwind CSS knowledge."""
        if self.tailwind_knowledge_file.exists():
            with open(self.tailwind_knowledge_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_knowledge(self):
        """Save knowledge base to disk."""
        with open(self.knowledge_file, 'w') as f:
            json.dump(self.knowledge, f, indent=2)

    def _save_patterns(self):
        """Save pattern library to disk."""
        with open(self.patterns_file, 'w') as f:
            json.dump(self.patterns, f, indent=2)

    def store_conversion(self, conversion_data: Dict[str, Any]) -> str:
        """
        Store a new conversion in the knowledge base.

        Args:
            conversion_data: Complete conversion data including:
                - figma_url: Figma design URL
                - figma_specs: Extracted specifications (colors, spacing, layout)
                - component_name: Generated component name
                - generated_code: The code generated
                - accuracy_score: Final accuracy percentage
                - iterations: Number of attempts needed
                - issues_solved: List of issues encountered and fixed
                - lessons_learned: Extracted lessons

        Returns:
            Conversion ID
        """
        conversion_id = self._generate_conversion_id(conversion_data)

        conversion_record = {
            "id": conversion_id,
            "timestamp": datetime.now().isoformat(),
            "figma_url": conversion_data.get("figma_url", ""),
            "component_name": conversion_data.get("component_name", ""),
            "specs": conversion_data.get("figma_specs", {}),
            "accuracy_final": conversion_data.get("accuracy_score", 0),
            "iterations": conversion_data.get("iterations", 1),
            "issues_solved": conversion_data.get("issues_solved", []),
            "lessons_learned": conversion_data.get("lessons_learned", {}),
            "reusable_patterns": conversion_data.get("reusable_patterns", []),
            "expert_rating": self._calculate_expert_rating(
                conversion_data.get("accuracy_score", 0),
                conversion_data.get("iterations", 1)
            )
        }

        # Add to knowledge base
        self.knowledge["conversions"].append(conversion_record)

        # Update statistics
        self._update_statistics(conversion_record)

        # Extract and store patterns
        self._extract_patterns(conversion_record)

        # Save to disk
        self._save_knowledge()
        self._save_patterns()

        print(f"🎨 Conversion stored: {conversion_id}")
        print(f"   Expert Rating: {conversion_record['expert_rating']}")
        print(f"   Patterns extracted: {len(conversion_record['reusable_patterns'])}")

        return conversion_id

    def query_similar_conversions(
        self,
        figma_url: Optional[str] = None,
        specs: Optional[Dict[str, Any]] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Query knowledge base for similar past conversions.

        Args:
            figma_url: Figma URL to match (exact or similar)
            specs: Design specs to match (colors, spacing, etc.)
            limit: Maximum number of results

        Returns:
            List of similar conversions with relevance scores
        """
        conversions = self.knowledge.get("conversions", [])

        if not conversions:
            return []

        # Simple similarity scoring (can be enhanced with ML embeddings)
        scored_conversions = []

        for conv in conversions:
            similarity_score = 0

            # URL similarity
            if figma_url and conv.get("figma_url"):
                if figma_url == conv["figma_url"]:
                    similarity_score += 50  # Exact match
                elif figma_url.split("?")[0] == conv["figma_url"].split("?")[0]:
                    similarity_score += 30  # Same file, different node

            # Spec similarity
            if specs and conv.get("specs"):
                # Color similarity
                if "colors" in specs and "colors" in conv["specs"]:
                    common_colors = set(specs["colors"].values()) & set(conv["specs"]["colors"].values())
                    similarity_score += len(common_colors) * 5

                # Spacing similarity
                if "spacing" in specs and "spacing" in conv["specs"]:
                    common_spacing = set(specs["spacing"].values()) & set(conv["specs"]["spacing"].values())
                    similarity_score += len(common_spacing) * 5

                # Layout similarity
                if "layout" in specs and "layout" in conv["specs"]:
                    if specs["layout"].get("max_width") == conv["specs"]["layout"].get("max_width"):
                        similarity_score += 10

            # High accuracy conversions are more valuable
            similarity_score += conv.get("accuracy_final", 0) * 0.2

            if similarity_score > 0:
                scored_conversions.append({
                    "conversion": conv,
                    "relevance_score": similarity_score
                })

        # Sort by relevance and return top results
        scored_conversions.sort(key=lambda x: x["relevance_score"], reverse=True)
        return scored_conversions[:limit]

    def get_pattern(self, pattern_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific pattern from the library.

        Args:
            pattern_name: Name of the pattern

        Returns:
            Pattern data or None
        """
        return self.patterns.get(pattern_name)

    def get_error_solution(self, error_type: str) -> Optional[Dict[str, Any]]:
        """
        Get known solution for a specific error type.

        Args:
            error_type: Type of error (e.g., 'component-style-conflict')

        Returns:
            Solution data or None
        """
        # Search through all conversions for this error type
        for conv in self.knowledge.get("conversions", []):
            for issue in conv.get("issues_solved", []):
                if issue.get("pattern") == error_type or issue.get("problem", "").lower().find(error_type.lower()) != -1:
                    return {
                        "problem": issue.get("problem"),
                        "solution": issue.get("solution"),
                        "confidence": issue.get("confidence", 50),
                        "success_count": 1  # Can be enhanced to track multiple uses
                    }
        return None

    def get_statistics(self) -> Dict[str, Any]:
        """Get current knowledge base statistics."""
        return self.knowledge.get("statistics", {})

    def get_expert_insights(self) -> Dict[str, Any]:
        """Get accumulated expert insights."""
        return self.knowledge.get("expert_insights", {})

    def count_conversions(self) -> int:
        """Get total number of conversions stored."""
        return len(self.knowledge.get("conversions", []))

    def _generate_conversion_id(self, data: Dict[str, Any]) -> str:
        """Generate unique ID for conversion."""
        url = data.get("figma_url", "")
        timestamp = datetime.now().isoformat()
        hash_input = f"{url}_{timestamp}".encode()
        return hashlib.md5(hash_input).hexdigest()[:12]

    def _calculate_expert_rating(self, accuracy: float, iterations: int) -> str:
        """
        Calculate expert rating based on performance.

        Args:
            accuracy: Final accuracy score (0-100)
            iterations: Number of attempts needed

        Returns:
            Expert rating string
        """
        if accuracy >= 100 and iterations == 1:
            return "S+ (Perfect First Try)"
        elif accuracy >= 98 and iterations <= 2:
            return "S (Exceptional)"
        elif accuracy >= 95 and iterations <= 3:
            return "A+ (Excellent)"
        elif accuracy >= 90:
            return "A (Very Good)"
        elif accuracy >= 85:
            return "B+ (Good)"
        elif accuracy >= 80:
            return "B (Acceptable)"
        else:
            return "C (Needs Improvement)"

    def _update_statistics(self, conversion: Dict[str, Any]):
        """Update knowledge base statistics."""
        stats = self.knowledge["statistics"]
        total = stats["total_conversions"]

        # Update averages
        stats["total_conversions"] = total + 1
        stats["average_accuracy"] = (
            (stats["average_accuracy"] * total + conversion["accuracy_final"])
            / (total + 1)
        )
        stats["average_iterations"] = (
            (stats["average_iterations"] * total + conversion["iterations"])
            / (total + 1)
        )

        # Count patterns
        stats["total_patterns_identified"] = len(self.patterns)

    def _extract_patterns(self, conversion: Dict[str, Any]):
        """
        Extract reusable patterns from conversion.

        Args:
            conversion: Conversion record
        """
        # Extract patterns from lessons and specs
        for pattern_name in conversion.get("reusable_patterns", []):
            if pattern_name not in self.patterns:
                self.patterns[pattern_name] = {
                    "name": pattern_name,
                    "usage_count": 1,
                    "success_rate": conversion["accuracy_final"],
                    "first_seen": conversion["timestamp"],
                    "description": f"Pattern identified in {conversion['component_name']}"
                }
            else:
                # Update existing pattern
                pattern = self.patterns[pattern_name]
                pattern["usage_count"] += 1
                pattern["success_rate"] = (
                    (pattern["success_rate"] * (pattern["usage_count"] - 1) + conversion["accuracy_final"])
                    / pattern["usage_count"]
                )
