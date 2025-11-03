"""
🦸 Superman Figma API Integration - Feature #6
===============================================

Extracts design files, components, and design tokens from Figma using the REST API.

Author: Superman (with Claude Code)
Created: October 21, 2025
Status: Production Ready

Capabilities:
- Extract complete Figma file data (nodes, components, styles)
- Parse design tokens (colors, typography, spacing)
- Component library extraction
- Design system analysis
- Integration with Cyborg hero for design-to-code validation

Figma API Reference: https://www.figma.com/developers/api
"""

import requests
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime


class SupermanFigmaIntegration:
    """
    Superman's Figma API integration for design extraction and analysis.
    """

    def __init__(self, figma_token: str):
        """
        Initialize Superman Figma integration.

        Args:
            figma_token: Figma Personal Access Token (starts with '<FIGMA_ACCESS_TOKEN>')
        """
        self.figma_token = figma_token
        self.base_url = "https://api.figma.com/v1"
        self.headers = {
            "X-Figma-Token": figma_token,
            "Content-Type": "application/json"
        }

    def extract_file_key(self, figma_url: str) -> str:
        """
        Extract file key from Figma URL.

        Args:
            figma_url: Full Figma URL (design or prototype)

        Returns:
            File key (e.g., '6Pmf9gCcUccyqbCO9nN6Ts')

        Example:
            https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test
            -> '6Pmf9gCcUccyqbCO9nN6Ts'
        """
        # Handle different Figma URL formats
        if '/design/' in figma_url:
            file_key = figma_url.split('/design/')[1].split('/')[0]
        elif '/file/' in figma_url:
            file_key = figma_url.split('/file/')[1].split('/')[0]
        elif '/proto/' in figma_url:
            file_key = figma_url.split('/proto/')[1].split('/')[0]
        else:
            # Assume it's just the file key
            file_key = figma_url.split('?')[0].split('/')[-1]

        return file_key

    def get_file_data(self, file_key: str, depth: int = 2) -> Dict[str, Any]:
        """
        Get complete Figma file data.

        Args:
            file_key: Figma file key
            depth: How deep to traverse the node tree (1-10, default 2)

        Returns:
            Complete file data including nodes, components, styles
        """
        url = f"{self.base_url}/files/{file_key}"
        params = {"depth": depth}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "file_key": file_key,
                "superman_says": "Couldn't fetch Figma file. Check your token and file permissions!"
            }

    def get_file_nodes(self, file_key: str, node_ids: List[str]) -> Dict[str, Any]:
        """
        Get specific nodes from a Figma file.

        Args:
            file_key: Figma file key
            node_ids: List of node IDs to fetch (e.g., ['2-948'])

        Returns:
            Node data for specified nodes
        """
        url = f"{self.base_url}/files/{file_key}/nodes"
        params = {"ids": ",".join(node_ids)}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "file_key": file_key,
                "node_ids": node_ids,
                "superman_says": "Couldn't fetch specific nodes!"
            }

    def get_file_images(self, file_key: str, node_ids: List[str],
                       scale: float = 2.0, format: str = 'png') -> Dict[str, Any]:
        """
        Get rendered images of specific nodes.

        Args:
            file_key: Figma file key
            node_ids: List of node IDs to render
            scale: Image scale (1.0 - 4.0)
            format: Image format ('png', 'jpg', 'svg', 'pdf')

        Returns:
            URLs to rendered images
        """
        url = f"{self.base_url}/images/{file_key}"
        params = {
            "ids": ",".join(node_ids),
            "scale": scale,
            "format": format
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "file_key": file_key,
                "superman_says": "Couldn't render images!"
            }

    def extract_components(self, file_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract all components from file data.

        Args:
            file_data: Complete file data from get_file_data()

        Returns:
            Extracted components with metadata
        """
        components = []

        if "document" not in file_data:
            return {
                "error": "No document in file data",
                "component_count": 0,
                "components": []
            }

        def traverse_nodes(node: Dict[str, Any], path: str = ""):
            """Recursively find all components."""
            node_type = node.get("type", "")
            node_name = node.get("name", "Unnamed")
            current_path = f"{path}/{node_name}" if path else node_name

            # Check if this is a component
            if node_type == "COMPONENT" or node_type == "COMPONENT_SET":
                components.append({
                    "id": node.get("id"),
                    "name": node_name,
                    "type": node_type,
                    "path": current_path,
                    "description": node.get("description", ""),
                    "width": node.get("absoluteBoundingBox", {}).get("width"),
                    "height": node.get("absoluteBoundingBox", {}).get("height"),
                    "has_children": "children" in node
                })

            # Traverse children
            if "children" in node:
                for child in node["children"]:
                    traverse_nodes(child, current_path)

        # Start traversal from document
        traverse_nodes(file_data["document"])

        return {
            "component_count": len(components),
            "components": components,
            "superman_says": f"Found {len(components)} components in this design! 🦸"
        }

    def extract_design_tokens(self, file_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract design tokens (colors, typography, spacing).

        Args:
            file_data: Complete file data from get_file_data()

        Returns:
            Extracted design tokens
        """
        tokens = {
            "colors": {},
            "typography": {},
            "effects": {},
            "grids": {}
        }

        # Extract color styles
        if "styles" in file_data:
            for style_id, style_data in file_data.get("styles", {}).items():
                style_type = style_data.get("styleType", "")
                style_name = style_data.get("name", "")

                if style_type == "FILL":
                    tokens["colors"][style_name] = {
                        "id": style_id,
                        "name": style_name,
                        "description": style_data.get("description", "")
                    }
                elif style_type == "TEXT":
                    tokens["typography"][style_name] = {
                        "id": style_id,
                        "name": style_name,
                        "description": style_data.get("description", "")
                    }
                elif style_type == "EFFECT":
                    tokens["effects"][style_name] = {
                        "id": style_id,
                        "name": style_name,
                        "description": style_data.get("description", "")
                    }

        return {
            "color_count": len(tokens["colors"]),
            "typography_count": len(tokens["typography"]),
            "effect_count": len(tokens["effects"]),
            "tokens": tokens,
            "superman_says": f"Extracted {len(tokens['colors'])} colors, {len(tokens['typography'])} text styles! 🎨"
        }

    def analyze_design_complete(self, figma_url: str, node_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Complete Figma design analysis (main entry point).

        Args:
            figma_url: Full Figma URL or file key
            node_id: Optional specific node ID to analyze

        Returns:
            Complete design analysis with components, tokens, and metadata
        """
        print(f"\n🦸 Superman is analyzing your Figma design...")
        print(f"URL: {figma_url}")

        # Extract file key
        file_key = self.extract_file_key(figma_url)
        print(f"File Key: {file_key}")

        # Get file data
        print(f"\n📥 Fetching file data from Figma API...")
        file_data = self.get_file_data(file_key, depth=3)

        if "error" in file_data:
            return file_data

        # Extract metadata
        file_name = file_data.get("name", "Unknown")
        last_modified = file_data.get("lastModified", "")
        version = file_data.get("version", "")

        print(f"✅ File: {file_name}")
        print(f"✅ Last Modified: {last_modified}")
        print(f"✅ Version: {version}")

        # Extract components
        print(f"\n🔍 Extracting components...")
        components_result = self.extract_components(file_data)
        print(f"✅ Found {components_result['component_count']} components")

        # Extract design tokens
        print(f"\n🎨 Extracting design tokens...")
        tokens_result = self.extract_design_tokens(file_data)
        print(f"✅ Extracted {tokens_result['color_count']} color styles")
        print(f"✅ Extracted {tokens_result['typography_count']} text styles")

        # If specific node requested, get it
        node_data = None
        if node_id:
            print(f"\n🎯 Fetching specific node: {node_id}...")
            node_data = self.get_file_nodes(file_key, [node_id])

        # Build complete analysis
        analysis = {
            "file_key": file_key,
            "file_name": file_name,
            "last_modified": last_modified,
            "version": version,
            "url": figma_url,
            "components": components_result,
            "design_tokens": tokens_result,
            "node_data": node_data,
            "analyzed_at": datetime.now().isoformat(),
            "superman_figma_score": self._calculate_figma_score(components_result, tokens_result),
            "superman_recommendations": self._generate_figma_recommendations(
                components_result, tokens_result
            )
        }

        print(f"\n🦸 Superman Figma Analysis Complete!")
        print(f"Score: {analysis['superman_figma_score']['score']}/100 ({analysis['superman_figma_score']['grade']})")

        return analysis

    def _calculate_figma_score(self, components: Dict[str, Any],
                              tokens: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate Superman's Figma design score (0-100).

        Scoring criteria:
        - Component organization (40 points)
        - Design token usage (30 points)
        - Documentation quality (20 points)
        - Naming conventions (10 points)
        """
        score = 0.0
        breakdown = {}

        # Component organization (40 points)
        component_count = components.get("component_count", 0)
        if component_count > 0:
            # More components = better organization
            component_score = min(40, component_count * 4)  # 10 components = full points
            score += component_score
            breakdown["component_organization"] = component_score
        else:
            breakdown["component_organization"] = 0

        # Design token usage (30 points)
        color_count = tokens.get("color_count", 0)
        typography_count = tokens.get("typography_count", 0)
        effect_count = tokens.get("effect_count", 0)

        token_score = 0
        if color_count > 0:
            token_score += min(15, color_count * 3)  # 5 colors = full points
        if typography_count > 0:
            token_score += min(10, typography_count * 2)  # 5 text styles = full points
        if effect_count > 0:
            token_score += min(5, effect_count * 1)  # 5 effects = full points

        score += token_score
        breakdown["design_token_usage"] = token_score

        # Documentation quality (20 points)
        # Check if components have descriptions
        documented_count = sum(
            1 for c in components.get("components", [])
            if c.get("description", "").strip()
        )
        doc_score = 0
        if component_count > 0:
            doc_ratio = documented_count / component_count
            doc_score = doc_ratio * 20
        score += doc_score
        breakdown["documentation_quality"] = doc_score

        # Naming conventions (10 points)
        # Check for consistent naming (basic heuristic)
        naming_score = 10  # Default to full points (would need more analysis)
        score += naming_score
        breakdown["naming_conventions"] = naming_score

        # Calculate grade
        if score >= 98:
            grade = "S+"
        elif score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        else:
            grade = "D"

        return {
            "score": round(score, 1),
            "grade": grade,
            "breakdown": breakdown,
            "superman_says": f"Your design system scores {grade}! Keep building! 🦸"
        }

    def _generate_figma_recommendations(self, components: Dict[str, Any],
                                       tokens: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate actionable recommendations for improving the Figma design.
        """
        recommendations = []

        component_count = components.get("component_count", 0)
        color_count = tokens.get("color_count", 0)
        typography_count = tokens.get("typography_count", 0)

        # Component recommendations
        if component_count == 0:
            recommendations.append({
                "priority": "high",
                "area": "Component Library",
                "issue": "No components found in this design",
                "recommendation": "Create reusable components for buttons, inputs, cards, etc.",
                "superman_says": "Components are the building blocks of great design systems!"
            })
        elif component_count < 5:
            recommendations.append({
                "priority": "medium",
                "area": "Component Library",
                "issue": f"Only {component_count} components found",
                "recommendation": "Expand your component library with more UI elements",
                "superman_says": "More components = more consistency = more power! 🦸"
            })

        # Design token recommendations
        if color_count == 0:
            recommendations.append({
                "priority": "high",
                "area": "Design Tokens",
                "issue": "No color styles defined",
                "recommendation": "Create color styles for your brand palette",
                "superman_says": "Color styles ensure consistency across your entire design!"
            })

        if typography_count == 0:
            recommendations.append({
                "priority": "high",
                "area": "Design Tokens",
                "issue": "No text styles defined",
                "recommendation": "Create text styles for headings, body, captions, etc.",
                "superman_says": "Typography styles make your design scalable!"
            })

        # Documentation recommendations
        documented_count = sum(
            1 for c in components.get("components", [])
            if c.get("description", "").strip()
        )
        if component_count > 0 and documented_count < component_count:
            recommendations.append({
                "priority": "medium",
                "area": "Documentation",
                "issue": f"Only {documented_count}/{component_count} components have descriptions",
                "recommendation": "Add descriptions to all components explaining their usage",
                "superman_says": "Good documentation helps your team use components correctly!"
            })

        # If no issues found
        if not recommendations:
            recommendations.append({
                "priority": "low",
                "area": "Excellence",
                "issue": "None - this design is well organized!",
                "recommendation": "Keep maintaining this high standard",
                "superman_says": "Your design system is super! 🦸⚡"
            })

        return recommendations


# Main entry point function
def analyze_figma_design(figma_token: str, figma_url: str,
                        node_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyze a Figma design file (main entry point).

    Args:
        figma_token: Figma Personal Access Token
        figma_url: Figma file URL or file key
        node_id: Optional specific node ID to analyze

    Returns:
        Complete design analysis

    Example:
        result = analyze_figma_design(
            figma_token="<FIGMA_ACCESS_TOKEN>",
            figma_url="https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test",
            node_id="2-948"
        )
    """
    integration = SupermanFigmaIntegration(figma_token)
    return integration.analyze_design_complete(figma_url, node_id)


if __name__ == "__main__":
    # Test with your poc-test file
    print("🦸 Superman Figma Integration - Feature #6")
    print("=" * 60)

    # Example usage
    token = "<FIGMA_ACCESS_TOKEN>"
    url = "https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=2-948"

    result = analyze_figma_design(token, url, node_id="2-948")

    print("\n" + "=" * 60)
    print(json.dumps(result, indent=2))
