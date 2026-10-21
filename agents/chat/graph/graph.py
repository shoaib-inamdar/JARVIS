from langgraph.graph import END, StateGraph
from agents.graph.state import JARVISState
from agents.graph.nodes import (
    planner_node,
    chat_node,
    safety_node,
    route_after_planner,
)

def build_graph():
    """Build and compile the JARVIS multi-agent workflow."""
    graph = StateGraph(JARVISState)
    graph.add_node("planner",planner_node)
    graph.add_node("chat",chat_node)
    graph.add_node("safety",safety_node)
    graph.set_entry_point("planner")
    graph.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "chat":"chat",
            "safety":"safety",
        },
    )
    graph.add_edge("chat",END)
    graph.add_edge("safety",END)
    return graph.compile()
jarvis_graph = build_graph()
