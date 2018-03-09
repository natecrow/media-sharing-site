import os
from enum import Enum

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


def get_image_path(instance, filename):
    return os.path.join('user', str(instance.id), filename)


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True)
    profile_picture = models.ImageField(
        upload_to=get_image_path, blank=True, null=True)
    GENDERS = [
        ('M', 'male'),
        ('F', 'female')
    ]
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True)

    def get_absolute_url(self):
        return reverse('accounts:profile_page', args=[str(self.user.username)])

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    When a User is created, create a corresponding Profile for it.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    When a User is saved, save its corresponding Profile too.
    """
    instance.profile.save()


@receiver(models.signals.post_delete, sender=Profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes profile picture from filesystem
    when corresponding `Profile` object is deleted.
    """
    if instance.profile_picture:
        if os.path.isfile(instance.profile_picture.path):
            os.remove(instance.profile_picture.path)
