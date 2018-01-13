from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^upload/$',
        views.ImageUploadView.as_view(), name='upload_images'),
    url(r'^$', views.images, name='images'),
    url(r'^categories/(?P<category>[a-zA-Z0-9]+)$',
        views.categories, name='images_by_category'),
    url(r'^(?P<image_id>[a-zA-Z0-9]+)$',
        views.view_image, name='view_image'),
]
