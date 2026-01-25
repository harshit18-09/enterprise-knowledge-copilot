from src.embedder import Embedder
import numpy as np

class SemanticGroundingValidator:
    def __init__(self, threshold=0.45):
        self.embedder = Embedder()
        self.threshold = threshold

    def is_grounded(self, answer: str, contexts: list) -> bool:
        if not answer.strip():
            return False

        answer_emb = self.embedder.embed([answer])[0]
        context_text = " ".join(c["text"] for c in contexts)
        context_emb = self.embedder.embed([context_text])[0]

        similarity = self.cosine_similarity(answer_emb, context_emb)

        return similarity >= self.threshold

    @staticmethod
    def cosine_similarity(a, b):
        a = np.array(a)
        b = np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
