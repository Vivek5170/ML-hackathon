import json
import random
import re
from search import search  # assuming search function is in search.py

# Load confessions from the JSON file

# More formal openings and closings
openings = [
    "Here are some reflections from confessions:",
    "Below are some insights from personal experiences shared by others:",
    "Some memories from people's pasts that they have revealed:",
    "A few confessions from that might surprise you:",
    "Here are a few notable confessions:"
]

closings = [
    "It seems that childhood was not as innocent as we remember.",
    "Such confessions shed light on the more mischievous side of us.",
    "These stories remind us of the unpredictable nature of growing up.",
    "It’s fascinating to see how memories from childhood evolve over time.",
    "These stories offer a glimpse into the complexities of life."
]

# Paraphrase templates
paraphrase_templates = [
    "There’s a story about a person who {}",
    "Apparently, someone {}",
    "One person remembered how they {}",
    "Once, someone {}",
    "A memory involved someone who {}"
]

# Pronoun conversion rules
pronoun_map = {
    r"\bmy\b": "their",
    r"\bmine\b": "theirs",
    r"\bme\b": "them",
    r"\bi\b": "they",
    r"\bI\b": "they",
    r"\bus\b": "them",
    r"\bour\b": "their",
    r"\bours\b": "theirs",
    r"\bwe\b": "they"
}

def convert_pronouns(text):
    for pattern, replacement in pronoun_map.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    text = re.sub(r"\bthey remember\b", "they remembered", text)
    text = re.sub(r"\bthey feel\b", "they felt", text)
    text = text[0].lower() + text[1:] if text else text
    return text

def generate_response(user_query):
    result = search(user_query)
    matched = result.get("matches", [])
    if not matched:
        return "Sorry, I couldn't find any related confessions."

    response = random.choice(openings) + "\n\n"
    selected = matched[:min(6, len(matched))]  # Top 6 in ranked order

    for confession in selected:
        body = convert_pronouns(confession['body'])
        paraphrased = random.choice(paraphrase_templates).format(body)

        # Include 1-5 comments if available
        if confession.get('comments'):
            available_comments = confession['comments']
            num_comments = random.randint(1, min(5, len(available_comments)))
            comments = random.sample(available_comments, num_comments)

            comment_intros = [
                "Someone remarked,",
                "Another person said,",
                "One comment read,",
                "A reply stated,",
                "An observer noted,"
            ]

            comments_text = " ".join([
                f"{random.choice(comment_intros)} \"{comment.strip()}\""
                for comment in comments
            ])

            combined = f"{paraphrased}. {comments_text}."
        else:
            combined = paraphrased + "."

        response += f"• {combined}\n"

    response += "\n" + random.choice(closings)
    return response


if __name__ == "__main__":
    import sys
    query = sys.argv[1]
    print(generate_response(query))