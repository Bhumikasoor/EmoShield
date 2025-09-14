import re
import emoji

ZERO_WIDTH = ["\u200b", "\u200c", "\u200d", "\ufeff"]

def unescape_unicode_escapes(s: str) -> str:
    """Convert literal sequences like '\\u200d' into real Unicode characters."""
    s = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)
    s = re.sub(r'\\U([0-9a-fA-F]{8})', lambda m: chr(int(m.group(1), 16)), s)
    s = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), s)
    return s

def remove_zero_width(s: str) -> str:
    """Remove zero-width characters (for keyword detection)."""
    for z in ZERO_WIDTH:
        s = s.replace(z, "")
    return s

def is_whitelisted_zwj_emoji(emo_text: str) -> bool:
    """Check if emoji is a safe family/people type sequence."""
    dem = emoji.demojize(emo_text)
    safe_keywords = ["family", "man", "woman", "girl", "boy", "people", "person", "heart"]
    return any(k in dem for k in safe_keywords)
