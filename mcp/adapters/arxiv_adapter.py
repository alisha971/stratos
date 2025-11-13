import arxiv

def arxiv_search(query: str, include_images: bool = False) -> list:
    print(f"\n[Tool: ArXiv] Searching for: '{query}'")

    try:
        search = arxiv.Search(
            query=query,
            max_results=5,
            sort_by=arxiv.SortCriterion.Relevance
        )
        results = []

        for r in search.results():
            results.append({
                "title": r.title,
                "url": r.pdf_url,
                "content": r.summary,
                "source": "arxiv",
                "images": []
            })

        return results

    except Exception as e:
        print(f"[Tool: ArXiv] ERROR: {e}")
        return []
