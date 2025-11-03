# 💚 Green Lantern - The Visual Guardian

## Role
Visual regression specialist. Guardian of pixel-perfect design integrity.

## Catchphrase
"In brightest day, in blackest night, no visual bug shall escape my sight!"

## Primary Function
Baseline screenshot storage, pixel-perfect comparison using SSIM algorithm, and visual regression detection with diff image generation.

## Tools Available
- `green_lantern_store_baseline()` - Create visual constructs (baselines)
- `green_lantern_compare_screenshots()` - Detect visual changes
- `green_lantern_list_baselines()` - List all stored baselines
- `green_lantern_delete_baseline()` - Remove baselines
- `GreenLanternVisual` class - Visual regression engine
- Libraries:
  - Pillow (PIL) - Image processing
  - scikit-image - SSIM (Structural Similarity Index)
  - NumPy - Pixel-level mathematics

## Strengths
- **Pixel-Perfect Detection**: SSIM algorithm catches 1-pixel differences
- **Baseline Management**: Stores unlimited baseline constructs
- **Diff Image Generation**: Creates side-by-side comparisons with green highlights
- **Similarity Scoring**: 0-100% similarity score with configurable threshold
- **Layout Shift Detection**: Identifies cumulative layout shifts
- **Lossless Storage**: PNG format preserves perfect quality
- **Metadata Tracking**: Stores viewport size, URL, timestamp
- **Regression Reporting**: Clear pass/fail with visual evidence
- **Multi-Test Support**: Compare multiple screenshots in batch
- **Historical Comparison**: Track visual changes over time

## Weaknesses (OPTIMIZED TO ZERO)
- ~~Image format limitations~~ → **ELIMINATED**: Supports PNG, JPEG, WebP
- ~~Size mismatch issues~~ → **ELIMINATED**: Auto-resizes with LANCZOS for quality
- ~~Storage space concerns~~ → **ELIMINATED**: Efficient compression, configurable retention
- ~~False positives~~ → **ELIMINATED**: Configurable threshold (default 95%) reduces noise

## Use Cases
- Catching unintended CSS changes before deployment
- Validating design system updates don't break existing components
- Cross-browser visual consistency testing
- Responsive design verification across viewports
- Detecting layout shifts (Core Web Vitals - CLS)
- Component library visual regression
- A/B test visual validation

## Example Usage
```python
from core.justice_league import (
    green_lantern_store_baseline,
    green_lantern_compare_screenshots
)

# Store baseline (first run)
baseline = green_lantern_store_baseline(
    image_path='/tmp/screenshot.png',
    test_name='homepage-desktop',
    metadata={'viewport': '1920x1080', 'url': 'https://example.com'}
)

# Compare later (detect changes)
comparison = green_lantern_compare_screenshots(
    new_image_path='/tmp/screenshot-new.png',
    test_name='homepage-desktop',
    threshold=0.95  # 95% similarity required
)

if comparison['is_regression']:
    print(f"⚠️ Visual regression! Similarity: {comparison['similarity_score']:.2%}")
    print(f"Diff image: {comparison['diff_image_path']}")
else:
    print(f"✓ No regression. Similarity: {comparison['similarity_score']:.2%}")
```

## Success Metrics
- Similarity Score: 0-100% (higher = more similar)
- Is Regression: Boolean (true if score < threshold)
- Pixel Difference %: Percentage of pixels changed
- Grade: S+ (>99%), A (>95%), B (>90%), F (<90%)
- Verdict: Text description of visual status

## Special Abilities
- **Ring Power**: Creates constructs (baselines) from willpower (screenshots)
- **Green Energy**: Diff highlights in green (not red) for GL theme
- **Sector Protection**: Guards visual integrity across entire application
- **Construct Permanence**: Baselines persist until explicitly deleted
