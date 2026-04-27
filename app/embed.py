from sentence_transformers import SentenceTransformer
from app.loader import extract_text_from_pdf

model = SentenceTransformer("all-MiniLM-L6-v2")
def create_embeddings(chunks):
    embeddings = []

    for chunk in chunks:
        vector = model.encode(chunk)
        embeddings.append(vector)

    return embeddings
    