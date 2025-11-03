# 🚀 Justice League v1.4.0 - Quick Start Guide

**How to Invoke and Use the Justice League**

---

## 📋 Prerequisites

### 1. Install Dependencies
```bash
cd /Users/admin/Documents/claudecode/Projects/aldo-vision
pip3 install -r requirements.txt
```

### 2. Install Playwright Browsers (Required for MCP Chrome DevTools)
```bash
playwright install chromium
```

---

## 🎯 Three Ways to Invoke Justice League

### **Option 1: Use Individual Heroes Directly** (Recommended for Testing)

```python
#!/usr/bin/env python3
"""Example: Using Litty to validate ethics"""

import sys
sys.path.insert(0, '/Users/admin/Documents/claudecode/Projects/aldo-vision')

from core.justice_league import litty_validate_ethics

# Mock MCP tools for testing (replace with real MCP Chrome DevTools)
def create_mock_mcp_tools():
    """Create mock MCP tools for testing without browser"""
    return {
        'evaluate_script': lambda function: {
            'darkPatterns': {'confirmshaming': 1, 'urgency': 2},
            'accessibility': {'contrast_issues': 5},
            'text_size': 12
        },
        'take_snapshot': lambda: {
            'text': 'Sample page content with small text and dark patterns'
        },
        'take_screenshot': lambda: '/tmp/screenshot.png'
    }

# Validate ethics
mcp_tools = create_mock_mcp_tools()
result = litty_validate_ethics(
    url="https://example.com",
    mcp_tools=mcp_tools
)

# Print results
print(f"\n🪔 Litty's Ethics Report:")
print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"Ethics Score: {result['ethics_score']}/100")
print(f"Grade: {result['grade']}")
print(f"Dark Patterns: {len(result.get('checks', {}).get('dark_patterns', {}).get('detected', []))}")
print(f"Guilt Trips: {len(result.get('guilt_trips', []))}")
print(f"\nUser Stories:")
for story in result.get('user_stories', [])[:3]:
    print(f"  • {story.get('persona')}: {story.get('impact', 'Impact not specified')}")
```

**Run it:**
```bash
python3 example_litty.py
```

---

### **Option 2: Use Superman Coordinator (Deploy All Heroes)**

```python
#!/usr/bin/env python3
"""Example: Deploy entire Justice League"""

import sys
sys.path.insert(0, '/Users/admin/Documents/claudecode/Projects/aldo-vision')

from core.justice_league import assemble_justice_league

# Mock MCP tools
def create_mock_mcp_tools():
    return {
        'navigate_page': lambda url, **kwargs: {'status': 'success'},
        'take_snapshot': lambda: {'text': 'Page content', 'elements': []},
        'take_screenshot': lambda **kwargs: '/tmp/screenshot.png',
        'evaluate_script': lambda function, **kwargs: {
            'performance': {'lcp': 2.5, 'fid': 100, 'cls': 0.1},
            'accessibility': {'violations': []},
            'network': {'requests': []},
        },
        'list_network_requests': lambda **kwargs: {'requests': []},
        'click': lambda uid: {'status': 'clicked'},
        'fill': lambda uid, value: {'status': 'filled'},
    }

# Assemble the Justice League!
mcp_tools = create_mock_mcp_tools()
results = assemble_justice_league(
    mission={
        'url': 'https://example.com',
        'mcp_tools': mcp_tools,
        'options': {
            'test_interactive': True,        # 🦇 Batman
            'store_baseline': False,         # 💚 Green Lantern
            'analyze_accessibility': True,   # ⚡ Wonder Woman
            'analyze_performance': True,     # ⚡ Flash
            'analyze_network': True,         # 🌊 Aquaman
            'connect_integrations': False,   # 🤖 Cyborg
            'analyze_components': True,      # 🔬 Atom
            'test_qa': True,                 # 🏹 Green Arrow
            'scan_security': True,           # 🧠 Martian Manhunter
            'test_responsive': True,         # 🤸 Plastic Man
            'analyze_seo': True,             # 🎩 Zatanna
            'validate_ethics': True,         # 🪔 Litty ⭐ NEW!
        }
    }
)

# Print summary
print(f"\n🦸 Justice League Mission Complete!")
print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"Overall Score: {results['overall_score']}/100")
print(f"Heroes Deployed: {len(results['heroes_deployed'])}")
print(f"\nHeroes:")
for hero in results['heroes_deployed']:
    print(f"  ✅ {hero}")
```

**Run it:**
```bash
python3 example_justice_league.py
```

---

### **Option 3: Use with Real MCP Chrome DevTools** (Production)

```python
#!/usr/bin/env python3
"""Example: Using Justice League with real MCP Chrome DevTools"""

import sys
sys.path.insert(0, '/Users/admin/Documents/claudecode/Projects/aldo-vision')

from core.justice_league import litty_validate_ethics
from playwright.sync_api import sync_playwright

def create_real_mcp_tools(page):
    """Create real MCP tools using Playwright"""
    return {
        'navigate_page': lambda url, **kwargs: page.goto(url),
        'take_snapshot': lambda: {'text': page.content()},
        'take_screenshot': lambda **kwargs: page.screenshot(path='/tmp/screenshot.png'),
        'evaluate_script': lambda function, **kwargs: page.evaluate(function),
        'click': lambda uid: page.click(f'[data-uid="{uid}"]'),
        'fill': lambda uid, value: page.fill(f'[data-uid="{uid}"]', value),
        'list_network_requests': lambda **kwargs: {'requests': []},
    }

# Use with real browser
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    mcp_tools = create_real_mcp_tools(page)

    # Validate ethics with real MCP tools
    result = litty_validate_ethics(
        url="https://example.com",
        mcp_tools=mcp_tools
    )

    print(f"\n🪔 Litty's Real Ethics Analysis:")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Ethics Score: {result['ethics_score']}/100")
    print(f"Grade: {result['grade']}")

    browser.close()
```

**Run it:**
```bash
python3 example_real_mcp.py
```

---

## 🪔 Litty-Specific Examples

### Example 1: Quick Ethics Check
```python
import sys
sys.path.insert(0, '/Users/admin/Documents/claudecode/Projects/aldo-vision')

from core.justice_league import LittyEthics

# Create Litty instance
litty = LittyEthics()

# Check her powers
print(f"Hero: {litty.name}")
print(f"Origin: {litty.origin}")
print(f"Dark Patterns Detected: {len(litty.dark_patterns)}")
print(f"User Personas: {list(litty.user_personas.keys())}")
print(f"\nMalayalam Guilt Phrase: {litty.guilt_phrases['severe']}")
```

### Example 2: Analyze Your Own Website
```python
import sys
sys.path.insert(0, '/Users/admin/Documents/claudecode/Projects/aldo-vision')

from core.justice_league import litty_validate_ethics
from playwright.sync_api import sync_playwright

url = "https://your-website.com"  # ← Change this!

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    mcp_tools = {
        'navigate_page': lambda url, **kw: page.goto(url),
        'take_snapshot': lambda: {'text': page.content()},
        'evaluate_script': lambda fn, **kw: page.evaluate(fn),
        'take_screenshot': lambda **kw: page.screenshot(),
    }

    result = litty_validate_ethics(url=url, mcp_tools=mcp_tools)

    print(f"\n🪔 Ethics Report for {url}")
    print(f"Score: {result['ethics_score']}/100 ({result['grade']})")
    print(f"\nTop Issues:")
    for check_name, check_data in result.get('checks', {}).items():
        if isinstance(check_data, dict) and 'issues' in check_data:
            print(f"  • {check_name}: {len(check_data['issues'])} issues")

    browser.close()
```

---

## 🎨 Using Claude Skills (In Claude Code)

If you're using Claude Code (VS Code extension), you can invoke skills directly:

### 1. Type `/litty` in Claude Code
This will invoke Litty's Claude skill and provide guided assistance.

### 2. Example Prompt:
```
/litty analyze https://example.com for ethical design issues
```

---

## 📁 File Locations

### Source Code
```
/Users/admin/Documents/claudecode/Projects/aldo-vision/core/justice_league/
├── litty_ethics.py              # Litty implementation
├── superman_coordinator.py      # Superman coordinator
├── batman_testing.py            # Batman
└── ... (all 13 heroes)
```

### Production Deployment
```
/tmp/aldo-vision-production/
├── justice-league/              # All heroes
├── current@ → source link       # Symlink to source
└── MANIFEST.json               # Deployment info
```

### Documentation
```
/Users/admin/Documents/claudecode/Projects/aldo-vision/
├── .claude/skills/litty.md     # Litty Claude skill
├── docs/INDEX.md               # Documentation index
└── QUICKSTART.md              # This file!
```

---

## 🔍 Available Heroes & Functions

Import any hero individually:

```python
from core.justice_league import (
    # Superman
    assemble_justice_league,
    SupermanCoordinator,

    # Batman
    batman_test_interactive_elements,
    BatmanTesting,

    # Green Lantern
    green_lantern_store_baseline,
    GreenLanternVisual,

    # Wonder Woman
    wonder_woman_accessibility_analysis,
    WonderWomanAccessibility,

    # Flash
    flash_profile_performance,
    FlashPerformance,

    # Aquaman
    aquaman_analyze_network,
    AquamanNetwork,

    # Cyborg
    cyborg_connect_systems,
    CyborgIntegrations,

    # The Atom
    atom_analyze_components,
    AtomComponentAnalysis,

    # Green Arrow
    green_arrow_test_league,
    GreenArrowTesting,

    # Martian Manhunter
    martian_manhunter_security_scan,
    MartianManhunterSecurity,

    # Plastic Man
    plastic_man_responsive_test,
    PlasticManResponsive,

    # Zatanna
    zatanna_seo_analysis,
    ZatannaSEO,

    # Litty ⭐ NEW!
    litty_validate_ethics,
    LittyEthics,
)
```

---

## 🧪 Quick Test

Run the production test suite to verify everything works:

```bash
cd /Users/admin/Documents/claudecode/Projects/aldo-vision
python3 test_production_ready.py
```

**Expected Output:**
```
✅ ALL TESTS PASSED! ✨
✅ Justice League v1.4.0 is PRODUCTION READY! 🚀
```

---

## 💡 Common Use Cases

### 1. **Test Your Website Ethics**
```bash
python3 << EOF
import sys
sys.path.insert(0, '.')
from core.justice_league import litty_validate_ethics

# Add your MCP tools setup here
result = litty_validate_ethics(url="https://your-site.com", mcp_tools=mcp_tools)
print(f"Score: {result['ethics_score']}/100")
EOF
```

### 2. **Run Complete Analysis**
```bash
python3 << EOF
import sys
sys.path.insert(0, '.')
from core.justice_league import assemble_justice_league

results = assemble_justice_league(mission={
    'url': 'https://your-site.com',
    'mcp_tools': mcp_tools,
    'options': {'validate_ethics': True, 'test_interactive': True}
})
print(f"Overall: {results['overall_score']}/100")
EOF
```

### 3. **Check Hero Availability**
```bash
python3 -c "
import sys
sys.path.insert(0, '.'
from core.justice_league import __version__, __heroes__
print(f'Version: {__version__}')
print(f'Heroes: {__heroes__}')
"
```

---

## 📚 Next Steps

1. **Read Full Documentation**: `docs/releases/v1.4.0/RELEASE_v1.4.0_SUMMARY.md`
2. **Explore Litty**: `LITTY_INTRODUCTION.md`
3. **Learn All Heroes**: `docs/releases/v1.4.0/JUSTICE_LEAGUE_SAVE_POINT_V1.4.0.md`
4. **Production Deployment**: `PRODUCTION_DEPLOYMENT_REPORT.md`

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'justice_league'"
**Solution:**
```python
import sys
sys.path.insert(0, '/Users/admin/Documents/claudecode/Projects/aldo-vision')
# Now import
from core.justice_league import litty_validate_ethics
```

### "MCP tools not working"
**Solution:** Use mock tools for testing (see Option 1 above), or set up real Playwright MCP integration.

### "Playwright not installed"
**Solution:**
```bash
pip3 install playwright
playwright install chromium
```

---

## 🎉 Quick One-Liner Test

Test Litty immediately:

```bash
python3 -c "import sys; sys.path.insert(0, '.'); from core.justice_league import LittyEthics; litty = LittyEthics(); print(f'🪔 {litty.name} from {litty.origin}'); print(f'Dark patterns: {len(litty.dark_patterns)}'); print(f'Personas: {len(litty.user_personas)}'); print(f'Guilt phrase: {litty.guilt_phrases[\"severe\"]}')"
```

**Expected:**
```
🪔 Litty from Kerala, India
Dark patterns: 15
Personas: 5
Guilt phrase: Eda mone! (Oh dear!)
```

---

**"Eda mone! Go analyze some websites and make them better!" 🪔**

**Justice League v1.4.0 - Ready to Use!** 🚀
