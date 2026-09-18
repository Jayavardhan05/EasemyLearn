import chromadb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_or_create_collection(
    name="documents"
)


def add_chunks(chunks, document_id):
    ids = []

    for i in range(len(chunks)):
        ids.append(f"{document_id}_{i}")

    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=[
            {"document_id": document_id}
            for _ in chunks
        ]
    )


def search_chunks(query, document_id, n_results=5):
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where={"document_id": document_id}
    )

    documents = results["documents"][0]
    distances = results["distances"][0]

    if distances[0] > 1.7:
        return []

    return documents