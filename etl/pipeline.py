from etl.extract import fetch_papers
from etl.transform import clean_papers
from etl.load import load_papers
from etl.topic_model import extract_topics

def run_pipeline():
    papers = fetch_papers("deep learning", 50)
    cleaned = clean_papers(papers)

    # Extract topics
    summaries = [p["summary"] for p in cleaned]
    topics = extract_topics(summaries)

    # attach topics
    for i, p in enumerate(cleaned):
        p["topic"] = topics[i % len(topics)]

    load_papers(cleaned)
    print("Pipeline executed successfully!")

if __name__ == "__main__":
    run_pipeline()