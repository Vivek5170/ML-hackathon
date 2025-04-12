import json
import random
import re


with open('C:/Users/HP/Desktop/ML/ML-hackathon/results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

matched = data['matched']

openings = [
    "Some childhood confessions people have dropped over the years:",
    "Turns out, kids have always been a little mischievous. Check these out:"
]

closings = [
    "Guess childhood wasn’t as innocent as it seemed.",
    "Makes you wonder what else people never confessed."
]

paraphrase_templates = [
    "There’s a story about a person who {}",
    "Apparently, someone {}",
    "One person remembered how they {}",
    "Once, someone {}",
    "A childhood memory involved someone who {}"
]

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
    # Fix verb tense for 'remember' and 'feel'
    text = re.sub(r"\bthey remember\b", "they remembered", text)
    text = re.sub(r"\bthey feel\b", "they felt", text)
    text = text[0].lower() + text[1:] if text else text
    return text

def generate_response(matched):
    response = random.choice(openings) + "\n\n"
    selected = random.sample(matched, min(6, len(matched)))  # No duplicates now

    for confession in selected:
        body = convert_pronouns(confession['body'])
        paraphrased = random.choice(paraphrase_templates).format(body)
        if confession.get('comments'):
            comment = random.choice(confession['comments'])
            combined = f"{paraphrased}. Someone even remarked, \"{comment}\"."
        else:
            combined = paraphrased + "."

        response += f"• {combined}\n"

    response += "\n" + random.choice(closings)
    return response

final_reply = generate_response(matched)
print(f"Bot:\n{final_reply}")