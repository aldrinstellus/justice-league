/**
 * webapp.gs — Web app endpoints for manual/emergency triggers
 *
 * Deploy as: Web app → Execute as: Me → Access: Anyone (or Anyone with Google account)
 * URL will be: https://script.google.com/macros/s/{DEPLOYMENT_ID}/exec
 */

/**
 * POST endpoint for manual/emergency notifications.
 *
 * Supported actions:
 *   1. send_override  — Send a custom message to a class, student, or all
 *   2. send_daily     — Trigger daily schedule (optionally for a specific date)
 *   3. send_test      — Send a test message to a single phone number
 *
 * All requests must include a valid "secret" field matching WEBHOOK_SECRET in Config.
 *
 * @param {Object} e - Apps Script web app event object
 * @return {ContentService.TextOutput} JSON response
 */
function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) {
      return jsonResponse_({ success: false, message: 'No request body' }, 400);
    }

    var body;
    try {
      body = JSON.parse(e.postData.contents);
    } catch (parseErr) {
      return jsonResponse_({ success: false, message: 'Invalid JSON body' }, 400);
    }

    // Validate shared secret
    var expectedSecret = getConfig('WEBHOOK_SECRET');
    if (!expectedSecret || expectedSecret === '(placeholder)') {
      return jsonResponse_({ success: false, message: 'WEBHOOK_SECRET not configured' }, 500);
    }
    if (body.secret !== expectedSecret) {
      return jsonResponse_({ success: false, message: 'Invalid secret' }, 403);
    }

    var action = body.action;

    switch (action) {
      case 'send_override':
        return handleOverride_(body);

      case 'send_daily':
        return handleDailyTrigger_(body);

      case 'send_test':
        return handleTestSend_(body);

      default:
        return jsonResponse_({ success: false, message: 'Unknown action: ' + action }, 400);
    }

  } catch (e) {
    Logger.log('doPost error: ' + e.message);
    return jsonResponse_({ success: false, message: 'Internal error: ' + e.message }, 500);
  }
}

/**
 * GET endpoint — simple health check.
 * @param {Object} e
 * @return {ContentService.TextOutput} JSON response
 */
function doGet(e) {
  var triggers = ScriptApp.getProjectTriggers();
  return jsonResponse_({
    status: 'ok',
    timestamp: getIndiaTimestamp(),
    triggerCount: triggers.length
  });
}

/**
 * Handles the send_override action.
 * Sends a custom message to a class, individual student, or all students.
 * @private
 */
function handleOverride_(body) {
  var targetType = body.target_type;   // 'class', 'student', or 'all'
  var targetValue = body.target_value; // class name, phone number, or 'all'
  var message = body.message;
  var sentBy = body.sent_by || 'API';

  if (!targetType || !message) {
    return jsonResponse_({ success: false, message: 'Missing target_type or message' }, 400);
  }

  var students = [];

  switch (targetType) {
    case 'class':
      if (!targetValue) {
        return jsonResponse_({ success: false, message: 'Missing target_value for class' }, 400);
      }
      students = getStudentsByClass(targetValue);
      break;

    case 'student':
      if (!targetValue) {
        return jsonResponse_({ success: false, message: 'Missing target_value for student' }, 400);
      }
      var student = getStudentByPhone(targetValue);
      if (student) {
        students = [student];
      } else {
        return jsonResponse_({ success: false, message: 'Student not found: ' + targetValue }, 404);
      }
      break;

    case 'all':
      students = getAllActiveStudents();
      break;

    default:
      return jsonResponse_({ success: false, message: 'Invalid target_type: ' + targetType }, 400);
  }

  if (students.length === 0) {
    return jsonResponse_({ success: false, message: 'No students found for target', sent: 0, failed: 0 }, 404);
  }

  // Send override message to each student
  var sent = 0;
  var failed = 0;
  var errors = [];

  students.forEach(function(student) {
    // For override, compose a simple message with the override text
    var phone = formatPhoneNumber(student.phone);
    var personalMessage = message.replace('{name}', student.name.split(' ')[0]);

    var result = sendTemplate(phone, getConfig('TEMPLATE_NAME') || 'class_update', [personalMessage]);

    logToSheet({
      studentName: student.name,
      phone: phone,
      messageType: 'override',
      messageSent: personalMessage,
      deliveryStatus: result.success ? 'sent' : 'failed',
      whatsappMsgId: result.messageId || '',
      error: result.error || ''
    });

    if (result.success) sent++; else {
      failed++;
      errors.push(student.name + ': ' + result.error);
    }

    Utilities.sleep(200);
  });

  // Log to Overrides tab
  logToOverrides({
    targetType: targetType,
    targetValue: targetValue || 'all',
    message: message,
    sentBy: sentBy,
    status: failed === 0 ? 'sent' : 'partial (' + sent + '/' + (sent + failed) + ')'
  });

  return jsonResponse_({
    success: true,
    sent: sent,
    failed: failed,
    errors: errors,
    message: 'Override sent to ' + sent + ' student(s)'
  });
}

/**
 * Handles the send_daily action.
 * Triggers the daily schedule sender, optionally for a specific date.
 * @private
 */
function handleDailyTrigger_(body) {
  var date = body.date || getIndiaDate();

  if (date !== getIndiaDate()) {
    sendDailyScheduleWithDate_(date);
  } else {
    sendDailySchedule();
  }

  return jsonResponse_({
    success: true,
    message: 'Daily schedule triggered for ' + date
  });
}

/**
 * Handles the send_test action.
 * Sends a test message to a single phone number.
 * @private
 */
function handleTestSend_(body) {
  var phone = body.phone;
  var message = body.message || 'This is a test message from the WhatsApp Class Notification System.';

  if (!phone) {
    return jsonResponse_({ success: false, message: 'Missing phone number' }, 400);
  }

  var formattedPhone = formatPhoneNumber(phone);
  var result = sendTemplate(formattedPhone, getConfig('TEMPLATE_NAME') || 'class_update', [message]);

  logToSheet({
    studentName: 'TEST',
    phone: formattedPhone,
    messageType: 'test',
    messageSent: message,
    deliveryStatus: result.success ? 'sent' : 'failed',
    whatsappMsgId: result.messageId || '',
    error: result.error || ''
  });

  return jsonResponse_({
    success: result.success,
    messageId: result.messageId || '',
    message: result.success ? 'Test message sent' : 'Failed: ' + result.error
  });
}

/**
 * Creates a JSON response for the web app.
 * @private
 * @param {Object} data - Response data
 * @param {number} [statusCode] - HTTP-like status (for logging only; Apps Script always returns 200)
 * @return {ContentService.TextOutput}
 */
function jsonResponse_(data, statusCode) {
  // Note: Apps Script web apps always return HTTP 200.
  // The status is conveyed in the JSON body's "success" field.
  if (statusCode && statusCode >= 400) {
    Logger.log('Error response (' + statusCode + '): ' + JSON.stringify(data));
  }
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
