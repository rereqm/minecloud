from django.test import TestCase, Client
from django.core.exceptions import PermissionDenied
from main.models import User


class Tests(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(username='test',
                                        email='test@test.com',
                                        password='test')

#

    def test_index_status_code(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_index_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'index.html')

#

    def test_registration_status_code(self):
        response = self.client.get('/registration', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_registration_template(self):
        response = self.client.get('/registration', follow=True)
        self.assertTemplateUsed(response, 'registration.html')

#

    def test_servers_status_code(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/servers', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_servers_template(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/servers', follow=True)
        self.assertTemplateUsed(response, 'servers.html')

#

    def test_profile_status_code(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/profile', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_template(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/profile', follow=True)
        self.assertTemplateUsed(response, 'profile.html')

#

    def test_login_status_code(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/login', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_login_template(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/login', follow=True)
        self.assertTemplateUsed(response, 'login.html')