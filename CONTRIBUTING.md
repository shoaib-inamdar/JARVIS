# 🤝 Contributing to JARVIS

Thank you for your interest in contributing! JARVIS is a learning project
but we follow real open-source contribution practices.

---

## 🪜 How to Contribute

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Create a branch** for your feature or fix — use a descriptive name
   like `feature/voice-input` or `fix/api-key-loading`
4. **Make your changes** following the code style below
5. **Run Ruff** to check your code before committing
6. **Write or update tests** in the `tests/` folder
7. **Push** your branch and open a **Pull Request**
8. CodeRabbit will automatically review your PR!

---

## 🦅 Code Style


This project uses **Ruff** for linting and formatting.

Before committing, run:
```bash
uv run ruff check .       # Check for issues
uv run ruff format .      # Auto-format your code
```

---

## 🛡️ Safety Rule

Any code that touches `agents/safety/` or `agents/desktop/`
**must** be reviewed carefully. These agents control the computer.
Never merge safety-critical changes without thorough review.

---

## 📋 Commit Message Style

Use clear, present-tense commit messages:

```
✅ Good:  "Add Gemini API connection to planner agent"
❌ Bad:   "stuff" or "fix" or "wip"
```

---

## 🧪 Running Tests

```bash
uv run pytest tests/ -v
```
