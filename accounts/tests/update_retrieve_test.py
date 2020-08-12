import json

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models.education import College, University, Faculty, Education
from accounts.models.profile import Profile
from accounts.api.serializers import EducationSerializer

from .register_login_tests import UserRegisterTests
User = get_user_model()


class UserRetrieveTests(APITestCase):
    """api test case for
    retrieving user information"""

    def setUp(self):
        self.user = User.objects.create(email = "hari@gmail.com", password = "1234")
        token = Token.objects.create(user = self.user )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_user_retrieve(self):
        response = self.client.get(reverse("account:user-profile"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.data['email'], "hari@gmail.com")    


class UserUpdateTests(APITestCase):
    """api test case for
    retrieving user information"""

    def setUp(self):
        self.user = User.objects.create(email = "hari@gmail.com", password = "1234")
        token = Token.objects.create(user = self.user )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_user_update(self):
        response = self.client.put(reverse("account:user-update"),{"email": "ram@gmail.com", "profile": ""})
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)