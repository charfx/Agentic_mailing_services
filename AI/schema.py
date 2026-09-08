from typing import Literal, Optional
from pydantic import BaseModel, Field


class EmailIntent(BaseModel):

    intent: Literal[
        "meeting",
        "non_meeting",
        "uncertain"
    ]

    meeting_action: Optional[
        Literal[
            "create",
            "confirm",
            "reschedule",
            "cancel",
            "unknown"
        ]
    ] = None

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )

    reason: str 