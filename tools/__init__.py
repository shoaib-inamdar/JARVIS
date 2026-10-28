import importlib
import logging
from pathlib import Path


def load_all_tools() -> None:
    """Walk every sub-module in the tools/ folder and import it.

    Each module is expected to call registry.register() at import time.
    """
    tools_dir = Path(__file__).parent

    for py_file in tools_dir.rglob("*.py"):
        if py_file.name in {"__init__.py", "registry.py"}:
            continue
        relative_path = py_file.relative_to(tools_dir.parent)
        module_path = ".".join(relative_path.with_suffix("").parts)

        try:
            importlib.import_module(module_path)
            logging.info("Loaded tool: %s", module_path)
        except Exception as exc:
            logging.error("Failed to load tool %s: %s", module_path, exc)


load_all_tools()
