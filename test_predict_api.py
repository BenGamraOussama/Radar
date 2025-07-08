import requests
import json

url = "http://localhost:5000/predict"
data = {
    "data": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, data=json.dumps(data), headers=headers)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
