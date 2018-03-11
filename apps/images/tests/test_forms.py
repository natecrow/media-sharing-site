from django.test import TestCase
from django.urls import reverse

from . import constants
from ..forms import ImageEditForm, ImageUploadForm


class TestImageUploadForm(TestCase):

    def test_form_with_one_image(self):
        form = ImageUploadForm(
            data={'tags': 'test black square'},
            files={'image': constants.VALID_IMAGE})
        self.assertTrue(form.is_valid())

    def test_form_with_multiple_images(self):
        form = ImageUploadForm(
            data={'tags': 'test black square'},
            files={'image': constants.VALID_IMAGE,
                   'image': constants.VALID_IMAGE})
        self.assertTrue(form.is_valid())

    def test_form_with_no_image(self):
        form = ImageUploadForm(files={})
        self.assertTrue(form.is_valid())

    def test_form_with_no_tags(self):
        form = ImageUploadForm(files={'image': constants.VALID_IMAGE})
        self.assertTrue(form.is_valid())

    def test_form_with_invalid_file_type(self):
        form = ImageUploadForm(
            files={'image': constants.TEXT_FILE})
        self.assertFalse(form.is_valid())


class TestImageEditForm(TestCase):

    def test_form_with_valid_tags(self):
        form = ImageEditForm(data={'tags': 'test 1 2 3'})
        self.assertTrue(form.is_valid())

    def test_form_with_no_tags(self):
        form = ImageEditForm(data={})
        self.assertTrue(form.is_valid())

    def test_form_with_empty_tags(self):
        form = ImageEditForm(data={'tags': ''})
        self.assertTrue(form.is_valid())
