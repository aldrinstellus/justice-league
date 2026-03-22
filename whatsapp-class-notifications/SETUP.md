# Setup Guide — WhatsApp Class Notifications

Complete step-by-step guide to deploy this Google Apps Script project.

---

## Prerequisites

- Google account (free)
- Meta Developer account (free) — [developers.facebook.com](https://developers.facebook.com)
- Anthropic API key (optional, for Claude-powered messages) — [console.anthropic.com](https://console.anthropic.com)
- A phone number with WhatsApp installed (to receive test messages)

---

## Step 1: Create the Google Apps Script Project

1. Open [script.google.com](https://script.google.com)
2. Click **New Project**
3. Rename the project to `WhatsApp Class Notifications`
4. You'll see a default `Code.gs` file — delete its contents

### Create the script files

For each `.gs` file in this folder, create a matching script file in the editor:

| File to create | How |
|----------------|-----|
| `setup.gs` | Click `+` next to Files → Script → name it `setup` |
| `config.gs` | Click `+` next to Files → Script → name it `config` |
| `utils.gs` | Click `+` next to Files → Script → name it `utils` |
| `composer.gs` | Click `+` next to Files → Script → name it `composer` |
| `sender.gs` | Click `+` next to Files → Script → name it `sender` |
| `watcher.gs` | Click `+` next to Files → Script → name it `watcher` |
| `scheduler.gs` | Click `+` next to Files → Script → name it `scheduler` |
| `webapp.gs` | Click `+` next to Files → Script → name it `webapp` |

Copy-paste the contents of each local `.gs` file into the matching script file.

You can delete the default `Code.gs` file after copying everything.

---

## Step 2: Build the Sheet Structure

1. In the Apps Script editor, select `setup.gs` from the file list
2. Select `createSheetStructure` from the function dropdown (top toolbar)
3. Click **Run**
4. When prompted, click **Review permissions** → choose your Google account → **Allow**
5. Check the **Execution log** — should say "Sheet structure created successfully"
6. Open the linked Google Sheet (it was created automatically) — you should see 5 tabs:
   - Students, Schedule, Log, Overrides, Config

---

## Step 3: Set Up WhatsApp Business API

### 3a: Create a Meta Developer App

1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Click **My Apps** → **Create App**
3. Select **Other** → **Business** → fill in app name
4. On the app dashboard, find **WhatsApp** → click **Set Up**
5. You'll get a **temporary access token** and **Phone Number ID** — copy both

### 3b: Create a Message Template

1. In the Meta Business Manager, go to **WhatsApp Manager** → **Message Templates**
2. Click **Create Template**
3. Configure:
   - **Category**: Utility
   - **Template name**: `class_update`
   - **Language**: English
   - **Body**: `{{1}}`
4. Submit for review (test phone numbers approve templates instantly)

### 3c: Add Your Test Phone as a Recipient

1. In the WhatsApp setup page, under **API Setup**
2. Find **To** field → click **Manage phone number list**
3. Add your personal WhatsApp number (the number that will RECEIVE messages)
4. Verify with the OTP sent to your WhatsApp

---

## Step 4: Fill the Config Tab

Open the Google Sheet → **Config** tab. Update these values:

| Key | Value | Where to get it |
|-----|-------|-----------------|
| `WHATSAPP_TOKEN` | `EAAxxxxxxx...` | Meta App Dashboard → WhatsApp → API Setup → Temporary access token |
| `PHONE_NUMBER_ID` | `1234567890` | Meta App Dashboard → WhatsApp → API Setup → Phone Number ID |
| `TEMPLATE_NAME` | `class_update` | The template you created in Step 3b |
| `CLAUDE_API_KEY` | `sk-ant-xxxxx` | console.anthropic.com → API Keys (or set USE_CLAUDE to FALSE to skip) |
| `USE_CLAUDE` | `TRUE` or `FALSE` | Set FALSE to use hardcoded templates instead of Claude AI |
| `DAILY_SEND_HOUR` | `8` | Hour in 24hr format (IST) for daily schedule sends |
| `DAILY_SEND_MINUTE` | `0` | Minute for daily sends |
| `TIMEZONE` | `Asia/Kolkata` | Leave as-is for IST |
| `SCHOOL_NAME` | `Your School Name` | Used in message composition |
| `WEBHOOK_SECRET` | `any-strong-secret-string` | You choose this — used to auth web app POST requests |

---

## Step 5: Add Test Data

### Students tab

Add rows below the header:

```
StudentID | Name           | Phone          | Class      | Active
S001      | Priya Sharma   | +919876543210  | Grade 10A  | TRUE
S002      | Rahul Verma    | +919876543211  | Grade 10A  | TRUE
S003      | Ananya Patel   | +919876543212  | Grade 10B  | TRUE
```

**Important**: Replace at least one phone number with YOUR real WhatsApp number to receive test messages.

### Schedule tab

Add rows with today's date (or tomorrow's):

```
ScheduleID | Class     | Subject  | Teacher     | Room   | Date       | Time  | Status | LastModified | ModifiedBy
SCH001     | Grade 10A | Physics  | Mr. Sharma  | Lab 2  | 2026-03-23 | 10:00 | Active |              |
SCH002     | Grade 10A | Maths    | Mrs. Gupta  | Room 5 | 2026-03-23 | 11:30 | Active |              |
SCH003     | Grade 10B | English  | Ms. Roy     | Room 3 | 2026-03-23 | 10:00 | Active |              |
```

---

## Step 6: Validate Setup

1. In Apps Script editor, select `setup.gs`
2. Select `testSetup` from the dropdown → click **Run**
3. Check execution log:
   - **All config values are set** = good
   - **Missing or placeholder config keys: [...]** = fill those in

---

## Step 7: Deploy as Web App

1. In Apps Script editor: **Deploy** → **New deployment**
2. Click the gear icon → **Web app**
3. Configure:
   - **Description**: `WhatsApp Notifications v1`
   - **Execute as**: Me
   - **Who has access**: Anyone
4. Click **Deploy**
5. Copy the **Web app URL** — this is your POST/GET endpoint
6. Test the health check:
   ```bash
   curl "YOUR_WEB_APP_URL"
   ```
   Should return: `{"status":"ok","timestamp":"...","triggerCount":0}`

---

## Step 8: Install Triggers

1. In Apps Script editor, select `setup.gs`
2. Select `installTriggers` from the dropdown → click **Run**
3. Verify in execution log: "Triggers installed: daily at 8:0 IST, onEdit for Schedule tab"
4. Confirm at **Triggers** page (clock icon in left sidebar): should see 2 triggers

---

## Step 9: End-to-End Test

### Test A: Manual WhatsApp Send

Run `testWhatsApp` from TESTING.md (see that file for the function).

### Test B: Edit Trigger

1. Go to the Schedule tab
2. Change a teacher name (e.g., "Mr. Sharma" → "Dr. Singh")
3. Check the **Log** tab — a new row should appear with the send result
4. Check your WhatsApp — you should receive the notification

### Test C: Web App Override

```bash
curl -X POST "YOUR_WEB_APP_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "secret": "your-webhook-secret",
    "action": "send_test",
    "phone": "+91YOUR_NUMBER",
    "message": "Test from the web app endpoint!"
  }'
```

### Test D: Daily Schedule

Run `sendDailySchedule()` manually from the editor. Check Log tab and your WhatsApp.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "WhatsApp API not configured" | Fill WHATSAPP_TOKEN and PHONE_NUMBER_ID in Config tab |
| Template not found error | Make sure template name in Config matches exactly, and template is approved |
| 401 Unauthorized from WhatsApp | Token expired — get a new temporary token from Meta dashboard |
| Claude API returns null | Check CLAUDE_API_KEY is valid; set USE_CLAUDE=FALSE to use fallback templates |
| No message received on WhatsApp | Verify your number is in the test recipient list on Meta dashboard |
| onEdit trigger not firing | Must be installable trigger (run installTriggers), not simple onEdit |
| Permissions error | Re-run any function and re-approve permissions when prompted |

---

## Going to Production

When ready to move beyond test mode:

1. **Verify your WhatsApp Business number** (not just the test number)
2. **Get a permanent System User token** instead of the temporary one
3. **Get your message template approved** with real content
4. **Add all student phone numbers** to the Students tab
5. **Set the daily trigger time** to your preferred morning hour
6. **Monitor the Log tab** for delivery failures
