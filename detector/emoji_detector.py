
from collections import Counter
from detector.emoji_rules import extract_emojis
from detector.emoji_patterns import CATEGORIES, RULES


def check_suspicious_patterns(text: str):
    
    emojis = set(extract_emojis(text))
    matches = []

    for categories, meaning in RULES:
        if all(any(e in emojis for e in CATEGORIES[cat]) for cat in categories):
            matches.append(meaning)

    return matches


def emoji_anomaly_score(text: str) -> dict:

    emojis = extract_emojis(text)
    emoji_count = len(emojis)
    text_len = len(text)
    ratio = emoji_count / text_len if text_len > 0 else 0
    unique_emojis = set(emojis)
    diversity = len(unique_emojis) / emoji_count if emoji_count else 0

    anomalies = []

    if emoji_count == text_len and emoji_count > 0:
        anomalies.append("Emoji-only message")

    if emoji_count > 5:
        anomalies.append(f"High emoji count ({emoji_count})")

    if ratio > 0.5:
        anomalies.append(f"Emoji-heavy ratio ({ratio:.2f})")

    if diversity > 0.5 and emoji_count > 3:
        anomalies.append("Diverse emojis (potential code)")

    return {
        "emoji_count": emoji_count,
        "emoji_ratio": round(ratio, 2),
        "emoji_diversity": round(diversity, 2),
        "anomalies": anomalies
    }


def analyze_emojis(text: str) -> dict:
   
    patterns = check_suspicious_patterns(text)
    anomaly = emoji_anomaly_score(text)

    risk = "LOW"
    if patterns or "potential code" in " ".join(anomaly["anomalies"]):
        risk = "HIGH"
    elif anomaly["anomalies"]:
        risk = "MEDIUM"

    return {
        "text": text,
        "patterns": patterns,
        "anomaly": anomaly,
        "risk": risk
    }
