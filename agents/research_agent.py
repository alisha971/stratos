# stratos/agents/research_agent.py

from typing import Dict, List, Any
from orchestrator.state import AgentState, PlanStep
from mcp.governor import mcp_governor  # singleton that routes tool calls
import uuid
import pprint

def run_researcher_node(state: AgentState) -> Dict[str, Any]:
    """
    Execute plan steps (from PlannerAgent) by calling tools through MCPGovernor.
    Return a list of citation objects in the unified format:
      { id, title, url, summary, source, score, images }
    """
    print(f"\n--- [Node: ResearchAgent] ---")
    topic = state.get('topic', '')
    plan: List[PlanStep] = state.get('plan', [])
    print(f"Topic: {topic}")
    print(f"Plan steps: {len(plan)}")

    all_docs: List[Dict[str, Any]] = []

    for step in plan:
        tool_name = step.get("tool")
        query = step.get("query", topic)
        include_images = bool(step.get("include_images", False))

        print(f"[ResearchAgent] Running tool {tool_name} for query '{query}' (images={include_images})")

        # Build the tool_input according to tool capabilities
        try:
            if tool_name in ("tavily_search",):
                tool_input = {"query": query, "include_images": include_images}
                raw = mcp_governor.execute_tool("ResearchAgent", tool_name, tool_input)

            elif tool_name in ("pdf_rag_query",):
                # pdf_rag_query expects url + query - sometimes query is URL in plan
                # Accept both: if query looks like a URL, treat as url param
                if query.startswith("http://") or query.startswith("https://"):
                    tool_input = {"url": query, "query": step.get("query", topic), "include_images": include_images}
                else:
                    tool_input = {"url": step.get("url", ""), "query": query, "include_images": include_images}
                raw = mcp_governor.execute_tool("ResearchAgent", tool_name, tool_input)

            else:
                # gnews, arxiv_search, read_webpage, etc. accept a single string argument
                raw = mcp_governor.execute_tool("ResearchAgent", tool_name, query)

        except PermissionError as pe:
            print(f"[ResearchAgent] PERMISSION ERROR calling {tool_name}: {pe}")
            continue
        except Exception as e:
            print(f"[ResearchAgent] ERROR calling {tool_name}: {e}")
            continue

        # Normalize the result into list[dict] unified format
        # Acceptable raw forms:
        # - [] or list of dicts (preferred)
        # - list of strings
        # - single dict
        # - single string
        hits: List[Dict[str, Any]] = []

        if not raw:
            print(f"[ResearchAgent] Tool {tool_name} returned no results.")
            continue

        # If the governor returned an error string instead of raising, handle it
        if isinstance(raw, str):
            raw = [raw]

        if isinstance(raw, list) and len(raw) > 0 and isinstance(raw[0], dict):
            # Already good shape: list of dicts
            hits = raw
        else:
            # Convert list of strings or other items into dict entries
            iterable = raw if isinstance(raw, list) else [raw]
            for item in iterable:
                # If item is dict-like but not the expected shape, gracefully map fields
                if isinstance(item, dict):
                    hits.append({
                        "title": item.get("title", "") or item.get("heading", "") or "Untitled",
                        "url": item.get("url", "") or item.get("link", ""),
                        "content": item.get("content", "") or item.get("snippet", ""),
                        "source": item.get("source", tool_name),
                        "score": float(item.get("score", 0.0)) if item.get("score") is not None else 0.0,
                        "images": item.get("images", []) or []
                    })
                else:
                    # string or other -> put into content
                    hits.append({
                        "title": f"Snippet from {tool_name}",
                        "url": "",
                        "content": str(item),
                        "source": tool_name,
                        "score": 0.0,
                        "images": []
                    })

        # Filter/clean hits and append with a stable citation id
        for hit in hits:
            content = (hit.get("content") or "").strip()
            # skip empty content
            if not content:
                continue

            cid = str(uuid.uuid4())
            doc = {
                "id": cid,
                "title": (hit.get("title") or "")[:300],
                "url": hit.get("url", ""),
                "summary": content[:3000],
                "source": hit.get("source", tool_name),
                "score": float(hit.get("score", 0.0)) if hit.get("score") is not None else 0.0,
                "images": hit.get("images", []) or []
            }
            all_docs.append(doc)

    # Deduplicate by (url, summary prefix) to avoid repeated identical hits
    seen = set()
    deduped = []
    for d in all_docs:
        key = (d.get("url", ""), d.get("summary", "")[:200])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(d)

    print(f"ResearchAgent found {len(deduped)} documents.")
    if len(deduped) < 1:
        pprint.pprint({"warning": "no documents collected", "topic": topic})

    return {
        "documents": deduped,
        "iteration_count": state.get("iteration_count", 0) + 1
    }
