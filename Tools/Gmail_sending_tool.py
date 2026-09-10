from email.mime.text import MIMEText
import base64

from langchain_core.tools import tool

from Gmail.auth import authenticate
from googleapiclient.discovery import build


@tool
def send_email(
    to: str,
    subject: str,
    body: str,
    thread_id: str | None = None,
) -> dict:
    """
    Send an email using Gmail API.

    Args:
        to: Recipient email address.
        subject: Email subject.
        body: Plain text email body.
        thread_id: Optional Gmail thread ID if replying inside an existing conversation.

    Returns:
        Dictionary containing sending status and Gmail message metadata.
    """

    creds = authenticate()

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    message = MIMEText(body)

    message["to"] = to
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    gmail_message = {
        "raw": raw_message
    }

    if thread_id:
        gmail_message["threadId"] = thread_id

    sent_message = (
        service.users()
        .messages()
        .send(
            userId="me",
            body=gmail_message
        )
        .execute()
    )

    return {
        "success": True,
        "message_id": sent_message.get("id"),
        "thread_id": sent_message.get("threadId"),
        "to": to,
        "subject": subject,
    }