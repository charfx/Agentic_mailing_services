from typing import Literal, Optional
from pydantic import BaseModel, Field


class MeetingDetails(BaseModel):

    title: Optional[str] = Field(
        default=None,
        description="Short meeting title derived only from the explicit purpose or event name in the email."
    )

    date: Optional[str] = Field(
        default=None,
        description=(
            "Meeting date in YYYY-MM-DD format. "
            "For create, this is the scheduled date. "
            "For reschedule, this is the NEW requested date."
        )
    )

    time: Optional[str] = Field(
        default=None,
        description=(
            "Meeting start time in HH:MM 24-hour format. "
            "For create, this is the scheduled time. "
            "For reschedule, this is the NEW requested time."
        )
    )

    previous_date: Optional[str] = Field(
        default=None,
        description=(
            "Current date of the existing meeting in YYYY-MM-DD format, "
            "only when explicitly stated in a rescheduling request."
        )
    )

    previous_time: Optional[str] = Field(
        default=None,
        description=(
            "Current start time of the existing meeting in HH:MM 24-hour format, "
            "only when explicitly stated in a rescheduling request."
        )
    )

    timezone: Optional[str] = Field(
        default=None,
        description=(
            "Timezone as an IANA identifier such as "
            "'Africa/Casablanca', 'Europe/Paris', "
            "'America/New_York'. "
            "Do not return expressions such as 'Morocco time'."
        )
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