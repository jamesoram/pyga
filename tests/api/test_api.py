import pytest
import requests

BASE_URL = "http://localhost:3000"
def test_localhost_landing_page_succeeds():
    response = requests.get(f"{BASE_URL}/")
    print(dir(response))
    assert response.status_code == 200
