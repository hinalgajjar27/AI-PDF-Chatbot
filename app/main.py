from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.loader import extract_text_from_pdf
from app.text_splitter import split_text
from app.embed import create_embeddings
from app.faiss_db import store_embeddings
from app.llm import get_llm_response
import pickle
import faiss
import shutil
import os
import numpy as np

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads folder inside app
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER,exist_ok=True)

@app.get("/")
def home():
    return {"message":"AI PDF Chatbot API is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    # delete old FAISS + chunks
    if os.path.exists("faiss_index.index"):
        os.remove("faiss_index.index")

    if os.path.exists("chunks.pkl"):
        os.remove("chunks.pkl")

    # delete old uploaded files
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("\nUploaded:", file.filename)

    text = extract_text_from_pdf(file_path)
    print("Preview:", text[:200])

    chunks = split_text(text)

    embeddings = create_embeddings(chunks)
    store_embeddings(chunks, embeddings)

    return {"message": "PDF processed successfully"}

@app.post("/chat")
async def chat(question: str):
    try:
        print("Question:", question)

        index = faiss.read_index("faiss_index.index")

        with open("chunks.pkl", "rb") as f:
            chunks = pickle.load(f)

        query_embedding = create_embeddings([question])
        query_embedding = np.array(query_embedding).astype("float32")

        q = question.lower()
 
        if "summarize" in q or "summary" in q:
            print("Mode: FULL CONTEXT")
            context = " ".join(chunks)

        else:
            print("Mode: RETRIEVAL")
            D, I = index.search(query_embedding, k=3)

            print("\nTop Chunks:")
            for i in I[0]:
                print("----")
                print(chunks[i][:200])

            context = " ".join([chunks[i] for i in I[0]])

        answer = get_llm_response(context, question)

        return {"answer": answer}

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}