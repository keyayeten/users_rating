from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(
        verbose_name=('Логин'),
        max_length=50,
        unique=True,
    )
    password = models.CharField(
        verbose_name=('Пароль'),
        max_length=50
    )
