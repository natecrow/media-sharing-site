from django.conf.urls import url

from . import views


app_name = 'social'
urlpatterns = [
    url(r'^$', views.profiles_directory, name='profiles_directory'),
    url(r'^(?P<username>[a-zA-Z0-9]+)$',
        views.profile_page, name='profile_page'),
]
