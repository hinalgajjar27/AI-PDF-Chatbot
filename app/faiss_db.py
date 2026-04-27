import faiss
import numpy as np
import pickle

def store_embeddings(chunks, embeddings):

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, "faiss_index.index")

    with open("chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    return index