import subprocess
from src.llm.base import BaseLLM

class OllamaLLM(BaseLLM):
    def __init__(self, model_name="tinyllama"):
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        result = subprocess.run(
            ["ollama", "run", self.model_name],
            input=prompt.encode("utf-8"),  # 🔑 FIX
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        return result.stdout.decode("utf-8", errors="ignore").strip()
