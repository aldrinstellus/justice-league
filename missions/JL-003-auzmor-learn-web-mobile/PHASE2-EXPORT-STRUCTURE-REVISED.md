# JL-003 Phase 2: Export Structure Specification (REVISED)

**Status**: ✅ UPDATED - Section handling added  
**Date**: 2025-11-03 (Revised)  
**Benchmark**: aldo-vision export scripts  

---

## 🎯 Export Requirements (Updated)

### Complete Hierarchy Cascade:
```
File
 └── Page
      ├── Page Overview PNG (full page)
      └── Content:
           ├── Direct Frames (not in sections)
           └── Sections (if exist)
                ├── Section Overview PNG
                └── Frames within section
```

### Per Figma File:
1. ✅ PNG export of each full page
2. ✅ **Section handling** - Parse sections within pages
3. ✅ Individual PNG per frame (in sections OR direct)
4. ✅ One consolidated PDF with all pages
5. ✅ Metadata JSON file with complete hierarchy

---

## 📂 Updated Export Structure

### With Sections (Recommended from Phase 1 Analysis)

```
[Number]-[Figma-File-Name]/
│
├── page-01-[PageName]/
│   ├── page-01-overview.png          # Full page PNG (2x scale)
│   │
│   ├── sections/                     # ⭐ NEW - Sections container
│   │   ├── section-01-[SectionName]/
│   │   │   ├── section-overview.png  # Full section PNG
│   │   │   └── frames/
│   │   │       ├── frame-001-[FrameName].png
│   │   │       ├── frame-002-[FrameName].png
│   │   │       └── ...
│   │   │
│   │   └── section-02-[SectionName]/
│   │       ├── section-overview.png
│   │       └── frames/
│   │           └── ...
│   │
│   └── frames/                       # Direct frames (not in sections)
│       ├── frame-001-[FrameName].png
│       └── ...
│
├── page-02-[PageName]/
│   └── ... (same structure)
│
├── [FILE-NAME]-COMPLETE.pdf          # All pages + sections + frames
└── file-info.json                     # Complete hierarchy metadata
```

### Example: Page with Sections

**Page**: "Task Dashboard"  
**Structure**:
- Section 1: "Active Tasks" (15 frames)
- Section 2: "Completed Tasks" (10 frames)
- Section 3: "Analytics" (5 frames)
- Direct frames (not in sections): 3 frames

```
045-2022-Q4-Tasks/
│
└── page-01-Task-Dashboard/
    ├── page-01-overview.png              # Full page with all sections
    │
    ├── sections/
    │   ├── section-01-Active-Tasks/
    │   │   ├── section-overview.png      # Active Tasks section only
    │   │   └── frames/
    │   │       ├── frame-001-Task-Card-1.png
    │   │       ├── frame-002-Task-Card-2.png
    │   │       └── ... (15 frames)
    │   │
    │   ├── section-02-Completed-Tasks/
    │   │   ├── section-overview.png
    │   │   └── frames/
    │   │       └── ... (10 frames)
    │   │
    │   └── section-03-Analytics/
    │       ├── section-overview.png
    │       └── frames/
    │           └── ... (5 frames)
    │
    └── frames/                           # Direct frames (not in sections)
        ├── frame-001-Header.png
        ├── frame-002-Sidebar.png
        └── frame-003-Footer.png
```

---

## 🗂️ Updated Metadata Format

### file-info.json (with sections)

```json
{
  "file_number": "045",
  "file_key": "VpwZ9n5Vkv7CZ5LVqKj9L6",
  "file_name": "2022 Q4 - Tasks",
  "last_modified": "2022-12-15T10:30:00Z",
  "export_date": "2025-11-03T15:00:00Z",
  "total_pages": 30,
  "total_frames": 933,
  "total_sections": 45,
  "total_components": 845,
  "export_cost": {
    "png": 2.33,
    "pdf": 2.80,
    "total": 5.13
  },
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
        },
        {
          "section_number": 2,
          "section_name": "Completed Tasks",
          "section_id": "10:567",
          "frames_count": 10,
          "overview_file": "page-01-Task-Dashboard/sections/section-02-Completed-Tasks/section-overview.png",
          "frames": []
        },
        {
          "section_number": 3,
          "section_name": "Analytics",
          "section_id": "10:789",
          "frames_count": 5,
          "overview_file": "page-01-Task-Dashboard/sections/section-03-Analytics/section-overview.png",
          "frames": []
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
        },
        {
          "frame_number": 2,
          "frame_name": "Sidebar",
          "frame_id": "10:222",
          "width": 280,
          "height": 1080,
          "file": "page-01-Task-Dashboard/frames/frame-002-Sidebar.png"
        }
      ]
    }
  ],
  "consolidated_pdf": "2022-Q4-Tasks-COMPLETE.pdf"
}
```

---

## 📊 Cascade Logic (from Phase 1 Analysis)

### From detailed_file_analysis.py:

```python
def _analyze_page_detailed(self, page_node):
    """Parse page → sections → frames cascade"""
    
    children = page_node.get('children', [])
    
    for child in children:
        child_type = child.get('type', '')
        
        # Direct frames (not in sections)
        if child_type == 'FRAME':
            page_info['frames'] += 1
            page_info['frame_list'].append(child)
        
        # Sections (contain frames)
        elif child_type == 'SECTION':
            page_info['sections'] += 1
            # Recursively parse frames within section
            section_frames = self._count_frames_in_node(child)
            page_info['frames'] += section_frames
```

**Key Insight**: Figma hierarchy is:
- Page → **SECTION** (optional) → FRAME
- Page → **FRAME** (direct, not in section)

We must check `child_type` and handle both cases!

---

## 🎨 Export Process (Updated)

### Step 1: Parse Figma Structure
```python
for page in file.pages:
    # Export page overview
    export_page_overview(page)
    
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

### Step 2: Folder Creation Logic
```python
# Create page folder
os.makedirs(f"page-{num}-{name}")
os.makedirs(f"page-{num}-{name}/frames")      # Direct frames
os.makedirs(f"page-{num}-{name}/sections")    # Sections container

# For each section
os.makedirs(f"page-{num}-{name}/sections/section-{num}-{name}/frames")
```

### Step 3: Export Priority
1. Page overview PNG (includes everything)
2. Section overview PNGs (if sections exist)
3. Individual frame PNGs (in section or direct)
4. Consolidated PDF (all pages + sections + frames)

---

## 📝 Naming Conventions (Updated)

### Section Folders
- **Format**: `section-{number:02d}-{sanitized-section-name}/`
- **Example**: `section-01-Active-Tasks/`
- **Location**: Inside `sections/` subfolder of page
- **Numbering**: 01, 02, 03... (original Figma order)

### Section Overview PNG
- **Format**: `section-overview.png`
- **Example**: `sections/section-01-Active-Tasks/section-overview.png`
- **Quality**: 2x scale, PNG format
- **Content**: Full section with all contained frames

### Frame Files in Sections
- **Format**: `frame-{number:03d}-{sanitized-frame-name}.png`
- **Example**: `sections/section-01-Active-Tasks/frames/frame-001-Task-Card.png`
- **Numbering**: Sequential within each section (001, 002, 003...)

### Frame Files (Direct)
- **Format**: `frame-{number:03d}-{sanitized-frame-name}.png`
- **Example**: `frames/frame-001-Header.png`
- **Location**: `page-XX/frames/` (not in sections folder)

---

## 📊 Updated Totals

### Per File:
- **Page overview PNGs**: 1,243 files (one per page)
- **Section overview PNGs**: ~2,000 files (estimated based on Phase 1 data)
- **Frame PNGs**: 16,389 files (one per frame, in sections OR direct)
- **Consolidated PDFs**: 182 files (one per Figma file)
- **Metadata JSON**: 182 files (one per Figma file)

### Grand Total:
- **PNG files**: ~19,632 files (1,243 pages + ~2,000 sections + 16,389 frames)
- **PDF files**: 182 files
- **JSON files**: 182 files
- **Total files**: **~19,996 files**

### Disk Space Estimate:
- **PNG files**: ~12-18 GB (with section overviews)
- **PDF files**: ~3-5 GB
- **JSON files**: ~50 MB
- **Total**: **~15-23 GB**

---

## 🔍 Decision Logic

### When to Create sections/ folder?
```python
has_sections = any(child.get('type') == 'SECTION' for child in page.children)

if has_sections:
    os.makedirs(f"page-{num}/sections")
    # Export sections with frames
else:
    # All frames go directly in frames/
    pass
```

### Benchmark from aldo-vision:
**Original structure**: `{file_name}/{page_name}/{frame-name}_{node-id}.png`
**Updated structure**: `{file_name}/{page_name}/sections/{section_name}/frames/{frame-name}_{node-id}.png`
**Fallback structure**: `{file_name}/{page_name}/frames/{frame-name}_{node-id}.png`

---

## ✅ Updated Success Criteria

### Per File:
- ✅ All pages have overview PNG
- ✅ **All sections have overview PNG** (if sections exist)
- ✅ All frames exported as individual PNG (in sections OR direct)
- ✅ Consolidated PDF contains all pages + sections + frames
- ✅ file-info.json has complete hierarchy (pages → sections → frames)

### Hierarchy Validation:
- ✅ Pages with sections have `sections/` folder
- ✅ Pages without sections have only `frames/` folder
- ✅ Section frames go in `sections/section-XX/frames/`
- ✅ Direct frames go in `frames/`
- ✅ Metadata JSON reflects actual structure

---

## 📋 Phase 1 Analysis Reference

From our detailed analysis:
- **Total sections detected**: Variable per file
- **Files with sections**: ~60% of files
- **Files without sections**: ~40% of files
- **Avg sections per page**: 0-3 sections

**Files known to have sections** (from Phase 1):
- 2022 Q4 - Tasks (30 pages, many sections)
- Blended Learning files (multiple sections per page)
- Social Learning files (organized by sections)

---

## 🚀 Export Script Structure

```python
def export_figma_file_with_sections(file_key, output_dir):
    """Export with section support"""
    
    # 1. Fetch file structure
    file_data = figma_api.get_file(file_key)
    
    # 2. For each page
    for page in file_data.pages:
        page_folder = create_page_folder(page)
        
        # Export page overview
        export_png(page, f"{page_folder}/page-{num}-overview.png")
        
        # 3. Parse children
        for child in page.children:
            if child.type == 'SECTION':
                # Export section
                section_folder = f"{page_folder}/sections/section-{num}-{child.name}"
                os.makedirs(f"{section_folder}/frames")
                
                # Section overview
                export_png(child, f"{section_folder}/section-overview.png")
                
                # Frames in section
                for frame in child.children:
                    if frame.type == 'FRAME':
                        export_png(frame, f"{section_folder}/frames/frame-{num}.png")
            
            elif child.type == 'FRAME':
                # Direct frame
                frames_folder = f"{page_folder}/frames"
                os.makedirs(frames_folder, exist_ok=True)
                export_png(child, f"{frames_folder}/frame-{num}.png")
        
    # 4. Generate PDF
    generate_pdf(page_folder, f"{output_dir}/{file_name}-COMPLETE.pdf")
    
    # 5. Generate metadata
    generate_metadata(file_data, f"{output_dir}/file-info.json")
```

---

## 💡 Key Learnings from Phase 1

1. **Sections are common**: ~60% of files use sections to organize frames
2. **Recursive parsing required**: Sections contain frames, must traverse tree
3. **Type checking critical**: Must check `child.type == 'SECTION'` vs `'FRAME'`
4. **Metadata completeness**: JSON must reflect actual hierarchy depth
5. **Folder structure flexibility**: Create `sections/` only when needed

---

**Status**: ✅ STRUCTURE REVISED WITH SECTION SUPPORT  
**Approved By**: Aldo  
**Benchmark**: aldo-vision export scripts  
**Phase 1 Analysis**: detailed_file_analysis.py cascade logic  
**Next**: Create export script with section parsing

---

**Key Changes from Original**:
1. ✅ Added `sections/` folder structure
2. ✅ Added section overview PNGs
3. ✅ Separate `direct_frames` vs `section_frames` in metadata
4. ✅ Cascade logic: File → Page → Section → Frame
5. ✅ Updated totals: ~20,000 files instead of ~18,000
