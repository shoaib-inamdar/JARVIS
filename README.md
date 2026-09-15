<div align="center">

# 🤖 JARVIS
### Just A Rather Very Intelligent System

**An AI-powered anime desktop companion that sees your screen, guides you step-by-step, and does tasks for you — safely.**

[![CI](https://github.com/yourusername/JARVIS/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/JARVIS/actions)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![uv](https://img.shields.io/badge/package%20manager-uv-orange)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## ✨ What Is JARVIS?

JARVIS is an anime-style AI assistant that lives on your Windows desktop.
Unlike a chatbot that only answers questions, JARVIS can:

- 🗣️ **Chat** — Talk to JARVIS naturally with voice or text
- 👆 **Guide** — JARVIS shows you exactly what to click on your real screen
- 🤖 **Act** — With your permission, JARVIS controls your computer to complete tasks
- 📱 **Connect** — Later: JARVIS coordinates between your desktop and phone

---

## 🏗️ Tech Stack

### Core Architecture

| Layer | Technology | Notes |
|-------|------------|-------|
| 🖥️ Desktop App | Electron + React | Transparent overlay window, system tray |
| 🎭 Avatar | Live2D | Anime-style with expressions (thinking, guiding, success, concern) |
| ⚡ Backend | FastAPI + WebSocket | Python backend the Electron frontend talks to |
| 🔗 Agent Orchestration | LangGraph | Multi-agent stateful graph with human-in-the-loop |
| 🛠️ Tool Decision Layer | LangGraph tool calling | Routes JSON tool calls to the right agent |

### AI Brain

| Provider | Role | When |
|----------|------|------|
| Google Gemini 1.5 Flash | Primary LLM | Now (free tier) |
| Groq | Fast backup LLM | If Gemini quota hit |
| Ollama + qwen3:4b | Local model fallback | Phase 15 (when hardware allows) |

### Voice

| Layer | Technology | Why |
|-------|------------|-----|
| 🎤 Speech-to-Text | Whisper (local) | Private, no API cost, runs offline |
| 🔊 Text-to-Speech | Kokoro.js (local) | Fast, free, private — perfect for anime avatar voice |
| 🔊 TTS Premium | ElevenLabs | Optional upgrade for higher quality voice |

### Desktop Control & Automation

| Tool | What It Does |
|------|-------------|
| PyAutoGUI | Mouse, keyboard, screenshots |
| Playwright | Browser automation (click, fill, navigate) |
| Windows APIs | File system, process control, system notifications |
| Screen capture | Screenshot + element detection for Guide Mode |

### Performance Target

> ⚡ **Under 2 seconds round-trip** from user input to JARVIS response.
> This is a hard design goal — critical for Guide Mode and voice conversations to feel natural.

### Data & Memory

| Layer | Technology |
|-------|------------|
| Session memory | In-memory conversation history |
| Long-term memory | SQLite (structured) + ChromaDB (vector search) |
| Secrets | `.env` file + OS secure storage |

### Developer Tooling

| Tool | Purpose |
|------|---------|
| uv | Package manager (fast, dependency-locked) |
| Ruff | Python linter and formatter |
| CodeRabbit | AI code review on every PR |
| GitHub Actions | CI: lint + test on every push |
| pytest | Python test framework |

### Future / Maybe Later

| Technology | Phase | Why |
|------------|-------|-----|
| Android companion app | Phase 14 | Phone-side counterpart for cross-device actions |
| WebSocket in VS Code | Phase 16 | Deep editor integration for developer workflows |

---

## 📁 Project Structure

```
JARVIS/
├── .github/
│   ├── workflows/ci.yml        # Automated CI checks
│   └── CODEOWNERS              # Code ownership rules
├── apps/
│   ├── desktop/                # Electron + React front-end
│   └── companion/              # Future: phone app
├── agents/
│   ├── planner/                # Plans multi-step tasks
│   ├── desktop/                # Controls the desktop
│   ├── safety/                 # Validates all actions
│   ├── memory/                 # Remembers past sessions
│   └── phone/                  # Future: phone actions
├── core/
│   ├── config/                 # Settings and secrets loader
│   ├── models/                 # Shared data models
│   └── utils/                  # Shared helper utilities
├── assets/
│   ├── avatar/                 # Live2D avatar files
│   └── sounds/                 # Sound effects
├── docs/
│   ├── architecture/           # System design docs
│   └── api/                    # API reference notes
├── tests/
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
├── main.py                     # Entry point
├── pyproject.toml              # Project config + dependencies (uv)
├── .ruff.toml                  # Ruff linting config
├── .gitignore                  # Files Git ignores
└── .coderabbit.yaml            # CodeRabbit AI reviewer config
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- Node.js 20+ (LTS)
- [uv](https://github.com/astral-sh/uv) package manager
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/JARVIS.git
cd JARVIS

# Install Python dependencies
uv sync

# Copy environment template and add your API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run JARVIS
uv run python main.py
```

---

## 🛡️ Safety First

JARVIS is designed with a **permission-first** approach:

- Every desktop action requires explicit user approval
- A dedicated Safety Agent validates all plans before execution
- Emergency stop is always available
- No action is irreversible without a clear warning

---

## 🗺️ Roadmap

| Phase | Status | Description |
|-------|--------|-------------|
| 1 | ✅ Done | Setup, tools, folder structure, Git, Ruff, CodeRabbit |
| 2 | 🔄 In Progress | ChatAgent + Gemini API + settings loader |
| 3 | ⏳ Planned | FastAPI backend — Python ↔ Electron bridge |
| 4 | ⏳ Planned | Electron window + React chat UI |
| 5 | ⏳ Planned | Live2D anime avatar with expressions |
| 6 | ⏳ Planned | LangGraph: Planner + Desktop + Safety agents skeleton |
| 7 | ⏳ Planned | Tool Decision Layer — JSON tool-call routing |
| 8 | ⏳ Planned | Desktop automation (PyAutoGUI + Playwright + Windows APIs) |
| 9 | ⏳ Planned | Guide Mode — screen capture + visual overlays + step arrows |
| 10 | ⏳ Planned | Safety & permissions — plan approval, emergency stop, hard blocks |
| 11 | ⏳ Planned | Voice I/O — Whisper STT + Kokoro.js TTS (both local, free) |
| 12 | ⏳ Planned | Memory & storage — SQLite + ChromaDB vector memory |
| 13 | ⏳ Planned | Latency optimization — under 2s round-trip design |
| 14 | ⏳ Planned | Phone connectivity — Android companion + Phone Agent |
| 15 | ⏳ Planned | Local model fallback — Ollama + qwen3:4b |
| 16 | ⏳ Later | VS Code WebSocket integration |

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute to JARVIS.

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

> Note: "JARVIS" is used as a project name / homage. Trademark clearance will be reviewed before any commercial launch.
