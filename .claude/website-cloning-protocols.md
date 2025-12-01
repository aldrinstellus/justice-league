# Website Cloning Protocols

## Overview
Multiple approaches for cloning websites with different strengths and use cases.

---

## Method 1: Wget Mirror (Recommended for Static Sites)

### When to Use
- Static HTML/CSS/JS sites
- Need complete offline copy with all assets
- JavaScript frameworks (React, Next.js, Framer, etc.)
- Want exact source code reference
- SiteSucker or other tools fail

### Advantages
- ✅ Downloads ALL assets (HTML, CSS, JS, images, fonts)
- ✅ Converts links to local relative paths
- ✅ Handles multiple domains (CDNs, font providers)
- ✅ Works with any static site
- ✅ Free and built into most systems
- ✅ Complete source code access

### Limitations
- ⚠️ JavaScript won't execute from `file://` due to CORS
- ⚠️ Need to serve via HTTP for full functionality
- ⚠️ Dynamic server-side features won't work

### Installation
```bash
# macOS
brew install wget

# Linux (Debian/Ubuntu)
sudo apt-get install wget

# Linux (RHEL/CentOS)
sudo yum install wget
```

### Command Template
```bash
wget --mirror \
     --convert-links \
     --adjust-extension \
     --page-requisites \
     --no-parent \
     --span-hosts \
     --domains=example.com,cdn.example.com,fonts.googleapis.com,fonts.gstatic.com \
     --wait=0.5 \
     --random-wait \
     --timeout=60 \
     --tries=3 \
     --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://example.com/" \
     2>&1 | tee wget-log.txt
```

### Flag Explanations
- `--mirror`: Recursive download with infinite depth, timestamping
- `--convert-links`: Convert absolute URLs to relative for offline use
- `--adjust-extension`: Add .html to files without extensions
- `--page-requisites`: Download CSS, images, JS needed to display
- `--no-parent`: Don't ascend to parent directory
- `--span-hosts`: Follow links to other hosts (CDNs)
- `--domains=`: Comma-separated list of allowed domains
- `--wait=0.5`: Wait 0.5 seconds between requests (polite)
- `--random-wait`: Randomize wait time (0.5x to 1.5x)
- `--timeout=60`: Network read timeout in seconds
- `--tries=3`: Retry failed downloads 3 times
- `--user-agent=`: Pretend to be a browser (avoid blocks)

### Common Domain Patterns
```bash
# Framer sites
--domains=example.com,framerusercontent.com,fonts.googleapis.com,fonts.gstatic.com

# WordPress sites
--domains=example.com,wp.com,wordpress.com,gravatar.com

# Generic sites with CDN
--domains=example.com,cdn.example.com,cloudflare.com,jsdelivr.net
```

### Serving Downloaded Site Locally
```bash
# Python 3
cd downloaded-site && python3 -m http.server 8000

# Node.js (with serve)
npm install -g serve
serve downloaded-site -p 8000

# Then visit: http://localhost:8000
```

### Expected Results
- **File Count**: 50-500+ files depending on site size
- **Directories**: Domain-based (example.com/, cdn.example.com/)
- **Download Time**: 30 seconds to 5 minutes
- **Assets**: HTML, CSS, JS, images (all scales), fonts

### Troubleshooting

**Issue**: JavaScript not working when opened locally
- **Cause**: CORS policy blocks `file://` protocol from loading modules
- **Solution**: Serve via HTTP (see "Serving Downloaded Site Locally" above)

**Issue**: Missing images from CDN
- **Cause**: CDN domain not in `--domains` list
- **Solution**: Add CDN domain to `--domains` parameter

**Issue**: wget command not found
- **Cause**: wget not installed
- **Solution**: Install wget (see Installation section)

**Issue**: Download incomplete or stuck
- **Cause**: Network issues or rate limiting
- **Solution**: Increase `--wait` time, check `--timeout` value

---

## Method 2: SiteSucker (macOS GUI)

### When to Use
- Prefer GUI interface
- Need visual progress tracking
- Simple static sites
- Want automated retry on failure

### Critical Settings
- **File Types**: Enable ALL (HTML, CSS, JS, images, fonts, etc.)
- **URL Constraints**: Set to "Domain" or "None" (not "Host")
- **Supporting Files**: ENABLED
- **Web Views**: ENABLED
- **Depth**: Set to 5-10 levels
- **External Links**: ENABLED for CDNs

### Limitations
- ⚠️ MacOS only
- ⚠️ May miss assets from external CDNs
- ⚠️ Less control than wget
- ⚠️ Paid software ($5-10)

---

## Method 3: Manual Build (Next.js/React)

### When to Use
- Need to understand site architecture
- Want to add custom features
- Building production app (not just clone)
- Have time for iterative development

### Advantages
- ✅ Clean, maintainable code
- ✅ Can modify and extend
- ✅ Production-ready framework
- ✅ Full control over implementation

### Limitations
- ⚠️ Time-consuming (2-8 hours)
- ⚠️ Risk of missing details
- ⚠️ Requires manual asset download
- ⚠️ May achieve only 80-90% fidelity

### Workflow
1. Scrape original site to analyze structure
2. Download key assets (images, fonts)
3. Build Next.js skeleton
4. Implement sections one by one
5. Compare with original via screenshots
6. Iterate until 100% match

---

## Method 4: Hybrid Approach (Recommended for Complex Sites)

### Process
1. **Download with wget** to get ALL assets and exact structure
2. **Serve downloaded site** via HTTP to verify completeness
3. **Use as reference** to build clean Next.js implementation
4. **Copy assets** from wget download to Next.js public folder
5. **Compare side-by-side** to ensure 100% fidelity

### Why This Works Best
- ✅ Wget ensures no assets are missed
- ✅ Reference copy shows exact layout/spacing
- ✅ Next.js build is clean and maintainable
- ✅ Can verify against downloaded copy at any time
- ✅ Achieves true 100% fidelity

---

## Comparison Matrix

| Method | Time | Fidelity | Maintainability | Assets | Offline |
|--------|------|----------|-----------------|--------|---------|
| Wget | 5 min | 100% | Low | 100% | ✅ Yes |
| SiteSucker | 10 min | 85-95% | Low | 85-95% | ✅ Yes |
| Manual Build | 2-8 hrs | 80-90% | High | Manual | ❌ No |
| Hybrid | 3-10 hrs | 100% | High | 100% | ✅ Yes |

---

## Decision Tree

```
Need 100% fidelity?
├─ Yes → Use Wget or Hybrid
└─ No → Manual Build OK

Need to modify/extend?
├─ Yes → Use Hybrid (wget + Next.js)
└─ No → Use Wget only

Have GUI preference?
├─ Yes (macOS) → Try SiteSucker first, fallback to wget
└─ No → Use wget

Time constraint?
├─ <30 min → Use wget
├─ 1-2 hrs → Try SiteSucker
└─ >2 hrs → Use Hybrid

Complex web app requiring near-perfect clone?
├─ Yes → Use TweakCN Pattern (see Success Stories section)
│         • 20-40 hours over 4 days
│         • 3 iterations (IT1 → IT2 → IT3)
│         • Chrome DevTools verification
│         • Multi-agent coordination
│         • 98% completeness achievable
└─ No → Use standard methods above
```

---

## Real-World Success Stories

### Success Story 1: TweakCN Clone (98% Completeness)

**Project**: ATC Design System (TweakCN Clone)
**Timeline**: 4 days (November 3-7, 2025)
**Cost**: $0
**Result**: 98% complete, production-ready theme editor
**Method**: Hybrid approach with iterative refinement

**Why This Was Successful**:
- **Systematic Research Phase** (Day 1): 32,189-word Master Blueprint documented complete architecture
- **Public Source Code Access** (Day 3): Found jnsahaj/tweakcn on GitHub → 40% → 90% completeness jump
- **Iterative Development** (IT1 → IT2 → IT3): Three major iterations with continuous improvement
- **Chrome DevTools Verification**: Visual validation after each change (standing protocol)
- **Multi-Agent Coordination**: 6 Justice League agents deployed in parallel (6x speed)

**The Pattern That Works**:
```
Day 1: Deep Research (Master Blueprint)
  ↓
Day 2: Gap Analysis (Reality Check: 40-45% complete)
  ↓
Day 3: Source Code Acquisition (Public GitHub found)
  ↓
Day 3-4: Systematic Debugging (4 critical bugs fixed)
  ↓
Day 4: Full Spectrum Validation (98% complete ✅)
```

**Key Metrics**:
- **Completeness**: 98% (production-ready)
- **Code Volume**: 35,000+ lines, 116 components
- **Build Status**: Zero errors, 100% type-safe
- **Visual Fidelity**: 97/100
- **Time Investment**: 20-40 hours over 4 days
- **Iterations**: 3 major versions (IT1, IT2, IT3)

**Critical Success Factors**:
1. **Public source code = 50% time savings** (40% → 90% jump when found)
2. **Iterative refinement works** (IT1 → IT2 → IT3 pattern)
3. **Chrome DevTools verification required** (catches hidden issues server logs miss)
4. **Multi-agent 6x faster** (parallel vs sequential deployment)
5. **Time investment matters** (20-40 hours vs MyCryptoKey's 4 hours)

**Lesson**: For complex web apps requiring near-perfect clones, use the **TweakCN Pattern**:
- Dedicate 20-40 hours over multiple days (not single 4-hour session)
- Use 3 iterations minimum (prototype → integration → production)
- Always verify with Chrome DevTools (visual + console + network)
- Look for public source code first (can save 50% time)
- Deploy multiple agents in parallel for 6x speed

**Full Case Study**: `/Users/admin/Documents/claudecode/best-practices/case-studies/tweakcn-clone/`

---

## Real-World Example: mycryptokey.xyz

### What We Used
**Method**: Wget Mirror

### Command
```bash
mkdir -p mycryptokey-wget && cd mycryptokey-wget
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent \
     --span-hosts \
     --domains=mycryptokey.xyz,framerusercontent.com,fonts.googleapis.com,fonts.gstatic.com \
     --wait=0.5 --random-wait --timeout=60 --tries=3 \
     --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://mycryptokey.xyz/" \
     2>&1 | tee wget-log.txt
```

### Results
- **Files Downloaded**: 155 files
- **Total Size**: 9.8 MB
- **Time**: ~5 minutes
- **HTML Pages**: 10 (home + 5 features + 4 blog posts)
- **Images**: 38 PNG files (multiple scales)
- **JavaScript**: 26 .mjs modules
- **Fonts**: 6 WOFF2 files
- **Fidelity**: 100% (all assets captured)

### Comparison with Manual Build
- **Manual**: 4 hours, 85-90% fidelity, missing scaled images
- **Wget**: 5 minutes, 100% fidelity, all assets present

### Verdict
Wget successfully captured the complete site in 5 minutes vs 4 hours of manual work that only achieved 85% fidelity.

---

## Best Practices

1. **Always add CDN domains** to `--domains` parameter
2. **Use `--wait` and `--random-wait`** to be polite and avoid rate limiting
3. **Save output to log file** with `2>&1 | tee wget-log.txt`
4. **Verify download** by counting files and checking console errors
5. **Serve via HTTP** to test JavaScript functionality
6. **Use as reference** for building clean production code

---

## Future Enhancements

- [ ] Script to auto-detect CDN domains from HTML
- [ ] Post-processing to fix CORS issues for local viewing
- [ ] Auto-conversion to Next.js project structure
- [ ] Asset optimization (image compression, unused file removal)
- [ ] Comparison tool (wget download vs Next.js build)

---

**Last Updated**: 2025-11-24
**Author**: Claude (Justice League System)
**Status**: Production-ready protocol
