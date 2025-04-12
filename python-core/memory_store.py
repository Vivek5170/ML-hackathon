import json
import os
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

DATA_FILE = "C:/Users/yakka/Desktop/VScode_Files/hackathon/ML-hackathon/confessions.json"

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

    if any(p["id"] == post["id"] for p in data):
        print(f"Confession {post['id']} already exists.")
        data.remove(post['id'])

    combined_text = post["title"] + " " + post["body"]
    post["clean_text"] = clean_text(combined_text)

    data.append(post)
    save_confessions(data)
    print(f"Added confession {post['id']}.")

def add_confession(post):
    data = load_confessions()

    existing_post_index = next((i for i, p in enumerate(data) if p["id"] == post["id"]), None)

    comments_text = " ".join(post.get("comments", []))
    combined_text = f"{post['title']} {post['body']} {comments_text}"
    post["clean_text"] = clean_text(combined_text)
    if existing_post_index is not None:
        data[existing_post_index] = post
        print(f"Replaced confession {post['id']}.")
    else:
        data.append(post)
        print(f"Added new confession {post['id']}.")

    save_confessions(data)
