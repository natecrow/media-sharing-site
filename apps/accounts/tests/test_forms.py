from django.test import TestCase
from django.urls import reverse

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
        response = self.client.post(
            reverse('accounts:upload'),
            {'image': constants.VALID_PROFILE_PIC})

        self.assertEqual(302, response.status_code)

    def test_form_with_wrong_filetype(self):
        response = self.client.post(
            reverse('accounts:upload'),
            {'image': constants.PROFILE_PIC_WRONG_FILETYPE})

        self.assertEqual(200, response.status_code)
        error_message = 'Upload a valid image. The file you uploaded was \
                        either not an image or a corrupted image.'
        self.assertFormError(response, 'form', 'image', error_message)
