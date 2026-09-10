from AI.classifier import analyze_email


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
        return "end"

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

    return "end"