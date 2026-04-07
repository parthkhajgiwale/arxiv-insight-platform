from db.db import get_connection

def load_papers(papers):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO papers (title, summary, authors, published, link, topic)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    for p in papers:
        cursor.execute(query, (
            p["title"],
            p["summary"],
            p["authors"],
            p["published"],  # YYYY-MM-DD
            p["link"],
            p["topic"]
        ))

    conn.commit()
    cursor.close()
    conn.close()