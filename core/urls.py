from django.conf.urls import url

from . import views


app_name = 'core'
urlpatterns = [
    url(r'^upload$', views.model_form_upload, name='upload'),
]
