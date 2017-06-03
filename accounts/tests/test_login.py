from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.test import TestCase
from django.urls.base import resolve


TEST_FIRST_NAME = 'test_first_name'
TEST_LAST_NAME = 'test_last_name'
TEST_EMAIL = 'test123@test.com'
TEST_USERNAME = 'test123'
TEST_PASSWORD = 'test123'
TEST_BIRTH_DATE = '1990-01-01'
TEST_LOCATION = 'somewhere'
 
class LoginTestCase(TestCase):
    def tearDown(self):
        User.objects.get(username=TEST_USERNAME).delete()
    
    def setUp(self):
        # create test user
        user = User.objects.create_user(
            first_name=TEST_FIRST_NAME,
            last_name=TEST_LAST_NAME,
            email=TEST_EMAIL,
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            #birth_date=TEST_BIRTH_DATE,
            #location=TEST_LOCATION,
        )
        user.is_active = True
        user.save()
    
    def test_login_url_resolves_to_login_view(self):
        found = resolve('/accounts/login')
        self.assertEqual(found.func, auth_views.login)
        