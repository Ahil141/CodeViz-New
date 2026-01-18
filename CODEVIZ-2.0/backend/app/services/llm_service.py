import traceback
from google import genai
from app.core.config import settings


class GeminiService:
    """
    Service class for interacting with the Gemini LLM
    using the official `google.genai` SDK.
    """

    def __init__(self):
        """
        Initialize the Gemini client using the API key from settings.
        """
        if not settings.GEMINI_API_KEY:
            print("Warning: GEMINI_API_KEY is not set.")
            self.client = None
        else:
            self.client = genai.Client(
                api_key=settings.GEMINI_API_KEY
            )

        # ✅ FREE-TIER SAFE & STABLE MODELS ONLY
        # DO NOT use *-exp or *-preview models
        self.model_name = "models/gemini-flash-latest"
        # Alternative if needed:
        # self.model_name = "models/gemini-pro-latest"

    async def generate_response(self, prompt: str, context: str = "") -> str:
        """
        Generate a response from the Gemini model.

        Args:
            prompt (str): User input question or instruction.
            context (str): Optional retrieved context (RAG).

        Returns:
            str: Generated response text.
        """
        try:
            if not self.client:
                return (
                    "Error: Gemini API Key is missing. "
                    "Please configure it in the .env file."
                )

            # Combine RAG context (if available) with user prompt
            if context:
                final_prompt = (
                    "You are an educational computer science tutor.\n\n"
                    f"Context:\n{context}\n\n"
                    f"User Question:\n{prompt}"
                )
            else:
                final_prompt = prompt

            # Call Gemini API
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=final_prompt
            )

            # Safety check
            if not response or not response.text:
                return "Error: Empty response received from Gemini."

            return response.text

        except Exception as e:
            traceback.print_exc()

            # Friendly message for quota issues
            if "RESOURCE_EXHAUSTED" in str(e):
                return (
                    "The AI service is temporarily rate-limited. "
                    "Please wait a minute and try again."
                )

            return (
                "Error: Failed to generate response. "
                f"Details: {str(e)}"
            )


# Singleton instance for easy import across the backend
llm_service = GeminiService()
