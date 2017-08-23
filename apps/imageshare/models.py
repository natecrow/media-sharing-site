from django.contrib.auth.models import User
from django.db import models


class MediaFile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='images')

    class Meta:
        abstract = True


class Image(MediaFile):
    image = models.ImageField()
