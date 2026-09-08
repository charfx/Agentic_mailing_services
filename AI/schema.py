from typing import Literal, Optional
from pydantic import BaseModel, Field


class MeetingDetails(BaseModel):

    date: Optional[str] = Field(
        default=None,
        description="Meeting date in YYYY-MM-DD format if explicitly known."
    )

    time: Optional[str] = Field(
        default=None,
        description="Meeting start time in HH:MM 24-hour format if known."
    )

    timezone: Optional[str] = Field(
        default=None,
        description="Explicit timezone if provided or clearly identifiable."
    )

    duration_minutes: Optional[int] = Field(
        default=None,
        description="Meeting duration in minutes if explicitly provided."
    )

    location: Optional[str] = Field(
        default=None,
        description="Physical location or online platform such as Google Meet or Zoom."
    )

    participants: Optional[list[str]] = Field(
        default=None,
        description="Explicitly mentioned meeting participants."
    )

    title: Optional[str] = Field(
        default=None,
        description="Short meeting title derived only from the explicit purpose of the email."
    )

    raw_datetime_text: Optional[str] = Field(
        default=None,
        description="Original date/time expression appearing in the email."
    )


class EmailAnalysis(BaseModel):

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

    meeting_details: Optional[MeetingDetails] = None