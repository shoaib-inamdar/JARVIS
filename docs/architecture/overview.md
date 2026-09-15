# Architecture Overview — JARVIS

## System Layers

```
\+-----------------------------------------------------------------------+
|  PRESENTATION LAYER                                                   |
|  Electron + React window  |  Live2D anime avatar  |  System tray      |
|  Transparent screen overlay (Guide Mode arrows and highlights)        |
+-----------------------------------------------------------------------+
                                    |
                              IPC / WebSocket
                                    |
+-----------------------------------------------------------------------+
|  BACKEND LAYER  (FastAPI)                                             |
|  /chat endpoint  |  /health endpoint  |  /action endpoint             |
|  WebSocket for real-time streaming responses                          |
+-----------------------------------------------------------------------+
                                    |
+-----------------------------------------------------------------------+
|  ORCHESTRATION LAYER  (LangGraph)                                     |
|  Planner Agent  |  Desktop Agent  |  Safety Agent                    |
|  Memory Agent   |  Phone Agent (Phase 14)                             |
|  Tool Decision Layer  --  routes JSON tool calls to correct agent     |
+-----------------------------------------------------------------------+
                                    |
+-----------------------------------------------------------------------+
|  INTELLIGENCE LAYER                                                   |
|  Google Gemini 1.5 Flash (primary, free tier)                        |
|  Groq (fast backup if Gemini quota hit)                               |
|  Ollama + qwen3:4b (local fallback, Phase 15)                        |
|  Whisper (local speech-to-text)                                       |
|  Kokoro.js (local TTS, free, private)                                 |
|  ElevenLabs (premium TTS option)                                      |
+-----------------------------------------------------------------------+
                                    |
+-----------------------------------------------------------------------+
|  EXECUTION LAYER                                                      |
|  PyAutoGUI -- mouse, keyboard, screenshots                            |
|  Playwright -- browser automation                                     |
|  Windows APIs -- file system, processes, notifications                |
|  Permission Manager -- plan approval, hard blocks, emergency stop     |
|  Action Logger -- full audit trail of everything JARVIS does          |
+-----------------------------------------------------------------------+
                                    |
+-----------------------------------------------------------------------+
|  DATA LAYER                                                           |
|  SQLite -- session memory and structured data                         |
|  ChromaDB -- vector memory for long-term recall                       |
|  .env + OS secure storage -- encrypted secrets                        |
+-----------------------------------------------------------------------+
                                    |
+-----------------------------------------------------------------------+
|  PHONE LAYER  (Phase 14)                                              |
|  Android companion app  |  Secure pairing (QR/code)  |  Easy revoke  |
|  Phone Agent in LangGraph (only after Safety approval)                |
+-----------------------------------------------------------------------+
\
```
## Agent Responsibilities

| Agent | Job | Safety Level | MVP? |
|-------|-----|-------------|------|
| Planner | Understands intent, builds step-by-step plan | Low | Yes |
| Desktop | Executes desktop actions (click, type, run) | HIGH | Yes |
| Safety | Validates every plan and action before execution | CRITICAL | Yes |
| Memory | Stores and retrieves context across sessions | Low | Basic in MVP |
| Phone | Coordinates cross-device actions | HIGH | Phase 14 |

## LangGraph Shared State

Every agent reads and writes a shared state object containing:

| Field | What It Holds |
|-------|--------------|
| user_intent | What the user asked for |
| current_mode | Chat / Guide / JARVIS / MultiDevice |
| device_target | desktop / phone / both |
| plan_steps | List of proposed actions |
| pending_permissions | What still needs user approval |
| action_history | Everything JARVIS has already done |
| safety_flags | Blocks or warnings from Safety agent |
| memory_context | Relevant past information retrieved by Memory agent |

## Performance Design Goal

> Target: under 2 seconds from user input to first JARVIS response.

Strategies:
- Stream responses from Gemini (do not wait for full response)
- Cache common tool-call decisions
- Use local Whisper for STT (no network round-trip)
- Use local Kokoro.js for TTS (no network round-trip)
- Keep LangGraph graph shallow for Chat Mode (direct path, no agent hops)

## Communication: Electron <-> Python

\User types in React UI
        |
        v
Electron main process
        |
   IPC / WebSocket
        |
        v
FastAPI server (Python)
        |
        v
LangGraph agent graph
        |
        v
Gemini API / tool execution
        |
        v (stream back)
FastAPI -> WebSocket -> Electron -> React UI renders response
\
## Security & Privacy Principles

- API keys never leave .env — loaded at runtime only
- Class A data (screen content, clipboard) stays on device
- Every autonomous action requires explicit user approval
- Hard-coded blocks for highly sensitive categories
- Full action log — user can see everything JARVIS did
- Emergency stop available at all times
- Phone actions require separate explicit pairing and consent
