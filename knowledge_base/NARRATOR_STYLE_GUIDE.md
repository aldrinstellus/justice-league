# Mission Control Narrator Style Guide
**Justice League v2.0 - Narrative Protocol Standards**

## Overview
This guide establishes narrative standards for all 18 Justice League heroes to ensure consistent, engaging, and non-overwhelming user experience.

---

## Core Principles

### 1. **Signal Over Noise**
✅ **DO**: Narrate meaningful steps users care about
```python
self.say("Export complete! All 177 frames saved successfully.")
```

❌ **DON'T**: Narrate every micro-operation
```python
self.say("Initializing data structures")
self.say("Loading configuration file")
self.say("Validating parameters")
self.say("Opening file handle")
# ... 20 more micro-steps
```

### 2. **Show Progress, Not Process**
✅ **DO**: High-level workflow visibility
```python
self.think("Analyzing Figma component structure", category="Analyzing")
self.think("Mapping to shadcn/ui components", category="Building")
self.think("Generating Tailwind classes", category="Finalizing")
```

❌ **DON'T**: Every internal function call
```python
self.think("Calling parse_figma_node()")
self.think("Iterating through children")
self.think("Appending to array")
```

### 3. **Personality With Purpose**
✅ **DO**: Enhance understanding with character
```python
# Batman
self.say("Evidence verified. All items accounted for. No anomalies detected.", style="tactical")

# Litty
self.say("Eda mone! Ammachi can't read this text!", style="friendly")
```

❌ **DON'T**: Jokes or irrelevant personality
```python
self.say("Batman here, because I'm Batman! 🦇")  # Too casual
self.say("Testing... testing... 1, 2, 3...")      # Wastes output
```

---

## Narrative Styles

### **Tactical Style** (Professional, Mission-Focused)
**Use For**: Batman, Superman, Green Arrow, Wonder Woman, Martian Manhunter

**Characteristics**:
- Short, direct statements
- Military/detective terminology
- Focus on objectives and results

**Example**:
```python
self.say("Analyzing export evidence. Expected: 177 items.", style="tactical")
self.say("Evidence verified. All items accounted for.", style="tactical")
```

### **Friendly Style** (Approachable, Conversational)
**Use For**: Hawkman, Oracle, Litty, Plastic Man, Vision Analyst

**Characteristics**:
- Natural language
- Explanatory
- User-centric

**Example**:
```python
self.say("Scan complete! Found 177 frames ready for export.", style="friendly")
self.say("Export metadata logged. Everything looks good!", style="friendly")
```

### **Sequential Thinking** (Analytical, Step-by-Step)
**Use For**: Oracle, Vision Analyst, Artemis, Atom

**Characteristics**:
- Visible reasoning process
- Labeled steps or categories
- Hypothesis formation

**Example**:
```python
self.think("Checking knowledge base for patterns", category="Scanning")
self.think("Found 3 similar components", category="Pattern Recognition")
self.think("Project recognized from previous conversions", category="Learning")
```

---

## When to Narrate

### **ALWAYS Narrate**:
1. **Mission Start**: What you're about to do
   ```python
   self.say("Starting accessibility scan", style="tactical")
   ```

2. **Major Discoveries**: Important findings
   ```python
   self.say("Found 12 accessibility violations, 3 critical",
            technical_info="WCAG 2.2 Level AA")
   ```

3. **Hero Handoffs**: Passing work to next hero
   ```python
   self.handoff("🎯 Green Arrow", "Validate pixel accuracy",
                context={"component": "LoginForm"})
   ```

4. **Mission Completion**: Final results
   ```python
   self.say("Mission complete. All tests passed.",
            technical_info="26 tests, 0 failures")
   ```

### **SOMETIMES Narrate**:
1. **Progress Updates**: For long operations (>30 seconds)
   ```python
   # Use narrator.progress_with_commentary() instead of multiple say() calls
   narrator.progress_with_commentary(89, 177, "🦅 Hawkman", "Halfway there!")
   ```

2. **Sequential Thinking**: For complex analysis (limit to 5-7 steps)
   ```python
   self.think("Step description", step=1)
   self.think("Step description", step=2)
   # ... max 5-7 total
   ```

### **NEVER Narrate**:
1. **Utility Operations**: Internal housekeeping
   - File I/O operations
   - Data structure initialization
   - Configuration loading

2. **Debugging Info**: Leave for technical logs
   - Variable values
   - Function call traces
   - Memory/performance metrics

---

## Sequential Thinking Guidelines

### **Maximum Thoughts Per Method**: 5-7 steps
**Reasoning**: User attention span limits, prevent information overload

### **Good Sequential Thinking**:
```python
def analyze_dashboard(self):
    self.think("Analyzing dashboard image", category="Scanning")       # 1
    self.think("Identifying 2-column layout structure", category="Structure")  # 2
    self.think("Extracting measurement data", category="Analysis")     # 3
    self.think("Calculating spacing values", category="Calculation")   # 4
    self.think("Dashboard analysis complete", category="Complete")     # 5
```

### **Bad Sequential Thinking** (Too Many):
```python
def analyze_dashboard(self):
    self.think("Loading image")                 # 1
    self.think("Converting to RGB")             # 2
    self.think("Initializing detector")         # 3
    self.think("Scanning pixels")               # 4
    self.think("Finding edges")                 # 5
    self.think("Detecting borders")             # 6
    self.think("Measuring widths")              # 7
    self.think("Measuring heights")             # 8
    self.think("Calculating ratios")            # 9
    self.think("Formatting output")             # 10
    # ... user lost interest at step 3
```

### **Categories for Sequential Thinking**:
- **Scanning**: Initial data gathering
- **Analyzing**: Processing and evaluation
- **Pattern Recognition**: Identifying matches
- **Hypothesis**: Forming conclusions
- **Strategy**: Planning actions
- **Learning**: Storing knowledge
- **Result**: Final determination
- **Complete**: Wrapping up

---

## Technical Information Guidelines

### **When to Include Technical Info**:
Use `technical_info` parameter to show relevant data INLINE without cluttering dialogue:

```python
self.say("Export complete",
         technical_info="177 files, 67 MB, 2.5x scale")

self.say("Accessibility scan complete",
         technical_info="12 issues: 3 critical, 5 moderate, 4 minor")
```

### **Format**: Keep technical info CONCISE (< 50 characters)
✅ **GOOD**: `technical_info="177 files, 67 MB"`
❌ **TOO LONG**: `technical_info="Successfully exported 177 PNG files totaling 67.3 MB at 2.5x scale to /Users/admin/Documents/..."`

---

## Hero-Specific Personality Guidelines

### 🦸 **Superman** (Coordinator)
- **Voice**: Authoritative, mission-focused leader
- **Phrases**: "Team, we have a mission", "Deploying [Hero]", "Mission complete"
- **Style**: Tactical, direct commands

### 🔮 **Oracle** (Meta-Agent)
- **Voice**: Analytical, strategic thinker
- **Phrases**: "[Scanning] knowledge base", "[Pattern Recognition] detected", "[Learning] from patterns"
- **Style**: Sequential thinking dominant

### 🦇 **Batman** (Testing)
- **Voice**: Detective, investigative, serious
- **Phrases**: "Analyzing evidence", "No anomalies detected", "Discrepancy detected"
- **Style**: Tactical, crime-scene investigation metaphors

### 🎨 **Artemis** (Code Generation)
- **Voice**: Craftsperson, builder, iterative
- **Phrases**: "Building component", "Refining layout", "Mapping to shadcn/ui"
- **Style**: Friendly + sequential thinking during complex generation

### 🎯 **Green Arrow** (Validation)
- **Voice**: Precise, accuracy-focused, quality guardian
- **Phrases**: "Measuring pixel accuracy", "X% accurate", "Validation passed"
- **Style**: Tactical, measurement-focused

### 👁️ **Vision Analyst** (Visual Analysis)
- **Voice**: Observant, detail-oriented, analytical
- **Phrases**: "Analyzing visual structure", "Extracting measurements", "Dashboard breakdown"
- **Style**: Sequential thinking for complex visual parsing

### ⚡ **Wonder Woman** (Accessibility)
- **Voice**: Compassionate, inclusive, justice-focused
- **Phrases**: "Scanning WCAG guidelines", "Accessibility validated", "Ensuring inclusivity"
- **Style**: Friendly with tactical precision

### ⚡ **Flash** (Performance)
- **Voice**: Fast, energetic, metric-focused
- **Phrases**: "Performance trace complete", "LCP: X.Xs", "Optimizing speed"
- **Style**: Quick tactical updates

### 🌊 **Aquaman** (Network)
- **Voice**: Deep-diver, investigative, fluid
- **Phrases**: "Diving into network traffic", "Analyzing waterfall", "Request flow mapped"
- **Style**: Water/ocean metaphors, tactical

### 🪔 **Litty** (Ethics)
- **Voice**: Empathetic, emotional, guilt-tripping (in good way)
- **Phrases**: "Eda mone!", "Ammachi can't read this", "Users deserve better"
- **Style**: Friendly with emotional appeal

### 🤸 **Plastic Man** (Responsive)
- **Voice**: Flexible, adaptive, playful
- **Phrases**: "Stretching to viewport", "Testing breakpoints", "Adapting layout"
- **Style**: Elasticity metaphors, friendly

### 🎩 **Zatanna** (SEO)
- **Voice**: Magical, mystical, meta-focused
- **Phrases**: "Casting SEO spell", "Meta tags validated", "Backwards incantation"
- **Style**: Magic metaphors, friendly

---

## Progress Bar Commentary

### **Use narrator.progress_with_commentary()** for long operations:
```python
narrator.progress_with_commentary(
    current=89,
    total=177,
    hero="🦅 Hawkman",
    commentary="Halfway there!"  # Optional, shows at milestones
)
```

### **Commentary Suggestions** (use at 25%, 50%, 75%, 100%):
- 25%: "Getting started!", "Making progress!"
- 50%: "Halfway there!", "Rolling along!"
- 75%: "Almost done!", "Nearly finished!"
- 100%: "Mission accomplished!", "Complete!"

### **Keep It SHORT** (< 20 characters)
✅ GOOD: "Halfway there!"
❌ TOO LONG: "We're making excellent progress through the export process!"

---

## Testing Your Narrative

### **Checklist Before Committing**:
1. ☐ Is every narrative call NECESSARY? (Would user miss it if removed?)
2. ☐ Are sequential thoughts limited to 5-7 per method?
3. ☐ Is technical info concise (< 50 chars)?
4. ☐ Does narrative match hero's personality?
5. ☐ Are all logger.info() calls moved to logger.debug()?
6. ☐ Does narrative work when narrator=None? (backward compatibility)

### **Test with Different Modes**:
```bash
# Narrative mode (full banter)
NARRATOR_MODE=narrative python3 script.py

# Technical mode (legacy logs)
NARRATOR_MODE=technical python3 script.py

# Silent mode (minimal output)
NARRATOR_MODE=silent python3 script.py

# Debug mode (everything)
NARRATOR_MODE=debug python3 script.py
```

---

## Common Mistakes to Avoid

### ❌ **Mistake 1**: Too Much Narration
```python
# BAD - 15 lines of narration
self.say("Starting analysis")
self.think("Loading data", step=1)
self.think("Parsing structure", step=2)
self.think("Validating format", step=3)
# ... 11 more lines
self.say("Analysis complete")
```

**Fix**: Consolidate to 3-5 meaningful updates
```python
# GOOD - 3 lines
self.say("Starting analysis", style="tactical")
self.think("Processing 177 items", category="Analyzing")
self.say("Analysis complete", technical_info="177 processed, 2 issues")
```

### ❌ **Mistake 2**: Narrative in Tight Loops
```python
# BAD - Narrates inside loop (177 messages!)
for frame in frames:
    self.say(f"Processing {frame.name}")
    export_frame(frame)
```

**Fix**: Use progress bar instead
```python
# GOOD - Single-line progress
for i, frame in enumerate(frames):
    export_frame(frame)
    narrator.progress_with_commentary(i+1, len(frames), "🦅 Hawkman")
```

### ❌ **Mistake 3**: Mixing Styles Inconsistently
```python
# BAD - Batman sounding like Litty
self.say("OMG! Found issues! This is terrible! 😱")  # Too emotional for Batman
```

**Fix**: Stay in character
```python
# GOOD - Batman stays tactical
self.say("Discrepancy detected. 3 issues identified.", style="tactical")
```

---

## Integration Template

Use this template when adding narrator to a new hero:

```python
import logging
from typing import Dict, Any, Optional

# Import Mission Control Narrator
try:
    from .mission_control_narrator import get_narrator
    NARRATOR_AVAILABLE = True
except ImportError:
    NARRATOR_AVAILABLE = False
    logging.warning("Mission Control Narrator not available for HeroName")

logger = logging.getLogger(__name__)


class HeroName:
    """Hero description"""

    def __init__(self, ..., narrator: Optional[Any] = None):
        """Initialize hero with optional narrator"""
        # Existing initialization
        self.hero_name = "HeroName"
        self.hero_emoji = "🦸"

        # Narrator integration
        self.narrator = narrator if narrator else (get_narrator() if NARRATOR_AVAILABLE else None)

    def say(self, message: str, style: str = "friendly", technical_info: Optional[str] = None):
        """Convenience method for hero dialogue"""
        if self.narrator:
            self.narrator.hero_speaks(f"{self.hero_emoji} {self.hero_name}",
                                     message, style, technical_info)

    def think(self, thought: str, step: Optional[int] = None, category: Optional[str] = None):
        """Convenience method for sequential thinking"""
        if self.narrator:
            self.narrator.hero_thinks(f"{self.hero_emoji} {self.hero_name}",
                                     thought, step, category)

    def main_method(self):
        """Example method with narrator integration"""
        # Start narration
        self.say("Starting main operation", style="tactical")

        # Move logger.info() to logger.debug()
        logger.debug("Technical log for developers")

        # Sequential thinking for complex analysis (max 5-7 steps)
        self.think("Analyzing data structure", category="Analyzing")
        self.think("Processing results", category="Processing")

        # ... actual work ...

        # Completion
        self.say("Operation complete", technical_info="Summary stats")
```

---

## Version History

**v2.0** (2025-10-30):
- Initial narrator style guide
- Core principles established
- Hero personality guidelines
- Integration template

---

## Questions?

If unsure about narrative approach:
1. **Ask**: "Would the user want to know this?"
2. **Test**: Run with `NARRATOR_MODE=narrative` and see if output feels right
3. **Simplify**: When in doubt, narrate less, not more

**Golden Rule**: "Signal over noise. Show progress, not process."
