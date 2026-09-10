from Graph.graph import build_graph

from Gmail.mailing import get_latest_email
from Gmail.parser import parse_email


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

    email = parse_email(raw_email)

    print("\n===== EMAIL RECEIVED =====")
    print("From:", email.get("from"))
    print("Subject:", email.get("subject"))
    print("Date:", email.get("date"))
    print("Body:", email.get("body"))

    # ==========================================
    # 3. Construire le graph
    # ==========================================

    graph = build_graph()

    # ==========================================
    # 4. Initial State
    # ==========================================

    initial_state = {
        "email": email,
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