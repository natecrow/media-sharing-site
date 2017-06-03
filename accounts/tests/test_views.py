from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.test import TestCase
from django.urls.base import resolve


class LoginTestCase(TestCase):
    
    def test_login_url_resolves_to_login_view(self):
        found = resolve('/accounts/login')
        self.assertEqual(found.func, auth_views.login)
        