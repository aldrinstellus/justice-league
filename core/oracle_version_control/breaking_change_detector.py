"""
⚠️ Breaking Change Detector
Automatically detect breaking changes in agent code

This module analyzes:
- Function signature changes
- Return value structure changes
- Removed/renamed functions
- Changed constants/configurations
- Interface modifications

"I detect what breaks before it breaks you." - Oracle
"""

import logging
import ast
import json
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime
from pathlib import Path
import difflib

logger = logging.getLogger(__name__)


class ChangeType(str):
    """Types of code changes"""
    FUNCTION_REMOVED = "function_removed"
    FUNCTION_RENAMED = "function_renamed"
    SIGNATURE_CHANGED = "signature_changed"
    RETURN_TYPE_CHANGED = "return_type_changed"
    CONSTANT_CHANGED = "constant_changed"
    CLASS_REMOVED = "class_removed"
    INTERFACE_CHANGED = "interface_changed"


class BreakingSeverity(str):
    """Severity of breaking changes"""
    CRITICAL = "critical"      # Will definitely break dependents
    HIGH = "high"              # Likely to break dependents
    MEDIUM = "medium"          # May break some dependents
    LOW = "low"                # Unlikely to break dependents


class BreakingChangeDetector:
    """
    ⚠️ Breaking Change Detector

    Analyzes code changes to detect breaking changes:
    - Parses Python AST (Abstract Syntax Tree)
    - Compares old vs new code
    - Identifies breaking changes
    - Assesses severity and impact
    """

    def __init__(self):
        """Initialize Breaking Change Detector"""
        logger.info("⚠️ Breaking Change Detector initialized")

    def detect_breaking_changes(self,
                                old_code: str,
                                new_code: str,
                                agent_name: str) -> Dict[str, Any]:
        """
        ⚠️ Detect breaking changes between two versions

        Args:
            old_code: Previous version code
            new_code: New version code
            agent_name: Agent name

        Returns:
            Breaking change analysis
        """
        analysis = {
            'agent': agent_name,
            'analyzed_at': datetime.now().isoformat(),
            'has_breaking_changes': False,
            'breaking_changes': [],
            'non_breaking_changes': [],
            'overall_severity': BreakingSeverity.LOW,
            'migration_required': False,
            'affected_apis': []
        }

        try:
            # Parse both versions
            old_ast = ast.parse(old_code)
            new_ast = ast.parse(new_code)

            # Extract APIs from both versions
            old_apis = self._extract_public_apis(old_ast)
            new_apis = self._extract_public_apis(new_ast)

            # Detect removed functions
            removed_funcs = self._detect_removed_functions(old_apis, new_apis)
            if removed_funcs:
                analysis['breaking_changes'].extend(removed_funcs)
                analysis['has_breaking_changes'] = True

            # Detect signature changes
            signature_changes = self._detect_signature_changes(old_apis, new_apis)
            if signature_changes:
                analysis['breaking_changes'].extend(signature_changes)
                analysis['has_breaking_changes'] = True

            # Detect constant changes
            constant_changes = self._detect_constant_changes(old_ast, new_ast)
            if constant_changes:
                analysis['breaking_changes'].extend(constant_changes)

            # Detect class changes
            class_changes = self._detect_class_changes(old_ast, new_ast)
            if class_changes:
                analysis['breaking_changes'].extend(class_changes)

            # Determine overall severity
            if analysis['breaking_changes']:
                severities = [c['severity'] for c in analysis['breaking_changes']]
                if BreakingSeverity.CRITICAL in severities:
                    analysis['overall_severity'] = BreakingSeverity.CRITICAL
                elif BreakingSeverity.HIGH in severities:
                    analysis['overall_severity'] = BreakingSeverity.HIGH
                elif BreakingSeverity.MEDIUM in severities:
                    analysis['overall_severity'] = BreakingSeverity.MEDIUM

            # Migration required if critical or multiple high-severity changes
            critical_count = sum(1 for c in analysis['breaking_changes'] if c['severity'] == BreakingSeverity.CRITICAL)
            high_count = sum(1 for c in analysis['breaking_changes'] if c['severity'] == BreakingSeverity.HIGH)

            analysis['migration_required'] = critical_count > 0 or high_count > 2

            # List affected APIs
            analysis['affected_apis'] = list(set(
                c.get('function_name', c.get('constant_name', c.get('class_name', 'unknown')))
                for c in analysis['breaking_changes']
            ))

            logger.info(f"⚠️ Detected {len(analysis['breaking_changes'])} breaking changes in {agent_name}")

        except SyntaxError as e:
            logger.error(f"Syntax error parsing code: {e}")
            analysis['error'] = str(e)

        return analysis

    def _extract_public_apis(self, tree: ast.AST) -> Dict[str, Any]:
        """Extract public API functions and their signatures"""
        apis = {
            'functions': {},
            'classes': {},
            'constants': {}
        }

        for node in ast.walk(tree):
            # Extract functions
            if isinstance(node, ast.FunctionDef):
                # Only public functions (not starting with _)
                if not node.name.startswith('_'):
                    apis['functions'][node.name] = {
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args],
                        'defaults': len(node.args.defaults),
                        'returns': self._get_return_type(node),
                        'decorators': [self._get_decorator_name(d) for d in node.decorator_list]
                    }

            # Extract classes
            elif isinstance(node, ast.ClassDef):
                if not node.name.startswith('_'):
                    methods = []
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef) and not item.name.startswith('_'):
                            methods.append(item.name)

                    apis['classes'][node.name] = {
                        'name': node.name,
                        'methods': methods,
                        'bases': [self._get_base_name(b) for b in node.bases]
                    }

            # Extract module-level constants (UPPERCASE variables)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        apis['constants'][target.id] = {
                            'name': target.id,
                            'value': ast.unparse(node.value) if hasattr(ast, 'unparse') else 'unknown'
                        }

        return apis

    def _get_return_type(self, node: ast.FunctionDef) -> Optional[str]:
        """Extract return type from function"""
        if node.returns:
            return ast.unparse(node.returns) if hasattr(ast, 'unparse') else 'unknown'
        return None

    def _get_decorator_name(self, node: ast.expr) -> str:
        """Get decorator name"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            return node.func.id
        return 'unknown'

    def _get_base_name(self, node: ast.expr) -> str:
        """Get base class name"""
        if isinstance(node, ast.Name):
            return node.id
        return 'unknown'

    def _detect_removed_functions(self,
                                  old_apis: Dict[str, Any],
                                  new_apis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect functions that were removed"""
        removed = []

        old_funcs = set(old_apis['functions'].keys())
        new_funcs = set(new_apis['functions'].keys())

        for func_name in old_funcs - new_funcs:
            removed.append({
                'change_type': ChangeType.FUNCTION_REMOVED,
                'severity': BreakingSeverity.CRITICAL,
                'function_name': func_name,
                'description': f"Public function '{func_name}' was removed",
                'migration_hint': f"Replace calls to {func_name}() with alternative implementation"
            })

        return removed

    def _detect_signature_changes(self,
                                  old_apis: Dict[str, Any],
                                  new_apis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect function signature changes"""
        changes = []

        common_funcs = set(old_apis['functions'].keys()) & set(new_apis['functions'].keys())

        for func_name in common_funcs:
            old_func = old_apis['functions'][func_name]
            new_func = new_apis['functions'][func_name]

            # Check argument changes
            old_args = old_func['args']
            new_args = new_func['args']

            if old_args != new_args:
                # Determine severity
                if len(new_args) < len(old_args):
                    # Parameters removed - critical
                    severity = BreakingSeverity.CRITICAL
                    description = f"Function '{func_name}' removed parameters: {set(old_args) - set(new_args)}"
                elif len(new_args) > len(old_args):
                    # Parameters added
                    added = set(new_args) - set(old_args)
                    # Check if new params have defaults
                    if new_func['defaults'] >= len(added):
                        # Has defaults - low severity
                        severity = BreakingSeverity.LOW
                        description = f"Function '{func_name}' added optional parameters: {added}"
                    else:
                        # No defaults - critical
                        severity = BreakingSeverity.CRITICAL
                        description = f"Function '{func_name}' added required parameters: {added}"
                else:
                    # Parameter names changed
                    severity = BreakingSeverity.HIGH
                    description = f"Function '{func_name}' parameter names changed"

                changes.append({
                    'change_type': ChangeType.SIGNATURE_CHANGED,
                    'severity': severity,
                    'function_name': func_name,
                    'old_signature': f"{func_name}({', '.join(old_args)})",
                    'new_signature': f"{func_name}({', '.join(new_args)})",
                    'description': description,
                    'migration_hint': f"Update calls to {func_name}() to match new signature"
                })

            # Check return type changes
            if old_func['returns'] != new_func['returns']:
                if old_func['returns'] and new_func['returns']:
                    changes.append({
                        'change_type': ChangeType.RETURN_TYPE_CHANGED,
                        'severity': BreakingSeverity.HIGH,
                        'function_name': func_name,
                        'old_return': old_func['returns'],
                        'new_return': new_func['returns'],
                        'description': f"Function '{func_name}' return type changed",
                        'migration_hint': f"Update code that processes {func_name}() return value"
                    })

        return changes

    def _detect_constant_changes(self,
                                old_tree: ast.AST,
                                new_tree: ast.AST) -> List[Dict[str, Any]]:
        """Detect constant value changes"""
        changes = []

        old_apis = self._extract_public_apis(old_tree)
        new_apis = self._extract_public_apis(new_tree)

        old_consts = old_apis['constants']
        new_consts = new_apis['constants']

        # Removed constants
        for const_name in set(old_consts.keys()) - set(new_consts.keys()):
            changes.append({
                'change_type': ChangeType.CONSTANT_CHANGED,
                'severity': BreakingSeverity.HIGH,
                'constant_name': const_name,
                'description': f"Constant '{const_name}' was removed",
                'migration_hint': f"Update references to {const_name}"
            })

        # Changed constant values
        for const_name in set(old_consts.keys()) & set(new_consts.keys()):
            old_value = old_consts[const_name]['value']
            new_value = new_consts[const_name]['value']

            if old_value != new_value:
                changes.append({
                    'change_type': ChangeType.CONSTANT_CHANGED,
                    'severity': BreakingSeverity.MEDIUM,
                    'constant_name': const_name,
                    'old_value': old_value,
                    'new_value': new_value,
                    'description': f"Constant '{const_name}' value changed",
                    'migration_hint': f"Verify that new value of {const_name} doesn't break logic"
                })

        return changes

    def _detect_class_changes(self,
                             old_tree: ast.AST,
                             new_tree: ast.AST) -> List[Dict[str, Any]]:
        """Detect class structure changes"""
        changes = []

        old_apis = self._extract_public_apis(old_tree)
        new_apis = self._extract_public_apis(new_tree)

        old_classes = old_apis['classes']
        new_classes = new_apis['classes']

        # Removed classes
        for class_name in set(old_classes.keys()) - set(new_classes.keys()):
            changes.append({
                'change_type': ChangeType.CLASS_REMOVED,
                'severity': BreakingSeverity.CRITICAL,
                'class_name': class_name,
                'description': f"Class '{class_name}' was removed",
                'migration_hint': f"Replace usage of {class_name} class"
            })

        # Changed class methods
        for class_name in set(old_classes.keys()) & set(new_classes.keys()):
            old_methods = set(old_classes[class_name]['methods'])
            new_methods = set(new_classes[class_name]['methods'])

            # Removed methods
            removed_methods = old_methods - new_methods
            if removed_methods:
                changes.append({
                    'change_type': ChangeType.INTERFACE_CHANGED,
                    'severity': BreakingSeverity.HIGH,
                    'class_name': class_name,
                    'removed_methods': list(removed_methods),
                    'description': f"Class '{class_name}' removed methods: {removed_methods}",
                    'migration_hint': f"Update code calling {class_name}.{list(removed_methods)[0]}()"
                })

        return changes

    def generate_migration_guide(self, breaking_changes: List[Dict[str, Any]]) -> str:
        """
        Generate migration guide based on breaking changes

        Args:
            breaking_changes: List of detected breaking changes

        Returns:
            Markdown migration guide
        """
        guide_lines = [
            "# Migration Guide",
            "",
            f"Generated: {datetime.now().isoformat()}",
            "",
            f"## Summary",
            "",
            f"Total breaking changes: {len(breaking_changes)}",
            ""
        ]

        # Group by severity
        by_severity = {
            BreakingSeverity.CRITICAL: [],
            BreakingSeverity.HIGH: [],
            BreakingSeverity.MEDIUM: [],
            BreakingSeverity.LOW: []
        }

        for change in breaking_changes:
            by_severity[change['severity']].append(change)

        # Critical changes
        if by_severity[BreakingSeverity.CRITICAL]:
            guide_lines.extend([
                "## Critical Changes (Immediate Action Required)",
                ""
            ])
            for change in by_severity[BreakingSeverity.CRITICAL]:
                guide_lines.append(f"### {change['description']}")
                guide_lines.append(f"**Migration:** {change.get('migration_hint', 'Manual review required')}")
                guide_lines.append("")

        # High severity changes
        if by_severity[BreakingSeverity.HIGH]:
            guide_lines.extend([
                "## High Severity Changes",
                ""
            ])
            for change in by_severity[BreakingSeverity.HIGH]:
                guide_lines.append(f"### {change['description']}")
                guide_lines.append(f"**Migration:** {change.get('migration_hint', 'Review and update code')}")
                guide_lines.append("")

        # Medium severity changes
        if by_severity[BreakingSeverity.MEDIUM]:
            guide_lines.extend([
                "## Medium Severity Changes",
                ""
            ])
            for change in by_severity[BreakingSeverity.MEDIUM]:
                guide_lines.append(f"- {change['description']}")

        guide_lines.extend([
            "",
            "## Testing Recommendations",
            "",
            "1. Run full test suite",
            "2. Test all affected functionality",
            "3. Verify dependent agents",
            "4. Perform integration testing",
            ""
        ])

        return '\n'.join(guide_lines)


def analyze_code_changes(old_code_path: Path, new_code_path: Path, agent_name: str) -> Dict[str, Any]:
    """
    ⚠️ Analyze code changes and detect breaking changes

    Args:
        old_code_path: Path to old version
        new_code_path: Path to new version
        agent_name: Agent name

    Returns:
        Breaking change analysis
    """
    detector = BreakingChangeDetector()

    if not old_code_path.exists() or not new_code_path.exists():
        return {
            'error': 'Code files not found',
            'has_breaking_changes': False
        }

    old_code = old_code_path.read_text()
    new_code = new_code_path.read_text()

    analysis = detector.detect_breaking_changes(old_code, new_code, agent_name)

    logger.info(f"⚠️ Analyzed {agent_name}: {len(analysis['breaking_changes'])} breaking changes detected")

    return analysis
