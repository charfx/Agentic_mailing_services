from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from Graph.State import AgentState

from Agents.Calendar_agent import (
    calendar_agent_node,
    calendar_tools
)

from Graph.Nodes import (
    classify_email_node,
    meeting_detected_node,
    review_required_node,
    route_email
)


calendar_tools_node = ToolNode(calendar_tools)


def build_graph():

    builder = StateGraph(AgentState)

    # -------------------------
    # Nodes
    # -------------------------

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

    builder.add_node(
        "calendar_agent",
        calendar_agent_node
    )

    builder.add_node(
        "calendar_tools",
        calendar_tools_node
    )

    # -------------------------
    # Start
    # -------------------------

    builder.add_edge(
        START,
        "classify_email"
    )

    # -------------------------
    # Email routing
    # -------------------------

    builder.add_conditional_edges(
        "classify_email",
        route_email,
        {
            "meeting": "meeting_detected",
            "review": "review_required",
            "non_meeting": END
        }
    )

    # -------------------------
    # Meeting → Calendar Agent
    # -------------------------

    builder.add_edge(
        "meeting_detected",
        "calendar_agent"
    )

    # -------------------------
    # Calendar Agent routing
    # -------------------------

    builder.add_conditional_edges(
        "calendar_agent",
        tools_condition,
        {
            "tools": "calendar_tools",
            "__end__": END,
        }
    )

    # Tool result returns to agent
    builder.add_edge(
        "calendar_tools",
        END
    )

    return builder.compile()