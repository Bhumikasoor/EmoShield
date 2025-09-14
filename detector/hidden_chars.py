
import unicodedata
import re
from typing import List, Tuple

HIDDEN_CODEPOINTS = {
    0x200B: "ZERO WIDTH SPACE",
    0x200C: "ZERO WIDTH NON-JOINER",
    0x200D: "ZERO WIDTH JOINER",
    0x2060: "WORD JOINER",
    0xFE0F: "VARIATION SELECTOR-16"
}

def list_hidden_chars(text: str) -> List[Tuple[int, str, str]]:
   
    found = []
    for i, ch in enumerate(text):
        cp = ord(ch)
        if cp in HIDDEN_CODEPOINTS:
            found.append((i, ch, HIDDEN_CODEPOINTS[cp]))
    return found


def strip_hidden_chars(text: str) -> str:
    """Remove all hidden/invisible characters from the text."""
    return "".join(ch for ch in text if ord(ch) not in HIDDEN_CODEPOINTS)


def normalize_text(text: str) -> str:
    """
    Normalize text (NFKC) and strip hidden characters.
    This prevents attackers from using Unicode variations.
    """
    nfkc = unicodedata.normalize("NFKC", text)
    return strip_hidden_chars(nfkc)


def classify_zwj_usage(text: str) -> str:
    """
    Classify ZWJ usage as SAFE, SUSPICIOUS, or NO_ZWJ using heuristics.
    - Safe: typical emoji combos (👍‍🔥, family 👨‍👩‍👧).
    - Suspicious: ZWJ inside plain words, too many ZWJs, or unusual patterns.
    """
    if "\u200d" not in text:
        return "NO_ZWJ"

    # Heuristic 1: suspicious if too many ZWJs
    if text.count("\u200d") > 2:
        return "SUSPICIOUS"

    # Heuristic 2: suspicious if ZWJ is used between letters/numbers
    if re.search(r"[a-zA-Z0-9]\u200d[a-zA-Z0-9]", text):
        return "SUSPICIOUS"

    # Otherwise, assume safe emoji use
    return "SAFE"
