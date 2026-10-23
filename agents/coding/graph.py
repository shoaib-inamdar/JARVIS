from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from .coding_state import CodingState
from .nodes import (
    code_node,
    memory_node,
    planner_node,
    safety_node,
    terminal_node,
    verifier_node,
)


def route_after_code(state: CodingState) -> str:
    """Route to terminal (with safety check) if a command is pending, else verify."""
    if state.get("pending_permission", "").strip():
        return "terminal"
    return "verifier"


def build_coding_graph() -> CompiledStateGraph:
    """Build and compile the JARVIS Coding Mode multi-agent graph."""
    g = StateGraph(CodingState)

    g.add_node("planner", planner_node)
    g.add_node("code", code_node)
    g.add_node("safety", safety_node)
    g.add_node("terminal", terminal_node)
    g.add_node("verifier", verifier_node)  # ← was missing
    g.add_node("memory", memory_node)

    g.set_entry_point("planner")

    g.add_edge("planner", "code")

    # pending_permission set → safety check → terminal → verify
    # nothing pending → go straight to verify
    g.add_conditional_edges(
        "code",
        route_after_code,
        {"terminal": "safety", "verifier": "verifier"},
    )

    g.add_edge("safety", "terminal")
    g.add_edge("terminal", "verifier")
    g.add_edge("verifier", "memory")
    g.add_edge("memory", END)

    return g.compile()


coding_graph = build_coding_graph()
