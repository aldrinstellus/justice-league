# Case Study: ATC Design System - Design Tokens Branch

**Project**: ATC Design System (atc.ds)
**Branch**: `feature/design-tokens-scale`
**Duration**: November - December 2025
**Heroes Involved**: Hephaestus, Artemis, Green Lantern, Batman, Flash, Cyborg

---

## Mission Overview

Transform a basic theme editor into a production-grade design token system with:
- W3C Design Token export to Figma
- Dual unit system (px/rem)
- 7 color format conversions
- Robust build protection

---

## Key Learnings for Justice League

### 1. CSS Cache Corruption Prevention

**Problem**: Build + dev server running simultaneously causes CSS 404 errors.

**Solution**: 5-layer protection system:

```
┌─────────────────────────────────────────────────────────────┐
│                    BUILD PROTECTION SYSTEM                   │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   PREBUILD   │───▶│    BUILD     │───▶│  POSTBUILD   │  │
│  │    GUARD     │    │   PROCESS    │    │ VERIFICATION │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                   │           │
│  [Block if dev]     [Clear .next]      [Verify CSS]        │
│  [Port 3003]        [Run next build]   [Check chunks]      │
└─────────────────────────────────────────────────────────────┘
```

**Applicable To**: ALL Next.js projects

---

### 2. Preference-Based Display Pattern

When users can change how data is displayed (formats, units), use this pattern:

```tsx
// 1. Get preference from store
const { colorFormat } = usePreferencesStore();

// 2. Compute display value
const displayValue = useMemo(() => {
  return formatValue(rawValue, colorFormat);
}, [rawValue, colorFormat]);

// 3. Sync ref-based inputs when preference changes
useEffect(() => {
  if (inputRef.current) {
    inputRef.current.value = displayValue;
  }
}, [displayValue]);
```

**Key Insight**: Audit ALL components that display the data type - not just the obvious ones.

---

### 3. Hydration-Safe Client Rendering

```tsx
const [mounted, setMounted] = useState(false);

useEffect(() => {
  setMounted(true);
}, []);

// Only render client-dependent values after mount
<div style={{
  backgroundColor: mounted ? dynamicColor : 'transparent'
}}>
```

**When to Use**: Any value from localStorage, Zustand, or client-only APIs.

---

### 4. Spacing Audit Pattern

**Bug Pattern**: `flex justify-between` without `gap` causes element collision.

**Fix**:
```tsx
// Always add gap to flex justify-between
<div className="flex justify-between gap-3">
```

**Audit Command**:
```bash
grep -r "flex justify-between" --include="*.tsx" | grep -v "gap"
```

---

### 5. Build Script Safety

**package.json additions**:
```json
{
  "prebuild": "node scripts/check-dev-server.js",
  "postbuild": "node scripts/verify-build.js",
  "build:safe": "npm run kill-dev && rm -rf .next && next build",
  "dev:safe": "bash scripts/safe-dev.sh",
  "dev:fresh": "npm run kill-dev && rm -rf .next && next dev"
}
```

---

## Bug Prevention Checklist

Use this checklist when adding preference/format features:

- [ ] Store preference in Zustand/global state
- [ ] Create selector component for preference
- [ ] Audit ALL display locations for the data type
- [ ] Add format conversion to each display component
- [ ] Handle uncontrolled inputs with `useEffect` sync
- [ ] Test switching between all format options
- [ ] Verify export uses preference

---

## Files Reference

| Purpose | File Pattern |
|---------|--------------|
| Preference Store | `src/stores/preferences-store.ts` |
| Format Converter | `src/utils/color-converter.ts` |
| Selector Component | `src/components/editor/*-selector.tsx` |
| Build Guard | `scripts/check-dev-server.js` |
| Build Verify | `scripts/verify-build.js` |

---

## Metrics Achieved

| Metric | Value |
|--------|-------|
| Bugs Fixed | 15+ |
| Protection Layers | 5 |
| Color Formats | 7 |
| Build Success Rate | 100% (after protections) |
| Hydration Errors | 0 (after fixes) |

---

## Quick Commands

```bash
# Safe development
npm run dev:safe

# Safe production build
npm run build:safe

# After crashes
npm run dev:fresh

# Kill zombie processes
npm run kill-dev
```

---

**Source Branch**: `feature/design-tokens-scale`
**Repository**: https://github.com/aldrinstellus/atc-design-system.git
**Full Learnings**: See `BRANCH-LEARNINGS-feature-design-tokens-scale.md` in project root
