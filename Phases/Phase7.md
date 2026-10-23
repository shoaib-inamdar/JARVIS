# 🖥️ Phase 7 — JARVIS Coding Mode

> This is the most powerful phase in the project. Read everything carefully before you start.
> **Stop after this phase and tell me "Phase 7 done!" when finished!**

---

## 🎯 Goal

Add a **Coding Mode** to JARVIS — a specialised multi-agent system that can:

- Read, write, and edit files safely
- Run terminal commands with your permission
- Fix bugs, explain code, add features, write tests
- Work with **free or local LLMs** (no paid Claude or GPT-4 required)
- Narrate every action through the JARVIS avatar

Think of it as your own personal junior-to-mid developer living inside JARVIS,
who asks permission before touching anything important and shows their work.

---

## 🤔 Should You Build This? (Yes — Here's Why)

Coding agents get their power from TWO things:
1. The language model (brain)
2. The **harness** — the tools, loop, planning, verification, and safety layer

Research by Anthropic, Google, and Stanford shows the **harness often matters as
much as the model**. A great harness with a free local model can outperform a
weak harness with an expensive one. That's exactly what you're going to build.

**Free/local model strategy:**
- Default: `Gemini 2.5 Flash` (free tier) — fast, good at code
- Local fallback: `Ollama` with `qwen2.5-coder:7b` or `deepseek-coder:6.7b`
- Router: small tasks → local, complex reasoning → Gemini free

---

## 🏗️ Architecture Overview

```
User request: "Fix the bug in server.py line 42"
                        │
                        ▼
              ┌─────────────────┐
              │  Planner Agent  │  Reads files, understands context,
              │                 │  makes a step-by-step plan
              └────────┬────────┘
                       │ plan approved by user?
                       ▼
              ┌─────────────────┐
              │   Code Agent    │  Reads/edits files, proposes patches
              └────────┬────────┘
                       │ needs terminal?
                  ┌────┴────┐
                  │         │
                  ▼         ▼
         ┌──────────┐  ┌──────────┐
         │ Terminal │  │ Safety   │  Permission check before
         │  Agent   │  │  Agent   │  any destructive command
         └────┬─────┘  └──────────┘
              │
              ▼
     ┌─────────────────┐
     │ Verifier Agent  │  Runs tests / lint / diff check
     └────────┬────────┘
              │ success?
              ▼
     ┌─────────────────┐
     │  Memory Agent   │  Saves what worked, what failed,
     │                 │  user preferences, project rules
     └────────┬────────┘
              │
              ▼
       JARVIS Avatar narrates the result 🎭
```

---

## 🧠 Shared State (The Whiteboard)

```
PSEUDOCODE — agents/graph/coding_state.py:

class CodingState(TypedDict):

    # ── Request ──────────────────────────────────────
    user_request:   str    # What the user asked for
    current_mode:   str    # Always "coding" for this graph

    # ── Context ──────────────────────────────────────
    project_root:   str    # Absolute path to project folder
    relevant_files: list   # List of file paths the agents should look at
    open_file:      str    # Currently active file (from Electron IDE)
    error_context:  str    # Error message / stack trace if fixing a bug

    # ── Planning ─────────────────────────────────────
    plan_steps:     list   # ["Read server.py", "Fix line 42", "Run tests"]
    current_step:   int    # Which step we are on
    plan_approved:  bool   # Did the user confirm the plan?

    # ── Actions ──────────────────────────────────────
    proposed_patch: str    # The diff/edit proposed by Code Agent
    patch_approved: bool   # Did the user confirm the patch?
    action_history: list   # Log of everything done so far

    # ── Verification ─────────────────────────────────
    test_results:   str    # Output from running tests
    lint_results:   str    # Output from ruff/mypy
    verified:       bool   # Did verification pass?

    # ── Safety ───────────────────────────────────────
    pending_permission: str   # Command waiting for user approval
    safety_flags:       list  # List of warnings from Safety Agent
    blocked:            bool  # True = stop everything

    # ── Output ───────────────────────────────────────
    final_reply:    str    # What JARVIS says back to the user
    avatar_mood:    str    # "thinking", "coding", "verifying", "happy", "stuck"
```

---

## 🤖 The Six Agents

### Agent 1: Planner Agent

**Job:** Understand the request, find relevant files, write a step-by-step plan.

```
PSEUDOCODE — planner_node(state):

1. Read the project rules file (JARVIS.md) if it exists
2. Read any files mentioned in user_request or open_file
3. Identify which files are relevant to the task
4. Build a numbered plan:
   "1. Read server.py to understand current code
    2. Identify the bug at line 42
    3. Propose a minimal patch
    4. Run ruff to check syntax
    5. Run tests if available"
5. Set avatar_mood = "thinking"
6. Return: {
       "plan_steps": [...],
       "relevant_files": [...],
       "plan_approved": False  ← wait for user approval
   }
```

**Key rule:** For any task touching more than 1 file OR running a command,
always write a plan first and wait for user confirmation.

---

### Agent 2: Code Agent

**Job:** Read files and propose patches. Never writes directly — always proposes first.

```
PSEUDOCODE — code_node(state):

TOOL: read_file(path) → returns file content
TOOL: search_codebase(query, root) → returns matching lines + file paths
TOOL: propose_patch(file_path, old_text, new_text) → returns unified diff

Steps:
1. Read relevant files using read_file tool
2. Understand the specific problem
3. Think: "What is the smallest change that fixes this?"
4. Generate a unified diff (patch) showing old vs new
5. Set proposed_patch = the diff
6. Set avatar_mood = "coding"
7. Return: {"proposed_patch": diff, "patch_approved": False}
```

**Key rule:** Always show the diff. Never silently overwrite a file.

---

### Agent 3: Terminal Agent

**Job:** Run shell commands — but ONLY after Safety Agent approves.

```
PSEUDOCODE — terminal_node(state):

TOOL: run_command(cmd, cwd, timeout=30) → stdout, stderr, exit_code

Steps:
1. Determine which command is needed (e.g. "uv run ruff check .")
2. Set pending_permission = the command
3. Wait for user confirmation (return state, UI shows "Allow this command?")
4. If approved:
   - Run the command
   - Capture stdout + stderr
   - Add to action_history
5. Return: {"test_results": output, "pending_permission": ""}
```

**Safe commands** (auto-approved): `ruff check`, `ruff format`, `pytest`, `python --version`
**Ask permission**: `pip install`, `uv add`, any file deletion, `git push`
**Always blocked**: `rm -rf`, `format`, `del /f /s`, anything with `sudo`

---

### Agent 4: Safety Agent

**Job:** Review every proposed action before it runs. Block dangerous things.

```
PSEUDOCODE — safety_node(state):

BLOCKLIST = [
    "rm -rf", "del /f /s", "format c:",
    "DROP TABLE", "os.remove", "shutil.rmtree",
    "> /dev/null", "sudo", "passwd"
]

Steps:
1. Check pending_permission against BLOCKLIST
2. Ask LLM: "Is this command safe to run in a coding context?
              Command: {state['pending_permission']}
              Reply: safe / unsafe / ask_user"
3. If "safe":   set blocked=False, allow
4. If "unsafe": set blocked=True, final_reply = "I blocked that — it's too risky."
5. If "ask_user": surface to UI, wait for explicit yes/no
6. Add result to safety_flags
7. Return: {"blocked": ..., "safety_flags": [...]}
```

---

### Agent 5: Verifier Agent

**Job:** After any edit or command, verify the result. Never claim success without checking.

```
PSEUDOCODE — verifier_node(state):

Steps:
1. Run ruff check on changed files → lint_results
2. If tests/ folder exists → run pytest → test_results
3. Otherwise: show the diff and ask user "Does this look correct?"
4. Parse results:
   - ruff: 0 errors = pass
   - pytest: all passed = pass
   - user confirmed = pass
5. Set verified = (all checks passed)
6. Set avatar_mood = "happy" if verified else "stuck"
7. Return: {"verified": ..., "lint_results": ..., "test_results": ...}
```

---

### Agent 6: Memory Agent

**Job:** Remember what worked, what failed, user preferences, project rules.

```
PSEUDOCODE — memory_node(state):

TOOL: read_rules(project_root) → reads JARVIS.md rules
TOOL: save_to_memory(key, value) → writes to .jarvis/memory.json
TOOL: recall(query) → searches .jarvis/memory.json for relevant past info

Steps:
1. Read JARVIS.md project rules at task start
2. After success: save what worked ("Fixed ImportError by adding __init__.py")
3. After failure: save what to avoid ("Running pytest without --no-header crashes")
4. Save user preferences if stated ("User prefers 4-space indent, no semicolons")
5. Return: {"action_history": [updated log]}
```

---

## 🛠️ Tool List

| Tool | What It Does | Permission Level |
|------|-------------|-----------------|
| `read_file(path)` | Read any file as text | Auto-approved |
| `list_files(dir)` | List directory contents | Auto-approved |
| `search_codebase(query, root)` | Grep-style search | Auto-approved |
| `propose_patch(path, old, new)` | Show diff — does NOT write | Auto-approved |
| `apply_patch(path, old, new)` | Actually write the change | **Requires confirmation** |
| `run_command(cmd)` | Run shell command | **Requires confirmation** |
| `run_safe_lint(path)` | Run ruff check only | Auto-approved |
| `run_tests(root)` | Run pytest | Auto-approved |
| `read_rules()` | Read JARVIS.md | Auto-approved |
| `save_memory(key, val)` | Write to .jarvis/memory.json | Auto-approved |

---

## 📋 JARVIS.md — Project Rules File

Create this file in any project you work on with JARVIS.
It tells the Coding Mode how to behave in that specific project:

```markdown
# JARVIS Project Rules

## Stack
- Language: Python 3.13
- Package manager: uv (NOT pip)
- Linter: ruff
- Test runner: pytest

## Code Style
- Max line length: 100
- Use type hints everywhere
- Prefer pathlib over os.path
- No commented-out code

## Commands
- Install package: uv add <package>
- Run tests: uv run pytest tests/ -v
- Check lint: uv run ruff check .
- Format: uv run ruff format .
- Start server: uv run python main.py --server

## Never Do
- Never use pip install
- Never delete files without confirmation
- Never push to main directly
- Never use os.system() — use subprocess instead

## Project Structure
- Backend: apps/desktop/backend/
- Agents: agents/
- Config: core/config/
```

---

## 🔄 Plan → Act → Verify Flow

```
SIMPLE TASK ("fix the syntax error"):
User → Planner reads file → Code Agent proposes patch →
User confirms → patch applied → Verifier runs ruff →
"Fixed!" → Memory saves the fix style

COMPLEX TASK ("refactor the entire auth module"):
User → Planner writes 5-step plan → User confirms plan →
Step 1: Code Agent reads all files → shows summary
Step 2: Code Agent proposes patch for file 1 → User confirms → Apply
Step 3: Code Agent proposes patch for file 2 → User confirms → Apply
Step 4: Terminal Agent runs tests → Verifier checks results
Step 5: Memory Agent saves refactor pattern
"Done! All 5 steps complete, 3 files changed, all tests pass." → avatar happy

RISKY TASK ("delete all __pycache__ folders"):
User → Planner writes plan → Safety Agent flags: "This deletes files" →
"Show me the files first?" → User sees list → User confirms →
Terminal Agent runs with explicit approval → Verifier confirms gone → Done
```

---

## 🤖 Free/Local LLM Strategy

### Default Stack (What To Use)

| Task | Model | Why |
|------|-------|-----|
| Planning + reasoning | `gemini-2.5-flash` (free) | Best free reasoning |
| Simple code edits | `qwen2.5-coder:7b` (local Ollama) | Fast, free, great at code |
| Routing decisions | `gemini-flash-lite` or tiny local | Cheap/fast |
| Verification analysis | `gemini-2.5-flash` (free) | Needs to understand test output |

### How To Keep Prompts Short (For Weak Models)

1. **Never pass the whole file** — pass only the relevant function + 5 lines of context
2. **Use structured output** — ask the model to reply in JSON or a fixed format
3. **One job per prompt** — don't ask a small model to plan AND code at once
4. **Pre-filter with search** — find relevant lines before sending to LLM

### Graceful Degradation

If the local model gives a bad patch:
1. Verifier catches it (ruff fails / tests fail)
2. Falls back to Gemini free for a second attempt
3. If still failing: shows the diff to user and says "I'm stuck — can you review this?"

---

## 📁 Folder Structure

```
JARVIS/
├── agents/
│   ├── chat/
│   │   └── agent.py          ← exists
│   ├── graph/                ← Phase 6 (LangGraph base)
│   │   ├── __init__.py
│   │   ├── state.py
│   │   ├── nodes.py
│   │   └── graph.py
│   └── coding/               ← Phase 7 (NEW)
│       ├── __init__.py
│       ├── coding_state.py   ← CodingState TypedDict
│       ├── tools.py          ← read_file, apply_patch, run_command, etc.
│       ├── nodes.py          ← all 6 agent nodes
│       ├── graph.py          ← builds the coding StateGraph
│       └── rules.py          ← reads JARVIS.md and .jarvis/memory.json
├── .jarvis/
│   ├── memory.json           ← what the Memory Agent saves
│   └── rules.md              ← global coding rules (project-specific goes in JARVIS.md)
└── JARVIS.md                 ← per-project rules (created by user in each project)
```

---

## 🚀 MVP vs Full Version

### MVP (Build This First) ✅

- [ ] `read_file` and `list_files` tools
- [ ] `propose_patch` (show diff, don't apply yet)
- [ ] `apply_patch` with user confirmation in terminal
- [ ] `run_safe_lint` (ruff only, auto-approved)
- [ ] Planner + Code + Verifier agents only (no Terminal/Safety/Memory yet)
- [ ] Coding Mode activated by typing "code: " before your request
- [ ] Avatar mood: thinking / coding / verifying / happy / stuck

### Full Version (Add Later) 🔮

- [ ] Terminal Agent with Safety permission system
- [ ] Memory Agent with `.jarvis/memory.json`
- [ ] JARVIS.md reader
- [ ] Local Ollama model routing
- [ ] Electron UI panel for Coding Mode (show plan, approve steps, see diff)
- [ ] Multi-file refactors
- [ ] Streaming output (see edits happen live)
- [ ] Skill library (reusable playbooks: "add API endpoint", "create React component")

---

## 🪜 Step-by-Step Implementation

---

### Step 1 — Install Dependencies

```
uv add langgraph langchain-google-genai ollama
```

Verify:
```
uv run python -c "import langgraph; print('LangGraph ok')"
```

---

### Step 2 — Create `agents/coding/tools.py`

```
PSEUDOCODE for agents/coding/tools.py:

IMPORTS:
    subprocess, pathlib, json, difflib

─────────────────────────────────────
TOOL: read_file(path: str) → str
─────────────────────────────────────
    file = Path(path)
    if not file.exists(): return "ERROR: File not found"
    if file.stat().st_size > 100_000: return "ERROR: File too large (>100KB)"
    return file.read_text(encoding="utf-8")

─────────────────────────────────────
TOOL: list_files(directory: str, extensions: list = None) → list[str]
─────────────────────────────────────
    root = Path(directory)
    results = []
    For each file in root.rglob("*"):
        Skip: .venv, node_modules, .git, __pycache__, *.egg-info
        If extensions is None OR file.suffix in extensions:
            results.append(str(file))
    return results[:50]   ← cap at 50 files

─────────────────────────────────────
TOOL: search_codebase(query: str, root: str) → str
─────────────────────────────────────
    results = []
    For each .py file in list_files(root, [".py"]):
        content = read_file(file)
        For each line in content.splitlines():
            if query.lower() in line.lower():
                results.append(f"{file}:{line_number}: {line}")
    return "\n".join(results[:30])   ← cap at 30 matches

─────────────────────────────────────
TOOL: propose_patch(path: str, old_text: str, new_text: str) → str
─────────────────────────────────────
    diff = difflib.unified_diff(
        old_text.splitlines(keepends=True),
        new_text.splitlines(keepends=True),
        fromfile=f"a/{path}",
        tofile=f"b/{path}",
    )
    return "".join(diff)   ← returns a readable diff, does NOT write anything

─────────────────────────────────────
TOOL: apply_patch(path: str, old_text: str, new_text: str) → str
─────────────────────────────────────
    file = Path(path)
    current = file.read_text(encoding="utf-8")
    if old_text not in current:
        return "ERROR: Old text not found — file may have changed"
    updated = current.replace(old_text, new_text, 1)
    file.write_text(updated, encoding="utf-8")
    return f"SUCCESS: {path} updated"

─────────────────────────────────────
TOOL: run_safe_lint(path: str) → str
─────────────────────────────────────
    result = subprocess.run(
        ["uv", "run", "ruff", "check", path],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout + result.stderr

─────────────────────────────────────
TOOL: run_tests(root: str) → str
─────────────────────────────────────
    tests_dir = Path(root) / "tests"
    if not tests_dir.exists():
        return "No tests/ folder found"
    result = subprocess.run(
        ["uv", "run", "pytest", "tests/", "-v", "--tb=short"],
        capture_output=True, text=True, timeout=60, cwd=root
    )
    return result.stdout[-3000:]  ← last 3000 chars (tests can be long)

─────────────────────────────────────
TOOL: read_rules(project_root: str) → str
─────────────────────────────────────
    jarvis_md = Path(project_root) / "JARVIS.md"
    if jarvis_md.exists():
        return jarvis_md.read_text(encoding="utf-8")
    return ""  ← no rules file, that's fine
```

---

### Step 3 — Create `agents/coding/coding_state.py`

Write the full `CodingState` TypedDict from the pseudocode in the Architecture section above.

---

### Step 4 — Create `agents/coding/nodes.py`

Write all 6 agent node functions (MVP: just Planner, Code, Verifier).

Use this LLM setup at the top:
```
PSEUDOCODE — LLM setup:

from langchain_google_genai import ChatGoogleGenerativeAI
from core.config.settings import GEMINI_API_KEY, AI_MODEL

llm = ChatGoogleGenerativeAI(
    model=AI_MODEL,
    google_api_key=GEMINI_API_KEY,
    temperature=0.2      ← lower temp for code = more predictable
)
```

---

### Step 5 — Create `agents/coding/graph.py`

```
PSEUDOCODE for agents/coding/graph.py:

from langgraph.graph import StateGraph, END
from .coding_state import CodingState
from .nodes import (
    planner_node, code_node, verifier_node,
    safety_node, terminal_node, memory_node
)

def build_coding_graph():
    g = StateGraph(CodingState)

    g.add_node("planner",  planner_node)
    g.add_node("code",     code_node)
    g.add_node("safety",   safety_node)
    g.add_node("terminal", terminal_node)
    g.add_node("verifier", verifier_node)
    g.add_node("memory",   memory_node)

    g.set_entry_point("planner")

    # After planning → code agent
    g.add_edge("planner", "code")

    # After code proposes patch → check if terminal needed
    g.add_conditional_edges(
        "code",
        route_after_code,    ← returns "terminal" or "verifier"
        {"terminal": "safety", "verifier": "verifier"}
    )

    # Safety check → then actually run terminal
    g.add_edge("safety",   "terminal")
    g.add_edge("terminal", "verifier")

    # Verifier → memory → done
    g.add_edge("verifier", "memory")
    g.add_edge("memory",   END)

    return g.compile()

ROUTER: route_after_code(state) → str:
    If state has a pending_permission (needs terminal):
        return "terminal"
    Else:
        return "verifier"   ← just lint check, no command needed

coding_graph = build_coding_graph()
```

---

### Step 6 — Add Coding Mode to the API

In `server.py`, add a new `/coding` endpoint alongside `/chat`:

```
PSEUDOCODE — new endpoint in server.py:

@app.post("/coding")
async def coding_endpoint(request: CodingRequest):
    initial_state = {
        "user_request": request.message,
        "current_mode": "coding",
        "project_root": request.project_root or ".",
        "relevant_files": [],
        "open_file": request.open_file or "",
        "error_context": request.error_context or "",
        "plan_steps": [],
        "current_step": 0,
        "plan_approved": False,
        "proposed_patch": "",
        "patch_approved": False,
        "action_history": [],
        "test_results": "",
        "lint_results": "",
        "verified": False,
        "pending_permission": "",
        "safety_flags": [],
        "blocked": False,
        "final_reply": "",
        "avatar_mood": "thinking",
    }
    result = coding_graph.invoke(initial_state)
    return {
        "reply":       result["final_reply"],
        "avatar_mood": result["avatar_mood"],
        "plan":        result["plan_steps"],
        "patch":       result["proposed_patch"],
        "verified":    result["verified"],
    }
```

Also add to `models.py`:
```
class CodingRequest(BaseModel):
    message:      str
    project_root: str = "."
    open_file:    str = ""
    error_context: str = ""
```

---

### Step 7 — Wire Avatar Moods to Coding Mode

In `App.jsx`, when a `/coding` response arrives, set the avatar expression:

```
PSEUDOCODE — changes to App.jsx:

When coding response arrives:
    if result.avatar_mood == "thinking":   setAvatarExpression("thinking")
    if result.avatar_mood == "coding":     setAvatarExpression("thinking")
    if result.avatar_mood == "verifying":  setAvatarExpression("thinking")
    if result.avatar_mood == "happy":      setAvatarExpression("happy")
    if result.avatar_mood == "stuck":      setAvatarExpression("speaking")
```

---

### Step 8 — Create a JARVIS.md for This Project

Create `JARVIS.md` in your project root (copy the template from the
Architecture section above and fill it in for the JARVIS project itself).

---

### Step 9 — Test Coding Mode

```
uv run python -c "
from agents.coding.graph import coding_graph

# Test 1: explain code
r = coding_graph.invoke({
    'user_request': 'Explain what agents/chat/agent.py does',
    'current_mode': 'coding',
    'project_root': '.',
    'relevant_files': [], 'open_file': '',
    'error_context': '', 'plan_steps': [],
    'current_step': 0, 'plan_approved': False,
    'proposed_patch': '', 'patch_approved': False,
    'action_history': [], 'test_results': '',
    'lint_results': '', 'verified': False,
    'pending_permission': '', 'safety_flags': [],
    'blocked': False, 'final_reply': '', 'avatar_mood': 'thinking'
})
print('Plan:', r['plan_steps'])
print('Reply:', r['final_reply'])
print('Mood:', r['avatar_mood'])
"
```

---

### Step 10 — Ruff, Format, Commit

```
uv run ruff check .
uv run ruff format .
git add .
git commit -m "Phase 7: Coding Mode - multi-agent coding harness"
git push
```

---

## ⚠️ Risks and How You Avoid Them

| Risk | How JARVIS Handles It |
|------|-----------------------|
| Bad patch breaks working code | `propose_patch` shows diff first, user confirms |
| Runaway terminal command | Safety Agent blocklist + explicit user confirmation |
| Weak model produces garbage | Verifier catches it; falls back to Gemini free |
| Model hallucinates a file path | `read_file` returns "File not found", agent retries |
| Infinite loop between agents | LangGraph `recursion_limit=25` stops it |
| File too large for context | 100KB limit in `read_file`; search instead of reading |
| User loses track of changes | `action_history` keeps full log; avatar narrates each step |

---

## ✅ Phase 7 Success Checklist

- [ ] 🟢 `agents/coding/tools.py` — all 7 tools implemented and tested
- [ ] 🟢 `agents/coding/coding_state.py` — CodingState TypedDict defined
- [ ] 🟢 `agents/coding/nodes.py` — Planner, Code, Verifier nodes working
- [ ] 🟢 `agents/coding/graph.py` — graph compiles without errors
- [ ] 🟢 Test script: "explain agents/chat/agent.py" returns a plan + reply
- [ ] 🟢 `/coding` API endpoint added to server.py
- [ ] 🟢 `JARVIS.md` created at project root
- [ ] 🟢 Avatar mood changes during coding tasks
- [ ] 🟢 `uv run ruff check .` — zero errors
- [ ] 🟢 Git commit + push done

---

## 🎊 What You Have After Phase 7

JARVIS can now help you write and fix code — safely, step by step, with:
- A Planner that thinks before acting
- A Code Agent that proposes (never blindly applies) changes
- A Verifier that catches mistakes before you even see them
- Safety blocks on dangerous commands
- An anime avatar that narrates every step 🎭

You have built something that most professional developers don't have on their machines.

---

## 🎉 When Done

Tell me **"Phase 7 done!"** and we move to **Phase 8 — Laya Tool Registry** 🧰

In Phase 8 you will install Laya and register your first desktop automation tools.
Every action JARVIS can take (open apps, take screenshots, click things) becomes
a Laya tool — adding new abilities = adding one new file.

---

*Phase 7 — JARVIS Coding Mode*
