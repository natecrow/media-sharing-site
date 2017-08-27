from django.conf.urls import url

from .views import ImageUploadView


app_name = 'imageshare'
urlpatterns = [
    url(r'^upload-images$',
        ImageUploadView.as_view(), name='upload_images'),
]
