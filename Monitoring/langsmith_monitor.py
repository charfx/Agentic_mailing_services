from dotenv import load_dotenv
import os 
from Gmail.mailing import get_latest_email
from Graph.graph import build_graph
load_dotenv()


os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
os.environ["LANGSMITH_TRACING"]="true"
os.environ["LANGSMITH_PROJECT"]="pr-sandy-owner-55"
os.environ["LANGSMITH_ENDPOINT"]="https://api.smith.langchain.com"


def main():

    print("\n======================================")
    print("      AGENTIC MAILING AI")
    print("======================================\n")

    # ==========================================
    # 1. Récupérer le dernier email Gmail
    # ==========================================

    raw_email = get_latest_email()

    if raw_email is None:
        print("Aucun email trouvé.")
        return

    # ==========================================
    # 2. Parser l'email
    # ==========================================

    print("\n===== EMAIL RECEIVED =====")
    print("From:", raw_email.get("from"))
    print("Subject:", raw_email.get("subject"))
    print("Date:", raw_email.get("date"))
    print("Body:", raw_email.get("body"))

    # ==========================================
    # 3. Construire le graph
    # ==========================================

    graph = build_graph()

    # ==========================================
    # 4. Initial State
    # ==========================================

    initial_state = {
        "email": raw_email,
        "messages": [],
    }

    # ==========================================
    # 5. Exécuter tout le workflow
    # ==========================================

    print("\n======================================")
    print("        STARTING LANGGRAPH")
    print("======================================\n")

    final_state = graph.invoke(initial_state)

    # ==========================================
    # 6. Résultat final
    # ==========================================

    print("\n======================================")
    print("            FINAL STATE")
    print("======================================")

    print("\nIntent:")
    print(final_state.get("intent"))

    print("\nMeeting action:")
    print(final_state.get("meeting_action"))

    print("\nConfidence:")
    print(final_state.get("confidence"))

    print("\nMeeting details:")
    print(final_state.get("meeting_details"))

    print("\nRequest status:")
    print(final_state.get("request_status"))

    print("\nCalendar result:")
    print(final_state.get("calendar_result"))

    print("\nResponse type:")
    print(final_state.get("response_type"))

    print("\nLog result:")
    print(final_state.get("log_result"))

    print("\n======================================")
    print("          WORKFLOW FINISHED")
    print("======================================\n")


if __name__ == "__main__":
    main()