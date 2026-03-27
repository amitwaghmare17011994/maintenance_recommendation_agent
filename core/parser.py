import json
import re

from openai import OpenAI
from dotenv import load_dotenv

from core.schema import ParsedReport

load_dotenv()

client = OpenAI()

PARSE_PROMPT = """
You are an industrial maintenance parser.

Extract structured information from the report.

Return ONLY valid JSON with these exact keys:

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
- issues must be a JSON array of strings
- description, observation, warning must be strings
- full_text must contain the full report text
- Do NOT include explanation or markdown
- Do NOT wrap output in code blocks
- Return ONLY the raw JSON object
"""


def _extract_json(raw: str) -> str:
    """Strip markdown code fences if the LLM wraps output in them."""
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw)
    if match:
        return match.group(1).strip()
    return raw.strip()


def _call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


def _parse_and_validate(raw: str) -> dict:
    cleaned = _extract_json(raw)
    data = json.loads(cleaned)
    validated = ParsedReport(**data)
    return validated.model_dump()


def parse_report(text: str) -> dict:

    prompt = f"{PARSE_PROMPT}\n\nReport:\n{text}"

    raw = _call_llm(prompt)

    try:
        return _parse_and_validate(raw)

    except Exception as first_error:
        print("PARSER ERROR (attempt 1):", first_error)

        retry_prompt = f"""
The following text should be valid JSON but has errors.
Fix it and return ONLY the corrected JSON with no explanation or markdown.

Text:
{raw}
"""

        try:
            fixed_raw = _call_llm(retry_prompt)
            return _parse_and_validate(fixed_raw)

        except Exception as second_error:
            print("PARSER ERROR (attempt 2):", second_error)
            return {
                "error": "Invalid structured output",
                "raw": raw,
            }
