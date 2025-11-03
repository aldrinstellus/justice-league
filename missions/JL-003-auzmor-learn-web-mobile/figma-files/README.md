# Figma Files - Auzmor Learn Web&Mobile

**Mission**: JL-003 - Auzmor-learn - Web&Mobile
**Total Files**: 100+ Figma files
**Status**: ⏳ Awaiting Phase 1 Discovery

---

## 📁 Directory Structure

This folder will contain analysis of all Figma files from the "Auzmor - Learn - Web&Mobile" project.

### Organization Pattern

```
figma-files/
├── Q3-2025-LXP-Mobile/
│   ├── pages/
│   │   ├── 01-onboarding/
│   │   ├── 02-home-dashboard/
│   │   ├── 03-course-catalog/
│   │   └── ...
│   └── analysis.md
├── Q3-2025-Release-4-1-2-Assessment-Summary/
│   ├── pages/
│   └── analysis.md
├── Q2-2025-Product-Enhancements/
│   ├── pages/
│   └── analysis.md
└── Q1-2024-LXP-Web/
    ├── pages/
    └── analysis.md
```

---

## 📋 File Naming Convention

### Figma File Folders
- Use kebab-case: `Q3-2025-LXP-Mobile`
- Include quarter/year: `Q3-2025`, `Q2-2025`, `Q1-2024`
- Include platform if specified: `Mobile`, `Web`
- Remove special characters: `(`, `)`, `,` become `-`

**Examples**:
- `Q3 (2025) - LXP Mobile (Mobile)` → `Q3-2025-LXP-Mobile`
- `Q2 (2025) - Product Enhancements (Web)` → `Q2-2025-Product-Enhancements`
- `Q3 (2025) - Release 4.1.2 - Assessment Summary (Web)` → `Q3-2025-Release-4-1-2-Assessment-Summary`

### Page Folders
- Use numbered prefixes: `01-`, `02-`, `03-`
- Use kebab-case: `01-home-screen`, `02-course-catalog`
- Numbers ensure sorted order

---

## 📊 Analysis Template

Each Figma file folder should contain:

1. **`analysis.md`** - Summary of entire file
   - File overview (total pages, frames, components)
   - Design system analysis (colors, typography, spacing)
   - Component inventory
   - Implementation notes

2. **`pages/`** - Subfolder for all pages
   - Individual page folders (only if detailed analysis needed)
   - Most pages will be summarized in `analysis.md`

---

## 🎯 Priority Order

### Phase 1: Catalog All Files (Week 1-2)
Create folder for each file, basic `analysis.md` with metadata only

### Phase 2-6: Deep Analysis on Priority Files
Focus on:
1. **Q3 2025 files** (latest, highest priority)
2. **Q2 2025 files** (recent, high priority)
3. **Q1 2024 files** (legacy, medium priority)
4. **Earlier files** (archive, low priority unless needed)

---

## 📝 Work Process

### For Each File:

1. **Create folder**: `mkdir Q3-2025-LXP-Mobile`
2. **Create pages subfolder**: `mkdir Q3-2025-LXP-Mobile/pages`
3. **Create analysis file**: `touch Q3-2025-LXP-Mobile/analysis.md`
4. **Populate metadata**:
   - File name
   - Timeframe (quarter/year)
   - Platform (Web/Mobile)
   - Total pages (from Figma)
   - Priority level

5. **Deep analysis** (if priority file):
   - Extract design tokens (colors, typography, spacing)
   - Document all components
   - Identify patterns and styles
   - Create implementation notes

---

## 🔍 What to Track

### File-Level Metadata
- Original Figma file name
- Timeframe (quarter, year)
- Platform (Web, Mobile, Both)
- Total pages
- Total frames
- Total components (estimate)
- Last modified date (from Figma API)
- Priority level (High, Medium, Low)

### Design System Elements
- **Colors**: All color tokens, hex/rgb values, semantic naming
- **Typography**: Font families, sizes, weights, line heights
- **Spacing**: Padding, margin, gaps (spacing scale)
- **Shadows**: Elevation system
- **Borders**: Radius, stroke width
- **Icons**: Icon library

### Components
- Component name
- Category (Navigation, Forms, Content, Feedback, etc.)
- Variants (if applicable)
- States (default, hover, active, disabled, etc.)
- Platform (Web/Mobile/Both)
- Usage frequency (estimate)

---

## ⏱️ Time Estimates

### Per File
- **Catalog (metadata only)**: 5-10 minutes
- **Quick analysis**: 15-30 minutes
- **Deep analysis**: 1-2 hours (for priority files only)

### Overall
- **100+ files × 5-10 min catalog**: 8-16 hours
- **40 files × 1-2 hour deep analysis**: 40-80 hours

---

## 📈 Progress Tracking

Track in `mission-log.md`:
- Files cataloged (count)
- Files analyzed (count)
- Pages inventoried (count)
- Components identified (count)
- Design tokens extracted (count)

---

**Created**: 2025-11-03
**Last Updated**: 2025-11-03
**Status**: Ready for Phase 1 (Discovery & Cataloging)
