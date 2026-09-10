from Tools.Logs_tool import append_log_row


result = append_log_row.invoke({
    "timestamp": "2026-09-10 18:20:00",
    "message_id": "test_message",
    "thread_id": "test_thread",
    "sender": "test@gmail.com",
    "subject": "Meeting Test",
    "intent": "meeting",
    "meeting_action": "create",
    "confidence": 0.95,
    "request_status": "complete",
    "missing_fields": [],
    "calendar_success": True,
    "calendar_event_id": "event_123",
    "response_type": "confirmation",
    "email_sent": True,
})

print(result)