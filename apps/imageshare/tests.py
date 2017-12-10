import os

import PIL.Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.six import BytesIO

from .models import Image


def create_image(size=(800, 600), image_mode='RGB', image_format='JPEG'):
    data = BytesIO()
    PIL.Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    return data


# valid data
VALID_FIRST_NAME = 'john'
VALID_LAST_NAME = 'doe'
VALID_EMAIL = 'johndoe@test.com'
VALID_USERNAME = 'johndoe'
VALID_PASSWORD = 'password123'
TEST_IMAGE_FILE = SimpleUploadedFile('test.png', create_image().getvalue())


class TestImage(TestCase):
    def setUp(self):
        # create test user
        self.credentials = {'username': VALID_USERNAME,
                            'password': VALID_PASSWORD}
        self.test_user = User.objects.create_user(
            first_name=VALID_FIRST_NAME,
            last_name=VALID_LAST_NAME,
            email=VALID_EMAIL,
            **self.credentials
        )
        self.test_user.is_active = True
        self.test_user.save()

    def tearDown(self):
        User.objects.get(username=VALID_USERNAME).delete()

    def test_auto_delete_image_on_delete(self):
        test_image = Image.objects.create(
            image=TEST_IMAGE_FILE, tags='test', user=self.test_user)
        test_image_path = test_image.image.path
        test_image.delete()

        self.assertFalse(os.path.isfile(test_image_path))
