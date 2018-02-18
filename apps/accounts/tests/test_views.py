from datetime import date

from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from . import constants
from .. import views
from ..forms import SignUpForm


class TestSignup(TestCase):

    def test_signup_page_loads(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Signup')

    def test_redirect_to_login_page_after_signing_up(self):
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

        response = self.client.post(
            reverse('accounts:signup'), data=valid_data, follow=True)

        expected_last_url = reverse('accounts:login')
        self.assertRedirects(response, expected_last_url)


class TestLogin(TestCase):

    def test_login_page_loads(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_login_and_redirect_to_profile_page(self):
        # Create a user
        credentials = {'username': constants.VALID_USERNAME,
                       'password': constants.VALID_PASSWORD}
        test_user = User.objects.create_user(
            first_name=constants.VALID_FIRST_NAME,
            last_name=constants.VALID_LAST_NAME,
            **credentials
        )

        response = self.client.post(
            reverse('accounts:login'), credentials, follow=True)

        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())

        expected_last_url = user.profile.get_absolute_url()
        self.assertRedirects(response, expected_last_url)


class TestEditProfile(TestCase):

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
        User.objects.get(id=self.test_user.id).delete()

    def test_edit_profile_page_redirects_to_login_page_when_not_logged_in(self):
        response = self.client.get(reverse('accounts:edit_profile'))
        expected_last_url = reverse(
            'accounts:login') + '?next=' + reverse('accounts:edit_profile')
        self.assertRedirects(response, expected_last_url)

    def test_edit_profile_page_loads(self):
        self.client.login(username=constants.VALID_USERNAME,
                          password=constants.VALID_PASSWORD)
        response = self.client.get(reverse('accounts:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Profile')
        self.assertContains(response, 'Change profile picture')
        self.assertContains(response, 'First name')
        self.assertContains(response, 'Last name')
        self.assertContains(response, 'Email')
        self.assertContains(response, 'Location')
        self.assertContains(response, 'Gender')

    def test_edit_profile_positive(self):
        self.client.login(username=constants.VALID_USERNAME,
                          password=constants.VALID_PASSWORD)

        updated_first_name = 'Jane'
        updated_last_name = 'Dough'
        updated_email = 'jane.dough@test.com'
        updated_gender = 'f'
        updated_location = 'Testlandia'
        valid_data = {
            'first_name': updated_first_name,
            'last_name': updated_last_name,
            'email': updated_email,
            'gender': updated_gender,
            'location': updated_location,
        }

        response = self.client.post(reverse('accounts:edit_profile'),
                                    data=valid_data, follow=True)

        expected_last_url = self.test_user.profile.get_absolute_url()
        self.assertRedirects(response, expected_last_url)

        # Assert that user profile info was updated correctly
        updated_user = User.objects.get(id=self.test_user.id)
        self.assertEqual(updated_user.email, updated_email)
        self.assertEqual(updated_user.first_name, updated_first_name)
        self.assertEqual(updated_user.last_name, updated_last_name)
        self.assertEqual(updated_user.profile.gender, updated_gender)
        self.assertEqual(updated_user.profile.location, updated_location)

    def test_edit_profile_negative(self):
        """
        Try to update profile with invalid email address.
        """
        self.client.login(username=constants.VALID_USERNAME,
                          password=constants.VALID_PASSWORD)

        invalid_data = {'email': constants.INVALID_EMAIL}

        response = self.client.post(
            reverse('accounts:edit_profile'), data=invalid_data)

        # Assert that we stay on edit profile page
        self.assertEqual(response.status_code, 200)

        # Assert that user profile info was NOT updated
        updated_user = User.objects.get(id=self.test_user.id)
        self.assertNotEqual(updated_user.email, constants.INVALID_EMAIL)


class TestChangeProfilePicture(TestCase):

    def setUp(self):
        # create test user
        self.credentials = {'username': constants.VALID_USERNAME,
                            'password': constants.VALID_PASSWORD}
        self.test_user = User.objects.create_user(
            email=constants.VALID_EMAIL,
            **self.credentials
        )
        self.test_user.is_active = True
        self.test_user.save()

    def tearDown(self):
        User.objects.get(id=self.test_user.id).delete()

    def test_change_profile_picture_page_redirects_to_login_page_when_not_logged_in(self):
        response = self.client.post(
            reverse('accounts:change_profile_picture'),
            {'profile_picture': constants.VALID_PROFILE_PIC})

        expected_last_url = reverse(
            'accounts:login') + '?next=' + reverse('accounts:change_profile_picture')
        self.assertRedirects(response, expected_last_url)

    def test_change_profile_picture_page_loads(self):
        self.client.login(username=constants.VALID_USERNAME,
                          password=constants.VALID_PASSWORD)
        response = self.client.get(reverse('accounts:change_profile_picture'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile picture:')
        self.assertContains(response, 'Return to profile')

    def test_change_profile_picture_positive(self):
        # TODO: fix this test
        pass
        # self.client.login(username=constants.VALID_USERNAME,
        #                   password=constants.VALID_PASSWORD)

        # response = self.client.post(reverse('accounts:change_profile_picture'),
        #                             {'profile_picture': constants.VALID_PROFILE_PIC},
        #                              follow=True)

        # print('Size of profile picture in test: ', constants.VALID_PROFILE_PIC.size)
        # # print('\n\nResponse content: ' + response.content.decode())

        # expected_last_url = self.test_user.profile.get_absolute_url()
        # self.assertRedirects(response, expected_last_url)

        # # Assert that profile picture was changed
        # updated_user = User.objects.get(id=self.test_user.id)
        # self.assertEqual(updated_user.profile.profile_picture,
        #                  constants.VALID_PROFILE_PIC)

    def test_change_profile_picture_negative(self):
        self.client.login(username=constants.VALID_USERNAME,
                          password=constants.VALID_PASSWORD)

        response = self.client.post(reverse('accounts:change_profile_picture'),
                                    {'profile_picture': constants.TEXT_FILE},
                                    follow=True)

        # Assert that we stay on change profile picture page
        self.assertEqual(response.status_code, 200)

        # Assert that user profile picture was NOT updated
        updated_user = User.objects.get(id=self.test_user.id)
        self.assertNotEqual(
            updated_user.profile.profile_picture, constants.TEXT_FILE)


class TestProfilePage(TestCase):

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
        self.test_user.profile.gender = constants.VALID_GENDER
        self.test_user.profile.location = constants.VALID_LOCATION

    def test_profile_page_loads_positive(self):
        """
        Test that profile page renders for a given user and that public info
        is displayed while private info is not.
        """
        self.test_user.profile.birth_date = constants.VALID_BIRTH_DATE
        self.test_user.save()
        response = self.client.get(self.test_user.profile.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        # Info that should be displayed
        self.assertContains(response, constants.VALID_USERNAME)
        self.assertContains(response, constants.VALID_FIRST_NAME)
        self.assertContains(response, constants.VALID_LAST_NAME)
        self.assertContains(response, constants.VALID_GENDER)
        self.assertContains(response, constants.VALID_LOCATION)
        self.assertContains(response, 'Age:')

        # Info that shouldn't be displayed
        self.assertNotContains(response, constants.VALID_EMAIL)
        self.assertNotContains(response, constants.VALID_PASSWORD)

        # tear down
        User.objects.get(id=self.test_user.id).delete()

    def test_age_is_unknown_when_user_has_not_given_birth_date(self):
        response = self.client.get(self.test_user.profile.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, 'Age:')


class TestAgeCalculation(TestCase):

    def test_calculate_age_with_valid_input(self):
        # [from_date, to_date, expected_age]
        params = [
            [date(1993, 12, 4), date(2017, 8, 11), 23],
            [date(1993, 12, 4), date(2017, 12, 25), 24],
            [date(1993, 12, 4), date(2017, 12, 4), 24],
        ]

        for from_date, to_date, expected_age in params:
            with self.subTest(from_date=str(from_date), to_date=str(to_date)):
                age = views.calculate_age(from_date, to_date)
                self.assertEqual(age, expected_age,
                                 'Actual age is not the expected age')

    def test_calculate_age_with_switched_dates(self):
        with self.assertRaisesRegex(AssertionError, 'from_date 2017-08-14 comes after the to_date 1993-12-04'):
            views.calculate_age(date(2017, 8, 14), date(1993, 12, 4))

    def test_calculate_age_with_invalid_type_from_date(self):
        with self.assertRaisesRegex(AssertionError, 'from_date 12.12.1985 is not a date'):
            views.calculate_age(
                constants.INVALID_BIRTH_DATE, date(1993, 12, 4))

    def test_calculate_age_with_invalid_type_to_date(self):
        with self.assertRaisesRegex(AssertionError, 'to_date 12.12.1985 is not a date'):
            views.calculate_age(date(2017, 8, 14),
                                constants.INVALID_BIRTH_DATE)
