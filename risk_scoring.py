from typing import Dict
from detector.hidden_chars import list_hidden_chars, classify_zwj_usage
from detector.emoji_detector import analyze_emojis 
from detector.text_analysis import detect_keywords, analyze_sentiment

def score_hidden_chars(text: str) -> int:
    """Score hidden characters for risk."""
    hidden = list_hidden_chars(text)
    zwj_class = classify_zwj_usage(text)

    score = 0
    if hidden:
        score += 20  # any hidden char is suspicious
    if zwj_class == "SUSPICIOUS":
        score += 30

    return score


def score_emojis(text: str):
    """Score emoji usage for risk."""    
    emoji_report = analyze_emojis(text)
    score = 0

    if emoji_report["risk"] == "MEDIUM":
        score += 20
    elif emoji_report["risk"] == "HIGH":
        score += 40

    return score, emoji_report


def calculate_risk(text: str) -> dict:
    """Calculate unified risk score for a message."""
    base_score = 0

    # Hidden characters
    hidden_score = score_hidden_chars(text)
    if hidden_score > 0:
        hidden_score += 10   # increase weight slightly
    base_score += hidden_score

    # Keyword detection
    keywords = detect_keywords(text)   # returns a list
    keyword_score = 0
    for kw in keywords:
        if "(violence)" in kw:         # very high risk
            keyword_score += 60
        elif "(drugs)" in kw:          # medium risk
            keyword_score += 30
        elif "(fraud)" in kw:          # medium-high risk
            keyword_score += 40

    base_score += keyword_score

    # Emoji analysis
    emoji_score, emoji_report = score_emojis(text)
    if emoji_report["risk"] == "HIGH" and keywords:
        emoji_score += 10   # combo: emojis + keywords = more suspicious
    base_score += emoji_score

    # Sentiment analysis
    sentiment = analyze_sentiment(text)
    sentiment_score = 0
    if sentiment["label"] == "Negative":
        if any("(violence)" in kw for kw in keywords):
            sentiment_score = 20   # escalate threats
        else:
            sentiment_score = 10   # normal negativity
    base_score += sentiment_score

    # Clamp score 0–100
    total_score = min(100, base_score)

    # Final Risk Levels (cleaned-up)
    if total_score >= 70:
        level = "HIGH"
    elif total_score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "text": text,
        "total_score": total_score,
        "risk_level": level,
        "hidden_score": hidden_score,
        "emoji_score": emoji_score,
        "keyword_score": keyword_score,
        "sentiment_score": sentiment_score,
        "keywords": keywords,
        "sentiment": sentiment,
        "emoji_report": emoji_report,
    }
