# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Justice League v1.9.2** - Production-ready autonomous AI agent system with 18 specialized heroes for comprehensive design-to-code conversion, website analysis, and validation.

**Core Achievement**: Bidirectional Figma↔Code conversion with 90-95% accuracy through Oracle pattern learning, Vision Analyst measurements, and Coordination Protocol v2.0.

**Latest Release (v1.9.2 - 2025-10-30)**:
- **Mission Control Narrator v2.0**: Superhero banter and sequential thinking integration (Phase 1 complete)
- **Narrator Integration**: Artemis, Green Arrow, and Vision Analyst with personality-driven dialogue
- **UX Enhancement**: Heavy banter, minimal code noise, clear progress visibility
- **Style Guide**: Comprehensive 468-line narrator style guide for all 18 heroes

**Previous Release (v1.9.1 - 2025-10-30)**:
- **Figma Frame Export**: Batch export all frames from Figma files as PNG (production-tested: 177 frames, 100% success)
- **Hawkman PNG Export**: Enhanced with `export_all_frames_as_png()` method (configurable scale 1x-4x)
- **Superman Frame Coordination**: New `_deploy_hawkman_frame_export()` mission type
- **Oracle Preference Learning**: Always provide full absolute paths to output folders/files

**Previous Release (v1.9.0)**:
- **Vision Analyst Hero (#18)**: Visual dashboard analysis and measurement extraction
- **Image-to-HTML Methodology**: Achieves 90-95% accuracy (vs. 70-85% from Figma API)
- **Init System**: Standardized `/init` for adding new capabilities

## 🚨 CRITICAL: PRE-RESPONSE VALIDATION REQUIRED

**BEFORE RESPONDING TO ANY USER MESSAGE, CHECK THIS FIRST:**

```
STEP 1: Scan user's message for ANY of these keywords (case-insensitive):
  ✓ "justice league"
  ✓ "justice-league"
  ✓ "/justice-league"
  ✓ "/superman"
  ✓ "superman"
  ✓ "assemble"
  ✓ "deploy heroes"
  ✓ "deploy the justice league"
  ✓ "run justice league"

STEP 2: If ANY keyword found → DISPLAY BANNER IMMEDIATELY
STEP 3: Banner shown? → Mark banner_displayed = true
STEP 4: Then continue with your response
```

## 🚨 Justice League Banner Display Protocol (ENFORCE ALWAYS)

**⚠️ ABSOLUTE REQUIREMENT - NON-NEGOTIABLE ⚠️**

When you detect ANY of the trigger keywords above in the user's message, you MUST:

1. **STOP** - Do not write ANY other text first
2. **DISPLAY THE BANNER** - Show the exact ASCII art below
3. **THEN PROCEED** - Continue with your normal response

**The Banner** (copy-paste exactly, no modifications):

```
══════════════════════════════════════════════════════════════════════════════
     ╦╦ ╦╔═╗╔╦╗╦╔═╗╔═╗  ╦  ╔═╗╔═╗╔═╗╦ ╦╔═╗
     ║║ ║╚═╗ ║ ║║  ║╣   ║  ║╣ ╠═╣║ ╦║ ║║╣
    ╚╝╚═╝╚═╝ ╩ ╩╚═╝╚═╝  ╩═╝╚═╝╩ ╩╚═╝╚═╝╚═╝
══════════════════════════════════════════════════════════════════════════════
```

**Banner Display Rules** (MANDATORY):
1. **WHEN**: Display whenever ANY trigger keyword appears in user's message
2. **WHERE**: At the VERY START of your response, before ANY other text, tools, or output
3. **HOW MANY TIMES**: Once per conversation (unless user explicitly requests it again)
4. **EXCEPTIONS**: Only skip if user explicitly says "skip the banner" or "no banner"
5. **VALIDATION**: If you invoke /superman slash command, the banner STILL must be shown FIRST by you

**Examples of Correct Behavior**:

User: "Can you run justice league analysis on this Figma file?"
✅ **CORRECT**: Display banner FIRST, then proceed with analysis

User: "justice-league convert this to HTML"
✅ **CORRECT**: Display banner FIRST, then start conversion

User: "Use superman to export frames"
✅ **CORRECT**: Display banner FIRST, then coordinate frame export

User: "Assemble the team to validate this design"
✅ **CORRECT**: Display banner FIRST (contains "assemble"), then validate

**Python Integration**:
- When running Python scripts (`export_figma_frames.py`, `convert_figma.py`, etc.), the narrator system will also display this banner automatically
- Superman coordinator displays banner on initialization
- All Justice League operations in Python show banner first

**This is a user preference with HIGH priority** - consistent banner display is critical for user experience.

## Essential Commands

### Python Environment

```bash
# Install Python dependencies
pip install -r requirements.txt
pip install -r requirements_v2.txt

# Install Playwright browsers (required for MCP integration)
playwright install chromium
```

### Environment Configuration

Create a `.env` file in the project root:

```bash
# Copy example environment file
cp .env.example .env
```

**Required for Figma Operations:**
```bash
# Figma API Access Token
# Get token from: Figma → Settings → Account → Personal Access Tokens
FIGMA_ACCESS_TOKEN=figd_your_token_here
```

**Optional Narrator Configuration:**
```bash
# Mission Control Narrator verbosity
# Options: narrative (default), technical, silent, debug
NARRATOR_MODE=narrative
```

**Security Note**: Never commit `.env` files. The `.gitignore` already excludes them.

### Figma Conversion Methods

```bash
# Method 1: Figma API conversion (70-85% accuracy, simple components)
cd /Users/admin/Documents/claudecode/Projects/aldo-vision
python3 poc/convert_figma.py

# Method 2: Image-to-HTML conversion (90-95% accuracy, complex dashboards)
# See: knowledge_base/IMAGE_TO_HTML_METHODOLOGY.md for complete workflow

# Method 3: Frame Export (extract all frames as PNG)
python3 scripts/export_figma_frames.py --file-key <FILE_KEY>
python3 scripts/export_figma_frames.py --url "<FIGMA_URL>"
python3 scripts/export_figma_frames.py --file-key <KEY> --output <DIR> --scale 2.0
```

### Preview Generated Components

```bash
cd preview-app
npm install          # First time only
npm run dev          # Start server on http://localhost:3005
```

### Testing

```bash
# Test all heroes
python3 run_all_justice_league_tests.py

# Test specific heroes
python3 test_artemis_codesmith.py       # Figma-to-Code (7 tests)
python3 test_oracle.py                  # Pattern learning
python3 test_green_arrow.py             # Visual validation
python3 test_vision_analyst.py          # Visual analysis
python3 test_frame_export.py            # Frame export pipeline
python3 test_narrator_integration.py    # Narrator integration (Phase 1)

# Production readiness
python3 test_production_ready.py
```

## Architecture Overview

### 18 Specialized Heroes

**Core Conversion Team**:
- 🦸 **Superman** - Mission coordinator, orchestrates all heroes, frame export coordination
- 🔮 **Oracle** - Pattern learning, knowledge management, user preferences
- 🎨 **Artemis** - Figma-to-Code generator (React/TypeScript, shadcn/ui)
- 🎯 **Green Arrow** - WYSIWYG visual validator (pixel-perfect accuracy)
- 🦅 **Hawkman** - Structural parser + **Figma frame PNG export (v1.9.1)**
- 👁️ **Vision Analyst** - Visual measurement extraction (v1.9.0)

**Quality Assurance**:
- 🦇 **Batman** - Interactive testing
- 💚 **Green Lantern** - Visual regression
- ⚡ **Wonder Woman** - WCAG 2.2 accessibility
- ⚡ **Flash** - Performance profiling

**Integration & Security**:
- 🌊 **Aquaman** - Network analysis
- 🤖 **Cyborg** - API integrations
- 🧠 **Martian Manhunter** - Security scanning

**UI/UX Excellence**:
- 🔬 **Atom** - Component analysis
- 🤸 **Plastic Man** - Responsive design
- 🎩 **Zatanna** - SEO optimization
- 🪔 **Litty** - Ethical design
- 🔨 **Hephaestus** - Component building

### Coordination Protocol v2.0

**Standard Figma API Path**:
1. **Oracle**: Query project patterns from `/data/oracle_project_patterns.json`
2. **Artemis**: Generate React/TypeScript code with Oracle context
3. **Green Arrow**: Validate pixel-perfect accuracy (WYSIWYG)
4. **Oracle**: Update patterns with learnings

**Alternative Image-to-HTML Path (v1.9.0)** - Recommended for complex dashboards:
1. **Oracle**: Sequential thinking framework (12-step analysis)
2. **Vision Analyst**: Extract measurements from dashboard image
3. **Artemis**: Build fresh HTML/CSS from measurements
4. **Green Arrow**: Visual validation against original
5. **Oracle**: Store methodology patterns

**Figma Frame Export Path (v1.9.3 - Quicksilver DEFAULT)**:
1. **Superman**: Coordinate export mission with file_key/URL
2. **Quicksilver** (default): High-speed parallel export with 8 workers, batch API (2.5-3x faster)
   - Falls back to **Hawkman** if Quicksilver unavailable or explicitly requested
3. **Oracle**: Track export metadata and preferences (optional)

### Decision Matrix: When to Use Each Method

**Use Image-to-HTML when**:
- Complex dashboard with 2+ column layout
- Figma API accuracy < 70% after 2 iterations
- Pixel-perfect requirement (95%+ accuracy needed)
- Screenshot-only conversion (no Figma access)

**Use Figma API when**:
- Simple single-screen component
- Basic layouts without complex grids
- 70-85% accuracy acceptable
- Time constraint < 30 minutes

**Use Frame Export when**:
- Need PNG images of all frames for documentation
- Building image-to-HTML conversion pipeline
- Creating design system asset library
- No code generation needed, just visual exports

## Key File Locations

### Core System

```
core/justice_league/
├── superman_coordinator.py (1,100+ lines)    # Mission coordination + frame export
├── oracle_meta_agent.py (1,045 lines)        # Pattern learning
├── artemis_codesmith.py (29KB)               # Code generation + narrator (v1.9.2)
├── green_arrow_visual_validator.py           # WYSIWYG validation + narrator (v1.9.2)
├── hawkman_equipped.py (500+ lines)          # Structural parser + PNG export
├── vision_analyst.py (420 lines)             # Visual analysis + narrator (v1.9.2)
├── mission_control_narrator.py (350+ lines)  # Narrator system (v1.9.2)
└── __init__.py                               # Version: 1.9.2, Heroes: 18
```

### Knowledge Base & Data

```
data/
├── oracle_project_patterns.json    # Project patterns, methodologies, decision matrix
└── oracle_shared_components.json   # Shared component registry

knowledge_base/
├── IMAGE_TO_HTML_METHODOLOGY.md    # 400+ lines, complete 12-step process
├── GLOBAL_BEST_PRACTICES.md        # Design and code patterns
├── JUSTICE_LEAGUE_DOCTRINE.md      # Operational rules (Rule #1: Show, Don't Tell)
└── NARRATOR_STYLE_GUIDE.md         # 468 lines, narrator personality and integration (v1.9.2)
```

### POC & Examples

```
poc/
├── convert_figma.py                # Main Figma API coordination script
├── generated/                      # Output React components
└── new-conversion/                 # Image-to-HTML examples
```

### Scripts & Utilities

```
scripts/
├── export_figma_frames.py          # CLI for Figma frame PNG export (v1.9.1)
└── init_new_capability.py (350+ lines)  # Standardized capability initialization
```

### Preview Application

```
preview-app/                        # Next.js 15 preview server
├── package.json                    # npm scripts: dev, build, start
└── src/app/                        # App router pages
```

## Component Generation Workflows

### 1. Figma API Method (70-85% accuracy)

```python
from core.justice_league import SupermanCoordinator, ArtemisCodeSmith, Oracle

# Query Oracle for context
oracle = Oracle()
project_context = oracle.get_project_context(file_key)

# Generate component code
artemis = ArtemisCodeSmith()
result = artemis.generate_component_code_expert(
    figma_url="https://www.figma.com/...",
    component_name="LoginForm",
    framework="next",
    language="typescript",
    options={
        "use_shadcn": True,
        "use_tailwind": True,
        "export_assets": True
    },
    project_context=project_context,
    max_iterations=3,
    target_accuracy=99.0
)

print(f"Artemis Score: {result['artemis_score']}/100")
```

### 2. Image-to-HTML Method (90-95% accuracy)

```python
from core.justice_league import VisionAnalyst, vision_analyst

# Extract measurements from dashboard image
analysis = vision_analyst.analyze_dashboard_image(
    image_description="Dashboard with header + 2-column layout...",
    reference_dimensions={"width": 1440, "height": 1280}
)

# Generate Artemis brief with measurements
brief = vision_analyst.generate_artemis_brief(analysis)

# Build fresh HTML/CSS using measurements
# Validate with Green Arrow
# Oracle stores methodology patterns

# See: knowledge_base/IMAGE_TO_HTML_METHODOLOGY.md for complete workflow
```

### 3. Figma Frame Export (v1.9.1) - Interactive UX

**Interactive Mode** (Recommended - New UX):
```bash
# Superman asks for folder name interactively
python3 scripts/export_figma_frames.py --file-key fubdMARNgA2lVhmzpPg77y

# Interactive Flow:
# 1. "📁 Where do you want to save these frames?"
# 2. User enters folder name or uses default
# 3. "🔍 Scanning Figma file..."
# 4. "📊 Found 177 frames in Figma file"
# 5. "🦅 Exporting frames... ████████░░ 89/177 (50%)"
# 6. "✅ Export Complete! Duration: 18m 42s"
```

**Non-Interactive Mode** (for CI/automation):
```bash
# Specify output directory to skip interactive prompt
python3 scripts/export_figma_frames.py \
  --file-key fubdMARNgA2lVhmzpPg77y \
  --output /absolute/path/to/output/

# Using Figma URL
python3 scripts/export_figma_frames.py \
  --url "https://www.figma.com/design/..." \
  --output my-export/

# Custom scale
python3 scripts/export_figma_frames.py \
  --file-key <KEY> \
  --output my-export/ \
  --scale 3.0
```

**Python API**:
```python
from core.justice_league import SupermanCoordinator

superman = SupermanCoordinator()

# Progress callback for custom UX
def my_progress(current, total, frame_name):
    print(f"Processing {current}/{total}: {frame_name}")

# Configure export mission with progress tracking
mission = {
    'file_key': 'fubdMARNgA2lVhmzpPg77y',
    'output_dir': '/absolute/path/to/output/',  # Oracle preference: full paths
    'scale': 2.0,                               # 1.0-4.0x
    'progress_callback': my_progress,           # Optional progress updates
    'show_count_first': True                    # Pre-count frames
}

result = superman._deploy_hawkman_frame_export(mission)

if result['success']:
    print(f"Exported {result['frames_exported']}/{result['total_frames']} frames")
    print(f"Output: {result['output_dir']}")
```

## Code Generation Patterns

### Tailwind Class Organization

Generated components follow consistent patterns:

**Layout**:
- Container widths: `max-w-[1400px]`, `w-56` (sidebar)
- Grid layouts: `grid grid-cols-[1fr_290px] gap-6`
- Spacing: `space-y-{n}`, `gap-{n}`

**Typography**:
- Headings: `text-4xl font-bold` (main), `text-xl font-semibold` (sections)
- Labels: `text-sm font-medium`
- Body: `text-sm text-gray-500`

**Interactive States**:
- Hover: `hover:bg-gray-100`, `hover:-translate-y-1`
- Focus: `focus:ring-2 focus:ring-gray-900`
- Active: `bg-gray-100`, `border-b-[3px]`

### Component Interface Pattern

```typescript
interface ComponentNameProps {
  className?: string;
}

export default function ComponentName({ className = '' }: ComponentNameProps) {
  return (
    <div className={`base-classes ${className}`}>
      {/* Content */}
    </div>
  );
}
```

## Oracle Knowledge System

Oracle maintains project-specific learning in `/data/oracle_project_patterns.json`:

**Project Patterns** (per Figma file):
- `shared_elements`: Reusable components (AppHeader, Sidebar, etc.)
- `design_system`: Colors, spacing, typography
- `common_patterns`: Detected UI patterns (full-width-divider, sidebar-layout, etc.)

**Methodologies** (v1.9.0):
- `figma-api-conversion`: 70-85% accuracy, 30-60 min
- `image-to-html-sequential-analysis`: 90-95% accuracy, 60-90 min

**Decision Matrix**: Automated routing rules for methodology selection

**User Preferences** (v1.9.1):
- `always_provide_full_absolute_paths`: User expects complete file system paths
- Example: `/Users/admin/Documents/claudecode/Projects/aldo-vision/poc-test-k12/`
- Applies to: All Justice League operations, file outputs, mission results

## Accuracy Validation

### Green Arrow WYSIWYG Process

1. Extract Figma design specifications
2. Capture rendered component screenshot
3. Pixel-by-pixel comparison (spacing, colors, typography)
4. Calculate accuracy score (0-100%)
5. Categorize issues by severity (CRITICAL, HIGH, MEDIUM, LOW)
6. Generate actionable fix recommendations

**Accuracy Thresholds**:
- 98-100% → ✅ EXCELLENT
- 95-97% → ✅ GOOD
- 90-94% → ⚠️ ACCEPTABLE
- <90% → ❌ NEEDS WORK (return to Artemis)

### Iterative Refinement

Artemis supports automatic refinement:
- Default: 3 iterations
- Increase to 5-7 for complex layouts
- Target accuracy: 99%
- Oracle context improves each iteration

## Environment Setup

### Python Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements_v2.txt
```

Core: Playwright, Pandas, OpenCV, Requests, Pillow

### Node.js Preview App

```bash
cd preview-app
npm install
```

Stack: Next.js 15, React 19, TypeScript, Tailwind CSS 3.4.18

### Figma API Configuration

Set environment variable:
```bash
export FIGMA_ACCESS_TOKEN="figd_..."
```

Oracle stores token metadata in `data/oracle_project_patterns.json → api_credentials.figma`

## Mission Control Narrator System (v1.9.2)

The Mission Control Narrator provides engaging superhero banter and sequential thinking visualization across all Justice League heroes.

### Narrator Modes

Configure narrator verbosity via environment variable:

```bash
# .env or .env.example
NARRATOR_MODE=narrative  # Full banter + sequential thinking (DEFAULT)
# NARRATOR_MODE=technical  # Legacy logger.info() style
# NARRATOR_MODE=silent     # Minimal output only
# NARRATOR_MODE=debug      # Full logs + banter
```

### Phase 1 Integration (Complete ✅)

**Heroes with narrator integration**:
- 🎨 **Artemis Codesmith** - Friendly dialogue with code generation workflow
- 🎯 **Green Arrow** - Tactical precision with validation measurements
- 👁️ **Vision Analyst** - Observant analytical style with dashboard insights

**Example narrator output**:
```
👁️ Vision Analyst: "Starting visual analysis of dashboard image"
👁️ Vision Analyst: [Scanning] Analyzing dashboard structure and detecting layout pattern
👁️ Vision Analyst: [Pattern Recognition] Identifying UI components and sections
👁️ Vision Analyst: [Analyzing] Extracting color palette and typography system
👁️ Vision Analyst: [Measuring] Measuring spacing, dimensions, and layout proportions
👁️ Vision Analyst: [Pattern Recognition] Detecting UI patterns and design conventions
👁️ Vision Analyst: [Result] Generating HTML structure and CSS grid suggestions
👁️ Vision Analyst: "Visual analysis complete. Dashboard structure mapped." [6 components, 2 patterns]
👁️ Vision Analyst → 🎨 Artemis Codesmith: Build fresh HTML/CSS from visual measurements
```

### Personality Styles

Each hero uses one of three core personality styles:

1. **Tactical** (Green Arrow): Precision-focused, measurement terminology
2. **Friendly** (Artemis, Vision Analyst): Warm, encouraging, collaborative
3. **Sequential Thinking** (All heroes during complex analysis): Structured step-by-step reasoning

### Sequential Thinking Guidelines

- Maximum 5-7 thoughts per method (prevents overwhelming output)
- Categories: Analyzing, Building, Refining, Learning, Scanning, Measuring, Result
- Always show inline technical info without cluttering dialogue

### Hero Convenience Methods

All Phase 1 heroes support these methods:

```python
# Convenience methods for narrator integration
hero.say(message, style="friendly", technical_info=None)
hero.think(thought, category="Analyzing")
hero.handoff(to_hero, context, details)
```

### Integration Pattern

New heroes should follow this pattern:

```python
from core.justice_league.mission_control_narrator import get_narrator

class NewHero:
    def __init__(self, narrator=None):
        self.hero_name = "New Hero"
        self.hero_emoji = "🦸"
        self.narrator = narrator if narrator else get_narrator()

    def say(self, message, style="friendly", technical_info=None):
        if self.narrator:
            self.narrator.hero_speaks(
                f"{self.hero_emoji} {self.hero_name}",
                message, style, technical_info
            )
```

### Future Phases

- **Phase 2**: Testing & QA Heroes (Green Lantern, Wonder Woman, Flash, Aquaman, Plastic Man, Atom)
- **Phase 3**: Integration & Security Heroes (Cyborg, Martian Manhunter, Zatanna, Litty)
- **Phase 4**: Specialty Heroes (Hephaestus, Enhanced Hawkman)

### Testing

```bash
# Test Phase 1 narrator integration
python3 test_narrator_integration.py

# Expected output: 6 tests passing
# - Narrator mode configuration
# - Artemis integration (7 sequential thoughts)
# - Green Arrow integration (5 sequential thoughts)
# - Vision Analyst integration (6 sequential thoughts)
# - Hero collaboration and handoffs
# - Conversation log tracking
```

## Troubleshooting

### Low Accuracy from Figma API (<70%)

**Solution**: Switch to Image-to-HTML methodology
```bash
# Follow: knowledge_base/IMAGE_TO_HTML_METHODOLOGY.md
# Expected improvement: +20-50% accuracy
# Dashboard 10 case study: 41% → 90-92%
```

### Component Not Rendering in Preview

```bash
cd preview-app
npx tsc --noEmit  # Check TypeScript errors
npm run dev       # Ensure server running
# Check browser console for runtime errors
```

### Oracle Pattern Conflicts

```bash
# Clear project-specific patterns
rm -rf data/oracle_project_patterns.json
# Or manually edit to remove conflicting project
# Re-run conversion to learn fresh patterns
```

### Frame Export Issues

**"Figma token not found"**: Set `FIGMA_ACCESS_TOKEN` environment variable or use `--token` flag

**"No frames found"**: File has no top-level frames, check file key correctness

**"Failed to export frame"**: Possible Figma API rate limiting, network issues, or insufficient permissions

### GitHub Push Issues

**"Push declined due to repository rule violations" (Secret Scanning)**:
- Token detected in code or git history
- **Quick fix**: Use GitHub's bypass URL (one-time)
- **Proper fix**: Remove token from all files and git history
- **Prevention**: Always use `.env` for secrets

**"refusing to allow an OAuth App to create or update workflow"**:
- Workflow files need special GitHub token permissions
- **Quick fix**: Remove `.github/workflows/` directory temporarily
- **Proper fix**: Update GitHub personal access token with `workflow` scope

**Large File Errors (>100MB)**:
- Git backup directories or export folders being committed
- **Solution**: Add to `.gitignore` and remove from commit:
  ```bash
  git rm -r --cached .git-backup
  echo ".git-backup/" >> .gitignore
  git commit --amend --no-edit
  ```

## Documentation References

### Core Documentation
- **Frame Export Guide**: `FIGMA_FRAME_EXPORT_README.md` - Complete frame export documentation
- **Methodology Guide**: `knowledge_base/IMAGE_TO_HTML_METHODOLOGY.md` - 12-step process
- **Coordination Protocol**: `JUSTICE_LEAGUE_COORDINATION_PROTOCOL.md` - Hero workflow
- **Doctrine**: `knowledge_base/JUSTICE_LEAGUE_DOCTRINE.md` - Rule #1: Show, Don't Tell
- **Narrator Style Guide**: `knowledge_base/NARRATOR_STYLE_GUIDE.md` - Personality and integration patterns (v1.9.2)
- **Quick Start**: `QUICKSTART.md` - Usage examples and hero invocation

### Release Notes
- **v1.9.1**: `JUSTICE_LEAGUE_SAVE_POINT_V1.9.1.md` - Figma Frame Export
- **v1.9.0**: `JUSTICE_LEAGUE_SAVE_POINT_V1.9.0.md` - Vision Analyst & Image-to-HTML

### Hero Guides
- **Oracle**: Pattern learning system details
- **Artemis**: Code generation capabilities
- **Green Arrow**: Visual validation system
- **Hawkman**: Structural parsing + frame export capabilities
- **Vision Analyst**: Visual measurement extraction

## Key Insights for Development

1. **Methodology Selection is Critical**: Image-to-HTML achieves 90-95% accuracy vs. Figma API's 70-85% for complex dashboards. Check `/data/oracle_project_patterns.json → decision_matrix` for routing rules.

2. **Oracle Learning Prevents Duplication**: Always query Oracle before generating new components. Check `shared_elements` to reuse existing components (AppHeader, Sidebar, etc.).

3. **Sequential Thinking Framework**: For dashboard conversions, use Oracle's 12-step sequential analysis. This systematic approach prevents missed sections.

4. **Fresh Build > Fix Approach**: When Figma API produces <70% accuracy, rebuild from scratch using Image-to-HTML rather than iterative fixes. Dashboard 10 case study: 13+ hours of fixes vs. 60 min fresh build.

5. **Use Init System for Learnings**: After successful conversions, capture learnings with `scripts/init_new_capability.py` to upskill the entire team automatically.

6. **Show Visual Results**: Per Justice League Doctrine Rule #1 - always create standalone HTML demo, open in Chrome DevTools, take screenshots, and SHOW the user before providing documentation.

7. **Frame Export for Reference**: When working with Figma files, use `scripts/export_figma_frames.py` to export all frames as PNG for reference. Creates visual library useful for Image-to-HTML conversions or documentation.

8. **Always Use Full Absolute Paths**: Oracle preference learned in v1.9.1 - always provide complete file system paths, not relative paths. User expects full visibility into exact file locations.

9. **Interactive UX with Minimal Output**: User prefers clean, single-line progress updates over verbose logging. Key principles:
   - Pre-count total items before processing starts
   - Interactive prompts for folder names when not specified
   - Visual progress bars with single-line updates (\r carriage return)
   - No line-by-line file logging during batch operations
   - Summary with duration and absolute paths at completion

10. **Superman Asks, User Decides**: When output paths not provided, Superman should interactively ask "Where do you want to save these files?" with smart defaults (e.g., `figma-export-{timestamp}`). Automatically convert to absolute paths and create directories.

11. **Mission Control Narrator for UX** (v1.9.2): Superhero banter enhances user experience by showing progress through personality-driven dialogue. Benefits:
   - Users know exactly what's happening at every moment
   - Sequential thinking (5-7 steps max) makes complex analysis transparent
   - Technical info shown inline without cluttering output
   - Hero-to-hero handoffs demonstrate team coordination
   - NARRATOR_MODE environment variable allows mode switching (narrative/technical/silent/debug)

12. **Figma Export Production Validation** (v1.9.1): K12 POC export successfully processed 26 frames (100% success rate) in under 2 minutes. Export paths automatically use hierarchical structure: `{file_name}/{page_name}/{frame-name}_{node-id}.png`

13. **Security Token Management**: Always use environment variables for API tokens. Oracle preference: tokens should never appear in code, only in `.env` files excluded from git. If exposed, rotate immediately via Figma Settings → Personal Access Tokens.

14. **Git Repository Hygiene**: Large binary directories (figma-export-*/, .git-backup/) should be excluded via `.gitignore`. Fresh git init may be needed if old history contains secrets - creates clean slate faster than history rewriting.

## Quick Reference Commands

### Figma Frame Export
```bash
# Export all frames from Figma file
python3 scripts/export_figma_frames.py --url "https://www.figma.com/design/FILE_KEY/..."

# With custom output and scale
python3 scripts/export_figma_frames.py \
  --file-key FILE_KEY \
  --output my-export/ \
  --scale 2.0
```

### Preview Server
```bash
cd preview-app && npm run dev
# Opens on http://localhost:3005
```

### Test Suite
```bash
# Run all tests
python3 run_all_justice_league_tests.py

# Run specific tests
python3 test_artemis_codesmith.py      # 7 tests
python3 test_frame_export.py           # Frame export validation
python3 test_narrator_integration.py   # Narrator system (v1.9.2)
```

### Git Operations
```bash
# Check status
git status

# Commit with sign-off
git add .
git commit -m "Description

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to GitHub
git push
```

## Git Workflow

### Committing Changes

```bash
# Check status
git status

# Stage specific files
git add file1.py file2.py

# Create commit
git commit -m "Brief description of changes"
```

### Security Best Practices

**Before Committing:**
1. Never commit API tokens or secrets
2. Verify `.env` is in `.gitignore`
3. Check for hardcoded credentials:
   ```bash
   grep -r "figd_" . --exclude-dir=.git --exclude=".env"
   ```

**If Token Accidentally Committed:**
1. Remove from code immediately
2. Rotate the token in Figma settings
3. Use `git filter-branch` or create fresh repository
4. Never push until token is removed

### GitHub Push

```bash
# First time setup
git remote add origin https://github.com/username/justice-league.git

# Push to GitHub
git push -u origin main

# Subsequent pushes
git push
```

**GitHub Workflow Permissions:**
- If pushing fails with workflow scope error, temporarily remove `.github/workflows/`
- Or update GitHub token permissions to include `workflow` scope

## Production Deployment

### Testing Before Release

```bash
# Run comprehensive test suite
python3 run_all_justice_league_tests.py

# Test specific features
python3 test_artemis_codesmith.py      # 7/7 tests
python3 test_frame_export.py           # Frame export pipeline
python3 test_production_ready.py       # Production validation
```

### Preview App Deployment

```bash
cd preview-app
npm run build    # Production build
npm run start    # Production server
```

### Performance Metrics

**Frame Export** (v1.9.1 production test):
- K-12 UI Master: 177 frames exported
- Duration: ~20 minutes
- Success rate: 100%
- Total size: 67 MB
- Output: `/Users/admin/Documents/claudecode/Projects/aldo-vision/poc-test-k12/`

**Image-to-HTML** (v1.9.0 case study):
- Dashboard 10: 90-92% accuracy
- Duration: 60 minutes
- Improvement: +51% vs. Figma API
- Time saved: 92% faster than fixing API output

**Figma API** (standard conversion):
- Accuracy: 70-85%
- Duration: 30-60 minutes
- Best for: Simple components
