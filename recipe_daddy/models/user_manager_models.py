from django.db import models
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password=None):
        if not username:
            raise ValueError("User should have an username")
        if not email:
            raise ValueError("User should have an email")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password):
        if not password:
            raise ValueError("User should have a password")
        user = self.create_user(username, email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user