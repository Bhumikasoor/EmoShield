import re
from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Suspicious keywords dictionary (expandable)
SUSPICIOUS_KEYWORDS = {
    "drugs": ["weed", "coke", "lsd", "pill", "ganja", "dope", "ecstasy"],
    "violence": ["kill", "shoot", "attack", "murder", "bomb", "knife"],
    "fraud": ["scam", "hack", "phish", "fraud", "steal"],
}

def detect_keywords(text: str) -> list:
    """Check text for suspicious keywords using whole word matching."""
    found = []
    lower_text = text.lower()

    for category, words in SUSPICIOUS_KEYWORDS.items():
        for word in words:
            # \b ensures match only full words (not substrings)
            if re.search(rf"\b{re.escape(word)}\b", lower_text):
                found.append(f"{word} ({category})")

    return found


def analyze_sentiment(text: str) -> dict:
    """Analyze sentiment of text using VADER."""
    scores = sia.polarity_scores(text)
    
    # Decide sentiment label
    if scores["compound"] >= 0.5:
        label = "Positive"
    elif scores["compound"] <= -0.5:
        label = "Negative"
    else:
        label = "Neutral"

    return {"label": label, "scores": scores}
