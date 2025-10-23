---
description: Validate user empathy and ethical design with guilt-tripping (Litty - The Conscience Keeper)
---

# 🪔 Litty - The Conscience Keeper

**Hero #13 in the Justice League**

## Overview

Litty is a Malayali superhero from Kerala, India who uses the ancient art of guilt-tripping to make developers aware of the real-world impact of their design decisions on actual users. She focuses on user empathy, ethical design patterns, and inclusive experiences.

**Catchphrase**: "Eda mone! Do you know how your ammachi (grandma) would struggle with this? Think about the users, not just the code!"

## Powers

### 🕵️ Guilt-Tripping Vision
Spots unethical and manipulative design patterns that harm users:
- Dark patterns (confirmshaming, hidden costs, urgency manipulation)
- Deceptive UI elements
- Cookie consent manipulation
- Forced continuity and obstruction

### 💝 Empathy Inducement
Makes developers feel the pain of real users through:
- User persona stories (ammachi, visually impaired users, elderly, rural users)
- Real-world impact narratives
- Consequences of poor design choices
- Emotional connection to user struggles

### ⚖️ Ethical Validation
Analyzes design ethics across 6 dimensions:
1. **Dark Patterns Detection** - Manipulative/deceptive patterns
2. **Inclusive Design** - Accessibility for ALL users
3. **Cognitive Load** - Interface complexity and overwhelm
4. **User Respect** - Respecting time, attention, and autonomy
5. **Accessibility Empathy** - Quality of accessibility implementation
6. **Ethical Language** - Inclusive, respectful communication

### 📖 User Story Generation
Creates empathy-driven user stories:
- "As [persona], I want [need], but I can't because [your issue]"
- Highlights impact on real people
- Connects technical decisions to human consequences

### 🇮🇳 Malayali Wisdom
Incorporates Kerala cultural phrases for maximum guilt-trip impact:
- "Eda mone!" (Oh dear!)
- "Enthina ithoke?" (Why do this?)
- "Shari aylaa mone" (This won't do)
- "നല്ലത്!" (Nallathu - Good!)
- Malayalam proverbs and wisdom

## Technical Specifications

### Function
```python
from core.justice_league import litty_validate_ethics

result = litty_validate_ethics(
    url="https://example.com",
    mcp_tools={
        'evaluate_script': mcp_evaluate_script,
        'take_screenshot': mcp_take_screenshot
    }
)
```

### Required MCP Tools
- `evaluate_script` - Execute JavaScript for analysis
- `take_screenshot` - Capture screenshots for evidence

### Return Structure
```python
{
    'hero': 'Litty',
    'emoji': '🪔',
    'title': 'The Conscience Keeper',
    'url': str,
    'timestamp': str (ISO format),
    'ethics_score': int (0-100),
    'grade': str ('S+', 'S', 'A', 'B', 'C', 'D', 'F'),
    'checks': {
        'dark_patterns': {...},
        'inclusive_design': {...},
        'cognitive_load': {...},
        'user_respect': {...},
        'accessibility_empathy': {...},
        'ethical_language': {...}
    },
    'guilt_trips': List[str],  # Guilt-inducing messages
    'user_stories': List[Dict],  # Empathy-driven stories
    'recommendations': List[str],  # Actionable advice with Malayali wisdom
    'litty_says': str,  # Litty's final verdict
    'passed': int,  # Number of checks passed
    'total': int  # Total checks (6)
}
```

## What Litty Checks

### 1. Dark Patterns Detection (🕵️)

**Checks for**:
- **Confirmshaming**: "No thanks, I don't want to save money"
- **Hidden Costs**: Surprise fees at checkout
- **Urgency Manipulation**: "Only 2 left! 5 people viewing!"
- **Forced Continuity**: Hard to cancel subscriptions
- **Obstruction**: Hidden cancel/unsubscribe links
- **Misdirection**: Pre-checked opt-in checkboxes
- **Bait and Switch**: Changed terms after signup

**Scoring**:
- 0 dark patterns: 100 points ✅
- Each dark pattern: -20 points
- 3+ dark patterns: Critical failure

**Guilt Trip Example**:
> "Eda mone! You have 3 dark patterns manipulating users! Would you want your ammachi (grandma) to be tricked like this?"

---

### 2. Inclusive Design (👵)

**Checks for**:
- **Touch Target Sizes**: Minimum 44x44px (WCAG AAA)
- **Font Sizes**: Minimum 16px for body text
- **Complex Language**: Technical jargon, long words
- **Color Contrast**: WCAG requirements
- **Motor Accessibility**: Large enough for shaky hands

**User Personas Considered**:
- Ammachi (Grandma, 72) - Vision issues, trembling hands
- Kuttan Uncle (68) - Tech novice, fear of mistakes
- Rural users - Small screens, basic literacy
- Users with dyslexia - Need simple language

**Scoring**:
- < 5 issues: Pass ✅
- Each issue: -5 points
- 10+ issues: Critical failure

**Guilt Trip Example**:
> "Enthina ithoke? (Why do this?) You have 12 issues making it hard for elderly people. Think about Kuttan Uncle trying to click your tiny buttons with his shaky hands!"

---

### 3. Cognitive Load (🧠)

**Checks for**:
- **Too Many Choices**: 50+ interactive elements (paradox of choice)
- **Complex Navigation**: 15+ navigation items
- **Unclear Primary Action**: 5+ prominent CTAs
- **Information Overload**: Walls of text (200+ words)
- **Visual Complexity**: Too many elements on screen

**Scoring**:
- 0 issues: 100 points ✅
- Each issue: -25 points
- 2+ issues: Failure

**Guilt Trip Example**:
> "Shari aylaa mone (This won't do)! Your interface is so complex. My ammachi would give up after 30 seconds!"

---

### 4. User Respect (🙏)

**Checks for**:
- **Auto-playing Media**: Videos/audio without user consent
- **Excessive Pop-ups**: 3+ modals/overlays
- **Cookie Dark Patterns**: Only "Accept" button, no "Decline"
- **Forced Registration**: Content locked behind signup walls
- **Attention Hijacking**: Interrupts and distractions

**Scoring**:
- 0 disrespects: 100 points ✅
- Each disrespect: -25 points
- 2+ disrespects: Failure

**Guilt Trip Example**:
> "Eda mone! You're disrespecting users with auto-playing videos and forced pop-ups. Would YOU tolerate this?"

---

### 5. Accessibility Empathy (♿)

**Checks for**:
- **Alt Text Quality**: Meaningful descriptions (not just "image")
- **ARIA Label Quality**: Descriptive labels (not just "button")
- **Skip Links**: Navigation shortcuts for keyboard users
- **Focus Indicators**: Visible focus states
- **Empathetic Implementation**: Accessibility with thought, not checkboxes

**User Persona**:
- Priya (35, screen reader user) - Needs meaningful alt text

**Scoring**:
- < 3 issues: Pass ✅
- Each issue: -10 points
- 10+ issues: Critical failure

**Guilt Trip Example**:
> "You have 8 accessibility issues with no empathy! Priya uses a screen reader and your alt text just says 'image'. How is that helpful?"

---

### 6. Ethical Language (💬)

**Checks for**:
- **Gendered Language**: "guys", "mankind", "manpower"
- **Ableist Language**: "crazy", "insane", "dumb", "stupid", "lame"
- **Violent Metaphors**: "kill", "destroy", "crush", "annihilate"
- **Respectful Error Messages**: Blame-free, helpful

**Scoring**:
- < 5 issues: Pass ✅
- Each issue: -10 points
- 5+ issues: Failure

**Recommendation Example**:
> "💬 Use inclusive language. Say 'everyone' instead of 'guys', 'unexpected' instead of 'crazy'."

---

## Scoring System

### Overall Ethics Score (0-100)

Calculated as: `(passed_checks / 6) × 100`

**Grade Scale**:
- **S+ (95-100)**: Perfect empathy! Ammachi would be proud! 🪔✨
- **S (90-94)**: Excellent user consideration
- **A (80-89)**: Good, but room for improvement
- **B (70-79)**: Acceptable, needs work
- **C (60-69)**: Many users struggling
- **D (50-59)**: Half your users can't use this
- **F (0-49)**: Terrible! Ammachi is crying! 😢

---

## User Story Generation

Litty generates empathy-driven user stories for failed checks:

### Format
```python
{
    'persona': 'Ammachi (Grandma)',
    'age': 72,
    'story': (
        "As a 72-year-old grandmother, I want to buy festival sarees online, "
        "but I can't because the buttons are too small and the text is tiny. "
        "I gave up and called my grandson instead."
    ),
    'impact': 'Lost sale, frustrated user, asks family for help'
}
```

### Personas Used
1. **Ammachi (Grandma, 72)** - Vision issues, tech struggles
2. **Priya (Screen Reader User, 35)** - Needs semantic HTML
3. **Kuttan Uncle (68)** - Tech novice, fears mistakes
4. **Village School Teacher (45)** - Slow internet, basic tech
5. **Student with Dyslexia (19)** - Needs readable design

---

## Recommendations

Litty provides actionable recommendations with Malayalam wisdom:

### Examples

**Dark Patterns**:
> "🙏 Remove dark patterns - Be honest and transparent. Like we say in Malayalam: 'സത്യം പറ' (Sathyam para - Speak truth). Your users will trust you more."

**Inclusive Design**:
> "👵 Make buttons at least 44x44px and text at least 16px. Think: 'Could my ammachi use this with her reading glasses?'"

**Cognitive Load**:
> "🧠 Simplify your interface. Follow the Malayalam principle: 'എളുപ്പം ആക്കുക' (Eluppam akkuka - Make it simple). One clear primary action, less clutter."

**User Respect**:
> "🙏 Respect users' time and attention. Treat users like you'd treat guests in your home (മെഹ്മാൻ - Mehman)."

---

## Example Output

```python
{
    'hero': 'Litty',
    'emoji': '🪔',
    'ethics_score': 65,
    'grade': 'C',
    'passed': 3,
    'total': 6,
    'checks': {
        'dark_patterns': {'passed': False, 'dark_patterns_found': 3},
        'inclusive_design': {'passed': False, 'issues_found': 12},
        'cognitive_load': {'passed': True, 'issues': []},
        'user_respect': {'passed': True, 'disrespects_found': 0},
        'accessibility_empathy': {'passed': False, 'issues_found': 8},
        'ethical_language': {'passed': True, 'issues_found': 2}
    },
    'guilt_trips': [
        "Eda mone! You have 3 dark patterns manipulating users! Would you want your ammachi to be tricked like this?",
        "Enthina ithoke? You have 12 issues making it hard for elderly people. Think about Kuttan Uncle!",
        "You have 8 accessibility issues with no empathy! Priya's screen reader just hears 'image'."
    ],
    'user_stories': [
        {
            'persona': 'Ammachi (Grandma)',
            'age': 72,
            'story': 'As a 72-year-old grandmother, I want to buy sarees online, but I can\'t because buttons are too small...',
            'impact': 'Lost sale, frustrated user'
        }
    ],
    'recommendations': [
        "🙏 Remove dark patterns - Be honest. 'സത്യം പറ' (Speak truth)",
        "👵 Make buttons 44x44px. Think: 'Could my ammachi use this?'",
        "♿ Write meaningful alt text. Describe your site like over the phone."
    ],
    'litty_says': "ഇത് എന്താണ് ഇതിന്റെ അവസ്ഥ? Half your users are struggling! Do better!"
}
```

---

## Usage Examples

### Example 1: Quick Ethics Check
```python
from core.justice_league import litty_validate_ethics

# Validate ethics
result = litty_validate_ethics(
    url="https://example.com",
    mcp_tools=mcp_tools
)

print(f"Ethics Score: {result['ethics_score']}/100 ({result['grade']})")
print(f"\nLitty says: {result['litty_says']}")

# Show guilt trips
if result['guilt_trips']:
    print("\n🪔 Guilt Trips:")
    for guilt in result['guilt_trips']:
        print(f"  - {guilt}")
```

### Example 2: User Story Analysis
```python
result = litty_validate_ethics(url, mcp_tools)

# Show user stories for empathy
print("\n📖 User Stories:")
for story in result['user_stories']:
    print(f"\n{story['persona']} ({story['age']} years old):")
    print(f"  {story['story']}")
    print(f"  Impact: {story['impact']}")
```

### Example 3: Comprehensive Ethics Report
```python
result = litty_validate_ethics(url, mcp_tools)

print(f"\n🪔 Litty's Ethics Report")
print(f"Score: {result['ethics_score']}/100 ({result['grade']})")
print(f"Passed: {result['passed']}/{result['total']} checks\n")

# Show each check
for check_name, check_result in result['checks'].items():
    status = "✅" if check_result['passed'] else "❌"
    print(f"{status} {check_name.replace('_', ' ').title()}: {check_result['score']}/100")

# Show recommendations
print("\n💡 Recommendations:")
for rec in result['recommendations']:
    print(f"  {rec}")

# Litty's verdict
print(f"\n{result['emoji']} Litty says:")
print(f"  {result['litty_says']}")
```

---

## Integration with Justice League

### Superman Coordinator Integration

Litty automatically runs when Superman assembles the Justice League:

```python
from core.justice_league import assemble_justice_league

mission = {
    'url': 'https://example.com',
    'options': {
        'test_interactive': True,
        'validate_ethics': True,  # ← Enable Litty
        'all': True
    }
}

results = assemble_justice_league(mission, mcp_tools)

# Litty's results
litty_results = results['heroes']['litty']
print(f"Ethics Score: {litty_results['ethics_score']}/100")
```

### Heroes Litty Complements

**Wonder Woman (Accessibility)**:
- Wonder Woman checks WCAG compliance
- Litty checks if accessibility is implemented with empathy

**Martian Manhunter (Security)**:
- Martian Manhunter checks OWASP vulnerabilities
- Litty checks ethical security practices (no dark patterns)

**Plastic Man (Responsive)**:
- Plastic Man checks breakpoints
- Litty checks if design works for elderly users on small screens

**Zatanna (SEO)**:
- Zatanna checks meta tags
- Litty checks ethical content and language

---

## Strengths

1. ✅ **Unique Perspective**: Only hero focused on user empathy and ethics
2. ✅ **Dark Pattern Detection**: Identifies 15+ manipulative patterns
3. ✅ **User Story Generation**: Creates emotional connection to users
4. ✅ **Inclusive Design Focus**: Considers elderly, disabled, rural users
5. ✅ **Guilt-Tripping**: Makes developers actually care about users
6. ✅ **Cultural Wisdom**: Incorporates Malayali sayings and principles
7. ✅ **Comprehensive**: 6 dimensions of ethical design
8. ✅ **Actionable**: Provides clear recommendations with cultural context

---

## Weaknesses Eliminated

1. ❌ ~~Cannot detect subtle dark patterns~~
   - ✅ **Fixed**: Checks 6 categories of dark patterns with heuristics

2. ❌ ~~No user persona consideration~~
   - ✅ **Fixed**: 5 detailed user personas with specific needs

3. ❌ ~~Generic accessibility checks~~
   - ✅ **Fixed**: Empathy-focused checks (alt text quality, not just presence)

4. ❌ ~~No cultural perspective~~
   - ✅ **Fixed**: Malayalam phrases, Kerala cultural wisdom integrated

---

## Best Practices

### When to Deploy Litty

**Always**:
- Consumer-facing products
- Government services
- Healthcare applications
- Financial services
- E-commerce sites

**Especially Important**:
- Products targeting elderly users
- Accessibility-critical applications
- Products used in rural/developing areas
- Educational platforms
- Social impact projects

### Interpreting Results

**Score 90+**: Ship it! You're thinking about users! 🎉

**Score 70-89**: Good foundation, fix the guilt trips

**Score 50-69**: Major empathy gaps, significant rework needed

**Score < 50**: Ammachi is crying! Complete redesign required 😢

### Acting on Guilt Trips

Litty's guilt trips are meant to:
1. Create emotional connection to real users
2. Highlight real-world consequences
3. Motivate empathetic design decisions
4. Make you think: "Would my ammachi struggle with this?"

**Don't ignore them** - they represent real user pain!

---

## Litty's Philosophy

> "Technology should serve people, not trick them.
> Good design makes everyone feel welcome.
> If your ammachi can't use it, it's not ready.
> സത്യം പറ (Speak truth), respect users."

---

## Malayalam Phrases Reference

- **Eda mone!** - "Oh dear!" (expression of concern)
- **Enthina ithoke?** - "Why do this?" (questioning poor choices)
- **Shari aylaa mone** - "This won't do" (gentle criticism)
- **Kozhapamilla** - "No problem" (all good)
- **നല്ലത്! (Nallathu)** - "Good!" (praise)
- **സത്യം പറ (Sathyam para)** - "Speak truth" (be honest)
- **എളുപ്പം ആക്കുക (Eluppam akkuka)** - "Make it simple"
- **മെഹ്മാൻ (Mehman)** - "Guest" (treat with respect)
- **Ammachi** - Grandmother
- **Kuttan Uncle** - Affectionate term for elderly man

---

**Remember**: Litty guilt-trips you because she cares about users! 🪔

Every guilt trip is a real user's pain point.
Every user story is someone who couldn't use your product.
Every recommendation is a path to more empathetic design.

**Would your ammachi be proud of this design?** ❤️
