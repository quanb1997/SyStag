from django.db import models
from django.contrib.auth.base_user import BaseUserManager


# Tristan: custom manager class for managing our custom user
# we may want to re add the **extra_fields at some point if we extend our user model
class SystagUserManager(BaseUserManager):

    # Tristan: reused this code from UserManager from django:
    # https://github.com/django/django/blob/master/django/contrib/auth/models.py
    def _create_user(self, username, password):
        """
        Create and save a user with the given username and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None):
        return self._create_user(username, password)

    def create_superuser(self, username, password=None):
        return self._create_user(username, password)