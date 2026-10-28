# 🤖 JARVIS — Just A Rather Very Intelligent System
### Your Complete Beginner's Build Guide

> **Teaching Philosophy**: You will *build* this yourself. I'll guide every step, explain every concept, and celebrate every win. By the end, you'll have an AI anime companion that lives on your desktop, sees your screen, and does tasks for you — safely. 🚀

> **The Rule**: Read the pseudocode carefully, understand it, then type the Python yourself. Do NOT copy-paste. Typing it yourself is how you actually learn!

---

## 🗺️ Project Roadmap (All Phases at a Glance)

> This is a living roadmap. Phases may grow as the project evolves — we never shrink scope, only add to it.

| Phase | Name | What You Build | Status |
|-------|------|----------------|--------|
| 1 | 🏗️ Setup & Workspace | Tools, folders, API keys, Git, Ruff, CodeRabbit | ✅ Done |
| 2 | 🧠 First Python Agent | ChatAgent + Gemini API + settings loader | ✅ Done |
| 3 | ⚡ FastAPI Backend | Python ↔ Electron communication bridge | ✅ Done |
| 4 | 🖥️ Electron + React UI | Real desktop window with Tailwind chat interface | ✅ Done |
| 5 | 🎭 Live2D Anime Avatar | Anime avatar with expressions and animations | ✅ Done |
| 6 | 🔗 LangGraph Agents | Planner + Desktop + Safety agents skeleton | ✅ Done |
| 7 | 🧰 Laya Tool Registry | Open-source plugin system for all JARVIS abilities | ⏳ Planned |
| 8 | 🛠️ Tool Decision Layer | LangGraph tool-call routing wired into Laya | ⏳ Planned |
| 9 | 🖱️ Desktop Automation | PyAutoGUI + Playwright + Windows APIs as Laya tools | ⏳ Planned |
| 10 | 👁️ Guide Mode | Screen capture + visual overlays + step-by-step arrows | ⏳ Planned |
| 11 | 🛡️ Safety & Permissions | Plan approval, emergency stop, Laya execution log | ⏳ Planned |
| 12 | 🎤 Voice I/O | Whisper STT (local) + Kokoro.js TTS (local, free) | ⏳ Planned |
| 13 | 🧩 Memory & Storage | SQLite session memory + ChromaDB vector long-term memory | ⏳ Planned |
| 14 | ⚡ Latency Optimization | Under 2s round-trip design for Guide Mode and voice | ⏳ Planned |
| 15 | 📱 Phone Connectivity | Android companion app + Phone Agent + safe pairing | ⏳ Planned |
| 16 | 🦙 Local Model Fallback | Ollama + qwen3:4b for offline/low-latency simple tasks | ⏳ Planned |
| 17 | 🧩 VS Code Integration | WebSocket inside editor for deep dev workflow support | ⏳ Later |

---

## ✅ Phase 1 — Setup Your Workspace (COMPLETE ✅)

### What You Built
- Installed Node.js, Python 3.13, Git, VS Code
- Set up `uv` as your package manager
- Created the full open-source project structure
- Configured `.ruff.toml`, `.gitignore`, `.coderabbit.yaml`
- Got your free Gemini API key
- Set up GitHub Actions CI

---

## ✅ Phase 2 — Make JARVIS Think (First Python Agent + Gemini API)

> **Stop after this phase and tell me "Phase 2 done" when finished!**

---

### 🎯 Goal

Build JARVIS's first working brain:

- A `settings.py` that safely loads your API key from `.env`
- A `ChatAgent` class in `agents/chat/agent.py` that talks to Google Gemini
- An updated `main.py` that runs a real back-and-forth terminal conversation

By the end, you will type a message in your terminal and JARVIS will reply — using real Gemini AI. 🎉

---

### 🤔 Why This Phase Matters

Right now JARVIS is just folders and config files — a body with no soul.

This phase gives JARVIS a brain. Everything we build later — the window, the avatar, the desktop control, the safety system — all of it connects back to this core: an agent that receives input, thinks using an LLM, and sends a response.

Understanding this well now means every future phase will make sense.

---

### 🧠 Four Concepts to Understand First

#### 1. What Is an Agent?

An **agent** is a program that:
1. Receives input (your message)
2. Thinks about it (using Gemini or another LLM)
3. Decides what to do
4. Takes an action or gives a response

In JARVIS, we will have five specialised agents that all work together:

| Agent | Job | When We Build It |
|-------|-----|-----------------|
| Planner | Understands your goal and makes a plan | Phase 6 |
| Desktop | Clicks, types, runs programs | Phase 7 |
| Safety | Checks every action before it runs | Phase 8 |
| Memory | Remembers past conversations | Phase 6 |
| Chat | Has a conversation with you | Phase 2 (NOW!) |

Today we build the Chat agent — the simplest but most important one.

#### 2. What Is a System Prompt?

When you call the Gemini API, you send two things:
- A **system prompt** — instructions that define who JARVIS is (personality, rules, behaviour)
- A **user message** — what you actually said

Think of the system prompt as JARVIS's job description. A well-written system prompt is the difference between generic AI output and JARVIS feeling like a real character.

#### 3. What Is Conversation History?

Real conversations have context. If you say "What about the second option?", JARVIS needs to know what options were discussed before. We store all past messages in a `history` list and send it along with every new message. Gemini reads the whole history and replies in context — exactly like a real conversation.

#### 4. What Is python-dotenv?

Your API key lives in `.env`. The `python-dotenv` library reads that file and makes its values available to Python via `os.getenv()`. This means your key never touches your code — it stays safely in a file that Git ignores.

---

### 🪜 Step-by-Step Instructions

---

#### Step 1 — Set Up Your `.env` File

1. In your JARVIS root folder, find `.env.example`
2. Copy it and rename the copy to `.env`
   (File Explorer: copy → paste → rename)
3. Open `.env` in VS Code
4. Replace the placeholder with your real Gemini API key:

```
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXX
```

**How to verify it worked:**
Open PowerShell in your JARVIS folder and type:
```
type .env
```
You should see your key. If you see an error, the file was not created yet.

> ⚠️ CRITICAL: Run `git status` right now. You should see `.env` listed under
> "Untracked files" — which means Git is ignoring it (from .gitignore). Good!
> If you ever see `.env` under "Changes to be committed", STOP and remove it.

---

#### Step 2 — Install Dependencies with uv

You need three packages. Use `uv add` (not `pip install`) for every package in this project.

| Package | What It Does |
|---------|-------------|
| `google-generativeai` | Official library to talk to Google Gemini |
| `python-dotenv` | Reads your `.env` file and loads the API key |
| `rich` | Makes terminal output beautiful with colours and formatting |

> The command pattern is: `uv add package-name`
> Install all three. Ask me if you need the exact commands!

**How to verify:**
Open `pyproject.toml` — you should see all three listed under `[project] dependencies`.
Also run: `uv run python -c "import google.generativeai; print('OK')"` — it should print `OK`.

---

#### Step 3 — Create the Folder Structure for Phase 2

Create these folders and files. `__init__.py` files are empty — they just tell Python
"this folder is a package you can import from."

```
JARVIS/
├── agents/
│   └── chat/
│       ├── __init__.py        ← Create this (empty)
│       └── agent.py           ← Your ChatAgent class goes here
├── core/
│   ├── __init__.py            ← Create this (empty)
│   └── config/
│       ├── __init__.py        ← Create this (empty)
│       └── settings.py        ← Loads your .env safely
```

> To create an empty file in VS Code: right-click the folder in Explorer → New File → type the name.

---

#### Step 4 — Write `core/config/settings.py`

This is the "front desk" of JARVIS. Every part of the code that needs the API key
or any setting comes here to get it — never hardcodes values themselves.

```
PSEUDOCODE for core/config/settings.py:
(Read carefully, then write Python yourself — do NOT copy!)

--- IMPORTS ---
Import: os
Import: load_dotenv from dotenv
Import: Path from pathlib

--- LOAD THE .env FILE ---
Find the project root:
    ROOT = the parent of the parent of this file (settings.py is 2 levels deep)

Load the .env file from the root:
    load_dotenv(ROOT / ".env")

--- SETTINGS ---
Read values from environment variables using os.getenv():

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY")    ← backup, can be None
JARVIS_MODE    = os.getenv("JARVIS_MODE", "development")
LOG_LEVEL      = os.getenv("LOG_LEVEL", "INFO")

# The Gemini model to use
AI_MODEL = "gemini-1.5-flash"   ← fastest and free-tier friendly

# Safety: crash early if the key is missing instead of failing mysteriously later
If GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY not found! Did you create your .env file?")
```

**Why this matters:** If someone forgets to set up `.env`, they get a clear error
message immediately — not a confusing crash 10 steps later.

---

#### Step 5 — Write `agents/chat/agent.py`

This is the main event! The `ChatAgent` class that actually talks to Gemini.

```
PSEUDOCODE for agents/chat/agent.py:
(Read carefully, then write Python yourself!)

--- IMPORTS ---
Import: google.generativeai as genai
Import: GEMINI_API_KEY, AI_MODEL from core.config.settings

--- CONFIGURE GEMINI (module level, outside any class) ---
Call: genai.configure(api_key=GEMINI_API_KEY)

--- JARVIS SYSTEM PROMPT ---
Create a variable: JARVIS_SYSTEM_PROMPT
This is a long triple-quoted string that defines JARVIS's personality.

Write it in your own words, but include these ideas:
  "You are JARVIS (Just A Rather Very Intelligent System),
   an intelligent AI desktop companion with an anime-style avatar.
   You are helpful, friendly, and slightly witty — like a knowledgeable
   friend who happens to know everything about computers and technology.
   
   You have three modes:
   - Chat Mode: have a helpful conversation
   - Guide Mode: walk the user through tasks step by step on their real screen
   - JARVIS Mode: take autonomous actions with the user's explicit permission
   
   Right now you are in Chat Mode.
   
   Always be concise, clear, and encouraging. If the user seems confused,
   ask a simple question to help them — don't overwhelm them.
   
   You are aware that you will later be able to see the user's screen,
   control their desktop, and connect to their phone — but only with permission."

--- CLASS: ChatAgent ---

  __init__(self) -> None:
    Create the Gemini model with the system prompt:
        self.model = genai.GenerativeModel(
            model_name=AI_MODEL,
            system_instruction=JARVIS_SYSTEM_PROMPT
        )
    Start a chat session (this holds conversation history automatically):
        self.chat_session = self.model.start_chat(history=[])
    
    Set: self.message_count = 0    ← track how many messages sent
    
    Print: "🤖 JARVIS ChatAgent initialised. Ready to chat!"

  ---

  chat(self, user_message: str) -> str:
    Purpose: Send one message, get one reply. The chat_session handles history.
    
    Steps:
      1. If user_message is empty or only whitespace:
         return "I didn't catch that — could you say it again?"
      
      2. Increment self.message_count
      
      3. Try:
           Send the message to Gemini:
               response = self.chat_session.send_message(user_message)
           
           Extract and return the text:
               return response.text.strip()
         
         Except Exception as error:
           Print: f"⚠️ Gemini error: {error}"
           return "Sorry, I'm having trouble thinking right now. Please try again!"

  ---

  clear_history(self) -> None:
    Purpose: Reset the conversation — start fresh.
    
    Start a brand new chat session:
        self.chat_session = self.model.start_chat(history=[])
    Reset: self.message_count = 0
    Print: "🔄 Conversation history cleared."

  ---

  get_message_count(self) -> int:
    Purpose: How many messages have been sent this session?
    Return: self.message_count
```

---

#### Step 6 — Update `main.py` with a Real Chat Loop

Now wire everything together. Update `main.py` so it runs a REPL —
Read-Evaluate-Print-Loop — the same pattern Python's own interactive shell uses.

```
PSEUDOCODE for updated main.py:
(Read carefully, then write Python yourself!)

--- IMPORTS ---
Import: ChatAgent from agents.chat.agent
Import: Console from rich.console
Import: Panel, Text from rich.panel (for pretty terminal output)

--- SETUP ---
Create a Console object:
    console = Console()

--- MAIN FUNCTION ---
def main() -> None:

  1. Print a welcome banner using rich:
     Something like a Panel with "JARVIS v0.1.0 — Chat Mode" and instructions.
     Include: "Type 'exit' to quit | Type 'clear' to reset conversation"

  2. Create the agent:
     agent = ChatAgent()

  3. Print: "JARVIS is ready. Say something!"

  4. Start the loop:
     While True:
     
       a. Get user input:
          user_input = input("You: ").strip()
       
       b. Handle special commands:
          If user_input is empty:
              continue   ← skip to next loop iteration
          
          If user_input.lower() is "exit" or "quit":
              Print: "JARVIS: Goodbye! Shutting down... 👋"
              break
          
          If user_input.lower() is "clear":
              agent.clear_history()
              Print: "JARVIS: Memory cleared! Fresh start."
              continue
       
       c. Send to JARVIS and print reply:
          reply = agent.chat(user_input)
          Print: f"JARVIS: {reply}"
          
          # Optionally use rich Panel for a nicer look

--- ENTRY POINT ---
if __name__ == "__main__":
    main()
```

---

#### Step 7 — Run and Test JARVIS

```
uv run python main.py
```

Try these test conversations to verify everything works:

**Test 1 — Basic chat:**
```
You: Hello JARVIS, who are you?
JARVIS: (Should introduce itself as JARVIS)
```

**Test 2 — Context memory:**
```
You: My name is Sam.
JARVIS: (Acknowledges)
You: What is my name?
JARVIS: (Should remember "Sam" — this tests conversation history!)
```

**Test 3 — Technical knowledge:**
```
You: Explain what LangGraph is in simple words
JARVIS: (Should give a clear explanation)
```

**Test 4 — Special commands:**
```
You: clear
JARVIS: Memory cleared! Fresh start.
You: What is my name?
JARVIS: (Should say it does not know — memory was cleared! ✅)
```

**Test 5 — Exit:**
```
You: exit
JARVIS: Goodbye! Shutting down...
```

---

#### Step 8 — Run Ruff and Fix Any Issues

Before committing, always run Ruff:

```
uv run ruff check .
uv run ruff format .
```

Ruff will tell you about issues like:
- Lines too long (over 100 characters)
- Missing type hints on function arguments
- Unused imports
- Variables that should be constants (all-caps)

Fix each issue it reports. This is how professional developers work — lint before every commit.

---

#### Step 9 — Commit Your Work

```
git add .
git status        ← double-check .env is NOT listed!
git commit -m "Phase 2: Add ChatAgent with Gemini API and settings loader"
```

If you have GitHub set up, push it and CodeRabbit will review your code! 🐇

---

### 📁 Files Changed in Phase 2

| File | What Changed |
|------|-------------|
| `core/__init__.py` | New — empty module marker |
| `core/config/__init__.py` | New — empty module marker |
| `core/config/settings.py` | New — safely loads .env and exports settings |
| `agents/chat/__init__.py` | New — empty module marker |
| `agents/chat/agent.py` | New — ChatAgent class with Gemini integration |
| `main.py` | Updated — real chat loop with rich terminal output |
| `pyproject.toml` | Updated — three new dependencies added |
| `.env` | New — your real API key (NEVER commit this!) |

---

### ⚠️ Common Mistakes to Watch Out For

| Mistake | Why It's Bad | How to Avoid It |
|---------|-------------|-----------------|
| Putting GEMINI_API_KEY directly in agent.py | Key leaks to GitHub | Always import from settings.py only |
| Committing .env | Your key goes public — you may get charged | Always check `git status` before committing |
| Using `pip install` instead of `uv add` | Breaks the uv-managed environment | Always use `uv add package-name` |
| Forgetting `__init__.py` files | Python cannot import your agents | Every Python package folder needs one |
| Not handling empty input in chat() | Crashes or sends blank messages to Gemini | Check for empty string before calling API |
| Not running Ruff before committing | Bad code style sneaks in undetected | Always: `uv run ruff check .` before `git commit` |

---

### 💡 Gemini API Tips

**Free tier limits for Gemini 1.5 Flash:**
- 15 requests per minute (RPM)
- 1 million tokens per day
- A normal conversation uses ~200–400 tokens per exchange

**If you get a quota error:**
- Wait 60 seconds and try again
- Or set `GROQ_API_KEY` in your `.env` and update settings.py to fall back to Groq

**To check your usage:**
Go to https://aistudio.google.com → your API key → "View usage"

---

### ✅ Phase 2 Success Checklist

You are done when you can check **ALL** of these:

- [ ] 🟢 `uv run python main.py` starts JARVIS in the terminal
- [ ] 🟢 You can type a message and JARVIS replies using Gemini
- [ ] 🟢 JARVIS remembers your name from earlier in the conversation
- [ ] 🟢 Typing "clear" resets the conversation history
- [ ] 🟢 Typing "exit" cleanly stops the program
- [ ] 🟢 `uv run ruff check .` shows zero errors
- [ ] 🟢 `pyproject.toml` shows google-generativeai, python-dotenv, rich
- [ ] 🟢 `git status` shows `.env` is NOT tracked by Git
- [ ] 🟢 You committed your work with a clear commit message

---

### 🎊 Phase 2 Celebration

You just integrated a real large language model into a Python application.
JARVIS now has a brain — it understands context, maintains conversation history,
and can answer almost anything intelligently.

You now have:
- A production-quality settings loader (environment-based config)
- A clean agent class with error handling and retry safety
- A proper REPL interface with special commands
- Ruff-clean code committed to Git

This is not beginner work. This is how professional AI applications are structured. 🏆

---

### 🎉 When You Are Done

Tell me **"Phase 2 done!"** and we will move on to **Phase 3 — FastAPI Backend** ⚡

In Phase 3, you will:
- Wrap your ChatAgent in a FastAPI web server
- Create `/chat` and `/health` endpoints
- Test the API with real HTTP requests
- Set up the Python ↔ Electron communication channel

This is the bridge that connects your Python brain to the Electron window you will build in Phase 4!

---

*Phase 2 complete ✅*

---

## ✅ Phase 3 — FastAPI Backend (Python ↔ Electron Bridge) ⚡

> **Stop after this phase and tell me "Phase 3 done" when finished!**

---

### 🎯 Goal

Wrap your `ChatAgent` in a **FastAPI web server** so the Electron front-end
(which you build in Phase 4) can talk to the Python brain over HTTP and WebSocket.

By the end, you will have a running API server that:
- Responds to `GET /health` — confirms JARVIS is alive
- Responds to `POST /chat` — takes your message, returns JARVIS's reply
- Supports WebSocket on `WS /ws/chat` — for real-time streaming later

You can test every endpoint from your terminal with no front-end needed.

---

### 🤔 Why This Phase Matters

Right now JARVIS only works in your terminal. But the final JARVIS lives in an
Electron desktop window — a JavaScript app. JavaScript cannot directly call Python functions.

The bridge is **FastAPI**: a Python web server that exposes your agents as HTTP
endpoints. Electron sends an HTTP request; FastAPI receives it, runs your Python
agent, and sends back a JSON response.

This is the exact pattern used by real production AI products.

```
React UI (JavaScript)
      |
   HTTP / WebSocket
      |
FastAPI server (Python)   <-- you build this in Phase 3
      |
ChatAgent -> Gemini API
```

---

### 🧠 Three Concepts to Understand First

#### 1. What is FastAPI?

FastAPI is a modern Python framework for building APIs (Application Programming Interfaces).
An API is just a way for two programs to talk to each other using HTTP — the same
protocol your browser uses to load web pages.

Think of FastAPI as a waiter at a restaurant:
- The front-end (React) is the customer placing an order
- The FastAPI endpoint is the waiter taking the order
- Your ChatAgent is the kitchen that makes the food

#### 2. What is an Endpoint?

An endpoint is a URL path that does a specific job:

| Endpoint | Method | What It Does |
|----------|--------|-------------|
| `/health` | GET | Returns "JARVIS is alive" — used to check the server is running |
| `/chat` | POST | Takes a message, returns JARVIS's reply |
| `/ws/chat` | WebSocket | Real-time two-way connection for streaming |

#### 3. What is JSON?

JSON (JavaScript Object Notation) is the data format APIs use to pass information.
Both Python and JavaScript can read it.

When you call `/chat`, you send:
```json
{"message": "Hello JARVIS"}
```
And get back:
```json
{"reply": "Hello! How can I help you today?", "message_count": 1}
```

---

### 🪜 Step-by-Step Instructions

---

#### Step 1 — Install FastAPI and uvicorn

You need two new packages:

| Package | What It Does |
|---------|-------------|
| `fastapi` | The web framework — defines your endpoints |
| `uvicorn` | The ASGI server — actually runs FastAPI and listens for requests |

Install them using `uv add`. You know the pattern by now!

**How to verify:**
```
uv run python -c "import fastapi; print(fastapi.__version__)"
```

---

#### Step 2 — Create the Folder Structure

```
JARVIS/
└── apps/
    └── desktop/
        └── backend/              ← Create this folder
            ├── __init__.py       ← Empty module marker
            ├── server.py         ← Your FastAPI app lives here
            └── models.py         ← Request/response data shapes (Pydantic)
```

---

#### Step 3 — Write `models.py` (Request and Response Shapes)

FastAPI uses Pydantic models to define exactly what data goes in and out of each endpoint.
Think of them as contracts — both sides agree on the shape of the data.

```
PSEUDOCODE for apps/desktop/backend/models.py:
(Read carefully, then write Python yourself!)

--- IMPORTS ---
Import: BaseModel from pydantic

--- MODELS ---

class ChatRequest(BaseModel):
    Purpose: Defines what the /chat endpoint expects to RECEIVE
    
    Fields:
        message: str          <- the user's message (required)
        session_id: str       <- defaults to "default"
                                 (later lets us track multiple users)

class ChatResponse(BaseModel):
    Purpose: Defines what the /chat endpoint sends BACK
    
    Fields:
        reply: str            <- JARVIS's response text
        message_count: int    <- how many messages this session
        status: str           <- "ok" or "error"

class HealthResponse(BaseModel):
    Purpose: What /health sends back
    
    Fields:
        status: str           <- always "ok"
        version: str          <- "0.1.0"
        agent_ready: bool     <- True if ChatAgent initialised OK
```

---

#### Step 4 — Write `server.py` (The FastAPI App)

This is the main file of Phase 3.

```
PSEUDOCODE for apps/desktop/backend/server.py:
(Read carefully, then write Python yourself!)

--- IMPORTS ---
Import: FastAPI, WebSocket, WebSocketDisconnect from fastapi
Import: CORSMiddleware from fastapi.middleware.cors
Import: ChatAgent from agents.chat.agent
Import: ChatRequest, ChatResponse, HealthResponse from .models

--- APP SETUP ---
Create the FastAPI app:
    app = FastAPI(title="JARVIS Backend", version="0.1.0")

Add CORS middleware (this lets Electron/React talk to Python without being blocked):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],        <- allow all origins (fine for local dev)
        allow_methods=["*"],
        allow_headers=["*"],
    )

Create one shared ChatAgent instance (module level):
    agent = ChatAgent()

--- ENDPOINT 1: GET /health ---
Purpose: Confirm JARVIS backend is alive.
Decorated with: @app.get("/health", response_model=HealthResponse)

Steps:
    Return a HealthResponse with:
        status="ok"
        version="0.1.0"
        agent_ready=True

--- ENDPOINT 2: POST /chat ---
Purpose: Receive a message, return JARVIS reply.
Decorated with: @app.post("/chat", response_model=ChatResponse)

Takes: request: ChatRequest

Steps:
    1. Call: reply = agent.chat(request.message)
    
    2. Return a ChatResponse with:
        reply=reply
        message_count=agent.get_message_count()
        status="ok"
    
    3. Wrap in try/except:
       If anything goes wrong, return ChatResponse with:
           reply="Internal error. Please try again."
           message_count=0
           status="error"

--- ENDPOINT 3: DELETE /chat/history ---
Purpose: Clear conversation history (like typing "clear" in the terminal)
Decorated with: @app.delete("/chat/history")

Steps:
    Call: agent.clear_history()
    Return: {"message": "Conversation history cleared."}

--- ENDPOINT 4: GET WS /ws/chat (WebSocket) ---
Purpose: Real-time connection for streaming responses later.
Decorated with: @app.websocket("/ws/chat")

Takes: websocket: WebSocket

Steps:
    1. Accept the connection: await websocket.accept()
    
    2. While True loop:
       Try:
         a. Receive text: data = await websocket.receive_text()
         
         b. Get reply from agent: reply = agent.chat(data)
         
         c. Send reply back: await websocket.send_text(reply)
       
       Except WebSocketDisconnect:
         Break out of the loop (client disconnected -- that is OK)

--- STARTUP AND SHUTDOWN EVENTS ---
@app.on_event("startup"):
    Print: "JARVIS backend starting up..."

@app.on_event("shutdown"):
    Print: "JARVIS backend shutting down..."

--- MAIN BLOCK (for running directly) ---
if __name__ == "__main__":
    Import: uvicorn
    Run: uvicorn.run(app, host="127.0.0.1", port=8000)
```

---

#### Step 5 — Update `main.py` to Support Both Modes

Add a `--server` flag so you can choose between terminal chat (Phase 2) and the API server (Phase 3):

```
PSEUDOCODE for updated main.py:
(Read carefully, then write Python yourself!)

--- IMPORTS ---
Import: sys
Keep existing imports: ChatAgent, Console, Panel, Text

--- UPDATE main() ---
def main() -> None:

  Check if user passed "--server" as a command line argument:
    If "--server" in sys.argv:
        Import uvicorn
        Import app from apps.desktop.backend.server
        Print: "Starting JARVIS backend server on http://127.0.0.1:8000"
        Print: "Docs at: http://127.0.0.1:8000/docs"
        uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
        Return   <- stop here, don't run the terminal loop
  
  Else:
    ... keep your existing terminal chat loop exactly as it is ...
```

---

#### Step 6 — Test the API Server

**Start the server:**
```
uv run python main.py --server
```

You should see:
```
JARVIS backend starting up...
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Open the auto-generated docs** — this is one of FastAPI's superpowers!
Navigate to: http://127.0.0.1:8000/docs

You will see a beautiful interactive page listing all your endpoints.
You can test each one directly from the browser — no code needed!

**Test manually using curl (in a second terminal):**

Test health:
```
curl http://127.0.0.1:8000/health
```
Expected: `{"status":"ok","version":"0.1.0","agent_ready":true}`

Test chat:
```
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "{"message": "Hello JARVIS"}"
```
Expected: `{"reply":"...JARVIS response...","message_count":1,"status":"ok"}`

Clear history:
```
curl -X DELETE http://127.0.0.1:8000/chat/history
```

**Stop the server:** Press `Ctrl+C`

---

#### Step 7 — Run Ruff and Commit

```
uv run ruff check .
uv run ruff format .
git add .
git status        <- make sure .env is NOT listed!
git commit -m "Phase 3: FastAPI backend with chat, health, and WebSocket endpoints"
```

---

### 📁 Files Changed in Phase 3

| File | What Changed |
|------|-------------|
| `apps/desktop/backend/__init__.py` | New — empty module marker |
| `apps/desktop/backend/models.py` | New — Pydantic request/response shapes |
| `apps/desktop/backend/server.py` | New — FastAPI app with all endpoints |
| `main.py` | Updated — added --server flag to run the API |
| `pyproject.toml` | Updated — fastapi and uvicorn added as dependencies |

---

### ⚠️ Common Mistakes to Watch Out For

| Mistake | Why It's Bad | How to Avoid It |
|---------|-------------|-----------------|
| Using `pip install fastapi` instead of `uv add fastapi` | Breaks your uv environment | Always use `uv add` |
| Forgetting the CORS middleware | Electron blocks the request with a CORS error | Always add CORSMiddleware for local dev |
| Creating a new ChatAgent on every request | Each request starts a fresh conversation with no memory | Create ONE agent at module level, reuse it |
| Not wrapping agent.chat() in try/except | One Gemini error crashes the whole server | Always handle exceptions in endpoints |
| Using `app.run()` instead of uvicorn | FastAPI does not have a built-in `.run()` | Always use uvicorn to run FastAPI |

---

### ✅ Phase 3 Success Checklist

You are done when you can check **ALL** of these:

- [ ] 🟢 `uv run python main.py --server` starts the server on port 8000
- [ ] 🟢 `http://127.0.0.1:8000/docs` shows the FastAPI interactive docs
- [ ] 🟢 `GET /health` returns `{"status": "ok", "agent_ready": true}`
- [ ] 🟢 `POST /chat` with `{"message": "Hello"}` returns a JARVIS reply
- [ ] 🟢 `DELETE /chat/history` clears the conversation
- [ ] 🟢 WebSocket endpoint `/ws/chat` accepts a connection (test from the docs page)
- [ ] 🟢 `uv run python main.py` (without --server) still works as terminal chat
- [ ] 🟢 `uv run ruff check .` shows zero errors
- [ ] 🟢 You committed your work with a clear commit message

---

### 🎊 Phase 3 Celebration

You now have a real working API! JARVIS's brain is no longer locked in a terminal —
it is accessible over HTTP, which means any program (Electron, a browser, a mobile app)
can talk to it.

You have:
- A proper FastAPI server with 4 endpoints
- Pydantic models for data validation
- CORS configured for Electron compatibility
- WebSocket support ready for real-time streaming
- Auto-generated interactive API documentation

This is professional backend engineering. 🏆

---

### 🎉 When You Are Done

Tell me **"Phase 3 done!"** and we will move on to **Phase 4 — Electron Window + React UI** 🖥️

In Phase 4, you will:
- Create an Electron app that opens a desktop window for JARVIS
- Build a React chat interface (input box, message bubbles, JARVIS name/status)
- Connect the React UI to your Phase 3 FastAPI server
- JARVIS will exist as a real desktop application for the first time!

---

*Phase 3 complete — last updated: Phase 3*

---

## ✅ Phase 3 — FastAPI Backend Complete ✅

Phase 3 bugs fixed in this session:
- `/health` endpoint was accidentally calling agent.chat() instead of returning status
- `/chat` endpoint was missing entirely
- WebSocket handler `websocket` was a bare annotation, not a real parameter
- `--server` flag was inside the chat loop instead of at the start of `main()`
- `google.generativeai` deprecated — migrated to new `google.genai` SDK
- Switched to `gemini-2.0-flash` model

---

## 🔨 Phase 4 — Electron + React Desktop Window 🖥️

> **Stop after this phase and tell me "Phase 4 done" when finished!**

---

### 🎯 Goal

Give JARVIS a real desktop window. By the end of this phase you will have:

- An Electron desktop app that opens when you run `npm start`
- A React chat interface — input box, message bubbles, JARVIS name and status
- The front-end connected live to your Phase 3 FastAPI server
- JARVIS existing as a real desktop application for the first time 🎉

---

### ⚠️ FIX YOUR API KEY FIRST — Do This Before Anything Else

Your `.env` file still has a placeholder key. **JARVIS will not work until you do this.**

1. Go to **https://aistudio.google.com**
2. Click **"Get API Key"** → **"Create API key"**
3. Copy the key (it starts with `AIza...`)
4. Open `.env` in VS Code
5. Replace `your_gemini_api_key_here` with your real key:
   ```
   GEMINI_API_KEY=AIzaSy.....your_real_key_here
   ```
6. Save. Then verify:
   ```
   uv run python main.py
   ```
   Type "hello" — if JARVIS replies, your key is working!

---

### 🤔 Why This Phase Matters

Right now JARVIS only exists in a black terminal window. The whole point of JARVIS
is that it lives *on* your desktop — it can see your screen, guide you, and display
an anime avatar. None of that is possible in a terminal.

**Electron** lets you build a desktop app using web technologies (HTML + CSS + JS).
The window is just a browser, packaged as a proper app with system access.

**React** is the most popular UI library in the world — VS Code, Slack, Discord,
and Figma all use Electron + React under the hood.

---

### 🧠 Four Concepts to Understand First

#### 1. What is Electron?

Electron has two parts that run separately:

- **Main process** — Node.js code that creates the window (`BrowserWindow`).
  Has access to your file system, system tray, OS notifications.
- **Renderer process** — The web page (React) the user sees.
  Like a browser tab embedded inside the window.

They communicate through a secure bridge called **IPC** (Inter-Process Communication).

#### 2. What is React?

React is a JavaScript library for building UIs from small reusable pieces called **components**.
You describe *what* the UI should look like based on data (**state**), and React
updates the screen efficiently whenever data changes.

#### 3. What is Vite?

Vite is a modern build tool that runs your React app with instant hot-reloading.
Changes you make appear in the app within milliseconds — no full rebuild needed.
In development, Electron loads your React app from Vite's dev server.

#### 4. How Does Front-end Talk to Back-end?

```
React UI  →  fetch("http://127.0.0.1:8000/chat", {...})  →  FastAPI  →  ChatAgent  →  Gemini
```

React sends HTTP requests to your Phase 3 server. The server calls your Python agent
and sends the response back as JSON. React displays it as a chat bubble.

---

### 🪜 Step-by-Step Instructions

---

#### Step 1 — Check Node.js Is Installed

Open a new terminal and run:
```
node --version
npm --version
```

You need Node.js v18 or higher and npm v9 or higher.
If not installed: go to https://nodejs.org and download the LTS version.

---

#### Step 2 — Create the React Project with Vite

Navigate into your desktop folder and initialise:
```
cd apps/desktop
npm create vite@latest . -- --template react
```

The `.` means "create in this folder, not a new subfolder."
Say yes to overwriting existing files if asked.

Then install packages:
```
npm install
```

Then add Electron:
```
npm install --save-dev electron electron-builder concurrently wait-on cross-env
```

---

#### Step 3 — Create `electron/main.js` (The Desktop Window Creator)

Create a folder `apps/desktop/electron/` and inside it create `main.js`.

```
PSEUDOCODE for apps/desktop/electron/main.js:
(This is JavaScript — read carefully, then type it yourself!)

--- IMPORTS ---
const { app, BrowserWindow, shell } = require("electron")
const path = require("path")

const isDev = process.env.NODE_ENV === "development"

--- CREATE WINDOW ---
function createWindow():
    win = new BrowserWindow({
        width: 420,
        height: 720,
        frame: false,              <- no default title bar
        transparent: true,         <- transparent bg (for avatar later)
        alwaysOnTop: false,
        resizable: true,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true
        }
    })
    
    If isDev:
        win.loadURL("http://localhost:5173")   <- Vite dev server
        win.webContents.openDevTools({ mode: "detach" })
    Else:
        win.loadFile(path.join(__dirname, "../dist/index.html"))

--- APP LIFECYCLE ---
app.whenReady().then(createWindow)

app.on("window-all-closed", () -> {
    if (process.platform !== "darwin") app.quit()
})

app.on("activate", () -> {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
})
```

---

#### Step 4 — Update `package.json`

Open `apps/desktop/package.json` and make these changes:

```
PSEUDOCODE — changes to package.json:
(Be careful with JSON — every key needs quotes, trailing commas cause errors!)

1. Add at the top level (same level as "name" and "version"):
   "main": "electron/main.js"

2. In "scripts", add these entries:
   "electron": "electron ."
   "electron:dev": "concurrently \"npm run dev\" \"wait-on http://localhost:5173 && cross-env NODE_ENV=development electron .\""
   "start": "npm run electron:dev"
   "build": "vite build && electron-builder"
```

---

#### Step 5 — Update `vite.config.js`

Electron needs Vite to serve on a specific port and base path.
Open `apps/desktop/vite.config.js` and update it:

```
PSEUDOCODE for vite.config.js:
(This is JavaScript — use the Vite defineConfig pattern)

import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"

export default defineConfig({
    plugins: [react()],
    server: {
        port: 5173,        <- must match the URL in electron/main.js
        strictPort: true   <- fail if port is taken (so we know immediately)
    },
    base: "./"             <- important for Electron production builds
})
```

---

#### Step 6 — Rewrite `src/App.jsx` (The Chat UI)

Delete everything Vite generated in App.jsx and write a real JARVIS chat interface.

```
PSEUDOCODE for apps/desktop/src/App.jsx:
(JavaScript/JSX — read carefully, then type it yourself!)

--- IMPORTS ---
Import useState, useEffect, useRef from "react"

--- CONSTANT ---
const API_URL = "http://127.0.0.1:8000"

--- COMPONENT: App ---
function App():

  --- STATE ---
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
  const messagesEndRef = useRef(null)

  --- EFFECT: Check backend health on load ---
  useEffect (runs once, [] dependency):
    async function checkHealth():
      Try:
        response = await fetch(API_URL + "/health")
        If response.ok: setIsConnected(true)
        Else: setIsConnected(false)
      Catch: setIsConnected(false)
    
    checkHealth()
    
    Add welcome message:
    setMessages([{
        id: 1,
        role: "jarvis",
        text: "Hello! I am JARVIS. How can I help you today?"
    }])

  --- EFFECT: Auto-scroll to bottom when messages update ---
  useEffect (runs whenever messages changes):
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })

  --- FUNCTION: sendMessage ---
  async function sendMessage():
    If input.trim() is empty OR isLoading: return
    
    const userText = input.trim()
    
    Add user message to state:
    setMessages(prev => [...prev, { id: Date.now(), role: "user", text: userText }])
    
    setInput("")
    setIsLoading(true)
    
    Try:
      response = await fetch(API_URL + "/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: userText })
      })
      data = await response.json()
      setMessages(prev => [...prev, { id: Date.now() + 1, role: "jarvis", text: data.reply }])
    Catch error:
      setMessages(prev => [...prev, {
          id: Date.now() + 1,
          role: "jarvis",
          text: "I lost connection to my brain. Is the Python server running?"
      }])
    Finally:
      setIsLoading(false)

  --- FUNCTION: handleKeyDown ---
  function handleKeyDown(e):
    If e.key === "Enter" AND NOT e.shiftKey:
        e.preventDefault()
        sendMessage()

  --- JSX RETURN ---
  return (
    <div className="app">
      
      <header className="header">
        <div className="title">
          <span className="title-icon">🤖</span>
          <span>JARVIS</span>
        </div>
        <div className="status">
          <div className={isConnected ? "status-dot connected" : "status-dot offline"} />
          <span>{isConnected ? "Connected" : "Offline"}</span>
        </div>
      </header>
      
      <div className="messages">
        {messages.map(msg => (
          <div key={msg.id} className={"message " + msg.role}>
            {msg.text}
          </div>
        ))}
        {isLoading && (
          <div className="message jarvis loading">
            <span>.</span><span>.</span><span>.</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="input-area">
        <textarea
          value={input}
          onChange={e -> setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Talk to JARVIS..."
          rows={1}
          disabled={isLoading}
        />
        <button
          onClick={sendMessage}
          disabled={isLoading || !input.trim()}
          className="send-btn"
        >
          {isLoading ? "..." : "Send"}
        </button>
      </div>
      
    </div>
  )
```

---

#### Step 7 — Write `src/App.css` (Dark Modern Styling)

Delete all Vite's default CSS and write this:

```
PSEUDOCODE for App.css — the rules you need:
(Translate to actual CSS!)

* (all elements):
    box-sizing: border-box
    margin: 0, padding: 0

body, html, #root:
    height: 100%
    overflow: hidden
    font-family: "Inter", "Segoe UI", system-ui, sans-serif

.app:
    height: 100vh
    display: flex, flex-direction: column
    background: rgba(13, 13, 23, 0.96)    <- very dark navy, slightly transparent
    border: 1px solid rgba(100, 80, 255, 0.3)    <- subtle purple border
    border-radius: 12px
    color: #e8e8f0
    overflow: hidden

.header:
    padding: 14px 18px
    background: rgba(20, 20, 35, 0.9)
    border-bottom: 1px solid rgba(100, 80, 255, 0.2)
    display: flex, justify-content: space-between, align-items: center

.title:
    display: flex, align-items: center, gap: 8px
    font-size: 16px, font-weight: 600
    letter-spacing: 1px

.title-icon:
    font-size: 20px

.status:
    display: flex, align-items: center, gap: 6px
    font-size: 11px, color: #888

.status-dot:
    width: 8px, height: 8px, border-radius: 50%

.status-dot.connected:
    background: #4ade80     <- green
    box-shadow: 0 0 6px #4ade80

.status-dot.offline:
    background: #f87171     <- red

.messages:
    flex: 1
    overflow-y: auto
    padding: 16px
    display: flex, flex-direction: column, gap: 10px

-- scrollbar styling (optional, makes it look clean) --
.messages::-webkit-scrollbar: width 4px
.messages::-webkit-scrollbar-track: transparent
.messages::-webkit-scrollbar-thumb: background rgba(100, 80, 255, 0.4), border-radius 2px

.message:
    max-width: 78%
    padding: 10px 14px
    border-radius: 14px
    font-size: 14px, line-height: 1.5
    word-break: break-word
    animation: fadeIn 0.2s ease

.message.user:
    align-self: flex-end
    background: linear-gradient(135deg, #6b4fff, #9b59ff)   <- purple gradient
    color: white
    border-bottom-right-radius: 4px

.message.jarvis:
    align-self: flex-start
    background: rgba(40, 40, 60, 0.9)
    color: #e0e0f0
    border-bottom-left-radius: 4px
    border: 1px solid rgba(100, 80, 255, 0.15)

.message.loading span:
    animation: blink 1.2s infinite
    Each span: animation-delay 0s, 0.2s, 0.4s respectively

@keyframes blink:
    0%, 80%, 100%: opacity 0
    40%: opacity 1

@keyframes fadeIn:
    from: opacity 0, transform translateY(4px)
    to: opacity 1, transform translateY(0)

.input-area:
    padding: 12px 16px
    border-top: 1px solid rgba(100, 80, 255, 0.2)
    display: flex, gap: 8px, align-items: flex-end
    background: rgba(15, 15, 25, 0.9)

.input-area textarea:
    flex: 1
    background: rgba(30, 30, 50, 0.8)
    border: 1px solid rgba(100, 80, 255, 0.25)
    border-radius: 10px
    color: #e0e0f0
    padding: 10px 14px
    font-size: 14px, font-family: inherit
    resize: none
    min-height: 44px, max-height: 120px
    outline: none
    When focus: border-color rgba(100, 80, 255, 0.6)

.send-btn:
    background: linear-gradient(135deg, #6b4fff, #9b59ff)
    color: white
    border: none
    border-radius: 10px
    padding: 10px 20px
    font-size: 14px, font-weight: 600
    cursor: pointer
    min-width: 64px
    transition: all 0.2s
    When disabled: opacity 0.4, cursor not-allowed
    When hover (not disabled): filter brightness(1.15), transform translateY(-1px)
```

---

#### Step 8 — Run It!

You need two terminals at the same time:

**Terminal 1** (JARVIS root folder):
```
uv run python main.py --server
```

**Terminal 2** (apps/desktop folder):
```
npm start
```

A dark, styled desktop window opens! Type a message to JARVIS. 🎉

---

### 📁 Files Changed in Phase 4

| File | What Changed |
|------|-------------|
| `apps/desktop/electron/main.js` | New — Electron main process |
| `apps/desktop/src/App.jsx` | Rewritten — React chat UI |
| `apps/desktop/src/App.css` | Rewritten — dark modern styling |
| `apps/desktop/package.json` | Updated — added Electron scripts |
| `apps/desktop/vite.config.js` | Updated — port and base path |

---

### ⚠️ Common Mistakes to Watch Out For

| Mistake | Why It's Bad | How to Avoid |
|---------|-------------|--------------|
| Not starting Python server first | All chat calls fail | Always start `uv run python main.py --server` first |
| Wrong API_URL in App.jsx | fetch() fails | Use `http://127.0.0.1:8000` exactly |
| Trailing comma in package.json | JSON parse error, app won't start | Validate JSON — every item except the last has no comma |
| Using `window.require()` in React | Crashes — renderer has no Node access | Only use fetch() in React, never Node APIs |
| API key still a placeholder | JARVIS replies "having trouble thinking" | Fix .env with real AIza... key from aistudio.google.com |

---

### ✅ Phase 4 Success Checklist

- [ ] 🟢 Real Gemini API key in `.env` (JARVIS replies in terminal mode)
- [ ] 🟢 `npm start` (in apps/desktop) opens a real desktop window
- [ ] 🟢 Window shows "Connected" (green dot) when Python server is running
- [ ] 🟢 Typing a message shows JARVIS reply in a styled bubble
- [ ] 🟢 User messages appear on the right (purple), JARVIS on the left (dark)
- [ ] 🟢 Window shows "Offline" (red dot) when Python server is stopped
- [ ] 🟢 Git commit done

---

### 🎊 Phase 4 Celebration

JARVIS is now a real desktop application! 🖥️

You have built a complete full-stack AI application:
- Python AI backend (Phases 2 + 3)
- React front-end with a dark, modern UI (Phase 4)
- Connected via HTTP — the same pattern used by every production AI product

From here, every phase adds new superpowers on top of this foundation! 🏆

---

### 🎉 When You Are Done

Tell me **"Phase 4 done!"** and we will move on to **Phase 5 — Live2D Anime Avatar** 🎭

In Phase 5 you will:
- Load a Live2D anime model inside the Electron window
- Wire JARVIS expressions to the chat (thinking, speaking, happy, concerned)
- JARVIS will feel genuinely alive for the first time!

---

*Phase 4 — last updated: Phase 4*

---

## ✅ Phase 4 — Electron + React Desktop Window Complete ✅

**What was fixed in this session:**
- Critical crash: `"main": "main.js"` → fixed to `"electron/main.cjs"`
- CJS vs ESM conflict: renamed `main.js` → `main.cjs` (Electron needs CommonJS)
- `setMessages()` at component root (infinite re-render) → moved into `useEffect`
- `useEffect(async...)` anti-pattern → fixed with inner async function
- `response`/`data` undeclared global variables → added `const`
- Missing `export default` on App component
- Migrated from plain CSS to **Tailwind v4** via `@tailwindcss/vite`
- `gemini-2.0-flash` deprecated → switched to `gemini-2.5-flash`
- CI/CD: `--all-extras` → `--all-groups`, `tool.uv.dev-dependencies` → `[dependency-groups]`
- Removed deprecated `google-generativeai` (saved 15 packages)

---

## 🎭 Phase 5 — Live2D Anime Avatar

> **Stop after this phase and tell me "Phase 5 done" when finished!**

---

### 🎯 Goal

Give JARVIS a face. By the end of this phase you will have:

- A Live2D anime avatar displayed inside the Electron window
- Smooth idle breathing/blinking animation running at all times
- Four expressions that JARVIS automatically switches between:
  - 😐 **Idle** — when waiting for you to type
  - 🤔 **Thinking** — while loading a reply (the dots are showing)
  - 💬 **Speaking** — right after a reply appears
  - 😊 **Happy** — after positive keywords in the reply
- The avatar sitting **above** the chat interface (or side by side)

---

### 🤔 Why This Phase Matters

JARVIS is meant to feel like a companion, not just a chat box. An animated anime avatar:

- Makes JARVIS feel **alive and present** on your desktop
- Gives visual feedback ("JARVIS is thinking...") without reading text
- Is the foundation for Phase 12 (voice) — lip sync comes later
- Differentiates JARVIS from a plain chatbot — this is the "desktop companion" part

Live2D is used in games like *Genshin Impact*, *Blue Archive*, and anime apps like
*VTuber* setups. You are adding the same technology to your desktop app.

---

### 🧠 Three Concepts to Understand First

#### 1. What is Live2D?

Live2D is a rendering technology for 2D anime characters. Instead of playing a
video loop, a Live2D model is a **rigged drawing** — individual parts (eyes, mouth,
head, hair) can move independently based on math.

The model file (`.moc3`) contains:
- All the art pieces (textures)
- Rigging data (how to deform each piece)
- Motion files (`.motion3.json`) — pre-made animations for idle, talking, etc.
- Expression files — parameter values for different moods

#### 2. What is `pixi-live2d-display`?

Pixi.js is a 2D WebGL rendering engine (the same one used in many browser games).
`pixi-live2d-display` is a plugin that loads Live2D models into Pixi.js.

It handles all the complex math — you just say:
```javascript
const model = await Live2DModel.from("path/to/model.model3.json")
app.stage.addChild(model)
model.expression("happy")
```

And the avatar appears and animates.

#### 3. What is a Free Live2D Model?

Live2D provides free sample models for learning/development. The most popular
for projects like this is **"hiyori"**, **"Mao"**, or **"koharu"** — all are
freely downloadable from the official Live2D sample page.

You can also use models from VTuber model packs shared under creative licenses.

---

### 🪜 Step-by-Step Instructions

---

#### Step 1 — Get a Free Live2D Model

Download a free sample model:

1. Go to: **https://www.live2d.com/en/cubism/download/sample-data/**
2. Download any free model (recommended: **"Mao"** or **"hiyori"** — both are anime style)
3. Extract the zip
4. Copy the entire model folder into your project:

```
apps/desktop/public/live2d/
└── Mao/                           ← or whatever model you downloaded
    ├── Mao.model3.json            ← the main file you will reference
    ├── Mao.moc3
    ├── Mao.physics3.json
    ├── textures/
    │   └── texture_00.png
    └── motions/
        ├── idle_01.motion3.json
        └── ...
```

**Why `public/`?** Vite serves everything in `public/` as static files — Electron
can access them with a simple URL.

---

#### Step 2 — Install Pixi.js and Live2D Plugin

```
cd apps/desktop
npm install pixi.js@7 pixi-live2d-display
```

**Important:** Use **Pixi.js v7** — `pixi-live2d-display` is not yet compatible
with v8. The version matters!

Verify:
```
node -e "const p = require('./node_modules/pixi.js/package.json'); console.log(p.version)"
```

---

#### Step 3 — Create the Avatar Component

Create a new file: `apps/desktop/src/Avatar.jsx`

```
PSEUDOCODE for apps/desktop/src/Avatar.jsx:
(Read carefully, then write JSX yourself!)

--- IMPORTS ---
Import: useEffect, useRef from "react"
Import: Application from "pixi.js"
Import: Live2DModel from "pixi-live2d-display"

--- CONSTANTS ---
MODEL_PATH = "/live2d/Mao/Mao.model3.json"
  (Update this to match your actual model folder and filename)

EXPRESSIONS = {
    idle:     null,          <- null means default/reset expression
    thinking: "thinking",   <- expression name defined in the .model3.json
    speaking: "speaking",
    happy:    "happy",
}

--- COMPONENT: Avatar ---
function Avatar({ expression = "idle" }):
  Purpose: Takes an expression prop ("idle", "thinking", "speaking", "happy")
           and displays the Live2D model with that expression applied.

  canvasRef = useRef(null)    <- reference to the <canvas> element
  modelRef  = useRef(null)    <- reference to the loaded Live2DModel
  appRef    = useRef(null)    <- reference to the Pixi Application

  --- EFFECT 1: Load the model (runs once on mount) ---
  useEffect (() => {
    async function loadModel():

        1. Create a Pixi Application:
           app = new Application({
               view: canvasRef.current,   <- attach to our <canvas>
               width: 300,
               height: 400,
               transparent: true,         <- no white background
               antialias: true,
           })
           appRef.current = app

        2. Load the Live2D model:
           model = await Live2DModel.from(MODEL_PATH)
           modelRef.current = model

        3. Add model to Pixi stage:
           app.stage.addChild(model)

        4. Position and scale the model:
           model.x = app.screen.width / 2   <- center horizontally
           model.y = app.screen.height       <- anchor at bottom
           model.anchor.set(0.5, 1.0)       <- center-bottom anchor point
           model.scale.set(0.25)            <- adjust until model fits nicely
                                                (try values between 0.1 and 0.5)

        5. Start idle motion:
           model.motion("idle")             <- plays the idle animation loop

    loadModel()

    Cleanup (returned function):
        If appRef.current exists: appRef.current.destroy()

  }, [])   <- empty array = run once

  --- EFFECT 2: Apply expression when prop changes ---
  useEffect (() => {
    If modelRef.current is null: return

    const expressionName = EXPRESSIONS[expression]

    If expressionName is null:
        model.expression()     <- reset to default
    Else:
        model.expression(expressionName)

  }, [expression])   <- runs whenever the expression prop changes

  --- RENDER ---
  Return:
    <div className="w-full flex justify-center">
      <canvas ref={canvasRef} style={{ background: "transparent" }} />
    </div>

export default Avatar
```

---

#### Step 4 — Wire Avatar Expressions to Chat State in App.jsx

Now connect the avatar's mood to what is happening in the chat.

```
PSEUDOCODE — changes to src/App.jsx:
(Add these on top of your existing App.jsx)

--- NEW IMPORT at top ---
Import Avatar from "./Avatar"

--- NEW STATE ---
const [avatarExpression, setAvatarExpression] = useState("idle")

--- CHANGES TO sendMessage() ---
When user sends a message:
    BEFORE fetching: setAvatarExpression("thinking")
    
    AFTER getting reply:
        If reply text includes any of ["great", "happy", "done", "sure", "love"]:
            setAvatarExpression("happy")
        Else:
            setAvatarExpression("speaking")
    
    After 3 seconds: setAvatarExpression("idle")   <- use setTimeout

--- RENDER CHANGES ---
ABOVE the messages div, add:
    <Avatar expression={avatarExpression} />

Your layout should now look like:
    <div className="app">              <- whole window
        <header ... />                 <- JARVIS title + status dot
        <Avatar expression={...} />   <- NEW: avatar panel
        <div messages ... />           <- chat history  
        <div input-area ... />         <- input box + send button
    </div>
```

---

#### Step 5 — Adjust the Window Height

The avatar takes vertical space. Update `electron/main.cjs` to make the window taller:

```
PSEUDOCODE — change in electron/main.cjs:
(Small change — update the height value)

In createWindow():
    Change: height: 720
    To:     height: 900      <- taller window to fit avatar + chat
```

---

#### Step 6 — Handle Missing Expressions Gracefully

Live2D models have different expression names. Your model might not have "thinking",
"speaking", or "happy" by default. Here is how to find out what expressions it has:

Open the `.model3.json` file in VS Code and look for the `"Expressions"` array:
```json
"Expressions": [
    { "Name": "angry", "File": "expressions/angry.exp3.json" },
    { "Name": "happy", "File": "expressions/happy.exp3.json" }
]
```

Update your `EXPRESSIONS` constant in `Avatar.jsx` to match the actual names
in your model file. If "thinking" does not exist, use "angry" or any available one.

---

#### Step 7 — Test It

1. Start the Python server (if not running):
   ```
   uv run python main.py --server
   ```

2. Start the Electron app:
   ```
   cd apps/desktop
   npm start
   ```

3. You should see:
   - The anime avatar displayed above the chat
   - The avatar's idle animation playing (breathing, blinking)
   - When you send a message: avatar switches to "thinking"
   - When JARVIS replies: avatar switches to "speaking" then "idle"

---

#### Step 8 — Commit

```
cd C:\Users\HP\Documents\JARVIS
git add .
git commit -m "Phase 5: Live2D anime avatar with expression system"
```

---

### 📁 Files Changed in Phase 5

| File | What Changed |
|------|-------------|
| `apps/desktop/public/live2d/` | New — your Live2D model files |
| `apps/desktop/src/Avatar.jsx` | New — the avatar component |
| `apps/desktop/src/App.jsx` | Updated — avatar wired to chat state |
| `apps/desktop/electron/main.cjs` | Updated — window height increased |
| `apps/desktop/package.json` | Updated — pixi.js and pixi-live2d-display added |

---

### ⚠️ Common Mistakes to Watch Out For

| Mistake | Why It's Bad | How to Avoid |
|---------|-------------|--------------|
| Using `pixi.js` v8 | `pixi-live2d-display` doesn't support v8 yet | Install `pixi.js@7` specifically |
| Wrong model path | "Failed to load model" error | Double-check the `.model3.json` filename and path |
| Expression name doesn't match model | No visible change | Open `.model3.json`, find exact expression names |
| Model appears but has white background | `transparent: false` in Pixi app | Set `transparent: true` in the Pixi Application config |
| Model is invisible or tiny | Wrong scale value | Try `model.scale.set(0.3)` and adjust up/down |
| Avatar cuts off at bottom | Window too short | Increase height in `electron/main.cjs` |

---

### ✅ Phase 5 Success Checklist

- [ ] 🟢 `npm start` shows the avatar above the chat interface
- [ ] 🟢 Idle animation is playing (model breathes/blinks smoothly)
- [ ] 🟢 Sending a message makes the avatar switch to "thinking"
- [ ] 🟢 After JARVIS replies, avatar switches to "speaking" then back to "idle"
- [ ] 🟢 Background is transparent (no white box around avatar)
- [ ] 🟢 Git commit done

---

### 🎊 Phase 5 Celebration

JARVIS now looks and feels like a real AI companion! 🎭

Your JARVIS has:
- A real desktop window (Phase 4) ✅
- A Live2D anime avatar with mood expressions (Phase 5) ✅
- A Python AI brain with FastAPI (Phases 2 + 3) ✅
- Everything connected end to end ✅

This is what most developers consider the hardest visual milestone of a desktop AI —
you have done it! Everything from here is adding *capabilities* to an already beautiful app.

---

### 🎉 When You Are Done

Tell me **"Phase 5 done!"** and we will move on to **Phase 6 — LangGraph Agents** 🔗

In Phase 6 you will:
- Replace the single ChatAgent with a LangGraph multi-agent system
- Build a Planner agent (decides what to do), Desktop agent (does it), and Safety agent (approves it)
- Wire them into a directed graph so JARVIS can do complex multi-step tasks

---

*Phase 5 — last updated: Phase 5*

---

## ✅ Phase 5 — Live2D Anime Avatar Complete ✅

**What was fixed:**
- `require()` mixed with `import` → pure ESM `import * as PIXI from "pixi.js"`
- `import Application from "pixi.js"` (no default export) → `import * as PIXI`
- Nested `useEffect` hooks → both at component root level
- `transparent` typo → `backgroundAlpha: 0`  (Pixi v7 API)
- `MODEL_PATH` / `EXPRESSIONS` undeclared → added `const`
- `model.expression()` → `model.motion()` (hiyori has NO Expressions, only Motions)
- Missing `Live2DModel.registerTicker(PIXI.Ticker)` → added (required for animation)
- Pixi vite ESM crash → fixed with `optimizeDeps.include` in vite.config.js
- CI ruff error → added `ruff>=0.9` to `[dependency-groups]` in pyproject.toml

**Hiyori model motion groups (from hiyori_free_t08.model3.json):**

| Chat State | Motion Group | Description |
|---|---|---|
| idle | `Idle` | Calm breathing loop (3 variants) |
| thinking | `FlickDown` | Looking down thoughtfully |
| speaking | `Tap` | Cheerful response |
| happy | `Flick` | Excited reaction |

---

## 🖼️ Bonus — How to Make JARVIS Use YOUR Face (Custom Avatar)

> This is a separate optional guide. You do not need to do this now.
> Come back to it whenever you want to replace hiyori with yourself!

---

### 🎯 Goal

Replace the hiyori anime model with a custom avatar made from your own photos —
turning JARVIS into a personalised AI companion that literally looks like you
(or any character you design).

---

### 🤔 Three Approaches — Pick One

#### Option A: VTuber-Style (Recommended for Beginners) 🟢

**What you need:** 1 clear front-facing photo of yourself

**How it works:**
1. Upload your photo to **ReadyPlayerMe** (https://readyplayer.me)
2. Their AI creates a 3D avatar from your photo in 2 minutes
3. Download as `.glb` (3D) or use their SDK
4. Render it in Electron using **Three.js** (WebGL 3D renderer)

**Why it's good:** Completely free, no art skills needed, auto-generated from your photo

**Why it's limited:** 3D avatar, not 2D anime style. Less "JARVIS" feeling.

---

#### Option B: AI-Generated Live2D Model 🟡

**What you need:** A few reference photos of yourself or a character you want

**How it works:**
1. Use **VRoid Studio** (https://vroid.com/en/studio) — free desktop app
   - Create a stylised anime character by adjusting sliders
   - Export as `.vrm` format
2. Use **live2d-converter** tools to approximate a Live2D rig from the VRM
   OR
   Use a **VRoid → Live2D** pipeline (requires Cubism Editor Pro — $160/year)

**Why it's good:** True anime style, your design, free base tools
**Why it's limited:** Full Live2D rigging from scratch needs Cubism Pro

---

#### Option C: AI Portrait → Animated PNG (Simplest) 🟢

**What you need:** A selfie

**How it works:**
1. Use **Lensa AI** or **Stable Diffusion** with your photo to generate an anime portrait
2. Use **DeepMotion** or **Animated Drawings** (Meta AI, free) to add movement
3. Export as animated WebP or a sprite sheet
4. Display in your Electron window as an `<img>` with CSS animations instead of Live2D

**Why it's good:** Fastest, no 3D or Live2D knowledge needed
**Why it's limited:** Pre-baked animation, can't change expressions dynamically

---

### 🪜 Recommended Path: Option C for Now, Option B Later

For a 15-year-old builder, this is the most realistic path:

**Phase 5 (now):** Use hiyori — free, works, looks great ✅
**Future upgrade:** When you have more time, use VRoid Studio to design a custom avatar,
then come back and replace the model path in `Avatar.jsx` — it is literally 1 line change.

---

### 🛠️ If You Want to Use Option C Right Now

Here are the exact steps:

**Step 1 — Generate an anime portrait of yourself:**
Go to https://huggingface.co/spaces/AP123/IllusionDiffusion
Upload your photo, choose anime style, download the result.

**Step 2 — Make it move (Meta's Animated Drawings):**
Go to https://sketch.metademolab.com/
Upload your anime portrait, select movement type, download the animated version.

**Step 3 — Add it to your Electron app:**
Instead of the `<canvas>` in Avatar.jsx, use:
```jsx
<img
  src={jarvisImage}
  className="h-48 object-contain"
  style={{ filter: expression === "thinking" ? "hue-rotate(180deg)" : "none" }}
/>
```

Use CSS filters (`brightness`, `hue-rotate`, `saturate`) to simulate mood changes.

---

## 🔗 Phase 6 — LangGraph Agents

> **Stop after this phase and tell me "Phase 6 done" when finished!**

---

### 🎯 Goal

Replace the single `ChatAgent` with a **multi-agent system** using LangGraph.

By the end, JARVIS will have three specialised agents working as a team:

- **Planner** — receives the user's message and decides the plan
- **Chat agent** — handles pure conversation (Phase 2's ChatAgent, enhanced)
- **Safety agent** — reviews every plan before execution (no dangerous actions)

Each agent is a node in a **directed graph** — LangGraph manages the flow between them.

---

### 🤔 Why This Phase Matters

Right now JARVIS can only chat. To do things — open apps, automate tasks, control
your desktop — it needs to make decisions:

```
"Open Chrome and search for Python tutorials"
        ↓
Planner: "I need to open Chrome, then search"
        ↓
Safety:  "Opening Chrome is safe. Searching is safe. ✅ Approved."
        ↓
Desktop Agent: executes the plan step by step
```

A single agent trying to do all this gets confused. Three specialised agents,
each great at one job, is how real AI systems are built — this pattern is used
by Google, OpenAI, Anthropic, and every serious AI company.

**LangGraph** is the framework that wires them together. It was built by the same
team that made LangChain and is the industry standard for multi-agent AI systems.

---

### 🧠 Two Concepts to Understand First

#### 1. What is a Graph in LangGraph?

A **graph** is a flowchart for your agents. Each box (node) is an agent or step.
Each arrow (edge) says "after this step, go here next."

```
START
  ↓
[Planner Node]          ← decides: "is this a chat or a task?"
  ↓
[Router]                ← "chat" → ChatNode | "task" → SafetyNode
  ↓              ↓
[Chat Node]   [Safety Node]    ← safety checks the plan
  ↓              ↓
[END]         [END or retry]
```

#### 2. What is State?

The **state** is the shared memory all nodes can read and write.
Think of it as a whiteboard that each agent can read and update:

```python
class JARVISState(TypedDict):
    messages: list         # full conversation history
    user_input: str        # what the user typed
    plan: str              # the Planner's current plan
    safe_to_run: bool      # Safety agent's verdict
    final_reply: str       # what JARVIS sends back to the user
```

Every node receives the current state, does its job, and returns updated state.

---

### 🪜 Step-by-Step Instructions

---

#### Step 1 — Install LangGraph

```
uv add langgraph langchain-google-genai
```

**What these do:**

| Package | Purpose |
|---|---|
| `langgraph` | The graph framework — `StateGraph`, nodes, edges, routing |
| `langchain-google-genai` | LangChain wrapper for Gemini — lets LangGraph call Gemini |

Verify:
```
uv run python -c "import langgraph; print(langgraph.__version__)"
```

---

#### Step 2 — Create the Folder Structure

```
JARVIS/
└── agents/
    ├── chat/
    │   └── agent.py          ← already exists (your Phase 2 ChatAgent)
    └── graph/                ← NEW folder
        ├── __init__.py       ← empty
        ├── state.py          ← JARVISState TypedDict
        ├── nodes.py          ← planner_node, safety_node, chat_node
        └── graph.py          ← builds and compiles the StateGraph
```

---

#### Step 3 — Write `agents/graph/state.py`

```
PSEUDOCODE for agents/graph/state.py:

--- IMPORTS ---
Import: TypedDict from typing
Import: Annotated from typing
Import: add_messages from langgraph.graph.message

--- STATE CLASS ---
class JARVISState(TypedDict):

    messages: Annotated[list, add_messages]
        Purpose: full conversation history.
        Annotated with add_messages means LangGraph
        automatically appends new messages instead of replacing

    user_input: str
        Purpose: the raw string the user typed

    intent: str
        Purpose: "chat" or "task" — set by planner
        Default: "chat"

    plan: str
        Purpose: the Planner's description of what to do
        Default: "" (empty string)

    safe_to_run: bool
        Purpose: True if Safety agent approved the plan
        Default: True

    final_reply: str
        Purpose: the reply that goes back to the user
        Default: ""
```

---

#### Step 4 — Write `agents/graph/nodes.py`

```
PSEUDOCODE for agents/graph/nodes.py:
(Write Python yourself — read carefully!)

--- IMPORTS ---
Import: ChatGoogleGenerativeAI from langchain_google_genai
Import: HumanMessage, SystemMessage, AIMessage from langchain_core.messages
Import: JARVISState from .state
Import: GEMINI_API_KEY, AI_MODEL from core.config.settings

Create one LLM instance (reused by all nodes):
    llm = ChatGoogleGenerativeAI(
        model=AI_MODEL,
        google_api_key=GEMINI_API_KEY,
        temperature=0.7
    )

--- NODE 1: planner_node ---
def planner_node(state: JARVISState) -> dict:
    Purpose: Look at the user's message and decide:
             - intent = "chat"  if it's conversation
             - intent = "task"  if it needs desktop action (open app, search, etc.)

    Steps:
        1. Build a prompt:
           system = """
           You are a planner. Classify the user message as one of:
           - "chat": normal conversation, questions, or information requests
           - "task": requests to open apps, control the desktop, search web,
                     create files, or take any real-world action

           Respond with ONLY the single word: chat OR task
           """
           messages = [SystemMessage(system), HumanMessage(state["user_input"])]

        2. Call the LLM:
           response = llm.invoke(messages)

        3. Parse intent:
           intent = response.content.strip().lower()
           If intent is not "task": intent = "chat"  (default to chat if unclear)

        4. If intent is "task":
           Make another LLM call to create a plan description:
           plan_prompt = f"The user wants to: {state['user_input']}. Describe the steps needed in one sentence."
           plan = llm.invoke([HumanMessage(plan_prompt)]).content

        5. Return updated state:
           Return {"intent": intent, "plan": plan if task else ""}

--- NODE 2: chat_node ---
def chat_node(state: JARVISState) -> dict:
    Purpose: Handle pure conversation using the existing ChatAgent style.

    Steps:
        1. Build conversation prompt from state["messages"]
        2. Add system prompt: "You are JARVIS, a helpful AI desktop companion..."
        3. Call llm.invoke(messages)
        4. Get reply from response.content
        5. Return: {"final_reply": reply}

--- NODE 3: safety_node ---
def safety_node(state: JARVISState) -> dict:
    Purpose: Review the plan and approve or reject it.

    Steps:
        1. Build prompt:
           "Review this plan: '{state['plan']}'
            Is this safe to execute on a Windows desktop?
            Does it avoid deleting files, accessing passwords, or private data?
            Respond with ONLY: safe OR unsafe"

        2. Call LLM.

        3. Parse response:
           verdict = response.content.strip().lower()
           safe_to_run = (verdict == "safe")

        4. If not safe:
           Set final_reply = "I am not allowed to do that — it might be unsafe."

        5. Return: {"safe_to_run": safe_to_run, "final_reply": ...}

--- ROUTER FUNCTION ---
def route_after_planner(state: JARVISState) -> str:
    Purpose: Decides which node to go to after the planner.
             This is used as a conditional edge in the graph.

    If state["intent"] == "task":
        Return "safety"        <- route to safety check
    Else:
        Return "chat"          <- route to chat
```

---

#### Step 5 — Write `agents/graph/graph.py`

```
PSEUDOCODE for agents/graph/graph.py:

--- IMPORTS ---
Import: StateGraph, END from langgraph.graph
Import: JARVISState from .state
Import: planner_node, chat_node, safety_node, route_after_planner from .nodes

--- BUILD GRAPH ---
def build_graph():
    1. Create the graph:
       graph = StateGraph(JARVISState)

    2. Add nodes:
       graph.add_node("planner", planner_node)
       graph.add_node("chat",    chat_node)
       graph.add_node("safety",  safety_node)

    3. Set the entry point:
       graph.set_entry_point("planner")

    4. Add conditional edge after planner:
       graph.add_conditional_edges(
           "planner",              <- from this node
           route_after_planner,   <- call this function to decide
           {
               "chat":   "chat",   <- if function returns "chat" → go to chat node
               "safety": "safety", <- if returns "safety" → go to safety node
           }
       )

    5. Add final edges:
       graph.add_edge("chat",   END)   <- chat → done
       graph.add_edge("safety", END)   <- safety → done

    6. Compile and return:
       return graph.compile()

--- MODULE LEVEL ---
Create a compiled graph ready to use:
    jarvis_graph = build_graph()
```

---

#### Step 6 — Update `main.py` and `server.py` to Use the Graph

In `server.py`, update the `/chat` endpoint to call the graph instead of the ChatAgent directly:

```
PSEUDOCODE — change in server.py:

--- NEW IMPORT ---
Import: jarvis_graph from agents.graph.graph

--- CHANGE THE /chat ENDPOINT ---
Old code: reply = agent.chat(request.message)

New code:
    result = jarvis_graph.invoke({
        "user_input": request.message,
        "messages": [],
        "intent": "chat",
        "plan": "",
        "safe_to_run": True,
        "final_reply": "",
    })
    reply = result["final_reply"]

Keep the ChatAgent for the terminal mode — it's simpler and useful for testing.
The API now uses the graph, which adds Planner + Safety on top.
```

---

#### Step 7 — Test the Graph

```
uv run python -c "
from agents.graph.graph import jarvis_graph

# Test 1: Pure chat
result = jarvis_graph.invoke({
    'user_input': 'Hello! What is 2 + 2?',
    'messages': [],
    'intent': 'chat',
    'plan': '',
    'safe_to_run': True,
    'final_reply': '',
})
print('Chat reply:', result['final_reply'])
print('Intent detected:', result['intent'])

# Test 2: Task request
result2 = jarvis_graph.invoke({
    'user_input': 'Open Chrome and search for Python tutorials',
    'messages': [],
    'intent': 'chat',
    'plan': '',
    'safe_to_run': True,
    'final_reply': '',
})
print('Task intent:', result2['intent'])
print('Plan:', result2['plan'])
print('Safe:', result2['safe_to_run'])
"
```

---

#### Step 8 — Ruff and Commit

```
uv run ruff check .
uv run ruff format .
git add .
git commit -m "Phase 6: LangGraph multi-agent system (Planner + Chat + Safety)"
```

---

### 📁 Files Changed in Phase 6

| File | What Changed |
|------|-------------|
| `agents/graph/__init__.py` | New — empty module marker |
| `agents/graph/state.py` | New — JARVISState TypedDict |
| `agents/graph/nodes.py` | New — planner, chat, and safety nodes |
| `agents/graph/graph.py` | New — StateGraph assembly and compilation |
| `apps/desktop/backend/server.py` | Updated — /chat uses jarvis_graph |
| `pyproject.toml` | Updated — langgraph + langchain-google-genai added |

---

### ⚠️ Common Mistakes to Watch Out For

| Mistake | Why It's Bad | How to Avoid |
|---------|-------------|--------------|
| Using `langgraph` without `langchain-google-genai` | Gemini won't work with LangGraph | Install both together |
| Forgetting to add `agents` to hatchling packages | Import errors in production | Already set in pyproject.toml |
| Not adding default values to JARVISState | Graph crashes if a key is missing | Always add defaults: `"intent": "chat"` |
| Returning full state from a node | LangGraph merges — only return changed keys | Return only what the node modified |
| Planner saying "task" for everything | Safety runs when not needed, slows things down | Tune the planner system prompt carefully |

---

### ✅ Phase 6 Success Checklist

- [ ] 🟢 `uv run python -c "from agents.graph.graph import jarvis_graph; print('graph ok')"` works
- [ ] 🟢 Test script shows correct intent ("chat" for questions, "task" for actions)
- [ ] 🟢 Server's `/chat` endpoint uses the graph (test via `npm start`)
- [ ] 🟢 Safety agent rejects obviously unsafe requests
- [ ] 🟢 `uv run ruff check .` — zero errors
- [ ] 🟢 Git commit done

---

### 🎊 Phase 6 Celebration

JARVIS is no longer just a chatbot — it's a **multi-agent AI system**! 🔗

You have:
- A Planner that understands intent
- A Safety agent that protects the user
- A graph that routes intelligently
- The same architecture used by serious AI products at Google and OpenAI 🏆

---

### 🎉 When You Are Done

Tell me **"Phase 6 done!"** and we will move on to **Phase 7 — Laya Tool Registry** 🧰

In Phase 7 you will:
- Install and configure the Laya open-source tool execution layer
- Register your first desktop tools (open app, search, screenshot)
- Wire Laya into the LangGraph Safety + Desktop agents
- Every new JARVIS ability from here on = a new Laya tool file

---

*Phase 6 — last updated: Phase 6*

---

# 🔗 Phase 6 — LangGraph Multi-Agent System

> **Stop after this phase and tell me "Phase 6 done!" when finished!**

---

## 🎯 Goal

Replace the single `ChatAgent` with a **multi-agent system** using LangGraph.

By the end of this phase, JARVIS has three specialised agents working as a team:

| Agent | Job |
|-------|-----|
| **Planner** | Reads the user's message, decides the *intent* (`chat` vs `task`) and writes a plan |
| **Chat Agent** | Handles pure conversation — same Gemini brain, but wired into the graph |
| **Safety Agent** | Reviews every plan before execution — rejects dangerous or unclear actions |

```
User types "Open Chrome and search Python tutorials"
        ↓
[Planner]  →  intent="task", plan="1. Open Chrome  2. Search for Python tutorials"
        ↓
[Safety]   →  "Both steps are safe." → safe_to_run=True
        ↓
[END]      →  final_reply sent back to the UI
         (Desktop automation comes in Phase 9 — for now Safety just approves/rejects)
```

---

## 🤔 Why This Phase Matters

Right now JARVIS can only chat.
To **do things** — open apps, control the desktop, search the web — it needs a
decision layer. A single agent doing everything gets confused.

LangGraph gives you a **directed graph**: each node is one agent, each arrow says
"after this step, go here next." It is the same architecture used at Google DeepMind,
OpenAI, and Anthropic. Learning it now puts you ahead of most developers.

---

## 🧠 Core Concepts Before You Start

### What is a Graph?

Think of a flowchart where each box is an agent and each arrow is a route.

```
START
  │
  ▼
[Planner] ──"chat"──▶ [Chat Agent] ──▶ END
    │
   "task"
    │
    ▼
[Safety Agent] ──▶ END
```

### What is State?

State is a **shared whiteboard** that every agent can read and update.
It travels through the graph — each agent adds its piece.

```python
class JARVISState(TypedDict):
    messages:    list   # full conversation history
    user_input:  str    # what the user typed
    intent:      str    # "chat" or "task" — set by Planner
    plan:        str    # Planner's step-by-step plan
    safe_to_run: bool   # Safety agent's verdict
    final_reply: str    # what goes back to the user
```

### What is a Node?

A node is just a Python function:
```
def my_node(state: JARVISState) -> dict:
    # read from state
    # do something
    # return only the keys you changed
    return {"final_reply": "hello"}
```

---

## 🪜 Step-by-Step Instructions

---

### Step 1 — Install LangGraph

```
uv add langgraph langchain-google-genai
```

Verify:
```
uv run python -c "import langgraph; print('LangGraph', langgraph.__version__)"
```

---

### Step 2 — Create the Folder Structure

```
JARVIS/
└── agents/
    ├── chat/
    │   └── agent.py        ← already exists (Phase 2)
    └── graph/              ← NEW
        ├── __init__.py     ← empty file
        ├── state.py        ← JARVISState TypedDict
        ├── nodes.py        ← planner_node, chat_node, safety_node
        └── graph.py        ← builds and compiles the StateGraph
```

---

### Step 3 — Write `agents/graph/__init__.py`

This file stays empty. It just tells Python that `graph` is a module.

---

### Step 4 — Write `agents/graph/state.py`

```
PSEUDOCODE for agents/graph/state.py:

IMPORTS:
    TypedDict from typing
    Annotated from typing
    add_messages from langgraph.graph.message

CLASS JARVISState(TypedDict):

    messages: Annotated[list, add_messages]
        → full conversation history
        → Annotated with add_messages so LangGraph APPENDS new messages
          instead of replacing the whole list

    user_input: str
        → the raw string the user typed

    intent: str
        → "chat" or "task"
        → set by the Planner node

    plan: str
        → the Planner's written plan (only filled for "task" intents)

    safe_to_run: bool
        → True = Safety agent approved, False = rejected

    final_reply: str
        → the reply that goes back to the UI via the /chat endpoint
```

---

### Step 5 — Write `agents/graph/nodes.py`

```
PSEUDOCODE for agents/graph/nodes.py:

IMPORTS:
    ChatGoogleGenerativeAI from langchain_google_genai
    HumanMessage, SystemMessage from langchain_core.messages
    JARVISState from .state
    GEMINI_API_KEY, AI_MODEL from core.config.settings

CREATE one shared LLM instance (all nodes reuse it):
    llm = ChatGoogleGenerativeAI(
        model=AI_MODEL,
        google_api_key=GEMINI_API_KEY,
        temperature=0.7
    )

────────────────────────────────────────────────────
NODE 1: planner_node(state: JARVISState) → dict
────────────────────────────────────────────────────
Purpose: Classify the user's message as "chat" or "task"

Steps:
    1. Build messages:
       system = """
           You are an intent classifier. Reply with ONLY one word:
           - "chat"  → if the user wants conversation or information
           - "task"  → if they want you to DO something (open apps,
                       search, take screenshots, create files, etc.)
       """
       msgs = [SystemMessage(system), HumanMessage(state["user_input"])]

    2. Call LLM:
       response = llm.invoke(msgs)
       intent = response.content.strip().lower()
       if intent not in ("chat", "task"):
           intent = "chat"   # default to chat if unclear

    3. If intent == "task": write a plan
       plan_prompt = (
           f"The user wants to: {state['user_input']}\n"
           "List the steps needed in ONE short sentence."
       )
       plan = llm.invoke([HumanMessage(plan_prompt)]).content
    else:
       plan = ""

    4. Return:
       {"intent": intent, "plan": plan}

────────────────────────────────────────────────────
NODE 2: chat_node(state: JARVISState) → dict
────────────────────────────────────────────────────
Purpose: Handle pure conversation, using the message history

Steps:
    1. Build the full message list from state["messages"]
       Prepend a SystemMessage:
       "You are JARVIS, a friendly and intelligent AI desktop companion.
        Keep answers concise but helpful."

    2. Call LLM with the messages

    3. Return:
       {"final_reply": response.content}

────────────────────────────────────────────────────
NODE 3: safety_node(state: JARVISState) → dict
────────────────────────────────────────────────────
Purpose: Review the plan and approve or reject it

Steps:
    1. Build prompt:
       "Review this plan: '{state['plan']}'
        Is it safe to run on a Windows desktop?
        Does it avoid: deleting files, passwords, private data, system changes?
        Reply with ONLY: safe OR unsafe"

    2. Call LLM

    3. Parse:
       verdict = response.content.strip().lower()
       safe_to_run = (verdict == "safe")

    4. If safe:
       final_reply = (
           f"I understand! Here's my plan:\n{state['plan']}\n\n"
           "(Desktop execution coming in Phase 9! 🚀)"
       )
    else:
       final_reply = (
           "I can't do that — it might be unsafe or I'm not allowed to. "
           "Please rephrase what you need!"
       )

    5. Return:
       {"safe_to_run": safe_to_run, "final_reply": final_reply}

────────────────────────────────────────────────────
ROUTER FUNCTION: route_after_planner(state) → str
────────────────────────────────────────────────────
Purpose: Tells LangGraph which node to visit after the Planner

    If state["intent"] == "task":
        return "safety"
    Else:
        return "chat"
```

---

### Step 6 — Write `agents/graph/graph.py`

```
PSEUDOCODE for agents/graph/graph.py:

IMPORTS:
    StateGraph, END from langgraph.graph
    JARVISState from .state
    planner_node, chat_node, safety_node, route_after_planner from .nodes

FUNCTION build_graph():

    1. Create graph:
       graph = StateGraph(JARVISState)

    2. Add nodes:
       graph.add_node("planner", planner_node)
       graph.add_node("chat",    chat_node)
       graph.add_node("safety",  safety_node)

    3. Set entry point:
       graph.set_entry_point("planner")

    4. Add conditional edge from planner:
       graph.add_conditional_edges(
           "planner",
           route_after_planner,
           {"chat": "chat", "safety": "safety"}
       )

    5. Both branches end the graph:
       graph.add_edge("chat",   END)
       graph.add_edge("safety", END)

    6. Compile and return:
       return graph.compile()

At module level (outside the function):
    jarvis_graph = build_graph()
```

---

### Step 7 — Update `apps/desktop/backend/server.py`

Wire the graph into the `/chat` API endpoint.

```
PSEUDOCODE — changes to server.py:

NEW IMPORT at the top:
    from agents.graph.graph import jarvis_graph

IN THE /chat ENDPOINT:
    (Replace: reply = agent.chat(request.message))

    New code:
        initial_state = {
            "user_input":  request.message,
            "messages":    [],
            "intent":      "chat",
            "plan":        "",
            "safe_to_run": True,
            "final_reply": "",
        }
        result = jarvis_graph.invoke(initial_state)
        reply  = result["final_reply"]

Keep the ChatAgent for terminal mode (main.py) — it is simpler and
great for debugging. The graph only runs via the FastAPI server.
```

---

### Step 8 — Test the Graph Directly

Before connecting it to the server, test it in isolation:

```
uv run python -c "
from agents.graph.graph import jarvis_graph

# Test 1 — Pure chat
r = jarvis_graph.invoke({
    'user_input': 'What is 2 + 2?',
    'messages': [], 'intent': 'chat',
    'plan': '', 'safe_to_run': True, 'final_reply': ''
})
print('--- TEST 1: CHAT ---')
print('Intent:', r['intent'])
print('Reply:', r['final_reply'])

# Test 2 — Task request
r2 = jarvis_graph.invoke({
    'user_input': 'Open Chrome and search for Python tutorials',
    'messages': [], 'intent': 'chat',
    'plan': '', 'safe_to_run': True, 'final_reply': ''
})
print()
print('--- TEST 2: TASK ---')
print('Intent:', r2['intent'])
print('Plan:', r2['plan'])
print('Safe:', r2['safe_to_run'])
print('Reply:', r2['final_reply'])
"
```

✅ Expected results:
- Test 1: `intent = "chat"`, reply is an actual answer
- Test 2: `intent = "task"`, plan has steps, reply shows the plan

---

### Step 9 — Ruff and Commit

```
uv run ruff check .
uv run ruff format .
git add .
git commit -m "Phase 6: LangGraph multi-agent system (Planner + Chat + Safety)"
git push
```

---

## 📁 New Files in Phase 6

| File | Purpose |
|------|---------|
| `agents/graph/__init__.py` | Module marker (empty) |
| `agents/graph/state.py` | `JARVISState` TypedDict — the shared whiteboard |
| `agents/graph/nodes.py` | Three agent nodes + router function |
| `agents/graph/graph.py` | Assembles and compiles the StateGraph |
| `apps/desktop/backend/server.py` | Updated `/chat` endpoint to use graph |

---

## ⚠️ Common Mistakes

| Mistake | Why It's Bad | How to Avoid |
|---------|-------------|--------------|
| Returning full state from a node | LangGraph merges — only return changed keys | Return only `{"intent": ...}` not the whole dict |
| Using `from agents.graph.nodes import *` | Name conflicts | Import exactly what you need |
| Forgetting `__init__.py` | `ModuleNotFoundError` | Empty file is enough |
| Using `model=AI_MODEL` without the `models/` prefix | Some LangChain wrappers need `"models/gemini-2.5-flash"` | Try both if you get a 404 |
| Planner says "task" for everything | Safety runs unnecessarily, slow | Tune the system prompt with more examples |

---

## ✅ Phase 6 Success Checklist

- [ ] 🟢 `uv run python -c "from agents.graph.graph import jarvis_graph"` — no errors
- [ ] 🟢 Test script: intent is "chat" for questions, "task" for action requests
- [ ] 🟢 Safety agent rejects clearly dangerous requests
- [ ] 🟢 `/chat` API endpoint returns replies from the graph (test via `npm start`)
- [ ] 🟢 `uv run ruff check .` — zero errors
- [ ] 🟢 Git commit + push done

---

## 🎊 What You Have After Phase 6

JARVIS is now a **multi-agent AI system** — the same architecture pattern used in
production AI products at every major tech company. You built it from scratch. 🏆

Your JARVIS now has:
- ✅ A Live2D anime companion face (Phase 5)
- ✅ A Planner that classifies every message
- ✅ A Safety agent that protects the user
- ✅ A graph that routes intelligently between agents
- ✅ FastAPI + Electron UI showing real AI replies

---

## 🎉 When Done

Tell me **"Phase 6 done!"** and we move to **Phase 7 — Laya Tool Registry** 🧰

In Phase 7 you will install and configure Laya — the open-source tool execution layer.
Every desktop action JARVIS can do (open apps, take screenshots, search the web)
will be registered as a Laya tool. Adding a new JARVIS ability = adding one new file.

---

*Phase 6 — LangGraph Agents*

---

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

---

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


---

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

---

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


---

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
