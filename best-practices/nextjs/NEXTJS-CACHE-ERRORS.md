# Next.js Cache Errors: Prevention & Recovery Guide

**Date**: 2025-12-08
**Severity**: HIGH - Can completely break UI rendering
**Incident**: CSS 404 error caused complete styling loss in atc.ds

---

## The Problem

### Symptom
```
GET /_next/static/css/app/layout.css?v=1765189387305 404
```

UI renders without ANY styling - raw HTML elements with no CSS.

### Root Cause
Running `npm run build` while dev server is active corrupts the `.next` cache:

1. Dev server creates CSS file: `.next/static/css/app/layout.css` with hash `v=ABC123`
2. `npm run build` clears `.next` directory
3. Build creates NEW CSS file with DIFFERENT hash `v=XYZ789`
4. Browser still has old hash cached
5. Browser requests `layout.css?v=ABC123` → **404 NOT FOUND**
6. Result: **Complete styling loss**

### Contributing Factors (This Incident)
- 4+ zombie dev servers running on same port (3003)
- Multiple `PORT=3003 npm run dev` commands never killed
- Build ran during active dev session

---

## Prevention Rules (MANDATORY)

### Rule 1: Never Build During Dev
```bash
# WRONG - Will corrupt cache if dev server running
npm run build

# RIGHT - Use safe build that clears cache first
npm run build  # (after adding safe scripts below)
```

### Rule 2: Kill Zombie Processes Before Dev
```bash
# ALWAYS run before starting dev server
lsof -i :3003 -t | xargs kill -9 2>/dev/null

# Or use this one-liner
pkill -f "next dev" 2>/dev/null; sleep 1
```

### Rule 3: Use Safe Package.json Scripts
Add these to every Next.js project:

```json
{
  "scripts": {
    "dev": "next dev",
    "dev:fresh": "rm -rf .next && next dev",
    "build": "rm -rf .next && next build",
    "build:unsafe": "next build",
    "clean": "rm -rf .next node_modules/.cache",
    "start": "next start"
  }
}
```

| Script | Use Case |
|--------|----------|
| `dev` | Normal development |
| `dev:fresh` | After cache corruption or weird errors |
| `build` | Safe build (default) - clears cache first |
| `build:unsafe` | CI/CD only - no dev server conflict |
| `clean` | Nuclear option - clears everything |

### Rule 4: One Port, One Server
Never have multiple dev servers on same port:
```bash
# Check what's running
lsof -i :3003

# Should show exactly 1 node process
# If multiple, kill all and restart
```

---

## Recovery Steps

### Quick Fix (90% of cases)
```bash
# 1. Kill all processes on port
lsof -i :3003 -t | xargs kill -9 2>/dev/null

# 2. Clear cache and restart
rm -rf .next && npm run dev
```

### Full Reset (If quick fix fails)
```bash
# 1. Kill ALL node processes for this project
pkill -f "next dev"

# 2. Clear all caches
rm -rf .next
rm -rf node_modules/.cache

# 3. Hard refresh browser (Cmd+Shift+R on Mac)

# 4. Restart dev server
npm run dev
```

### Nuclear Option (Last resort)
```bash
# Complete clean slate
rm -rf .next node_modules
npm install
npm run dev
```

---

## Detection Checklist

If UI looks broken (no styling), check:

- [ ] Console shows 404 for CSS files?
- [ ] Multiple `node` processes on same port?
- [ ] Recently ran `npm run build`?
- [ ] Dev server been running for hours/days?

If any YES → Run recovery steps above.

---

## Claude Code Agent Rules

### Before Running Build Commands
```
1. CHECK: Is dev server running? → Kill it first
2. CHECK: Are there zombie processes? → Kill them
3. USE: Safe build script (rm -rf .next && next build)
4. NEVER: Run build in background while dev is running
```

### After CSS 404 Error
```
1. STOP: Don't try to debug the CSS issue
2. CLEAR: rm -rf .next
3. RESTART: npm run dev
4. VERIFY: Take screenshot to confirm fix
```

### When Starting New Session
```bash
# Always start with clean state
lsof -i :3003 -t | xargs kill -9 2>/dev/null
rm -rf .next
npm run dev
```

---

## Incident Log

### 2025-12-08: atc.ds CSS Corruption
- **Project**: tweakcn-clone-IT3
- **Port**: 3003
- **Cause**: `npm run build` ran while 4 dev servers were active
- **Symptom**: `layout.css?v=1765189387305 404`
- **Fix**: Killed processes, cleared `.next`, restarted
- **Prevention**: Added safe build scripts to package.json
- **Commit**: `bc71475`

---

## Related Files

- `~/.claude/troubleshooting/nextjs-cache-errors.md` - Quick reference
- Project-specific: `package.json` scripts section

---

## Summary

| Situation | Action |
|-----------|--------|
| CSS 404 error | `rm -rf .next && npm run dev` |
| Multiple processes | `lsof -i :PORT -t \| xargs kill -9` |
| Want to build | Stop dev server FIRST, then build |
| Weird cache issues | `npm run clean` |
| Nothing works | Delete node_modules, reinstall |

**Golden Rule**: One port, one server, clear cache before build.
