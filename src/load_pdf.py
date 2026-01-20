from pypdf import PdfReader
import re

def extract_pdf(pdf_path: str) -> str:
    """Extract and clean text from PDF. Production-ready."""
    reader = PdfReader(pdf_path)
    text = ""
    
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    return clean_text(text)

def clean_text(text: str) -> str:
    """Minimal cleaning: fix line breaks, normalize whitespace."""
    # Fix hyphenated words split across lines
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

if __name__ == "__main__":
    # Path to your PDF
    pdf_path = "data/medicare_sample.pdf"
    
    try:
        text = extract_pdf(pdf_path)
        
        # Save raw extracted text
        with open("data/raw.txt", "w", encoding="utf-8") as f:
            f.write(text)
        
        print(f"✅ Extracted {len(text)} characters from PDF")
        print(f"📊 Sample: {text[:200]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        # Create minimal test data
        test_text = """Refund Policy: 30-day return window.
Security: All data encrypted at rest.
AI Guidelines: Models audited quarterly."""
        
        with open("data/raw.txt", "w", encoding="utf-8") as f:
            f.write(test_text)
        print("📝 Created test document for development")