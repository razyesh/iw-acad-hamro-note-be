from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models.education import College, University, Faculty, Education
from accounts.api.serializers import EducationSerializer

User = get_user_model()


class UserTests(APITestCase):
    """
    api test for registering user
    """

    def setUp(self):
        """
        setting up education as it is
        required while registering user
        """
        self.college = self.setup_college()
        self.university = self.setup_university()
        self.faculty = self.setup_faculty()
        self.url = reverse('account:user-register')
        self.education = EducationSerializer(self.setup_education()).data

    def setup_education(self):
        return Education.objects.create(semester=1, year=2,
                                        college=self.college,
                                        faculty=self.faculty,
                                        university=self.university)

    @staticmethod
    def setup_college():
        return College.objects.create(
            college_name='Test College',
            college_short_form='TC'
        )

    @staticmethod
    def setup_university():
        return University.objects.create(
            university_name='Test Uni',
            uni_short_form='TU'
        )

    @staticmethod
    def setup_faculty():
        return Faculty.objects.create(
            faculty_name='Test Faculty',
            fac_short_form='TF'
        )

    def test_user_register(self):
        """
        ensure that we can create new user with the respective
        profile and education detail
        """
        data = {
            "username": "testUser",
            "email": "testuser@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "1234",
            "confirm_password": "1234",
            "profile": {
                "user": 1,
                "contact_number": "9860476499",
                "address": "kapan",
                "education": self.education
            }
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@gmail.com')

    def test_user_retrieve(self):
        data = {
            "username": "testUser",
            "email": "testuser@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "1234",
            "confirm_password": "1234",
            "profile": {
                "user": 1,
                "contact_number": "9860476499",
                "address": "kapan",
                "education": self.education
            }
        }
        response = self.client.post(self.url, data=data, format='json')
        login_data = {
            "email" : "testuser@gmail.com",
            "password" : "1234"
        }
        login_response = self.client.post(reverse("account:user-login"),login_data, format = "json")
        token = login_response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(reverse("account:user-profile"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.data['email'], "testuser@gmail.com")

    def test_user_update(self):
        data = {
            "username": "testUser",
            "email": "testuser@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "1234",
            "confirm_password": "1234",
            "profile": {
                "user": 1,
                "contact_number": "9860476499",
                "address": "kapan",
                "education": self.education
            }
        }
        update_data = {
            "username": "testnotUser",
            "email": "testuser@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "1234",
            "confirm_password": "1234",
            "profile": {
                "user": 1,
                "contact_number": "9860476499",
                "address": "kapan",
                "education": self.education
            }
        }
        response = self.client.post(self.url, data=data, format='json')
        login_data = {
            "email" : "testuser@gmail.com",
            "password" : "1234"
        }
        login_response = self.client.post(reverse("account:user-login"),login_data, format = "json")
        token = login_response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.put(reverse("account:user-update"),update_data,format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "testnotUser")
        self.assertNotEqual(response.data['username'], "testUser")

    def test_user_login(self):
        pass





