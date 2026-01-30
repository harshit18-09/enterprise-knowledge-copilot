import chromadb
from chromadb.config import Settings
from src.embedder import Embedder

class Retriever:
    def __init__(self, top_k=2):
        self.top_k = top_k
        self.embedder = Embedder()

        self.client = chromadb.PersistentClient(
            path="data/chroma",
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_collection("enterprise_docs")
        self.ACCESS_MAP = {
            "public": ["public"],
            "internal": ["public", "internal"],
            "confidential": ["public", "internal", "confidential"]
        }


    def retrieve(self, query: str, filters: dict = None, user_access_level="internal"):
        if user_access_level not in self.ACCESS_MAP:
            raise ValueError(f"Invalid access level: {user_access_level}")
            
        if user_access_level == "public":
            permission_filter = {"access_level": "public"}
        elif user_access_level == "internal":
            # internal can see BOTH → we must NOT filter
            permission_filter = None
        else:  # confidential
            permission_filter = None



        if filters and permission_filter:
            where_clause = {**filters, **permission_filter}
        elif permission_filter:
            where_clause = permission_filter
        else:
            where_clause = filters


        query_embedding = self.embedder.embed([query])[0]

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=self.top_k,
            where=where_clause,
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
        print("ACCESS LEVELS:", [c["metadata"]["access_level"] for c in chunks])

        return chunks
