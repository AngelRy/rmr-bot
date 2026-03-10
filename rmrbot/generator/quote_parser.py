import re


def parse_quote(raw: str) -> dict:
    """
    Robustly parses quote text and author.
    Extracts human author names and removes book titles and site artifacts.
    """

    if not raw:
        return {"quote": "", "author": None}

    text = raw.strip()

    # Normalize dash variants
    text = text.replace("—", "―").replace("–", "―")

    quote = text
    author = None

    # Split quote and author
    if "―" in text:
        quote_part, author_part = text.split("―", 1)
        quote = quote_part.strip(' "\n')
        author_raw = author_part.strip()
    else:
        quote = text.strip(' "\n')
        author_raw = ""

    # Normalize whitespace inside quote
    quote = re.sub(r"\s+", " ", quote).strip()

    if author_raw:
        # Remove zero-width and non-breaking spaces
        author_raw = author_raw.replace("\u200b", "").replace("\xa0", " ")

        # Remove Goodreads junk
        author_raw = re.split(
            r"(tags:|likes\b|Like$|\d+\s*likes)",
            author_raw,
            flags=re.IGNORECASE,
        )[0]

        # --- CRITICAL FIX ---
        # Extract a plausible human name (2–4 words)
        match = re.search(
            r"\b([A-Z][a-z]+(?:\s+(?:Mc|Mac)?[A-Z][a-z]+){0,3})\b",
            author_raw,
        )

        if match:
            author = match.group(1).strip()
        else:
            author = None

        # Normalize Mc / Mac spacing
        if author:
            author = re.sub(r"\b(Mc|Mac)\s+([A-Z])", r"\1\2", author)

        # Final sanity check
        if not author or len(author) > 60:
            author = None

    return {
        "quote": quote,
        "author": author,
    }
