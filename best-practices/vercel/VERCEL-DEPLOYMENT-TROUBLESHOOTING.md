# Vercel Deployment Troubleshooting Guide

> **For Superman & Oracle**: This guide captures real deployment failures and solutions from the ATCK project (2025-12-01). Use these patterns to diagnose Vercel deployment issues quickly.

---

## Quick Reference - Common Errors

### 1. Duplicate Path Error (`/vercel/path0/vercel/path0/`)

**Error Message**:
```
Error: ENOENT: no such file or directory, lstat '/vercel/path0/vercel/path0/.next/routes-manifest.json'
```

**Key Indicator**: Path appears TWICE (`/vercel/path0/vercel/path0/`)

**Root Cause**: `outputFileTracingRoot` in `next.config.ts` pointing to parent directories

```ts
// THIS CAUSES THE ERROR - remove it for standalone projects
outputFileTracingRoot: path.join(__dirname, "../../")
```

**Solution**: Remove or comment out `outputFileTracingRoot` from `next.config.ts`

**Why It Happens**: This setting is designed for monorepos where Next.js lives in a subdirectory. When used in standalone projects, it creates path confusion on Vercel's build server.

**Evidence**: ATCK project deployment session (2025-12-01)

---

### 2. Invalid vercel.json Properties

**Error Message**:
```
Error: Invalid vercel.json - should NOT have additional property `nodeVersion`. Please remove it.
```

**Root Cause**: `nodeVersion` is NOT a valid vercel.json property

**Invalid Example**:
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "nodeVersion": "22.x"  // INVALID - causes error
}
```

**Valid Example**:
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs"
}
```

**Solution**: Remove `nodeVersion` from vercel.json. Set Node.js version in:
- Vercel Dashboard → Project Settings → General → Node.js Version
- Or in `.vercel/project.json` under `settings.nodeVersion`

---

### 3. Node.js Version Issues

**Symptom**: Build fails with version-related errors or unexpected behavior

**Valid Node.js Versions** (as of December 2025):
- `18.x` - LTS
- `20.x` - LTS (recommended)
- `22.x` - Current

**Invalid Values**:
- `24.x` - Does not exist yet
- `19.x`, `21.x`, `23.x` - Odd versions are not LTS

**Where to Check**:
1. `.vercel/project.json` → `settings.nodeVersion`
2. Vercel Dashboard → Project Settings

---

## Diagnostic Checklist

Before deploying Next.js to Vercel, verify these:

```markdown
## Pre-Deployment Checklist

- [ ] **next.config.ts**: No `outputFileTracingRoot` (unless monorepo)
- [ ] **vercel.json**: No `nodeVersion` property
- [ ] **Node.js version**: Valid (18.x, 20.x, or 22.x)
- [ ] **Clean build**: Delete `.next/` folder
- [ ] **Fresh link**: Delete `.vercel/` and run `vercel link` if issues persist
```

### Quick Diagnostic Commands

```bash
# Check for outputFileTracingRoot
grep -r "outputFileTracingRoot" next.config.*

# Check vercel.json for invalid properties
cat vercel.json | grep -i "nodeVersion"

# Check current Node.js version setting
cat .vercel/project.json | grep -i "nodeVersion"

# Clean and relink
rm -rf .next .vercel/output
vercel link --yes
```

---

## Prevention Guidelines

### For Standalone Next.js Projects

**DO NOT use these settings**:
```ts
// next.config.ts - REMOVE these for standalone projects
outputFileTracingRoot: path.join(__dirname, "../../")  // Causes duplicate path error
```

**Safe minimal config**:
```ts
// next.config.ts - Safe for Vercel deployment
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Your config here - no outputFileTracingRoot
};

export default nextConfig;
```

### For Monorepos

If you DO need `outputFileTracingRoot` for a monorepo:

1. **Test locally first**:
   ```bash
   vercel build
   ```

2. **Check the output path** - if you see duplicate paths, adjust the config

3. **Consider disabling build cache**:
   ```bash
   # In Vercel Dashboard → Environment Variables
   VERCEL_FORCE_NO_BUILD_CACHE=1
   ```

4. **Alternative**: Use Turborepo or Nx which handle monorepo builds better

---

## Debugging Workflow

When Vercel deployment fails:

```
1. READ THE ERROR MESSAGE CAREFULLY
   ↓
2. Look for these patterns:
   - "/vercel/path0/vercel/path0/" → outputFileTracingRoot issue
   - "should NOT have additional property" → Invalid vercel.json
   - Version errors → Node.js version issue
   ↓
3. Apply the specific fix from this guide
   ↓
4. Clean build artifacts:
   rm -rf .next .vercel/output
   ↓
5. Redeploy:
   vercel --prod --yes
```

---

## Failed Approaches (Don't Waste Time On These)

These do NOT fix the duplicate path error:

| Approach | Result |
|----------|--------|
| Delete Vercel project and recreate | Still fails |
| Disconnect GitHub integration | Still fails |
| Change project name | Still fails |
| Change Node.js version | Still fails |
| Remove nodeVersion from vercel.json | Helps but doesn't fix duplicate path |

**Only removing `outputFileTracingRoot` fixes the duplicate path error.**

---

## Reference

- **GitHub Discussion**: https://github.com/vercel/next.js/discussions/47517
- **Vercel Project Configuration**: https://vercel.com/docs/concepts/projects/project-configuration
- **Evidence Source**: ATCK project deployment session (2025-12-01)

---

## Session Context

**Project**: ATCK (Enterprise Task Manager)
**Date**: 2025-12-01
**Framework**: Next.js 16 with Turbopack
**Outcome**: Successful deployment after removing `outputFileTracingRoot`
**Production URL**: https://atck-iota.vercel.app
