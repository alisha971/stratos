# Create this file: insightbridge/mcp/adapters/tavily_adapter.py

import os
from tavily import TavilyClient
from typing import List, Dict, Any

# Initialize the client once, when the file is loaded
tavily_client = None
if TavilyClient is not None:
    try:
        tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    except Exception as e:
        print(f"[tavily_adapter] Could not init TavilyClient: {e}")


def tavily_search(query: str, include_images: bool = False, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Run Tavily search and return list of result objects:
    { title, url, content, images: [...], score }
    """
    print(f"\n[Tool: Tavily] Searching for: '{query}' (include_images={include_images})")
    if tavily_client is None:
        print("[Tool: Tavily] Tavily client not configured. Returning placeholder.")
        return [{
            "title": f"Placeholder result for {query}",
            "url": "",
            "content": f"No tavily client configured. Query was: {query}",
            "images": [],
            "score": 0.0
        }]

    try:
        result = tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            include_images=include_images
        )
        results = []
        for obj in result.get("results", []):
            images = obj.get("images", []) if include_images else []
            results.append({
                "title": obj.get("title") or obj.get("heading") or "",
                "url": obj.get("url") or obj.get("link") or "",
                "content": obj.get("content") or obj.get("snippet") or "",
                "images": images,
                "score": float(obj.get("score") or 0.0)
            })
        return results
    except Exception as e:
        print(f"[Tool: Tavily] ERROR: {e}")
        return [{
            "title": "Error",
            "url": "",
            "content": f"Error in Tavily search: {e}",
            "images": [],
            "score": 0.0
        }]