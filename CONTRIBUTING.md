# 🤝 Contributing to Litty - The Conscience Keeper

**Thank you for wanting to make the web more empathetic!** 🪔

Litty is built on empathy, and so is our community. Whether you're adding a new dark pattern, creating a cultural hero, or fixing a typo - **every contribution matters**.

---

## 🌟 Code of Conduct

### Our Values

**Empathy First**: We're building tools that create empathy for users. Treat contributors with the same empathy we show users.

**Cultural Respect**: Litty is a Malayali superhero from Kerala. We celebrate cultural diversity and welcome heroes from ALL cultures.

**Accessibility is Non-Negotiable**: We're fighting for accessibility - our code, documentation, and community must be accessible too.

**No Dark Patterns**: We detect manipulation - we don't practice it. Be honest, transparent, and respectful.

### Expected Behavior

✅ **DO**:
- Assume good intentions
- Provide constructive feedback with empathy
- Credit others for their work
- Welcome newcomers warmly
- Celebrate diverse perspectives
- Make the web better for REAL people

❌ **DON'T**:
- Use offensive language or imagery
- Harass or discriminate against anyone
- Share private information without consent
- Engage in trolling or inflammatory behavior
- Dismiss accessibility concerns
- Treat users as "edge cases"

### Reporting Issues

If you experience or witness unacceptable behavior, please report it by opening an issue or contacting the maintainers directly.

---

## 🚀 Quick Start for Contributors

### 1. Set Up Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/litty-conscience-keeper.git
cd litty-conscience-keeper

# Install dependencies
pip install -r requirements_v2.txt

# Install development dependencies
pip install -r requirements-dev.txt  # pytest, black, mypy, etc.

# Set up pre-commit hooks (optional but recommended)
pre-commit install
```

### 2. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_litty_agent.py -v

# Run with coverage
pytest tests/ --cov=core.justice_league_v2
```

### 3. Test Litty

```bash
# Test in demo mode (no API key needed)
python example_litty_autonomous.py

# Test with real API key
export ANTHROPIC_API_KEY='your-key'
python example_litty_autonomous.py
```

---

## 🎯 Ways to Contribute

### 1. Add More Dark Patterns

**What**: Expand Litty's detection of manipulative design patterns

**How**:
1. Research a dark pattern not yet detected
2. Add to `self.dark_patterns` list in `litty_agent.py`
3. Update `detect_dark_patterns()` tool logic
4. Add test case
5. Document with real-world example

**Example**:
```python
# In litty_agent.py
self.dark_patterns = [
    'confirmshaming',
    'bait_and_switch',
    # ... existing patterns
    'forced_enrollment',  # NEW: Auto-adds items to subscription
]

# Add detection logic
async def detect_dark_patterns(page_content: str, url: str) -> Dict:
    # ... existing logic ...

    # Check for forced enrollment
    if 'automatically added' in page_content.lower():
        patterns.append({
            'type': 'forced_enrollment',
            'severity': 'high',
            'description': 'Items automatically added to subscription'
        })
```

**Documentation**: Add to `LITTY_SNAPSHOT.md` under "Dark Patterns Detected"

### 2. Add More User Personas

**What**: Expand the champions Litty fights for

**How**:
1. Research a user group facing barriers
2. Create persona with realistic details (age, challenges, tech skill)
3. Add to `self.user_personas` in `litty_agent.py`
4. Create guilt trips specific to this persona
5. Add to documentation

**Example**:
```python
# In litty_agent.py __init__()
self.user_personas = {
    'ammachi': {...},
    'priya': {...},
    # ... existing personas
    'stroke_survivor': {
        'name': 'Stroke Survivor (62)',
        'age': 62,
        'challenges': [
            'one-hand navigation',
            'slow typing',
            'fatigue from complex tasks'
        ],
        'tech_skill': 'intermediate',
        'assistive_tech': 'adaptive mouse, voice control'
    }
}
```

### 3. Improve Guilt-Trip Messaging

**What**: Make guilt trips more emotionally effective while staying respectful

**How**:
1. Identify guilt trip that could be stronger
2. Link to specific persona pain point
3. Use cultural phrases appropriately (Kerala Malayalam for Litty)
4. Test emotional impact (does it create empathy?)
5. Ensure it's respectful, not mean

**Guidelines**:
- **Focus on user pain**, not developer blame
- **Be specific**: "Ammachi (72) can't read 10px text" > "Text too small"
- **Show consequence**: "She's getting a headache and giving up"
- **Ask question**: "Is this how you treat grandmothers?"
- **Give solution**: "Increase to 16px minimum"

**Bad Example** ❌:
```python
"You're a terrible developer for using small text!"
```

**Good Example** ✅:
```python
"Eda mone! Ammachi (72) is squinting at your 10px text,
getting a headache. She WANTS to read your content but
you've made it physically painful. Is this how you treat
grandmothers? Increase to 16px minimum."
```

### 4. Add New Cultural Heroes

**What**: Create autonomous agents from other cultures (Japanese, Nigerian, Mexican, etc.)

**How**:
1. Research cultural values and communication style
2. Follow the migration guide: `MIGRATION_GUIDE_V1_TO_V2.md`
3. Create new agent file: `core/justice_league_v2/agents/hero_name_agent.py`
4. Define cultural personas the hero champions
5. Add cultural phrases/expressions
6. Register specialized tools
7. Test thoroughly
8. Document

**Template**:
```python
# core/justice_league_v2/agents/akira_agent.py
class AkiraAgent(AutonomousAgent):
    """
    🇯🇵 Akira - The Cultural Guardian

    Japanese superhero validating cultural appropriateness,
    respect, and inclusive design for Asian markets.
    """

    def __init__(self, api_key=None, **kwargs):
        # Japanese cultural phrases
        self.cultural_phrases = {
            'severe': 'Mottainai! (What a waste!)',
            'high': 'Chotto matte! (Wait a moment!)',
            'medium': 'Sō desu ka? (Is that so?)',
            'low': 'Daijōbu desu (It\'s okay)'
        }

        # User personas for Asian markets
        self.user_personas = {
            'grandparent_tokyo': {...},
            'rural_student': {...},
            # etc.
        }

        super().__init__(
            name="Akira",
            role="The Cultural Guardian",
            expertise="Cultural appropriateness for Asian markets",
            api_key=api_key,
            **kwargs
        )
```

### 5. Build Integrations

**What**: Extend Litty beyond Python (browser extensions, VS Code, Figma, etc.)

**Integration Ideas**:
- **Browser Extension**: Check ethics in real-time while browsing
- **VS Code Extension**: Lint for dark patterns in HTML/CSS
- **Figma Plugin**: Validate designs before handoff
- **GitHub Action**: Ethics checks in CI/CD pipeline
- **Slack Bot**: Get ethics reports in team channels

**Requirements**:
- Must use Litty's Python core (don't reimplement)
- Must maintain empathy-first messaging
- Must be accessible (WCAG 2.1 AA minimum)
- Must document setup clearly

### 6. Improve Documentation

**What**: Make docs clearer, add examples, translate to other languages

**How**:
- Fix typos or unclear explanations
- Add code examples
- Create tutorials or videos
- Translate to other languages (keep Malayalam for Litty!)
- Add diagrams or visuals

**Documentation Files**:
- `OPENSOURCE_README.md` - Main README for open source
- `JUSTICE_LEAGUE_V2_GUIDE.md` - Complete v2.0 guide
- `LITTY_SNAPSHOT.md` - Comprehensive Litty deep-dive
- `MIGRATION_GUIDE_V1_TO_V2.md` - How to build new agents
- `QUICK_REFERENCE_V2.md` - 5-minute overview

### 7. Write Tests

**What**: Increase test coverage and confidence

**How**:
1. Identify untested code paths
2. Write test following pytest conventions
3. Include both success and failure cases
4. Test edge cases
5. Document what you're testing

**Test Structure**:
```python
# tests/test_litty_agent.py
import pytest
from core.justice_league_v2.agents.litty_agent import LittyAgent

class TestLittyAgent:
    @pytest.fixture
    def litty(self):
        """Create Litty instance for testing"""
        return LittyAgent()  # Demo mode

    @pytest.mark.asyncio
    async def test_guilt_trip_for_ammachi(self, litty):
        """Test: Litty generates appropriate guilt trip for Ammachi"""
        result = await litty.execute_tool('generate_guilt_trip', {
            'issue': 'Small text size (10px)',
            'severity': 'severe',
            'affected_persona': 'ammachi'
        })

        assert result['success']
        assert 'Eda mone!' in result['result']['guilt_phrase']
        assert 'Ammachi' in result['result']['persona']

    # Add more tests...
```

---

## 📝 Pull Request Process

### Before Submitting

1. **Run Tests**: `pytest tests/ -v` - All tests must pass
2. **Format Code**: `black core/ tests/` - Consistent style
3. **Type Check**: `mypy core/` - No type errors
4. **Update Docs**: Add/update relevant documentation
5. **Test Example**: Run `python example_litty_autonomous.py`

### PR Template

```markdown
## What does this PR do?

Brief description of changes.

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that breaks existing functionality)
- [ ] Documentation update

## Dark Pattern / Persona / Hero Added (if applicable)

**Name**: [Dark pattern name / Persona name / Hero name]
**Description**: [What it detects / Who it represents / What it does]
**Real-world example**: [Link or description]

## Testing

- [ ] Tests pass locally (`pytest tests/ -v`)
- [ ] Formatted code (`black core/ tests/`)
- [ ] Type checked (`mypy core/`)
- [ ] Tested example (`python example_litty_autonomous.py`)
- [ ] Added new tests for new functionality

## Empathy Check

- [ ] Creates empathy for real users
- [ ] Doesn't blame developers (focuses on user pain)
- [ ] Culturally respectful
- [ ] Accessibility considered

## Screenshots (if applicable)

[Add screenshots of new features, guilt trips, or reports]

## Related Issues

Closes #[issue number]

## Additional Context

[Any other context about the PR]
```

### Review Process

1. **Automated Checks**: CI runs tests, linting, type checking
2. **Code Review**: Maintainer reviews for quality and empathy
3. **Testing**: Maintainer tests locally
4. **Feedback**: Address any requested changes
5. **Merge**: Approved PRs merged to main

---

## 🎨 Style Guide

### Python Code Style

**Use Black formatter** (run `black .` before committing):
```python
# Good ✅
def generate_guilt_trip(issue: str, severity: str, persona: str) -> Dict:
    """Generate empathetic guilt trip message."""
    return {
        'guilt_phrase': phrase,
        'persona': persona_name
    }

# Bad ❌ (inconsistent spacing, no types)
def generate_guilt_trip(issue,severity,persona):
    return {"guilt_phrase":phrase,"persona":persona_name}
```

**Use Type Hints**:
```python
# Good ✅
async def analyze(self, url: str, options: Dict[str, Any]) -> Dict[str, Any]:
    pass

# Bad ❌
async def analyze(self, url, options):
    pass
```

**Write Descriptive Names**:
```python
# Good ✅
affected_persona = 'ammachi'
guilt_phrase_for_elderly = self.guilt_phrases['severe']

# Bad ❌
p = 'ammachi'
g = self.guilt_phrases['severe']
```

### Documentation Style

**Use Clear Examples**:
```python
# Good ✅
"""
Generate guilt trip for ethical violations.

Args:
    issue: "Small text size (10px)"
    severity: "severe" (severe|high|medium|low)
    affected_persona: "ammachi" (which user persona is affected)

Returns:
    {
        'guilt_phrase': 'Eda mone!',
        'persona': 'Ammachi (Grandma)',
        'message': 'Full guilt trip message...'
    }

Example:
    >>> result = await litty.execute_tool('generate_guilt_trip', {
    ...     'issue': 'Small text',
    ...     'severity': 'severe',
    ...     'affected_persona': 'ammachi'
    ... })
    >>> print(result['guilt_phrase'])
    'Eda mone!'
"""
```

### Guilt Trip Style

**Structure**:
1. **Malayalam phrase** (sets emotional tone)
2. **Persona + specific pain** (creates empathy)
3. **Consequence** (shows impact)
4. **Question** (prompts reflection)
5. **Fix** (gives actionable solution)

**Example**:
```
Eda mone! [Malayalam phrase]

Ammachi (72) is squinting at your 10px text, getting a headache. [Persona + pain]

She WANTS to read your content but you've made it physically painful. [Consequence]

Is this how you treat grandmothers? [Question]

Increase font-size to 16px minimum. [Fix]
```

---

## 🐛 Reporting Bugs

### Before Reporting

1. **Search existing issues**: Your bug might already be reported
2. **Test with latest version**: Update to latest commit
3. **Try demo mode**: Test without API key to isolate issue

### Bug Report Template

```markdown
## Bug Description

Clear description of the bug.

## Steps to Reproduce

1. Step 1
2. Step 2
3. Step 3

## Expected Behavior

What you expected to happen.

## Actual Behavior

What actually happened.

## Environment

- OS: [e.g., macOS 13.0, Ubuntu 22.04]
- Python Version: [e.g., 3.9.7]
- Litty Version: [e.g., v2.0.0-alpha]
- API Key Set: [Yes/No (demo mode)]

## Error Output

```
Paste full error traceback here
```

## Additional Context

Screenshots, links, or other context.
```

---

## 💡 Feature Requests

### Feature Request Template

```markdown
## Feature Description

Clear description of the feature.

## User Impact

Who benefits from this feature?
- [ ] Ammachi (elderly users)
- [ ] Priya (screen reader users)
- [ ] Kuttan Uncle (aging users)
- [ ] Village Teacher (budget-conscious users)
- [ ] Dyslexic Student (learning differences)
- [ ] Other: [describe]

## Example Use Case

Real-world scenario where this feature helps.

## Proposed Implementation

How might this be implemented? (Optional)

## Empathy Check

How does this create empathy for users?
```

---

## 🌍 Translation Guidelines

### Translating Documentation

**What to Translate**:
- README files
- User-facing messages
- Error messages
- Examples in documentation

**What NOT to Translate**:
- Code comments (keep English for international contributors)
- Variable names
- Litty's Malayalam phrases (they're part of her cultural identity!)
- Technical terms (dark pattern names, WCAG references)

**How to Translate**:
1. Create new file: `OPENSOURCE_README.{language_code}.md` (e.g., `OPENSOURCE_README.ja.md` for Japanese)
2. Translate with cultural sensitivity
3. Keep code examples in original language
4. Add note at top: "This is a community translation. For the official English version, see OPENSOURCE_README.md"
5. Submit PR with translation

### Adding Cultural Heroes (Different Languages)

**Respect Cultural Authenticity**:
- Research the culture deeply
- Consult with native speakers
- Use authentic phrases (not Google Translate!)
- Represent cultural values accurately
- Avoid stereotypes

**Example**:
- Litty uses Malayalam because she's from Kerala
- A Japanese hero should use Japanese expressions
- A Nigerian hero should represent Nigerian values
- Each hero should champion personas from their culture

---

## ❓ Questions?

**Have questions about contributing?**

- 📖 Read the docs: `JUSTICE_LEAGUE_V2_GUIDE.md`
- 💬 Open a discussion in GitHub Discussions
- 🐛 Found a bug? Open an issue
- 💡 Have an idea? Create a feature request

**Want to chat?**

We're building a community of empathy-driven developers! Join us and let's make the web accessible together.

---

## 🙏 Thank You!

**Every contribution makes the web more empathetic.**

Whether you're:
- Adding a dark pattern detection
- Creating a cultural hero
- Fixing a typo
- Suggesting an improvement
- Sharing Litty with others

**You're making a difference.** 🪔

*"Eda mone! Together, we'll create a web that respects ALL users!"*

---

**Contributing to Litty - The Conscience Keeper**
**Because empathy is not optional. ❤️**
