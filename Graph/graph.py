from langgraph.graph import StateGraph, START, END
from IPython.display import display,Image
from Graph.State import AgentState

from Graph.Nodes import (
    classify_email_node,
    meeting_detected_node,
    review_required_node,
    route_email
)


def build_graph():

    builder = StateGraph(AgentState)

    builder.add_node(
        "classify_email",
        classify_email_node
    )

    builder.add_node(
        "meeting_detected",
        meeting_detected_node
    )

    builder.add_node(
        "review_required",
        review_required_node
    )


    builder.add_edge(
        START,
        "classify_email"
    )


    builder.add_conditional_edges(
        "classify_email",
        route_email,
        {
            "meeting": "meeting_detected",

            "review": "review_required",

            "non_meeting": END
        }
    )


    builder.add_edge(
        "meeting_detected",
        END
    )

    builder.add_edge(
        "review_required",
        END
    )

    return builder.compile()

