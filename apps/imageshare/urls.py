from django.conf.urls import url

from . import views


app_name = 'imageshare'
urlpatterns = [
    url(r'^upload-images$',
        views.ImageUploadView.as_view(), name='upload_images'),
    url(r'^Images$', views.images, name='images')
]
