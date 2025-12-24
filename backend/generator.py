import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()


class GeminiGenerator:
    """
    Gemini-based answer generator.
    """

    def __init__(self, model_name: str | None = None):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY not found. Please set it in the .env file."
            )

        #  Default to the latest supported Flash model
        # Future-ready for Gemini 3 Flash
        self.model_name = model_name or os.getenv(
            "GEMINI_MODEL",
            "gemini-1.5-flash-latest"
        )

        self.client = genai.Client(api_key=api_key)

    def generate_answer(self, query: str, context_chunks: list[str]) -> str:
        context = "\n\n".join(context_chunks)

        prompt = f"""
You are a policy assistant.

Answer the user question using ONLY the policy excerpts below.
Do NOT use outside knowledge.
If the answer is not present in the policy, say:
"The policy does not specify this."

Policy Excerpts:
{context}

User Question:
{query}

Answer:
"""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip()

        except Exception as e:
            raise RuntimeError(
                f"Gemini generation failed for model '{self.model_name}': {e}"
            )
