# Figma Export Best Practices

**Version**: 1.0.0
**Last Updated**: 2025-12-01
**Status**: Production Ready

---

## Overview

This guide documents best practices for exporting Figma designs to code using the Justice League system, based on production experience with 1000+ frames.

---

## Export Methods

### Method Comparison

| Method | Speed | Accuracy | Best For |
|--------|-------|----------|----------|
| **Quicksilver Parallel** | 3x faster | 98%+ | Large files (100+ frames) |
| **Hawkman Serial** | 1x baseline | 99%+ | Small files, reliability |
| **Image-to-HTML** | Slower | 90-95% | Complex dashboards |
| **Figma API Direct** | Fast | 70-85% | Simple components |

---

## Quick Start

### Basic Export

```bash
# Export entire Figma file as PNG
python3 export_figma_png.py <FILE_KEY>

# Export with custom options
python3 export_figma_png.py <FILE_KEY> --scale 2 --output ./my-export/
```

### From URL

```bash
# Extract file key from URL and export
python3 export_figma_png.py "https://www.figma.com/design/RSMfJWl2TkykvXWa7JRP8X/..."
```

---

## Configuration

### Environment Variables

```bash
# Required
export FIGMA_ACCESS_TOKEN="figd_your_token_here"

# Optional (Performance)
export QUICKSILVER_MAX_WORKERS=8       # Parallel workers (default: 8)
export QUICKSILVER_BATCH_SIZE=15       # Frames per API batch (default: 15)
export QUICKSILVER_API_TIMEOUT=60      # API timeout seconds (default: 60)
export QUICKSILVER_CDN_TIMEOUT=120     # CDN timeout seconds (default: 120)
export QUICKSILVER_MAX_RETRIES=5       # Max retry attempts (default: 5)
```

### Recommended Settings by File Size

| File Size | Workers | Batch Size | Timeouts |
|-----------|---------|------------|----------|
| <50 frames | 4 | 10 | Default |
| 50-200 frames | 8 | 15 | Default |
| 200-500 frames | 8 | 10 | +50% |
| >500 frames | 6 | 8 | +100% |

---

## Export Workflow

### Phase 1: Pre-Export Checks

```python
# 1. Validate file access
result = quicksilver.validate_file_access(file_key)
if not result["accessible"]:
    print(f"Error: {result['reason']}")
    return

# 2. Get frame count
frame_count = quicksilver.count_frames(file_key)
print(f"Found {frame_count} frames to export")

# 3. Estimate time and resources
estimate = quicksilver.estimate_export(file_key)
print(f"Estimated time: {estimate['duration_minutes']} minutes")
print(f"Estimated size: {estimate['size_mb']} MB")
```

### Phase 2: Export with Progress

```python
def progress_callback(current, total, frame_name):
    percent = (current / total) * 100
    print(f"\r[{'=' * int(percent/5)}{' ' * (20-int(percent/5))}] {percent:.1f}% - {frame_name}", end="")

result = quicksilver.export_frames_parallel(
    file_key=file_key,
    output_dir=output_dir,
    scale=2.0,
    progress_callback=progress_callback
)
```

### Phase 3: Post-Export Validation

```python
# Validate exports
validation = quicksilver.validate_exports(output_dir)

print(f"Total frames: {validation['total']}")
print(f"Successful: {validation['successful']}")
print(f"Failed: {validation['failed']}")

if validation['failed'] > 0:
    print("Failed frames:")
    for frame in validation['failures']:
        print(f"  - {frame['name']}: {frame['error']}")
```

---

## Output Structure

### Directory Layout

```
figma-export-{timestamp}/
├── manifest.json           # Export metadata
├── {page-name}/
│   ├── {frame-name}_{node-id}.png
│   ├── {frame-name}_{node-id}.png
│   └── ...
└── errors.json             # Any failed exports
```

### Manifest Format

```json
{
  "file_key": "RSMfJWl2TkykvXWa7JRP8X",
  "file_name": "Design System",
  "export_date": "2025-12-01T10:00:00Z",
  "total_frames": 150,
  "exported_frames": 148,
  "failed_frames": 2,
  "scale": 2.0,
  "duration_seconds": 180
}
```

---

## Handling Large Files

### Chunked Export

For files >500 frames:

```python
# Export in chunks to manage memory and rate limits
chunks = quicksilver.chunk_frames(file_key, chunk_size=100)

for i, chunk in enumerate(chunks):
    print(f"Exporting chunk {i+1}/{len(chunks)}")
    quicksilver.export_frames_parallel(
        file_key=file_key,
        frames=chunk,
        output_dir=f"{output_dir}/chunk_{i}"
    )
    time.sleep(5)  # Rate limit buffer between chunks
```

### Memory Management

```python
# Enable memory-efficient mode for very large exports
quicksilver.export_frames_parallel(
    file_key=file_key,
    output_dir=output_dir,
    memory_efficient=True,  # Writes directly to disk
    cleanup_temp=True       # Removes temp files immediately
)
```

---

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| 429 Rate Limit | Too many requests | Reduce batch size, add delays |
| Timeout | Large frame/slow network | Increase timeout, retry |
| No image URL | Frame has no visible content | Skip or check frame settings |
| Invalid token | Token expired/wrong | Regenerate Figma token |
| File not found | Wrong file key | Verify file key from URL |

### Retry Configuration

```python
# For unreliable networks
quicksilver = QuicksilverSpeedExport(
    max_retries=5,
    retry_delay=2.0,
    retry_backoff=2.0  # Exponential backoff
)
```

---

## Quality Settings

### Scale Options

| Scale | Size | Use Case |
|-------|------|----------|
| 1x | 100% | Preview, quick review |
| 2x | 200% | Production, retina displays |
| 3x | 300% | High-DPI, marketing |
| 4x | 400% | Print, maximum quality |

### Format Options

| Format | Size | Quality | Transparency |
|--------|------|---------|--------------|
| PNG | Large | Lossless | Yes |
| JPG | Small | Lossy | No |
| WebP | Small | Lossless | Yes |
| PDF | Medium | Vector | Yes |

---

## PDF Compilation

### White Background Conversion

For PDF compilation, always convert transparent PNGs:

```python
from core.justice_league import PDFCompiler

compiler = PDFCompiler()

# Convert all PNGs in directory to white background
compiler.convert_transparent_to_white(export_dir)

# Compile to PDF
compiler.compile_to_pdf(
    input_dir=export_dir,
    output_file="design-export.pdf"
)
```

### Why White Background?

- Transparent PNGs render with black borders in PDF viewers
- White background ensures consistent appearance
- Required for print and presentation use

---

## Integration with Oracle

### Track Export Statistics

```python
# Oracle automatically tracks:
# - Export success rates
# - Average export times
# - Common failure patterns
# - Optimal settings per file size

# Query recommendations
recommendations = oracle.get_export_recommendations(file_key)
print(f"Recommended workers: {recommendations['workers']}")
print(f"Recommended batch size: {recommendations['batch_size']}")
```

### Learn from Failures

```python
# After export completes
oracle.log_export_result(
    file_key=file_key,
    success_rate=validation['success_rate'],
    duration=result['duration_seconds'],
    failures=validation['failures']
)
```

---

## Automation Patterns

### Trigger Phrase Detection

The system automatically exports when detecting:

```
- "export this figma file to .png"
- "export figma to png"
- "export to .png"
```

Followed by a Figma URL or file key.

### Scheduled Exports

```python
# Export on schedule (e.g., nightly design sync)
schedule.every().day.at("02:00").do(
    quicksilver.export_frames_parallel,
    file_key=file_key,
    output_dir=f"/exports/{datetime.now().strftime('%Y-%m-%d')}"
)
```

---

## Troubleshooting

### Export Hangs

```bash
# Check for rate limiting
curl -I -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY"

# Look for: X-RateLimit-Remaining header
```

### Missing Frames

```python
# Compare exported frames with file structure
figma_frames = quicksilver.list_all_frames(file_key)
exported_frames = list(Path(export_dir).glob("**/*.png"))

missing = set(f["name"] for f in figma_frames) - set(f.stem for f in exported_frames)
print(f"Missing frames: {missing}")
```

### Quality Issues

```python
# Re-export specific frames at higher quality
quicksilver.export_frames_parallel(
    file_key=file_key,
    frames=[frame_id for frame_id in problem_frames],
    output_dir=f"{export_dir}/reexport",
    scale=4.0  # Maximum quality
)
```

---

## Performance Benchmarks

### Production Results

| File Size | Frames | Duration | Success Rate |
|-----------|--------|----------|--------------|
| Small | 26 | 2 min | 100% |
| Medium | 177 | 18 min | 99% |
| Large | 484 | 30 min | 92.6% |
| XL | 1000+ | 60 min | 90%+ |

### Optimization Tips

1. **Pre-fetch**: Warm up connection pool before large export
2. **Batch API**: Group frame URL requests (15 per call)
3. **Parallel Downloads**: 8 workers for CDN downloads
4. **Rate Limit Awareness**: Monitor and adapt to 429 responses

---

## Related Documentation

- [QUICKSILVER_README.md](../../QUICKSILVER_README.md) - Quicksilver hero details
- [PARALLEL-ORCHESTRATION-GUIDE.md](../guides/PARALLEL-ORCHESTRATION-GUIDE.md) - Parallel processing
- [SELF-HEALING-GUIDE.md](../guides/SELF-HEALING-GUIDE.md) - Error recovery

---

**Maintainer**: Justice League Team
