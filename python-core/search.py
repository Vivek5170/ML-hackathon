import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from memory_store import load_confessions
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize


nltk.download('punkt')
nltk.download('wordnet')

def expand_query_with_synonyms(query):
    tokens = word_tokenize(query.lower())
    expanded_tokens = set(tokens)

    for word in tokens:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                if "_" not in lemma.name():
                    expanded_tokens.add(lemma.name().lower())

    return " ".join(expanded_tokens)



def search(query):
    expanded_query = expand_query_with_synonyms(query)

    data = load_confessions()
    corpus = [post['clean_text'] for post in data]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    query_tfidf = vectorizer.transform([expanded_query])
    cosine_similarities = (tfidf_matrix * query_tfidf.T).toarray()
    matched_indexes = cosine_similarities.flatten().argsort()[-5:][::-1]
    matched_posts = [data[i] for i in matched_indexes if cosine_similarities[i] > 0.01]

    related_keywords = set(expanded_query.split())
    result = {
        "query": query,
        "matches": [
            {
                "title": post["title"],
                "body": post["body"],
                "comments": post["comments"]
            } for post in matched_posts
        ],
        "related_keywords": list(related_keywords)
    }

    return result
