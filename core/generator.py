from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def generate_recommendation(parsed, docs):

    context = "\n".join([d.page_content for d in docs[:2]])

    machine_summary = f"""
Machine ID: {parsed.get("machine_id", "unknown")}
Temperature: {parsed.get("temperature", "unknown")}
Vibration: {parsed.get("vibration", "unknown")}
Last Service: {parsed.get("last_service", "unknown")}
Issues: {parsed.get("issues", [])}
Observation: {parsed.get("observation", "")}
Warning: {parsed.get("warning", "")}
""".strip()

    prompt = f"""
You are a maintenance assistant.

Machine data:
{machine_summary}

Maintenance guide:
{context}

Give:

1. Issue detected
2. Possible cause
3. Recommended action
4. Priority level
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content