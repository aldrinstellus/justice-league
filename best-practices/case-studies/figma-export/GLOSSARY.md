# Figma Export Best Practices - Glossary

**Purpose**: Define key terms used throughout the documentation
**Audience**: Anyone using the Figma export best practices guides
**Updated**: 2025-11-05

---

## Core Concepts

### Figma Export
The process of extracting visual content (designs, frames, components) from Figma files and converting them to static image formats (PNG, PDF, SVG) for use outside Figma.

**Example**: Exporting a design system's 100 component frames to PNG for documentation.

**Related**: [README.md](README.md), [PERFORMANCE-EXPECTATIONS.md](PERFORMANCE-EXPECTATIONS.md)

---

### Frame
A container in Figma that holds design content. Frames are the basic exportable units - similar to artboards in other design tools.

**Structure**:
```
File
  └─ Page
      └─ Section (optional)
          └─ Frame ← Exportable unit
              └─ Layers (shapes, text, components)
```

**Example**: A button component might live in a frame named "Button/Primary/Default"

**Related**: [SCOPE-ESTIMATION-GUIDE.md](SCOPE-ESTIMATION-GUIDE.md#empty-file-filter)

---

### Frame Count
The total number of frames to be exported from a Figma file or project. This is the primary metric for estimating export time and cost.

**Calculation**:
```python
# Single file
frame_count = len(file['document']['children'])

# Entire project
total_frames = sum(f['frame_count'] for f in files)
```

**JL-004 Example**:
- Phase 1 count: 16,389 frames
- Actual export: 24,820 frames (51% undercount)
- Buffered estimate: 24,583 frames (1% variance)

**Related**: [SCOPE-ESTIMATION-GUIDE.md](SCOPE-ESTIMATION-GUIDE.md#the-50-buffer-rule)

---

### Exportable Files
Figma files that contain at least one frame with exportable content. Determined by checking if `frame_count > 0`.

**Filter Pattern**:
```python
exportable_files = [f for f in all_files if f.get('frame_count', 0) > 0]
```

**JL-004 Data**:
- Total files: 182
- Exportable: 99 (54.4%)
- Empty: 83 (45.6%)

**Why This Matters**: Prevents wasted time attempting to export empty files.

**Related**: [SCOPE-ESTIMATION-GUIDE.md](SCOPE-ESTIMATION-GUIDE.md#empty-file-filter)

---

### Empty Files
Figma files with zero exportable frames (`frame_count = 0`). Common in projects with placeholder files, archived designs, or unsupported file types (FigJam, Slides).

**Identification**:
```python
empty_files = [f for f in all_files if f.get('frame_count', 0) == 0]
```

**Common Reasons**:
- Placeholder files (created but not used)
- FigJam files (whiteboarding, not design)
- Archived/deprecated files
- Failed API responses during Phase 1

**JL-004 Discovery**: 45.6% of files were empty (83/182)

**Related**: [SCOPE-ESTIMATION-GUIDE.md](SCOPE-ESTIMATION-GUIDE.md#empty-file-filter)

---

## Performance Terms

### Quicksilver
Oracle's codename for the high-performance Figma export script that uses direct Figma API with optimal configuration (8 workers, batch 15, 1.2s rate limiting).

**Origin**: Named after The Flash's speedster abilities (Justice League theme)

**Performance**: 2.5-3x faster than sequential export, 0.50 fps theoretical maximum

**Configuration**:
```python
{
    'max_workers': 8,
    'batch_size': 15,
    'rate_limit_delay': 1.2,
    'api_timeout': 60,
    'cdn_timeout': 120
}
```

**Related**: [PERFORMANCE-EXPECTATIONS.md](PERFORMANCE-EXPECTATIONS.md#quicksilver-configuration)

---

### fps (frames per second)
The rate at which frames are exported. Used to calculate export time.

**Formula**:
```
time_seconds = frame_count / fps
time_hours = time_seconds / 3600
```

**Theoretical Maximum**: 0.50 fps (given Figma API rate limits)

**Real-World**: 0.40-0.50 fps (depending on network, file size)

**Example**:
```
24,820 frames ÷ 0.50 fps = 49,640 seconds = 13.8 hours
```

**Related**: [PERFORMANCE-EXPECTATIONS.md](PERFORMANCE-EXPECTATIONS.md#the-math)

---

### Rate Limit
Restrictions imposed by Figma API to prevent abuse and ensure fair usage. Enforced through mandatory delays between requests.

**Figma API Limits**:
- **Per-request delay**: 1.2 seconds minimum
- **Concurrent requests**: 8-10 maximum (more causes throttling)
- **CDN timeout**: 120 seconds per image
- **Daily quota**: Exists but rarely hit (thousands of requests)

**Why It Matters**: Cannot be bypassed - determines minimum export time

**Violation Consequences**:
- 429 errors (Too Many Requests)
- Temporary API blocks
- Degraded performance

**Related**: [PERFORMANCE-EXPECTATIONS.md](PERFORMANCE-EXPECTATIONS.md#api-constraints)

---

### CDN (Content Delivery Network)
Figma's distributed network of servers that store and deliver exported images. Export requests return CDN URLs where images can be downloaded.

**Flow**:
```
1. API Request: "Export this frame"
2. API Response: CDN URL (https://s3-alpha-sig.figma.com/...)
3. Download: Fetch image from CDN (120s timeout)
```

**Bottleneck**: Large exports (9+ GB) are network I/O bound, not CPU bound

**Related**: [PERFORMANCE-EXPECTATIONS.md](PERFORMANCE-EXPECTATIONS.md#network-io)

---

### Worker
An independent process that exports frames in parallel. Multiple workers can run simultaneously if using different Figma API tokens.

**Sequential** (1 worker):
```
Worker 1: Files 1-99 → 13.8 hours
```

**Parallel** (6 workers):
```
Worker 1: Files 1-17   → 2.3 hours
Worker 2: Files 18-34  → 2.3 hours
Worker 3: Files 35-51  → 2.3 hours
Worker 4: Files 52-67  → 2.3 hours
Worker 5: Files 68-83  → 2.3 hours
Worker 6: Files 84-99  → 2.3 hours
```

**Speedup**: Linear with number of workers (6 workers = 6x faster)

**Related**: [PARALLEL-EXECUTION-GUIDE.md](PARALLEL-EXECUTION-GUIDE.md#overview)

---

## Cost Terms

### Direct Figma API
The FREE Figma REST API used to export frames without per-frame charges. Requires Figma Pro account and Personal Access Token.

**Cost Structure**:
```
Oracle Coordination: $1.00 (Claude API)
Figma API:          $0.00 (FREE)
PDF Conversion:     $0.00 (FREE local tools)
───────────────────────────────
TOTAL:              $1.00
```

**Trade-off**: Slower (13-14h) but 99% cost savings vs paid services

**Related**: [COST-OPTIMIZATION-GUIDE.md](COST-OPTIMIZATION-GUIDE.md#the-1-strategy)

---

### Paid Service
Third-party managed export services that charge per-frame fees. Faster (3-4h) but significantly more expensive.

**Pricing (2025)**:
```
PNG Export: $0.0025 per frame
PDF Export: $0.0030 per frame
Combined:   $0.0055 per frame
```

**Example (24,820 frames)**:
```
PNG: 24,820 × $0.0025 = $62.05
PDF: 24,820 × $0.0030 = $74.46
───────────────────────────────
TOTAL: $136.51
```

**Trade-off**: Faster (3-4h) but 99% more expensive vs direct API

**Related**: [COST-OPTIMIZATION-GUIDE.md](COST-OPTIMIZATION-GUIDE.md#the-95-100-alternative)

---

### Oracle Coordination
The cost of using Claude API (via Oracle) to coordinate, monitor, and validate Figma exports. Typically $1-2 per mission.

**Activities**:
- Script configuration
- Progress monitoring
- Error handling
- QA validation
- Documentation generation

**Token Usage**: ~100K tokens = $0.50-1.00

**Related**: [COST-OPTIMIZATION-GUIDE.md](COST-OPTIMIZATION-GUIDE.md#the-1-strategy)

---

## Estimation Terms

### Phase 1 Discovery
The required first step of any Figma export project. Individual file-by-file analysis to determine:
- Total file count
- Exportable files (frame_count > 0)
- Per-file frame counts
- Total frame count (raw)

**Duration**: 2-3 hours (for 100-200 files with 1.2s rate limiting)

**Output**: JSON file with complete project structure

**Why Required**: Cannot estimate cost/time without knowing frame counts

**Related**: [SCOPE-ESTIMATION-GUIDE.md](SCOPE-ESTIMATION-GUIDE.md#pre-mission-checklist)

---

### 50% Buffer Rule
The practice of multiplying raw frame counts by 1.5x to account for Phase 1 API undercounting.

**Formula**:
```python
buffered_frames = raw_frame_count * 1.5
```

**Origin**: JL-004 discovered 51% undercount (16,389 → 24,820)

**Application**:
```
Phase 1: 16,389 frames
Buffered: 16,389 × 1.5 = 24,583 frames
Actual: 24,820 frames
Variance: 1% (vs 51% without buffer) ✅
```

**Why It Works**: Accounts for nested sections, components, variants that Phase 1 misses

**Related**: [SCOPE-ESTIMATION-GUIDE.md](SCOPE-ESTIMATION-GUIDE.md#the-50-buffer-rule)

---

### Scope Creep
The phenomenon where actual work exceeds initial estimates. In Figma exports, this manifests as higher-than-expected frame counts.

**Common Causes**:
1. Phase 1 API undercounting (30-51%)
2. Nested sections not visible in initial scan
3. Component variants not included
4. Deep hierarchy (page → section → subsection → frame)

**Prevention**: Apply 50% buffer to all estimates

**JL-004 Example**:
```
Estimated: 16,389 frames (no buffer)
Actual:    24,820 frames
Scope creep: +51% ❌

With buffer: 24,583 frames
Actual:      24,820 frames
Scope creep: +1% ✅
```

**Related**: [SCOPE-ESTIMATION-GUIDE.md](SCOPE-ESTIMATION-GUIDE.md#the-50-buffer-rule)

---

### Complexity Multiplier
An adjustment factor (typically 1.0-1.3x) applied to time estimates when projects have many large files (>1000 frames each).

**Usage**:
```python
ideal_time = buffered_frames / 0.50 / 3600  # hours
large_files = [f for f in files if f['frame_count'] > 1000]

if len(large_files) > 10:
    complexity_multiplier = 1.3
else:
    complexity_multiplier = 1.0

estimated_time = ideal_time * complexity_multiplier
```

**Reasoning**: Large files have overhead (parsing, network, memory) beyond simple frame count

**Related**: [SCOPE-ESTIMATION-GUIDE.md](SCOPE-ESTIMATION-GUIDE.md#estimate-template)

---

## Technical Terms

### API Token
A Personal Access Token generated from Figma account settings. Used to authenticate API requests.

**Format**: Starts with `figd_` followed by alphanumeric characters

**Example**: `figd_aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890abcdef`

**Generation**:
1. Login to Figma
2. Settings → Personal Access Tokens
3. Generate new token
4. Copy immediately (shown only once)

**Security**: Never commit to git, store in environment variables only

**Related**: [PARALLEL-EXECUTION-GUIDE.md](PARALLEL-EXECUTION-GUIDE.md#quick-start)

---

### Batch Size
The number of frames processed in a single API request batch. Larger batches = fewer requests but higher timeout risk.

**Optimal**: 15 frames per batch (proven in JL-004)

**Trade-offs**:
- Too small (5): More requests, slower overall
- Too large (30): Timeout errors, failures
- Just right (15): Balance of speed and reliability

**Configuration**:
```python
BATCH_SIZE = 15  # Optimal for most projects
```

**Related**: [PERFORMANCE-EXPECTATIONS.md](PERFORMANCE-EXPECTATIONS.md#quicksilver-configuration)

---

### max_workers
The number of concurrent workers (threads) used by Quicksilver for parallel requests within a single API token.

**Optimal**: 8 workers (proven in JL-004)

**Trade-offs**:
- Too few (2-4): Underutilizes API capacity
- Too many (16+): Triggers rate limiting, 429 errors
- Just right (8): Maximum speed without throttling

**Configuration**:
```python
MAX_WORKERS = 8  # Optimal for Figma API
```

**Note**: Different from "Worker" (multi-account parallel) - this is within a single account

**Related**: [PERFORMANCE-EXPECTATIONS.md](PERFORMANCE-EXPECTATIONS.md#quicksilver-configuration)

---

### Sequential Export
The baseline export approach using a single Figma API token and processing files one at a time.

**Performance**: 0.40-0.50 fps, 13-14 hours for 24,820 frames

**Cost**: $1 (Oracle only)

**Pros**: Simple, proven, works with 1 account

**Cons**: Slowest option (14h for large exports)

**Related**: [PARALLEL-EXECUTION-GUIDE.md](PARALLEL-EXECUTION-GUIDE.md#overview)

---

### Parallel Execution
The advanced export approach using multiple Figma API tokens to process files simultaneously, achieving 6x-18x speedup.

**Performance**: 6x (basic) to 18x (optimized) faster than sequential

**Requirements**:
- 2-6 Figma Pro accounts
- 8+ CPU cores
- 16GB+ RAM
- 50GB+ disk space

**Cost**: FREE (local) or $5 (cloud optimized)

**Related**: [PARALLEL-EXECUTION-GUIDE.md](PARALLEL-EXECUTION-GUIDE.md)

---

## Format Terms

### PNG (Portable Network Graphics)
Raster image format with lossless compression and transparency support. Default export format for Figma frames.

**Scale**: 2x recommended (high resolution for reference)

**Typical Size**: 50-500 KB per frame (varies by complexity)

**Use Cases**:
- Web documentation
- Design handoff
- Visual reference
- Component library

**JL-004 Stats**: 24,820 PNGs, 9.7 GB total

**Related**: [README.md](README.md#what-this-guide-covers)

---

### PDF (Portable Document Format)
Multi-page document format compiled from PNG exports. Each Figma file becomes one PDF containing all its frames.

**Compilation**: Local PNG → PDF conversion (no Figma API re-export)

**Typical Size**: 2-50 MB per file (varies by frame count)

**Use Cases**:
- Print documentation
- Client presentations
- Offline reference
- Long-term archival

**JL-004 Stats**: 99 PDFs, 11.2 GB total, 29 seconds to compile

**Related**: [README.md](README.md#what-this-guide-covers)

---

### Scale Factor
The resolution multiplier applied to exports. Higher scale = higher resolution but larger file sizes.

**Options**:
- **1x**: Base resolution (smallest files)
- **2x**: Recommended (high resolution, reasonable size)
- **3x**: Maximum quality (largest files)

**Example** (500×500 frame):
```
1x: 500×500 pixels (50 KB)
2x: 1000×1000 pixels (150 KB)
3x: 1500×1500 pixels (300 KB)
```

**Recommendation**: 2x for reference implementation, 3x for detailed assets only

**Related**: [PERFORMANCE-EXPECTATIONS.md](PERFORMANCE-EXPECTATIONS.md#export-quality)

---

## Workflow Terms

### Mission
A complete Figma export project with defined scope, budget, timeline, and deliverables. Uses Justice League mission tracking system.

**Structure**:
```
missions/JL-XXX-mission-name/
├── mission-brief.md     # Scope, objective, budget
├── mission-log.md       # Progress tracking
├── JL-XXX-ESTIMATE.md   # Pre-work cost estimate
├── JL-XXX-INVOICE.md    # Post-work actual costs
└── deliverables/        # Export outputs
```

**Example**: JL-004 Auzmor Figma Export (182 files, 24,820 frames, $1 cost)

**Related**: Justice League Missions CLAUDE.md

---

### Estimate
A pre-work document that projects costs, time, and deliverables for a Figma export mission.

**Template Structure**:
- Phase 1 discovery results
- Buffered frame count (×1.5)
- Time calculation (frames ÷ 0.50 fps)
- Cost comparison (Direct API vs Paid Service)
- Budget impact analysis

**Purpose**: Get user approval before starting work

**Related**: [SCOPE-ESTIMATION-GUIDE.md](SCOPE-ESTIMATION-GUIDE.md#estimate-template)

---

### Invoice
A post-work document that reports actual costs, deliverables, and variance from estimate.

**Template Structure**:
- Cost summary (estimated vs actual)
- Deliverables list
- Success metrics
- Time breakdown
- Budget impact

**Purpose**: Record actual costs for budget tracking

**Related**: JL-004-INVOICE.md (in mission folder)

---

## Metrics Terms

### Success Rate
The percentage of frames successfully exported without errors.

**Formula**:
```
success_rate = (successful_frames / total_frames) × 100
```

**JL-004 Stats**:
```
Attempted: 25,313 frames
Successful: 24,820 frames
Success rate: 98.05% ✅
```

**Target**: ≥95% (acceptable), ≥98% (excellent)

**Related**: [PERFORMANCE-EXPECTATIONS.md](PERFORMANCE-EXPECTATIONS.md#success-metrics)

---

### Speedup
The performance improvement ratio compared to baseline (sequential export).

**Formula**:
```
speedup = baseline_time / optimized_time
```

**Examples**:
```
Parallel (6 workers): 13.8h ÷ 2.3h = 6x speedup
Parallel Optimized: 13.8h ÷ 0.75h = 18x speedup
```

**Related**: [PARALLEL-EXECUTION-GUIDE.md](PARALLEL-EXECUTION-GUIDE.md#performance-comparison)

---

### ROI (Return on Investment)
The financial benefit gained from cost optimizations or parallel execution setup.

**Formula**:
```
roi = (savings / cost) × 100
```

**Example (JL-004)**:
```
Direct API: $1
Paid Service: $136.51
Savings: $135.51
ROI: ($135.51 / $1) × 100 = 13,551% ✅
```

**Related**: [COST-OPTIMIZATION-GUIDE.md](COST-OPTIMIZATION-GUIDE.md#roi-calculator)

---

## Common Abbreviations

**API**: Application Programming Interface
**CDN**: Content Delivery Network
**PNG**: Portable Network Graphics
**PDF**: Portable Document Format
**fps**: Frames per second
**GB**: Gigabytes (storage)
**MB**: Megabytes (storage)
**KB**: Kilobytes (storage)
**RAM**: Random Access Memory
**CPU**: Central Processing Unit
**SSD**: Solid State Drive
**ROI**: Return on Investment

---

## Cross-References

**For performance details**: See [PERFORMANCE-EXPECTATIONS.md](PERFORMANCE-EXPECTATIONS.md)

**For cost strategies**: See [COST-OPTIMIZATION-GUIDE.md](COST-OPTIMIZATION-GUIDE.md)

**For scope estimation**: See [SCOPE-ESTIMATION-GUIDE.md](SCOPE-ESTIMATION-GUIDE.md)

**For parallel execution**: See [PARALLEL-EXECUTION-GUIDE.md](PARALLEL-EXECUTION-GUIDE.md)

**For decision guidance**: See [DECISION-TREE.md](DECISION-TREE.md)

**For getting started**: See [README.md](README.md)

---

**Version**: 1.0.0
**Terms**: 50+ key concepts defined
**Last Updated**: 2025-11-05
**Author**: Oracle (Justice League Coordinator)

---

**Note**: This glossary will be updated as new terms emerge from future missions. Suggest additions via pull requests.
