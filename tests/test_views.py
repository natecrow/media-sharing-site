from django.test import TestCase
from django.urls.base import resolve
#from django.views.generic import TemplateView


class TemplateViewTests(TestCase):

    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.view_name, 'homepage')
        