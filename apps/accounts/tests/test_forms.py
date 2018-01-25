from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import ValidationError
from django.test import TestCase
from django.urls import reverse

from . import constants
from ..forms import EditProfileForm, ProfilePictureUploadForm, SignUpForm


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
        form = SignUpForm(data=valid_data)
        self.assertTrue(form.is_valid())

    def test_form_with_no_data(self):
        """
        Form should not be valid with no data because some fields are required
        """
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())

    def test_form_with_invalid_birth_date(self):
        invalid_data = {
            'first_name': constants.VALID_FIRST_NAME,
            'last_name': constants.VALID_LAST_NAME,
            'email': constants.VALID_EMAIL,
            'username': constants.VALID_USERNAME,
            'password1': constants.VALID_PASSWORD,
            'password2': constants.VALID_PASSWORD,
            'birth_date': constants.INVALID_BIRTH_DATE,
            'gender': constants.VALID_GENDER,
            'location': constants.VALID_LOCATION,
        }
        form = SignUpForm(data=invalid_data)
        self.assertFalse(form.is_valid())

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
        form = SignUpForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError, form.clean)


class TestEditProfileForm(TestCase):

    def test_form_with_valid_data(self):
        valid_data = {
            'first_name': constants.VALID_FIRST_NAME,
            'last_name': constants.VALID_LAST_NAME,
            'email': constants.VALID_EMAIL,
            'location': constants.VALID_LOCATION,
            'gender': constants.VALID_GENDER,
        }
        form = EditProfileForm(data=valid_data)
        self.assertTrue(form.is_valid())

    def test_form_with_no_data(self):
        """
        Form should be valid with no data because the fields are not
        required by the Profile model
        """
        form = EditProfileForm(data={})
        self.assertTrue(form.is_valid())

    def test_form_with_invalid_data(self):
        invalid_data = {
            'email': constants.INVALID_EMAIL
        }
        form = EditProfileForm(data=invalid_data)
        self.assertFalse(form.is_valid())


class TestProfilePictureUploadForm(TestCase):

    def test_form_with_valid_file_type(self):
        form = ProfilePictureUploadForm(
            files={'profile_picture': constants.VALID_PROFILE_PIC})
        self.assertTrue(form.is_valid())

    def test_form_with_no_data(self):
        """
        Form should be valid with no file because profile picture is not
        required by the Profile model
        """
        form = ProfilePictureUploadForm(files={})
        self.assertTrue(form.is_valid())

    def test_form_with_invalid_file_type(self):
        form = ProfilePictureUploadForm(
            files={'profile_picture': constants.TEXT_FILE})
        self.assertFalse(form.is_valid())
