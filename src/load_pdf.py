from pypdf import PdfReader
from src.chunk import Chunk
from typing import List
import re

def extract_pdf(pdf_path: str) -> List[Chunk]:
    """Extract and clean text from PDF. Production-ready."""
    reader = PdfReader(pdf_path)
    text = ""
    
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    cleaned_text = clean_text(text)
    
    from pathlib import Path
    path_obj = Path(pdf_path)
    doc_id = path_obj.stem.lower().replace(" ", "_") 
    doc_name = path_obj.stem
    source = path_obj.name  
    
    from src.chunk import chunk_text
    chunks = chunk_text(
        text=cleaned_text,
        doc_id=doc_id,
        doc_name=doc_name,
        source=source,
        section_title="Document"  
    )
    
    return chunks
def clean_text(text: str) -> str:
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

if __name__ == "__main__":
    pdf_path = "../data/medicare_sample.pdf"
    
    try:
        chunks = extract_pdf(pdf_path)
        
        all_text = "\n".join([chunk.text for chunk in chunks])
        with open("../data/raw.txt", "w", encoding="utf-8") as f:
            f.write(all_text)
        
        print(f"✅ Extracted {len(chunks)} chunks from PDF")
        print(f"📊 Total characters: {len(all_text)}")
        
        if chunks:
            print(f"📋 Sample chunk metadata: {chunks[0].metadata}")
            print(f"📝 Sample text: {chunks[0].text[:200]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        from chunk import Chunk
        test_chunk = Chunk(
            text="""Refund Policy: 30-day return window.
                    Security: All data encrypted at rest.
                    AI Guidelines: Models audited quarterly.""",
            metadata={
                "doc_id": "test_doc",
                "doc_name": "Test Document",
                "section": "Document",
                "chunk_id": 0,
                "source": "test.pdf",
                "start": 0,
                "end": 100
            }
        )
        
        with open("data/raw.txt", "w", encoding="utf-8") as f:
            f.write(test_chunk.text)
        print("📝 Created test document for development")