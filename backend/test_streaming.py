"""
Quick diagnostic to check if streaming endpoint exists
"""
import httpx
import asyncio

async def test_stream():
    print("Testing streaming endpoint...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            async with client.stream(
                'POST',
                'http://127.0.0.1:8001/api/v1/chat/stream',
                json={'prompt': 'Say hello'},
                headers={'Content-Type': 'application/json'}
            ) as response:
                print(f"Status: {response.status_code}")
                if response.status_code == 200:
                    print("✅ Streaming endpoint exists!")
                    print("Receiving chunks:")
                    async for line in response.aiter_lines():
                        if line.startswith('data: '):
                            print(f"  Chunk: {line[:50]}...")
                else:
                    print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n⚠️  The backend server needs to be RESTARTED to load the streaming endpoint!")

if __name__ == "__main__":
    asyncio.run(test_stream())
