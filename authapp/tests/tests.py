from django.test import TestCase

from authapp.models import ShopUser
from authapp.statuses import status


class UserAuthTestCase(TestCase):
    username = 'test'
    password = 'test'
    email = 'test@test.com'

    def setUp(self):
        self.user = ShopUser.objects.create_superuser(
            username=self.username,
            password=self.password,
            email=self.email
        )

    def test_login_user(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(response.context['user'].is_anonymous)

        self.client.login(username=self.username, password=self.password)

        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_anonymous)

