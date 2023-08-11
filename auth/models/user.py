import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from core.mixins import TimeStampMixin
from ..managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimeStampMixin):
    """
    Our custom user model that extends Django's AbstractBaseUser."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=255, blank=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
