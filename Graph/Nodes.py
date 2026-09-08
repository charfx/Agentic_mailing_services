from AI.classifier import classify_email


def classify_email_node(state):

    email = state["email"]

    result = classify_email(email)

    return {
        "intent": result.intent,
        "meeting_action": result.meeting_action,
        "confidence": result.confidence,
        "reason": result.reason
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