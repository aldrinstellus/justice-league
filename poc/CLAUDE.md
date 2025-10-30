# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Proof-of-Concept (POC) directory within the Aldo Vision Justice League system, demonstrating **Figma-to-React conversion** with 95-97% accuracy using the Coordination Protocol v2.0. The POC validates the 4-step autonomous pipeline: Oracle → Artemis → Green Arrow → Oracle.

**Parent System**: Justice League v1.7.0 - Autonomous AI agent system with 16 specialized heroes
**POC Target**: Settings/Billing page from Figma design (node-id: 2-948)
**Achievement**: Successfully converted Figma design to production-ready React component

## Architecture

### 4-Step Coordination Protocol

The POC implements Superman's Coordination Protocol v2.0:

1. **Oracle Meta Agent** - Queries project patterns and design tokens from knowledge base
2. **Artemis CodeSmith** - Generates React component code using Oracle context for consistency
3. **Green Arrow Visual Validator** - Performs WYSIWYG validation via pixel-perfect comparison
4. **Oracle Update** - Learns and stores new patterns for future component generation

### Key Components

- **`convert_figma.py`** - Main coordination script that orchestrates the 4-step pipeline
- **`generated/PocTestComponent.tsx`** - Output React component (308 lines, TypeScript)
- **Preview App** - Next.js 15 preview server located at `../preview-app/`

### Justice League Integration

This POC uses core modules from the parent system (`../core/justice_league/`):
- `superman_coordinator.py` - Overall coordination and hero deployment
- `oracle_meta_agent.py` - Pattern learning and knowledge persistence
- `artemis_codesmith.py` - Expert-level code generation with iterative refinement
- `green_arrow_visual_validator.py` - Visual accuracy validation and WYSIWYG comparison

## Development Commands

### Running the POC Conversion

```bash
# From the poc directory
python3 convert_figma.py
```

This executes the full 4-step pipeline:
- Queries Oracle for existing patterns
- Generates component code with Artemis
- Validates visually with Green Arrow (when rendered)
- Updates Oracle with learned patterns

### Preview Generated Components

```bash
# Navigate to preview app
cd ../preview-app

# Install dependencies (first time only)
npm install

# Start Next.js development server
npm run dev

# Access at http://localhost:3005/poc-test
```

### Running Justice League Tests

```bash
# From parent directory (../)
python3 run_all_justice_league_tests.py

# Test specific heroes
python3 test_artemis_codesmith.py
python3 test_oracle.py
python3 test_green_arrow.py
```

## Technical Specifications

### Generated Component Stack

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript with strict mode
- **Styling**: Tailwind CSS 3.4.18
- **Icons**: Lucide React
- **React**: 19.0.0

### Accuracy Achievements

**Final Metrics** (documented in `FINAL_ACCURACY_REPORT.md`):
- Overall accuracy: **95-97%**
- Content area accuracy: **98%+**
- Iterations: 4 refinement cycles
- Fixes applied: 17 major + 30+ minor adjustments

### Component Structure

The generated component includes:
- Top navigation header with logo, tabs, upgrade button, user avatar
- Left sidebar with settings navigation (224px width exactly)
- Main content area with forms (Card Details, Customer Details)
- Black promotional card with CTAs
- 2-column grid layouts with proper spacing
- All form data matching Figma exactly

## File Organization

```
poc/
├── convert_figma.py              # Main coordination script
├── generated/
│   ├── PocTestComponent.tsx      # Generated React component
│   └── PocTestComponent_result.json  # Full generation metadata
├── COMPONENT_STATUS_REPORT.md    # Iteration history and fixes
├── FINAL_ACCURACY_REPORT.md      # Final accuracy assessment
├── figma_design.png              # Source Figma export
├── figma_export_response.json    # Figma API response
└── rendered_*.png                # Visual validation snapshots
```

## Development Workflow

### Generating New Components

1. **Configure Target** - Update `convert_figma.py` with:
   - `figma_url` - Full Figma design URL
   - `file_key` - Extracted from URL (e.g., "6Pmf9gCcUccyqbCO9nN6Ts")
   - `node_id` - Frame/component node ID (e.g., "2-948")
   - `component_name` - Desired React component name

2. **Execute Pipeline**:
```python
python3 convert_figma.py
```

3. **Review Output**:
   - Component code: `generated/{component_name}.tsx`
   - Full result JSON: `generated/{component_name}_result.json`
   - Console output shows accuracy score and grade

4. **Preview & Validate**:
   - Create route in `../preview-app/src/app/{route-name}/page.tsx`
   - Import and render the generated component
   - Start preview server and visually compare
   - Use Green Arrow for automated pixel comparison

### Iterative Refinement

The system supports automatic iterative refinement via `max_iterations` parameter in `artemis.generate_component_code_expert()`:

```python
result = artemis.generate_component_code_expert(
    figma_url=figma_url,
    component_name=component_name,
    framework="next",
    language="typescript",
    options={
        "use_shadcn": True,
        "use_tailwind": True,
        "export_assets": True,
        "generate_tests": False,
    },
    project_context=project_context,
    max_iterations=3,      # Number of refinement cycles
    target_accuracy=99.0   # Target accuracy percentage
)
```

## Key Patterns and Conventions

### Tailwind Class Organization

Generated components follow consistent patterns:

**Layout**:
- Container widths: `w-56` (sidebar), `max-w-[1400px]` (content)
- Spacing: `space-y-{n}`, `gap-{n}` for consistent vertical/grid spacing
- Flexbox: `flex`, `items-center`, `justify-between`

**Typography**:
- Headers: `text-4xl font-bold` (main), `text-xl font-semibold` (sections)
- Labels: `text-sm font-medium`
- Body: `text-sm text-gray-500`

**Interactive States**:
- Hover: `hover:bg-gray-100`, `hover:bg-gray-800`
- Focus: `focus:outline-none`, `focus:ring-2`, `focus:ring-gray-900`
- Active: `bg-gray-100` (navigation), `border-b-[3px]` (tabs)

### Component Interface Pattern

```typescript
interface {ComponentName}Props {
  className?: string;
}

export default function {ComponentName}({ className = '' }: {ComponentName}Props) {
  return (
    <div className={`base-classes ${className}`}>
      {/* Component content */}
    </div>
  );
}
```

## Oracle Knowledge Base

Oracle maintains learned patterns in `../knowledge_base/`:
- `patterns/` - Reusable UI patterns across components
- `shared_components/` - Common components (headers, sidebars, forms)
- `design_tokens/` - Colors, spacing, typography scales
- `projects/` - Project-specific pattern collections

When generating components, Oracle provides context to ensure:
- Consistent styling across components in same project
- Reuse of established patterns
- Proper design token usage
- Compliance with project conventions

## Accuracy Validation

### Visual Comparison Process

Green Arrow performs WYSIWYG validation by:
1. Capturing screenshot of Figma design export
2. Capturing screenshot of rendered React component
3. Pixel-by-pixel comparison with tolerance thresholds
4. Identifying layout, spacing, typography, and color discrepancies
5. Categorizing issues by severity (CRITICAL, HIGH, MEDIUM, LOW)
6. Generating actionable fix recommendations

### Iteration History (Current POC)

- **Iteration 1**: Initial generation (~70% accuracy, wrong design)
- **Iteration 2**: Vision Agent analysis (47 discrepancies identified, ~85% accuracy)
- **Iteration 3**: Header addition and critical fixes (~92% accuracy)
- **Iteration 4**: Final polish and micro-adjustments (**95-97% accuracy**)

## Environment Setup

### Prerequisites

**Python Dependencies** (from parent `requirements.txt`):
```bash
pip install -r ../requirements.txt
```

Core packages:
- Playwright (browser automation)
- Pandas (data processing)
- OpenCV (image comparison)
- Requests (Figma API)

**Node.js Dependencies** (for preview app):
```bash
cd ../preview-app
npm install
```

### Figma API Configuration

Set environment variables (if using Figma API directly):
```bash
export FIGMA_ACCESS_TOKEN="your-figma-token"
```

For the POC, design data is pre-exported and committed to version control.

## Production Readiness

### Code Quality Standards

Generated components meet production requirements:
- ✅ TypeScript with proper type definitions
- ✅ Semantic HTML structure
- ✅ Accessible form inputs with labels
- ✅ Clean, well-commented code
- ✅ No runtime JavaScript dependencies (static rendering)
- ✅ Optimized CSS with Tailwind

### Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Responsive design via Tailwind breakpoints
- No polyfills required for target environments

### Performance

- Minimal bundle size (no external dependencies)
- Fast initial render (static components)
- Optimized CSS with Tailwind JIT compiler

## Troubleshooting

### Component Not Rendering

1. Verify import path in preview app page
2. Check for TypeScript errors: `cd ../preview-app && npx tsc --noEmit`
3. Ensure preview server is running: `npm run dev`
4. Check browser console for runtime errors

### Low Accuracy Scores

1. Increase `max_iterations` parameter (default: 3, try 5-7)
2. Verify Figma export quality (ensure high-res PNG export)
3. Check Oracle context for conflicting patterns
4. Review Green Arrow validation output for specific issues

### Oracle Pattern Conflicts

1. Clear project patterns: Delete `../knowledge_base/projects/{file-key}/`
2. Re-run conversion to learn fresh patterns
3. Review and curate learned patterns manually if needed

## Related Documentation

- **Parent README**: `../README.md` - Full Justice League system overview
- **Oracle Documentation**: `../ORACLE_README.md` - Pattern learning system
- **Artemis Guide**: `../ARTEMIS_EXPERT.md` - Code generation capabilities
- **Green Arrow Guide**: `../GREEN_ARROW_GUIDE.md` - Visual validation system
- **Coordination Protocol**: `../JUSTICE_LEAGUE_COORDINATION_PROTOCOL.md` - Multi-agent orchestration
