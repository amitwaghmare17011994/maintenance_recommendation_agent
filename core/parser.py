from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()


def parse_report(text: str) -> str:
    """
    Use LLM to extract machine data
    """

    prompt = f"""
Extract machine information from the report.

Return JSON with keys:
machine_id
temperature
vibration
last_service
issue

Report:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content