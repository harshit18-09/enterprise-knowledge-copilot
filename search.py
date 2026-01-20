import chromadb
from chromadb.config import Settings
from src.embedder import Embedder

client = chromadb.PersistentClient(
    path="data/chroma",
    settings=Settings(anonymized_telemetry=False)
)

collection = client.get_collection("enterprise_docs")

embedder = Embedder()

while True:
    q = input("Query: ")
    emb = embedder.embed([q])[0]

    res = collection.query(
        query_embeddings=[emb],
        n_results=5,
        include=["documents", "metadatas", "distances"]
    )

    for d, m, dist in zip(
        res["documents"][0],
        res["metadatas"][0],
        res["distances"][0]
    ):
        print("\n---")
        print("Score:", dist)
        print("Meta:", m)
        print(d[:300])
