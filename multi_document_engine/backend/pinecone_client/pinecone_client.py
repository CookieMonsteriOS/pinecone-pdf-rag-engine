import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from pinecone.exceptions import PineconeApiException

load_dotenv()

pinecone_client = None


def init_pinecone():
    """
    Create a global Pinecone client instance (SDK v3/v4).
    No 'environment' arg needed in serverless mode.
    """
    global pinecone_client
    if pinecone_client is None:
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise RuntimeError("PINECONE_API_KEY not set")
        pinecone_client = Pinecone(api_key=api_key)
    return pinecone_client


def create_index(name: str, dimension: int, metric: str = "cosine"):
    """
    Idempotently create (serverless) index if missing; return an Index handle.
    Requires cloud+region for serverless (set via env or defaults).
    """
    assert pinecone_client is not None, "Call init_pinecone() first"

    cloud = os.getenv("PINECONE_CLOUD", "aws")
    region = os.getenv("PINECONE_REGION", "us-east-1")

    # list_indexes() may return dicts or objects depending on SDK version
    existing = []
    for i in pinecone_client.list_indexes():
        if isinstance(i, dict):
            existing.append(i.get("name"))
        else:
            # v4 returns IndexDescription objects with .name
            existing.append(getattr(i, "name", str(i)))

    if name not in existing:
        try:
            pinecone_client.create_index(
                name=name,
                dimension=dimension,
                metric=metric,
                spec=ServerlessSpec(cloud=cloud, region=region),
            )
        except PineconeApiException as e:
            # tolerate races / re-runs
            if getattr(e, "status", None) != 409:
                raise

    # return a live Index handle
    return pinecone_client.Index(name)


def upsert_vectors(index, vectors, batch_size: int = 100):
    """
    Upsert vectors in batches. Each vector is (id, embedding, metadata).
    """
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i: i + batch_size]
        index.upsert(vectors=batch)


def query_index(index, query_text: str, model, top_k: int = 5):
    """
    Embed the query and run a Pinecone similarity search (with metadata).
    """
    query_emb = model.encode(query_text).tolist()
    result = index.query(
        vector=query_emb,
        top_k=top_k,
        include_metadata=True,
    )
    # normalize to a simple list of dicts
    matches = result.get("matches", []) if isinstance(
        result, dict) else getattr(result, "matches", [])
    # Some SDKs return objects; convert uniformly
    normalized = []
    for m in matches or []:
        if isinstance(m, dict):
            normalized.append({"id": m.get("id"), "score": m.get(
                "score"), "metadata": m.get("metadata", {})})
        else:
            normalized.append({"id": getattr(m, "id", None), "score": getattr(
                m, "score", None), "metadata": getattr(m, "metadata", {})})
    return normalized
