from openai import OpenAI

from core.parser import parse_report
from core.rag import retrieve
from core.generator import generate_recommendation
from core.context_cache import get_cache, set_cache

client = OpenAI()


def list_detected_issues_impl(text: str) -> str:

    print("Listing issues...")

    cached = get_cache("issues", text)

    if cached:
        print("CACHE HIT")
        return cached

    prompt = f"""
You are a maintenance expert.

Read the report and list all detected issues.

Report:
{text}

Return result as bullet points.

Format:
- issue 1
- issue 2
- issue 3

Do not explain.
Do not ask questions.
"""

    r = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    result = r.choices[0].message.content

    set_cache("issues", text, result)

    return result


def risk_assessment_impl(text: str) -> str:

    print("Assessing risk level...")

    cached = get_cache("risk", text)

    if cached:
        print("CACHE HIT")
        return cached

    prompt = f"""
You are a maintenance expert.

Analyze the report and determine risk level.

Report:
{text}

Return in format:

Risk Level: LOW / MEDIUM / HIGH / CRITICAL

Reason:
- reason 1
- reason 2
- reason 3
"""

    r = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    result = r.choices[0].message.content

    set_cache("risk", text, result)

    return result


def create_maintenance_plan_impl(text: str) -> str:

    print("Creating maintenance plan...")

    cached = get_cache("plan", text)

    if cached:
        print("CACHE HIT")
        return cached

    prompt = f"""
You are a maintenance expert.

Create step-by-step maintenance plan.

Report:
{text}

Return format:

Maintenance Plan:
1.
2.
3.
4.
"""

    r = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    result = r.choices[0].message.content

    set_cache("plan", text, result)

    return result


def recommend_from_text_impl(text: str) -> str:

    print("Generating recommendation from text...")

    cached = get_cache("recommend", text)

    if cached:
        print("CACHE HIT")
        return cached

    parsed = parse_report(text)

    docs = retrieve(parsed)

    result = generate_recommendation(parsed, docs)

    set_cache("recommend", text, result)

    return result


def predict_failure_impl(text: str) -> str:

    print("Predicting failure...")

    cached = get_cache("failure", text)

    if cached:
        print("CACHE HIT")
        return cached

    prompt = f"""
You are a predictive maintenance expert.

Analyze the report and predict machine failure.

Report:
{text}

Return in format:

Failure Risk: LOW / MEDIUM / HIGH / CRITICAL

Estimated Time to Failure: (hours/days)

Reasons:
- reason 1
- reason 2
- reason 3

Recommendation:
- action 1
- action 2
"""

    r = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    result = r.choices[0].message.content

    set_cache("failure", text, result)

    return result


def get_report_context_impl(last_pdf: str = "") -> str:

    print("Getting last uploaded report text...")

    if not last_pdf:
        return "No report available"

    return last_pdf
