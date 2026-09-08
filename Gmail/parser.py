## ce parser sert exactement au loading en format forte dans extraction des elements necessaire dans 
#workflow
## cette base64 a role majeur qui peut transformer un element binaire(image,file binaire,....) en format text 
#exploitable et compose de 64 caractere

import base64 

#c'est claire il extrait le header du mail !
def extract_headers(payload):

    headers = payload.get("headers", [])

    extracted = {}

    for header in headers:

        name = header.get("name", "").lower()
        value = header.get("value", "")

        extracted[name] = value

    return extracted

##decodage du body via base64 :
def decode_body(data):

    if not data:
        return ""

    decoded_bytes = base64.urlsafe_b64decode(data)

    return decoded_bytes.decode(
        "utf-8",
        errors="replace"
    )

## maintenant la vrai extraction des elements !
def extract_plain_text(payload):

    # Cas 1 :
    # le payload lui-même contient directement du texte
    if payload.get("mimeType") == "text/plain":

        data = payload.get("body", {}).get("data")

        return decode_body(data)

    # Cas 2 :
    # multipart/*
    for part in payload.get("parts", []):

        if part.get("mimeType") == "text/plain":

            data = part.get("body", {}).get("data")

            return decode_body(data)

    return ""

## le parser qui appelle tous les outils definie 
def parse_email(message):

    payload = message.get("payload", {})

    headers = extract_headers(payload)

    body = extract_plain_text(payload)

    return {
        "message_id": message.get("id"),

        "thread_id": message.get("threadId"),

        "labels": message.get("labelIds", []),

        "from": headers.get("from"),

        "to": headers.get("to"),

        "subject": headers.get("subject"),

        "date": headers.get("date"),

        "body": body
    }