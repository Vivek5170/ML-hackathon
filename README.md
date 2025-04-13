# Reddit Confession Chatbot

This project is a Reddit-style confession search chatbot that uses Natural Language Processing (NLP) and TF-IDF-based semantic search. It allows users to ask natural language queries and receive relevant confessions pulled from Reddit, including titles, body text, and comments.

Once initialized, the chatbot functions completely offline, making it fast, efficient, and privacy-friendly.

![App UI](https://drive.google.com/uc?export=view&id=1FUllk60rRr-tV-bTy0SgE8T242_i31_r)

---

## Features

- Semantic search across Reddit confessions using TF-IDF and WordNet
- Offline functionality after initial data scraping
- Smart indexing of title, body, and comments for better relevance
- Desktop interface built using Electron
- Clean and customizable UI
- Modular Python backend with extendable components

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/reddit-confession-chatbot.git
cd reddit-confession-chatbot
```

### 2. Python Setup

Install the required Python libraries:

```bash
pip install python-dotenv praw nltk scikit-learn
```

### 3. Reddit API Credentials

To scrape confessions from Reddit, you must create a Reddit API app:

1. Visit [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Choose **script** as the application type
4. Fill out the form:
   - Name: Any name
   - Redirect URI: `http://localhost`
5. Note down:
   - `client_id` (displayed under the app name)
   - `client_secret`

Now create a `.env` file in the root directory with the following format:

```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_SECRET=your_secret_here
REDDIT_USER_AGENT=YourAppName/1.0 by your_username
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
```

> **Important**: Never share or commit this `.env` file. It contains sensitive credentials.

---

## Scrape Confessions

Run the scraper to collect Reddit posts and store them locally:

```bash
python scrapper.py
```

You only need to do this once. The chatbot will then work fully offline.

---

## Running the Chatbot Interface

Install frontend dependencies and start the Electron app:

```bash
npm install
npm start
```

This will launch the chatbot interface where you can type questions and receive relevant responses.

---

## Technologies Used

- Python 3
- PRAW (Python Reddit API Wrapper)
- NLTK for text cleaning and synonyms
- Scikit-learn for TF-IDF vectorization
- Electron for desktop interface
- dotenv for environment variable management

---