# Experience Story: Figma MCP + Claude Code + Playwright MCP

**Author:** Orhan Asım Arslan
**Date:** October 13, 2025
**Source:** [Medium Article](https://medium.com/javascript-in-plain-english/experience-story-figma-mcp-claude-code-playwright-68b20bb0f8ce)

---

## Summary

How combining three tools — Figma's MCP server, AI interpretation, and automated validation — created a framework for building 21 components across 4 breakpoints and catching 12+ bugs before deployment.

---

## The Challenge: 84 Responsive Variations to Validate

I was tasked with building a component library — 21 components across 4 breakpoints. That's 84 variations to implement and validate. The question wasn't if I could build them, but how efficiently I could achieve high accuracy across all screen sizes without manual testing becoming a bottleneck.

**The core challenge:** Responsive design validation at scale.

For a single component, manually comparing Figma screenshots against implementation might work. But for 21 components? That's unsustainable. I needed a systematic, data-driven approach.

This led me to discover a powerful combination: **Figma's MCP (Model Context Protocol) server**, **Claude Code for AI interpretation**, and **Playwright MCP for programmatic validation**. Together, these three tools solve the exact problems that make responsive development at scale so challenging.

### This article shares:
- The three-tool system I built
- The workflow that emerged from combining them
- The real bugs this combination caught before deployment

To demonstrate why this approach works, I'll contrast it with screenshot-based workflows — showing exactly what each tool contributes and why all three are necessary.

**The key insight?** Treating Figma as a database (not a design viewer), AI as a responsive interpreter (not just a code generator), and Playwright as a validation engine (not just a testing tool) changes everything.

---

## The Analysis: Screenshot-Based Workflows at Scale

To demonstrate why the Figma MCP + Claude Code + Playwright MCP combination is so effective, let's first examine traditional screenshot-based approaches and their limitations at scale. I tested this method initially to understand what gaps the three-tool system would need to address:

### The Screenshot Approach:

1. Export Figma screenshots via Figma MCP for each component
2. Analyze design visually (with AI vision tools)
3. Implement based on visual interpretation
4. Compare screenshots side-by-side
5. Iterate until visually acceptable

For small projects, maybe this works. But when I mapped this workflow against 84 variations (21 components × 4 breakpoints), three critical limitations emerged:

### Limitation 1: Single-Context Analysis

**Scenario:** Card grid component with three news articles.

**Visual Analysis (Desktop frame only):**
- AI vision correctly identifies: `flex-row` layout, vertical dividers, exact spacing
- Implementation proceeds based on desktop specifications

**The Gap:** When I analyzed the mobile frame separately, the design was fundamentally different: `flex-col` layout with horizontal dividers. This wasn't a responsive scaling — it was an intentional layout restructure.

**The Issue:** Screenshot-based analysis is inherently single-context. Each frame must be analyzed separately, then manually synthesized to understand responsive behavior. With 4 breakpoints per component, that's 4 separate analyses plus manual comparison — per component.

**Scale impact:** 21 components × 4 breakpoints = 84 separate visual analyses + manual synthesis work.

### Limitation 2: Visual Output vs. Computed Properties

**Scenario:** Three-column article layout component.

**Visual Validation:**
- Alignment: ✅ Perfect
- Spacing: ✅ Matches Figma
- Colors: ✅ Accurate

**Hidden Issue (discovered during width testing at 1440px):**

Programmatic measurement revealed the container was 1142px wide, but cards were only 375px each — leaving 392px of unintended empty space. The cards had `flex-grow: 0`, keeping them at minimum content width instead of filling available space.

**The Issue:** Screenshots capture visual output, not computed CSS properties. You can see rendered dimensions, but you can't see:

- `flex-grow` values (0 vs 1)
- Actual computed widths after layout
- z-index stacking context
- Hidden overflow behavior

**Scale impact:** Visual validation alone creates false confidence. A component can look "correct" visually while having fundamental layout issues. At 84 variations, relying solely on visual comparison means missing entire categories of bugs.

### Limitation 3: State Transitions Across Breakpoints

**Scenario:** Navigation bar with progressive disclosure (0 links on mobile → 6 on tablet → 9 on desktop).

**Implementation Approach:** Using Tailwind's responsive prefixes: `tablet:inline-flex` for the first 6 links, assuming it meant "show on tablet and above only."

**The Issue (discovered during mobile viewport testing):** Without a base `hidden` class, responsive prefixes are additive, not replacements. `tablet:inline-flex` applies inline-flex starting at tablet, but elements remain visible on mobile by default.

**What this revealed:** Responsive behavior isn't just about layout dimensions — it's about:

- Visibility state transitions (hidden → visible)
- Hierarchy changes (primary nav → overflow menu)
- Progressive disclosure (content revealed at larger viewports)

Screenshot comparison shows static states. It doesn't capture the conditional logic driving visibility across breakpoints and also AI vision analysis not returning stable and correct analysis, even you described the issue it won't return with correct analysis.

**Scale impact:** With 84 variations, state transition bugs compound. Each breakpoint isn't just a resized layout — it's a different behavioral state that requires explicit validation.

### The Systematic Gap

These three limitations weren't isolated issues — they revealed a systematic gap in screenshot-based workflows:

- **Gap 1:** Multi-context synthesis — 4 breakpoints = 4 separate analyses + manual comparison work
- **Gap 2:** Programmatic validation — Visual output doesn't reveal computed properties or layout behavior
- **Gap 3:** State logic verification — Static screenshots can't validate dynamic responsive transitions

**The calculation:** 45 minutes sessions per component using screenshot-based validation. For 21 components, that's too much hours of manual work — and still no guarantee of catching computed style bugs or state transition issues.

### The conclusion:

I needed a workflow that:

1. Queried all breakpoints simultaneously
2. Provided exact specifications (not interpretations)
3. Validated computed properties programmatically
4. Scaled efficiently to 84+ variations

This led me to explore code-first alternatives.

---

## The Discovery: Three Tools, One System

To address these three limitations — multi-context synthesis, programmatic validation, and state logic verification — I discovered three complementary tools that, when combined, create a comprehensive framework. Here's how each tool solves a specific gap:

### Part 1: Figma as a Database

I found Figma's MCP (Model Context Protocol) server — a relatively new tool most developers don't know exists yet.

**Here's the key insight:** As far as you know, Figma doesn't just store images of your designs. It stores structured data — padding values, layout properties, typography specs, color codes. Every design decision lives in Figma's API as queryable information. These are become **Design Tokens**.

Also, instead of asking an AI vision model to interpret a screenshot, you can ask Figma's API to generate code directly from the design nodes.

#### The shift:

❌ Screenshot → AI interprets visual → Suggests code

✅ Design node → Query structured data → Generate code

One returns an interpretation. The other returns exact specifications. Much more professional approach.

You can query code for every breakpoint in your Figma file separately — desktop frame, laptop frame, tablet frame, mobile frame — and compare what changes:

- When does layout direction flip? (flex-row → flex-col)
- How does typography scale? (24px → 16px → 14px)
- Where does padding adjust? (89px → 63px → 42px)

No interpretation layer. Just data.

**But here's the catch:** Figma-generated code isn't production-ready.

#### The Reality of Figma Code Generation

When Figma generates code from design nodes, you get exact CSS values — padding, font-size, colors — but the code often has limitations:

**Issue #1: Static, Not Responsive**

Figma outputs exact pixel values for one frame at a time. If you query the desktop frame, you get:

```css
padding: 89px 331px;
font-size: 24px;
```

But no responsive logic. Figma doesn't automatically generate `laptop:px-[346px]` or `tablet:text-[16.216px]`. You get static values per breakpoint.

**Issue #2: Design Structure and Constraints Variability**

How designers structure Figma files significantly impacts code quality. Depending on auto-layout usage, constraint configuration, and component architecture, generated code can vary widely:

- Fixed widths instead of flexible layouts (when responsive constraints aren't configured)
- Absolute positioning instead of flex/grid (when auto-layout isn't utilized)
- Missing semantic structure (Figma focuses on visual output, not HTML semantics)
- No mobile-first CSS consideration (Figma generates frame-specific code, not responsive logic)

The reality: Even with professionally structured Figma files, the API generates presentation-focused code, not production-ready responsive components. The interpretation layer (Claude Code) bridges this gap.

**Issue #3: No Cross-Breakpoint Synthesis**

Querying 4 breakpoints gives you 4 separate code outputs. Figma doesn't tell you:

- "Layout direction flips on mobile"
- "This component is hidden on tablet"
- "Gap value changes at laptop breakpoint"

You still need to compare and synthesize the differences.

This is where Claude Code entered my workflow — not as a code generator, but as a **responsive code interpreter**.

### Part 2: Claude Code as Responsive Interpreter

I created a detailed strategy document (CLAUDE.md) that defined:

- Responsive breakpoint strategy (mobile-first, exact Tailwind classes)
- Design token comparison methodology
- Component hierarchy rules
- When to use flex-grow vs fixed widths
- How to handle visibility state transitions

**Claude Code's role:**

1. Query all 4 breakpoints from Figma MCP simultaneously
2. Compare outputs — identify what changes between breakpoints
3. Generate comparison tables — document padding/font/layout differences
4. Apply responsive strategy — transform static Figma code into responsive Tailwind classes
5. Implement semantic structure — use proper HTML/React patterns, not just div soup

#### Example transformation:

**Figma Output (4 separate queries):**

```
Desktop:
  flexDirection: column
  gap: 28px
  width: 351px
  padding: 10px

Tablet:
  flexDirection: row
  gap: 8.512px
  width: 100%
  padding: 9.279px
```

**Claude Code Interpretation:**

```jsx
<div className={cn(
  // Base mobile-first: vertical layout
  'flex flex-col',
  'gap-[28px]',
  'w-full max-w-[351px]',
  'p-[10px]',

  // Tablet+: horizontal layout transformation
  'tablet:flex-row',
  'tablet:gap-[8.512px]',
  'tablet:max-w-none',
  'tablet:p-[9.279px]'
)}>
  {/* Card content */}
</div>
```

**The key insight:** Figma provides the specifications. Claude Code provides the responsive logic.

Without this interpretation layer, I'd have 4 separate static implementations instead of 1 responsive component.

But getting exact code from Figma — even with responsive interpretation — only solved half the problem. I still needed to validate that my implementation matched the specs across all breakpoints.

That's where Playwright entered the picture.

### Part 3: Playwright as Validation Engine

Playwright isn't just a testing tool. In this workflow, it became the validation engine that closed the loop:

1. **Computed Style Verification** — Measure actual CSS properties (flex-grow, rendered widths, z-index) that screenshots can't show
2. **Multi-Breakpoint Testing** — Programmatically resize browser, capture metrics at every breakpoint
3. **Automated Regression** — Compare implementation against specs across all screen sizes systematically

**Why this matters:** Figma MCP tells you what the design should be. Playwright tells you what your implementation actually is. Together, they create a feedback loop that's both precise and scalable.

#### Think of it this way:

- **Figma MCP** = Source of truth (exact design specifications per breakpoint)
- **Claude Code** = Interpretation layer (transforms static specs → responsive logic)
- **Playwright MCP** = Validation engine (measures implementation reality)

#### The workflow:

```
Figma MCP
    ↓ (Queries 4 breakpoints)
Raw specs:
  Desktop: flex-direction: column; gap: 28px; width: 351px;
  Tablet: flex-direction: row; gap: 8.512px; width: 100%;
    ↓
Claude Code
    ↓ (Synthesizes & applies responsive strategy)
Responsive code:
  flex flex-col gap-[28px] w-full max-w-[351px]
  tablet:flex-row tablet:gap-[8.512px] tablet:max-w-none
    ↓
Implementation
    ↓
Playwright
    ↓ (Measures actual computed values)
Validation:
  Desktop → flexDirection: "column", gap: "28px" ✅
  Tablet → flexDirection: "row", gap: "8.512px" ✅
    ↓
✅ Match or ❌ Fix & re-validate
```

#### Why all three are necessary:

1. **Figma alone** → Static values, no responsive logic
2. **Figma + Claude Code** → Responsive code, but no verification
3. **Figma + Claude Code + Playwright** → Comprehensive validation framework ✅

**The paradigm shift:**

I stopped treating Figma as a design viewer, Claude Code as just an assistant, and Playwright as a testing tool. I started treating them as three interconnected parts of a validation system.

---

## The Workflow: 7 Steps to Responsive Validation

After building 21 components with this approach, I refined it into a repeatable 7-step process.

```
Steps 1–4: Get code for all breakpoints
↓
Step 5: Compare & identify what changes
↓
Step 6: Implement with exact values
↓
Step 7: Validate programmatically
```

### Step 1-4: Query All Breakpoints First

Don't just build the desktop version. Get code for every screen size before you write a single line of code.

For each component, query all four breakpoint variants:

- Desktop frame (1920px)
- Laptop frame (1440px)
- Tablet frame (1024px)
- Mobile frame (393px)

**Example: Video gallery section**

When I queried all four breakpoints, I discovered:

- Desktop, laptop, tablet all returned the same "video-section" node with scaled values
- Mobile returned a completely different node: "photo-section" (no video icons)

This immediately revealed the designer's intent: Use a different component on mobile, not a responsive variant.

If I'd analyzed screenshots one at a time, I would've built the wrong component for mobile and discovered it in QA — or worse, after deployment.

### Step 5: Build Comparison Tables

Let Claude Code create a table of what changes between breakpoints:

| Property      | Desktop     | Laptop  | Tablet  | Mobile |
|---------------|-------------|---------|---------|--------|
| **Padding X** | 331px       | 346px   | 233.78px| 20px   |
| **Padding Y** | 89px        | 63px    | 42.57px | 24px   |
| **Font Size** | 24px        | 24px    | 16.216px| 14px   |
| **Layout**    | flex-row    | flex-row| flex-row| flex-col ⚠️ |
| **Gap**       | 28px        | 28px    | 8.512px | 16px   |
| **Border**    | 2px         | 2px     | 1.351px | 1px    |

This table became my source of truth.

**Key observations:**

- Padding changes at every breakpoint (not just mobile)
- Font size scales down at tablet
- Layout direction flips on mobile
- Even border width scales proportionally

Without this table, I would have guessed most of these values wrong.

### Step 6: Implement with Exact Values

Now implementation becomes straightforward — translate your comparison table directly into responsive Tailwind classes.

For each property that changes per breakpoint, use Tailwind's arbitrary value syntax with responsive prefixes:

- Base mobile-first values (no prefix)
- Tablet overrides (`tablet:` prefix)
- Laptop overrides (`laptop:` prefix)
- Desktop overrides (`desktop:` prefix)

**Example:** Padding that scales from 89px/331px (desktop) → 63px/346px (laptop) → 42.57px/233.78px (tablet) becomes:

```
py-[89px] px-[331px] laptop:py-[63px] laptop:px-[346px] tablet:py-[42.57px] tablet:px-[233.78px]
```

**The key insight:** Tailwind's arbitrary value syntax (`[89px]`) lets you use exact Figma values instead of approximating to the nearest Tailwind scale value (`p-20`, `p-24`, etc.).

Minimal rounding. Minimal guesswork. Design specs directly in code.

### Step 7: Validate with Playwright

This is where Playwright closes the loop. For each component, run three types of validation:

#### a) Visual Snapshots Across Breakpoints

Programmatically resize the browser to each breakpoint width (1920px, 1440px, 1024px, 393px) and capture screenshots. This creates a visual record you can compare against Figma — but unlike manual screenshot comparison, it's automated and repeatable.

**Note on Advanced Visual Comparison:** Playwright also offers pixel-by-pixel visual regression testing using tools like `pixelmatch` (automated screenshot diffing). However, this feature requires installing Playwright standalone via `pnpm` and setting up comparison workflows — it's not available through Playwright MCP. When Figma designs are professionally structured with precise measurements, this automated visual comparison can provide an additional validation layer, automatically highlighting any pixel differences between Figma screenshots and implementation.

#### b) Computed Style Verification

This is the secret sauce. Use Playwright's evaluate function to measure actual CSS properties that screenshots can't show:

- **flex-grow** — Is the element set to expand? (0 vs 1)
- **Rendered widths** — What's the actual pixel width after layout?
- **Gap values** — Does the computed gap match your Tailwind class?
- **Padding** — Is the browser rendering the exact padding you specified?

**Example:** When I checked flex-grow on those article cards, Playwright showed me `flex-grow: 0` when I expected `1`. That's a bug I couldn't see visually.

#### c) Console Error Check

Automated console monitoring catches runtime issues:

- React hydration errors (SSR mismatches)
- Image loading failures
- Missing dependencies
- CSS warnings about invalid values

**Why This Matters:**

Each validation layer catches different bug types:

- **Visual snapshots** → Layout/alignment issues
- **Computed styles** → Invisible property bugs
- **Console errors** → Runtime problems

Together, they create comprehensive coverage across all 4 breakpoints.

### The Complete Flow:

1. Generate Figma code (all breakpoints) ✅
2. Build comparison table ✅
3. Implement with exact values ✅
4. Validate with Playwright ✅
5. Fix any bugs found 🔧
6. Re-validate ✅
7. Ship with much higher confidence 🚀

---

## Real Bugs This System Caught

Let me show you three real bugs this workflow caught before deployment.

### Bug #1: Mobile Component Mismatch

**Component:** Video gallery section (homepage hero)

**What I Expected:**
- Desktop/laptop/tablet: Video grid with play buttons
- Mobile: Smaller video thumbnails

**What Code Generation Revealed:**

```javascript
// Desktop (1920px)
get_code(nodeId: "1:67560")
→ Component: "video-section"
→ Children: Video thumbnails with play icons

// Laptop (1440px)
get_code(nodeId: "1:63905")
→ Component: "video-section"
→ Same structure

// Tablet (1024px)
get_code(nodeId: "1:65036")
→ Component: "video-section"
→ Same structure

// Mobile (393px)
get_code(nodeId: "816:12905")
→ Component: "photo-section" // ⚠️ DIFFERENT NODE!
→ Children: Photo gallery (no video icons)
```

**The Discovery:**

The designer used a completely different component on mobile. Not a responsive variant — a different component entirely.

**If I'd Used Screenshots:**
1. I'd have built the desktop video section
2. Added some `mobile:` classes to shrink it
3. Shipped the wrong component on mobile
4. QA would catch it (maybe)

**Because I Used Code-First:**
1. Caught it immediately during code generation (Step 1)
2. Built conditional rendering:

```jsx
<VideoSection className="hidden mobile:hidden tablet:block" />
<PhotoSection className="block tablet:hidden" />
```

3. Bug avoided before testing phase ✅

**Lesson:** Never assume mobile = shrunk desktop. Always check all breakpoints.

### Bug #2: The Invisible Flex-Grow Issue

**Component:** Featured articles (three-column layout)

**Visual Inspection:** ✅ Looked perfect on my 1920px monitor

**Discovered During:** Playwright validation at 1440px breakpoint

**The Issue:**

Computed style validation revealed the measurements immediately:

- Container width: 1142px
- Card 1 width: 375px
- Card 2 width: 375px
- Empty space: 392px (should be filled!)

The killer detail: Both cards had `flex-grow: 0`, meaning they stayed at minimum content width instead of expanding to fill available space.

**The Fix:**

Added `laptop:flex-1` to both cards. After the fix, Playwright confirmed:

- Card 1 width: 537px (fills space)
- Card 2 width: 537px (fills space)
- `flex-grow: 1` (expanding properly)

**Lesson:** Visual inspection can't reveal computed CSS properties. You can't see flex-grow, z-index, or layout behavior in screenshots. Playwright's programmatic measurement caught a bug that was invisible to the eye.

### Bug #3: Responsive Visibility Misunderstanding

**Component:** Navigation bar with progressive disclosure

**Expected Behavior:**
- Mobile: 0 links (hamburger only)
- Tablet: 6 links
- Laptop: 9 links

**What I Thought:** I used `tablet:inline-flex` for the first 6 links, thinking it meant "show on tablet and above only."

**The Bug:** When Playwright tested at mobile (393px), it counted 6 visible links instead of 0.

**Why It Failed:** Tailwind's responsive prefixes are additive. `tablet:inline-flex` means "apply inline-flex starting at tablet breakpoint" — but without a base `hidden` class, elements default to visible on mobile too.

**The Fix:** Changed to `hidden tablet:inline-flex` — start hidden (mobile-first), then show at tablet+.

After fix, Playwright validated:
- Mobile: 0 links ✅
- Tablet: 6 links ✅
- Laptop: 9 links ✅

**Lesson:** Responsive prefixes don't replace; they add. Always think mobile-first: what's the base state before responsive overrides kick in?

---

## Results After 21 Components

After building 21 components with this workflow, here's what changed:

### By The Numbers:

✅ 21 components built
✅ 4 breakpoints validated (393px, 1024px, 1440px, 1920px)
✅ 84 component variations tested

### Bugs Caught Pre-Deployment:

- 1 major component mismatch (mobile used different component)
- 6 layout/spacing issues (flex-grow, padding, gaps)
- 2 responsive visibility bugs (missing `hidden` base classes)
- 3 typography scaling issues (wrong font-size at breakpoints)
- Multiple breakpoint-specific edge cases

**Total bugs caught before users saw them:** 12+

### Design Accuracy:

**Before:** Approximated Tailwind scale values (`px-8`, `py-20`) that "looked close enough"

**After:** Exact arbitrary values from Figma (`px-[331px]`, `py-[89px]`)

**Results:**
- ✅ Very close to Figma specs at all 4 breakpoints
- ✅ Minimal responsive bugs in production (most caught pre-deployment)
- ✅ Maintainable (design tokens match Figma closely)
- ✅ Self-documenting (exact values, not approximations)

### Confidence Level:

**Before:** "I hope this works on most devices…"

**After:** "I've validated 84 variations programmatically."

---

## Lessons Learned

After this journey, here's what I'd tell my past self:

### 1. Don't Assume Mobile = Shrunk Desktop

❌ Build desktop → Add responsive classes → Hope for the best

✅ Get all 4 codes → Compare changes → Implement precisely

Mobile isn't always a shrunk desktop. Sometimes it's a different component entirely.

### 2. Build Comparison Tables First

That design token comparison table saved me hours of debugging. It became my single source of truth.

```
| Property | Desktop | Tablet  | Mobile  | Changes?|
| -------- | ------- | ------- | ------- | --------|
| Layout   | flex-row| flex-row| flex-col| ⚠️ FLIPS |
| Gap      | 28px    | 8.512px | 16px    | ⚠️ VARIES|
```

If something changes, document it before coding.

### 3. Screenshots Hide Critical Bugs

You can't see in screenshots:
- `flex-grow: 0` vs `1`
- Actual rendered widths
- z-index stacking issues
- Hidden overflow

Measure programmatically. Use Playwright's evaluate function to get actual computed CSS properties, not guesses.

### 4. Automate Or Drown

- 1 component × 4 breakpoints = 4 checks (manageable manually)
- 21 components × 4 breakpoints = 84 checks (impossible manually)

That means automate or drown.

### 5. Use Arbitrary Values

Use Tailwind's arbitrary value syntax (`px-[331px]`) instead of approximating to the nearest scale value (`px-8`). When Figma specifies 331px, use 331px — not "close enough."

Tailwind supports arbitrary values for a reason: high-fidelity implementations.

### 6. Document Everything

Future you will thank present you:
- Component mapping tables
- Design token comparisons
- Validation checklists

Don't skip documentation.

---

## Important Reality Check

💡 **Even with this workflow, frontend developers remain essential.** Here's why:

- **AI interpretation has limits** — Claude Code accelerates responsive logic generation, but developers make final architectural decisions
- **Semantic structure matters** — Accessibility, performance optimization, and proper HTML semantics require human judgment
- **Business logic integration** — Design specs don't include state management, API integration, or user interactions
- **Edge cases** — Real-world scenarios often require adjustments beyond what Figma specifies

**What this workflow provides:** A dramatically faster starting point — not a finished product. Instead of spending 45 minutes per component guessing dimensions and debugging responsive issues, you spend 25 minutes implementing with exact specs and programmatic validation. The developer's expertise is applied where it matters most: architecture, accessibility, and refinement — not measuring pixels.

For smaller projects (quick prototypes, single landing pages, <5 components), the traditional screenshot-based approach may be sufficient. The ROI of setting up this system comes from scale — the more components and breakpoints you're building, the more time this saves.

---

## The Future is Code-First

Figma MCP was released in 2025. Most developers don't know it exists yet. AI-assisted development is accelerating — not just for code generation, but for code interpretation and systematic validation. The design-to-code gap is shrinking rapidly.

### The tools are available today:

- **Figma MCP** (subscription based, There are open-source alternatives which works via API Auth Token but limited abilities) — Design specifications
- **Claude Code** (or other AI assistants) — Responsive interpretation
- **Playwright MCP** (free) — Programmatic validation

**The key insight:** You don't need just tools — you need a system. Figma provides data. AI interprets it into responsive logic. Playwright validates the output. Together, they create a feedback loop that scales.

The question isn't whether to adopt code-first development. The question is: **How much longer will you keep guessing dimensions from screenshots when you could be querying structured data?**

---

## How to Start

The workflow I've shared is fully reproducible:

1. **Set up Figma MCP** — Connect to your Figma files
2. **Configure AI interpretation** — Define your responsive strategy (CLAUDE.md document)
3. **Query all breakpoints** — Get exact specs for each screen size
4. **Generate comparison tables** — Identify what changes between breakpoints
5. **Implement responsive components** — Transform static specs into responsive Tailwind classes
6. **Validate with Playwright MCP** — Programmatically test all breakpoints
7. **Ship with higher confidence** — Framework-driven validation complete

### The three-part system:

- **Figma MCP** for specifications
- **AI assistant** for interpretation
- **Playwright** for validation

---

## Key Takeaways

1. **Treat Figma as a database**, not just a design viewer
2. **Use AI for responsive interpretation**, not just code generation
3. **Leverage Playwright for programmatic validation**, not just testing
4. **Build comparison tables** to identify changes across breakpoints
5. **Use exact Tailwind arbitrary values** instead of approximations
6. **Automate validation** across all breakpoints systematically
7. **Frontend developers remain essential** for architecture, accessibility, and refinement

---

**Tags:** #Figma #MCP #ClaudeCode #Playwright #ResponsiveDesign #WebDevelopment #DesignToCode #ComponentLibrary #TailwindCSS #Automation

---

*Article parsed and saved to knowledge base on October 28, 2025*
