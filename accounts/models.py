from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True)
    
    class Sexes(Enum):
        male = 0
        female = 1
        other = 2
    sex = models.SmallIntegerField(choices=[(s.value, s.name) for s in Sexes], blank=True, null=True)
    
    def __str__(self):
        return self.name or str(self.user)
    
