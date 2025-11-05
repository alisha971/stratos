# Create this file: insightbridge/mcp/adapters/gnews_adapter.py

from gnews import GNews

# Initialize the client once
gnews_client = GNews(language='en', country='US', max_results=5)

def gnews(query: str) -> list:
    """Searches Google News and returns a list of articles."""
    print(f"\n[Tool: GNews] Searching for: '{query}'")
    try:
        articles = gnews_client.get_news(query)
        results = []
        for article in articles:
            result_str = (
                f"ARTICLE_TITLE: {article['title']}\n"
                f"SOURCE: {article['publisher']['title']}\n"
                f"URL: {article['url']}"
            )
            results.append(result_str)
        return results
    except Exception as e:
        print(f"[Tool: GNews] ERROR: {e}")
        return [f"Error in GNews search: {e}"]