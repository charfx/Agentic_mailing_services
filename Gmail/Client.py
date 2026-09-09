from googleapiclient.discovery import build

from Gmail.auth import authenticate


def get_gmail_service():

    credentials = authenticate()

    service = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    return service