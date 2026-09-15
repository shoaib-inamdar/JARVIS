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
| 2 | 🧠 First Python Agent | ChatAgent + Gemini API + settings loader | 🔄 In Progress |
| 3 | ⚡ FastAPI Backend | Python ↔ Electron communication bridge | ⏳ Planned |
| 4 | 🖥️ Electron + React UI | Real desktop window with chat interface | ⏳ Planned |
| 5 | 🎭 Live2D Anime Avatar | Anime avatar with expressions and animations | ⏳ Planned |
| 6 | 🔗 LangGraph Agents | Planner + Desktop + Safety agents skeleton | ⏳ Planned |
| 7 | 🛠️ Tool Decision Layer | JSON tool-call routing (LangGraph tool calling) | ⏳ Planned |
| 8 | 🖱️ Desktop Automation | PyAutoGUI + Playwright + Windows APIs | ⏳ Planned |
| 9 | 👁️ Guide Mode | Screen capture + visual overlays + step-by-step arrows | ⏳ Planned |
| 10 | 🛡️ Safety & Permissions | Plan approval, emergency stop, action log, hard blocks | ⏳ Planned |
| 11 | 🎤 Voice I/O | Whisper STT (local) + Kokoro.js TTS (local, free) | ⏳ Planned |
| 12 | 🧩 Memory & Storage | SQLite session memory + ChromaDB vector long-term memory | ⏳ Planned |
| 13 | ⚡ Latency Optimization | Under 2s round-trip design for Guide Mode and voice | ⏳ Planned |
| 14 | 📱 Phone Connectivity | Android companion app + Phone Agent + safe pairing | ⏳ Planned |
| 15 | 🦙 Local Model Fallback | Ollama + qwen3:4b for offline/low-latency simple tasks | ⏳ Planned |
| 16 | 🧩 VS Code Integration | WebSocket inside editor for deep dev workflow support | ⏳ Later |

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

*Phase 2 complete — last updated: Phase 2*
