from datetime import UTC, datetime
import json
from pathlib import Path
import re
from shlex import shlex
import subprocess

from langchain_google_genai import ChatGoogleGenerativeAI

from agents.coding.coding_state import CodingState
from agents.coding.tools import (
    list_files,
    read_file,
    read_rules,
    run_safe_lint,
    run_tests,
    search_codebase,
)
from core.config.settings import AI_MODEL, GEMINI_API_KEY

AUTO_APPROVED_PREFIXES = (
    ("ruff", "check"),
    ("ruff", "format", "--check"),
    ("pytest",),
    ("python", "--version"),
)

BLOCKED_TOKENS = (
    "rm -rf",
    "del /f /s",
    "format c:",
    "drop table",
    "os.remove",
    "shutil.rmtree",
    "sudo",
    "passwd",
    ">/dev/null",
    "> /dev/null",
)

ASK_PREFIXES = (
    "pip install",
    "uv add",
    "git push",
    "git reset",
    "npm install",
)

llm = ChatGoogleGenerativeAI(model=AI_MODEL, google_api_key=GEMINI_API_KEY, temperature=0.2)


def planner_node(state: CodingState) -> dict:
    root = Path(state["project_root"]).resolve()
    request = state["user_request"]
    relevant_files: list[str] = []
    plan_steps: list[str] = []

    if not root.is_dir():
        return {
            "plan_steps": [],
            "relevant_files": [],
            "plan_approved": False,
            "avatar_mood": "stuck",
            "final_reply": f"Project directory does not exist: {root}",
            "blocked": True,
        }

    rules_path = root / "JARVIS.md"
    if rules_path.is_file():
        rules = read_file(str(rules_path))

    candidates = []

    if state.get("open_file"):
        candidates.append(state["open_file"])

    for match in re.findall(
        r"""[\w./\\-]+\.(?:py|js|jsx|ts|tsx|json|yaml|yml|md|html|css)""",
        request,
    ):
        candidates.append(match)

    for candidate in candidates:
        try:
            path = (root / candidate).resolve()
            if path.is_file() and path.is_relative_to(root) and str(path) not in relevant_files:
                relevant_files.append(str(path))
        except (OSError, ValueError):
            continue

        if not relevant_files:
            try:
                relevant_files = list_files(
                    str(root), extension=[".py", ".js", ".ts", ".tsx", ".jsx"]
                )
                relevant_files = relevant_files[:10]
            except (OSError, ValueError):
                relevant_files = []

        plan_steps.append("Inspect JARVIS.md project rules and relevant files.")

        if relevant_files:
            plan_steps.append(f"Read and analyze {len(relevant_files)} relevant file(s).")
        else:
            plan_steps.append("Locate the source files related to the request.")

        plan_steps.append(f"Analyze the request: {request}")
        plan_steps.append("Propose the smallest necessary code change.")
        plan_steps.append("Show the proposed diff and wait for approval.")

        if any(
            word in request.lower() for word in ("fix", "bug", "error", "test", "lint", "refactor")
        ):
            plan_steps.append("Run relevant lint checks and tests after approval.")

        if rules:
            plan_steps.insert(0, "Follow the project instructions in JARVIS.md.")

        return {
            "plan_steps": plan_steps,
            "relevant_files": relevant_files,
            "current_step": 0,
            "plan_approved": False,
            "avatar_mood": "thinking",
            "final_reply": "Plan ready. Review and approve it before execution.",
            "action_history": [
                *state.get("action_history", []),
                "Planner created a plan; awaiting user approval.",
            ],
            "blocked": False,
        }


def code_node(state: CodingState) -> dict:
    if state.get("blocked"):
        return {"final_reply": "Coding is blocked by the safety checks."}

    if not state.get("plan_approved", False):
        return {
            "final_reply": "Approve the plan before the Code Agent proceeds.",
            "avatar_mood": "thinking",
        }

    root = Path(state["project_root"]).resolve()
    context: list[str] = []

    for file_path in state.get("relevant_files", []):
        try:
            path = Path(file_path).resolve()
            if path.is_relative_to(root) and path.is_file():
                content = read_file(str(path))
                context.append(f"\n--- {path.relative_to(root)} ---\n{content}")
        except (OSError, ValueError):
            continue

    request = state["user_request"]
    search_results = search_codebase(request, str(root))

    if search_results:
        context.append(f"\n--- Search results ---\n{search_results}")

    if not context:
        return {
            "proposed_patch": "",
            "patch_approved": False,
            "avatar_mood": "stuck",
            "final_reply": (
                "Could not read relevant project files. Check the project path and permissions."
            ),
        }

    return {
        "proposed_patch": "",
        "patch_approved": False,
        "avatar_mood": "coding",
        "final_reply": (
            "Code context collected. Connect your model provider to generate "
            "a patch, then display the diff for user approval.\n\n" + "\n".join(context)[:12000]
        ),
        "action_history": [
            *state.get("action_history", []),
            "Code Agent collected context; no files were modified.",
        ],
    }


def terminal_node(state: CodingState) -> dict:
    command = state.get("pending_permissions", "").strip()

    if state.get("blocked"):
        return {"final_reply": "Command blocked by safety checks."}

    if not command:
        return {"final_reply": "No command has been requested."}

    return {
        "pending_permission": command,
        "avatar_mood": "thinking",
        "final_reply": f"Command requires safety review and permission: {command}",
        "action_history": [
            *state.get("action_history", []),
            f"Command submitted for review: {command}",
        ],
    }


def execute_approved_command(
    command: list[str],
    project_root: str,
    user_approved: bool,
    timeout: int = 30,
) -> dict:
    """Execute an argument-list command after explicit user approval."""
    if not user_approved:
        return {
            "test_results": "Command cancelled: user did not approve.",
            "exit_code": None,
        }

    root = Path(project_root).resolve()
    if not root.is_dir():
        return {"test_results": "Invalid project directory.", "exit_code": None}

    if not command or not all(isinstance(arg, str) for arg in command):
        return {"test_results": "Invalid command arguments.", "exit_code": None}

    blocked_commands = {
        "sudo",
        "format",
        "rm",
        "rmdir",
        "del",
        "diskpart",
        "shutdown",
        "reboot",
        "passwd",
    }
    if Path(command[0]).name.lower() in blocked_commands:
        return {"test_results": "Blocked dangerous command.", "exit_code": None}

    try:
        result = subprocess.run(
            command,
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
            check=False,
        )
        output = (
            f"Exit code: {result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
        return {"test_results": output, "exit_code": result.returncode}
    except subprocess.TimeoutExpired:
        return {"test_results": "Command timed out.", "exit_code": None}
    except OSError as exc:
        return {"test_results": f"Could not run command: {exc}", "exit_code": None}


def safety_node(state: CodingState) -> dict:
    """Apply deterministic safety checks before any command runs."""

    command = state.get("pending_permissions", "").strip()
    flags = list(state.get("safety_flags", []))

    if not command:
        return {
            "blocked": False,
            "safety_flags": flags,
            "final_reply": "No pending command to review.",
        }

    normalized = command.lower()

    if any(token in normalized for token in BLOCKED_TOKENS):
        message = f"Blocked dangerous command: {command}"
        flags.append(message)
        return {
            "blocked": True,
            "safety_flags": flags,
            "final_reply": "I blocked that command because it may be dangerous.",
            "pending_permission": "",
            "action_history": [*state.get("action_history", []), message],
        }

    try:
        parts = shlex.split(command, posix=False)
    except ValueError:
        parts = []

    executable = parts[0].lower() if parts else ""

    allowed = (
        executable in {"ruff", "pytest"}
        or (executable == "python" and parts[1:2] == ["--version"])
        or (executable == "uv" and len(parts) >= 3 and parts[1:3] == ["run", "ruff"])
        or (executable == "uv" and len(parts) >= 3 and parts[1:3] == ["run", "pytest"])
    )

    if any(normalized.startswith(prefix) for prefix in ASK_PREFIXES):
        allowed = False

    if allowed:
        flags.append(f"Command passed allowlist review: {command}")
        return {
            "blocked": False,
            "safety_flags": flags,
            "final_reply": "Command passed the allowlist; execute through the approved runner.",
        }

    message = f"Explicit user approval required: {command}"
    flags.append(message)
    return {
        "blocked": False,
        "safety_flags": flags,
        "pending_permission": command,
        "final_reply": message,
    }


def verifier_node(state: CodingState) -> dict:
    """Run verification and report actual results."""
    root = Path(state["project_root"]).resolve()

    files = state.get("relevant_files", [])

    if state.get("blocked"):
        return {
            "verified": False,
            "avatar_mood": "stuck",
            "final_reply": "Verification skipped because execution is blocked.",
        }

    lint_outputs: list[str] = []

    for file_path in files:
        path = Path(file_path).resolve()

        if not path.is_relative_to(root) or not path.is_file():
            continue

        if path.suffix == ".py":
            lint_outputs.append(f"--- {path.name} ---\n{run_safe_lint(str(path))}")

    lint_results = "\n".join(lint_outputs) or "No Python files available for linting."

    tests_dir = root / "tests"
    if tests_dir.is_dir():
        test_results = run_tests(str(root))
    else:
        test_results = "No tests/ directory found; tests were not run."

    lint_passed = bool(lint_outputs) and all(
        "error:" not in output.lower()
        and "failed" not in output.lower()
        and "traceback" not in output.lower()
        for output in lint_outputs
    )
    tests_passed = "no tests/ directory" in test_results.lower() or (
        "passed" in test_results.lower() and "failed" not in test_results.lower()
    )

    verified = lint_passed and tests_passed

    return {
        "lint_results": lint_results,
        "test_results": test_results,
        "verified": verified,
        "avatar_mood": "happy" if verified else "stuck",
        "final_reply": (
            "Verification passed."
            if verified
            else "Verification is incomplete or failed. Review the lint and test results."
        ),
        "action_history": [
            *state.get("action_history", []),
            f"Verification completed: {'passed' if verified else 'not passed'}.",
        ],
    }


def memory_node(state: CodingState) -> dict:
    """Read project rules and persist a small, project-local task log."""
    root = Path(state["project_root"]).resolve()
    memory_dir = root / ".jarvis"
    memory_file = memory_dir / "memory.json"

    history = list(state.get("action_history", []))

    read_rules(str(root))

    entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        "request": state.get("user_request", ""),
        "verified": state.get("verified", False),
        "summary": state.get("final_reply", ""),
        "safety_flags": state.get("safety_flags", []),
    }

    try:
        memory_dir.mkdir(parents=True, exist_ok=True)

        records = []
        if memory_file.exists():
            with memory_file.open("r", encoding="utf-8") as file:
                loaded = json.load(file)
                if isinstance(loaded, list):
                    records = loaded

        records.append(entry)
        records = records[-100:]

        temporary_file = memory_file.with_suffix(".tmp")
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(records, file, indent=2, ensure_ascii=False)
        temporary_file.replace(memory_file)

        history.append(
            "Memory updated with task outcome."
            if state.get("verified")
            else "Memory updated with task outcome; verification incomplete."
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        history.append(f"Could not save memory: {exc}")

    return {
        "action_history": history,
        "final_reply": state.get("final_reply", ""),
        "avatar_mood": state.get("avatar_mood", "thinking"),
    }
