from typing import Annotated, Literal, TypedDict

from langgraph.graph.message import add_messages


class JARVISState(TypedDict):
    messages: Annotated[list, add_messages]
    user_input: str
    intent: Literal["chat", "task"]
    plan: str
    safe_to_run: bool
    final_reply: str
