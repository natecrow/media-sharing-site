from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse

from . import constants
from .. import views
from ..models import Image


class TestImageUploadView(TestCase):

    def setUp(self):
        # create test user
        self.test_user = User.objects.create_user(
            username=constants.VALID_USERNAME,
            password=constants.VALID_PASSWORD,
            email=constants.VALID_EMAIL,
        )
        self.test_user.is_active = True
        self.test_user.save()

    def tearDown(self):
        User.objects.get(id=self.test_user.id).delete()

    def test_upload_images_page_redirects_to_login_page_when_not_logged_in_GET(self):
        response = self.client.get(reverse('upload_images'))
        expected_last_url = reverse(
            'accounts:login') + '?next=' + reverse('upload_images')
        self.assertRedirects(response, expected_last_url)

    def test_upload_images_page_redirects_to_login_page_when_not_logged_in_POST(self):
        response = self.client.post(reverse('upload_images'), {
                                    'image': constants.VALID_IMAGE})
        expected_last_url = reverse(
            'accounts:login') + '?next=' + reverse('upload_images')
        self.assertRedirects(response, expected_last_url)

    def test_upload_images_page_loads(self):
        self.client.login(username=constants.VALID_USERNAME,
                          password=constants.VALID_PASSWORD)
        response = self.client.get(reverse('upload_images'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Image:')
        self.assertContains(response, 'Tags:')

    def test_upload_images_valid_image(self):
        # TODO: fix this test
        pass
        # self.client.login(username=constants.VALID_USERNAME,
        #                   password=constants.VALID_PASSWORD)

        # response = self.client.post(reverse('upload_images'),
        #                             {'image': constants.VALID_IMAGE},
        #                             follow=True)

        # # expected_last_url = self.test_user.profile.get_absolute_url()
        # # self.assertRedirects(response, expected_last_url)

        # # Assert that image was uploaded
        # uploaded_image = get_object_or_404(Image, image=constants.VALID_EMAIL)
        # self.assertEquals(uploaded_image, constants.VALID_IMAGE)

    def test_upload_images_wrong_file_type(self):
        self.client.login(username=constants.VALID_USERNAME,
                          password=constants.VALID_PASSWORD)

        response = self.client.post(reverse('upload_images'),
                                    {'image': constants.TEXT_FILE},
                                    follow=True)

        # Assert that we stay on same page
        self.assertEqual(response.status_code, 200)

        # Assert that image was not uploaded
        self.assertRaises(Image.DoesNotExist, Image.objects.get,
                          image=constants.TEXT_FILE)
