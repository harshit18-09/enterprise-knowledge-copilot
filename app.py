import streamlit as st
import tempfile
import os

from src.load_pdf import extract_pdf
from src.chunk import chunk_text
from src.embedder import Embedder
from src.vector_store import VectorStore
from src.qa_pipeline import QAPipeline

st.set_page_config(
    page_title="Enterprise Knowledge Copilot",
    layout="wide"
)

st.title("Enterprise Knowledge Copilot")
st.caption("Deterministic, permission-aware, grounded RAG system")

@st.cache_resource
def init_backend():
    qa = QAPipeline()
    embedder = Embedder()
    vector_store = VectorStore()
    return qa, embedder, vector_store

qa, embedder, vector_store = init_backend()

st.sidebar.header("Query Controls")

namespace = st.sidebar.text_input("Namespace (required)")
access_level = st.sidebar.selectbox(
    "Access Level",
    ["public", "internal", "confidential"]
)
uploaded_pdf = st.sidebar.file_uploader(
    "Upload PDF (optional)",
    type=["pdf"]
)
if st.sidebar.button("Index PDF"):
    if not uploaded_pdf or not namespace:
        st.sidebar.error("PDF and namespace are required")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_pdf.read())
            tmp_path = tmp.name

        pages = extract_pdf(tmp_path)
        docs = "\n".join(c.text for c in pages)

        doc_id = os.path.splitext(uploaded_pdf.name)[0]
        doc_name = uploaded_pdf.name
        source = "streamlit_upload"

        chunks = chunk_text(
            docs,
            doc_id=doc_id,
            doc_name=doc_name,
            source=source
        )

        embeddings = embedder.embed([c.text for c in chunks])

        vector_store.add_chunks(
            namespace=namespace,
            chunks=chunks,
            embeddings=embeddings
        )

        os.remove(tmp_path)
        st.sidebar.success(
            f"Indexed {len(chunks)} chunks into kb_{namespace}"
        )


question = st.text_input("Enter your question")

if st.button("Ask"):
    if not question or not namespace:
        st.error("Question and namespace are required")
    else:
        answer, contexts = qa.answer(
            question=question,
            namespace=namespace,
            user_access_level=access_level
        )

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Retrieved Contexts")

        if not contexts:
            st.info("No contexts retrieved.")
        else:
            for c in contexts:
                meta = c["metadata"]
                with st.expander(
                    f"Chunk {meta['chunk_id']} | "
                    f"doc: {meta['doc_id']} | "
                    f"access: {meta['access_level']}"
                ):
                    st.write(c["text"])

