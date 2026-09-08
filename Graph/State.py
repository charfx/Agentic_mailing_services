from typing import TypedDict, Optional


class AgentState(TypedDict):

    email: dict

    intent: Optional[str]
    meeting_action: Optional[str]
    confidence: Optional[float]
    reason: Optional[str]
    status: Optional[str]