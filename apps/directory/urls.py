from django.conf.urls import url

from . import views


app_name = 'directory'
urlpatterns = [
    url(r'^$', views.profiles_directory, name='profiles_directory'),
]
