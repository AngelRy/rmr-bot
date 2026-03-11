
import os
import random
from rmrbot.config.settings import RUNNING_HASHTAGS
from openai import OpenAI
client = OpenAI()

#USE_LLM = bool(os.getenv("OPENAI_API_KEY"))
USE_LLM = False
if USE_LLM:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    except Exception:
        USE_LLM = False


SYSTEM_PROMPT = (
    "You write concise, thoughtful social media captions for distance runners. "
    "The tone is reflective, grounded, and authentic. "
    "Avoid clichés, emojis, and hashtags. "
    "Write 2–3 sentences only."
)


def append_hashtags(text: str, k: int = 6) -> str:
    tags = random.sample(RUNNING_HASHTAGS, k=min(k, len(RUNNING_HASHTAGS)))
    return text.rstrip() + "\n\n" + " ".join(tags)


def _fallback_caption(quote: str, author: str | None = None) -> str:
    """
    Fallback caption: exact quote text.
    """
    base = quote
    return append_hashtags(base)


def generate_caption(quote: str, author: str | None = None) -> str:
    """
    Generate a short complementary caption.
    Uses LLM if available, otherwise falls back to a deterministic caption.
    """

    if not USE_LLM:
        return _fallback_caption(quote, author)

    user_prompt = f"Quote:\n{quote}\n"
    if author:
        user_prompt += f"\nAuthor: {author}\n"

    user_prompt += (
        "\nWrite a short complementary caption that expands on the idea of the quote "
        "without repeating it verbatim."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=120,
        )

        caption = response.choices[0].message.content.strip()
        return append_hashtags(caption)

    except Exception:
        # Any API failure → fallback
        return _fallback_caption(quote, author)
'''

import os
import random
from rmrbot.config.settings import RUNNING_HASHTAGS
from openai import OpenAI

USE_LLM = False
client = None

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        USE_LLM = True
    except Exception:
        USE_LLM = False  # disable LLM if import fails

SYSTEM_PROMPT = (
    "You write concise, thoughtful social media captions for distance runners. "
    "The tone is reflective, grounded, and authentic. "
    "Avoid clichés, emojis, and hashtags. "
    "Write 2–3 sentences only."
)

def append_hashtags(text: str, k: int = 6) -> str:
    tags = random.sample(RUNNING_HASHTAGS, k=min(k, len(RUNNING_HASHTAGS)))
    return text.rstrip() + "\n\n" + " ".join(tags)

def _fallback_caption(quote: str, author: str | None = None) -> str:
    """Fallback caption: exact quote text."""
    base = quote
    return append_hashtags(base)

def generate_caption(quote: str, author: str | None = None) -> str:
    """
    Generate a short complementary caption.
    Uses LLM if available, otherwise falls back to a deterministic caption.
    """
    if not USE_LLM or client is None:
        return _fallback_caption(quote, author)

    user_prompt = f"Quote:\n{quote}\n"
    if author:
        user_prompt += f"\nAuthor: {author}\n"
    user_prompt += "\nWrite a short complementary caption that expands on the idea of the quote without repeating it verbatim."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=120,
        )
        caption = response.choices[0].message.content.strip()
        return append_hashtags(caption)

    except Exception:
        # fallback if API fails for any reason
        return _fallback_caption(quote, author)
'''