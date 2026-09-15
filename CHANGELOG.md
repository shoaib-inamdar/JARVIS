# 📋 Changelog

All notable changes to JARVIS will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased] — Phase 2 In Progress

### In Progress
- ChatAgent connected to Google Gemini API
- Settings loader using python-dotenv
- Terminal REPL interface with rich output

### Planned (Upcoming Phases)
- Phase 3: FastAPI backend + WebSocket (Python to Electron bridge)
- Phase 4: Electron window + React chat UI
- Phase 5: Live2D anime avatar with expressions
- Phase 6: LangGraph skeleton (Planner + Desktop + Safety agents)
- Phase 7: Tool Decision Layer (JSON tool-call routing)
- Phase 8: Desktop automation (PyAutoGUI + Playwright + Windows APIs)
- Phase 9: Guide Mode (screen capture + visual overlays)
- Phase 10: Safety & permissions (plan approval, emergency stop, hard blocks)
- Phase 11: Voice I/O (Whisper STT + Kokoro.js TTS — both local and free)
- Phase 12: Memory & storage (SQLite + ChromaDB vector memory)
- Phase 13: Latency optimization (under 2s round-trip design)
- Phase 14: Phone connectivity (Android companion + Phone Agent)
- Phase 15: Local model fallback (Ollama + qwen3:4b)
- Phase 16: VS Code WebSocket integration (later)

---

## [0.1.0] — Phase 1 Complete

### Added
- Initial project folder structure (top open-source style)
- `pyproject.toml` with uv package manager configuration
- `.ruff.toml` with production-grade linting rules
- `.gitignore` covering Python, Node, Electron, secrets
- `.coderabbit.yaml` for AI code review
- `README.md` with full tech stack and roadmap
- `CONTRIBUTING.md` with contribution guidelines
- GitHub Actions CI workflow (lint + test)
- Git repository initialized
