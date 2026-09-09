from Gmail.mailing import get_latest_email
from Graph.graph import build_graph
from IPython.display import Image,display
from pathlib import Path

def main():

    email = get_latest_email()

    if email is None:
        print("No email found.")
        return

    graph = build_graph()

    initial_state = {

        "email": email,

        "intent": None,
        "meeting_action": None,
        "confidence": None,
        "reason": None,

        "meeting_details": None,

        "status": None,

        "messages": []
    }

    result = graph.invoke(
        initial_state
    )
    

    print(result)


if __name__ == "__main__":
    main()