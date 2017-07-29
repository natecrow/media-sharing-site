from django.conf.urls import url

from . import views


app_name = 'social'
urlpatterns = [
    url(r'^directory$', views.profiles_directory, name='profiles_directory'),
]
