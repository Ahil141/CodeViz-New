import requests
import json

def test_chat_api():
    url = "http://127.0.0.1:8000/api/v1/chat"
    payload = {
        "prompt": "Show me an HTML button."
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print("Status Code:", response.status_code)
        print("Response JSON:", json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        if response is not None:
             print("Response content:", response.text)

if __name__ == "__main__":
    test_chat_api()
