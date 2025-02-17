import requests

base_url = "http://localhost"

def test_find_by_status():
    endpoint = "/api/add_user"
    query_params = {"username":"available", "email": "test@test.com"}
    response = requests.post(base_url+endpoint, json=query_params)
    assert response.status_code == 201, "Wrong status code"
    pet_json = response.json()
    # assert pet_json.get("name") is not None, "Name not found"
    # assert pet_json.get("photoUrls") is not None, "URL not found"
