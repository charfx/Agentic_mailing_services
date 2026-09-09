from datetime import datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from langchain_core.tools import tool
from googleapiclient.discovery import build

from Gmail.auth import authenticate


@tool
def create_calendar_event(
    date: str,
    time: str,
    title: Optional[str] = None,
    timezone: str = "Africa/Casablanca",
    duration_minutes: int = 30,
    location: Optional[str] = None,
) -> dict:
    """
    Create a new Google Calendar event.

    Use this tool only when meeting_action is "create".

    Required:
    - date: YYYY-MM-DD
    - time: HH:MM

    Optional/defaulted:
    - title: defaults to "Meeting"
    - timezone: defaults to Africa/Casablanca
    - duration_minutes: defaults to 30
    - location: optional

    Never invent date or time.
    TIMEZONE NORMALIZATION RULE:

    When the timezone is explicitly recognizable,
    normalize it to a valid IANA timezone identifier.

    Examples:
    - "Morocco time" -> "Africa/Casablanca"
    - "Paris time" -> "Europe/Paris"
    - "New York time" -> "America/New_York"

    Never return informal timezone expressions such as
    "Morocco time", "Paris time", etc.

    If the timezone cannot be safely identified, return null.
    """

    if not date:
        raise ValueError("date is required.")

    if not time:
        raise ValueError("time is required.")

    if title is None or not title.strip():
        title = "Meeting"

    if duration_minutes <= 0:
        duration_minutes = 30

    try:
        tz = ZoneInfo(timezone)

    except ZoneInfoNotFoundError as exc:
        raise ValueError(
            f"Invalid IANA timezone: {timezone}"
        ) from exc

    try:
        start_datetime = datetime.strptime(
            f"{date} {time}",
            "%Y-%m-%d %H:%M"
        ).replace(tzinfo=tz)

    except ValueError as exc:
        raise ValueError(
            "date must use YYYY-MM-DD and time must use HH:MM."
        ) from exc

    end_datetime = start_datetime + timedelta(
        minutes=duration_minutes
    )

    event = {
        "summary": title,

        "start": {
            "dateTime": start_datetime.isoformat(),
            "timeZone": timezone,
        },

        "end": {
            "dateTime": end_datetime.isoformat(),
            "timeZone": timezone,
        },
    }

    if location:
        event["location"] = location

    creds = authenticate()

    calendar_service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    created_event = (
        calendar_service
        .events()
        .insert(
            calendarId="primary",
            body=event
        )
        .execute()
    )

    return {
        "success": True,
        "event_id": created_event["id"],
        "html_link": created_event.get("htmlLink"),
        "start": created_event["start"].get("dateTime"),
        "end": created_event["end"].get("dateTime"),
    }