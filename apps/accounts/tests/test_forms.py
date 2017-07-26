from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from ..forms import ProfilePictureUploadForm, SignUpForm


class TestSignupForm(TestCase):

    def setUp(self):
        self.valid_data = {
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'email': 'test123@test.com',
            'username': 'test123',
            'password1': 'password123',
            'password2': 'password123',
            'birth_date': '1990-01-01',
            'gender': 'm',
            'location': 'somewhere',
        }

    def test_form_with_valid_data(self):
        data = self.valid_data
        form = SignUpForm(data, self.valid_data)
        self.assertTrue(form.is_valid())


class TestProfilePictureUploadForm(TestCase):

    def test_form_with_valid_data(self):
        picture = SimpleUploadedFile(
            name='test_image.jpg',
            content=b"file_content",
            content_type='image/jpeg')
        form = ProfilePictureUploadForm(picture)
        self.assertTrue(form.is_valid())
