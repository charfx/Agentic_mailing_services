from AI.llm import get_llm
from Tools.Calandar_tools import create_calendar_event,find_calendar_event,reschedule_calendar_event,cancel_calendar_event
from langchain_core.messages import HumanMessage
from langchain.messages import SystemMessage

calendar_tools = [
    create_calendar_event,find_calendar_event,reschedule_calendar_event,cancel_calendar_event
]


calendar_llm = get_llm().bind_tools(
    calendar_tools
)
def calendar_agent_node(state):

    action = state["meeting_action"]
    details = state["meeting_details"]

    system_message = SystemMessage(
        content=f"""
You are a Google Calendar execution agent.

The email has ALREADY been analyzed by another model.
Do NOT reinterpret the original email.

AUTHORITATIVE STATE:

meeting_action:
{action}

meeting_details:
{details}

The values above are authoritative and MUST be used.

==================================================
CREATE
==================================================

If meeting_action == "create":

Call create_calendar_event using:
- title = meeting_details.title
- date = meeting_details.date
- time = meeting_details.time
- timezone = meeting_details.timezone
- duration_minutes = meeting_details.duration_minutes
- location = meeting_details.location

==================================================
RESCHEDULE
==================================================

If meeting_action == "reschedule":

meeting_details.previous_date and previous_time
represent the CURRENT event schedule.

meeting_details.date and time
represent the NEW requested schedule.

Step 1:
Call find_calendar_event using:
- title = meeting_details.title
- date = meeting_details.previous_date
- time = meeting_details.previous_time
- timezone = meeting_details.timezone

Step 2:
After find_calendar_event returns:

If count == 1:
IMMEDIATELY call reschedule_calendar_event using:

- event_id = the event_id returned by find_calendar_event
- new_date = meeting_details.date
- new_time = meeting_details.time
- timezone = meeting_details.timezone
- duration_minutes = meeting_details.duration_minutes

DO NOT ask the user for the new date or time
if meeting_details.date and meeting_details.time already exist.

If count == 0:
Stop.

If count > 1:
Stop because the event is ambiguous.

==================================================
CANCEL
==================================================

If meeting_action == "cancel":

First call find_calendar_event.

If exactly one event is found,
call cancel_calendar_event using its event_id.

==================================================
SAFETY
==================================================

Never invent an event_id.
Never change meeting_action.
Never create an event during a reschedule or cancel operation.
Never ask for information already available in meeting_details.
"""
    )

    history = state.get("messages", [])

    response = calendar_llm.invoke(
        [system_message] + history
    )

    print("\n===== CALENDAR AGENT =====")
    print("Action:", action)
    print("Tool calls:", response.tool_calls)

    return {
        "messages": [response]
    }