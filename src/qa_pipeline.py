from src.retrieval.retriever import Retriever
from src.llm.ollama_llm import OllamaLLM
from src.prompting.grounded_promt import build_grounded_prompt
from src.grounding.semantic_validator import SemanticGroundingValidator

class QAPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = OllamaLLM()
        self.validator = SemanticGroundingValidator()

    def answer(self, question: str, filters: dict = None):
        contexts = self.retriever.retrieve(
            query=question,
            filters=filters
        )

        prompt = build_grounded_prompt(question, contexts)
        answer = self.llm.generate(prompt)

        if not self.validator.is_grounded(answer, contexts):
            return (
                "The provided documents do not contain sufficient information to answer this question.",
                contexts
            )

        return answer, contexts