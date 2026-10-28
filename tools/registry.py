from collections.abc import Callable
import dataclasses


@dataclasses.dataclass
class Tool:
    name: str
    description: str
    func: Callable
    parameters: dict


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list_tools(self) -> list[dict]:
        """Return a list of {name, description} for the AI to read."""
        return [
            {
                "name": t.name,
                "description": t.description,
            }
            for t in self._tools.values()
        ]

    def call(self, name: str, **kwargs: object) -> str:
        tool = self.get(name)
        if tool is None:
            return f"ERROR: Tool '{name}' not found"
        try:
            result = tool.func(**kwargs)
            return str(result)
        except Exception as exc:
            return f"ERROR: {exc}"


registry = ToolRegistry()
