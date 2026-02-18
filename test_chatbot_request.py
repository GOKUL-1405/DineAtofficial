import requests
import json

url = 'http://127.0.0.1:8000/chat/'
headers = {'Content-Type': 'application/json'}
data = {"message": "What is DineAt?"}

try:
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
