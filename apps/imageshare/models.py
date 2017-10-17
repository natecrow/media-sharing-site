import os

from django.contrib.auth.models import User
from django.db import models
from tagulous import models as tagulous_models


def get_image_path(instance, filename):
    return os.path.join('user', str(instance.user.id), filename)


class ImageTag(tagulous_models.TagModel):
    class TagMeta:
        force_lowercase = True
        # autocomplete_view = 'tags_autocomplete'


class MediaFile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='images')
    uploaded_date = models.DateTimeField(
        null=False, blank=False, auto_now_add=True)

    class Meta:
        abstract = True


class Image(MediaFile):
    image = models.ImageField(upload_to=get_image_path)
    tags = tagulous_models.TagField(to=ImageTag)

    def __str__(self):
        return str(self.image.name)
