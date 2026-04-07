from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF


def extract_topics(texts, n_topics=5):
    vectorizer = TfidfVectorizer(
        max_df=0.95,
        min_df=2,
        stop_words='english'
    )

    tfidf = vectorizer.fit_transform(texts)

    model = NMF(n_components=n_topics, random_state=42)
    model.fit(tfidf)

    words = vectorizer.get_feature_names_out()

    topics = []
    for topic_idx, topic in enumerate(model.components_):
        top_words = [words[i] for i in topic.argsort()[-5:]]
        topics.append(", ".join(top_words))

    return topics