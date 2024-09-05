import os
import requests
import pytest

BASE_URL = "https://fa-data-ingestion.azurewebsites.net/api/user_data"
FUNCTION_KEY = os.getenv("FUNCTIONS_KEY")

@pytest.fixture
def user_id():
    return "WalleM"

def test_get_user_data(user_id):
    if not FUNCTION_KEY:
        pytest.skip("FUNCTIONS_KEY environment variable is not set.")

    url = f"{BASE_URL}?userId={user_id}"
    response = requests.get(url, headers={"x-functions-key": FUNCTION_KEY})

    # Validate the response status code
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    
    # Validate the response body
    user_data = response.json()
    assert user_data["userId"] == user_id, f"Expected userId {user_id}, but got {user_data['userId']}"
    assert "email" in user_data, "Expected 'email' field in user data"
    assert "firstName" in user_data, "Expected 'firstName' field in user data"
    assert "lastName" in user_data, "Expected 'lastName' field in user data"
    assert "flightId" in user_data, "Expected 'flightId' field in user data"
    assert "id" in user_data, "Expected 'id' field in user data"
    assert "_rid" in user_data, "Expected '_rid' field in user data"
    assert "_self" in user_data, "Expected '_self' field in user data"
    assert "_etag" in user_data, "Expected '_etag' field in user data"
    assert "_attachments" in user_data, "Expected '_attachments' field in user data"
    assert "_ts" in user_data, "Expected '_ts' field in user data"

def test_get_user_data_not_found():
    if not FUNCTION_KEY:
        pytest.skip("FUNCTIONS_KEY environment variable is not set.")
        
    url = f"{BASE_URL}?userId=NonExistentUser"
    response = requests.get(url, headers={"x-functions-key": FUNCTION_KEY})
    
    # Validate the response status code
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    assert response.text == "User not found.", f"Expected 'User not found.', but got {response.text}"