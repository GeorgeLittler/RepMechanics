import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("NEBIUS_API_KEY")
if not api_key:
    raise RuntimeError("NEBIUS_API_KEY is missing from .env")

client = OpenAI(
    api_key=api_key,
    base_url=os.getenv("NEBIUS_BASE_URL"),
)

response = client.chat.completions.create(
    model=os.getenv("NEBIUS_MODEL"),
    messages=[
        {
            "role": "system",
            "content": (
                "You are a biomechanics assistant. "
                "Explain exercise mechanics accurately and concisely."
            ),
        },
        {
            "role": "user",
            "content": (
                "In one sentence, explain why a dumbbell curl "
                "has its greatest external elbow torque when "
                "the forearm is horizontal."
            ),
        },
    ],
    max_tokens=2048,
)

print(response.choices[0].message.content)