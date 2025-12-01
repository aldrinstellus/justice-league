# Figma Best Practices & Learnings

**Location**: `/Users/admin/Documents/claudecode/best-practices/figma/`
**Status**: Active - Iterating on solutions
**Last Updated**: 2025-11-25

---

## Overview

This folder documents all learnings, problems, and solutions related to Figma workflows including:
- Figma-to-code conversion
- CSS extraction methods
- Automation capabilities and limitations
- API vs Desktop app features

---

## Documents Index

| Document | Purpose |
|----------|---------|
| [FIGMA-TO-CODE-CONVERSION.md](./FIGMA-TO-CODE-CONVERSION.md) | Main problem statement and solution approaches |
| [CSS-EXTRACTION-METHODS.md](./CSS-EXTRACTION-METHODS.md) | Comparison of all CSS extraction methods |
| [AUTOMATION-LIMITATIONS.md](./AUTOMATION-LIMITATIONS.md) | What can/cannot be automated |
| [OPEN-PROBLEMS.md](./OPEN-PROBLEMS.md) | Unsolved problems for future iteration |

---

## Quick Reference

### The Core Problem

**Goal**: Convert Figma designs to React code with 99%+ accuracy at scale (100+ files)

**Current Gap**:
- Manual CSS copy achieves 99% accuracy but doesn't scale
- API automation achieves 90-95% accuracy and scales
- No solution exists for 99% accuracy + full automation

### Current Best Approaches

| Use Case | Method | Accuracy | Scalability |
|----------|--------|----------|-------------|
| Single component demo | Manual CSS paste | 99%+ | Manual |
| Bulk export (100+ files) | Figma REST API | 90-95% | Automated |
| Production pipeline | API + Manual QA | 95-99% | Semi-automated |

### Key Insight

> "Figma's 'Copy as code → CSS (all layers)' is a **client-side UI feature** with no API equivalent. This is the fundamental automation gap."

---

## Related Resources

- **Figma MCP Guide**: `/Users/admin/Documents/claudecode/justice-league-missions/FIGMA_MCP_GUIDE.md`
- **JL-004 Export Learnings**: `/Users/admin/Documents/claudecode/justice-league-missions/missions/JL-004-auzmor-figma-export/`
- **Quicksilver FAQ**: `/Users/admin/Documents/claudecode/justice-league-missions/knowledge_base/QUICKSILVER-PERFORMANCE-FAQ.md`

---

## Iteration History

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | 2025-11-25 | Initial documentation of problems and current solutions |

---

**Note**: This is an active area of research. Solutions documented here represent current best knowledge but are expected to evolve.
