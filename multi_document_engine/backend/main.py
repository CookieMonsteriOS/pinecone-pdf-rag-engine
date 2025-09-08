import os
from dotenv import load_dotenv
from loaders.pdf_loader import load_pdfs
from chunking.chunker import chunk_documents
from embeddings.embedder import load_model, embed_chunks
from pinecone_client.pinecone_client import init_pinecone, create_index, upsert_vectors, query_index

# Load env
load_dotenv()

# --- Load PDFs ---
pdf_folder = "data/pdfs"
docs = load_pdfs(pdf_folder)
print(f"Loaded {len(docs)} pages from PDFs")

# --- Chunk ---
chunk_size = 1000
stride = 200
chunks = chunk_documents(docs, chunk_size=chunk_size, stride=stride)
print(f"Created {len(chunks)} chunks total.\n")

# --- Load embedding model ---
model = load_model()
vectors = embed_chunks(model, chunks)
print(f"Generated embeddings for {len(vectors)} chunks.\n")

# --- Pinecone setup ---
# 1️ Initialize Pinecone client
pinecone_client = init_pinecone()  # returns PineconeClient instance

# 2️ Create or get the index
vectors = []

for i, chunk in enumerate(chunks):
    embedding = model.encode(chunk["text"]).tolist()
    vector_id = f"chunk_{i}"
    metadata = {
        "document": chunk["document"],
        "page": chunk["page"]
    }
    vectors.append((vector_id, embedding, metadata))

index_name = "pdf-chunks"
index = create_index(index_name, dimension=len(vectors[0][1]))
upsert_vectors(index, vectors)  # Adds all vectors
results = query_index(index, query_text, model, top_k=5)
print(f"Pinecone index '{index_name}' ready.\n")

# --- Upsert vectors ---
upsert_vectors(index, vectors)
print(f"Upserted {len(vectors)} vectors to Pinecone.\n")

# --- Test query ---
query_text = "What are the main optimization methods for large-scale ML?"
results = query_index(index, query_text, model, top_k=5)

print(f"Top {len(results)} results for query: '{query_text}'\n")
for match in results:
    print(match["metadata"]["document"], "Page:", match["metadata"]["page"])
    print(match["metadata"]["text"][:300])
    print("-"*80)
