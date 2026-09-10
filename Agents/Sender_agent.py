from langchain_core.messages import SystemMessage
from AI.llm import get_llm

from Tools.Gmail_sending_tool import send_email


sender_tools = [
    send_email
]

sender_llm = get_llm().bind_tools(
    sender_tools
)


def sender_agent_node(state):

    response_type = state.get("response_type")
    email = state.get("email", {})
    missing_fields = state.get("missing_fields", [])
    meeting_action = state.get("meeting_action")
    meeting_details = state.get("meeting_details") or {}
    calendar_result = state.get("calendar_result")

    system_message = SystemMessage(
        content=f"""
You are an email response agent for a meeting management system.

You do NOT decide calendar actions.
You do NOT modify calendar events.
You do NOT reinterpret the original email.

Your responsibility is:

1. Generate the correct response email.
2. Send it using the send_email tool.

AUTHORITATIVE STATE

Original sender:
{email.get("from")}

Original subject:
{email.get("subject")}

Original thread_id:
{email.get("thread_id")}

response_type:
{response_type}

meeting_action:
{meeting_action}

meeting_details:
{meeting_details}

missing_fields:
{missing_fields}

calendar_result:
{calendar_result}

RULES

If response_type == "clarification":
- Ask only for the missing information.
- Do not claim any calendar action succeeded.

If response_type == "confirmation":
- Confirm only an action that has actually been completed.
- Do not invent information.

When sending:
- send the response to the original sender
- keep the original conversation thread
- use a Re: subject
- call send_email exactly once
"""
    )

    response = sender_llm.invoke(
        [system_message]
    )

    print("\n===== SENDER AGENT =====")
    print("Response type:", response_type)
    print("Tool calls:", response.tool_calls)

    return {
        "messages": [response]
    }