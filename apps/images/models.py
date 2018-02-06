import os

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from tagulous import models as tagulous_models


def get_image_path(instance, filename):
    return os.path.join('user', str(instance.id), filename)


# Workaround to prevent naming error from tagulous
class ImageTag(tagulous_models.TagModel):
    class TagMeta:
        space_delimiter = False


class MediaFile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='images')
    uploaded_date = models.DateTimeField(
        null=False, blank=False, auto_now_add=True)

    class Meta:
        abstract = True


class Image(MediaFile):
    image = models.ImageField(upload_to=get_image_path)
    tags = tagulous_models.TagField(to=ImageTag, blank=True)

    def get_absolute_url(self):
        return reverse('view_image', args=[str(self.id)])

    def __str__(self):
        return str(self.image.name)


@receiver(models.signals.post_delete, sender=Image)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """
    Deletes image file from filesystem
    when corresponding `Image` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
