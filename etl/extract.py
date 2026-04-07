import requests
import feedparser

ARXIV_URL = "http://export.arxiv.org/api/query"


def fetch_papers(query, max_results=20, start=0):
    """
    Fetch research papers from arXiv API.

    Args:
        query (str): Search keyword
        max_results (int): Number of papers to fetch
        start (int): Pagination offset

    Returns:
        list[dict]: Raw paper data
    """

    params = {
        "search_query": f"all:{query}",
        "start": start,
        "max_results": max_results
    }

    try:
        response = requests.get(ARXIV_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch data: {e}")
        return []

    feed = feedparser.parse(response.text)

    papers = []
    for entry in feed.entries:
        paper = {
            "title": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "published": entry.get("published", ""),
            "authors": [author.name for author in entry.get("authors", [])],
            "link": entry.get("link", ""),
            "categories": entry.get("tags", [])
        }
        papers.append(paper)

    print(f"[INFO] Fetched {len(papers)} papers from arXiv")
    return papers