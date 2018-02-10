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


class TestImages(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(
            username=constants.VALID_USERNAME,
            password=constants.VALID_PASSWORD,
            email=constants.VALID_EMAIL
        )

    def test_no_images_to_display(self):
        response = self.client.get(reverse('images'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Images')
        self.assertContains(response, 'There are no images to display.')

        self.assertContains(response, 'Tags')
        self.assertContains(response, 'There are no tags to display.')

    def test_show_all_images_no_tags(self):
        # Create images without tags
        test_image_1 = Image.objects.create(
            image=constants.VALID_IMAGE,
            user=self.test_user
        )
        test_image_2 = Image.objects.create(
            image=constants.VALID_IMAGE,
            user=self.test_user
        )

        response = self.client.get(reverse('images'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Images')

        # Check that no tags message is shown
        self.assertContains(response, 'Tags')
        self.assertContains(response, 'There are no tags to display.')

        # Check that test image 1 is on page
        self.assertContains(response, '<a href="/media/' +
                            test_image_1.image.name + '"')
        self.assertContains(response, '<img src="/media/' +
                            test_image_1.image.name + '"')

        # Check that test image 2 is on page
        self.assertContains(response, '<a href="/media/' +
                            test_image_2.image.name + '"')
        self.assertContains(response, '<img src="/media/' +
                            test_image_2.image.name + '"')

        # Check that test user is shown on page as uploader
        self.assertContains(response, 'Uploader:')
        self.assertContains(response, '<a href="' +
                            self.test_user.profile.get_absolute_url() + '"')

    def test_show_all_images(self):
        # Create images with tags
        test_image_1 = Image.objects.create(
            image=constants.VALID_IMAGE,
            user=self.test_user,
            tags=['abc']
        )
        test_image_2 = Image.objects.create(
            image=constants.VALID_IMAGE,
            user=self.test_user,
            tags=['abc', 'def']
        )

        response = self.client.get(reverse('images'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Images')

        # Check that tag links are on page
        self.assertContains(response, 'Tags')
        self.assertContains(response, '<a href="/images/?tag=abc">')
        self.assertContains(response, '<a href="/images/?tag=def">')

        # Check that test image 1 is on page
        self.assertContains(response, '<a href="/media/' +
                            test_image_1.image.name + '"')
        self.assertContains(response, '<img src="/media/' +
                            test_image_1.image.name + '"')

        # Check that test image 2 is on page
        self.assertContains(response, '<a href="/media/' +
                            test_image_2.image.name + '"')
        self.assertContains(response, '<img src="/media/' +
                            test_image_2.image.name + '"')

        # Check that test user is shown on page as uploader
        self.assertContains(response, 'Uploader:')
        self.assertContains(response, '<a href="' +
                            self.test_user.profile.get_absolute_url() + '"')

    def test_show_images_by_tag(self):
        # Create images with tags
        test_image_1 = Image.objects.create(
            image=constants.VALID_IMAGE,
            user=self.test_user,
            tags=['abc']
        )
        test_image_2 = Image.objects.create(
            image=constants.VALID_IMAGE,
            user=self.test_user,
            tags=['abc', 'def']
        )
        test_image_3 = Image.objects.create(
            image=constants.VALID_IMAGE,
            user=self.test_user,
            tags=['abc', 'def', 'ghi']
        )

        response = self.client.get(reverse('images') + '?tag=def')

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Images')

        # Check that selected tags are displayed and don't have links
        self.assertContains(response, 'Tags')
        self.assertContains(response, '<a href="/images/?page=1">clear all</a>')
        self.assertContains(response, 'selected:\n      \n        def')
        self.assertNotContains(response, '<a href="/images/?tag=def">')

        # Check that links for additional tags are shown
        self.assertContains(response, '<a href="/images/?tag=abc&tag=def">')
        self.assertContains(response, '<a href="/images/?tag=ghi&tag=def">')

        # Check that test image 1 is NOT on page
        self.assertNotContains(response, '<a href="/media/' +
                            test_image_1.image.name + '"')
        self.assertNotContains(response, '<img src="/media/' +
                            test_image_1.image.name + '"')

        # Check that test image 2 is on page
        self.assertContains(response, '<a href="/media/' +
                            test_image_2.image.name + '"')
        self.assertContains(response, '<img src="/media/' +
                            test_image_2.image.name + '"')

        # Check that test image 3 is on page
        self.assertContains(response, '<a href="/media/' +
                            test_image_3.image.name + '"')
        self.assertContains(response, '<img src="/media/' +
                            test_image_3.image.name + '"')

        # Check that test user is shown on page as uploader
        self.assertContains(response, 'Uploader:')
        self.assertContains(response, '<a href="' +
                            self.test_user.profile.get_absolute_url() + '"')

    def test_show_images_by_multiple_tags(self):
        # Create images with tags
        test_image_1 = Image.objects.create(
            image=constants.VALID_IMAGE,
            user=self.test_user,
            tags=['abc']
        )
        test_image_2 = Image.objects.create(
            image=constants.VALID_IMAGE,
            user=self.test_user,
            tags=['abc', 'def']
        )
        test_image_3 = Image.objects.create(
            image=constants.VALID_IMAGE,
            user=self.test_user,
            tags=['abc', 'def', 'ghi']
        )

        response = self.client.get(reverse('images') + '?tag=def&tag=ghi')

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Images')

        # Check that selected tags are displayed and don't have links
        self.assertContains(response, 'Tags')
        self.assertContains(response, '<a href="/images/?page=1">clear all</a>')
        self.assertContains(response, 'selected:\n      \n        def\n      \n        ghi')
        self.assertNotContains(response, '<a href="/images/?tag=def&tag=ghi">')

        # Check that links for additional tags are shown
        self.assertContains(response, '<a href="/images/?tag=abc&tag=def&amp;tag=ghi">')

        # Check that test image 1 is NOT on page
        self.assertNotContains(response, '<a href="/media/' +
                            test_image_1.image.name + '"')
        self.assertNotContains(response, '<img src="/media/' +
                            test_image_1.image.name + '"')

        # Check that test image 2 is on page
        self.assertNotContains(response, '<a href="/media/' +
                            test_image_2.image.name + '"')
        self.assertNotContains(response, '<img src="/media/' +
                            test_image_2.image.name + '"')

        # Check that test image 3 is on page
        self.assertContains(response, '<a href="/media/' +
                            test_image_3.image.name + '"')
        self.assertContains(response, '<img src="/media/' +
                            test_image_3.image.name + '"')

        # Check that test user is shown on page as uploader
        self.assertContains(response, 'Uploader:')
        self.assertContains(response, '<a href="' +
                            self.test_user.profile.get_absolute_url() + '"')
