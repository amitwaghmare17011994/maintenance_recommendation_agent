from fastapi import FastAPI, UploadFile, File, Header, HTTPException
import shutil
import uuid
import tempfile
import os

from core.reader import read_pdf
from core.parser import parse_report
from core.rag import retrieve
from core.generator import generate_recommendation
from core.logger import save_log
from core.session_store import save_report, get_report
from core.controller import handle_query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


API_KEY = "my-secret-key"


def verify_api_key(x_api_key: str = Header(...)) -> None:
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


class QueryRequest(BaseModel):
    action: str
    session_id: str


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

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        temp_path = tmp.name
        shutil.copyfileobj(file.file, tmp)

    try:
        text = read_pdf(temp_path)
    finally:
        os.remove(temp_path)

    session_id = str(uuid.uuid4())
    save_report(session_id, text)

    parsed = parse_report(text)

    if not parsed or "error" in parsed:
        docs = retrieve(text)
    else:
        query_text = f"""
Machine: {parsed.get("machine_id")}
Issue: {parsed.get("issues")}
Temperature: {parsed.get("temperature")}
Vibration: {parsed.get("vibration")}
""".strip()
        docs = retrieve(query_text)

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


@app.post("/agent")
async def agent_api(req: QueryRequest, x_api_key: str = Header(...)):

    verify_api_key(x_api_key)

    if req.action not in {"issues", "risk", "plan", "failure"}:
        return {"answer": f"Invalid action. Valid actions: issues, risk, plan, failure"}

    report_text = get_report(req.session_id)

    if not report_text:
        return {"answer": "Invalid session. Please upload report again."}

    result = handle_query(req.action, report_text)

    return {"answer": result}
