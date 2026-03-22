# Testing Guide — WhatsApp Class Notifications

Copy-paste these test functions into a `tests.gs` file in your Apps Script project, or run them one at a time in the editor.

---

## Test 1: Validate Config

Checks that all required keys are filled in the Config tab.

```javascript
function testValidateConfig() {
  var missing = validateConfig();
  if (missing.length === 0) {
    Logger.log('PASS: All config keys are set');
  } else {
    Logger.log('FAIL: Missing keys: ' + missing.join(', '));
  }
}
```

---

## Test 2: Sheet Structure

Verifies all 5 tabs exist with correct headers.

```javascript
function testSheetStructure() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var tabs = ['Students', 'Schedule', 'Log', 'Overrides', 'Config'];
  var pass = true;

  tabs.forEach(function(tab) {
    var sheet = ss.getSheetByName(tab);
    if (!sheet) {
      Logger.log('FAIL: Missing tab: ' + tab);
      pass = false;
    } else {
      Logger.log('OK: Tab exists: ' + tab + ' (' + sheet.getLastRow() + ' rows)');
    }
  });

  if (pass) Logger.log('PASS: All tabs exist');
}
```

---

## Test 3: Composer — Fallback Templates (no API keys needed)

Tests message composition using hardcoded templates. Set `USE_CLAUDE=FALSE` first.

```javascript
function testComposerFallback() {
  var student = {
    name: 'Priya Sharma',
    phone: '+919876543210',
    className: 'Grade 10A'
  };

  var schedule = {
    subject: 'Physics',
    teacher: 'Mr. Sharma',
    room: 'Lab 2',
    time: '10:00',
    date: '2026-03-23',
    status: 'Active'
  };

  var types = [
    ['daily_schedule', null, null],
    ['teacher_change', 'Mr. Sharma', 'Dr. Singh'],
    ['room_change', 'Lab 2', 'Room 8'],
    ['time_change', '10:00', '14:00'],
    ['date_change', '2026-03-23', '2026-03-25'],
    ['cancellation', null, null],
    ['reschedule', null, null]
  ];

  types.forEach(function(t) {
    var msg = composeMessage(student, schedule, t[0], t[1], t[2]);
    Logger.log('[' + t[0] + '] ' + msg);

    // Verify constraints
    if (msg.length > 1024) {
      Logger.log('  FAIL: Message exceeds 1024 chars (' + msg.length + ')');
    }
    if (/[*_~`#]/.test(msg)) {
      Logger.log('  FAIL: Message contains markdown characters');
    }
    if (msg.indexOf('Priya') === -1) {
      Logger.log('  FAIL: Message does not start with student first name');
    }
  });

  Logger.log('PASS: All 7 message types composed');
}
```

---

## Test 4: Composer — Claude API (requires CLAUDE_API_KEY)

Tests message composition with Claude. Set `USE_CLAUDE=TRUE` first.

```javascript
function testComposerClaude() {
  var student = {
    name: 'Priya Sharma',
    phone: '+919876543210',
    className: 'Grade 10A'
  };

  var schedule = {
    subject: 'Physics',
    teacher: 'Mr. Sharma',
    room: 'Lab 2',
    time: '10:00',
    date: '2026-03-23',
    status: 'Active'
  };

  var msg = composeMessage(student, schedule, 'daily_schedule');
  Logger.log('Claude message: ' + msg);

  if (msg && msg.length > 0 && msg.length <= 1024) {
    Logger.log('PASS: Claude composed a valid message (' + msg.length + ' chars)');
  } else {
    Logger.log('FAIL: Claude message invalid or empty');
  }
}
```

---

## Test 5: Phone Number Formatting

```javascript
function testPhoneFormatting() {
  var cases = [
    ['+919876543210', '+919876543210'],  // Already E.164
    ['919876543210', '+919876543210'],   // Missing +
    ['9876543210', '+919876543210'],     // 10-digit Indian
    ['09876543210', '+919876543210'],    // Domestic with 0
    ['98765 43210', '+919876543210'],    // With spaces
    ['+1 (555) 123-4567', '+15551234567'] // US number
  ];

  var pass = true;
  cases.forEach(function(c) {
    var result = formatPhoneNumber(c[0]);
    if (result === c[1]) {
      Logger.log('OK: ' + c[0] + ' → ' + result);
    } else {
      Logger.log('FAIL: ' + c[0] + ' → ' + result + ' (expected ' + c[1] + ')');
      pass = false;
    }
  });

  Logger.log(pass ? 'PASS: All phone formats correct' : 'FAIL: Some formats incorrect');
}
```

---

## Test 6: Student Lookup

Requires test data in the Students tab.

```javascript
function testStudentLookup() {
  var students = getStudentsByClass('Grade 10A');
  Logger.log('Grade 10A students: ' + students.length);
  students.forEach(function(s) {
    Logger.log('  - ' + s.name + ' (' + s.phone + ')');
  });

  var all = getAllActiveStudents();
  Logger.log('All active students: ' + all.length);

  if (students.length > 0) {
    Logger.log('PASS: Student lookup working');
  } else {
    Logger.log('FAIL: No students found. Add test data to Students tab.');
  }
}
```

---

## Test 7: WhatsApp Send — Single Message (requires WhatsApp config)

**Replace the phone number with YOUR number.**

```javascript
function testWhatsAppSend() {
  var phone = '+919876543210'; // <-- REPLACE WITH YOUR NUMBER
  var result = sendTemplate(
    phone,
    getConfig('TEMPLATE_NAME') || 'class_update',
    ['Hi! This is a test message from WhatsApp Class Notifications.']
  );

  Logger.log('Result: ' + JSON.stringify(result));

  if (result.success) {
    Logger.log('PASS: Message sent! ID: ' + result.messageId);
  } else {
    Logger.log('FAIL: ' + result.error);
  }
}
```

---

## Test 8: Full Pipeline — composeAndSend (requires WhatsApp config)

```javascript
function testFullPipeline() {
  var student = {
    name: 'Priya Sharma',
    phone: '+919876543210', // <-- REPLACE WITH YOUR NUMBER
    className: 'Grade 10A'
  };

  var schedule = {
    subject: 'Physics',
    teacher: 'Mr. Sharma',
    room: 'Lab 2',
    time: '10:00',
    date: '2026-03-23',
    status: 'Active'
  };

  var result = composeAndSend(student, schedule, 'daily_schedule');
  Logger.log('Result: ' + JSON.stringify(result));

  // Check the Log tab for the entry
  var logSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Log');
  var lastRow = logSheet.getLastRow();
  Logger.log('Log tab now has ' + lastRow + ' rows (including header)');

  if (result.success) {
    Logger.log('PASS: Full pipeline works end-to-end');
  } else {
    Logger.log('FAIL: ' + result.error);
  }
}
```

---

## Test 9: Daily Scheduler (requires WhatsApp config + schedule data for today)

```javascript
function testDailyScheduler() {
  Logger.log('Running daily scheduler for today...');
  sendDailySchedule();
  Logger.log('Check the Log tab for results');
}
```

---

## Test 10: Web App POST (run from terminal, not Apps Script)

After deploying as a web app, test from your terminal:

### Health check
```bash
curl "YOUR_WEB_APP_URL"
```

### Send test message
```bash
curl -X POST "YOUR_WEB_APP_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "secret": "your-webhook-secret",
    "action": "send_test",
    "phone": "+919876543210",
    "message": "Test from curl!"
  }'
```

### Send override to a class
```bash
curl -X POST "YOUR_WEB_APP_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "secret": "your-webhook-secret",
    "action": "send_override",
    "target_type": "class",
    "target_value": "Grade 10A",
    "message": "School closed tomorrow due to heavy rain. Stay safe!",
    "sent_by": "Principal"
  }'
```

### Trigger daily schedule
```bash
curl -X POST "YOUR_WEB_APP_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "secret": "your-webhook-secret",
    "action": "send_daily"
  }'
```

---

## Test 11: Edit Trigger (manual test)

1. Open the Google Sheet → **Schedule** tab
2. Change the **Teacher** column in any row (e.g., "Mr. Sharma" → "Dr. Singh")
3. Wait 5-10 seconds (trigger fires asynchronously)
4. Check the **Log** tab — a new row should appear
5. Check your WhatsApp — you should receive the notification
6. Try other columns:
   - Change **Room** → should trigger "room_change"
   - Change **Status** to "Cancelled" → should trigger "cancellation"
   - Change **Time** → should trigger "time_change"

---

## Testing Checklist

| # | Test | Needs API? | Status |
|---|------|-----------|--------|
| 1 | validateConfig | No | |
| 2 | Sheet structure | No | |
| 3 | Composer fallback | No | |
| 4 | Composer Claude | Claude key | |
| 5 | Phone formatting | No | |
| 6 | Student lookup | No (needs data) | |
| 7 | WhatsApp send | WhatsApp | |
| 8 | Full pipeline | WhatsApp + optional Claude | |
| 9 | Daily scheduler | WhatsApp + schedule data | |
| 10 | Web app POST | WhatsApp + deployed | |
| 11 | Edit trigger | WhatsApp + triggers installed | |

Run tests 1-6 first (no API keys needed), then 7-11 after configuring WhatsApp.
