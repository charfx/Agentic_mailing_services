from AI.classifier import analyze_email
from Tools.Gmail_sending_tool import send_email
from datetime import datetime
from Tools.Logs_tool import append_log_row
import json
import ast

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

def log_node(state):

    email = state.get("email", {})

    result = append_log_row.invoke({
        "timestamp": datetime.now().isoformat(),

        "message_id": email.get("message_id"),
        "thread_id": email.get("thread_id"),
        "sender": email.get("from"),
        "subject": email.get("subject"),

        "intent": state.get("intent"),
        "meeting_action": state.get("meeting_action"),
        "confidence": state.get("confidence"),

        "request_status": state.get("request_status"),
        "missing_fields": state.get("missing_fields", []),

        "calendar_success": None,
        "calendar_event_id": None,

        "response_type": state.get("response_type"),

        "email_sent": True,
    })

    print("\n===== GOOGLE SHEETS LOG =====")
    print(result)

    return {
        "log_result": result
    }
def capture_calendar_result_node(state):
    """
    Capture le résultat du dernier Calendar Tool exécuté
    et le stocke dans state["calendar_result"].
    """

    messages = state.get("messages", [])

    if not messages:
        return {
            "calendar_result": {
                "success": False,
                "error": "No tool message found"
            }
        }

    last_message = messages[-1]

    content = getattr(last_message, "content", None)

    if content is None:
        return {
            "calendar_result": {
                "success": False,
                "error": "Calendar tool returned no content"
            }
        }

    # Selon la version LangGraph/LangChain,
    # le ToolMessage peut contenir directement un dict
    if isinstance(content, dict):
        calendar_result = content

    # Très souvent ToolNode convertit le dict retourné
    # par le tool en string
    elif isinstance(content, str):
        try:
            calendar_result = json.loads(content)

        except json.JSONDecodeError:
            try:
                calendar_result = ast.literal_eval(content)

            except (ValueError, SyntaxError):
                calendar_result = {
                    "success": False,
                    "error": "Unable to parse calendar tool result",
                    "raw_content": content
                }

    else:
        calendar_result = {
            "success": False,
            "error": "Unexpected calendar tool result format",
            "raw_content": str(content)
        }

    print("\n===== CAPTURE CALENDAR RESULT =====")
    print(calendar_result)

    return {
        "calendar_result": calendar_result
    }