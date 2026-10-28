from duckduckgo_search import DDGS

from tools.registry import Tool, registry


def web_search(query: str, max_results: int = 5) -> str:  # fixed typo: qeury → query
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return "No results found."

        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(f"{i}. {r['title']}\n   {r['href']}\n   {r['body'][:200]}")

        return "\n\n".join(formatted)

    except Exception as exc:
        return f"Search error: {exc}"


registry.register(
    Tool(
        name="web_search",
        description=(
            "Searches the web using DuckDuckGo (no API key needed). "
            "Returns title, URL, and a short description for each result. "
            "Use for factual questions or finding resources."
        ),
        func=web_search,
        parameters={
            "query": {"type": "string", "description": "What to search for"},
            "max_results": {"type": "integer", "description": "Number of results (default 5)"},
        },
    )
)
