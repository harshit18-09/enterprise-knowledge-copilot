def build_grounded_prompt(question: str, contexts: list) -> str:
    context_block = ""
    for c in contexts:
        cid = c["metadata"]["chunk_id"]
        context_block += f"[CHUNK {cid}] {c['text']}\n"

    return f"""
Answer the QUESTION using ONLY the information in the CONTEXT.

CONTEXT:
{context_block}

QUESTION:
{question}

RESPONSE RULES:
- Respond ONLY with bullet points.
- Each bullet point must state ONE requirement.
- Each bullet point must end with a citation like [CHUNK <id>].
- Do NOT include explanations, headings, rules, or meta text.
- Do NOT repeat the context.
- If the answer cannot be supported, respond exactly with:
The provided documents do not contain sufficient information to answer this question.

ANSWER:
"""
