# JL-003 Phase 2: Export Structure Specification

**Status**: ✅ APPROVED by Aldo  
**Date**: 2025-11-03  
**Purpose**: Define exact folder structure for exporting 182 Figma files  

---

## 🎯 Export Requirements

### Per Figma File:
1. ✅ PNG export of each full page
2. ✅ Individual PNG per frame
3. ✅ One consolidated PDF with all pages
4. ✅ Metadata JSON file

### Scope:
- **182 Figma files** total
- **1,243 pages** total
- **16,389 frames** total
- **20,447 components** total

---

## 📂 Standard Export Structure

### Root Organization
```
exports/
└── figma-files/
    ├── 001-AUZMOR-MASTER-FILE-2021/
    ├── 002-AUZMOR-MOBILE-APP-2021/
    ├── 003-2022-Q1-Blended-Learning/
    ├── ... (182 folders total)
    └── 182-WorkplaceNL-For-Sales/
```

---

## 📁 Per-File Structure (Standard)

### Template:
```
[Number]-[Figma-File-Name]/
│
├── page-01-[PageName]/
│   ├── page-01-overview.png          # Full page as PNG (2x scale)
│   └── frames/
│       ├── frame-001-[FrameName].png
│       ├── frame-002-[FrameName].png
│       └── ... (all frames in this page)
│
├── page-02-[PageName]/
│   ├── page-02-overview.png          # Full page as PNG (2x scale)
│   └── frames/
│       └── ... (all frames in this page)
│
├── page-XX-[PageName]/
│   └── ... (repeat for all pages)
│
├── [FILE-NAME]-COMPLETE.pdf          # Consolidated PDF (all pages)
└── file-info.json                     # Metadata (structure details)
```

---

## 📊 Real Examples

### Example 1: Small File
**File**: "(Firefight) 2023 Q4 - Homeward Bound || Unlock Assessments"  
**Stats**: 3 pages, 2 frames, 30 components

```
001-Firefight-2023-Q4-Homeward-Bound-Unlock-Assessments/
│
├── page-01-[PageName]/
│   ├── page-01-overview.png
│   └── frames/
│       └── frame-001-[Name].png
│
├── page-02-[PageName]/
│   ├── page-02-overview.png
│   └── frames/
│       └── frame-001-[Name].png
│
├── page-03-[PageName]/
│   ├── page-03-overview.png
│   └── frames/
│       └── (no frames)
│
├── Firefight-2023-Q4-Homeward-Bound-COMPLETE.pdf
└── file-info.json
```

### Example 2: Large File
**File**: "2022 Q4 - Tasks"  
**Stats**: 30 pages, 933 frames, 845 components

```
045-2022-Q4-Tasks/
│
├── page-01-Task-Dashboard/
│   ├── page-01-overview.png
│   └── frames/
│       ├── frame-001-Dashboard-Overview.png
│       ├── frame-002-Task-List.png
│       ├── frame-003-Filter-Panel.png
│       └── ... (assume ~30 frames)
│
├── page-02-Task-Creation/
│   ├── page-02-overview.png
│   └── frames/
│       ├── frame-001-Create-Form.png
│       ├── frame-002-Assignment.png
│       └── ... (assume ~30 frames)
│
├── page-03-Task-Details/
│   ├── page-03-overview.png
│   └── frames/
│       └── ... (assume ~30 frames)
│
├── ... (pages 04-30)
│
├── 2022-Q4-Tasks-COMPLETE.pdf         # 933 frames compiled
└── file-info.json
```

### Example 3: Master File
**File**: "AUZMOR MASTER FILE 2021"  
**Stats**: 2 pages, 190 frames, 26 components

```
002-AUZMOR-MASTER-FILE-2021/
│
├── page-01-Main-Design/
│   ├── page-01-overview.png
│   └── frames/
│       ├── frame-001-Login-Screen.png
│       ├── frame-002-Dashboard-Home.png
│       ├── frame-003-User-Profile.png
│       └── ... (95 frames total)
│
├── page-02-Components/
│   ├── page-02-overview.png
│   └── frames/
│       ├── frame-001-Primary-Button.png
│       ├── frame-002-Input-Field.png
│       ├── frame-003-Dropdown.png
│       └── ... (95 frames total)
│
├── AUZMOR-MASTER-FILE-2021-COMPLETE.pdf    # 190 pages
└── file-info.json
```

---

## 🗂️ Metadata File Format

### file-info.json
```json
{
  "file_number": "002",
  "file_key": "VgYbzCNroh3XVgpk5v40AV",
  "file_name": "AUZMOR MASTER FILE 2021",
  "last_modified": "2021-12-15T10:30:00Z",
  "export_date": "2025-11-03T15:00:00Z",
  "total_pages": 2,
  "total_frames": 190,
  "total_components": 26,
  "export_cost": {
    "png": 0.48,
    "pdf": 0.57,
    "total": 1.05
  },
  "pages": [
    {
      "page_number": 1,
      "page_name": "Main Design",
      "page_id": "0:1",
      "frames_count": 95,
      "overview_file": "page-01-Main-Design/page-01-overview.png",
      "frames": [
        {
          "frame_number": 1,
          "frame_name": "Login Screen",
          "frame_id": "10:234",
          "width": 1920,
          "height": 1080,
          "file": "page-01-Main-Design/frames/frame-001-Login-Screen.png"
        },
        {
          "frame_number": 2,
          "frame_name": "Dashboard Home",
          "frame_id": "10:456",
          "width": 1920,
          "height": 1080,
          "file": "page-01-Main-Design/frames/frame-002-Dashboard-Home.png"
        }
      ]
    },
    {
      "page_number": 2,
      "page_name": "Components",
      "page_id": "0:2",
      "frames_count": 95,
      "overview_file": "page-02-Components/page-02-overview.png",
      "frames": [
        {
          "frame_number": 1,
          "frame_name": "Primary Button",
          "frame_id": "20:123",
          "width": 200,
          "height": 48,
          "file": "page-02-Components/frames/frame-001-Primary-Button.png"
        }
      ]
    }
  ],
  "consolidated_pdf": "AUZMOR-MASTER-FILE-2021-COMPLETE.pdf"
}
```

---

## 📝 Naming Conventions

### File Folders
- **Format**: `{number:03d}-{sanitized-file-name}/`
- **Example**: `002-AUZMOR-MASTER-FILE-2021/`
- **Rules**:
  - Zero-padded 3-digit number (001-182)
  - Replace spaces with hyphens
  - Remove special characters: `/ \ | : ? * " < >`
  - Max 100 characters

### Page Folders
- **Format**: `page-{number:02d}-{sanitized-page-name}/`
- **Example**: `page-01-Main-Design/`
- **Rules**:
  - Zero-padded 2-digit number (01-99)
  - Same sanitization as file names
  - Use original Figma page order

### Page Overview PNG
- **Format**: `page-{number:02d}-overview.png`
- **Example**: `page-01-overview.png`
- **Location**: Inside page folder
- **Quality**: 2x scale, PNG format

### Frame Files
- **Format**: `frame-{number:03d}-{sanitized-frame-name}.png`
- **Example**: `frame-001-Login-Screen.png`
- **Location**: `page-XX-[PageName]/frames/`
- **Rules**:
  - Zero-padded 3-digit number (001-999)
  - Sequential within each page
  - Same sanitization rules

### Consolidated PDF
- **Format**: `{FILE-NAME}-COMPLETE.pdf`
- **Example**: `AUZMOR-MASTER-FILE-2021-COMPLETE.pdf`
- **Location**: Root of file folder
- **Content**: All pages, all frames in order

### Metadata File
- **Format**: `file-info.json`
- **Location**: Root of file folder
- **Format**: JSON with complete structure info

---

## 🎨 Export Quality Settings

### PNG Files (Frames & Page Overviews)
- **Scale**: 2x (high quality)
- **Format**: PNG (lossless)
- **Color Space**: RGB
- **Background**: White (or transparent if frame design requires)
- **Compression**: PNG standard (lossless)

### PDF Files (Consolidated)
- **Quality**: High (300 DPI equivalent)
- **Compression**: Optimized for web
- **Page Size**: Auto-fit to frame dimensions
- **Color Space**: RGB
- **Format**: PDF/A (archival quality)

---

## 📊 Total Exports Generated

### Per File:
- **Page overview PNGs**: 1,243 files (one per page)
- **Frame PNGs**: 16,389 files (one per frame)
- **Consolidated PDFs**: 182 files (one per Figma file)
- **Metadata JSON**: 182 files (one per Figma file)

### Grand Total:
- **PNG files**: 17,632 files (1,243 page overviews + 16,389 frames)
- **PDF files**: 182 files
- **JSON files**: 182 files
- **Total files**: **17,996 files**

### Disk Space Estimate:
- **PNG files**: ~10-15 GB (depends on complexity)
- **PDF files**: ~3-5 GB
- **JSON files**: ~50 MB
- **Total**: **~13-20 GB**

---

## 🔢 File Numbering System

### Priority Order (001-182):
1. **Master/Reference Files** (001-010)
   - AUZMOR MASTER FILE 2021
   - AUZMOR MOBILE APP 2021
   - Sapiens Design System

2. **2025 Files** (011-054)
   - Latest product work
   - Organized by quarter

3. **2024 Files** (055-100)
   - Recent product work
   - Organized by quarter

4. **2023 Files** (101-139)
   - Previous year work
   - Organized by quarter

5. **2022 & Earlier** (140-182)
   - Legacy files
   - Archived designs

---

## 🚀 Export Process Workflow

### Step 1: Setup
```bash
# Create main export folder
mkdir -p exports/figma-files

# Set Figma token
export FIGMA_ACCESS_TOKEN='figd_aPXrH3Rqpm8sdez_nHmmXKHvZ9vcK3sOcJwvhE7s'
```

### Step 2: Per-File Export
For each of 182 files:

```python
1. Create file folder: {number}-{file-name}/
2. For each page in file:
   a. Create page folder: page-{number}-{page-name}/
   b. Export page overview: page-{number}-overview.png (2x scale)
   c. Create frames subfolder: frames/
   d. For each frame in page:
      - Export frame PNG: frame-{number}-{frame-name}.png (2x scale)
3. Generate consolidated PDF: {FILE-NAME}-COMPLETE.pdf
4. Generate metadata: file-info.json
5. Rate limit: Wait 1-2 seconds between files
```

### Step 3: Verification
```bash
# Verify structure
ls -R exports/figma-files/001-AUZMOR-MASTER-FILE-2021/

# Check counts
find exports/figma-files/ -name "*.png" | wc -l  # Should be 17,632
find exports/figma-files/ -name "*.pdf" | wc -l  # Should be 182
find exports/figma-files/ -name "*.json" | wc -l # Should be 182
```

---

## 💰 Cost Breakdown

### PNG Exports
- **Page overviews**: 1,243 pages × $0.0025 = $3.11
- **Frame PNGs**: 16,389 frames × $0.0025 = $40.97
- **Subtotal**: $44.08

### PDF Exports
- **Consolidated PDFs**: 182 files × $0.20 = $36.40
- **Or per-page method**: 1,243 pages × $0.0030 = $3.73
- **Subtotal**: $36.40 - $40.13 (depending on method)

### Total: $80.48 - $84.21
(Well within $90.14 budget)

---

## 📋 Export Checklist

### Before Starting:
- [ ] Figma API token set and verified
- [ ] Folder structure created
- [ ] Export scripts tested on sample file
- [ ] Rate limiting configured (1.2s between files)
- [ ] Disk space available (~20 GB)

### During Export:
- [ ] Monitor progress with live updates
- [ ] Log any errors or failures
- [ ] Verify file counts match expectations
- [ ] Check file sizes are reasonable

### After Completion:
- [ ] Verify total file counts
- [ ] Spot-check random files for quality
- [ ] Generate export summary report
- [ ] Update Phase 2 status in mission log

---

## 🎯 Success Criteria

### Per File:
- ✅ All pages have overview PNG
- ✅ All frames exported as individual PNG
- ✅ Consolidated PDF contains all pages
- ✅ file-info.json has complete metadata

### Overall:
- ✅ 182 file folders created
- ✅ 17,632 PNG files exported
- ✅ 182 PDF files generated
- ✅ 182 JSON metadata files created
- ✅ All within $90.14 budget
- ✅ Completed in 6 weeks

---

## 📂 Quick Navigation Examples

### Find a specific file:
```bash
ls exports/figma-files/ | grep "2024"
# Shows all 2024 files
```

### View a file's structure:
```bash
tree exports/figma-files/002-AUZMOR-MASTER-FILE-2021/
```

### Count frames in a file:
```bash
find exports/figma-files/045-2022-Q4-Tasks/*/frames/ -name "*.png" | wc -l
# Should show 933
```

### Access page overview:
```bash
open exports/figma-files/002-AUZMOR-MASTER-FILE-2021/page-01-Main-Design/page-01-overview.png
```

### View consolidated PDF:
```bash
open exports/figma-files/002-AUZMOR-MASTER-FILE-2021/AUZMOR-MASTER-FILE-2021-COMPLETE.pdf
```

---

## ✅ Approved Structure Summary

**For each of 182 Figma files:**

1. ✅ **Page Overview PNG** - Full page exported (page-XX-overview.png)
2. ✅ **Individual Frame PNGs** - Each frame as separate PNG (frames/ subfolder)
3. ✅ **Consolidated PDF** - All pages in one PDF file
4. ✅ **Metadata JSON** - Complete structure information

**Total Output**: ~18,000 files organized in clear folder hierarchy

---

**Status**: ✅ STRUCTURE APPROVED  
**Approved By**: Aldo  
**Approved Date**: 2025-11-03  
**Next Step**: Create export scripts (Phase 2A)  
**Prepared By**: Oracle (Justice League Mission Control)
