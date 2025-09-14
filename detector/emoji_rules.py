import emoji

def extract_emojis(text: str) -> str:
    return "".join(ch for ch in text if ch in emoji.EMOJI_DATA)
