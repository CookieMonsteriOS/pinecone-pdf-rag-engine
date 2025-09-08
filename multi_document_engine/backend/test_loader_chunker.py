from loaders.pdf_loader import load_pdfs
from chunking.chunker import chunk_documents


pdf_folder = "data/pdfs"  # relative to current folder (backend/)
docs = load_pdfs(pdf_folder)
print(f"Loaded {len(docs)} pages from PDFs")

if not docs:
    print("No pages loaded. Check PDF folder and file contents.")
    exit()

# --- Chunk documents ---
chunk_size = 1000  # number of characters per chunk
stride = 200       # overlap between chunks
chunks = chunk_documents(docs, chunk_size=chunk_size, stride=stride)
print(f"Created {len(chunks)} chunks total.\n")

# --- Preview first 5 chunks ---
for i, c in enumerate(chunks[:5], 1):
    print(f"Chunk {i}:")
    print(f"Document: {c['document']}, Page: {c['page']}")
    print(f"Text preview: {c['text'][:300]}")
    print("-" * 80)
