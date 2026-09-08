from googleapiclient.discovery import build

from Gmail.auth import authenticate_gmail


def get_gmail_service():

    credentials = authenticate_gmail()

    service = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    return service