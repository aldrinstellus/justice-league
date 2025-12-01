---
description: View live token usage monitor (toggle on/off)
---

Start the token monitor and tell the user how to view it. Ensure the monitor is running in the background, then provide the simple attach command.

**Action:** Silently ensure monitor is running, then tell user to run this ONE command in their terminal:

```bash
tmux attach -t claude-monitor
```

**Shortcuts while viewing:**
- `Ctrl+B` then `D` - Hide monitor (keeps running)
- `Ctrl+C` - Stop monitor completely

Next time they type `/monitor`, just remind them of the attach command above.
