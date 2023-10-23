from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    password = models.CharField(
        verbose_name="password",
        max_length=128,
    )
    date_joined = models.DateTimeField(
        verbose_name="date joined",
        auto_now_add=True,
    )

    def __str__(self):
        return self.email
