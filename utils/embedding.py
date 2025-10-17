from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def embed_and_index(chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    faiss.write_index(index, "policy_embeddings.index")
    return index, embeddings, model