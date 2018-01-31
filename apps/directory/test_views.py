from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import Profile
from apps.accounts.tests import constants


class TestProfilesDirectory(TestCase):

    def test_display_profiles(self):
        '''
        Create three users and check that their usernames and profile pictures
        are displayed on the page.
        Profile pictures are the default ones.
        TODO: It would be good to test with uploaded profile pictures, but the
        thumbnails are generated with random names by Sorl Thumbnail, so would
        need to figure out how to locate them and clear them from the cache
        when test finishes running, if possible.
        '''
        test_user_1 = User.objects.create_user(
            username='testuser1',
            password='password123',
            email='testuser1@test.com'
        )
        test_user_2 = User.objects.create_user(
            username='testuser2',
            password='password123',
            email='testuser2@test.com'
        )
        test_user_3 = User.objects.create_user(
            username='testuser3',
            password='password123',
            email='testuser3@test.com'
        )

        response = self.client.get(reverse('directory:profiles_directory'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profiles')
        self.assertContains(response, test_user_1.username)
        self.assertContains(response, test_user_2.username)
        self.assertContains(response, test_user_3.username)
        self.assertContains(response, 'default_profile_pic.svg')

    def test_no_profiles_to_display(self):
        '''
        Should not display any profiles on the page when there are no users.
        '''
        response = self.client.get(reverse('directory:profiles_directory'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profiles')
        self.assertContains(response, 'There are no profiles to display.')
