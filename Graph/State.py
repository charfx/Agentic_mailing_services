from typing import TypedDict, Optional,Annotated

from langgraph.graph.message import add_messages

class AgentState(TypedDict):

    email: dict

    intent: Optional[str]

    meeting_action: Optional[str]

    confidence: Optional[float]

    reason: Optional[str]

    meeting_details: Optional[dict]

    status: Optional[str]

    messages: Annotated[list, add_messages]

    request_status: Optional[str]

    missing_fields: Optional[list[str]]

    response_type: Optional[str]

    calendar_result: Optional[dict]

    generated_email: Optional[str]

    log_result: Optional[dict]