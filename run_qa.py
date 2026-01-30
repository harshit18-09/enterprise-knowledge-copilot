from src.qa_pipeline import QAPipeline

qa = QAPipeline()

# MANUAL TEST HOOK
filters = None

# CHANGE THIS VALUE TO TEST
USER_ACCESS_LEVEL = "public"   # or "confidential"

while True:
    q = input("Question: ")
    
    answer, contexts = qa.answer(
        q,
        filters=filters,
        user_access_level=USER_ACCESS_LEVEL
    )

    print("\nANSWER:")
    print(answer)

    print("\nRETRIEVED CONTEXT CHUNKS (for traceability):")
    for c in contexts:
        print("-", c["metadata"]["chunk_id"], "|", c["metadata"]["access_level"])
