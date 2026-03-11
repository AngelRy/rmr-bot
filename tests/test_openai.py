from openai import OpenAI

client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Write a short running motivation caption"}],
    max_tokens=40
)

print(resp.choices[0].message.content)