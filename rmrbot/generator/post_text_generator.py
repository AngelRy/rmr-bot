import os
import random
from rmrbot.config.settings import RUNNING_HASHTAGS
from openai import OpenAI


# Enable LLM only if API key exists
USE_LLM = bool(os.getenv("GROQ_API_KEY"))

'''
SYSTEM_PROMPT = (
    "You write concise, thoughtful social media captions for distance runners. "
    "The tone is reflective, grounded, and authentic. "
    "Avoid clichés, emojis, and hashtags. "
    "Write 2–3 sentences only."
)
'''

SYSTEM_PROMPT = (
    "You write thoughtful Facebook captions for a community of distance runners. "
    "The caption reflects on the deeper meaning of the quote and connects it to the mindset "
    "of running, discipline, patience, and long-term progress. "
    "Frame the reflection so that experienced runners recognize themselves in it. "
    "Focus on habits, struggles, or quiet moments runners experience during training. "
    "Tone is reflective, authentic, and grounded — never motivational hype. "
    "Avoid clichés, emojis, and hashtags. "
    "Write 2–3 sentences only. "
    "The caption should add perspective to the quote rather than repeat it. "
    "Occasionally end with a subtle question that invites runners to share their experience."
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
        client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=160,
        )

        caption = response.choices[0].message.content.strip()
        return append_hashtags(caption)

    except Exception:
        # Any API failure → fallback
        return _fallback_caption(quote, author)