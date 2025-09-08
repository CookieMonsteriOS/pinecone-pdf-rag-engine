from sentence_transformers import SentenceTransformer


def load_model(model_name="all-MiniLM-L6-v2"):
    """Load the embedding model"""
    return SentenceTransformer(model_name)


def embed_chunks(model, chunks):
    """Return list of (id, embedding, metadata) for each chunk"""
    vectors = []
    for i, chunk in enumerate(chunks):
        emb = model.encode(chunk["text"]).tolist()
        vectors.append((str(i), emb, {
                       "document": chunk["document"], "page": chunk["page"], "text": chunk["text"]}))
    return vectors
