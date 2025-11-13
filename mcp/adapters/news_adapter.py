from gnews import GNews

gnews_client = GNews(language='en', country='US', max_results=5)

def gnews(query: str, include_images: bool = False) -> list:
    print(f"\n[Tool: GNews] Searching for: '{query}'")
    try:
        articles = gnews_client.get_news(query)
        results = []
        for article in articles:
            results.append({
                "title": article['title'],
                "url": article['url'],
                "content": article['description'],
                "source": article['publisher']['title'],
                "images": []
            })
        return results
    except Exception as e:
        print(f"[Tool: GNews] ERROR: {e}")
        return []
