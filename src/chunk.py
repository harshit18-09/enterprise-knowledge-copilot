import os
import re

CHUNK_SIZE = 1000
OVERLAP = 200


def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def strip_front_matter(text: str) -> str:
    """
    Remove TOC / index by keeping text starting from
    the first real explanatory paragraph.
    """
    paragraphs = re.split(r"\n{2,}", text)

    for i, p in enumerate(paragraphs):
        clean = p.strip()

        # Real content heuristic:
        # long paragraph + multiple sentences
        if len(clean) > 700 and clean.count(".") >= 5:
            return "\n\n".join(paragraphs[i:])

    # Fallback: return original text
    return text


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append({
                "text": chunk,
                "start": start,
                "end": min(end, text_length)
            })

        start = end - overlap

    return chunks


if __name__ == "__main__":
    input_path = "data/raw.txt"
    output_path = "data/chunks.txt"

    text = load_text(input_path)

    # 🔑 STRUCTURAL FIX (this is the key)
    text = strip_front_matter(text)

    chunks = chunk_text(text)

    os.makedirs("data", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for i, c in enumerate(chunks):
            f.write(
                f"{i}||{c['start']}||{c['end']}||{c['text']}\n"
            )

    print(f"✅ Created {len(chunks)} chunks")
    print(f"📊 Example chunk:\n{chunks[0]['text'][:300]}...")
