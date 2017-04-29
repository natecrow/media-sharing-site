from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True)
    
    class Genders(Enum):
        male = 'm'
        female = 'f'
    gender = models.CharField(max_length=1, choices=[(s.value, s.name) for s in Genders], blank=True)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    
    def __str__(self):
        return self.name or str(self.user)
    