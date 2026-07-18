import os
from tavily import TavilyClient

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_web(query: str, max_results: int = 5):
    """Runs a live web search and returns a list of
    {title, url, content} dicts. Returns [] on any failure so callers
    can fall back gracefully instead of crashing the request."""
    try:
        results = client.search(query=query, max_results=max_results)
        return results.get("results", [])
    except Exception as e:
        print("Search service error:", e)
        return []
        