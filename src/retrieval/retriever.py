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
        self.ACCESS_MAP = {
            "public": ["public"],
            "internal": ["public", "internal"],
            "confidential": ["public", "internal", "confidential"]
        }


    def retrieve(self, query: str, namespace: str, filters: dict = None, user_access_level="internal"):
        if not namespace:
            raise ValueError("Namespace is required for retrieval")
        collection = self.client.get_collection(f"kb_{namespace}")

        if user_access_level not in self.ACCESS_MAP:
            raise ValueError(f"Invalid access level: {user_access_level}")
            
        if user_access_level == "public":
            permission_filter = {"access_level": "public"}
        elif user_access_level == "internal":
            permission_filter = {"access_level": {"$in": ["public", "internal"]}}
        else:  
            permission_filter = None



        if filters and permission_filter:
            where_clause = {**filters, **permission_filter}
        elif permission_filter:
            where_clause = permission_filter
        else:
            where_clause = filters


        query_embedding = self.embedder.embed([query])[0]

        results = collection.query(
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
