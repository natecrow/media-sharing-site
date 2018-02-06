from django.apps import apps
from django.test import TestCase

from ..apps import ImagesConfig


class ImagesConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(ImagesConfig.name, 'images')
        self.assertEqual(apps.get_app_config(
            'images').verbose_name, 'Images')
