from sklearn.feature_extraction.text import TfidfVectorizer
import spacy

# Load the spaCy model once globally
nlp = spacy.load('en_core_web_sm')

def extract_keywords(text):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = X.sum(axis=0).A1
    tfidf_scores_dict = dict(zip(feature_names, tfidf_scores))
    keywords = [word for word, score in sorted(tfidf_scores_dict.items(), key=lambda x: x[1], reverse=True)[:50]]
    return keywords

def extract_entities(text):
    doc = nlp(text)
    entities = [entity.text.lower() for entity in doc.ents]
    return entities

def recommend_ads(text, ad_topic_mapping):
    # Extract keywords using TF-IDF
    keywords = extract_keywords(text)

    # Extract named entities using spaCy
    entities = extract_entities(text)

    # Generate ad topics
    ad_topics = set()
    for keyword in keywords:
        if keyword in ad_topic_mapping:
            ad_topics.add(ad_topic_mapping[keyword])
    for entity in entities:
        if entity in ad_topic_mapping:
            ad_topics.add(ad_topic_mapping[entity])

    return list(ad_topics)
