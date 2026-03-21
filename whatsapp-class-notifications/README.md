# WhatsApp Class Notifications — Google Apps Script

Event-driven WhatsApp notification system for class scheduling. Runs entirely on Google Apps Script with zero infrastructure cost.

## Architecture

```
Google Sheet (source of truth)
  ├── Students tab      → Contact directory
  ├── Schedule tab      → Class timetable
  ├── Config tab        → API keys & settings
  ├── Log tab           → Delivery audit trail
  └── Overrides tab     → Manual message log

Triggers:
  ├── Time-driven       → Daily schedule at configured hour (scheduler.gs)
  ├── onEdit            → Real-time change detection (watcher.gs)
  └── Web app POST      → Manual/emergency sends (webapp.gs)

Message Pipeline:
  Sheet data → composer.gs (Claude API or templates) → sender.gs (WhatsApp Cloud API)
```

## Setup

1. **Create a new Google Apps Script project** at [script.google.com](https://script.google.com)
2. **Copy each `.gs` file** into the script editor (File → New → Script file)
3. **Run `createSheetStructure()`** to build all sheet tabs
4. **Fill in the Config tab** with your API keys:
   - `WHATSAPP_TOKEN` — Meta Cloud API bearer token
   - `PHONE_NUMBER_ID` — WhatsApp Business phone number ID
   - `CLAUDE_API_KEY` — Anthropic API key (optional, set `USE_CLAUDE=FALSE` to skip)
   - `SCHOOL_NAME` — Your school name
   - `WEBHOOK_SECRET` — Shared secret for web app POST authentication
5. **Run `installTriggers()`** to set up daily and onEdit triggers
6. **Run `testSetup()`** to validate everything is configured
7. **Deploy as web app** (Deploy → New deployment → Web app) for the POST/GET endpoints

## Files

| File | Purpose |
|------|---------|
| `setup.gs` | Sheet creation, trigger management, validation |
| `config.gs` | Config read/cache/validate from Config tab |
| `utils.gs` | Student lookups, date helpers, phone formatting, logging |
| `composer.gs` | Message composition — Claude API with template fallback |
| `sender.gs` | WhatsApp Cloud API — template and free-form sending |
| `watcher.gs` | Installable onEdit handler for Schedule changes |
| `scheduler.gs` | Daily schedule sender (time-triggered) |
| `webapp.gs` | Web app POST/GET endpoints for manual triggers |

## WhatsApp Template Setup

Create an approved message template in Meta Business Manager:
- **Template name**: `class_update` (or match your `TEMPLATE_NAME` config)
- **Category**: Utility
- **Body**: `{{1}}` (single parameter that receives the full message text)

## Web App API

### POST — Send notifications

```bash
curl -X POST "YOUR_WEB_APP_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "secret": "your-webhook-secret",
    "action": "send_override",
    "target_type": "class",
    "target_value": "Grade 10A",
    "message": "School closed tomorrow due to weather.",
    "sent_by": "Principal"
  }'
```

### GET — Health check

```bash
curl "YOUR_WEB_APP_URL"
# → {"status":"ok","timestamp":"2026-03-21 10:00:00","triggerCount":2}
```

## Cost

- **Infrastructure**: ₹0 (Google Apps Script is free)
- **WhatsApp**: Per Meta's utility template pricing (~₹0.35/message in India)
- **Claude API**: ~$0.01-0.03 per message (optional, disable with `USE_CLAUDE=FALSE`)
