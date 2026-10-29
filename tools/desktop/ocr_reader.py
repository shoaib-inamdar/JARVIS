import os
from pathlib import Path

from PIL import Image
import pyautogui
import pytesseract

from tools.registry import Tool, registry

# Point pytesseract at the Tesseract binary from .env
_tess_path = os.getenv("TESSERACT_PATH", "")
if _tess_path and Path(_tess_path).is_file():
    pytesseract.pytesseract.tesseract_cmd = _tess_path


def read_screen_text(image_path: str = "") -> str:
    """Read all visible text from the screen or an image file via OCR."""
    img = Image.open(image_path) if image_path else pyautogui.screenshot()

    try:
        text = pytesseract.image_to_string(img)
    except pytesseract.TesseractNotFoundError:
        return (
            "ERROR: Tesseract is not installed or TESSERACT_PATH is wrong. "
            "Set TESSERACT_PATH=C:\\Program Files\\Tesseract-OCR\\tesseract.exe in .env"
        )

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines[:100])


registry.register(
    Tool(
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
                "description": (
                    "Optional path to a saved screenshot. Leave empty to take a new one."
                ),
            }
        },
    )
)
