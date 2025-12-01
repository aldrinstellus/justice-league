# Next.js Cache Error Resolution

Complete troubleshooting guide for diagnosing and fixing Next.js localhost errors. Distinguishes between real server errors and phantom browser cache errors.

## Critical Understanding

**CRITICAL**: Oracle must distinguish between **Phantom 500s** (non-blocking) and **Real 500s** (critical) when debugging localhost errors.

---

## Error Type 1: Corrupted .next Cache (BLOCKING)

### Symptoms
- User reports "localhost error" or "page won't load"
- Homepage returns 500 Internal Server Error
- Network: `GET /` returns 500
- Server logs: `ENOENT: no such file or directory, open '.next/static/development/_buildManifest.js.tmp.*'`
- Page completely broken (not cosmetic)

### Diagnosis Protocol

#### Step 1: Use Chrome DevTools MCP
```javascript
// Check console errors
mcp__chrome-devtools__list_console_messages({ types: ["error"] })
// Look for: 500 Internal Server Error messages
```

#### Step 2: Check Network Requests
```javascript
// List recent network requests
mcp__chrome-devtools__list_network_requests({ pageSize: 20 })
// Look for: GET / [failed - 500]
```

#### Step 3: Take Screenshot for Documentation
```javascript
// Capture error state
mcp__chrome-devtools__take_screenshot({ filePath: "error-diagnosis.png" })
```

### Fix Workflow

#### Step 1: Kill Dev Server
```bash
# Find and kill process on port
lsof -ti:3003 | xargs kill -9

# Or use pkill
pkill -f "npm run dev"
```

#### Step 2: Remove Corrupted Cache
```bash
# Navigate to project
cd /path/to/project

# Remove .next cache
rm -rf .next
```

#### Step 3: Fresh Rebuild
```bash
# Restart dev server
npm run dev  # or pnpm dev
```

#### Step 4: Hard Refresh Browser
- **Mac**: `Cmd+Shift+R`
- **Windows**: `Ctrl+Shift+R`
- **Alternative**: DevTools → Right-click refresh → "Empty Cache and Hard Reload"

#### Step 5: Verify Fix with MCP
```javascript
// Hard refresh page
mcp__chrome-devtools__navigate_page({ type: "reload", ignoreCache: true })

// Check console for errors
mcp__chrome-devtools__list_console_messages({ types: ["error"] })
// Expected: <no console messages found>
```

#### Step 6: Take "After" Screenshot
```javascript
// Document fixed state
mcp__chrome-devtools__take_screenshot({ filePath: "fixed-state.png" })
```

### Root Cause
- Multiple rapid dev server restarts corrupt `.next` build cache
- Stale `_buildManifest.js.tmp` references prevent page compilation
- **Server-side** cache corruption (not browser cache)

### Prevention
- Avoid multiple rapid `npm run dev` restarts
- Use Ctrl+C for clean shutdown before restarting
- Let dev server run continuously when possible
- Clean cache after major refactoring: `rm -rf .next`

---

## Error Type 2: Phantom 500s (NON-BLOCKING)

### Symptoms
- Console shows 500 errors for webpack chunks
- Network: Webpack vendor chunks return 404/500
- Network: `GET /` returns 200 OK (page works!)
- Page renders correctly despite console errors
- Errors look like: `Failed to load resource: ./vendor-chunks/lucide-react@0.552.0_react@18.3.1.js (500)`

### Diagnosis
```javascript
// Check Network panel
mcp__chrome-devtools__list_network_requests()
// If GET / = 200 but webpack chunks = 500 → Phantom errors
```

### Fix
Simple hard refresh (no cache rebuild needed):

- **Mac**: `Cmd+Shift+R`
- **Windows**: `Ctrl+Shift+R`
- **Alternative**: DevTools → Right-click refresh → "Empty Cache and Hard Reload"

### Root Cause
- `.next` directory cleared during debugging
- Webpack generates NEW chunk URLs with different hashes
- **Browser cache** still has references to OLD chunk URLs
- Browser tries to fetch old URLs → 404/500 from server
- BUT: New chunks load successfully, app works perfectly

### Key Difference from Real 500s
- ✅ Page renders correctly
- ✅ Network shows `GET /` = 200 OK
- ✅ Only webpack chunks show errors
- ✅ **Browser cache issue, NOT server cache**

---

## Quick Decision Tree

```
User reports "localhost error"
↓
Use Chrome DevTools MCP:
mcp__chrome-devtools__list_network_requests()
↓
┌─────────────────────────┬────────────────────────┐
│ GET / returns 500?      │ GET / returns 200?     │
│ Page won't load?        │ Page loads fine?       │
│                         │                        │
│ → REAL 500              │ → PHANTOM 500          │
│ → rm -rf .next          │ → Hard refresh         │
│ → npm run dev           │ → Cmd+Shift+R          │
└─────────────────────────┴────────────────────────┘
```

---

## Oracle's Error Resolution Checklist

When user reports "localhost error" or "page broken":

1. ✅ **Use MCP First**: `mcp__chrome-devtools__list_console_messages({ types: ["error"] })`
2. ✅ **Check Network**: `mcp__chrome-devtools__list_network_requests()`
3. ✅ **Take Screenshot**: `mcp__chrome-devtools__take_screenshot({ filePath: "error-state.png" })`
4. ✅ **Diagnose**: Is `GET /` returning 500 or 200?
5. ✅ **Apply Correct Fix**:
   - If 500 → `rm -rf .next && npm run dev`
   - If 200 → Hard refresh browser
6. ✅ **Verify Fix**: Check console again with MCP
7. ✅ **Document**: Take "after" screenshot

### Time Savings
5-10 minutes per error with MCP automation vs manual debugging

---

## Real-World Example (2025-11-09)

### Scenario
User: "localhost error"

### Oracle's Response

#### Step 1: Diagnosis with MCP
```javascript
// Checked console
mcp__chrome-devtools__list_console_messages({ types: ["error"] })
// Result: 500 Internal Server Error

// Checked network
mcp__chrome-devtools__list_network_requests()
// Result: GET / → 500 (failed)

// Took screenshot
mcp__chrome-devtools__take_screenshot({ filePath: "error-diagnosis.png" })
```

#### Step 2: Identified Root Cause
Diagnosed: Corrupted .next cache

#### Step 3: Applied Fix
```bash
# Killed dev server
lsof -ti:3003 | xargs kill -9

# Removed cache
cd /Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v15-presentation
rm -rf .next

# Restarted dev server
npm run dev
```

#### Step 4: Verified Fix
```javascript
// Hard refresh
mcp__chrome-devtools__navigate_page({ type: "reload", ignoreCache: true })

// Checked console
mcp__chrome-devtools__list_console_messages({ types: ["error"] })
// Result: <no console messages found> ✅

// Checked network
mcp__chrome-devtools__list_network_requests()
// Result: All requests 200 OK ✅

// Took "after" screenshot
mcp__chrome-devtools__take_screenshot({ filePath: "fixed-state.png" })
```

#### Result
0 errors, all requests 200 OK ✅

### Documentation
Full savepoint: `/Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v15-presentation/PROJECT-SAVEPOINT-2025-11-09-CACHE-FIX.md`

---

## Key Learnings

### 1. Not All 500 Errors Are the Same
Use MCP to distinguish phantom vs real errors. Don't assume all 500s require cache rebuild.

### 2. Chrome DevTools MCP Saves Time
Automated diagnosis beats manual checking. Visual proof via screenshots reduces back-and-forth.

### 3. Visual Proof Matters
Screenshots document the error and fix. User can see exactly what was broken and what's fixed.

### 4. Prevention Is Better
Avoid rapid dev server restarts. Let dev server run continuously when possible.

### 5. Hard Refresh ≠ Cache Rebuild
Different fixes for different issues:
- **Hard refresh**: Browser cache issue (phantom 500s)
- **Cache rebuild**: Server cache issue (real 500s)

---

## Common Variations

### Variation 1: Module Not Found Errors
**Symptoms**:
```
Error: Cannot find module './components/Button'
```

**Cause**: Stale module resolution in .next cache

**Fix**: `rm -rf .next && npm run dev`

---

### Variation 2: Overlapping UI Elements
**Symptoms**:
- UI elements appear stacked on top of each other
- Layout completely broken
- Styles not applied correctly

**Cause**: Stale CSS/component cache

**Fix**: `rm -rf .next && npm run dev`

---

### Variation 3: Build Manifest Errors
**Symptoms**:
```
ENOENT: no such file or directory, open '.next/static/development/_buildManifest.js.tmp.1234567890'
```

**Cause**: Build manifest corruption from rapid restarts

**Fix**: `rm -rf .next && npm run dev`

---

## Related Issues

### Issue: TypeScript Errors After Cache Clean
**Scenario**: Cleaned cache, now seeing TypeScript errors

**Solution**: TypeScript errors were always there, just hidden by broken build. Fix TypeScript errors normally.

---

### Issue: Dev Server Won't Start After Cache Clean
**Scenario**: Removed .next, dev server fails to start

**Solution**:
```bash
# Reinstall dependencies
npm install  # or pnpm install

# Try again
npm run dev
```

---

### Issue: Port Already in Use
**Scenario**: Dev server says port already in use

**Solution**:
```bash
# Find and kill process
lsof -ti:3003 | xargs kill -9

# Start dev server
npm run dev
```

---

## Advanced Debugging

### Check Server Logs
```bash
# Watch dev server logs
npm run dev | tee dev-server.log
```

### Check Node Modules
```bash
# Verify node_modules exists
ls -la node_modules/

# Reinstall if needed
rm -rf node_modules package-lock.json
npm install
```

### Check Build Config
```bash
# Verify next.config.js exists
cat next.config.js

# Check for syntax errors
node -c next.config.js
```

---

## MCP Automation Script

### Complete Diagnosis Workflow
```javascript
// Navigate to page
await mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3003",
  type: "url"
})

// Take "before" state
await mcp__chrome-devtools__take_screenshot({
  filePath: "before-diagnosis.png"
})

// Check console
const consoleErrors = await mcp__chrome-devtools__list_console_messages({
  types: ["error"]
})

// Check network
const networkRequests = await mcp__chrome-devtools__list_network_requests({
  pageSize: 20
})

// Analyze results
if (networkRequests includes "GET / [500]") {
  // Real 500 - cache rebuild needed
  console.log("Diagnosis: Real 500 - Corrupted server cache")
} else if (networkRequests includes "GET / [200]") {
  // Phantom 500 - browser cache issue
  console.log("Diagnosis: Phantom 500 - Browser cache issue")
}
```

---

**Last Updated**: 2025-11-24
**Purpose**: Complete troubleshooting guide for Next.js cache errors with MCP automation
**Reference Savepoint**: `/Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v15-presentation/PROJECT-SAVEPOINT-2025-11-09-CACHE-FIX.md`
