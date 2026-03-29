from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

GROUNDING_SYSTEM_PROMPT = """
You are a maintenance assistant.

STRICT RULES:
- Only use the provided CONTEXT to answer.
- Do NOT use external knowledge.
- If the answer is not in CONTEXT, say: "Not found in report."
- Every important statement must include a citation.
- If context does not contain relevant information, do NOT guess.

Citation format:
(Source: <short snippet from context>)
"""


def generate_recommendation(parsed, docs):

    if not docs:
        return "No relevant context found."

    context = "\n\n".join([d.page_content[:200] for d in docs[:2]])

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
CONTEXT:
{context}

REPORT:
{machine_summary}

Task:
1. Identify issues detected in the report
2. Explain possible causes using ONLY the CONTEXT above
3. Provide recommended actions

IMPORTANT:
- Every explanation must cite the CONTEXT using format: (Source: ...)
- If context does not cover a point, write: "Not found in report."
- Do NOT guess or use external knowledge
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": GROUNDING_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
    )

    return response.choices[0].message.content
