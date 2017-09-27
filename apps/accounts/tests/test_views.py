from datetime import date

from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from . import constants
from .. import views


class TestViews(TestCase):

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
        User.objects.get(username=constants.VALID_USERNAME).delete()

    def test_redirect_to_profile_page_after_logging_in(self):
        response = self.client.post(
            reverse('accounts:login'), self.credentials, follow=True)

        user = auth.get_user(self.client)
        assert user.is_authenticated()
        last_url = response.request['PATH_INFO']
        expected_last_url = '/accounts/users/' + constants.VALID_USERNAME
        self.assertEqual(last_url, expected_last_url)


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
