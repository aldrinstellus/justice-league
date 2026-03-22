# WhatsApp Class Notifications — Master Setup Prompt for Claude Code

## What This Is

This folder contains a complete Google Apps Script project for event-driven WhatsApp class notifications. Use the prompt below to have Claude Code guide you through setup, or follow SETUP.md manually.

---

## Master Prompt

Copy and paste this into Claude Code:

```
I have a complete Google Apps Script project in the `whatsapp-class-notifications/` folder. It's an event-driven WhatsApp notification system for class scheduling. Help me deploy it.

Here's what the project contains:
- 8 `.gs` files (setup, config, utils, composer, sender, watcher, scheduler, webapp)
- It uses Google Sheets as the database, WhatsApp Cloud API for delivery, and optionally Claude API for message personalization

I need you to:

1. Read all 8 `.gs` files so you understand the full codebase
2. Walk me through setting up a new Google Apps Script project at script.google.com
3. Help me create a WhatsApp Business App on Meta's developer platform and get:
   - WHATSAPP_TOKEN (bearer token)
   - PHONE_NUMBER_ID (test phone number ID)
   - A message template named "class_update" with body {{1}}
4. Help me fill the Config tab with real values
5. Help me add test student data and schedule data
6. Help me run testComposer() to verify messages work
7. Help me run testSetup() to validate the full config
8. Help me deploy as a web app and test the POST endpoint with curl
9. Help me run installTriggers() to activate daily + onEdit triggers
10. Help me test end-to-end: edit a Schedule row and verify WhatsApp delivery

Read SETUP.md and TESTING.md in the same folder for the detailed guides.
```

---

## Files in This Project

| File | Purpose |
|------|---------|
| `PROMPT.md` | This file — master prompt and overview |
| `SETUP.md` | Step-by-step deployment guide |
| `TESTING.md` | All test functions and verification steps |
| `README.md` | Technical architecture reference |
| `setup.gs` | Sheet structure creation and trigger management |
| `config.gs` | CacheService-backed configuration reader |
| `utils.gs` | Student lookups, phone formatting, logging |
| `composer.gs` | Claude API message composition + template fallback |
| `sender.gs` | WhatsApp Cloud API sending (template + free-form) |
| `watcher.gs` | Real-time Schedule tab edit detection |
| `scheduler.gs` | Daily time-triggered schedule notifications |
| `webapp.gs` | Web app POST/GET endpoints for manual triggers |
