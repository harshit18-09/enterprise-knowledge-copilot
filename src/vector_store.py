import chromadb
from chromadb.config import Settings

class VectorStore:
    def __init__(self, path="data/chroma"):
        # Create persistent client
        self.client = chromadb.PersistentClient(
            path=path,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="enterprise_docs"
        )

    def add(self, ids, embeddings, documents, metadatas):
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        # Persistence is automatic with PersistentClient
        # No need for client.persist()