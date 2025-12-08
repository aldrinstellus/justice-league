# Quicksilver - High-Speed Parallel Export Specialist

**Hero**: Quicksilver 💨
**Category**: Design & Code Generation
**Specialty**: High-Speed Parallel Export Operations

---

## Overview

Quicksilver is the Justice League's speed specialist, optimized for parallel processing and high-throughput export operations. When you need to process hundreds of Figma files, export thousands of frames, or execute bulk operations at maximum velocity, Quicksilver is your hero.

---

## Core Capabilities

### 1. Parallel Export Operations
- **Multi-file Processing**: Export from multiple Figma files simultaneously
- **Concurrent Frame Export**: Process 6+ frames in parallel per file
- **Rate Limit Management**: Intelligent throttling to avoid API limits
- **Token Rotation**: Automatic switching between multiple API tokens

### 2. Speed Optimization
- **Batch Processing**: Group operations for maximum efficiency
- **Queue Management**: Priority-based task scheduling
- **Progress Tracking**: Real-time status across all parallel operations
- **Failure Recovery**: Automatic retry with exponential backoff

### 3. Scale Operations
- **100+ Files**: Handle large-scale Figma library exports
- **1000+ Frames**: Process entire design systems efficiently
- **CDN Optimization**: Smart caching and download strategies
- **Memory Management**: Stream-based processing for large exports

---

## Activation Triggers

Quicksilver activates when detecting:
- "parallel export"
- "bulk export"
- "export all frames"
- "high-speed"
- "batch process"
- "multiple files"
- "concurrent"
- "speed up export"

---

## Workflow Patterns

### Pattern 1: Multi-File Parallel Export
```bash
# Setup multiple tokens for parallel processing
export FIGMA_TOKEN_1='token_1'
export FIGMA_TOKEN_2='token_2'
export FIGMA_TOKEN_3='token_3'

# Run parallel export across files
python3 quicksilver_parallel_export.py \
  --files file1.json file2.json file3.json \
  --workers 6 \
  --output ./exports/
```

### Pattern 2: Frame Queue Processing
```python
# Quicksilver queue-based processing
async def quicksilver_export(file_keys: list, max_concurrent: int = 6):
    semaphore = asyncio.Semaphore(max_concurrent)
    tasks = []

    for file_key in file_keys:
        task = asyncio.create_task(
            export_with_semaphore(semaphore, file_key)
        )
        tasks.append(task)

    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

### Pattern 3: Token Rotation Strategy
```python
class TokenRotator:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.current_index = 0
        self.rate_limits = {token: 0 for token in tokens}

    def get_next_token(self):
        # Round-robin with rate limit awareness
        available = [t for t in self.tokens if self.rate_limits[t] < 100]
        if not available:
            time.sleep(60)  # Wait for rate limit reset
            return self.get_next_token()

        token = available[self.current_index % len(available)]
        self.current_index += 1
        return token
```

---

## Performance Benchmarks

### Export Speed (Measured)
| Operation | Single Thread | Quicksilver (6x) | Improvement |
|-----------|--------------|------------------|-------------|
| 100 frames | 25 min | 5 min | 5x faster |
| 500 frames | 2 hours | 25 min | 4.8x faster |
| 1000 frames | 4 hours | 50 min | 4.8x faster |

### Optimal Configuration
| Metric | Recommended Value |
|--------|-------------------|
| Concurrent Workers | 6 |
| Tokens Required | 3-6 |
| Batch Size | 50 frames |
| Retry Attempts | 3 |
| Timeout per Frame | 30s |

---

## Rate Limit Management

### Figma API Limits
- **Standard**: 100 requests/minute per token
- **With 6 tokens**: 600 requests/minute effective rate
- **Recommended**: 80% utilization (480 req/min) for safety margin

### Throttling Strategy
```python
RATE_LIMIT_CONFIG = {
    'requests_per_minute': 80,  # Per token
    'cooldown_on_429': 60,      # Seconds to wait
    'max_retries': 3,
    'backoff_multiplier': 2
}
```

---

## Error Handling

### Common Errors & Recovery
| Error | Cause | Quicksilver Response |
|-------|-------|---------------------|
| 429 Too Many Requests | Rate limit hit | Switch token, wait 60s |
| 500 Server Error | Figma API issue | Retry with backoff |
| Timeout | Large frame | Increase timeout, retry |
| Network Error | Connection issue | Retry up to 3 times |

### Recovery Protocol
1. **Detect failure** - Log error type and context
2. **Switch token** - Rotate to next available token
3. **Backoff** - Wait exponentially (1s, 2s, 4s)
4. **Retry** - Attempt up to 3 times
5. **Queue for later** - If all retries fail, add to retry queue

---

## Integration with Justice League

### Works With
| Hero | Integration |
|------|-------------|
| **Hawkman** 🦅 | Quicksilver exports, Hawkman parses structure |
| **Artemis** 🎨 | Quicksilver exports PNG, Artemis converts to code |
| **Oracle** 🔮 | Oracle tracks costs, Quicksilver optimizes throughput |
| **Vision Analyst** 👁️ | Vision extracts measurements from Quicksilver exports |

### Handoff Protocol
```
1. Oracle estimates cost for bulk export
2. Quicksilver executes parallel export
3. Hawkman parses exported data
4. Artemis generates code from parsed structure
5. Green Arrow validates output
```

---

## Configuration

### Environment Variables
```bash
# Required
export FIGMA_TOKEN_1='your_primary_token'

# Optional (for parallel operations)
export FIGMA_TOKEN_2='your_second_token'
export FIGMA_TOKEN_3='your_third_token'
export FIGMA_TOKEN_4='your_fourth_token'
export FIGMA_TOKEN_5='your_fifth_token'
export FIGMA_TOKEN_6='your_sixth_token'

# Quicksilver settings
export QUICKSILVER_WORKERS=6
export QUICKSILVER_TIMEOUT=30
export QUICKSILVER_RETRY_ATTEMPTS=3
```

### Python Dependencies
```
aiohttp>=3.8.0
asyncio
aiofiles
tqdm
tenacity
```

---

## Usage Examples

### Example 1: Export Entire Design System
```bash
# Quicksilver bulk export command
quicksilver export \
  --file-key "ABC123" \
  --all-frames \
  --scale 2 \
  --format png \
  --output ./design-system-export/
```

### Example 2: Multi-Project Export
```bash
# Export from multiple Figma files
quicksilver batch-export \
  --files project1.key project2.key project3.key \
  --parallel 6 \
  --resume-on-failure \
  --output ./multi-project-export/
```

### Example 3: Incremental Export
```bash
# Export only changed frames since last run
quicksilver incremental \
  --file-key "ABC123" \
  --since "2025-11-01" \
  --output ./incremental-export/
```

---

## Metrics & Monitoring

### Key Metrics
- **Throughput**: Frames per minute
- **Success Rate**: % of successful exports
- **Token Utilization**: Rate limit usage per token
- **Queue Depth**: Pending operations
- **Error Rate**: Failures per 100 operations

### Logging Format
```json
{
  "timestamp": "2025-12-01T10:30:00Z",
  "operation": "frame_export",
  "file_key": "ABC123",
  "frame_id": "1:234",
  "token_index": 2,
  "duration_ms": 1250,
  "status": "success",
  "size_bytes": 245000
}
```

---

## Best Practices

### Do's
- Use multiple tokens for parallel operations
- Implement exponential backoff on failures
- Monitor rate limit headers in responses
- Use streaming for large file downloads
- Log all operations for debugging

### Don'ts
- Don't exceed 6 concurrent workers per token
- Don't ignore rate limit warnings
- Don't retry immediately after 429 errors
- Don't process files sequentially when parallel is possible
- Don't forget to rotate tokens on rate limit

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `quicksilver export` | Single file export |
| `quicksilver batch-export` | Multi-file parallel export |
| `quicksilver incremental` | Export changed frames only |
| `quicksilver status` | Show current queue status |
| `quicksilver resume` | Resume failed operations |

---

**Last Updated**: 2025-12-01
**Version**: 1.0.0
**Maintainer**: Justice League Team

### 2025-12-03
- **useSyncExternalStore pattern**: Use useSyncExternalStore for hydration-safe client-side state in React 18+


## Design System Capabilities

- Design token extraction from Figma
- Multi-format token export automation
- Brand-specific asset generation
- Design system asset pipeline management


## Design System Tools

- Token-aware Figma export
- Automated brand asset generation
- Design system asset validation
- Multi-brand export workflows


---
**Auto-Enhanced**: 2025-12-04T12:04:27.017148
**Source**: UI Collective Design System Course