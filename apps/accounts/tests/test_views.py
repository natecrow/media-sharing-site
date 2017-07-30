from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from . import constants


class TestViews(TestCase):

    def setUp(self):
        # create test user
        self.credentials = {'username': constants.TEST_USERNAME,
                            'password': constants.TEST_PASSWORD}
        self.test_user = User.objects.create_user(
            first_name=constants.TEST_FIRST_NAME,
            last_name=constants.TEST_LAST_NAME,
            email=constants.TEST_EMAIL,
            **self.credentials
        )
        self.test_user.profile.birth_date = constants.TEST_BIRTH_DATE
        self.test_user.profile.gender = constants.TEST_GENDER
        self.test_user.profile.location = constants.TEST_LOCATION
        self.test_user.profile.profile_picture = constants.TEST_PROFILE_PICTURE
        self.test_user.is_active = True
        self.test_user.save()

    def tearDown(self):
        User.objects.get(username=constants.TEST_USERNAME).delete()

    def test_redirect_to_profile_page_after_logging_in(self):
        response = self.client.post(
            reverse('accounts:login'), self.credentials)
        self.assertRedirects(response, '/accounts/profile')
