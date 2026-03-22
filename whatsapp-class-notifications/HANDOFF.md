# WhatsApp Class Notifications — Mac Handoff

## Quick Start

```bash
# Clone/pull the repo (code is merged to main)
git clone https://github.com/aldrinstellus/justice-league.git
cd justice-league/whatsapp-class-notifications
```

## Status

- [x] Code complete — 8 `.gs` files, ~1,150 LOC, fully reviewed
- [x] PR merged to `main` (PR #1)
- [ ] Google Apps Script project created
- [ ] WhatsApp Business API configured
- [ ] Config tab filled with credentials
- [ ] Triggers installed
- [ ] End-to-end test passed

## What Needs to Be Done

### Step 1: Install `clasp` (Google Apps Script CLI)

```bash
npm install -g @google/clasp
clasp login  # Opens browser — sign in with Google account
```

### Step 2: Create Google Sheet + Apps Script Project

```bash
# Enable Apps Script API first:
# Go to https://script.google.com/home/usersettings → toggle ON "Google Apps Script API"

# Create a new Apps Script project (bound to a sheet)
cd whatsapp-class-notifications
clasp create --type sheets --title "Class Notifications"
```

This creates:
- A new Google Sheet named "Class Notifications"
- An Apps Script project bound to it
- A `.clasp.json` file locally with the project ID

### Step 3: Push All Code

```bash
# Create .claspignore to skip non-script files
echo -e "HANDOFF.md\nPROMPT.md\nREADME.md\nSETUP.md\nTESTING.md\n.clasp.json\n.claspignore" > .claspignore

# Push all .gs files to Apps Script
clasp push
```

Verify: `clasp open` opens the Apps Script editor in browser — you should see all 8 files.

### Step 4: Run Sheet Setup

```bash
clasp run createSheetStructure
```

If `clasp run` doesn't work (requires extra GCP setup), open the script editor manually:
```bash
clasp open
```
Then in the editor: select `createSheetStructure` from dropdown → click Run → grant permissions.

After running, the Google Sheet should have 5 tabs: Students, Schedule, Config, Log, Overrides.

### Step 5: WhatsApp Business API Setup

1. Go to https://developers.facebook.com → My Apps → Create App
2. Select "Other" → "Business" → name it "Class Notifications"
3. Add WhatsApp product → Set Up
4. On Getting Started page, copy:
   - **Temporary access token** → this is `WHATSAPP_TOKEN`
   - **Phone number ID** (under "From" dropdown) → this is `PHONE_NUMBER_ID`
5. Add your WhatsApp number to sandbox: click "Add phone number" → verify with code
6. Create message template:
   - Go to WhatsApp → Message Templates → Create Template
   - Category: Utility
   - Name: `class_update`
   - Language: English
   - Body: `{{1}}`
   - Submit (approves in ~1 minute)

### Step 6: Fill Config Tab

Open the Google Sheet → Config tab → fill Value column:

| Key | Value |
|-----|-------|
| `WHATSAPP_TOKEN` | Bearer token from Step 5 |
| `PHONE_NUMBER_ID` | Phone number ID from Step 5 |
| `TEMPLATE_NAME` | `class_update` |
| `CLAUDE_API_KEY` | Your Anthropic key (optional) |
| `USE_CLAUDE` | `FALSE` (start without AI) |
| `DAILY_SEND_HOUR` | `8` |
| `DAILY_SEND_MINUTE` | `0` |
| `TIMEZONE` | `Asia/Kolkata` |
| `SCHOOL_NAME` | Your school name |
| `WEBHOOK_SECRET` | Any random string e.g. `mySecret2026xyz` |

### Step 7: Add Test Data

**Students tab** (row 2):

| StudentID | Name | Phone | Class | Active |
|-----------|------|-------|-------|--------|
| S001 | Test User | 9876543210 | Grade 10A | TRUE |

**Schedule tab** (row 2):

| ScheduleID | Class | Subject | Teacher | Room | Date | Time | Status | LastModified | ModifiedBy |
|------------|-------|---------|---------|------|------|------|--------|--------------|------------|
| SCH001 | Grade 10A | Mathematics | Mrs. Sharma | Room 201 | (tomorrow YYYY-MM-DD) | 9:00 AM | Active | | |

### Step 8: Validate

In Apps Script editor (or via `clasp run`):
- Run `testSetup` → should report all config valid, all tabs exist

### Step 9: Deploy

1. In Apps Script editor: Deploy → New deployment → Web app → Execute as: Me, Access: Anyone → Deploy
2. Run `installTriggers` → installs daily + onEdit triggers

### Step 10: End-to-End Test

1. In Google Sheet → Schedule tab → change Teacher from "Mrs. Sharma" to "Mr. Gupta"
2. Wait 5-10 seconds
3. Check phone for WhatsApp message
4. Check Log tab for delivery record

## Architecture

| File | LOC | Purpose |
|------|-----|---------|
| `setup.gs` | 171 | Sheet structure, triggers, validation |
| `config.gs` | 101 | Config read/cache (CacheService, 10min TTL) |
| `utils.gs` | 304 | Phone formatting, student lookups, date helpers, logging |
| `composer.gs` | 203 | Claude API + fallback message templates (8 change types) |
| `sender.gs` | 194 | WhatsApp Cloud API v19.0, template + free-form, batch send |
| `watcher.gs` | 115 | onEdit handler — detects schedule changes, notifies students |
| `scheduler.gs` | 220 | Daily schedule sender, grouped by class |
| `webapp.gs` | 246 | POST/GET web endpoints (override, daily, test, health check) |

## Key Technical Details

- **WhatsApp API**: Meta Cloud API v19.0, template-based (no 24hr window needed)
- **Claude API**: `claude-sonnet-4-20250514`, `anthropic-version: 2023-06-01`
- **Phone formatting**: Handles E.164, `91XXXXXXXXXX`, 10-digit, `0`-prefixed Indian numbers
- **Rate limiting**: 200ms between WhatsApp sends
- **Config caching**: CacheService with 10min TTL
- **Monitoring**: Log tab + email summaries on failures

## GitHub

- Repo: `https://github.com/aldrinstellus/justice-league`
- Code location: `whatsapp-class-notifications/`
- Branch: `main` (merged from `claude/whatsapp-class-notifications-vaKW3`)
- PR: #1 (merged)
