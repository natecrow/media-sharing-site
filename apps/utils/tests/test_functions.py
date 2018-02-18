from django.test import TestCase

from ..functions import determine_page_numbers


class TestDeterminePageNumbers(TestCase):

    def test_determine_page_numbers_with_standard_parameters(self):
        # [middle_number, max_numbers_per_side, total_numbers,
        # expected list of numbers]
        params = [
            [1, 3, 10, [1, 2, 3, 4]],
            [2, 3, 10, [1, 2, 3, 4, 5]],
            [3, 3, 10, [1, 2, 3, 4, 5, 6]],
            [4, 3, 10, [1, 2, 3, 4, 5, 6, 7]],
            [5, 3, 10, [2, 3, 4, 5, 6, 7, 8]],
            [6, 3, 10, [3, 4, 5, 6, 7, 8, 9]],
            [7, 3, 10, [4, 5, 6, 7, 8, 9, 10]],
            [8, 3, 10, [5, 6, 7, 8, 9, 10]],
            [9, 3, 10, [6, 7, 8, 9, 10]],
            [10, 3, 10, [7, 8, 9, 10]],
            [1, 3, 1, [1]],
        ]
        for middle_number, max_numbers_per_side, total_numbers, expected_list_of_numbers in params:
            actual_list_of_numbers = determine_page_numbers(
                middle_number, max_numbers_per_side, total_numbers)
            self.assertEqual(actual_list_of_numbers, expected_list_of_numbers)

    def test_determine_page_numbers_with_middle_number_as_0(self):
        with self.assertRaisesRegex(AssertionError,
                                    'Middle number 0 is outside the allowed range'):
            determine_page_numbers(0, 3, 10)

    def test_determine_page_numbers_with_negative_middle_number(self):
        with self.assertRaisesRegex(AssertionError,
                                    'Middle number -1 is outside the allowed range'):
            determine_page_numbers(-1, 3, 10)

    def test_determine_page_numbers_with_middle_number_higher_than_total_numbers(self):
        with self.assertRaisesRegex(AssertionError,
                                    'Middle number 11 is outside the allowed range'):
            determine_page_numbers(11, 3, 10)

    def test_determine_page_numbers_with_0_max_numbers_per_side(self):
        # [middle_number, max_numbers_per_side, total_numbers,
        # expected list of numbers]
        params = [
            [1, 0, 3, [1]],
            [2, 0, 3, [2]],
            [3, 0, 3, [3]],
        ]
        for middle_number, max_numbers_per_side, total_numbers, expected_list_of_numbers in params:
            actual_list_of_numbers = determine_page_numbers(
                middle_number, max_numbers_per_side, total_numbers)
            self.assertEqual(actual_list_of_numbers, expected_list_of_numbers)

    def test_determine_page_numbers_with_negative_max_numbers_per_side(self):
        with self.assertRaisesRegex(AssertionError,
                                    'Max numbers per side -1 is not 0 or higher'):
            determine_page_numbers(5, -1, 10)

    def test_determine_page_numbers_with_0_total_numbers(self):
        with self.assertRaisesRegex(AssertionError,
                                    'Total numbers 0 is not 1 or more'):
            determine_page_numbers(5, 3, 0)

    def test_determine_page_numbers_with_negative_total_numbers(self):
        with self.assertRaisesRegex(AssertionError,
                                    'Total numbers -1 is not 1 or more'):
            determine_page_numbers(5, 3, -1)
