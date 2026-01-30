from src.load_chunks import load_chunks
from src.embedder import Embedder
from src.vector_store import VectorStore

chunks = load_chunks("data/chunks.txt")

embedder = Embedder()
store = VectorStore()

texts = [c.text for c in chunks]
embeddings = embedder.embed(texts)

store.add(
    ids=[f"{c.metadata['doc_id']}_{c.metadata['chunk_id']}" for c in chunks],
    embeddings=embeddings,
    documents=texts,
    metadatas=[c.metadata for c in chunks]
)

print(f"Indexed {len(chunks)} chunks")
