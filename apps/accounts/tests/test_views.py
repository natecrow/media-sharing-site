from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from . import constants


class TestViews(TestCase):

    def setUp(self):
        # create test user
        self.credentials = {'username': constants.VALID_USERNAME,
                            'password': constants.VALID_PASSWORD}
        self.test_user = User.objects.create_user(
            first_name=constants.VALID_FIRST_NAME,
            last_name=constants.VALID_LAST_NAME,
            email=constants.VALID_EMAIL,
            **self.credentials
        )
        self.test_user.profile.birth_date = constants.VALID_BIRTH_DATE
        self.test_user.profile.gender = constants.VALID_GENDER
        self.test_user.profile.location = constants.VALID_LOCATION
        self.test_user.profile.profile_picture = constants.VALID_PROFILE_PIC
        self.test_user.is_active = True
        self.test_user.save()

    def tearDown(self):
        User.objects.get(username=constants.VALID_USERNAME).delete()

    def test_redirect_to_profile_page_after_logging_in(self):
        response = self.client.post(
            reverse('accounts:login'), self.credentials)

        user = auth.get_user(self.client)
        assert user.is_authenticated()
        self.assertRedirects(response, reverse('accounts:profile'))
