# 🧰 Phase 8 — Laya Tool Registry & Desktop Automation

> **Stop after this phase and tell me "Phase 8 done!" when finished!**

---

## 🎯 Goal

Give JARVIS the ability to **do things on your computer**, not just talk about them.

By the end of this phase:
- JARVIS can open applications (Chrome, Notepad, VS Code)
- JARVIS can take screenshots and describe what's on screen
- JARVIS can search the web and return results
- Every action is registered as a **Laya Tool** — adding a new ability = creating one file
- All actions go through the Safety Agent (no surprises)

---

## 🤔 What Is Laya?

**Laya** is an open-source Python tool registry designed for AI agents.

Think of it as a **plugin system for JARVIS**:
- Each tool = one Python function with a name, description, and schema
- The AI reads the description to know when to use it
- Laya handles the registration, discovery, and calling of tools
- You add a new JARVIS ability by dropping a new file into `tools/`

Compared to writing raw tool calls:

| Without Laya | With Laya |
|-------------|----------|
| Tools scattered across files | All tools in `tools/` folder |
| Agent must know exact tool names | Agent reads descriptions, picks automatically |
| Hard to add new tools | Drop a file → tool is auto-registered |
| No schema validation | Laya validates inputs/outputs |

---

## 🏗️ Architecture After Phase 8

```
User: "Open Chrome and search for Python tutorials"
            │
            ▼
     [Planner Agent]
      intent = "task"
      plan = ["Open Chrome", "Search Python tutorials"]
            │
            ▼
     [Safety Agent]
      "Both steps are safe"
            │
            ▼
     [Desktop Agent]  ← NEW in Phase 8
      Laya Tool: open_app("chrome")
      Laya Tool: web_search("Python tutorials")
            │
            ▼
     [Verifier Agent]
      Screenshot confirms Chrome opened ✅
            │
            ▼
     JARVIS reply: "Done! Chrome is open and I searched for Python tutorials."
     Avatar: happy 😊
```

---

## 🛠️ The Tool Registry Design

```
JARVIS/
└── tools/                    ← NEW folder
    ├── __init__.py            ← auto-discovers all tools
    ├── registry.py            ← Laya registry setup
    ├── desktop/
    │   ├── open_app.py        ← open any Windows app
    │   ├── screenshot.py      ← take and save a screenshot
    │   └── type_text.py       ← type text into a window
    └── web/
        ├── web_search.py      ← search DuckDuckGo (free, no API key)
        └── open_url.py        ← open a URL in the browser
```

Every tool file follows the same 3-part pattern:
1. A Python function that does the work
2. A `ToolSchema` that describes it in English
3. Registration with the Laya registry

---

## 🪜 Step-by-Step Instructions

---

### Step 1 — Install Dependencies

```bash
uv add pyautogui pillow duckduckgo-search psutil
```

- `pyautogui` — control mouse and keyboard, take screenshots
- `pillow` — image handling for screenshots
- `duckduckgo-search` — free web search, no API key needed
- `psutil` — list and check running processes

Verify:
```bash
uv run python -c "import pyautogui, PIL, duckduckgo_search, psutil; print('All good!')"
```

---

### Step 2 — Create `tools/registry.py`

```
PSEUDOCODE for tools/registry.py:

IMPORTS:
    dataclasses, typing, logging

@dataclass
class Tool:
    name:        str    # snake_case identifier e.g. "open_app"
    description: str    # plain English for the AI to understand
    func:        callable  # the actual Python function to run
    parameters:  dict   # JSON Schema of the function's inputs

class ToolRegistry:

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list_tools(self) -> list[dict]:
        """Return a list of {name, description} for the AI to read."""
        return [
            {"name": t.name, "description": t.description}
            for t in self._tools.values()
        ]

    def call(self, name: str, **kwargs) -> str:
        tool = self.get(name)
        if tool is None:
            return f"ERROR: Tool '{name}' not found"
        try:
            result = tool.func(**kwargs)
            return str(result)
        except Exception as exc:
            return f"ERROR: {exc}"

# Singleton — imported everywhere
registry = ToolRegistry()
```

---

### Step 3 — Create `tools/__init__.py`

This file auto-discovers and registers all tools:

```
PSEUDOCODE for tools/__init__.py:

IMPORTS:
    importlib, pkgutil, pathlib, logging

def load_all_tools() -> None:
    """Walk every sub-module in the tools/ folder and import it.
    Each module is expected to call registry.register() at import time.
    """
    tools_dir = Path(__file__).parent

    For each .py file found recursively in tools_dir:
        Skip __init__.py and registry.py
        Build the dotted module path: "tools.desktop.open_app"
        importlib.import_module(module_path)
        log: "Loaded tool: {module_path}"

load_all_tools()
```

---

### Step 4 — Create `tools/desktop/open_app.py`

```
PSEUDOCODE for tools/desktop/open_app.py:

IMPORTS:
    subprocess, psutil, shutil
    from tools.registry import registry, Tool

KNOWN_APPS = {
    "chrome":   ["chrome", "google-chrome", "chrome.exe"],
    "firefox":  ["firefox", "firefox.exe"],
    "notepad":  ["notepad", "notepad.exe"],
    "vscode":   ["code", "code.exe"],
    "explorer": ["explorer", "explorer.exe"],
    "terminal": ["wt", "cmd.exe", "powershell.exe"],
}

def open_app(app_name: str) -> str:
    name_lower = app_name.lower().strip()

    candidates = KNOWN_APPS.get(name_lower, [name_lower])

    For candidate in candidates:
        executable = shutil.which(candidate)
        if executable:
            subprocess.Popen([executable])
            return f"Opened {app_name} successfully."

    return f"ERROR: Could not find '{app_name}'. Is it installed?"

# Register with Laya
registry.register(Tool(
    name="open_app",
    description=(
        "Opens an application on the Windows desktop. "
        "Supported: chrome, firefox, notepad, vscode, explorer, terminal. "
        "Pass the app name as a string."
    ),
    func=open_app,
    parameters={
        "app_name": {"type": "string", "description": "Name of the app to open"}
    }
))
```

---

### Step 5 — Create `tools/desktop/screenshot.py`

```
PSEUDOCODE for tools/desktop/screenshot.py:

IMPORTS:
    pyautogui, pathlib, datetime
    from tools.registry import registry, Tool

SCREENSHOT_DIR = Path(".jarvis") / "screenshots"

def take_screenshot(label: str = "") -> str:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{label or 'screenshot'}.png"
    path = SCREENSHOT_DIR / filename

    screenshot = pyautogui.screenshot()
    screenshot.save(str(path))

    return f"Screenshot saved: {path}"

registry.register(Tool(
    name="take_screenshot",
    description=(
        "Takes a screenshot of the entire screen and saves it. "
        "Returns the file path. Use to verify what is on screen."
    ),
    func=take_screenshot,
    parameters={
        "label": {"type": "string", "description": "Optional label for the filename"}
    }
))
```

---

### Step 6 — Create `tools/web/web_search.py`

```
PSEUDOCODE for tools/web/web_search.py:

IMPORTS:
    from duckduckgo_search import DDGS
    from tools.registry import registry, Tool

def web_search(query: str, max_results: int = 5) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return "No results found."

        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(
                f"{i}. {r['title']}\n   {r['href']}\n   {r['body'][:200]}"
            )

        return "\n\n".join(formatted)

    except Exception as exc:
        return f"Search error: {exc}"

registry.register(Tool(
    name="web_search",
    description=(
        "Searches the web using DuckDuckGo (no API key needed). "
        "Returns title, URL, and a short description for each result. "
        "Use for factual questions or finding resources."
    ),
    func=web_search,
    parameters={
        "query":       {"type": "string",  "description": "What to search for"},
        "max_results": {"type": "integer", "description": "Number of results (default 5)"}
    }
))
```

---

### Step 7 — Add a Desktop Agent Node

Add a new node `desktop_node` to the existing multi-agent graph in
`agents/chat/graph/nodes.py`:

```
PSEUDOCODE for desktop_node(state: JARVISState) -> dict:

IMPORTS:
    import tools   ← this triggers load_all_tools() automatically
    from tools.registry import registry

Steps:
    1. Get the plan steps from state["plan"]
    2. Build a list of available tools: registry.list_tools()
    3. Ask the LLM:
       "You have these tools available: {tools_list}
        The user's plan is: {state['plan']}
        Which tool(s) should you call, and with what arguments?
        Reply as JSON: [{'tool': 'open_app', 'args': {'app_name': 'chrome'}}]"
    4. Parse the LLM's JSON response
    5. For each tool call:
       a. Send to Safety Agent first (via state["pending_permission"])
       b. If approved: result = registry.call(tool_name, **args)
       c. Append result to action_history
    6. Build a summary reply
    7. Return: {
           "final_reply": summary,
           "action_history": [...],
           "avatar_mood": "happy" if all succeeded else "stuck"
       }
```

---

### Step 8 — Add Desktop Node to the Graph

In `agents/chat/graph/graph.py`, update the task flow:

```
PSEUDOCODE — update to graph.py:

Before:
    safety → END

After:
    safety → desktop_node → verifier → END

New edges:
    graph.add_node("desktop", desktop_node)
    graph.add_edge("safety", "desktop")
    graph.add_edge("desktop", "verifier")
    graph.add_edge("verifier", END)
```

---

### Step 9 — Test the Tools Directly

Test each tool without the graph first:

```bash
uv run python -c "
import tools  # loads all tools
from tools.registry import registry

print('Available tools:')
for t in registry.list_tools():
    print(f'  - {t[\"name\"]}: {t[\"description\"][:60]}')

# Test web search
result = registry.call('web_search', query='Python tutorials', max_results=3)
print()
print('Search result:')
print(result[:300])

# Test screenshot
shot = registry.call('take_screenshot', label='test')
print()
print('Screenshot:', shot)
"
```

---

### Step 10 — Test Full Graph With a Task

```bash
uv run python -c "
from agents.chat.graph.graph import jarvis_graph

r = jarvis_graph.invoke({
    'user_input': 'Search the web for Python LangGraph tutorials',
    'messages': [], 'intent': 'chat',
    'plan': '', 'safe_to_run': True, 'final_reply': ''
})

print('Intent:', r['intent'])
print('Reply:', r['final_reply'][:300])
"
```

---

### Step 11 — Ruff, Format, Commit

```bash
uv run ruff check .
uv run ruff format .
git add .
git commit -m "Phase 8: Laya Tool Registry + Desktop automation tools"
git push
```

---

## 📁 New Files in Phase 8

| File | Purpose |
|------|---------|
| `tools/__init__.py` | Auto-discovers and loads all tools |
| `tools/registry.py` | `ToolRegistry` + `Tool` dataclass |
| `tools/desktop/open_app.py` | Open Windows applications |
| `tools/desktop/screenshot.py` | Take desktop screenshots |
| `tools/desktop/type_text.py` | Type text via pyautogui |
| `tools/web/web_search.py` | DuckDuckGo search (no API key) |
| `tools/web/open_url.py` | Open a URL in the browser |

---

## ⚠️ Common Mistakes

| Mistake | Fix |
|---------|-----|
| `pyautogui.screenshot()` fails on Windows | Add `import pyautogui; pyautogui.FAILSAFE = False` |
| `registry.call()` returns ERROR: Tool not found | You forgot `import tools` to trigger load_all_tools |
| DuckDuckGo rate limits | Add `time.sleep(1)` between searches |
| `subprocess.Popen` opens then closes | You need `subprocess.Popen(detach=True)` or `shell=True` on Windows |
| Tool descriptions are too vague | The AI can't pick the right tool — be specific in description |

---

## ✅ Phase 8 Success Checklist

- [ ] 🟢 `uv run python -c "import tools; print('Tools loaded')"` — no errors
- [ ] 🟢 `registry.list_tools()` shows at least 4 tools
- [ ] 🟢 `web_search("Python")` returns real results
- [ ] 🟢 `take_screenshot()` saves a file in `.jarvis/screenshots/`
- [ ] 🟢 `open_app("notepad")` opens Notepad
- [ ] 🟢 Full graph handles task: "Search for Python tutorials"
- [ ] 🟢 `uv run ruff check .` — zero errors
- [ ] 🟢 Git commit + push done

---

## 🎊 What You Have After Phase 8

JARVIS can now **do things** — not just talk.

- 🔍 Search the web in real time
- 📸 See what's on your screen
- 💻 Open apps on command
- 🧰 A clean tool registry where adding new abilities = one new file
- 🛡️ Every action safely checked before execution

---

## 🎉 When Done

Tell me **"Phase 8 done!"** and we move to **Phase 9 — Guide Mode** 🗺️

In Phase 9, JARVIS will watch your screen using screenshots + OCR,
understand what you're working on, and give you step-by-step real-time help.
Think of it as having a pair programmer who can actually see your screen.

---

*Phase 8 — Laya Tool Registry & Desktop Automation*
