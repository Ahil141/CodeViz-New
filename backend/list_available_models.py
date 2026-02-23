import os
from google import genai
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in .env")
else:
    client = genai.Client(api_key=api_key)
    print("Available Models:")
    try:
        for model in client.models.list():
            print(f"- Name: {model.name}")
            # print(dir(model)) # To see all attributes if name is wrong
    except Exception as e:
        print(f"Error listing models: {e}")
