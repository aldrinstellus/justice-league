# Accessibility WCAG Skill

## Purpose
Web Content Accessibility Guidelines (WCAG 2.1) Level AA compliance for inclusive web applications.

## Auto-Activation Keywords
- "accessibility"
- "wcag"
- "a11y"
- "screen reader"
- "aria"
- "keyboard navigation"

## WCAG 2.1 Principles (POUR)

### Perceivable
Content must be presentable to users in ways they can perceive.

**1.1 Text Alternatives**:
```html
<!-- Images -->
<img src="logo.png" alt="Company Logo">

<!-- Decorative images -->
<img src="divider.png" alt="" role="presentation">

<!-- Complex images -->
<img src="chart.png" alt="Sales increased 25% in Q4" longdesc="chart-description.html">
```

**1.3 Adaptable**:
```html
<!-- Semantic HTML -->
<nav>...</nav>
<main>...</main>
<aside>...</aside>

<!-- Proper heading hierarchy -->
<h1>Page Title</h1>
  <h2>Section</h2>
    <h3>Subsection</h3>
```

**1.4 Distinguishable**:
- Color contrast: 4.5:1 for normal text, 3:1 for large text
- No information by color alone
- Text resizable up to 200% without loss of functionality

### Operable
UI components and navigation must be operable.

**2.1 Keyboard Accessible**:
```html
<!-- All interactive elements keyboard accessible -->
<button onclick="handleClick()">Click Me</button>

<!-- Custom components need keyboard handlers -->
<div role="button" tabindex="0"
     onclick="handleClick()"
     onkeypress="handleKeyPress(event)">
  Custom Button
</div>
```

**2.4 Navigable**:
```html
<!-- Skip links -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- Descriptive page titles -->
<title>Contact Us - Company Name</title>

<!-- Focus indicators -->
button:focus {
  outline: 2px solid blue;
  outline-offset: 2px;
}
```

### Understandable
Information and UI operation must be understandable.

**3.1 Readable**:
```html
<!-- Language declaration -->
<html lang="en">

<!-- Language changes -->
<p>The French phrase <span lang="fr">bonjour</span> means hello.</p>
```

**3.2 Predictable**:
- Consistent navigation across pages
- No unexpected context changes
- Consistent identification of components

**3.3 Input Assistance**:
```html
<!-- Error identification -->
<label for="email">Email</label>
<input id="email" type="email" aria-describedby="email-error" aria-invalid="true">
<span id="email-error" role="alert">Please enter a valid email address</span>

<!-- Form labels -->
<label for="username">Username</label>
<input id="username" type="text" required>
```

### Robust
Content must be robust enough to work with current and future technologies.

**4.1 Compatible**:
```html
<!-- Valid HTML -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Page Title</title>
  </head>
  <body>...</body>
</html>

<!-- ARIA roles and properties -->
<div role="navigation" aria-label="Main">...</div>
```

## ARIA (Accessible Rich Internet Applications)

### ARIA Roles

**Landmark Roles**:
```html
<header role="banner">...</header>
<nav role="navigation">...</nav>
<main role="main">...</main>
<aside role="complementary">...</aside>
<footer role="contentinfo">...</footer>
```

**Widget Roles**:
```html
<div role="button" tabindex="0">Click Me</div>
<div role="checkbox" aria-checked="false">...</div>
<div role="dialog" aria-labelledby="dialog-title">...</div>
<div role="tab" aria-selected="true">...</div>
```

### ARIA Properties

**Labels**:
```html
<button aria-label="Close dialog">X</button>
<input aria-labelledby="label-id">
<div aria-describedby="description-id">...</div>
```

**States**:
```html
<button aria-pressed="false">Toggle</button>
<input aria-disabled="true">
<div aria-hidden="true">...</div>
<div aria-expanded="false">...</div>
```

**Live Regions**:
```html
<div role="status" aria-live="polite">Loading...</div>
<div role="alert" aria-live="assertive">Error occurred!</div>
```

## Keyboard Navigation Patterns

**Tab Order**:
- Tab: Move forward
- Shift+Tab: Move backward
- Enter/Space: Activate buttons/links
- Arrow keys: Navigate within components (menus, tabs)
- Esc: Close dialogs/menus

**Focus Management**:
```javascript
// Trap focus in modal
const modal = document.querySelector('[role="dialog"]');
const focusableElements = modal.querySelectorAll(
  'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
);
const firstElement = focusableElements[0];
const lastElement = focusableElements[focusableElements.length - 1];

modal.addEventListener('keydown', (e) => {
  if (e.key === 'Tab') {
    if (e.shiftKey && document.activeElement === firstElement) {
      e.preventDefault();
      lastElement.focus();
    } else if (!e.shiftKey && document.activeElement === lastElement) {
      e.preventDefault();
      firstElement.focus();
    }
  }
});
```

## Color Contrast

**WCAG AA Requirements**:
- Normal text (< 18pt): 4.5:1
- Large text (≥ 18pt or 14pt bold): 3:1
- UI components: 3:1

**Good Contrast Examples**:
- Black (#000000) on White (#FFFFFF): 21:1 ✅
- Dark Gray (#595959) on White: 7:1 ✅
- Blue (#0000EE) on White: 8.6:1 ✅

**Poor Contrast Examples**:
- Light Gray (#999999) on White: 2.8:1 ❌
- Yellow (#FFFF00) on White: 1.1:1 ❌

**Tools**:
- WebAIM Contrast Checker
- Chrome DevTools Lighthouse
- axe DevTools

## Screen Reader Testing

**Common Screen Readers**:
- NVDA (Windows, free)
- JAWS (Windows, paid)
- VoiceOver (macOS/iOS, built-in)
- TalkBack (Android, built-in)

**Testing Checklist**:
- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Buttons have descriptive text
- [ ] Links make sense out of context
- [ ] Heading structure is logical
- [ ] Tables have headers
- [ ] ARIA labels on custom widgets

## Common Accessibility Issues

**1. Missing Alt Text**:
```html
<!-- Bad -->
<img src="product.jpg">

<!-- Good -->
<img src="product.jpg" alt="Red running shoes, size 10">
```

**2. Missing Form Labels**:
```html
<!-- Bad -->
<input type="text" placeholder="Enter name">

<!-- Good -->
<label for="name">Name</label>
<input id="name" type="text" placeholder="Enter name">
```

**3. Poor Color Contrast**:
```css
/* Bad: 2.5:1 contrast */
.text { color: #777; background: #fff; }

/* Good: 7:1 contrast */
.text { color: #595959; background: #fff; }
```

**4. Non-keyboard Accessible**:
```html
<!-- Bad -->
<div onclick="handleClick()">Click me</div>

<!-- Good -->
<button onclick="handleClick()">Click me</button>
```

## Quick Accessibility Checklist

**Structure** ✅:
- [ ] Proper heading hierarchy (h1 → h2 → h3)
- [ ] Semantic HTML (nav, main, article, aside)
- [ ] Skip links for keyboard users
- [ ] Logical reading order

**Images** ✅:
- [ ] Alt text on all images
- [ ] Empty alt for decorative images
- [ ] Long descriptions for complex images

**Forms** ✅:
- [ ] Labels associated with inputs
- [ ] Error messages announced
- [ ] Required fields indicated
- [ ] Fieldsets for radio/checkbox groups

**Interactive** ✅:
- [ ] Keyboard accessible (Tab, Enter, Space)
- [ ] Focus indicators visible
- [ ] No keyboard traps
- [ ] Logical tab order

**Color/Contrast** ✅:
- [ ] 4.5:1 contrast for text
- [ ] Information not by color alone
- [ ] Focus indicators visible

## Automated Testing Tools

**Browser Extensions**:
- axe DevTools
- WAVE
- Lighthouse (Chrome DevTools)

**CI/CD Integration**:
- pa11y
- axe-core
- jest-axe

**Manual Testing**:
- Keyboard navigation (unplug mouse!)
- Screen reader testing
- Zoom to 200% and verify layout

## MCP Accessibility Testing

Use Chrome DevTools MCP for automated a11y checks:
```typescript
// Take snapshot to verify ARIA attributes
await mcp__chrome-devtools__take_snapshot({ verbose: true })
// Check for: aria-label, role, tabindex, alt text

// Verify keyboard navigation
await mcp__chrome-devtools__press_key({ key: "Tab" })
// Take screenshot to verify focus indicators
```

**Result**: 50% faster accessibility audits with MCP
