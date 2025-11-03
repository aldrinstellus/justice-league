# Inter-Agent Debate Protocol

**Justice League v2.0 - Collaborative Decision Making Through Debate**

## Overview

The Inter-Agent Debate Protocol enables Justice League heroes to collaboratively debate complex decisions using sequential thinking and reach better solutions together.

**Key Principle**: *"My agents fighting with each other"* - in the BEST way! Heroes question orders, present evidence, challenge each other, and Superman makes informed decisions based on team expertise.

---

## Architecture

### Debate Flow

```
1. Issue Raised → Investigation Complete
     ↓
2. Hero Takes Position (with sequential thinking)
     ↓
3. Heroes Question Each Other
     ↓
4. Heroes Present Evidence & Proposals
     ↓
5. Oracle Asks Mission-Critical Question (reframes debate)
     ↓
6. Superman Analyzes All Input (sequential thinking)
     ↓
7. Superman Makes Informed Decision
     ↓
8. Team Agreement & Execution
```

### Debate Participants

**Typical Debate Team**:
- 🦸 **Superman** - Final decision maker, analyzes all input
- 🦇 **Batman** - Investigates, raises concerns, questions orders
- 🎨 **Artemis** - Technical analysis, design expertise
- 🎯 **Green Arrow** - Validation evidence, quality concerns
- 🔮 **Oracle** - Strategic questions, pattern analysis, mission framing

**Any hero can participate** - debates are open to all 18 Justice League heroes.

---

## Narrator Methods

### 1. `debate_start(initiator, issue, participants, context)`

**Purpose**: Start an inter-agent debate on a specific issue

**Example**:
```python
narrator.debate_start(
    initiator="🦇 Batman",
    issue="Component has 3 CRITICAL WCAG violations",
    participants=["🦸 Superman", "🦇 Batman", "🎨 Artemis", "🎯 Green Arrow", "🔮 Oracle"],
    context={
        "violations_found": 3,
        "severity": "CRITICAL",
        "wcag_level": "AA",
        "impact": "Keyboard-only and low-vision users excluded"
    }
)
```

**Output**:
```
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
  🦇 Batman: INVESTIGATION COMPLETE
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥

🦇 Batman: Component has 3 CRITICAL WCAG violations

📋 Context:
  • Violations Found: 3
  • Severity: CRITICAL
  • Wcag Level: AA
  • Impact: Keyboard-only and low-vision users excluded
```

---

### 2. `debate_position(hero, position, reasoning, evidence)`

**Purpose**: Hero takes a position with sequential thinking

**Example**:
```python
narrator.debate_position(
    "🦇 Batman",
    "Should we proceed knowing we'll exclude keyboard-only and low-vision users?",
    reasoning=[
        "Analyzing Figma file structure",
        "No Focus state detected in component",
        "WCAG 2.4.7 requires visible focus indicators",
        "Color contrast ratios below 4.5:1 threshold"
    ],
    evidence="3 CRITICAL violations found"
)
```

**Output**:
```
🦇 Batman: [Investigating] Analyzing Figma file structure
🦇 Batman: [Investigating] No Focus state detected in component
🦇 Batman: [Investigating] WCAG 2.4.7 requires visible focus indicators
🦇 Batman: [Questioning] Color contrast ratios below 4.5:1 threshold
🦇 Batman: Should we proceed knowing we'll exclude keyboard-only and low-vision users? [3 CRITICAL violations found]
```

---

### 3. `debate_question(from_hero, to_hero, question, concern)`

**Purpose**: Hero questions another hero in the debate

**Example**:
```python
narrator.debate_question(
    "🦇 Batman",
    "🦸 Superman",
    "Should we proceed knowing we'll exclude keyboard-only users?",
    concern="Mission accessibility requirements"
)
```

**Output**:
```
🦇 Batman → 🦸 Superman: Should we proceed knowing we'll exclude keyboard-only users? [⚠️ Mission accessibility requirements]
```

---

### 4. `debate_evidence(hero, finding, evidence_type)`

**Purpose**: Hero presents evidence in the debate

**Example**:
```python
narrator.debate_evidence(
    "🎨 Artemis",
    "Figma file has NO Focus state - this is a design gap",
    evidence_type="Design Analysis"
)
```

**Output**:
```
🎨 Artemis: [Design Analysis] Figma file has NO Focus state - this is a design gap
```

---

### 5. `debate_proposal(hero, proposal, approach)`

**Purpose**: Hero proposes a solution in the debate

**Example**:
```python
narrator.debate_proposal(
    "🎯 Green Arrow",
    "Build with accessible defaults, refine with designer later",
    approach="Accessibility-first development"
)
```

**Output**:
```
🎯 Green Arrow: 💡 Proposal: Build with accessible defaults, refine with designer later
  Approach: Accessibility-first development
```

---

### 6. `debate_critical_question(hero, question, stakes)`

**Purpose**: Oracle asks a mission-critical question that reframes the debate

**Example**:
```python
narrator.debate_critical_question(
    "🔮 Oracle",
    "If a student with disabilities cannot use this, have we succeeded?",
    stakes="Mission success criteria"
)
```

**Output**:
```
🔮 Oracle: ⚡ MISSION-CRITICAL QUESTION:
  "If a student with disabilities cannot use this, have we succeeded?"
  Stakes: Mission success criteria
```

---

### 7. `debate_resolution(leader, decision, rationale, team_agreement)`

**Purpose**: Leader resolves the debate with final decision

**Example**:
```python
narrator.debate_resolution(
    leader="🦸 Superman",
    decision="Build with accessibility enhancements NOW",
    rationale=[
        "Analyzing team input: Batman raised valid concerns",
        "Artemis confirmed design gap in Figma file",
        "Oracle framed mission-critical question",
        "Green Arrow proposed practical solution",
        "Mission goal: K-12 students MUST be able to use this"
    ],
    team_agreement="Unanimous - team aligned on accessible approach"
)
```

**Output**:
```
──────────────────────────────────────────────────────────────────────────────
🦸 Superman: DECISION
──────────────────────────────────────────────────────────────────────────────
🦸 Superman: [Analyzing Team Input] Analyzing team input: Batman raised valid concerns
🦸 Superman: [Analyzing Team Input] Artemis confirmed design gap in Figma file
🦸 Superman: [Analyzing Team Input] Oracle framed mission-critical question
🦸 Superman: [Analyzing Team Input] Green Arrow proposed practical solution
🦸 Superman: [Deciding] Mission goal: K-12 students MUST be able to use this

🦸 Superman: ✅ Build with accessibility enhancements NOW

  Team Status: Unanimous - team aligned on accessible approach

==============================================================================
```

---

## Hero Convenience Methods (HeroBase)

All heroes inheriting from `HeroBase` have access to these debate methods:

### `debate_with_sequential_thinking(position, reasoning_steps, evidence)`

Take a position in debate using sequential thinking.

**Example**:
```python
batman.debate_with_sequential_thinking(
    position="Should we proceed knowing we'll exclude keyboard-only users?",
    reasoning_steps=[
        "Analyzing Figma file structure",
        "No Focus state detected in component",
        "WCAG 2.4.7 requires visible focus indicators"
    ],
    evidence="3 CRITICAL violations found"
)
```

### `question_hero(target_hero, question, concern)`

Question another hero in the debate.

**Example**:
```python
batman.question_hero(
    "🦸 Superman",
    "Should we proceed knowing we'll exclude users?",
    concern="Mission accessibility requirements"
)
```

### `present_evidence(finding, evidence_type)`

Present evidence in the debate.

**Example**:
```python
artemis.present_evidence(
    "Figma file has NO Focus state - this is a design gap",
    evidence_type="Design Analysis"
)
```

### `propose_solution(proposal, approach)`

Propose a solution in the debate.

**Example**:
```python
green_arrow.propose_solution(
    "Build with accessible defaults, refine with designer later",
    approach="Accessibility-first development"
)
```

### `ask_critical_question(question, stakes)`

Ask a mission-critical question that reframes the debate.

**Example**:
```python
oracle.ask_critical_question(
    "If a student with disabilities cannot use this, have we succeeded?",
    stakes="Mission success criteria"
)
```

---

## Debate Examples

### Example 1: Accessibility Violations Debate

**Scenario**: Batman finds 3 CRITICAL WCAG violations. Should the team proceed?

**Debate Flow**:

1. **Batman** raises the issue with sequential thinking investigation
2. **Batman** questions **Superman**: "Should we proceed knowing we'll exclude users?"
3. **Artemis** confirms evidence: "Figma file has NO Focus state - design gap"
4. **Green Arrow** proposes solution: "Build with accessible defaults, refine later"
5. **Oracle** asks mission-critical question: "If students with disabilities can't use this, have we succeeded?"
6. **Superman** analyzes all input and decides: "Build with accessibility enhancements NOW"

**Result**: ✅ Team reaches better solution through collaborative debate

---

### Example 2: Methodology Selection Debate

**Scenario**: Oracle detects complex dashboard. Which methodology should be used?

**Debate Flow**:

1. **Oracle** raises complexity concern with sequential analysis
2. **Oracle** presents evidence: "Image-to-HTML achieved 90-95% accuracy vs. Figma API 70-85%"
3. **Artemis** confirms complexity: "Complexity score 8.5/10, exceeds Figma API threshold"
4. **Superman** analyzes data and decides: "Use Image-to-HTML methodology with Vision Analyst"

**Result**: ✅ Team chooses optimal approach based on evidence and past learnings

---

### Example 3: Order Questioning Debate

**Scenario**: Superman orders desktop-first approach. Artemis questions the order.

**Debate Flow**:

1. **Artemis** questions order: "Should we query all breakpoints first?"
2. **Artemis** provides reasoning with sequential thinking
3. **Green Arrow** supports with evidence: "12 visual regressions on previous desktop-only"
4. **Oracle** provides strategic data: "23% accuracy improvement with breakpoint-first"
5. **Superman** revises order based on team expertise: "Query all breakpoints first"

**Result**: ✅ Heroes questioned the order and Superman revised based on team expertise

---

## Debate Guidelines

### When to Use Debates

**Use inter-agent debates when**:
- Mission-critical decision with multiple valid approaches
- Hero identifies issues with current plan/order
- Complex technical decision requiring multiple perspectives
- Accessibility, security, or quality concerns arise
- Methodology selection for complex components
- Hero questions Superman's order with valid reasoning

### Sequential Thinking in Debates

**Maximum thoughts per position**: 3-7 steps
- Too few: Looks hasty, lacks depth
- Too many: Overwhelming, loses focus

**Good Sequential Thinking**:
```python
reasoning=[
    "Analyzing Figma file structure",              # Step 1: Analysis
    "No Focus state detected in component",        # Step 2: Finding
    "WCAG 2.4.7 requires visible focus indicators" # Step 3: Requirement
]
```

**Categories for debate thinking**:
- **Investigating**: Initial analysis
- **Questioning**: Raising concerns
- **Analyzing Team Input**: Evaluating contributions
- **Deciding**: Making final decision

### Oracle's Role

Oracle's mission-critical questions **reframe debates** by focusing on:
- Mission success criteria
- User impact
- Ethical considerations
- Long-term consequences

**Example**: Instead of debating technical details, Oracle asks:
> "If a student with disabilities cannot use this, have we succeeded?"

This shifts focus from *"Can we build it faster?"* to *"Are we building the right thing?"*

---

## Integration with Narrator

All debate methods integrate seamlessly with the Mission Control Narrator system:

**Narrator Modes**:
- `narrative` (default): Full debate banter with sequential thinking
- `technical`: Minimal debate output
- `silent`: Debates logged but not displayed
- `debug`: Full debate output + internal logs

**Configure via environment**:
```bash
export NARRATOR_MODE=narrative
```

---

## Testing

### Run Inter-Agent Debate Tests

```bash
cd /Users/admin/Documents/claudecode/Projects/aldo-vision
python3 test_inter_agent_debate.py
```

**Test Coverage**:
- ✅ Accessibility violations debate
- ✅ Methodology selection debate
- ✅ Order questioning debate

**Expected Output**: 3/3 tests passing with full debate banter visible

---

## Benefits of Inter-Agent Debates

### 1. **Better Decisions Through Collaboration**
- Heroes bring diverse expertise (accessibility, design, validation, strategy)
- Multiple perspectives prevent blind spots
- Evidence-based decision making

### 2. **Autonomous Critical Thinking**
- Heroes independently investigate before debating
- Heroes question orders when they have better ideas
- Superman revises decisions based on team expertise

### 3. **Transparent Reasoning Process**
- Sequential thinking shows *why* heroes reach conclusions
- User sees complete debate unfold
- Full audit trail of decision-making process

### 4. **Mission-Critical Framing**
- Oracle's questions ensure focus on what matters
- Debates resolve on mission goals, not technical preferences
- Team alignment on "why" before "how"

### 5. **Learning and Improvement**
- Debates stored in Oracle's knowledge base
- Team learns from past debates
- Future decisions benefit from historical debates

---

## Version History

**v2.0** (2025-10-31):
- Initial Inter-Agent Debate Protocol
- 7 narrator debate methods implemented
- 5 HeroBase convenience methods added
- Full sequential thinking integration
- 3 comprehensive debate test scenarios

---

## Questions?

**Key Principles**:
1. **Question Everything** - Heroes should challenge orders if they have better ideas
2. **Evidence Over Opinion** - Support positions with data and past learnings
3. **Mission First** - Oracle frames debates around mission success
4. **Sequential Thinking** - Show reasoning process (3-7 steps max)
5. **Collaborative Decision** - Superman analyzes all input before deciding

**Golden Rule**: *"My agents fighting with each other"* - productive debate leads to better solutions!

---

**"Superman's orders, investigated independently, debated with each other, and reached a better solution together!"**
