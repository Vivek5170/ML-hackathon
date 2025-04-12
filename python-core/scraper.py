import praw
from dotenv import load_dotenv
import os
from memory_store import add_confession

# Load environment variables
load_dotenv()
print(os.getenv("REDDIT_CLIENT_ID"))
print(os.getenv("REDDIT_SECRET"))
print(os.getenv("REDDIT_USER_AGENT"))

# Get credentials
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD
)

print(f"Reddit API connected as: {reddit.user.me()}")

# Subreddits
subreddits_bits = ["bitspilani", "BITSPilani", "Indian_Academia", "BITSians_withADHD", "Btechtards"]
subreddit_relationships = ["collegeconfessions", "collegeLife", "relationship_advice", "hyderabad", "indianstudents"]
subreddit_health = ["depression", "Anxiety"]
subreddit_tier2 = ["developersIndia", "gradschool", "AskAcademia", "INDIA", "academia", "IndiaHacks", "indianstudents"]

# Keywords
keywords = [k.lower() for k in [
    "mess", "ragging", "fd", "attendance", "professor", "grades", "course", "academic pressure",
    "thesis", "project", "final year", "assignments", "hostel", "freshers", "fest", "club",
    "clubs", "recruitment", "drama", "crush", "confession", "relationship", "broke up",
    "mental health", "anxiety", "stress", "PS", "PS1", "PS2", "practice school", "internship"
]]

def mentions_bits(text):
    campuses = ["bits pilani", "bits goa", "bits hyderabad", "birla", "ps1", "ps2", "practice school"]
    return any(c in text for c in campuses)

results = []

# 🟢 Main scraping loop
def scrape_subreddit(subreddit_name, search_query):
    print(f"Searching in r/{subreddit_name}")
    subreddit = reddit.subreddit(subreddit_name)
    for post in subreddit.search(search_query, sort="relevance", time_filter="all", limit=300):
        title = post.title.strip()
        body = post.selftext.strip()
        post_text = f"{title} {body}".lower()
        
        if any(k in post_text for k in keywords):
            post_data = {
                "id": post.id,
                "title": title,
                "body": body,
                "comments": []
            }
            post.comments.replace_more(limit=0)
            for comment in post.comments[:5]:
                post_data["comments"].append(comment.body.strip())
            results.append(post_data)

# Run for different subreddit groups
for sub in subreddits_bits:
    scrape_subreddit(sub, "bits pilani OR bits goa OR bits hyderabad OR PS OR PS1 OR PS2 OR mess food OR birla")

for sub in subreddit_relationships:
    scrape_subreddit(sub, "university OR college")

for sub in subreddit_health:
    scrape_subreddit(sub, "college OR exam OR university ")

for sub in subreddit_tier2:
    print(f"Searching in r/{sub}")
    subreddit = reddit.subreddit(sub)
    for post in subreddit.search("bits pilani OR bits goa OR bits hyderabad OR PS OR PS1 OR PS2 OR birla", sort="relevance", time_filter="all", limit=100):
        title = post.title.strip()
        body = post.selftext.strip()
        post_text = f"{title} {body}".lower()

        if mentions_bits(post_text) and any(k in post_text for k in keywords):
            post_data = {
                "id": post.id,
                "title": title,
                "body": body,
                "comments": []
            }
            post.comments.replace_more(limit=0)
            for comment in post.comments[:5]:
                post_data["comments"].append(comment.body.strip())
            results.append(post_data)


for post in results:
    add_confession(post)