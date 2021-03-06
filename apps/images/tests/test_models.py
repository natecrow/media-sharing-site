import fnmatch
import os

from django.contrib.auth.models import User
from django.test import TestCase

from . import constants
from ..models import Image, get_image_path


class TestImage(TestCase):

    def setUp(self):
        self.credentials = {'username': constants.VALID_USERNAME,
                            'password': constants.VALID_PASSWORD}
        self.test_user = User.objects.create_user(
            first_name=constants.VALID_FIRST_NAME,
            last_name=constants.VALID_LAST_NAME,
            email=constants.VALID_EMAIL,
            **self.credentials
        )
        self.test_image = Image.objects.create(
            image=constants.VALID_IMAGE, user=self.test_user)

    def tearDown(self):
        Image.objects.get(id=self.test_image.id).delete()
        User.objects.get(id=self.test_user.id).delete()

    def test_get_absolute_url(self):
        expected_absolute_url = '/images/' + str(self.test_image.id)
        self.assertEqual(self.test_image.get_absolute_url(),
                         expected_absolute_url)

    def test_object_name_is_image_name(self):
        self.assertTrue(fnmatch.fnmatch(
            str(self.test_image), 'user/None/test_image_*.jpg'))


class TestImageAncillaryFunctions(TestCase):
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

    def tearDown(self):
        User.objects.get(id=self.test_user.id).delete()

    def test_get_image_path(self):
        expected_path = 'user/1/' + constants.VALID_IMAGE.name
        actual_path = get_image_path(
            self.test_user, constants.VALID_IMAGE.name)
        self.assertEqual(actual_path, expected_path)

    def test_auto_delete_image_on_delete(self):
        test_image = Image.objects.create(
            image=constants.VALID_IMAGE, tags='test', user=self.test_user)
        test_image_path = test_image.image.path
        test_image.delete()

        self.assertFalse(os.path.isfile(
            test_image_path), test_image_path +
            ' was not deleted when its Image model was deleted')
