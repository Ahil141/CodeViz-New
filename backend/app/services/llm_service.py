import traceback
import requests
from app.core.config import settings


class DualAgentService:
    def __init__(self):
        self.base_url = settings.NGROK_KAGGLE_URL.rstrip('/')
        self.generate_endpoint = f"{self.base_url}/generate"

    def generate_response(self, prompt: str) -> dict:
        try:
            resp = requests.post(
                self.generate_endpoint,
                json={"prompt": prompt},
                timeout=120,
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
            return {"ai_html": None, "explanation": "⚠️ Could not connect to the AI backend. The Ngrok tunnel may be offline."}
        except requests.exceptions.Timeout:
            return {"ai_html": None, "explanation": "⚠️ The AI backend timed out."}
        except requests.exceptions.HTTPError as e:
            return {"ai_html": None, "explanation": f"⚠️ The AI backend returned an error ({e})."}
        except Exception as e:
            traceback.print_exc()
            return {"ai_html": None, "explanation": f"⚠️ An unexpected error occurred: {str(e)}"}


llm_service = DualAgentService()
