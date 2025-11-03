#!/usr/bin/env python3
"""
🧠 Knowledge Base Integration Example

Shows how Justice League heroes reference the global knowledge base
during their analysis.
"""

import sys
sys.path.insert(0, '/Users/admin/Documents/claudecode/Projects/aldo-vision')

from core.knowledge_base_loader import (
    get_knowledge_base,
    get_dark_patterns,
    get_wcag_guidelines,
    get_core_web_vitals,
    get_litty_knowledge,
    get_wonder_woman_knowledge,
    get_flash_knowledge
)

def main():
    print("\n" + "=" * 70)
    print("🧠 JUSTICE LEAGUE KNOWLEDGE BASE INTEGRATION")
    print("How Heroes Reference Best Practices During Analysis")
    print("=" * 70 + "\n")

    kb = get_knowledge_base()

    # ===================================================================
    # SCENARIO 1: Litty analyzing for dark patterns
    # ===================================================================

    print("📍 SCENARIO 1: Litty Analyzing E-commerce Site")
    print("-" * 70)
    print()

    print("🪔 Litty: 'Let me check the knowledge base for dark patterns...'\n")

    # Litty queries KB for dark patterns
    dark_patterns = get_dark_patterns()
    litty_kb = get_litty_knowledge()

    print(f"📚 KB Query: Found {len(dark_patterns)} dark patterns to check")
    print(f"📋 Checklist items: {len(litty_kb.get('checklist', []))}")
    print()

    # Simulate Litty finding issues
    site_text = "No thanks, I don't want to save 50%"

    print("🔍 Litty analyzing page text...")
    print(f'   Page text: "{site_text}"')
    print()

    # Check against KB
    for pattern in dark_patterns[:3]:
        if pattern['pattern'] == 'Confirmshaming':
            print(f"⚠️  MATCH FOUND!")
            print(f"   Pattern: {pattern['pattern']}")
            print(f"   KB Definition: {pattern['description']}")
            print(f"   KB Example: {pattern['example']}")
            print()
            print('🪔 Litty: "Eda mone! This is confirmshaming!"')
            print('   "Village Teacher is being emotionally manipulated."')
            print('   "KB recommends: Change to neutral \'No thanks\'"')
            break

    print()

    # ===================================================================
    # SCENARIO 2: Wonder Woman checking accessibility
    # ===================================================================

    print("📍 SCENARIO 2: Wonder Woman Checking Accessibility")
    print("-" * 70)
    print()

    print("⚡ Wonder Woman: 'Referencing WCAG guidelines from KB...'\n")

    # Wonder Woman queries KB
    wcag = get_wcag_guidelines()
    ww_kb = get_wonder_woman_knowledge()

    print("📚 KB Query: WCAG 2.1 Level AA Standards")
    print(f"   Font size minimum: {wcag['font_size']}")
    print(f"   Color contrast: {wcag['contrast']['normal_text']}")
    print()

    # Simulate checking a site
    site_font_size = "10px"
    site_contrast = "2.1:1"

    print("🔍 Wonder Woman analyzing site...")
    print(f"   Site font size: {site_font_size}")
    print(f"   Site contrast: {site_contrast}")
    print()

    # Validate against KB
    if site_font_size < "16px":
        print("❌ VIOLATION: Font size below KB minimum")
        print(f"   Found: {site_font_size}")
        print(f"   KB requires: {wcag['font_size']}")
        print()

    if site_contrast < "4.5":
        print("❌ VIOLATION: Contrast below KB minimum")
        print(f"   Found: {site_contrast}")
        print(f"   KB requires: {wcag['contrast']['normal_text']}")
        print()

    print("⚡ Wonder Woman: 'These fail WCAG 2.1 Level AA per our KB.'")
    print("   'Ammachi (72) cannot read this text!'")
    print()

    # ===================================================================
    # SCENARIO 3: Flash checking performance
    # ===================================================================

    print("📍 SCENARIO 3: Flash Checking Performance")
    print("-" * 70)
    print()

    print("⚡ Flash: 'Checking Core Web Vitals from KB...'\n")

    # Flash queries KB
    cwv = get_core_web_vitals()
    flash_kb = get_flash_knowledge()

    print("📚 KB Query: Core Web Vitals Targets")
    for metric, values in list(cwv.items())[:3]:
        print(f"   {metric}: Good = {values['good']}")
    print()

    # Simulate performance test
    site_lcp = 3.2  # seconds
    site_fid = 150  # ms
    site_cls = 0.15

    print("🔍 Flash analyzing site performance...")
    print(f"   LCP: {site_lcp}s")
    print(f"   FID: {site_fid}ms")
    print(f"   CLS: {site_cls}")
    print()

    # Validate against KB
    lcp_good = float(cwv['LCP']['good'].replace('≤', '').replace('s', ''))
    fid_good = float(cwv['FID']['good'].replace('≤', '').replace('ms', ''))
    cls_good = float(cwv['CLS']['good'].replace('≤', ''))

    if site_lcp > lcp_good:
        status = 'needs_improvement' if site_lcp <= 4.0 else 'poor'
        print(f"⚠️  LCP {status.upper()}: {site_lcp}s")
        print(f"   KB good: {cwv['LCP']['good']}")
        print(f"   KB status: {cwv['LCP'][status]}")
        print()

    if site_fid > fid_good:
        status = 'needs_improvement' if site_fid <= 300 else 'poor'
        print(f"⚠️  FID {status.upper()}: {site_fid}ms")
        print(f"   KB good: {cwv['FID']['good']}")
        print()

    print("⚡ Flash: 'Per KB standards, this site needs optimization.'")
    print("   'Village Teacher on 3G will wait too long!'")
    print()

    # ===================================================================
    # SCENARIO 4: Superman coordinating with KB
    # ===================================================================

    print("📍 SCENARIO 4: Superman Checking Minimum Standards")
    print("-" * 70)
    print()

    print("🦸 Superman: 'Checking if site meets ALL minimum standards...'\n")

    standards = kb.get_minimum_standards()

    print("📚 KB Query: Minimum Pass/Fail Standards")
    print()

    # Simulate overall check
    site_results = {
        'ethics': 'FAIL - confirmshaming found',
        'accessibility': 'FAIL - font too small, contrast too low',
        'performance_lcp': 'FAIL - 3.2s (needs < 2.5s)',
        'performance_fid': 'NEEDS IMPROVEMENT - 150ms',
        'performance_cls': 'NEEDS IMPROVEMENT - 0.15',
        'security': 'PASS - HTTPS enabled',
        'seo': 'PASS - meta tags present'
    }

    failed = 0
    passed = 0

    for area, standard in standards.items():
        result = site_results.get(area, 'NOT TESTED')

        if 'FAIL' in result:
            print(f"   ❌ {area}: {standard}")
            print(f"      Result: {result}")
            failed += 1
        elif 'PASS' in result:
            print(f"   ✅ {area}: {standard}")
            passed += 1
        elif 'NEEDS' in result:
            print(f"   ⚠️  {area}: {standard}")
            print(f"      Result: {result}")

    print()
    print(f"📊 Summary: {passed} passed, {failed} failed, {len(standards) - passed - failed} needs improvement")
    print()

    print("🦸 Superman: 'Site fails KB minimum standards.'")
    print("   'Litty found ethics violations.'")
    print("   'Wonder Woman found accessibility issues.'")
    print("   'Flash found performance problems.'")
    print("   'Grade: D - Major fixes needed!'")
    print()

    # ===================================================================
    # SUMMARY
    # ===================================================================

    print("=" * 70)
    print("📊 KNOWLEDGE BASE INTEGRATION BENEFITS")
    print("=" * 70)
    print()

    print("✅ Heroes have consistent standards to reference")
    print("✅ Analysis is backed by documented best practices")
    print("✅ Users get KB-referenced recommendations")
    print("✅ All heroes validate against same baseline")
    print("✅ KB can be updated as standards evolve")
    print()

    print("📚 Knowledge Base Stats:")
    print(f"   • 12 hero specializations")
    print(f"   • {len(dark_patterns)} dark patterns")
    print(f"   • {len(wcag['checklist'])} accessibility checklist items")
    print(f"   • {len(cwv)} Core Web Vitals metrics")
    print(f"   • {len(standards)} minimum standards")
    print()

    print("🦸 'Together, with our knowledge base, we make the web better!' - Superman")
    print()


if __name__ == '__main__':
    main()
