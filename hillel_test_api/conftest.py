import pytest
from hillel_api import API
import requests

@pytest.fixture
def get_regisered_user():
    email = "alex22222@gmail.com"
    password = "AA12aa!@"
    query_data = {
        "name": "name",
        "lastName": "lastname",
        "email": email,
        "password": password,
        "repeatPassword": password
    }
    s = requests.Session()
    API.auth.signup(s, request_body=query_data)
    yield email, password
    API.users.users(s)