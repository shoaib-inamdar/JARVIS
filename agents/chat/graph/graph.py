from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from agents.chat.graph.nodes import (
    chat_node,
    desktop_node,
    guide_node,
    planner_node,
    route_after_planner,
    safety_node,
)
from agents.chat.graph.state import JARVISState


def build_graph() -> CompiledStateGraph:
    """Build and compile the JARVIS multi-agent workflow."""
    graph = StateGraph(JARVISState)

    # Register every node that is referenced in edges
    graph.add_node("planner", planner_node)
    graph.add_node("chat", chat_node)
    graph.add_node("safety", safety_node)
    graph.add_node("desktop", desktop_node)
    graph.add_node("guide", guide_node)  # ← was missing

    graph.set_entry_point("planner")

    # planner routes to: chat | safety (→ desktop) | guide
    graph.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "chat": "chat",
            "safety": "safety",
            "guide": "guide",
        },
    )

    graph.add_edge("chat", END)
    graph.add_edge("safety", "desktop")
    graph.add_edge("desktop", END)  # verifier not yet wired into chat graph
    graph.add_edge("guide", END)

    return graph.compile()


jarvis_graph = build_graph()
