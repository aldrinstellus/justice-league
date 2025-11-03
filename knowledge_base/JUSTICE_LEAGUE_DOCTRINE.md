# 🔮 Justice League Operational Doctrine

**Last Updated:** October 28, 2025
**Authority:** Oracle & Superman
**Status:** ACTIVE - MANDATORY FOR ALL MISSIONS

---

## 🎨 CRITICAL RULE #1: SHOW, DON'T JUST TELL

### The Problem Identified (October 28, 2025)

**Mission:** K12 Homework Component Extraction
**What Happened:** Heroes built complete component, wrote 3,662 lines of code and documentation, achieved WCAG 2.1 AA compliance - but **NEVER SHOWED THE USER THE ACTUAL COMPONENT VISUALLY.**

**User Feedback:**
> "i need to see in html page, spin a chrome dev server and show me, oracle and superman, this has to defato modus operandi, plz remember and execute, we are a design focussed design, all the tell is good, but without the show is meaningless, justice-league remember this"

---

## 📜 NEW MANDATORY PROTOCOL

### For EVERY Design/Component/UI Mission:

**RULE:** After building ANY visual component, you MUST:

1. ✅ **Create standalone HTML demo** (no build tools required)
2. ✅ **Open in Chrome DevTools MCP**
3. ✅ **Take full-page screenshot** and show user
4. ✅ **Demonstrate interactions** (hover, focus, click with screenshots)
5. ✅ **Only THEN provide documentation**

### Order of Operations (MANDATORY):

```
OLD (WRONG) WORKFLOW:
1. Build component
2. Write documentation
3. Create commit
4. Done ❌

NEW (CORRECT) WORKFLOW:
1. Build component
2. Create standalone HTML demo
3. Open in Chrome
4. SHOW user with screenshots ✅
5. Demonstrate interactions ✅
6. Then provide documentation
7. Create commit
```

---

## 🎯 Why This Matters

### User Perspective:
- User is **design-focused**
- Visual proof > Documentation
- "Show me" > "Tell me about it"
- Live demo = immediate feedback loop

### Justice League Values:
- **Design-First Culture**: We build for visual impact
- **User-Centric**: User needs to SEE results, not just read about them
- **Rapid Feedback**: Screenshots enable immediate iteration
- **Proof of Work**: Visual demos prove functionality

---

## 🛠️ Technical Implementation

### Required Tools:

**Chrome DevTools MCP:**
```typescript
// 1. Create standalone HTML (no React, no build tools)
// 2. Open in Chrome
mcp__chrome-devtools__new_page({
  url: "file:///path/to/demo.html"
})

// 3. Take screenshot
mcp__chrome-devtools__take_screenshot({
  format: "png",
  fullPage: true
})

// 4. Demonstrate interactions
mcp__chrome-devtools__hover({ uid: "..." })
mcp__chrome-devtools__take_screenshot()

mcp__chrome-devtools__click({ uid: "..." })
mcp__chrome-devtools__take_screenshot()
```

### Standalone HTML Requirements:

✅ **Self-contained** - No external dependencies (or CDN only)
✅ **Tailwind via CDN** - `<script src="https://cdn.tailwindcss.com"></script>`
✅ **Inline CSS** - Component styles in `<style>` tag
✅ **Inline JavaScript** - Interactions in `<script>` tag
✅ **Design tokens** - Extract from Figma and embed
✅ **Accessibility** - Full ARIA, keyboard navigation
✅ **Professional presentation** - Headers, instructions, hero attribution

---

## 📋 Checklist for Component Missions

### Oracle's Mission Checklist:

Before marking a component mission as complete, verify:

- [ ] Component built with all states (Default, Hover, Focus, Active, Disabled)
- [ ] **Standalone HTML demo created** ⭐
- [ ] **Demo opened in Chrome DevTools MCP** ⭐
- [ ] **Full-page screenshot taken and shown to user** ⭐
- [ ] **Hover state screenshot taken** ⭐
- [ ] **Focus state screenshot taken (keyboard navigation)** ⭐
- [ ] Interactions demonstrated (click, keyboard)
- [ ] User has SEEN the visual result
- [ ] Documentation provided (after visual demo)
- [ ] Git commit created

**⭐ = Absolutely mandatory, never skip**

---

## 🦸 Superman's Responsibility

As Mission Commander, Superman MUST ensure:

1. **Every hero knows this doctrine**
2. **Visual demos are created BEFORE documentation**
3. **User sees results, not just descriptions**
4. **Chrome DevTools MCP is used for ALL UI missions**

### Superman's Question to Heroes:

Before marking component complete, Superman asks:
> "Has the user SEEN the component working in Chrome?"

If answer is NO → Mission NOT complete

---

## 🏹 Artemis's Role (Figma Extraction)

When Artemis extracts Figma:

1. Extract component structure ✅
2. Extract design tokens ✅
3. **Create visual reference board** (NEW)
4. **Show Figma component next to implemented component** (NEW)

### Side-by-Side Comparison Required:

```
[Figma Design]     [Implemented Component]
    📐                     🖥️
  Original          →   Working Demo
```

---

## 🦇 Batman's Role (Accessibility)

Batman's investigation MUST include:

1. WCAG compliance analysis ✅
2. **Visual accessibility demo** (NEW)
   - Show focus states in Chrome
   - Demonstrate keyboard navigation
   - Capture screen reader output
3. Before/After screenshots showing improvements

---

## 🎯 Green Arrow's Role (Implementation)

Green Arrow builds:

1. React/TypeScript component ✅
2. **Standalone HTML demo** (NEW) ⭐
3. Tailwind config ✅
4. **Live demo with interactions** (NEW) ⭐

### Green Arrow's Deliverable:

Not just code - **working visual demo user can see immediately**

---

## 🔮 Oracle's Role (Knowledge Management)

Oracle ensures:

1. Doctrine is followed ✅
2. **Visual demos are created** ⭐
3. **User sees results before documentation** ⭐
4. Lessons learned are documented
5. Process improvements are implemented

### Oracle's Veto Power:

Oracle can PAUSE mission if:
- Component built but not visually demonstrated
- User has not seen working demo
- Screenshots not provided

---

## 📊 Success Metrics

### OLD (Failed) Approach:
- Lines of code written: 3,662 ✅
- Documentation created: 11 files ✅
- WCAG compliance: AA ✅
- **User saw component: ❌ FAIL**

### NEW (Correct) Approach:
- Component built: ✅
- **Standalone demo created: ✅** ⭐
- **Chrome screenshot shown: ✅** ⭐
- **User saw result: ✅** ⭐
- Documentation provided: ✅
- User satisfaction: ✅

---

## 🎨 Examples of Proper Visual Demos

### Minimum Required Screenshots:

1. **Full page overview** - Entire demo page
2. **Default state** - Component in default state
3. **Hover state** - Mouse hovering over component
4. **Focus state** - Keyboard focus visible
5. **Interaction result** - After click/activation
6. **Responsive views** - Mobile, tablet, desktop (if applicable)

### Professional Demo Page Elements:

✅ **Hero header** - Title, badges, branding
✅ **Instructions** - How to test (keyboard, mouse, screen reader)
✅ **Component showcase** - Multiple examples, states
✅ **Stats/metrics** - Show data visually
✅ **Technical details** - Implementation info
✅ **Hero attribution** - Justice League credits

---

## 🚨 When This Doctrine Applies

### ALWAYS Required For:

- ✅ **Component libraries** (React, Vue, Web Components)
- ✅ **UI design implementations** (Figma → Code)
- ✅ **Dashboard visualizations** (Charts, graphs, tables)
- ✅ **Interactive widgets** (Forms, cards, modals)
- ✅ **Accessibility enhancements** (Focus states, ARIA)
- ✅ **Animation/transitions** (Hover effects, loading states)
- ✅ **Responsive layouts** (Mobile, tablet, desktop)

### Optional For:

- ❓ **Backend APIs** (but provide Postman/API docs)
- ❓ **CLI tools** (but show terminal output screenshots)
- ❓ **Data processing** (but show visual results)

**When in doubt: SHOW IT**

---

## 💡 Key Learnings from K12 Mission

### What Went Right:
- ✅ Batman questioned orders (prevented accessibility issues)
- ✅ Heroes debated solutions (reached optimal decision)
- ✅ Component built with full WCAG 2.1 AA compliance
- ✅ Comprehensive documentation created

### What Went Wrong:
- ❌ User never SAW the component until they asked
- ❌ No visual demo created proactively
- ❌ Focused on "tell" instead of "show"
- ❌ Missed user's design-focused priority

### Lesson Learned:
**"All the tell is good, but without the show is meaningless"** - User

---

## 🔄 Process Update

### Before This Doctrine:
```
Build → Document → Commit → Done
```

### After This Doctrine:
```
Build → Demo → SHOW → Document → Commit → Done
         ↓       ↓
    Standalone  Screenshots
       HTML     in Chrome
```

---

## 🎯 Enforcement

### Oracle's Authority:

Oracle has authority to:
1. **PAUSE missions** if visual demo not created
2. **VETO completion** if user hasn't seen results
3. **REQUIRE re-demos** if screenshots inadequate
4. **UPDATE doctrine** based on user feedback

### Superman's Responsibility:

Superman must:
1. **Ensure all heroes know this doctrine**
2. **Check visual demos before mission complete**
3. **Ask: "Has the user SEEN it?"**
4. **Model behavior** by creating demos himself

---

## 📚 Required Reading for All Heroes

Every hero must read and acknowledge:

1. ✅ This doctrine (JUSTICE_LEAGUE_DOCTRINE.md)
2. ✅ Chrome DevTools MCP documentation
3. ✅ Standalone HTML demo template
4. ✅ K12 Homework mission case study

---

## 🔮 Oracle's Final Word

### New Justice League Mantra:

**"SHOW first, TELL second, DOCUMENT third"**

### Core Principle:

**Visual proof > Written description**

### User Truth:

**"We are design-focused. Show us the design."**

---

## 🦸 Superman's Commitment

As Mission Commander, I commit to:

1. ✅ **Never marking UI mission complete until user SEES result**
2. ✅ **Creating visual demos for every component**
3. ✅ **Opening Chrome DevTools MCP for every UI task**
4. ✅ **Taking screenshots to show user**
5. ✅ **Prioritizing "show" over "tell"**

**This is now Justice League operational standard.**

---

## 📋 Quick Reference Card

### Every UI Mission Must Include:

```bash
# 1. Build component
✅ Component code (React/Vue/HTML)
✅ Styles (Tailwind/CSS)
✅ Interactions (JavaScript)

# 2. Create standalone demo
✅ demo.html (self-contained)
✅ Design tokens embedded
✅ Professional presentation

# 3. SHOW in Chrome
✅ Open Chrome DevTools MCP
✅ Take full-page screenshot
✅ Show hover state screenshot
✅ Show focus state screenshot
✅ Demonstrate interactions

# 4. THEN document
✅ README
✅ Technical docs
✅ Git commit
```

---

**Status:** ✅ ACTIVE - EFFECTIVE IMMEDIATELY

**Signed:**
- 🔮 Oracle (Doctrine Author)
- 🦸 Superman (Mission Commander)
- 🏹 Artemis (Figma Specialist)
- 🦇 Batman (Accessibility Guardian)
- 🎯 Green Arrow (Implementation Master)

**"Show, don't just tell. This is the way."** - Justice League

---

**Document Version:** 1.0
**Effective Date:** October 28, 2025
**Next Review:** After every UI mission
**Mandatory Compliance:** YES
