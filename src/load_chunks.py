from typing import List, Dict

def load_chunks(path: str) -> List[Dict]:
    chunks = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            chunk_id, start, end, text = line.split("||", 3)

            chunks.append({
                "id": chunk_id,
                "text": text,
                "metadata": {
                    "chunk_id": int(chunk_id),
                    "char_start": int(start),
                    "char_end": int(end),
                    "source": "medicare_sample.pdf"
                }
            })

    return chunks
