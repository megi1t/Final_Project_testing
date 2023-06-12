import requests
import unittest
import pytest
from allure_commons._allure import title, description


BASE_URL = "http://restapi.adequateshop.com/api"

# Tests for Registration and login


@pytest.mark.allure
class LoginAndRegistrationTests(unittest.TestCase):
    @pytest.mark.test
    @title("Successful Registration")
    @description("Test successful registration of a user")
    def test_successful_registration(self):
        payload = {"name": "Test",
                   "email": "testtest001@test.com", "password": "123GGG"}
        response = requests.post(
            f"{BASE_URL}/AuthAccount/Registration", json=payload)
        self.assertEqual(response.status_code, 200)

    @pytest.mark.test
    @title("Unsucsessfull Registration")
    @description("Test registering user with password that is shorter than 6 characters")
    def test_unsuccessful_registration_short_password(self):
        payload = {"name": "TestUser",
                   "email": "someuser@test.com", "password": "123GG"}
        response = requests.post(
            f"{BASE_URL}/AuthAccount/Registration", json=payload)
        self.assertEqual(response.status_code, 400)

    @pytest.mark.test
    @title("Unsucsessfull Registration")
    @description("Test re-registering already registered user")
    def test_unsuccessful_registration_registered_user(self):
        payload = {"name": "TestUser1",
                   "email": "random_test_user2@test.com", "password": "123GGH"}
        response = requests.post(
            f"{BASE_URL}/AuthAccount/Registration", json=payload)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        error_message = json_data["message"]
        expected_message = "The email address you have entered is already registered"
        self.assertEqual(error_message, expected_message)

    @pytest.mark.test
    @title("Successful Login")
    @description("Test successful login with valid email and password")
    def test_successful_login(self):
        payload = {"email": "valid_megi@test.com", "password": "123GGG"}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 200)

    @pytest.mark.test
    @title("Successful Login")
    @description("Test successful login with valid email and password")
    def test_unsuccessful_login_incorrect_email(self):
        payload = {"email": "invalid_megi@test.com", "password": "123GGG"}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        error_message = json_data["message"]
        expected_message = "invalid username or password"
        self.assertEqual(error_message, expected_message)

    @pytest.mark.test
    @title("Unsuccessful Login")
    @description("Test unsuccessful login with valid email and incorrect password")
    def test_unsuccessful_login_incorrect_password(self):
        payload = {"email": "valid_megi@test.com", "password": "123GGGG"}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        error_message = json_data["message"]
        expected_message = "invalid username or password"
        self.assertEqual(error_message, expected_message)

    @pytest.mark.test
    @title("Unsuccessful Login")
    @description("Test unsuccessful login with incorrect credentials")
    def test_unsuccessful_login_incorrect_credentials(self):
        payload = {"email": "invalid_megi@test.com", "password": "123GGGG"}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        error_message = json_data["message"]
        expected_message = "invalid username or password"
        self.assertEqual(error_message, expected_message)

    @pytest.mark.test
    @title("Unsuccessful Login")
    @description("Test unsuccessful login with empty credentials")
    def test_unsuccessful_login_empty_credentials(self):
        payload = {"email": "", "password": ""}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 400)

    @pytest.mark.test
    @title("Unsuccessful Login")
    @description("Test unsuccessful login with empty email")
    def test_unsuccessful_login_empty_username(self):
        payload = {"email": "", "password": "123GGG"}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 400)

    @pytest.mark.test
    @title("Unsuccessful Login")
    @description("Test unsuccessful login with empty password")
    def test_unsuccessful_login_empty_password(self):
        payload = {"email": "valid_megi@test.com", "password": ""}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 400)


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
            "tourist_email": "jamesbondtest@test.com",
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
            "tourist_email": "jamesbondtest1@test.com",
            "tourist_location": "London",
            "createdat": "2023-06-12T18:59:56.868Z"
        }
        create_response = requests.post(f"{BASE_URL}/Tourist", json=payload)
        assert create_response.status_code == 201
        # retrieve tourist id
        tourist_id = 1
        get_response = requests.get(f"{BASE_URL}/Tourist/{tourist_id}")
        assert get_response.status_code == 404
        print(get_response.json())

    @pytest.mark.test
    @title("Unsuccessfully retrieve a tourist with invalid id")
    @description("Test unsuccessfully retrieves a tourist with invalid id")
    def test_get_tourist_by_invalidid(self):
        tourist_id = "djfk2"
        response = requests.get(f"{BASE_URL}/Tourist/{tourist_id}")
        assert response.status_code == 404
