# Phase 2 Export Scripts

**Status**: ✅ Ready for testing
**Created**: 2025-11-03
**Implements**: PHASE2-EXPORT-STRUCTURE-REVISED.md

---

## Scripts Overview

### `export_with_sections.py`

**Purpose**: Export Figma files with complete section support

**Features**:
- ✅ Complete hierarchy cascade: File → Page → Section → Frame
- ✅ Section handling: Parses SECTION nodes and their child frames
- ✅ Page overview PNGs (full page with all content)
- ✅ Section overview PNGs (if sections exist)
- ✅ Individual frame PNGs (in appropriate folders)
- ✅ Metadata JSON with complete hierarchy
- ✅ Smart folder structure (sections/ only when needed)

**Benchmark**: aldo-vision Quicksilver export scripts
**Reference**: Phase 1 `detailed_file_analysis.py` cascade logic

---

## Prerequisites

### 1. Environment Variables

```bash
# Required: Figma API token
export FIGMA_ACCESS_TOKEN='figd_aPXrH3Rqpm8sdez_nHmmXKHvZ9vcK3sOcJwvhE7s'

# Optional: Timeout settings (defaults shown)
export QUICKSILVER_API_TIMEOUT=60
export QUICKSILVER_CDN_TIMEOUT=120
```

### 2. Python Dependencies

```bash
pip install requests
```

---

## Usage

### Single File Export (Testing)

**Test on one file first before full export:**

```bash
cd /Users/admin/Documents/claudecode/justice-league-missions/missions/JL-003-auzmor-learn-web-mobile/scripts/phase2-export

# Export specific file
python3 export_with_sections.py \
  --file-key cuTXuQCQo5J5X0Xp9ifWUH \
  --file-name "(Firefight) 2023 Q4 - Homeward Bound" \
  --file-number 1 \
  --output-dir ../../test-exports/
```

**Expected output structure**:
```
test-exports/
└── 001-Firefight-2023-Q4-Homeward-Bound/
    ├── page-01-[PageName]/
    │   ├── page-01-overview.png
    │   ├── sections/                     # If sections exist
    │   │   ├── section-01-[Name]/
    │   │   │   ├── section-overview.png
    │   │   │   └── frames/
    │   │   │       └── frame-001-[Name].png
    │   │   └── ...
    │   └── frames/                       # Direct frames (not in sections)
    │       └── frame-001-[Name].png
    └── file-info.json
```

### Full Export (All 182 Files)

**⚠️ Only run after testing single file export!**

```bash
# Export all files from Phase 1 analysis
python3 export_with_sections.py \
  --all \
  --output-dir ../../exports/figma-files/
```

**This will**:
- Read Phase 1 analysis: `outputs/phase1-discovery/FINAL/phase1-files-list.json`
- Export all 182 files with section support
- Create ~20,000 PNG files
- Generate 182 metadata JSON files
- **Estimated duration**: 6-8 hours (with rate limiting)
- **Estimated cost**: $90.14 (Quicksilver pricing)

---

## Output Structure

### Per File Folder

```
[Number]-[Figma-File-Name]/
│
├── page-01-[PageName]/
│   ├── page-01-overview.png          # Full page PNG (2x scale)
│   │
│   ├── sections/                     # ⭐ Sections container (if exist)
│   │   ├── section-01-[SectionName]/
│   │   │   ├── section-overview.png  # Full section PNG
│   │   │   └── frames/
│   │   │       ├── frame-001-[FrameName].png
│   │   │       └── ...
│   │   └── section-02-[SectionName]/
│   │       └── ...
│   │
│   └── frames/                       # Direct frames (not in sections)
│       ├── frame-001-[FrameName].png
│       └── ...
│
├── page-02-[PageName]/
│   └── ... (same structure)
│
└── file-info.json                     # Complete hierarchy metadata
```

### Metadata JSON Structure

```json
{
  "file_number": "001",
  "file_key": "cuTXuQCQo5J5X0Xp9ifWUH",
  "file_name": "Firefight 2023 Q4",
  "export_date": "2025-11-03T...",
  "total_pages": 3,
  "total_frames": 33,
  "total_sections": 3,
  "pages": [
    {
      "page_number": 1,
      "page_name": "Task Dashboard",
      "page_id": "0:1",
      "total_frames": 33,
      "total_sections": 3,
      "overview_file": "page-01-Task-Dashboard/page-01-overview.png",

      "sections": [
        {
          "section_number": 1,
          "section_name": "Active Tasks",
          "section_id": "10:234",
          "frames_count": 15,
          "overview_file": "page-01-Task-Dashboard/sections/section-01-Active-Tasks/section-overview.png",
          "frames": [
            {
              "frame_number": 1,
              "frame_name": "Task Card 1",
              "frame_id": "10:456",
              "width": 400,
              "height": 200,
              "file": "page-01-Task-Dashboard/sections/section-01-Active-Tasks/frames/frame-001-Task-Card-1.png"
            }
          ]
        }
      ],

      "direct_frames": [
        {
          "frame_number": 1,
          "frame_name": "Header",
          "frame_id": "10:111",
          "width": 1920,
          "height": 100,
          "file": "page-01-Task-Dashboard/frames/frame-001-Header.png"
        }
      ]
    }
  ]
}
```

---

## Export Settings

### PNG Quality
- **Scale**: 2x (high quality)
- **Format**: PNG (lossless)
- **Background**: Transparent (preserves original)

### Rate Limiting
- **Delay**: 1.2 seconds between API calls
- **API Timeout**: 60 seconds
- **CDN Timeout**: 120 seconds

---

## Testing Checklist

### Before Full Export

- [ ] ✅ Test single file export
- [ ] ✅ Verify folder structure matches spec
- [ ] ✅ Check section handling (if test file has sections)
- [ ] ✅ Validate metadata JSON structure
- [ ] ✅ Confirm PNG quality (2x scale)
- [ ] ✅ Check file naming conventions

### During Export

- [ ] Monitor progress logs
- [ ] Check disk space (~20 GB required)
- [ ] Watch for API errors
- [ ] Verify rate limiting (no throttling errors)

### After Export

- [ ] Verify total file count (~20,000 PNG files)
- [ ] Spot-check random files for quality
- [ ] Validate metadata JSON for random files
- [ ] Check section vs. direct frame organization
- [ ] Generate export summary report

---

## Troubleshooting

### Error: "Figma access token required"
**Solution**: Set `FIGMA_ACCESS_TOKEN` environment variable

### Error: "Phase 1 analysis not found"
**Solution**: Ensure Phase 1 is complete and `outputs/phase1-discovery/FINAL/phase1-files-list.json` exists

### Error: "Failed to fetch file"
**Solution**:
- Check file key is correct
- Verify Figma token has access to file
- Check network connection

### Error: "Failed to get image URL"
**Solution**:
- Possible rate limiting (wait and retry)
- Check API timeout settings
- Verify node IDs are valid

### Slow export speed
**Expected**: 6-8 hours for 182 files with rate limiting
**Optimization**: Cannot reduce rate limit (Figma API limits)

---

## Cost Estimation

### PNG Exports
- **Page overviews**: 1,243 pages × $0.0025 = $3.11
- **Section overviews**: ~2,000 sections × $0.0025 = $5.00
- **Frame PNGs**: 16,389 frames × $0.0025 = $40.97
- **Subtotal**: ~$49.08

### PDF Exports
- **Note**: This script exports PNG only
- **PDF generation**: To be added in Phase 2B

### Total Phase 2A: ~$49.08

---

## Next Steps

### Phase 2B (Future)
1. **PDF Generation**: Add consolidated PDF per file
2. **Parallel Export**: Implement concurrent processing
3. **Resume Support**: Handle interrupted exports
4. **Progress Tracking**: Add real-time progress bar

### After Export Complete
1. Update mission log
2. Generate export summary report
3. Update expense tracking
4. Create delivery package for Aldo

---

## Script Implementation Details

### Cascade Logic

```python
for child in page.children:
    # Case 1: Child is SECTION
    if child.type == 'SECTION':
        export_section_overview(child)  # Section PNG

        for frame in child.children:
            if frame.type == 'FRAME':
                export_frame(frame, parent_path=f"sections/section-XX/frames/")

    # Case 2: Child is direct FRAME
    elif child.type == 'FRAME':
        export_frame(child, parent_path="frames/")
```

### Decision Logic

```python
# Create sections/ folder only when needed
has_sections = any(child.get('type') == 'SECTION' for child in page.children)

if has_sections:
    os.makedirs(f"page-{num}/sections")
```

---

**Status**: ✅ Script ready for testing
**Approved By**: Aldo
**Benchmark**: aldo-vision Quicksilver exports
**Reference**: PHASE2-EXPORT-STRUCTURE-REVISED.md
**Created By**: Oracle (Justice League Mission Control)
