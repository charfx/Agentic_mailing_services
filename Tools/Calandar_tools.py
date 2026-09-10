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

## selecting event meeting already defined in the google calendar 
@tool
def find_calendar_event(
    title: str,
    date: Optional[str]=None ,
    time: Optional[str] = None,
    timezone: str = "Africa/Casablanca",
) -> dict:
    """
    Find an existing Google Calendar event.

    Use before rescheduling or cancelling an event.

    This tool only searches.
    It does not modify or delete calendar events.
    """

    tz = ZoneInfo(timezone)

    start_datetime = datetime.strptime(
        date,
        "%Y-%m-%d"
    ).replace(
        hour=0,
        minute=0,
        second=0,
        tzinfo=tz
    )

    end_datetime = start_datetime + timedelta(
        days=1
    )

    creds = authenticate()

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=start_datetime.isoformat(),
            timeMax=end_datetime.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get(
        "items",
        []
    )

    matches = []

    for event in events:

        event_title = event.get(
            "summary",
            ""
        )

        event_start = event.get(
            "start",
            {}
        ).get(
            "dateTime"
        )

        if not event_start:
            continue

        if title:
            if title.lower() not in event_title.lower():
                continue

        if time:

            event_time = datetime.fromisoformat(
                event_start
            ).strftime(
                "%H:%M"
            )

            if event_time != time:
                continue

        matches.append(
            {
                "event_id": event["id"],
                "title": event_title,
                "start": event_start,
                "end": event.get(
                    "end",
                    {}
                ).get(
                    "dateTime"
                ),
                "location": event.get(
                    "location"
                ),
            }
        )

    return {
        "success": True,
        "count": len(matches),
        "events": matches,
    }

## update reschedualing the events :
@tool
def reschedule_calendar_event(
    event_id: str,
    new_date: str,
    new_time: str,
    timezone: str = "Africa/Casablanca",
    duration_minutes: Optional[int] = None,
) -> dict:
    """
    Reschedule an EXISTING Google Calendar event.

    Use ONLY when:
    - meeting_action is "reschedule"
    - the target event has already been identified
    - event_id is known
    - new_date and new_time are known

    Do NOT use this tool to create a new event.
    Do NOT guess the event_id.

    Args:
        event_id: Google Calendar event identifier.
        new_date: New meeting date in YYYY-MM-DD format.
        new_time: New meeting time in HH:MM 24-hour format.
        timezone: IANA timezone identifier.
        duration_minutes: Optional new duration. If omitted,
                          preserve the existing event duration.
    """

    if not event_id:
        raise ValueError("event_id is required.")

    if not new_date:
        raise ValueError("new_date is required.")

    if not new_time:
        raise ValueError("new_time is required.")

    try:
        tz = ZoneInfo(timezone)

    except Exception as exc:
        raise ValueError(
            f"Invalid IANA timezone: {timezone}"
        ) from exc

    creds = authenticate()

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    # -------------------------
    # Retrieve existing event
    # -------------------------

    event = (
        service.events()
        .get(
            calendarId="primary",
            eventId=event_id
        )
        .execute()
    )

    # -------------------------
    # Existing start/end
    # -------------------------

    old_start_raw = event.get(
        "start",
        {}
    ).get("dateTime")

    old_end_raw = event.get(
        "end",
        {}
    ).get("dateTime")

    if not old_start_raw or not old_end_raw:
        raise ValueError(
            "This event does not contain standard start/end datetimes."
        )

    old_start = datetime.fromisoformat(
        old_start_raw
    )

    old_end = datetime.fromisoformat(
        old_end_raw
    )

    # Preserve original duration if no new duration supplied
    if duration_minutes is None:

        duration = old_end - old_start

    else:

        if duration_minutes <= 0:
            raise ValueError(
                "duration_minutes must be greater than 0."
            )

        duration = timedelta(
            minutes=duration_minutes
        )

    # -------------------------
    # Construct new datetime
    # -------------------------

    try:
        new_start = datetime.strptime(
            f"{new_date} {new_time}",
            "%Y-%m-%d %H:%M"
        ).replace(
            tzinfo=tz
        )

    except ValueError as exc:
        raise ValueError(
            "new_date must use YYYY-MM-DD "
            "and new_time must use HH:MM."
        ) from exc

    new_end = new_start + duration

    # -------------------------
    # Update event
    # -------------------------

    event["start"] = {
        "dateTime": new_start.isoformat(),
        "timeZone": timezone,
    }

    event["end"] = {
        "dateTime": new_end.isoformat(),
        "timeZone": timezone,
    }

    updated_event = (
        service.events()
        .update(
            calendarId="primary",
            eventId=event_id,
            body=event
        )
        .execute()
    )

    return {
        "success": True,
        "event_id": updated_event["id"],
        "title": updated_event.get("summary"),
        "old_start": old_start_raw,
        "new_start": updated_event["start"].get(
            "dateTime"
        ),
        "new_end": updated_event["end"].get(
            "dateTime"
        ),
    }
## Canceling event from google calendar ;
@tool
def cancel_calendar_event(
    event_id: str,
) -> dict:
    """
    Cancel an EXISTING Google Calendar event.

    Use ONLY when:
    - meeting_action is "cancel"
    - the target event has already been identified
    - event_id is known

    Do NOT guess the event_id.
    Do NOT use this tool for rescheduling or creating events.
    """

    if not event_id:
        raise ValueError(
            "event_id is required."
        )

    creds = authenticate()

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    # Retrieve first so we can return useful information
    event = (
        service.events()
        .get(
            calendarId="primary",
            eventId=event_id
        )
        .execute()
    )

    event_title = event.get(
        "summary"
    )

    event_start = event.get(
        "start",
        {}
    ).get(
        "dateTime"
    )

    # Delete event
    (
        service.events()
        .delete(
            calendarId="primary",
            eventId=event_id
        )
        .execute()
    )

    return {
        "success": True,
        "event_id": event_id,
        "title": event_title,
        "start": event_start,
        "status": "cancelled",
    }