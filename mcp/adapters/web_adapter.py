# Create this file: insightbridge/mcp/adapters/web_adapter.py

import requests
from bs4 import BeautifulSoup

def read_webpage(url: str) -> str:
    """Reads the text content of a single webpage URL."""
    print(f"\n[Tool: WebReader] Reading: {url}")
    try:
        # Set headers to mimic a real browser
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise error for bad responses
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get all text, strip whitespace, and join
        text = ' '.join(t.strip() for t in soup.stripped_strings)
        
        # Return first 4000 chars to avoid overloading the context
        return text[:4000]
    except Exception as e:
        print(f"[Tool: WebReader] ERROR: {e}")
        return f"Error reading URL {url}: {e}"