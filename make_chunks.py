from src.load_pdf import extract_pdf
import os

os.makedirs("data", exist_ok=True)

out = open("data/chunks.txt", "w", encoding="utf-8")

docs = [
    {
        "pdf": "data/medicare_sample.pdf",
        "access_level": "public"
    },
    {
        "pdf": "data/medicare_sample_confidential.pdf",
        "access_level": "confidential"
    }
]

for d in docs:
    chunks = extract_pdf(d["pdf"])

    for c in chunks:
        # override permission per document
        c.metadata["access_level"] = d["access_level"]

        m = c.metadata
        escaped = c.text.replace("\n", "\\n")

        out.write(
            f"{m['doc_id']}||{m['doc_name']}||{m['section']}||"
            f"{m['chunk_id']}||{m['start']}||{m['end']}||"
            f"{m['source']}||{m['access_level']}||{escaped}\n"
        )

out.close()
print("✅ chunks.txt created with correct permissions")
