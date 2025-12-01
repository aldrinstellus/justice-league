# Claude Max Plan - Context Window Clarification

**Date**: 2025-11-24
**Plan**: Claude Max ($200/month)

---

## CONFIRMED: 200K Context Window (NOT 1M)

### Your Claude Max Plan
- **Cost**: $200/month
- **Context Window**: 200,000 tokens (same as Pro/Team plans)
- **Benefit**: 20x more usage (messages per month), NOT bigger context
- **Priority**: Access during high-traffic periods

### 1M Context Window Availability
**NOT available for Claude Max personal plans.**

Available only for:
- Organizations in usage tier 4
- Organizations with custom rate limits
- Via Claude API, Amazon Bedrock, Google Cloud Vertex AI
- Enterprise agreements only

---

## Your Context Budget with Skills (200K Window)

### Current Usage:
- Global CLAUDE.md: 40,000 tokens (20%)
- Skills metadata (50 skills): 5,000 tokens (2.5%)
- Active skills (2-3 per request): 3,000-5,000 tokens (1.5-2.5%)
- **Total overhead**: 48,000-50,000 tokens (24-25%)
- **Remaining for conversation**: 150,000-152,000 tokens (75-76%)

### Conclusion
✅ Installing 50+ skills is **safe and efficient**
✅ Skills use only 2.5-5% of context window
✅ 75-76% remains available for actual work
✅ Can comfortably install Superpowers + Documents + ClaudeKit

---

## Recommended Installation (Updated for 200K)

### Option B: Moderate (Recommended)
```bash
# Superpowers (20+ skills, critical for coordination)
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace

# Document Skills (4 skills, RFP/client docs)
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

**Total**: 24+ skills, ~15-30MB, ~2,400 tokens metadata (1.2%)

**Why not ClaudeKit immediately?**
- Test Superpowers for 1 week first
- ClaudeKit has 30+ skills with potential overlap
- Add later if needed

### After 1 Week Testing
If Superpowers works well, add:
```bash
# ClaudeKit (30+ skills, comprehensive)
git clone https://github.com/mrgoonie/claudekit-skills ~/.claude/skills/claudekit
```

---

## Sources

- [How large is the context window on paid Claude plans?](https://support.claude.com/en/articles/8606394-how-large-is-the-context-window-on-paid-claude-plans)
- [About Claude's Max Plan Usage](https://support.claude.com/en/articles/11014257-about-claude-s-max-plan-usage)
- [Is Claude AI Getting Expensive? New 2025 Max Plan Explained](https://hostbor.com/claude-ai-max-plan-explained/)
- [A practical guide to the Claude code context window size](https://www.eesel.ai/blog/claude-code-context-window-size)
- [Claude Max plan limits](https://gist.github.com/eonist/5ac2fd483cf91a6e6e5ef33cfbd1ee5e)
- [Claude pricing and plan limits explained](https://www.datastudios.org/post/claude-pricing-and-plan-limits-explained-full-guide-to-free-pro-team-and-max-tiers)
- [Context windows - Claude Docs](https://platform.claude.com/docs/en/build-with-claude/context-windows)

---

**Key Takeaway**: Your $200/month Max plan = more messages, NOT bigger context. 200K limit applies, so original skills analysis was correct.
