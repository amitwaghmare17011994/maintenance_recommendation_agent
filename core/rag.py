from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from dotenv import load_dotenv
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


DB_PATH = "vector_db"


def build_db():

    with open("data/manual.txt", "r") as f:
        text = f.read()

    splitter = CharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )

    chunks = splitter.split_text(text)

    embeddings = OpenAIEmbeddings()

    db = FAISS.from_texts(chunks, embeddings)

    db.save_local(DB_PATH)

    print("Vector DB created")


def retrieve(query: str):

    query = query.strip()

    embeddings = OpenAIEmbeddings()

    db = FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = db.similarity_search(query, k=3)

    return docs




def chat_with_manual(question):

    embeddings = OpenAIEmbeddings()

    db = FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = db.similarity_search(question, k=3)

    context = "\n".join([d.page_content for d in docs])

    prompt = f"""
You are a maintenance assistant.

Use the manual to answer.

Manual:
{context}

Question:
{question}
"""

    r = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return r.choices[0].message.content