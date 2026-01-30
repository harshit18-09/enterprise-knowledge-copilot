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
        self.collection = self.client.get_or_create_collection(
            name="enterprise_docs"
        )

    def add_chunks(self, chunks: List[Chunk], embeddings: List[List[float]] = None):
        """Add chunks with optional embeddings"""
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
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
        else:
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
    
    # Keep the generic add method for backward compatibility
    def add(self, ids, embeddings, documents, metadatas):
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )