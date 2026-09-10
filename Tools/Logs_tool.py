from langchain_core.tools import tool
from googleapiclient.discovery import build

from Gmail.auth import authenticate


SPREADSHEET_ID = "1Keh4jYZC4nEf17bM2h7SH83q1udMqz2pK3HJGuCt1IM"
SHEET_NAME = "logs"


@tool
def append_log_row(
    timestamp: str,
    message_id: str,
    thread_id: str,
    sender: str,
    subject: str,
    intent: str,
    meeting_action: str | None,
    confidence: float | None,
    request_status: str | None,
    missing_fields: list[str] | None,
    calendar_success: bool | None,
    calendar_event_id: str | None,
    response_type: str | None,
    email_sent: bool | None,
) -> dict:

    """
    this function is made to insert a raw in a spreedsheet in google sheet 
    the args are the variable used below in the function
    """
    creds = authenticate()

    service = build(
        "sheets",
        "v4",
        credentials=creds
    )

    values = [[
        timestamp,
        message_id,
        thread_id,
        sender,
        subject,
        intent,
        meeting_action,
        confidence,
        request_status,
        ", ".join(missing_fields or []),
        calendar_success,
        calendar_event_id,
        response_type,
        email_sent,
    ]]

    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:N",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body={
                "values": values
            },
        )
        .execute()
    )

    return {
        "success": True,
        "updated_range": result.get(
            "updates",
            {}
        ).get("updatedRange"),
    }