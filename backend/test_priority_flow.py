import asyncio
import httpx
import json

async def test_chat_flow():
    url = "http://localhost:8001/api/v1/chat/"
    
    # Test 1: Generic concept that should trigger LLM visualization
    payload = {
        "prompt": "Explain and visualize a simple counter in HTML/CSS/JS",
    }
    
    print(f"\n--- Test 1: LLM Primary Flow ---")
    print(f"Prompt: {payload['prompt']}")
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                print("Status: Success")
                print(f"Visualization Type: {data.get('visualization_type')}")
                print(f"Code Blocks: {len(data.get('code_blocks', []))}")
                if data.get('code_blocks'):
                    print("Found LLM-generated code blocks!")
                else:
                    print("WARNING: No code blocks found. RAG fallback might have triggered if this was valid.")
            else:
                print(f"Status: Failed ({response.status_code})")
                print(response.text)
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    # Note: Ensure the backend server is running before executing this test
    # If not running, you can start it with 'python backend/run_debug.py'
    asyncio.run(test_chat_flow())
