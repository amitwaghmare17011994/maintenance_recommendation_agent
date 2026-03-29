import json
import re

from openai import OpenAI

client = OpenAI()

VALID_INTENTS = {"structured", "reasoning", "plan"}

ROUTER_SYSTEM_PROMPT = """
You are an intent classifier for a maintenance AI system.

Classify the user query into ONE of these intents:

1. structured → asking for direct data (machine id, issues list, last service date, etc.)
2. reasoning  → asking "why", "how", explanations, causes, danger levels
3. plan       → asking for maintenance plan, recommendations, risks, failure prediction, repair steps

Rules:
- Return ONLY valid JSON.
- No explanation, no markdown, no code block.
- Format:

{"intent": "structured" | "reasoning" | "plan"}
"""


def route_query(query: str) -> str:

    try:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": ROUTER_SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ]
        )

        raw = response.choices[0].message.content.strip()

        # strip markdown fences if present
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw)
        if match:
            raw = match.group(1).strip()

        data = json.loads(raw)
        intent = data.get("intent", "reasoning")

        if intent not in VALID_INTENTS:
            intent = "reasoning"

        print("ROUTER:", query, "→", intent)
        return intent

    except Exception as e:

        print("ROUTER ERROR:", e)
        return "reasoning"
