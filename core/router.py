from openai import OpenAI

client = OpenAI()

VALID_ROUTES = {"issues", "risk", "plan", "recommend", "failure", "chat"}


def route_query(query: str) -> str:

    prompt = f"""
Classify the following user query into ONE category:

- issues (if asking about problems, faults, issues)
- risk (if asking about risk, danger, safety)
- plan (if asking what to do, fix, repair, steps, maintenance plan)
- recommend (if asking for recommendations or suggestions)
- failure (if asking about breakdown, failure prediction, will it fail, time to fail, estimated failure)
- chat (if none of the above)

Only return ONE word from:
issues, risk, plan, recommend, failure, chat

Query:
{query}
"""

    try:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        result = response.choices[0].message.content.strip().lower()

        print("ROUTER RESULT:", result)

        if result in VALID_ROUTES:
            return result

        return "chat"

    except Exception as e:

        print("ROUTER ERROR:", e)

        return "chat"
