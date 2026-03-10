import re


def clean(text: str) -> str:
    if not text:
        return ""

    # 1. Normalize HTML whitespace artifacts
    text = text.replace("\xa0", " ")

    # 2. Ensure spaces around ellipses
    text = re.sub(r"\.\.\.", " ... ", text)

    # 3. Remove smart quotes and normalize quotes
    text = text.replace("“", '"').replace("”", '"').replace("’", "'")

    # 4. Remove unwanted control characters
    text = re.sub(r"[\r\n\t]", " ", text)

    # 5. FIX: ensure word boundaries are preserved
    # Insert space between lowercase-uppercase or word-word collisions
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    text = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", text)
    text = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", text)

    # 6. Collapse multiple spaces AFTER all fixes
    text = re.sub(r"\s+", " ", text)

    return text.strip()
