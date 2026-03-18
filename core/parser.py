from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()


def parse_report(text: str) -> str:
    """
    Use LLM to extract machine data from complex report
    """

    prompt = f"""
You are an industrial maintenance parser.

Extract structured information from the report.

Return valid JSON with keys:

machine_id
machine_type
temperature
vibration
noise
pressure
coolant
lubrication
last_service
description
observation
warning
issues
full_text

Rules:
- issues must be list
- keep description as paragraph
- keep observation as paragraph
- keep warning text
- full_text must contain full report

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