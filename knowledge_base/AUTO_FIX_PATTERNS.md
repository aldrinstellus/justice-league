# AUTO-FIX PATTERNS - Justice League Autonomous Error Recovery

**Version:** 1.0.0 (v1.9.3)
**Created:** 2025-10-30
**Status:** Production Ready ✅

---

## 🎯 Overview

The Justice League Auto-Fix System enables autonomous error detection, classification, and recovery without user intervention. Oracle learns from every fix outcome to continuously improve confidence scores.

---

## 🧠 Core Concepts

### Confidence-Based Decision Making

```
Error Detected
    ↓
Oracle Classifies Error
    ↓
Query Knowledge Base
    ↓
Confidence Check:
    ≥80%: AUTO-IMPLEMENT (no user prompt)
    50-79%: SUGGEST (ask user once)
    <50%: DEFER (log for manual review)
```

### Self-Learning Loop

```python
# Successful Fix
confidence_score += 0.05  # Increase by 5%
usage_stats['successful'] += 1

# Failed Fix
confidence_score -= 0.10  # Decrease by 10%
usage_stats['failed'] += 1

# Track Success Rate
success_rate = successful / total_attempts
```

---

## 📋 Pattern Library

### 1. Network Timeout Recovery

**Pattern ID:** `figma-export-retry-with-exponential-backoff`

**Problem:**
- **Symptom:** HTTPSConnectionPool timeout
- **Context:** Large PNG file downloads from Figma CDN
- **Frequency:** Intermittent (network-dependent)
- **Impact:** Partial completion (e.g., 96% - 25/26 frames)

**Solution:**
```python
# Exponential Backoff Retry
MAX_RETRIES = 5
TIMEOUT_API = 60      # Figma API metadata
TIMEOUT_CDN = 120     # Large PNG downloads
BACKOFF_FACTOR = 2.0  # 1s, 2s, 4s, 8s, 16s

def download_with_retry(url, headers, max_retries=5, timeout=120):
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return (True, response.content, None)
        except requests.exceptions.Timeout:
            wait_time = BACKOFF_FACTOR ** (attempt - 1)
            time.sleep(wait_time)
    return (False, None, "All retries exhausted")
```

**Confidence Score:** 100% (production-validated)

**Production Test Results:**
- **Before:** 25/26 frames (96% success)
- **After:** 26/26 frames (100% success)
- **Duration:** 1m 51s
- **Validation:** K-12 UI Dashboard

**Reusable For:**
- Any external API with large file downloads
- CDN downloads
- Network-dependent batch operations
- Intermittent connection issues

---

### 2. Permission Errors

**Pattern ID:** `permission-error-recovery`

**Problem:**
- **Symptom:** Permission denied, 403 Forbidden
- **Context:** API authentication or file system access
- **Auto-Fixable:** ❌ (requires manual intervention)

**Solution:**
- Check token validity
- Verify file system permissions
- Suggest token refresh or permission grant
- **Confidence:** Low (<50%) - defer to user

---

### 3. Rate Limiting

**Pattern ID:** `api-rate-limit-backoff`

**Problem:**
- **Symptom:** 429 Too Many Requests
- **Context:** API rate limiting hit
- **Auto-Fixable:** ✅

**Solution:**
```python
# Respect Retry-After header
retry_after = response.headers.get('Retry-After', 60)
time.sleep(int(retry_after))

# Exponential backoff if no header
wait_time = min(2 ** attempt, 300)  # Max 5 minutes
```

**Confidence Score:** 95% (proven pattern)

---

## 🔧 Implementation Guide

### For New Error Patterns

**Step 1: Classify the Error**
```python
def _classify_error(self, error: Dict[str, Any]) -> Dict[str, str]:
    return {
        'type': 'Network Timeout',
        'category': 'network_reliability',
        'severity': 'medium',
        'auto_fixable': True
    }
```

**Step 2: Add to Oracle Knowledge Base**
```json
{
  "error_recovery_patterns": {
    "your-pattern-name": {
      "name": "Descriptive Pattern Name",
      "pattern_type": "error_category",
      "description": "What this pattern solves",
      "problem": {
        "symptom": "Error message pattern",
        "context": "When it occurs",
        "frequency": "How often",
        "impact": "What breaks"
      },
      "solution": {
        "technique": "Recovery approach",
        "parameters": {
          "key": "value"
        },
        "implementation": {
          "file": "path/to/implementation.py",
          "function": "function_name()"
        }
      },
      "confidence_score": 1.0,
      "production_validated": true,
      "reusable_for": [
        "Use case 1",
        "Use case 2"
      ]
    }
  }
}
```

**Step 3: Create Fix Implementation**
```python
# In appropriate hero file or retry patch
def fix_your_error(error_details, mission_context):
    # Implement fix logic
    # Return success/failure
    pass
```

**Step 4: Test**
```python
# test_auto_fix_orchestrator.py
def test_your_pattern(self):
    error = {'type': 'your_error', 'message': 'error msg'}
    patterns = self.orchestrator._query_local_patterns(error)

    self.assertGreater(len(patterns), 0)
    self.assertGreaterEqual(patterns[0]['confidence'], 0.8)
```

**Step 5: Production Validate**
- Test with real error scenario
- Track success rate
- Adjust confidence based on outcomes

---

## 📊 Monitoring & Learning

### Usage Statistics

Every pattern tracks:
```json
{
  "usage_stats": {
    "total_attempts": 10,
    "successful": 9,
    "failed": 1,
    "success_rate": 0.9,
    "last_used": "2025-10-30T13:00:00Z"
  }
}
```

### Confidence Adjustment Rules

**Reinforcement (Success):**
```python
new_confidence = min(1.0, current_confidence + 0.05)
```

**Penalty (Failure):**
```python
new_confidence = max(0.0, current_confidence - 0.10)
```

**Threshold for Auto-Fix:**
```python
AUTO_FIX_THRESHOLD = 0.80  # 80%
SUGGEST_THRESHOLD = 0.50   # 50%
```

---

## 🎓 Best Practices

### DO ✅
1. **Start Conservative:** Begin with low confidence (0.5-0.7) for new patterns
2. **Track Everything:** Log all fix attempts with full context
3. **Validate Production:** Test with real scenarios before enabling auto-fix
4. **Document Thoroughly:** Include problem symptoms, solution, and reusability
5. **Set Timeouts:** Always have max retry limits and timeout values

### DON'T ❌
1. **Auto-Fix High-Risk Errors:** Authentication, permissions, data loss scenarios
2. **Infinite Retries:** Always cap retries (typically 3-5)
3. **Ignore Outcomes:** Always track and learn from results
4. **Skip Testing:** Never deploy untested patterns
5. **Overfit:** Make patterns reusable, not too specific

---

## 🔍 Troubleshooting

### Pattern Not Triggering

**Check:**
1. Error classification matches pattern type
2. Confidence score ≥ threshold
3. Pattern exists in `oracle_project_patterns.json`
4. Oracle initialized properly

### Low Success Rate

**Actions:**
1. Review fix implementation logic
2. Check if error context varies
3. Add more specific classification
4. Consider pattern splitting

### False Positives

**Actions:**
1. Tighten error matching rules
2. Add context checks
3. Increase similarity threshold
4. Add negative patterns (what NOT to match)

---

## 📚 Examples

### Example 1: Simple Timeout Fix

```python
error = {
    'type': 'timeout',
    'message': 'Read timed out after 30s',
    'context': 'Figma CDN download'
}

# Oracle finds pattern
patterns = oracle.query_error_solutions(error, min_similarity=0.8)

if patterns and patterns[0]['confidence'] >= 0.8:
    # Auto-fix
    fix = patterns[0]['solution']
    apply_fix(fix)
    retry_mission()
```

### Example 2: Multi-Step Recovery

```python
def recover_from_connection_error(error, mission):
    # Step 1: Wait for network
    time.sleep(2)

    # Step 2: Retry with exponential backoff
    for attempt in range(MAX_RETRIES):
        try:
            result = retry_operation(mission)

            # Step 3: Track success
            oracle.reinforce_solution(error, solution, success=True)
            return result

        except Exception as e:
            wait_time = 2 ** attempt
            time.sleep(wait_time)

    # Step 4: Track failure
    oracle.reinforce_solution(error, solution, success=False)
    return None
```

---

## 🚀 Future Enhancements

### Planned Features

1. **Machine Learning Prediction**
   - Predict failures before they occur
   - Suggest preventive measures
   - Pattern clustering and similarity analysis

2. **A/B Testing**
   - Test multiple fix strategies in parallel
   - Automatically choose best performer
   - Gradual rollout of new patterns

3. **Rollback System**
   - Automatic rollback on failed fixes
   - Snapshot state before fix attempt
   - Restore previous working state

4. **Fix Recommendation**
   - Proactive improvement suggestions
   - Code quality enhancements
   - Performance optimizations

---

## 📖 References

- **Auto-Fix Orchestrator:** `core/justice_league/auto_fix_orchestrator.py`
- **Oracle Auto-Fix:** `core/justice_league/oracle_meta_agent.py`
- **Superman Integration:** `core/justice_league/superman_coordinator.py`
- **Test Suite:** `test_auto_fix_orchestrator.py`
- **Save Point:** `JUSTICE_LEAGUE_SAVE_POINT_V1.9.3.md`

---

**Status:** ✅ Production Ready
**Test Coverage:** 18/18 tests passing
**Confidence:** 100% for network timeout pattern
**Last Updated:** 2025-10-30
