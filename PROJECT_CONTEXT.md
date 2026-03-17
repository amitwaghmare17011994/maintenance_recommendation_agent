# Project Context – Maintenance Recommendation Agent

## Purpose

This project is an AI-based maintenance recommendation system using:

* LLM (OpenAI)
* RAG (vector DB)
* PDF parsing
* FastAPI backend
* Streamlit UI

No ML training is used.

The system reads maintenance reports, retrieves knowledge from manual,
and generates recommendations.

---

## Features implemented

1. PDF upload
2. Text extraction using pdfplumber
3. LLM parsing
4. RAG using FAISS vector DB
5. Recommendation generation using LLM
6. FastAPI backend
7. Streamlit UI
8. Chat with RAG
9. Logging
10. Chat uses manual + uploaded PDF

---

## Project structure

maintenance_agent/

core/
reader.py
parser.py
rag.py
generator.py
logger.py

api/
main.py

ui/
app.py

data/
manual.txt

vector_db/

logs/

test files

---

## Pipeline

PDF → reader → parser → rag → generator → API → UI

Chat:

question → rag → manual + last pdf → LLM → answer

---

## Reader

core/reader.py

Reads PDF and returns text.

---

## Parser

core/parser.py

Uses OpenAI to extract machine info.

---

## RAG

core/rag.py

Uses:

* FAISS
* OpenAI embeddings
* manual.txt

Vector DB stored in vector_db/

retrieve(query) returns context.

---

## Generator

core/generator.py

Uses:

parsed data + retrieved context

Returns recommendation.

---

## API

api/main.py

Endpoints:

POST /analyze
POST /chat

/analyze

* read pdf
* parse
* retrieve
* generate
* log

/chat

* retrieve manual
* add last pdf text
* LLM answer

last_pdf_text stored globally.

---

## UI

ui/app.py

Features:

Upload PDF
Analyze
Show parsed data
Show context
Show recommendation

Chat icon bottom right
Chat only after analyze

Chat uses API /chat

---

## Logging

core/logger.py

Logs saved in logs/logs.json

Saved:

text
parsed
context
recommendation
chat
time

---

## Goal

Demonstrate:

LLM
RAG
Vector DB
PDF parsing
API
UI
Logging
Chat

No ML training.
