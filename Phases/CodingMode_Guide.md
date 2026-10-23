# 🧠 JARVIS Coding Mode — Capability Guide

> What can you build with it? How do you use it? How strong is it?
> Read this once — then you'll know exactly what to expect.

---

## ✅ What Can JARVIS Coding Mode Do RIGHT NOW?

Even with the MVP you just built, JARVIS can:

| Task | Example |
|------|---------|
| **Explain code** | "Explain what server.py does" |
| **Find bugs** | "Find where the CORS error is coming from" |
| **Plan a refactor** | "How would I split agents/chat into smaller modules?" |
| **Lint and verify** | Runs ruff automatically after every change |
| **Remember context** | Saves task history in `.jarvis/memory.json` |
| **Block dangerous commands** | `rm -rf`, `format c:` are always blocked |
| **Read project rules** | Follows your JARVIS.md before every task |

---

## 🏗️ Apps and Websites You Can Build With It

### 🟢 Beginner Level — JARVIS helps you write from scratch

| Project | How JARVIS helps |
|---------|-----------------|
| **To-do list app** (HTML + JS) | Writes the HTML, JS, and CSS for you |
| **Calculator** | Generates the logic and layout |
| **Weather app** (fetch API) | Writes the fetch call and UI |
| **Personal portfolio site** | Generates pages, styles, and layout |
| **Python number game** | Writes the game loop and input handling |
| **FastAPI Hello World** | Sets up the routes and models |

**How to ask JARVIS:**
```
code: Create a simple weather app in HTML that fetches weather from OpenWeatherMap API
```
JARVIS will: plan → read project rules → write the code → show the diff → lint it

---

### 🟡 Intermediate Level — JARVIS helps you extend and fix

| Project | How JARVIS helps |
|---------|-----------------|
| **React dashboard** | Adds new components, fixes prop errors |
| **FastAPI REST API** | Adds routes, fixes validation errors |
| **Discord bot** (discord.py) | Adds commands, handles events |
| **CLI tool** (Click/Typer) | Adds flags, writes help text |
| **Browser extension** | Writes manifest.json + background scripts |
| **Data analysis script** | Writes pandas/matplotlib code from description |
| **Automated test suite** | Writes pytest tests for existing functions |

**How to ask JARVIS:**
```
code: Add a /users endpoint to apps/desktop/backend/server.py that returns a list of users
code: Fix the TypeError on line 42 of agents/chat/nodes.py
code: Write pytest tests for the read_file function in agents/coding/tools.py
```

---

### 🔴 Advanced Level — JARVIS assists a senior developer

| Project | What JARVIS can do |
|---------|-------------------|
| **Multi-file refactor** | Plans across files, shows diffs one at a time |
| **LangGraph agent** | Writes state, nodes, graph like it did for you |
| **Electron desktop app** | Writes main.cjs, preload, IPC bridge |
| **Database integration** | Writes SQLAlchemy models, alembic migrations |
| **Web scraper** | Writes BeautifulSoup/playwright scraping logic |
| **Custom CLI** | Full Typer/Click app with subcommands |

> ⚠️ At this level JARVIS helps — but you need to understand the output
> and approve every step. It won't magically write a full production app.

---

## 📏 How Strong Is It Compared To Antigravity / Claude Code?

This is an honest comparison:

| Feature | Claude Code / Antigravity | Your JARVIS Coding Mode |
|---------|--------------------------|------------------------|
| **Model intelligence** | ⭐⭐⭐⭐⭐ Frontier models | ⭐⭐⭐ Gemini Flash (free) |
| **Tool quality** | ⭐⭐⭐⭐⭐ Very mature | ⭐⭐⭐ Good MVP |
| **Multi-file edits** | ✅ Native | 🔄 One file at a time (now) |
| **Streaming** | ✅ Live | ❌ Not yet |
| **Terminal execution** | ✅ Full | ✅ With safety blocks |
| **Diff + approval** | ✅ | ✅ |
| **Cost** | 💸 $20+/month | 🆓 Free |
| **Local model support** | ❌ | ✅ (Ollama, Phase 8) |
| **Anime avatar** | ❌ | ✅ 🎭 |
| **You understand every line** | ❌ | ✅ You built it |

**Honest answer:**
- For simple-to-intermediate tasks: **comparable results** with a weaker model
- For complex multi-file production refactors: Claude Code is currently much stronger
- But your harness is solid — swapping in a stronger model (GPT-4o, Claude 3.5 via API) makes it much more competitive
- **The harness you built is what matters.** The model is swappable.

---

## 🤖 How To Use Local LLMs (Ollama)

### Step 1 — Install Ollama

Go to [ollama.com](https://ollama.com) and install for Windows.

### Step 2 — Pull a Coding Model

```bash
# Best free coding models (pick one):
ollama pull qwen2.5-coder:7b      # Best for code — highly recommended
ollama pull deepseek-coder:6.7b   # Very good at debugging
ollama pull codellama:7b           # Meta's coding model
ollama pull llama3.2:3b            # Tiny but fast for routing
```

### Step 3 — Install LangChain Ollama

```bash
uv add langchain-ollama
```

### Step 4 — Update `nodes.py` to Use Ollama

In `agents/coding/nodes.py`, replace the LLM setup:

```python
# BEFORE (Gemini cloud):
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model=AI_MODEL, ...)

# AFTER (Ollama local):
from langchain_ollama import ChatOllama
llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0.2)
```

Or use **both** — Gemini for complex reasoning, Ollama for fast simple tasks:

```python
import os
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

USE_LOCAL = os.getenv("JARVIS_USE_LOCAL", "false").lower() == "true"

if USE_LOCAL:
    llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0.2)
else:
    llm = ChatGoogleGenerativeAI(model=AI_MODEL, google_api_key=GEMINI_API_KEY, temperature=0.2)
```

Set in `.env`:
```
JARVIS_USE_LOCAL=true   # use Ollama
JARVIS_USE_LOCAL=false  # use Gemini (default)
```

### Which Model For Which Task?

| Task | Best Local Model | Why |
|------|-----------------|-----|
| Write new code | `qwen2.5-coder:7b` | Trained specifically on code |
| Fix a bug | `deepseek-coder:6.7b` | Great at debugging reasoning |
| Explain code | `llama3.2:3b` | Fast, good at explanations |
| Routing/planning | `llama3.2:3b` | Tiny but sufficient |
| Complex multi-file | Gemini Flash (cloud) | Needs more context window |

---

## 💡 Simple Steps — How To Actually Use It

### Method 1: Python script (right now, works today)

```bash
uv run python -c "
from agents.coding.graph import coding_graph

result = coding_graph.invoke({
    'user_request': 'Explain what main.py does',
    'current_mode': 'coding',
    'project_root': '.',
    'relevant_files': [], 'open_file': '', 'error_context': '',
    'plan_steps': [], 'current_step': 0, 'plan_approved': True,
    'proposed_path': '', 'patch_approved': False, 'action_history': [],
    'test_results': '', 'list_results': '', 'verified': False,
    'pending_permission': '', 'safety_flags': [], 'blocked': False,
    'final_reply': '', 'avatar_mood': 'thinking'
})
print(result['final_reply'])
"
```

### Method 2: FastAPI endpoint (coming in Phase 8)

```bash
# Start server
uv run python main.py --server

# Send a coding request
curl -X POST http://localhost:8000/coding \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain agents/chat/agent.py", "project_root": "."}'
```

### Method 3: JARVIS UI chat (Phase 9)

Type in the UI chat box:
```
code: Fix the bug in server.py line 42
```
JARVIS will detect "code:" prefix → route to Coding Mode → show avatar in "thinking" state → return the plan

---

## 🛣️ What We're Adding Next (The Roadmap)

| Phase | Feature | What It Unlocks |
|-------|---------|----------------|
| **8** | Laya Tool Registry | JARVIS can open apps, search the web, take screenshots |
| **9** | Desktop Automation | "Open Chrome", "Take a screenshot", "Click that button" |
| **10** | Guide Mode | JARVIS watches your screen and gives step-by-step help |
| **11** | Voice | Talk to JARVIS, hear replies with a custom voice |
| **12** | Memory + Learning | Remembers your preferences across sessions |

---

## 🔮 My Suggestions For You

**1. Upgrade the coding model first (biggest impact)**
Once you want JARVIS to actually apply patches (not just plan), use
`qwen2.5-coder:7b` locally — it's free, fast, and trained specifically on code.

**2. Add "code:" prefix routing to the UI**
In `App.jsx`, detect messages starting with `"code:"` and route them to `/coding`
instead of `/chat`. Makes the mode feel seamless.

**3. Add the Verifier to the UI**
Show a green/red "Verification" badge in the chat when the verifier runs.
Makes JARVIS feel much more trustworthy.

**4. Build something with it!**
The best way to improve your coding agent is to USE it.
Try: `"code: Write a simple snake game in Python using pygame"`

**5. Don't try to match Claude Code immediately**
Build the foundation first (phases 8-12), then iterate.
By Phase 12 with voice + memory + Ollama local models,
you'll have something genuinely impressive.

---

*JARVIS Coding Mode Capability Guide — Phase 7*
