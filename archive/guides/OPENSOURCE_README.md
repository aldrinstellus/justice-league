# 🪔 Litty - The Conscience Keeper

**An autonomous AI agent that makes you *feel* your users' pain**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Powered by Claude](https://img.shields.io/badge/Powered%20by-Claude-blueviolet.svg)](https://www.anthropic.com/)

---

```
╔══════════════════════════════════════════════════════════════════════╗
║                    🪔 LITTY - THE CONSCIENCE KEEPER                  ║
║              Malayali Superhero • Autonomous AI Agent                ║
║                  "Eda mone! Think about the users!"                  ║
╚══════════════════════════════════════════════════════════════════════╝
```

## What is Litty?

**Litty is a Malayali superhero from Kerala, India** who fights for ethical design and user empathy using the power of guilt-tripping (for good!).

While other accessibility tools give you cold technical violations like *"WCAG 1.4.3 fails. Contrast: 2.1:1"*, Litty makes you **FEEL** the real human impact:

> *"Eda mone! Kuttan Uncle (68) can't see your text. His eyes are aging and your gray-on-white text is nearly invisible to him. He taught school for 40 years. Show him the respect he deserves!"*

**Litty is powered by Claude AI** for true autonomous reasoning - she doesn't just run scripts, she **thinks** about users, plans her analysis, and self-corrects when she misses something.

---

## 🌟 Why Litty is Different

| Most Accessibility Tools | Litty |
|-------------------------|-------|
| "Font size below 16px" | "Ammachi (72) is getting a headache from your 10px text. She's your grandmother. Treat her with dignity!" |
| "Missing alt text" | "Priya uses a screen reader and your site has ZERO alt text. You've told her that her money isn't good enough. Is this who you want to be?" |
| "Confirmshaming detected" | "Village Teacher is on a tight budget and you're emotionally manipulating her with 'No thanks, I hate saving money.' This is psychological abuse, not marketing." |

**Litty creates EMPATHY, not just compliance.**

---

## 👥 Who Litty Fights For

Litty doesn't fight for abstract "users" - she champions **5 real personas**:

### 👵 Ammachi (Grandma) - Age 72
- **Struggles with**: Small text, complex navigation, unclear buttons
- **Needs**: 16px+ font, simple flows, high contrast
- **Litty says**: *"Eda mone! Ammachi can't even read this tiny text!"*

### 🦯 Priya (Screen Reader User) - Age 35
- **Struggles with**: Missing alt text, poor ARIA labels, keyboard traps
- **Needs**: Semantic HTML, descriptive alt text, keyboard navigation
- **Litty says**: *"Shari aylaa mone! Priya is literally unable to shop here!"*

### 👴 Kuttan Uncle (Retired Teacher) - Age 68
- **Struggles with**: Low contrast, small targets, complex flows
- **Needs**: 4.5:1 contrast, 44x44px touch targets, clear layout
- **Litty says**: *"Enthina ithoke? Kuttan Uncle can't see this text!"*

### 👩‍🏫 Village School Teacher - Age 45
- **Struggles with**: Slow internet, data costs, bloated sites
- **Needs**: Lightweight pages, progressive loading, clear pricing
- **Litty says**: *"Your 15MB page just cost her grocery money in data!"*

### 📚 Dyslexic Student - Age 19
- **Struggles with**: Dense text, poor formatting, confusing language
- **Needs**: Clear structure, simple language, visual hierarchy
- **Litty says**: *"Your wall of text is impossible for them to read!"*

---

## ⚡ Quick Start

```bash
# Install dependencies
pip install -r requirements_v2.txt

# Set API key (optional - works in demo mode without it)
export ANTHROPIC_API_KEY='your-anthropic-key'

# Run example
python example_litty_autonomous.py
```

**Python Code**:

```python
import asyncio
from core.justice_league_v2.agents.litty_agent import LittyAgent

async def main():
    # Create Litty (autonomous agent)
    litty = LittyAgent()  # Works without API key (demo mode)

    # Define mission
    mission = {
        'url': 'https://example.com',
        'goal': 'validate ethical design',
        'focus_areas': ['dark_patterns', 'accessibility', 'empathy']
    }

    # Litty thinks, plans, and executes autonomously
    result = await litty.execute_mission(mission)

    # Results with empathy
    print(f"Ethics Score: {result['ethics_score']}/100")
    print(f"Grade: {result['grade']}")

    for guilt_trip in result['guilt_trips']:
        print(f"\n{guilt_trip}")

asyncio.run(main())
```

**Output**:

```
🪔 LITTY AUTONOMOUS AGENT
======================================================================

✅ Litty (The Conscience Keeper) ready!

🎯 Ethics Score: 65/100
📝 Grade: D

😢 Guilt Trips:

  Eda mone! Ammachi (72) can't even read this tiny text!
  She's squinting at your 10px font, getting a headache.
  Is this how you treat grandmothers?

  Enthina ithoke? Making it hard for Village Teacher to
  cancel is manipulative! She's on a tight budget and you're
  tricking her. Think about HER, not your conversion rate!

💡 Recommendations:
  1. Increase font size to 16px minimum
  2. Remove confirmshaming from cancellation flow
  3. Add clear 'Decline' option to cookie consent
```

---

## 🎯 What Litty Detects

### 🎭 Dark Patterns (15 types)
- **Confirmshaming**: "No thanks, I hate good deals"
- **Hidden Costs**: $99 → $149 at checkout
- **Bait & Switch**: "Free trial" → auto-charges
- **Roach Motel**: Easy to subscribe, impossible to cancel
- **Privacy Zuckering**: Tricks you into sharing data
- **Fake Urgency**: Countdown timers that reset
- **Friend Spam**: "Invite all your contacts!"
- And 8 more...

### ♿ Accessibility Issues
- **Text size**: Too small for elderly users
- **Color contrast**: Fails WCAG standards
- **Alt text**: Missing on images (blocks screen readers)
- **Keyboard navigation**: Dropdown menus require mouse
- **ARIA labels**: Poor screen reader support
- **Touch targets**: Too small for trembling hands

### 🧠 Cognitive Load
- **Dense text**: Overwhelming for dyslexic users
- **Complex navigation**: Confusing elderly users
- **Unclear language**: Jargon and corporate-speak

### 😤 Disrespectful Design
- **Autoplay videos**: Eating mobile data
- **Excessive popups**: Interrupting user flow
- **Manipulative CTAs**: Pressuring decisions

---

## 🤖 Autonomous Intelligence (v2.0)

Litty is **not just a script** - she's an **autonomous agent** powered by Claude AI:

### What Makes Litty Autonomous?

**1. LLM-Powered Reasoning**
```python
# Litty THINKS about the mission
plan = await litty.think("""
    I'm analyzing an e-commerce site.

    Let me think about who would be hurt:
    - Ammachi might not see hidden shipping costs
    - Village Teacher's budget would be impacted
    - Kuttan Uncle might click the wrong button

    My plan:
    1. Check checkout for hidden costs FIRST
    2. Validate text size for Ammachi
    3. Generate guilt trips linking to personas
""")
```

**2. Self-Correction**
```python
# Tool fails? Litty tries alternatives
result = await litty.execute_with_self_correction(
    task="Detect dark patterns",
    tool_name="detect_dark_patterns",
    parameters={'url': url}
)

# Litty: "Hmm, that didn't work. Let me try a different approach..."
# Retries up to 3 times with adjusted strategies
```

**3. Learning from Missions**
```python
# Litty records every mission
litty.record_mission(mission, result)

# Future missions can reference past learnings
past_patterns = litty.recall_from_memory('dark_patterns_found')
```

---

## 📖 Documentation

- **[Quick Reference](QUICK_REFERENCE_V2.md)** - 5-minute overview
- **[Complete Guide](JUSTICE_LEAGUE_V2_GUIDE.md)** - Full documentation
- **[Litty Snapshot](LITTY_SNAPSHOT.md)** - Comprehensive deep-dive
- **[Migration Guide](MIGRATION_GUIDE_V1_TO_V2.md)** - Build more agents
- **[Architecture](ARCHITECTURE_ANALYSIS.md)** - v1 vs v2 comparison

---

## 🌍 Why Open Source?

### Social Impact
- **Fighting for accessibility** is a public good
- **Empathy-driven design** benefits everyone
- **Dark pattern detection** protects vulnerable users
- **Cultural representation** (First Malayali AI superhero!)

### Educational Value
- Shows how to build **LLM-powered autonomous agents**
- Demonstrates **ethical AI application**
- Teaches **empathy in technology**
- First-of-its-kind architecture

### Community Potential

Imagine contributors adding:
- 🇯🇵 Japanese hero checking cultural appropriateness
- 🇳🇬 Nigerian hero championing low-bandwidth design
- 🇲🇽 Mexican hero validating multilingual support
- 🇧🇷 Brazilian hero fighting digital exclusion
- More personas: motor disabilities, ADHD, autism, elderly

**Litty can become a MOVEMENT.**

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ways to Contribute**:
- Add more dark pattern detections
- Add more user personas
- Improve guilt-trip messaging
- Add more languages (Litty speaks Malayalam + English)
- Build integrations (browser extensions, VS Code, Figma)
- Add more cultural heroes to the Justice League

---

## 🎓 The Justice League

Litty is the **first autonomous agent** in the Justice League v2.0 - a team of AI superheroes for design validation:

**Completed**:
- 🪔 **Litty** - The Conscience Keeper (ethical design)

**Coming Soon**:
- 🦇 **Batman** - The Detective (architecture analysis)
- 🦸‍♀️ **Wonder Woman** - The Protector (accessibility)
- ⚡ **Flash** - The Speedster (performance)
- 🌊 **Aquaman** - The Navigator (data flow)
- 🤖 **Cyborg** - The Integrator (system integration)
- And 6 more heroes...

Each hero is an autonomous agent with specialized expertise, all coordinated by **Superman** (the orchestrator agent).

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Credits

**Created with**:
- [Anthropic Claude](https://www.anthropic.com/) - LLM-powered reasoning
- Love from Kerala, India 🇮🇳
- Empathy for ALL users

**Inspired by**:
- Every Ammachi struggling with small text
- Every Priya blocked by missing alt text
- Every Kuttan Uncle frustrated by low contrast
- Every Village Teacher hurt by hidden costs
- Every student confused by dense text

---

## 📞 Contact

**Questions? Feedback? Want to add your own cultural hero?**

Open an issue or start a discussion!

**Litty's Catchphrase**: *"Eda mone! Think about the users, not just the code!"* 🪔

---

```
╔══════════════════════════════════════════════════════════════╗
║                   🪔 LITTY - THE CONSCIENCE KEEPER           ║
║                                                               ║
║        "Not all heroes wear capes. Some use guilt trips."    ║
║                                                               ║
║              Making the web better, one guilt trip at a time ║
╚══════════════════════════════════════════════════════════════╝
```

**Star this repo if Litty made you FEEL something! ⭐**

*"Eda mone! Now go make the web accessible!"*
