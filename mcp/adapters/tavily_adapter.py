# Create this file: insightbridge/mcp/adapters/tavily_adapter.py

import os
from tavily import TavilyClient

# Initialize the client once, when the file is loaded
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def tavily_search(query: str) -> list:
    """Runs a Tavily search and returns a clean list of content."""
    print(f"\n[Tool: Tavily] Searching for: '{query}'")
    try:
        result = tavily_client.search(
            query=query, 
            search_depth="advanced", 
            max_results=5
        )
        # Return a clean list of just the content
        return [obj["content"] for obj in result["results"]]
    except Exception as e:
        print(f"[Tool: Tavily] ERROR: {e}")
        return [f"Error in Tavily search: {e}"]