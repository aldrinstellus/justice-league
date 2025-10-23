# 🦸 Justice League Quick Reference Guide

**Version**: 1.3.0 | **Heroes**: 12 | **Status**: ✅ Operational

---

## Quick Import

```python
from core.justice_league import (
    # Coordinator
    assemble_justice_league,            # Superman - All heroes

    # Testing & QA
    batman_test_interactive_elements,   # Batman - Interactive elements
    green_arrow_test_league,            # Green Arrow - QA testing

    # Visual & Design
    green_lantern_compare_screenshots,  # Green Lantern - Visual regression
    plastic_man_responsive_test,        # Plastic Man - Responsive design ⭐

    # Accessibility & Standards
    wonder_woman_accessibility_analysis, # Wonder Woman - WCAG 2.2 AAA

    # Performance & Network
    flash_profile_performance,          # Flash - Core Web Vitals
    aquaman_analyze_network,            # Aquaman - Network traffic

    # Components & Integrations
    atom_analyze_components,            # The Atom - Component library
    cyborg_connect_systems,             # Cyborg - External APIs

    # Security & SEO
    martian_manhunter_security_scan,    # Martian Manhunter - OWASP Top 10
    zatanna_seo_analysis                # Zatanna - SEO & metadata ⭐
)
```

---

## Hero Cheat Sheet

| Hero | Emoji | Function | Primary Use |
|------|-------|----------|-------------|
| Superman | 🦸 | `assemble_justice_league()` | Coordinate all heroes |
| Batman | 🦇 | `batman_test_interactive_elements()` | Test buttons, links, forms |
| Green Lantern | 💚 | `green_lantern_compare_screenshots()` | Visual regression testing |
| Wonder Woman | ⚡ | `wonder_woman_accessibility_analysis()` | WCAG accessibility |
| Flash | ⚡ | `flash_profile_performance()` | Performance & CWV |
| Aquaman | 🌊 | `aquaman_analyze_network()` | Network requests |
| Cyborg | 🤖 | `cyborg_connect_systems()` | Figma/Penpot/APIs |
| The Atom | 🔬 | `atom_analyze_components()` | Component library |
| Green Arrow | 🏹 | `green_arrow_test_league()` | QA testing |
| Martian Manhunter | 🧠 | `martian_manhunter_security_scan()` | Security scanning |
| **Plastic Man** ⭐ | 🤸 | `plastic_man_responsive_test()` | **Responsive design** |
| **Zatanna** ⭐ | 🎩 | `zatanna_seo_analysis()` | **SEO & metadata** |

---

## Common Usage Patterns

### 1. Full Analysis (All Heroes)
```python
from core.justice_league import assemble_justice_league

results = assemble_justice_league({
    'url': 'https://example.com',
    'mcp_tools': mcp_tools,
    'options': {
        'test_interactive': True,
        'test_visual': True,
        'test_accessibility': True,
        'test_performance': True,
        'test_network': True,
        'test_components': True,
        'test_security': True,
        'test_responsive': True,  # Plastic Man ⭐
        'test_seo': True          # Zatanna ⭐
    }
})
```

### 2. Responsive Testing (Plastic Man)
```python
from core.justice_league import plastic_man_responsive_test

results = plastic_man_responsive_test(
    mcp_tools={'resize_page': resize, 'evaluate_script': eval_js, 'take_screenshot': screenshot},
    test_scenarios=['mobile', 'tablet_portrait', 'desktop']  # Optional
)

# Check results
print(f"Score: {results['plastic_man_score']['score']}/100")
print(f"Breakpoints tested: {len(results['breakpoint_results'])}")
```

### 3. SEO Analysis (Zatanna)
```python
from core.justice_league import zatanna_seo_analysis

results = zatanna_seo_analysis(
    mcp_tools={'evaluate_script': eval_js},
    target_url='https://example.com'
)

# Check results
print(f"Score: {results['zatanna_score']['score']}/100")
print(f"Issues: {len(results['issues'])}")
print(f"Magic spells cast: {len(results['magic_spells_cast'])}")
```

### 4. Security Scan (Martian Manhunter)
```python
from core.justice_league import martian_manhunter_security_scan

results = martian_manhunter_security_scan({
    'url': 'https://example.com',
    'html_content': html,
    'headers': headers,
    'source_code_path': '/path/to/code',
    'package_json_path': '/path/to/package.json'
})

# Check vulnerabilities
print(f"Score: {results['security_score']['score']}/100")
print(f"Critical: {results['critical_count']}")
print(f"High: {results['high_count']}")
```

### 5. Accessibility Testing (Wonder Woman)
```python
from core.justice_league import wonder_woman_accessibility_analysis

results = wonder_woman_accessibility_analysis(
    mcp_tools={'evaluate_script': eval_js}
)

# Check WCAG compliance
print(f"Score: {results['wcag_score']['score']}/100")
print(f"Level: {results['wcag_score']['level']}")
print(f"Violations: {len(results['violations'])}")
```

---

## Plastic Man (Responsive) Quick Reference

### Breakpoints Tested (10)
```python
{
    'smartwatch': {'width': 272, 'height': 340},       # Apple Watch
    'mobile_small': {'width': 320, 'height': 568},     # iPhone SE
    'mobile': {'width': 375, 'height': 667},           # iPhone 8
    'mobile_large': {'width': 414, 'height': 896},     # iPhone 11
    'phablet': {'width': 540, 'height': 720},          # Large phones
    'tablet_portrait': {'width': 768, 'height': 1024}, # iPad
    'tablet_landscape': {'width': 1024, 'height': 768},# iPad rotated
    'laptop': {'width': 1366, 'height': 768},          # Laptop
    'desktop': {'width': 1920, 'height': 1080},        # Full HD
    'desktop_4k': {'width': 3840, 'height': 2160}      # Ultra HD
}
```

### Key Checks
- ✅ Horizontal scroll detection
- ✅ Touch targets >= 44x44px (WCAG 2.1 AAA)
- ✅ Viewport meta tag validation
- ✅ Font size >= 16px on mobile
- ✅ Portrait/landscape orientation
- ✅ Device feature detection (touch, hover, pointer)

### Scoring
- Failed breakpoint: **-10 points**
- Horizontal scroll: **-15 points** (critical)
- Missing viewport: **-20 points** (critical)
- Small touch targets: **-2 points each** (max -20)

---

## Zatanna (SEO) Quick Reference

### Magic Spells (5)
1. **!sgat atem laeveR** - Reveal meta tags
2. **!atad derutcurts dniF** - Find structured data
3. **!ytilibwalwarc kcehC** - Check crawlability
4. **!erocs OES etaluclaC** - Calculate SEO score
5. **!seussi OES xiF cigaM** - Fix SEO issues

### SEO Elements Analyzed (20+)
- **Meta Tags**: title, description, canonical, OG, Twitter, viewport, robots
- **Structured Data**: JSON-LD, Microdata (14 schema types)
- **Headings**: H1-H6 hierarchy (exactly one H1)
- **Images**: Alt text coverage
- **Links**: Internal/external/broken counts
- **Mobile**: Viewport meta validation
- **CWV**: LCP, FID, CLS impact
- **Crawlability**: Robots, canonical, hreflang

### Supported Schemas (14)
Organization, Person, Product, Article, BreadcrumbList, WebSite, WebPage, FAQPage, HowTo, Review, Event, LocalBusiness, JobPosting, Recipe

### Scoring
- Critical issues: **-15 points** (missing title, noindex, missing viewport)
- High issues: **-10 points** (title length, missing H1)
- Medium issues: **-5 points** (missing OG tags, alt text)
- Low issues: **-2 points** (missing Twitter tags)

---

## Grading Scale (All Heroes)

| Score | Grade | Description |
|-------|-------|-------------|
| >98% | S+ | Superhuman Excellence |
| >95% | S | Superior |
| >90% | A+ | Excellent Plus |
| >85% | A | Excellent |
| >80% | B+ | Very Good Plus |
| >75% | B | Very Good |
| >70% | C+ | Good Plus |
| >60% | C | Good |
| <60% | D | Needs Improvement |

---

## MCP Tools Required

### Core Tools (All Heroes)
- `navigate_page(url)` - Navigate to page
- `take_snapshot()` - Get DOM snapshot
- `evaluate_script(function)` - Execute JavaScript

### Hero-Specific Tools
- **Batman**: `click(uid)`, `fill(uid, value)`
- **Green Lantern**: `take_screenshot()`
- **Flash**: `performance_start_trace()`, `performance_stop_trace()`
- **Aquaman**: `list_network_requests()`
- **Plastic Man**: `resize_page(width, height)` ⭐
- **Zatanna**: (uses evaluate_script only) ⭐

---

## File Locations

### Implementation Files
```
core/justice_league/
├── __init__.py (v1.3.0)
├── superman_coordinator.py
├── batman_testing.py
├── green_lantern_visual.py
├── wonder_woman_accessibility.py
├── flash_performance.py
├── aquaman_network.py
├── cyborg_integrations.py
├── atom_component_analysis.py
├── green_arrow_testing.py
├── martian_manhunter_security.py
├── plastic_man_responsive.py ⭐
└── zatanna_seo.py ⭐
```

### Documentation Files
```
.claude/skills/
├── README.md (v1.3.0)
├── superman.md
├── batman.md
├── green-lantern.md
├── wonder-woman.md
├── flash.md
├── aquaman.md
├── cyborg.md
├── atom.md
├── green-arrow.md
├── martian-manhunter.md
├── plastic-man.md ⭐
└── zatanna.md ⭐
```

---

## Version Info

```python
from core.justice_league import __version__, __heroes__, __league__

print(f"Version: {__version__}")        # 1.3.0
print(f"Heroes: {__heroes__}")          # 12
print(f"League: {__league__}")          # Justice League of Aldo Vision
```

---

## Common Result Patterns

### All Heroes Return
```python
{
    'hero_score': {
        'score': 85.0,      # 0-100
        'grade': 'A',       # S+, S, A+, A, B+, B, C+, C, D
        'verdict': 'Hero-specific message'
    },
    'issues': [...],        # List of problems found
    'recommendations': [...], # List of fixes
    # Hero-specific data
}
```

### Plastic Man Returns
```python
{
    'breakpoint_results': {
        'mobile': {'success': True, 'issues': []},
        'tablet_portrait': {'success': False, 'issues': ['Horizontal scroll']},
        # ... all breakpoints
    },
    'viewport_validation': {...},
    'touch_target_validation': {...},
    'orientation_tests': {...},
    'plastic_man_score': {
        'score': 82.0,
        'grade': 'B+',
        'verdict': 'Great flexibility, some improvements possible'
    },
    'recommendations': [...]
}
```

### Zatanna Returns
```python
{
    'meta_tags': {
        'extracted': {...},
        'validation': {
            'title': {'valid': True, 'issues': []},
            'description': {'valid': False, 'issues': ['Too short']},
            # ... all meta tags
        }
    },
    'structured_data': [...],  # List of schemas found
    'headings': {...},
    'images': {...},
    'links': {...},
    'mobile': {...},
    'core_web_vitals_impact': {...},
    'crawlability': {...},
    'zatanna_score': {
        'score': 88.0,
        'grade': 'A',
        'verdict': 'Magic is strong, but needs polish'
    },
    'magic_spells_cast': ['!sgat atem laeveR', '!atad derutcurts dniF', ...],
    'recommendations': [...]
}
```

---

## Troubleshooting

### Import Errors
```python
# Check version
from core.justice_league import __version__
print(__version__)  # Should be 1.3.0

# Check hero availability
from core.justice_league import SupermanCoordinator
superman = SupermanCoordinator()
print(f"Heroes: {superman.heroes_available}/12")
```

### Missing MCP Tools
```python
# Verify MCP tools
required_tools = ['evaluate_script', 'resize_page', 'take_screenshot']
for tool in required_tools:
    if tool not in mcp_tools:
        print(f"⚠️ Missing: {tool}")
```

### Low Scores
```python
# Check issues by severity
critical = [i for i in results['issues'] if i['severity'] == 'critical']
high = [i for i in results['issues'] if i['severity'] == 'high']

print(f"Critical: {len(critical)}")
print(f"High: {len(high)}")

# Review recommendations
for rec in results['recommendations'][:5]:
    print(f"{rec['priority']}: {rec['recommendation']}")
```

---

## Testing Commands

### Test Import
```bash
python3 -c "from core.justice_league import plastic_man_responsive_test, zatanna_seo_analysis; print('✅ Import successful')"
```

### Test Version
```bash
python3 -c "from core.justice_league import __version__, __heroes__; print(f'v{__version__} - {__heroes__} heroes')"
```

### Test Initialization
```bash
python3 -c "from core.justice_league import PlasticManResponsive, ZatannaSEO; pm = PlasticManResponsive(); z = ZatannaSEO(); print(f'PM: {len(pm.BREAKPOINTS)} breakpoints, Z: {len(z.MAGIC_SPELLS)} spells')"
```

---

## Quick Tips

### For Responsive Testing
- Always test mobile-first (smallest screens first)
- Use custom `test_scenarios` to focus on specific breakpoints
- Check `touch_target_validation` for accessibility compliance
- Review `viewport_validation` for mobile optimization

### For SEO Analysis
- Focus on critical/high issues first
- Ensure exactly one H1 per page
- Validate meta description is 120-160 characters
- Check structured data for rich snippets
- Use backwards spells in recommendations for fun

### For Full Analysis (Superman)
- Enable only heroes needed for faster execution
- Review `overall_score` for aggregate health
- Check `critical_issues` across all heroes
- Use hero-specific scores for targeted improvements

---

*"Justice League, ASSEMBLE!"* 🦸‍♂️

**Quick Reference v1.0 for Justice League v1.3.0**
