from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from embeddings.embedder import load_model, embed_chunks
from loaders.pdf_loader import load_pdfs
from chunking.chunker import chunk_documents
from pinecone_client.pinecone_client import init_pinecone, create_index, upsert_vectors, query_index

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


INDEX_NAME = "pdf-chunks"
EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 outputs 384-d embeddings

# Globals
model = None
index = None


@app.on_event("startup")
def startup_event():
    """Initialize Pinecone and embedding model at startup"""
    global model, index
    pinecone_client = init_pinecone()

    # Ensure index exists (won’t fail if already exists)
    index = create_index(INDEX_NAME, dimension=EMBEDDING_DIM)

    # Load embedding model once
    model = load_model()


@app.get("/")
def read_root():
    return {"message": "Multi-Document Insight Engine API is running!"}


@app.get("/process-pdfs")
def process_pdfs():
    """Load, chunk, embed PDFs and upsert into Pinecone"""
    docs = load_pdfs("data/pdfs")
    chunks = chunk_documents(docs)

    vectors = embed_chunks(model, chunks)
    upsert_vectors(index, vectors)

    return {"total_chunks": len(chunks), "preview": chunks[:5]}


@app.get("/query")
def rag_query(
    q: str = Query(..., description="Your query text"),
    top_k: int = 5
):
    """Query the Pinecone index and return top-k relevant chunks"""
    if index is None:
        return {"error": "Pinecone index not initialized. Restart the backend."}

    results = query_index(
        index=index,
        query_text=q,
        model=model,
        top_k=top_k
    )

    return [
        {"id": r["id"], "score": r["score"], "metadata": r["metadata"]}
        for r in results
    ]
