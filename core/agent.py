from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from core.parser import parse_report
from core.rag import retrieve, chat_with_manual
from core.generator import generate_recommendation


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
def retrieve_manual(query: str) -> str:
    """Search maintenance manual"""

    docs = retrieve(query)

    return "\n".join([d.page_content for d in docs])


@tool
def chat_manual(query: str) -> str:
    """Answer maintenance questions"""

    return chat_with_manual(query)


@tool
def recommend_from_text(text: str) -> str:
    """Generate recommendation from report text"""

    parsed = parse_report(text)

    docs = retrieve(parsed)

    return generate_recommendation(parsed, docs)

@tool
def get_report_context(query: str = "") -> str:
    """Get last uploaded report text"""

    global LAST_PDF

    return LAST_PDF

tools = [
    retrieve_manual,
    chat_manual,
    recommend_from_text,
    get_report_context,
]


# -------------------------
# AGENT
# -------------------------

agent = create_react_agent(
    llm,
    tools,
)


# -------------------------
# RUN AGENT
# -------------------------

# def run_agent(query: str, pdf_text: str):

#     global LAST_PDF

#     LAST_PDF = pdf_text

#     result = agent.invoke(
#         {
#             "messages": [
#                 ("user", query)
#             ]
#         }
#     )

#     return result["messages"][-1].content


def run_agent(query: str, pdf_text: str):

    global LAST_PDF

    LAST_PDF = pdf_text

    # print("\n=== AGENT TRACE ===")
    # print("User:", query)

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