from django.apps import apps
from django.test import TestCase

from ..apps import DirectoryConfig


class DirectoryConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(DirectoryConfig.name, 'directory')
        self.assertEqual(apps.get_app_config(
            'directory').verbose_name, 'Directory')
