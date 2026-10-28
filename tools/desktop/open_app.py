import shutil
import subprocess

from tools.registry import Tool, registry

KNOWN_APPS = {
    "chrome": ["chrome", "google-chrome", "chrome.exe"],
    "firefox": ["firefox", "firefox.exe"],
    "notepad": ["notepad", "notepad.exe"],
    "vscode": ["code", "code.exe"],
    "explorer": ["explorer", "explorer.exe"],
    "terminal": ["wt", "cmd.exe", "powershell.exe"],
}


def open_app(app_name: str) -> str:
    name_lower = app_name.lower().strip()
    candidates = KNOWN_APPS.get(name_lower, [name_lower])

    for candidate in candidates:
        found = shutil.which(candidate)  # renamed from 'executable' to avoid shadowing
        if found:
            subprocess.Popen([found])
            return f"Opened {app_name} successfully."

    return f"ERROR: Could not find '{app_name}'. Is it installed?"


registry.register(
    Tool(
        name="open_app",
        description=(
            "Opens an application on the Windows desktop. "
            "Supported: chrome, firefox, notepad, vscode, explorer, terminal. "
            "Pass the app name as a string."
        ),
        func=open_app,
        parameters={
            "app_name": {"type": "string", "description": "Name of the app to open"},
        },
    )
)
