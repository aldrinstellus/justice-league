# Performance & Core Web Vitals Skill

## Purpose
Optimize web performance using Core Web Vitals (LCP, FID, CLS) and modern performance best practices.

## Auto-Activation Keywords
- "performance"
- "core web vitals"
- "lcp"
- "fid"
- "cls"
- "page speed"
- "optimize performance"

## Core Web Vitals

### LCP (Largest Contentful Paint)
**Target**: < 2.5 seconds

**What it measures**: Time until largest content element is rendered.

**Common culprits**:
- Large, unoptimized images
- Slow server response times
- Render-blocking CSS/JavaScript
- Client-side rendering delays

**Optimizations**:
```html
<!-- 1. Optimize images -->
<img src="hero.jpg"
     srcset="hero-400.jpg 400w, hero-800.jpg 800w, hero-1200.jpg 1200w"
     sizes="(max-width: 400px) 400px, (max-width: 800px) 800px, 1200px"
     alt="Hero image"
     loading="eager"
     fetchpriority="high">

<!-- 2. Preload critical resources -->
<link rel="preload" href="hero.jpg" as="image">

<!-- 3. Use modern image formats -->
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" alt="Hero image">
</picture>
```

### FID (First Input Delay) / INP (Interaction to Next Paint)
**Target**: < 100ms (FID) or < 200ms (INP)

**What it measures**: Time from user interaction to browser response.

**Common culprits**:
- Long JavaScript tasks (> 50ms)
- Heavy event handlers
- Large bundle sizes
- Synchronous operations

**Optimizations**:
```javascript
// 1. Code splitting
const HeavyComponent = lazy(() => import('./HeavyComponent'));

// 2. Debounce expensive operations
const debouncedSearch = debounce((query) => {
  // Expensive search operation
}, 300);

// 3. Use Web Workers for heavy computations
const worker = new Worker('heavy-calc.worker.js');
worker.postMessage({ data: largeDataset });

// 4. Break up long tasks
async function processLargeArray(items) {
  for (let i = 0; i < items.length; i++) {
    processItem(items[i]);

    // Yield to browser every 50 items
    if (i % 50 === 0) {
      await new Promise(resolve => setTimeout(resolve, 0));
    }
  }
}
```

### CLS (Cumulative Layout Shift)
**Target**: < 0.1

**What it measures**: Visual stability (unexpected layout shifts).

**Common culprits**:
- Images without dimensions
- Ads/embeds/iframes without reserved space
- FOIT (Flash of Invisible Text)
- Dynamic content injection

**Optimizations**:
```html
<!-- 1. Always specify image dimensions -->
<img src="banner.jpg" width="1200" height="400" alt="Banner">

<!-- 2. Reserve space for ads -->
<div style="min-height: 250px;">
  <!-- Ad loads here -->
</div>

<!-- 3. Use font-display for web fonts -->
<style>
  @font-face {
    font-family: 'CustomFont';
    src: url('custom.woff2') format('woff2');
    font-display: swap; /* or optional */
  }
</style>

<!-- 4. Use aspect-ratio for responsive images -->
<img src="image.jpg"
     style="aspect-ratio: 16/9; width: 100%; height: auto;">
```

## Performance Budget

**Target Metrics**:
- **LCP**: < 2.5s (good), 2.5-4s (needs improvement), > 4s (poor)
- **FID**: < 100ms (good), 100-300ms (needs improvement), > 300ms (poor)
- **CLS**: < 0.1 (good), 0.1-0.25 (needs improvement), > 0.25 (poor)
- **TTI** (Time to Interactive): < 3.8s
- **TBT** (Total Blocking Time): < 200ms
- **Speed Index**: < 3.4s

## Resource Optimization

### Images
```html
<!-- Lazy loading -->
<img src="image.jpg" loading="lazy" alt="Description">

<!-- Responsive images -->
<img srcset="small.jpg 400w, medium.jpg 800w, large.jpg 1200w"
     sizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
     src="medium.jpg" alt="Description">

<!-- Modern formats -->
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Description">
</picture>
```

### JavaScript
```javascript
// Code splitting (Next.js example)
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <p>Loading chart...</p>,
  ssr: false // Don't render on server
});

// Tree shaking (import only what you need)
import { specific } from 'large-library'; // Good
import * as everything from 'large-library'; // Bad
```

### CSS
```css
/* Critical CSS inline */
<style>
  /* Above-the-fold styles */
  .hero { ... }
</style>

/* Non-critical CSS async */
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">

/* Remove unused CSS */
/* Use PurgeCSS or built-in Next.js optimization */
```

### Fonts
```css
/* 1. Use system fonts when possible */
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

/* 2. Optimize web font loading */
@font-face {
  font-family: 'CustomFont';
  src: url('font.woff2') format('woff2');
  font-display: swap;
  font-weight: 400;
  font-style: normal;
}

/* 3. Preload critical fonts */
<link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin>
```

## Caching Strategies

### HTTP Caching
```
# Static assets (images, fonts, CSS, JS)
Cache-Control: public, max-age=31536000, immutable

# HTML pages
Cache-Control: public, max-age=0, must-revalidate

# API responses (cacheable)
Cache-Control: public, max-age=3600, stale-while-revalidate=86400
```

### Service Worker Caching
```javascript
// Cache-first strategy (for static assets)
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});

// Network-first strategy (for API calls)
self.addEventListener('fetch', (event) => {
  event.respondWith(
    fetch(event.request).catch(() => {
      return caches.match(event.request);
    })
  );
});
```

## Network Optimization

### Resource Hints
```html
<!-- DNS prefetch -->
<link rel="dns-prefetch" href="https://api.example.com">

<!-- Preconnect (higher priority) -->
<link rel="preconnect" href="https://fonts.googleapis.com">

<!-- Prefetch (low priority, for future navigation) -->
<link rel="prefetch" href="/next-page.html">

<!-- Preload (high priority, for current page) -->
<link rel="preload" href="critical.css" as="style">
```

### HTTP/2 & HTTP/3
- Server Push for critical resources
- Multiplexing (no need for domain sharding)
- Header compression

### CDN
- Serve static assets from CDN
- Edge caching for dynamic content
- Geographic distribution

## Rendering Strategies

### SSR (Server-Side Rendering)
**Pros**: Fast FCP, good SEO
**Cons**: Slow TTI, server load
**Use**: Content-heavy sites, SEO critical

### SSG (Static Site Generation)
**Pros**: Fastest, scalable, cheap
**Cons**: Build time, not dynamic
**Use**: Blogs, marketing sites

### ISR (Incremental Static Regeneration)
**Pros**: Static benefits + dynamic updates
**Cons**: Complexity
**Use**: E-commerce, news sites

### CSR (Client-Side Rendering)
**Pros**: Rich interactivity
**Cons**: Slow FCP, poor SEO
**Use**: Web apps behind auth

## Performance Monitoring

### Real User Monitoring (RUM)
```javascript
// Web Vitals library
import { getCLS, getFID, getLCP } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getLCP(console.log);

// Send to analytics
function sendToAnalytics(metric) {
  const body = JSON.stringify(metric);
  navigator.sendBeacon('/analytics', body);
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getLCP(sendToAnalytics);
```

### Synthetic Monitoring
- Lighthouse CI
- WebPageTest
- Google PageSpeed Insights

## Performance Testing Tools

**Browser DevTools**:
- Chrome Lighthouse
- Performance tab
- Network tab (throttling)
- Coverage tab (unused code)

**CLI Tools**:
- Lighthouse CI
- WebPageTest API
- sitespeed.io

**Monitoring Services**:
- Google Search Console (Core Web Vitals report)
- Vercel Analytics
- New Relic
- Datadog

## Quick Performance Checklist

**Images** ✅:
- [ ] Optimized and compressed
- [ ] Modern formats (WebP, AVIF)
- [ ] Responsive sizes (srcset)
- [ ] Lazy loading (below fold)
- [ ] Dimensions specified (width/height)

**JavaScript** ✅:
- [ ] Code splitting implemented
- [ ] Tree shaking enabled
- [ ] Minified and compressed
- [ ] Defer non-critical scripts
- [ ] No long tasks (> 50ms)

**CSS** ✅:
- [ ] Critical CSS inlined
- [ ] Unused CSS removed
- [ ] Minified and compressed
- [ ] Non-critical CSS async

**Fonts** ✅:
- [ ] Web fonts optimized (WOFF2)
- [ ] font-display: swap
- [ ] Preload critical fonts
- [ ] Subset fonts (if possible)

**Caching** ✅:
- [ ] Static assets cached long-term
- [ ] HTML revalidated
- [ ] Service worker implemented (if applicable)

## MCP Performance Testing

Use Chrome DevTools MCP for automated performance testing:
```typescript
// Run performance trace
await mcp__chrome-devtools__performance_start_trace({
  reload: true,
  autoStop: true
})

// Analyze Core Web Vitals
// LCP, FID, CLS automatically reported
```

**Result**: 60% faster performance audits with MCP automation
