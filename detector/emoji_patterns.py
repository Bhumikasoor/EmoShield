
from detector.emoji_rules import extract_emojis

CATEGORIES = {
    "plant": {"🍀", "🌿", "🍃", "🌱", "🌴", "🍁"},
    "smoke": {"💨", "🔥", "😮‍💨", "🚬"},
    "pills": {"💊", "🍬", "🟣", "🧪"},
    "injection": {"💉", "🩸", "🧬", "🪡"},
    "mushroom": {"🍄"},
    "weapons": {"🔫", "🔪", "💣", "🧨"},
    "alcohol": {"🍺", "🍷", "🥃"},
    "money": {"💵", "💰", "🪙"}
}

RULES = [
    (["plant", "smoke"], "Marijuana / Weed"),
    (["pills"], "Pills / Ecstasy"),
    (["injection"], "Injection / Drugs"),
    (["mushroom"], "Mushrooms / Psychedelics"),
    (["weapons", "money"], "Illegal deals / Arms trade"),
    (["alcohol"], "Alcohol reference"),
]

