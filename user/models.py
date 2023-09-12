from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=14)
    block = models.BooleanField(default=False)
    role = models.CharField(max_length=20, default="user")
    verification_code = models.PositiveIntegerField(default=0)


class Support(models.Model):
    user_fk = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    sanded_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    read = models.BooleanField(default=False, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    rasm = models.FileField(upload_to='categories/', blank=True, null=True)
