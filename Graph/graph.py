from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from Graph.State import AgentState

from Agents.Calendar_agent import (
    calendar_agent_node,
    calendar_tools
)

from Agents.Sender_agent import (
    sender_agent_node,
    sender_tools
)

from Graph.Nodes import (
    classify_email_node,
    meeting_detected_node,
    review_required_node,
    route_email,
    route_after_calendar_tool,
    route_required_items,
    required_items_node,
    prepare_confirmation_node,
    prepare_clarification_node,
)


calendar_tools_node = ToolNode(
    calendar_tools
)

sender_tools_node = ToolNode(
    sender_tools
)


def build_graph():

    builder = StateGraph(
        AgentState
    )

    # ==================================================
    # NODES
    # ==================================================

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
        "required_items",
        required_items_node
    )

    builder.add_node(
        "calendar_agent",
        calendar_agent_node
    )

    builder.add_node(
        "calendar_tools",
        calendar_tools_node
    )

    builder.add_node(
        "prepare_confirmation",
        prepare_confirmation_node
    )

    builder.add_node(
        "prepare_clarification",
        prepare_clarification_node
    )

    builder.add_node(
        "sender_agent",
        sender_agent_node
    )

    builder.add_node(
        "sender_tools",
        sender_tools_node
    )

    # ==================================================
    # START
    # ==================================================

    builder.add_edge(
        START,
        "classify_email"
    )

    # ==================================================
    # EMAIL CLASSIFICATION
    # ==================================================

    builder.add_conditional_edges(
        "classify_email",
        route_email,
        {
            "meeting": "meeting_detected",
            "review": "review_required",
            "non_meeting": END,
        }
    )

    # ==================================================
    # MEETING DETECTED
    # ==================================================

    builder.add_edge(
        "meeting_detected",
        "required_items"
    )

    # ==================================================
    # REQUIRED ITEMS VALIDATION
    # ==================================================

    builder.add_conditional_edges(
        "required_items",
        route_required_items,
        {
            "calendar": "calendar_agent",
            "clarification": "prepare_clarification",
        }
    )

    builder.add_edge(
        "prepare_clarification",
        "sender_agent"
    )

    # ==================================================
    # CALENDAR AGENT
    # ==================================================

    builder.add_conditional_edges(
        "calendar_agent",
        tools_condition,
        {
            "tools": "calendar_tools",
            "__end__": END,
        }
    )

    # ==================================================
    # CALENDAR TOOL RESULT
    # ==================================================

    builder.add_conditional_edges(
        "calendar_tools",
        route_after_calendar_tool,
        {
            "agent": "calendar_agent",
            "confirmation": "prepare_confirmation",
        }
    )

    # ==================================================
    # PREPARE CONFIRMATION
    # ==================================================

    builder.add_edge(
        "prepare_confirmation",
        "sender_agent"
    )

    # ==================================================
    # SENDER AGENT
    # ==================================================

    builder.add_conditional_edges(
        "sender_agent",
        tools_condition,
        {
            "tools": "sender_tools",
            "__end__": END,
        }
    )

    # ==================================================
    # SENDER TOOL
    # ==================================================

    builder.add_edge(
        "sender_tools",
        END
    )

    # ==================================================
    # REVIEW
    # ==================================================

    builder.add_edge(
        "review_required",
        END
    )

    return builder.compile()