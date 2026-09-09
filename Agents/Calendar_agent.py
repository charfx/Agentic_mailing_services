from AI.llm import get_llm
from Tools.Calandar_tools import create_calendar_event


calendar_tools = [
    create_calendar_event
]


calendar_llm = get_llm().bind_tools(
    calendar_tools
)


def calendar_agent_node(state):

    action = state["meeting_action"]
    details = state["meeting_details"]

    prompt = f"""
You are a Google Calendar execution agent.

The email has already been analyzed.

Meeting action:
{action}

Meeting details:
{details}

Rules:
- Do not reinterpret the original email.
- Do not change meeting_action.
- Do not invent information.
- If meeting_action is "create", call create_calendar_event.
- Use only the meeting details provided.
"""

    response = calendar_llm.invoke(prompt)

    print("\n===== CALENDAR AGENT =====")
    print("Action:", action)
    print("Details:", details)
    print("Tool calls:", response.tool_calls)

    return {
        "messages": [response]
    }