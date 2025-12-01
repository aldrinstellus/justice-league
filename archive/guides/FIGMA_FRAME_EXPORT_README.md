# Figma Frame Export Feature

## Overview

The Figma Frame Export feature allows you to automatically export all top-level frames from a Figma file as PNG images. This feature is coordinated by **Superman** and executed by **Hawkman**, with optional tracking by **Oracle**.

## Features

✅ **Automatic Frame Discovery** - Finds all top-level frames in a Figma file
✅ **Batch Export** - Exports all frames in one operation
✅ **Smart Naming** - Files named as `{frame-name}_{node-id}.png`
✅ **Configurable Scale** - Export at 1x to 4x resolution (default: 2x)
✅ **Custom Output** - Save to any directory
✅ **Oracle Tracking** - Optional metadata tracking for exports
✅ **Command-Line Interface** - Easy-to-use CLI script

## Installation

No additional installation required! The feature uses existing Justice League infrastructure:

- **Hawkman** - Frame export execution
- **Superman** - Mission coordination
- **Oracle** - Export tracking (optional)

## Usage

### Method 1: Command-Line Script (Recommended)

```bash
# Basic usage with file key
python3 scripts/export_figma_frames.py --file-key 6Pmf9gCcUccyqbCO9nN6Ts

# Using Figma URL
python3 scripts/export_figma_frames.py --url "https://www.figma.com/file/6Pmf9gCcUccyqbCO9nN6Ts/Dashboard"

# Custom output directory
python3 scripts/export_figma_frames.py \
    --file-key 6Pmf9gCcUccyqbCO9nN6Ts \
    --output exports/my-frames/

# High-resolution export (3x scale)
python3 scripts/export_figma_frames.py \
    --file-key 6Pmf9gCcUccyqbCO9nN6Ts \
    --scale 3.0

# With custom Figma token
python3 scripts/export_figma_frames.py \
    --file-key 6Pmf9gCcUccyqbCO9nN6Ts \
    --token "figd_YOUR_TOKEN_HERE"
```

### Method 2: Python API

```python
from core.justice_league import SupermanCoordinator

# Initialize Superman
superman = SupermanCoordinator()

# Configure export mission
mission = {
    'file_key': '6Pmf9gCcUccyqbCO9nN6Ts',  # Or 'figma_url'
    'output_dir': 'exports/frames',        # Optional
    'scale': 2.0                           # Optional (1.0-4.0)
}

# Deploy Hawkman for export
result = superman._deploy_hawkman_frame_export(mission)

# Check results
if result['success']:
    print(f"Exported {result['frames_exported']} frames")
    for file_info in result['exported_files']:
        print(f"  - {file_info['frame_name']}: {file_info['file_path']}")
```

### Method 3: Direct Hawkman Usage

```python
from core.justice_league.hawkman_equipped import HawkmanEquipped

# Initialize Hawkman
hawkman = HawkmanEquipped()

# Export all frames
exported_files = hawkman.export_all_frames_as_png(
    file_key='6Pmf9gCcUccyqbCO9nN6Ts',
    output_dir='exports/frames',  # Optional
    scale=2.0                     # Optional
)

# Process results
for file_info in exported_files:
    print(f"Frame: {file_info['frame_name']}")
    print(f"Path: {file_info['file_path']}")
```

## Configuration

### Figma Access Token

You need a Figma Personal Access Token to use this feature.

**Option 1: Environment Variable** (Recommended)
```bash
export FIGMA_ACCESS_TOKEN='figd_YOUR_TOKEN_HERE'
```

**Option 2: .env File**
```bash
# Add to .env file in project root
FIGMA_ACCESS_TOKEN=figd_YOUR_TOKEN_HERE
```

**Option 3: Command-Line Argument**
```bash
python3 scripts/export_figma_frames.py --token "figd_YOUR_TOKEN_HERE" --file-key ABC123
```

### Getting a Figma Token

1. Log in to [Figma](https://www.figma.com/)
2. Go to Settings → Personal Access Tokens
3. Click "Generate new token"
4. Copy the token (starts with `figd_`)

## Output Format

Exported PNG files are named using this pattern:

```
{sanitized-frame-name}_{node-id}.png
```

**Examples:**
- `Settings-billing_2:948.png`
- `Dashboard-Home_17:1440.png`
- `User-Profile_24:2186.png`

## Export Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file_key` | string | required | Figma file key (or extract from `figma_url`) |
| `figma_url` | string | optional | Full Figma file URL (alternative to `file_key`) |
| `output_dir` | string | `data/hawkman/figma_exports/` | Directory to save PNG files |
| `scale` | float | `2.0` | Export scale (1.0 = 1x, 2.0 = 2x, up to 4.0 = 4x) |

## Testing

Run the test suite to verify the pipeline works:

```bash
# Run comprehensive test
python3 test_frame_export.py
```

**Expected Output:**
```
======================================================================
✅ TEST PASSED - Frame export pipeline working correctly!
======================================================================
```

## Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│  CLI Script (scripts/export_figma_frames.py)           │
│  - Parse arguments                                      │
│  - Configure mission                                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  🦸 Superman Coordinator                                │
│  - _deploy_hawkman_frame_export(mission)               │
│  - Extract file_key from URL                            │
│  - Coordinate with Oracle (optional)                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  🦅 Hawkman Equipped                                    │
│  - export_all_frames_as_png(file_key, output_dir, scale)│
│  - Fetch Figma file structure                           │
│  - Find all top-level frames                            │
│  - Export each frame as PNG                             │
│  - Download and save files                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  🔮 Oracle Meta Agent (Optional)                        │
│  - Track export metadata                                │
│  - Log frame names and timestamps                       │
└─────────────────────────────────────────────────────────┘
```

### Method Flow

1. **Input Validation**
   - Check for Figma token
   - Extract file_key from URL if needed
   - Validate scale parameter (1.0-4.0)

2. **File Structure Fetch**
   - Call Figma REST API: `GET /v1/files/{file_key}`
   - Parse file structure JSON
   - Identify all CANVAS nodes (pages)
   - Extract FRAME nodes from each canvas

3. **Frame Export**
   - For each frame:
     - Request PNG export: `GET /v1/images/{file_key}?ids={node_id}`
     - Get temporary image URL
     - Download image
     - Save with sanitized filename

4. **Result Compilation**
   - Return list of exported files
   - Include frame names, node IDs, file paths
   - Update Oracle tracking (if available)

## File Locations

### Core Implementation
- `core/justice_league/hawkman_equipped.py` - Main export logic (lines 288-398)
- `core/justice_league/superman_coordinator.py` - Coordination (lines 838-930)

### CLI Scripts
- `scripts/export_figma_frames.py` - Command-line interface
- `test_frame_export.py` - Test suite

### Output Directories
- Default: `data/hawkman/figma_exports/`
- Custom: Configurable via `--output` or `output_dir` parameter

## Troubleshooting

### "Figma token not found"
**Solution:** Set `FIGMA_ACCESS_TOKEN` environment variable or use `--token` argument

### "Hawkman not available"
**Solution:** Ensure `HawkmanEquipped` is properly imported in `core/justice_league/__init__.py`

### "No frames found"
**Possible causes:**
- File has no top-level frames (only components or other node types)
- File key is incorrect
- Figma API returned unexpected structure

### "Failed to export frame"
**Possible causes:**
- Figma API rate limiting (retry after delay)
- Network connectivity issues
- Invalid node ID
- Insufficient permissions for file

## Performance

**Typical Export Times:**
- Small file (1-5 frames): 5-10 seconds
- Medium file (5-20 frames): 15-30 seconds
- Large file (20+ frames): 30-60+ seconds

**Factors affecting speed:**
- Number of frames
- Frame complexity
- Export scale (higher scale = larger files = slower)
- Network latency to Figma API

**Figma API Rate Limits:**
- ~100 requests per minute (may vary)
- Frame export respects rate limits automatically

## Examples

### Export Design System Frames

```bash
# Export all components from design system
python3 scripts/export_figma_frames.py \
    --url "https://www.figma.com/file/ABC123/Design-System" \
    --output design-system-exports/ \
    --scale 2.0
```

### Batch Export Multiple Files

```bash
# Create a batch script
#!/bin/bash
FILES=(
    "6Pmf9gCcUccyqbCO9nN6Ts"
    "ABC123XYZ456"
    "DEF789GHI012"
)

for FILE_KEY in "${FILES[@]}"; do
    python3 scripts/export_figma_frames.py \
        --file-key "$FILE_KEY" \
        --output "exports/$FILE_KEY/"
done
```

### High-Resolution Export

```bash
# Export at 4x resolution for print/high-DPI
python3 scripts/export_figma_frames.py \
    --file-key 6Pmf9gCcUccyqbCO9nN6Ts \
    --scale 4.0 \
    --output high-res-exports/
```

## Integration with Other Heroes

The frame export feature integrates seamlessly with other Justice League heroes:

### With Vision Analyst
```python
# Export frames first
superman = SupermanCoordinator()
result = superman._deploy_hawkman_frame_export({'file_key': 'ABC123'})

# Then analyze with Vision Analyst
from core.justice_league import vision_analyst
for file_info in result['exported_files']:
    analysis = vision_analyst.analyze_dashboard_image(
        image_path=file_info['file_path']
    )
```

### With Green Arrow
```python
# Export frames and validate
exported_files = hawkman.export_all_frames_as_png('ABC123')

# Use Green Arrow for visual validation
for file_info in exported_files:
    green_arrow.validate_screenshot(file_info['file_path'])
```

## API Reference

### `HawkmanEquipped.export_all_frames_as_png()`

```python
def export_all_frames_as_png(
    self,
    file_key: str,
    output_dir: Optional[str] = None,
    scale: float = 2.0
) -> List[Dict[str, str]]
```

**Parameters:**
- `file_key` (str): Figma file key
- `output_dir` (str, optional): Custom output directory
- `scale` (float): Export scale 1.0-4.0

**Returns:**
```python
[
    {
        'frame_name': 'Settings/billing',
        'node_id': '2:948',
        'file_path': '/path/to/Settingsbilling_2:948.png'
    },
    # ... more frames
]
```

### `SupermanCoordinator._deploy_hawkman_frame_export()`

```python
def _deploy_hawkman_frame_export(
    self,
    mission: Dict[str, Any]
) -> Optional[Dict[str, Any]]
```

**Mission Parameters:**
```python
{
    'file_key': '6Pmf9gCcUccyqbCO9nN6Ts',  # or 'figma_url'
    'output_dir': 'exports/',              # optional
    'scale': 2.0                           # optional
}
```

**Returns:**
```python
{
    'success': True,
    'hero': 'Hawkman',
    'frames_exported': 3,
    'exported_files': [...],
    'file_key': '6Pmf9gCcUccyqbCO9nN6Ts',
    'output_dir': 'exports/',
    'scale': 2.0
}
```

## Version History

- **v1.0.0** (2025-10-30)
  - Initial release
  - Superman + Hawkman coordination
  - CLI script
  - Oracle tracking integration
  - Comprehensive testing

## Contributing

To extend this feature:

1. **Add new export formats** - Modify Hawkman to support SVG, PDF, etc.
2. **Add filtering** - Export only frames matching certain patterns
3. **Add batch processing** - Process multiple Figma files
4. **Add progress tracking** - Real-time progress updates
5. **Add retry logic** - Automatic retry on API failures

## License

Part of the Justice League AI Agent System.

## Support

For issues or questions:
- Check the troubleshooting section above
- Review test output: `python3 test_frame_export.py`
- Check logs from Superman and Hawkman
- Verify Figma API token is valid and has permissions

---

**Created:** 2025-10-30
**Version:** 1.0.0
**Heroes:** Superman 🦸, Hawkman 🦅, Oracle 🔮
