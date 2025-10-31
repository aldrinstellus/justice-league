# 💨 Quicksilver PNG Export - Quick Start Guide

## Simple Export (Recommended)

```bash
# Export from file key
python3 export_figma_png.py RSMfJWl2TkykvXWa7JRP8X

# Export from URL
python3 export_figma_png.py "https://www.figma.com/design/RSMfJWl2TkykvXWa7JRP8X/..."

# Custom output folder
python3 export_figma_png.py RSMfJWl2TkykvXWa7JRP8X --output my-export/

# High-resolution export (3x scale)
python3 export_figma_png.py RSMfJWl2TkykvXWa7JRP8X --scale 3.0
```

## Production-Tested Defaults

Quicksilver now ships with **production-tested settings** that work reliably:

- ✅ **8 concurrent workers** - Optimal parallel processing
- ✅ **60s API timeout** - Handles slow Figma API responses
- ✅ **120s CDN timeout** - Downloads large PNG files without errors
- ✅ **2.0x scale** - High-quality exports (default)

**Tested with**: 484-frame Figma file, 100% success rate

## Setup (One-Time)

1. **Set your Figma token** (get from Figma → Settings → Account):
   ```bash
   export FIGMA_ACCESS_TOKEN='figd_your_token_here'
   ```

2. **Or add to `.env` file** (recommended):
   ```bash
   cp .env.example .env
   # Edit .env and add your token
   ```

## What Gets Exported

```
figma-export-TIMESTAMP/
└── Document/
    ├── Components/           # All frames from "Components" page
    │   ├── Button_1234.png
    │   └── Card_5678.png
    ├── Student-Workflow/     # All frames from workflow pages
    └── ...
```

- **Organized by page**: Each Figma page becomes a folder
- **Unique names**: Each frame gets `{name}_{id}.png`
- **Total files**: Count matches Figma frame count

## Troubleshooting

### "Figma access token not found"
```bash
export FIGMA_ACCESS_TOKEN='figd_...'
```

### Timeout errors on huge files
Increase timeouts (rare):
```bash
export QUICKSILVER_API_TIMEOUT=90
export QUICKSILVER_CDN_TIMEOUT=180
python3 export_figma_png.py <FILE_KEY>
```

### Want faster export (smaller files only)
Reduce workers or batch size:
```bash
export QUICKSILVER_MAX_WORKERS=4
python3 export_figma_png.py <FILE_KEY>
```

## Advanced: Environment Variables

Override defaults in `.env` or export before running:

```bash
# Speed optimization (default: production-tested values)
QUICKSILVER_MAX_WORKERS=8       # Concurrent workers
QUICKSILVER_BATCH_SIZE=15       # Frames per API batch
QUICKSILVER_API_TIMEOUT=60      # API timeout (seconds)
QUICKSILVER_CDN_TIMEOUT=120     # CDN timeout (seconds)
QUICKSILVER_MAX_RETRIES=5       # Retry attempts per frame
```

## Version History

**v1.0.1** (2025-10-31)
- ✅ Updated default timeouts: 60s API / 120s CDN
- ✅ Production-tested with 484 frame files
- ✅ Simple CLI: `export_figma_png.py`
- ✅ 100% success rate on complex files

**v1.0.0** (2025-10-31)
- Initial Quicksilver release
- 8 parallel workers
- Batch API requests
