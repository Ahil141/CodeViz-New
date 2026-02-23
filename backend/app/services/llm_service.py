import re
import traceback
import asyncio
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

        # ✅ List of models for failover (ordered by priority)
        # Using Gemini 2.x models (available for this API key)
        self.models = [
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-2.5-pro",
            "gemini-flash-latest",
            "gemini-pro-latest",
            "gemini-2.0-flash-lite"
        ]

    async def generate_response(self, prompt: str, context: str = "") -> str:
        """
        Generate a response from the Gemini model with automatic failover.
        """
        if not self.client:
            return (
                "Error: Gemini API Key is missing. "
                "Please configure it in the .env file."
            )

        # Combine RAG context (if available) with user prompt
        final_prompt = (
            f"You are an educational computer science tutor.\n\n"
            f"Context:\n{context}\n\n"
            f"User Question:\n{prompt}"
        ) if context else prompt

        # Try each model in sequence if rate-limited
        for model_name in self.models:
            try:
                print(f"DEBUG: Using model: {model_name}")
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=final_prompt
                )

                if response and response.text:
                    return response.text
                
                print(f"WARNING: Empty response from {model_name}. Trying next...")
                continue

            except Exception as e:
                error_str = str(e).upper()
                
                # Check for rate limit / quota error OR model not found
                if any(err in error_str for err in ["RESOURCE_EXHAUSTED", "429", "404", "NOT_FOUND", "400", "INVALID_ARGUMENT"]):
                    print(f"WARNING: Issue with {model_name} (Error: {error_str}). Switching model...")
                    continue # Try next model
                
                traceback.print_exc()
                return f"Error: Failed to generate response. Details: {str(e)}"

        return "Error: All available AI models have failed. Please try again later."

    async def generate_response_stream(self, prompt: str, context: str = ""):
        """
        Generate a streaming response from the Gemini model with automatic failover.
        Yields text chunks as they are generated.
        """
        if not self.client:
            yield "Error: Gemini API Key is missing. Please configure it in the .env file."
            return

        # Combine RAG context (if available) with user prompt
        final_prompt = (
            f"You are an educational computer science tutor.\n\n"
            f"Context:\n{context}\n\n"
            f"User Question:\n{prompt}"
        ) if context else prompt

        # Try each model in sequence if rate-limited
        for model_name in self.models:
            try:
                print(f"DEBUG: Using model (streaming): {model_name}")
                
                # Use generate_content_stream for streaming responses
                stream = self.client.models.generate_content_stream(
                    model=model_name,
                    contents=final_prompt
                )

                # Yield chunks as they arrive, split into words/tokens for smoother streaming
                has_content = False
                for chunk in stream:
                    if chunk.text:
                        has_content = True
                        # Split by whitespace but keep the delimiters (spaces, newlines, etc.)
                        # This preserves the exact formatting of the original text
                        tokens = re.split(r'(\s+)', chunk.text)
                        
                        for token in tokens:
                            if token: # Skip empty strings
                                yield token
                                # Small delay for visible streaming effect (adjust as needed)
                                # Only delay on actual words, not just whitespace, to make it feel more natural
                                if token.strip():
                                    await asyncio.sleep(0.05)
                
                if has_content:
                    return  # Successfully streamed, exit
                
                print(f"WARNING: Empty stream from {model_name}. Trying next...")
                continue

            except Exception as e:
                error_str = str(e).upper()
                
                # Check for rate limit / quota error OR model not found
                if any(err in error_str for err in ["RESOURCE_EXHAUSTED", "429", "404", "NOT_FOUND", "400", "INVALID_ARGUMENT"]):
                    print(f"WARNING: Issue with {model_name} (streaming) (Error: {error_str}). Switching model...")
                    continue  # Try next model
                
                traceback.print_exc()
                yield f"Error: Failed to generate response. Details: {str(e)}"
                return

        yield "Error: All available AI models have failed. Please try again later."


# Singleton instance for easy import across the backend
llm_service = GeminiService()
