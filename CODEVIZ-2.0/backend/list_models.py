from google import genai
import os

# Make sure your .env variables are loaded
from dotenv import load_dotenv
load_dotenv()  # This reads your .env file

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# List all models your API key can access
models = client.models.list()
for m in models:
    print(m.name)
