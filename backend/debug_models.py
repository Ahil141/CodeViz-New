
import os
import sys
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def list_models_sync():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return

    print(f"Using API Key: {api_key[:5]}...{api_key[-5:]}")

    try:
        client = genai.Client(api_key=api_key)
        
        with open("models_list.txt", "w", encoding="utf-8") as f:
            f.write("--- Available Models ---\n")
            # List models synchronously
            count = 0
            for model in client.models.list():
                f.write(f"- {model.name}\n")
                count += 1
            
            if count == 0:
                f.write("No models found.\n")
        
        print(f"Models listed to models_list.txt ({count} models found)")
            
    except Exception as e:
        print(f"Error listing models: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    list_models_sync()

