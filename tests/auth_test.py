import requests
import unittest
import pytest
import allure_commons._allure


BASE_URL = "http://restapi.adequateshop.com/api"

# Tests for Registration and login
@pytest.mark.allure
class LoginAndRegistrationTests(unittest.TestCase):
    @pytest.mark.test
    @allure_commons._allure.title("Successful Registration")
    @allure_commons._allure.description("Test successful registration of a user")
    def test_successful_registration(self):
        payload = {"name": "Test",
                   "email": "testtest001@test.com", "password": "123GGG"}
        response = requests.post(
            f"{BASE_URL}/AuthAccount/Registration", json=payload)
        self.assertEqual(response.status_code, 200)

    @pytest.mark.test
    @allure_commons._allure.title("Unsucsessfull Registration")
    @allure_commons._allure.description("Test registering user with password that is shorter than 6 characters")
    def test_unsuccessful_registration_short_password(self):
        payload = {"name": "TestUser",
                   "email": "someuser@test.com", "password": "123GG"}
        response = requests.post(
            f"{BASE_URL}/AuthAccount/Registration", json=payload)
        self.assertEqual(response.status_code, 400)

    @pytest.mark.test
    @allure_commons._allure.title("Unsucsessfull Registration")
    @allure_commons._allure.description("Test re-registering already registered user")
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
    @allure_commons._allure.title("Successful Login")
    @allure_commons._allure.description("Test successful login with valid email and password")
    def test_successful_login(self):
        payload = {"email": "valid_megi@test.com", "password": "123GGG"}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 200)

    @pytest.mark.test
    @allure_commons._allure.title("Successful Login")
    @allure_commons._allure.description("Test successful login with valid email and password")
    def test_unsuccessful_login_incorrect_email(self):
        payload = {"email": "invalid_megi@test.com", "password": "123GGG"}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        error_message = json_data["message"]
        expected_message = "invalid username or password"
        self.assertEqual(error_message, expected_message)

    @pytest.mark.test
    @allure_commons._allure.title("Unsuccessful Login")
    @allure_commons._allure.description("Test unsuccessful login with valid email and incorrect password")
    def test_unsuccessful_login_incorrect_password(self):
        payload = {"email": "valid_megi@test.com", "password": "123GGGG"}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        error_message = json_data["message"]
        expected_message = "invalid username or password"
        self.assertEqual(error_message, expected_message)

    @pytest.mark.test
    @allure_commons._allure.title("Unsuccessful Login")
    @allure_commons._allure.description("Test unsuccessful login with incorrect credentials")
    def test_unsuccessful_login_incorrect_credentials(self):
        payload = {"email": "invalid_megi@test.com", "password": "123GGGG"}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        error_message = json_data["message"]
        expected_message = "invalid username or password"
        self.assertEqual(error_message, expected_message)

    @pytest.mark.test
    @allure_commons._allure.title("Unsuccessful Login")
    @allure_commons._allure.description("Test unsuccessful login with empty credentials")
    def test_unsuccessful_login_empty_credentials(self):
        payload = {"email": "", "password": ""}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 400)

    @pytest.mark.test
    @allure_commons._allure.title("Unsuccessful Login")
    @allure_commons._allure.description("Test unsuccessful login with empty email")
    def test_unsuccessful_login_empty_username(self):
        payload = {"email": "", "password": "123GGG"}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 400)

    @pytest.mark.test
    @allure_commons._allure.title("Unsuccessful Login")
    @allure_commons._allure.description("Test unsuccessful login with empty password")
    def test_unsuccessful_login_empty_password(self):
        payload = {"email": "valid_megi@test.com", "password": ""}
        response = requests.post(f"{BASE_URL}/AuthAccount/Login", json=payload)
        self.assertEqual(response.status_code, 400)
