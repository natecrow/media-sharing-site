from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login
from django.test import TestCase
from django.urls.base import resolve

from accounts import views


class LoginTestCase(TestCase):
    
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
        