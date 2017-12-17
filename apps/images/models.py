import os

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from tagulous import models as tagulous_models


def get_image_path(instance, filename):
    return os.path.join('user', str(instance.user.id), filename)


# Workaround to prevent naming error from tagulous
class ImageTag(tagulous_models.TagModel):
    pass


class MediaFile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='images')
    uploaded_date = models.DateTimeField(
        null=False, blank=False, auto_now_add=True)
    CATEGORIES = [
        ('ABSTRACT', 'abstract'),
        ('ANIMALS', 'animals'),
        ('ARCHITECTURE', 'architecture'),
        ('FANTASY', 'fantasy'),
        ('FOOD', 'food'),
        ('HOLIDAYS', 'holidays'),
        ('MISC', 'misc'),
        ('MUSIC', 'music'),
        ('NATURE', 'nature'),
        ('SCI-FI', 'sci-fi'),
        ('SPACE', 'space'),
        ('SPORTS', 'sports'),
        ('VEHICLES', 'vehicles'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORIES, default='MISC')

    class Meta:
        abstract = True


class Image(MediaFile):
    image = models.ImageField(upload_to=get_image_path)
    tags = tagulous_models.TagField(to=ImageTag)
    COLORS = [
        ('RED', 'red'),
        ('ORANGE', 'orange'),
        ('YELLOW', 'yellow'),
        ('GREEN', 'green'),
        ('TEAL', 'teal'),
        ('BLUE', 'blue'),
        ('PURPLE', 'purple'),
        ('PINK', 'pink'),
        ('WHITE', 'white'),
        ('GRAY', 'gray'),
        ('BLACK', 'black'),
        ('BROWN', 'brown'),
    ]
    color = models.CharField(max_length=6, choices=COLORS, blank=True)

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