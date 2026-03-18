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

]


# -------------------------
# AGENT
# -------------------------
agent = create_react_agent(
    llm,
    tools,
    prompt="""
You are a maintenance AI agent.

Important rules:

- The maintenance report is already uploaded.
- Never ask the user to provide the report.
- Always call get_report_context first to read the report.

Tool usage rules:

If user asks about issues / problems:
    get_report_context -> list_detected_issues

If user asks about risk / safety / danger / priority:
    get_report_context -> risk_assessment

If user asks about recommendation / fix / repair:
    get_report_context -> recommend_from_text

If user asks about manual / guide:
    retrieve_manual

Never ask user for report.
Never say "please provide report".
Report already exists.
"""
)


# -------------------------
# RUN AGENT
# -------------------------
 

def run_agent(query: str, pdf_text: str):

    global LAST_PDF

    LAST_PDF = pdf_text

    # print("\n=== AGENT TRACE ===")
    print("User:", query)
    print("Agent: Thinking...")

    # # ---------- STREAM ----------
    # for step in agent.stream(
    #     {
    #         "messages": [
    #             ("user", query)
    #         ]
    #     }
    # ):

    #     # print raw step if needed
    #     # print(step)

    #     # -------- agent step (tool call decision) --------
    #     if "agent" in step:

    #         msgs = step["agent"]["messages"]

    #         for m in msgs:

    #             # print thought
    #             if hasattr(m, "content") and m.content:
    #                 print("Thought:", m.content)

    #             # print tool call
    #             if hasattr(m, "tool_calls") and m.tool_calls:

    #                 for t in m.tool_calls:
    #                     print("Action:", t["name"])

    #     # -------- tool execution --------
    #     if "tools" in step:

    #         msgs = step["tools"]["messages"]

    #         for m in msgs:

    #             print("Observation from tool:", m.name)

    #             # optional: print result
    #             # print(m.content)

    # print("=== END TRACE ===\n")

    # ---------- FINAL RESULT ----------
    result = agent.invoke(
        {
            "messages": [
                ("user", query)
            ]
        }
    )

    return result["messages"][-1].content