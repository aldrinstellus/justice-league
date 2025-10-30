# 🔮 Oracle Best Practices Guide

**Development standards and guidelines for Oracle and Justice League agents**

Version: 1.0.0
Last Updated: January 2025

---

## Table of Contents

1. [Introduction](#introduction)
2. [Agent Development Standards](#agent-development-standards)
3. [Testing Guidelines](#testing-guidelines)
4. [Version Control Practices](#version-control-practices)
5. [Deployment Procedures](#deployment-procedures)
6. [Health Monitoring](#health-monitoring)
7. [Self-Healing Configuration](#self-healing-configuration)
8. [Dependency Management](#dependency-management)
9. [Performance Optimization](#performance-optimization)
10. [Security Best Practices](#security-best-practices)

---

## Introduction

This guide establishes standards and best practices for developing, testing, and deploying Justice League agents with Oracle oversight. Following these guidelines ensures consistent quality, maintainability, and reliability across the entire agent ecosystem.

### Core Principles

1. **Consistency**: All agents follow the same patterns and standards
2. **Testability**: Every feature has comprehensive tests
3. **Observability**: Health metrics are tracked and monitored
4. **Versioning**: Semantic versioning for all changes
5. **Self-Healing**: Design for automatic recovery
6. **Learning**: Share knowledge across agents

---

## Agent Development Standards

### Agent Structure

Every Justice League agent should follow this structure:

```
hero_name/
├── __init__.py
├── main.py              # Entry point
├── config.py            # Configuration
├── analyzers/           # Core analysis logic
│   ├── page_analyzer.py
│   ├── selector_analyzer.py
│   └── ...
├── utils/               # Helper utilities
│   ├── mcp_tools.py
│   └── ...
├── tests/               # Test files
│   ├── test_main.py
│   ├── test_analyzers.py
│   └── ...
└── README.md            # Agent documentation
```

### Code Style

#### Python Style Guide

Follow PEP 8 with these specific requirements:

```python
# Good: Clear, documented function
def analyze_interactive_elements(
    url: str,
    mcp_tools: Dict[str, Any],
    timeout: int = 30
) -> Dict[str, Any]:
    """
    Analyze interactive elements on webpage.

    Args:
        url: Target webpage URL
        mcp_tools: MCP tools for browser automation
        timeout: Maximum analysis time in seconds

    Returns:
        Analysis results with scores and recommendations

    Raises:
        TimeoutError: If analysis exceeds timeout
        ValueError: If URL is invalid
    """
    # Implementation...
    pass


# Bad: Unclear, undocumented
def analyze(u, t, x=30):
    # Do stuff
    pass
```

#### Type Hints

Always use type hints:

```python
from typing import Dict, List, Any, Optional

# Good
def process_results(
    results: List[Dict[str, Any]],
    threshold: float = 0.5
) -> Optional[Dict[str, float]]:
    pass

# Bad
def process_results(results, threshold=0.5):
    pass
```

#### Error Handling

Proper error handling with specific exceptions:

```python
# Good: Specific error handling
try:
    result = mcp_tools['navigate'](url, timeout=30)
except TimeoutError as e:
    logger.error(f"Navigation timeout for {url}: {e}")
    return {'error': 'timeout', 'url': url}
except ValueError as e:
    logger.error(f"Invalid URL {url}: {e}")
    return {'error': 'invalid_url', 'url': url}
finally:
    # Cleanup
    mcp_tools.get('cleanup', lambda: None)()

# Bad: Catch-all error handling
try:
    result = mcp_tools['navigate'](url)
except:
    return {'error': 'failed'}
```

### Logging Standards

Use structured logging:

```python
import logging

logger = logging.getLogger(__name__)

# Good: Structured logging with context
logger.info(
    "Analysis complete",
    extra={
        'agent': 'batman',
        'url': url,
        'duration': 1.5,
        'score': 0.92
    }
)

# Good: Appropriate log levels
logger.debug("Starting selector analysis")
logger.info("Analysis complete")
logger.warning("Slow response time detected")
logger.error("Failed to load page")
logger.critical("System failure - emergency rollback required")
```

### Documentation Standards

Every agent must have:

1. **README.md** with:
   - Purpose and capabilities
   - Usage examples
   - Configuration options
   - Known limitations

2. **Docstrings** for all:
   - Modules
   - Classes
   - Public functions
   - Complex private functions

3. **Inline comments** for:
   - Complex algorithms
   - Business logic
   - Workarounds

Example README.md:

```markdown
# Batman - Webpage Analysis Agent

## Purpose
Batman analyzes webpages for structure, selectors, and interactive elements.

## Capabilities
- Page structure analysis
- Selector stability scoring
- Interactive element detection
- Accessibility validation

## Usage
```python
from batman import analyze

result = analyze("https://example.com", mcp_tools)
```

## Configuration
- `BATMAN_TIMEOUT`: Analysis timeout (default: 30s)
- `BATMAN_MAX_DEPTH`: Maximum DOM depth (default: 10)

## Known Limitations
- Cannot analyze pages requiring authentication
- Limited support for Shadow DOM
```

---

## Testing Guidelines

### Test Coverage Requirements

- **Minimum**: 80% code coverage
- **Target**: 90% code coverage
- **Required**: 100% coverage for critical paths

### Test Structure

Every agent must have tests for:

1. **Unit Tests**: Individual functions
2. **Integration Tests**: Component interactions
3. **End-to-End Tests**: Complete workflows
4. **Performance Tests**: Response time and throughput

Example test structure:

```python
import pytest
from unittest.mock import Mock, patch
from batman import analyze

class TestBatmanAnalyzer:
    """Test suite for Batman analyzer"""

    def test_basic_analysis(self):
        """Test basic webpage analysis"""
        # Arrange
        url = "https://example.com"
        mcp_tools = self._get_mock_mcp_tools()

        # Act
        result = analyze(url, mcp_tools)

        # Assert
        assert result['success']
        assert 'selectors' in result
        assert result['score'] > 0

    def test_timeout_handling(self):
        """Test timeout error handling"""
        url = "https://slow-site.com"
        mcp_tools = self._get_slow_mcp_tools()

        result = analyze(url, mcp_tools, timeout=1)

        assert not result['success']
        assert result['error'] == 'timeout'

    def test_invalid_url(self):
        """Test invalid URL handling"""
        with pytest.raises(ValueError):
            analyze("not-a-url", {})

    def _get_mock_mcp_tools(self) -> Dict:
        """Helper to create mock MCP tools"""
        return {
            'navigate': Mock(return_value={'status': 'success'}),
            'take_snapshot': Mock(return_value={'content': '<html>...'}),
            'evaluate_script': Mock(return_value={'result': [...]})
        }

    def _get_slow_mcp_tools(self) -> Dict:
        """Helper to create slow MCP tools for timeout testing"""
        import time

        def slow_navigate(*args, **kwargs):
            time.sleep(5)
            return {'status': 'success'}

        return {
            'navigate': slow_navigate,
            'take_snapshot': Mock(),
            'evaluate_script': Mock()
        }
```

### Test Naming Convention

```python
# Good: Descriptive test names
def test_analyze_returns_selectors_for_valid_page():
    pass

def test_analyze_raises_timeout_error_for_slow_page():
    pass

def test_analyze_handles_missing_mcp_tools_gracefully():
    pass

# Bad: Unclear test names
def test_1():
    pass

def test_analyze():
    pass

def test_error():
    pass
```

### Running Tests

All agents must pass tests before commit:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=batman --cov-report=html tests/

# Run specific test
pytest tests/test_main.py::TestBatmanAnalyzer::test_basic_analysis

# Run performance tests
pytest tests/test_performance.py --benchmark-only
```

---

## Version Control Practices

### Semantic Versioning

Follow SemVer strictly:

- **MAJOR** (x.0.0): Breaking changes
  - Changed function signatures
  - Removed functions/classes
  - Changed return types
  - Modified behavior significantly

- **MINOR** (0.x.0): New features, backward compatible
  - New functions/classes
  - New parameters with defaults
  - Enhanced functionality
  - Performance improvements

- **PATCH** (0.0.x): Bug fixes
  - Bug fixes
  - Documentation updates
  - Code refactoring (no behavior change)
  - Dependency updates

### Version Creation Workflow

```python
from core.oracle_integration.superman_connector import get_superman_interface

connector = get_superman_interface()

# 1. Determine change type
change_type = 'minor'  # 'major', 'minor', or 'patch'

# 2. Analyze impact (for major/minor)
if change_type in ['major', 'minor']:
    impact = connector.analyze_update_impact('batman', 'next_version')
    if impact['breaking_risk'] == 'high':
        print("⚠️ High breaking risk - coordinate with team")

# 3. Create version
version = connector.request_version_update(
    'batman',
    change_type,
    'Description of changes',
    breaking_changes=['List of breaking changes'] if change_type == 'major' else []
)

# 4. Test in staging
# Run comprehensive tests

# 5. Deploy to production
# Follow deployment procedures
```

### Branching Strategy

```
main (production)
  ├── develop (integration)
  │   ├── feature/batman-shadow-dom-support
  │   ├── feature/flash-speed-optimization
  │   └── bugfix/aquaman-timeout-issue
  └── hotfix/critical-batman-selector-bug
```

**Branch naming**:
- `feature/agent-feature-description`
- `bugfix/agent-bug-description`
- `hotfix/critical-issue-description`

### Commit Messages

Follow conventional commits:

```
# Good commit messages
feat(batman): add Shadow DOM support
fix(flash): resolve timeout issue for slow pages
docs(oracle): update API reference
test(aquaman): add integration tests for deep analysis
refactor(wonder_woman): simplify selector logic
perf(cyborg): optimize snapshot processing

# Bad commit messages
fixed stuff
update
wip
batman changes
```

---

## Deployment Procedures

### Pre-Deployment Checklist

- [ ] All tests passing (100%)
- [ ] Code coverage >= 80%
- [ ] No critical security vulnerabilities
- [ ] Documentation updated
- [ ] Version number incremented
- [ ] Breaking changes documented
- [ ] Impact analysis completed (if major/minor)
- [ ] Staging environment tested
- [ ] Rollback plan prepared

### Deployment Workflow

```python
# 1. Pre-deployment health check
connector = get_superman_interface()
health = connector.get_agent_health_summary()

if health['health_percentage'] < 90:
    print("⚠️ System health below 90% - postpone deployment")
    exit(1)

# 2. Create version
version = connector.request_version_update(
    'batman',
    'minor',
    'Deployment: Added new feature X'
)

# 3. Monitor for 15 minutes
import time
time.sleep(900)  # 15 minutes

# 4. Check health after deployment
post_health = connector.get_agent_health_summary()

if post_health['agents']['batman']['status'] != 'healthy':
    # Emergency rollback
    connector.emergency_rollback('batman', 'Post-deployment health check failed')
    print("🚨 Emergency rollback executed")
else:
    print("✅ Deployment successful")
```

### Staged Rollout

For high-risk changes, use staged rollout:

```python
# Phase 1: Deploy to 10% of traffic
deploy_to_percentage('batman', '2.0.0', percentage=10)
monitor_for_minutes(30)

# Phase 2: Deploy to 50% if Phase 1 successful
if get_error_rate('batman') < 0.02:
    deploy_to_percentage('batman', '2.0.0', percentage=50)
    monitor_for_minutes(30)
else:
    rollback('batman')

# Phase 3: Deploy to 100% if Phase 2 successful
if get_error_rate('batman') < 0.02:
    deploy_to_percentage('batman', '2.0.0', percentage=100)
else:
    rollback('batman')
```

---

## Health Monitoring

### Metrics to Track

Every agent must expose these metrics:

```python
{
    'agent': 'batman',
    'timestamp': '2025-01-23T10:00:00',
    'metrics': {
        'success_rate': 0.95,           # Percentage of successful analyses
        'error_rate': 0.02,              # Percentage of errors
        'response_time_avg': 1500,      # Average in milliseconds
        'response_time_p95': 3000,      # 95th percentile
        'response_time_p99': 5000,      # 99th percentile
        'memory_usage': 0.45,            # Percentage (0-1)
        'cpu_usage': 0.30,               # Percentage (0-1)
        'requests_per_minute': 60,
        'active_connections': 5
    }
}
```

### Health Check Implementation

```python
def get_health_metrics() -> Dict[str, Any]:
    """Get current health metrics for this agent"""
    return {
        'success_rate': calculate_success_rate(),
        'error_rate': calculate_error_rate(),
        'response_time_avg': get_avg_response_time(),
        'response_time_p95': get_p95_response_time(),
        'memory_usage': get_memory_usage(),
        'cpu_usage': get_cpu_usage()
    }

def calculate_success_rate() -> float:
    """Calculate success rate from recent operations"""
    recent_ops = get_recent_operations(limit=100)
    if not recent_ops:
        return 0.0

    successful = sum(1 for op in recent_ops if op['success'])
    return successful / len(recent_ops)
```

### Alerting Thresholds

Configure alerts for your agent:

```python
ALERT_THRESHOLDS = {
    'success_rate': {
        'warning': 0.90,    # Alert if < 90%
        'critical': 0.80     # Critical if < 80%
    },
    'error_rate': {
        'warning': 0.05,    # Alert if > 5%
        'critical': 0.10     # Critical if > 10%
    },
    'response_time_p95': {
        'warning': 5000,    # Alert if > 5s
        'critical': 10000    # Critical if > 10s
    }
}
```

---

## Self-Healing Configuration

### Design for Self-Healing

Build agents with self-healing in mind:

```python
class ResilientAnalyzer:
    """Example of self-healing design patterns"""

    def __init__(self):
        self.retry_config = {
            'max_retries': 3,
            'backoff_factor': 2,
            'timeout': 30
        }

    def analyze(self, url: str) -> Dict[str, Any]:
        """Analyze with automatic retry and recovery"""
        for attempt in range(self.retry_config['max_retries']):
            try:
                return self._do_analysis(url)
            except TimeoutError:
                if attempt < self.retry_config['max_retries'] - 1:
                    # Exponential backoff
                    wait_time = self.retry_config['backoff_factor'] ** attempt
                    logger.warning(f"Timeout, retrying in {wait_time}s")
                    time.sleep(wait_time)
                else:
                    # Final attempt failed
                    logger.error("Max retries exceeded")
                    return self._get_fallback_result(url)
            except Exception as e:
                # Unexpected error - attempt recovery
                logger.error(f"Unexpected error: {e}")
                self._attempt_recovery()

                if attempt < self.retry_config['max_retries'] - 1:
                    continue
                else:
                    return self._get_fallback_result(url)

    def _attempt_recovery(self):
        """Attempt to recover from error"""
        # Clear caches
        self._clear_caches()
        # Reset connections
        self._reset_connections()
        # Reload configuration
        self._reload_config()

    def _get_fallback_result(self, url: str) -> Dict[str, Any]:
        """Return safe fallback result"""
        return {
            'success': False,
            'url': url,
            'error': 'analysis_failed',
            'fallback': True
        }
```

### Cachingfor Resilience

Implement caching to reduce failures:

```python
from functools import lru_cache
import time

class CachedAnalyzer:
    """Analyzer with caching for resilience"""

    def __init__(self):
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes

    def analyze(self, url: str) -> Dict[str, Any]:
        """Analyze with caching"""
        cache_key = self._get_cache_key(url)

        # Check cache
        if cache_key in self.cache:
            cached_result, cached_time = self.cache[cache_key]
            if time.time() - cached_time < self.cache_ttl:
                logger.debug(f"Cache hit for {url}")
                return cached_result

        # Perform analysis
        try:
            result = self._do_analysis(url)
            self.cache[cache_key] = (result, time.time())
            return result
        except Exception as e:
            # If analysis fails, return stale cache if available
            if cache_key in self.cache:
                logger.warning(f"Analysis failed, returning stale cache for {url}")
                cached_result, _ = self.cache[cache_key]
                cached_result['stale'] = True
                return cached_result
            raise
```

---

## Dependency Management

### Declaring Dependencies

Declare all dependencies explicitly:

```python
from core.oracle_version_control.dependency_tracker import (
    DependencyTracker, DependencyType
)

# In agent initialization
tracker = DependencyTracker()

# Required dependency
tracker.add_dependency(
    'batman',
    'oracle',
    '>=1.0.0',
    DependencyType.REQUIRES
)

# Optional enhancement
tracker.add_dependency(
    'batman',
    'cyborg',
    '>=2.0.0',
    DependencyType.ENHANCES
)
```

### Avoiding Circular Dependencies

**Bad**: Circular dependency

```
batman → flash → batman  # ❌ Circular!
```

**Good**: Hierarchical dependency

```
oracle
  ├── batman
  └── flash
      └── batman  # ✅ No circle
```

### Version Constraints

Use appropriate version constraints:

```python
# Good: Specific constraints
'>=1.0.0,<2.0.0'  # Major version 1.x.x
'~=1.2.0'          # 1.2.x (minor lock)
'==1.2.3'          # Exact version (use sparingly)

# Bad: Too loose
'>=1.0.0'          # Any version >= 1.0.0 (risky)
'*'                # Any version (very risky)
```

---

## Performance Optimization

### Response Time Goals

| Agent | Target (p95) | Maximum (p99) |
|-------|--------------|---------------|
| Batman | 2s | 5s |
| Flash | 1s | 3s |
| Wonder Woman | 2s | 5s |
| All others | 3s | 7s |

### Optimization Techniques

#### 1. Parallel Processing

```python
import concurrent.futures

def analyze_multiple_pages(urls: List[str]) -> List[Dict]:
    """Analyze multiple pages in parallel"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(analyze, url) for url in urls]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    return results
```

#### 2. Selector Optimization

```python
# Good: Specific, fast selector
selector = '[data-testid="submit-button"]'

# Bad: Slow, fragile selector
selector = 'div > div > div > button.btn.btn-primary:nth-child(3)'
```

#### 3. Resource Cleanup

```python
def analyze(url: str) -> Dict[str, Any]:
    """Ensure resources are cleaned up"""
    browser = None
    try:
        browser = launch_browser()
        result = browser.navigate(url)
        return process_result(result)
    finally:
        if browser:
            browser.close()  # Always cleanup
```

---

## Security Best Practices

### Input Validation

Always validate inputs:

```python
import re
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """Validate URL is safe"""
    # Check format
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False
    except:
        return False

    # Check against blocklist
    if is_blocked_domain(result.netloc):
        return False

    # Check for suspicious patterns
    if re.search(r'[<>{}]', url):
        return False

    return True
```

### Secrets Management

Never hardcode secrets:

```python
# Bad: Hardcoded secret
API_KEY = "sk_live_abc123def456"

# Good: Environment variable
import os
API_KEY = os.getenv('API_KEY')

if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
```

### Rate Limiting

Implement rate limiting:

```python
from time import time, sleep

class RateLimiter:
    """Simple rate limiter"""

    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []

    def allow_request(self) -> bool:
        """Check if request is allowed"""
        now = time()

        # Remove old requests
        self.requests = [r for r in self.requests if r > now - self.time_window]

        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True

        return False

# Usage
limiter = RateLimiter(max_requests=60, time_window=60)  # 60 requests per minute

def analyze(url: str) -> Dict:
    if not limiter.allow_request():
        raise Exception("Rate limit exceeded")

    # Proceed with analysis
```

---

## Quick Reference Checklist

### Before Creating Version
- [ ] All tests passing
- [ ] Code coverage >= 80%
- [ ] Documentation updated
- [ ] No hardcoded secrets
- [ ] Performance benchmarks met
- [ ] Security scan passed

### Before Deployment
- [ ] Version created in Oracle
- [ ] Impact analysis reviewed
- [ ] Staging environment tested
- [ ] Rollback plan prepared
- [ ] Team notified
- [ ] Monitoring configured

### After Deployment
- [ ] Health metrics monitored (15 min)
- [ ] Error rates checked
- [ ] Performance validated
- [ ] User feedback reviewed
- [ ] Documentation published

---

**Oracle says**: "Excellence is not an act, but a habit. Follow these practices always." 🔮
