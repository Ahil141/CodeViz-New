import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unittest.mock import MagicMock, patch
from app.services.llm_service import GeminiService

async def test_failover_logic():
    print("\n--- Testing Model Failover Logic ---")
    
    # Create service instance
    service = GeminiService()
    
    # Mock the client and generate_content method
    mock_client = MagicMock()
    service.client = mock_client
    
    # First call: Raise RESOURCE_EXHAUSTED
    # Second call: Return success
    mock_response = MagicMock()
    mock_response.text = "Success from fallback model"
    
    def side_effect(*args, **kwargs):
        model = kwargs.get('model')
        print(f"Mocking call for model: {model}")
        if model == "models/gemini-1.5-flash":
            raise Exception("429 RESOURCE_EXHAUSTED: Quota hit")
        return mock_response

    mock_client.models.generate_content.side_effect = side_effect
    
    print("Sending test prompt...")
    result = await service.generate_response("Test prompt")
    
    print(f"Final Result: {result}")
    
    if result == "Success from fallback model":
        print("\n✅ SUCCESS: Failover logic worked! It caught the 429 and tried the next model.")
    else:
        print("\n❌ FAILED: Failover logic did not work as expected.")

if __name__ == "__main__":
    asyncio.run(test_failover_logic())
