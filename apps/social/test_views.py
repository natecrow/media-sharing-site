from datetime import date

from django.test import TestCase

from . import views


class TestViews(TestCase):

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
