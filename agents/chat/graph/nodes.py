import json
import re
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from agents.chat.graph.state import JARVISState
from core.config.settings import AI_MODEL, GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(
    model=AI_MODEL,
    google_api_key=GEMINI_API_KEY,
    temperature=0.7,
)


def planner_node(state: JARVISState) -> dict:
    """Classify the request and create a plan for tasks."""

    classifier_prompt = """
    You are an intent classifier. Reply with ONLY one word:
    - chat: conversation or information requests
    - task: requests to perform actions, such as opening apps,
      searching, taking screenshots, or creating files.
    """

    response = llm.invoke(
        [
            SystemMessage(content=classifier_prompt),
            HumanMessage(content=state["user_input"]),
        ]
    )

    guide_keywords = [
        "help me with",
        "guide me",
        "step by step",
        "how do i",
        "what should i do",
        "i'm stuck",
        "i am stuck",
        "walk me through",
    ]

    intent = str(response.content).strip().lower()

    if any(kw in state["user_input"].lower() for kw in guide_keywords):
        intent = "guide"

    if intent not in ("chat", "task", "guide"):  # include guide as valid
        intent = "chat"

    plan = ""

    if intent == "task":
        plan_prompt = (
            f"The user wants to: {state['user_input']}\n"
            "List the steps needed in ONE short sentence. "
            "Do not execute anything."
        )

        plan_response = llm.invoke([HumanMessage(content=plan_prompt)])
        plan = str(plan_response.content).strip()

    return {
        "intent": intent,
        "plan": plan,
    }


def chat_node(state: JARVISState) -> dict:
    """Answer the user using the available conversation history."""

    messages = [
        SystemMessage(
            content=(
                "You are JARVIS, a friendly and intelligent AI "
                "desktop companion. Keep answers concise but helpful."
            )
        ),
        *state["messages"],
        # Always add user_input as the final message so Gemini has content
        HumanMessage(content=state["user_input"]),
    ]

    response = llm.invoke(messages)

    return {
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

    response = llm.invoke([HumanMessage(content=safety_prompt)])

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
    elif state["intent"] == "guide":
        return "guide"

    return "chat"


def desktop_node(state: JARVISState) -> dict:
    from tools.registry import registry

    history = list(state.get("action_history", []))
    if state.get("blocked", False):
        return {
            "final_reply": "Desktop actions are blocked by safety checks.",
            "action_history": history,
            "avatar_mood": "stuck",
        }
    plan = state.get("plan", state.get("plan_steps", []))
    if not plan:
        return {
            "final_reply": "No plan found. Create a plan before performing desktop actions.",
            "action_history": history,
            "avatar_mood": "stuck",
        }

    try:
        available_tools = registry.list_tools()
    except Exception as exc:
        return {
            "final_reply": f"Could not list desktop tools: {exc}",
            "action_history": history,
            "avatar_mood": "stuck",
        }

    try:
        from agents.llm import get_llm

        llm = get_llm()
        prompt = f"""
You are JARVIS's desktop-action planner.

User request:
{state.get("user_request", "")}

Approved plan:
{json.dumps(plan, ensure_ascii=False)}

Available tools:
{json.dumps(available_tools, ensure_ascii=False, default=str)}

Return ONLY a JSON array in this format:
[
  {{"tool": "tool_name", "args": {{"argument": "value"}}}}
]

Rules:
- Use only tools listed above.
- Use only arguments supported by the selected tool.
- Choose the minimum number of tools needed.
- Do not invent tool names or arguments.
- Do not execute commands or bypass permission checks.
- Return [] if no tool is needed.
"""
        response = llm.invoke(prompt)
        content = getattr(response, "content", response)
        if not isinstance(content, str):
            content = str(content)

    except Exception as exc:
        return {
            "final_reply": f"Could not get a tool plan from the LLM: {exc}",
            "action_history": history,
            "avatar_mood": "stuck",
        }

    try:
        cleaned = re.sub(
            r"^\s*```(?:json)?\s*|\s*```\s*$",
            "",
            content.strip(),
            flags=re.IGNORECASE,
        )
        tool_calls = json.loads(cleaned)

        if not isinstance(tool_calls, list):
            raise ValueError("LLM response must be a JSON array.")

        for call in tool_calls:
            if (
                not isinstance(call, dict)
                or not isinstance(call.get("tool"), str)
                or not isinstance(call.get("args", {}), dict)
            ):
                raise ValueError("Invalid tool-call structure.")

    except (json.JSONDecodeError, ValueError) as exc:
        return {
            "final_reply": f"Could not parse the LLM tool plan: {exc}",
            "action_history": history,
            "avatar_mood": "stuck",
        }

    results: list[dict[str, Any]] = []
    all_succeeded = True

    for call in tool_calls:
        tool_name = call["tool"]
        args = call.get("args", {})

        try:
            current_tools = registry.list_tools()
            allowed_names = {
                item if isinstance(item, str) else item.get("name") for item in current_tools
            }
            if tool_name not in allowed_names:
                results.append(
                    {
                        "tool": tool_name,
                        "success": False,
                        "result": "Tool is not registered.",
                    }
                )
                history.append(f"Rejected unregistered tool: {tool_name}")
                all_succeeded = False
                continue
        except Exception as exc:
            results.append(
                {
                    "tool": tool_name,
                    "success": False,
                    "result": f"Could not validate tool: {exc}",
                }
            )
            all_succeeded = False
            break

        permission_request = json.dumps(
            {"tool": tool_name, "args": args},
            ensure_ascii=False,
        )

        approved_request = state.get("approved_desktop_action", "")
        if approved_request != permission_request:
            results.append(
                {
                    "tool": tool_name,
                    "success": False,
                    "result": "Awaiting explicit user approval.",
                }
            )
            history.append(f"Approval required for desktop action: {tool_name}")

            return {
                "pending_permission": permission_request,
                "final_reply": (
                    f"JARVIS wants to use '{tool_name}'. "
                    "Review the action and approve it before execution."
                ),
                "action_history": history,
                "avatar_mood": "thinking",
            }

        try:
            result = registry.call(tool_name, **args)
            results.append(
                {
                    "tool": tool_name,
                    "success": True,
                    "result": str(result),
                }
            )
            history.append(f"Executed {tool_name}: {result}")

        except Exception as exc:
            results.append(
                {
                    "tool": tool_name,
                    "success": False,
                    "result": str(exc),
                }
            )
            history.append(f"Tool failed ({tool_name}): {exc}")
            all_succeeded = False

    if not tool_calls:
        summary = "No desktop actions were needed."
    else:
        summary_lines = ["Desktop action results:"]
        for item in results:
            status = "SUCCESS" if item["success"] else "FAILED"
            summary_lines.append(f"- {item['tool']}: {status} — {item['result']}")
        summary = "\n".join(summary_lines)

    all_succeeded = all_succeeded and all(item["success"] for item in results)

    return {
        "final_reply": summary,
        "action_history": history,
        "avatar_mood": "happy" if all_succeeded else "stuck",
        "pending_permission": "",
    }


def guide_node(state: JARVISState) -> dict:
    """Read screen content and give numbered step-by-step guidance."""
    from tools.registry import registry

    window = registry.call("get_active_window")
    screen_text = registry.call("read_screen_text")

    context = (
        f"Currently active app: {window}\n\n"
        f"Text visible on screen:\n{screen_text}\n\n"
        f"User's question: {state['user_input']}"
    )

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
        "final_reply": str(response.content).strip(),
        "avatar_mood": "speaking",
        "action_history": [
            *state.get("action_history", []),
            f"Guide Mode: analysed screen, active app: {window}",
        ],
    }
