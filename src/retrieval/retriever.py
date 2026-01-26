import chromadb
from chromadb.config import Settings
from src.embedder import Embedder

class Retriever:
    def __init__(self, top_k=5):
        self.top_k = top_k
        self.embedder = Embedder()

        self.client = chromadb.PersistentClient(
            path="data/chroma",
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_collection("enterprise_docs")

    def retrieve(self, query: str, filters: dict = None):
        query_embedding = self.embedder.embed([query])[0]

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=self.top_k,
            where=filters, 
            include=["documents", "metadatas"]
        )

        chunks = []
        for doc, meta in zip(
            results["documents"][0],
            results["metadatas"][0]
        ):
            chunks.append({
                "text": doc,
                "metadata": meta
            })

        return chunks
