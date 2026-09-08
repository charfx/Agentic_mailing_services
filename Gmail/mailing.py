#file that call all previous files to receive tha latest mail 
##the latest mail in our case is received by the mailing ids and thread id 
## because the google cloud console precisement gmail api livre pas en api les mail
## mais il livre leur ids et c'est a nous de faire pulling to our terminal

from Gmail.Client import get_gmail_service
from Gmail.parser import parse_email

def get_latest_email():

    service = get_gmail_service()

    # 1. Récupérer l'ID du dernier message
    result = (
        service
        .users()
        .messages()
        .list(
            userId="me",
            maxResults=1
        )
        .execute()
    )

    messages = result.get("messages", [])

    if not messages:
        return None

    message_id = messages[0]["id"]

    # 2. Récupérer le message complet
    message = (
        service
        .users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="full"
        )
        .execute()
    )

    return parse_email(message)