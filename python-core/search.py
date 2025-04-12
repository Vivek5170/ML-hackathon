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
    # Load confessions
    data = load_confessions()

    # Extract the clean text (already processed) for search comparison
    corpus = [post['clean_text'] for post in data]

    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the corpus to get the term frequencies
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Transform the query to the same vector space
    query_tfidf = vectorizer.transform([query])

    # Compute similarity scores
    cosine_similarities = (tfidf_matrix * query_tfidf.T).toarray()

    # Find the indexes of the top matching posts (highest cosine similarity)
    matched_indexes = cosine_similarities.flatten().argsort()[-5:][::-1]  # Top 5 matches

    # Get matched posts
    matched_posts = [data[i] for i in matched_indexes]

    # Extract related keywords from the query and the matched posts (optional)
    related_keywords = set(vectorizer.get_feature_names_out())
    related_keywords = list(related_keywords)

    # Format the result
    result = {
        "query": query,
        "matches": [
            {
                "title": post["title"],
                "body": post["body"],
                "comments": post["comments"]
            } for post in matched_posts
        ],
        "related_keywords": related_keywords
    }

    return result
