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
            reverse('accounts:signup'), valid_data, follow=True)

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
        test_user.save()

        response = self.client.post(
            reverse('accounts:login'), credentials, follow=True)

        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())

        expected_last_url = reverse('accounts:profile_page',
                                    kwargs={'username': constants.VALID_USERNAME})
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

    def test_calculate_age_with_invalid_input(self):
        self.assertRaises(AssertionError, views.calculate_age,
                          date(2017, 8, 14), date(1993, 12, 4))
