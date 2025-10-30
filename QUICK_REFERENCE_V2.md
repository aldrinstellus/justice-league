# ⚡ Justice League v2.0 - Quick Reference Card

**For Developers: 5-Minute Overview**

---

## 🎯 What Is This?

Justice League v2.0 = **Autonomous agents** with **LLM-powered reasoning** for design validation.

**v1.4.0 (Production)**: Static Python classes with hardcoded logic
**v2.0 (Development)**: Autonomous agents that think, plan, and self-correct

---

## 🚀 Quick Start

### Installation

```bash
cd /Users/admin/Documents/claudecode/Projects/aldo-vision
pip3 install -r requirements_v2.txt
export ANTHROPIC_API_KEY='your-key-here'  # Optional for demo mode
```

### Run Example

```bash
python3 example_litty_autonomous.py
```

**Expected**: Litty executes autonomous mission with LLM reasoning (or demo mode)

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `JUSTICE_LEAGUE_V2_GUIDE.md` | 📚 **READ THIS FIRST** - Complete v2.0 guide |
| `MIGRATION_GUIDE_V1_TO_V2.md` | 🔄 Step-by-step hero conversion guide |
| `V2_COMPLETION_SUMMARY.md` | ✅ Phase 1 & 2 completion report |
| `core/justice_league_v2/base/autonomous_agent.py` | 🏗️ Base class for all agents |
| `core/justice_league_v2/agents/litty_agent.py` | 🪔 Litty pilot implementation |
| `example_litty_autonomous.py` | 💡 Working example code |
| `requirements_v2.txt` | 📦 v2.0 dependencies |

---

## 🦸 Agent Conversion Status

| Hero | Status | Priority |
|------|--------|----------|
| 🪔 **Litty** | ✅ Complete | Pilot |
| 🦇 **Batman** | ⏳ Next | 1 |
| 🦸‍♀️ **Wonder Woman** | ⏳ Pending | 2 |
| ⚡ **Flash** | ⏳ Pending | 3 |
| 🌊 **Aquaman** | ⏳ Pending | 4 |
| 🤖 **Cyborg** | ⏳ Pending | 5 |
| ⚛️ **Atom** | ⏳ Pending | 6 |
| 🏹 **Green Arrow** | ⏳ Pending | 7 |
| 👽 **Martian Manhunter** | ⏳ Pending | 8 |
| 🧪 **Plastic Man** | ⏳ Pending | 9 |
| 🎩 **Zatanna** | ⏳ Pending | 10 |
| 💚 **Green Lantern** | ⏳ Pending | 11 |
| 🦸 **Superman** | ⏳ Last | Orchestrator |

**Progress**: 1/13 (7.7%) - **Next: Batman**

---

## 💻 Code Patterns

### Create Agent

```python
from core.justice_league_v2.agents.litty_agent import LittyAgent

# With API key
litty = LittyAgent(api_key='sk-ant-...')

# Demo mode (no key needed)
litty = LittyAgent()
```

### Execute Mission

```python
mission = {
    'url': 'https://example.com',
    'goal': 'validate ethical design',
    'focus_areas': ['dark_patterns', 'accessibility']
}

result = await litty.execute_mission(mission)

print(f"Score: {result['ethics_score']}/100")
print(f"Reasoning: {result['agent_reasoning']}")
```

### Agent Thinks

```python
thought = await litty.think("What dark patterns should I check first?")
# Returns: LLM-generated reasoning
```

### Execute Tool with Self-Correction

```python
result = await litty.execute_with_self_correction(
    task="Detect dark patterns",
    tool_name="detect_dark_patterns",
    parameters={'page_content': html, 'url': url}
)

if result['success']:
    print(f"Found: {result['result']}")
    print(f"Attempts: {result['attempts']}")
    print(f"Corrections: {result['corrections']}")
```

---

## 🛠️ Converting a Hero (8 Steps)

1. **Analyze v1.4.0** - What does hero do?
2. **Design Tools** - Convert methods → tools
3. **Craft Prompt** - How should agent think?
4. **Implement Class** - Extend AutonomousAgent
5. **Register Tools** - Define schemas
6. **Write execute_mission()** - Autonomous workflow
7. **Test** - Unit + integration
8. **Document** - Update guides

**Time**: ~3 hours per hero

**Template**: Use Litty (`litty_agent.py`) as reference

---

## 🧪 Testing

### Unit Test

```python
import pytest
from core.justice_league_v2.agents.hero_agent import HeroAgent

@pytest.mark.asyncio
async def test_hero_mission():
    hero = HeroAgent()  # Demo mode
    result = await hero.execute_mission({'url': 'https://test.com'})
    assert result['status'] == 'completed'
```

### Run Tests

```bash
pytest tests/test_hero_agent.py -v
```

---

## ⚠️ Common Issues

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: anthropic` | `pip3 install anthropic>=0.18.0` |
| `AttributeError` during init | Define attributes BEFORE `super().__init__()` |
| Agent not reasoning (demo) | Set `ANTHROPIC_API_KEY` for full mode |
| Tool execution fails | Check tool parameters match schema |
| Mission not recorded | Call `self.record_mission()` at end |

---

## 📚 Documentation Flow

**New to v2.0?**
1. Read `JUSTICE_LEAGUE_V2_GUIDE.md` (start here)
2. Run `example_litty_autonomous.py` (see it work)
3. Read `MIGRATION_GUIDE_V1_TO_V2.md` (learn to convert)

**Converting a Hero?**
1. Read `MIGRATION_GUIDE_V1_TO_V2.md` (detailed steps)
2. Study `litty_agent.py` (working example)
3. Follow 8-step process
4. Update `QUICK_REFERENCE_V2.md` (this file)

**Understanding Architecture?**
1. Read `ARCHITECTURE_ANALYSIS.md` (v1 vs v2)
2. Read `V2_COMPLETION_SUMMARY.md` (what's done)
3. Study `autonomous_agent.py` (base class)

---

## 🎯 Next Actions

**Immediate** (Today):
- [ ] Convert Batman to autonomous agent (3 hours)
- [ ] Test Batman agent thoroughly
- [ ] Update progress tracking

**Short-term** (This Week):
- [ ] Convert Wonder Woman (2.5 hours)
- [ ] Convert Flash (2.5 hours)
- [ ] Create test suite template

**Medium-term** (This Month):
- [ ] Convert remaining 9 heroes
- [ ] Convert Superman orchestrator
- [ ] Implement inter-agent communication

---

## 💡 Key Concepts

**Autonomous Agent** = Class that:
- Uses LLM to reason and plan
- Executes tools strategically
- Self-corrects on failures
- Learns from missions

**Tool** = Function that agent can call:
- Registered with JSON schema
- Agent decides when to use
- Returns structured data

**Mission** = Task for agent:
- Input: URL, goal, focus areas
- Output: Findings, reasoning, recommendations

**Self-Correction** = Retry loop:
- Tool fails → LLM suggests fix → Retry
- Max 3 attempts per tool

---

## 📊 Progress Metrics

**Completed**:
- ✅ Architecture designed
- ✅ Base class implemented (350 lines)
- ✅ Litty agent converted (428 lines)
- ✅ Documentation written (2500+ lines)
- ✅ Example working

**Remaining**:
- 🚧 12 heroes to convert (~36 hours)
- 🚧 Superman orchestrator (~8 hours)
- 🚧 Advanced features (~20 hours)

**Total**: ~64 hours to full v2.0

---

## 🔗 Quick Links

**Documentation**:
- [V2.0 Guide](JUSTICE_LEAGUE_V2_GUIDE.md) - Comprehensive guide
- [Migration Guide](MIGRATION_GUIDE_V1_TO_V2.md) - Hero conversion
- [Completion Summary](V2_COMPLETION_SUMMARY.md) - Phase 1 & 2 report

**Code**:
- [Base Class](core/justice_league_v2/base/autonomous_agent.py) - Foundation
- [Litty Agent](core/justice_league_v2/agents/litty_agent.py) - Pilot
- [Example](example_litty_autonomous.py) - Working demo

**Production (v1.4.0)**:
- [Quickstart](QUICKSTART.md) - v1.4.0 usage
- [Deployment Report](PRODUCTION_DEPLOYMENT_REPORT.md) - Production status

---

## 🎓 Learning Path

**Beginner** (Never used v2.0):
1. Install dependencies
2. Run `example_litty_autonomous.py`
3. Read `JUSTICE_LEAGUE_V2_GUIDE.md` sections 1-4

**Intermediate** (Ready to convert hero):
1. Read `MIGRATION_GUIDE_V1_TO_V2.md` Step 1-3
2. Study `litty_agent.py` implementation
3. Start with Step 1 on chosen hero

**Advanced** (Building features):
1. Read `autonomous_agent.py` source
2. Review `V2_COMPLETION_SUMMARY.md` for architecture
3. Implement advanced capabilities (Phase 5)

---

## 🚀 Call to Action

**Ready to build?**

```bash
# 1. Read the guide
open JUSTICE_LEAGUE_V2_GUIDE.md

# 2. See it work
python3 example_litty_autonomous.py

# 3. Convert next hero
# Follow MIGRATION_GUIDE_V1_TO_V2.md Step 1-8
```

**Questions?** Check troubleshooting in `JUSTICE_LEAGUE_V2_GUIDE.md`

---

**"Eda mone! Let's build autonomous agents!"** 🪔

*Last updated: 2025-10-20*
