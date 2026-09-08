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

    "status": None
}


    result = graph.invoke(initial_state)

    # try:
    #     png_data = graph.get_graph().draw_mermaid_png()

    #     output_path = Path("graph.png")
    #     output_path.write_bytes(png_data)

    #     print(f"\nGraph saved to: {output_path.resolve()}")

    # except Exception as e:
    #     print("Graph visualization failed:", e)

    print("\n======= FINAL STATE =======\n")

    print("Intent         :", result["intent"])
    print("Meeting action :", result["meeting_action"])
    print("Confidence     :", result["confidence"])
    print("Reason         :", result["reason"])
    print("Status         :", result["status"])

    print("\n======= MEETING DETAILS =======\n")

    details = result["meeting_details"]

    if details is None:

        print("No meeting details.")

    else:

        print("Date         :", details["date"])
        print("Time         :", details["time"])
        print("Timezone     :", details["timezone"])
        print("Duration     :", details["duration_minutes"])
        print("Location     :", details["location"])
        print("Participants :", details["participants"])
        print("Title        :", details["title"])
        print("Raw datetime :", details["raw_datetime_text"])


if __name__ == "__main__":
    main()