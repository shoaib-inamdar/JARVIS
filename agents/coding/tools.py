import difflib
from pathlib import Path
import subprocess

SKIP_FOLDERS = {".venv", "node_modules", ".git", "__pycache__"}


def read_file(path: str) -> str:
    file = Path(path)
    if not file.exists():
        return "ERROR: File not Found"
    if file.stat().st_size > 100_000:
        return "ERROR: File is too Large"
    return file.read_text(encoding="utf-8")


def list_files(directory: str, extensions: list | None = None) -> list[str]:
    root = Path(directory)
    results = []
    for file in root.rglob("*"):
        if any(skip in file.parts for skip in SKIP_FOLDERS):
            continue
        if not file.is_file():
            continue
        if extensions is None or file.suffix in extensions:
            results.append(str(file))
    return results[:50]


def search_codebase(query: str, root: str) -> str:
    results = []
    for file in list_files(root, [".py"]):
        content = read_file(file)
        if content.startswith("ERROR:"):
            continue
        for line_number, line in enumerate(content.splitlines(), 1):
            if query.lower() in line.lower():
                results.append(f"{file}:{line_number}:{line.strip()}")
    return "\n".join(results[:30])


def propose_patch(path: str, old_text: str, new_text: str) -> str:
    diff = difflib.unified_diff(
        old_text.splitlines(keepends=True),
        new_text.splitlines(keepends=True),
        fromfile=f"a/{path}",
        tofile=f"b/{path}",
    )
    return "".join(diff)


def apply_patch(path: str, old_text: str, new_text: str) -> str:
    file = Path(path)
    current = file.read_text(encoding="utf-8")
    if old_text not in current:
        return "ERROR: Old text not found - file may have changed"
    updated = current.replace(old_text, new_text, 1)
    file.write_text(updated, encoding="utf-8")
    return f"SUCCESS: {path} updated"


def run_safe_lint(path: str) -> str:
    result = subprocess.run(
        ["uv", "run", "ruff", "check", path],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.stdout + result.stderr


def run_tests(root: str) -> str:
    tests_dir = Path(root) / "tests"
    if not tests_dir.exists():
        return "No tests/ folder found"
    result = subprocess.run(
        ["uv", "run", "pytest", "tests/", "-v", "--tb=short"],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=root,
    )
    return result.stdout[-3000:]


def read_rules(project_root: str) -> str:
    jarvis_md = Path(project_root) / "JARVIS.md"
    if jarvis_md.exists():
        return jarvis_md.read_text(encoding="utf-8")
    return ""
