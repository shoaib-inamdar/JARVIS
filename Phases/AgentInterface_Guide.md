# 🤖 How JARVIS Will Work Like Antigravity — The Agent Interface Guide

> You asked: "I want this same chat interface — file changes, line edits,
> what thinking the agent is performing."
>
> This guide explains what that interface is, how it works, why JARVIS can't
> do it yet, and exactly which phases will add each piece of it.

---

## 🔍 What You're Describing — The "Agent IDE" Interface

When you work with Antigravity (this tool), it does several things that feel
like magic:

| What You See | What's Actually Happening |
|---|---|
| 💭 Thinking shown | The model's reasoning is streamed live before the answer |
| 📁 File shown being edited | A tool call to `view_file` reads the file, you see it |
| ✏️ Diff shown | A tool call to `replace_file_content` applies a patch and shows what changed |
| 🔧 Command run | A tool call to `run_command` executes it and streams output |
| 📋 Plan created | The model outlines steps before doing them |
| ✅ Verified | Ruff/tests run after edits, result shown |

This is called an **agentic coding loop**:

```
Read context → Think → Plan → Act (tool call) → Observe result → Think → Act → ...
```

Every "action" is a **tool call** — a structured JSON the model outputs, which
the runtime intercepts and executes.

---

## 🤔 Why Can't JARVIS Do This Yet?

Right now JARVIS's Coding Mode does:
```
User types request → Graph runs → Final reply text returned
```

It **cannot** yet:
- Show its thinking live
- Show file diffs in the UI
- Actually apply changes to files with visible confirmation
- Stream output token by token
- Loop: act → observe → act again

The gap is not in the agent logic (that's built!) — it's in the **UI and
the execution loop**.

---

## 🏗️ What We Need To Build

### 1. Streaming Output (so you see thinking live)
- FastAPI sends Server-Sent Events (SSE) instead of one JSON blob
- React reads the stream and renders each token as it arrives
- Avatar animates while thinking

### 2. Tool Call Visibility (so you see what JARVIS is doing)
- Each tool call (read_file, apply_patch, run_command) shows as a card in the UI
- Like: `🔧 Running: uv run ruff check agents/coding/tools.py`

### 3. Apply Patches (so JARVIS can actually edit files)
- The coding agent proposes a diff
- The diff is shown in the UI with green/red coloring
- You click ✅ Accept or ❌ Reject
- Only then does `apply_patch()` actually write to disk

### 4. Action Transparency Panel
- A side panel or expandable section showing:
  - Current plan step
  - Files read
  - Commands run
  - Verification status

### 5. The Agentic Loop
- Instead of one-shot: input → graph → output
- Becomes: input → step → show step → ask continue? → next step → ...

---

## 📅 When Does Each Piece Get Built?

| Phase | What Gets Added | Antigravity Feature Unlocked |
|-------|----------------|------------------------------|
| **9** | Guide Mode (screen reading) | Avatar watches screen, narrates |
| **10** | Streaming API (SSE) | See tokens arrive live, like me |
| **11** | Diff UI in React | See file changes before approval |
| **12** | Full agentic loop | JARVIS loops: act → observe → act |
| **13** | Action panel in UI | See every tool call with status |
| **14** | Voice | Speak requests, hear replies |

---

## 🛠️ The Technical Architecture (Simple Version)

```
You type: "Fix the bug in server.py line 42"
                    │
                    ▼
         FastAPI /coding/stream endpoint
         (sends Server-Sent Events, not JSON)
                    │
      ┌─────────────┴─────────────────┐
      │ Event 1: "thinking"           │  ← Avatar shows thinking face
      │ Event 2: "step: Read server.py│  ← Tool card appears in UI
      │ Event 3: "diff: ..."          │  ← Diff card with Accept/Reject
      │ Event 4: "waiting"            │  ← Pause for your approval
      └───────────────────────────────┘
                    │
             You click Accept
                    │
      ┌─────────────┴─────────────────┐
      │ Event 5: "applying patch"     │  ← File written to disk
      │ Event 6: "running lint"       │  ← ruff runs
      │ Event 7: "verified: pass ✅"  │  ← Green badge
      │ Event 8: "done"               │  ← Avatar happy
      └───────────────────────────────┘
```

---

## 💡 How JARVIS Will Actually Edit Files

This is the key thing to understand: **right now JARVIS can only suggest code**.
Here's why and how we fix it:

### Why It Can't Edit Yet

In the current Coding Mode:
- `code_node` reads files and builds context ✅
- `code_node` calls the LLM to plan a fix ✅
- But the LLM returns text — it's not wired to call `apply_patch()` ❌

The LLM needs to be given `apply_patch` as a **LangChain tool** it can invoke,
not just a Python function.

### How We'll Fix It (Phase 12)

```python
# Phase 12: Give the LLM actual tools to call

from langchain_core.tools import tool

@tool
def apply_patch(path: str, old_text: str, new_text: str) -> str:
    """Apply a code change to a file. Shows diff and waits for approval."""
    # ... show diff in UI, wait for user confirm, then write

# Bind tools to LLM so it can call them
llm_with_tools = llm.bind_tools([apply_patch, read_file, run_command])
```

When you bind tools to the LLM:
- The LLM outputs structured JSON: `{"tool": "apply_patch", "args": {...}}`
- LangGraph intercepts and runs the tool
- Result goes back to the LLM for the next step
- This is exactly the agentic loop

---

## 🔁 The Full Agentic Loop (Phase 12)

```
PSEUDOCODE for the agentic coding loop:

state = initial_state

while not done:
    # LLM decides what to do next
    response = llm_with_tools.invoke(state["messages"])

    if response has tool_calls:
        for tool_call in response.tool_calls:

            # Show in UI
            stream_event("tool_call", tool_call.name, tool_call.args)

            # If risky: pause and ask user
            if needs_approval(tool_call):
                stream_event("waiting_approval", tool_call)
                approval = wait_for_user_input()
                if not approval:
                    continue

            # Execute
            result = tools[tool_call.name](**tool_call.args)

            # Show result
            stream_event("tool_result", result)

            # Add to conversation so LLM sees what happened
            state["messages"].append(tool_result_message(result))

    else:
        # LLM gave a final answer, no more tool calls
        stream_event("done", response.content)
        done = True
```

This is exactly how Antigravity works internally — and it's exactly what
Phase 12 will build into JARVIS.

---

## 📋 What You Can Do Right Now

Even without the full UI, JARVIS Coding Mode works **in the terminal**.

Here's how to use it as a coding assistant today:

### Ask JARVIS to explain code
```bash
uv run python -c "
from agents.coding.graph import coding_graph

r = coding_graph.invoke({
    'user_request': 'Explain what server.py does and how the /chat endpoint works',
    'current_mode': 'coding', 'project_root': '.',
    'relevant_files': [], 'open_file': 'apps/desktop/backend/server.py',
    'error_context': '', 'plan_steps': [], 'current_step': 0,
    'plan_approved': True, 'proposed_path': '', 'patch_approved': False,
    'action_history': [], 'test_results': '', 'list_results': '',
    'verified': False, 'pending_permission': '', 'safety_flags': [],
    'blocked': False, 'final_reply': '', 'avatar_mood': 'thinking'
})
print(r['final_reply'])
"
```

### Ask JARVIS to find a bug
```bash
# Change user_request to:
# "Find any bugs or issues in agents/coding/tools.py"
```

### Use the API (when server is running)
```bash
curl -X POST http://localhost:8000/coding \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Explain main.py\", \"project_root\": \".\"}"
```

---

## 🔮 The Vision — JARVIS As Your Personal Antigravity

By Phase 14 (end of the main roadmap), JARVIS will:

1. You say: **"JARVIS, add a new API endpoint for getting user history"**
2. JARVIS reads the project rules (JARVIS.md)
3. JARVIS reads `server.py` and `models.py`
4. JARVIS shows its thinking: *"I'll add a GET /chat/history endpoint..."*
5. JARVIS shows the diff in the UI with line highlights
6. You click **Accept**
7. File is written, ruff runs, tests run
8. JARVIS: **"Done! The endpoint is at GET /chat/history. All tests pass."** 😊

That's the goal. You're building it phase by phase — and you're almost halfway there.

---

*Agent Interface Guide — After Phase 8*
