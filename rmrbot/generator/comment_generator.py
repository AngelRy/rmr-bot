import os
from openai import OpenAI


SYSTEM_PROMPT = (
    "You write thoughtful follow-up comments under Facebook posts for a community "
    "of distance runners. Expand slightly on the idea of the quote and encourage "
    "reflection or discussion. Keep the tone reflective and authentic. "
    "Write 1–2 sentences only."
)


def generate_first_comment(quote: str):

    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
    )

    user_prompt = f"""
Quote:
{quote}

Write a short follow-up comment that expands on the idea of the quote and invites reflection.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=80,
    )

    return response.choices[0].message.content.strip()