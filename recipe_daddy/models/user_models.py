from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from . import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=300, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email