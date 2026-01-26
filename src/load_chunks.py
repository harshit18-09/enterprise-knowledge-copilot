from typing import List
from chunk import Chunk

def load_chunks(path: str) -> List[Chunk]:
    chunks = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split("||", 7)  
            if len(parts) != 8:
                print(f"⚠️ Skipping malformed line: {line[:50]}...")
                continue

            doc_id, doc_name, section, chunk_id, start, end, source, text = parts
            
            text = text.replace("\\n", "\n")

            chunks.append(Chunk(
                text=text,
                metadata={
                    "doc_id": doc_id,
                    "doc_name": doc_name,
                    "section": section,
                    "chunk_id": int(chunk_id),
                    "source": source,
                    "start": int(start),
                    "end": int(end)
                }
            ))

    return chunks
