from django.conf.urls import url

from . import views


app_name = 'imageshare'
urlpatterns = [
    url(r'^upload-images$',
        views.ImageUploadView.as_view(), name='upload_images'),
    url(r'^images$', views.images, name='images'),
    url(r'^images/(?P<image_id>[a-zA-Z0-9]+)$', views.view_image, name='view_image'),
]
