from fastapi import FastAPI, UploadFile, File, Header, HTTPException
import shutil
import uuid

from core.reader import read_pdf
from core.parser import parse_report
from core.rag import retrieve
from core.generator import generate_recommendation
from core.rag import chat_with_manual
from core.logger import save_log
from core.session_store import save_report, get_report
from core.controller import handle_query
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


API_KEY = "my-secret-key"

BLOCKED_WORDS = [
    "ignore previous",
    "system prompt",
    "developer message",
    "reveal instructions",
]


def verify_api_key(x_api_key: str = Header(...)) -> None:
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


def check_query(query: str) -> str | None:
    """Returns an error string if the query is invalid, else None."""
    if not query or len(query) > 500:
        return "Invalid query"
    if any(word in query.lower() for word in BLOCKED_WORDS):
        return "Unsafe query detected"
    return None


class QueryRequest(BaseModel):
    query: str
    session_id: str


class ChatRequest(BaseModel):
    question: str
    session_id: str


client = OpenAI()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://maintenance-recommendation-agent-fe.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Maintenance Agent API running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), x_api_key: str = Header(...)):

    verify_api_key(x_api_key)

    if file.content_type != "application/pdf":
        return {"error": "Only PDF files are allowed"}

    temp_path = "temp.pdf"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = read_pdf(temp_path)

    session_id = str(uuid.uuid4())
    save_report(session_id, text)

    parsed = parse_report(text)
    docs = retrieve(parsed)
    context = [d.page_content for d in docs]

    result = generate_recommendation(parsed, docs)

    save_log({
        "type": "analyze",
        "text": text,
        "parsed": parsed,
        "context": context,
        "recommendation": result
    })

    return {
        "session_id": session_id,
        "parsed": parsed,
        "context": context,
        "recommendation": result
    }

 

@app.post("/chat")
async def chat(req: ChatRequest, x_api_key: str = Header(...)):

    verify_api_key(x_api_key)

    error = check_query(req.question)
    if error:
        return {"answer": error}

    report_text = get_report(req.session_id)

    if not report_text:
        return {
            "answer": "Invalid session. Please upload report again."
        }

    docs = retrieve(req.question)

    manual_context = "\n".join([d.page_content for d in docs])

    prompt = f"""
You are a maintenance assistant.

Manual:
{manual_context}

Report:
{report_text}

Question:
{req.question}
"""

    r = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = r.choices[0].message.content

    save_log({
        "type": "chat",
        "question": req.question,
        "answer": answer,
        "pdf": report_text
    })

    return {
        "answer": answer
    }


@app.post("/agent")
async def agent_api(req: QueryRequest, x_api_key: str = Header(...)):

    verify_api_key(x_api_key)

    error = check_query(req.query)
    if error:
        return {"answer": error}

    report_text = get_report(req.session_id)

    if not report_text:
        return {
            "answer": "Invalid session. Please upload report again."
        }

    result = handle_query(req.query, report_text)

    return {
        "answer": result
    }