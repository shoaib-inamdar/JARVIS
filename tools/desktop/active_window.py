import pygetwindow as gw

from tools.registry import Tool, registry


def get_active_window() -> str:
    """Return the title of the currently focused window."""
    try:
        window = gw.getActiveWindow()
        if window and window.title:
            return window.title
    except Exception:
        pass
    return "Unknown"


registry.register(
    Tool(
        name="get_active_window",
        description=(
            "Returns the title of the currently focused window on screen. "
            "Use this to know which application the user has open."
        ),
        func=get_active_window,
        parameters={},
    )
)
