from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=10, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"



