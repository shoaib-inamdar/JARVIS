from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

from agents.graph.state import JARVISState
from core.config.settings import GEMINI_API_KEY, AI_MODEL


llm = ChatGoogleGenerativeAI(
    model=AI_MODEL,
    google_api_key=GEMINI_API_KEY,
    temperature=0.7,
)


def planner_node(state: JARVISState) -> dict:
    """Classify the request and create a plan for tasks."""

    classifier_prompt= """
    You are an intent classifier. Reply with ONLY one word:
    - chat: conversation or information requests
    - task: requests to perform actions, such as opening apps,
      searching, taking screenshots, or creating files.
    """

    response=llm.invoke([
        SystemMessage(content=classifier_prompt),
        HumanMessage(content=state["user_input"]),
    ])

    intent=str(response.content).strip().lower()

    if intent not in ("chat", "task"):
        intent = "chat"

    plan=""

    if intent=="task":
        plan_prompt=(
            f"The user wants to: {state['user_input']}\n"
            "List the steps needed in ONE short sentence. "
            "Do not execute anything."
        )

        plan_response=llm.invoke([
            HumanMessage(content=plan_prompt)
        ])
        plan=str(plan_response.content).strip()

    return {
        "intent": intent,
        "plan": plan,
    }


def chat_node(state:JARVISState) -> dict:
    """Answer the user using the available conversation history."""

    messages=[
        SystemMessage(
            content=(
                "You are JARVIS, a friendly and intelligent AI "
                "desktop companion. Keep answers concise but helpful."
            )
        ),
        *state["messages"],
    ]

    response=llm.invoke(messages)

    return{
        "final_reply": str(response.content).strip(),
    }


def safety_node(state: JARVISState) -> dict:
    """Review the proposed task plan before any execution."""

    safety_prompt = f"""
    Review this plan:
    {state["plan"]}

    Original user request:
    {state["user_input"]}

    Assess whether the plan is appropriate for a Windows desktop
    assistant. Reject destructive file operations, credential theft,
    unauthorized access, exposure of private data, and risky system
    changes.

    Reply with ONLY: safe OR unsafe.
    """

    response = llm.invoke([
        HumanMessage(content=safety_prompt)
    ])

    verdict = str(response.content).strip().lower()
    safe_to_run = verdict == "safe"

    if safe_to_run:
        final_reply = (
            f"I understand! Here's my plan:\n{state['plan']}\n\n"
            "(Desktop execution coming in Phase 9! 🚀)"
        )
    else:
        final_reply = (
            "I can't do that because it might be unsafe or isn't "
            "allowed. Please rephrase what you need!"
        )

    return {
        "safe_to_run": safe_to_run,
        "final_reply": final_reply,
    }


def route_after_planner(state: JARVISState) -> str:
    """Route the workflow according to the detected intent."""

    if state["intent"] == "task":
        return "safety"

    return "chat"
