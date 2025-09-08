def chunk_text(text, chunk_size=300, overlap=50):
    """
    Split text into chunks of ~chunk_size words with overlap.
    Returns a list of chunks.
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        if chunk:
            chunks.append(" ".join(chunk))

    return chunks


def chunk_documents(docs, chunk_size=1000, stride=200):
    chunks = []

    for doc in docs:
        text = doc['text']
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            chunks.append({
                "document": doc["document"],
                "page": doc["page"],
                "text": chunk_text
            })
            start += chunk_size - stride  # overlap
    return chunks
