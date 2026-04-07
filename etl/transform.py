from datetime import datetime


def clean_text(text):
    """Basic text cleaning"""
    if not text:
        return ""
    return " ".join(text.strip().replace("\n", " ").split())


def parse_date(date_str):
    """Convert arXiv date string to YYYY-MM-DD"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").date()
    except Exception:
        return None


def extract_categories(tags):
    """Extract category terms from tag objects"""
    if not tags:
        return ""
    return ", ".join(tag["term"] for tag in tags)


def clean_papers(papers):
    """
    Transform raw arXiv data into clean structured format.

    Args:
        papers (list): Raw papers from extract step

    Returns:
        list[dict]: Cleaned papers
    """

    cleaned = []

    for p in papers:
        cleaned.append({
            "title": clean_text(p.get("title")),
            "summary": clean_text(p.get("summary")),
            "authors": ", ".join(p.get("authors", [])),
            "published": parse_date(p.get("published")),
            "link": p.get("link"),
            "categories": extract_categories(p.get("categories"))
        })

    print(f"[INFO] Transformed {len(cleaned)} papers")
    return cleaned