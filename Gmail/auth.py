from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
BASE_DIR = Path(__file__).resolve().parent.parent

CREDENTIALS_FILE = BASE_DIR / "Credentiels" / "credentiel.json"
TOKEN_FILE = BASE_DIR / "token.json"


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.send",
]


def authenticate() -> Credentials:

    credentials = None

    # 1. Si nous avons déjà un token OAuth
    if TOKEN_FILE.exists():

        credentials = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    # 2. Token absent ou invalide
    if not credentials or not credentials.valid:

        # Token expiré mais refresh token disponible
        if (
            credentials
            and credentials.expired
            and credentials.refresh_token
        ):
            credentials.refresh(Request())

        # Première authentification
        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )

            credentials = flow.run_local_server(port=0)

        # Sauvegarde du token
        TOKEN_FILE.write_text(
            credentials.to_json(),
            encoding="utf-8"
        )

    return credentials