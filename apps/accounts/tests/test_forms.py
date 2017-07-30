from django.test import TestCase

from . import constants
from ..forms import ProfilePictureUploadForm, SignUpForm


class TestSignupForm(TestCase):

    def test_form_with_valid_data(self):
        valid_data = {
            'first_name': constants.TEST_FIRST_NAME,
            'last_name': constants.TEST_LAST_NAME,
            'email': constants.TEST_EMAIL,
            'username': constants.TEST_USERNAME,
            'password1': constants.TEST_PASSWORD,
            'password2': constants.TEST_PASSWORD,
            'birth_date': constants.TEST_BIRTH_DATE,
            'gender': constants.TEST_GENDER,
            'location': constants.TEST_LOCATION,
        }
        form = SignUpForm(valid_data)
        self.assertTrue(form.is_valid())


class TestProfilePictureUploadForm(TestCase):

    def test_form_with_valid_data(self):
        form = ProfilePictureUploadForm(constants.TEST_PROFILE_PICTURE)
        self.assertTrue(form.is_valid())
