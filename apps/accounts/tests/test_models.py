import os

from django.contrib.auth.models import User
from django.test import TestCase

from . import constants
from ..models import get_image_path, Profile

class TestProfile(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(
            username=constants.VALID_USERNAME,
            password=constants.VALID_PASSWORD,
            first_name=constants.VALID_USERNAME,
            last_name=constants.VALID_LAST_NAME,
            email=constants.VALID_EMAIL)
        cls.test_user.profile.profile_picture = constants.VALID_PROFILE_PIC

    def test_location_max_length(self):
        max_length = self.test_user.profile._meta.get_field(
            'location').max_length
        self.assertEqual(max_length, 30)

    def test_profile_picture_upload_path(self):
        upload_to = self.test_user.profile._meta.get_field(
            'profile_picture').upload_to
        self.assertEqual(upload_to, get_image_path)

    def test_gender_max_length(self):
        max_length = self.test_user.profile._meta.get_field(
            'gender').max_length
        self.assertEqual(max_length, 1)

    def test_object_name_is_username(self):
        self.assertEqual(str(self.test_user), constants.VALID_USERNAME)

    def test_get_absolute_url(self):
        expected_absolute_url = '/accounts/users/' + constants.VALID_USERNAME
        self.assertEqual(self.test_user.profile.get_absolute_url(),
                         expected_absolute_url)


class TestProfileAncillaryFunctions(TestCase):

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

    def test_get_image_path(self):
        expected_path = 'user/1/' + constants.VALID_PROFILE_PIC.name
        actual_path = get_image_path(
            self.test_user, constants.VALID_PROFILE_PIC.name)
        self.assertEqual(actual_path, expected_path)

    def test_create_user_profile_when_user_is_created(self):
        self.assertTrue(self.test_user.profile,
                        'Profile was not created for ' + str(self.test_user))

    def test_save_user_profile_when_user_is_saved(self):
        # check that user's profile is saved when user is saved
        self.test_user.save()
        profile_from_db = User.objects.get(id=self.test_user.id).profile
        self.assertEqual(profile_from_db.location, constants.VALID_LOCATION)

        # check that user's profile is saved after updating it
        NEW_LOCATION = 'New Testland'
        self.test_user.profile.location = NEW_LOCATION
        self.test_user.save()
        profile_from_db = User.objects.get(id=self.test_user.id).profile
        self.assertEqual(profile_from_db.location, NEW_LOCATION)

    def test_do_not_save_user_profile_when_user_is_not_saved(self):
        # check that user's profile is not saved when user is not saved
        profile_from_db = User.objects.get(id=self.test_user.id).profile
        self.assertNotEqual(profile_from_db.location, constants.VALID_LOCATION)

        # check that user's profile is not saved when updated but user is not saved
        NEW_LOCATION = 'New Testland'
        self.test_user.profile.location = NEW_LOCATION
        profile_from_db = User.objects.get(id=self.test_user.id).profile
        self.assertNotEqual(profile_from_db.location, NEW_LOCATION)

    def test_auto_delete_file_on_delete(self):
        profile_picture_path = self.test_user.profile.profile_picture.path
        self.test_user.delete()
        self.assertFalse(os.path.isfile(profile_picture_path),
                         profile_picture_path + ' was not deleted when profile was deleted')
