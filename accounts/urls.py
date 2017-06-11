from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


app_name = 'accounts'
urlpatterns = [
    url(r'^profile$', views.profile, name='profile'),
    url(r'^login$', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout$', auth_views.logout, {'template_name': 'accounts/logged_out.html', 'next_page': 'login'}, name='logout'),
    url(r'^signup$', views.signup, name='signup'),
]
