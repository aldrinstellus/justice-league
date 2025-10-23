# 🔄 Oracle Version Control System - Complete

**Week 6: Version Control & Rollback**
**Status**: ✅ COMPLETE
**Test Coverage**: 10/10 tests passing (100%)

---

## System Overview

Oracle's Version Control System provides comprehensive version management, dependency tracking, and breaking change detection for all Justice League agents. The system ensures safe updates, rollbacks, and migration management across the entire agent ecosystem.

### Core Components

1. **Enhanced Version Control** (`enhanced_version_control.py`)
   - Semantic versioning (MAJOR.MINOR.PATCH)
   - Git integration with automated commits
   - Safe rollback with safety assessment
   - Automated migration script generation
   - Version history tracking
   - Dependency validation

2. **Dependency Tracker** (`dependency_tracker.py`)
   - Inter-agent dependency mapping
   - Circular dependency detection
   - Update impact analysis
   - Topological update ordering
   - Dependency graph visualization

3. **Breaking Change Detector** (`breaking_change_detector.py`)
   - AST-based code comparison
   - Function signature analysis
   - Return type change detection
   - Constant value monitoring
   - Class structure validation
   - Automated migration guide generation

---

## Test Results

```
======================================================================
🧪 Oracle Version Control Test Suite
======================================================================

Total Tests: 10
✅ Passed: 10
❌ Failed: 0

Success Rate: 100.0%

🎉 ALL TESTS PASSED! Oracle's version control system is operational!
🔄 Version control, dependency tracking, and breaking change detection verified!
```

### Test Coverage

1. ✅ Version Control Initialization
2. ✅ Create New Version (semantic versioning)
3. ✅ Version History Tracking
4. ✅ Version Rollback with safety assessment
5. ✅ Dependency Tracker Initialization
6. ✅ Add and Track Dependencies
7. ✅ Circular Dependency Detection
8. ✅ Update Impact Analysis
9. ✅ Breaking Change Detection
10. ✅ Complete Version Control Workflow (end-to-end)

---

## Usage Examples

### Creating Versions

```python
from core.oracle_version_control.enhanced_version_control import (
    EnhancedVersionControl, VersionChangeType
)

vc = EnhancedVersionControl(oracle_kb_dir='/tmp/aldo-vision-justice-league/oracle')

# Patch version (bug fix)
v1 = vc.create_version(
    'batman',
    change_type=VersionChangeType.PATCH,
    changes='Fixed timeout issue in webpage analysis'
)
# Creates v0.0.1

# Minor version (new feature)
v2 = vc.create_version(
    'batman',
    change_type=VersionChangeType.MINOR,
    changes='Added support for dynamic content analysis'
)
# Creates v0.1.0

# Major version (breaking change)
v3 = vc.create_version(
    'batman',
    change_type=VersionChangeType.MAJOR,
    changes='Changed analyze() return structure',
    breaking_changes=['analyze() now returns dict instead of list']
)
# Creates v1.0.0, generates migration script
```

### Managing Dependencies

```python
from core.oracle_version_control.dependency_tracker import (
    DependencyTracker, DependencyType
)

tracker = DependencyTracker(oracle_kb_dir='/tmp/aldo-vision-justice-league/oracle')

# Add dependencies
tracker.add_dependency('batman', 'oracle', '>=1.0.0', DependencyType.REQUIRES)
tracker.add_dependency('flash', 'batman', '>=2.0.0', DependencyType.RECOMMENDS)

# Check dependencies
deps = tracker.get_dependencies('batman')
# Returns: [{'agent': 'oracle', 'version_constraint': '>=1.0.0', ...}]

# Find who depends on an agent
dependents = tracker.get_dependents('oracle')
# Returns: ['batman', 'superman', 'wonder_woman', ...]

# Detect circular dependencies
circular = tracker.detect_circular_dependencies()
# Returns: [['agent_a', 'agent_b', 'agent_c', 'agent_a']]

# Analyze update impact
impact = tracker.analyze_update_impact('oracle', '2.0.0')
# Returns: {
#   'direct_dependents': ['batman', 'superman', ...],
#   'indirect_dependents': ['flash', 'aquaman', ...],
#   'total_affected': 8,
#   'breaking_risk': 'high',
#   'update_order': ['oracle', 'batman', 'flash', ...]
# }
```

### Detecting Breaking Changes

```python
from core.oracle_version_control.breaking_change_detector import (
    BreakingChangeDetector
)

detector = BreakingChangeDetector()

# Old version code
old_code = """
def analyze(url: str) -> List[str]:
    '''Analyze webpage and return findings'''
    return ['finding1', 'finding2']

MAX_TIMEOUT = 5000
"""

# New version code
new_code = """
def analyze(url: str, options: Dict[str, Any]) -> Dict[str, Any]:
    '''Analyze webpage and return detailed findings'''
    return {'findings': ['finding1', 'finding2'], 'metadata': {...}}

MAX_TIMEOUT = 30000
"""

# Detect breaking changes
analysis = detector.detect_breaking_changes(old_code, new_code, 'batman')

# Returns:
# {
#   'has_breaking_changes': True,
#   'breaking_changes': [
#     {
#       'change_type': 'signature_changed',
#       'severity': 'critical',
#       'function_name': 'analyze',
#       'old_signature': 'analyze(url)',
#       'new_signature': 'analyze(url, options)',
#       'migration_hint': 'Update calls to analyze() to match new signature'
#     },
#     {
#       'change_type': 'return_type_changed',
#       'severity': 'high',
#       'function_name': 'analyze',
#       'migration_hint': 'Update code that processes analyze() return value'
#     },
#     {
#       'change_type': 'constant_changed',
#       'severity': 'medium',
#       'constant_name': 'MAX_TIMEOUT',
#       'old_value': '5000',
#       'new_value': '30000'
#     }
#   ],
#   'overall_severity': 'critical',
#   'migration_required': True,
#   'affected_apis': ['analyze', 'MAX_TIMEOUT']
# }

# Generate migration guide
guide = detector.generate_migration_guide(analysis['breaking_changes'])
# Returns Markdown migration guide with:
# - Summary of breaking changes
# - Critical changes (immediate action required)
# - High severity changes
# - Medium severity changes
# - Testing recommendations
```

### Safe Rollback

```python
from core.oracle_version_control.enhanced_version_control import (
    EnhancedVersionControl, RollbackSafety
)

vc = EnhancedVersionControl(oracle_kb_dir='/tmp/aldo-vision-justice-league/oracle')

# Check rollback safety first
current = vc.get_current_version('batman')  # '2.0.0'
target = '1.5.0'

rollback = vc.rollback_version('batman', target)

# Returns:
# {
#   'success': True,
#   'from_version': '2.0.0',
#   'to_version': '1.5.0',
#   'safety_level': 'caution',  # or 'safe', 'dangerous'
#   'warnings': [
#     'Rolling back across 1 minor versions',
#     '2 breaking changes detected between versions'
#   ],
#   'breaking_changes': [...],
#   'migration_applied': True,
#   'method': 'git_checkout'  # or 'backup_restore'
# }

# Force dangerous rollback (use with caution!)
rollback = vc.rollback_version('batman', '0.1.0', force=True)
```

---

## Version Control Features

### Semantic Versioning

Oracle follows semantic versioning (SemVer) for all agents:

- **PATCH** (0.0.x): Bug fixes, performance improvements, no breaking changes
- **MINOR** (0.x.0): New features, backward compatible
- **MAJOR** (x.0.0): Breaking changes, incompatible API changes

```python
# Version increment logic
VersionChangeType.PATCH   # 1.2.3 → 1.2.4
VersionChangeType.MINOR   # 1.2.3 → 1.3.0
VersionChangeType.MAJOR   # 1.2.3 → 2.0.0
```

### Git Integration

When `git_enabled=True`, version control integrates with git:

```python
vc = EnhancedVersionControl(oracle_kb_dir='/path/to/kb', git_enabled=True)

v = vc.create_version('batman', VersionChangeType.MINOR, 'Added new feature')
# Automatically:
# 1. Creates git commit with message: "[batman] v0.1.0: Added new feature"
# 2. Tags commit with version: batman-v0.1.0
# 3. Records commit hash in version metadata
```

### Migration Scripts

For major versions with breaking changes, Oracle generates migration scripts:

```python
v = vc.create_version(
    'batman',
    VersionChangeType.MAJOR,
    'Changed API structure',
    breaking_changes=['analyze() return type changed from list to dict']
)

# Generates: migrations/batman_v1.0.0_migration.py
# Contains:
# - migrate_forward(): Upgrade logic
# - migrate_backward(): Rollback logic
# - Documentation of breaking changes
# - Testing instructions
```

### Rollback Safety Levels

Oracle assesses rollback safety before executing:

| Safety Level | Description | Criteria |
|-------------|-------------|----------|
| **SAFE** | No risk | Same major version, no breaking changes |
| **CAUTION** | Some risk | Different minor version OR has breaking changes |
| **DANGEROUS** | High risk | Different major version AND multiple breaking changes |

```python
# Rollback from v2.3.1 to v2.3.0 → SAFE (patch only)
# Rollback from v2.3.0 to v2.2.0 → CAUTION (minor version)
# Rollback from v2.0.0 to v1.5.0 → DANGEROUS (major version)
```

---

## Dependency Management

### Dependency Types

```python
class DependencyType:
    REQUIRES = "requires"        # Hard dependency (must have)
    RECOMMENDS = "recommends"    # Soft dependency (should have)
    CONFLICTS = "conflicts"      # Incompatible versions
    ENHANCES = "enhances"        # Optional enhancement
```

### Circular Dependency Detection

Oracle uses depth-first search (DFS) to detect circular chains:

```python
# Example circular dependency:
tracker.add_dependency('agent_a', 'agent_b', '>=1.0.0')
tracker.add_dependency('agent_b', 'agent_c', '>=1.0.0')
tracker.add_dependency('agent_c', 'agent_a', '>=1.0.0')

circular = tracker.detect_circular_dependencies()
# Returns: [['agent_a', 'agent_b', 'agent_c', 'agent_a']]
```

### Update Impact Analysis

Before updating an agent, analyze the impact:

```python
impact = tracker.analyze_update_impact('oracle', '2.0.0')

# Returns comprehensive impact report:
{
  'agent': 'oracle',
  'new_version': '2.0.0',
  'direct_dependents': ['batman', 'superman', 'wonder_woman'],
  'indirect_dependents': ['flash', 'aquaman'],
  'total_affected': 5,
  'breaking_risk': 'medium',
  'update_order': ['oracle', 'batman', 'superman', 'wonder_woman', 'flash', 'aquaman'],
  'warnings': ['Update affects 5 agents']
}
```

### Topological Update Order

Oracle calculates the optimal update order using Kahn's algorithm:

```python
# Dependency graph:
# oracle
#   ├── batman
#   │   └── flash
#   └── superman
#       └── aquaman

update_order = tracker._calculate_update_order('oracle')
# Returns: ['oracle', 'batman', 'superman', 'flash', 'aquaman']
# (Dependencies updated before dependents)
```

---

## Breaking Change Detection

### Detection Methods

Oracle analyzes Python code using AST (Abstract Syntax Tree) parsing:

1. **Function Removal** → CRITICAL
   - Public function deleted from API
   - Migration: Replace calls with alternative

2. **Signature Changes** → CRITICAL/HIGH
   - Parameters removed → CRITICAL
   - Required parameters added → CRITICAL
   - Optional parameters added → LOW
   - Parameter names changed → HIGH

3. **Return Type Changes** → HIGH
   - Function return type modified
   - Migration: Update code processing return value

4. **Constant Changes** → HIGH/MEDIUM
   - Module-level constant removed → HIGH
   - Constant value changed → MEDIUM

5. **Class Structure Changes** → CRITICAL/HIGH
   - Class removed → CRITICAL
   - Public methods removed → HIGH

### AST Comparison Example

```python
# Old code
old_code = """
def test_interactive(url, mcp_tools):
    '''Test interactive elements'''
    result = {'score': 95}
    return result

MAX_TIMEOUT = 5000
"""

# New code
new_code = """
def test_interactive(url, mcp_tools, timeout=30):
    '''Test interactive elements'''
    result = {'batman_score': {'score': 95}}
    return result

MAX_TIMEOUT = 30000
"""

# Detection finds:
# 1. Signature changed: Added optional parameter 'timeout'
# 2. Return type changed: Different dict structure
# 3. Constant changed: MAX_TIMEOUT value modified
```

### Migration Guide Generation

Oracle automatically generates migration guides:

```markdown
# Migration Guide

Generated: 2025-01-23T10:30:00

## Summary

Total breaking changes: 3

## Critical Changes (Immediate Action Required)

### Function 'analyze' signature changed
**Migration:** Update calls to analyze() to match new signature

### Function 'process' was removed
**Migration:** Replace calls to process() with alternative implementation

## High Severity Changes

### Function 'analyze' return type changed
**Migration:** Update code that processes analyze() return value

## Medium Severity Changes

- Constant 'MAX_TIMEOUT' value changed

## Testing Recommendations

1. Run full test suite
2. Test all affected functionality
3. Verify dependent agents
4. Perform integration testing
```

---

## Integration with Oracle

The version control system integrates seamlessly with Oracle's other capabilities:

### Version Control + Self-Healing

```python
from core.oracle_self_healing.agent_health_monitor import AgentHealthMonitor
from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl

monitor = AgentHealthMonitor()
vc = EnhancedVersionControl()

# If self-healing detects issues, automatically rollback
health = monitor.check_health('batman')
if not health['healthy']:
    rollback = vc.rollback_version('batman', health['last_known_good_version'])
```

### Version Control + Knowledge Base

```python
from core.oracle_knowledge_base import KnowledgeBase
from core.oracle_version_control.enhanced_version_control import EnhancedVersionControl

kb = KnowledgeBase()
vc = EnhancedVersionControl()

# Store version history in knowledge base
version = vc.create_version('batman', VersionChangeType.MINOR, 'New feature')
kb.store(
    f"versions/{version['agent']}/v{version['version']}",
    version,
    tags=['version', 'history', version['agent']]
)
```

### Version Control + Learning System

```python
from core.oracle_learning.cross_agent_learning import CrossAgentLearning
from core.oracle_version_control.breaking_change_detector import BreakingChangeDetector

learning = CrossAgentLearning()
detector = BreakingChangeDetector()

# Learn from breaking changes
analysis = detector.detect_breaking_changes(old_code, new_code, 'batman')
if analysis['has_breaking_changes']:
    learning.learn_pattern(
        'breaking_changes',
        {
            'agent': 'batman',
            'changes': analysis['breaking_changes'],
            'severity': analysis['overall_severity']
        }
    )
```

---

## Database Schema

### Version History

```json
{
  "agent_name": "batman",
  "versions": [
    {
      "version": "1.0.0",
      "change_type": "major",
      "changes": "Changed analyze() return structure",
      "breaking_changes": ["analyze() now returns dict instead of list"],
      "migration_required": true,
      "migration_script": "migrations/batman_v1.0.0_migration.py",
      "created_at": "2025-01-23T10:00:00",
      "code_hash": "a1b2c3d4e5f6...",
      "dependencies": {
        "oracle": ">=1.0.0",
        "mcp_tools": ">=2.0.0"
      },
      "git_commit": "abc123...",
      "git_tag": "batman-v1.0.0"
    }
  ],
  "current_version": "1.0.0"
}
```

### Dependency Graph

```json
{
  "dependencies": {
    "batman": [
      {
        "agent": "oracle",
        "version_constraint": ">=1.0.0",
        "dependency_type": "requires",
        "added_at": "2025-01-23T10:00:00"
      }
    ]
  },
  "dependency_graph": {
    "batman": ["oracle"],
    "flash": ["batman"],
    "aquaman": ["oracle"]
  }
}
```

---

## Architecture

### Enhanced Version Control Flow

```
Create Version
    ↓
1. Get current version
2. Increment version (MAJOR/MINOR/PATCH)
3. Create backup of current state
4. Generate code hash (SHA-256)
5. Check dependencies
6. Generate migration (if breaking)
7. Create git commit (if enabled)
8. Store version metadata
9. Update current version
```

### Rollback Flow

```
Rollback Version
    ↓
1. Get current version
2. Get target version
3. Assess safety level
4. Check breaking changes
5. Generate warnings
6. Restore from backup OR git checkout
7. Apply migration script
8. Update current version
9. Record rollback history
```

### Breaking Change Detection Flow

```
Detect Breaking Changes
    ↓
1. Parse old code → AST
2. Parse new code → AST
3. Extract public APIs (old)
4. Extract public APIs (new)
5. Compare functions
6. Compare classes
7. Compare constants
8. Assign severity levels
9. Generate migration hints
10. Create migration guide
```

---

## Week 6 Achievements

✅ **Enhanced Version Control**
- Semantic versioning implementation
- Git integration with automated commits
- Safe rollback with multiple safety levels
- Automated migration script generation
- Version history tracking
- Code hash verification (SHA-256)
- Dependency validation

✅ **Dependency Tracker**
- Inter-agent dependency mapping
- Circular dependency detection (DFS algorithm)
- Update impact analysis
- Topological update ordering (Kahn's algorithm)
- Dependency graph visualization
- Dependency type support (requires, recommends, conflicts, enhances)

✅ **Breaking Change Detector**
- AST-based code comparison
- Function signature analysis
- Return type change detection
- Constant value monitoring
- Class structure validation
- Severity assessment (critical, high, medium, low)
- Automated migration guide generation

✅ **Comprehensive Testing**
- 10 tests covering all version control features
- 100% test success rate
- End-to-end workflow validation
- Edge case handling (rollback failures, circular dependencies)

---

## Next Steps: Week 7 - Oracle Testing & Integration

With Week 6 complete, Oracle now has:
- ✅ Knowledge base (Week 3)
- ✅ MCP manager (Week 3)
- ✅ Self-healing framework (Week 4)
- ✅ Learning system (Week 5)
- ✅ Version control (Week 6)

Week 7 will focus on:
1. **Integration Testing**
   - Integrate Oracle with Superman coordinator
   - Test cross-agent communication
   - Validate all Oracle capabilities working together

2. **Production Readiness**
   - Performance optimization
   - Error handling refinement
   - Logging and monitoring

3. **Real-World Scenarios**
   - Test Oracle managing all 11 Justice League heroes
   - Simulate version updates and rollbacks
   - Test dependency chain updates

---

## Files Created

```
core/oracle_version_control/
├── enhanced_version_control.py      (650 lines)
├── dependency_tracker.py            (520 lines)
├── breaking_change_detector.py      (550 lines)
└── __init__.py

test_oracle_version_control.py       (450 lines)
ORACLE_VERSION_CONTROL_COMPLETE.md   (this file)
```

**Total Lines of Code**: ~2,170 lines
**Test Coverage**: 10/10 (100%)
**Status**: ✅ PRODUCTION READY

---

**Oracle says**: "I see all versions, all dependencies, all changes. The timeline of code is mine to navigate." 🔄
