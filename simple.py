import requests

port = 5000
_id = 2
url = f"http://localhost:{port}/api/item/{_id}"
user_data = {"key": "Vladyslav"}

resp = requests.post(url, json=user_data)
print(resp.status_code)
print(resp.json())