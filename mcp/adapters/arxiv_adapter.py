# Create this file: insightbridge/mcp/adapters/arxiv_adapter.py

import arxiv

def arxiv_search(query: str) -> list:
    """Searches ArXiv and returns a list of paper summaries & URLs."""
    print(f"\n[Tool: ArXiv] Searching for: '{query}'")
    try:
        search = arxiv.Search(
            query=query,
            max_results=3, # Keep it focused
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = []
        for r in search.results():
            result_str = (
                f"PAPER_TITLE: {r.title}\n"
                f"PUBLISHED: {r.published.date()}\n"
                f"URL: {r.pdf_url}\n"
                f"SUMMARY: {r.summary}"
            )
            results.append(result_str)
        return results
    except Exception as e:
        print(f"[Tool: ArXiv] ERROR: {e}")
        return [f"Error in ArXiv search: {e}"]