# 🔮 Oracle Integration Guide

**Step-by-step guide to integrating Oracle with Justice League agents**

Version: 1.0.0
Last Updated: January 2025

---

## Table of Contents

1. [Introduction](#introduction)
2. [Integration Overview](#integration-overview)
3. [Step-by-Step Integration](#step-by-step-integration)
4. [Health Metrics Integration](#health-metrics-integration)
5. [Version Control Integration](#version-control-integration)
6. [Self-Healing Integration](#self-healing-integration)
7. [Testing Integration](#testing-integration)
8. [Example: Integrating Batman](#example-integrating-batman)
9. [Troubleshooting](#troubleshooting)

---

## Introduction

This guide walks through integrating existing Justice League agents with Oracle's oversight capabilities. After integration, agents will benefit from:

- Automated health monitoring
- Version control and rollback
- Self-healing capabilities
- Cross-agent learning
- Dependency management

### Prerequisites

- Existing Justice League agent implementation
- Oracle system running
- Python 3.9+
- Access to agent codebase

---

## Integration Overview

### Integration Architecture

```
Before Integration:
    Agent → Direct Execution

After Integration:
    Agent → Oracle Monitoring → Execution
      ↓
    Health Tracking
    Version Control
    Self-Healing
    Learning
```

### What Gets Added

1. **Health Metrics**: Agent exposes health metrics
2. **Version Info**: Agent reports version number
3. **Error Handling**: Enhanced error reporting
4. **Self-Healing Hooks**: Recovery mechanisms
5. **Oracle Communication**: Integration points

---

## Step-by-Step Integration

### Step 1: Add Oracle Dependencies

Update your agent's imports:

```python
# At the top of your agent's main file
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

# Oracle integration
from core.oracle_integration.superman_connector import get_superman_interface

logger = logging.getLogger(__name__)
```

### Step 2: Add Version Information

Add version constant to your agent:

```python
# In your agent's main file
AGENT_NAME = "batman"
AGENT_VERSION = "1.0.0"  # Semantic versioning
AGENT_DESCRIPTION = "Webpage analysis specialist"
```

### Step 3: Create Health Metrics Tracker

Add a health metrics class:

```python
class AgentHealthMetrics:
    """Track health metrics for this agent"""

    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_response_time = 0.0
        self.response_times = []
        self.last_error = None
        self.last_error_time = None

    def record_success(self, response_time: float):
        """Record successful request"""
        self.total_requests += 1
        self.successful_requests += 1
        self.total_response_time += response_time
        self.response_times.append(response_time)

        # Keep only last 100 response times
        if len(self.response_times) > 100:
            self.response_times.pop(0)

    def record_failure(self, error: Exception):
        """Record failed request"""
        self.total_requests += 1
        self.failed_requests += 1
        self.last_error = str(error)
        self.last_error_time = datetime.now().isoformat()

    def get_metrics(self) -> Dict[str, Any]:
        """Get current health metrics"""
        if self.total_requests == 0:
            return {
                'success_rate': 0.0,
                'error_rate': 0.0,
                'avg_response_time': 0.0,
                'total_requests': 0
            }

        return {
            'success_rate': self.successful_requests / self.total_requests,
            'error_rate': self.failed_requests / self.total_requests,
            'avg_response_time': (
                self.total_response_time / self.total_requests
                if self.total_requests > 0 else 0
            ),
            'p95_response_time': self._calculate_percentile(95),
            'p99_response_time': self._calculate_percentile(99),
            'total_requests': self.total_requests,
            'successful_requests': self.successful_requests,
            'failed_requests': self.failed_requests,
            'last_error': self.last_error,
            'last_error_time': self.last_error_time
        }

    def _calculate_percentile(self, percentile: int) -> float:
        """Calculate percentile of response times"""
        if not self.response_times:
            return 0.0

        sorted_times = sorted(self.response_times)
        index = int(len(sorted_times) * (percentile / 100))
        return sorted_times[min(index, len(sorted_times) - 1)]

# Initialize global metrics tracker
health_metrics = AgentHealthMetrics()
```

### Step 4: Update Main Analysis Function

Wrap your main function with metrics tracking:

```python
import time

def analyze(url: str, mcp_tools: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze webpage with Oracle integration.

    Args:
        url: Target URL
        mcp_tools: MCP tools for browser automation

    Returns:
        Analysis results
    """
    start_time = time.time()

    try:
        # Your existing analysis logic
        result = _do_analysis(url, mcp_tools)

        # Record success
        response_time = (time.time() - start_time) * 1000  # Convert to ms
        health_metrics.record_success(response_time)

        # Add version info to result
        result['agent_version'] = AGENT_VERSION
        result['agent_name'] = AGENT_NAME

        return result

    except Exception as e:
        # Record failure
        health_metrics.record_failure(e)

        # Log error
        logger.error(
            f"Analysis failed for {url}",
            extra={
                'agent': AGENT_NAME,
                'url': url,
                'error': str(e),
                'version': AGENT_VERSION
            }
        )

        # Return error result
        return {
            'success': False,
            'error': str(e),
            'agent_name': AGENT_NAME,
            'agent_version': AGENT_VERSION
        }

def _do_analysis(url: str, mcp_tools: Dict[str, Any]) -> Dict[str, Any]:
    """Your original analysis logic goes here"""
    # ... existing code ...
    pass
```

### Step 5: Add Health Check Endpoint

Add a function to report health:

```python
def get_health() -> Dict[str, Any]:
    """
    Get agent health status for Oracle.

    Returns:
        Health status and metrics
    """
    metrics = health_metrics.get_metrics()

    # Determine health status
    status = 'healthy'
    if metrics['success_rate'] < 0.70:
        status = 'critical'
    elif metrics['success_rate'] < 0.85:
        status = 'unhealthy'
    elif metrics['success_rate'] < 0.95:
        status = 'warning'

    return {
        'agent': AGENT_NAME,
        'version': AGENT_VERSION,
        'status': status,
        'timestamp': datetime.now().isoformat(),
        'metrics': metrics
    }
```

### Step 6: Add Oracle Registration

Register with Oracle on startup:

```python
def register_with_oracle():
    """Register this agent with Oracle"""
    try:
        connector = get_superman_interface()

        # Create initial version if needed
        versions = connector.get_agent_versions()
        if AGENT_NAME not in versions or versions[AGENT_NAME] == '0.0.0':
            connector.request_version_update(
                AGENT_NAME,
                'minor',
                'Initial Oracle integration'
            )

        logger.info(f"{AGENT_NAME} registered with Oracle")

    except Exception as e:
        logger.warning(f"Failed to register with Oracle: {e}")
        # Don't fail if Oracle is unavailable

# Call during initialization
if __name__ == '__main__':
    register_with_oracle()
```

---

## Health Metrics Integration

### Metrics to Track

Every agent should track:

```python
{
    'success_rate': float,      # 0.0 to 1.0
    'error_rate': float,        # 0.0 to 1.0
    'avg_response_time': float, # Milliseconds
    'p95_response_time': float, # 95th percentile
    'p99_response_time': float, # 99th percentile
    'total_requests': int,
    'memory_usage': float,      # Optional: 0.0 to 1.0
    'cpu_usage': float          # Optional: 0.0 to 1.0
}
```

### Advanced Metrics (Optional)

For more detailed monitoring:

```python
import psutil
import os

class AdvancedHealthMetrics(AgentHealthMetrics):
    """Health metrics with system resource tracking"""

    def get_metrics(self) -> Dict[str, Any]:
        """Get metrics including system resources"""
        base_metrics = super().get_metrics()

        # Add system metrics
        process = psutil.Process(os.getpid())

        base_metrics.update({
            'memory_usage': process.memory_percent() / 100,
            'cpu_usage': process.cpu_percent() / 100,
            'thread_count': process.num_threads(),
            'open_files': len(process.open_files())
        })

        return base_metrics
```

---

## Version Control Integration

### Semantic Versioning

Follow these rules for version numbers:

```python
# MAJOR.MINOR.PATCH

# Increment MAJOR when:
# - Breaking API changes
# - Changed function signatures
# - Removed functionality

# Increment MINOR when:
# - New features added
# - Enhanced functionality
# - New parameters with defaults

# Increment PATCH when:
# - Bug fixes
# - Performance improvements
# - Documentation updates
```

### Version Update Workflow

```python
def update_version(change_type: str, changes: str, breaking_changes: List[str] = None):
    """
    Update agent version through Oracle.

    Args:
        change_type: 'major', 'minor', or 'patch'
        changes: Description of changes
        breaking_changes: List of breaking changes (for major versions)
    """
    connector = get_superman_interface()

    version = connector.request_version_update(
        AGENT_NAME,
        change_type,
        changes,
        breaking_changes or []
    )

    # Update agent version constant
    global AGENT_VERSION
    AGENT_VERSION = version['version']

    logger.info(f"Updated {AGENT_NAME} to v{version['version']}")

    return version

# Example usage:
if __name__ == '__main__':
    # Minor version update
    update_version(
        'minor',
        'Added support for iframe analysis'
    )

    # Major version update with breaking changes
    update_version(
        'major',
        'Changed analyze() return structure',
        breaking_changes=['analyze() now returns dict with "results" key']
    )
```

---

## Self-Healing Integration

### Add Recovery Mechanisms

Implement automatic recovery:

```python
class SelfHealingAnalyzer:
    """Analyzer with self-healing capabilities"""

    def __init__(self):
        self.max_retries = 3
        self.backoff_factor = 2

    def analyze_with_recovery(self, url: str, mcp_tools: Dict) -> Dict:
        """Analyze with automatic retry and recovery"""
        for attempt in range(self.max_retries):
            try:
                return self._analyze(url, mcp_tools)

            except TimeoutError as e:
                logger.warning(f"Timeout on attempt {attempt + 1}")
                if attempt < self.max_retries - 1:
                    self._attempt_recovery()
                    time.sleep(self.backoff_factor ** attempt)
                else:
                    health_metrics.record_failure(e)
                    return self._get_fallback_result(url)

            except Exception as e:
                logger.error(f"Error on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    self._attempt_recovery()
                else:
                    health_metrics.record_failure(e)
                    raise

    def _attempt_recovery(self):
        """Attempt to recover from error"""
        logger.info("Attempting recovery...")

        # Clear any caches
        self._clear_caches()

        # Reset connections
        self._reset_connections()

        # Reload configuration
        self._reload_config()

    def _clear_caches(self):
        """Clear internal caches"""
        # Implementation depends on your agent
        pass

    def _reset_connections(self):
        """Reset any network connections"""
        # Implementation depends on your agent
        pass

    def _reload_config(self):
        """Reload configuration"""
        # Implementation depends on your agent
        pass

    def _get_fallback_result(self, url: str) -> Dict:
        """Return safe fallback result"""
        return {
            'success': False,
            'url': url,
            'error': 'analysis_failed_after_retries',
            'fallback': True,
            'agent_name': AGENT_NAME,
            'agent_version': AGENT_VERSION
        }
```

---

## Testing Integration

### Add Integration Tests

Create tests to verify Oracle integration:

```python
import pytest
from unittest.mock import Mock, patch

def test_health_metrics_tracking():
    """Test that health metrics are properly tracked"""
    metrics = AgentHealthMetrics()

    # Record some successes
    for _ in range(10):
        metrics.record_success(1000.0)  # 1 second

    # Record some failures
    for _ in range(2):
        metrics.record_failure(Exception("Test error"))

    # Get metrics
    result = metrics.get_metrics()

    assert result['total_requests'] == 12
    assert result['successful_requests'] == 10
    assert result['failed_requests'] == 2
    assert result['success_rate'] == pytest.approx(10/12)
    assert result['error_rate'] == pytest.approx(2/12)

def test_version_reporting():
    """Test that version is reported correctly"""
    result = analyze("https://example.com", mock_mcp_tools)

    assert 'agent_version' in result
    assert result['agent_version'] == AGENT_VERSION
    assert 'agent_name' in result
    assert result['agent_name'] == AGENT_NAME

def test_oracle_registration():
    """Test Oracle registration on startup"""
    with patch('your_agent.get_superman_interface') as mock_connector:
        mock_instance = Mock()
        mock_connector.return_value = mock_instance
        mock_instance.get_agent_versions.return_value = {}

        register_with_oracle()

        mock_instance.request_version_update.assert_called_once()

@pytest.mark.integration
def test_end_to_end_with_oracle():
    """Integration test with real Oracle"""
    # This test requires Oracle to be running
    from core.oracle_integration.superman_connector import get_superman_interface

    connector = get_superman_interface()

    # Perform analysis
    result = analyze("https://example.com", get_real_mcp_tools())

    # Verify Oracle received metrics
    health = connector.get_agent_health_summary()
    assert AGENT_NAME in health['agents']
```

---

## Example: Integrating Batman

Here's a complete example of integrating the Batman agent:

### Before Integration

```python
# batman/main.py (before integration)

def analyze(url, mcp_tools):
    """Analyze webpage"""
    # Navigate to page
    mcp_tools['navigate'](url)

    # Take snapshot
    snapshot = mcp_tools['take_snapshot']()

    # Analyze selectors
    selectors = analyze_selectors(snapshot)

    return {
        'url': url,
        'selectors': selectors,
        'score': calculate_score(selectors)
    }
```

### After Integration

```python
# batman/main.py (after integration)

import time
import logging
from typing import Dict, Any
from datetime import datetime
from core.oracle_integration.superman_connector import get_superman_interface

logger = logging.getLogger(__name__)

# Agent info
AGENT_NAME = "batman"
AGENT_VERSION = "1.0.0"
AGENT_DESCRIPTION = "Webpage structure and selector analysis"

# Health metrics
class BatmanHealthMetrics:
    """Track Batman's health metrics"""

    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.response_times = []

    def record_success(self, response_time: float):
        self.total_requests += 1
        self.successful_requests += 1
        self.response_times.append(response_time)
        if len(self.response_times) > 100:
            self.response_times.pop(0)

    def record_failure(self, error: Exception):
        self.total_requests += 1
        self.failed_requests += 1
        logger.error(f"Analysis failed: {error}")

    def get_metrics(self) -> Dict[str, Any]:
        if self.total_requests == 0:
            return {
                'success_rate': 0.0,
                'error_rate': 0.0,
                'avg_response_time': 0.0
            }

        return {
            'success_rate': self.successful_requests / self.total_requests,
            'error_rate': self.failed_requests / self.total_requests,
            'avg_response_time': sum(self.response_times) / len(self.response_times) if self.response_times else 0,
            'total_requests': self.total_requests
        }

health_metrics = BatmanHealthMetrics()

def analyze(url: str, mcp_tools: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze webpage with Oracle integration.

    Args:
        url: Target URL
        mcp_tools: MCP browser automation tools

    Returns:
        Analysis results with scores and recommendations
    """
    start_time = time.time()

    try:
        # Navigate to page
        mcp_tools['navigate'](url)

        # Take snapshot
        snapshot = mcp_tools['take_snapshot']()

        # Analyze selectors
        selectors = analyze_selectors(snapshot)

        # Calculate score
        score = calculate_score(selectors)

        # Record success
        response_time = (time.time() - start_time) * 1000
        health_metrics.record_success(response_time)

        # Return result with agent info
        return {
            'success': True,
            'url': url,
            'selectors': selectors,
            'score': score,
            'agent_name': AGENT_NAME,
            'agent_version': AGENT_VERSION,
            'response_time': response_time
        }

    except Exception as e:
        # Record failure
        health_metrics.record_failure(e)

        logger.error(
            f"Batman analysis failed for {url}",
            extra={
                'agent': AGENT_NAME,
                'url': url,
                'error': str(e),
                'version': AGENT_VERSION
            }
        )

        return {
            'success': False,
            'error': str(e),
            'url': url,
            'agent_name': AGENT_NAME,
            'agent_version': AGENT_VERSION
        }

def get_health() -> Dict[str, Any]:
    """Get Batman's health status"""
    metrics = health_metrics.get_metrics()

    status = 'healthy'
    if metrics['success_rate'] < 0.70:
        status = 'critical'
    elif metrics['success_rate'] < 0.85:
        status = 'unhealthy'
    elif metrics['success_rate'] < 0.95:
        status = 'warning'

    return {
        'agent': AGENT_NAME,
        'version': AGENT_VERSION,
        'status': status,
        'timestamp': datetime.now().isoformat(),
        'metrics': metrics
    }

def register_with_oracle():
    """Register Batman with Oracle on startup"""
    try:
        connector = get_superman_interface()

        # Check if version exists
        versions = connector.get_agent_versions()
        if AGENT_NAME not in versions or versions[AGENT_NAME] == '0.0.0':
            # Create initial version
            connector.request_version_update(
                AGENT_NAME,
                'minor',
                'Initial Oracle integration for Batman'
            )

        logger.info(f"Batman registered with Oracle (v{AGENT_VERSION})")

    except Exception as e:
        logger.warning(f"Failed to register with Oracle: {e}")

if __name__ == '__main__':
    # Register on startup
    register_with_oracle()

    # Example usage
    from batman.mcp_tools import get_mcp_tools
    result = analyze("https://example.com", get_mcp_tools())
    print(f"Analysis: {result}")
    print(f"Health: {get_health()}")
```

---

## Troubleshooting

### Issue: Oracle Connection Failed

**Symptoms**: Agent can't connect to Oracle

**Solutions**:
```python
# 1. Check Oracle is running
from core.oracle_integration.superman_connector import get_superman_interface

try:
    connector = get_superman_interface()
    status = connector.get_oracle_status()
    if status['oracle_online']:
        print("✅ Oracle is online")
except Exception as e:
    print(f"❌ Oracle connection failed: {e}")

# 2. Check knowledge base directory
import os
kb_dir = '/tmp/aldo-vision-justice-league/oracle'
if os.path.exists(kb_dir):
    print(f"✅ KB directory exists: {kb_dir}")
else:
    print(f"❌ KB directory missing: {kb_dir}")
    os.makedirs(kb_dir, exist_ok=True)
```

### Issue: Metrics Not Updating

**Symptoms**: Health metrics always show 0

**Solution**: Ensure metrics are being recorded:

```python
# Add debug logging
def record_success(self, response_time: float):
    print(f"DEBUG: Recording success - time: {response_time}ms")
    self.successful_requests += 1
    # ... rest of method
```

### Issue: Version Not Recognized

**Symptoms**: Oracle shows version as "0.0.0"

**Solution**: Explicitly create version:

```python
connector = get_superman_interface()
connector.request_version_update(
    AGENT_NAME,
    'minor',
    'Force version creation'
)
```

---

## Integration Checklist

Use this checklist when integrating an agent:

- [ ] Added Oracle dependencies
- [ ] Added AGENT_NAME and AGENT_VERSION constants
- [ ] Created health metrics tracker
- [ ] Updated main analysis function with metrics
- [ ] Added get_health() function
- [ ] Added register_with_oracle() function
- [ ] Added self-healing mechanisms (optional)
- [ ] Created integration tests
- [ ] Tested with Oracle running
- [ ] Documentation updated

---

**Oracle says**: "Integration complete. The agent is now under my protection." 🔮
