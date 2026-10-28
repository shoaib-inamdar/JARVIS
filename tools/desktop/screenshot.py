from datetime import datetime
from pathlib import Path

import pyautogui

from tools.registry import Tool, registry

SCREENSHOT_DIR = Path(".jarvis") / "screenshots"


def take_screenshot(label: str = "") -> str:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{label or 'screenshot'}.png"
    path = SCREENSHOT_DIR / filename

    screenshot = pyautogui.screenshot()
    screenshot.save(str(path))

    return f"Screenshot saved: {path}"


registry.register(
    Tool(
        name="take_screenshot",
        description=(
            "Takes a screenshot of the entire screen and saves it. "
            "Returns the file path. Use to verify what is on screen."
        ),  # was a dict {} instead of a string — caused silent failure
        func=take_screenshot,
        parameters={
            "label": {"type": "string", "description": "Optional label for the filename"},
        },
    )
)
