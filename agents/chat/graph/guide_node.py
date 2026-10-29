from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from agents.chat.graph.state import JARVISState
from tools.registry import registry

llm = ChatGroq(model="openai/gpt-oss-20b")


def guide_node(state: JARVISState) -> dict:

    window = registry.call("get_active_window")

    screen_text = registry.call("read_screen_text")

    context = f"""
       Currently active app: {window}

       Text visible on screen:
       {screen_text}

       User's question: {state["user_input"]}
       """

    messages = [
        SystemMessage(
            content=(
                "You are JARVIS, a helpful desktop assistant. "
                "The user has asked for help. You can see what's on their screen. "
                "Give clear, numbered, step-by-step instructions. "
                "Be specific about what to click, type, or look for. "
                "Keep steps short and actionable. "
                "Reference what you actually see on the screen."
            )
        ),
        HumanMessage(content=context),
    ]

    response = llm.invoke(messages)

    return {
        "final_reply": response.content,
        "avatar_mood": "speaking",
        "action_history": [
            *state.get("action_history", []),
            f"Guide Mode: analyzed screen, active app: {window}",
        ],
    }
