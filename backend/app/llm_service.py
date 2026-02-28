import traceback
import requests
from app.config import settings

class DualAgentService:
    """
    Service class for the Dual-Agent architecture.
    Sends prompts to a remote Ngrok tunnel and expects back
    a JSON response with 'ai_html', 'explanation', and 'python_code' keys.
    """

    def __init__(self):
        self.base_url = settings.NGROK_KAGGLE_URL.rstrip('/')
        self.generate_endpoint = f"{self.base_url}/chat"

    def generate_response(self, prompt: str) -> dict:
        """
        Send a prompt to the remote Dual-Agent Ngrok tunnel.
        """
        try:
            print(f"DEBUG: Calling Dual-Agent endpoint: {self.generate_endpoint}")
            resp = requests.post(
                self.generate_endpoint,
                json={"query": prompt},
                timeout=300,
                headers={"Content-Type": "application/json"},
            )
            resp.raise_for_status()
            data = resp.json()

            return {
                "ai_html":     data.get("ai_html", None),
                "explanation": data.get("explanation", "The AI returned an empty explanation."),
                "python_code": data.get("python_code", None),
            }

        except requests.exceptions.ConnectionError:
            print("ERROR: Could not connect to the Ngrok tunnel.")
            return {
                "ai_html":     None,
                "explanation": "⚠️ Could not connect to the AI backend. The Ngrok tunnel may be offline. A hardcoded fallback visualizer will be shown if one is available.",
                "python_code": None
            }
        except requests.exceptions.Timeout:
            print("ERROR: Ngrok tunnel timed out.")
            return {
                "ai_html":     None,
                "explanation": "⚠️ The AI backend timed out. A hardcoded fallback visualizer will be shown if one is available.",
                "python_code": None
            }
        except requests.exceptions.HTTPError as e:
            print(f"ERROR: Ngrok tunnel returned HTTP error: {e}")
            return {
                "ai_html":     None,
                "explanation": f"⚠️ The AI backend returned an error ({e}). Please try again.",
                "python_code": None
            }
        except Exception as e:
            traceback.print_exc()
            return {
                "ai_html":     None,
                "explanation": f"⚠️ An unexpected error occurred: {str(e)}",
                "python_code": None
            }

# Singleton instance for easy import across the backend
llm_service = DualAgentService()
