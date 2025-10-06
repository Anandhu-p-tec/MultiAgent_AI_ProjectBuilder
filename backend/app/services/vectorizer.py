from chromadb import Client
from chromadb.config import Settings as ChromaSettings
import hashlib

from chromadb import PersistentClient

client = PersistentClient(path="./chroma_store")


def process_and_vectorize_document(text: str):
    """Vectorize text and store it locally using ChromaDB."""
    if not text.strip():
        return []

    collection = client.get_or_create_collection(name="documents")

    doc_id = hashlib.md5(text.encode("utf-8")).hexdigest()
    collection.add(documents=[text], ids=[doc_id])

    return [{"id": doc_id, "text": text[:200]}]  # sample snippet
