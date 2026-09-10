from AI.classifier import analyze_email
from Tools.Gmail_sending_tool import send_email

def classify_email_node(state):

    email = state["email"]

    result = analyze_email(email)

    meeting_details = None

    if result.meeting_details is not None:
        meeting_details = result.meeting_details.model_dump()

    return {
        "intent": result.intent,
        "meeting_action": result.meeting_action,
        "confidence": result.confidence,
        "reason": result.reason,
        "meeting_details": meeting_details
    }


def meeting_detected_node(state):

    return {
        "status": "meeting_detected"
    }


def review_required_node(state):

    return {
        "status": "review_required"
    }


def route_email(state):

    intent = state["intent"]
    confidence = state["confidence"]

    if intent == "non_meeting":
        return "non_meeting"

    if intent == "uncertain":
        return "review"

    if confidence is not None and confidence < 0.70:
        return "review"

    return "meeting"
def route_after_calendar_tool(state):

    messages = state.get("messages", [])

    if not messages:
        return "confirmation"

    last_message = messages[-1]

    tool_name = getattr(
        last_message,
        "name",
        None
    )

    print("\n===== TOOL ROUTING =====")
    print("Last tool:", tool_name)

    if tool_name == "find_calendar_event":
        return "agent"

    return "confirmation"

def required_items_node(state):

    action = state.get("meeting_action")
    details = state.get("meeting_details") or {}

    missing_fields = []

    if action == "create":
        required_fields = [
            "date",
            "time"
        ]

    elif action == "reschedule":
        required_fields = [
            "title",
            "date",
            "time"
        ]

    elif action == "cancel":
        required_fields = [
            "title"
        ]

    else:
        return {
            "request_status": "incomplete",
            "missing_fields": ["meeting_action"],
            "response_type": "clarification"
        }

    for field in required_fields:
        if not details.get(field):
            missing_fields.append(field)

    if missing_fields:
        return {
            "request_status": "incomplete",
            "missing_fields": missing_fields,
            "response_type": "clarification"
        }

    return {
        "request_status": "complete",
        "missing_fields": [],
        "response_type": None
    }
def route_required_items(state):

    if state["request_status"] == "complete":
        return "calendar"

    return "clarification"

def prepare_confirmation_node(state):

    return {
        "response_type": "confirmation"
    }
def prepare_clarification_node(state):

    return {
        "response_type": "clarification"
    }

def send_email_node(state):

    email = state["email"]
    generated_email = state["generated_email"]

    sender = email["from"]
    subject = email["subject"]
    thread_id = email.get("thread_id")

    if not subject.lower().startswith("re:"):
        subject = f"Re: {subject}"

    result = send_email.invoke({
        "to": sender,
        "subject": subject,
        "body": generated_email,
        "thread_id": thread_id,
    })

    print("\n===== GMAIL SENDING =====")
    print("To:", sender)
    print("Subject:", subject)
    print("Result:", result)

    return {
        "email_send_result": result
    }