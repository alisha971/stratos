import requests
from bs4 import BeautifulSoup

def read_webpage(url: str, include_images: bool = False) -> list:
    print(f"\n[Tool: WebReader] Reading: {url}")

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        text = ' '.join(t.strip() for t in soup.stripped_strings)

        return [{
            "title": "Webpage Content",
            "url": url,
            "content": text[:4000],
            "source": "web_reader",
            "images": []
        }]

    except Exception as e:
        print(f"[Tool: WebReader] ERROR: {e}")
        return []
