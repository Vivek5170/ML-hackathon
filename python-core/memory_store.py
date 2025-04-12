import json
import os
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

DATA_FILE = "confessions.json"

def clean_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t not in string.punctuation]
    tokens = [t for t in tokens if t not in stopwords.words('english')]
    return ' '.join(tokens)

def load_confessions():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_confessions(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def add_confession(post):
    data = load_confessions()

    # Check for duplicate by ID
    if any(p["id"] == post["id"] for p in data):
        print(f"Confession {post['id']} already exists.")
        data.remove(post['id'])

    # Add cleaned text for search
    combined_text = post["title"] + " " + post["body"]
    post["clean_text"] = clean_text(combined_text)

    data.append(post)
    save_confessions(data)
    print(f"Added confession {post['id']}.")

def add_confession(post):
    data = load_confessions()

    # Find if a confession with the same ID exists
    existing_post_index = next((i for i, p in enumerate(data) if p["id"] == post["id"]), None)

    combined_text = post["title"] + " " + post["body"]
    post["clean_text"] = clean_text(combined_text)
    # If it exists, replace it
    if existing_post_index is not None:
        data[existing_post_index] = post
        print(f"Replaced confession {post['id']}.")
    else:
        # Add cleaned text for search
        data.append(post)
        print(f"Added new confession {post['id']}.")

    save_confessions(data)
