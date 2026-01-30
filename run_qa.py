from src.qa_pipeline import QAPipeline

qa = QAPipeline()

# MANUAL TEST HOOK 
filters = None

while True:
    q = input("Question: ")
    
    answer, contexts = qa.answer(q, filters=filters)

    print("\nANSWER:")
    print(answer)

    print("\nRETRIEVED CONTEXT CHUNKS (for traceability):")
    for c in contexts:
        print("-", c["metadata"]["chunk_id"])