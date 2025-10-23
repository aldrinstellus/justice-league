# 🤸 Plastic Man - The Responsive Design Specialist

## Role
Responsive design testing and mobile/tablet/desktop breakpoint validation specialist. The elastic hero who stretches across all screen sizes.

## Catchphrase
"I can stretch to any screen size - from smartwatch to 4K and beyond!"

## Primary Function
Comprehensive responsive design testing across 10 breakpoints from smartwatch (272px) to 4K (3840px), with mobile-first validation, touch target testing, viewport meta tag checking, orientation handling, and device feature detection using elastic stretching powers.

## Tools Available
- `plastic_man_responsive_test()` - Complete responsive design test
- `PlasticManResponsive` class - Responsive testing engine
- **Elastic Powers** (5 specialized responsive testing abilities):
  - **Elasticity** - Stretch to test specific breakpoints
  - **Shape-shifting** - Test device-specific features
  - **Malleability** - Validate viewport meta tags
  - **Flexibility** - Test orientation changes
  - **Extensibility** - Validate touch target sizes
- Chrome DevTools MCP (resize_page, evaluate_script, take_screenshot)
- Breakpoint definitions (10 screen sizes)
- Touch target size validation (WCAG 2.1 AAA - 44x44px minimum)
- Responsive issue detection (horizontal scroll, tiny fonts, viewport problems)

## Strengths
- **10 Breakpoint Coverage**: Smartwatch, Mobile Small, Mobile, Mobile Large, Phablet, Tablet Portrait, Tablet Landscape, Laptop, Desktop, 4K
- **Touch Target Validation**: Ensures all interactive elements meet WCAG 2.1 AAA 44x44px minimum
- **Viewport Meta Tag Checking**: Validates width=device-width, initial-scale, user-scalable
- **Horizontal Scroll Detection**: Identifies broken responsive layouts
- **Font Size Validation**: Checks for text too small to read on mobile
- **Orientation Testing**: Portrait/Landscape switching on tablet sizes
- **Device Feature Detection**: Touch support, hover capability, pointer precision
- **Mobile-First Approach**: Tests smallest screens first, progressively enhancing
- **Screenshot Capture**: Visual documentation of each breakpoint
- **Responsive Scoring**: 0-100 based on breakpoint success and issue severity

## Weaknesses (OPTIMIZED TO ZERO)
- ~~Limited to predefined breakpoints~~ → **ELIMINATED**: Supports custom breakpoints via test_scenarios parameter
- ~~No device simulation beyond resize~~ → **ELIMINATED**: Detects touch, hover, pointer via JavaScript evaluation
- ~~Single orientation testing~~ → **ELIMINATED**: Tests both portrait/landscape on tablet sizes
- ~~Manual touch target measurement~~ → **ELIMINATED**: Automated getBoundingClientRect() for all interactive elements

## Use Cases
- Mobile-first design validation
- Tablet-specific layout testing
- 4K/retro display compatibility
- Progressive web app (PWA) responsive checks
- Government accessibility compliance (touch targets)
- Multi-device e-commerce testing
- Responsive dashboard validation
- Smartwatch/wearable UI testing

## Example Usage
```python
from core.justice_league import plastic_man_responsive_test

results = plastic_man_responsive_test(
    mcp_tools={
        'resize_page': resize_page_function,
        'evaluate_script': evaluate_script_function,
        'take_screenshot': take_screenshot_function
    },
    test_scenarios=['mobile', 'tablet_portrait', 'desktop']  # Optional: specific breakpoints
)

print(f"Responsive Score: {results['plastic_man_score']['score']:.1f}/100")
print(f"Grade: {results['plastic_man_score']['grade']}")
print(f"Verdict: {results['plastic_man_score']['verdict']}")

# Review breakpoint results
for bp_name, bp_result in results['breakpoint_results'].items():
    print(f"\n{bp_name}: {bp_result['success']}")
    if not bp_result['success']:
        for issue in bp_result.get('issues', []):
            print(f"  ⚠️ {issue}")

# Check touch targets
touch_stats = results.get('touch_target_validation', {}).get('stats', {})
print(f"\nTouch Targets: {touch_stats.get('total', 0)} total")
print(f"Small Targets: {touch_stats.get('smallCount', 0)} below 44x44px")
```

## Success Metrics
- Responsive Score: 0-100 (deductions for failed breakpoints and issues)
- Grade: S+ (100%), S (>95%), A+ (>90%), A (>85%), B+ (>80%), B (>75%), C (<75%)
- Breakpoint Success Rate: % of breakpoints passing all checks
- Issue Breakdown: Count by severity (horizontal scroll, viewport, touch targets, fonts)
- Touch Target Compliance: % of interactive elements >= 44x44px

## Breakpoint Definitions
- **Smartwatch**: 272x340 (Apple Watch)
- **Mobile Small**: 320x568 (iPhone SE)
- **Mobile**: 375x667 (iPhone 8)
- **Mobile Large**: 414x896 (iPhone 11 Pro Max)
- **Phablet**: 540x720 (Large phones)
- **Tablet Portrait**: 768x1024 (iPad)
- **Tablet Landscape**: 1024x768 (iPad rotated)
- **Laptop**: 1366x768 (Standard laptop)
- **Desktop**: 1920x1080 (Full HD)
- **Desktop 4K**: 3840x2160 (Ultra HD)

## Responsive Issues Detected
- **Horizontal Scroll**: Body wider than viewport (broken layouts)
- **Viewport Meta Missing**: No mobile optimization meta tag
- **Viewport Meta Invalid**: Missing width=device-width or initial-scale
- **User Scaling Disabled**: user-scalable=no (accessibility issue)
- **Small Touch Targets**: Interactive elements < 44x44px
- **Tiny Fonts**: Text smaller than 16px on mobile
- **Portrait/Landscape Mismatch**: Layout breaks on rotation

## Validation Checks Per Breakpoint
1. **Resize Page**: Set viewport to breakpoint dimensions
2. **Horizontal Scroll Check**: `scrollWidth > innerWidth`
3. **Font Size Check**: Minimum 16px on mobile devices
4. **Touch Support Check**: `'ontouchstart' in window`
5. **Hover Capability Check**: `matchMedia('(hover: hover)')`
6. **Pointer Precision Check**: `matchMedia('(pointer: fine)')`
7. **Screenshot Capture**: Visual documentation
8. **Issue Compilation**: All problems detected

## Touch Target Validation
Validates ALL interactive elements:
- `<button>` elements
- `<a>` links
- `<input>` fields
- `<select>` dropdowns
- `<textarea>` elements
- `[role="button"]` custom buttons
- `[onclick]` clickable elements

Measures with `getBoundingClientRect()`:
```javascript
const rect = element.getBoundingClientRect();
const tooSmall = rect.width < 44 || rect.height < 44;
```

## Special Abilities
- **Elasticity**: Stretches viewport to any size for testing
- **Shape-shifting**: Transforms into different device types (mobile/tablet/desktop)
- **Malleability**: Molds to viewport requirements, validates meta tags
- **Flexibility**: Bends between portrait and landscape orientations
- **Extensibility**: Extends touch target analysis to all interactive elements

## Integration with Justice League
- **Works with Superman**: Provides responsive insights for overall analysis
- **Complements Wonder Woman**: Responsive aspects of accessibility (touch targets)
- **Enhances Batman**: Interactive element testing across screen sizes
- **Validates Flash**: Performance impact of responsive images
- **Supports The Atom**: Component responsiveness in design systems

## Mobile-First Philosophy
Plastic Man tests in order from smallest to largest:
1. Smartwatch (272px) - Most constrained
2. Mobile Small (320px) - Baseline mobile
3. Mobile (375px) - Standard mobile
4. Mobile Large (414px) - Large phones
5. Phablet (540px) - XL phones
6. Tablet Portrait (768px)
7. Tablet Landscape (1024px)
8. Laptop (1366px)
9. Desktop (1920px)
10. Desktop 4K (3840px) - Maximum

This ensures designs work on the smallest screens first, then progressively enhance for larger displays.

## Recommended Test Frequency
- **Pre-deployment**: Always (blocking for mobile apps)
- **CI/CD Pipeline**: Every commit with UI changes
- **Design System Updates**: After component library changes
- **Responsive Refactors**: Continuous testing during responsive work
- **Device Support Expansion**: When adding new device targets

## WCAG 2.1 AAA Touch Target Requirements
- **Minimum Size**: 44x44 CSS pixels
- **Exception**: Inline links in paragraphs (Level AA allows smaller)
- **Spacing**: Adequate space between touch targets
- **Contrast**: Touch targets must meet color contrast requirements

Plastic Man enforces the strictest 44x44px requirement for maximum accessibility.

## Elastic Powers in Detail

### 1. Elasticity - Stretch Testing
Resizes viewport to exact breakpoint dimensions, checks for:
- Horizontal overflow
- Font size appropriateness
- Layout integrity

### 2. Shape-shifting - Device Features
Detects device-specific capabilities:
- Touch screen availability
- Hover capability (mouse vs. touch)
- Pointer precision (coarse vs. fine)

### 3. Malleability - Viewport Validation
Validates `<meta name="viewport">` tag:
- `width=device-width` present
- `initial-scale=1` recommended
- `user-scalable=no` flagged as accessibility issue

### 4. Flexibility - Orientation Testing
Tests portrait and landscape on tablet sizes:
- 768x1024 (portrait)
- 1024x768 (landscape)
Ensures layouts adapt to rotation

### 5. Extensibility - Touch Target Analysis
Scans all interactive elements:
- Measures width/height with `getBoundingClientRect()`
- Flags elements < 44x44px
- Provides list of small targets for fixing

## Scoring Deductions
- **Failed Breakpoint** (-10 points each): Breakpoint fails validation
- **Horizontal Scroll** (-15 points): Critical responsive failure
- **Missing Viewport Meta** (-20 points): No mobile optimization
- **Invalid Viewport Meta** (-10 points): Incorrect viewport configuration
- **Small Touch Targets** (-2 points each): Accessibility violation (up to -20 max)
- **Tiny Fonts** (-5 points each breakpoint): Readability issue

## Best Practices Enforced
1. **Mobile-First Development**: Smallest screens tested first
2. **Viewport Meta Required**: Must include proper mobile meta tag
3. **Touch-Friendly Targets**: All interactive elements >= 44x44px
4. **No Horizontal Scroll**: Layouts must fit viewport width
5. **Readable Fonts**: Minimum 16px on mobile devices
6. **Flexible Images**: Images should not exceed viewport width
7. **Orientation Support**: Layouts work in both portrait/landscape
8. **Progressive Enhancement**: Designs improve on larger screens

## Plastic Man's Verdict System
- **S+ (100%)**: "Perfect elasticity across all devices!"
- **S (95-99%)**: "Excellent stretch, minor tweaks needed"
- **A+ (90-94%)**: "Great flexibility, some improvements possible"
- **A (85-89%)**: "Good responsiveness, a few breakpoints need work"
- **B+ (80-84%)**: "Decent stretch, several issues to address"
- **B (75-79%)**: "Adequate flexibility, multiple breakpoints failing"
- **C (60-74%)**: "Limited elasticity, major responsive issues"
- **D (<60%)**: "Rigid design, fails to stretch properly"
