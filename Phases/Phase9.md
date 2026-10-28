# 🗺️ Phase 9 — Guide Mode (Screen-Aware Step-by-Step Help)

> **Stop after this phase and tell me "Phase 9 done!" when finished!**

---

## 🎯 Goal

Give JARVIS the ability to **see your screen** and **guide you step by step**
through any task — like having an expert sitting next to you.

By the end of this phase:
- JARVIS takes a screenshot when you ask for help
- It reads what's on screen using OCR (Optical Character Recognition)
- It understands which app is open and what you're doing
- It gives you numbered steps tailored to what it actually sees
- The avatar narrates while guiding (thinking → speaking → happy)

---

## 🤔 What Is Guide Mode?

Guide Mode is JARVIS's "eyes". Instead of you describing what's on screen,
JARVIS takes a screenshot and reads it directly.

**Example conversation:**

```
You:    "JARVIS, I'm trying to set up a virtual environment in VS Code but I'm stuck"
JARVIS: [takes screenshot]
JARVIS: [reads screen using OCR → sees VS Code open with a terminal]
JARVIS: "I can see VS Code is open with a terminal panel.
         Here's what to do:
         1. In the terminal, type: python -m venv .venv
         2. Press Enter and wait for it to finish
         3. Then type: .venv\Scripts\activate
         4. You should see (.venv) appear in the terminal prompt"
Avatar: speaking 💬
```

---

## 🏗️ Architecture

```
User: "Help me with this"
          │
          ▼
  [Screenshot Tool]          ← tools/desktop/screenshot.py (already built!)
  Takes screenshot
          │
          ▼
  [OCR Reader]               ← NEW: reads text from the screenshot
  Extracts all visible text
          │
          ▼
  [Window Detector]          ← NEW: which app is in focus?
  Returns: "VS Code", "Chrome", "File Explorer", etc.
          │
          ▼
  [Guide Agent]              ← NEW LangGraph node
  Sends: screenshot text + window name + user question → LLM
  Returns: numbered step-by-step instructions
          │
          ▼
  JARVIS UI shows steps + Avatar speaks them
```

---

## 🛠️ New Tools To Build

### Tool 1: OCR Reader

```
PSEUDOCODE for tools/desktop/ocr_reader.py:

IMPORTS:
    PIL (Pillow) — for image handling
    pytesseract — for OCR (reading text from images)
    from tools.registry import registry, Tool

def read_screen_text(image_path: str = "") -> str:
    """Read all visible text from the screen or an image file."""

    if image_path:
        # Read from a saved screenshot file
        img = PIL.Image.open(image_path)
    else:
        # Take a fresh screenshot
        img = pyautogui.screenshot()

    # OCR: extract text from the image
    text = pytesseract.image_to_string(img)

    # Clean up whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines[:100])   ← cap at 100 lines for LLM context

registry.register(Tool(
    name="read_screen_text",
    description=(
        "Takes a screenshot and reads all visible text from the screen "
        "using OCR. Returns up to 100 lines of text found on screen. "
        "Use this to understand what the user is currently looking at."
    ),
    func=read_screen_text,
    parameters={
        "image_path": {
            "type": "string",
            "description": "Optional path to a screenshot. Leave empty to take a new one."
        }
    }
))
```

### Tool 2: Active Window Detector

```
PSEUDOCODE for tools/desktop/active_window.py:

IMPORTS:
    pygetwindow OR win32gui (Windows only)
    from tools.registry import registry, Tool

def get_active_window() -> str:
    """Return the title of the currently focused window."""

    Method 1 (pygetwindow — simpler):
        import pygetwindow as gw
        window = gw.getActiveWindow()
        if window:
            return window.title
        return "Unknown"

    Method 2 (win32gui — fallback for Windows):
        import win32gui
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd)

registry.register(Tool(
    name="get_active_window",
    description=(
        "Returns the title of the currently focused window on screen. "
        "Use this to know which application the user has open."
    ),
    func=get_active_window,
    parameters={}
))
```

---

## 🪜 Step-by-Step Instructions

---

### Step 1 — Install Dependencies

```bash
uv add pytesseract pygetwindow
```

**Important for Windows:** Pytesseract needs the Tesseract OCR binary installed.

1. Download from: [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install it (remember the installation path, e.g. `C:\Program Files\Tesseract-OCR\`)
3. Add to your `.env`:
   ```
   TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
   ```

Then in `tools/desktop/ocr_reader.py`, add this at the top:
```python
import os
import pytesseract

tesseract_path = os.getenv("TESSERACT_PATH")
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
```

Verify:
```bash
uv run python -c "import pytesseract; print(pytesseract.get_tesseract_version())"
```

---

### Step 2 — Create `tools/desktop/ocr_reader.py`

Follow the pseudocode above. Key points:
- Import `pyautogui` for fresh screenshots
- Import `PIL.Image` for opening saved images
- Import `pytesseract` for OCR
- Cap the output at 100 lines
- Register with the tool registry

---

### Step 3 — Create `tools/desktop/active_window.py`

Follow the pseudocode above. Use `pygetwindow` (simpler).
If it fails on your system, try `win32gui` (`uv add pywin32`).

---

### Step 4 — Create Guide Agent Node

Create `agents/chat/graph/guide_node.py`:

```
PSEUDOCODE for guide_node(state: JARVISState) -> dict:

IMPORTS:
    import tools  ← triggers tool loading
    from tools.registry import registry
    from langchain_core.messages import HumanMessage, SystemMessage

Steps:
    1. Get the active window name:
       window = registry.call("get_active_window")

    2. Read the screen text:
       screen_text = registry.call("read_screen_text")

    3. Build context for the LLM:
       context = f"""
       Currently active app: {window}

       Text visible on screen:
       {screen_text}

       User's question: {state["user_input"]}
       """

    4. Build messages:
       messages = [
           SystemMessage(content=(
               "You are JARVIS, a helpful desktop assistant. "
               "The user has asked for help. You can see what's on their screen. "
               "Give clear, numbered, step-by-step instructions. "
               "Be specific about what to click, type, or look for. "
               "Keep steps short and actionable. "
               "Reference what you actually see on the screen."
           )),
           HumanMessage(content=context)
       ]

    5. Call LLM:
       response = llm.invoke(messages)

    6. Return:
       {
           "final_reply": response.content,
           "avatar_mood": "speaking",
           "action_history": [*state.get("action_history", []),
               f"Guide Mode: analyzed screen, active app: {window}"]
       }
```

---

### Step 5 — Add Guide Mode Routing

In `agents/chat/graph/nodes.py`, update `route_after_planner`:

```
PSEUDOCODE — update route_after_planner:

Before:
    if intent == "task": return "safety"
    else: return "chat"

After:
    if intent == "task":    return "safety"
    elif intent == "guide": return "guide"
    else:                   return "chat"
```

In `planner_node`, detect guide intent:

```
PSEUDOCODE — update planner_node intent detection:

GUIDE_KEYWORDS = ["help me with", "guide me", "step by step", "how do i",
                  "what should i do", "i'm stuck", "i am stuck", "walk me through"]

After classifying intent:
    if any(kw in user_input.lower() for kw in GUIDE_KEYWORDS):
        intent = "guide"
```

---

### Step 6 — Add Guide Node to Graph

In `agents/chat/graph/graph.py`:

```
PSEUDOCODE — update graph:

Add node:
    from agents.chat.graph.guide_node import guide_node
    graph.add_node("guide", guide_node)

Add edge from planner:
    graph.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "chat":   "chat",
            "safety": "safety",
            "guide":  "guide",   ← NEW
        }
    )

Add guide → END:
    graph.add_edge("guide", END)
```

---

### Step 7 — Add Guide Mode to UI

In `App.jsx`, show a **"Guide Mode"** button above the chat input:

```
PSEUDOCODE — App.jsx addition:

Add a button: "🗺️ Guide Me"

When clicked:
    Send a request to /chat with message:
    "guide: Help me with what I'm currently doing on screen"

When response arrives with avatar_mood === "speaking":
    Show each step on a separate numbered line in the chat bubble
    setAvatarExpression("speaking")
```

---

### Step 8 — Test Guide Mode

```bash
# Test OCR + window detection
uv run python -c "
import tools
from tools.registry import registry

window = registry.call('get_active_window')
print('Active window:', window)

text = registry.call('read_screen_text')
print('Screen text (first 200 chars):')
print(text[:200])
"

# Test full guide flow
uv run python -c "
from agents.chat.graph.graph import jarvis_graph

r = jarvis_graph.invoke({
    'user_input': 'guide: Help me with what I see on screen',
    'messages': [], 'intent': 'chat',
    'plan': '', 'safe_to_run': True, 'final_reply': ''
})
print('Intent:', r['intent'])
print('Reply:', r['final_reply'][:400])
print('Mood:', r.get('avatar_mood', 'unknown'))
"
```

---

### Step 9 — Ruff, Format, Commit

```bash
uv run ruff check .
uv run ruff format .
git add .
git commit -m "Phase 9: Guide Mode — screen-aware step-by-step assistant"
git push
```

---

## 📁 New Files in Phase 9

| File | Purpose |
|------|---------|
| `tools/desktop/ocr_reader.py` | Read text from screen via OCR |
| `tools/desktop/active_window.py` | Detect which app is in focus |
| `agents/chat/graph/guide_node.py` | Guide agent — sees screen, gives steps |
| Updates to `nodes.py` | Add "guide" to intent routing |
| Updates to `graph.py` | Wire guide node into graph |
| Updates to `App.jsx` | "Guide Me" button in UI |

---

## ⚠️ Common Mistakes

| Mistake | Fix |
|---------|-----|
| `pytesseract` throws `tesseract is not installed` | Install Tesseract binary, set TESSERACT_PATH in .env |
| `pygetwindow` returns empty string | Window has no title — use win32gui fallback |
| OCR returns garbage | Screen has icons/images — OCR works best on text-heavy screens |
| Guide gives generic steps, not screen-specific | The screen text context is missing — check OCR is passing output |
| Avatar stays on "thinking" | `avatar_mood` key not set to "speaking" in guide_node return |

---

## ✅ Phase 9 Success Checklist

- [ ] 🟢 `pytesseract` installed + Tesseract binary working
- [ ] 🟢 `read_screen_text` tool returns actual screen content
- [ ] 🟢 `get_active_window` returns the app name
- [ ] 🟢 Guide node gives numbered steps based on screen content
- [ ] 🟢 "guide:" prefix correctly routes to guide node
- [ ] 🟢 Avatar shows "speaking" mood during guide
- [ ] 🟢 "🗺️ Guide Me" button in UI works
- [ ] 🟢 `uv run ruff check .` — zero errors
- [ ] 🟢 Git commit + push done

---

## 🎊 What You Have After Phase 9

JARVIS can now SEE what you're doing and HELP you with it.

This is a genuinely unique feature — not just chatting, but **contextual guidance**:
- You're stuck in VS Code → JARVIS sees VS Code and gives VS Code-specific help
- You're on a website → JARVIS reads the page and gives page-specific steps
- You have an error on screen → JARVIS reads the error text and explains the fix

Combined with the anime avatar narrating the steps — this is the experience
that makes JARVIS feel like a real companion, not just a chatbot.

---

## 🎉 When Done

Tell me **"Phase 9 done!"** and we move to **Phase 10 — Streaming UI** ⚡

In Phase 10, you'll see JARVIS's thinking arrive token by token, just like
you experience with Antigravity. Server-Sent Events (SSE) in FastAPI +
React streaming make this possible.

---

*Phase 9 — Guide Mode*
