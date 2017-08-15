from django.test import TestCase

from . import constants
from ..forms import ProfilePictureUploadForm, SignUpForm


class TestSignupForm(TestCase):

    def test_form_with_valid_data(self):
        valid_data = {
            'first_name': constants.VALID_FIRST_NAME,
            'last_name': constants.VALID_LAST_NAME,
            'email': constants.VALID_EMAIL,
            'username': constants.VALID_USERNAME,
            'password1': constants.VALID_PASSWORD,
            'password2': constants.VALID_PASSWORD,
            'birth_date': constants.VALID_BIRTH_DATE,
            'gender': constants.VALID_GENDER,
            'location': constants.VALID_LOCATION,
        }
        form = SignUpForm(valid_data)
        self.assertTrue(form.is_valid())

    def test_form_with_future_birth_date(self):
        invalid_data = {
            'first_name': constants.VALID_FIRST_NAME,
            'last_name': constants.VALID_LAST_NAME,
            'email': constants.VALID_EMAIL,
            'username': constants.VALID_USERNAME,
            'password1': constants.VALID_PASSWORD,
            'password2': constants.VALID_PASSWORD,
            'birth_date': constants.FUTURE_BIRTH_DATE,
            'gender': constants.VALID_GENDER,
            'location': constants.VALID_LOCATION,
        }
        form = SignUpForm(invalid_data)
        self.assertFalse(form.is_valid())


class TestProfilePictureUploadForm(TestCase):

    def test_form_with_valid_data(self):
        form = ProfilePictureUploadForm(constants.VALID_PROFILE_PIC)
        self.assertTrue(form.is_valid())
