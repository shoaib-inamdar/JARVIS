# JARVIS Project Rules

> This file is read by JARVIS Coding Mode at the start of every coding task.
> Keep it updated as the project evolves.

---

## 🏗️ Stack

| Layer | Technology |
|-------|-----------|
| AI Framework | LangGraph + Google Gemini |
| Backend | FastAPI + Uvicorn (Python 3.13) |
| Frontend | React + Vite + Tailwind CSS v4 |
| Desktop shell | Electron (main.cjs) |
| Package manager | `uv` (**not** pip, not poetry) |
| Linter | Ruff |
| Formatter | Ruff |
| Test runner | Pytest |

---

## 📋 Code Style

- Max line length: **100**
- Indent: **4 spaces**
- Quotes: **double**
- Use **type hints** on all functions
- Use **pathlib** (`Path`) instead of `os.path`
- No commented-out code (ruff ERA rule enabled)
- Imports sorted with isort (via ruff `I` rules)

---

## ⚡ Commands

```bash
# Install a package
uv add <package>

# Install dev dependency
uv add --group dev <package>

# Run lint check
uv run ruff check .

# Auto-format
uv run ruff format .

# Run tests
uv run pytest tests/ -v

# Start Python backend
uv run python main.py --server

# Start Electron + Vite dev (from apps/desktop/)
npm start
```

---

## 🚫 Never Do

- ❌ Never use `pip install` — always `uv add`
- ❌ Never delete files without showing the list first
- ❌ Never push directly to `main` — commit to a feature branch
- ❌ Never use `os.system()` — use `subprocess.run()` instead
- ❌ Never hardcode the API key — it lives in `.env`
- ❌ Never import from `apps/desktop/` in Python code
- ❌ Never run `npm install` inside the project root — only inside `apps/desktop/`

---

## 📁 Project Structure

```
JARVIS/
├── agents/          ← Python AI agents
│   ├── chat/        ← Phase 2: ChatAgent
│   ├── graph/       ← Phase 6: LangGraph base graph
│   └── coding/      ← Phase 7: Coding Mode agents
├── apps/
│   └── desktop/     ← Electron + React + Vite frontend
│       ├── electron/
│       ├── public/live2d/   ← Hiyori Live2D model
│       └── src/     ← React components (App.jsx, Avatar.jsx)
├── core/
│   └── config/
│       └── settings.py  ← API keys, model name, config
├── tests/           ← Pytest tests
├── Phases/          ← Walkthrough files for each phase
├── .jarvis/         ← JARVIS memory + global rules
├── JARVIS.md        ← THIS FILE — project rules for Coding Mode
└── walkthrough.md   ← Full beginner guide
```

---

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `core/config/settings.py` | All configuration (model name, API key) |
| `main.py` | Entry point — terminal mode or server mode |
| `agents/chat/agent.py` | Phase 2 ChatAgent |
| `apps/desktop/src/App.jsx` | Main React UI |
| `apps/desktop/src/Avatar.jsx` | Live2D anime avatar |
| `apps/desktop/electron/main.cjs` | Electron window creation |
| `.env` | Secrets (never commit!) |

---

## 🤖 AI Model

- Current model: `gemini-2.5-flash` (via `core/config/settings.py`)
- Change model in settings.py `AI_MODEL` variable
- API key: `GEMINI_API_KEY` in `.env`

---

*Last updated: Phase 7*
