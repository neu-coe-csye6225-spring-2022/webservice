import django.contrib.auth
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.utils import timezone
from rest_framework import status


# Create your tests here.
class UserTest(APITestCase):
    base_url = "http://127.0.0.1:8000/"
    test_user_name = "test@example.com"
    test_user_token = ""

    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user(self.test_user_name, self.test_user_name, 'testpassword')
        self.test_user.first_name = "AB"
        self.test_user.last_name = "CD"
        self.test_user_token = Token.objects.create(user=self.test_user)

        # URL for creating an account.
        # self.create_url = reverse('user:')

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "password": "skdjfhskdfjhg",
            "username": "jane.doe@example.com"
        }

        response = self.client.post(self.base_url + "v1/user/", data, format='json')

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # user is created
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])
        self.assertFalse(response.data['id'] is None)
        self.assertFalse(response.data['account_created'] is None)
        self.assertFalse(response.data['account_updated'] is None)
        self.assertFalse('password' in response.data)

    def test_create_user_with_useless_param(self):
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "password": "skdjfhskdfjhg",
            "username": "jane.doe@example.com",
            "account_created": timezone.now(),
            "account_updated": timezone.now()
        }

        response = self.client.post(self.base_url + "v1/user/", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # user is created
        self.assertNotEqual(response.data['account_created'], data['account_created'])
        self.assertNotEqual(response.data['account_updated'], data['account_updated'])

    def test_create_user_existed(self):
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "password": "skdjfhskdfjhg",
            "username": "jane.doe@example.com"
        }

        response = self.client.post(self.base_url + "v1/user/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # user is created

        response = self.client.post(self.base_url + "v1/user/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_without_first_name(self):
        data = {
            "last_name": "Doe",
            "password": "skdjfhskdfjhg",
            "username": "jane.doe@example.com"
        }

        response = self.client.post(self.base_url + "v1/user/", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_without_last_name(self):
        data = {
            "first_name": "Jane",
            "password": "skdjfhskdfjhg",
            "username": "jane.doe@example.com"
        }

        response = self.client.post(self.base_url + "v1/user/", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_without_password(self):
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "username": "jane.doe@example.com"
        }

        response = self.client.post(self.base_url + "v1/user/", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_without_username(self):
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "password": "skdjfhskdfjhg",
        }

        response = self.client.post(self.base_url + "v1/user/", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_wrong_username(self):
        data = {
            "last_name": "Doe",
            "password": "skdjfhskdfjhg",
            "username": "examplecom"
        }

        response = self.client.post(self.base_url + "v1/user/", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_info_with_token(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_token.key)
        response = client.get(self.base_url + "v1/user/self/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['username'] is None)
        self.assertFalse(response.data['first_name'] is None)
        self.assertFalse(response.data['last_name'] is None)
        self.assertFalse(response.data['id'] is None)
        self.assertFalse(response.data['account_created'] is None)
        self.assertFalse(response.data['account_updated'] is None)
        self.assertFalse('password' in response.data)

    def test_get_user_info_without_token(self):
        response = self.client.get(self.base_url + "v1/user/self/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_info_with_wrong_token(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_token.key + 'abc')
        response = client.get(self.base_url + "v1/user/self/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_info(self):
        data = {
            "first_name": "Bill",
            "last_name": "Gates",
            "password": "skdjfhskdfjhgeee"
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_token.key)
        response = client.put(self.base_url + "v1/user/self/", data, format='json')

        response_get = client.get(self.base_url + "v1/user/self/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(response_get.data['first_name'], data['first_name'])
        self.assertEqual(response_get.data['last_name'], data['last_name'])

    def test_update_user_info_with_username(self):
        data = {
            "first_name": "Bill",
            "last_name": "Gates",
            "password": "skdjfhskdfjhgeee",
            "username": "abc@aabc.ab"
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_token.key)
        response = client.put(self.base_url + "v1/user/self/", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_info_with_account_updated(self):
        data = {
            "first_name": "Bill",
            "last_name": "Gates",
            "password": "skdjfhskdfjhgeee",
            "account_updated": timezone.now()
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_token.key)
        response = client.put(self.base_url + "v1/user/self/", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_info_with_account_created(self):
        data = {
            "first_name": "Bill",
            "last_name": "Gates",
            "password": "skdjfhskdfjhgeee",
            "account_created": timezone.now()
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_token.key)
        response = client.put(self.base_url + "v1/user/self/", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_info_without_token(self):
        data = {
            "first_name": "Bill",
            "last_name": "Gates",
            "password": "skdjfhskdfjhgeee"
        }

        response = self.client.put(self.base_url + "v1/user/self/", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_info_with_wrong_token(self):
        data = {
            "first_name": "Bill",
            "last_name": "Gates",
            "password": "skdjfhskdfjhgeee"
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_token.key + 'abc')
        response = client.put(self.base_url + "v1/user/self/", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
