import requests
import unittest
import pytest
import sys
from allure_commons._allure import title, description

BASE_URL = "http://restapi.adequateshop.com/api"

# Tests for Registration and login
class LoginAndRegistrationTests(unittest.TestCase):
    @title("Successful Registration")
    @description("Test successful registration of a user")
    def test_successful_registration(self):
        payload = {"name": "Test",
                   "email": "new123-mail@test.com",
                   "password": "123GGG"}
        response = requests.post(
            f"{BASE_URL}/AuthAccount/Registration", json=payload)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        actual_message = json_data["message"]
        expected_message = "success"
        self.assertEqual(actual_message, expected_message)

    @title("Unsucsessfull Registration")
    @description("Test registering user with password that is shorter than 6 characters")
    def test_unsuccessful_registration_short_password(self):
        payload = {"name": "TestUser",
                   "email": "someuser@test.com", "password": "123GG"}
        response = requests.post(
            f"{BASE_URL}/AuthAccount/Registration", json=payload)
        self.assertEqual(response.status_code, 400)
        json_data = response.json()
        error_message = json_data["ModelState"]["User.password"][0]
        expected_message = "password at least 6 characters"
        self.assertEqual(error_message, expected_message)

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

    @title("Successful Login")
    @description("Test successful login with valid email and password")
    def test_successful_login(self):
        payload = {"email": "valid_megi@test.com", "password": "123GGG"}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 200)

    @title("Unsuccessful Login")
    @description("Test unsuccessful login with invalid email")
    def test_unsuccessful_login_incorrect_email(self):
        payload = {"email": "invalid_megi@test.com", "password": "123GGG"}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        error_message = json_data["message"]
        expected_message = "invalid username or password"
        self.assertEqual(error_message, expected_message)

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

    @title("Unsuccessful Login")
    @description("Test unsuccessful login with empty credentials")
    def test_unsuccessful_login_empty_credentials(self):
        payload = {"email": "", "password": ""}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 400)

    @title("Unsuccessful Login")
    @description("Test unsuccessful login with empty email")
    def test_unsuccessful_login_empty_username(self):
        payload = {"email": "", "password": "123GGG"}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 400)

    @title("Unsuccessful Login")
    @description("Test unsuccessful login with empty password and valid email")
    def test_unsuccessful_login_empty_password(self):
        payload = {"email": "valid_megi@test.com", "password": ""}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 400)


# Tests for Get Tourist Endpoint
class GetTouristEndpointTests(unittest.TestCase):
    @title("Successfully create and retrieve a specific tourist")
    @description("Test successfully creates a tourist and retrieves created tourist by id")
    def test_get_tourist_by_id(self):
        payload = {
            "id": 17,
            "tourist_name": "James Bond",
            "tourist_email": "test_234567@test.com",
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

    @title("Unsuccessfully retrieve a tourist with wrong id")
    @description("Test unsuccessfully retrieves tourist by wrong id")
    def test_get_tourist_by_wrongid(self):
        tourist_id = 1598
        get_response = requests.get(f"{BASE_URL}/Tourist/{tourist_id}")
        assert get_response.status_code == 404

    @title("Unsuccessfully retrieve a tourist with invalid id")
    @description("Test unsuccessfully retrieves a tourist with an invalid alphanumeric id")
    def test_get_tourist_by_invalidid(self):
        tourist_id = "djfk2"
        response = requests.get(f"{BASE_URL}/Tourist/{tourist_id}")
        assert response.status_code == 400
        json_data = response.json()
        error_message = json_data["Message"]
        expected_message = "The request is invalid."
        self.assertEqual(error_message, expected_message)


if __name__ == "__main__":
    # Run the tests using pytest
    result = pytest.main(["-qq", "--tb=no", __file__])

    # Exit with appropriate status code based on test result
    sys.exit(int(result != 0))

