from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


app_name = 'accounts'
urlpatterns = [
    url(r'^login$', auth_views.login, {
        'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout$', auth_views.logout, {
        'template_name': 'accounts/logged_out.html'}, name='logout'),
    url(r'^signup$', views.signup, name='signup'),

    url(r'^users/(?P<username>[a-zA-Z0-9]+)$',
        views.profile_page, name='profile_page'),
    url(r'^profile-redirect/$', views.profile_redirect, name='profile_redirect'),
    url(r'^edit-profile$', views.edit_profile, name='edit_profile'),
    url(r'^upload-profile-picture$', views.change_profile_picture,
        name='change_profile_picture'),
]
