import requests
import unittest
import pytest
from allure_commons._allure import title, description

BASE_URL = "http://restapi.adequateshop.com/api"

# Tests for Get Tourist Endpoint
@pytest.mark.allure
class GetTouristEndpointTests(unittest.TestCase):
    @pytest.mark.test
    @title("Successfully create and retrieve a specific tourist")
    @description("Test successfully creates a tourist and retrieves created tourist by id")
    def test_get_tourist_by_id(self):
        payload = {
            "id": 17,
            "tourist_name": "James Bond",
            "tourist_email": "jb0@test.com",
            "tourist_location": "London",
            "createdat": "2023-06-12T18:59:56.868Z"
        }
        create_response = requests.post(f"{BASE_URL}/Tourist", json=payload)
        assert create_response.status_code == 201
        # retrieve tourist id
        tourist_id = create_response.json()['id']
        get_response = requests.get(f"{BASE_URL}/Tourist/{tourist_id}")
        assert get_response.status_code == 200
        print(get_response.json())

    @pytest.mark.test
    @title("Successfully create a tourist and retrieve it with wrong id")
    @description("Test successfully creates a tourist but retrieves tourist by wrong id")
    def test_get_tourist_by_wrongid(self):
        payload = {
            "id": 19,
            "tourist_name": "James Bond 007",
            "tourist_email": "jb3@test.com",
            "tourist_location": "London",
            "createdat": "2023-06-12T18:59:56.868Z"
        }
        create_response = requests.post(f"{BASE_URL}/Tourist", json=payload)
        assert create_response.status_code == 201
        # retrieve tourist id
        tourist_id = 1
        get_response = requests.get(f"{BASE_URL}/Tourist/{tourist_id}")
        assert get_response.status_code == 404

    @pytest.mark.test
    @title("Unsuccessfully retrieve a tourist with invalid id")
    @description("Test unsuccessfully retrieves a tourist with invalid id")
    def test_get_tourist_by_invalidid(self):
        tourist_id = "djfk2"
        response = requests.get(f"{BASE_URL}/Tourist/{tourist_id}")
        assert response.status_code == 400
        json_data = response.json()
        error_message = json_data["Message"]
        expected_message = "The request is invalid."
        self.assertEqual(error_message, expected_message)
