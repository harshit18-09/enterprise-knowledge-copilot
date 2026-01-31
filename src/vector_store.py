import chromadb
from chromadb.config import Settings
from typing import List
from src.chunk import Chunk

class VectorStore:
    def __init__(self, path="data/chroma"):
        # Create persistent client
        self.client = chromadb.PersistentClient(
            path=path,
            settings=Settings(anonymized_telemetry=False)
        )
        
    def get_collection(self, namespace: str):
        if not namespace:
            raise ValueError("Namespace must be provided for vector store access")

        return self.client.get_or_create_collection(
            name=f"kb_{namespace}"
        )


    def add_chunks(self, namespace: str, chunks: List[Chunk], embeddings: List[List[float]] = None):
        if not chunks:
            return
        
        ids = []
        documents = []
        metadatas = []
        
        for chunk in chunks:
            chunk_id = f"{chunk.metadata['doc_id']}_{chunk.metadata['chunk_id']}"
            ids.append(chunk_id)
            documents.append(chunk.text)
            metadatas.append(chunk.metadata)
        
        if embeddings:
            self.get_collection(namespace).add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
        else:
            self.get_collection(namespace).add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
    