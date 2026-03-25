from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from core.parser import parse_report
from core.rag import retrieve, chat_with_manual
from core.generator import generate_recommendation
from openai import OpenAI

client = OpenAI()
# -------------------------
# LLM
# -------------------------

llm = ChatOpenAI(model="gpt-4.1-mini")


# -------------------------
# GLOBAL PDF STORAGE
# -------------------------

LAST_PDF = ""


# -------------------------
# TOOLS
# -------------------------

@tool
def create_maintenance_plan(text: str) -> str:
    """Generate maintenance plan from report"""

    print("Creating maintenance plan...")

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

    return r.choices[0].message.content


@tool
def risk_assessment(text: str) -> str:
    """Assess risk level from maintenance report"""

    print("Assessing risk level...")

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

    return r.choices[0].message.content



@tool
def list_detected_issues(text: str) -> str:
    """Extract issues from maintenance report"""

    print("Listing issues...")

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

    return r.choices[0].message.content

@tool
def retrieve_manual(query: str) -> str:
    """Search maintenance manual"""
    print("Retrieving manual...")
    docs = retrieve(query)

    return "\n".join([d.page_content for d in docs])


@tool
def chat_manual(query: str) -> str:
    """Answer maintenance questions"""
    print("Chatting with manual...")
    return chat_with_manual(query)


@tool
def recommend_from_text(text: str) -> str:
    """Generate recommendation from report text"""
    print("Generating recommendation from text...")
    parsed = parse_report(text)

    docs = retrieve(parsed)

    return generate_recommendation(parsed, docs)
    
@tool
def get_report_context(query: str = "") -> str:
    """Get last uploaded report text"""

    print("Getting last uploaded report text...")

    global LAST_PDF

    if not LAST_PDF:
        return "No report available"

    return LAST_PDF

tools = [
    retrieve_manual,
    chat_manual,
    recommend_from_text,
    get_report_context,
    list_detected_issues,
    risk_assessment,
    create_maintenance_plan,
]


# -------------------------
# AGENT
# -------------------------
agent = create_react_agent(
    llm,
    tools,
    prompt="""
You are an industrial maintenance AI agent.

The maintenance report is already uploaded.
Never ask the user to provide the report.

IMPORTANT RULES:

1. Always call get_report_context first to read the report.
2. Always use tools to answer.
3. Never invent report data.
4. Never ask user for report.
5. Do NOT rewrite tool output.
6. Return tool output exactly as it is.
7. Keep formatting from tools (bullet points, numbers, etc).

TOOL USAGE RULES:

If user asks about issues / problems / faults:
    get_report_context → list_detected_issues

If user asks about risk / safety / danger / priority:
    get_report_context → risk_assessment

If user asks about recommendation / fix / solution:
    get_report_context → recommend_from_text

If user asks about plan / steps / repair / maintenance plan:
    get_report_context → create_maintenance_plan

If user asks about manual / guide / rules:
    retrieve_manual

VERY IMPORTANT:

- Do not summarize tool output
- Do not reformat tool output
- Do not add explanation unless asked
- Return tool result directly
"""
)
 


# -------------------------
# RUN AGENT
# -------------------------

def run_agent(query: str, pdf_text: str):

    global LAST_PDF

    LAST_PDF = pdf_text

    print("User:", query)
    print("Agent: Thinking...")

    result = agent.invoke(
        {
            "messages": [
                ("user", query)
            ]
        }
    )

    return result["messages"][-1].content


# -------------------------
# STREAM AGENT
# -------------------------


def run_agent_stream(query: str, pdf_text: str):

    global LAST_PDF

    LAST_PDF = pdf_text

    for step in agent.stream(
        {
            "messages": [
                ("user", query)
            ]
        }
    ):

        # ---------- AGENT THINK ----------
        if "agent" in step:

            msgs = step["agent"]["messages"]

            for m in msgs:

                # tool call
                if hasattr(m, "tool_calls") and m.tool_calls:

                    for t in m.tool_calls:

                        name = t["name"]

                        yield f"⚙️ Calling tool: {name}\n"

                # thought text
                if hasattr(m, "content") and m.content:
                    yield f"🤖 {m.content}\n"

        # ---------- TOOL RESULT ----------
        if "tools" in step:

            msgs = step["tools"]["messages"]

            for m in msgs:

                yield f"✔ Tool finished: {m.name}\n"