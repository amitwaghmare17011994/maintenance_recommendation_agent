from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

r = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "user", "content": "hello"}
    ]
)

print(r.choices[0].message.content)