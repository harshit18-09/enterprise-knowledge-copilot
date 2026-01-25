from src.qa_pipeline import QAPipeline

qa = QAPipeline()

while True:
    q = input("Question: ")
    answer, contexts = qa.answer(q)

    print("\nANSWER:")
    print(answer)

    print("\nRETRIEVED CONTEXT CHUNKS (for traceability):")
    for c in contexts:
        print("-", c["metadata"]["chunk_id"])
