from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.urls.base import resolve

from accounts import views


class ViewTests(TestCase):
    
    def setUp(self):
        self.credentials = {'username': 'test123', 'password': 'password123'}
        self.user = User.objects.create_user(**self.credentials)
    
    def test_profile_url_resolves_to_profile_view(self):
        found = resolve('/accounts/profile')
        self.assertEqual(found.func, views.profile)
    
    def test_login_url_resolves_to_login_view(self):
        found = resolve('/accounts/login')
        self.assertEqual(found.func, auth_views.login)
        
    def test_logout_url_resolves_to_logout_view(self):
        found = resolve('/accounts/logout')
        self.assertEqual(found.func, auth_views.logout)
    
    def test_signup_url_resolves_to_signup_view(self):
        found = resolve('/accounts/signup')
        self.assertEqual(found.func, views.signup)
        
    def test_login_redirect(self):
        response = self.client.post(reverse('accounts:login'), self.credentials)
        self.assertRedirects(response, '/accounts/profile')
        