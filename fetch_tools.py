import requests
from datetime import datetime, timedelta
from utils import clean_title

AI_KEYWORDS = ["ai", "gpt", "llm", "agent", "rag", "chatbot", "ml model", "neural"]


def fetch_new_ai_tools(hours_back=24):
    """
    Fetch AI-related 'Show HN' launches from the last N hours.
    Uses the Hacker News Algolia API - free, no API key required.
    """
    since_ts = int((datetime.utcnow() - timedelta(hours=hours_back)).timestamp())
    url = "http://hn.algolia.com/api/v1/search_by_date"
    params = {
        "tags": "show_hn",
        "query": "AI",
        "numericFilters": f"created_at_i>{since_ts}",
        "hitsPerPage": 50,
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    hits = resp.json().get("hits", [])

    tools = []
    for hit in hits:
        title = hit.get("title", "")
        title_lower = title.lower()
        # Extra filter since HN's search is fuzzy - keep only clearly AI-related titles
        if not any(kw in title_lower for kw in AI_KEYWORDS):
            continue
        tools.append({
            "id": hit["objectID"],
            "title": clean_title(title),
            "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit['objectID']}",
            "hn_link": f"https://news.ycombinator.com/item?id={hit['objectID']}",
            "points": hit.get("points", 0),
            "created_at": hit.get("created_at"),
        })
    return tools


if __name__ == "__main__":
    # Quick manual test: python fetch_tools.py
    for t in fetch_new_ai_tools(hours_back=72):
        print(t["title"], "->", t["url"])