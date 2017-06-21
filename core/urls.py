from django.conf.urls import url

from . import views


app_name = 'core'
urlpatterns = [
    url(r'^upload$', views.simple_upload, name='upload'),
]
