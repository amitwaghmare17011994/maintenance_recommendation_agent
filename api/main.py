from fastapi import FastAPI, UploadFile, File
import shutil

from core.reader import read_pdf
from core.parser import parse_report
from core.rag import retrieve
from core.generator import generate_recommendation
from core.rag import chat_with_manual
from core.logger import save_log
from core.agent import run_agent
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from core.agent import run_agent_stream
client = OpenAI()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

last_pdf_text = ""
@app.get("/")
def home():
    return {"message": "Maintenance Agent API running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    temp_path = "temp.pdf"

    # save uploaded file
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 1 read
    text = read_pdf(temp_path)

    global last_pdf_text

    last_pdf_text = text

    # 2 parse
    parsed = parse_report(text)

    # 3 retrieve
    docs = retrieve(parsed)
    context = [d.page_content for d in docs]

    # 4 generate
    result = generate_recommendation(parsed, docs)
    save_log({
        "type": "analyze",
        "text": text,
        "parsed": parsed,
        "context": context,
        "recommendation": result
    })
    return {
        "parsed": parsed,
        "context": [d.page_content for d in docs],
        "recommendation": result
    }

 

@app.post("/chat")
async def chat(question: str):

    global last_pdf_text

    docs = retrieve(question)

    manual_context = "\n".join(
        [d.page_content for d in docs]
    )

    pdf_context = last_pdf_text

    prompt = f"""
You are a maintenance assistant.

Manual:
{manual_context}

Report:
{pdf_context}

Question:
{question}
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
        "question": question,
        "answer": answer,
        "pdf": pdf_context
    })

    return {
        "answer": r.choices[0].message.content
    }
    
@app.post("/agent")
async def agent_api(query: str):

    global last_pdf_text

    if last_pdf_text == "":
        return {
            "answer": "No report uploaded. Please call /analyze first."
        }

    result = run_agent(query, last_pdf_text)

    return {
        "answer": result
    }

@app.post("/agent-stream")
async def agent_stream(query: str):

    global last_pdf_text

    if last_pdf_text == "":
        return {"answer": "No report uploaded"}

    def generate():

        for chunk in run_agent_stream(query, last_pdf_text):

            yield chunk.encode("utf-8")

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )