import asyncio
import os
from app.services.llm_service import llm_service

# Mock the settings for test if needed, or rely on .env
# For this script to work, .env must be set up or env var exported

async def main():
    print("Testing Gemini Service...")
    response = await llm_service.generate_response("Explain binary search in one sentence.")
    print(f"Response: {response}")

if __name__ == "__main__":
    # Ensure we are in the backend directory context for imports if running directly
    # But usually running as module 'python -m scripts.test_llm' is better
    # Here we will try running it directly assuming pythonpath is set or running from backend root
    
    import sys
    sys.path.append(os.getcwd())
    
    asyncio.run(main())
