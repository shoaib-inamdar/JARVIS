import os

from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
JARVIS_MODE = os.getenv("JARVIS_MODE", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
AI_MODEL = "gemini-1.5-flash"

if GEMINI_API_KEY is None:
    raise ValueError(
        "GEMINI_API_KEY not found!! Did you create your .env file?"
    )