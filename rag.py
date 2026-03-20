import os
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

chunks = []
embeddings = None
query_cache = {}


def load_docs(docs_dir="docs"):
    global chunks, embeddings

    chunks = []
    for filename in os.listdir(docs_dir):
        if filename.endswith(".txt") or filename.endswith(".md"):
            path = os.path.join(docs_dir, filename)
            text = open(path).read()
            for chunk in text.split("\n\n"):
                chunk = chunk.strip()
                if chunk:
                    chunks.append({"text": chunk, "source": filename})

    embeddings = model.encode([c["text"] for c in chunks])
    print(f"Loaded {len(chunks)} chunks from {docs_dir}/")


def retrieve(query, top_k=3):
    if query not in query_cache:
        query_cache[query] = model.encode([query])[0]

    q_emb = query_cache[query]
    scores = np.dot(embeddings, q_emb) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(q_emb) + 1e-9
    )
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [chunks[i] for i in top_indices]
