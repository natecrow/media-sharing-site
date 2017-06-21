from django.core.urlresolvers import reverse
from django.test import TestCase
from django.urls.base import resolve

from core import views


class ViewTests(TestCase):
     
    def test_upload_url_resolves_to_upload_view(self):
        found = resolve('/core/upload')
        self.assertEqual(found.func, views.simple_upload)
    