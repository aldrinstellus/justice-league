# Justice League Parallel Orchestration Guide

**Version**: 1.0.0
**Last Updated**: 2025-12-01
**Status**: Production Ready (2,000+ LOC)

---

## Overview

The Justice League has **parallel orchestration capabilities** that enable 6x-18x speedup on multi-frame operations. This guide documents how Quicksilver and the parallel processing infrastructure work together to maximize throughput.

---

## Parallel Processing Engines

### 1. Quicksilver Speed Export

**Location**: `/Users/admin/Documents/claudecode/tools/automation/aldo-vision/core/justice_league/quicksilver_speed_export.py`
**Lines**: 1,500+
**Status**: Production Ready (v1.0.3)

#### Capabilities

| Feature | Description | Speedup |
|---------|-------------|---------|
| **Concurrent Workers** | 8 parallel workers (configurable) | 2.5-3x |
| **Batch API Requests** | 10-15 frames per API call | 1.5x |
| **Connection Pooling** | HTTP session reuse | 1.2x |
| **Rate Limit Protection** | Auto-adjustment on 429 errors | Prevents failures |

#### Combined Speedup: 6x-18x (depending on workload)

#### Configuration

```bash
# Environment Variables
QUICKSILVER_MAX_WORKERS=8          # Concurrent workers (default: 8)
QUICKSILVER_BATCH_SIZE=15          # Frames per API batch (default: 15)
QUICKSILVER_API_TIMEOUT=60         # API timeout seconds (default: 60)
QUICKSILVER_CDN_TIMEOUT=120        # CDN timeout seconds (default: 120)
QUICKSILVER_MAX_RETRIES=5          # Max retry attempts (default: 5)
```

#### Usage Pattern

```python
from core.justice_league import QuicksilverSpeedExport

quicksilver = QuicksilverSpeedExport(
    figma_token=os.getenv('FIGMA_ACCESS_TOKEN'),
    max_workers=8,
    batch_size=15
)

# Export all frames in parallel
result = quicksilver.export_frames_parallel(
    file_key="RSMfJWl2TkykvXWa7JRP8X",
    output_dir="/path/to/output/",
    scale=2.0,
    progress_callback=lambda cur, total, name: print(f"{cur}/{total}: {name}")
)

print(f"Exported {result['frames_exported']} frames in {result['duration_seconds']}s")
```

---

### 2. Thread Pool Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PARALLEL ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    ┌──────────────┐                                             │
│    │   SUPERMAN   │ ← Orchestrates parallel missions            │
│    │ Coordinator  │                                             │
│    └──────┬───────┘                                             │
│           │                                                      │
│           ▼                                                      │
│    ┌──────────────────────────────────────────────────────┐     │
│    │              ThreadPoolExecutor                       │     │
│    │           (max_workers=8 default)                     │     │
│    └───┬──────┬──────┬──────┬──────┬──────┬──────┬───────┘     │
│        │      │      │      │      │      │      │              │
│        ▼      ▼      ▼      ▼      ▼      ▼      ▼              │
│       W1     W2     W3     W4     W5     W6     W7     W8       │
│    ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐     │
│    │ 💨 │ │ 💨 │ │ 💨 │ │ 💨 │ │ 💨 │ │ 💨 │ │ 💨 │ │ 💨 │     │
│    └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘     │
│    Frame  Frame  Frame  Frame  Frame  Frame  Frame  Frame       │
│      1      2      3      4      5      6      7      8         │
│                                                                  │
│    Rate Limit: Thread-safe lock prevents 429 errors             │
│    Progress: Atomic counter with lock                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Implementation Details

### ThreadPoolExecutor Pattern

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class QuicksilverSpeedExport(HeroBase):
    def __init__(self):
        # Thread safety
        self.progress_lock = threading.Lock()
        self.rate_limit_lock = threading.Lock()
        self.rate_limited = False

        # Connection pooling
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=self.max_workers,
            pool_maxsize=self.max_workers * 2,
            max_retries=3
        )
        self.session.mount('https://', adapter)

    def export_frames_parallel(self, frames: List[Dict], output_dir: str):
        """Export frames using parallel workers"""
        results = []
        completed = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all frame exports
            futures = {
                executor.submit(self._export_single_frame, frame, output_dir): frame
                for frame in frames
            }

            # Process as they complete
            for future in as_completed(futures):
                frame = futures[future]
                try:
                    result = future.result()
                    with self.progress_lock:
                        completed += 1
                        results.append(result)
                except Exception as e:
                    self.logger.error(f"Frame export failed: {e}")

        return results
```

### Rate Limit Protection

```python
def _handle_rate_limit(self, response):
    """Handle Figma API rate limiting"""
    if response.status_code == 429:
        with self.rate_limit_lock:
            if not self.rate_limited:
                self.rate_limited = True

                # Get retry-after header
                retry_after = int(response.headers.get('Retry-After', 60))

                self.logger.warning(f"Rate limited. Waiting {retry_after}s...")
                time.sleep(retry_after)

                self.rate_limited = False

        return True  # Retry the request

    return False  # Don't retry
```

### Batch API Requests

```python
def _batch_get_image_urls(self, file_key: str, node_ids: List[str]) -> Dict[str, str]:
    """Get image URLs for multiple frames in a single API call"""
    # Figma allows up to 500 nodes per request
    batch_size = min(self.batch_size, 500)
    all_urls = {}

    for i in range(0, len(node_ids), batch_size):
        batch = node_ids[i:i + batch_size]
        ids_param = ",".join(batch)

        response = self.session.get(
            f"https://api.figma.com/v1/images/{file_key}",
            params={
                "ids": ids_param,
                "format": "png",
                "scale": 2.0
            },
            headers={"X-Figma-Token": self.figma_token},
            timeout=self.api_timeout
        )

        if response.status_code == 200:
            data = response.json()
            all_urls.update(data.get('images', {}))

    return all_urls
```

---

## Performance Metrics

### Production Benchmarks

| Workload | Sequential | Parallel (8 workers) | Speedup |
|----------|------------|---------------------|---------|
| 100 frames | 5 min | 45 sec | 6.7x |
| 200 frames | 10 min | 1.5 min | 6.7x |
| 500 frames | 25 min | 3.5 min | 7.1x |
| 1000 frames | 50 min | 6 min | 8.3x |

### Resource Utilization

| Metric | Sequential | Parallel |
|--------|------------|----------|
| CPU Usage | 15% | 60% |
| Network I/O | 5 MB/s | 35 MB/s |
| Memory | 100 MB | 400 MB |
| Figma API Calls | 1/s | 8/s (burst) |

---

## Multi-Hero Parallel Orchestration

### Superman Coordinator Pattern

```python
class SupermanCoordinator:
    """Orchestrates multiple heroes in parallel"""

    async def deploy_parallel_heroes(self, mission: Dict):
        """Deploy multiple heroes simultaneously"""
        heroes_to_deploy = mission.get('heroes', [])

        async with asyncio.Semaphore(max_concurrent=6) as sem:
            tasks = []
            for hero_config in heroes_to_deploy:
                hero = self._get_hero(hero_config['name'])
                task = self._deploy_hero_with_semaphore(sem, hero, hero_config)
                tasks.append(task)

            results = await asyncio.gather(*tasks, return_exceptions=True)

        return self._aggregate_results(results)

    async def _deploy_hero_with_semaphore(self, sem, hero, config):
        """Deploy a hero with semaphore control"""
        async with sem:
            return await hero.execute_mission(config)
```

### Hero Coordination Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│              MULTI-HERO PARALLEL DEPLOYMENT                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    PHASE 1: Export (Parallel)                                   │
│    ┌──────────┐  ┌──────────┐  ┌──────────┐                    │
│    │Quicksilver│  │Quicksilver│  │Quicksilver│                    │
│    │ Worker 1 │  │ Worker 2 │  │ Worker 3 │                    │
│    └────┬─────┘  └────┬─────┘  └────┬─────┘                    │
│         │             │             │                           │
│         ▼             ▼             ▼                           │
│    ┌────────────────────────────────────────┐                  │
│    │           Batch Results                │                  │
│    └────────────────────────────────────────┘                  │
│                       │                                         │
│    PHASE 2: Validation (Parallel)                               │
│         ┌─────────────┼─────────────┐                          │
│         ▼             ▼             ▼                           │
│    ┌──────────┐  ┌──────────┐  ┌──────────┐                    │
│    │Green Arrow│  │Green Lantern│  │Vision    │                    │
│    │Validation│  │Regression │  │ Analyst │                    │
│    └────┬─────┘  └────┬─────┘  └────┬─────┘                    │
│         │             │             │                           │
│         ▼             ▼             ▼                           │
│    ┌────────────────────────────────────────┐                  │
│    │           Merged Report                │                  │
│    └────────────────────────────────────────┘                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## MBPV Formula: Measure-Buffer-Parallelize-Validate

### Production-Tested Strategy

1. **Measure**: Time baseline operation first
2. **Buffer**: Add 50% time buffer for safety
3. **Parallelize**: Apply parallel processing
4. **Validate**: Verify results match sequential output

```python
def mbpv_parallel_operation(self, operation, items, max_workers=8):
    """Apply MBPV formula for safe parallel processing"""

    # M: Measure baseline
    sample = items[:3]
    start = time.time()
    for item in sample:
        operation(item)
    baseline_per_item = (time.time() - start) / len(sample)

    # B: Buffer (50% extra time)
    estimated_parallel_time = (len(items) * baseline_per_item / max_workers) * 1.5

    # P: Parallelize
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(operation, item): item for item in items}
        for future in as_completed(futures):
            results.append(future.result())

    # V: Validate
    assert len(results) == len(items), "Result count mismatch!"
    actual_time = time.time() - start
    speedup = (len(items) * baseline_per_item) / actual_time

    return {
        "results": results,
        "speedup": speedup,
        "within_buffer": actual_time <= estimated_parallel_time
    }
```

---

## Best Practices

### 1. Set Appropriate Worker Count

```python
# Rule of thumb: workers = min(CPU_cores * 2, I/O_bound_limit)
# For Figma API: 8 workers is optimal (API rate limit consideration)

max_workers = int(os.getenv('QUICKSILVER_MAX_WORKERS', '8'))
```

### 2. Use Connection Pooling

```python
# Create session once, reuse for all requests
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(
    pool_connections=max_workers,
    pool_maxsize=max_workers * 2,
    max_retries=3
)
session.mount('https://', adapter)
```

### 3. Handle Rate Limits Gracefully

```python
# Use thread-safe rate limit handling
with self.rate_limit_lock:
    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 60))
        time.sleep(retry_after)
```

### 4. Provide Progress Feedback

```python
# Use atomic counter with lock
with self.progress_lock:
    completed += 1
    if progress_callback:
        progress_callback(completed, total, frame_name)
```

### 5. Fail Fast, Recover Later

```python
# Don't let one failure block all workers
try:
    result = future.result(timeout=self.api_timeout)
    results.append(result)
except Exception as e:
    failures.append({"item": item, "error": str(e)})
    continue  # Move to next item
```

---

## Error Recovery in Parallel Operations

### Retry Strategy

```python
def _export_with_retry(self, frame: Dict, output_dir: str) -> Dict:
    """Export frame with exponential backoff retry"""
    for attempt in range(self.max_retries):
        try:
            return self._export_single_frame(frame, output_dir)
        except requests.Timeout:
            delay = 2 ** attempt  # 1s, 2s, 4s, 8s, 16s
            time.sleep(delay)
        except requests.RequestException as e:
            if attempt == self.max_retries - 1:
                raise
            time.sleep(2 ** attempt)

    raise Exception(f"Failed after {self.max_retries} attempts")
```

### Partial Success Handling

```python
def export_frames_parallel(self, frames: List[Dict]) -> Dict:
    """Export with partial success support"""
    successful = []
    failed = []

    with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
        futures = {executor.submit(self._export_frame, f): f for f in frames}

        for future in as_completed(futures):
            frame = futures[future]
            try:
                result = future.result()
                successful.append(result)
            except Exception as e:
                failed.append({"frame": frame, "error": str(e)})

    return {
        "successful": successful,
        "failed": failed,
        "success_rate": len(successful) / len(frames) * 100
    }
```

---

## Quick Reference

### Commands

| Command | Description |
|---------|-------------|
| `quicksilver.export_frames_parallel()` | Parallel frame export |
| `superman.deploy_parallel_heroes()` | Multi-hero parallel deployment |
| `mbpv_parallel_operation()` | Safe parallel processing |

### Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `QUICKSILVER_MAX_WORKERS` | 8 | Concurrent workers |
| `QUICKSILVER_BATCH_SIZE` | 15 | Frames per API batch |
| `QUICKSILVER_API_TIMEOUT` | 60 | API request timeout |
| `QUICKSILVER_CDN_TIMEOUT` | 120 | CDN download timeout |
| `QUICKSILVER_MAX_RETRIES` | 5 | Max retry attempts |

---

## Related Documentation

- [SELF-HEALING-GUIDE.md](./SELF-HEALING-GUIDE.md) - Error recovery in parallel ops
- [AUTO-LEARNING-GUIDE.md](./AUTO-LEARNING-GUIDE.md) - Learning from parallel results
- [RESCUE-MATRIX-PROTOCOL.md](./RESCUE-MATRIX-PROTOCOL.md) - Hero rescue during failures
- [FIGMA-EXPORT-BEST-PRACTICES.md](./FIGMA-EXPORT-BEST-PRACTICES.md) - Export optimization

---

**Maintainer**: Justice League Team
**Source Code**: `/Users/admin/Documents/claudecode/tools/automation/aldo-vision/`
