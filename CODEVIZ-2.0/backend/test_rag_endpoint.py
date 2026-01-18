import requests
import json
import sys

def verify_api():
    url = "http://localhost:8000/api/v1/rag/query"
    payload = {"data_structure_name": "Stack"}
    
    try:
        print(f"Testing API: {url}")
        print(f"Payload: {payload}")
        response = requests.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Response JSON keys:", data.keys())
            if data.get("success") and data.get("visualizer_code"):
                print("SUCCESS: Retrieved visualization code.")
                print("Code snippet:", data["visualizer_code"][:100] + "...")
            else:
                print("FAILURE: API returned success=False or no code.")
                print("Response:", data)
        else:
            print(f"FAILURE: Status code {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"ERROR: Could not connect to API. Is the backend running? {e}")

if __name__ == "__main__":
    verify_api()
