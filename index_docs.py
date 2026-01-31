from collections import defaultdict
from src.load_chunks import load_chunks
from src.embedder import Embedder
from src.vector_store import VectorStore

chunks = load_chunks("data/chunks.txt")

groups = defaultdict(list)
for c in chunks:
    groups[c.metadata["doc_id"]].append(c)

embedder = Embedder()
store = VectorStore()

total = 0

for namespace, doc_chunks in groups.items():
    texts = [c.text for c in doc_chunks]
    embeddings = embedder.embed(texts)

    store.add_chunks(
        namespace=namespace,
        chunks=doc_chunks,
        embeddings=embeddings
    )

    total += len(doc_chunks)
    print(f"Indexed {len(doc_chunks)} chunks into namespace '{namespace}'")

print(f"\nTotal indexed chunks: {total}")
