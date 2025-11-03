# 🌍 Justice League Global Knowledge Base
## Universal Best Practices for Web Design & Development

**Version**: 1.0.0
**Last Updated**: 2025-10-20
**Maintained By**: Justice League v2.0 (All 13 Heroes)

---

## 📚 Table of Contents

1. [Ethical Design (Litty)](#ethical-design-litty)
2. [Accessibility (Wonder Woman)](#accessibility-wonder-woman)
3. [Performance (Flash)](#performance-flash)
4. [Interactive Elements (Batman)](#interactive-elements-batman)
5. [Component Design (Atom)](#component-design-atom)
6. [Responsive Design (Plastic Man)](#responsive-design-plastic-man)
7. [Security (Martian Manhunter)](#security-martian-manhunter)
8. [SEO (Zatanna)](#seo-zatanna)
9. [Network Optimization (Aquaman)](#network-optimization-aquaman)
10. [Visual Consistency (Green Lantern)](#visual-consistency-green-lantern)
11. [Testing (Green Arrow)](#testing-green-arrow)
12. [Integrations (Cyborg)](#integrations-cyborg)
13. [Design-to-Code Workflows (Artemis)](#design-to-code-workflows-artemis)

---

## 🪔 Ethical Design (Litty)

### Core Principles

**User Respect > Conversion Rate**

### ✅ DO:

1. **Honest Language**
   ```
   ✅ Good: "No thanks, maybe later"
   ❌ Bad: "No thanks, I hate saving money"
   ```

2. **Transparent Pricing**
   ```
   ✅ Show ALL costs upfront before checkout
   ❌ Hidden fees at final step
   ```

3. **Clear Consent**
   ```
   ✅ Equal-weight buttons: [Accept] [Decline]
   ❌ Highlighted "Accept" vs tiny "Decline"
   ```

4. **Easy Opt-Out**
   ```
   ✅ Unsubscribe link in every email
   ❌ "Contact customer service to cancel"
   ```

5. **Respect User Time**
   ```
   ✅ Save form progress
   ❌ Clear form on error without saving
   ```

### ❌ AVOID (15 Dark Patterns):

| Pattern | Description | Example |
|---------|-------------|---------|
| **Confirmshaming** | Shame user for declining | "No thanks, I hate good deals" |
| **Hidden Costs** | Reveal fees late | $99 → $149 at checkout |
| **Bait & Switch** | Change offer after signup | "Free trial" → auto-charges |
| **Roach Motel** | Easy in, hard out | Simple subscribe, complex cancel |
| **Privacy Zuckering** | Trick into sharing data | Pre-checked "Share with partners" |
| **Forced Continuity** | Auto-renewal without notice | Trial ends, charges without warning |
| **Friend Spam** | Spam contacts without consent | "Invite all contacts" pre-selected |
| **Disguised Ads** | Ads look like content | "Recommended" = paid placement |
| **Misdirection** | Highlight wrong choice | Big "Yes" vs tiny "No thanks" |
| **Price Comparison Prevention** | Block comparison shopping | Disable right-click, hide prices |
| **Sneak into Basket** | Add items without consent | "Protection plan" auto-added |
| **Trick Questions** | Double negatives | "Don't not send me emails" |
| **Urgency/Scarcity** | Fake countdown timers | Timer resets on refresh |
| **Obstruction** | Make tasks artificially hard | Cancel requires phone call |
| **Nagging** | Endless popups | Cookie popup on every page |

### 👥 Think About Real Users:

- **👵 Ammachi (72)**: Would she understand this? Is text big enough?
- **🦯 Priya (35)**: Can screen readers navigate this?
- **👴 Kuttan Uncle (68)**: Can he see the contrast?
- **👩‍🏫 Village Teacher (45)**: Will this waste her mobile data?
- **📚 Dyslexic Student (19)**: Is text clear and well-formatted?

### 📏 Ethical Design Checklist:

- [ ] No manipulative language (confirmshaming, urgency)
- [ ] All costs shown upfront
- [ ] Easy to cancel/unsubscribe
- [ ] Clear, honest CTAs
- [ ] Respect user's "No"
- [ ] Save user progress
- [ ] No auto-play audio/video
- [ ] Privacy-respecting defaults
- [ ] Equal-weight consent options
- [ ] No fake scarcity/urgency

---

## ⚡ Accessibility (Wonder Woman)

### WCAG 2.1 Level AA Compliance

### ✅ Text & Typography:

```css
/* Minimum Requirements */
body {
  font-size: 16px;        /* Minimum for body text */
  line-height: 1.5;       /* 150% for readability */
  color: #1a1a1a;         /* 4.5:1 contrast on white */
  font-family: sans-serif; /* Clear, readable font */
}

h1, h2, h3 {
  line-height: 1.2;       /* Tighter for headings */
  font-weight: 600;       /* Clear hierarchy */
}
```

**Guidelines**:
- **Font Size**: 16px minimum for body (14px absolute minimum)
- **Line Height**: 1.5 for body text, 1.2 for headings
- **Line Length**: 50-75 characters per line (optimal readability)
- **Contrast**: 4.5:1 for normal text, 3:1 for large text (18px+)

### ✅ Color Contrast:

| Text Size | Minimum Contrast |
|-----------|------------------|
| Normal text (<18px) | 4.5:1 |
| Large text (≥18px or 14px bold) | 3:1 |
| UI components (buttons, inputs) | 3:1 |

**Tools**: WebAIM Contrast Checker, Chrome DevTools

### ✅ Keyboard Navigation:

```html
<!-- All interactive elements must be keyboard accessible -->
<button tabindex="0">Keyboard accessible button</button>
<a href="#" tabindex="0">Keyboard accessible link</a>

<!-- Skip links for screen readers -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- Focus indicators (never remove outline!) -->
<style>
  button:focus,
  a:focus,
  input:focus {
    outline: 2px solid #0066cc;
    outline-offset: 2px;
  }

  /* Better visible focus */
  :focus-visible {
    outline: 3px solid #0066cc;
    outline-offset: 2px;
  }
</style>
```

### ✅ Semantic HTML:

```html
<!-- ✅ GOOD: Semantic structure -->
<header>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
    </ul>
  </nav>
</header>

<main id="main-content">
  <h1>Page Title</h1>

  <article>
    <h2>Article Title</h2>
    <p>Content...</p>
  </article>
</main>

<footer>
  <p>&copy; 2025</p>
</footer>

<!-- ❌ BAD: Div soup -->
<div class="header">
  <div class="nav">
    <div class="link">Home</div>
  </div>
</div>
```

### ✅ ARIA Attributes:

```html
<!-- Buttons that open menus -->
<button
  aria-haspopup="menu"
  aria-expanded="false"
  aria-controls="dropdown-menu">
  Menu
</button>

<!-- Form inputs with labels -->
<label for="email">Email address</label>
<input
  type="email"
  id="email"
  aria-required="true"
  aria-describedby="email-help">
<span id="email-help">We'll never share your email</span>

<!-- Loading states -->
<div aria-live="polite" aria-busy="true">
  Loading...
</div>

<!-- Images -->
<img src="chart.png" alt="Revenue chart showing 20% growth in Q4">

<!-- Decorative images -->
<img src="decorative.png" alt="" role="presentation">
```

### ✅ Alt Text Guidelines:

```html
<!-- ✅ GOOD: Descriptive -->
<img src="product.jpg" alt="Red cotton t-shirt, size medium, front view">

<!-- ✅ GOOD: Context matters -->
<a href="/product">
  <img src="product.jpg" alt="View red cotton t-shirt details">
</a>

<!-- ✅ GOOD: Decorative (empty alt) -->
<img src="decorative-line.png" alt="">

<!-- ❌ BAD: Useless -->
<img src="product.jpg" alt="image">
<img src="product.jpg" alt="img_12345.jpg">

<!-- ❌ BAD: Missing -->
<img src="product.jpg">
```

### 📏 Accessibility Checklist:

- [ ] Minimum 16px font size
- [ ] 4.5:1 color contrast (normal text)
- [ ] All interactive elements keyboard accessible
- [ ] Visible focus indicators (never remove outline!)
- [ ] Semantic HTML (header, nav, main, footer)
- [ ] All images have alt text (or alt="" if decorative)
- [ ] Form inputs have associated labels
- [ ] ARIA attributes where needed
- [ ] Skip links for screen readers
- [ ] Tested with screen reader (NVDA/JAWS)
- [ ] Tested keyboard-only navigation

---

## ⚡ Performance (Flash)

### Core Web Vitals

Target metrics for excellent performance:

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | ≤2.5s | 2.5-4.0s | >4.0s |
| **FID** (First Input Delay) | ≤100ms | 100-300ms | >300ms |
| **CLS** (Cumulative Layout Shift) | ≤0.1 | 0.1-0.25 | >0.25 |
| **INP** (Interaction to Next Paint) | ≤200ms | 200-500ms | >500ms |
| **TTFB** (Time to First Byte) | ≤800ms | 800-1800ms | >1800ms |

### ✅ Optimize Images:

```html
<!-- Modern formats with fallbacks -->
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Description" loading="lazy" width="800" height="600">
</picture>

<!-- Responsive images -->
<img
  srcset="small.jpg 480w, medium.jpg 800w, large.jpg 1200w"
  sizes="(max-width: 600px) 480px, (max-width: 1000px) 800px, 1200px"
  src="medium.jpg"
  alt="Description"
  loading="lazy">

<!-- Native lazy loading -->
<img src="below-fold.jpg" alt="Description" loading="lazy">
```

**Guidelines**:
- Use WebP/AVIF formats (60-80% smaller than JPEG)
- Lazy load images below the fold
- Provide width/height to prevent CLS
- Compress images (TinyPNG, Squoosh)
- Use CDN for image delivery

### ✅ Optimize JavaScript:

```javascript
// ✅ Code splitting
const HeavyComponent = lazy(() => import('./HeavyComponent'));

// ✅ Tree shaking (import only what you need)
import { debounce } from 'lodash/debounce'; // ✅
import _ from 'lodash'; // ❌ Imports entire library

// ✅ Defer non-critical scripts
<script src="analytics.js" defer></script>

// ✅ Use async for independent scripts
<script src="tracking.js" async></script>
```

### ✅ Optimize CSS:

```css
/* ✅ Critical CSS inline in <head> */
<style>
  /* Above-the-fold styles only */
  body { font-family: sans-serif; }
  .header { background: #000; }
</style>

/* ✅ Non-critical CSS loaded async */
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">

/* ❌ Avoid @import (blocks rendering) */
@import url('another.css'); /* DON'T DO THIS */
```

### ✅ Optimize Fonts:

```html
<!-- Preload critical fonts -->
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>

<!-- Use font-display -->
<style>
  @font-face {
    font-family: 'MyFont';
    src: url('/fonts/main.woff2') format('woff2');
    font-display: swap; /* Show fallback while loading */
  }
</style>

<!-- Limit font weights -->
/* ✅ Load only what you need */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

/* ❌ Loading all weights */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900');
```

### 📏 Performance Checklist:

- [ ] LCP < 2.5s
- [ ] FID < 100ms
- [ ] CLS < 0.1
- [ ] Images optimized (WebP/AVIF)
- [ ] Images lazy loaded
- [ ] Code splitting implemented
- [ ] Critical CSS inlined
- [ ] Fonts optimized (woff2, font-display: swap)
- [ ] JavaScript deferred/async
- [ ] Tested with Lighthouse
- [ ] Tested on slow 3G network

---

## 🦇 Interactive Elements (Batman)

### Button Best Practices

```html
<!-- ✅ GOOD: Clear, descriptive buttons -->
<button type="submit">Create Account</button>
<button type="button" aria-label="Close dialog">×</button>
<button disabled aria-disabled="true">Processing...</button>

<!-- ❌ BAD: Vague buttons -->
<button>Click</button>
<button>Submit</button> <!-- Submit what? -->
<div onclick="...">Button</div> <!-- Not a button! -->
```

**Guidelines**:
- Use `<button>` or `<a>` (not `<div onclick>`)
- Descriptive text ("Create Account" not "Submit")
- Minimum 44x44px touch target (mobile)
- Visible focus states
- Disabled state when processing

### Form Best Practices

```html
<!-- ✅ GOOD: Accessible form -->
<form>
  <label for="email">Email address</label>
  <input
    type="email"
    id="email"
    name="email"
    aria-required="true"
    aria-describedby="email-help"
    autocomplete="email">
  <span id="email-help">We'll never share your email</span>

  <!-- Error state -->
  <input
    type="email"
    id="email"
    aria-invalid="true"
    aria-describedby="email-error">
  <span id="email-error" role="alert">Please enter a valid email</span>
</form>
```

**Guidelines**:
- Every input has a `<label>`
- Use proper input types (email, tel, number)
- Add `autocomplete` attributes
- Show errors inline with `aria-invalid`
- Don't disable paste
- Preserve data on errors

### Touch Targets

```css
/* Minimum 44x44px for touch */
button,
a,
input[type="checkbox"],
input[type="radio"] {
  min-width: 44px;
  min-height: 44px;
  /* Or padding to reach 44x44 */
}

/* Increase click area with padding */
.small-icon-button {
  padding: 12px;  /* Makes 20px icon → 44px total */
}
```

### 📏 Interactive Elements Checklist:

- [ ] All buttons properly labeled
- [ ] Touch targets ≥44x44px
- [ ] Forms have labels for all inputs
- [ ] Autocomplete attributes used
- [ ] Error messages clear and helpful
- [ ] Focus states visible
- [ ] Loading states indicated
- [ ] Keyboard accessible (Tab, Enter, Space)
- [ ] Tested with keyboard only

---

## 🔬 Component Design (Atom)

### Design System Principles

**Consistency > Creativity**

### ✅ Component Anatomy:

```
Component = Base + Variants + States + Composition

Example: Button
├── Base (default style)
├── Variants (primary, secondary, ghost)
├── States (default, hover, focus, active, disabled)
└── Sizes (sm, md, lg)
```

### ✅ Naming Convention:

```
ComponentName-variant-size-state

Examples:
- Button-primary-lg
- Card-outline-md
- Input-error
```

### ✅ Component Library Structure:

```
components/
├── Button/
│   ├── Button.tsx
│   ├── Button.test.tsx
│   ├── Button.stories.tsx
│   └── Button.module.css
│
├── Card/
│   ├── Card.tsx
│   ├── CardHeader.tsx
│   ├── CardContent.tsx
│   ├── CardFooter.tsx
│   └── index.ts
│
└── index.ts (exports all)
```

### ✅ Design Tokens:

```css
:root {
  /* Colors */
  --color-primary: #0066cc;
  --color-secondary: #6c757d;
  --color-success: #28a745;
  --color-danger: #dc3545;
  --color-warning: #ffc107;

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'Fira Code', monospace;

  /* Font sizes */
  --text-xs: 0.75rem;   /* 12px */
  --text-sm: 0.875rem;  /* 14px */
  --text-base: 1rem;    /* 16px */
  --text-lg: 1.125rem;  /* 18px */
  --text-xl: 1.25rem;   /* 20px */

  /* Spacing */
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */

  /* Border radius */
  --radius-sm: 0.125rem; /* 2px */
  --radius-md: 0.375rem; /* 6px */
  --radius-lg: 0.5rem;   /* 8px */
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}
```

### 📏 Component Design Checklist:

- [ ] Consistent naming convention
- [ ] All variants documented
- [ ] All states implemented (hover, focus, active, disabled)
- [ ] Responsive across breakpoints
- [ ] Accessible (ARIA, keyboard)
- [ ] Design tokens used (no hardcoded values)
- [ ] Storybook documentation
- [ ] Unit tests
- [ ] Visual regression tests

---

## 🤸 Responsive Design (Plastic Man)

### Mobile-First Approach

```css
/* ✅ Mobile first (default) */
.container {
  padding: 1rem;
  font-size: 1rem;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    padding: 1.5rem;
    font-size: 1.125rem;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

### Standard Breakpoints:

| Device | Width | Breakpoint |
|--------|-------|------------|
| Mobile (portrait) | <640px | default |
| Mobile (landscape) | ≥640px | sm |
| Tablet | ≥768px | md |
| Laptop | ≥1024px | lg |
| Desktop | ≥1280px | xl |
| Large Desktop | ≥1536px | 2xl |

### ✅ Responsive Images:

```html
<!-- Responsive with srcset -->
<img
  srcset="image-320w.jpg 320w,
          image-640w.jpg 640w,
          image-1024w.jpg 1024w"
  sizes="(max-width: 640px) 100vw,
         (max-width: 1024px) 50vw,
         33vw"
  src="image-640w.jpg"
  alt="Description">
```

### ✅ Responsive Typography:

```css
/* Fluid typography */
:root {
  --font-size-sm: clamp(0.875rem, 0.8rem + 0.25vw, 1rem);
  --font-size-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --font-size-lg: clamp(1.125rem, 1rem + 0.625vw, 1.5rem);
  --font-size-xl: clamp(1.25rem, 1.1rem + 0.75vw, 2rem);
}
```

### 📏 Responsive Design Checklist:

- [ ] Mobile-first CSS
- [ ] Tested on real devices
- [ ] Touch targets ≥44x44px
- [ ] No horizontal scroll on mobile
- [ ] Readable font sizes (≥16px)
- [ ] Images responsive
- [ ] Tables responsive (scroll or stack)
- [ ] Navigation adapts to mobile
- [ ] Forms usable on mobile
- [ ] Tested on slow networks

---

## 🧠 Security (Martian Manhunter)

### OWASP Top 10 Protection

### 1. Injection Prevention

```javascript
// ✅ GOOD: Parameterized queries
const user = await db.query(
  'SELECT * FROM users WHERE email = $1',
  [userEmail]
);

// ❌ BAD: SQL injection vulnerable
const user = await db.query(
  `SELECT * FROM users WHERE email = '${userEmail}'`
);
```

### 2. XSS Prevention

```javascript
// ✅ GOOD: Escape user input
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(dirty);

// ✅ Use React (auto-escapes)
<div>{userInput}</div>

// ❌ BAD: dangerouslySetInnerHTML with raw input
<div dangerouslySetInnerHTML={{__html: userInput}} />
```

### 3. CSRF Protection

```javascript
// ✅ GOOD: CSRF tokens
<form>
  <input type="hidden" name="_csrf" value="{csrfToken}" />
</form>

// ✅ SameSite cookies
res.cookie('session', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict'
});
```

### 4. Authentication

```javascript
// ✅ GOOD: Bcrypt for passwords
const bcrypt = require('bcrypt');
const hash = await bcrypt.hash(password, 10);

// ✅ Strong password requirements
// - Minimum 12 characters
// - Mix of upper, lower, numbers, symbols
// - Not in common password list

// ✅ Rate limiting
const rateLimit = require('express-rate-limit');
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5 // 5 attempts
});
app.use('/login', limiter);
```

### 5. Sensitive Data

```javascript
// ✅ GOOD: Environment variables
const apiKey = process.env.API_KEY;

// ❌ BAD: Hardcoded secrets
const apiKey = 'sk-1234567890abcdef';

// ✅ HTTPS only
if (req.protocol !== 'https') {
  return res.redirect('https://' + req.hostname + req.url);
}
```

### 📏 Security Checklist:

- [ ] SQL injection protected (parameterized queries)
- [ ] XSS protected (input sanitization)
- [ ] CSRF tokens on forms
- [ ] HTTPS enforced
- [ ] Passwords hashed (bcrypt, argon2)
- [ ] Rate limiting on login
- [ ] Secrets in environment variables
- [ ] Security headers (CSP, X-Frame-Options)
- [ ] Dependencies updated (no known vulnerabilities)
- [ ] Input validation on server AND client

---

## 🎩 SEO (Zatanna)

### On-Page SEO

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Title (50-60 characters) -->
  <title>Best Practices for Web Design | Justice League KB</title>

  <!-- Meta description (150-160 characters) -->
  <meta name="description" content="Comprehensive guide to web design best practices including accessibility, performance, security, and ethical design.">

  <!-- Open Graph (social sharing) -->
  <meta property="og:title" content="Best Practices for Web Design">
  <meta property="og:description" content="Comprehensive guide to web design best practices.">
  <meta property="og:image" content="https://example.com/share-image.jpg">
  <meta property="og:url" content="https://example.com/best-practices">
  <meta property="og:type" content="article">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Best Practices for Web Design">
  <meta name="twitter:description" content="Comprehensive guide to web design best practices.">
  <meta name="twitter:image" content="https://example.com/share-image.jpg">

  <!-- Canonical URL -->
  <link rel="canonical" href="https://example.com/best-practices">

  <!-- Structured Data (JSON-LD) -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Best Practices for Web Design",
    "author": {
      "@type": "Organization",
      "name": "Justice League"
    },
    "datePublished": "2025-10-20"
  }
  </script>
</head>
```

### Semantic HTML for SEO

```html
<!-- ✅ Proper heading hierarchy -->
<h1>Main Page Title</h1>
  <h2>Section Title</h2>
    <h3>Subsection Title</h3>

<!-- ❌ Skipping levels -->
<h1>Title</h1>
<h4>Subtitle</h4> <!-- Skipped h2 and h3 -->
```

### 📏 SEO Checklist:

- [ ] Unique title tag (50-60 chars)
- [ ] Meta description (150-160 chars)
- [ ] H1 tag (only one per page)
- [ ] Proper heading hierarchy (H1 → H2 → H3)
- [ ] Alt text on all images
- [ ] Open Graph tags
- [ ] Twitter Card tags
- [ ] Canonical URLs
- [ ] Sitemap.xml
- [ ] Robots.txt
- [ ] Mobile-friendly
- [ ] Page speed < 3s

---

## 🌊 Network Optimization (Aquaman)

### Resource Loading

```html
<!-- Preconnect to external domains -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://cdn.example.com">

<!-- Preload critical resources -->
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/critical.css" as="style">

<!-- DNS prefetch for later-needed domains -->
<link rel="dns-prefetch" href="https://analytics.example.com">
```

### Compression

```javascript
// Enable gzip/brotli compression
const compression = require('compression');
app.use(compression());
```

### Caching

```javascript
// Cache static assets
app.use('/static', express.static('public', {
  maxAge: '1y',  // 1 year cache
  immutable: true
}));

// Cache headers
res.set('Cache-Control', 'public, max-age=31536000, immutable');
```

### 📏 Network Checklist:

- [ ] Gzip/Brotli compression enabled
- [ ] Static assets cached (1 year)
- [ ] CDN for static files
- [ ] Minified CSS/JS
- [ ] HTTP/2 or HTTP/3
- [ ] Preconnect to external domains
- [ ] Resource hints (preload, dns-prefetch)
- [ ] Tested on slow 3G

---

## 💚 Visual Consistency (Green Lantern)

### Design System

```css
/* Consistent spacing scale */
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;
}

/* Consistent colors */
:root {
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-900: #111827;
}
```

### 📏 Visual Consistency Checklist:

- [ ] Design tokens defined
- [ ] Spacing scale consistent
- [ ] Color palette limited and consistent
- [ ] Typography scale defined
- [ ] Border radius consistent
- [ ] Shadow system defined
- [ ] Icon system consistent
- [ ] Animation timing consistent

---

## 🏹 Testing (Green Arrow)

### Testing Strategy

```javascript
// Unit tests
describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const onClick = jest.fn();
    render(<Button onClick={onClick}>Click</Button>);
    fireEvent.click(screen.getByText('Click'));
    expect(onClick).toHaveBeenCalled();
  });
});

// E2E tests
test('user can create account', async ({ page }) => {
  await page.goto('/signup');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'SecurePass123!');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});
```

### 📏 Testing Checklist:

- [ ] Unit tests (>80% coverage)
- [ ] Integration tests
- [ ] E2E tests (critical paths)
- [ ] Visual regression tests
- [ ] Accessibility tests (axe, WAVE)
- [ ] Performance tests (Lighthouse)
- [ ] Cross-browser tests
- [ ] Mobile device tests

---

## 🤖 Integrations (Cyborg)

### API Best Practices

```javascript
// ✅ RESTful API design
GET    /api/users       // List users
GET    /api/users/:id   // Get user
POST   /api/users       // Create user
PUT    /api/users/:id   // Update user
DELETE /api/users/:id   // Delete user

// ✅ Versioning
GET /api/v1/users

// ✅ Error handling
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "field": "email"
  }
}

// ✅ Rate limiting
{
  "X-RateLimit-Limit": "100",
  "X-RateLimit-Remaining": "95",
  "X-RateLimit-Reset": "1635724800"
}
```

### 📏 Integration Checklist:

- [ ] API versioned
- [ ] Rate limiting implemented
- [ ] Error handling consistent
- [ ] Authentication required
- [ ] CORS configured
- [ ] API documentation (OpenAPI/Swagger)
- [ ] Webhooks secured
- [ ] Third-party dependencies updated

---

## 🎨 Design-to-Code Workflows (Artemis)

### Figma MCP + Claude Code + Playwright Workflow

**For**: Building responsive component libraries at scale (3+ components, 2+ breakpoints)

**Why Use This**: Catch computed CSS bugs that visual inspection misses, validate 84+ variations programmatically

**Read Full Workflow**: [Figma MCP + Claude Code + Playwright](./workflows/figma-mcp-claude-playwright-workflow.md)

### The Three-Tool System

```
Figma MCP → Extract exact design tokens (not interpretations)
    ↓
Claude Code → Synthesize responsive Tailwind components
    ↓
Playwright MCP → Validate computed CSS properties
```

### 7-Step Workflow (Quick Reference)

1. **Query All Breakpoints** - Get Figma code for desktop (1920px), laptop (1440px), tablet (1024px), mobile (393px)
2. **Build Comparison Tables** - Document what changes between breakpoints (padding, font-size, layout, gap)
3. **Implement with Exact Values** - Use Tailwind arbitrary values `px-[331px]` for exact Figma specs
4. **Visual Validation** - Automated screenshots at each breakpoint
5. **Computed Style Verification** - Measure flex-grow, widths, gaps programmatically
6. **Console Error Check** - Automated monitoring for runtime issues
7. **Fix & Re-validate** - Address bugs, confirm with Playwright

### Key Principles

```typescript
// ✅ GOOD: Query all breakpoints first
const desktop = await figmaMCP.getCode('1920px-frame');
const laptop = await figmaMCP.getCode('1440px-frame');
const tablet = await figmaMCP.getCode('1024px-frame');
const mobile = await figmaMCP.getCode('393px-frame');

// Compare and build responsive component
const comparisonTable = compareBreakpoints([desktop, laptop, tablet, mobile]);

// ❌ BAD: Build desktop first, then "make it responsive"
const desktop = await figmaMCP.getCode('1920px-frame');
// ...implement desktop...
// ...add mobile classes later (misses layout changes!)
```

### Comparison Table Example

```markdown
| Property      | Desktop  | Laptop  | Tablet   | Mobile   |
|---------------|----------|---------|----------|----------|
| **Padding X** | 331px    | 346px   | 233.78px | 20px     |
| **Padding Y** | 89px     | 63px    | 42.57px  | 24px     |
| **Font Size** | 24px     | 24px    | 16.216px | 14px     |
| **Layout**    | flex-row | flex-row| flex-row | flex-col ⚠️ |
| **Gap**       | 28px     | 28px    | 8.512px  | 16px     |
```

### Implementation with Tailwind Arbitrary Values

```jsx
// ✅ GOOD: Exact values from Figma
<div className={cn(
  // Mobile-first base
  'flex flex-col',
  'gap-[28px]',
  'py-[89px] px-[331px]',
  'text-[24px]',

  // Tablet overrides
  'tablet:flex-row',
  'tablet:gap-[8.512px]',
  'tablet:py-[42.57px] tablet:px-[233.78px]',
  'tablet:text-[16.216px]',

  // Laptop overrides
  'laptop:py-[63px] laptop:px-[346px]'
)}>
  {children}
</div>

// ❌ BAD: Approximations
<div className="flex flex-col gap-7 py-20 px-80 text-2xl tablet:flex-row tablet:gap-2 tablet:py-10 tablet:px-56">
  {children}
</div>
```

### Playwright Validation

```typescript
// Computed style verification
const flexGrow = await page.locator('.card').evaluate(
  el => window.getComputedStyle(el).flexGrow
);
expect(flexGrow).toBe('1'); // Catches invisible flex-grow bugs!

// Width validation
const width = await page.locator('.container').evaluate(
  el => el.offsetWidth
);
expect(width).toBe(1142); // Catches layout issues

// Responsive visibility
await page.setViewportSize({ width: 393, height: 844 }); // Mobile
const visibleLinks = await page.locator('nav a:visible').count();
expect(visibleLinks).toBe(0); // Catches responsive visibility bugs
```

### Common Bugs This Catches

| Bug Type | Visual Inspection | Computed Style Check |
|----------|-------------------|----------------------|
| Invisible flex-grow issues | ✅ Looks correct | ❌ Actually `flex-grow: 0` |
| Mobile component mismatch | ⚠️  Might miss | ✅ Different node ID detected |
| Responsive visibility bugs | ⚠️  Hard to test | ✅ Element count verified |
| Typography scaling | ⚠️  "Looks close" | ✅ Exact font-size validated |

### Best Practices

- **Never assume mobile = shrunk desktop** - Always query all breakpoints
- **Use Tailwind arbitrary values** - `px-[331px]` not `px-80` (approximation)
- **Validate computed properties** - flex-grow, widths, gaps (not just visuals)
- **Think mobile-first** - Establish base state before responsive overrides
- **Automate validation** - Manual checking doesn't scale beyond ~10 components
- **Document everything** - Comparison tables, design tokens, validation checklists

### When NOT to Use This Workflow

- Single landing pages (<5 components)
- Quick prototypes without multi-breakpoint requirements
- Projects without access to Figma MCP
- Simple static sites

### Metrics & ROI

```
Time Investment: ~2 hours setup
Time Savings: ~20 min per component
Break-even: After ~6 components

Scale Example:
21 components × 4 breakpoints = 84 variations
Traditional approach: 45 min/component = ~16 hours
This workflow: 25 min/component = ~9 hours
Savings: 7 hours + 12+ bugs caught pre-deployment
```

### Tools Required

```json
{
  "figma-mcp": "Subscription-based (or open-source API with limits)",
  "claude-code": "AI assistant with MCP support",
  "playwright-mcp": "Free (or standalone Playwright)",
  "tailwind-css": "With arbitrary values support"
}
```

### 📏 Design-to-Code Checklist:

- [ ] All breakpoints queried before coding
- [ ] Comparison table created (documents all changes)
- [ ] Tailwind arbitrary values used (exact specs)
- [ ] Visual snapshots captured at all breakpoints
- [ ] Computed CSS properties validated
- [ ] Console errors monitored
- [ ] Mobile-first approach (base state defined)
- [ ] Responsive visibility logic verified
- [ ] Component mappings documented
- [ ] Validation passed at all 4 breakpoints

### Further Reading

- Full workflow documentation: `./workflows/figma-mcp-claude-playwright-workflow.md`
- Workflow metadata: `./workflows/WORKFLOW_INDEX.json`
- Article source: [Medium - Experience Story](https://medium.com/javascript-in-plain-english/experience-story-figma-mcp-claude-code-playwright-68b20bb0f8ce)

---

## 🎯 Quick Reference Summary

| Hero | Focus | Key Metric |
|------|-------|------------|
| 🪔 Litty | Ethics | No dark patterns |
| ⚡ Wonder Woman | Accessibility | WCAG 2.1 AA |
| ⚡ Flash | Performance | LCP < 2.5s |
| 🦇 Batman | Interactive | All functional |
| 🔬 Atom | Components | Consistent |
| 🤸 Plastic Man | Responsive | Mobile-first |
| 🧠 Martian Manhunter | Security | OWASP Top 10 |
| 🎩 Zatanna | SEO | Meta tags complete |
| 🌊 Aquaman | Network | Compressed & cached |
| 💚 Green Lantern | Visual | Design tokens used |
| 🏹 Green Arrow | Testing | >80% coverage |
| 🤖 Cyborg | Integrations | API documented |
| 🎨 Artemis | Design-to-Code | Figma MCP validated |

---

## 📝 How to Use This Knowledge Base

1. **Before Building**: Review relevant sections
2. **During Development**: Reference checklists
3. **Before Launch**: Validate against all checklists
4. **Continuous**: Update with new learnings

---

## 🔄 Contributing

Found a best practice we missed? Submit updates to this knowledge base!

**Format**:
```markdown
### ✅ Practice Name:

**Why**: Explanation
**How**: Code example
**Impact**: User benefit
```

---

**"Together, we make designs perfect, secure, responsive, discoverable, and ethical!"**

*Maintained by the Justice League v2.0* 🦸


### autonomous-error-recovery

**Category**: methodologies

Confidence-based auto-fix with self-learning: 80%+ confidence = auto-implement, 50-79% = suggest, Oracle learns from every fix outcome

**Accuracy**: 100%

**Best_For**:

**Pros**:

**Cons**:

*Added: 2025-10-30*
