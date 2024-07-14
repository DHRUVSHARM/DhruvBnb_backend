from typing import Any
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models

# Create your models here.


# this is a custom user model to manage user related data
class CustomUserManager(UserManager):
    def _create_user(
        self,
        username: str,
        email: str | None = ...,
        password: str | None = ...,
        **extra_fields: Any
    ) -> Any:
        # in this function we will set the model for the user , we will sve the email and username among other fields
        if not email:
            raise ValueError("valid email not specified ")

        email = self.normalize_email(email)
        user = self.model(email=email, name=username, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_user(
        self,
        username: str,
        email: str | None,
        password: str | None,
        **extra_fields: Any
    ) -> Any:
        # this fn is used to create a general user
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(
        self,
        username: str,
        email: str | None,
        password: str | None,
        **extra_fields: Any
    ) -> Any:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to="uploads/avatars")

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = [
        "name",
    ]
