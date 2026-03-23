from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

response = client.chat.completions.create(
    model="mistralai/mistral-7b-instruct:free",
            messages=[{"role": "user", "content": "Write one motivational sentence about running."}]
)

print(response.choices[0].message.content)