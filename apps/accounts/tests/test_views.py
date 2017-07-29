from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.urls.base import resolve

from .. import views


TEST_FIRST_NAME = 'test_first_name'
TEST_LAST_NAME = 'test_last_name'
TEST_EMAIL = 'test123@test.com'
TEST_USERNAME = 'test123'
TEST_PASSWORD = 'password123'
TEST_BIRTH_DATE = '1990-01-01'
TEST_GENDER = 'm'
TEST_LOCATION = 'somewhere'


class TestViews(TestCase):

    def setUp(self):
        # create test user
        self.credentials = {'username': TEST_USERNAME,
                            'password': TEST_PASSWORD}
        self.test_user = User.objects.create_user(
            first_name=TEST_FIRST_NAME,
            last_name=TEST_LAST_NAME,
            email=TEST_EMAIL,
            **self.credentials
        )
        self.test_user.profile.birth_date = TEST_BIRTH_DATE
        self.test_user.profile.location = TEST_LOCATION
        self.test_user.profile.gender = TEST_GENDER
        self.test_user.profile.profile_picture = SimpleUploadedFile(
            name='test_image.jpg',
            content=b"file_content",
            content_type='image/jpeg')
        self.test_user.is_active = True
        self.test_user.save()

    def tearDown(self):
        User.objects.get(username=TEST_USERNAME).delete()

    def test_redirect_to_profile_page_after_logging_in(self):
        response = self.client.post(
            reverse('accounts:login'), self.credentials)
        self.assertRedirects(response, '/accounts/profile')
